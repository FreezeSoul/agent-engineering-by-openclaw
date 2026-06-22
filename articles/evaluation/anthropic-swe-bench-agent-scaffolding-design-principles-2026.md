# SWE-Bench 49% 背后：Anthropic 的 Agent Scaffolding 设计哲学

> 原文：[Claude SWE-Bench Performance](https://www.anthropic.com/engineering/swe-bench-sonnet)  
> 来源：Anthropic Engineering Blog  
> 收录：R494（2026-06-22）

---

## 核心命题

Claude 3.5 Sonnet 在 SWE-bench Verified 上达到 **49%**，首次逼近 50% 大关。但这篇 blog 的价值不在于这个数字本身，而在于 Anthropic 公开了他们做这个 benchmark 时使用的 **agent scaffold 设计哲学**：

> **给模型最大控制权，Scaffold 保持最小化。**

这个原则反直觉地有效——当社区普遍认为 agent 框架越复杂越好时，Anthropic 用最简 scaffold 打败了更重的方案。

---

## 一、重新理解 SWE-Bench 的本质

SWE-bench 不是在测模型，而是在测**整个 agent 系统**（模型 + scaffold 的组合）。

Anthropic 明确指出：

> "SWE-bench doesn't just evaluate the AI model in isolation, but rather an entire 'agent' system. The scaffolding is responsible for generating the prompts that go into the model, parsing the model's output to take action, and managing the interaction loop."

这意味着同一个模型，换不同的 scaffold，实现效果可以天差地别。社区已经多次验证了这一点——有人用同样的模型，通过优化 scaffold 把 SWE-bench 分数从 30% 拉到 40%+。

---

## 二、核心设计原则：最小化 Scaffold，最大化模型控制权

Anthropic 的 scaffold 只有三个组件：

1. **Prompt**：描述任务和通用方法论
2. **Bash Tool**：执行命令
3. **Edit Tool**：查看和编辑文件

没有：
- 复杂的 action 路由器
- 状态机或工作流引擎
- 多步骤强制流程
- 外部检索或 memory 机制

设计哲学原文是：

> "Give as much control as possible to the language model itself, and keep the scaffolding minimal."

模型的交互循环是：**采样直到模型决定结束，或达到 200k context 上限**。没有任何硬编码的步骤序列。

---

## 三、Prompt 设计的工程细节

### 通用方法论，而非具体指令

Anthropic 的 prompt 包含了**建议性的方法论**，而不是硬编码的步骤：

```markdown
Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo
2. Create a script to reproduce the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed
5. Think about edge cases and make sure your fix handles them
```

「might be a good idea」这个措辞是有意为之的——它给模型留出了「不按照这个步骤走」的空间，让模型根据实际情况自主决策。

### 工具描述是工程重点

Anthropic 花大量时间打磨的是**工具描述**（tool description），而不是 prompt 本身。他们测试了各种可能的模型误解场景，然后修改描述来预防这些问题。

Bash Tool 的描述包含了对模型来说至关重要的细节：
- 输入转义处理
- 无互联网访问
- 如何后台运行命令
- 状态在命令间是持久的

Edit Tool 的描述更复杂，包含了文件操作的所有边界情况。

Anthropic 的判断是：

> "We believe that much more attention should go into designing tool interfaces for models, in the same way that a large amount of attention goes into designing tool interfaces for humans."

**工具接口设计**（tool interface design）是一个被严重低估的工程维度。

---

## 四、SWE-Bench 的工程启示

### 1. 模型能力 vs Scaffold 能力的解耦

SWE-bench 揭示了一个关键事实：**模型能力和 scaffold 能力是独立的变量**。提升 agent 效果有两条路：

- 提升模型能力（scaling、architecture）
- 优化 scaffold（prompt engineering、tool design、interaction loop design）

Anthropic 的工作证明了第一条路还有很大空间（49% 还没到 50%），但第二条路同样重要。

### 2. Scaffold 复杂度是双刃剑

复杂 scaffold 的问题在于：

- 它会**限制模型的决策空间**，让模型无法根据实际情况灵活调整
- 它会**引入新的失败点**（scaffold bug）
- 它会**增加调试难度**（分不清是模型问题还是 scaffold 问题）

最小化 scaffold 的优势在于：
- 模型可以完全发挥其判断力
- scaffold 本身几乎不会引入 bug
- 失败模式清晰（要么模型能力不足，要么 prompt 描述不够清楚）

### 3. 评测即工程情报

SWE-bench 这类 benchmark 不只是用来「刷分」的，它是**工程情报来源**。通过分析哪些任务失败、为什么失败，可以得到大量关于模型能力和 scaffold 改进方向的信息。

---

## 五、49% 的意义：还没到拐点，但方向清晰

SWE-bench Verified 目前没有模型超过 50%。Anthropic 的 49% 是目前最高，但距离「实用」还有距离。

笔者认为，这个 benchmark 的意义更多在于**揭示工程方向**而非证明某种能力：

- 它告诉我们**最小化 scaffold 的设计哲学是可行的**
- 它告诉我们**工具描述的设计质量对最终效果影响巨大**
- 它告诉我们**模型在代码任务上还有很大提升空间**

下一步的突破点可能是：
1. 更强的模型能力（这是 Anthropic 的主赛道）
2. 更精细的工具描述工程
3. 在 scaffold 中引入 evaluation/feedback 机制（但需要小心不要让 scaffold 变得太重）

---

## 结论

Anthropic 在 SWE-bench 上的工作最重要的贡献不是那个 49% 的数字，而是他们公开的 **scaffold 设计哲学**：给模型最大控制权，Scaffold 保持最小化。

这个原则的核心洞察是：**Agent 的智能应该来自模型本身，而不是来自 scaffold 的复杂流程控制**。当 scaffold 开始「替模型做决定」的时候，它就开始限制模型的能力发挥了。

对于 Agent 框架设计者而言，这意味着：与其花时间构建复杂的工作流引擎，不如花时间打磨 prompt 和工具描述——后者对效果的影响往往更大。