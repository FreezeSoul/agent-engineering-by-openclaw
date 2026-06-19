# Anthropic 工程实践：构建有效 Agent 的Workflow模式体系

> 本文源自 Anthropic 工程团队与数十个团队合作构建 LLM Agent 的经验总结，核心洞察是「最成功的实现往往不是用复杂的框架，而是用简单、可组合的模式」。
> 原文：https://www.anthropic.com/research/building-effective-agents

---

## 核心问题：什么时候该用 Agent？

Anthropic 提出的第一个关键判断是：**先问自己要不要用 Agent**。

> "When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed."
> 
> 构建 LLM 应用时，我们建议先找最简单的解，只有在确有必要时才增加复杂度。

这个判断建立在一个基本的成本-收益模型上：
- **Agent 系统往往用延迟和成本换取更好的任务表现**
- 对于很多应用，优化单次 LLM 调用（加上检索和上下文示例）就足够了
- **不要为了用 Agent 而用 Agent**

---

## 核心区分：Workflows vs Agents

Anthropic 明确区分了两类系统：

| 类型 | 定义 | 适用场景 |
|------|------|---------|
| **Workflows** | LLM 和工具通过**预定义的代码路径**编排 | 任务可预测、需要一致性的固定流程 |
| **Agents** | LLM **动态指导**自己的流程和工具使用，自己决定如何完成任务 | 需要灵活性、需要模型驱动决策的开放场景 |

> "Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."

这个区分看似简单，但决定了架构选择的方向。笔者的判断是：**大多数团队应该从 Workflows 入手，只有当固定路径确实不够用时才走向 Agents。**

---

## 五大 Workflow 模式

### 1. Prompt Chaining（链式调用）

**结构**：任务分解为**顺序步骤序列**，每步 LLM 处理上一步的输出。

```
输入 → LLM1 → 门控检查 → LLM2 → 门控检查 → LLM3 → 输出
```

**适用场景**：
- 任务能干净地分解为固定子任务
- 需要在中间步骤做程序化检查确保流程正常
- 典型例子：写大纲 → 检查大纲 → 写正文

**工程要点**：在每个中间步骤加 "gate"（门控），检查输出是否符合预期，不符合就及时中断或调整。

---

### 2. Routing（路由）

**结构**：输入先经过分类器，决定走哪条专用路径。

```
输入 → 分类器 → 路由到专用 LLM/工具链
```

**适用场景**：
- 复杂任务有明确的分类，不同类别需要不同处理
- 优化某一类输入会影响其他类的表现，需要分离关注点
- 例子：客服分流（普通/退款/技术支持 → 不同流程）；大语言模型路由（简单问题 → Haiku，复杂问题 → Sonnet）

**工程要点**：分类可以由 LLM 自己做，也可以用传统分类模型，取决于准确率和成本权衡。

---

### 3. Parallelization（并行化）

**结构**：多个 LLM **同时**处理任务，结果按程序聚合。

两种变体：
- **Sectioning（分段）**：任务拆分为独立子任务并行执行
- **Voting（投票）**：同一任务跑多次获取多样化输出

**适用场景**：
- 子任务可并行以提升速度
- 需要多角度评估或多次尝试以获取高置信度结果
- 典型例子：代码审查（多个 prompt 从不同角度审查）；Guardrails（一个 LLM 处理请求，另一个同时做内容安全审查）

> "LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect."

**笔者判断**：Parallelization 是被低估的模式。很多团队习惯在一个 LLM call 里塞入所有考虑，但实际上拆开效果更好——这和人类一样，让专人做专事的效率高于让一个人同时处理多个维度。

---

### 4. Orchestrator-Workers（编排器-工作器）

**结构**：中央 LLM 动态分解任务，分配给工作 LLM，最后综合结果。

```
输入 → 编排器 LLM（动态决定子任务） → 多个工作 LLM 并行 → 综合 LLM → 输出
```

**关键特征**：子任务不是预定义的，而是**由编排器根据输入动态决定**。这和固定并行化的本质区别在于灵活性。

**适用场景**：
- 复杂任务，无法提前预测需要哪些子任务
- 典型例子：代码修改（需要改哪些文件、改什么，每个输入都不同）；多源搜索分析

**工程要点**：这是通往完全自主 Agent 的中间态。编排器负责「规划」，工作器负责「执行」，综合 LLM 负责「收口」。

---

### 5. Evaluator-Optimizer（评估器-优化器）

**结构**：一个 LLM 生成响应，另一个 LLM 在循环中提供评估和反馈。

```
LLM1 生成 → LLM2 评估 → 不满意？→ 反馈给 LLM1 重写 → 循环 → 满意 → 输出
```

