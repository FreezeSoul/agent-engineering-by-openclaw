# Deep Agents v0.5：为什么 Async Subagent 选择了 Agent Protocol 而非 ACP 或 A2A

> **核心问题**：LangChain 在 Deep Agents v0.5 中发布了异步 Subagent 功能——一个 Supervisor 可以并行启动多个远程 Subagent，继续与用户对话，并在结果就绪时收集结果。但更重要的是他们选择 Agent Protocol 的工程理由：ACP 为什么不行，A2A 为什么不够好。本文从这个具体的工程决策出发，拆解三种 Agent 通信协议的架构取舍，以及这背后的设计哲学。
>
> **读完能得到什么**：理解 Agent Protocol / ACP / A2A 三种协议的设计假设和适用场景；理解为什么异步任务模型对协议选择有决定性影响；获得在自托管和托管环境之间做协议选择的工程判断框架。

---

## 1. 从同步到异步：为什么 Subagent 需要「不阻塞」

在 Deep Agents 0.4 及之前，Subagent 是**内联（Inline）的**——Supervisor 启动一个 Subagent，然后**阻塞等待**它完成。这在 Subagent 任务只需几秒钟时没有问题。但随着 Agent 任务复杂度的增长，问题出现了：

- 深度研究任务：可能需要数分钟
- 大规模代码分析：涉及大量文件扫描
- 多步骤数据管道：跨多个系统的协调

这些任务所需的时间量级已经从「秒」变成「分钟甚至更长」。Supervisor 阻塞在 Subagent 上，意味着在这段时间内它**无法响应用户、无法处理其他请求、无法做其他工作**。

Deep Agents v0.5 的解法是**异步 Subagent**：

```
Inline Subagent：  Supervisor → [等待 Subagent 完成] → 继续
Async Subagent：   Supervisor → [立即返回 Task ID] → 继续处理其他事
                   (Subagent 在后台独立运行)
                   Supervisor → 定期查询 Task ID → 收集结果
```

这个变化带来了两个新特性：

1. **非阻塞执行**：Supervisor 不再被 Subagent 阻塞，可以并行处理多个任务
2. **有状态的跨交互**：Supervisor 可以向运行中的 Subagent 发送修正指令，Subagent 记住之前的上下文（而不像 Inline Subagent 那样每次从零开始）

---

## 2. 协议三选一：ACP 为什么出局

Deep Agents v0.5 的技术挑战不仅是「如何让 Subagent 异步运行」，而是**选择哪个通信协议**来与远程 Subagent 通信。LangChain 评估了三条路：ACP、A2A 和 Agent Protocol。

### 2.1 ACP（Agent Client Protocol）：Editor-to-Agent 的设计，不适合远程 Subagent

ACP 是专门为 **Editor-to-Agent 通信**设计的协议（比如 Claude Code 桌面应用与内置 Agent 的通信）。Deep Agents v0.5 指出了 ACP 的两个致命问题：

**问题一：同步 Session 模型**

ACP 的通信模式是：

```
Client → 发送 Prompt → 等待 Response → 完成
```

这是一个典型的请求-响应回合制。对于需要数分钟的后台任务，这个模型完全无法映射——Supervisor 不可能在那里等待数分钟。

**问题二：只支持 stdio 传输**

ACP 目前只支持 stdio transport，意味着远程 Agent 必须作为**本地子进程**运行。这与「异步 Subagent 部署在远程服务器上」的需求直接冲突。HTTP 支持在 ACP Roadmap 上，但尚未发布。

> **工程判断**：ACP 的设计假设是「本地、同步、短时」。这个假设对 Editor-to-Agent 场景是合理的，但对异步 Subagent 场景完全不适用。ACP 的约束不是 bug，是设计选择——但这个选择限制了它的适用范围。

### 2.2 A2A（Agent-to-Agent Protocol）：更接近，但太「宽」了

A2A 是 **Google/Microsoft 等推动的行业标准协议**，有完整的 HTTP 支持和原生的异步任务模型，理论上完全兼容 Deep Agents 的需求。Deep Agents v0.5 也明确表示 A2A「技术上是兼容的」。

但 LangChain 最终没有选择 A2A，原因是：

> **"Since async subagents are still evolving, we prioritized a protocol that allows for faster iteration."**

A2A 是一个**通用行业标准**，需要覆盖 Agent 发现、能力协商、推送/拉取订阅等多种场景。协议的宽泛性意味着它的演进速度受行业共识驱动，不如 LangChain 自有的协议灵活。

> **笔者观点**：这个选择揭示了一个重要的工程原则——**在快速迭代期，选择可演进性而非标准化**。A2A 是正确的长期目标，但 Deep Agents v0.5 的 Subagent 功能本身也在快速演进，选择一个能跟上自己节奏的协议是务实的决定。

---

## 3. Agent Protocol 为什么赢了

