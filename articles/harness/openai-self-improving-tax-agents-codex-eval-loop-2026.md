# OpenAI Tax AI 如何让 Codex 成为自优化的 Tax Agent——Eval Loop 工程机制全解

> 本文原发于 OpenAI Engineering Blog（2026-05-27），由 OpenAI 与 Thrive Holdings 联合开发，专注于用 Codex 构建自优化的 Tax AI 系统。  
> 原文：[Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/)

---

## 核心问题：生产环境的失败为什么总是「慢半拍」？

做 AI Agent 系统的人，几乎都会遇到一个经典困境：实验室环境表现良好，生产环境却频频崩溃，修复速度跟不上发现速度。

OpenAI 与 Thrive Holdings 在 Crete 地区 30+ 会计师事务所的真实场景中，遇到了同样的问题。在 Tax AI 产品上线后，他们需要处理 W-2、K-1、Schedule E 等各种复杂税表，每个错误可能来自提取失误、映射问题、产品不支持、税务判断，以及正常的工作流噪音——这些混在一起，让改进循环变得缓慢且昂贵。

**关键问题**：如何把生产环境中的真实反馈，变成可执行的工程任务？而不是每次都要工程师介入，手动翻译反馈？

---

## 核心解法：三段式闭环

OpenAI 的方案核心是一个三层闭环结构：

```
 practitioner's correction
        ↓
 production trace（结构化路径）
        ↓
   tailored evals（定制化评估）
        ↓
  Codex-driven iteration（Codex 驱动迭代）
```

这个循环的独特之处在于：**它不需要工程师来驱动每一次改进**。整个过程是半自动化的——Codex 会接收 eval 目标、调查根因、提出修复、运行验证，最后提交 PR。

---

## Eval Loop 的工程机制拆解

### 1. 评估器循环（Evaluator Loop）

这是 Harness Engineering 的核心机制。Codex 不只是被要求「去修复这个错误」，而是被给予了一个**有边界、有验证标准、有明确成功条件的任务环境**。

关键要素：
- **Bounded Task**：任务范围被精确限制，例如「修复租金收入提取中遗漏的 fair rental days 字段」
- **Completion Criteria**：有明确的评估指标，例如「fair rental days 字段准确率从 X% 提升到 Y%」
- **Stop Condition**：有明确的停止条件，不是无限重试

```yaml
# 评估套件结构示例
datasets/fair-rental-days.yaml   # 代表性测试数据集
suites/fair-rental-days.yaml    # 目标评估套件
suites/rental-income-regression.yaml  # 回归评估
grader/rental-income.yaml       # 评分器
```

### 2. 生产 Trace（Production Trace）

生产 trace 是 OpenAI 这套系统的第二层核心机制。它不是简单的输入输出日志，而是**从源文件到最终提交的完整路径记录**。

```
源文件 → 字段提取（含溯源）→ 映射到税务引擎 → 从业者修正 → 最终申报
```

这套 trace 体系让「发现错误」变得可定位：当系统报告错误时，可以精确定位到是提取环节、映射环节、还是从业者修正环节出了问题。

### 3. 接力机制（Context Handover）

Codex 在处理一个任务时，接收到的上下文结构如下：

```
repo/ (codex/fix-rental-0042 branch)
├── AGENTS.md
├── tasks/FIND-RENTAL-0042/
│   ├── task.yaml          # 任务定义
│   ├── EXEC_PLAN.md       # 执行计划
│   └── RESULTS.md         # 执行结果
├── app/tax-ai/rental-income/
│   ├── agent.ts           # Agent 代码
│   ├── schema.ts          # 提取 schema
│   ├── provenance.ts      # 溯源逻辑
│   └── mapper.ts         # 映射逻辑
├── evals/                 # 目标 + 回归评估套件
├── skills/                # 可复用技能（eval-runner 等）
├── docs/                  # 架构文档
└── scoped-tools/          # 受限工具集
    ├── production-trace   # 生产 trace（只读）
    ├── source-artifacts   # 源文件（只读）
    └── tax-engine-docs    # 税务引擎文档（只读）
```

**接力设计的精妙之处**：Codex 的可写工作区（worktree）和生产上下文（scoped-tools）是严格分离的。Codex 只能修改 `app/tax-ai/` 下的文件，但只能读取 production-trace、source-artifacts 和 tax-engine-docs。这种**写边界控制**是 Harness 机制的重要组成部分。

---

## 三段式 Loop 的实际执行流程

### 第一段：从 Practitioner Correction 到 Structured Finding

当从业者在系统中修正一个提取值时，修正被自动记录为结构化数据：

```json
{
  "tax_ai_proposed": "rental_income: $12,400",
  "practitioner_modified": "rental_income: $13,100",
  "filed_return_value": "$13,100"
}
```

这些修正数据经过聚类分析后，重复出现的模式成为「可行动的发现」：

- fair rental days 字段频繁被遗漏
- "other expenses" 字段处理错误
- 同一源包中的多个租赁物业被混淆

### 第二段：从 Structured Finding 到 Eval Target

