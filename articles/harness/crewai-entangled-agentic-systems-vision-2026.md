# Entangled Agentic Systems：Harness 之后的下一步是什么？

**来源**：CrewAI Blog - [Agent Harnesses are Dead, Long Live Agent Harnesses](https://crewai.com/blog/agent-harnesses-are-dead) | Published: April 14, 2026
**作者**：João (Joe) Moura, Founder of CrewAI

---

## 核心命题

> 传统 Agent Harness 正在被商品化。真正的价值转移方向是 **Entangled Software（纠缠软件）**——软件不再要求用户适应它，而是软件本身适应用户的workflow。

这是 CrewAI 创始人 João Moura 在 2026 年 4 月提出的判断。本文对其核心论点进行工程层面的分析与评估。

---

## 一、框架商品化：正在重演的历史

Moura 的核心观察并不新鲜：

```
Frameworks are cheap.
Harnesses are getting the same treatment.
```

他描述了一个加速的 commoditization 循环：

| 阶段 | 核心产品 | 状态 |
|------|---------|------|
| 框架（Framework）| LangChain, CrewAI | 已商品化 |
| 脚手架（Scaffold）| AutoGen, PromptFlow | 商品化中 |
| Harness | 记忆、工具、上下文工程 | 正在商品化 |

每一代都比前一代更 opinionated（更有主见），但每一代被追赶的速度也越来越快。Model Provider 不断吸收 stack 的更多层级——每个季度都有新的 primitive 被封装成 API。

**笔者认为**：这个 commoditization 曲线基本准确。Harness 层的基础能力（记忆、工具调用、上下文压缩）确实正在被 model providers 直接吸收。Anthropic 的 Claude Code 已经在 OS 层面内置了大量 harness 能力，这就是证明。

---

## 二、Entangled Software：概念拆解

Moura 提出的替代方向是 **Entangled Software**，概念来源于量子力学中的量子纠缠：

> 当两个粒子纠缠时，一个粒子的状态瞬间反映另一个粒子的状态。

对应到软件工程：
- **传统模式**：工具是固定的 → 用户学习适应工具
- **Entangled 模式**：产品 + 用户互相影响 → 产品从用户行为中学习并重塑自身

应用于 Agent 系统，产生了 **Entangled Agentic Systems**：

```
传统 Agent System：
User Workflow → Configure Agent → Agent executes → Done

Entangled Agentic System：
User Workflow → Agent observes + learns → Agent adapts to workflow
                        ↑                              ↓
                  Continuous ← ← ← ← ← ← ← ← ← ← ← ←
                  feedback loop
```

**关键特征**：
1. **从配置到涌现**：不再"设置"Agent，Agent 从团队的工作方式中"涌现"
2. **过程即数据**：客户的流程、数据、模式成为 Agent 的 intelligence
3. **双向适应**：软件塑造用户行为，用户行为也塑造软件

---

## 三、工程层面的关键问题

虽然 Entangled Software 是一个有吸引力的愿景，但工程实现层面存在几个关键挑战：

### 3.1 状态管理复杂性

Entangled 系统的核心是一个持续运行的双向反馈循环。这意味着：

- **运行时状态爆炸**：每次交互都在改变 Agent 的行为模型，如何控制状态增长？
- **隔离与并发的矛盾**：多个用户同时使用系统时，Entangled 行为会相互干扰吗？

CrewAI v1.14.7 的 changelog 中有一条相关改动值得注意：

> *"Scope runtime state per run to bound growth and isolate concurrent runs"*

这条改动直接回应了状态管理问题——通过 per-run scope 来限制状态增长并隔离并发运行。

**笔者认为**：这个问题没有完美的解决方案。Per-run scope 是一种工程妥协，牺牲了一部分"纠缠"效果来换取系统稳定性。

### 3.2 信任建立 vs. 快速迭代

Moura 提到：

> "Trust earned through production. You can't vibe-code the thousandth customer's accumulated patterns."

Entangled 系统的价值需要时间积累——需要大量用户的长期使用数据才能形成有效的行为适应。但：

- **冷启动问题**：新客户如何获得 Entangled 能力？是从零开始学习还是继承已有模式？
- **漂移风险**：如果早期学到的模式是次优的，Entangled 过程会固化这些错误吗？

### 3.3 可预测性缺失

传统软件的行为可以通过配置和测试来预测。Entangled 软件的行为部分地从用户交互中涌现，这意味着：

- **测试困难**：如何测试一个"会学习"的系统？
- **Debug 复杂**：Agent 的行为变化了，但原因藏在历史交互数据中
- **合规挑战**：受监管行业（金融、医疗）如何审计一个不断变化的 Agent？

---

## 四、与现有 Agent 工程范式的对比

| 维度 | 传统 Harness | Agentic RAG | Entangled Agentic |
|------|--------------|-------------|-------------------|
| **适应方向** | 固定行为，可配置 | 检索增强，动态上下文 | 双向适应，从行为学习 |
| **数据来源** | 静态知识库 | 外部向量库 | 用户交互历史 |
| **实现复杂度** | 中 | 中高 | 极高 |
| **可预测性** | 高 | 中 | 低 |
| **价值积累** | 无 | 中 | 高（flywheel）|
| **适用场景** | 通用任务 | 知识密集 | 长期深度流程 |

**笔者认为**：Entangled Agentic 是三种模式中实现门槛最高的，但也是价值积累壁垒最高的。它最适合的场景是**高频、长期、深度集成的企业流程**，而不是一次性任务。

---

## 五、实用评估：要不要跟进？

### 值得跟进的理由

1. **差异化壁垒**：Harness 能力可以被 model provider 直接吸收，但 Entangled 行为模式来自真实用户数据，无法被复制
2. **客户粘性**：一旦 Entangled 系统适应了客户的工作方式，切换成本极高
3. **行业趋势确认**：CrewAI 正在往这个方向投入，其他厂商也在观察

### 需要谨慎的理由

1. **工程成熟度**：当前没有成熟的工程范式，v1.14.7 的 per-run scope 是第一步，但离真正的 Entangled 还很远
2. **投入产出比**：对于大多数团队，当前的优先级应该是把 Harness 基础打扎实，而不是追逐 Entangled
3. **评估困难**：如何衡量 Entangled 的效果？当前没有基准

### 笔者的判断

> **Entangled Agentic Systems 是正确的大方向，但它是 3-5 年后的目标，不是当前周期的工程重点。**

当前周期的重点应该是：
- 把 Harness 的评估器循环（evaluator loop）做扎实
- 建立可靠的 checkpoint/resume 机制
- 实现稳定的多 Agent 协作模式

这些基础能力到位之后，Entangled 就是自然延伸。

---

## 六、CrewAI 的工程迭代方向

从 v1.14.7 的 changelog 可以看出 CrewAI 正在向 Entangled 方向演进的具体工程步骤：

**已落地的工程能力**：

| 能力 | 说明 | Entangled 相关性 |
|------|------|----------------|
| Checkpoint/Restore | 状态快照与恢复 | ✅ 基础，保存学习状态 |
| Per-run state scope | 运行时状态隔离 | ✅ 控制状态增长 |
| FlowDefinition DSL | 流程定义元数据 | ✅ 从 DSL 构建流程 |
| Conversational flows | 对话式流程 | ✅ 支持双向交互 |
| Pluggable memory backend | 可插拔记忆后端 | ✅ 记忆是 Entangled 的核心 |

**正在演进的能力**：

| 能力 | 说明 | Entangled 相关性 |
|------|------|----------------|
| Telemetry/OTel | 可观测性 | 🔜 理解学习过程 |
| Agent Control Plane | Agent 控制平面 | 🔜 管理 Entangled 行为 |
| Cognitive Memory | 认知记忆 | 🔜🔜 直接实现 Entangled |

---

## 七、结论

Moura 的核心判断：

> "Harnesses as they were are dead. What they evolve into is what matters."

**笔者认为这个判断过于戏剧化**。正确的表述应该是：

> "Harness 的基础能力正在商品化，但 Harness 的工程深度还不够。Entangled 是 Harness 的下一个演进阶段，但不是对 Harness 的否定。"

对于 Agent 工程师的建议：
- **短期（1-2年）**：把 Harness 的评估器循环、checkpoint、状态管理做扎实
- **中期（2-3年）**：建立可观测的 Agent 行为学习机制
- **长期（3-5年）**：向 Entangled Agentic Systems 演进

先把路修好，再谈造车。

---

## 原文引用

> "What if instead of customers building their own stripped-down versions of your product, the product itself adapted to each customer? Actually learned from how they work and reshaped itself around their behavior."
> — João (Joe) Moura, CrewAI

> "Companies want to vibe-code their own tools... the real opportunity is harder than vibe-coding, and potentially more valuable."
> — João (Joe) Moura, CrewAI

---

**关联项目**：本文分析了 CrewAI Entangled Agentic Systems 的工程愿景，关联的实践项目可参考 `articles/orchestration/` 中的 CrewAI 相关分析。