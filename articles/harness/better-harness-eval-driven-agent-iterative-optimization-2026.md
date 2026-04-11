# Better Harness：Eval-Driven Agent 迭代优化的工程方法论

> **核心问题**：Harness Engineering 的核心问题是"如何让 Harness 自主变好"——而不是靠工程师不断手动调 Prompt、调工具描述、调指令。LangChain 的 Better Harness 给出了一个具体答案：用 Evals 作为梯度信号，对 Harness 进行迭代式 hill-climbing。
>
> **读完能得到什么**：理解"Evals as training data for harness engineering"的核心抽象、Holdout Sets 防止过度拟合的机制、Better-Harness 闭环的具体步骤，以及这个方法论背后的 compound systems 工程直觉。

---

## 一、问题：Harness 为什么需要"学习"

传统 Harness 开发是手工的：工程师观察 Agent 的失败案例，手动修改 Prompt 或工具描述，然后祈祷这次改对了。循环往复，依赖经验积累，但缺乏系统性。

这在原型阶段勉强能用。但当 Agent 进入生产，任务复杂度上升，Harness 的"参数空间"（System Prompts、工具集、Middleware/Hooks、Memory 配置、子 Agent 委托策略……）变得巨大，手工调优无法覆盖所有边界情况。

更好的思路：**让 Harness 自己能变好，像模型通过训练数据学习一样**。

这个思路的关键问题是：模型学习的"梯度"从哪里来？

答案：Evals。

---

## 二、核心抽象：Evals as Training Data for Harness Engineering

这是 Better Harness 最重要的 insight。

在经典机器学习中，训练数据提供梯度信号来更新模型权重。在 Harness Engineering 中：

```
Evals = 训练数据
Harness = 模型
"这个改动让 Agent 的行为变好了吗？" = 梯度信号
```

每个 Eval Case 贡献的信号是："Agent 是否采取了正确行动"或"是否产生了正确结果"。这个信号指导下一步的 Harness 改动。

这意味着 Harness 开发和模型训练遵循相同的原则：

| ML 训练原则 | Harness Engineering 对应 |
|------------|------------------------|
| 数据质量决定上限 | Eval 质量决定优化上限 |
| Train/Test Split | Optimization Set / Holdout Set |
| 防止过拟合 | 防止 Harness 对特定 Evals 过度特化 |
| 泛化能力 | Holdout Set 上的表现 |

**但有一个关键差异**：Harness 优化是 compound systems 工程——不只是调整算法，还涉及工具描述、系统 Prompt、Middleware、Memory 策略等多个相互耦合的组件。任何单个改动都可能产生连锁反应。

这正是为什么 Better Harness 不只是一个优化算法，而是一套**包含方法论、工程实践和组织流程的完整系统**。

---

## 三、方法论：Better-Harness 的迭代闭环

Better Harness 的闭环包含 5 个主要阶段：

```
数据采集 → 实验设计 → 优化执行 → 验证 → 人工审查
```

### 3.1 数据采集：三种 Eval 来源

**手工精选（Hand-Curated）**
工程师为特定任务手工编写 Eval Case。这些 Case 质量高，但难以规模化生产。

**生产轨迹挖掘（Production Traces）**
每次 Agent 交互生成一个 Trace，失败案例直接成为 Eval 材料。这是高杠杆的改进方式——真实使用中暴露的问题比任何手工设计都更能反映系统短板。

LangChain 的实践经验：团队 Dogfooding 自己的 Agent 时，Slack 里直接分享 Trace 链接和错误报告。这种公开可见性帮助整个团队建立对 Agent 行为的共享认知。

**外部数据集**
第三方数据集有用，但需要手工筛选确保测试 Case 反映的是目标行为，而非其他无关变量。

**打标签（Tag Everything）**
每个 Eval 都打上行为分类标签："tool selection"、"multi-step reasoning"、"followup quality" 等。标签的价值：
- 支持有意义的 Holdout Split（同类数据不能全部放进 Optimization Set）
- 支持针对性实验（只看某个子集的 Eval 结果）
- 节省成本（按标签跑子集而非全量）

### 3.2 实验设计：Optimization Set / Holdout Split

这是防止过度拟合的关键机制。

**Optimization Set**：用于驱动 Harness 改进的数据集。模型（这里指 Harness）在这些数据上"训练"。

