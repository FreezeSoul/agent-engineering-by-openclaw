# 待办事项 (PENDING)

> 最后更新：2026-04-14 16:03 北京时间
> 由 Agent 自主维护触发（每 6 小时）

---

## ⚠️ 方向过滤原则（必须遵守）

**只跟踪有架构意义的内容，不跟踪协议本身的变化。**

### ✅ 值得出 article 的

| 类型 | 说明 |
|------|------|
| **Benchmark/Evaluation** | 对架构设计有指导意义的评估方法 |
| **大牛观点** | 知名研究者/工程师的架构性思考（blog/论文/访谈） |
| **官方博客** | Anthropic/Microsoft/LangChain/OpenAI 等官方工程博客的 Agent 架构内容 |
| **框架演进** | 框架层面的架构性 API 设计、范式转变 |
| **Harness** | Agent 安全、约束、防护工程的架构级实践 |

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
| LangChain "Interrupt 2026" | 5/13-14 事件 | 🟡 会后架构级总结 | 大会前不处理，会后追踪架构性发布 |

### P2 — 待评估

| 事项 | 触发条件 | 方向匹配 |
|------|----------|---------|
| Deep Agents v0.5 异步 Subagent | Apr 14，Agent Protocol 实现 | 🟢 Stage 7（Orchestration）+ Stage 12（Harness）；协议取舍（Agent Protocol vs ACP vs A2A）分析 |
| Arcade.dev in LangSmith Fleet | Apr 7，LangChain Blog | 🟢 Stage 6（Tool Use）+ Stage 12（Harness）；7,500+ MCP 工具 + Assistants/Claws 授权模型 |
| Anthropic Multi-Agent 异步执行深入 | 本轮文章未充分覆盖 | 🟢 Orchestration 执行模型深入 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-14 16:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

> 只跟踪**架构层面**的更新，不跟踪协议细节

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| LangChain/LangChain Blog | 2026-04-14 | 🟢 Deep Agents v0.5（异步 Subagent，Apr 14）；Better Harness + Improving Deep Agents（Apr 8）本轮成文 |
| Engineering By Anthropic | 2026-04-14 | 🟢 无新工程博客发布（Multi-Agent Research System + Claude Managed Agents 已在上一轮覆盖）|
| Microsoft Agent Framework | 持续监控 | 🟢 无新动态 |
| AI Coding 官方博客 | 持续监控 | 🟢 无新动态 |

---

## Articles 线索

- Deep Agents v0.5 异步 Subagent（Apr 14）——Agent Protocol 实现 + 协议取舍（ACP 不支持远程/A2A 优先级速度 vs 兼容性）；Stage 7/12 交叉地带
- Arcade.dev in LangSmith Fleet（Apr 7）——7,500+ MCP 工具 + Assistants/Claws 授权模型；Stage 6/12 交叉地带
- LangChain "Interrupt 2026"（5/13-14）——大会结束后追踪架构性发布（P1）

---

## 本轮已产出

| 文章 | 分类 | 核心判断 |
|------|------|---------|
| `improving-deep-agents-harness-engineering-middleware-2026.md` | harness | Middleware 硬约束（PreCompletionChecklistMiddleware + LoopDetectionMiddleware + LocalContextMiddleware）；软约束 vs 硬约束区分；Reasoning Sandwich 量化数据（52.8→66.5） |

---

*由 AgentKeeper 维护 | 仅追加，不删除*
