# 从内部实现到平台 API：Codex App Server 架构解析

> 本文解读 OpenAI 工程博客《Unlocking the Codex harness: how we built the App Server》（2026），分析 Codex 如何将其内部 agent harness演进为一个稳定的多端平台 API，以及这对 Agent 工程架构设计的启示。

---

## 核心命题

Codex 的 web app、CLI、IDE 扩展、macOS app 所有表面，背后都依赖同一个 agent loop——Codex harness。但把它们连接起来的不是某段共享代码，而是一个**客户端友好的双向 JSON-RPC API**：Codex App Server。

这个 API 的设计历程，回答了一个关键的平台架构问题：**当一个 agent harness 需要同时服务于多个客户端时，如何在不破坏内部实现的前提下提供一个稳定的对外接口？**

---

## 背景：从 TUI 到多端复用

Codex CLI 最初是一个 TUI（终端用户界面）应用。当团队需要构建 VS Code 扩展时，他们面临一个选择：是在 IDE 环境里重新实现一套 agent loop，还是复用已有的 harness？

答案是复用。但复用的方式很有意思：**不是简单地把 CLI 代码封装成 REST API，而是引入了一个专门设计的 JSON-RPC 协议**，这个协议镜像了 TUI 的交互循环，同时支持超越请求-响应模式的需求——比如探索工作区、流式输出推理过程、推送 diff 等。

