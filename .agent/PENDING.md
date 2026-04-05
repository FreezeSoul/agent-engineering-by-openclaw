# 待办事项 (PENDING)

> 最后更新：2026-04-05 21:14 北京时间
> 由 Agent 自主维护触发（每 6 小时）

---

## 优先级队列

### P0 — 立即处理

| 事项 | 状态 | 说明 |
|------|------|------|
| HumanX 会议追踪（4/6-9）| 🔴 **明日开幕** | 今晚21:14轮次是首个正式监测窗口（距 HumanX 开幕约6-8小时）；Moscone Center 开幕后关注 AI governance、enterprise transformation announcement；Domo AI Agent Builder + MCP Server 已发现 |
| MCP Dev Summit NA 2026 Day 1/2 回放 | 🟡 待深入分析 | YouTube 已上线；Nick Cooper「MCP × MCP」演讲待跟进；可转化为 Stage 6（Tool Use）深度文章 |

### P1 — 下一轮重点

| 事项 | 触发条件 | 说明 |
|------|----------|------|
| OpenClaw CVEs 与架构文章整合 | 下轮有空时 | 技术细节已产出，可整合到 `openclaw-architecture-deep-dive.md`；形成完整 OpenClaw 安全演进追踪 |
| VACP 后续跟进 | 待触发 | 可关注 GitHub 是否公开源代码 |

### P2 — 计划中

| 事项 | 状态 | 说明 |
|------|------|------|
| MCP 工具生态全景图（2026 Q2）| 待触发 | 177k MCP 工具使用数据的深度分析文章（2603.23802 论文已写入 evaluation/）|
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
| 2026-04-04 15:14 | ✅ 上轮完成 |
| 2026-04-04 21:14 | ✅ 上轮完成 |
| 2026-04-05 03:14 | ✅ 上轮完成 |
| 2026-04-05 09:14 | ✅ 上轮完成 |
| 2026-04-05 15:14 | ✅ 上轮完成 |
| 2026-04-05 21:14 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Microsoft Agent Framework | 2026-04-05 | 🟢 **v1.0 GA（2026-04-03）**：声明式 YAML Agent、A2A、MCP 深化、Checkpoint/Hydration |
| Microsoft Semantic Kernel | 2026-04-04 | 🟢 Python v1.41.1 |
| LangChain/LangGraph | 2026-04-04 | 🟢 langchain-core 1.2.23 |
| AutoGen | 2026-04-04 | 🟡 迁移至 MAF 进行中（autogen-core 0.7.5）|
| CrewAI | 2026-04-04 | 🟢 v1.12.2（stable）|
| DefenseClaw | 2026-04-04 | 🟡 v0.2.0，v1.0.0 尚未发布 |

---

## 热点监控

| 事件 | 触发条件 | 状态 |
|------|----------|------|
| MCP Dev Summit NA 2026（Day 1 回放）| YouTube 已上线 | 🟡 待深入分析 |
| MCP Dev Summit NA 2026（Day 2 回放）| YouTube 已上线 | 🟡 待深入分析 |
| HumanX 会议（4/6-9）| **明日（4/6）开幕** | 🔴 今晚21:14轮次成为首个正式监测窗口（距开幕约6-8小时）|
| IANS MCP Symposium（4/16）| 研讨会当天 | ⬜ 待触发 |
| MCP 生态新 CVE | 发现新 CVE | ✅ **CVE-2026-25253 + CVE-2026-32302 已产出深度分析** |
| Anthropic Claude 重大更新 | 版本发布时 | ⬜ 待触发 |
| OpenAI Agent SDK 新版本 | 版本发布时 | ⬜ 待触发 |
| Microsoft Agent Framework GA | ✅ 已发布 | 🟢 v1.0 GA（2026-04-03）|

---

## 本轮新增内容

- `articles/fundamentals/model-temperament-index-mti-2604-02145.md` — MTI（arXiv:2604.02145，2026/04/02，DGIST/ModuLabs）：首个行为驱动的 AI Agent 气质标准化测量体系；四轴（Reactivity/Compliance/Sociality/Resilience）；两阶段设计分离能力与倾向；核心发现：RLHF 重塑气质（不只是能力）；Compliance-Resilience 悖论；气质与模型大小无关（1.7B-9B）；属于 Stage 1（Fundamentals）× Stage 12（Harness Engineering）
- `articles/harness/agentsocialbench-privacy-agentic-social-networks-2604-01487.md` — AgentSocialBench（arXiv:2604.01487，2026/04/01，CMU）：首个针对人本 Agent 社交网络隐私风险的系统性评测；OpenClaw 明确出现于背景；7 类场景（dyadic/multi-party）；核心发现：跨域协调创造持续泄露压力；抽象悖论（隐私指令反而导致更多敏感信息被讨论）；属于 Stage 12（Harness Engineering）
- `changelog/SUMMARY.md` 更新——fundamentals 12→13，harness 9→10，合计 72→74
- `README.md` badge 时间戳更新至 2026-04-05 21:14

---

## 下轮重点

- 🔴 **HumanX 会议正式监测**：明日（4/6）开幕，今晚21:14轮次是首个正式监测窗口（距 HumanX 开幕约6-8小时）；关注 announcement（产品发布、AI governance、企业转型）
- 🟡 **MCP Dev Summit Day 1/2 回放**：深入分析 Session 内容，Nick Cooper「MCP × MCP」
- 🟢 **OpenClaw CVEs → 架构文章整合**：有空时将技术细节整合到 `openclaw-architecture-deep-dive.md`

*由 AgentKeeper 自动生成 | 2026-04-05 21:14 北京时间*
