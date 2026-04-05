# Microsoft Agent Framework Changelog Watch

> 追踪 Microsoft Agent Framework 版本变化与生态动态

---

## 更新记录

### 2026-04（v1.0 GA · 正式版）

**2026-04-03 · 生产就绪正式发布**

Microsoft Agent Framework v1.0 正式版GA发布，同时上线 .NET（NuGet: `Microsoft.Agents.AI`）和 Python（PyPI: `agent-framework`）。**承诺长期支持与向后兼容**。

**GA 关键变化**（相对于 RC）：
- **声明式 Agent（YAML）**：以版本控制的 YAML 文件定义 Agent 指令、工具、记忆配置和编排拓扑，一行 API 调用即可加载运行
- **A2A 协议支持**：Agent-to-Agent 协议实现跨运行时协作，Agent 可与运行在其他框架中的 Agent 通过结构化协议消息协调
- **MCP 深化集成**：Agent 可动态发现和调用 MCP 兼容服务器暴露的外部工具
- **Checkpoint/Hydration**：图工作流支持检查点保存与恢复，长时运行进程可从中断处继续

**核心功能集（GA 锁定）**：
| 能力 | 说明 |
|------|------|
| 单 Agent + Service Connectors | 统一 Agent 抽象，稳定跨 .NET/Python；原生连接 Foundry / Azure OpenAI / OpenAI / Claude / Bedrock / Gemini / Ollama |
| 中间件管道 | 内容安全过滤器、日志、合规策略——无需修改 Agent 提示词即可插入 |
| 记忆与上下文 | 可插拔架构：Foundry Agent Service Memory / Mem0 / Redis / Neo4j / 自定义存储 |
| Graph Workflows | 确定性、可持续复的工作流引擎：分支条件、并行展开、结果收敛 |
| 多 Agent 编排 | Sequential / Concurrent / Handoff / Group Chat / Magentic-One，全模式支持流式、检查点、人机审批、暂停/恢复 |
| Declarative Agents | YAML 驱动的声明式 Agent 定义 |

**上手示例**（Python）：
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

**生态定位确认**：
- Semantic Kernel（企业特性：状态管理、类型安全、中间件、遥测）→ 继承
- AutoGen（Agent 抽象：handoff、group chat）→ 继承
- Graph-based workflows → 新增（融合两者优势）

> 来源：[Microsoft DevBlogs - v1.0 GA Announcement](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/) | 2026-04-03

---

### 2026-03（Release Candidate · v1.0 RC）

**2026-03-25 · RC 状态确认**

Microsoft Agent Framework RC 确认发布，同时支持 .NET（NuGet: `Microsoft.Agents.AI`）和 Python（PyPI: `agent-framework`）。

**RC 关键信息**：
- **API 稳定**：v1.0 正式版前 API 不再变更
- **协议栈完整**：A2A（Agent-to-Agent）+ AG-UI（Streaming UI）+ MCP（Model Context Protocol）三协议原生支持
- **多语言统一**：.NET + Python 提供一致的开发体验
- **Graph-based workflows**：声明式多 Agent 编排，支持 sequential / concurrent / handoff / group chat 模式

**新增生态信息**：
- Interview Coach 参考应用已开源（Blazor UI + 多 Agent Handoff + MCP 外置工具）
- 与 Microsoft Foundry / Azure AI Agent Service / Aspire 深度集成
- 支持 Ollama、OpenAI、Azure OpenAI、GitHub Copilot、Anthropic Claude、AWS Bedrock 等多 Provider

**与 Semantic Kernel/AutoGen 关系**：
- Semantic Kernel（企业特性：状态管理、类型安全、中间件、遥测）→ 继承
- AutoGen（Agent 抽象：handoff、group chat）→ 继承
- Graph-based workflows → 新增（融合两者优势）

> 来源：[Microsoft Foundry Blog - RC Announcement](https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/) | [InfoQ](https://www.infoq.com/news/2026/02/ms-agent-framework-rc/) | [Nikiforovall Blog](https://nikiforovall.blog/dotnet/ai/2026/03/07/microsoft-agent-framework-workflows-mcp-a2a-agui.html)

---

### 2026-03（v1.0 初始版本）

**2026-03 · v1.0 正式发布**

Microsoft Agent Framework 首个正式版本发布，标志 Microsoft 官方 AI Agent 框架正式整合 Semantic Kernel + AutoGen 两条技术路线。

**核心发布内容**：
- **统一 Agent 抽象**：ChatClientAgent + handoff 模式
- **IChatClient 接口**：统一对接任意模型（Ollama、OpenAI、Azure OpenAI 等）
- **Graph Workflows**：声明式多 Agent 编排
- **生产集成**：OpenTelemetry、中间件管道、Aspire 编排
- **Interview Coach 示例**：生产级参考应用（Blazor UI + 多 Agent + MCP）

**框架定位**：
- Semantic Kernel 企业特性（状态管理、类型安全、中间件、遥测）→ 继承
- AutoGen Agent 抽象（handoff、group chat）→ 继承
- Graph-based workflows → 新增
- MCP 原生支持 → 新增

**生态意义**：
- 微软 .NET AI 开发从双框架并行进入统一框架时代
- MCP 成为 Microsoft 官方支持的工具协议
- Azure Foundry 成为推荐的 Agent 后端平台

> 来源：[Microsoft Developer Blog](https://developer.microsoft.com/blog/build-a-real-world-example-with-microsoft-agent-framework-microsoft-foundry-mcp-and-aspire) | [Gabriel Mongeon Blog](https://gabrielmongeon.ca/en/2026/03/microsoft-agent-framework-ollama-mcp/) | [Microsoft Agent Framework 官方](https://aka.ms/agent-framework)

---

*持续追踪中*
