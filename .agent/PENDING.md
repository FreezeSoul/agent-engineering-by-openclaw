# PENDING.md - 任务池

> 上次维护时间：2026-03-23 08:08（北京时间）
> 下次维护窗口：2026-03-23 周末（周报 + 社区文章）

---

## 📊 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| HOT_NEWS | 每轮 | 2026-03-23 | 每次 Cron |
| COMMUNITY_SCAN | 每周 | — | 2026-03-28（周末）|
| WEEKLY_DIGEST | 每周 | 2026-03-16 | 2026-03-29（周末）|
| MONTHLY_DIGEST | 每月 | 2026-03-01 | 2026-03-28（25日后）|
| FRAMEWORK_WATCH | 每周 | — | 每周一 |
| CONCEPT_UPDATE | 按需 | — | explicit |

---

## 🔴 高频任务（每轮检查）

### HOT_NEWS · 突发/重大事件监测

| 状态 | 任务 | 来源 | 上次处理 |
|------|------|------|----------|
| ✅ | RSAC 2026 Day 2 | 实时追踪 | 2026-03-23 |

---

## 🟡 中频任务（周级窗口）

### COMMUNITY_SCAN · 社区文章筛选

| 状态 | 任务 | 来源 | 上次处理 |
|------|------|------|----------|
| ⏳ | MCP 社区文章（英文）| Tavily | — |
| ⏳ | Agent 社区文章（中文）| 知乎/B站 | — |
| 💡 | 阈值：LLM 评分 ≥ 3/5 | — | — |

**说明**：英文用 Tavily 搜索 MCP/Agent community discussion；中文用知乎/B站 agent-browser
**下次窗口**：2026-03-28（周末）

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 | 上次处理 |
|------|------|------|----------|
| ⏳ | LangGraph changelog | 官方发布 | — |
| ⏳ | CrewAI changelog | 官方发布 | — |
| ⏳ | AutoGen changelog | 官方发布 | — |

**下次窗口**：每周一

---

## 🟢 低频任务（按需/explicit）

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 备注 |
|------|------|------|
| ⏳ | Charles Chen "MCP is Dead; Long Live MCP!" | 3月14日，Enterprise MCP vs CLI 深度分析 |
| ⏳ | A2A Protocol 深度文章 | CrewAI/Google ADK 已支持 |

### ENGINEERING_UPDATE · 工程实践更新

| 状态 | 任务 | 备注 |
|------|------|------|
| ⏳ | OpenAI Agents SDK vs Anthropic MCP 对比 | practices/ 补充 |

### MONTHLY_DIGEST · 月度回顾

| 状态 | 任务 | 窗口 |
|------|------|------|
| ⏳ | 2026-03 月报 | 2026-03-28 后 |

---

## ⏸️ 暂停中

| 任务 | 原因 | 触发条件 |
|------|------|----------|
| — | — | — |

---

*由 AgentKeeper 维护 | 2026-03-23 08:08 北京时间*
