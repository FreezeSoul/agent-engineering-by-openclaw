# OpenAI AI Chemist：科学验证驱动的多智能体 Harness 工程

**核心论点**：科学领域的 Agent 不能只靠推理——必须有一个 Evaluator Loop 将实验验证纳入反馈链。OpenAI 与 Molecule.one 的 AI Chemist 项目展示了一个完整的多智能体 Harness 架构：GPT-5.4 生成研究提案 → Maria AI 执行高通量实验 → 科学家把关 Steering Prompt → 循环迭代。

---

## 背景：为什么科学领域是 Agent 的特殊战场

大多数 Agent 应用场景（代码生成、文档写作、信息检索）的输出可以被语言模型直接评估——对不对，好不好，人能看懂。

但化学、生物、物理这类实验科学不同。一个假说是否成立，取决于现实世界中分子是否按预期反应。语言模型再强，也无法通过"思考"验证一个化学反应是否真的发生。

这就是为什么科学 Agent 需要一种特殊的 Harness：**Evaluator 不只是另一个模型，而是实验台本身**。

---

## 系统架构：三层 Loop 的嵌套

OpenAI 与 Molecule.one 合作的 AI Chemist 项目，构建了一个三层嵌套的多智能体架构：

```
┌─────────────────────────────────────────────────────────┐
│  科学家层（Human-in-the-Loop）                           │
│  · 编写 Steering Prompt（方向性指导）                   │
│  · 编写 Grader Prompt（评价标准）                       │
│  · 审核 AI 生成的提案，决定哪些进入实验                 │
│  · 独立重复关键实验，验证结果                           │
└─────────────────────────────────────────────────────────┘
                          ↑ 提案筛选 ↓ 实验结果
┌─────────────────────────────────────────────────────────┐
│  GPT-5.4（研究提案生成器）                              │
│  · 读取文献，设计研究提案                              │
│  · 对数千个提案排序打分                                │
│  · 分析实验结果，提出下一轮假设                        │
│  · 核心职责：生成 + 排序，不是执行                    │
└─────────────────────────────────────────────────────────┘
                          ↑ 实验指令 ↓ 原始数据
┌─────────────────────────────────────────────────────────┐
│  Maria AI + Maria Lab（实验执行层）                      │
│  · 将高层提案翻译为详细实验指令                        │
│  · 控制高通量实验室，执行数千个反应                    │
│  · 返回结构化实验数据                                  │
│  · 核心职责：执行 + 测量，不是思考                    │
└─────────────────────────────────────────────────────────┘
```

这个架构的核心洞察是：**每层只做它最擅长的事**。GPT-5.4 擅长生成和推理，但不擅长操作实验仪器；Maria AI 擅长精确执行，但不擅长提出突破性假设。两者通过一个结构化的 Loop 连接，而科学家是整个系统的质量门。

---

## Evaluator Loop 的具体实现

### 提案生成 → 实验验证 Loop

一个完整的研究循环如下：

1. **提案生成**：GPT-5.4 基于文献和科学家的 Steering Prompt，生成数千个研究提案（Prompt 中明确要求提出"令人惊讶但有科学依据"的假设）
2. **提案排序**：用 Grader Prompt 对提案打分，排序后取 Top N 提交给科学家审核
3. **科学家筛选**：科学家从 Top N 中选择 4 个有化学意义的提案投入实验（关键过滤步骤）
4. **实验执行**：Maria AI 将提案翻译为实验网格，运行 10,080 个反应（OAI-M1-03 提案的规模）
5. **结果分析**：Maria AI 分析原始数据，返回结构化结果给 GPT-5.4
6. **下一轮假设**：GPT-5.4 根据实验结果，提出新的假设，进入下一个 Loop

### 最成功的提案：TEMPO 氧化剂发现

OAI-M1-03 提案是整个项目最成功的输出。GPT-5.4 独立发现：温和氧化剂（包括 TEMPO）可以显著改善 Chan-Lam 偶联反应中初级磺酰胺的产率。

科学家当时认为这个提议"令人惊讶且有趣"——这正是好的研究假设应有的品质。

**最终效果**：
- 88% 的硼酸和 83% 的磺酰胺产率提升
- 平均产率从 16.6% 提升到 25.2%
- 30% 以上产率反应的比例从 15.6% 提升到 37.5%
- 科学家独立重复 14 个底物对，11 个确认了微升规模的结论

---

## 为什么这是 Harness 工程，不是普通的 AI 应用

### 关键区别：Evaluator 是实验现实，不是模型输出

传统 Agent 的 Evaluator Loop 通常是：
```
Agent 输出 → 另一个 LLM 评估 → 通过则结束，不通过则重试
```

