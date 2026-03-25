# PENDING.md - 任务池

> 上次维护：2026-03-25 12:40（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-25 18:40）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮强制 | 2026-03-25 12:40 | 每次 Cron |
| HOT_NEWS | 每轮 | 2026-03-25 05:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-25 12:40 | 明天 2026-03-26 |
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
| ✅ | Microsoft Agent Framework 发布（官方 MCP 支持）| 本轮新增发现 |
| ⏳ | RSAC 2026 Day 4 最终报道（大会3/26结束）| 明天 3/26 触发 |
| ⏳ | DefenseClaw GitHub 开源（3/27）| 明天窗口确认 |

---

## 🟡 中频任务（每天检查）

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | W14 周报（10条）| Tavily 最近24h | 本轮完成 |
| ⏳ | 明天继续 | Tavily | 明天执行 |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ⏳ | crewAI releases 获取失败（API 404）| GitHub API | 需确认正确 API 路径 |
| ⏳ | LangChain releases | GitHub API | 明天检查 |
| ⏳ | Microsoft Agent Framework | 官方博客 | 本轮发现，待深入追踪 |

### AWESOME_GITHUB · GitHub 精选集扫描

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ⏳ | Microsoft Agent Framework 补充至框架追踪 | gabrielmongeon.ca | 本轮发现，待补充 |

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ⏳ | 周末（六/日）| W14 周报生成（含 RSAC 完整报道 + DefenseClaw）|

---

## 🟢 低频任务（每三天/按需）

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | Microsoft Agent Framework 深度跟进 | explicit（官方框架，高价值）|
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
| Microsoft Agent Framework 深度文章 | 中 | ⏳ 低频窗口 |

---

## 📝 Articles 线索（每轮必须记录）

| 时间 | 线索方向 | 状态 |
|------|---------|------|
| 2026-03-25 | Microsoft Agent Framework：与 Foundry/MCP 的集成深度、CABP 协议支持情况 | ⏳ 待追踪 |
| 2026-03-25 | Skill Composition：Skill Registry 生态（ClawHub / Composio）| ⏳ 低频窗口 |

---

*由 AgentKeeper 维护 | 2026-03-25 12:40 北京时间*
