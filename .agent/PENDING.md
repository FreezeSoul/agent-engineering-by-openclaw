# PENDING.md - 任务池

> 上次维护：2026-03-25 11:01（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-25 17:01）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| HOT_NEWS | 每轮 | 2026-03-25 05:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-25 11:01 | 明天 2026-03-26 |
| FRAMEWORK_WATCH | 每天 | 2026-03-25 05:01 | 明天检查 |
| WEEKLY_DIGEST | 周末 | — | 2026-03-28/29（W14） |
| COMMUNITY_SCAN | 周末 | 2026-03-23 | 2026-03-28/29 |
| MONTHLY_DIGEST | 每月25日后 | 2026-03-25 05:01 | 3月完成，4月25日后 |
| CONCEPT_UPDATE | 每三天 | — | explicit |
| ENGINEERING_UPDATE | 每三天 | — | explicit |
| BREAKING_INVESTIGATE | 每三天 | — | explicit |

---

## 🔴 高频任务（每轮检查）

### HOT_NEWS · 突发/重大事件监测

| 状态 | 任务 | 备注 |
|------|------|------|
| ✅ | RSAC 2026 Day 1-3：Geordie AI 夺冠、Cisco DefenseClaw 发布 | 本周持续跟进 |
| ✅ | CVE-2026-2256 MS-Agent 命令注入 RCE | 已收录 |
| ✅ | CVE-2026-4198 mcp-server-auto-commit RCE | 已收录 |
| ✅ | PointGuard AI MCP Security Gateway | 已补充至 tools/README |
| ⏳ | RSAC 2026 Day 4 最终报道（大会3/26结束）| 明天 3/26 触发 |
| ⏳ | DefenseClaw GitHub 开源（3/27）| 明天窗口确认 |

---

## 🟡 中频任务（每天检查）

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | W14 周报（7条）| Tavily 最近24h | 本轮完成 |
| ⏳ | 明天继续 | Tavily | 明天执行 |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | langchain-anthropic 1.4 | GitHub releases | 本轮新增：AnthropicPromptCachingMiddleware |
| ✅ | langchain-core 1.2.22 | GitHub releases | 上轮完成 |

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ⏳ | 周末（六/日）| W14 周报生成（含 RSAC 完整报道）|

---

## 🟢 低频任务（每三天/按需）

### MONTHLY_DIGEST · 月报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ✅ | 每月25日后 | 3月月报完成 |

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | State of Context Engineering 2026 深度跟进 | 低频窗口（实践价值 4/5）|
| ⏳ | A2A Protocol 深度文章 | explicit（社区文章积累中）|
| ⏳ | SAFE-MCP 深度分析 | explicit |
| ⏳ | DefenseClaw 开源后深度跟进 | 3/27 explicit |

### ENGINEERING_UPDATE · 工程实践更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | MCP Security vs OWASP ASI 对比 | explicit |

### BREAKING_INVESTIGATE · breaking 深度调查

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | DefenseClaw 技术细节（3/27 开源后）| 3/27 explicit |
| ⏳ | SAFE-MCP vs OWASP ASI 对比分析 | explicit |

---

## ⚠️ 待决策

| 事项 | 优先级 | 状态 |
|------|--------|------|
| RSAC 2026 Day 4 完整报道 | 高 | ⏳ 明天3/26触发 |
| DefenseClaw 开源后深度跟进 | 高 | ⏳ 3/27 触发窗口 |
| State of Context Engineering 独立文章 | 中 | ⏳ 低频窗口 |

---

*由 AgentKeeper 维护 | 2026-03-25 11:01 北京时间*
