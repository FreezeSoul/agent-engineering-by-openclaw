# lmnr-ai/lmnr — Laminar：面向长时 Agent 的开源可观测性平台

## 概述

| 维度 | 信息 |
|------|------|
| **项目名** | Laminar |
| **仓库** | [github.com/lmnr-ai/lmnr](https://github.com/lmnr-ai/lmnr) |
| **Stars** | 2,954（截至 2026-06-06） |
| **语言** | TypeScript + Rust（实时引擎） |
| **定位** | 面向 AI Agent 的开源可观测性平台 |
| **YC** | YC S24 |

## 核心定位

Laminar 是专为 AI Agent 设计的开源可观测性平台。与传统的 LLM 调用日志记录不同，Laminar 从第一天就围绕「长时运行的多步骤 Agent」场景建模：

- **嵌套 trace**：Agent 嵌套 Tool 嵌套 LLM Call 的深度调用链
- **长时间跨度**：单次 Agent 运行可能跨越数小时，涉及多次工具调用和子 Agent 协作
- **实时反馈**：需要实时看到 Agent 当前在做什么，而非事后分析

## 技术架构

### 核心组件

```
┌──────────────────────────────────────────────┐
│              Laminar 架构                     │
├──────────────────────────────────────────────┤
│  Laminar Python SDK（ instrumentation）       │
│  Laminar JS/TS SDK                           │
├──────────────────────────────────────────────┤
│  Frontend（Next.js）                          │
│  Backend API（TypeScript）                   │
│  Real-time Engine（Rust，自研）               │
├──────────────────────────────────────────────┤
│  PostgreSQL（metadata）                      │
│  ClickHouse / Object Storage（trace data）   │
└──────────────────────────────────────────────┘
```

### 实时引擎（Rust 自研）

Laminar 的核心竞争力是一个用 Rust 编写的自定义实时引擎。这个引擎处理：

1. **Trace 流式写入**：Agent 运行时的事件实时流入，不需要等待整个 run 完成
2. **嵌套 span 管理**：深度嵌套的 trace 结构（Agent → Tool → LLM Call）的实时聚合
3. **实时查询**：P50 毫秒级响应，支持即时调试

这个实时引擎与 LangChain 的 SmithDB 解决了不同层级的问题：SmithDB 解决的是**存储层**（如何高效存储和查询 PB 级 trace 数据），Laminar 解决的是**查询和可视化层**（如何让开发者实时看到 Agent 在做什么）。

### 集成框架

Laminar 支持主流 Agent 框架的开箱即用集成：

| 框架 | 集成方式 |
|------|---------|
| **LangChain** | 官方 SDK |
| **Browser-use** | 官方 SDK |
| **Claude Agent SDK** | 官方 SDK |
| **Vercel AI SDK** | 官方 SDK |
| **OpenHands** | 官方 SDK |
| **LiteLLM** | 官方 SDK |

这意味着如果你的 Agent 用的是这些框架，只需要几行代码就能接入 Laminar。

## 核心功能

### 1. Trace 可视化

Laminar 的 trace 视图展示 Agent 的完整执行路径：

```
Agent: "分析销售数据"
  ├── Tool: "查询数据库" (12ms)
  │     └── LLM Call: "GPT-4o" (1,203ms)
  ├── Tool: "生成图表" (4,521ms)
  │     └── LLM Call: "GPT-4o" (4,498ms)
  └── Tool: "发送邮件" (892ms)
        └── LLM Call: "GPT-4o" (867ms)
```

每个节点展开可以看到完整的输入输出、token 消耗、执行时间。

### 2. Eval 评估

Laminar 内置了 eval 框架，支持：

- **在线评估**：基于规则的评估器，实时打分
- **离线评估**：Ground truth 数据集评估
- **Trace 评分**：对单次 trace 的整体评分和细粒度评分

### 3. SQL Editor（AI 辅助）

Laminar 支持用自然语言查询 trace 数据：

> "Show me all traces where the agent called the wrong tool"

底层是 LLM 将自然语言转换为结构化查询，在 trace 数据上执行。

### 4. Dashboard

聚合视图展示：

- Token 消耗趋势
- 工具调用频率
- Agent 错误率
- 延迟分布（P50/P95/P99）

## 与 SmithDB 的互补关系

| 维度 | SmithDB（LangChain） | Laminar（lmnr-ai/lmnr） |
|------|---------------------|------------------------|
| **层级** | 存储层 | 查询/可视化层 |
| **语言** | Rust（DataFusion + Vortex） | TypeScript + Rust（实时引擎） |
| **定位** | 基础设施（供平台使用） | 开发者工具（供人使用） |
| **Stars** | N/A（闭源内部） | 2,954 ⭐ |
| **部署** | 嵌入 LangSmith 平台 | Self-hosted + Managed |
| **核心价值** | 高性能 trace 存储 | 实时 trace 可视化 + Eval |

两者共同验证了一个趋势：**Agent 可观测性正在从「LLM 调用日志」进化为「运行时行为数据库」**——需要专门的数据架构来处理嵌套、异步、大体量的 trace 数据。

## 工程亮点

### 1. Self-hosted 的完整方案

Laminar 提供完整的 self-hosted 部署方案（docker-compose），包括：

- 前端（Next.js）
- 后端 API
- 实时引擎
- PostgreSQL metadata store
- ClickHouse 或 S3 兼容存储（trace 数据）

对于不想把 trace 数据放到第三方托管服务的团队，这是完整的数据主权方案。

### 2. YC S24 背景

Laminar 是 YC Summer 2024 批次成员，2026 年 3 月刚完成 $3M seed 轮融资。团队在融资公告中明确表示：Agent 可观测性是 2026 年的关键基础设施需求，现有的 APM 和 LLM 日志工具都不足以应对 Agent 场景。

### 3. 前端 AI 功能

Laminar 是最早在可观测性产品中引入 AI 辅助查询的项目之一：

- **Chat with Trace**：用自然语言提问 trace 内容
- **SQL with AI**：自然语言转 SQL 查询 trace 数据

这让 trace 调试不再需要记忆复杂的查询语法。

## 适用场景

- **团队使用 LangChain/LangGraph**：Laminar 是官方推荐的可观测性集成方案
- **自建 Agent 平台**：需要完整的 trace 可视化和评估能力
- **数据主权要求高**：需要 self-hosted 部署，不接受数据上云
- **多框架混合**：同时使用 Claude SDK + Browser-use + LangChain，需要统一观测

## Stars 轨迹

Laminar 的 Stars 增长反映了 Agent 可观测性赛道的热度：

- 2026-03-16：$3M seed 轮公告（~2,000 ⭐）
- 2026-06-06：2,954 ⭐（3 个月增长 ~50%）

## 来源

- [Laminar 官网](https://laminar.sh)
- [GitHub: lmnr-ai/lmnr](https://github.com/lmnr-ai/lmnr)
- [Laminar Blog: $3M Seed Launch](https://laminar.sh/blog/2026-03-16-laminar-launch)
- [Laminar GitHub Topics: agent-observability](https://github.com/topics/agent-observability)

## 相关主题

- **Cluster**: `agent-observability` / `tracing` / `eval` / `laminar` / `open-source` / `self-hosted`
- **关联 Article**: LangChain SmithDB（Round 270）— 存储层基础设施，与 Laminar 的查询/可视化层互补
- **关联 Article**: LangChain Interpreter（Round 268）— Interpreter Skills 作为第三 context surface，与 trace 可观测性共同构成 Agent 运行时完整视图
