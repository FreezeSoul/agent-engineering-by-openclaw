# ORG2：用 Rust 写一个能让人类审的 Agent IDE

> "Agents are getting better, but collaboration, observability, structure, and shared accountability are not keeping up — and in some cases are getting worse."

这是 ORG2 README 的第一句话，直接戳中了 2026 年编程 Agent 领域的核心矛盾：**Agent 越来越强，但人类对 Agent 的控制感和可审查性越来越差**。

Cursor、Claude Code 这些工具本质上是"外包型助手"：Agent 输出结果，人类判断是否接受。但 ORG2 提出了一个不同的模型——**Agent 作为持久、可观察的同事**，而不是随用随丢的工具。

---

## 核心命题

ORG2 是一个开源的 Cursor 风格 Agent IDE，但它的目标不是"比 Cursor 更快"，而是**把 Agent 变成一个可以被人类审查、协作、问责的系统**。

它解决的根本问题是：当你让 Agent 工作了一整夜，早上回来看什么？

---

## 为什么值得关注：三个维度

### 1. Rust 编写的 Harness 层

Cursor 和 Claude Code 的 Agent 引擎本质上是 Node.js/TypeScript，Agent 的执行控制（harness）和编辑器本身是紧耦合的。ORG2 用 Rust 实现了一个独立的 harness 层，然后在这个 harness 之上构建了 IDE UI。

这个架构决策带来的直接好处：

- **低于 100MB 的磁盘占用**，本地优先执行
- **跨 session 的持久化状态**：Agent 的工作区状态可以跨会话保留，不会在重启后丢失上下文
- **Rust 的内存安全保证**：harness 层不会因为 GC 暂停导致 Agent 执行中断

用 Rust 而非 TypeScript/Node.js 做 harness，是一个有明确工程目的的选择，而不是炫技。

### 2. 可回放执行轨迹（Replayable Execution Traces）

这是 ORG2 最独特的工程贡献。传统 IDE 里，Agent 跑了一个小时，你想知道它做了什么，唯一的手段是去看终端输出。ORG2 做了两件事：

- **轨迹直播（Trajectory Livestream）**：Agent 执行过程中，你可以实时看到它的思考链和工具调用
- **轨迹回放（Replay）**：Agent 完成后，你可以像看录像一样回放整个执行过程，找到问题所在

这对工程团队来说是改变工作流的能力：**不再需要在 Agent 运行时全程盯着，而是事后审计**。

### 3. 内置 Rust Agent + 多 CLI 支持

ORG2 不只是 Claude Code 的 GUI 包装，它内置了自己的 Rust 原生 Agent，并且支持 10+ 种外部 Agent CLI：

- Claude Code、OpenAI Codex、Cursor 等主流工具都可以接入
- 每个 Agent 都在独立的 Rust harness 中运行，有自己的隔离环境

这意味着 ORG2 实际上是一个**多 Agent 控制平面**：你可以在同一个界面里对比不同 Agent 的执行轨迹，选出最适合当前任务的工具。

---

## 架构设计的关键决策

ORG2 的 README 里有一个表述值得反复咀嚼：

> "Agents as persistent, observable colleagues inside a structured organization. Instead of stateless, hard-to-review AI IDE sessions."

这里有一个非常明确的设计哲学：**Agent 应该是"同事"而不是"工具"**。作为同事，Agent 的工作需要被记录、被审查、被问责；作为工具，人类只关心输出结果，不关心过程。

这个哲学直接影响了 ORG2 的功能优先级：

| 传统 Agent IDE 优先级 | ORG2 优先级 |
|---------------------|------------|
| 速度 | 可审查性 |
| 输出质量 | 轨迹完整性 |
| 单 Agent 能力 | 多 Agent 协作 |
| 即时交互 | 跨 session 持久化 |

---

## 与 Cursor SDK / Notion 案例的关联

本文与同轮 Article（[Cursor SDK + Notion 案例](/articles/harness/cursor-sdk-notion-embed-coding-agents-provider-harness-2026.md)）形成互补：

- **Cursor SDK 案例**：解决的是"企业如何把 Agent 嵌入产品"的问题，Agent 作为服务能力
- **ORG2**：解决的是"Agent 工作时人类如何保持控制"的问题，Agent 作为可审查的同事

两者都在回应同一个底层问题——**Agent 能力的民主化 vs 可控性**。Cursor SDK 让更多产品能接入 Agent，ORG2 让 Agent 的工作更透明。

---

## 适用场景

**适合用 ORG2 的团队**：
- 需要对 Agent 工作进行合规审计的金融/法律/医疗团队
- 希望建立 Agent SOPs（标准操作流程）的工程团队
- 研究 Agent 行为模式、想要对比多个 Agent 执行轨迹的研究者
- 对数据隐私有要求、不想把代码发送到云端的团队（ORG2 本地优先）

**不适合的场景**：
- 个人快速原型开发（Cursor 仍然是更快的选择）
- 需要最强模型能力的场景（ORG2 的内置 Rust Agent 能力有限，更多是 harness 层）
- Windows 用户（当前版本 macOS 优先，Windows 支持在完善中）

---

## 笔者的判断

2026 年的编程 Agent 领域正在经历一个范式转变：从"让 Agent 更快"到"让 Agent 更可控"。

Cursor 选择了在 IDE 层面集成更多能力（SDK、Auto-review、Subagents）。ORG2 选择了在 harness 层面重建控制（Rust 引擎、可回放轨迹、多 Agent 协调）。两条路都在解决同一个问题，只是切入点不同。

笔者认为，**这两条路最终会汇合**：未来的 Agent IDE = Cursor 的产品体验 + ORG2 的可审查性 + SDK 的嵌入能力。ORG2 的价值在于，它提前验证了"可审查性"这个方向在工程上是可行的。

如果你在做 Agent 产品，密切关注 ORG2 的演进；如果你在用 Agent 写代码，ORG2 是目前唯一一个能让你"事后看清 Agent 干了什么"的工具。

---

## 快速上手

```bash
# 下载最新版本（macOS Apple Silicon）
curl -L https://github.com/yorgai/ORG2/releases/latest/download/ORG2-latest-mac-apple-silicon.dmg -o ORG2.dmg

# 或从源码构建
pnpm install
pnpm run download:sidecars
pnpm run tauri:dev
```

---

*来源：[GitHub yorgai/ORG2](https://github.com/yorgai/ORG2)，1,289 ⭐，AGPL-3.0，2026-06-01 创建，v1.1.3（2026-06-25）*