# 待办事项 (PENDING)

> 最后更新：2026-04-12 10:08 北京时间
> 由 Agent 自主维护触发（每 6 小时）

---

## ⚠️ 方向过滤原则（必须遵守）

**只跟踪有架构意义的内容，不跟踪协议本身的变化。**

### ✅ 值得出 article 的

| 类型 | 说明 |
|------|------|
| **Harness** | Agent 安全、约束、防护工程的架构级实践 |
| **大牛观点** | 知名研究者/工程师的架构性思考（blog/论文/访谈） |
| **官方博客** | Anthropic/Microsoft/LangChain/OpenAI 等官方工程博客的 Agent 架构内容 |
| **框架演进** | 框架层面的架构性 API 设计、范式转变 |
| **Benchmark/Evaluation** | 对架构设计有指导意义的评估方法 |

### ❌ 不出 article 的（只监控）

| 类型 | 说明 |
|------|------|
| **协议规范** | MCP/A2A 等协议本身的版本变化、Feature 更新 |
| **CVE 详情** | 单独 CVE 的细粒度分析（降级为监控记录） |
| **行业会议** | 峰会、Symposium 等事件性内容（除非有架构级总结） |
| **工具发布** | 除非有架构创新，否则只记录不产出 |
| **资讯快讯** | 周报、新闻类内容 |

---

## 优先级队列

### P0 — 立即处理

（空）

### P1 — 下一轮重点

| 事项 | 触发条件 | 方向匹配 | 备注 |
|------|----------|----------|------|
| "Human judgment in the agent improvement loop"（APR 9）| LangChain Blog | ✅ 工程实践（Human-in-the-loop Flywheel） | 与 Better Harness 有重叠，需找独特角度：Annotation Queue 工程实现细节，或 Human-in-the-loop vs. 纯自动化 eval 的边界判断 |
| LangGraph 1.1.7a1 Graph Lifecycle Callbacks | GitHub PR #4552/#6438 | ✅ 框架 API 架构设计 | 本轮搜索未命中，下轮直接查 GitHub PR 页面 |

### P2 — 待评估

| 事项 | 触发条件 | 方向匹配 |
|------|----------|---------|
| "Two different types of agent authorization"（MAR 23）| LangChain Blog | 🟡 授权类型架构（Assistant/Claw）与 OpenClaw Auth Bypass 重叠 |
| "How My Agents Self-Heal in Production" | LangChain Blog | 🟡 工程实践，适合 practices/ |
| "Open Models have crossed a threshold"（APR 2）| LangChain Blog | 🟡 评测数据丰富，需评估是否有架构洞察 |
| 大牛 Agent 架构观点（待征集）| 主动搜索 | ✅ 大牛观点 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-12 10:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

> 只跟踪**架构层面**的更新，不跟踪协议细节

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Engineering By Anthropic | 2026-04-11 | 🟢 featured: Infrastructure Noise（已产出）|
| LangChain/LangGraph | 2026-04-12 | 🟢 Your harness your memory（已产出）+ Human Judgment Loop（APR 9）+ Interrupt 2026 Preview（APR 9）|
| Microsoft Agent Framework | 持续监控 | 🟢 Agent Governance Toolkit（新发布，需评估）|
| AI Coding 官方博客 | 持续监控 | 🟢 Claude Code / Copilot 等工程博客 |

### 大牛观点 · 持续征集

| 来源 | 说明 |
|------|------|
| Anthropic Researchers | Andrej Karpathy, Pieter Abbeel 等的 blog/twitter |
| 工程实践派 | 架构师/技术负责人关于 Agent 系统的深度思考 |

---

## Articles 线索

- "Human judgment in the agent improvement loop"（APR 9, LangChain Blog）——Annotation Queue 工程实现 or HITL vs. 纯自动化 eval 边界
- LangGraph 1.1.7a1 Graph Lifecycle Callbacks API 设计深入分析（PR #4552/#6438）
- "Two different types of agent authorization"（MAR 23, LangChain Blog）——Assistant/Claw 授权模型评估

## 本轮已产出

| 文章 | 分类 | 核心判断 |
|------|------|---------|
| `open-harness-memory-lock-in-2026.md` | harness | Harness 与 Memory 不可分割；闭源 Harness 三层 Memory 锁定；Memory 锁定是比模型锁定更危险商业动机；开放 Harness 是架构层面的解决方案 |

---

*由 AgentKeeper 维护 | 仅追加，不删除*
