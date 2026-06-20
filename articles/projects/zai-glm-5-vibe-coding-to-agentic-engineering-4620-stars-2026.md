# GLM-5：从 Vibe Coding 到 Agentic Engineering

> 来源：https://github.com/zai-org/GLM-5 | Stars: 4,620 | License: Apache-2.0
> 关联 Article：本文与 AddyOsmani《长程 Agent 的三层工程架构》形成闭环——Article 描述长程执行所需的 Harness 工程能力，GLM-5 代表模型层如何在架构层面支持这些能力
> 标签：#foundation-model #长程Agent #ARC能力 #异步RL #DSA注意力

---

## 核心命题

GLM-5 的核心主张是：模型层面的能力演进（长程推理、Agent 自主决策、复杂任务完成）是让 Agent 从「能跑 demo」到「能跑生产」的前提条件之一——而这个能力是可以被训练出来的，不是靠 Scale 换来的附属品。

**一句话亮点**：第一个在 Artificial Analysis Intelligence Index v4.0 突破 50 分的开源模型，在 Vending-Bench 2（年度级模拟经营任务）上排名第 1 开源模型，终局账户余额 $4,432，逼近 Claude Opus 4.5。

---

## 为什么这个项目值得推荐

### 1. 「Vibe Coding → Agentic Engineering」的框架价值

GLM-5 论文标题本身就是最好的知识贡献。「Vibe Coding」是 2025 年的主流范式：给模型一个指令，模型生成代码，人来 review。「Agentic Engineering」是 2026 年的目标：模型在真实软件工程任务里自主规划、执行、验证、迭代。

这个范式转变的核心难点不在于「模型能生成代码」，而在于：

- 模型能自主做多步规划（Planner 角色）
- 模型能在长程执行中保持上下文连贯性（对应 AddyOsmani 提到的三个壁垒）
- 模型能自我验证，不在完成度 30% 的时候自信退出（Judge 角色）

**笔者认为**：这个框架价值比 GLM-5 本身的 benchmark 分数更有持久性——它给行业提供了一套描述范式转变的词汇体系。

### 2. 异步 RL 基础设施：工程化层面的创新

GLM-5 公开的技术贡献里，最容易被忽视的是异步 RL 基础设施：

> 「Building on the 'slime' framework and the decoupled rollout engines initialized in GLM-4.5, our new infrastructure further decouples generation from training to maximize GPU utilization. This system allows for massive-scale exploration of agent trajectories without the synchronization bottlenecks that previously hampered iteration speed.」

这个描述和 AddyOsmani 文章里的「Harness 把 Brain/Hands/Session 解耦」是同一类工程哲学——通过解耦获得并发和弹性。RL 训练侧的解耦（生成和训练分离）对应 Agent 执行侧的解耦（推理和执行分离）。

**关键工程判断**：这种解耦模式正在从 Agent 执行层向上蔓延到 RL 训练层，意味着 AI 系统的工程化正在向分布式、事件驱动方向收敛。

### 3. Vending-Bench 2：年度级任务的能力标尺

Vending-Bench 2 是 GLM-5 最有特色的评测任务——模型被要求自主经营一个模拟自动贩卖机生意一年，评分标准是年终账户余额。这个 benchmark 直接对应 AddyOsmani 文章里提到的三个壁垒中的「长程执行」和「持久化主体性」：

- 需要跨多个月份做决策（长程推理）
- 需要从错误中学习并调整策略（自我修正）
- 需要在变化的环境中保持连贯性（持久化状态）

GLM-5 在这个任务上排名第 1 开源模型，终局余额 $4,432，逼近 Claude Opus 4.5——这意味着在「年」级时间跨度的任务上，开源模型已经接近前沿闭源模型的水平。

### 4. DSA（DeepSeek Sparse Attention）：架构创新的实用路径

GLM-5 采用了 DeepSeek 的稀疏注意力机制，并在其基础上做了适配：

> 「The core philosophy of DSA is to replace the traditional dense O(L²) attention—which becomes prohibitively expensive at 128K contexts—with a dynamic, fine-grained selection mechanism. Unlike fixed patterns (like sliding windows), DSA 'looks' at the content to decide which tokens are important.」

关键发现：**约 90% 的长程上下文注意力是冗余的**——这解释了为什么稀疏注意力在长上下文任务上能和 dense attention 持平，同时计算量降低 1.5-2 倍。

这对 Agent 工程的启示：Context 管理和压缩（对应 AddyOsmani 文章里的 Context Rot 问题）不是工程补丁，而是模型架构设计的一部分。

---

## 核心技术数据

| 指标 | 数值 |
|------|------|
| 总参数量 | 744B（40B 激活，MoE） |
| 专家数量 | 256 |
| 训练 Token 数 | 28.5T |
| 最长上下文 | 200K |
| Intelligence Index v4.0 | 50（第 1 开源） |
| SWE-bench Verified | SOTA 级别 |
| Vending-Bench 2 终局余额 | $4,432（开源第 1） |
| LMArena Text / Code Arena | #1 开源 |

---

## 与本文 Article 的闭环

| Article 发现 | GLM-5 对应 |
|-------------|-----------|
| 长程推理的三个壁垒：有限上下文、无持久状态、无自我验证 | DSA 解决有限上下文；异步 Agent RL 学习长程交互中的自我修正 |
| 「范式转变：委托经济可行性」——30+ 小时自主编码已经突破临界点 | GLM-5 的 Vending-Bench 2 证明年尺度任务在可控范围内 |
| 模型-角色匹配——GPT 适合 Worker，Opus 适合 Planner | GLM-5 的 Agentic RL 专门训练模型的自主决策能力 |
| Context Rot 需要架构级解决方案 | DSA 稀疏注意力确认 90% 上下文是冗余的 |

---

## 原文引用

1. 「GLM-5 represents a paradigm shift in both performance and efficiency, achieving state-of-the-art status on major open leaderboards. More significantly, GLM-5 redefines the standard for real-world coding, demonstrating an unprecedented ability to handle complex, end-to-end software development tasks that go far beyond the scope of traditional static benchmarks.」— GLM-5 Paper, arXiv:2602.15763

2. 「The core philosophy of DSA is to replace the traditional dense O(L²) attention...with a dynamic, fine-grained selection mechanism. Unlike fixed patterns (like sliding windows), DSA 'looks' at the content to decide which tokens are important.」— GLM-5 Paper

3. 「We have developed asynchronous algorithms that allow the model to learn from diverse, long-horizon interactions continuously. These algorithms are specifically optimized to improve the model's planning and self-correction capabilities in dynamic environments.」— GLM-5 Paper
