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
| Anthropic `writing-tools-for-agents` | 工具设计原则 + 评估驱动迭代 | ✅ 已写（URL NEW + BM25 clean）|
| Anthropic `claude-code-sandboxing` | OS 级隔离 + 84% permission reduction | ⬇️ BM25 重复（47.2 similarity）跳过 |

### 下轮可深挖方向

1. **Anthropic Claude Security**（安全扫描 + Opus 4.7）——需要找官方来源
2. **Anthropic "agent-capabilities-api"** 页面（JS 渲染）——需要 agent-browser 重试
3. **microsoft/autogen** (58K stars) ——编程框架，与工具设计主题关联
4. **crewAIInc/crewAI** (52K stars) ——多 Agent 编排

## 长期追踪（持续性）

### 信息源优先级
- 🔴 **第一批次**：Anthropic / OpenAI / Cursor / CrewAI / Replit / Augment 官方博客（每月扫描一次）
- 🔴 **第一批次**：LangChain Blog
- 🟡 **第二批次**：Cursor changelog（每月一次节奏）
- 🟡 **第二批次**：Hacker News / Folo RSS

### GitHub Trending 扫描（每轮扫描）
- **待验证**：khoj-ai/khoj（34,933⭐）— AI personal knowledge assistant，与记忆主题强关联
- **待验证**：agentscope-ai/agentscope（26,344⭐）— Microsoft + 北大多 Agent 平台
- **待验证**：TencentCloud/TencentDB-Agent-Memory（4,909⭐）— 4-tier 内存管道
- **新发现**：karpathy/autoresearch（85,397⭐）— ✅ 本轮已写 Project
- **新发现**：microsoft/autogen（58,738⭐）— 仅追踪
- **新发现**：crewAIInc/crewAI（52,950⭐）— 仅追踪
- **新发现**：langchain-ai/langchain（138,684⭐）— 仅追踪（高度覆盖）
- 优先关注：新进入 Trending 的项目（不在 sources_tracked.jsonl）
- 重点关注：星数在 5K-30K 之间的高速增长项目

###已知 backlog
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
| **AI Agent OS** | 0 | 🆕 待启动 |
| **Agent Use-Case Mining** | 0 | 🆕 待启动 |
| **HITL Architecture** | 0 | 🆕 待启动 |

## 本轮已追踪的新源（待后续深挖）

| URL | 类型 | Stars | 状态 | 建议 |
|-----|------|-------|------|------|
| `github.com/karpathy/autoresearch` | project | 85,397 | ✅ 本轮已写 | — |
| `github.com/microsoft/autogen` | project | 58,738 | 仅追踪 | 编程框架，与工具设计关联 |
| `github.com/crewAIInc/crewAI` | project | 52,950 | 仅追踪 | 多 Agent 编排 |
| `github.com/langchain-ai/langchain` | project | 138,684 | 仅追踪 | 高度覆盖，跳过 |
| `anthropic.com/engineering/writing-tools-for-agents` | article | — | ✅ 本轮已写 | — |
| `anthropic.com/engineering/claude-code-sandboxing` | article | — | BM25 重复跳过 | 可评估增量价值 |

## 规则提醒

1. **Content Quality > Quantity**：宁可少发一篇，不发低质内容
2. **先 pull 再 push**：避免覆盖他人的更新
3. **道德底线**：不碰版权/商标/诽谤内容
4. **模糊地带**：停手 → PENDING.md → 等待决策
5. **R241 协议**：写 Article/Project 文件与写 jsonl 条目必须在同一 atomic 操作
6. **R271 协议**：每轮 orphan 扫描必执行，jsonl 不是 ground truth，articles/ 才是
7. **BM25 + URL 双验证**：URL NEW + 独特视角 = 写；URL USED = 跳过；URL NEW + BM25 高相似度 = 需判断视角是否独特