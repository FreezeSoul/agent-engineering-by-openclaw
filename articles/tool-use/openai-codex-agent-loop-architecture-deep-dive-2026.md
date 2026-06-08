# OpenAI Codex Agent Loop 架构深度解析：工程机制的三个核心设计

> 本文深度解析 OpenAI 工程团队官方发布的 Codex Agent Loop 架构设计，揭示软件 Agent 工程化落地的三个核心技术决策。

---

## 核心命题

Codex CLI 的 Agent Loop 本质上是一个**受控的推理-工具调用循环**，但 OpenAI 工程团队在这基础上叠加了三层工程机制：**Prompt Caching 优化**、**上下文窗口管理**、以及**无状态设计**。这三个设计决策不是孤立的技术选择，而是相互制约的工程权衡。

---

## 一、Agent Loop 的本质

Agent Loop 是 Codex 的核心逻辑，负责协调用户、模型、和工具三者之间的交互。一个简化的循环如下：

```
用户输入 → 构建 Prompt → 模型推理 → 响应解析
    ↑ ↓
    └────工具调用执行 ──────────→追加结果到 Prompt
```

关键点：
- **每次工具调用后，输出结果会追加到原始 Prompt**，形成新的输入用于下一轮推理
- **循环终止条件**：模型停止发出工具调用，返回 assistant message
- **对话延续**：每次新消息都包含完整对话历史，Prompt 持续增长

> 原文引用：*"This process repeats until the model stops emitting tool calls and instead produces a message for the user (referred to as an assistant message in OpenAI models)."*

---

## 二、Prompt Caching：静态内容前置是性能关键

模型采样（sampling）成本远大于网络传输成本，因此 **Prompt Caching 是核心效率优化手段**。

Cache hits 的前提是**精确前缀匹配**。OpenAI 给出了明确的最佳实践：

> 原文引用：*"Cache hits are only possible for exact prefix matches within a prompt. To realize caching benefits, place static content like instructions and examples at the beginning of your prompt, and put variable content, such as user-specific information, at the end."*

Codex 的 prompt 结构设计验证了这一原则：

1. **系统级内容**（instructions）：固定不变 → 前置
2. **工具定义**（tools）：配置后不常变化 → 前置
3. **用户指令**（input）：动态变化 → 后置

### 一个真实教训：MCP 工具顺序 Bug

OpenAI 提到他们的 MCP 工具支持曾引入一个 Bug：**工具枚举顺序不一致**，导致每次工具列表变化都产生 Cache Miss。

这揭示了一个重要工程实践：**对于 MCP 这类动态工具集，必须在初始化时固定排序规则**，否则对话中途工具变化会触发昂贵的 Cache Miss。

> 原文引用：*"our initial support for MCP tools introduced a bug where we failed to enumerate the tools in a consistent order, causing cache misses."*

---

## 三、上下文窗口管理：Compaction 策略

随着对话进行，Prompt 持续增长，最终可能触及上下文窗口上限。Codex 的解决方案是 **Compaction（压缩）**：

### 演进路径

| 阶段 | 实现方式 | 问题 |
|------|---------|------|
| **v1** | 用户手动执行 `/compact` 命令触发摘要 | 需要用户介入，无法自动 |
| **v2** | Responses API 的 `/responses/compact` 端点 | 服务端自动完成，更高效 |

压缩后，对话历史被替换为一个代表性的摘要项，使模型能够基于压缩后的上下文继续工作。

### 设计权衡：为何不用 previous_response_id？

OpenAI 的 Responses API 支持 `previous_response_id` 参数，理论上可以避免每次请求都传递完整历史。但 Codex 选择**主动放弃这一机制**，原因有二：

1. **无状态设计**：保持请求完全无状态，简化服务提供方的实现
2. **ZDR（Zero Data Retention）合规**：使用 `previous_response_id` 需要服务端存储数据，与 ZDR 客户的数据不留存政策冲突

> 原文引用：*"Avoiding previous_response_id simplifies things for the provider of the Responses API because it ensures that every request is stateless. This also makes it straightforward to support customers who have opted into Zero Data Retention (ZDR)."*

**关键洞察**：这个权衡说明，在企业级 Agent 设计中，**合规约束会直接影响技术架构选择**。不是技术最优解，而是业务约束下的最优解。

---

## 四、中途配置变更的处理

对话中途可能发生配置变更（如工作目录变化、审批模式变化）。Codex 的处理策略是**追加新消息而非修改历史消息**：

-沙箱配置或审批模式变化 → 追加 `role=developer` 消息
- 当前工作目录变化 → 追加 `role=user` 消息

这种设计的优势：**不破坏已有 Prompt 的前缀结构**，从而保留 Cache Hit 的可能性。

---

## 五、工程师视角的三个核心教训

### 教训 1：Prompt 结构是性能工程

Prompt 的组织方式不是随意填充，而是直接影响 Cache Hit 率的技术决策。静态内容前置、动态内容后置——这个原则在设计任何长期运行的 Agent 时都适用。

### 教训 2：MCP 动态工具集需要固定排序

如果你的 Agent 支持 MCP 工具，必须在初始化时建立固定的工具排序规则。否则中途工具变化会导致整个 Prompt 的 Cache失效，引发性能退化。

### 教训 3：合规约束会反向影响架构

ZDR 合规要求推动了 Codex 放弃 `previous_response_id` 的决定。这说明在企业场景中，安全和合规不是"额外考虑"，而是会直接影响核心架构设计的第一性约束。

---

## 总结

Codex Agent Loop 的工程实现揭示了软件 Agent 落地的三个核心技术挑战：

| 挑战 | Codex 的解决方案 | 可复用性 |
|------|----------------|---------|
| 长对话性能 | Prompt Caching + 结构化前缀 |⭐⭐⭐ |
| 上下文耗尽 | Compaction 自动压缩 | ⭐⭐⭐ |
| 合规约束 | 无状态设计 + ZDR | ⭐⭐ |

这三个设计决策的内在逻辑是：**在可靠性、性能、合规三者之间寻找动态平衡**，而非追求单一维度的最优。

---

**引用来源**：
- [Unrolling the Codex agent loop - OpenAI Engineering](https://openai.com/index/unrolling-the-codex-agent-loop/)
- [OpenAI Codex GitHub Repository](https://github.com/openai/codex)
- [Responses API Documentation](https://platform.openai.com/docs/api-reference/responses)

---

*本文属于 AI Agent 工程机制系列，关于 Harness Engineering 的更多讨论，参见 [Harness Engineering 专题](../harness/)。*