# Harmonic Scout V2：从「刚性 subgraph」到「Deep Agents + 共享文件系统」，4 倍留存不是设计目标而是结构副产品

> **核心反直觉**：大多数 production agent 团队把"留存"当作 prompt/tuning 问题，但 Harmonic 把它当作**架构问题**解决——当 Agent 不再被刚性 workflow 束缚，4x 留存、10x 会话时长、涌现式新用例，都只是「让模型自己思考」之后的**结构副产品**。这篇文章揭示的不是 tuning 技巧，而是**生产 Agent 架构的范式转移**。

## 核心洞察

**当你的 Agent 架构开始拒绝「为每种意图写一个 subgraph」时，4x 留存、10x 会话时长、「每天涌现新用例」就不是你设计出来的，而是结构必然**。Scout V1 已经是一个有能力的产品，但它有 100+ 个 evals 维护、每个新能力意味着新 subgraph、用户问"为什么这三家排在最上面"时模型根本看不到结果集——架构是瓶颈。Scout V2 用「一个 frontier model + 一个 Deep Agents harness + 两类工具」替代了 100 个 evals，**V1 的优化极限是 V2 的起点**。

更深的洞察是：把"4x 留存"和"4x 模型"分清楚。Harmonic 没换模型、没换团队规模、没增加运营投入——他们**取消了为每种意图写 workflow 的工程实践**。这是工程组织层面的胜利，不是 ML 层面的胜利。

## 来源

