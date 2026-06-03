# openai-agents-python：官方多 Agent 编排框架，26.8k Stars 的生产级选择

> 26,875 Stars | GitHub Trending 常客 | 官方维护 | Python + JS/TS 双语言

## 核心命题

当你需要构建多 Agent 协作系统时，第一个问题是：**用哪个框架？** LangGraph 太重，CrewAI 学习曲线陡，AutoGen 偏向研究导向。openai-agents-python 给出了一个更直接的选择——**用 OpenAI 官方维护的框架来 Orchestrate 多 Agent 工作流**，轻量、文档完善、生产可用。

这个项目不只是一个 Python 库。它是 OpenAI Responses API 的编排层，也是 Swarm（已废弃）的生产级延续。

## 为什么关注这个项目

### 1. Sandbox Agents：让 Agent 真正能做长程任务

这是 v0.14.0 引入的最重要特性，也是它与上一代 Swarm 的本质区别。

传统 Agent 的问题是：给你一个 LLM、一些工具，但你让 Agent 去修改一个代码仓库，它怎么持久化工作状态？怎么跨 session 保持上下文？Sandbox Agents 给出了答案：

```python
from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
from agents.sandbox.entries import GitRepo
from agents.sandbox.sandboxes import UnixLocalSandboxClient

agent = SandboxAgent(
    name="Workspace Assistant",
    instructions="Inspect the sandbox workspace before answering.",
    default_manifest=Manifest(entries={"repo": GitRepo(
        repo="openai/openai-agents-python", ref="main"
    )}),
)

result = Runner.run_sync(
    agent,
    "Summarize what this project does",
    run_config=RunConfig(sandbox=SandboxRunConfig(client=UnixLocalSandboxClient()))
)
```

Sandbox Agent 可以：
- **检查文件系统**：读取仓库中的文件
- **运行命令**：执行 shell 命令
- **跨更长的时间跨度携带工作区状态**：任务中断后可以恢复

**笔者认为**：Sandbox Agents 的设计直接解决了"Agent 在真实代码库中工作"的核心工程问题。如果 Claude Code 是单 Agent 场景下的终极实践，Sandbox Agents 就是 OpenAI 对多 Agent 场景下"Agent 如何操作真实工作区"给出的官方答案。

### 2. Handoffs：Agent 协作的上下文传递机制

Handoffs 是 agents SDK 的核心概念之一——当一个 Agent 需要将任务转交给另一个 Agent 时，转交的不是原始对话历史，而是经过"智能压缩"的任务上下文：

```python
from agents import Agent

sales_agent = Agent(name="Sales", instructions="...", tools=[...], handoffs=[escalation_agent])
support_agent = Agent(name="Support", instructions="...", tools=[...])

# LLM 自动决定何时转交给哪个 Agent
result = client.agents.run(agent=sales_agent, input="我想升级到企业版")
```

**Handoffs 机制的关键价值**：
- 任务交接时，下一个 Agent 获得的不只是用户输入，还有前一个 Agent 的执行历史和背景说明
- 这避免了"把所有对话历史都给下一个 Agent"的噪声传递问题
- LLM 自主决定是否需要 handoff，不需要手动写复杂的路由逻辑

### 3. Guardrails：内置的安全检查层

生产环境里，Agent 接收不可信输入、输出不可控内容是最大风险之一。Agents SDK 内置了 Guardrails 机制：

```python
from agents import Agent, ModelSettings
from agents.guardrails import Guardrail, GuardrailResult

# 输入 Guardrail：验证用户输入
input_guardrail = Guardrail(
    name="profanity_check",
    logic=lambda input: not contains_profanity(input),
    action="block"
)

# 输出 Guardrail：验证模型输出
output_guardrail = Guardrail(
    name="PII_check",
    logic=lambda output: not contains_pii(output),
    action="block"
)

agent = Agent(
    name="Customer Assistant",
    instructions="You are a helpful customer assistant.",
    input_guardrails=[input_guardrail],
    output_guardrails=[output_guardrail]
)
```

Guardrails 是在 Agent 层面配置的，不是应用层事后检查。这是设计上的进步。

### 4. Sessions + Tracing：生产可观测性的基础设施

