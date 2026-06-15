# Trace 是 AI Agent 时代的新源代码——论可观测性重写调试范式

> 本文解读自 LangChain 官方博客 *In software, the code documents the app. In AI, the traces do.*  
> 原文链接：https://blog.langchain.com/in-software-the-code-documents-the-app-in-ai-the-traces-do/

---

## 核心命题

传统软件中，代码是唯一真实的信息源（source of truth）：调试读代码，优化读代码，理解功能读代码。

但在 AI Agent 系统中，代码只是**脚手架**，真正的决策发生在模型运行时刻。你无法通过读代码知道 agent 会做什么——因为决定"做什么"的不是代码，是模型。

> **笔者认为**：这是 AI Agent 工程化与传统软件工程最根本的分叉点。一旦理解这个转变，就会明白为什么传统调试手段在 agent 场景下几乎失效，以及为什么可观测性（observability）不再是"锦上添花"而是"核心基础设施"。**

---

## 为什么代码不再等于行为

看一个典型的 agent 代码：

```python
agent = Agent(
    model="gpt-4",
    tools=[search_tool, analysis_tool, visualization_tool],
    system_prompt="You are a helpful data analyst..."
)
result = agent.run(user_query)
```

代码定义了组件：用什么模型、什么工具、什么指令。但真正的执行逻辑不在这里——它在模型内部运行。

**同一段代码、同一个输入，两次运行可能产生完全不同的输出。** 不同的 tool call、不同的推理链、不同的结果。代码只能保证"orchestration 层"（tool calling、parsing）的正确性，无法保证"智能层"（决策质量、推理有效性）的正确性。

这不是 bug，是设计假设的改变。传统软件是确定性的，AI agent 是概率性的。代码管不了的决策，必须换一套机制来管。

---

## Trace：替代代码成为新的真实信息源

LangChain 提出了一个关键命题：**trace 是 AI agent 时代的源代码**。

A trace 是 agent 执行过程中完整的行为序列——每一步的推理、tool call 的选择与参数、返回值、耗时。**它记录的不是"代码说了什么"，而是"agent 实际做了什么以及为什么"。**

这个定义意味着：传统软件中在代码层面做的所有操作——调试、测试、优化、监控——在 AI Agent 时代都必须转移到 trace 层面。

| 操作 | 传统软件 | AI Agent |
|------|---------|---------|
| 调试 | 读代码，设断点 | 分析 trace，还原决策路径 |
| 测试 | 跑单元测试，验证输出 | 构建 eval 数据集，评估 trace 质量 |
| 性能优化 | Profiling 代码 hot loop | 分析 trace 中的决策模式 |
| 监控 | 盯错误率和 uptime | 追踪任务成功率、推理质量、tool 使用效率 |
| 协作 | GitHub PR review | 在 observability 平台上对 trace 打标讨论 |

**关键洞察**：传统软件中"代码"和"行为"是同一件事的两面（同一份源文件），AI Agent 中它们彻底分离了。代码定义了边界条件，trace 才是实际发生的事。

---

## 调试范式的根本转移

### 你无法在推理层设断点

传统软件找到 bug 后，在对应代码行设断点，单步执行，还原现场。

AI Agent 中，决策发生在模型内部——你无法在模型的 forward pass 里设断点。

但你可以在**逻辑层**设断点：用 trace + playground。打开某个特定时刻的 trace，还原当时的状态：agent 看到了什么上下文、内存里有什么、可用工具是什么、prompt 是什么。然后在 playground 里迭代——改 prompt、调上下文、换策略——看 agent 是否做出更好的决策。

> **笔者认为**：Playground 在 AI Agent 调试中的角色，等价于 IDE 断点调试在传统软件开发中的角色。但本质上要解决的是同一个问题：**在决策发生之前获得干预的能力**。

### 测试变成 Eval 驱动

传统软件测试：输入 → 运行代码 → 验证输出是否符合预期。

AI Agent 测试：
1. **建立 trace 数据集**：捕获真实运行中的 trace，积累到测试数据集
2. **持续 Eval**：对数据集运行 agent，评估 trace 质量（不只是对错，而是决策质量）

这种模式的转变源于 agent 的非确定性：同一输入可能多次运行产生不同输出，所以你不能依赖单次测试结果。必须依赖**统计意义上的质量评估**——这正是 eval 框架（如 LangSmith、OpenAI Evals）的核心价值。

### 生产监控从"存活率"转向"质量"

一个 agent 可以"在线"（0 errors）但实际表现极差：完成了错误的任务、以 10 倍低效完成正确任务、或给出了正确但无用的答案。

监控维度必须改变：

```
传统监控：系统是否报错
Agent 监控：任务是否成功 → 推理质量 → Tool 使用效率 → 成本合理性
```

LangChain 指出：**质量监控离不开对 trace 的采样和分析**。没有 trace 采样，所谓的监控只是自我欺骗。

---

## 从代码协作到 Trace 协作

传统软件的协作发生在 GitHub：review 代码、PR 评论、issue 讨论。代码是所有人共同操作的 artifact。

AI Agent 时代，逻辑不在代码里，在 trace 里。所以协作也必须在 trace 层面发生：

- Debug agent 为何做出错误决策 → 分享 trace，在特定决策点打标讨论
- 产品分析用户行为 → 分析 agent trace 序列，理解用户意图与 agent 响应的匹配度
- Prompt 优化 → 对比优化前后的 trace 差异，而非对比代码 diff

**这意味着 observability 平台不再只是监控工具，而是协作平台。** 这是与传统软件开发完全不同的工具链演进方向。

> **笔者认为**：未来 2-3 年，会出现一批专门针对 AI Agent trace 协作的工具，类比 GitHub 在代码协作中的地位。LangChain 已经在朝这个方向走，但这个领域目前仍然极度缺乏工程化深度。

---

## 为什么这个转变对 Agent 工程师至关重要

理解"代码 ≠ 行为"这个范式转变，是区分"会用 LangChain"和"真正理解 Agent 工程"的分水岭。

**实践中，这意味着**：如果你在构建 agent，只写代码远远不够。你必须同时构建：

1. **Trace 采集基础设施**：自动记录每个 agent run 的完整 trace
2. **Eval pipeline**：将 trace 转化为可量化的质量信号
3. **Playground 调试能力**：支持在任意历史 state 下重放和迭代
4. **Trace 分析工作流**：让团队能够对 trace 打标、讨论、归类

没有这四样东西，你的 agent 系统是"黑盒运行，出了问题靠猜"的状态。

---

## 结论

LangChain 提出的核心命题值得每个 Agent 工程师记住：

> **代码是传统软件的 source of truth。Trace 是 AI Agent 时代的 source of truth。**

这不是比喻，而是工程实践的真实转变。理解这一点，才能理解为什么可观测性在 agent 系统中不是"附加功能"而是"核心基础设施"——就像代码是传统软件的核心一样。

下一个问题：**你的 agent 系统，有完整的 trace 基础设施吗？**

---

**关联项目**：本文分析的 Trace-as-Document 范式，需要强大的 Eval 框架支撑。OpenAI Cookbook 的 *Agent Improvement Loop* 展示了如何用真实 trace + human/model feedback 构建可持续改进的 agent harness，详见：[openai-agents-sdk-agent-improvement-loop-trace-eval-codex-2026.md](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/deep-dives/openai-agents-sdk-agent-improvement-loop-trace-eval-codex-2026.md)

---

*本文来源：LangChain 官方博客（2026）*  
*引用原文 3 处：trace 定义、playground-as-debugger 类比、observability-as-collaboration 命题*