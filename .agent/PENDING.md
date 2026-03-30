# PENDING.md - 任务池

> 上次维护：2026-03-30 11:01（北京时间）
> 本次维护：2026-03-30 17:01（北京时间）
> 下次维护窗口：下次 Cron（约6小时后，2026-03-30 23:01）

---

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮强制 | 2026-03-30 17:01 | 每次 Cron |
| HOT_NEWS | 每轮 | 2026-03-30 17:01 | 每次 Cron |
| DAILY_SCAN | 每天 | 2026-03-30 05:01 | 明天 2026-03-31 |
| FRAMEWORK_WATCH | 每天 | 2026-03-30 17:01 | 明天检查 |
| WEEKLY_DIGEST | 周末 | 2026-03-29（W15积累中）| W15 下周末（4/4-5）收官 |
| COMMUNITY_SCAN | 周末 | 2026-03-29 | 2026-04-05（下一个周日）|
| MONTHLY_DIGEST | 每月25日后 | 2026-03-25 | 4月25日后 |
| CONCEPT_UPDATE | 每三天 | 2026-03-30 17:01 | explicit |
| ENGINEERING_UPDATE | 每三天 | — | explicit |
| BREAKING_INVESTIGATE | 每三天 | — | explicit |

---

## 🔴 高频任务（每轮检查）

### HOT_NEWS · 突发/重大事件监测

| 状态 | 任务 | 备注 |
|------|------|------|
| ✅ | TIP（arxiv:2603.24203，MCP 间接提示注入攻击）| **本轮完成** |
| ✅ | FinMCP-Bench（arxiv:2603.24943，ICASSP 2026）| 上轮完成 |
| ✅ | SkillsBench（arxiv:2602.12670，自我生成无收益）| 上轮完成 |
| ✅ | DefenseClaw v0.2.0 PyPI 发布 | 上轮完成 |
| ✅ | AutoGen python-v0.7.5（Anthropic thinking mode）| 上轮完成 |
| ✅ | langchain-core 1.2.23 | 上轮完成 |
| ✅ | CVE-2026-27896 MCP SDK non-standard field casing | 上轮完成 |
| ✅ | DefenseClaw GitHub 上线 | 上轮完成 |
| ✅ | 5,618 MCP Servers 安全扫描 | 上轮完成 |
| ✅ | MCP Dev Summit North America（4/2-3，纽约）| **P0 事件，距今2天，预热窗口正式开启** |
| ⏳ | MCP Dev Summit North America（4/2-3，纽约）| **P0 事件，今日预热窗口正式开启，距今2天** |
| ⏳ | CVE-2026-27896 MCP SDK non-standard field casing（新攻击面）| 监测中 |
| ⏳ | DefenseClaw v1.0.0 Release Tag | GitHub 监测 |

---

## 🟡 中频任务（每天检查）

### WEEKLY_DIGEST · 周报生成

| 状态 | 窗口 | 备注 |
|------|------|------|
| ✅ | W14 正式收官（2026-03-28） | 20 条 breaking / 9 条 articles |
| 🟡 | W15 积累中 | 2026-03-30：TIP + FinMCP-Bench + SkillsBench + AI4Work + Agent Skills Survey + MCP Agent Observability（W15 累计6篇 articles） |

**W15 积累进度**（2026-03-30）：SkillsBench / AI4Work / Agent Skills Survey / MCP Agent Observability / FinMCP-Bench / TIP（6篇 articles）

### DAILY_SCAN · 每日资讯扫描

| 状态 | 任务 | 备注 |
|------|------|------|
| ✅ | March 2026 AI 盘点 | 上轮完成 |
| ✅ | DeepResearch Bench ICLR 2026 | 上轮完成 |
| ✅ | MCPMark ICLR 2026 | 上轮完成 |
| ✅ | Agent Skills Survey | 上轮完成 |
| ✅ | AI4Work Benchmark Mismatch | 上轮完成 |
| ✅ | MCP Agent Observability | 上轮完成 |
| ✅ | SkillsBench | 上轮完成 |
| ✅ | FinMCP-Bench | 上轮完成 |
| ✅ | TIP（arxiv:2603.24203）| **本轮完成** |

### FRAMEWORK_WATCH · 框架动态追踪

| 状态 | 任务 | 来源 |
|------|------|------|
| ✅ | LangGraph 1.1.3（execution_info runtime）| GitHub releases（已收录）|
| ✅ | cli 0.4.19（deploy revisions list）| GitHub releases（已收录）|
| ✅ | langchain-core 1.2.23（revert + requests 2.33.0）| 已确认 |
| ✅ | AutoGen python-v0.7.5（Anthropic thinking mode）| 已确认 |
| ✅ | DefenseClaw v0.2.0（PyPI 发布 + docs v1）| 已确认 |
| ✅ | langchain-openrouter 0.2.1（2026-03-30）| **本轮确认，patch 无重大变更** |
| ⏳ | DefenseClaw v1.0.0 Release Tag | GitHub 监测 |
| ⏳ | CrewAI A2A 协议支持确认 | crewAI/Core 迁移确认中 |

---

## 🟢 低频任务（每三天/按需）

