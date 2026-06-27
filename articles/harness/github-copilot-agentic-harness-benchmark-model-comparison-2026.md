# GitHub Copilot Agentic Harness 基准测试：Harness 设计比模型选择更重要

> 来源：[Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks](https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)，GitHub Blog，2026-06-25

## 核心命题

GitHub 官方发布了一份系统性基准测试报告，核心结论反直觉：**在固定模型和任务的前提下，GitHub Copilot 的 agentic harness 与 Claude Code、Codex CLI 等模型厂商原生 harness 相比，任务完成率持平，但 token 消耗更低**。这意味着 **harness 的工程设计本身就能直接决定成本和效率，模型不是唯一的瓶颈**。

笔者认为，这个结论对整个行业都有深远影响：当我们讨论"哪个模型更强"时，往往忽略了 harness 这个关键的中间层——它才是让模型能力真正落地的工程载体。

## 为什么这个话题值得写

过去一年，Agent 系统的对比评测大多围绕"模型能力"展开：Claude 强在推理、GPT 强在代码、 Opus 强在复杂任务……但很少有人系统性地对比 **harness 这一层**——同样的模型，换一个 harness 实现，效率可能差 30% 以上。

GitHub 这篇文章的意义在于：**第一次由头部厂商用控制变量法证明了 harness 的独立价值**。这不是在吹捧 Copilot，而是通过严谨的实验设计揭示了一个被长期忽视的工程事实。

## GitHub Copilot Agentic Harness 是什么

根据官方定义，GitHub Copilot 的 agentic harness 是 SDK 中的单一共享组件，负责编排工具调用、上下文管理和工作流：

> "While the model provides the raw intelligence, the harness shapes how effectively that intelligence is applied."

这个 harness 驱动了 GitHub Copilot CLI、GitHub Copilot App、Copilot code review，以及 GitHub 和 Microsoft 内部的大量产品体验。官方明确指出：**改进 harness，所有产品线同时受益**。

## 实验设计：如何公平地对比 Harness

这是本文最有工程价值的方法论部分。GitHub 采用了严格的控制变量：

- **固定模型**：同一模型（如 Claude Sonnet 4.6）在不同 harness 下对比
- **固定任务**：相同 benchmark 任务
- **标准化上下文窗口**
- **标准化推理投入（reasoning efforts）**
- **标准化工具选择和 MCP server**

对比对象：
- Claude Code（Harness 模式）vs GitHub Copilot CLI
- Codex CLI vs GitHub Copilot CLI

笔者认为，这种"模型不变、harness 变"的设计是评测 harness 性能的正确姿势——大多数竞品对比做不到这一点，往往是"模型+harness 打包"一起比，然后宣称"我们的模型最强"。

## 评测基准：5 个维度

| 基准 | 领域 | 用途 |
|------|------|------|
| **SWE-bench Verified** | 500 个人类验证的 bug-fix 任务 | 行业标准 coding agent 基准 |
| **SWE-bench Pro** | 更难的多步工程任务，需要更深推理 | 反映复杂真实软件工程工作 |
| **SkillsBench** | Agent 使用技能解决问题的能力 | 评估可扩展性和技能触发机制 |
| **TerminalBench** | 命令行工作流中的 Agent 表现 | 衡量开发者日常终端使用场景 |
| **Win-Hill** | Windows 容器内任务 | 验证跨操作系统泛化能力 |

## 核心发现 1：Token 效率

**结论：GitHub Copilot harness 在大多数配置下达到与其他 harness 同等任务完成率，但 token 消耗更低。**

这背后的工程含义是：harness 对上下文的管理方式（是否冗余、是否压缩、是否有效利用工具返回）直接决定了 token 消耗量，而这直接关联到成本。

## 核心发现 2：TerminalBench 的方差分析

这是笔者认为整篇文章最有洞察的部分。GitHub 发布了 TerminalBench 2.0 的详细 run-to-run 方差分析图，横轴是单任务成本，纵轴是解决率，每个点是一个"agent+model"配置，椭圆表示 ±1σ 的运行间波动范围。

三个关键观察：

1. **Copilot harness 在任务完成率和成本两个维度都与竞品持平或领先**：紫色（Copilot）标记与同模型竞品在两个轴上都有重叠的椭圆——差异在运行间方差范围内。Copilot 从未在完成率上低于竞品，也从未在成本上高于竞品。

2. **运行间方差（run-to-run variance）才是真正的差异点**：这不是模型性能差异，而是 harness 对随机性的处理能力。方差越大，意味着每次运行的结果越不可预测，对于生产环境来说是严重的问题。

3. **大模型确实更可靠，但成本更高**：图表显示 GPT-5.5 和 Opus 4.7 在右上角（高完成率、高成本），但 Copilot harness 能让这些大模型的每任务成本更有竞争力。

## 关键工程判断

笔者认为，GitHub 这篇文章揭示了三个被行业低估的事实：

**1. Harness 是独立的工程变量，不应该被模型选择掩盖**

大多数技术选型讨论停留在"用 Claude 还是 GPT"这个层面。但 GitHub 的数据表明，在模型固定的情况下，换一个 harness 实现就能显著改变成本和可靠性。这意味着企业在评估 Agent 方案时，应该把 harness 质量作为独立的评估维度。

**2. Token 效率不等于节省成本，而是工程成熟的标志**

Token 消耗低通常被理解为"省钱"，但更深层的含义是：harness 对上下文的压缩和复用做得好，不会在每轮对话中冗余地传递历史数据。这在长任务场景下（Agent 工作流通常持续数十分钟到数小时）是决定性的。

**3. 方差分析与均值同等重要**

GitHub 没有只报平均分，而是展示了每个配置的运行间方差。这个细节体现了工程思维：对于生产级 Agent 系统，"平均成功率 85%"可能不如"99% 的运行落在 83%-87% 之间"可靠。方差决定了 SLA 的可承诺性。

## 局限性

笔者认为这篇文章也有值得关注的局限：

1. **对比范围有限**：只对比了 Claude Code 和 Codex CLI，没有对比 LangChain Agent、CrewAI 等第三方框架的 harness
2. **Benchmark 的代表性**：SWE-bench Verified 只有 500 个任务，是否足以代表真实生产环境中的复杂分布？
3. **厂商自测**：数据由 GitHub 自行测量和发布，缺乏第三方独立复现

## 适用场景与不适用场景

**适用**：
- 评估 Agent 方案时，应该把 harness 效率作为独立维度
- 在模型选型后，关注该模型在不同 harness 下的 token 消耗差异
- 生产环境需要关注 run-to-run 方差，而非只看平均成功率

**不适用**：
- 这不是"Copilot 比 Claude Code 强"的证明——harness 只是其中一个变量
- 不能直接推广到非代码场景（benchmark 主要覆盖 coding 和 terminal 任务）

## 结语

GitHub 这篇文章的核心贡献不是证明 Copilot harness 最强，而是**用严谨的实验设计证明了 harness 这个工程层本身就是一种竞争力**。对于构建 Agent 系统的工程师来说，这个结论意味着：与其一味追逐更大参数的模型，不如先审视自己的 harness 设计是否足够高效。

真正的 Agent 工程，不只是在模型层做选择，更是在 harness 层做权衡。

---

**引用来源**：
- "While the model provides the raw intelligence, the harness shapes how effectively that intelligence is applied." — GitHub Blog, 2026-06-25
- "Improve the harness, and every surface benefits." — GitHub Blog, 2026-06-25
- TerminalBench 2.0 variance analysis, GitHub Copilot agentic harness benchmark