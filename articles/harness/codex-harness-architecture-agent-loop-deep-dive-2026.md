# Codex Harness 架构：Agent Loop 的工程深度解析

> **核心命题**：Codex 的设计揭示了一个关键洞察——Agent Loop 不是「模型+工具」的简单循环，而是一个包含沙箱隔离、上下文管理、性能优化的复杂工程系统。理解这个系统，是理解现代 AI Agent 架构的钥匙。

Michael Bolin 在 OpenAI 官方博客上发布了这篇深度技术文章，作为 Codex 系列的第一篇。他在文中明确指出：

> "To unpack those insights, this is the first post in an ongoing series where we'll explore various aspects of how Codex works, as well as hard-earned lessons."

本文将深入分析 Codex Harness 的核心设计，揭示那些藏在 Agent Loop 表象之下的工程机制。

---

## 一、Agent Loop：Harness 的本质角色

### 1.1 什么是 Harness

在 Codex 的语境里，"harness"（挽具/驾驭）是一个精确的工程隐喻：**它不是模型本身，而是控制模型如何与真实世界交互的框架**。

Agent Loop 是 Harness 的核心逻辑，负责编排用户、模型、工具三者之间的交互。Michael Bolin 给出了一个高度抽象的流程图：

```
用户输入 → Prompt 构建 → 模型推理 → 
  ├─ 最终响应 → 结束
  └─ 工具调用 → 结果回传 → 重新推理（循环）
```

每一轮循环称为一个 "turn"，每个 turn 包含多次模型推理和工具调用，直到模型输出一个 assistant message 作为终止信号。

### 1.2 为什么 Harness 设计很重要

Bolin 在文中指出了一个关键设计约束：

> "Because tokens are produced incrementally, this translation can happen as the model runs, which is why many LLM-based applications display streaming output."

Token 的流式输出意味着 Harness 必须能够处理部分完成的响应——模型可能在输出完整答案之前就调用了一个工具。Harness 必须能够**中断正在进行的推理、执 行工具、然后恢复推理**，这是一个需要精心设计的状态机。

笔者认为，这才是 Agent Loop 最核心的工程挑战：**不是「让模型调用工具」，而是「让模型在任意时刻中断并恢复」**。

---

## 二、Prompt 构建：Roles 的优先级体系

### 2.1 三层输入结构

Codex 调用 OpenAI Responses API 时，Prompt 被组织为一个 "list of items"，每个 item 有三个属性：`type`、`role`、`content`。

**核心三层**：

```json
{
  "instructions": "...",    // 系统级指令（system/developer）
  "tools": [...],           // 可用工具列表
  "input": [...]            // 用户输入 + 对话历史
}
```

`instructions` 对应 system 或 developer role，Codex 会在这个字段中注入沙箱配置、权限策略等信息。

### 2.2 Roles 的优先级

OpenAI Responses API 定义了 roles 的优先级（从高到低）：

| 优先级 | Role | 用途 | 权重 |
|--------|------|------|------|
| 1 | system | 全局系统级配置 | 最高 |
| 2 | developer | 开发者级配置（可被用户覆盖） | 高 |
| 3 | user | 用户输入 | 中 |
| 4 | assistant | 模型历史输出 | 低 |

Codex 在构建 prompt 时，会按照这个优先级顺序插入内容。值得注意的是，**system message 的内容由服务端控制**，而非客户端——这意味着 OpenAI 可以统一管理一些系统级行为（如安全策略）。

### 2.3 工具的来源

Codex 的工具来源有三层：

1. **Codex 提供的工具**：如 shell tool，受 Codex 的沙箱机制保护
2. **Responses API 提供的工具**：OpenAI 原生的工具集
3. **MCP 服务器提供的工具**：用户通过 MCP 协议接入的第三方工具

这里有一个关键的设计差异：

> "That is, other tools, such as those provided from MCP servers, are not sandboxed by Codex and are responsible for enforcing their own guardrails."

**MCP 工具必须自己负责 guardrails**，这是 MCP 协议的一个核心设计约束。Codex 只对自家工具负责。

---

## 三、上下文窗口管理：Compaction 机制

### 3.1 二次方增长问题

随着对话的进行，每个 turn 的输入都包含之前所有的 messages 和 tool calls。Bol in 指出了一个关键的性能问题：

> "You might be asking yourself, 'Wait, isn't the agent loop quadratic in terms of the amount of JSON sent to the Responses API over the course of the conversation?' And you would be right."

确实如此。每次推理请求的输入长度都在增长，而每次推理的成本与输入长度成正比。如果不做任何优化，总成本将呈现二次方增长。

### 3.2 Compaction：上下文压缩

Codex 的解决方案是 **compaction（压缩）**：

当 token 数量超过某个阈值时，Harness 会用一个新的、更小的输入列表替换原有的对话历史。这个新列表"representative of the conversation"，能够保留关键信息同时大幅减少 token 数量。

Codex 的 compaction 经历了两个阶段：

1. **手动 compaction**：用户手动调用 `/compact` 命令，触发 summarization
2. **自动 compaction**：OpenAI Responses API 引入了 `/responses/compact` 端点，可以更高效地执行压缩

自动 compaction 相比手动 compaction 的优势在于：它可以在对话进行中自动触发，无需用户介入。

### 3.3 笔者的工程判断

Compaction 机制揭示了一个重要的工程取舍：**完全准确的历史记录 vs. 可扩展的上下文管理**。

