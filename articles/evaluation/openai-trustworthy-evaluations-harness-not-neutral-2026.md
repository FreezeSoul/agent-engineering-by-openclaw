# OpenAI 第三评估方评估方法论：Harness 不是中立的

> 本文解读自 OpenAI 官方博客 *A shared playbook for trustworthy third party evaluations*。
> 原文：[openai.com/index/trustworthy-third-party-evaluations-foundations](https://openai.com/index/trustworthy-third-party-evaluations-foundations)

---

## 核心命题

评估 AI Agent 的第三方测试报告，通常只给你一个分数。但没有人告诉你：**那个分数是在什么"笼子"里测出来的**。

OpenAI 最新的方法论博客揭示了一个被长期忽视的事实——**Harness（评估框架/笼子）不是中立的测量工具，而是评估结果的一部分**。同一个模型，在不同的 Harness 下跑，分数可能差出一大截。这个差距不是模型能力变了，是"笼子"的形状不同。

---

## 一、问题：Harness 被当成透明的黑箱

传统的模型评测把评测环境当作"自然条件"——就像在标准温度下测水的密度。但 AI Agent 不一样。当模型可以调用工具、保持状态、跨步骤恢复错误时，**Harness 决定了任务是否能被完成，以及如何被完成**。

原文的核心洞察：

> *"A harness that preserves state and retries failed actions may let a model finish a multi-step task that the same model never completes in a simpler harness."*

换句话说：有些"能力"其实是 Harness 赋予的，不是模型本身就有的。评测如果不披露 Harness 配置，就是在用未标注的变量玩游戏。

---

## 二、三类评估声明：评估前先说清楚你在测什么

OpenAI 把评估方想要证明的结论分成三类，每类对 Harness 有不同的要求：

| 声明类型 | 测什么 | 需要的 Harness |
|---------|--------|---------------|
| **能力诱导（Capability Elicitation）** | 系统 A 在真实使用条件下能否完成 X 类任务 | 最强配置——包括用户实际会用到的工具、预算、错误恢复机制 |
| **受控对比（Controlled Comparison）** | 系统 A 是否比系统 B 更好 | 固定 Harness + 固定任务集 + 固定预算，各系统用同一套配置 |
| **安全护栏（Safeguard Robustness）** | 系统的安全护栏能否抵御专家级攻击 | 攻击诱导配置——需要给足预算和攻击策略空间 |

这个分类的价值在于：**它把"评测结果"还原成"某套配置下的测量值"**，而不是一个绝对的能力标签。

---

## 三、五个有效性威胁：为什么评测结果可能是假的

即便 Harness 设计良好，评估仍然可能被以下五种效应扭曲：

| 威胁 | 是什么 | 如何识别 |
|------|--------|---------|
| **Reward Hacking** | 模型找到评分漏洞，拿分但不展示目标行为 | 人工抽检输出样本 |
| **Refusals** | 模型以掩盖测试行为的方式拒绝回答 | 检查拒绝模式是否异常 |
| **Contamination** | 评测任务或变体出现在训练数据里，或在评测中被浏览发现 | 数据来源审计 |
| **Broken Problems** | 任务本身就是无效的（答案需要未说明的实现细节，或环境缺少关键文件） | 环境可用性验证 |
| **Sandbagging** | 模型检测到被评测，故意压低表现 | 对比已知基线 |

原文指出：**这五项检查应该在每次评估运行时都执行**，而不是只在论文发表前跑一遍。

---

## 四、Harness 决定测出了什么：三个具体案例

### 案例 1：Compaction 改变评测结果

GPT-5.5 在 OpenAI 的网络靶场（cyber ranges）评测中，使用 **compaction**（上下文压缩）技术的 Harness 版本得分显著更高。Compaction 保留了任务相关的上下文，使模型在长交互中不丢失关键信息。如果 Harness 没有 compaction，实测的性能会严重低估模型的实际能力。

这意味着：Compaction 不是模型的能力，是 Harness 弥补了模型上下文管理的局限。

### 案例 2：预算可以改变排名

UK AISI 的网络靶场评测显示，把评测预算从 10M tokens 提升到 100M tokens，性能最高提升了 59%，而且在最高预算下仍未达到天花板。

这说明：**很多"能力上限"其实是预算上限**。评测报告如果不披露预算，就是给了一个误导性的能力标签。

### 案例 3：标准化 Harness 的局限

对于跨系统对比，OpenAI 建议使用 Codex CLI 作为标准化 Harness——它提供了固定的 Agent 循环和工具接口。但原文也承认：

> *"The ideal approach for maximum elicitation would be to optimize a bespoke harness for each task and system, but doing so is currently impractical in practice."*

标准化意味着公平比较，但也意味着对每个系统的"真实最强表现"有所压抑。

---

## 五、这对 Agent 工程意味着什么

作为构建 AI Agent 系统的工程师，这个方法论有三条直接的实践启示：

**1. 评估你的 Harness，不只是你的模型**

当你的 Agent 在生产环境中表现不如预期，先问：生产 Harness 和评测 Harness 差在哪里？有没有状态持久化？有没有错误重试？有没有工具可用性差异？

**2. 披露即责任**

如果你在用第三方评测结果做技术选型，问清楚：Harness 配置是什么？预算多少？有没有五项有效性检查？不知道这些，数字没有任何参考价值。

**3. 把 Harness 纳入你的 CI/CD**

原文提到的 Agent 改进循环（Traces + Evals + Codex）把评测变成了一个持续反馈系统。Harness 的变化应该被版本控制，评测结果应该在每次代码变更后重新跑——而不是只在发布前跑一次。

---

## 总结

OpenAI 这篇方法论的核心信息只有一句：**测量结果依赖测量工具，AI Agent 领域尤其如此**。Harness 不是评测的"背景"，是评测的"演员"。

在 Agent 工程中，这意味着：
- 评测报告不披露 Harness 配置 = 数据无效
- 能力上限在很大程度上 = Harness 配置的上限
- 真正的改进需要评测环境和生产环境使用同一个 Harness

这不是学术问题。是你在部署 Agent 系统时每天都在面对的工程现实。

---

## 参考来源

- OpenAI, *"A shared playbook for trustworthy third party evaluations"*, [openai.com/index/trustworthy-third-party-evaluations-foundations](https://openai.com/index/trustworthy-third-party-evaluations-foundations)
- UK AISI Cyber Range Evaluation, [arxiv.org/pdf/2603.11214](https://arxiv.org/pdf/2603.11214)
- OpenAI Cyber Ranges with compaction, [openai.com/index/equip-responses-api-computer-environment](https://openai.com/index/equip-responses-api-computer-environment)