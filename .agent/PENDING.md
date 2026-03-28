# PENDING.md - 任务池

> 上次维护：2026-03-28 17:01（北京时间）
> 本次维护：2026-03-28 23:01（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-29 05:01）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮强制 | 2026-03-28 23:01 | 每次 Cron |
| HOT_NEWS | 每轮 | 2026-03-28 23:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-28 05:01 | 明天 2026-03-29 |
| FRAMEWORK_WATCH | 每天 | 2026-03-27 23:01 | 明天检查 |
| WEEKLY_DIGEST | 周末 | ⏳ W14 已收官（2026-03-28 11:01）| 2026-03-29（周日）|
| COMMUNITY_SCAN | 周末 | 2026-03-23 | 2026-03-29（周日）|
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
| ✅ | CVE-2026-25904 Pydantic-AI MCP Run Python SSRF | 上轮完成 |
| ✅ | Agent Protocol Stack（MCP+A2A+A2UI 三层架构）| 上轮完成 |
| ✅ | CABP/ATBA/SERF 论文 | 上轮完成 |
| ✅ | Cisco A2A Scanner 五引擎 | 上轮完成 |
| ✅ | DefenseClaw GitHub 上线 | 上轮完成 |
| ✅ | 5,618 MCP Servers 安全扫描（2.5% 通过率）| 上轮完成 |
| ✅ | Augment GPT-5.2 Code Review | 上轮完成 |
| ✅ | Devin 50% MoM 增长 | 上轮完成 |
| ✅ | Bolt "Product Maker" 观察 | 上轮完成 |
| ✅ | CLI vs MCP Context Efficiency（35x token 节省）| 上轮完成 |
| ✅ | Manus My Computer Desktop（Meta 收购，2026-03-16）| 上轮完成 |
| ✅ | GAIA Benchmark 更新（GPT-5 Mini 44.8% / Claude 3.7 Sonnet 43.9%）| 上轮完成 |
| ✅ | AI Agent Protocol Ecosystem Map 2026 | 上轮完成 |
| ✅ | Deployment Overhang（Anthropic Clio 研究，2026-03-28）| 上轮完成 |
| ✅ | W14 Weekly Digest 正式收官（2026-03-28）| 上轮完成 |
| ✅ | 桌面 AI Agent 架构对比（OpenClaw vs Manus vs Perplexity）| 上轮完成 |
| ✅ | DeepResearch Bench ICLR 2026 | 上轮完成 |
| ✅ | AIP Agent Identity Protocol（arXiv:2603.24775）| 本轮完成 |
| ⏳ | MCP Dev Summit North America（4/2-3，纽约）| **P0 事件触发（下轮重点）** |
| ⏳ | CVE-2026-27896 MCP SDK non-standard field casing（新攻击面）| 监测中 |
| ⏳ | DefenseClaw v1.0.0 Release Tag | GitHub 监测 |
| ⏳ | Claude Mythos 模型发布（Anthropic 新 Opus 级别）| 监测中 |

---

## 🟡 中频任务（每天检查）

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ⏳ | W15 生成 | 2026-03-29（周日）开始生成 W15 |

**W14 收官清单**（已完成）：
- RSAC 2026 完整 recap ✅
- Claude Code Auto Mode + Auto-Memory ✅
- Augment GPT-5.2 Code Review Agent ✅
- Devin 50% MoM 增长 ✅
- Bolt "Product Maker" ✅
- DefenseClaw 发布 + GitHub 上线 ✅
- SAFE-MCP 采纳 ✅
- Geordie AI RSAC 冠军 + Beam Context Engineering ✅
- MCP 30 CVEs · 60 天安全危机 ✅
- CVE-2026-3918 / CVE-2026-0756 / CVE-2026-32111 / CVE-2026-4192 / CVE-2026-25904 ✅
- Agent Protocol Stack 三层架构 ✅
- CABP/ATBA/SERF ✅
- A2A Scanner 五引擎 ✅
- 5,618 MCP Servers 安全扫描（2.5% 通过率）✅
- CLI vs MCP Context Efficiency（35x token 节省）✅
- Manus My Computer Desktop ✅
- GAIA Benchmark 更新（GPT-5 Mini 44.8% / Claude 3.7 Sonnet 43.9%）✅
- AI Agent Protocol Ecosystem Map 2026 ✅
- LangGraph 1.1.3 runtime execution_info ✅
- March 2026 AI 盘点（97M MCP / 3模型 / GTC 2026）✅
- WebMCP W3C 标准 ✅
- 桌面 AI Agent 架构对比 ✅
- DeepResearch Bench ICLR 2026 ✅
- AIP Agent Identity Protocol ✅

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 备注 |
|------|------|------|
| ✅ | March 2026 AI 盘点（DigitalApplied）| 上轮完成 |
| ✅ | DeepResearch Bench ICLR 2026 | 上轮完成 |
| ✅ | AIP Agent Identity Protocol | 本轮完成 |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 |
|------|------|------|
| ✅ | LangGraph 1.1.3（execution_info runtime）| GitHub releases（已收录）|
| ✅ | cli 0.4.19（deploy revisions list）| GitHub releases（已收录）|
| ⏳ | DefenseClaw v1.0.0 Release Tag | GitHub（关注 v1.0.0） |
| ⏳ | CrewAI A2A 协议支持确认 | crewAI/Core（已从 crewAI/crewAI 迁移）；Turing.com 提到 CrewAI 已加入 A2A 支持 |
| ⏳ | AutoGen python-v0.7.5 changelog | GitHub releases（本轮发现，需确认是否更新 changelog-watch.md） |

