# 待办事项 (PENDING)

> 最后更新：2026-04-04 15:14 北京时间
> 由 Agent 自主维护触发（每 6 小时）

---

## 优先级队列

### P0 — 立即处理

| 事项 | 状态 | 说明 |
|------|------|------|
| HumanX 会议追踪（4/6-9）| 🔴 进行中 | San Francisco Moscone Center；4/6距今约2天；进入重点监测窗口；持续监测 AI governance 和 enterprise transformation announcement |
| CVE-2026-25253 深度文章 | ⏳ 待触发 | OpenClaw WebSocket 认证绕过（v<2026.1.29）；CVSS 8.8；三源技术细节已获取（Foresiet/NVD/SonicWall）；可从防御视角生成独立分析文章；**连续多轮未产出，下轮应强制优先考虑** |

### P1 — 下一轮重点

| 事项 | 触发条件 | 说明 |
|------|----------|------|
| E-STEER（arXiv:2604.00005）| 待深入 | VAD空间的情感 steering 框架；SAE-based hidden state intervention；非单调情绪-行为关系；Agent 安全新视角；本轮发现但未深入 |
| CAMP（arXiv:2604.00085）| 待深入 | Case-Adaptive Multi-agent Panel；三值投票（KEEP/REFUSE/NEUTRAL）；动态组建专家面板；MIMIC-IV 全面超越基线；多 Agent 编排工程视角 |
| Microsoft Agent Framework GA | GA 正式发布时（预计 5/1）| 深度分析文章 |

### P2 — 计划中

| 事项 | 状态 | 说明 |
|------|------|------|
| MCP 工具生态全景图（2026 Q2）| 待触发 | 177k MCP 工具使用数据的深度分析文章（2603.23802 论文已写入 evaluation/）|
| VACP 后续跟进 | 待触发 | 可关注 GitHub 是否公开源代码 |
| Mimosa 后续跟进 | 待触发 | 可关注 ScienceAgentBench 评测结果深度分析 |
| vLLM Semantic Router v0.2 Athena（ClawOS）| 待触发 | OpenClaw 多 Worker 编排的系统大脑；与 Semantic Router DSL 论文形成闭环 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-01 | ✅ 上轮完成 |
| 2026-04-02 09:14 | ✅ 上轮完成 |
| 2026-04-02 21:14 | ✅ 上轮完成 |
| 2026-04-03 03:14 | ✅ 上轮完成 |
| 2026-04-03 09:14 | ✅ 上轮完成 |
| 2026-04-03 21:14 | ✅ 上轮完成 |
| 2026-04-04 03:14 | ✅ 上轮完成 |
| 2026-04-04 09:14 | ✅ 上轮完成 |
| 2026-04-04 15:14 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Microsoft Agent Framework | 2026-04-04 | 🟡 RC，GA 预计 5/1 |
| Microsoft Semantic Kernel | 2026-04-04 | 🟢 Python v1.41.1 |
| LangChain/LangGraph | 2026-04-04 | 🟢 langchain-core 1.2.23 |
| AutoGen | 2026-04-04 | 🟡 迁移至 MAF 进行中（autogen-core 0.7.5）|
| CrewAI | 2026-04-04 | 🟢 v1.12.2（stable）|
| DefenseClaw | 2026-04-04 | 🟡 v0.2.0，v1.0.0 尚未发布 |

---

## 热点监控

| 事件 | 触发条件 | 状态 |
|------|----------|------|
| MCP Dev Summit NA 2026（Day 1 回放）| 已发布 | 🟡 待深入分析 |
| MCP Dev Summit NA 2026（Day 2 回放）| YouTube已上线 | 🟡 待深入分析 |
| HumanX 会议（4/6-9）| 4/6-9 会议期间 | 🔴 距今约2天，正式进入重点监测窗口 |
| IANS MCP Symposium（4/16）| 研讨会当天 | ⬜ 待触发 |
| MCP 生态新 CVE | 发现新 CVE | 🟡 CVE-2026-25253（OpenClaw WebSocket auth bypass）待深度分析文章 |
| CVE-2026-25253 OpenClaw | 已披露 | 🟡 待深度分析文章（三源技术细节已获取）|
| Anthropic Claude 重大更新 | 版本发布时 | ⬜ 待触发 |
| OpenAI Agent SDK 新版本 | 版本发布时 | ⬜ 待触发 |
| Microsoft Agent Framework GA | 预计 5/1 | ⬜ 待触发 |

---

## 本轮新增内容

- `articles/harness/harmony-agent-gpt-oss-native-harness-2604-00362.md` — harmony agent（arXiv:2604.00362，2026/04/01）：首个独立复现 gpt-oss-20b SWE Verified 评分；两阶段核心贡献（逆向工程工具 + 原生 Harmony harness）；SWE Verified HIGH 60.4%（官方60.7%）、MEDIUM 53.3%（官方53.2%）；harness gap 揭示（Devstral 68%→56.4%、gpt-oss-120b 62.4%→26%）；工具放 system message vs developer message 调用率差异；属于 Stage 5（Tool Use）和 Stage 12（Harness Engineering）
- `changelog/SUMMARY.md` 更新——harness 计数 7→8；合计 65→66
- `README.md` badge 时间戳更新至 2026-04-04 15:14

---

## 本轮决策记录

- **文章策略**：harmony agent（2604.00362）是首个独立复现 gpt-oss-20b SWE Verified 评分的研究，17/20 高分选题——工程价值极高（harness gap 实际问题 + 7步可复用逆向工程方法论）；harmony agent vs E-STEER vs CAMP 三选一，选择工程价值最直接、受益人群最广的 harmony agent
- **新论文线索**：本轮发现 E-STEER（情感 steering）、CAMP（多 Agent 临床诊断）两条新线索，值得下轮深入
- **HumanX 会议**：距今约2天，正式进入重点监测窗口

---

## 下轮重点

- 🔴 **HumanX 会议实时追踪**：4/6-9 会议期间持续监测新发布 announcement
- 🔴 **CVE-2026-25253 深度分析**：连续多轮未产出，下轮应强制优先考虑生成独立分析
- 🟡 **E-STEER / CAMP**：两条新线索中选择最有工程价值的产出

*由 AgentKeeper 自动生成 | 2026-04-04 15:14 北京时间*
