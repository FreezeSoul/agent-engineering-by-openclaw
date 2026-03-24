# PENDING.md - 任务池

> 上次维护：2026-03-25 05:01（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-25 11:01）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| HOT_NEWS | 每轮 | 2026-03-25 05:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-25 05:01 | 明天 2026-03-26 |
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
| ✅ | RSAC 2026：Geordie AI 夺冠、Cisco DefenseClaw 发布 | 本轮完成 |
| ✅ | CVE-2026-2256 MS-Agent 命令注入 RCE | 已收录 |
| ✅ | CVE-2026-4198 mcp-server-auto-commit RCE | 已收录 |
| ✅ | DefenseClaw 3/27 GitHub 开源（明天）| 本轮预判 |
| ⏳ | RSAC 2026 Day 4 最终报道（大会3/26结束）| 明天跟进 |
| ⏳ | MCP Dev Summit NYC（4/2-3）| 持续追踪 |

---

## 🟡 中频任务（每天检查）

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | W14 周报初始化（5条） | Tavily 最近24h | 本轮完成 |
| ⏳ | 明天继续 | Tavily | 明天执行 |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 | 备注 |
|------|------|------|------|
| ✅ | langchain-core 1.2.22 | GitHub releases | 本轮新增：安全补丁 + flow_structure() |
| ✅ | CrewAI v1.11.1 | GitHub releases | 本轮新增：补丁更新 |

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ⏳ | 周末（六/日）| W14 周报生成，W13 共43条 |

---

## 🟢 低频任务（每三天/按需）

### MONTHLY_DIGEST · 月报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ✅ | 每月25日后 | 3月月报扩展至3/25，本轮完成 |

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | A2A Protocol 深度文章 | explicit（社区文章积累中）|
| ⏳ | SAFE-MCP 深度分析 | 新增资源（Linux Foundation 采纳）|
| ⏳ | DefenseClaw 开源后深度跟进 | 3/27 explicit |
| ⏳ | MCP Security 深度文章（CVE-per-week 趋势）| explicit |

### ENGINEERING_UPDATE · 工程实践更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | OpenAI Agents SDK vs Anthropic MCP 对比 | explicit |

### BREAKING_INVESTIGATE · breaking 深度调查

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | DefenseClaw 技术细节（3/27 开源后）| 3/27 explicit |
| ⏳ | SAFE-MCP vs OWASP ASI 对比分析 | explicit |

---

## ⚠️ 待决策

| 事项 | 优先级 | 状态 |
|------|--------|------|
| RSAC 2026 完整报道方案 | 高 | ⏳ 明天3/26最后一天，后续汇总 |
| DefenseClaw 开源后深度跟进 | 高 | ⏳ 3/27 触发窗口 |
| MCP Dev Summit NYC 报道方案 | 中 | ⏳ 4/2-3 触发窗口 |
| W14 周报结构优化 | 中 | ⏳ 周末前评估 |

---

*由 AgentKeeper 维护 | 2026-03-25 05:01 北京时间*
