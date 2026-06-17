# microsoft/agent-framework：微软生产级多语言 Agent 框架

> "Microsoft Agent Framework is an open, multi-language framework for building production-grade AI agents and multi-agent workflows in .NET and Python."
> — [GitHub README](https://github.com/microsoft/agent-framework)

## 核心命题

2025 年 10 月微软把 Semantic Kernel 和 AutoGen 的核心能力合并成一个 SDK 时，业界还在观望。2026 年 4 月，这个框架达到 1.0——**生产就绪**，稳定 API，长期支持承诺。11428 Stars，Python + C# 双语言，跨 Foundry / Azure OpenAI / OpenAI / Anthropic Claude / Amazon Bedrock / Google Gemini / Ollama 全支持。

这个框架解决了一个实际问题：**企业想把 agents 从原型推到生产时，市面上没有统一的生产级方案**。Agent Framework 1.0 是微软给出的答案。

## 为什么这个框架值得关注

**第一，多语言不等于两个 SDK**。市面上多数框架声称"多语言"，实际上 Python SDK 和 C# SDK 是两套不同的抽象、不同的 API、不同的行为。Microsoft Agent Framework 的设计目标是**同一个抽象、同一套 API 行为**，Python 和 C# 都能用 `SequentialBuilder` / `ConcurrentBuilder` 构建 workflow，差异只在语言语法层面。

**第二，A2A + MCP 双协议支持**。MCP 让 agent 调用外部工具（Model Context Protocol），A2A 让 agent 之间互相通信。Agent Framework 1.0 同时支持两者，且 A2A 1.0 支持已在路线图上。这在生产环境中意味着：你的 agents 可以调用 MCP 服务器暴露的工具，也可以和其他框架里运行的 agents 协作——而不被锁定在单一生态。

**第三，Checkpointing 和长时间运行工作流**。这是生产级的关键特性： workflow 在执行过程中可以被打断（网络故障、人类审批、超时），然后从中断点恢复，而不是从头重来。微软的表述是"checkpointing and hydration ensure long-running processes survive interruptions"——这在真正的业务场景中不是可选项，是必选项。

**第四，Declarative Agents（YAML 定义）**。用 YAML 文件定义 agent 的指令、工具、记忆配置和编排拓扑，版本控制，一次 API 调用加载运行。好处是 agent 的行为可以被 code review，而不只是代码本身。

## 关键能力一览

| 能力 | 说明 |
|------|------|
| 多 Provider | Foundry / Azure OpenAI / OpenAI / Claude / Bedrock / Gemini / Ollama |
| 编排模式 | Sequential / Concurrent / Handoff / Group Chat / Magentic-One |
| Checkpointing | 长时间工作流中断恢复 |
| Middleware | 请求/响应拦截，内容安全过滤器，日志，合规策略 |
| Memory | Foundry / Mem0 / Redis / Neo4j 或自定义存储 |
| Observability | 内置 OpenTelemetry 集成，分布式追踪 |
| Declarative Agents | YAML 定义，版本控制，可 code review |
| DevUI | 交互式开发 UI，测试和调试 workflow |

## 与竞品的差异化定位

笔者认为，Agent Framework 的定位介于"轻量级单 agent SDK"（如 smolagents）和"重量级图编排引擎"（如 LangGraph）之间。它的目标不是取代这些框架，而是**覆盖企业从原型到生产的路径上那些中间阶段的工程需求**——多语言一致性、生产级耐久性和可观测性、微软生态的深度集成（Foundry、Azure）。

如果你的团队在用 .NET + Python 混合开发，或者已经在微软生态里（Azure / Foundry），Agent Framework 1.0 的迁移成本和集成成本都更低。如果你只需要快速跑一个单 agent 原型，其他轻量框架更合适。

## 快速上手

Python：

```bash
pip install agent-framework
```

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

agent = Agent(
    client=FoundryChatClient(
        project_endpoint="https://your-project.services.ai.azure.com",
        model="gpt-5.3",
        credential=AzureCliCredential(),
    ),
    name="HelloAgent",
    instructions="You are a friendly assistant."
)
print(asyncio.run(agent.run("Write a haiku about shipping 1.0.")))
```

多 agent 工作流：

```python
from agent_framework import Agent
from agent_framework.orchestrations import SequentialBuilder

writer = Agent(name="writer", instructions="You are a concise copywriter.")
reviewer = Agent(name="reviewer", instructions="You are a thoughtful reviewer.")

workflow = SequentialBuilder(participants=[writer, reviewer]).build()
```

## 数据来源

- **GitHub**: [microsoft/agent-framework](https://github.com/microsoft/agent-framework), 11,428 Stars, MIT License
- **Blog**: [Microsoft Agent Framework Version 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/), April 3, 2026
- **Docs**: [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)