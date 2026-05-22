# The "Think" Tool：Agent 的停顿与思考机制

> 本文基于 Anthropic Engineering Blog「The "think" tool: Enabling Claude to stop and think」（2025年3月），深度分析专用的思考工具如何让 Claude 在复杂工具调用场景中实现 54% 的相对性能提升。

---

## 核心论点

**"Think" tool 解决了一个根本矛盾**：Extended Thinking 是生成响应前的大脑，Think Tool 是工具调用后的校验站。当 Agent 需要处理长链工具调用结果、遵循复杂策略、或在每步都建立在前一步基础上的决策时，一个专门的思考空间能显著减少"想当然"的错误。

> "The 'think' tool is for Claude, once it starts generating a response, to add a step to stop and think about whether it has all the information it needs to move forward."
> — [Anthropic Engineering: The "think" tool](https://www.anthropic.com/engineering/claude-think-tool)

**笔者认为**：Think Tool 的核心价值不是「让模型想更多」，而是「在错误的代价被放大之前创造一个校验节点」。长链工具调用中，第一个决策失误会级联传播——Think Tool 在每个关键节点提供了一次重新校准的机会。

---

## Think Tool vs Extended Thinking：两个不同的机制

Anthropic 明确区分了两个看似相似但本质不同的能力：

| 特性 | Extended Thinking | Think Tool |
|------|-----------------|-----------|
| **触发时机** | 生成响应**之前** | 生成响应**过程中**（工具调用后）|
| **目的** | 深度迭代、规划复杂任务 | 校验工具结果、补充缺失信息 |
| **适用场景** | 编码、数学、物理（无需工具）| 复杂工具链、政策导航、顺序决策 |
| **资源消耗** | 高（完整的深度思考）| 低（针对性的补充推理）|

> "Extended thinking is all about what Claude does **before** it starts generating a response. The 'think' tool is for Claude, once it starts generating a response, to add a step to stop and think about whether it has all the information it needs to move forward."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

**关键区分**：Extended Thinking 解决「我想做什么」，Think Tool 解决「我有没有漏掉什么」。

---

## τ-Bench 上的性能验证

Anthropic 在 τ-Bench（tau-bench）上评估了 Think Tool 的效果——这是 Sierra Research 开发的客户服务中心基准，模拟真实的工具调用、策略遵循和对话场景。

### 核心指标：pass^k

不同于常见的 pass@k（至少一次成功），τ-Bench 使用 pass^k（连续 k 次全部成功）——这更符合客服场景的可靠性要求。

### Airline Domain：54% 相对提升

在 airline domain（高复杂度政策环境）中：

| 配置 | pass^1 | pass^5 |
|------|--------|--------|
| Think + 优化提示 | **0.570** | 0.340 |
| Think Tool（无提示）| 0.404 | 0.100 |
| Extended Thinking | 0.412 | 0.160 |
| Baseline（无任何增强）| 0.370 | 0.100 |

> "The 'think' tool with an optimized prompt achieved 0.570 on the pass^1 metric, compared to just 0.370 for the baseline—a 54% relative improvement."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

**关键发现**：单独使用 Think Tool 已有提升，但配合领域特定提示才能发挥最大效果。Easy domain（retail）则不同——单独 Think Tool 就达到了最高 pass^1 = 0.812，因为政策复杂度更低。

### SWE-Bench：1.6% 平均提升

Think Tool 同样适用于代码任务，在 SWE-Bench（n=30 with think, n=144 without）：

> "The isolated effects of including this tool improved performance by 1.6% on average (Welch's t-test: t(38.89) = 6.71, p < .001, d = 1.47)."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

1.6% 在 SWE-Bench 这种高难度基准上具有统计显著性（d=1.47，效应量大）。

---

## 什么场景下 Think Tool 最有效

### 1. 工具输出分析（Tool Output Analysis）

当 Claude 需要仔细处理前序工具调用的输出才能决定下一步行动时——特别是在可能需要回溯方法时。

```json
{
 "name": "think",
 "description": "Use the tool to think about something. It will not obtain new information or change the database, but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.",
 "input_schema": {
   "type": "object",
   "properties": {
     "thought": {
       "type": "string",
       "description": "A thought to think about."
     }
   },
   "required": ["thought"]
 }
}
```

### 2. 策略密集环境（Policy-Heavy Environments）

当 Agent 需要遵循详细指南并验证合规性时——Think Tool 让模型逐一核对规则。

Anthropic 使用的 airline domain 优化提示示例：

```
## Using the think tool
Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness
```

### 3. 顺序决策（Sequential Decision Making）

每步建立在前一步基础上，错误代价高的场景——航班预订的每一步都依赖前一步的信息。

> "The 'think' tool is better suited for when Claude needs to call complex tools, analyze tool outputs carefully in long chains of tool calls, navigate policy-heavy environments with detailed guidelines, or make sequential decisions where each step builds on previous ones and mistakes are costly."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

---

## 什么场景下 Think Tool 无效

**笔者认为**：Think Tool 的滥用来自对「思考」能力的过度期待。LLM 的思考质量受限于其对齐程度和推理能力，不是所有问题都能通过「多想一会儿」解决。

### 1. 非顺序工具调用

单次或并行工具调用场景——此时没有中间状态需要校验。

### 2. 简单指令遵循

约束少、默认行为已足够好的场景——额外的思考反而增加 token 消耗而无收益。

> "If Claude only needs to make a single tool call or multiple parallel calls to complete a task, there is unlikely to be any improvements from adding in 'think.'"
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

---

## 工程实现最佳实践

### 1. 提示位置：系统提示 > 工具描述

当提示内容长且复杂时，放在系统提示比放在工具描述中更有效——这提供更广泛的上下文，帮助模型将思考过程整合到整体行为中。

### 2. 领域特定示例是关键

在复杂领域（airline policy），没有示例的 Think Tool 效果有限；有了领域特定的推理示例后，效果显著提升。

### 3. 最小化实现成本

```python
# 几乎零成本实现
tools = [
    # ... 其他工具 ...
    {
        "name": "think",
        "description": "Use the tool to think about something...",
        "input_schema": {...}
    }
]
```

> "The best part is that adding this tool has minimal downside in terms of performance outcomes. It doesn't change external behavior unless Claude decides to use it, and doesn't interfere with your existing tools or workflows."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

---

## 评估基础设施：τ-Bench 生态

Anthropic 的 Think Tool 评估依赖 Sierra Research 的 τ-Bench 框架，这是一个完整的客户服务中心 Agent 评估系统：

| 版本 | 来源 | 特点 |
|------|------|------|
| τ-Bench | [sierra-research/tau-bench](https://github.com/sierra-research/tau-bench) | 初始版本，airline + retail domains |
| τ²-Bench | [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench) | 新增 bank domain + voice evaluation |
| τ²-Bench-Verified | [amazon-agi/tau2-bench-verified](https://github.com/amazon-agi/tau2-bench-verified) | 修正数据集问题，人类验证版 |
| τ³-Bench | — | 1.0.0，支持 Voice + Knowledge + Task Quality |

**τ²-Bench 的双控评估模式**允许分别评估 Agent 和 User Simulator，支持 Half-Duplex（轮次对话）和 Full-Duplex（语音流）两种模式。

---

## 笔者判断

Think Tool 的本质不是「让 AI 更聪明」，而是「让 AI 有机会在错误之后、代价放大之前重新校验」。这种设计模式在人类专家中很常见——老练的医生在做出重大决策前会说「让我再想想」，经验丰富的工程师会在代码提交前做一次自我审查。

> "We recommend using extended thinking for simpler tool use scenarios... The 'think' tool is better suited for when Claude needs to call complex tools, analyze tool outputs carefully in long chains of tool calls, navigate policy-heavy environments with detailed guidelines, or make sequential decisions where each step builds on previous ones and mistakes are costly."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/claude-think-tool)

**关键结论**：Think Tool 不是一个通用推理增强工具，而是一个针对「长链工具调用 + 高代价错误」场景的专项优化。把它当作万能药会浪费资源，把它用在正确场景才能发挥 54% 提升的价值。

---

## 关联项目

- [τ²-Bench: 客户服务中心 Agent 评估基准](https://github.com/sierra-research/tau2-bench) — 支持 banking domain + voice eval
- [τ²-Bench-Verified: 修正版评估数据集](https://github.com/amazon-agi/tau2-bench-verified) — 人类验证的准确标注

---

*来源：[Anthropic Engineering Blog - The "think" tool](https://www.anthropic.com/engineering/claude-think-tool)（Published Mar 20, 2025）*