# 传统软件看代码，AI Agent 看 Tracing——论可观测性的范式转移

> **核心论点**：当 Agent 的决策逻辑不再存在于代码中，而存在于模型的运行时推理中，传统的"代码即文档"范式彻底失效。Tracing 成为了 AI Agent 的新"源代码"——它是唯一记录了 Agent 真正做了什么、为什么这样做的证据。
>
> **工程机制稀缺性**：⭐⭐⭐（行业稀缺的认知框架）——这个论点触及了 AI Agent 与传统软件最根本的范式差异，是所有上层工程实践的底层认知基础。

## 一、范式断裂：代码为什么不再记录行为

在传统软件中，代码是唯一的事实来源（Single Source of Truth）。

你想知道"用户提交表单时发生了什么"？打开 `handleSubmit()` 读函数。决策逻辑就在那里：验证输入、检查认证、调用 API、处理错误。确定性的——同样的输入，同样的代码路径，同样的输出。

**但在 AI Agent 中，代码只是脚手架。**

```python
agent = Agent(
    model="claude-sonnet-4",
    tools=[search_tool, analysis_tool, visualization_tool],
    system_prompt="You are a helpful data analyst..."
)
result = agent.run(user_query)
```

你定义了组件：用哪个模型、哪些工具、什么指令。但决策逻辑不在代码里——它只是编排 LLM 调用。

真正的决策——何时调用哪个工具、如何推理问题、何时停止、优先什么——全部发生在模型运行时的黑箱里。

> 💡 **关键洞察**：随着 LLM 驱动越来越多的应用逻辑，你仅通过看代码越来越难以预测应用实际会做什么。

## 二、Tracing 成为新的"源代码"

那么，Agent 的实际行为记录在哪里？**在 Tracing 里。**

Trace 是 Agent 执行步骤的序列。它记录了应用的逻辑——每一步的推理、调用了哪些工具及原因、执行结果和耗时。

```
[Step 1] Tool: search_tool
  Input: "latest AI agent framework benchmark 2026"
  Output: [17 results]

[Step 2] Reasoning: "The user wants to compare frameworks.
  I should use the analysis_tool to structure this comparison."
  Tool: analysis_tool
  Input: {comparison维度: ["stars", "architecture", "use cases"]}
  Output: {structured comparison}

[Step 3] Reasoning: "Good analysis. Now I should
  create visualizations to make this clearer."
  Tool: visualization_tool
  ...
```

**这意味着你在传统软件中对代码做的所有操作——调试、测试、性能分析、监控——在 AI Agent 时代都需要转移到 Tracing 上执行。**

> 💡 **操作平移**：传统软件中你在代码上做的操作，在 AI Agent 时代需要在 Trace 上做。

## 三、具体工程影响

### 3.1 调试变成 Trace 分析

当用户报告"Agent 失败了"，你不打开代码找 bug。你打开 Trace 找推理哪里出了问题：Agent 是否误解了任务？调用了错误的工具？陷入了循环？

**Bug 不是代码中的逻辑错误，而是 Agent 实际行为中的推理错误。**

实例：Agent 重复重试同一个失败的 API 调用 5 次才放弃。你的重试逻辑代码没问题——Bug 是 Agent 没有从错误信息中学习。你只能在 Trace 中看到这个问题：同样的工具调用、同样的参数、同样的失败、重复出现。

### 3.2 你无法在推理中设置断点

在传统软件中，发现 bug 后你在代码中设置断点。

在 AI Agent 中，你无法在推理中设置断点——决策发生在模型内部。

**但你可以在逻辑中使用 Trace + Playground 设置断点。** 在某个时间点打开 Trace——就在 Agent 做了错误决策之前。将那个状态加载到 Playground。Playground 就像是调试器，但调试的是推理而不是代码。

你能看到：Agent 有什么上下文？内存里有什么？有哪些可用工具？Prompt 长什么样？然后迭代——调整 Prompt、更改上下文、尝试不同方法——看 Agent 是否做出更好的决策。

### 3.3 测试变成 Eval-Driven

由于逻辑的事实来源转移到了 Trace，你需要对 Trace 进行测试。这意味着两件事：

**第一：建立 Trace 测试数据集管道。** 当 Agent 运行时，捕获 Trace 并将其添加到测试数据集中。你的测试套件变成了"已知好的 Trace 集合"。

**第二：用 Eval 判断行为质量。** 传统软件测试用 assert 验证输出——Agent 测试用 Eval 验证推理质量。同样的输入和代码可能产生不同输出（不同的工具调用、不同的推理链、不同的结果）。理解发生了什么唯一的方法是看 Trace。

## 四、这个认知框架为什么重要

LangChain 这篇文章的核心贡献不是技术细节，而是一个认知框架：**在 AI Agent 时代，Tracing 不是"可选项"而是"事实来源"**。

这意味着：

| 传统软件 | AI Agent |
|---------|----------|
| 代码是事实来源 | Trace 是事实来源 |
| 调试 = 读代码 | 调试 = 分析 Trace |
| 测试 = 验证输出 | 测试 = Eval 验证推理质量 |
| 监控 = 日志分析 | 监控 = Trace 流分析 |
| 文档 = 代码注释 | 文档 = Trace 历史 |

> 💡 **真正的工程含义**：如果你在构建 Agent 时没有好的可观测性，你缺失的是系统实际在做什么的事实来源。你在盲目飞行。

## 五、实践启示

1. **从第一天起构建 Tracing**：不要等上线后再加可观测性。Tracing 是你理解 Agent 实际行为的唯一窗口
2. **建立 Trace 即文档的文化**：当团队讨论"Agent 做了什么"时，对话的起点应该是 Trace 而不是代码
3. **投资 Eval 基础设施**：用已知好的 Trace 构建测试数据集，用结构化 Eval 验证推理质量
4. **Playground 即调试器**：在本地复现问题场景，加载问题时刻的完整状态，迭代调试

**行业背景**：根据 LangChain 的 [State of Agent Engineering](https://www.langchain.com/state-of-agent-engineering) 报告，89% 的组织已为 Agent 实现某种形式可观测性，62% 有详细 Tracing 可检查单个 Agent 行为。这意味着可观测性不再是差异化优势，而是基础要求。

---

**引用**：
- LangChain Blog: "In software, the code documents the app. In AI, the traces do." ([langchain.com](https://blog.langchain.com/in-software-the-code-documents-the-app-in-ai-the-traces-do))
- LangChain State of Agent Engineering Report 2026