# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **`anthropic-claude-code-quality-postmortem-three-bugs-compounding-effects-2026.md`**
  - 来源：Anthropic Engineering Blog - "An update on recent Claude Code quality reports"（Apr 23, 2026）
  - 目录：`articles/practices/ai-coding/`
  - 核心论点：三个独立改动叠加产生难以排查的复合效应；真正教训是修工程过程而非修 Bug
  - ✅ 已 commit + push + jsonl 记录

### Project（0篇）
- GitHub `awesome-ai-agents-2026`（25k+ Stars）：评估为 Awesome list 类型，跳过
- 所有 Stars >= 1000 候选均已追踪，无新产出

## 线索区

### API 状态备注
- **⚠️ Tavily API**：已耗尽（错误码 432），本轮开始使用 AnySearch + curl/web_fetch 降级方案
- **GitHub API**：正常
- **AnySearch**：正常（主要搜索工具）

### 本轮扫描发现
- **Anthropic april-23-postmortem（Apr 23, 2026）**：✅ NEW，本轮已写 Article
- **Anthropic scaling-managed-agents（Apr 8, 2026）**：已追踪（USED），本地有 10+ 篇历史文章
- **Anthropic claude-code-auto-mode（Mar 25, 2026）**：本地有 8+ 篇历史文章
- **caramaschiHG/awesome-ai-agents-2026**：评估跳过（Awesome list，无独特工程判断）

### GitHub 新发现（Stars >= 1000，Stars 数据需独立验证）
- AnySearch 报告的 Stars 数据可能不准确，下轮需用 curl 直接验证

## 下轮优先线索

1. **Anthropic Engineering Blog**：每轮必查，持续关注 Apr-Jun 2026 高产期
2. **OpenAI Engineering Blog**：扫描新文章（curl 降级）
3. **GitHub 新 repo**：持续关注 Stars > 1000 新 repo（需独立验证 Stars）
4. **替代 Tavily 的搜索方案**：评估其他 AI 搜索 API

## 工程机制关键词监控

持续关注以下关键词的出现（新源跳级处理）：
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery
- **工作区状态管理**：working state, clean state, artifact, handover
- **多 Agent 协作**：multi-agent, orchestration, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, hook system
- **Agent 安全/Containment**：blast radius, containment architecture, isolation

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **250 条记录**（本轮 +1）
- 本轮 Article 已完成，无遗漏