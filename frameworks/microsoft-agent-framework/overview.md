# Microsoft Agent Framework

> **本质**：微软将 Semantic Kernel（企业特性）与 AutoGen（Agent 抽象）合并为统一框架，为 .NET 开发者提供生产级 Agent 开发平台

## 核心定位

Microsoft Agent Framework 并非从零构建，而是整合两条已有技术路线的最佳实践：
- **AutoGen 遗产**：Agent 抽象、handoff 模式、group chat
- **Semantic Kernel 遗产**：IChatClient 接口、依赖注入、OpenTelemetry、中间件管道、状态管理

统一后的框架面向 .NET 开发者，提供：
- 一个框架替代两个（不再选择困难）
- ASP.NET 相同的托管模型和 DI 容器
- OpenTelemetry + 中间件 = 生产级可观测性
- Graph-based workflows 用于多 Agent 编排

## 关键概念

### IChatClient

统一模型接口，一次编写可在任意模型上运行：

```csharp
// 本地开发用 Ollama，生产切换 Azure OpenAI，只改配置
var chatClient = new OllamaChatClient(model: "llama3");
var agent = new ChatClientAgent(chatClient: chatClient, name: "assistant", instructions: "...");
```

### Handoff 模式

Agent 之间完全转移控制权的机制，与"Agent-as-Tool"的区别：

| 模式 | 说明 | 适用 |
|------|------|------|
| Agent-as-Tool | 主 Agent 调用辅助 Agent 完成任务，保留控制权 | 工具调用式协作 |
| Handoff | 当前 Agent 完全交出控制权，接收方接管对话 | 职责切换（如接待员→面试官）|

### Graph Workflows

声明式多 Agent 编排：

```csharp
var workflow = AgentWorkflowBuilder
    .CreateHandoffBuilderWith(triageAgent)
    .WithHandoffs(triageAgent, [receptionistAgent, behaviouralAgent, technicalAgent, summariserAgent])
    .Build();
```

## 生态集成

### 与 Microsoft Foundry

Foundry 是 Azure 上的 AI 应用平台，为框架提供：
- 统一模型端点（OpenAI / Meta / Mistral 等）
- 内容安全（moderation + PII 检测）
- 成本路由（自动选择最优模型）
- 企业治理（Entra ID + Defender）

### 与 Aspire

Aspire 是 .NET 云原生应用框架，负责：
- 服务发现（多 Agent 进程间自动感知）
- 健康检查（每个 MCP 服务器状态可观测）
- 遥测聚合（统一 OTEL 数据视图）
- 一键启动（`dotnet run` 启动整个系统）

### 与 MCP

工具在 Agent 外部独立部署（ MCP 服务器），通过 MCP 协议连接：
- **跨语言**：Python 工具服务 .NET Agent
- **解耦**：工具团队与 Agent 团队独立迭代
- **标准化**：符合 Model Context Protocol 规范

## 生产案例：Interview Coach

AI 模拟面试应用，展示生产级 Agent 架构：
- **5 Agent 分工**：Triage → Receptionist → Behavioral → Technical → Summarizer
- **MarkItDown MCP**：Python 解析 PDF/DOCX 简历
- **InterviewData MCP**：.NET 会话存储
- **Aspire 编排**：本地/云端统一开发体验

## 快速开始

```bash
# 安装
dotnet add package Microsoft.Agent.Component

# 基础 Agent
var agent = new ChatClientAgent(
    chatClient: new OllamaChatClient(model: "llama3"),
    name: "assistant",
    instructions: "You are a helpful assistant");

var response = await agent.RunAsync("Hello!");
```

## 链接

- 官方文档：https://aka.ms/agent-framework
- Interview Coach 示例：https://aka.ms/agentframework/interviewcoach
- GitHub：https://github.com/microsoft/agent-framework（预计）

## 标签

#microsoft #dotnet #agent-framework #semantic-kernel #autogen #foundry #aspire #handoff #multi-agent