Agent Protocol 是 LangChain 自有的开放规范，是 LangGraph Platform 的底层协议。选择它的理由有三条，层层递进：

### 理由一：模型对齐

Agent Protocol 的核心抽象是：

```
Thread（线程）= 持有对话上下文
Run（运行）   = 启动工作时创建
```

这与 Deep Agents Subagent 的任务模型**直接对应**：

- Supervisor 创建一个 Thread 来持有 Subagent 的上下文
- 启动一个 Run 来触发 Subagent 工作
- 定期检查 Run 状态来获取结果

这个对齐不是巧合——Agent Protocol 本身就设计为服务于「有状态的 LLM Agent」场景。

### 理由二：状态ful 的 Mid-Task 更新

当 Supervisor 需要向运行中的 Subagent 发送修正指令（"update_async_task"）时：

- **Inline Subagent**：Supervisor 只能从完整的对话历史重新构建上下文
- **Async Subagent + Agent Protocol**：Supervisor 发送 update，Subagent 从 Thread 历史中恢复上下文，继续工作

这意味着 Subagent 真正记住了任务进展，而不是每次更新都重新开始。

### 理由三：跨托管和自托管部署

Agent Protocol 既支持托管服务（LangSmith），也支持自托管（FastAPI 服务）。这与 Deep Agents 作为 **Model-Agnostic 开放 Harness** 的定位完全一致——Deep Agents 要支持任何部署方式，不能被单一协议的传输层限制。

---

## 4. Async Subagent 的架构含义

Deep Agents v0.5 还展示了 Async Subagent 带来的一种新架构模式：**异构部署（Heterogeneous Deployments）**。

在 Inline Subagent 模式下，Supervisor 和 Subagent 通常部署在同一环境、使用相同模型。但 Async Subagent 解耦了这个约束：

```
Supervisor（轻量级）→ 调度任务
Subagent A（GPU 实例，Claude Sonnet）→ 深度代码分析
Subagent B（CPU 实例，GPT-4）→ 文档检索
Subagent C（专用硬件，Gemini）→ 多模态处理
```

每个 Subagent 可以使用**不同的硬件、不同的模型、不同的工具集**，专注于自己的任务类型。这是 Inline Subagent 完全无法实现的能力。

---

## 5. Async Subagent 工具接口

Deep Agents v0.5 为 Async Subagent 定义了 5 个工具，这是 Supervisor 与 Subagent 交互的完整接口：

| 工具 | 作用 |
|------|------|
| `start_async_task` | 立即返回 Task ID，Subagent 在后台独立运行 |
| `check_async_task` | 查询 Task 状态并在完成后获取结果 |
| `update_async_task` | 向运行中的 Task 发送修正指令 |
| `cancel_async_task` | 取消正在运行的 Task |
| `list_async_tasks` | 列出所有追踪中的 Task 及其当前状态 |

这个接口的设计遵循了**命令查询分离（CQS）原则**：start/update/cancel 是命令（改变状态），check/list 是查询（不改变状态）。这是一个干净的任务管理接口。

---

## 6. 这个选择对工程实践的启示

Deep Agents v0.5 的协议选择揭示了一个对 Agent 架构师重要的判断框架：

| 维度 | ACP | A2A | Agent Protocol |
|------|-----|-----|----------------|
| **传输层** | stdio only | HTTP | HTTP |
| **通信模型** | 同步请求-响应 | 异步任务 | 异步任务 |
| **适用场景** | Editor-to-Agent | Agent 互操作（通用） | 自有 Agent 服务编排 |
| **演进速度** | 中（行业协议） | 慢（标准协议） | 快（LangChain 控制） |
| **状态ful 支持** | 无 | 有 | 有 |

> **工程建议**：如果你的 Agent 系统与外部 Agent 通信（跨组织边界），选 A2A。如果你的 Agent 系统是内部的自有服务编排，选 Agent Protocol。如果你的 Agent 是 Editor 内置的本地 Agent，选 ACP。

---

## 7. 与仓库现有文章的关系

| 文章 | 与本篇文章的关系 |
|------|----------------|
| `agentdm-mcp-a2a-protocol-bridge.md` | AgentDM 桥接 MCP 和 A2A；本文是纯 A2A vs ACP vs Agent Protocol 的内部取舍分析 |
| `anthropic-multi-agent-research-system-architecture-2026.md` | Anthropic 的 Lead-Subagent 模式是并行执行，但未涉及协议选择；本文提供了协议取舍的工程视角 |
| `open-harness-memory-lock-in-2026.md` | Deep Agents 是 Model-Agnostic 开放 Harness 的代表；本文展示了它的协议层设计选择 |

---

*参考文献：[Deep Agents v0.5](https://blog.langchain.com/deep-agents-v0-5/)（LangChain Blog，2026-04-14）；[Agent Protocol 规范](https://agentprotocol.ai/)*
