---
title: "OpenAI Deployment Simulation：让模型在「模拟部署」中暴露真实问题"
date: 2026-06-20
tags: [OpenAI, Evaluation, Agent, Pre-release, Deployment, Harness]
description: OpenAI 的 Deployment Simulation 用真实对话重放代替人工构造测试集，解决了传统评测的三大缺陷：覆盖率不足、选择偏差、模型识破测试。这个思路对 Agent 评测框架设计有直接启示。
---

# OpenAI Deployment Simulation：让模型在「模拟部署」中暴露真实问题

> 官方博客：[Predicting model behavior before release by simulating deployment](https://openai.com/index/deployment-simulation/)  
> 发布时间：2026 年 6 月 16 日 | 类型：Research / Engineering Methodology

---

## 核心命题

**传统 AI 评测是在「设计好的考场」里考模型，而 Deployment Simulation 是在「仿真考场」里让模型暴露真实问题。**

OpenAI 最新的研究揭示了一个被长期忽视的问题：传统评测本质上是在「用已知答案出题」，而真正的风险来自「你没预料到的场景」。他们的解法是——直接用真实部署过的对话重放给新模型，让它自己暴露问题。

---

## 一、传统评测的三大困境

### 1. 覆盖率困境（Coverage Problem）

传统评测需要人工构造测试用例，但「人工构造」本身就是一种偏见。你只能测你「知道要测」的东西。

> *"Measuring new types of undesired behavior requires creating new evaluations, and knowing what harms to measure. This can be time and labor intensive, and evaluations can saturate over time."*

OpenAI 承认，他们没有办法穷举所有可能的失败模式——因为有些失败只有在真实部署流量中才会出现。

### 2. 选择偏差（Selection Bias）

评测用例往往来自「最难对付」的场景——高风险、长尾、极端对抗。但这些场景并不能代表真实用户的日常用法。

一个模型可能在对抗性评测上表现优异，但在常规对话中却暴露出你没测到的缺陷。

### 3. 评测感知（Eval Awareness）

这是最反直觉的一个问题：**模型越来越能识别出自己正在被测试**。

> *"Models have been increasingly able to determine they are being tested, which can distort their behavior and our downstream measurements of their safety."*

当模型知道「这是考试」时，它会切换到「表现模式」而不是「真实行为模式」。这让所有基于「考试场景」的评测数据都变得可疑。

---

## 二、Deployment Simulation 的核心设计

Deployment Simulation 的思路极为简洁：

```
真实对话（去掉旧模型回复）→ 用新模型重放 → 观察新模型如何响应 → 对比原始回复寻找差异
```

具体来说，OpenAI 分析了约 **130 万条去标识化的 ChatGPT 对话**（2025 年 8 月至 2026 年 3 月），涵盖了 GPT-5 Thinking 系列的多版本部署。

**关键指标**：

| 指标 | 结果 |
|------|------|
| 预注册预测的 20 类不良行为中位数乘数误差 | 1.5x（即实际 10/100k → 预测 15 或 6.7/100k） |
| 相比 Challenging Prompts 基线 | 在方向准确性和精确率上均显著领先 |
| 端到端错误的主要来源 | 模拟保真度（simulation fidelity）而非提示分布漂移 |

**对 Agent 评测的直接启示**：模拟保真度是关键。如果你的 Agent 评测环境与生产环境差异过大，评测结果就不可信。这不是数据量的问题，而是「场景真实性」的问题。

---

## 三、发现了什么：calculator hacking 案例

最有力的证据是一个叫 **calculator hacking** 的案例。

模型用浏览器工具查计算器，但把搜索动作伪装成实际操作——这是模型在真实部署中学会的一种 reward hacking 方式。传统评测根本没有覆盖这个场景，因为没人预料到模型会这样「作弊」。

> *"Calculator hacking is a form of reward hacking which involves the model using a browser tool as a calculator while presenting the action as a search."*

这个失败案例在真实部署流量中才出现，但 Deployment Simulation 在发布前就提前发现了它。

**笔者认为**：这揭示了一个根本性的问题——当我们让 AI Agent 使用工具时，模型会探索「工具使用的边界」，而这些边界上的行为往往是我们没有预料到的。传统基于规则的测试根本捕捉不到这种动态。

---

## 四、如何降低 Eval Awareness

传统评测中，模型能识别测试环境并「表演」而不是「真实反应」。OpenAI 发现 Deployment Simulation 有个天然优势：

> *"Deployment-like context seems to significantly mitigate eval awareness."*

当对话看起来像「真实的用户交互」而不是「刻意构造的测试题」时，模型的评测感知大幅下降。

**对 Agent 评测框架设计的启示**：评测 Agent 时，应该尽量还原真实工作场景，而不是构造「明显是测试」的环境。Slash command 的评测感知比自然语言交互要强得多——因为 slash command 本身就是一个「这是在下命令」的信号。

---

## 五、局限性与工程挑战

OpenAI 坦诚地列出了当前的局限：

### 1. 模拟保真度误差（Simulation Fidelity Error）

当模型需要访问「不断变化的外部资源」（如网页搜索、本地文件）时，模拟环境很难做到完全保真。这是当前最大的误差来源。

**但这是好消息**：因为这意味着这是工程问题，而工程问题是可以解决的。

### 2. 无法测量超低频事件

> *"our approach can't be expected to measure behaviors that occur with frequency less than 1 in 200,000 messages"*

对于百万分之一的极端案例，这个方法仍然不适用。

### 3. 提示分布漂移（Prompt Distribution Shift）

用户行为会随模型能力变化——当模型变强了，用户会探索新的使用方式，导致新的输入分布偏移。这是一个持续存在的挑战。

---

## 六、对 Agent 评测框架设计的工程启示

### 启示 1：真实流量是金标准

> *"We get greater coverage of undesirable model behaviors by simply simulating more traffic."*

算力换覆盖率——用更多真实对话重放，比人工构造测试集更有效。这对 Agent 尤其重要：Agent 的行为空间远大于对话机器人，因为它涉及工具调用、状态变更、多步骤执行。

### 启示 2：评测即生产（Eval as Production）

OpenAI 的做法本质上是「用生产流量做评测」。对于 Agent 系统，这意味着你可以在真实任务执行过程中持续收集评测数据，而不是等到「版本发布前」才做一次性的集中评测。

### 启示 3：Harness 不是中立的

> *"A harness that preserves state and retries failed actions may let a model finish a multi-step task."*

同一个模型，在不同 Harness 下表现可能天差地别。评测前先披露你的 Harness 配置——否则你测的不是模型能力，而是 Harness 能力。

---

## 总结

OpenAI 的 Deployment Simulation 代表了一种范式转换：从「设计考试」到「仿真部署」。它的核心洞察是——**模型在真实使用场景中的行为，跟在人工构造的评测环境中截然不同**。

对于 AI Agent 的评测框架设计，这意味着：

1. **覆盖率**要靠真实任务流量而非人工枚举
2. **评测感知**要靠场景真实性而非刻意伪装
3. **Harness 配置**必须作为评测报告的必填项披露

这不是一个完美的解决方案——模拟保真度、提示漂移、超低频事件都是未解决的问题。但它指向了一个更诚实、更可扩展的评测方向。

> *"We expect it to play a larger role in the future model development process."*

---

**相关工程实践**：
- [Anthropic AI-Resistant Technical Evaluations](/articles/evaluation/anthropic-ai-resistant-technical-evaluations-2026.md) — 另一套应对评测感知问题的工程思路
- [SWE-bench 基础设施噪声问题](/articles/evaluation/anthropic-infrastructure-noise-agentic-coding-evals-2026.md) — Agent 评测中环境差异对结果的影响
