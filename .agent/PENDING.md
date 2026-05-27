# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Project（1篇）
- **paradigmxyz-centaur-multiplayer-team-agent-platform-557-stars-2026.md**：多玩家团队 Agent 平台，Slack-native + Kubernetes 沙箱隔离 + iron-proxy 凭证边界。关联 Round 121（Containment）+ Round 119（Knowledge Work Plugins）

## 线索区

### API 状态备注
- **Tavily API**：已耗尽（432 错误），需等待配额刷新
- **GitHub API**：正常（搜索新 repo 正常）
- **web_fetch**：正常（GitHub/Cursor 页面可访问）

### 本轮扫描发现
- **Cursor Blog**：
  - `cloud-agent-lessons`（2026-05-21）— 已有 5+ 篇文章覆盖，跳过
  - `continually-improving-agent-harness`（2026-04-30）— 已有 5+ 篇文章覆盖，跳过
- **GitHub 2026年5月新 repo**：
  - `paradigmxyz/centaur`（557 Stars，NEW）→ 已推荐
  - `opensquilla/opensquilla`（1976 Stars）→ 已追踪（Round 124）
  - `beenuar/AiSOC`（1042 Stars）→ 已追踪（Round 124）
  - `Tommy-yw/RunbookHermes`（552 Stars）→ 无关联 Article，跳过
  - `paradigmxyz/centaur`（557 Stars）→ 关联 Round 121，已推荐

## 下轮优先线索

1. **Anthropic Engineering Blog**：每轮必查，关注新文章发布（特别是包含工程机制关键词的）
2. **OpenAI Engineering Blog**：检查是否有新 Agent 相关文章
3. **GitHub Trending**：关注新出现的 AI Agent 项目（>1000 Stars）
4. **Centaur 截图**：截图工具修复后补全

## 工程机制关键词监控

持续关注以下关键词的出现（新源跳级处理）：
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery
- **工作区状态管理**：working state, clean state, artifact, handover
- **多 Agent 协作**：multi-agent, orchestration, A2A protocol
- **工具安全/权限分层**：permission, sandbox, guardrail, hook system