# 待办事项 — agent-engineering-by-openclaw

## Round 276 交接说明

- **接手的上一轮**：`Round 275`，author: AgentKeeper，commit: `dbb1f5e`
- **本轮 author**：AgentKeeper
- **续接方式**：round 编号续接（`Round 276`）
- **本轮核心产出**：1 Article（认知记忆五操作）+ 1 Project（agentmemory 21564⭐）

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
- 优先关注：新进入 Trending 的项目（不在 sources_tracked.jsonl）
- 重点关注：星数在 5K-30K 之间的高速增长项目

### 已知 backlog
- Anthropic **2026 Agentic Coding Trends Report**（PDF）深度分析 — Round 256 已浅写，本轮可深化
- OpenAI Codex agent loop 全文（Michael Bolin 博客）—— **SOURCE ALREADY TRACKED**，可写但需新角度
- LangChain `introducing-langchain-labs` (May 14, 2026) — cluster 强饱和（self-evolving 24+ 文章）

## 已知 Cluster 饱和度

| Cluster | 文章数 | 状态 |
|---------|--------|------|
| Harness Engineering | 30+ | ⚠️ 强饱和 |
| Self-evolving Agents | 24+ | ⚠️ 强饱和 |
| Sandbox / Agent Execution | 5+ | ⚠️ 强饱和 |
| Agent Skills | 5+ | ⚠️ 接近饱和 |
| Memory Layer | 7+ | ⚠️ 接近饱和（认知记忆五操作 + Mnemosyne + 多个 RAG/Memory 文章）|
| LangSmith Engine | 4+ | ⚠️ 接近饱和 |
| **SKILL.md 技能工程** | 1+1 | 🟡 新建（Round 273）|
| **AI Agent OS** | 0 | 🆕 待启动（OpenCognit 仅 30⭐，已放弃）|
| **Agent Use-Case Mining** | 0 | 🆕 待启动（CrewAI Discovery, 2026-04-30）|
| **HITL Architecture** | 0 | 🆕 待启动（CrewAI missing-layer, 2026-01-21）|

## 本轮待跟进的新源

| URL | 类型 | 状态 | 建议 |
|-----|------|------|------|
| `crewai.com/blog/agent-harnesses-are-dead` | article | jsonl tracked | 评估是否营销噱头 vs 工程洞察 |
| `crewai.com/blog/a-missing-layer-in-agentic-systems` | article | jsonl tracked | HITL Architecture 集群起点候选 |
| `crewai.com/blog/how-to-optimize-token-spend` | article | jsonl tracked | 成本优化方向，非核心工程 |
| `crewai.com/blog/your-first-ai-agent-should-do-one-thing-badly` | article | jsonl tracked | 指导原则方向，非核心工程 |
| `github.com/khoj-ai/khoj` | project | jsonl tracked | 34,933⭐，值得深写 |
| `github.com/agentscope-ai/agentscope` | project | jsonl tracked | 26,344⭐，值得深写 |
| `github.com/TencentCloud/TencentDB-Agent-Memory` | project | jsonl tracked | 4,909⭐，可选 |

## 规则提醒

1. **Content Quality > Quantity**：宁可少发一篇，不发低质内容
2. **先 pull 再 push**：避免覆盖他人的更新
3. **道德底线**：不碰版权/商标/诽谤内容
4. **模糊地带**：停手 → PENDING.md → 等待决策
5. **R241 协议**：写 Article/Project 文件与写 jsonl 条目必须在同一 atomic 操作
6. **R271 协议**：每轮 orphan 扫描必执行，jsonl 不是 ground truth，articles/ 才是
7. **gen_article_map.py 已知问题**：Round 274/276 均出现超时卡死 → 下轮可考虑跳过或优化脚本