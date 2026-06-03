# OpenAI Responses API + Agents SDK：面向生产环境的 Agent 开发框架

> 本文深度解读 OpenAI 2026 年发布的 Responses API 与 Agents SDK，分析其从原型验证到生产可用的工程跨越，以及对现有 Agent 生态的实质性影响。

## 核心命题

OpenAI 终于正视了一个行业早已知晓的现实：让开发者从 Chat Completions API 手动拼装一个生产级 Agent，门槛远高于它应有的水平。Responses API + Agents SDK 的组合，本质上是 OpenAI 官方给出了**经过生产验证的多 Agent 编排范式**——不是 demo，不是教程，而是一个可以直接集成到生产系统的开源框架。

## 一、为什么需要 Responses API

### 1.1 现有 API 的分裂困境

在 Responses API 之前，OpenAI 的 Agent 相关能力分散在三个地方：

| API | 工具能力 | 状态 |
|-----|---------|------|
| Chat Completions | 无内置工具 | 需自行实现 Function Calling |
| Assistants API | 有工具（Code Interpreter、File Search） | Beta，迁移中 |
| 独立工具 API | 各自为政 | 无统一抽象 |

这种分裂意味着：同一个团队的 Agent 项目，有人用 Chat Completions + 手动拼接，有人用 Assistants API，代码风格、数据存储、追踪方式全部不统一。

### 1.2 Responses API 的统一设计

Responses API 的核心思路是：**用同一个 API 原语解决所有 Agent 构建需求**。

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search"}, {"type": "file_search"}],
    input="帮我查一下 Anthropic 最新发的 Agent Skills 规范"
)
```

一个调用里，模型可以自主决定是否需要调用 web search 或 file search，不需要你手动写循环、判断 tool_calls。

**这和 Assistants API 的本质区别是什么？** Assistants API 是"有状态的会话管理"（Thread/Run），而 Responses API 是"单次原子操作 + 工具协同"——前者适合需要一个长期上下文管理窗口的场景，后者更适合追求简单性和原子性的轻量 Agent 设计。

## 二、Agents SDK：多 Agent 编排的官方答案

### 2.1 从 Swarm 到 Agents SDK

OpenAI 此前有一个实验性框架 [Swarm](https://github.com/openai/swarm)，定位是"轻量多 Agent 编排的教育性探索"。现在 Swarm 已被标记为 **deprecated**，Agents SDK 是其生产级演进：

> "Swarm is now replaced by the OpenAI Agents SDK, which is a production-ready evolution of Swarm."

Agents SDK 的核心概念非常简洁：

**Agent = Instructions + Tools + Handoffs**

```python
from openai import Agents

# 定义一个 Agent
sales_agent = Agent(
    name="Sales Agent",
    instructions="你是一个销售助手，帮助客户了解产品",
    tools=[search_catalog, get_pricing],
    handoffs=[escalation_agent]  # 可转交给其他 Agent
)

# 定义路由逻辑
result = client.agents.run(
    agent=sales_agent,
    input="我想了解一下企业版的价格"
)
```

每个 Agent 拥有独立的指令、工具集和交接规则。LLM 在执行过程中可以**自主决定**：
- 调用哪个工具
- 是否需要转交给其他 Agent
- 何时结束任务

### 2.2 Handoffs：多 Agent 协作的核心机制

Handoffs（交接）是 Agents SDK 最值得关注的设计决策之一。它解决了一个关键问题：**Agent 之间的上下文传递**。

当一个 Agent 将任务转交给另一个 Agent 时，下一个 Agent 不仅接收用户的原始输入，还自动获得：
- 前一个 Agent 的执行历史
- 明确的任务背景说明（handoff 原因）
- 前一个 Agent 认为重要的上下文摘要

这比简单地把对话历史拼接给下一个 Agent 要聪明得多——它经过了前一个 Agent 的"总结提炼"，不是噪声传递。

**笔者认为**：Handoffs 机制是 Agents SDK 相比 LangGraph 等竞品最显著的差异化优势。LangGraph 的 state 传递是显式的、图结构化的，适合复杂工作流；Agents SDK 的 handoffs 是隐式的、智能的，适合以 LLM 为主导的协作流程。两者适用场景不同，但 Agents SDK 的方式对大多数场景更自然。

### 2.3 内置可观测性

生产级 Agent 系统最头疼的问题之一是**调试和追踪**。Agents SDK 集成了官方的 tracing 和 evaluation 工具：

```python
# 自动追踪每个 Agent 的决策路径
with client.agents.trace("order-processing") as trace:
    result = client.agents.run(agent=order_agent, input=user_input)
    # trace 中记录了每个工具调用、每次 handoff、每次决策
