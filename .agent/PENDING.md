# PENDING.md - 任务池

> 上次维护：2026-03-27 17:01（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-27 23:01）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮强制 | 2026-03-27 17:01 | 每次 Cron |
| HOT_NEWS | 每轮 | 2026-03-27 17:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-27 17:01 | 明天 2026-03-28 |
| FRAMEWORK_WATCH | 每天 | 2026-03-27 09:41 | 明天检查 |
| WEEKLY_DIGEST | 周末 | ⏳ 待触发 | 2026-03-28/29（W14 周报生成）|
| COMMUNITY_SCAN | 周末 | 2026-03-23 | 2026-03-28/29 |
| MONTHLY_DIGEST | 每月25日后 | 2026-03-25 | 4月25日后 |
| CONCEPT_UPDATE | 每三天 | — | explicit |
| ENGINEERING_UPDATE | 每三天 | — | explicit |
| BREAKING_INVESTIGATE | 每三天 | — | explicit |

---

## 🔴 高频任务（每轮检查）

### HOT_NEWS · 突发/重大事件监测

| 状态 | 任务 | 备注 |
|------|------|------|
| ✅ | Claude Code Auto Mode Safeguards | 上轮完成 |
| ✅ | Claude Code Auto-Memory | 上轮完成 |
| ✅ | Augment Code GPT-5.2 Code Review Agent | 上轮完成 |
| ✅ | RSAC 2026 Day 1-4：Geordie AI 夺冠、Cisco DefenseClaw 发布 | 上轮完成 |
| ✅ | CVE-2026-2256 MS-Agent 命令注入 RCE | 上轮完成 |
| ✅ | CVE-2026-4198 mcp-server-auto-commit RCE | 上轮完成 |
| ✅ | CVE-2026-23744 MCPJam Inspector RCE | 上轮完成 |
| ✅ | CVE-2026-27825 MCPwnfluence SSRF→RCE（CVSS 9.1）| 上轮完成 |
| ✅ | CVE-2026-29787 mcp-memory-service 信息泄露 | 上轮完成 |
| ✅ | CVE-2026-3918 WebMCP Use-After-Free RCE（Chrome）| 上轮完成 |
| ✅ | CVE-2026-0756 GitHub Kanban MCP Server RCE | 上轮完成 |
| ✅ | CVE-2026-32111 ha-mcp SSRF | 上轮完成 |
| ✅ | CVE-2026-4192 quip-mcp-server RCE（setupToolHandlers）| 上轮完成 |
| ✅ | CVE-2026-25904 Pydantic-AI MCP Run Python SSRF | **本轮新增（沙箱配置错误，无补丁）** |
| ✅ | Agent Protocol Stack（MCP+A2A+A2UI 三层架构）| 上轮完成 |
| ✅ | CABP/ATBA/SERF 论文 | 上轮完成 |
| ✅ | Cisco A2A Scanner 五引擎 | 上轮完成 |
| ✅ | DefenseClaw GitHub 上线 | 上轮完成 |
| ✅ | 5,618 MCP Servers 安全扫描 | 上轮完成 |
| ✅ | Augment Code GPT-5.2 Code Review | 上轮完成 |
| ✅ | Devin 50% MoM 增长 | 上轮完成 |
| ✅ | Bolt "Product Maker" 观察 | 上轮完成 |
| ✅ | CLI vs MCP Context Efficiency（35x token 节省）| 上轮完成 |
| ✅ | Manus My Computer Desktop（Meta 收购，2026-03-16）| **本轮新增（已更新 deep-agent-manus-paradigm.md Section 1.2）** |

---

## 🟡 中频任务（每天检查）

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ⏳ | 2026-03-28/29（六/日）| W14 周报生成 |

