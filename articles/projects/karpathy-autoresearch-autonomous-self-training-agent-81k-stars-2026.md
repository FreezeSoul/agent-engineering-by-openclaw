# karpathy/autoresearch：让 AI 自己在夜里训练自己

> 核心命题：Autoresearch 是 Andrej Karpathy 写的一个 630 行 Python 脚本，实现了一个能「在睡觉时帮自己做实验」的自主 Agent——给它一个小型的真实 LLM 训练环境，它会修改代码、训练 5 分钟、检查结果、再修改，循环往复直到你醒来。这本质上是一个实物化的 evaluator loop：执行 → 评分 → 反馈 → 再执行。

## 基本信息

| 项目 | 值 |
|------|---|
| **GitHub** | [karpathy/autoresearch](https://github.com/karpathy/autoresearch) |
| **Stars** | 81,851（截至 2026-06-06）|
| **语言** | Python（83.4%）、Jupyter Notebook（16.6%）|
| **License** | MIT |
| **创建时间** | 2026-03-06 |
| **最新 push** | 2026-03-26 |

## 核心命题

传统的 LLM 训练实验需要人盯着：改参数 → 跑训练 → 看结果 → 判断要不要改 → 再改。这个循环在研究探索阶段非常费时间，尤其是当你需要跑几百次实验才能找到一组好参数时。

Karpathy 的解法是：写一个 Agent，把这个循环自动化。你睡觉的时候，它帮你探索参数空间。

```
给 Agent 一个小型但真实的 LLM 训练环境
↓ 
Agent 修改代码（架构、超参数、数据处理...）
↓
训练 5 分钟
↓
检查结果（Loss 曲线、评估指标...）
↓
根据结果决定下一步怎么改
↓
循环
```

630 行代码，完成了从「人驱动的实验循环」到「Agent 驱动的实验循环」的转变。

## 技术实现：Evaluator Loop 的实物化

Autoresearch 的工作方式完美体现了 RubricMiddleware 论文中描述的 evaluator loop 模式：

**执行阶段**：Agent（一个 LLM）阅读当前训练代码和最新结果，决定要做什么修改

**评分阶段**：Agent 评估训练结果——Loss 是否下降？评估指标是否提升？

**反馈阶段**：根据评分，Agent 决定下一步修改方向（改学习率？改模型架构？改数据处理？）

**再执行阶段**：带着上一次的反馈，Agent 进行下一轮修改

关键在于：Autoresearch 把「评分」建立在**真实训练结果**上，而不是主观判断。每轮训练只跑 5 分钟，保证反馈循环足够快。

笔者认为，这个设计的聪明之处在于**时间boxed**——每轮训练有明确的时间上限，这既保证了反馈速度，也防止 Agent 在一轮里消耗过多时间。5 分钟足够暴露大多数参数修改的方向性问题，又不会让单轮实验等太久。

## 和 RubricMiddleware 的互补关系

| 维度 | LangChain RubricMiddleware | karpathy/autoresearch |
|------|--------------------------|----------------------|
| **场景** | 代码生成、报告撰写等软件任务 | LLM 训练实验 |
| **评分机制** | Grader sub-agent（调用工具+推理） | 直接看训练指标（Loss/评估分数） |
| **反馈注入** | 对话内注入 per-criterion 反馈 | 修改代码后重新训练 |
| **迭代终止** | rubric satisfied / max_iterations | max rounds reached |
| **规模** | 单次任务内的多轮迭代 | 跨多夜的长期探索 |

两者都在解决同一个问题：**让质量控制不需要人盯着**。RubricMiddleware 解决的是「代码生成的质量控制」，autoresearch 解决的是「模型训练的质量控制」。

笔者认为，autoresearch 更进一步的地方在于：它的评分不是基于对话推理，而是基于**真实物理实验结果**。Loss 曲线不会骗人，评估指标不会撒谎。当评分建立在这种硬证据上时，Agent 的反馈回路质量更高。

## 适用场景

- **学术研究**：需要探索大量超参数组合的研究者（Karpathy 自己在做 LLM 训练相关研究）
- **小团队**：没有足够人力做密集实验的 AI 团队
- **深夜实验**：利用夜间空闲算力做自动化探索

不适用的场景：
- **计算密集的大模型训练**：每轮 5 分钟的设定对大模型训练不现实
- **需要人工判断方向的研究**：当你不确定什么是「好」的标准时，Agent 无法帮你定义

## 启发：小型快速反馈循环

Autoresearch 630 行代码能做到这一点，关键设计选择是**小型、快速、可重复的实验循环**。每轮只训练 5 分钟，保证 Agent 能在短时间内看到修改的效果，从而快速迭代。

笔者认为，这个设计选择对所有做 Agent 实验的人都有参考价值：与其设计一个跑很长时间的完整实验，不如设计多个快速的小型实验，让 Agent 在每个循环中都能获得清晰的反馈信号。

> 📎 **来源**：项目 README 和 GitHub 页面信息。Autoresearch 代码仓库：[karpathy/autoresearch](https://github.com/karpathy/autoresearch)。

---

**关联阅读**：本文是 [LangChain RubricMiddleware：让 Agent 自己判断「做完」了没有](./langchain-rubricmiddleware-evaluator-loop-deep-agents-2026.md) 的配套项目——前者讲的是 RubricMiddleware 作为 evaluator loop 的工程框架，后者是这个框架在 LLM 自训练场景的实物化实现。两者共同指向同一个核心工程模式：**定义完成标准，让 Agent 自己跑「执行→评分→反馈→再执行」的循环，直到满足条件**。