每个可行动的发现被转化为：

1. **Capture the difference**：对比 Tax AI 输出与申报值，生成字段级审查行
2. **Group related failures**：将相似审查行分组，分离重复性产品失败与正常噪音
3. **Turn repeated patterns into eval targets**：将审查后的发现变成 Codex 可执行的任务目标

### 第三段：从 Eval Target 到 Codex-Scoped Engineering Task

这是整个循环最关键的一步。Codex 接收到的任务包包含：

- **Targeted Eval Set**：代表性源文件和预期输出
- **Trace**：完整的产品路径记录
- **Repo**：可修改的产品代码
- **Skills**：如何运行 eval 的技能文档

Codex 的工作流程：

```
1. Investigate：检查提取 schema、mapper 行为、代码路径，确定根因
2. Implement：修复 schema、改进源选择、更新 mapper、或修正 grader
3. Validate：运行目标评估 + 回归评估，生成候选 PR
4. Close the loop：如果证据模糊或无法安全自动化，则路由回产品团队
```

---

## 为什么这个模式有效？

### 1. 有边界的任务，而非模糊的改进

传统的 Agent 系统改造循环通常是：**发现问题 → 手动描述 → 手动修复 → 验证**。这种方式的问题在于：描述问题和验证解决都需要人工介入。

OpenAI 的做法是把「描述」自动化：通过结构化的 trace 和 eval 体系，让问题的描述本身就变成了可执行的任务包。Codex 拿到的是一个**有明确成功标准的任务**，而不是「请修复这个 bug」。

### 2. 从「我修了什么」到「系统学到了什么」

大多数 Agent 系统的改进循环是离散的——修复了就结束了。但 OpenAI 的三段式闭环把每一次修正都沉淀为系统的学习：

- 从业者的修正 → 结构性发现 → Eval 目标 → Codex 任务 → 新的生产 evidence
- 新的生产 evidence → 下一轮循环的输入

这种模式让系统越往后越强，因为每一次真实的税务申报修正都在教系统变得更好。

### 3. 人仍然在回路中，但只在正确的地方

Codex 不是全自动的。对于**证据模糊或涉及税务判断**的情况，Case 会被路由回工程师或产品团队。人在回路中的位置是**边界决策者**，而不是每一次修复的执行者。

---

## 工程实践的关键设计原则

### 原则 1：Eval 是 first-class citizen

评估不是事后的 QA，而是驱动开发的核心信号。在这套体系里，**每个产品功能都有一个对应的 eval 套件**，而这个套件直接从生产数据中生成。

### 原则 2：上下文必须分层，而非堆砌

Codex 的 context 是稀缺资源。如果给一个 Agent 1000 页的指令手册，它要么错过关键约束，要么开始优化错误的约束。

OpenAI 的设计是：**AGENTS.md 是目录，不是手册**。真正的知识存储在 `docs/` 目录中，按主题分类索引，机械验证其新鲜度和正确性。

### 原则 3：让生产环境自己「说话」

这套系统最聪明的地方在于：生产环境本身就是信号源。当从业者修正一个值时，他们不是在「反馈 bug」，而是在**生成训练数据**。系统把这些修正转化为结构化数据，再转化为 eval，再转化为 Codex 任务——整个链路是自动化的。

---

## 对 Harness Engineering 的启示

OpenAI 明确提到这个系统建立在两个先前工作的基础上：

1. **[Harness Engineering](https://openai.com/index/harness-engineering/)**：如何让任务对 Codex 可读、可执行、有验证
2. **[Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/)**：多 Agent 编排规范

Tax AI 系统的创新在于：**它把 production trace 和 eval system 直接对接**，让生产数据直接驱动开发循环。在 Harness Engineering 的框架里，这是一个完整的「评估器循环」（evaluator loop）的实现案例：

- 有外部验证源（从业者的修正）
- 有结构化的评估集（目标 + 回归）
- 有明确的成功条件（completion criteria）
- 有受控的修改边界（scoped-tools 只读隔离）
- 有自动化的循环关闭机制

---

## 笔者的判断

**这个系统的本质是一个生产驱动的自我优化引擎，而不是一个普通的错误修正流程。**

它解决的核心问题不只是「Tax AI 准确率提高了」，而是：**当真实的用户行为（从业者的修正）发生时，系统能不能把这个行为自动转化为系统的能力提升，而不需要工程师每一次都介入？**

这是一个很有启发性的设计思路。对于任何需要 Agent 长时间在生产环境中运行、并持续改进的场景——无论是代码生成、文档处理、还是多步骤工作流——这套「生产 Trace → Eval → Codex 任务」的闭环都值得参考。

关键不在于用什么模型，而在于**如何设计让反馈自动流动、让改进可累积**的工程机制。

---

> **引用来源**：
> - [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/)（OpenAI Engineering, 2026-05-27）
> - [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)（OpenAI Engineering, 2026-02-11）
> - [An open-source spec for Codex orchestration: Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/)（OpenAI Engineering, 2026-04-27）