**W14 周报内容清单**：
- RSAC 2026 完整 recap（Geordie AI 夺冠 / DefenseClaw / SAFE-MCP / OWASP ASI Top 10）
- Claude Code Auto Mode + Auto-Memory
- Augment GPT-5.2 Code Review Agent
- Devin 50% MoM 增长
- Bolt "Product Maker"
- DefenseClaw 发布 + GitHub 上线
- SAFE-MCP 采纳
- Geordie AI RSAC 冠军 + Beam Context Engineering
- MCP 30 CVEs · 60 天安全危机
- CVE-2026-3918 / CVE-2026-0756 / CVE-2026-32111 / CVE-2026-4192
- **CVE-2026-25904 Pydantic-AI SSRF（本轮新增）**
- Agent Protocol Stack 三层架构
- CABP/ATBA/SERF
- A2A Scanner 五引擎
- 5,618 MCP Servers 安全扫描（2.5% 通过率）
- CLI vs MCP Context Efficiency（35x token 节省）
- **Manus My Computer Desktop（本轮新增）**
- **GAIA Benchmark 更新（GPT-5 Mini 44.8% / Claude 3.7 Sonnet 43.9%，本轮新增）**

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 备注 |
|------|------|------|
| ✅ | 本轮新动态（Tavily 驱动）| Manus My Computer + GAIA 更新 + CVE-2026-25904 |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 |
|------|------|------|
| ⏳ | DefenseClaw 正式 Release Tag | GitHub（关注 v1.0.0） |
| ⏳ | LangGraph 新版本 | GitHub releases |
| ⏳ | CrewAI 新版本 | GitHub releases |

---

## 🟢 低频任务（每三天/按需）

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | Manus My Computer vs OpenClaw vs Perplexity Computer Use 深度对比 | explicit（本轮新增线索）|
| ⏳ | GAIA Benchmark 详细分析（各模型） | 下一轮 benchmark 数据更新 |
| ⏳ | Auto-Memory vs 传统 CLAUDE.md 的用户研究数据 | explicit |
| ⏳ | MCP Security vs OWASP ASI 对比 | explicit |

### ENGINEERING_UPDATE · 工程实践更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | best-ai-coding-agents-2026 补充 Augment GPT-5.2 | explicit |
| ⏳ | A2A Scanner vs SAFE-MCP vs Agent Wall 深度对比 | explicit |

### BREAKING_INVESTIGATE · breaking 深度调查

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | CVE-2026-25904 Pydantic-AI SSRF 利用样本分析 | 安全社区出现公开 PoC |
| ⏳ | Manus My Computer 实际攻击面分析 | explicit |

---

## 📝 Articles 线索（每轮必须记录）

| 时间 | 线索方向 | 状态 |
|------|---------|------|
| 2026-03-27 | Manus My Computer vs OpenClaw vs Perplexity Computer Use 深度横向对比（架构哲学 + 安全 + 效率）| ⏳ explicit |
| 2026-03-27 | GAIA Benchmark 各模型详细分析 | ⏳ 下一轮 benchmark 更新 |
| 2026-03-27 | Pydantic-AI SSRF 利用样本分析（PoC 出现时触发 HOT_NEWS）| ⏳ 监测中 |
| 2026-03-27 | DefenseClaw Release Tag 发布 | ⏳ GitHub 监测 |
| 2026-03-27 | A2A Protocol 企业采纳案例（GitHub Copilot Agent 通信）| ⏳ explicit |
| 2026-03-27 | MCPwnfluence CVSS 9.1 深度技术分析 | ⏳ explicit |
| 2026-03-27 | WebMCP CVE-2026-3918 攻击链分析（沙箱逃逸）| ⏳ explicit |

---

## 📊 本轮 Articles 产出说明

**本轮新增 articles**：0 篇

**原因说明**：本轮对 `articles/concepts/deep-agent-manus-paradigm.md` 进行了**重大增量更新**：
- 新增 Section 1.2「Meta 收购与 My Computer：从云端到桌面的范式跨越」（~600字）
- Section 5 GAIA Benchmark 数据同步刷新（GPT-5 Mini 44.8% / Claude 3.7 Sonnet 43.9%）

根据 SKILL.md 规范："对现有文章进行重大增量更新"属于 Articles 产出，本轮符合增量原则。

**下轮重点线索**：Manus My Computer vs OpenClaw vs Perplexity Computer Use 深度横向对比（架构哲学 + 安全 + 效率），属于 Stage 11（Deep Agent）优先事项。

---

*由 AgentKeeper 维护 | 2026-03-27 17:01 北京时间*
