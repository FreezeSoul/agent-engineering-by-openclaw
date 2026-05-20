# microsoft/agent-framework：微软生产级多语言 Agent 框架

> "Microsoft Agent Framework (MAF) is an open, multi-language framework for building production-grade AI agents and multi-agent workflows in .NET and Python."

## 一句话评价

**microsoft/agent-framework** 是微软最新的生产级 Agent 框架，Python + .NET 双语言支持，Graph-based workflow 编排，内置 OpenTelemetry 可观测性，支持 Foundry/ Azure OpenAI / OpenAI / GitHub Copilot SDK，瞄准从原型到生产的团队。

---

## 核心命题

多 Agent 系统从原型到生产最大的挑战不是"能不能跑起来"，而是**如何在保持架构灵活性的同时获得生产级能力**（checkpointing、restart、observability、human-in-the-loop、provider flexibility）。

MAF 的设计哲学：**开放架构 + 生产级能力 + 多语言一致性**。

---

## 目标用户

- 企业团队构建多 Agent 系统并期望投入生产
- 需要跨 Python/.NET 保持一致性的组织
- 已经使用 Azure Foundry 或 GitHub Copilot SDK 的团队
- 需要清晰迁移路径的 Semantic Kernel / AutoGen 用户

---

## 核心特性解析

### 1. 双语言一致性

Python 和 C#/.NET 实现**一致的 API 设计**：

```python
from agent_framework import Agent

agent = Agent(
    client=FoundryChatClient(credential=AzureCliCredential()),
    name="HaikuAgent",
    instructions="You are an upbeat assistant that writes beautifully.",
)
print(await agent.run("Write a haiku about Microsoft Agent Framework."))
```

```csharp
// .NET - 相同的概念模型
var agent = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential())
    .AsAIAgent(model: deploymentName, instructions: "You are an upbeat assistant that writes beautifully.", name: "HaikuAgent");

Console.WriteLine(await agent.RunAsync("Write a haiku about Microsoft Agent Framework."));
```

这对大型组织很重要——Python 数据科学团队和 .NET 后端团队现在可以共享同一套 Agent 设计模式。

### 2. Graph-Based Workflow Orchestration

MAF 支持四种核心编排模式：

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| **Sequential** | 按顺序执行，输出作为输入 | 管道式处理 |
| **Concurrent** | 并行执行，合并结果 | 独立并行任务 |
| **Handoff** | Agent 之间转移控制权 | 交接场景 |
| **Group Collaboration** | 多 Agent 协作完成同一目标 | 团队协作 |

> 包含 checkpointing、streaming、human-in-the-loop 和 time-travel 能力

### 3. Middleware 管道

```python
agent = Agent(
    client=client,
    middleware=[
        LoggingMiddleware(),      # 请求/响应日志
        ExceptionHandler(),       # 异常处理
        RateLimiter(),            # 限流
        CustomPipeline(),         # 自定义管道
    ]
)
```

灵活的 middleware 系统允许在请求/响应层面插入处理逻辑，与 Web 框架的 middleware 模式一致，降低了团队的学习成本。

### 4. Provider 灵活性

支持多种 LLM Provider，架构设计允许在不重写代码的情况下切换 Provider：

> 支持 Microsoft Foundry、Azure OpenAI、OpenAI 和 GitHub Copilot SDK，后续会增加更多

这意味着组织可以在早期使用 OpenAI 测试，后期迁移到 Azure OpenAI 或 Foundry，而不需要重写 Agent 代码。

### 5. Declarative Agents（YAML 定义）

```yaml
# declarative-agents/example.yaml
name: MyAgent
instructions: You are a helpful assistant
tools:
  - type: file_read
  - type: bash
  - type: web_search
```

通过 YAML 定义 Agent，快速设置和版本控制。对于需要频繁调整 Agent 配置的场景（运维、客服等），这提供了比代码更灵活的界面。

### 6. Observability（内置 OpenTelemetry）

```python
from agent_framework.observability import configure_tracing

configure_tracing(
    service_name="my-agent",
    otlp_endpoint="http://otel-collector:4317",
)
```

分布式追踪、监控、调试开箱即用。生产环境中，可观测性是调试多 Agent 行为的关键——MAF 没有假设你会用什么监控后端，而是通过标准 OTLP 协议兼容任何后端。

### 7. Foundry Hosted Agents（2行代码部署）

```python
# 仅需额外2行代码
from agent_framework.foundry import FoundryHostedAgent

agent = FoundryHostedAgent(name="production-agent")
agent.deploy()  # 部署到 Foundry 基础设施
```

这可能是 MAF 最实用的特性——团队可以本地开发调试，然后一键部署到 Azure Foundry 基础设施，省去自己管理 Agent 运行时的运维成本。

### 8. Agent Skills（知识库驱动的工具发现）

```python
# 从文件、代码库、类库构建领域知识库
agent = Agent(
    skills=Skills.from_sources([
        "path/to/documentation",
        "path/to/codebase",
        ClassLibraryToolProvider(MyDomainLibrary),
    ])
)
```

Agent Skills 允许为 Agent 构建可发现的专业知识库——这比传统的"给 Agent 塞 prompt"更结构化，也更容易维护。

### 9. AF Labs（前沿实验）

Labs 目录包含 benchmark、reinforcement learning 等前沿研究的实验包：

> 面向 benchmark、reinforcement learning 和研究举措的实验包

这是微软将研究转化为生产能力的信号——前沿研究可以通过 Labs 快速试用，成熟后进入主线框架。

---

## 与同类对比

| 框架 | 语言 | 核心差异 | 适用场景 |
|------|------|---------|---------|
| **microsoft/agent-framework** | Python + .NET | 双语言一致性、Foundry 集成、生产级完整性 | 企业团队、Azure 用户 |
| **LangGraph JS** | TypeScript | 固定拓扑、成熟 checkpointing | 需要确定性 workflow 的团队 |
| **CrewAI** | Python | 角色扮演、多 Agent 协作 | 快速原型、单语言 Python |
| **AutoGen/AG2** | Python | 成熟生态、广泛采用 | 已有 AutoGen 投入的团队 |

**关键区分**：MAF 的目标不是"最灵活"，而是"最完整"——它假设你在做生产部署，愿意用一致性换可靠性。

---

## 快速上手

```bash
# Python
pip install agent-framework

# .NET
dotnet add package Microsoft.Agents.AI
```

从 Hello World 到部署的完整路径：[Getting Started Guide](https://learn.microsoft.com/agent-framework/overview/agent-framework-overview)

**迁移路径**：
- 从 Semantic Kernel 迁移：有官方迁移指南
- 从 AutoGen 迁移：有官方迁移指南

---

## 引用

> "Microsoft Agent Framework is built for teams taking agents from prototype to production."
> — [GitHub README](https://github.com/microsoft/agent-framework)

> "MAF is a strong fit if you: need orchestration beyond a single prompt or stateless chat loop, want graph-based patterns such as sequential, concurrent, handoff, and group collaboration, care about durability, restartability, observability, governance, or human-in-the-loop control."
> — [GitHub README](https://github.com/microsoft/agent-framework)