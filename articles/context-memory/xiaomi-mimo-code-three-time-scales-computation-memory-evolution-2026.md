# Xiaomi MiMo Code：长时域 Agent 的三重时间尺度工程框架

> **核心论点**：MiMo Code 的最大贡献不是又一个"更好用的 coding agent"，而是一套将 Agent 可靠性问题分解为**三重时间尺度**的系统框架——计算（单步决策质量）、记忆（多轮状态连续性）、演化（跨会话经验蒸馏）。每个时间尺度都有对应的工程机制，而非用同一套方法处理所有问题。
>
> **金句**：当你的 agent 开始运行超过 10 轮时，"上下文不够"只是表象，真正的问题是**你还没有想清楚不同时间尺度需要不同的工程机制**。

---

## 背景：长时域任务的失效模式

传统的 coding agent 架构很简单：把语言模型放进一个运行时循环里，模型负责推理和决策，运行时管理工具、持久化状态、组装每一轮的输入。这套结构在短任务（通常少于 10 轮）上运作良好——对话历史本身就是充足的工作记忆。

但随着任务轮数增加，两个问题逐渐浮现：

**问题一：上下文窗口终将耗尽。** 无论窗口多大，几十轮的工具输出、代码片段、错误日志最终都会填满它。此时只能压缩或丢弃部分历史。简单的压缩方案（生成摘要替换丢弃内容）面临一个内在困境：类似 Mamba 这类循环模型的状态——有状态，但无法按需回看。真正需要的不是更好的压缩，而是一个**显式的存储-检索机制**，决定什么信息应该写入持久结构，以及何时应该被召回。

**问题二：即使窗口足够大，模型的指令遵循能力也随输入长度增长而下降。** 有用的约束和意图被大量工具输出稀释，模型越来越难提取"下一步该做什么"。

这两个问题的本质是：**不同时间尺度上，可靠性的瓶颈不同**。

---

## 三重时间尺度：MiMo Code 的核心框架

MiMo Code 团队观察到，最突出的瓶颈在不同时间尺度上差异明显：

| 时间尺度 | 可靠性瓶颈 | 对应工程机制 |
|---------|-----------|-------------|
| **单步决策**（一轮内） | 计算资源不足 | Computation（Max Mode + Goal）|
| **多轮连续性**（会话内） | 状态管理断裂 | Memory（持久状态架构）|
| **跨会话进化**（会话间） | 经验蒸馏机制缺失 | Evolution（跨会话学习）|

这套框架的价值在于：**它把一个模糊的"Agent 不够可靠"问题，拆解成了三个可独立工程化的问题**。

---

## 一、Computation：单步决策的质量扩展

当任务扩展到几十甚至上百步时，单步错误率会随时间累积，而 Agent 在长时域执行期间往往缺乏外部纠正信号。MiMo 的解法是在不同粒度级别投入额外计算资源以换取可靠性。

### 1.1 Max Mode：并行采样与选择

Max Mode 在每一轮并行生成 N 个候选解（N 默认设为 5）。每个候选独立完成推理和工具调用规划，但并不真正执行计划。然后用同一个模型作为评判者，比较所有候选的推理过程和行动方案，选择最佳者执行。

> "By default, temperature is set to 1, so five independent samples almost never produce identical results. If multiple candidates happen to converge, that itself indicates high confidence in that direction; when candidates differ significantly, having a low-temperature judge select the most robust plan is more reliable than depending on a single sample." — MiMo Code Blog

在 SWE-Bench Pro 上，Max Mode 相比单采样提升 10-20% 性能，代价是大约 4-5 倍的 token 消耗。

**关键洞察**：这不是简单的"多试几次"，而是一个**自路由的可靠性机制**——当候选收敛时说明方向高置信，当候选分歧时，低温 judge 选择最稳健方案比单样本更可靠。

Max Mode 和 Goal 是两个正交的 test-time compute 方向：Max Mode 是并行的，在同一 step 上花费 N 倍计算选择最优；Goal 是串行的，在同一任务内花费更多时间自检和继续执行。两者可以同时启用。

### 1.2 Goal：独立完成验证机制

Max Mode 解决的是"做对"的问题；Goal 解决的是"做完"的问题。

长任务中的一个常见失败模式是：Agent 在后续轮次看到之前的进展后，容易过早宣布"完成了"或"需要问一个问题"。这在自动化执行中尤其危险——没有人类在旁边纠正或提供反馈。

Goal 机制的工作方式：**由用户定义一个自然语言的停止条件**（如"所有测试通过且代码已提交"），每当 Agent 试图终止时，系统自动启动一个独立模型调用，审查完整对话历史，判断条件是否真正满足。如果没有满足，将具体差距反馈给 Agent 让其继续；如果确认任务不可能完成，则标记为不可能完成。

> "This verifier does not participate in the actual work, so it does not develop an alignment bias toward the parts the agent has already completed. Each time, it receives exactly the same context as the agent, including the actual tool outputs." — MiMo Code Blog

**关键设计**：这个 verifier 不参与实际工作，因此不会对 Agent 已完成的部分产生对齐偏见。每次它收到的上下文与 Agent 完全相同，包括实际工具输出。

### 1.3 工具调用语法：更少的 token，更少的错误

模型发出工具调用的格式直接影响准确率和 token 效率。MiMo 团队发现：
- 部分模型（尤其是 GPT-5.5 系列）在输出结构化 JSON 时格式化错误率较高
- XML 格式比 JSON 略好
- 受约束的命令行语法（constrained command-line syntax）token 效率最高，且格式化错误更少，因为大多数模型都在密集的 shell 环境数据上训练过

MiMo Code 的工具调用语法刻意设计为不支持管道、重定向或变量展开——借用 shell 的简洁性，而不是给模型一个不受控制的执行环境。

