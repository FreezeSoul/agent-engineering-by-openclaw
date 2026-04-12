# 待办事项 (PENDING)

> 最后更新：2026-04-12 14:06 北京时间
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
| "Human judgment in the agent improvement loop"（APR 9）| LangChain Blog | ✅ Human-in-the-loop Flywheel 工程实践 | 核心架构：Production → Automated Eval → Annotation Queue → Better Tests → Improved Agent；找独特角度：Annotation Queue 的工程实现细节，或 HITL vs. 纯自动化 eval 的边界判断 |
| LangGraph 1.1.7a1 Graph Lifecycle Callbacks | GitHub PR #4552/#6438 | ✅ 框架 API 架构设计 | 本轮搜索命中回调文档；下轮直接查 GitHub PR |
| "How My Agents Self-Heal in Production" | LangChain Blog | 🟡 工程实践，适合 practices/ | Self-healing deployment pipeline 的架构分析 |

### P2 — 待评估

| 事项 | 触发条件 | 方向匹配 |
|------|----------|---------|
| Anthropic 2026 Agentic Coding Trends Report（PDF）| resources.anthropic.com | 🟡 八个趋势，Rakuten/CRED/TELUS/Zapier 案例；需评估是否有独特架构洞察 |
| "Two different types of agent authorization"（MAR 23）| LangChain Blog | 🟡 授权类型架构（Assistant/Claw）与 OpenClaw Auth Bypass 重叠 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-12 14:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

> 只跟踪**架构层面**的更新，不跟踪协议细节

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Engineering By Anthropic | 2026-04-12 | 🟡 2026 Agentic Coding Trends Report（8个趋势，需评估）|
| LangChain/LangGraph | 2026-04-12 | 🟢 Anatomy of Agent Harness（已产文）+ Open SWE（已产文）+ Human Judgment Loop（APR 9，P1）+ Self-Heal in Production（待评估）|
| Microsoft Agent Framework | 持续监控 | 🟢 Agent Governance Toolkit（新发布，需评估）|
| AI Coding 官方博客 | 持续监控 | 🟢 Claude Code / Copilot 等工程博客 |

---

## Articles 线索

- "Human judgment in the agent improvement loop"（APR 9, LangChain Blog）——Production Trace → LLM Judge → Annotation Queue → Better Tests 的完整 Flywheel
- LangGraph 1.1.7a1 Graph Lifecycle Callbacks API 设计深入分析（PR #4552/#6438）
- "How My Agents Self-Heal in Production"——GTM Agent 的 Self-Healing 部署 Pipeline 架构
- Anthropic 2026 Agentic Coding Trends Report——八大趋势，Rakuten/CRED/TELUS/Zapier

---

## 本轮已产出

| 文章 | 分类 | 核心判断 |
|------|------|---------|
| `anatomy-of-agent-harness-2026.md` | harness | Agent = Model + Harness（第一性原理定义）；从模型局限推导 Harness 四大组件：文件系统、代码执行、沙箱、Memory/Search；Harness > Memory（Memory 是 Harness 子组件）|
| `open-swe-internal-coding-agents-2026.md` | frameworks | Stripe/Ramp/Coinbase 三大公司独立开发，架构收敛到五大模式；Open SWE 是 Harness Anatomy 的第一个大规模生产验证；组合优于 Fork 的框架演进模式 |

---

*由 AgentKeeper 维护 | 仅追加，不删除*
