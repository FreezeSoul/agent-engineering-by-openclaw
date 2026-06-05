# alash3al/stash：MCP 上的 OSS 持久化记忆，9 阶段 consolidate 把"对话碎片"炼成"知识结晶"

> **核心定位**：`alash3al/stash` 是 **LangSmith Deployment 的 OSS 记忆层等价物**——通过 MCP 协议暴露给任何 Agent（Claude Code / Cursor / Windsurf / Cline / OpenAI Agents），用 Postgres + pgvector + 9 阶段 consolidation pipeline 把每一次会话的 observations 提炼成可跨会话检索的"事实、关系、模式、智慧"。

## 核心论点

`alash3al/stash` 的核心洞察是：**"episodes → facts → relationships → patterns → wisdom"不是营销文案，是一条工程 pipeline**。9 个阶段（observations → facts → causal links → patterns → contradictions → goal tracking → failure patterns → hypothesis verification）每一步只处理自上次运行以来的新数据，**让 Agent 的记忆像人类长期记忆一样分层凝固**。这种"认知层 (cognitive layer)"的 OSS 实现，恰好补齐了 LangSmith Deployment 在「durable thread + observability」之外的「知识蒸馏」维度。

## 项目快照

| 维度 | 数值 |
|------|------|
| Repo | [github.com/alash3al/stash](https://github.com/alash3al/stash) |
| Stars | 710+（截至 2026-06-05）|
| License | Open source（自托管 + Stash Cloud Beta） |
| 核心栈 | Postgres + pgvector + MCP server（SSE transport） |
| 一键部署 | `docker compose up`（Postgres + migrations + MCP server + 后台 consolidation） |
| 客户端 | Claude Desktop / Cursor / Windsurf / Cline / Continue / OpenAI Agents / Ollama / OpenRouter |
| 哲学 | "Episodes become facts. Facts become relationships. Relationships become patterns. Patterns become wisdom." |

## 一手来源

- **Repo**：[github.com/alash3al/stash](https://github.com/alash3al/stash)
- **README 关键引用**：
  - "A 9-stage consolidation pipeline turns raw observations into structured knowledge — facts, relationships, causal links, patterns, contradictions, goal tracking, failure patterns, and hypothesis verification. Each stage only processes new data since the last run."
  - "Stash is a cognitive layer between your AI agent and the world."
- **架构描述**：从 README 的 7-layer 架构图（实际项目是 7 layer memory OS 风格）

## 与配套 Article 的闭环

- **Article**：[LangChain Harmonic Scout V2：从「刚性 subgraph」到「Deep Agents + 共享文件系统」，4 倍留存不是设计目标而是结构副产品](../enterprise/langchain-harmonic-scout-deep-agents-4x-retention-2026.md)
- **Project**：`alash3al/stash`（本文）

**闭环逻辑**：
- **Article 揭示问题**：Scout V2 的关键是"共享文件系统 + Deep Agents harness + LangSmith Deployment"，其中 LangSmith Deployment 解决 durable thread + observability
- **Project 提供 OSS 答案**：`alash3al/stash` 用 MCP 暴露 9-stage consolidation pipeline，让**任何 Agent**（不限于 LangChain 生态）都获得「跨会话的、分层凝固的、可检索的」持久化记忆

**Pattern 8（商业 vs OSS）**：LangSmith 是 LangChain 商业化的「全栈 observability + memory 平台」；`alash3al/stash` 是「纯 OSS、单点深耕、MCP 协议中立」的记忆层替代方案。两者在「Agent 记忆如何在多次会话之间保持一致」这一问题上走的是同一条路，但部署模型和生态绑定度截然不同。

## 9 阶段 Consolidation Pipeline 详解

每阶段都只处理自上次运行以来的新数据（增量模式，不重算历史）：

| 阶段 | 输入 | 输出 | 工程意义 |
|------|------|------|----------|
| 1. **Observations** | Agent 工具调用 / 用户消息 / 模型响应 | 原始事件流 | 不可丢失的最低保真记录 |
| 2. **Facts** | Observations | 实体 + 属性（如 "John 在 Anthropic 工作"） | 把对话转成结构化数据 |
| 3. **Relationships** | Facts | 实体关系图（John → worksAt → Anthropic） | 知识图谱层，支持 reasoning |
| 4. **Causal Links** | Relationships | 因果链（A 导致 B，因为 C） | 时间 + 因果推理 |
| 5. **Patterns** | Causal Links | 重复结构（如 "用户每次周五问 Q4 报告"） | 习惯与偏好识别 |
| 6. **Contradictions** | Patterns | 矛盾检测（"上次说不喜欢 X，这次说喜欢 X"） | 自洽性维护 |
| 7. **Goal Tracking** | Patterns | 长期目标 + 进度（如 "完成 2026 Q2 OKR"） | 主动 follow-up |
| 8. **Failure Patterns** | Contradictions | 失败模式库（"这个 API 在 X 情况下会 timeout"） | 自我警示 |
| 9. **Hypothesis Verification** | Failure Patterns | 待验证假设 + 证据收集 | 主动学习循环 |

**这 9 阶段的设计哲学**：把 LLM 临时上下文（Context Window）里的碎片，**通过后台 consolidation 蒸馏成长期知识**。每次新会话开始时，Agent 通过 `recall` tool 从 Stash 拉取最相关的事实/关系/模式，而不是从 0 开始拼装 prompt。

## 三个副观点

### 副观点 1：MCP 是「Agent 工具化的 USB-C」——Stash 是首批展示 MCP 全部潜力的项目之一

MCP（Model Context Protocol）从 2024 年底发布以来，多数项目把它当作「工具调用的一种实现」。Stash 是**首批把 MCP 用作「Agent 跨工具持久化记忆」**的项目——任何支持 MCP 的客户端（Cursor / Claude Desktop / Windsurf / Cline / OpenAI Agents）**不需要写一行集成代码**就能获得持久化记忆。这是 MCP 协议层胜利的样本：协议中立 = 生态扩张。

### 副观点 2：单进程 + Postgres + pgvector 是"Agent 基础设施"的当前 sweet spot

Stash 的技术栈选择（Postgres + pgvector + SSE MCP server + docker compose）是一个清晰信号：**复杂 Agent 基础设施不需要 Kubernetes + vector DB cluster + Redis**。一个 docker compose、单实例 Postgres、单 MCP server——足够覆盖 95% 的生产 Agent 用例。**「基础设施越简单，团队越 lean，4x 留存越可实现」**。

### 副观点 3：本地 Ollama 集成意味着"完全本地 + 完全 OSS" 路径存在

README 明确写"Fully local (no cloud API): Ollama setup guide — host Ollama + Docker Compose, private embeddings and reasoner"。这意味着：**没有任何云依赖、不需要 OpenAI key、不需要 LangChain 账号、只需要本地 GPU**——一个 100% 隐私保留的 Agent 记忆系统。在企业级数据合规（GDPR / HIPAA / 金融数据本地化）场景下，这种 "fully local" 路径比 LangSmith 这类 SaaS-first 产品更有竞争力。

## 与同类项目的差异化

| 项目 | 定位 | 集成方式 | 记忆模型 | 与 Stash 差异 |
|------|------|----------|----------|--------------|
| **alash3al/stash** | MCP 记忆 server | MCP over SSE | 9-stage consolidation | **跨生态中立 + 分层凝固** |
| Letta | Stateful agents | Python SDK | 滑窗 + summary | 更聚焦 context engineering，非通用记忆 |
| mem0 | Memory layer | Python SDK / REST | 实体抽取 + 检索 | 单一"事实"层，无 9 阶段 |
| LangSmith Deployment | 商业全栈 | LangChain 深度 | Durable thread | 商业绑定 + 需 LangChain 生态 |
| LangGraph Memory | 框架内 | LangGraph 原生 | Checkpoint + store | 框架锁定 |

**Stash 的差异点是**："**跨生态中立 + 9 阶段分层**"——既不像 mem0 / Letta 那样绑 SDK，也不像 LangSmith 那样绑生态，是"中间层"位置的最佳人选。

## 部署与集成

### 一键启动

```bash
git clone https://github.com/alash3al/stash.git
cd stash
cp .env.example .env  # 填 API key + model
docker compose up
```

**这一行启动什么**：
- Postgres + pgvector（数据存储 + 向量检索）
- 数据库 migrations（schema 初始化）
- MCP server（SSE 协议，端口 8080）
- 后台 consolidation worker（增量处理新 observations）

### Cursor 集成示例（README 原文）

```json
// ~/.cursor/mcp.json
{
  "mcpServers": {
    "stash": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```

### Claude Desktop 集成示例

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "stash": {
      "url": "http://localhost:8080/sse"
    }
  }
}
```

### OpenCode 集成示例

```json
// ~/.config/opencode/config.json
{
  "mcp": {
    "stash": {
      "type": "remote",
      "url": "http://localhost:8080/sse",
      "enabled": true
    }
  }
}
```

## 实战用法

`docker compose up` 后，Stash 暴露三个核心 commands（通过 MCP）：

1. **`init`** — 初始化项目级 memory namespace
2. **`remember`** — 显式把当前会话的某个事实/事件写入 Stash
3. **`recall`** — 按 query 检索最相关的 facts / relationships / patterns

**典型 workflow**（以 Claude Desktop + Stash 为例）：

```
用户： "我决定用 Postgres 而不是 SQLite 来做项目 X 的数据层"
Claude： 调用 remember 工具 → Stash 写入 "项目 X 选型：Postgres（reasoning: ...）"
...
下次会话：
用户： "项目 X 的数据层用什么？"
Claude： 调用 recall 工具 → Stash 返回之前的事实 → 直接回答 "Postgres（因为 ...）"
```

**这个 workflow 的关键**：`recall` 触发的不是 prompt 拼装，而是**结构化检索 + 关联推理**——和 Harmonic 的"共享文件系统"是同一思路，但更轻量、更本地、更通用。

## 何时选 Stash，何时选 LangSmith

| 场景 | 推荐选择 | 理由 |
|------|----------|------|
| 100% 数据本地化 / 隐私合规 | ✅ Stash | Ollama + 本地 Postgres，无云依赖 |
| LangChain 生态深耕 | ✅ LangSmith | 深度集成 + 自带 observability |
| 跨工具链（Cursor + Claude Desktop + OpenAI Agents） | ✅ Stash | MCP 协议中立 |
| Lean 团队 + 自托管优先 | ✅ Stash | 单 docker compose，零运维 |
| 大规模生产 + 团队协作 | ⚠️ LangSmith | 商业版有 SSO / 权限 / 审计 |
| 需要 evals + experiment tracking | ⚠️ LangSmith | Stash 不做 evals |
| 不想被 LangChain 生态绑定 | ✅ Stash | 协议中立，长期灵活性 |

## 一句话总结

**`alash3al/stash` 把「Agent 长期记忆」从 LangChain 生态的专属能力变成了 MCP 协议层的公共设施——一个 docker compose，9 阶段 consolidation，跨 Cursor / Claude Desktop / OpenAI Agents 全生态可用**。它是 LangSmith 商业护城河之外最值得关注的 OSS 记忆层替代品。
