# LangChain RubricMiddleware：让 Agent 自己知道"做得够不够好"

> **核心命题**：Self-Improving Agent 的核心工程机制不是"让模型更聪明"，而是**在模型外部建立独立的评估器循环**。LangChain 的 RubricMiddleware 提供了目前最完整的产品级实现。

---

## 一、问题：Agent 输出是概率的，但"完成标准"不是

Agent 系统有一个结构性矛盾：模型的输出是概率性的——同一条 prompt，这次可能通过，下次可能失败——而人类的任务目标通常是确定性的：测试通过 / 报告完整 / 邮件已发送。

当任务简单、上下文短时，这个矛盾不突出。但随着 context 增长，三种退化机制同时作用：

| 退化机制 | 表现 | 根本原因 |
|---------|------|---------|
| **指令漂移** | Agent 偏离了用户的原始意图 | 上下文过长时，关键指令被稀释 |
| **工具误用** | 调用了错误的工具或参数 | 复杂任务中工具选择的排列组合爆炸 |
| **非确定性累积** | 每一步的小错误级联放大 | 概率误差在长链路中复合 |

结果是：**开发者变成了人工质检员**——每次都要检查输出，不通过就重新跑任务。这种模式不可扩展。

---

## 二、解决方案：独立的评估器循环

LangChain 的回答是 RubricMiddleware（beta），其核心设计哲学是：

> **不要让 Agent 自己判断自己做得够不够好。让一个专门的 Grader Sub-Agent 来判断。**

这个思路不是 LangChain 独创的。让我们先看看行业里类似的设计：

| 系统 | 评估机制 | 评估粒度 | 工具能力 |
|------|---------|---------|---------|
| **Claude Code `/goal`** | 主模型自评 | 整体完成度 | 无工具 |
| **OpenAI Codex Tax Agents** | 三段式循环（执行→验证→修正）| 函数级 | 测试工具 |
| **LangChain RubricMiddleware** | Grader Sub-Agent | **逐条标准** | 可调用任意工具 |

Claude Code 的 `/goal` 机制是单次评估——模型自己判断是否完成，然后决定是否继续。Codex 的三段式循环更结构化，但没有统一的 rubric 标准。RubricMiddleware 的关键突破是：**评估维度被明确分解为可独立判断的 criterion，每条 criterion 有独立的 verdict**。

---

## 三、RubricMiddleware 架构解析

### 3.1 核心组件

```
User Request
    │
    ▼
┌─────────────────────┐
│   Deep Agent         │ ← 主执行 Agent（Claude Sonnet 4 等）
│   (执行任务)          │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  RubricMiddleware    │ ← 评估拦截层
│  ┌───────────────┐  │
│  │ Grader Sub-Agent│ ← 独立评估 Agent（可用更小的 Haiku）  │
│  │ 逐条判断 rubric │  │
│  └───────────────┘  │
└─────────────────────┘
    │
    ├─ ✅ 全部通过 → 结束
    └─ ❌ 部分失败 → 注入反馈 → 回到主 Agent 重新执行
```

### 3.2 三行代码接入

```python
from deepagents import RubricMiddleware, create_deep_agent
from langchain.messages import HumanMessage

# Step 1: 定义评估中间件
rubric_middleware = RubricMiddleware(
    model="anthropic:claude-haiku-4-5",   # Grader 可以用更便宜的模型
    system_prompt="You are a code reviewer grading generated code against a rubric.",
    tools=[run_test_suite],                  # Grader 可调用工具获取硬证据
    max_iterations=5,                        # 修复循环上限
)

# Step 2: 附加到 Deep Agent
agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt="You are a careful Python engineer...",
    middleware=[rubric_middleware],
)

# Step 3: 调用时传入 rubric
result = agent.invoke({
    "messages": [HumanMessage(content="Write find_duplicates(lst)...")],
    "rubric": (
        "- All tests pass in run_test_suite\n"
        "- The function is named `find_duplicates` and accepts a single list argument\n"
    ),
})
```

注意最后一行：**rubric 在调用时传入，而不是硬编码到系统提示里**。这意味着同一个 agent 可以被调用多次，每次用不同的验收标准——这是工程复用性的关键。

### 3.3 评估粒度：逐条 Criterion Verdict

这是 RubricMiddleware 与"简单重试"最核心的区别。

当 Agent 第一次尝试失败时，Grader 的输出不是泛泛的"再试一次"，而是：

> "One test fails: `test_unhashable`. The function crashes with TypeError when encountering unhashable types like lists within the input list."

每条 criterion 独立给出 verdict，Agent 因此**精确知道哪个点出了问题**，而不是在模糊的反馈里猜测。

---

## 四、为什么 Grader 能比主模型自评更好

这里有一个反直觉的设计决策：为什么不让主模型自己判断，而要单独起一个 Grader？

**因为判断"完成度"和执行任务是两种不同的认知模式。**

| 维度 | 主模型自评 | 独立 Grader |
|------|----------|------------|
| **注意力** | 执行任务时消耗注意力 | 100% 注意力在评估 |
| **工具有效性** | 无法实时验证输出 | 可以调用测试套件、lint 等工具 |
| **评判客观性** | 受"已经花了这么多力气"的偏差影响 | 与执行过程解耦，更客观 |
| **模型选择** | 必须用主模型 | 可以用更小/更便宜的模型 |

LangChain 默认推荐用 `claude-haiku-4-5` 作为 Grader——比主模型低 3 档，成本显著降低，但评估质量足够。**这是一个刻意设计的成本-质量权衡，不是技术限制。**

