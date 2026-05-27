# langchain-ai/deepagents：来自 LangChain 的生产级 Agent Harness

> 项目来源：[GitHub langchain-ai/deepagents](https://github.com/langchain-ai/deepagents)（23,434 Stars，MIT License）
>
> 官方文档：[Deep Agents Documentation](https://docs.langchain.com/oss/python/deepagents/overview)
>
> 本文与 **OpenAI self-improving tax agents with Codex** 文章关联，主题：Harness Engineering 中的 eval loop 与生产 trace 机制。

---

## 核心命题

当 Agent 系统从实验室走向生产环境，最大的问题不是「Agent 够不够聪明」，而是**「如何让 Agent 的每次执行都变得可观测、可评估、可改进」**。

langchain-ai/deepagents 是 LangChain 官方开源的一个「生产级 Agent Harness」——一个开箱即用、默认配置已经为长时序、多步骤任务优化过的 Agent 框架。它的定位不是又一个 Agent 框架，而是**一个经过生产验证的 Harness 实现**，体现了 LangChain 对 Eval Loop、工程机制和上下文管理的完整理解。

---

## 为什么这个项目值得关注

### 1. 它是 Harness 工程思想的完整实现

当前 Agent 开源社区中，「Harness」这个概念经常被误解为「安全防护」或「沙盒隔离」。但从 OpenAI 和 LangChain 的实践来看，**Harness 是一个更完整的工程框架**，包含：

- **评估器循环（Evaluator Loop）**：有明确的成功条件和验证标准
- **生产 Trace**：每次执行都有完整的路径记录，从输入到最终输出
- **上下文管理**：防止长对话中的 context overflow
- **权限分层**：Human-in-the-loop 机制，敏感操作需要人工确认
- **记忆持久化**：跨会话的状态恢复

Deep Agents 的设计直接体现了这些原则：

| Harness 机制 | Deep Agents 实现 |
|-------------|-----------------|
| Evaluator Loop | 集成 LangSmith，第一class tracing + evaluation |
| Production Trace | LangGraph 持久化/checkpointing，每次执行都有轨迹记录 |
| Context 管理 | summarize 长线程，工具输出 offload 到磁盘 |
| Human-in-the-loop | `Tool interrupt` 机制，敏感工具调用前可暂停等待确认 |
| 记忆持久化 | Pluggable state 和 store 后端，支持跨会话 recall |
| 工具安全 | 沙盒化 Shell 访问，支持本地/sandboxed/远程多种后端 |

### 2. LangGraph 原生，第一class Eval 支持

Deep Agents 构建在 LangGraph 之上，这意味着：

- **Streaming**：流式输出，用户体验好
- **Persistence**：状态持久化，支持 Checkpointing
- **Evaluation**：与 LangSmith 无缝集成，有现成的 eval 框架

它的 Eval 支持包括：
- **Behavioral evaluation suite**：端到端测试，运行 agent 对真实 LLM 并断言轨迹（工具调用、最终文本、文件变更）
- **外部基准集成**：FRAMES、Nexus、BFCL v3 等公开基准
- **LLM-as-judge**：`SuccessAssertion` 使用 `openevals` 做 LLM 评判
- **Harbor 集成**：提供沙盒环境（Docker、Modal、Daytona、E2B 等）和自动评分

### 3. 可插拔架构，不是又一个「全家桶」

Deep Agents 的核心理念是「opinionated but extensible」——默认配置已经为生产优化，但任何组件都可以被替换：

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[my_custom_tool],          # 替换或新增工具
    system_prompt="You are...",       # 自定义 prompt
    filesystem=my_backend,            # 替换文件系统后端
    store=my_memory_backend,           # 替换记忆后端
    sub_agents=custom_subagents,       # 自定义子 Agent
)
```

这种设计让 Deep Agents 成为一个**好的起点，而不是一个封闭的系统**。

---

## 技术架构图

```
User Input
    ↓
Deep Agent (create_deep_agent)
    ├── Model (any LLM with tool calling)
    ├── Tools (custom / MCP / built-in)
    ├── Sub-Agents (isolated context windows)
    ├── Filesystem (local / sandboxed / remote)
    ├── Context Manager (summarize + offload)
    ├── Persistent Memory (cross-session recall)
    ├── Human-in-the-loop (Tool interrupt)
    └── Skills (loadable behaviors)
         ↓
    LangGraph Runtime
         ├── Streaming
         ├── Checkpointing (persistence)
         └── Tracing → LangSmith
              ↓
         Eval / Harbor
              ↓
         Harbor Score (0.0 - 1.0)
```

---

## 与本文的关联

在 [OpenAI self-improving tax agents with Codex]() 中，我分析了 OpenAI 的三段式闭环：

```
practitioner's correction → production trace → tailored evals → Codex iteration
```

这个闭环得以运转的前提是：**Harness 机制必须足够完整**——有 Trace、有 Eval、有权限边界、有上下文管理。

langchain-ai/deepagents 提供了这套 Harness 机制的开源实现参考。如果你想在 LangChain 生态内实现类似的 eval loop，Deep Agents 是一个可以直接基于的起点。

---

## 适用场景

| 场景 | 是否适合 |
|------|---------|
| 需要长时序 Agent 任务的生产环境 | ✅ 专为长时序优化 |
| 需要完整的 Eval/Tracing 体系 | ✅ LangSmith 原生集成 |
| 团队没有精力自建 Harness 机制 | ✅ 开箱即用的默认配置 |
| 需要 Human-in-the-loop 控制 | ✅ Tool interrupt 机制 |
| 想要快速原型但不想被框架锁定 | ✅ 可插拔架构 |

---

## 引用

> Deep Agents is an open source agent harness — an opinionated agent that runs out of the box. Extend, override, or replace any piece.
>
> — [Deep Agents README](https://github.com/langchain-ai/deepagents)

> The batteries-included agent harness. Built on LangGraph (streaming, persistence, checkpointing) with first-class tracing, evaluation, and deployment via LangSmith.
>
> — [Deep Agents README](https://github.com/langchain-ai/deepagents)