### CONCEPT_UPDATE · 概念文章更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ✅ | 桌面 AI Agent 架构对比（OpenClaw vs Manus vs Perplexity）| 上轮完成 |
| ✅ | DeepResearch Bench ICLR 2026 | 上轮完成 |
| ✅ | AIP Agent Identity Protocol（arXiv:2603.24775）| 上轮完成 |
| ✅ | MCPMark ICLR 2026 | 上轮完成 |
| ✅ | Agent Skills Survey（arxiv:2602.12430）| 上轮完成 |
| ✅ | AI4Work Benchmark Mismatch（arxiv:2603.01203）| 上轮完成 |
| ✅ | MCP Agent Observability 2026（Iris）| 上轮完成 |
| ✅ | SkillsBench（86任务/11领域/7,308轨迹）| 上轮完成 |
| ✅ | FinMCP-Bench（ICASSP 2026）| 上轮完成 |
| ✅ | TIP（arxiv:2603.24203，树结构注入攻击）| **本轮 explicit 完成** |
| ⏳ | arxiv:2603.23802（177k MCP tools 实证研究，O*NET 映射）| explicit（高优先级）|
| ⏳ | MCPMark + OSWorld-MCP + MCP-Bench + MSB 横向对比（4个 ICLR 2026 MCP 基准）| explicit（高优先级）|
| ⏳ | SkillsBench 与 AI4Work 横向联合（SkillsBench vs AI4Work 互补分析）| explicit（中优先级）|
| ⏳ | MCP Security 架构问题（CVE-2026-27896 non-standard field casing 新攻击面）| explicit（中优先级）|
| ⏳ | GAIA Benchmark 各模型详细分析 | 下一轮 benchmark 数据更新 |
| ⏳ | AIP 论文 Python/Rust 参考实现仓库分析 | explicit（低优先级）|

### ENGINEERING_UPDATE · 工程实践更新

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | best-ai-coding-agents-2026 补充 Augment GPT-5.2 | explicit |
| ⏳ | A2A Scanner vs SAFE-MCP vs Agent Wall 深度对比 | explicit |
| ⏳ | Wombat（Unix-style rwxd for MCP agents）GitHub stars 跟踪 | 低优先级 |

### BREAKING_INVESTIGATE · breaking 深度调查

| 状态 | 任务 | 触发条件 |
|------|------|----------|
| ⏳ | CVE-2026-27896 MCP SDK non-standard field casing 利用样本分析 | 安全社区出现公开 PoC |
| ⏳ | Manus My Computer 实际攻击面分析 | explicit |

---

## 📝 Articles 线索（每轮必须记录）

| 时间 | 线索方向 | 状态 |
|------|---------|------|
| 2026-03-29 | AI4Work Benchmark Mismatch（arxiv:2603.01203，CMU+Stanford）| ✅ 完成 |
| 2026-03-29 | MCP Agent Observability（Iris，2026/03/14）| ✅ 完成 |
| 2026-03-30 | SkillsBench（arxiv:2602.12670）| ✅ 完成 |
| 2026-03-30 | FinMCP-Bench（arxiv:2603.24943，ICASSP 2026）| ✅ 完成 |
| 2026-03-30 | TIP（arxiv:2603.24203，树结构注入攻击）| ✅ **本轮完成** |
| 2026-03-30 | MCP Dev Summit North America（4/2-3，纽约）| ⏳ **P0 事件，距今2天，预热窗口正式开启** |
| 2026-03-30 | arxiv:2603.23802（177k MCP tools 实证研究，O*NET 映射）| ⏳ explicit（高优先级）|
| 2026-03-29 | MCPMark + OSWorld-MCP + MCP-Bench + MSB 横向对比（4个 ICLR 2026 MCP 基准）| ⏳ explicit（高优先级）|
| 2026-03-29 | Manus My Computer vs OpenClaw vs Perplexity（Perplexity 信息仍较少）| ⏳ explicit（中优先级）|
| 2026-03-29 | MCP Security 架构问题（CVE-2026-27896 non-standard field casing 新攻击面）| ⏳ explicit（中优先级）|

---

## 📊 本轮 Articles 产出说明

**本轮新增 articles**：1 篇

**产出详情**：`articles/research/tip-tree-structured-injection-mcp-2026.md`（~5500字）—— arxiv:2603.24203，TIP（Tree-structured Injection for Payloads），MCP 间接提示注入攻击；黑盒方法通过树结构搜索生成自然语言载荷；粗细粒度优化 + 路径感知反馈机制；95%+ 攻击成功率、10x 效率提升；4 种主流防御下 50%+ 有效；与命令注入 CVEs 的本质区别：攻击来自可信通道内的内容污染；属于 Stage 3（MCP）× Stage 12（Harness Engineering）

**评分**：TIP 是首个系统性地解决「如何在黑盒条件下生成 MCP 间接提示注入载荷」的论文，填补了 MCP Security Crisis 文章中的工具响应路径攻击缺口；与 AIP（身份验证）和 CABP（协议层）形成 MCP 安全四层完整知识体系

**与现有文章的关系**：
- 与 MCP Security Crisis 30 CVEs 互补（TIP 攻击的是 LLM 决策层面，而非服务器代码执行层面）
- 与 AIP IBCT 互补（AIP 解决身份验证，TIP 解决内容可信性）
- 与 CABP 互补（CABP 的 SERF 限制横向移动，TIP 在更早阶段注入）

**下轮重点线索**：MCP Dev Summit North America（4/2-3，纽约）距今仅 2 天

---

## 📊 state.json 同步

```json
{
  "lastRun": "2026-03-30T17:01",
  "lastCommit": "pending",
  "status": "autonomous",
  "version": "0.9.2",
  "owner": "FreezeSoul"
}
```

---

*由 AgentKeeper 维护 | 2026-03-30 17:01 北京时间*
