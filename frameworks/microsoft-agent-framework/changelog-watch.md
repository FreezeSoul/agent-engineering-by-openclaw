# Microsoft Agent Framework Changelog Watch

> 追踪 Microsoft Agent Framework 版本变化与生态动态

---

## 更新记录

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
