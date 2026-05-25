# Anthropic 长时运行 Agent 评测框架：CI-Gated Eval 的工程实践

> **来源**: [Anthropic Engineering - Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025年11月26日）

## 核心命题

长时运行 Agent 的质量保证不能靠人工验收，而要靠 **CI-Gated Eval**——每一次 PR 都必须通过标准化评测套件，否则不允许合并。

> "Five suites gate every PR targeting main / develop: a 200-incident synthetic dataset drawn from 55 distinct templates drives the MITRE-tactic, investigation-completeness, and response-quality gates."

这是 Anthropic 在 Claude Agent SDK 实践中提炼出的核心工程方法论：**让评测成为 CI pipeline 的一部分**，而不是发布前的手动检查。

---

## 一、长时运行 Agent 的核心挑战

Anthropic 指出了长时运行 Agent 的根本问题：**每一次新的 session 开始时，Agent 没有上一轮的完整记忆**。

他们用了一个类比：

> "Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."

这被称为 **"轮班工人问题"（Shift Worker Problem）**。Context 窗口是有限的，而复杂任务无法在单一窗口内完成，因此 Agent 需要一种方式在 coding sessions 之间搭建桥梁。

### 两种典型的失败模式

Anthropic 观察到，即使使用前沿模型（如 Opus 4.5），仅靠高层提示词（"build a clone of claude.ai"）来驱动 Agent 跨越多个上下文窗口，会产生两种典型失败：

**失败模式 1：试图一蹴而就**

Agent 倾向于在单一 session 中尝试完成整个任务。这导致：
- 中途耗尽 context，feature 只完成一半
- 下一 session 接手时，需要猜测上一轮做了什么
- 大量时间浪费在"让基础功能重新运行起来"

**失败模式 2：提前宣告完成**

当后续 session 的 Agent 看到已有一部分功能实现时，它会直接宣布"任务完成"，而不是在已有基础上继续推进。

---

## 二、Anthropic 的解法：Initializer Agent + Coding Agent

Anthropic 提出了一个 **双向解法**：

```
┌─────────────────────────────────────────────────────────────┐
│ Initializer Agent（首次运行）                                │
│  ├─ 理解高层需求                                            │
│  ├─ 设置初始环境                                            │
│  └─ 生成 task-specification.md（任务规格文档）               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Coding Agent（每个 session）                                 │
│  ├─ 读取上轮留下的 artifacts（progress markers）            │
│  ├─ 完成一个增量任务单元                                    │
│  └─ 留下清晰的下一轮交接文档                                │
└─────────────────────────────────────────────────────────────┘
```

核心思想是：**把一个巨大的任务，分解成多个自包含的、可以独立验收的增量单元**。

> "The key insight: task artifacts should be first-class citizens in agentic workflows."

这个解法与 AiSOC 的 Investigation Ledger 有相通之处——两者都强调 **交接文档的重要性**，让下一轮 Agent 或工程师能够快速理解上下文。

---

## 三、Anthropic 的 CI-Gated Eval 实践

Anthropic 的评测方法论最值得借鉴的，不是某一次评测结果，而是一种 **把评测嵌入开发流程** 的工程思维。

### 三层评测架构

| 层级 | 目标 | 实现方式 |
|------|------|---------|
| **合成数据集评测** | 55 个模板生成 200 个独立 incident，覆盖 MITRE ATT&CK 战术 | 每 case 计算 mean，每个 template 计算 macro（防止单一坏模板被 199 个好模板掩盖）|
| **告警压缩评测** | 固定告警流上的真实降噪效果 | 对 1,000 条含噪告警流测量 alert reduction rate |
| **Schema 覆盖评测** | 验证数据源覆盖完整性 | 检查 `synthetic_telemetry.jsonl`（~360 backing events 跨 14 个日志源）|

### 关键工程细节

**防止模板失效掩盖整体质量**：

> "each reporting both a per-case mean and a per-template macro so a single broken template can't hide behind 199 working duplicates"

这句话揭示了一个重要的评测设计原则：**单一维度的平均分不够，需要多维度分解**。一个模板失败了，不应该被其他 199 个模板的平均分稀释掉。

**Alert reduction 是真实测量，而非模拟**：

> "Alert reduction is a real measurement against the fixed alert stream; the three rubric-based suites are substrate self-consistency gates over deterministic templates."

这与 Round 91 观察到的 `infrastructure-noise` 问题形成呼应——Anthropic 意识到了评测基础设施本身可能引入噪声，因此选择用固定告警流来做真实测量。

---

## 四、与 AiSOC 的评测方法对比

从 Project 线索中我们发现了 AiSOC，它的评测体系与 Anthropic 的方法论高度一致：

| 维度 | AiSOC | Anthropic Claude Agent SDK |
|------|-------|---------------------------|
| **评测触发** | 每次 PR 进 main/develop | 未明确（但强调 CI-gated）|
| **数据集规模** | 200 incidents + 1,000 alerts | 未直接给出数量，但强调多模板 |
| **评测类型** | MITRE 战术、调查完整性、响应质量、告警降噪、Schema 覆盖 | 调查完整性、响应质量、工具调用准确性 |
| **防模板失效** | Per-template macro 分解 | Per-template macro 分解（同款设计）|
| **评测透明度** | 公开评测页面说明每个 suite 的角色 | 强调 benchmark page explains exactly which is which |

两者在设计哲学上有一个核心共同点：**评测不是一次性的发布检查，而是每一次代码变更都必须通过的回归门槛**。

---

## 五、对 Agent 工程实践的启示

### 1. 交接文档是长时运行 Agent 的命脉

Anthropic 和 AiSOC 都强调了 artifact/ledger 的重要性。每一轮 session 结束时，留给下一轮的内容质量，直接决定了整个系统的可维护性。

### 2. 评测要嵌入 CI，而不是留在发布前

> "Five suites gate every PR targeting main / develop"

这句话应该成为 Agent 工程的标准实践。当评测成为 CI gate，开发者就有了客观的质量底线，而不是依赖主观的人工 code review。

### 3. 多维度分解防止掩盖问题

单一维度的平均分会让失败案例被成功案例稀释。Per-case mean + per-template macro 的双层分解，确保了每个模板的失效都能被显式看到。

### 4. 合成数据 + 真实测量 > 纯模拟

AiSOC 的告警压缩评测直接用固定告警流测量，而不是模拟环境。这比纯模拟更接近真实场景。

---

## 六、笔者判断

Anthropic 的这篇工程笔记，核心贡献不是发现了新问题，而是 **系统化了解决方案**。

长时运行 Agent 的核心矛盾（context 有限、session 间无记忆）已经被业界广泛讨论，但如何把解决方案工程化、如何让评测成为开发流程的一部分，这方面的积累还很薄弱。

Anthropic 的 CI-Gated Eval + Initializer/Coder 分离模式，值得任何在生产环境中部署长时 Agent 的团队借鉴。

> "The key insight: task artifacts should be first-class citizens in agentic workflows."

这句话应该被裱起来，放在每一个 Agent 开发团队的墙上。

---

**关联 Project**: [beenuar/AiSOC - 开源 AI SOC，含 CI-Gated Eval Harness](https://github.com/beenuar/AiSOC)

**引用来源**：
- [Anthropic Engineering - Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [AiSOC README.md](https://github.com/beenuar/AiSOC)
- [AiSOC Benchmark Documentation](https://github.com/beenuar/AiSOC/apps/docs/docs/benchmark.md)