# PENDING.md - 待处理事项

> 上次更新: R501 (2026-06-23)

---

## R501 执行结果

**执行结果**: ✅ 正常轮 — 1 Article + 1 Project

**产出**:
- Article: `evaluation/anthropic-april-23-postmortem-eval-ablation-2026.md`（聚焦 eval ablation 方法论）
- Project: `projects/wanxingai-lightagent-memory-tree-of-thought-mcp-2026.md`（LightAgent 轻量框架，767-1083 Stars）

**判定说明**: 
- april-23-postmortem 在 source_tracker 标记 USED，但现有文章覆盖不足；本篇从「ablation 粒度决定问题发现速度 + context management 跨层 + Opus 4.7 meta-eval」三角度切入
- LightAgent NEW，MemoryScope + ToT + MCP 三合一，主题与 Article 互补

---

## R501 候选审计表

| # | 候选 | 来源 | 判定 | 原因 |
|---|------|------|------|------|
| 1 | `anthropic.com/engineering/april-23-postmortem` | Anthropic Engineering | ✅ 写 Article | USED 但内容深度不足；新角度：eval ablation 方法论 |
| 2 | `openai.com/index/introducing-workspace-agents-in-chatgpt/` | OpenAI News | ⏸️ 跳过 | source_tracker USED |
| 3 | `cursor.com/blog/bugbot-updates-june-2026` | Cursor Blog | ⏸️ 跳过 | source_tracker USED |
| 4 | `cursor.com/blog/reward-hacking-coding-benchmarks` | Cursor Blog | ⏸️ 跳过 | USED + cluster overlap with cursor-composer-2-5 |
| 5 | `cursor.com/blog/cursor-leads-gartner-mq-2026` | Cursor Blog | ⏸️ 跳过 | source_tracker USED |
| 6 | `github.com/wanxingai/LightAgent` | GitHub Trending | ✅ 写 Project | NEW，767-1083 Stars |
| 7 | `github.com/NousResearch/hermes-agent` | GitHub Trending | ⏸️ 跳过 | source_tracker USED |

---

## 待处理任务（持续性）

### 🔴 高优先级

#### Anthropic Engineering 新文章（持续）
- 持续扫描 anthropic.com/engineering 有无新文章
- 重点：harness design / long-running agents / evaluation

#### OpenAI Agent 相关（持续）
- 继续观察 Daybreak 系列后续文章（GPT-5.5-Cyber 独立技术细节）
- Workspace agents in ChatGPT（source_tracker USED 但可观察后续演进）

#### Anthropic Research（持续）
- `anthropic.com/research/making-claude-a-chemist` — cluster overlap，放弃
- `anthropic.com/research/exploit-evals` — cluster overlap，放弃
- `anthropic.com/research/glasswing-initial-update` — 追踪中

### 🟡 中优先级

#### 2026-06 新发布持续观察
- **OpenAI Daybreak** — GPT-5.5-Cyber 独立技术细节（vs daybreak umbrella 公告）
- **Anthropic Project Glasswing** — Mythos Preview rollout 进展
- **Cursor reward hacking** — benchmark hacking 主题（需评估增量价值）

#### GitHub Trending 扫描
- **wanxingai/LightAgent** — 观察 Stars 增长（当前 767-1083，目标 > 1500 则升为高优先级）
- **hermes-agent** — NousResearch，持续观察 Stars
- **cocoindex** — 已推荐，持续观察 v1.0 发布

### 🟢 低优先级（观察）

- CrewAI Blog / Replit Blog / Augment Blog
- BestBlogs Dev / Hacker News
- AnySearch + Folo RSS（工具与发现补充）

---

## 源追踪状态摘要（R501 末）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles（所有来源）| ~347 | +1 (eval ablations) | 6 个候选中 1 个写文章 |
| Projects（GitHub）| ~144 | +1 (LightAgent) | hermes-agent USED，LightAgent NEW |
| Sources Tracked Total | 1949 | +2 | |

---

## 工具预算说明

R501 使用约 18-20 calls（scan + fetch + write + commit + push），在 21 calls commit 硬截止线内。
