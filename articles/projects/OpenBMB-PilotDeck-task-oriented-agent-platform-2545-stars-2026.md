# OpenBMB/PilotDeck：任务导向的 Agent 生产力平台

> **核心命题**：PilotDeck 解决了一个让很多 Agent 框架「做得不够优雅」的问题——**跨任务的状态持久化和上下文演进**。它的 WorkSpace 概念将 Agent 的工作状态从「每次对话重建」变成了「可持续累积的经验」。

---

## 这个项目解决什么问题

当前大多数 Agent 框架（包括 LangChain、CrewAI 等）的工作模式是：**每次对话都是一次新的上下文**，Agent 需要在对话开始时接收所有相关信息。

这对短任务有效，但当 Agent 需要在多个任务之间保持连续性时，问题就来了：

- Agent 需要反复在每次对话中解释「我正在做什么」「进展到哪里了」
- 不同任务之间无法共享中间状态，每次都要重新构建上下文
- 长期运行的 Agent（如监控、CI/CD 值守）的上下文会不断膨胀

PilotDeck 的解法是引入 **WorkSpace（工作空间）**概念——一个 Agent 的工作状态持久化单元，让 Agent 的上下文可以在多个任务之间持续演进，而不是每次都从零开始。

---

## 核心架构设计

根据官方 README，PilotDeck 的核心设计包括：

### 1. 任务导向的 Agent 范式

> Task-oriented AI Agent productivity platform — redefining operational boundaries and memory evolution, one WorkSpace at a time.

「memory evolution」是关键词——PilotDeck 不只是存储上下文，而是让 Agent 的上下文随着任务推进不断演进，保留每个阶段的关键决策和中间产物。

### 2. MCP 原生支持

作为 MCP Native 项目，PilotDeck 通过 MCP 协议连接外部工具。这意味着：
- 工具扩展不依赖框架内置实现
- 可以接入任何支持 MCP 的工具（数据库、API、文件系统等）
- 协议层的标准化降低了工具集成的复杂度

### 3. 适用场景

从 Demo 和官方文档看，PilotDeck 适合：

- **项目管理**：Agent 持续追踪多个任务的状态，在不同任务之间切换时保持上下文连续
- **运维自动化**：Agent 监控多个服务，每个服务有自己的 WorkSpace 记录状态
- **复杂对话流程**：需要跨多个会话累积上下文的长流程

---

## 与 Cursor /loop 的互补性

在本文仓库的同轮文章 **[Cursor /loop：事件驱动的长时运行 Agent 循环模式](./cursor-loop-event-driven-agent-loop-2026.md)** 中，我们分析了 Cursor `/loop` 技能如何解决「何时唤醒 Agent」的问题。

PilotDeck 解决的则是另一个维度的问题：**Agent 被唤醒后，如何在多次任务之间累积和管理上下文**。

两者结合的组合价值：

| 维度 | Cursor /loop | PilotDeck |
|------|------------|-----------|
| **核心问题** | 何时再次激活 Agent | 如何在多次任务间管理上下文 |
| **机制** | 事件驱动的自我评估循环 | WorkSpace 状态持久化 |
| **层次** | Harness 循环控制 | Context/Memory 管理 |

如果一个长时运行 Agent 需要同时解决「何时唤醒」和「上下文如何累积」，`/loop` + PilotDeck 提供了从控制层到上下文层的完整覆盖。

---

## 技术概览

| 维度 | 描述 |
|------|------|
| **类型** | Agent 生产力平台 |
| **协议** | MCP Native |
| **License** | AGPL 3.0 |
| **Stars** | 2,545（2026-05） |
| **机构** | OpenBMB（知名中文 AI 开源组织）|
| **语言** | 英文 + 中文双语文档 |
| **官网** | pilotdeck.openbmb.cn |

---

## 笔者认为

PilotDeck 的 WorkSpace 概念本质上是对「Agent Context 作为有状态单元」这一理念的工程化实践。

目前大多数 Agent 框架的上下文管理是「对话级」的——每次对话结束后上下文就消失。PilotDeck 尝试将上下文管理提升到「项目/任务级」，让 Agent 可以在跨会话的维度上累积经验。

这个方向的价值在于，随着 Agent 应用越来越复杂，「上下文如何持久化、如何跨任务演进」会成为越来越突出的工程问题。PilotDeck 是对这个问题的一次有意义的探索。

对于构建需要长期运行的 Agent 系统的工程师，PilotDeck 的 WorkSpace 设计值得参考。

---

**引用来源**：
- [OpenBMB/PilotDeck - GitHub](https://github.com/OpenBMB/PilotDeck)
- [PilotDeck 官网](https://pilotdeck.openbmb.cn)
- [PilotDeck Live Demo](https://pilotdeck.openbmb.cn/pilotdeck.github.io/demo/p/pilotdeck-demo)