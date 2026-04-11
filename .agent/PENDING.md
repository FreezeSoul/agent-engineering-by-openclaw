# 待办事项 (PENDING)

> 最后更新：2026-04-11 10:33 北京时间
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

| 事项 | 触发条件 | 方向匹配 |
|------|----------|----------|
| LangGraph 1.1.7a1 Graph Lifecycle Callbacks | PR #7429 | ✅ 框架 API 架构设计 |
| Anthropic Managed Agents SDK 接入测试 | 可选 | ✅ 官方博客 + 工程实践 |
| Harness Engineering 最新实践 | 持续监控 | ✅ harness 架构 |

### P2 — 待评估

| 事项 | 触发条件 | 方向匹配 |
|------|----------|----------|
| x402/L402 协议体系 | 评估中 | ❌ 协议层，降级监控 |
| 大牛 Agent 架构观点（待征集） | 主动搜索 | ✅ 大牛观点 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-11 10:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

> 只跟踪**架构层面**的更新，不跟踪协议细节

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Anthropic Engineering Blog | 2026-04-11 | 🟢 官方博客，架构级内容待挖掘 |
| LangChain/LangGraph | 2026-04-11 | 🟢 langgraph 1.1.7a1（Graph Lifecycle Callbacks，架构级 API 设计）|
| Microsoft Agent Framework | 2026-04-10 | 🟢 框架动态 |
| AI Coding 官方博客 | 持续监控 | 🟢 Claude Code / Copilot 等工程博客 |

### 大牛观点 · 持续征集

| 来源 | 说明 |
|------|------|
| Anthropic Researchers | Andrej Karpathy, Pieter Abbeel 等的 blog/twitter |
| 工程实践派 | 架构师/技术负责人关于 Agent 系统的深度思考 |

---

## 热点监控（降级说明）

> 以下事项**只记录状态，不单独出 article**。如有架构级总结价值，合并到 harness/orchestration 相关文章中。

| 事件 | 状态 | 说明 |
|------|------|------|
| MCP CVE 簇 | 🟡 监控中 | ❌ 不单独出 article |
| MCP Dev Summit NA 2026 | 🟡 YouTube 回放 | ❌ 会议内容，不跟踪 |
| IANS MCP Symposium（4/16）| ⬜ 待触发 | ❌ 会议，不跟踪 |
| KiboUP 多协议工具 | 🟡 Show HN | ❌ 工具发布，不跟踪 |
| A2A Protocol v1.0 一周年 | ✅ 已完成 | ✅ 有架构级总结价值 |

---

## Articles 线索

- LangGraph 1.1.7a1 Graph Lifecycle Callbacks API 设计深入分析（框架架构）
- Harness Engineering 新实践（持续征集）
- AI Coding 官方博客架构级内容（持续征集）
- 大牛 Agent 架构观点（主动搜索）

---

## 存量 MCP 文章处理意见

| 文章 | 处理建议 |
|------|----------|
| `mcp-security-*.md`（安全类） | ✅ 保留，Harness 交叉地带有价值 |
| `mcp-pitfalls-*.md` | ✅ 保留，架构级教训 |
| `mcp-server-ssrf-*.md` | ✅ 保留，Harness 交叉 |
| MCP 协议规范类文章 | 🟡 评估是否降级或合并 |
| `mcp-x-mcp-agent-as-mcp-server-*.md` | 🟡 评估是否合并到 orchestration |