```python
# 自动会话历史管理
result = client.agents.run(agent=my_agent, input="继续上一话题")

# 内置 tracing
with client.agents.trace("order-processing") as trace:
    result = client.agents.run(agent=order_agent, input=user_input)
    # 每个工具调用、每次 handoff、每次决策都被追踪
```

Sessions 解决"跨 Agent 运行周期保持上下文"的问题，Tracing 解决"Agent 执行过程不透明"的问题。两者结合，才算有基本的生产可观测性。

### 5. Provider-Agnostic：不绑死在 OpenAI

虽然叫 openai-agents-python，但它支持的不只是 OpenAI API：

> "It is provider-agnostic, supporting the OpenAI Responses and Chat Completions APIs, as well as 100+ other LLMs."

这意味着你可以用同一个框架，换一个 API key 就能切换到 Anthropic、Azure、Google 等其他 LLM 提供商。对于不想被单一供应商绑死的团队，这个灵活性很重要。

## 技术规格

| 维度 | 数值/信息 |
|------|----------|
| Stars | **26,875**（截至 2026-06-03）|
| 语言 | Python（另有 JS/TS 版本 openai-agents-js，3,167 Stars）|
| 最低 Python 版本 | 3.10+ |
| 安装方式 | `pip install openai-agents` 或 `uv add openai-agents` |
| 核心依赖 | Pydantic、Requests、MCP Python SDK |
| 可选依赖 | websockets（Realtime 支持）、SQLAlchemy（Redis Session）、any-llm/LiteLLM（多 LLM 支持）|
| 活跃维护 | 持续更新中（v0.14.0 刚发布 Sandbox Agents）|

## 与竞品对比

| 维度 | openai-agents-python | LangGraph | CrewAI |
|------|---------------------|-----------|--------|
| **定位** | 轻量多 Agent 编排 | 复杂状态管理工作流 | 多 Agent 协作平台 |
| **学习曲线** | 低（官方文档完善）| 高（图结构复杂）| 中 |
| **Handoffs 机制** | ✅ 内置，智能上下文传递 | 需手动实现 | 部分支持 |
| **Sandbox 环境** | ✅ 内置（v0.14.0）| ❌ | ❌ |
| **Guardrails** | ✅ 内置 | ❌ | 部分 |
| **Provider 支持** | 100+ LLMs | 多 | 多 |
| **生产成熟度** | 高（OpenAI 官方维护）| 高 | 中 |
| **适合场景** | 快速构建多 Agent 协作 | 复杂图结构工作流 | 需要角色分工的 Agent 团队 |

**笔者认为**：openai-agents-python 最适合的场景是**需要快速构建多 Agent 协作、且不想在框架选型上花太多时间的团队**。它的上手成本最低，文档最完善，OpenAI 官方维护意味着和 Responses API 的集成是最无缝的。但如果你需要复杂的 DAG 工作流、状态持久化、多租户支持，LangGraph 仍然是更好的选择。

## 快速上手

```bash
# 安装
pip install openai-agents

# 或者用 uv（更快）
uv init && uv add openai-agents
```

```python
from openai import OpenAI
from agents import Agent, Runner

client = OpenAI()

# 定义一个 Agent
agent = Agent(
    name="Research Agent",
    instructions="你是一个研究助手，帮助用户搜索和分析信息",
    tools=[{"type": "web_search"}]
)

# 运行
result = Runner.run_sync(agent, "Anthropic 的 Agent Skills 规范是什么？")
print(result.final_output)
```

## 关联文章

本文与 **《OpenAI Responses API + Agents SDK：面向生产环境的 Agent 开发框架》** 配套阅读。该文详细分析了 Responses API 的统一设计思路、内置工具集（Web Search / File Search / Computer Use）以及 Assistants API 的 sunset 对现有生态的影响。

---

*来源：*
- *[openai/openai-agents-python - GitHub](https://github.com/openai/openai-agents-python) (26,875 Stars)*
- *[openai/openai-agents-js - GitHub](https://github.com/openai/openai-agents-js) (3,167 Stars)*
- *[Agents SDK Documentation](https://openai.github.io/openai-agents-python/)*
- *[New tools for building agents - OpenAI](https://openai.com/index/new-tools-for-building-agents/)*