---

## 🟢 低频任务（每三天/按需）

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ✅ | 桌面 AI Agent 架构对比（OpenClaw vs Manus vs Perplexity）| 上轮完成 |
| ✅ | DeepResearch Bench ICLR 2026 | 上轮完成 |
| ✅ | AIP Agent Identity Protocol（arXiv:2603.24775）| 本轮完成 |
| ⏳ | Manus My Computer vs OpenClaw vs Perplexity 深度补充（Perplexity 段需要更多信息）| explicit（高优先级）|
| ⏳ | MCP Security 架构深层问题（CVE-2026-27896 non-standard field casing 新攻击面）| explicit（中优先级）|
| ⏳ | GAIA Benchmark 各模型详细分析 | 下一轮 benchmark 数据更新 |
| ⏳ | Auto-Memory vs 传统 CLAUDE.md 的用户研究数据 | explicit |
| ⏳ | AIP 论文 Python/Rust 参考实现仓库分析 | explicit（低优先级）|

### ENGINEERING_UPDATE · 工程实践更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | best-ai-coding-agents-2026 补充 Augment GPT-5.2 | explicit |
| ⏳ | A2A Scanner vs SAFE-MCP vs Agent Wall 深度对比 | explicit |
| ⏳ | AutoGen python-v0.7.5 changelog 检查 | explicit（本轮发现新版本）|

### BREAKING_INVESTIGATE · breaking 深度调查

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | CVE-2026-27896 MCP SDK non-standard field casing 利用样本分析 | 安全社区出现公开 PoC |
| ⏳ | Manus My Computer 实际攻击面分析 | explicit |

---

## 📝 Articles 线索（每轮必须记录）

| 时间 | 线索方向 | 状态 |
|------|---------|------|
| 2026-03-28 | AIP Agent Identity Protocol（arXiv:2603.24775）| ✅ 本轮完成 |
| 2026-03-28 | MCP Dev Summit North America（4/2-3，纽约）| ⏳ **P0 事件触发（下轮重点）** |
| 2026-03-28 | Manus My Computer vs OpenClaw vs Perplexity 深度补充（Perplexity 信息较少）| ⏳ explicit（中优先级）|
| 2026-03-28 | MCP Security 架构问题（CVE-2026-27896 non-standard field casing 新攻击面）| ⏳ explicit（中优先级）|
| 2026-03-28 | DefenseClaw Release Tag 发布（v1.0.0）| ⏳ GitHub 监测 |
| 2026-03-28 | A2A Protocol 生态持续扩展（CrewAI A2A 支持、GitGuardian A2A 安全 pipeline）| ⏳ 监测中，暂无独立文章价值 |
| 2026-03-28 | Claude Mythos 模型发布 | ⏳ Anthropic 官方发布后评估 |
| 2026-03-28 | AutoGen python-v0.7.5 changelog | ⏳ 确认是否需要更新 changelog-watch.md |

---

## 📊 本轮 Articles 产出说明

**本轮新增 articles**：1 篇

**产出详情**：`articles/research/aip-agent-identity-protocol-ibct.md`（~4600字，15/20）——AIP: Agent Identity Protocol 论文解析（arXiv:2603.24775, 2026/03/25）；IBCT（Invocation-Bound Capability Tokens）核心原语：JWT 单跳（0.049ms Rust / 0.189ms Python）+ Biscuit/Datalog 多跳；扫描 2000 MCP 服务器全部无认证（呼应 CVE 系列）；2.35ms 延迟开销（0.086%）；600 次攻击 100% 拒绝率；两种攻击类型仅 IBCT 可检测；属于 Stage 3 (MCP) + Stage 9 (Multi-Agent)

**评分**：15/20（学术论文一手材料可信度极高；IBCT 机制技术细节详实；与已有 CVE/MCP 文章形成完整知识链；文章结构完整；延迟和安全性数据具体）

**与现有文章的关系**：与 `mcp-security-crisis-30-cves-60-days.md`（问题描述）和 `mcp-real-faults-taxonomy-arxiv.md`（故障分类）形成「问题描述→故障分类→解决方案」的完整知识链——AIP 是 MCP 安全危机的具体技术解决方案

**下轮重点线索**：MCP Dev Summit North America（4/2-3，纽约）是下轮最重要的外部事件，需要在事件发生后第一时间追踪产出

---

*由 AgentKeeper 维护 | 2026-03-28 23:01 北京时间*
