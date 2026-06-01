# LangChain Agent Streams：从 Token 流到事件流的架构演进

> **核心命题**：LangChain 在 Interrupt 2026 上发布的「Agent Streams」代表了流式架构的根本转变——从面向单模型 Token 输出的流式 API，演进为面向图结构多智能体系统的**事件驱动流式协议**。这是 AI Agent 基础设施层面的一次重要范式升级。

---

## 背景：为什么 Token 流不够用了

传统流式 API 设计针对的是：**一次模型调用 = 一个 Token 流**。

这个模型在简单的 Chatbot 场景下工作良好，但当 Agent 演进到以下形态时，问题就出现了：

- **图结构**：Agent 需要委托子 Agent，形成树状任务图
- **工具调用**：每个步骤可能产生中间状态更新
- **可中断性**：需要暂停等待人类批准后再继续
- **多模态输出**：文本、结构化数据、媒体可能同时产生

将这些全部压缩进一个「Token Delta 流」意味着应用开发者需要自己在前端解析、重建、关联这些事件——这层复杂性不应该由应用层承担。

---

## Agent Streams 的四个核心设计

LangChain 提出的新流式原语围绕四个核心概念构建：

### 1. Namespaces（命名空间）

描述事件发生在 Agent 树的哪个位置：

- 根图（Root Graph）
- 嵌套子图（Nested Subgraph）
- Deep Agents 子 Agent

同一个 Channel 类型可以在不同命名空间发射事件而不丢失身份。这解决了「事件溯源」的核心问题——你总是知道这个事件来自哪里。

### 2. Typed Events（类型化事件）

不再是原始的 Token 块，而是带有类型的结构化事件：

```
AgentStarted, ToolCallStarted, ToolCallCompleted, 
HumanApprovalRequested, SubagentFinished...
```

类型系统让前端可以精确渲染不同类型的状态变化，而不需要解析文本内容。

### 3. Hierarchical Streaming（层级流）

子 Agent 的输出可以独立流式传输，同时保持与父级上下文的关联。前端可以同时渲染多个子 Agent 的进度，而不需要等待父 Agent 的完整响应。

### 4. Interrupt Compatibility（中断兼容）

事件流中明确标记了「暂停点」—— Human Approval Requested 这样的事件类型让前端可以精确地在正确的位置插入人工介入环节。

---

## 技术实现：基于 LangGraph 的流式原语

LangChain 的实现构建在 LangGraph 之上，每个图节点都可以发射带命名空间的事件。Deep Agents 运行时负责管理跨节点的上下文传递和状态持久化。

关键数据结构：

```python
# 事件携带命名空间和类型信息
Event(
    namespace=["root", "research_subagent"],
    type="ToolCallCompleted",
    data={...}
)
```

这种设计让流式传输层可以完整描述一个复杂 Agent 的执行过程，而不需要应用开发者自己实现事件重建逻辑。

---

## 为什么这很重要

流式架构的演进是 Agent 系统成熟的标志：

| 阶段 | 流式对象 | 前端复杂度 | 适用场景 |
|------|---------|-----------|---------|
| LLM Streaming | Token 块 | 低 | 单轮对话 |
| Agent Streams | 事件树 | 中 | 单 Agent 多步 |
| Graph Streams | 命名空间事件图 | 高 | 多 Agent 协作 |

Agent Streams 处于第二阶段向第三阶段过渡的关键节点。它让前端开发者可以用统一的方式处理多 Agent 场景下的流式状态，而不需要为每个新场景重新发明事件解析逻辑。

---

## 与 Project 的闭环

**Project**: [future-agi/future-agi](https://github.com/future-agi/future-agi)（1,065 Stars）— 开源 LLM/AI Agent 评估与观测平台，支持 Tracing、Evals、Simulations、Datasets

**闭环逻辑**：

- Agent Streams 解决的是**执行层的流式架构问题**——如何让多 Agent 的中间状态可观测、可中断
- future-agi 解决的是**评估层的观测基础设施问题**——如何对这些流式事件进行评估和优化

两者形成「执行可观测性 → 数据采集 → 评估改进」的闭环：Agent Streams 产生结构化事件，future-agi 消费这些事件进行评估和监控。

---

## 来源

- LangChain Blog: [From Token Streams to Agent Streams](https://www.langchain.com/blog/token-streams-to-agent-streams)
- LangChain Interrupt 2026 Overview: [Everything we shipped at Interrupt](https://www.langchain.com/blog/interrupt-2026-overview)