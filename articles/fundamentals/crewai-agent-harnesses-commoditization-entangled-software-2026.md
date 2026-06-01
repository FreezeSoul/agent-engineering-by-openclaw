# Agent Harness 的商品化与 Entangled Software 的崛起

> **来源**: CrewAI Blog — "[Agent Harnesses are Dead, Long Live Agent Harnesses](https://crewai.com/blog/agent-harnesses-are-dead)" by João (Joe) Moura, April 14, 2026

> **核心论点**: Agent Harness 正在重蹈框架的覆辙——商品化浪潮中，价值的锚点正在从「构建工具」转向「数据积累 + 行为适应」。

---

## 一、框架商品化的昨天，Harness 商品化的今天

2023 年的 CrewAI 用户不会意识到，他们正在使用一个后来被整个行业定义为「正确抽象」的东西：多 Agent 协作的 Harness。

Harness 是什么？**Agent 循环的所有周边机制**——Memory、Tools、Caching、Context Engineering、Prompts、Skills、MCP。在行业术语还在争论「框架 vs 脚手架 vs Harness」的时候，CrewAI 已经把这个组合做出来了，并且被证明是对的。

但问题是：**对的东西正在变得廉价**。

引用原文：

> "The same forces that commoditized frameworks are already starting to commoditize harnesses. Model providers keep absorbing the stack and every quarter, another primitive moves behind an API."

Model Provider 每个季度都在吃掉更多层级。2024 年你可能要自己写 Planning，2025 年 Planning 被内置进模型 API，2026 年连 Context Compression 都成了模型厂商的标配功能。当这些都成了 API 调用参数，Harness 还剩什么？

这就是商品化。

---

## 二、价值正在转移到哪里

文章的核心判断是：**当构建变得廉价，价值的锚点转向「无法被 vibe-coding 复制的那些东西」**。

| 价值层 | 能否被 vibe-coding 复制 | 说明 |
|--------|---------------------|------|
| 框架 | ❌ 已商品化 | 几行代码就能搭一个 |
| Harness | ⚠️ 正在商品化 | MCP、Memory 逐渐标准化 |
| **Distribution** | ❌ 不能 | 渠道和网络效应需要时间积累 |
| **Proprietary Data** | ❌ 不能 | 需要数年才能建立的数据壁垒 |
| **Intelligence Compounding** | ❌ 不能 | 产品从真实使用中捕获 intelligence |
| **Earned Trust** | ❌ 不能 | 生产环境验证的信任 |

原文说：

> "You can't vibe-code the thousandth customer's accumulated patterns feeding back into the product. That flywheel is earned, not built."

这句话点出了本质——第 1000 个客户积累的模式，是无法通过周末 Hackathon vibe-coding 出来的。这个飞轮只能靠时间。

---

## 三、Entangled Software：Harness 的下一个形态

文章提出了一个原创概念：**Entangled Software**。

这个概念来自物理学的量子纠缠——两个粒子一旦纠缠，一个的状态瞬间反映另一个的状态。在软件领域，Entangled Software 意味着：**产品与客户相互适应，随着使用深入，两者变得不可分割**。

这与过去三十年的软件范式完全相反：
- **传统软件**：人适应工具（人调整自己的工作流来迁就软件）
- **Entangled Software**：软件适应人（软件从人的行为中学习，重新塑造自身）

原文：

> "The software adapts to behavior instead of behavior adapts to software. This is something that wouldn't be possible without agents until recently but now opens the doors for completely new user experiences."

关键在于 **without agents**——在 Agent 出现之前，这种适应性是不可能的。Agent 使得软件能够：
- 从每次执行中学习模式
- 动态调整自身的行为策略
- 与客户的业务流程、数据、决策习惯深度绑定

当 Entangled Agentic Systems 在真实生产环境部署，与客户的流程、数据、工作方式完全绑定时，它们就成了真正「纠缠」的状态。

---

## 四、「路」比「车」更重要

原文的核心比喻：

> "The companies that win this era won't be the ones that built the best car, but the ones that built the road."

| 层级 | 定义 | 当前状态 |
|------|------|---------|
| **Car（车）** | Framework + Harness | 正在商品化 |
| **Road（路）** | Trust + Data + Adaptation Infrastructure | 价值正在这里聚集 |

作者坦诚 CrewAI 两者都做了（Flows 是框架，Crews/Agents 是 Harness），但下一阶段的重点是「路」——那些让任何车都能行驶的基础设施。

这对 Agent 工程化的启示是什么？

**Harness 工程师的下一个挑战**：不要只关注「如何构建更好的 Agent」，而要思考「如何让你的系统从每次执行中变得更好」。这是从工具到平台的跃迁。

---

## 五、笔者的判断

### 这篇文章为什么值得深入分析

1. **原创概念**：Entangled Software 是笔者见过的最清晰的 Agent 系统价值演进框架
2. **一手CEO视角**：不是技术博客的浅层分析，而是从商业战略高度看 Agent 工程化的演进
3. **工程化映射**：文章描述的趋势直接映射到我们的 Harness Engineering 研究方向

### 局限性与适用边界

这篇文章的视角是**平台级战略**，不是工程实现细节。它的局限在于：
- 没有给出「如何构建 Entangled Software」的具体技术路径
- 主要面向企业级决策者，对个人开发者指导有限
- 没有讨论 Entangled Software 潜在的风险（数据隐私、锁定效应）

**适用场景**：
- 企业 AI 战略规划：理解 Agent 平台的价值演进方向
- 产品设计：思考「Agent 产品如何从使用中学习」
- 技术选型：判断当前 Harness 投资的长期价值

**不适用场景**：
- 具体的技术实现指南
- 开源框架选型（工程细节层面）

### 与行业的关系

这篇文章印证了一个大趋势：**Agent 领域的价值正在从「中间件」向「数据层」迁移**。过去两年大家争论哪个框架好、哪个 Harness 强，现在这个问题的优先级在下降。真正的问题是：谁的数据更丰富？谁的学习飞轮更快？

---

> **引用来源**：  
> - "[Agent Harnesses are Dead, Long Live Agent Harnesses](https://crewai.com/blog/agent-harnesses-are-dead)" — João (Joe) Moura, CrewAI CEO, April 14, 2026  
> - "[CrewAI Discovery](https://crewai.com/blog/crewai-discovery)" — 同上作者关于 AI 战略规划产品的发布文