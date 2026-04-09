# MCP × MCP：当 Agent 开始暴露 MCP Resources

MCP（Model Context Protocol）最初解决的是一个具体问题：如何让 AI 模型统一地接入外部工具和数据源。这个问题在 2025 年已经被很好地回答了——MCP 作为工具协议，已经成为行业事实标准。

但 2026 年 4 月，一个新的问题开始浮现：谁来给 Agent 提供上下文？答案正在变得清晰——**Agent 自己**。

---

## 旧范式：Agent 是 MCP 客户端

在传统架构中，Agent 是 MCP 的消费端：

```
User/LLM Host → [MCP Client] → [MCP Server: Tools/Resources]
```

MCP Client 嵌入在 LangChain、OpenAI Agents SDK 或 Anthropic SDK 中，向部署了 MCP Server 的外部服务（文件系统、数据库、Slack）发起请求。Agent 始终站在消费链的起点。

这个模型的局限很快暴露出来：**多 Agent 系统中，Agent 之间的上下文无法通过 MCP 流转**。如果一个调度 Agent 需要读取子 Agent 的执行状态、记忆或中间结果，唯一的方式是让子 Agent 暴露一个工具（Tool），调度 Agent 通过工具调用来获取信息。

这带来一个问题：**工具调用是命令式的，而资源读取是声明式的**。调度 Agent 必须知道子 Agent 暴露了哪些工具、怎么调用、参数是什么。耦合在工具边界上，而不是在数据边界上。

---

## 新范式：Agent 同时是 MCP Server

MCP Dev Summit NA 2026（4月2-3日，纽约）揭示了一个正在发生的技术收敛：

**OpenAI Agents SDK v0.13.0 新增了 `list_resources()`、`read_resource()`、`list_resource_templates()` 三个方法，直接在 `MCPServer` 类上实现。**

这意味着什么？OpenAI Agents SDK 中的 Agent 现在可以**同时是 MCP 客户端（连接外部 MCP 服务器）和 MCP 服务器（向其他客户端暴露 MCP Resources）**。

这个变化不是 OpenAI 独家推动的。同场峰会中，Anthropic Python SDK 正在同步实现相同的 MCP Resources API。两家公司的团队在同一时间、用同一个规范，实现了这个相同的接口——这是生态级别的信号，不是竞争性功能差异。