这个项目中的 Evaluator Loop 是：
```
Agent 提案 → 物理实验验证 → 结果作为下一个 Loop 的输入
```

实验现实作为 Evaluator 的意义在于：**它不会被 Prompt 注入欺骗，不会被模型自我欺骗影响，不会饱和**。只要实验设计合理，物理结果就是客观的。

### Steering Prompt 的设计哲学

科学家编写的 Steering Prompt 不是告诉模型"做什么"，而是定义"什么样的提案值得做"：

> "提出令人惊讶但有化学依据的假设，避免显而易见的组合"

这是一个评价标准的编码，而不是任务指令。这种 Prompt 设计让 GPT-5.4 能够探索更广阔的假设空间，而不是在熟悉的区域打转。

### Human 作为质量门，不是瓶颈

传统观点认为 Human-in-the-Loop 会成为瓶颈——科学家时间有限，AI 生成速度远超人工审核速度。

但这个项目展示了另一种模式：**科学家做的是粗筛，不是精读**。科学家不需要理解每个提案的化学细节，只需要判断"这个提案是否符合化学基本规律"和"这个方向是否有科学价值"。真正深入的化学分析由后续实验完成。

---

## 工程机制提炼：什么让这个 Harness 有效

笔者认为，这个项目展示了三个关键工程机制，对所有科学 Agent 设计都有参考价值：

### 1. 分层抽象，每层专注一个职责

GPT-5.4 不直接控制实验仪器，Maria AI 不直接读文献，科学家不直接分析原始数据。每层只处理它能可靠处理的抽象级别。

> 这比让一个 Agent 同时处理文献、实验、分析更可靠——因为每种能力的最佳模型和工具都不同。

### 2. Grader Prompt 与 Steering Prompt 分离

Steering Prompt 定义方向（"做有价值的研究"），Grader Prompt 定义评价标准（"什么样的提案符合方向"）。两者分离让科学家可以独立调整研究方向，而不需要重写整个 Prompt 系统。

### 3. 物理实验作为不可绕过的事实边界

当 Evaluator 是另一个 LLM 时，模型可以通过"推理得更好"来欺骗评估。但当 Evaluator 是物理实验时，分子不会因为模型认为产率应该高就真的产率高。

这是科学 Agent 相对于纯语言 Agent 的本质优势：**事实边界不可绕过**。

---

## 局限性：为什么说是"Near-Autonomous"而非 Fully Autonomous

科学家在项目中的角色包括：
- 设计初始 Steering Prompt 和 Grader Prompt（一次性工作）
- 选择哪些提案进入实验（每个 Loop 约 4 个决策）
- 纠正实验计划的具体细节（如用 DMSO 替代方案）
- 独立重复关键实验（验证微升规模的结论可复现）

笔者认为，即使在成熟的未来版本中，科学家仍然是必要的：
1. **评价标准的设计**：什么样的科学发现是"有价值的"，这本质上是人类判断
2. **异常处理**：当实验结果出乎意料时，决定是"实验错误"还是"发现了新东西"需要人类判断
3. **责任归属**：科学发现的 credit 和责任归属需要人类承担

---

## 对 Agent Engineering 的启示

这个项目对 Agent 工程的启示超越了化学领域：

**对于任何输出需要物理世界验证的 Agent**（材料科学 Agent、生物实验 Agent、硬件设计 Agent），这个架构提供了一个参考模式：分层 Loop + 物理 Evaluator + Human 质量门。

**对于所有长周期 Agent 任务**，这个项目验证了"Evaluator Loop"范式的有效性：不是一次性生成然后评估，而是多轮迭代，每轮通过更接近 ground truth 的反馈来改进。

**对于 Agent 工程实践**，Steering Prompt 和 Grader Prompt 的分离是一个值得借鉴的设计模式——它让人类专家可以高效地指导 Agent 方向，而不需要深入每个细节。

---

## 引用来源

> "We describe this workflow as near-autonomous, not fully autonomous, because human chemists still made important decisions throughout the process."
> — OpenAI Blog, "A near-autonomous AI chemist improves a challenging reaction in medicinal chemistry", 2026

> "The combined system paired complementary capabilities. Prompts written by scientists working with Maria AI were used with GPT-5.4 within a harness to generate and rank thousands of possible research proposals."
> — OpenAI Blog, 2026

---

**相关主题**：[Harness 工程](/articles/harness/)、[多智能体编排](/articles/orchestration/)、[长周期 Agent](/articles/harness/addyosmani-long-running-agents-three-walls-harness-2026.md)
