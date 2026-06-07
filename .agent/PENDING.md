## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-08 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-08 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮 Article 来源分析

| 来源 | 文章主题 | 评估结果 |
|------|---------|---------|
| Anthropic Engineering | 所有候选 URL 均已追踪 | ⬇️ 跳过 |
| OpenAI | "one-year-of-responses" 被 403 阻断 | ⏸️ 下轮用 agent-browser 重试 |
| Cursor Blog | 新文章多为定价/公司新闻，非工程深度 | ⬇️ 跳过 |
| Microsoft Agent Framework | BUILD 2026 已于 Round 282 覆盖 | ⏸️ 等待窗口 |

### 下轮可深挖方向

1. **OpenAI one-year-of-responses** — 用 agent-browser 重试获取完整内容（Responses API 一周年 + Assistants API 迁移指南）
2. **Anthropic June 2026 新 Engineering 文章** — 确认是否有新文章发布
3. **kseni/kiss_ai** (515⭐) — Terminal Bench 2.0 高分，关注后续 Star 增长
4. **Cursor SDK auto-review 机制** — permissions.json + natural language 审批规则，与 Harness ToolApprovalAgent 关联

## 长期追踪（持续性）

### 信息源优先级
- 🔴 **第一批次**：Anthropic / OpenAI / Cursor / CrewAI / Replit / Augment 官方博客（每月扫描一次）
- 🔴 **第一批次**：LangChain Blog
- 🟡 **第二批次**：Microsoft Agent Framework Blog（BUILD 2026 后重点关注）
- 🟡 **第二批次**：Hacker News / Folo RSS

### GitHub Trending 扫描（每轮扫描）
- **已归档**：mvanhorn/last30days-skill（29,367⭐）— ✅ Round 281 已写
- **已归档**：emcie-co/parlant（18,103⭐）— ✅ 已写
- **已归档**：mukul975/Anthropic-Cybersecurity-Skills（14,718⭐）— ✅ Round 282 已写
- **已归档**：HKUDS/nanobot（43.8K⭐）— ✅已有2篇文章
- **已归档**：addyosmani/agent-skills（48.7K⭐）— ✅ 已有2篇文章
- **已归档**：RightNow-AI/openfang（17.7K⭐）— ✅ 已写
- **已归档**：aaif-goose/goose（47,302⭐）— ✅ Round 284 已写
- **已归档**：Purewhiter/mobilegym（549⭐）— ✅ Round 284 orphan backfill
- **待验证**：ksenxx/kiss_ai（515⭐）— Terminal Bench 2.0 高分但 Stars 不足
- 优先关注：新进入 Trending 的项目（不在 sources_tracked.jsonl + articles/）
- 重点关注：星数在 5K-30K 之间的高速增长项目

### 已知 backlog
- Anthropic **2026 Agentic Coding Trends Report**（PDF）深度分析 — Round 256 已浅写，本轮可深化
- LangChain `introducing-langchain-labs` (May 14, 2026) — cluster 强饱和（self-evolving 24+ 文章）

## 已知 Cluster 饱和度

| Cluster | 文章数 | 状态 |
|---------|--------|------|
| Harness Engineering | 30+ | ⚠️ 强饱和 |
| Self-evolving Agents | 24+ | ⚠️ 强饱和 |
| Sandbox / Agent Execution | 5+ | ⚠️ 强饱和 |
| Agent Skills | 5+ | ⚠️ 接近饱和 |
| Memory Layer | 7+ | ⚠️ 接近饱和 |
| LangSmith Engine | 4+ | ⚠️ 接近饱和 |
| **Tool Use / MCP** | 多个 | 🟡 活跃 |
| **AI Coding** | 多个 | 🟡 活跃 |
| **Real-time Voice AI** | 1 | 🟡 刚启动 |
| **Customer-Facing AI Harness** | 1 | 🟡 刚启动 |
| **Local / Open Source Agent** | 1 | 🆕 刚启动（goose） |
| **AI Agent Eval — Mobile/Desktop GUI** | 1 | 🆕 刚启动（mobilegym） |
| **AI Agent OS** | 0 | 🆕 待启动 |
| **Agent Use-Case Mining** | 0 | 🆕 待启动 |
| **HITL Architecture** | 0 | 🆕 待启动 |

## 本轮已追踪的新源

| URL | 类型 | Stars | 状态 | 建议 |
|-----|------|-------|------|------|
| `github.com/aaif-goose/goose` | project | 47,302 | ✅ 本轮已写 | Rust 原生本地 AI Agent + hooks 系统 |
| `github.com/Purewhiter/mobilegym` | project | 549 | ✅ 本轮已写 | 可验证手机 GUI Agent 训练平台 |

## 规则提醒

1. **Content Quality > Quantity**：宁可少发一篇，不发低质内容
2. **先 pull 再 push**：避免覆盖他人的更新
3. **道德底线**：不碰版权/商标/诽谤内容
4. **模糊地带**：停手 → PENDING.md → 等待决策
5. **R241 协议**：写 Article/Project 文件与写 jsonl 条目必须在同一 atomic 操作
6. **R271 协议**：每轮 orphan 扫描必执行，jsonl 不是 ground truth，articles/ 才是
7. **BM25 + URL 双验证**：URL NEW + 独特视角 = 写；URL USED = 跳过；URL NEW + BM25 高相似度 = 需判断视角是否独特
8. **source_tracker + articles/ 交叉验证**：source_tracker check 必须与 articles/ 目录交叉验证，避免 jsonl orphan 导致的重复写入