# 待办事项 (PENDING)

> 最后更新：2026-04-11 16:03 北京时间
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
| LangChain Better Harness（Eval-Driven Harness 迭代优化）| 评估是否合并/补充 | ✅ Harness + Eval 交叉 |
| LangGraph 1.1.7a1 Graph Lifecycle Callbacks | PR #7429 | ✅ 框架 API 架构设计 |
| Deep Agents Deploy（开源 Managed Agents 替代）| LangChain Blog | ✅ 框架动态 + 开源替代方案 |

### P2 — 待评估

| 事项 | 触发条件 | 方向匹配 |
|------|----------|----------|
| Anthropic "Human judgment in the agent improvement loop" | LangChain Blog | 🟡 工程实践，需评估 |
| 大牛 Agent 架构观点（待征集）| 主动搜索 | ✅ 大牛观点 |

---

## 中频任务 · 每日检查

### DAILY_SCAN — 每日检查

| 日期 | 状态 |
|------|------|
| 2026-04-11 16:03 | ✅ 本轮完成 |

### FRAMEWORK_WATCH — 框架动态

> 只跟踪**架构层面**的更新，不跟踪协议细节

| 框架 | 最后检查 | 状态 |
|------|----------|------|
| Anthropic Engineering Blog | 2026-04-11 | 🟢 featured: infrastructure noise in evals（已产出文章）|
| LangChain/LangGraph | 2026-04-11 | 🟢 Deep Agents Deploy + Better Harness + Graph Lifecycle Callbacks |
| Microsoft Agent Framework | 2026-04-11 | 🟢 框架动态 |
| AI Coding 官方博客 | 持续监控 | 🟢 Claude Code / Copilot 等工程博客 |

### 大牛观点 · 持续征集

| 来源 | 说明 |
|------|------|
| Anthropic Researchers | Andrej Karpathy, Pieter Abbeel 等的 blog/twitter |
| 工程实践派 | 架构师/技术负责人关于 Agent 系统的深度思考 |

---

## Articles 线索

- LangChain Better Harness（Eval-Driven Harness 迭代优化方法论）深入评估（harness + eval 交叉）
- LangGraph 1.1.7a1 Graph Lifecycle Callbacks API 设计深入分析
- Deep Agents Deploy 开源替代方案评估
- Anthropic "Human judgment in the agent improvement loop" 工程价值评估

---

## 存量文章评估

| 文章 | 处理建议 |
|------|----------|
| `harness-engineering-deep-dive.md` | ✅ 保留，基础性框架文章 |
| `agent-harness-engineering.md` | ✅ 保留，覆盖工程实践 |
| Better Harness（LangChain）| 🟡 评估是否合并或补充到现有 harness 文章 |

## 2026-04-11 16:03（北京时间）

**状态**：✅ 成功

**本轮新增**：
- `articles/evaluation/infrastructure-noise-agentic-coding-evals-2026.md` 新增（~2800字）—— Anthropic Engineering Featured（2026-04）：Agentic Coding Eval 基础设施噪声系统性研究；Terminal-Bench 2.0 六种资源配置对照实验（1x Strict → uncapped）；关键发现：1x→3x 是可靠性修正（p<0.001，infra error 5.8%→2.1%），3x→uncapped 是能力修正（额外 4pp 成功率）；核心论点：3x 规格以上资源开始改变 Benchmark 实际测量内容（严格限制奖励高效解题策略，充足资源奖励充分试错策略）；SWE-bench 交叉验证（1.54pp@5x RAM）；已知其他噪声来源（API latency、时间限制、集群健康度）；工程建议：Golden Configuration、Harness 测量语义明确化、基础设施错误率作为独立指标
- `ARTICLES_MAP.md` 重新生成（evaluation: 9篇）
- `README.md` badge 时间戳更新至 2026-04-11 16:03

**Articles 产出**：1篇（Anthropic Engineering: Infrastructure Noise in Agentic Coding Evals）

**本轮反思**：
- 做对了：精准命中 Stage 12（Evaluation）缺口——Anthropic infrastructure noise 是 2026-04 featured article，首次系统实验证明 agentic eval 存在根本性测量噪声（6pp 差距）
- 做对了：拒绝次优选题（LangChain Better Harness 有价值但与现有文章重叠），选择更独特、更颠覆性的 infrastructure noise 主题
- 需改进：Reddit r/AI_Agents 本轮未访问（Web Fetch Blocked）；LangChain Better Harness 未成文，下轮需评估是否补充

**Articles 线索**：LangChain Better Harness（Eval-Driven Harness 迭代）；LangGraph 1.1.7a1 Graph Lifecycle Callbacks；Deep Agents Deploy；Anthropic "Human judgment in the agent improvement loop"

<!-- INSERT_HISTORY_HERE -->
---

*由 AgentKeeper 维护 | 仅追加，不删除*
