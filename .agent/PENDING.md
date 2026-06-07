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
| OpenAI "One year of Responses" | Oracle 深度推理架构 | ✅ **本轮已写** |
| CrewAI Fintech compliance | 企业合规自动化 2 天→2 小时 | ⏸️ 下轮深挖 |
| nex-agi/Nex-N2 | Agentic Thinking 模型 | ⏸️ 关注 Star 增长 |

### 下轮可深挖方向

1. **CrewAI Fintech compliance case study** — 已确认为新源，Fintech 合规 2天→2小时的 Agent 工作流
2. **nex-agi/Nex-N2**（33⭐，2026-06-03）— Agentic Thinking 模型，关注后续 Star 增长
3. **lfnovo/open-notebook**（555⭐）— NotebookLM 开源替代品，隐私优先 AI 研究助手
4. **RyanCodrai/turbovec**（1.5K⭐）— Rust 向量索引库（MLinfra，非核心 Agent）

## 长期追踪（持续性）

### 信息源优先级
- 🔴 **第一批次**：Anthropic / OpenAI / Cursor / CrewAI / Replit / Augment 官方博客
- 🔴 **第一批次**：LangChain Blog
- 🟡 **第二批次**：Hacker News / Folo RSS / AnySearch 补充

### GitHub Trending 扫描（每轮扫描）
- **已归档**：mvanhorn/last30days-skill（29,367⭐）— ✅ Round 281 已写
- **已归档**：emcie-co/parlant（18,103⭐）— ✅ 已写
- **已归档**：mukul975/Anthropic-Cybersecurity-Skills（14,718⭐）— ✅ Round 282 已写
- **已归档**：HKUDS/nanobot（43.8K⭐）— ✅ 已有文章
- **已归档**：addyosmani/agent-skills（48.7K⭐）— ✅ 已有文章
- **已归档**：aaif-goose/goose（47,302⭐）— ✅ Round 284 已写
- **已归档**：NousResearch/hermes-agent（180K⭐）— ✅ 已有文章
- **待验证**：nex-agi/Nex-N2（33⭐，2026-06-03）— Agentic Thinking 模型，关注 Star 增长
- **待验证**：lfnovo/open-notebook（555⭐）— NotebookLM 开源替代，低于 1000 门槛
- 优先关注：新进入 Trending 的 Agent 工程框架
- 重点关注：星数在 5K-30K 之间的高速增长项目

### 已知 backlog
- Anthropic **2026 Agentic Coding Trends Report**（PDF）深度分析 — 已有浅写，可深化
- LangChain `introducing-langchain-labs` (May 14, 2026) — cluster 强饱和

## 已知 Cluster 饱和度

| Cluster | 文章数 | 状态 | 备注 |
|---------|--------|------|------|
| Harness Engineering | 30+ | ⚠️ 强饱和 | — |
| Self-evolving Agents | 24+ | ⚠️ 强饱和 | — |
| **Deep Reasoning / Oracle Architecture** | 🆕 新增 | 🟡 活跃 | Round 285 新增 |
| Sandbox / Agent Execution | 5+ | ⚠️ 强饱和 | — |
| Agent Skills | 5+ | ⚠️ 接近饱和 | — |
| Memory Layer | 7+ | ⚠️ 接近饱和 | — |
| LangSmith Engine | 4+ | ⚠️ 接近饱和 | — |
| Orchestration | 多个 | 🟡 活跃 | Oracle 架构新增至此 |
| Context-Memory | 多个 | 🟡 活跃 | 上下文包概念新增 |
| **Tool Use / MCP** | 多个 | 🟡 活跃 | — |
| **AI Coding** | 多个 | 🟡 活跃 | — |
| **Real-time Voice AI** | 1 | 🟡 活跃 | — |
| **Customer-Facing AI Harness** | 1 | 🟡 活跃 | Parlant 开辟客服场景 |
| **Local / Open Source Agent** | 1 | 🟡 活跃 | goose 成为此 cluster 首个项目 |
| **AI Agent Eval — Mobile/Desktop GUI** | 1 | 🟡 活跃 | mobilegym 成为此 cluster 首个项目 |
| **AI Agent OS** | 0 | 🆕 待启动 | — |
| **Agent Use-Case Mining** | 0 | 🆕 待启动 | — |
| **HITL Architecture** | 0 | 🆕 待启动 | — |

## 本轮已追踪的新源

| URL | 类型 | Stars | 状态 | 建议 |
|-----|------|-------|------|------|
| `developers.openai.com/blog/one-year-of-responses` | article | — | ✅ 本轮已写 | Oracle 深度推理架构 |
| `blog.crewai.com/how-a-leading-fintech...` | article | — | ⏸️ 下轮深挖 | 企业合规自动化 |

## 规则提醒

1. **Content Quality > Quantity**：宁可少发一篇，不发低质内容
2. **先 pull 再 push**：避免覆盖他人的更新
3. **道德底线**：不碰版权/商标/诽谤内容
4. **模糊地带**：停手 → PENDING.md → 等待决策
5. **R241 协议**：写 Article/Project 文件与写 jsonl 条目必须在同一 atomic 操作
6. **R271 协议**：每轮 orphan 扫描必执行，jsonl 不是 ground truth，articles/ 才是
7. **BM25 + URL 双验证**：URL NEW + 独特视角 = 写；URL USED = 跳过；URL NEW + BM25 高相似度 = 需判断视角是否独特
8. **source_tracker + articles/ 交叉验证**：source_tracker check 必须与 articles/ 目录交叉验证
