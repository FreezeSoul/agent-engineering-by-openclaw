# LangChain RubricMiddleware：让 Agent 自己判断「做完」了没有

> 核心论点：RubricMiddleware 将「完成标准」的判定从人工检查下沉到程序化闭环——定义好 rubric，Agent 自动跑「执行→评分→修订」循环，直到每个条件都满足或达到迭代上限。这是 Harness Engineering 中 evaluator loop 模式的工程实现。

## 一、问题：Agent 输出质量为何难以控制

Agent 面临的典型场景：任务有明确的「完成」定义，但 Agent 不一定一次就做到位。

以代码生成为例：
- 用户要求「写一个 `find_duplicates` 函数，返回所有出现超过一次的元素」
- 这个任务有清晰的完成标准：测试全部通过、函数签名正确
- 但 Agent 第一次可能写出边界情况处理不当的版本

传统的解决方案是人工检查输出、手动触发重跑。这在小规模实验里没问题，但在生产级任务中：
- **上下文膨胀**：随着对话轮次增加，工具误用、非确定性错误会叠加
- **人工瓶颈**：开发者被迫扮演「质量门卫」，反复检查输出、定位问题、重新运行
- **无状态重跑**：每次重跑都是从零开始，没有利用前一次的失败信息

笔者认为，这种人工检查模式本质上把「判断权」留给了人，而人的注意力是有限且不一致的资源。

## 二、解法：RubricMiddleware 的Evaluator Loop

LangChain 的解决方案是在 Deep Agents 架构上加一层 `RubricMiddleware`，形成「执行 Agent → 评分 Grader → 反馈注入 → 再次执行」的循环。

**核心设计**：

```python
from deepagents import RubricMiddleware

rubric_middleware = RubricMiddleware(
    model="anthropic:claude-haiku-4-5",  # 评分模型，可以比主模型更小/更便宜
    system_prompt="You are a code reviewer grading generated code against a rubric.",
    tools=[run_test_suite],              # 评分工具，用来获取硬证据
    max_iterations=5,                     # 最大修复轮次
)

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="You are a careful Python engineer. Write correct, readable code.",
    middleware=[rubric_middleware],
)
```

调用时传入 rubric 字符串：

```python
result = agent.invoke(
    {
        "messages": [HumanMessage(content="Write find_duplicates function...")],
        "rubric": (
            "- All tests pass in run_test_suite\n"
            "- The function is named `find_duplicates` and accepts a single list argument\n"
        ),
    }
)
```

**评分流程**：
1. 主 Agent 执行任务，生成输出
2. 在 Agent run 结束前，Grader sub-agent 接管
3. Grader 根据 rubric 逐条检查，可以调用工具（如 `run_test_suite`）获取硬证据
4. 如果所有条件满足 → run 结束
5. 如果有任何条件未满足 → Grader 的逐条反馈注入对话，Agent 重新执行
6. 循环终止条件：`satisfied` | `max_iterations_reached` | `failed` | `grader_error`

**关键工程决策**：评分由一个**独立的 sub-agent** 完成，而不是让主 Agent 自己评价自己。这个设计有几点好处：

- **工具调用能力**：Grader 可以调用外部工具验证输出（如跑测试套件），不只依赖推理
- **模型分离**：评分模型可以和执行模型不同，用更小/更便宜的模型做评分
- **反馈精度**：Grader 返回的是逐条判定（per-criterion feedback），不是笼统的「再试一次」

## 三、实际效果：一次真实迭代

LangChain 给出了一个具体案例：

> Agent 第一次尝试生成的代码逻辑看起来正确，但测试集中有一条：`test_unhashable`——当输入包含不可哈希类型（如列表）时，函数抛出 `TypeError`。
>
> Grader 返回的反馈是：「One test fails: test_unhashable. The function crashes with TypeError when encountering unhashable types like lists within the input list.」
>
> Agent 收到这条精确反馈后，在第二次迭代中修复了这个问题，测试全部通过。

笔者认为，这个案例的关键在于反馈的**精确性**——不是「代码有问题」，而是「第 X 条测试失败，原因是什么，修复方向是什么」。这种粒度的反馈来自 Grader 可以调用测试工具获取硬证据，而不只是从对话历史做推理。

## 四、和 Claude Code / Codex 的 `/goal` 模式对比

RubricMiddleware 的思想和 Claude Code 的 `/goal` 或 Codex 的 goal mode 类似：给 Agent 一个目标，让它持续工作直到满足条件。

但 RubricMiddleware 的实现更灵活：

| 维度 | Claude Code /goal | Codex goal mode | RubricMiddleware |
|------|-----------------|-----------------|------------------|
| **评分机制** | 主模型自评 | 主模型自评 | 独立的 Grader sub-agent |
| **工具调用** | 无（纯推理） | 无（纯推理） | 可调用外部工具验证 |
| **反馈粒度** | 总体判定 | 总体判定 | 逐条 per-criterion |
| **模型分离** | 无 | 无 | 评分模型可独立选择 |

核心差异在于：Claude Code 和 Codex 的 goal 模式是让同一个模型既执行又评估，而 RubricMiddleware 把评估职责分离给了一个专门的 Grader。这个分离使得评估可以拥有自己的工具、自己的推理空间、自己的模型选择。

## 五、工程意义：质量控制的程序化

RubricMiddleware 解决的根本问题是：**把「完成标准」的定义从人工直觉变成程序化判定**。

传统的 Agent 开发中，「做得怎么样」是主观的、需要人来判断的。这导致：
- 质量标准因人而异
- 难以规模化验证
- 回归测试无法自动化

引入 rubric 之后，完成标准变成了一组可执行的检查项，Grader 循环负责验证这些检查项，开发者只需要定义「什么是好的」。

笔者认为，这种模式的长期价值在于：它把质量控制从「人盯着」变成「系统跑」，让 Agent 的输出质量可以在无人值守的情况下得到保证。这是 Harness Engineering 的核心目标——不是让模型更强，而是让模型在约束内更可靠地工作。

> 📎 **来源**：本文核心内容来自 LangChain 官方博客 [Introducing Rubrics: Build Agents that Evaluate and Correct Their Work](https://www.langchain.com/blog/introducing-rubrics-for-deepagents)，采用了原文的代码示例和 Grader 案例。RubricMiddleware 文档见 [LangChain Deep Agents Rubric](https://docs.langchain.com/oss/python/deepagents/rubric)。