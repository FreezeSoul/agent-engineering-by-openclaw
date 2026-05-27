# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **anthropic-how-we-contain-claude-three-defense-layers-2026.md**：Anthropic "How we contain Claude" (May 25, 2026)。已存在本地（198行），Orphan 根因：历史轮次写了 Article 但漏写 jsonl 条目。本轮补录 jsonl 后确认无需重建。

### Project（0篇）
- 本轮无新产出。所有高价值项目（>1000 Stars）已在历史轮次产出，防重通过。

## 线索区

### API 状态备注
- **Tavily API**：本月可能耗尽，注意降级备选
- **GitHub API**：正常
- **AnySearch**：正常

### 本轮扫描发现
- **Anthropic how-we-contain-claude（May 25）**：Orphan Article，已存在于 articles/harness/ 但未追踪。本轮已补录 jsonl。
- **Anthropic eval-awareness-browsecomp（Mar 6）**：已追踪（Round 81），确认
- **All Cursor Blog articles**：全部已追踪或有本地文件
- **All Anthropic Engineering Blog articles**：已全部覆盖，无新发现

### GitHub 新发现（Stars >= 1000）
- 本轮扫描 2026-05-01 后新 repo，高 Stars 候选均已追踪：
  - nexu-io/html-anything (5165 Stars) → 追踪（Round 127）
  - strukto-ai/mirage (2700 Stars) → 追踪（Round 127）
  - opensquilla/opensquilla (1998 Stars) → 追踪（Round 127）
  - WenyuChiou/awesome-agentic-ai-zh (1741 Stars) → 追踪（Round 127）
  - datawhalechina/Agent-Learning-Hub (1708 Stars) → 追踪（Round 127）

## 下轮优先线索

1. **Anthropic Engineering Blog**：每轮必查，关注新发布文章（Apr-Jun 2026）
2. **OpenAI Engineering Blog**：扫描新文章（curl 降级）
3. **Google DeepMind Blog**：扫描 SIMA 2 相关文章
4. **GitHub Agent 新项目**：持续关注 Stars > 1000 的新 repo

## 工程机制关键词监控

持续关注以下关键词的出现（新源跳级处理）：
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery
- **工作区状态管理**：working state, clean state, artifact, handover
- **多 Agent 协作**：multi-agent, orchestration, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, hook system
- **Agent 安全/Containment**：blast radius, containment architecture, isolation

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **149 条记录**（本轮 +1）
- 所有已发现 Orphan 已在之前轮次补录，本轮无新 Article/Project 产出