> 引用来源：[MCP Dev Summit NA 2026 报道](https://chatforest.com/guides/mcp-dev-summit-2026-guide/)；[DEV Community: MCP Dev Summit Python 开发者指南](https://dev.to/peytongreen_dev/mcp-dev-summit-2026-what-actually-changed-for-python-developers-16ep)；[OpenAI Agents SDK MCP 文档](https://openai.github.io/openai-agents-python/ref/mcp/server/)

---

## 「MCP × MCP」的工程含义

### 嵌套 Agent 架构成为可能

当一个 Agent 暴露 MCP Resources，其他 Agent 就可以用标准 MCP Resource 读取的方式消费它的上下文，而不需要知道它暴露了哪些具体工具：

```
[OpenAI 调度 Agent]
    ├── MCP Client → [外部 MCP Server: 文件系统/数据库]
    └── MCP Client → [Claude Agent MCP Server]
                          └── 暴露: conversation_history, current_plan, memory
```

调度 Agent 只需调用 `read_resource("agent://claude-agent/conversation_history")` 就能获取子 Agent 的对话历史，而不需要知道这个子 Agent 暴露了哪些工具。这是**松耦合的上下文共享**。

### 上下文变成标准化的可寻址资源

在传统模式中，子 Agent 的上下文是一个黑箱，父 Agent 要获取它只能通过预定义的工具。在 MCP × MCP 模式下，上下文被标准化为：

- `agent://{agent-id}/memory` — 当前记忆内容
- `agent://{agent-id}/conversation_history` — 对话历史
- `agent://{agent-id}/current_plan` — 当前执行计划
- `agent://{agent-id}/tools` — 该 Agent 暴露的能力列表

任何 MCP 客户端都可以用统一的方式发现和读取这些资源，不依赖 Agent 内部实现。

### 横向扩展：多 Agent 资源发现

当系统中有 N 个 Agent，每个 Agent 都暴露 MCP Resources，就形成了一个**可发现的多 Agent 资源网络**：

```
Agent A → 发现 Agent B 的 resources
Agent A → 发现 Agent C 的 resources
Agent B → 发现 Agent A 的 resources
...
```

这是 MCP 的服务发现（Service Discovery）机制在多 Agent 层面的复用。每个 Agent 不需要知道其他 Agent 的内部细节，只需要通过标准的 `list_resources()` 了解对方提供了什么。

---

## MCP Resources API 的跨生态一致性

为什么这个收敛很重要？MCP Resources API（`list_resources` / `read_resource` / `list_resource_templates`）在 OpenAI 和 Anthropic 的 SDK 中以相同签名实现，意味着：

**一个 Python MCP Server 实现 resources 接口后，可以同时被 OpenAI Agents SDK 客户端和 Anthropic Claude 客户端消费。**

这相当于 MCP 的生态锁定效应从「工具层」扩展到了「资源层」。一旦你的 MCP Server 正确实现了 Resources API，它就天然适配两个主流 Agent 运行时，而不需要为每个平台写独立的适配层。

这对 MCP Server 开发者是一个明确的方向信号：**在 2026 年，正确实现 Resources 接口不是可选项，而是生产级部署的必要条件**。

> 引用来源：[OpenAI Agents SDK MCP Reference](https://openai.github.io/openai-agents-python/ref/mcp/server/)；[MCP Python SDK v1.27.0 Release Notes (2026-04-02)](https://github.com/modelcontextprotocol/python-sdk/releases)

---

## MCP SDK V2 的路线图信号

MCP Dev Summit NA 还透露了 SDK V2 的进展：

| SDK | V2 状态 | 关键信息 |
|-----|--------|---------|
| TypeScript | v2.0.0-alpha 已发布（2026-04-01） | Standard Schema（Zod v4/Valibot/ArkType），Fastify 集成，TaskManager 重构 |
| Python | V2 仍在 pre-alpha | 不早于 Q3 2026，不要在生产中等待 |
| Python | v1.27.0（2026-04-02） | OAuth 资源验证（RFC 8707），V2 功能 backport（TasksCallCapability），V2 方向已明确 |

V2 在两个 SDK 中的共同方向是：**Standard Schema 支持**（跨验证库兼容性）和 **Tasks 能力增强**。Resources API 是 V1/V2 共同稳定的功能，不会因为 V2 发布而改变。

---

## 工程的实际建议

**现在（2026 Q2）该做什么：**

1. **如果你的 MCP Server 还没有实现 Resources 接口**：这是最优先的补全项。确保 `list_resources()` 和 `read_resource()` 正确实现，这是跨生态兼容的基础。

2. **如果你的系统有多个 Agent**：考虑让每个 Agent 同时作为一个 MCP Server 暴露其上下文（memory、history、plan）。这比通过工具调用传递上下文更松耦合。

3. **如果你的 Agent 需要消费外部 Agent 的上下文**：用 MCP Resource 的方式访问，而不是直接调用工具。未来的多 Agent 编排层可能会基于 MCP 的服务发现机制来构建。

**不需要做的事情：**

- 不需要为 V2 做破坏性重构。MCP Resources API 在 V1 和 V2 之间是稳定的。
- 不需要同时对接 OpenAI 和 Anthropic 的实现细节。Resources 接口的行为在两个生态中是一致的。

---

## 局限与未解问题

「MCP × MCP」模式目前有几个重要局限：

**1. 认证尚未在嵌套场景中充分解决**

MCP Auth（RFC 8707 / OAuth 2.1）目前主要解决的是「外部服务」到「MCP Server」的认证问题。当两个 Agent 之间通过 MCP Resources 共享上下文时，认证如何传递、是否需要 Agent 级别的身份断言（参见 XAA / Cross-App Access）仍是开放问题。XAA（SEP-990，2025年11月入 spec）在 Okta 有开发者 playground，但 Python SDK 尚未实现。

**2. 实时性与状态一致性问题**

MCP Resources 是请求-响应模式的，不是发布-订阅模式。如果一个 Agent 的状态频繁变化（如执行中 plan 的实时进度），通过 `read_resource` 获取的可能是过期快照。这在需要强实时性的场景（如 Agent 级别的错误恢复）还不适用。

**3. 协议层尚未正式定义「Agent-as-MCP-Server」**

这是一个正在发生的实现收敛，还没有进入 MCP 规范的主体。「MCP × MCP」目前是 SDK 层面的功能，还没有像「MCP Tool」那样被正式写入规范文档。

---

## 结论

「MCP × MCP」揭示了一个底层逻辑：当 MCP 作为工具协议被广泛接受后，它开始向上下文协议延伸。Agent 不再只是 MCP 客户端，它们正在成为 MCP Resources 的提供者，形成一个可发现、可寻址的多 Agent 上下文网络。

这个变化对多 Agent 系统的影响是深远的——它把 Agent 之间的耦合从「工具调用接口」降到了「数据资源地址」。系统设计者需要开始考虑：我的 Agent 应该暴露哪些 MCP Resources？这些 Resources 的寻址schema 是什么？谁有权限读取？

这是 MCP 从工具协议演化为 Agent 网络基础设施的关键一步。

---

## 参考文献

- [MCP Dev Summit 2026 Guide - ChatForest](https://chatforest.com/guides/mcp-dev-summit-2026-guide/) — 峰会整体回顾，95+ Sessions 现场直播
- [MCP Dev Summit 2026: What Python Developers Should Actually Pay Attention To - DEV Community](https://dev.to/peytongreen_dev/mcp-dev-summit-2026-what-actually-changed-for-python-developers-16ep) — Python SDK V2 详细分析，MCP × MCP 跨生态 convergence 背景
- [OpenAI Agents SDK - MCP Server Reference](https://openai.github.io/openai-agents-python/ref/mcp/server/) — MCPServer 类 API 文档，含 list_resources/read_resource
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) — v1.27.0 发布说明（OAuth resource validation，TasksCallCapability backport）
- [OpenAI Agents SDK MCP GitHub](https://github.com/lastmile-ai/openai-agents-mcp) — OpenAI MCP 扩展包示例
- [MCP Specification - SEP-990 (XAA)](https://modelcontextprotocol.io/specification) — Cross-App Access 规范背景