### 1.4 Dynamic Workflow：编排逻辑从提示词到代码

前面的机制解决的是单轮和单 Agent 级别质量问题。当任务规模大到需要协调数十甚至数百个并行工作单元时（如整个项目从一种编程语言迁移到另一种），逐轮工具调用就不够用了。

传统方案是把流程写入 SKILL.md，用自然语言告诉模型："先做 A，然后做 B，如果 C 发生就做 D"。这在简单场景有效，但在复杂工作流中系统性失效：上下文压缩可能吞掉步骤、模型可能跳过某些阶段、分支和重试逻辑依赖模型判断而非代码保证、同一工作流在两次运行中可能遵循不同执行路径。

**根本问题**：编排逻辑存在于自然语言中，而自然语言是模糊的、容易遗忘的、不可验证的。

Dynamic Workflow 把编排逻辑从提示词变成代码。主 Agent 生成一个 JavaScript 脚本，在隔离沙箱中确定性执行。脚本通过 `agent()` 分发子 Agent，通过 `parallel()` / `pipeline()` 控制并发——if 语句不会忘记分支，for 循环不会提前退出，barrier 不会漏掉子 Agent。模型的判断只用在该用的地方（理解并生成代码），而不是浪费在流程控制上。

> "Our implementation is compatible with the core semantics of Anthropic Dynamic Workflow, and extends it in several ways. The workflow() primitive allows scripts to call other scripts, so orchestration logic can be organized into reusable and composable building blocks." — MiMo Code Blog

**关键扩展**：
- `workflow()` 原语允许脚本调用其他脚本，编排逻辑可组织为可复用、可组合的构建块
- 每个 `agent()` 调用结果同步写入磁盘，允许进程从日志中断点恢复而非从头重跑
- 沙箱内可直接读写文件

---

## 二、Memory：多轮状态连续性

[MiMo Code Blog 在此处截断，以下内容基于 blog 提及的框架推断]

MiMo 框架中 Memory 主题的核心问题是：**如何让 Agent 在多轮会话中保持状态连续性，而不依赖无限增长的上下文窗口？**

从框架图中可以看出，Memory 层要解决的是"状态管理"——具体机制包括：
- **显式存储-检索机制**：不是更好的压缩，而是决定什么信息应该写入持久结构，以及何时应该被召回
- **状态持久化架构**：每个 `agent()` 调用结果同步写入磁盘，支持中断恢复
- **上下文压缩的正确姿势**：摘要替换的困境是有状态但无法按需回看，需要的是显式存储而非更好的压缩

---

## 三、Evolution：跨会话经验蒸馏

[内容基于 MiMo Code Blog 框架推断]

Evolution 主题处理的是跨会话尺度的可靠性问题。核心观察是：**改进跨会话表现的主要制约是经验蒸馏机制**。

这与 OpenAI 的 Dreaming 机制（让 ChatGPT 在后台"做梦"处理复杂查询）和 Anthropic 的"agents that learn across sessions"形成有趣的呼应——不同团队都在探索如何让 Agent **不只是执行，还能在执行中学到东西**。

---

## 工程意义：为什么三重时间尺度框架重要

笔者认为，MiMo Code 这套三重时间尺度框架的核心价值不是具体哪个机制（Max Mode、Goal、Dynamic Workflow），而是**它提供了一种分解问题的方式**。

当我们说"Agent 不够可靠"时，实际上可能是三种不同的问题：
- 单步决策质量不足 → 需要更多计算（Max Mode）
- 多轮状态断裂 → 需要更好的状态管理架构（Memory）
- 跨会话没有进步 → 需要学习/蒸馏机制（Evolution）

用同一套方法（更大的上下文窗口）试图解决所有三个问题，是方向性错误。

**真正的教训**：当你发现你的 Agent 在长任务中表现不好时，先问自己——**这是哪个时间尺度的问题？** 而不是直接去调模型或加上下文。

---

## 与现有工作的关联

| 相关工作 | 关联点 | 差异点 |
|---------|-------|-------|
| Anthropic Dynamic Workflow | 相同的核心理念（编排逻辑→代码） | MiMo 扩展了 workflow() 可组合性和中断恢复 |
| OpenAI Dreaming | 跨会话学习/经验蒸馏 | MiMo 框架更完整地覆盖三个时间尺度 |
| Hindsight (16K stars) | "agents that learn, not just remember" | Hindsight 专注 Memory 层；MiMo 是三层统一框架 |
| Claude Code | 长时域 coding agent | Claude Code 用更大的上下文；MiMo 用显式存储-检索机制 |

---

## 结论

MiMo Code 的三重时间尺度框架是 2026 年长时域 Agent 工程领域的一个重要贡献。它不是又一个"更好的 coding agent"，而是一套**问题分解框架**——把可靠性问题按时间尺度拆解，每个尺度有对应的工程机制。

核心判断：
1. **Computation 层**（Max Mode + Goal）代表了 test-time compute 的两个正交方向，值得在 harness 目录深入分析
2. **Dynamic Workflow** 体现了"编排逻辑从提示词到代码"的演进趋势，与 Anthropic Dynamic Workflow 兼容但有重要扩展
3. **三重时间尺度框架本身**是真正的知识贡献——它提供了一种诊断问题的思维方式，而不是又一套"万能解决方案"

真正的工程问题不是"模型不够强"，而是**我们还没有为不同时间尺度的问题设计对应的工程机制**。MiMo Code 正确地指出了这一点。

---

**引用来源**：
- [MiMo Code Blog: Scaling Coding Agents to Long-Horizon Tasks](https://mimo.xiaomi.com/blog/mimo-code-long-horizon)
- [GitHub: XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code)