**适用场景**：
- 有**明确的评估标准**
- 迭代优化能带来可衡量的价值
- 典型例子：文学翻译（初译 → 评估反馈 → 重译 → 循环）；复杂搜索（搜索 → 评估相关性 → 决定是否继续搜索）

> "This is analogous to the iterative writing process a human writer might go through when producing a polished document."

**工程要点**：这个模式和 Harness Engineering 中的「Stop Condition」设计高度相关——明确的评估标准就是 Stop Condition 的基础。

---

## Agents：从 Workflows 到完全自主

Anthropic 对 Agents 的定义：

> "Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement."

Agents 的核心能力（由 LLM 成熟度支撑）：
- 理解复杂输入
- 推理和规划
- 可靠地使用工具
- 从错误中恢复

**Agents 的典型实现**：

> "They are typically just LLMs using tools based on environmental feedback in a loop."

这就是 Harness Engineering 所说的 **Evaluator Loop** 的本质——Agent 在环境中执行动作，环境反馈给 Agent，Agent 根据反馈决定下一步。

**自主性的代价**：
- 更高的成本
- 错误可能叠加（compounding errors）
- 需要在沙箱环境中充分测试

**设计原则**：

1. **保持简洁**（Maintain simplicity）
2. **优先透明**（Prioritize transparency）——明确展示 Agent 的规划步骤
3. **精心设计 ACI**（Agent-Computer Interface）——工具文档和测试要到位

> "Carefully craft your agent-computer interface (ACI) through thorough tool documentation and testing."

笔者认为第三条是大多数团队最容易忽视的。工具的接口设计就是 Agent 的「操作系统 API」，设计得好不好直接决定了 Agent 能否可靠地完成复杂任务。

---

## 框架建议：何时用、何时不用

Anthropic 明确建议：

> "We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code."

提到的主流框架：
- Claude Agent SDK
- Strands Agents SDK (AWS)
- Rivet（拖拽式 GUI workflow builder）
- Vellum（GUI 工具）

框架的价值：
- 降低起步门槛
- 简化标准底层任务（LLM 调用、工具定义和解析、链式调用）

框架的风险：
- **增加额外抽象层**，可能掩盖底层的 prompts 和 responses，增加调试难度
- **容易让人过度工程**——明明更简单的方案就够用，却因为框架的便利性而过度设计

> "Incorrect assumptions about what's under the hood are a common source of customer error."

**笔者的判断**：框架是双刃剑。起步阶段用框架没问题，但必须持续问自己：「我是否真的需要这个抽象层？」到生产阶段，很多团队会发现裸 API 调用反而更容易控制和调试。

---

## 五大模式的关系图

```
Augmented LLM（基础构建块）
    ↓
┌───────────────────────────────────────────┐
│           Workflows（预定义路径）            │
│  Prompt Chaining → Routing → Parallelization │
│       Orchestrator-Workers                  │
│          Evaluator-Optimizer                │
└───────────────────────────────────────────┘
    ↓ （当灵活性确实不够时）
┌───────────────────────────────────────────┐
│         Agents（动态自主控制）               │
│  LLM 动态规划 + 工具 + 环境反馈循环         │
└───────────────────────────────────────────┘
```

---

## 关键工程洞察

### 1. 从简单开始，逐级增加复杂度

Anthropic 的核心建议：**不要一开始就用 Agent**。

```
单次 LLM 调用 + 检索 + 上下文示例
    ↓ （不够用时）
Workflows（预定义模式）
    ↓ （仍然不够用时）
Agents（完全自主）
```

### 2. 评估先行

> "The key to success, as with any LLM features, is measuring performance and iterating on implementations."

任何模式的选择都应该有数据支撑。定义清晰的评估标准，然后迭代。

### 3. 工具设计就是 API 设计

Anthropic 提出的 **ACI（Agent-Computer Interface）** 概念值得深入理解。工具的接口设计就是 Agent 与世界交互的界面，设计质量直接决定了 Agent 的可靠性。

---

## 原文引用

1. "Over the past year, we've worked with dozens of teams building large language model (LLM) agents across industries. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

2. "Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."

3. "The key to success, as with any LLM features, is measuring performance and iterating on implementations. To repeat: you should consider adding complexity only when it demonstrably improves outcomes."

---

## 下一步

Anthropic 的文章是关于 Workflow 模式的方法论层，下一步应该看这些模式在具体框架中如何实现。

**关联阅读**：
- [Anthropic Claude Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview) — SDK 层实现
- [ NousResearch/Hermes-Agent](../projects/nousresearch-hermes-agent-self-improving-agent-197k-stars-2026.md) — 一个实践了 Evaluator Loop + Skill 创建的 Agent 框架

---

*本文是对 Anthropic 工程博客的深度解读，原文版权归 Anthropic 所有。*