```

这个内置追踪能力，是 OpenAI 将 Responses API + Agents SDK 作为完整 Agent 开发平台的意图体现——不只是给 API，还给开发工具链。

## 三、Responses API 的内置工具集

### 3.1 Web Search

OpenAI 的 web search 工具直接集成在 Responses API 中，不需要你再调用第三方搜索 API：

```python
response = client.responses.create(
    model="gpt-4o",
    tools=[{"type": "web_search"}],
    input="2026 年 AI Agent 领域的主要技术趋势是什么？"
)
```

根据 OpenAI 公布的数据，在 SimpleQA 基准测试中，GPT-4o search preview 达到了 **90% 的准确率**，GPT-4o-mini search preview 达到了 **88%**。这个准确率水平意味着 web search 工具在大多数场景下可以作为可靠的"模型外部知识来源"。

### 3.2 File Search（向量检索）

这是 OpenAI 官方给出的 RAG 方案：

```python
response = client.responses.create(
    model="gpt-4o",
    tools=[{
        "type": "file_search",
        "vector_store_ids": ["vs_abc123"]
    }],
    input="我们公司的差旅政策是什么？"
)
```

支持多文件类型、query 优化、元数据过滤和自定义 reranking。根据 Navan（商务旅行平台）的实际使用案例，他们的 AI 旅行助手可以在无需额外调优的情况下，从公司知识库中精确回答员工的差旅政策问题。

### 3.3 Computer Use（CUA）

这是 OpenAI Operator 背后的核心技术（Computer-Using Agent）。在 Responses API 中以工具形式提供：

| 基准 | OpenAI CUA | Previous SOTA | 人类水平 |
|------|-----------|-------------|---------|
| OSWorld（通用计算） | **38.1%** | 22.0% | — |
| WebArena（Web 交互） | **58.1%** | 36.2% | 78.2% |
| WebVoyager（Web 交互） | **87.0%** | 56.0% | — |

CUA 在 OSWorld 上的 38.1% 意味着它在**不到一半的场景**下能可靠地完成通用计算任务。但 87% 的 WebVoyager 分数表明，在浏览器自动化场景下它已经相当可用。

**笔者认为**：CUA 目前最适合的场景是**浏览器自动化**（WebArena 58.1% 已超过大多数 RPA 方案），而非通用操作系统级自动化。企业在选型时需要明确这一点。

## 四、API 策略：对现有生态的影响

### 4.1 Assistants API 正式走向终点

OpenAI 明确给出了 Assistants API 的 sunset 时间线：**2026 年中正式废弃**，届时会提供完整的迁移指南。这意味着：

- 所有基于 Assistants API 构建的开发者需要在窗口期内迁移到 Responses API
- Assistants API 的核心能力（Code Interpreter、Thread 管理）将逐步迁移到 Responses API

### 4.2 Chat Completions 的定位

Chat Completions API 不会被废弃，但它的定位变成了"纯文本补全"——**不需要工具调用能力的场景**继续用它，需要工具/Agent 能力的场景迁移到 Responses API。

这个分层策略是合理的：Chat Completions 的简单性对于不需要 Agent 特性的场景仍然是最好的选择。

### 4.3 对第三方框架的影响

Agents SDK 的发布对 LangGraph、CrewAI、AutoGen 等框架意味着什么？

**竞争**：OpenAI 官方给出了"够用"的 Agent 编排方案，对于不需要复杂自定义工作流的团队，Agents SDK 的学习成本和集成成本都更低。

**共存**：Agents SDK 是一个相对轻量的方案，它不试图解决复杂的状态管理、持久化、多租户等问题。LangGraph 在这些复杂场景下仍然是更好的选择。

**生态整合**：实际上，许多团队已经在用 LangGraph 做工作流编排，同时底层调用 OpenAI API。Responses API 的工具化会让这种组合更自然。

## 五、安全与责任

OpenAI 公布了对 CUA 在 API 场景下的安全评估：

> "While these mitigations help reduce risk, the model is still susceptible to inadvertent mistakes, especially in non-browser environments."

他们新增的安全措施包括：
- Prompt injection 防护检查
- 敏感任务确认提示
- 隔离执行环境工具
- 潜在策略违规检测

但坦率地说，这些措施和 Claude Code 的 Security-Guidance Plugin 三层审查（Per-Edit 模式匹配 → End-of-Turn 模型审查 → Commit/Push 深层审查）相比，深度还有差距。OpenAI 的安全方案目前更偏向"提示层面"，而非 Claude Code 的"执行环境层面"。

## 六、总结：适合谁

| 场景 | 推荐方案 |
|------|---------|
| 快速原型，单 Agent + 工具 | **Responses API**，几行代码搞定 |
| 多 Agent 协作，需要 handoffs | **Agents SDK**，官方出品，开箱即用 |
| 复杂状态管理，持久化工作流 | LangGraph / CrewAI，生态更成熟 |
| 浏览器自动化（RPA 替代） | Responses API + Computer Use，当前可用 |
| 通用操作系统级自动化 | **暂不推荐**，CUA 38.1% OSWorld 成功率不够 |

**笔者认为**：OpenAI 这次发布的最大价值不是某个单一功能，而是**给出了生产级 Agent 开发的最小路径**——不需要在 LangChain、CrewAI、AutoGen 之间做选择，不需要自己实现 handoffs 和 tracing，用官方方案就能完成大多数 Agent 场景的开发。这对整个行业的 Agent 开发门槛是实质性降低。

---

*来源：*
- *[New tools for building agents - OpenAI](https://openai.com/index/new-tools-for-building-agents/)*
- *[Agents SDK Documentation - OpenAI](https://openai.github.io/openai-agents-python/multi_agent)*
- *[openai/openai-agents-python - GitHub](https://github.com/openai/openai-agents-python) (26,875 Stars)*
- *[openai/swarm - GitHub](https://github.com/openai/swarm) (deprecated, reference only)*
