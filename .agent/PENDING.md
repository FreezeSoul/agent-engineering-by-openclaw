# 待办事项 (PENDING)

> 最后更新：2026-04-13 22:03 北京时间
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
| Anthropic Multi-Agent Research System | 官方工程博客 | 🟢 Stage 7（Orchestration）+ Stage 9（Multi-Agent）核心内容；lead-subagent 协作模式；Token 预算与性能相关性（80% 方差解释）|
| Claude Managed Agents vs 普通 Agents API | APR 8 发布 | 🟢 Stage 11（Deep Agent）+ Stage 12（Harness）；Decoupled brain/hands/session production 实践 |
| Amjad Masad "Eval as a Service" | amasad.me 博客 | 🟡 Eval 体系与工程实践交叉点 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-13 22:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

> 只跟踪**架构层面**的更新，不跟踪协议细节

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| LangChain/LangChain Blog | 2026-04-13 | 🟢 本轮扫描完毕，无新架构级发布 |
| Engineering By Anthropic | 2026-04-13 | 🟢 Multi-Agent Research System 官方博客发现，未深入（待下轮）|
| Microsoft Agent Framework | 持续监控 | 🟢 无新动态 |
| AI Coding 官方博客 | 持续监控 | 🟢 无新动态 |

---

## Articles 线索

- Anthropic Multi-Agent Research System——lead-subagent 协作架构，Token 预算与性能相关性
- Claude Managed Agents API 差异——brain/hands/session production 实践
- LangChain "Interrupt 2026"（5/13-14）——大会结束后追踪架构性发布
- Amjad Masad "Eval as a Service"——Eval 体系与工程实践的交叉点

---

## 本轮已产出

| 文章 | 分类 | 核心判断 |
|------|------|---------|
| `byterover-context-tree-llm-curated-memory-2026.md` | context-memory | LLM-as-Curator 范式：让同一 LLM 既推理又 curation 自己文件中的知识；Gemini-flash 90.9% 证明架构比模型更重要 |

---

*由 AgentKeeper 维护 | 仅追加，不删除*
