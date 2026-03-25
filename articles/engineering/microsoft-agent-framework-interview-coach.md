# Microsoft Agent Framework：Semantic Kernel + AutoGen 合并的生产实践

> **本质**：微软将 Semantic Kernel 的企业特性与 AutoGen 的 Agent 抽象融合为统一框架，并通过 Interview Coach 示例展示 MCP + Aspire 的多 Agent 编排工程路径

> **来源**：[Microsoft Developer Blog](https://developer.microsoft.com/blog/build-a-real-world-example-with-microsoft-agent-framework-microsoft-foundry-mcp-and-aspire) | 2026-03

## 一、背景：为什么是"合并"而不是"新造"

微软在 .NET AI 开发领域长期并行维护两个框架：
- **Semantic Kernel**：企业级特性（状态管理、类型安全、中间件、遥测）
- **AutoGen**：Agent 抽象（多 Agent 对话、handoff、group chat）

两者各有优势，但用户面临选择困难。**Microsoft Agent Framework** 并非从零构建，而是将两者优势整合：
- 继承 AutoGen 的 Agent 抽象和对话模式
- 叠加 Semantic Kernel 的企业级特性（DI、IChatClient、OTel）
- 新增 graph-based workflows 用于多 Agent 编排

这意味着：**已在使用 Semantic Kernel 或 AutoGen 的团队，可以平滑迁移到统一框架。**

## 二、核心特性：企业级 + Agent 原生

| 特性 | 来源 | 说明 |
|------|------|------|
| 统一 IChatClient 接口 | Semantic Kernel | 一个接口对接所有模型，替换成本低 |
| 依赖注入 | Semantic Kernel | 与 ASP.NET 生态无缝集成 |
| OpenTelemetry | Semantic Kernel | 生产级可观测性开箱即用 |
| 中间件管道 | Semantic Kernel | 请求/响应拦截，安全/日志即插即用 |
| Handoff 模式 | AutoGen | Agent 之间转移控制权 |
| Group Chat | AutoGen | 多 Agent 并行讨论 |
| Graph Workflows | 新增 | 声明式多 Agent 编排 |

## 三、Interview Coach：五 Agent Handoff 生产示例

Interview Coach 是一个 AI 模拟面试应用，用户提交简历 + 职位描述，Agent 自动完成：
1. 收集信息（简历解析 + 职位理解）
2. STAR 法则行为面试
3. 技术面试
4. 生成面试评估报告

### 3.1 五 Agent 分工

```
Triage Agent（路由）
  ↓ handoff
Receptionist Agent（接待：收集简历 + 职位）
  ↓ handoff
Behavioral Interviewer Agent（STAR 行为面试）
  ↓ handoff
Technical Interviewer Agent（技术面试）
  ↓ handoff
Summarizer Agent（生成评估报告）
  ↓ handoff
Triage Agent（重新路由）
```

| Agent | 角色 | 工具 | 特殊设计 |
|-------|------|------|---------|
| Triage | 路由器 | 无 | 纯路由，不执行业务逻辑 |
| Receptionist | 接待 | MarkItDown（简历解析）+ InterviewData（会话存储）| 只拿到需要的工具 |
| Behavioral | 行为面试 | InterviewData | 只读会话 |
| Technical | 技术面试 | InterviewData | 只读会话 |
| Summarizer | 评估报告 | InterviewData | 只读写报告 |

**关键设计**：Triage Agent 始终是 fallback——任何 Agent 发现偏离脚本时，自动 handoff 回 Triage 重新路由。这解决了纯顺序流程无法应对异常的问题。

### 3.2 Handoff 代码

```csharp
var workflow = AgentWorkflowBuilder
    .CreateHandoffBuilderWith(triageAgent)
    // 每个 Agent 可以 handoff 到谁
    .WithHandoffs(triageAgent, [receptionistAgent, behaviouralAgent, 
                                technicalAgent, summariserAgent])
    .WithHandoffs(receptionistAgent, [behaviouralAgent, triageAgent])
    .WithHandoffs(behaviouralAgent, [technicalAgent, triageAgent])
    .WithHandoffs(technicalAgent, [summariserAgent, triageAgent])
    .WithHandoff(summariserAgent, triageAgent)
    .Build();
```

这是声明式的，比手写状态机更易读。底层由 AutoGen 的 handoff 机制驱动。

### 3.3 MCP 外置工具：跨语言解耦

Interview Coach 中的两个 MCP 服务器：
- **MarkItDown**（Python）：解析 PDF/DOCX 为 Markdown
- **InterviewData**（.NET）：SQLite 会话存储

工具不在 Agent 内部，而在独立进程中，通过 MCP 协议连接。这种设计：
- **工具团队与 Agent 团队解耦**：MCP 服务器可独立迭代
- **跨语言**：Python 工具服务 .NET Agent，无需统一技术栈
- **语言无关性**：同一 MCP server 可被任何框架调用

```csharp
var receptionistAgent = new ChatClientAgent(
    chatClient: chatClient,
    name: "receptionist",
    instructions: "You are the Receptionist...",
    tools: [.. markitdownTools, .. interviewDataTools]);
```

每个 Agent 只拿到它需要的工具——遵循最小权限原则。

### 3.4 Aspire 编排：本地/云端统一开发体验

Aspire（.NET 云原生应用框架）负责：
- **服务发现**：多进程之间相互感知，无需手动配置端口
- **健康检查**：每个 MCP 服务器状态可观测
- **遥测聚合**：所有服务的 OTEL 数据汇入统一视图
- **一键启动**：`dotnet run` 启动整个分布式系统

这解决了"本地 OK 云端 NO"的问题——开发环境和生产环境使用相同的声明式配置。

## 四、与 Foundry 的集成：企业级 AI 基础设施

Microsoft Foundry 是 Azure 上的 AI 应用平台，为 Agent Framework 提供：
- **统一模型端点**：OpenAI、Meta、Mistral 等一个接口
- **内容安全**：内置 moderation + PII 检测
- **成本路由**：自动选择最优模型
- **企业治理**：Entra ID + Microsoft Defender

关键点：`IChatClient` 接口让 Foundry 成为配置选择而非代码耦合——本地开发用 OpenAI，生产切 Foundry，只需改配置。

## 五、工程启示录

### 5.1 Handoff vs Agent-as-Tool

| 模式 | 适用场景 | 控制权 |
|------|---------|--------|
| Agent-as-Tool | 主 Agent 调用辅助 Agent 执行特定任务 | 主 Agent 保留控制权 |
| Handoff | Agent 之间需要完全交接（职责切换）| 交出控制权 |

Interview Coach 中从接待员到面试官就是典型 handoff——新 Agent 需要完全接管对话上下文。

### 5.2 MCP 作为工具边界

MCP 解决了工具归属问题：
- 工具在 Agent 外部独立部署
- 工具团队与 Agent 团队解耦
- 工具是语言无关的服务

这比在 Agent 代码中硬编码工具更符合微服务哲学。

### 5.3 Aspire 的价值

Aspire 本质是一个分布式应用的仪表盘 + 启动器。对于多 Agent 系统：
- 每个 Agent 可以是独立进程
- Aspire 统一管理生命周期
- 健康状态一目了然

## 六、局限性

- **.NET 生态锁定**：目前主要面向 .NET 开发者
- **Interview Coach 仍是示例**：生产级稳定性需自己验证
- **Foundry 依赖**：完整能力需要 Azure Foundry，不是纯开源路径
- **Handoff 调试复杂**：多 Agent 流转时的状态追踪比单 Agent 更难

## 七、链接

- 官方文档：https://aka.ms/agent-framework
- Interview Coach 示例：https://aka.ms/agentframework/interviewcoach
- Microsoft Foundry：https://learn.microsoft.com/azure/foundry/what-is-foundry
- MCP 官网：https://modelcontextprotocol.io/

## 标签

#microsoft #agent-framework #semantic-kernel #autogen #mcp #aspire #foundry #dotnet #handoff-pattern #multi-agent #production-patterns
