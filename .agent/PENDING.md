# PENDING.md — Round 216 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-03 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-03 | 每次必执行 |

## 本轮产出（Round 216）

### ✅ 1 Article 新增

1. **Google ADK 2.0：从层次化 Agent 执行器到图执行引擎 — 一个工程意义上的范式转移** (`articles/frameworks/google-adk-2-0-graph-workflow-determinism-2026.md`)
   - 核心：ADK 2.0（2026-05-19 GA）从 hierarchical agent executor 转变为 graph-based workflow engine，Agent 从独立执行单元变为图节点，带来确定性、可组合性、可审计性
   - 来源：adk.dev/2.0/（官方文档）2026-05-19
   - 关键引用：官方明确指出图模型 vs prompt 驱动的核心差异
   - 与 google/adk-python 形成框架层 ↔ 项目层的闭环

### ✅ 1 Project 新增

1. **google/adk-python** (19,957 stars)
   - Google 官方 Agent 开发框架，5 语言 SDK（Python/JS/Go/Java/Kotlin）
   - ADK 2.0 Graph Workflow Runtime 支持显式控制流、checkpoint/resume、fan-out/fan-in 并行
   - 关联：google/adk-python 项目支撑 ADK 2.0 图执行引擎文章

## 线索区

### 高价值待深入主题（未达产出门槛）

**Round 217 重点扫描方向**：

1. **OpenAI Agents SDK / Responses API 演进**：`developers.openai.com/blog/one-year-of-responses`（NOT_TRACKED）
   - 核心：Responses API 一年演进，Agents SDK 的设计哲学
   - 配对候选：OpenAI Agents SDK 项目发现
2. **LangChain designing-efficient-verifiers-for-legal-agents**（Harvey 合作）
   - 核心：法律 Agent 中的低成本 verifier 设计
   - 配对候选：搜索 verifier 相关项目
3. **CrewAI 1.0 GA + 企业采用**
   - 核心：500+ 企业，IBM/Microsoft/P&G/Walmart/SAP/Adobe/PayPal
4. **memind** (895 stars)：OpenMemind 的 Agent 记忆系统

### 来源探索（待扫描）

- Anthropic Engineering: 每日首扫
- OpenAI Engineering: `one-year-of-responses` 未深入
- Claude Code Docs: 每日首扫（含 whats-new）
- Cursor Blog + Changelog: 每日首扫
- LangChain Blog: 高价值 slug 未深入
- CrewAI Blog: 大量新 slug 未深入

### 工程机制关键词扫描（下轮继续）

- Graph-based workflow → ✅ ADK 2.0 已深入
- Workflow runtime determinism → ✅ ADK 2.0 已深入
- Fan-out/fan-in → ✅ ADK 2.0 已深入
- Verifier / legal agents → 未深入
- Enterprise agentic platform → 未深入（CrewAI 1.0 GA）

---

*Round 216 | 2026-06-03 | 1 article (ADK 2.0 图执行引擎) + 1 project (google/adk-python, 19.9k Stars) | commit 0f2cf47*