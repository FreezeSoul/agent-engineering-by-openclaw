# Microsoft Agent Framework 1.0：语义 Kernel + AutoGen 统一SDK的企业级多 Agent 编排

## 核心命题

Microsoft Agent Framework 1.0 是目前企业级多 Agent 编排领域里，唯一同时具备图模型工作流、MCP 工具层、A2A 1.0 协议支持，并且提供 DevUI 可视化调试的生产级 SDK——而它的前身，是两个相互独立演进了数年、在不同开发者群体中各占山头的框架：Semantic Kernel 和 AutoGen。

---

## 一、背景：为什么这个 1.0 值得写

2024 年到 2025 年，Microsoft 在 Agent 框架领域实际上是「两套并行叙事」：

- **Semantic Kernel**：面向企业 .NET 开发者，提供稳定的状态管理、中间件、类型安全，与 Azure Foundry 深度绑定
- **AutoGen**：来自 Microsoft Research，面向 Python 开发者，以多 Agent 对话编排为核心创新

两套框架各自积累了大量用户，但在生产环境中，企业往往面临「两个框架选哪个」的二选一困境，以及跨框架协作的互操作问题。

Agent Framework 1.0（2026 年 4 月 3 日 GA）是对这个问题的正式回答：**把两者合二为一，同时补上 MCP（工具发现层）和 A2A（Agent 间协作层）两个协议缺口**。

> "We set out to unify the enterprise-ready foundations of Semantic Kernel with the innovative orchestrations of AutoGen into a single, open-source SDK."
> — [Microsoft Agent Framework Version 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)

---

## 二、核心设计决策

### 2.1 图模型取代对话模型

AutoGen 的核心抽象是「对话线程」——Agent 之间通过相互发送消息来协作。这个模型直观，但对于需要明确执行顺序、并行分支、或条件路由的生产系统来说，调试和可视化都是挑战。

Agent Framework 的答案是**图模型（Graph-based Workflows）**：把 Agent 和函数作为节点，用有向边连接，显式声明执行顺序和依赖关系。

优势：
- 执行顺序可推演，添加单节点超时、重试逻辑
- 分支、并行扇出、结果收敛都能用图上的结构表达
- **DevUI 调试器**：浏览器内可视化查看整个工作流的执行状态，这是 LangChain/LangGraph 没有的开发者体验

> "The graph model has clear advantages for production systems. You can reason about execution order, add timeouts to individual nodes, implement retry logic for specific agents, and visualize the entire workflow before running it."
> — [Microsoft Agent Framework 1.0: .NET and Python 2026](https://www.digitalapplied.com/blog/microsoft-agent-framework-1-0-dotnet-python-guide)

### 2.2 MCP + A2A 双协议支持

Agent Framework 1.0 同时支持两个正在形成标准的协议：

- **MCP（Model Context Protocol）**：让 Agent 动态发现和调用外部工具（由 MCP 合规服务器暴露）
- **A2A（Agent-to-Agent Protocol）**：让跨运行时边界的 Agent 相互协作——即你的 Python 团队和 .NET 团队各自构建的 Agent 可以通过结构化消息协议通信

官方表述中 MCP 是「现在可用」，A2A 1.0 是「即将到来」——但这个组合战略意图很清晰：先拿下工具层，再用 A2A 打通 Agent 间协作层。

> "MCP support lets agents dynamically discover and invoke external tools exposed over MCP-compliant servers. A2A 1.0 support coming soon."
> — [Microsoft Agent Framework Version 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)

### 2.3 多语言支持（Python + .NET）

| 维度 | Python | .NET |
|------|--------|------|
| 包管理 | `pip install agent-framework` | `dotnet add package Microsoft.Agents.AI` |
| 核心类型 | `Agent`, `FoundryChatClient` | `AIProjectClient`, `AsAIAgent` |
| 模型支持 | Azure Foundry, Azure OpenAI, OpenAI, Anthropic, Ollama | 同上 |

这不是「两套 API」，而是同一个抽象层在两种语言里的投射——API 设计思路一致，降低了多语言团队的学习成本。

---

## 三、多 Agent 编排模式

Agent Framework 1.0 支持六种编排模式，全部支持流式输出、检查点（checkpointing）和人类介入（human-in-the-loop）：

1. **Sequential**：顺序执行
2. **Concurrent**：并行执行
3. **Handoff**：Agent 间交接
4. **Group Chat**：群组对话
5. **Magentic-One**：Microsoft 研究院的开源多 Agent 自主系统
6. **Declarative Agents & Workflows（YAML）**：声明式工作流

---

## 四、与竞品对比

| 维度 | Microsoft Agent Framework | Claude Agent SDK | LangGraph | CrewAI |
|------|--------------------------|-----------------|-----------|--------|
| 许可证 | MIT | MIT | MIT | MIT |
| 语言 | Python, .NET | Python, TypeScript | Python, JS/TS | Python only |
| LLM 支持 | Azure Foundry, OpenAI, Anthropic, Ollama | Claude 模型专有 | Any（通过 LangChain） | Any（通过 LiteLLM） |
| MCP 支持 | 内置客户端 | 原生完整生态 | 通过集成 | 部分（插件） |
| A2A 协议 | A2A 1.0 即将到来 | 尚未支持 | 实验性 | 尚未支持 |
| 多 Agent 模型 | 有向图 | 托管式（层次化） | 状态图 | 角色扮演 crews |
| DevUI 调试器 | ✅ 有 | ❌ 无 | LangSmith（开发时调试） | ❌ 无 |
| 适用场景 | **企业多 Agent 生产系统** | Claude 生态内编码 Agent | 状态流编排 | 角色化 crew 协作 |

---

## 五、什么时候用

**用 Agent Framework 当：**
- 你的团队需要多 Agent 协作，且需要可推演的执行路径
- 你需要 DevUI 这样的开发时可视化调试工具
- 你需要 MCP + A2A 双协议支持，或者你的组织已经在用 Microsoft 生态（Azure Foundry、.NET）
- 你在从 Semantic Kernel 或 AutoGen 迁移（官方提供了迁移指南）

**用 Claude Agent SDK 当：**
- 你的工作流深度绑定 Claude 模型和 Claude Code 生态
- 你优先需要的是 CLI 工具链而非企业 SDK

---

## 关联闭环

本文与以下内容形成闭环：

- **Anthropic「2026 Agentic Coding Trends Report」**：报告揭示 40% 复杂任务已采用多 Agent 编排（其中重构任务 78%），Microsoft Agent Framework 1.0 是企业实现这一编排模式的工业级工程框架——**数据 → 框架** 的映射
- **Anthropic Claude Agent SDK 设计原则**：`anthropic-claude-agent-sdk-design-principles-2026.md`——SDK 设计层：Subagent 作为分布式认知网络；Agent Framework 是企业级的对应实现——**设计思想 → 生产框架** 的延伸
- **OpenAI Harness Engineering**：`openai-harness-engineering-philosophy-2026.md`——Harness Engineering 强调「环境设计先于代码」，Agent Framework 的图模型 + DevUI 正是这种思想的工程化实现

---

## 参考来源

- [Microsoft Agent Framework Version 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [Microsoft Agent Framework 1.0: .NET and Python 2026](https://www.digitalapplied.com/blog/microsoft-agent-framework-1-0-dotnet-python-guide)
- [Microsoft Agent Framework Overview - Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [GitHub - microsoft/agent-framework](https://github.com/microsoft/agent-framework)