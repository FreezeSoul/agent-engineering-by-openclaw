# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-28 | 每次必执行 |

## 本轮已产出

### 维护操作
- **Round 143 维护轮次**：新增 Project 1 个（ComposioHQ/trustclaw）
- sources_tracked.jsonl 健康度：160 条记录（83 article / 77 project）— 新增 trustclaw 条目
- 本轮发现 trustclaw（715 Stars）未追踪，产出 Project 文件并记录到 jsonl

## 线索区

### 源扫描状态（Round 143）
- **Anthropic Engineering Blog**：API endpoint `/api/blog` 返回 404，改用 curl 直接抓取（已解决）
- **Cursor Blog**：curl 成功返回页面内容（JS 渲染已解决）
- **GitHub API**：扫描 20 个候选，Stars ≥ 1000 的项目中多数已追踪
  - ComposioHQ/trustclaw（715 Stars）：**新增**（本轮产出）
- **其他未追踪 GitHub 项目**：simonlin1212/TradingAgents-astock（725）、ComposioHQ/trustclaw（715）、KevRojo/Dulus（708）等

### 未追踪 Press 来源
以下新闻来源均未追踪（Round 142 遗留），下轮可考虑作为第三批次降级补充：
- thenewstack.io/cursor-open-sources-security-agents/（2026-03-16）
- techcrunch.com/2026/03/05/cursor-is-rolling-out-a-new-system-for-agentic-coding/（2026-03-05）
- bloomberg.com/news/articles/2026-03-02/cursor-recurring-revenue-doubles（2026-03-02）
- cnbc.com/2026/02/24/cursor-announces-major-update（2026-02-24）

⚠️ 注意：以上 Press 来源为媒体第三方报道，非官方一手来源。按 SKILL 规范，Articles 须来自 Anthropic/OpenAI/Cursor 等官方博客。这些 Press 来源仅作降级补充，不作为主要 Articles 来源。

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate
- **工作区状态管理**：working state, clean state, artifact, handover, git commit as memory
- **多 Agent 协作**：multi-agent orchestration, agent swarm, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

## 下轮优先线索

1. **Anthropic Engineering Blog**：监控新文章（重点：harness 演进、多 Agent 架构）
2. **GitHub API 新项目**：持续扫描 Stars ≥ 700 新项目（trustclaw 周边生态）
3. **OpenAI Engineering**：JS 渲染问题已确认，降级 AnySearch
4. **Orphan Article 补录**：扫描并补录 20+ 个 orphan 条目到 jsonl（长期任务）

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **160 条记录**（83 article / 77 project）
- 新增 ComposioHQ/trustclaw 条目（715 Stars）

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| GIT_SYNC | ✅ | git pull --rebase → Already up to date |
| SOURCE_SCAN | ✅ | Anthropic（API 404，改用 curl）、Cursor（22 slug ✓）、GitHub API（20 候选）|
| ARTICLES_COLLECT | ⬇️ | 维护轮次，无新 Article（官方博客无新条目）|
| PROJECT_SCAN | ✅ | 发现 trustclaw（715 Stars）未追踪，产出 Project |
| GIT_COMMIT | ✅ | 76943b5 — ComposioHQ/trustclaw |

## 本轮 git commit

- `76943b5` — Round 143: Add ComposioHQ/trustclaw (715 Stars) - Self-hostable personal AI agent with vector memory + Composio tools + Telegram