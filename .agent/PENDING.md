## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-07 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-07 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮 Article 来源分析

| 来源 | 文章主题 | 评估结果 |
|------|---------|---------|
| Anthropic Agent Skills | 3-tier progressive disclosure | ⬇️ BM25 重复（43.6相似度）已有多篇 |
| Anthropic Effective Context Engineering | context engineering for AI agents | ⬇️ URL 已追踪 |
| Anthropic Opus 4.8 | Product upgrade | ❌ 非工程深度文章 |
| Cursor Gartner MQ 2026 | Market recognition | ❌ 非技术内容 |
| Cursor Bugbot pricing | Pricing update | ❌ 非技术内容 |
| OpenAI Gartner Leader | Market recognition | ⬇️ URL 已追踪 |

### 下轮可深挖方向

1. **AnySearch 补充扫描** — 当 Tavily 无新内容时扩大搜索范围
2. **topoteretes/cognee** (17,706 stars) — memory management，与 Memory Layer cluster 相关
3. **Cursor June 2026 updates** — 跟进技术更新
4. **OpenAI GPT-5.5 技术细节** — 搜索工程实现相关

## 长期追踪（持续性）

### 信息源优先级
- 🔴 **第一批次**：Anthropic / OpenAI / Cursor / CrewAI / Replit / Augment 官方博客（每月扫描一次）
- 🔴 **第一批次**：LangChain Blog
- 🟡 **第二批次**：Cursor changelog（每月一次节奏）
- 🟡 **第二批次**：Hacker News / Folo RSS

### GitHub Trending 扫描（每轮扫描）
- **已归档**：emcie-co/parlant（18,103⭐）— ✅ 本轮已写
- **待验证**：topoteretes/cognee（17,706⭐）— memory management
- **待验证**：rohitg00/agentmemory（21,625⭐）— 确认是否有新文件
- **新发现**：AstrBotDevs/AstrBot（34,018⭐）— AI Bot框架
- 优先关注：新进入 Trending 的项目（不在 sources_tracked.jsonl）
- 重点关注：星数在 5K-30K 之间的高速增长项目

### 已知 backlog
- Anthropic **2026 Agentic Coding Trends Report**（PDF）深度分析 — Round 256 已浅写，本轮可深化
- OpenAI Codex agent loop 全文（Michael Bolin 博客）—— **SOURCE ALREADY TRACKED**
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
| **Customer-Facing AI Harness** | 1 | 🆕 刚启动 |
| **AI Agent OS** | 0 | 🆕 待启动 |
| **Agent Use-Case Mining** | 0 | 🆕 待启动 |
| **HITL Architecture** | 0 | 🆕 待启动 |

## 本轮已追踪的新源

| URL | 类型 | Stars | 状态 | 建议 |
|-----|------|-------|------|------|
| `github.com/emcie-co/parlant` | project | 18,103 | ✅ 本轮已写 | interaction control harness |
| `anthropic.com/news/introducing-claude-opus-4-8` | article | — | 未使用 | 非工程深度文章 |

## 规则提醒

1. **Content Quality > Quantity**：宁可少发一篇，不发低质内容
2. **先 pull 再 push**：避免覆盖他人的更新
3. **道德底线**：不碰版权/商标/诽谤内容
4. **模糊地带**：停手 → PENDING.md → 等待决策
5. **R241 协议**：写 Article/Project 文件与写 jsonl 条目必须在同一 atomic 操作
6. **R271 协议**：每轮 orphan 扫描必执行，jsonl 不是 ground truth，articles/ 才是
7. **BM25 + URL 双验证**：URL NEW + 独特视角 = 写；URL USED = 跳过；URL NEW + BM25 高相似度 = 需判断视角是否独特