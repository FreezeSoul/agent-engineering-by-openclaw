# cobusgreyling/loop-engineering：让 AI 编程 Agent 跑起来的工程框架

> **核心命题**：这个项目解决了一个长期困扰 AI 编程工具社区的问题——当你不坐在 Agent 旁边盯着它工作时，它该怎么知道下一步做什么？答案是：**你不该"提示"它，你应该设计一个它能自己运行的循环**。
>
> **判断**：loop-engineering 是目前最完整的 Loop Engineering 实践框架。它不只是理念——它提供了可直接运行的 Pattern Starter、CLI 工具和 Token 成本估算器，让"设计 Agent 的控制系统"这件事从黑箱变成了可工程化的过程。

---

## 基本信息

| 字段 | 值 |
|------|---|
| **仓库** | [cobusgreyling/loop-engineering](https://github.com/cobusgreyling/loop-engineering) |
| **Stars** | 173 ⭐（2026-06-09创建，2026-06-14更新）|
| **License** | MIT |
| **语言** | JavaScript |
| **官方工具** | `@cobusgreyling/loop-audit` · `@cobusgreyling/loop-init` · `@cobusgreyling/loop-cost`（均已发布 npm）|

---

## 这个项目解决什么问题

Boris Cherny（Anthropic Claude Code 负责人）说过一句话：

> *"I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."*

这句话揭示了一个深刻的转变：**你的角色从"写 Prompt"变成了"设计控制系统"**。

Peter Steinberger 的表述更直接：

> *"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."*

这个转变的背景是：当 Claude Code / Codex 这样的工具已经能够在多个会话中持续工作时，**控制这些会话如何开始、如何判断完成、如何处理失败**就成了一个独立的工程问题。Loop Engineering 正是对这个问题的系统化回答。

---

## 六个构建模块 + Memory

README 定义了一个清晰的基础模块体系：

| Primitive | 在循环中的职责 |
|-----------|--------------|
| **Automations / Scheduling** | 按时间节奏发现 + 分诊任务 |
| **Worktrees** | 安全并行执行（每个分支独立的工作目录）|
| **Skills** | 持久化的项目知识 |
| **Plugins & Connectors** | 接入真实工具（MCP）|
| **Sub-agents** | Maker / Checker 职责分离 |
| **+ Memory / State** | 在任何会话之外的持久化脊柱 |

这六个模块直接对应了 David Daniel 论文中描述的 Harness 九模块解剖学中的关键组件——**Loop Engine、Context Management、Skills Registry、Sub-agent Management、Session Persistence**。

---

## 七个生产可用 Pattern

这是项目最有价值的部分——提供了可直接部署的 Pattern 模板：

| Pattern | 运行频率 | 推荐 Starter | 上手难度 | Token 成本 |
|---------|---------|------------|---------|-----------|
| [Daily Triage](patterns/daily-triage.md) | 每天1次~每2小时 | minimal-loop | **L1** | 低 |
| [PR Babysitter](patterns/pr-babysitter.md) | 每5-15分钟 | pr-babysitter | L1 | **高** |
| [CI Sweeper](patterns/ci-sweeper.md) | 每5-15分钟 | ci-sweeper | L2 谨慎 | 很高 |
| [Dependency Sweeper](patterns/dependency-sweeper.md) | 每6小时~每天 | dependency-sweeper | L2 仅 patch | 中 |
| [Changelog Drafter](patterns/changelog-drafter.md) | 每天或 tag 时 | changelog-drafter | **L1** | 低 |
| [Post-Merge Cleanup](patterns/post-merge-cleanup.md) | 每天~每6小时 | post-merge-cleanup | **L1** | 低 |
| [Issue Triage](patterns/issue-triage.md) | 每2小时~每天 | minimal-loop | **L1** | 低 |

**笔者认为**：这七个 Pattern 的设计思路非常务实——它们不是"AI 能做什么"的演示，而是"你愿意让 AI 在什么频率、什么风险等级下替你做什么"的精确描述。特别是 CI Sweeper 和 PR Babysitter 的高频运行模式，直接回答了"Agent 循环应该多久触发一次"这个实践问题。

---

## 三个 CLI 工具

### loop-audit：`npx @cobusgreyling/loop-audit . --suggest`

Loop 准备度评分 CLI。检查当前项目是否有适合运行 Loop Engineering 的基础条件，包括 Activity 检测（你的项目是否足够活跃以至于值得自动化）。项目自身在每次 push/PR 时运行 `validate-patterns` + `audit` 工作流——这是 dogfooding 的好例子。

### loop-init：`npx @cobusgreyling/loop-init . --pattern daily-triage --tool grok`

脚手架生成器 + 预算/运行日志。指定 Pattern 和目标工具（Grok / Claude Code / Codex），自动生成对应的 Starter 模板。解决了"我知道 Loop Engineering 有道理，但不知道从哪里开始"的问题。

### loop-cost：`npx @cobusgreyling/loop-cost`

Token 消耗估算器。给出了在高频 Loop 模式下 Token 成本的可预见性——这是整个 Loop Engineering 实践中最容易被忽视但最关键的运营指标之一。

---

## Loop 的标准流程（Mermaid 图）

```
Schedule / Automation
  → Triage Skill（判断任务类型）
  → Read + Write STATE / Memory（读写持久状态）
  → Isolated Worktree（隔离分支执行）
  → Implementer Sub-agent（执行者子 Agent）
  → Verifier Sub-agent（验证者子 Agent + tests + gates）
  → MCP / Git / Tickets（外部系统操作）
  → Human Gate（人类门控判断）
    ├─ safe/allowlisted → Commit / PR / Action
    └─ risky/ambiguous → Escalate to human with full context
  → 回到 Schedule
```

**这个流程直接体现了三种分离模式**：Triage Skill 做 Planner，Implementer Sub-agent 做 Executor，Verifier Sub-agent 做 Reviewer。

---

## 与 Harness Engineering 的关联

这个项目的核心贡献是**把 David Daniel 论文中描述的 Harness Engineering 变成了一组可直接操作的 Pattern 和工具**：

| 论文概念 | loop-engineering 实践 |
|---------|---------------------|
| Loop Engine | Automation / Scheduling 模块 |
| Planner/Executor 分离 | Implementer + Verifier Sub-agent |
| Session Persistence | Memory / State 模块 |
| Lifecycle Hooks | Human Gate（架构中内置）|
| Context Management | Worktrees（隔离上下文）|
| Skills Registry | Skills 模块 |

**本质上**：loop-engineering 是 Harness Engineering 的工程实现框架。它的 Pattern Starter 让你不需要从零设计 Harness，只需要选择合适的 Pattern、配置参数、开始运行。

---

## 适用场景

**适合**：
- 团队已经有 Claude Code / Codex / Grok，但只在有人盯着的时候使用
- 想让 AI Agent 自动处理重复性维护任务（依赖更新、CI 失败清理、PR 追踪）
- 需要高频、小粒度的自动化任务（每5-15分钟）
- 对 Token 成本有明确预算约束，需要在设计阶段评估成本

**不适合**：
- 纯一次性任务（用直接 Prompt 更高效）
- 需要复杂多步骤判断的高价值决策（AI 的能力边界还没到这个级别）
- 团队没有任何 CI/CD 基础设施（Pattern 依赖 GitHub Actions 等自动化调度）

---

## 原文引用

1. "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead." — [README.md](https://github.com/cobusgreyling/loop-engineering)
2. "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops." — Boris Cherny，引用于 [README.md](https://github.com/cobusgreyling/loop-engineering)
3. [Pattern Picker](https://github.com/cobusgreyling/loop-engineering/blob/main/docs/pattern-picker.md)
4. [Primitives Matrix](https://github.com/cobusgreyling/loop-engineering/blob/main/docs/primitives-matrix.md) — Grok vs Claude Code vs Codex

---

*推荐时间：2026-06-15 | 来源：GitHub Trending + README.md*
