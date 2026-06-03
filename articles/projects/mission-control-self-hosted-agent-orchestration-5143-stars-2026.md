# Mission Control：企业级自托管多 Agent 编排平台

> **核心能力**：一站式自托管平台，集任务调度、多 Agent 工作流执行、支出监控和运营治理于一体，支持 MCP 协议和 Claude 集成。

**Stars**：5,143 | **License**：MIT | **技术栈**：TypeScript / Next.js / SQLite | **创建时间**：2026-02-13

## 解决什么问题

企业在生产环境运行多个 AI Agent 时，通常面临分散的工具链：任务调度用一套系统、监控用另一套、API 成本又是一套。Mission Control 将这些能力整合到一个自托管平台上，让团队可以在一个 dashboard 中完成所有 Agent 运营管理工作。

## 核心功能

**多 Agent 编排与任务调度**
支持创建复杂的 multi-agent 工作流，在单一平台内定义任务分配、依赖关系和执行顺序。不需要将任务分散到多个独立服务中。

**支出监控与成本治理**
内置 spend tracking 功能，可以按 Agent、按工作流、按时间维度追踪 API 支出，并设置预算上限。这对于企业控制 AI 运营成本至关重要。

**MCP 协议支持**
内置 MCP（Model Context Protocol）支持，可以连接各种外部工具和数据源，扩展 Agent 的能力边界。

**Claude 深度集成**
平台原生支持 Claude 的 agent 能力，可以直接部署基于 Claude 的 autonomous agents。

**运营治理**
提供完整的运营可见性：任务执行日志、Agent 状态监控、错误追踪和告警。

## 技术亮点

- **自托管**：数据不离开企业自己的基础设施，满足数据安全合规要求
- **SQLite 存储**：轻量级持久化，降低部署复杂度
- **TypeScript/Next.js**：现代 Web 技术栈，便于二次开发和定制
- **MCP 原生**：内置 MCP 客户端，生态扩展能力强

## 适用场景

- 需要在私有环境运行多个 AI Agent 的企业
- 对 API 支出有严格管控需求的团队
- 需要统一管理多种不同来源 Agent 的运营团队
- 希望避免 vendor lock-in 的组织

## 与 Articles 的闭环

| Article 主题 | Mission Control 提供的闭环 |
|-------------|--------------------------|
| CrewAI Entangled Agentic Systems（框架商品化） | 企业级编排平台层，差异化在运营而非框架 |
| 法律 Agent Verifier（验证成本优化） | Agent 运营成本监控能力，直接支撑成本优化命题 |
| CrewAI 65% 企业采用率 | Mission Control 的 self-hosted 部署模式，满足企业数据隔离需求 |

---

*来源：[GitHub — builderz-labs/mission-control](https://github.com/builderz-labs/mission-control)（5,143 Stars，MIT License）*