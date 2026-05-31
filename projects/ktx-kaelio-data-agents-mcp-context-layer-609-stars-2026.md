# ktx：数据与分析智能体的上下文中间件层

> ktx is an executable context layer for data and analytics agents 🐙 Allow Claude Code, Codex, and any AI agent to query data accurately through MCP with skills, memory and a semantic layer.

## 基本信息

| 指标 | 数值 |
|------|------|
| GitHub | [Kaelio/ktx-ai-data-agents-mcp-context-skills](https://github.com/Kaelio/ktx-ai-data-agents-mcp-context-skills) |
| Stars | ⭐ 609 (2026-05-10) |
| License | Apache 2.0 |
| 语言 | TypeScript |
| 文档 | [docs.kaelio.com/ktx](https://docs.kaelio.com/ktx/docs/) |
| 社区 | [ktx Slack](https://join.slack.com/t/ktxcommunity/shared_invite/zt-3y9b44m1x-LVyNNJD5nwaZHq4XS29LMQ) |
| YC | Y Combinator P25 |

## 核心定位

ktx 是一个**可执行的上下文中间件层**（executable context layer），专门解决数据和分析智能体「如何准确查询数据」的问题。它通过 MCP（Model Context Protocol）与 Claude Code、Codex 等主流 AI Coding Agent 集成，提供 skills、memory 和 semantic layer 三层能力。

### 三层架构

| 层级 | 能力 |
|------|------|
| **Skills** | 预置数据查询模式（SQL、数据管道、可视化） |
| **Memory** | 跨会话的数据 schema 和业务语义记忆 |
| **Semantic Layer** | 自然语言到精确数据查询的语义映射 |

### MCP 集成模式

ktx 的 MCP 集成方式值得关注——它不是简单提供工具，而是通过 MCP 协议传递：
- **可执行的上下文**：schema + 业务语义 + 查询模式
- **工具发现**：数据源动态发现而不是静态配置
- **结果缓存**：避免重复查询同一数据源

## 与 Context-Mode 的主题关联

[mksglu/context-mode](articles/projects/context-mode-mksglu-98-percent-context-reduction-2026.md)（16,000 Stars）解决的是「跨仓库 Context 优化」的问题，而 ktx 解决的是「跨数据源上下文一致性问题」——两者都是 Context 层的工程实践，只是 domain 不同。

| 维度 | context-mode | ktx |
|------|--------------|-----|
| 上下文类型 | 代码仓库 | 数据/分析 |
| 优化目标 | Token 压缩（98%） | 查询准确性 |
| 集成协议 | MCP | MCP |
| 目标 Agent | Coding Agent | Data Agent |

## 工程洞察

ktx 的价值在于：**它填补了 Data Agent 在「上下文工程」领域的空白**。现有的 AI Coding Agent 已有完整的上下文工程体系（参见 [anthropic-context-engineering-triple-layer](articles/context-memory/anthropic-context-engineering-triple-layer-long-horizon-2026.md)），但 Data Agent 一直缺少类似的中间件层。ktx 通过 Y Combinator P25 的背书，展示了市场对「数据智能体上下文中间件」的需求。

---

*数据来源：[GitHub API](https://api.github.com/repos/Kaelio/ktx-ai-data-agents-mcp-context-skills)，抓取于 2026-05-31*