---

## 五、与其他 Self-Improvement 机制的对比

如果我们把"让 Agent 改进自己"作为一个连续谱，可以看到行业正在从不同方向收敛到这个模式：

```
简单重试
    ↓
Claude Code /goal（整体自评，单次）
    ↓
OpenAI Codex 三段式循环（执行→验证→修正，结构化）
    ↓
LangChain RubricMiddleware（逐条标准，工具化 Grader，循环迭代）
```

笔者认为，这个连续谱的演化方向是：**从"让 Agent 自己猜"到"让 Agent 在结构化反馈中精确修正"**。

RubricMiddleware 处于这个连续谱目前最成熟的产品实现点：它不只是一个 prompt 技巧，而是一个完整的工程框架——中间件模式、工具化评估、逐条 verdict、迭代上限控制。

---

## 六、工程实践中的关键设计决策

### 6.1 Rubric 怎么写才有效

Rubric 的质量直接决定评估的有效性。LangChain 文档的建议是：**每条 criterion 应该是可验证的，而非抽象的**。

❌ 低质量 rubric：
```
"- The code is correct
- The code is readable"
```

✅ 高质量 rubric：
```
"- All tests pass in run_test_suite
- The function is named `find_duplicates` and accepts a single list argument
- No TypeError or ValueError raised for edge cases (empty list, single element, duplicates)"
```

核心区别：高质量 rubric 的每条都可以被工具或明确的检查验证，而不只是"看起来对"。

### 6.2 Grader 工具选择

Grader 可以调用的工具是 RubricMiddleware 威力最大的部分。典型选择：

| 工具 | 适用场景 | 价值 |
|------|---------|------|
| `run_test_suite` | 代码生成任务 | 硬证据，不依赖主观判断 |
| `lint/format` | 代码质量检查 | 自动化的风格一致性 |
| `validate_output` | 结构化输出（如 JSON）| 格式验证 |
| 无工具 | 开放性任务 | 纯推理评估 |

笔者认为：**优先给 Grader 配工具**。当 Grader 可以调用测试套件时，它的 verdict 就是基于真实运行结果，而不是猜测。这将"评估"从软技能变成硬验证。

### 6.3 循环终止条件

RubricMiddleware 有四个终止条件：

```
satisfied      → 全部 criterion 通过，结束
max_iterations → 达到迭代上限，结束（可能部分通过）
failed         → Grader 判断无法通过（即使继续迭代也无效）
grader_error   → Grader 自身出错，安全降级
```

这里有个重要的工程决策点：**max_iterations 应该设多少？** LangChain 默认不设置（意味着无限循环直到 satisfied），但建议明确设置以控制成本。笔者的建议是：

- 代码生成类任务：3-5 次（通常 2-3 次就能收敛）
- 开放性写作任务：2-3 次（更多迭代边际收益递减）
- 复杂研究任务：5-10 次（长链任务需要更多修正轮次）

---

## 七、与 2026 年框架收敛的横向呼应

RubricMiddleware 不是 LangChain 独有的创新。它反映的是 2026 年所有主流 Agent 框架都在做的事情：**把评估从隐性的"模型自己判断"变成显性的"工程化反馈循环"**。

| 框架 | 评估机制 | 关联点 |
|------|---------|-------|
| **Claude Code** | `/goal` 整体自评 | 单次评估，非迭代 |
| **OpenAI Agents SDK** | Handoffs + Guardrails | 路由与安全，非自我修正 |
| **Google ADK 2.0** | 图执行引擎的条件边 | 状态机条件判断，非逐条 rubric |
| **CrewAI** | 1.7B 工作流数据支撑的确定性骨架 | 架构层面，非执行层面 |
| **LangChain Deep Agents** | RubricMiddleware | ⭐ **最完整的 evaluator loop 实现** |

值得注意的是，Claude Code 的 `/goal` 和 RubricMiddleware 本质上是同一个模式的两种实现——**区别在于评估的粒度和是否有工具支撑**。随着 Agent 进入生产环境，这种 evaluator loop 正在从"实验性技巧"变成"标准工程组件"。

---

## 八、结论：Self-Improvement 的工程化拐点

RubricMiddleware 的发布意味着 Agent 的 Self-Improvement 机制正在经历一个拐点：

> **从"让模型自己反思"（软技能）进化到"结构化的评估-修正循环"（工程组件）。**

这个拐点的重要信号是：
1. **评估器独立为 Sub-Agent**：不再是主模型的附庸，而是有自己工具和指令的独立组件
2. **逐条 Criterion Verdict**：评估粒度从"整体通过/失败"细化到"每条标准独立判断"
3. **工具化 Grader**：评估从纯推理变成硬验证（测试套件、lint 等）
4. **中间件模式**：评估逻辑与执行逻辑解耦，可插拔、可复用

对于构建生产级 Agent 系统的工程师来说，这意味着：**不要依赖模型的自省能力来保证输出质量，而是要在架构层面建立独立的评估器循环**。这是让 Agent 系统真正可靠的最后一块工程短板。

---

**引用来源**：
- [Introducing Rubrics: Build Agents that Evaluate and Correct Their Work](https://www.langchain.com/blog/introducing-rubrics-for-deepagents)（LangChain 官方博客，2026-06-02）
- [Deep Agents Rubric 文档](https://docs.langchain.com/oss/python/deepagents/rubric)
- [Claude Code /goal 文档](https://code.claude.com/docs/en/goal)（Claude Code，2026）