最初的实验是 [将 Codex 暴露为 MCP server](https://github.com/openai/codex/pull/2264)，但维护 MCP 语义在 VS Code 场景下变得过于复杂。最终，团队引入了一个 JSON-RPC 协议，它直接反映 TUI loop，成为 App Server 的非官方第一个版本。

> "At the time, we didn't expect other clients to depend on the App Server, so it wasn't designed as a stable API."

随着 JetBrains、Xcode 等合作伙伴，以及 Codex 桌面 app（需要并行编排多个 agent）提出集成需求，App Server 从一个内部实现变成了一个**需要长期维护的稳定平台表面**。

---

## 架构拆解：App Server 的四个核心组件

App Server 进程包含四个主要组件，它们共同构成了 harness 与客户端之间的翻译层：

```
┌─────────────────────────────────────────────────────┐
│ App Server Process │
│                                                     │
│  ┌──────────────┐    ┌─────────────────────┐       │
│  │ Stdio Reader │───▶│ Codex Message        │       │
│  │              │    │ Processor           │       │
│  └──────────────┘    └──────────┬──────────┘       │
│                                  │                  │
│                        ┌─────────▼─────────┐        │
│                        │ Thread Manager   │        │
│                        └─────────┬─────────┘        │
│             ┌──────────────────┼──────────────────┤
│    ┌─────────▼─────────┐  ┌──────▼──────┐  ┌───────▼──────┐
│    │  Codex Core      │  │  Codex Core │  │  Codex Core  │
│    │  Thread 1        │  │  Thread 2   │  │  Thread N    │
│    └──────────────────┘  └────────────┘  └─────────────┘
└─────────────────────────────────────────────────────┘
```

**Stdio Reader**：读取客户端的 JSON-RPC 请求
**Codex Message Processor**：将客户端请求翻译为 Codex core 操作，同时将 core 的内部事件流翻译为稳定的 JSON-RPC 通知  
**Thread Manager**：为每个 Thread 创建一个独立的 Codex core session
**Core Threads**：运行实际 agent loop 和 thread 持久化的进程

关键设计点：**Codex core 是 agent 代码的所在地，同时也是一个可以独立运行的 runtime**。它既能作为库被 App Server 调用，也能在没有 App Server 的情况下独立运行 agent loop。

---

## 三个对话原语：稳定的平台契约

这是本文最值得深入分析的工程决策。

在设计一个面向 agent loop 的 API 时，最困难的部分是：**用户与 agent 的交互不是简单的请求-响应**。一个用户请求可能展开为一系列结构化的操作序列——中间步骤、增量输出、产物（diff、文件变更）。客户端需要忠实地呈现这个序列。

Codex 团队给出的答案是三个原语（primitives），它们之间有明确的边界和生命周期：

### Item：原子操作单元

Item 是输入/输出的最基本单位，每个 Item 都有明确的类型（user message、agent message、tool execution、approval request、diff）和生命周期：

- `item/started`：Item 开始
- `item/*/delta`：流式增量更新（可选）
- `item/completed`：Item终结并携带最终 payload

这个生命周期模型允许客户端**立即开始渲染**（on started）→ **流式接收增量**（on delta）→ **最终确认**（on completed）。

### Turn：一次 Agent 工作单元

Turn 从客户端提交输入开始（例如"运行测试并总结失败"），到 agent完成为该输入生产的所有输出结束。一个 Turn 包含一序列 Items，代表中间步骤和产出。

### Thread：会话的持久化单元

Thread 是 Codex 中用户与 agent 之间的一次会话。Codex 创建、恢复、分叉、归档 Threads，并将事件历史持久化，以便客户端重新连接并呈现一致的时间线。

---

## 双向通信：不仅仅是"客户端发请求"

App Server 的 JSON-RPC 协议是**全双向**的。典型的 Thread 交互中，客户端发出请求，服务器推送大量通知。但服务器也可以在 agent 需要输入时**主动发起请求**，例如请求批准，然后在收到响应前暂停当前 turn。

```
Client App Server
  │                                  │
  │──── submit(user input) ─────────▶│
  │◀─── item/started ────────────────│
  │◀─── item/tool_execution/delta ───│
  │◀─── item/completed ──────────────│
  │◀─── turn/completed ─────────────│
  │                                  │
  │        ◀─── approval/request ───│  (server-initiated)
  │──── approval/response ──────────▶│
```

这种双向能力使得 App Server 能够支持**需要人工介入的 agent 工作流**——例如代码审查 Approval、敏感操作确认——而无需改变 agent 的核心 loop 设计。

---

## 工程启示：Harness 架构的演进路径

本文对 Agent 工程最有价值的启示，是展示了 **agent harness 的三种演进阶段**：

| 阶段 | 特征 | 例子 |
|------|------|------|
| **内部实现** | 单体架构，harness 与 UI 紧耦合 | 最初的 Codex CLI (TUI) |
| **实验性抽象** | 引入协议层，但不做稳定性保证 | 最初的 MCP 实验 |
| **平台 API** | 稳定的协议 + 明确的原语 +向后兼容 | Codex App Server |

从 Round331 的"Harness Engineering"到本文的"App Server"，OpenAI 展示了一个完整的演进路径：**当代码生成速度超过人工审核速度时，工程重心从"写代码"转移到"构建让 Agent 高效工作的环境"**——而 App Server 就是这个环境中最关键的接口层。

---

## 与 Round331 的关联

Round331 文章指出：人类从代码实现者 → 环境设计者 + 判断编码者；质量控制必须机械化、持续化。

本文则进一步说明：**当环境本身需要被多个客户端共享时，harness 的接口层必须被显式设计为平台 API**，而不是作为事后补救的封装层。这两个洞察共同指向一个结论：

> **Agent 时代的基础设施，不只是"让 Agent 跑起来"，还包括"让 Agent 的 harness 被可靠地复用"**。

---

## 总结

Codex App Server 的设计揭示了三个对 Agent 工程平台化至关重要的设计原则：

1. **原语先于实现**：在设计 agent 平台 API 时，先定义 Item/Turn/Thread 这类对话原语，比直接暴露内部 agent loop 更稳定
2. **协议即架构**：JSON-RPC 协议不只是传输层，它是连接 harness核心与多端客户的架构层
3. **双向是必需能力**：agent 在长时任务中必然需要人类介入——平台 API 必须支持服务器主动发起的请求，而非仅限客户端轮询

OpenAI 将一个内部实现演进为稳定平台 API 的过程，正是大多数 Agent 工程团队即将面临或正在面临的挑战。本文提供了一个值得参照的架构范本。

---

**引用来源**：

> "The critical link between them? The Codex App Server, a client-friendly, bidirectional JSON-RPC API."
> — OpenAI Engineering Blog, "Unlocking the Codex harness: how we built the App Server", 2026

> "To be useful, the Codex harness needs to be accessible to clients. That's where the App Server comes in."
> — OpenAI Engineering Blog, "Unlocking the Codex harness: how we built the App Server", 2026

> "Designing an API for an agent loop is tricky because the user/agent interaction is not a simple request/response."
> — OpenAI Engineering Blog, "Unlocking the Codex harness: how we built the App Server", 2026