压缩后的上下文必然丢失一些细节，但换来的是模型可以持续工作而非在上下文窗口耗尽后崩溃。笔者的判断是：**对于大多数软件开发任务，这种取舍是值得的**，因为开发过程中的中间状态（如「正在实现某个函数」）远不如最终结果重要。

---

## 四、性能优化：Prompt Caching

### 4.1 线性 vs. 二次方

除了 compaction，Codex 还利用了 **Prompt Caching** 来降低采样成本：

> "When we get cache hits, sampling the model is linear rather than quadratic."

Prompt Caching 的核心机制是：对于相同的 prompt 前缀，API 可以复用之前的计算结果，无需重新处理。

### 4.2 Cache Hit 的条件

Cache hits 只发生在 **exact prefix match** 的情况下。这意味着：

- 工具列表必须完全相同
- 模型必须相同
- 沙箱配置、approval mode、当前工作目录都必须相同

文中特别指出了一个 MCP 工具相关的陷阱：

> "MCP tools can be particularly tricky because MCP servers can change the list of tools they provide on the fly via a notifications/tools/list_changed notification. Honoring this notification in the middle of a long conversation can cause an expensive cache miss."

如果在长对话中途 MCP 服务器更新了工具列表，Codex 必须重新构建 prompt，导致 cache miss。

### 4.3 配置变更的处理策略

Codex 的设计选择是：**不修改历史消息，而是追加新消息**。

当沙箱配置或 approval mode 变更时，Codex 会插入一个新的 `role=developer` 消息；当工作目录变更时，会插入一个新的 `role=user` 消息。这样可以最大限度地保留 prompt 前缀的一致性。

---

## 五、企业隐私：Zero Data Retention（ZDR）

### 5.1 无状态请求设计

Codex 的架构选择了一条有趣的路：**避免使用 `previous_response_id` 参数**。

`previous_response_id` 是 OpenAI Responses API 提供的一个参数，允许客户端引用之前的对话状态，从而避免每次都发送完整的对话历史。但这需要服务端存储对话状态。

Codex 选择不使用这个参数，原因在于：

> "This also makes it straightforward to support customers who have opted into Zero Data Retention (ZDR), as storing the data required to support previous_response_id would be at odds with ZDR."

ZDR 意味着 OpenAI 不会存储任何对话数据——这对企业客户至关重要。

### 5.2 ZDR 的代价与收益

不使用 `previous_response_id` 意味着每次请求都要发送完整的对话历史，成本是二次方的。但 Codex 通过 Prompt Caching 将成本降为线性，同时支持了 ZDR 合规。

这是一个典型的工程取舍：**用计算换隐私**。

Bolin 特别指出，即使在 ZDR 模式下，reasoning messages 仍然可以被解密使用（通过 encrypted_content），这意味着用户不会因为隐私合规而丧失所有上下文能力。

---

## 六、工程启示：Harness 设计的关键维度

### 6.1 核心设计原则

从 Codex 的架构中，我们可以提取出 Harness 设计的几个核心原则：

| 维度 | Codex 的做法 | 工程意义 |
|------|-------------|---------|
| **状态管理** | 无状态请求 + Prompt Caching | 支持 ZDR，换来隐私合规 |
| **上下文管理** | Compaction + 阈值触发 | 避免上下文窗口耗尽 |
| **工具安全** | 分层沙箱（Codex vs. MCP）| 各司其职，不过度绑定 |
| **性能优化** | Exact prefix caching | 线性成本替代二次方 |
| **配置变更** | 追加而非修改历史 | 保留 cache hit 机会 |

### 6.2 笔者的核心判断

笔者认为，Codex 的设计揭示了一个重要的范式转变：**从「让模型做所有事」到「让 harness 控制模型」**。

Agent Loop 不只是模型推理的循环，它是一个**状态机 + 上下文管理器 + 性能优化器**的复合体。没有精心设计的 harness，模型的能力再强也无法可靠地完成复杂任务。

这也解释了为什么 "harness engineering" 成为 2026 年的重要研究方向——**模型能力的上限已经很高，但工程能力的差距决定了实际应用效果的上限**。

---

## 七、相关工程机制

Codex 的 Agent Loop 与其他工程机制形成了一个完整的系统：

- **Evaluator Loop**：Agent Loop 的本质就是不断评估（模型输出）→ 执行（工具调用）→ 评估的循环
- **Checkpoint & Progress File**：Compaction 机制本质上是将对话历史压缩为 checkpoint
- **Sandbox & Guardrails**：工具沙箱的分层设计是安全 Agent 的基础
- **Context Management**：Prompt Caching + Compaction 是上下文管理的两个维度

---

## 附录：关键引用

> "To kick off, we'll focus on the agent loop, which is the core logic in Codex CLI that is responsible for orchestrating the interaction between the user, the model, and the tools the model invokes to perform meaningful software work."
> — Michael Bolin, OpenAI Engineering Blog

> "We hope this post gives you a good view into the role our agent (or 'harness') plays in making use of an LLM."
> — Michael Bolin, OpenAI Engineering Blog

> "Because the agent can execute tool calls that modify the local environment, its 'output' is not limited to the assistant message."
> — Michael Bolin, OpenAI Engineering Blog

---

**标签**：Harness Engineering、Agent Loop、Prompt Caching、Compaction、Context Management、ZDR、OpenAI Codex

**相关项目**：
- OpenAI Codex CLI（开源仓库：github.com/openai/codex）
- LiteLLM（与 Codex 的 model provider 集成相关）

**关联文章**：
- CrewAI Token Spend Optimization（Token 经济学编排层）
- Portkey-AI/gateway（云优先 LLM Gateway）
- BerriAI/litellm（自托管 LLM Gateway）