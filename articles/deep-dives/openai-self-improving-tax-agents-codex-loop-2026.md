# 自进化 Agent 架构：一条可编程的改进回路

> 本文源自 OpenAI 与 Thrive Holdings 合作构建 Tax AI 的实践复盘，原文链接：[Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/)（2026-05-27）。结合 Loop Engineering 框架与 Harness Engineering 思想，对自进化 Agent 的工程化路径做系统梳理。

---

## 核心命题

**手动调优是 Agent 落地的最大瓶颈，而不是模型能力。**

大多数 Agent 团队在部署后会遇到一个熟悉的困境：系统在前几个月的表现还行，但改进速度越来越慢——每一次迭代都依赖工程师人工介入：找到问题、定位根因、修改提示词、等待下一轮测试。反馈回路掌握在人手里，不是掌握在系统手里。

OpenAI 与 Thrive Holdings 的合作案例给出了一个不同的答案：让 Agent 自己成为改进回路的驱动者。系统从"需要工程师推进才能变好"，转变为"只要生产环境在运行，就在持续变好"。

---

## 传统 Agent 改进回路的问题

在深入自进化架构之前，有必要先理解传统方案的局限性。

### 问题 1：反馈信号无法结构化

当 practitioners（领域专家）修正 Agent 输出时，这个修正行为包含丰富的信息——它不仅说明"这里错了"，还说明了"什么类型的错误"、"优先级如何"、"是否有系统性规律"。但传统系统只记录"最终正确答案"，中间的过程信息全部丢失。

### 问题 2：改进依赖人工介入

即便团队知道某个错误模式存在，将它转化为可修复的工程任务仍然需要：
1. 工程师识别错误模式
2. 判断是否值得修复
3. 定位代码路径
4. 编写修复代码
5. 验证修复有效

每一步都需要人工调度，整个回路不是自动化的。

### 问题 3：eval 与生产环境脱节

大多数团队在本地跑 eval，生产环境是完全不同的上下文。eval 通过了，但上线后效果差——这是因为 eval 没有吃到真实的 signal。

---

## 自进化架构：三支柱循环

Tax AI 的设计围绕三个支柱展开，每个支柱解决上述的一个核心问题：

### 支柱一：让 practitioners 成为 signal 源

领域专家的修正行为本身就是最高质量的 feedback signal。关键是**捕获修正的结构化信息，而不仅仅是修正结果**。

Tax AI 的做法是：每一次 practitioner 修正都被记录为一条 `review row`，包含：
- Agent 预测值
- Practitioner 修正后的值
- 最终上报值
- 错误类型分类（提取失误 / 映射错误 / 不支持的功能 / 工作流噪音）

这样一来，practitioners 的日常修正行为本身就变成了改进系统的原材料——**不需要工程师介入，signal 已经在产生**。

> 原文引用：*"Practitioners helped us discern those cases so we could identify which actions required a practitioner correction or blocked a submission. Because we could see these corrections in detail, we transformed the review process from a terminal, post-failure step into a continuous learning cycle."*

### 支柱二：生产追踪（Production Traces）

第二条支柱是**完整路径追踪**：不仅记录输入和输出，还记录从源文件到最终提交的完整路径。

对于 rental property 场景，这意味着追踪：
- 源文件读取过程（哪个文件被解析了）
- 字段提取（哪些字段从哪里提取，引用链是什么）
- 映射到 tax engine 的过程
- Practitioner 的最终修正
- 最终上报值

完整追踪的价值在于：当 eval 标记某个返回"错误"时，Codex 可以**直接定位到失败发生在哪个环节**——是提取层、映射层、还是 grader 层，而不是盲猜。

### 支柱三：Codex 驱动的改进循环

第三条支柱是**将 structured findings 直接转化为 Codex 的 scoped engineering task**。

这是整个回路的核心。流程如下：

```
 Practitioner 修正
        ↓
 捕获为 review row
        ↓
 聚类分析（找出重复模式）
        ↓
 重复出现的模式 → eval target
        ↓
 封装为 Codex scoped task
  (evidence + editable surface + eval gates)
        ↓
 Codex 调查根因并实现修复
        ↓
 运行 targeted + regression evals
        ↓
 候选 PR → 工程师 review → 合并
        ↓
 新版本发布 → 新一轮生产 signal
```

Codex 收到的不是模糊的"结果不好"，而是一个 bounded task，包含：

- **Production trace**：真实的生产证据（输入→输出→修正全链路）
- **Targeted eval set**：该错误模式的代表性测试集
- **Editable product surfaces**：可以直接修改的代码位置
- **Eval gates**：成功的明确定义（targeted + regression）

> 原文引用：*"The end-to-end self-improvement loop: production traces surface repeated field-level corrections, which become failure signals that Codex can inspect alongside the trace, evals, repo, and skills."*

---

## 实战案例：Rental Property 场景

以 Schedule E 中的 rental property 字段提取为例，走一遍完整循环：

**初始状态**：Tax AI 在 rental property 的 "fair rental days" 字段上持续出错，practitioners 每次都要手动修正。

### Step 1：Practitioner 修正揭示失败

系统捕获 practitioner 的修正行为。每一次修正产生一条 review row，记录：
- 预测值 vs 实际值
- 修正发生在哪个环节（提取 / 映射 / 提交）
- 是否为重复性错误