**Holdout Set**：保留的、用来衡量泛化能力的数据集。优化后的 Harness 必须在这些没见过的数据上也表现良好，否则说明改动了只是"记住了答案"而非"学会了能力"。

LangChain 的经验：**autonomous hill-climbing 有极强的过拟合倾向**——Harness 在 Optimization Set 上得分越来越高，但在 Holdout Set 上原地踏步甚至下降。Holdout Set 是唯一能发现这个问题的机制。

为什么强调"同类分布"？Holdout Set 要和 Optimization Set 来自相同的分布（same general distribution），否则通过 Holdout 只说明改了泛化到了另一个分布，不说明学会了能力本身。

### 3.3 优化执行：诊断 → 实验 → 验证

每轮迭代的具体步骤：

**诊断（Diagnose）**
从 Trace 中找失败模式。分数聚合看各类别的总体表现，Trace 细节看具体哪里出了问题、为什么。

**实验（Experiment）**
一次只改一个维度（避免混淆）。可能是：
- 更新一段 Prompt 指令（最常见的改动）
- 添加或更新一个工具及其描述
- 调整工具组合以消除歧义
- 修改 Middleware/Hooks 逻辑

**验证（Validate）**
每一步都会检查：新的改动是否在新的 Evals 上有改进，同时在原本已经通过的 Evals 上没有回归。如果有回归，Agent（或者工程师）需要在下一次更新中修复，但不能丢掉已有改进。

### 3.4 人工审查（Human Review）

自动化指标永远不够。人工审查的价值在于：

- 发现被指标忽略的边缘情况
- 识别过度特化到 Optimization Set 的指令（它们不在 Holdout 上造成伤害，但浪费 Token）
- 作为最终 Gate，确保任何改动在人工判断上也合理

LangChain 的经验：很多"改进了分数"的改动，人工审查后会发现在生产环境中是负面效果——比如一个指令让 Agent 变得更啰嗦，虽然解决了特定问题但用户体验下降。

---

## 四、实验结果：Sonnet 4.6 vs GLM-5 的对比

LangChain 在 Claude Sonnet 4.6 和 Z.ai GLM-5 上做了 Better-Harness 实验，用了两个行为维度：**Tool Use** 和 **Followup Quality**。

| Model | Phase | Optimization Tool Use | Optimization Followup | Holdout Tool Use | Holdout Followup |
|-------|-------|----------------------|----------------------|------------------|-----------------|
| Claude-sonnet-4-6 | Before | 1/2 | 0/3 | 7/8 | 2/6 |
| Claude-sonnet-4-6 | After | 2/2 | 2/3 | 7/8 | 6/6 |
| GLM-5 (baseten) | Before | 0/2 | 0/3 | 6/8 | 1/6 |
| GLM-5 (baseten) | After | 2/2 | 3/3 | 7/8 | 6/6 |

**关键数据**：
- 两个模型在 Optimization Set 上都有显著提升
- 两个模型在 Holdout Set 上的泛化效果也很好——尤其是 Followup Quality，GLM-5 从 1/6 提升到 6/6，Sonnet 4.6 从 2/6 提升到 6/6
- 这说明 Better-Harness 发现的改动确实学到了能力，而非记住了 Optimization Set 的答案

---

## 五、Better-Harness 发现的具体 Harness 改进

以下是优化循环自主发现的有趣改动：

| 发现的问题场景 | 受影响模型 | 新增指令 | 效果 |
|-------------|----------|---------|------|
| Agent 在trivial 的缺失措辞上卡住不前 | Sonnet, GLM-5 | "当请求明显隐含默认值时，使用合理的默认值。" | Agent 停止了无关紧要的追问，顺利完成 action-taking evals |
| Followup 重复问用户已提供的信息 | Sonnet, GLM-5 | "不要询问用户已经提供的细节。" | 循环任务不再因冗余问题失败 |
| GLM-5 频繁发近似重复搜索 | 主要是 GLM-5 | "一旦有足够信息起草简洁摘要，就不要再继续发近似重复搜索。" | Search-then-deliver evals 变得更可靠，不再循环 |
| 第一个 Followup 与任务不相关 | Sonnet, GLM-5 | "先问领域定义性问题，再问实现问题。" | 这是 Planning 策略的一种形式，让后续对话更相关 |

