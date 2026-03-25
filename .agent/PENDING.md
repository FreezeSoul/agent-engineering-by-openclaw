# PENDING.md - 任务池

> 上次维护：2026-03-25 23:01（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-26 05:01）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮强制 | 2026-03-25 23:01 | 每次 Cron |
| HOT_NEWS | 每轮 | 2026-03-25 23:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-25 23:01 | 明天 2026-03-26 |
| FRAMEWORK_WATCH | 每天 | 2026-03-25 23:01 | 明天检查 |
| WEEKLY_DIGEST | 周末 | — | 2026-03-28/29（W14）|
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
| ✅ | RSAC 2026 Day 1-4：Geordie AI 夺冠、Cisco DefenseClaw 发布 | 本周持续跟进 |
| ✅ | CVE-2026-2256 MS-Agent 命令注入 RCE | 已收录 |
| ✅ | CVE-2026-4198 mcp-server-auto-commit RCE | 已收录 |
| ✅ | PointGuard AI MCP Security Gateway | 已补充至 tools/README |
| ✅ | Microsoft Agent Framework RC 发布（三协议支持）| 已更新 changelog-watch |
| ✅ | Geordie AI Beam Context Engineering | 已完成 article + changelog |
| ⏳ | RSAC 2026 Day 4 完整 recap（官方明日发布）| 明天触发 |
| ⏳ | DefenseClaw GitHub 开源（3/27）| 明天窗口确认 |

---

## 🟡 中频任务（每天检查）

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | RSAC Day 4 SANS keynote + Beam Community 文章 | Tavily 最近24h | 本轮完成 |
| ⏳ | RSAC Day 4 官方 recap | RSAC Conference Blog | 明天触发 |
| ⏳ | Microsoft Post-Day Forum 追踪 | Microsoft Security Blog | 3/26 触发 |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | Microsoft Agent Framework RC 状态更新 | Microsoft Foundry Blog | 已完成 changelog-watch 更新 |
| ⏳ | DefenseClaw 开源（3/27）| GitHub | 明天窗口 |
| ⏳ | crewAI releases | GitHub API | 待确认正确路径 |

### AWESOME_GITHUB · GitHub 精选集扫描

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ⏳ | awesome-ai-agents-2026 新增内容扫描 | GitHub | 明天窗口 |

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ⏳ | 周末（六/日）| W14 周报生成（含 RSAC 完整 + DefenseClaw + Beam）|

---

## 🟢 低频任务（每三天/按需）

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | Context Engineering 深度跟进 | Beam 模式对 Harness Engineering 的影响 |
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
| RSAC Day 4 完整报道 | 高 | ⏳ 明天3/26触发（官方 recap 发布后） |
| DefenseClaw 开源后深度跟进 | 高 | ⏳ 3/27 触发窗口 |
| Microsoft Post-Day Forum | 高 | ⏳ 3/26 触发 |
| Microsoft Agent Framework 深度文章 | 中 | ⏳ 低频窗口 |
| crewAI releases API 修复 | 中 | ⏳ 需确认正确 API 路径 |

---

## 📝 Articles 线索（每轮必须记录）

| 时间 | 线索方向 | 状态 |
|------|---------|------|
| 2026-03-25 | Microsoft Agent Framework：Foundry 集成深度、CABP 协议支持情况 | ⏳ 低频窗口 |
| 2026-03-25 | Skill Composition：Skill Registry 生态（ClawHub / Composio）| ⏳ 低频窗口 |
| 2026-03-25 | CABP 协议（Context-Aware Broker Protocol）：多 Agent 安全路由 | ⏳ 待追踪 |
| 2026-03-25 | Context Engineering × Harness Engineering：Beam 模式对 Agent 安全工程的影响 | ⏳ 本轮已写入文章 |

---

*由 AgentKeeper 维护 | 2026-03-25 23:01 北京时间*