- 一手来源：[Harmonic Rebuilt Scout on Deep Agents and 4x'd Retention with LangSmith](https://www.langchain.com/blog/how-harmonic-rebuilt-scout-on-deep-agents-and-4xd-retention-with-langsmith) — Sofia Sulikowski, June 3, 2026, 8 min
- 相关：[How Rippling Went AI-Native Across Every Product in 6 Months with Deep Agents and LangSmith](https://www.langchain.com/blog/how-rippling-went-ai-native-across-every-product-in-6-months-with-deep-agents-and-langsmith) — Sofia Sulikowski, June 1, 2026, 6 min
- 相关：[How Lyft Built a Self-Serve AI Agent Platform for Customer Support with LangGraph and LangSmith](https://www.langchain.com/blog/lyft-built-a-self-serve-ai-agent-platform-for-customer-support-with-langgraph-and-langsmith) — Akshay Sharma, May 27, 2026, 10 min
- 评分：5/5（生产案例 + 数据可验证 + 工程深度高 + 范式突破）

---

## 1. Scout V1 的天花板：架构即瓶颈

Scout V1 是一个典型「V1 即巅峰」的故事：

- **架构**：composable subgraphs + LangSmith evals at every node（LangGraph-powered）
- **能力**：用户用自然语言查询，Scout 翻译为精确的 filter configurations
- **优势**：用户不再需要手动配置 filter（"show me AI companies in SF or NY..."）
- **天花板**：
  1. 任何 workflow 之外的意图 → 失败
  2. 维护 100+ evals 才能稳定
  3. 每个新能力 = 一个新 subgraph
  4. 用户问"why are those three at the top?" → **模型根本没看过结果集**（最致命）

V1 的设计者 Austin Berke 把 V1 的失败总结为「我们花了大量时间构建 rigid structures、writing evals、tediously iterating on every node」。这不是能力问题，是**架构选择**问题。

## 2. Scout V2 的反直觉决策：取消 workflow

V2 的设计哲学是 Austin 的原话：

> "Before, we spent a lot of time building rigid structures, writing evals, and tediously iterating on every node. **With this version, we said: let's use the best and smartest models, give it access to thoughtful tools that interface with our data, and see how Deep Agents does. And immediately we saw incredible improvements.**"

**V2 的架构只有 3 个组件**：

1. **一个 frontier model**（不微调、不 ensemble）
2. **一个 Deep Agents harness**（自带 long-horizon task execution + context window management）
3. **两类工具**：
   - 工具集 A：查询 Harmonic 的 global data layer（40M companies / 200M people / 230K investors）
   - 工具集 B：访问 firm-specific context（pipeline lists / CRM notes / 之前的 email 和 LinkedIn 关系）

**Deep Agents harness**（LangChain 的 Deep Agents 框架）负责 long-horizon task execution 和 context window management——这些 V1 需要手工搭 subgraph 才能完成的能力，V2 由 harness 内置。

## 3. 关键工程创新：共享文件系统（Shared Filesystem）

V2 最聪明的工程决策不是用 Deep Agents，而是**用共享文件系统连接模型和数据**：

> "The design where Scout fired a search, rendered results in a side panel, and moved on, breaks down the moment the user asks 'why are those three at the top?' **The model never saw the result set, so it can't answer.**"

V1 的问题不只是 subgraph 太刚性，更根本的是**模型与结果脱节**。当 Agent 把搜索结果推到 side panel、然后移向下一步时，结果集对模型不可见。V2 的解法是：

1. **Scout 把搜索结果写入共享文件系统**（agent 可按需读）
2. **模型通过 tool 接口分页浏览**用户正在看的同一份数据
3. **前端按行渲染**结果到达情况
4. **模型随时可以重新访问**任何一个 row 当 conversation 需要时

> "Using the shared filesystem design, Scout doesn't need a custom workflow for every use case. '**Not having to build a unique workflow experience for every individual use case or customers is a huge unlock,**' noted Austin."

**这个设计模式值得所有 Agent 团队学习**：把"数据和模型在同一个视图层"作为第一原则，而不是"模型调用工具返回数据"。

## 4. 产品哲学的转移：从「预设交互」到「观察涌现」

V1 的 PM 流程是：用户反馈 → feature requests → 优先级 → 权衡 → 排期。V2 完全颠覆了这个流程：

> "Before Scout, we'd build for how we expected users to interact with our product. We would get feature requests, prioritize them, and make tradeoffs. Now, **in this agentic model, we give users the ability to interact with the data how they want to and we observe how they use it. We discover emergent use cases every day.**"

**这是产品工程领域的范式转移**：
- V1：build → measure → learn（Lean Startup 循环）
- V2：observe emergent behavior → discover new use cases → expand TAM

Seth（产品负责人）的原话直接反驳了"Agent 是 LLM 玩具"的说法——Agent 让产品团队从"想象用户怎么用"解放出来，转向"观察用户怎么用"。

## 5. 数字说话：4x 留存、10x 会话时长、新 TAM

| 指标 | V1 | V2 | 倍数 |
|------|-----|-----|------|
| Week-1 to Week-4 留存 | 基准 | 4x | 4 倍 |
| 平均会话时长 | 基准 | 10x | 10 倍 |
| 投资人对 Scout 的描述 | "有用的工具" | **"必备工具"** | 范式跃迁 |
| 每日涌现的新用例 | 0 | "every day" | 不可计算 |

**这些数字不来自模型升级、不来自 prompt 调优、不来自数据飞轮——它们来自「取消 rigid subgraph」这一个架构决策**。这就是 V1 的优化极限是 V2 起点的原因。

更值得关注的是 **TAM 扩展**：Scout V2 之前是 VC 工具，现在扩展到：
- **Innovation & Corporate Development** 团队
- **Talent / Recruiters**
- **GTM** 团队（卖给 startup 的销售）
- 等所有"需要 know what's happening in private markets"的角色

**Agent 不只是改进了产品，它让产品从「投资人专用工具」变成「任何需要 startup 数据的角色」**。这是 TAM ×10 的乘数效应。

## 6. LangSmith Deployment 的角色：基础设施即产品

Harmonic 团队是 lean and product-focused——他们**不自己写 infra**。LangSmith Deployment 提供：

1. **Durable thread execution**（不丢失任何对话状态）
2. **Reliable deployments**（按需无限扩展）
3. **Observability**（每次工具调用、每次决策都可追踪）

Austin 的原话是 "set and forget"——基础设施层不再是他们的产品瓶颈。**LangSmith 解决了 Agent 产品在生产环境的「3 个 9」问题**（持久性、可扩展性、可观测性），让 lean team 可以专注在差异化能力上（global company+person data + firm-specific context）。

## 7. 反模式：为什么大多数团队做不到

Scout V2 的成功有几个**不可复制条件**：

| 条件 | Harmonic 有 | 多数团队 |
|------|------------|----------|
| Frontier model access | ✅（隐含 Claude Opus 4.x） | ⚠️ 受限 |
| Deep Agents 框架 | ✅（LangChain 的 Deep Agents） | ⚠️ 自己写 |
| 共享文件系统基础设施 | ✅（自建 + LangSmith） | ❌ 不知道这是关键模式 |
| Lean 团队 | ✅（产品聚焦） | ❌ 平台/infra 团队庞大 |
| 完整的 global data layer | ✅（40M companies / 200M people） | ⚠️ 数据稀疏 |

**对其他团队的可借鉴部分**：
1. **共享文件系统模式**——可以本地化实现（任何持久化层 + paged read tool）
2. **取消 rigid subgraph**——用 Deep Agents 风格的 harness（LangChain / LangGraph / OpenAI Agents SDK 都有等价物）
3. **观察涌现用例**——产品哲学而非技术决策
4. **LangSmith 风格的 deployment**——OSS 替代是 `alash3al/stash`（见配套 Project）

## 8. 三个副观点

### 副观点 1：4x 留存是「取消 workflow」的副产品，不是 tuning 目标

很多团队尝试用 prompt engineering、fine-tuning、RAG 优化追求留存提升。Harmonic 的故事是反例：**当架构允许模型自己思考，留存是涌现的**。调优在 V1 是必要工作，但在 V2 是优化错对象。

### 副观点 2：共享文件系统是 Agent 架构的「隐藏主线」

V1→V2 的本质修复是**让模型看到结果集**。这不只是「工具调用模式」，而是「Agent 与数据的物理拓扑」。所有 Agent 框架（LangGraph / OpenAI Agents SDK / CrewAI）的核心质量问题，往往是 Agent 看到数据 vs 不看到数据。

### 副观点 3：Lean 团队能赢，靠的是「让基础设施外包给 LangSmith」

"Set and forget" 是因为 LangSmith Deployment 把 durable execution / observability / scaling 都解决了。**生产 Agent 的下一个分水岭是「lean team + 强基础设施」**，而不是「大团队 + 自建 infra」。

---

## 与配套 Project 的闭环

- **Article**（本文）：Scout V2 → 揭示了「共享文件系统 + Deep Agents harness + LangSmith 部署」是 production agent 的当代最佳架构
- **Project**：[alash3al/stash](https://github.com/alash3al/stash) → 提供了**OSS 版的 LangSmith Deployment 记忆层**：9-stage consolidation pipeline，把"episodes → facts → relationships → patterns → wisdom"作为 Agent 的持久化记忆

**闭环**：LangSmith 是商业的「durable thread execution + observability」平台；`alash3al/stash` 是 OSS 的「持久化记忆 + 跨会话 context」MCP server。两者都解决同一个问题：**Agent 的记忆如何在多次会话、多个工具调用之间保持一致且可访问**。

| 维度 | LangSmith Deployment | alash3al/stash |
|------|---------------------|----------------|
| 定位 | 商业 platform（含 observability + scaling） | OSS MCP memory server |
| 核心抽象 | Durable thread + evals | 9-stage consolidation pipeline |
| 部署 | SaaS / Self-hosted | Self-hosted（Postgres + pgvector） |
| 集成 | LangChain/LangGraph deep | 任何 MCP-compatible 客户端 |
| 哲学 | "Set and forget" 全栈 | "Episodes → facts → wisdom" 单点 |
| 替代关系 | 商业版 | **OSS 等价（Pattern 8：商业 vs OSS）** |

## 一句话总结

**4x 留存不是 prompt 的胜利，是「取消 rigid subgraph + 共享文件系统 + lean 团队 + 强基础设施」这 4 个架构决策的复合涌现**。Agent 时代的产品哲学已经从「build for expected interactions」转向「observe emergent behaviors」。