### Step 2：Review rows 聚类转化为 eval targets

系统将相似的 review rows 聚类：
- "fair rental days" 字段错误 → 重复出现 N 次
- 其他 rental property 字段错误模式 → 各自聚类

重复出现的模式被标记为 eval target，生成针对性的测试集。

### Step 3：Codex 执行 scoped engineering task

Codex 接收到的上下文包含：
1. 源文件包和 extraction schema
2. Mapper 行为和代码路径
3. Rental property 文档的 source selection 逻辑
4. Targeted eval + regression eval
5. 相关 skills/docs

Codex 调查后输出：
- 根因分析（"问题出在 source selection 对 rental property 文档的分类逻辑"）
- 修复方案（修改 source selection → 更新 extraction schema → 调整 grader）
- 验证结果（targeted eval 通过 + regression eval 无回归）

### 结果

从 initial state 到 production-ready，整个循环在 **6 周**内完成，且产出的抽象（review artifacts、eval conventions、implementation patterns）可以被复用到 Schedule C 和 Schedule A。

---

## 量化改进效果

这是该案例最有说服力的部分：**改进是可以被量化的**。

Tax AI 的核心指标是"返回无需后续修正的比例"（field completion rate）：

| 时间节点 | 75% 正确率 | 90% 正确率 | 100% 正确率 |
|---------|-----------|-----------|------------|
| 上线时 | 25% | - | - |
| 6 周后 | 86% | 快速提升 | 快速提升 |

更值得注意的是：**随着任务复杂度提升，每单位工作量节省的时间反而更多**。因为越复杂的任务（如 K-1s、schedules），原本越需要人力介入，自动化的杠杆效应越大。

---

## 与 Harness Engineering 的关联

OpenAI 官方博客在脚注中直接引用了 Harness Engineering 和 Symphony：

> *"This builds on the principles described in our work on harness engineering and Symphony, which walk through how to make tasks legible to Codex, provide scoped context and tools, and keep validation and human review part of the environment."*

这是 Harness Engineering 思想在生产环境的首次大规模验证：

| Harness Engineering 模块 | Tax AI 实现 |
|------------------------|-----------|
| **Evaluator Loop** | Practitioner corrections → eval targets → Codex task → measurable improvement |
| **Production Traces** | 完整输入→输出→修正链路追踪 |
| **Bounded Task Context** | evidence + editable surface + eval gates |
| **Human-in-the-loop** | Practitioners 掌舵改进方向，工程师 review 最终方案 |
| **Scoped Agent Capability** | Codex 作用于 bounded worktree，不越界 |

Tax AI 的三支柱架构本质上是一个**完整运行的 Harness**——不只是安全防护，而是包含了评估、追踪、作用域控制和人机协作的完整工程框架。

---

## 可复用的工程模式

这个案例最重要的贡献不是 Tax AI 本身，而是一套**可复用到其他领域的模式抽象**：

### 核心条件

要让自进化回路运转，需要满足三个条件：
1. **Practitioners 产生的 signal 可结构化**：修正行为必须被捕获为数据，不仅仅是自然语言反馈
2. **Production traces 可完整重建**：eval 上下文必须与生产环境一致
3. **Agent 有能力理解代码库**：Codex 能直接读代码、改代码、跑测试，这是区别于普通 Agent 的关键能力

### 抽象层级

从 Tax AI 的实践中可以抽象出以下可复用组件：

**Review Row Schema**：
```json
{
  "predicted_value": "...",
  "practitioner_corrected": "...",
  "final_filed": "...",
  "error_type": "extraction_miss | mapping_error | unsupported | workflow_noise",
  "环节": "extraction | mapping | submission",
  "repeat_count": 5
}
```

**Codex Scoped Task Context**：
- Read-only: production trace + source documents + eval results
- Read-write: worktree（代码 + schema + mapper）
- Validation: targeted eval + regression eval gates

---

## 笔者的判断

### 这个方向是否值得跟进？

**是，但有条件。**

自进化 Agent 架构的核心价值在于：**它把改进回路的调度权从人转移到了系统**。这在任务复杂度高、领域专家稀缺、但生产 volume 大的场景下价值巨大。

但这个方案的门槛也很高：
1. 需要 practitioners 的修正行为可被结构化捕获——这要求工作流本身数字化程度高
2. 需要 Codex 级别的代码理解和修改能力——普通 GPT-4 API 级别的 Agent 无法承担这个角色
3. 需要生产环境足够稳定，能够产生大量高质量 signal

对于大多数团队，这意味着**先要有稳定的单轮 Agent，再谈多轮自进化**。

### 核心判断

2026 年，能力差距已经从"模型版本"迁移到了"改进回路设计"。模型能力的提升是边际递减的，但改进回路的效率是线性累积的——每一次生产运行都在为下一轮改进积累 signal。

**能建立自进化回路的团队，与只能手动调优的团队，差距会随时间指数级扩大。**

---

## 参考来源

1. [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/) — OpenAI Engineering Blog, 2026-05-27
2. [Harness Engineering](https://openai.com/index/harness-engineering/) — OpenAI
3. [Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/) — OpenAI
4. [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic Engineering
5. [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Anthropic Engineering