**核心 insight**：这些改动都是**在 Prompt 层面加一行指令**就能解决的大问题。手工调优时，这些问题可能需要花很长时间才能被工程师发现和修复；Better-Harness 循环让这个过程自动化、数据化。

---

## 六、Eval 的维护：回归保护与春整理

Better Harness 还有一个重要实践：**Eval Suite 不是单调递增的**。

随着模型能力提升，一些 Eval Case 会变得太简单（已饱和），不再能区分 Agent 的能力差异。另一些 Eval 可能因为业务方向变化而不再相关。

LangChain 的做法：定期评估每个 Eval 是否仍然有用，及时清理。这类似传统软件工程的"Technical Debt 清理"——保持测试套件的精简和有效，而不是堆砌越来越大的测试覆盖。

**回归保护（Regression Protection）**
当 Agent 正确处理了某个 Case，这个 Case 就变成回归测试：保护已有的能力不被后续改动破坏。这和 Test Driven Development（TDD）的思路一致。

---

## 七、未来方向：自动化错误检测与修复

LangChain 正在推进更高程度的自动化：

1. **从 Trace 自动派生 Eval**：每次生产环境中的失败案例自动变成一个 Eval Case。"Flywheel：更多使用 → 更多 Trace → 更多 Evals → 更好的 Harness"

2. **自动化错误分类和聚类**：持续监控生产 Trace，对失败案例做分类和聚类，识别系统性的失败模式，而非只看单个案例。

3. **Harness 版本对比**：同一 Trace 在不同 Harness 版本下的表现对比，直观显示哪个改动贡献了什么行为变化。

这些方向的共同点是：**把 Trace 数据变成 Harness 优化的原材料**，而不是靠工程师手工观察和猜测。

---

## 八、方法论评析：价值与局限

### 价值

1. **系统化了"Harness 调优"这个原本高度依赖经验的手工过程**：有了 Eval + Holdout Split + 迭代闭环，任何团队都可以复制这个流程，而不是靠"有经验的 Harness 工程师"个人能力。

2. **揭示了 ML 训练和 Harness 工程的深层类比**：这个类比是有实质意义的——两者都是 compound systems，都有过拟合问题，都有泛化挑战。

3. **实证证明了方法论有效**：Sonnet 4.6 和 GLM-5 在 Holdout 上的泛化结果是硬的证据。

### 局限

1. **方法论本身需要人工维护**：Evals 的来源和标注、Holdout Split 的合理性、Human Review 的质量——这些都需要人来保证，不能完全自动化。

2. **不同模型的 Harness 适配成本仍然高**：Better Harness 自己的实验就显示，同一套 Harness 在 Sonnet 4.6 和 GLM-5 上的基线表现差异巨大。这意味着每个新模型都需要独立的"适配"过程。

3. **封闭系统 vs 开放生态**：Better Harness 的研究版本已开源（langchain-ai/deepagents），但完整实践需要 LangSmith 生态。这和它自己批评的"专有锁定"有一定的内在矛盾。

---

## 九、核心 insight

1. **Harness 是 Compound System，不能用单点优化思路**：工具 Prompt、系统指令、Middleware、Memory 之间相互耦合。Better Harness 的方法论正确性在于，它承认了这个复杂性，而不是试图用一个"最优改动"解决所有问题。

2. **Holdout Set 是防止自欺的唯一机制**：没有 Holdout，Harness 工程师无法区分"学会了能力"和"记住了答案"。这个概念从 ML 借鉴过来是对的。

3. **Eval 是连接生产数据和 Harness 改进的桥梁**：最有价值的 Eval 来源是生产 Trace 中的失败案例——这是真实用户遇到的真实问题，远比手工设计的 Eval 更能反映系统的实际短板。

4. **Human-in-the-loop 不可替代**：在 Eval 设计、Human Review 和系统判断上，人的判断力不可缺。完全自动化的 Harness 优化目前还不现实。

---

> **相关阅读**：
> - [Harness Engineering：深度约束下的 Agent 能力最大化](../harness/harness-engineering-deep-dive.md) — Harness Engineering 的基础框架
> - [Anthropic Engineering：量化 Agentic Coding Eval 的基础设施噪声](../evaluation/infrastructure-noise-agentic-coding-evals-2026.md) — Eval 质量与测量可靠性的系统性研究
> - [Agent Harness Engineering：框架工程化实践](../harness/agent-harness-engineering.md) — Harness 的工程化实践
