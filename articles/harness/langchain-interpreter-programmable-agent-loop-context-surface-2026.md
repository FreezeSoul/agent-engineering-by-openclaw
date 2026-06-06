# LangChain Interpreter：把 Agent Loop 变成可编程运行时的工程设计

> **核心论点**：Agent 的工具调用模式正在经历一次范式转移——从「模型调用工具 → 观察结果 → 再调用工具」的串行循环，进化到「Agent 在一个受限运行时里写代码，以编程方式编排工具调用」。这个运行时叫做 **Interpreter**，它解决的不是 Agent 能做什么的问题，而是 **Agent 如何组织中间状态** 的问题。

---

## 1. 串行工具调用的问题：中间状态是 context 的敌人

理解 Interpreter 之前，先看清楚现有的工具调用模式有什么结构性问题。

最简单的 Agent Loop 是这样的：

```
模型调用工具 → 接收完整结果 → 推理 → 调用下一个工具 → ...
```

每一步的结果都会以文本形式回流到 context window。对于简单的两步序列这不是问题，但当工作流涉及多步数据变换、临时变量、循环逻辑时，这个模式开始暴露缺陷：

**第一，context window 的隐性消耗。** 中间结果不管是原始数据还是总结后的文本，都要占用 context。如果一个任务涉及 20 次工具调用，每次返回 500 token 的中间数据，context 会迅速膨胀。

**第二，模型需要「翻译」每一次观察。** 模型不仅要做决策，还要把每次工具调用的结果重新吸收进推理过程。这相当于让模型同时扮演「执行者」和「总结者」两个角色——当中间步骤涉及结构化数据（数组、对象、映射）时，这种翻译的代价更高。

**第三，工具调用的粒度与业务逻辑的粒度不匹配。** 业务逻辑往往是「对这个数组里的每个元素做 X，然后按 Y 排序，再取前 N 个」。但串行工具调用模式只能一次做一件事，循环必须由模型控制——每次循环迭代都是一次额外的模型 round trip。

这三个问题有一个共同根源：**中间状态被强制塞进了模型可以推理的 context surface**，而不是留在模型可以高效访问的地方。

---

## 2. Interpreter 模式：工具调用和沙箱之间的中间地带

LangChain 在 Deep Agents 里引入了 Interpreter 模式。它的核心思想是：**在 Agent Loop 和完整沙箱之间，提供一个受限的代码运行时，让 Agent 可以在里面写代码来组织自己的行为。**

这个运行时不是完整的 Python/Node 环境。它默认只有：

- 基本数据类型：对象、数组、映射、JSON
- 控制流：循环、条件、函数定义
- **显式桥接**：只有明确 bridged 到 host runtime 的工具才能被调用

也就是说，这个 Interpreter 是有意设计的「小语言」，而不是一个通用编程环境。

```
Agent 写代码：
const rows = [
  { team: "support", tickets: 18 },
  { team: "infra", tickets: 7 },
];
const total = rows.reduce((sum, row) => sum + row.tickets, 0);
const busiest = rows.sort((a, b) => b.tickets - a.tickets)[0];
`${busiest.team} has the most tickets.`
```

这个代码在 Interpreter 里运行，结果只有最后那个字符串回流到 context。中间所有计算过程都在 Interpreter 内部，不消耗 context。

**这里的关键设计洞察是：Interpreter state is a third context surface。** Agent 的 context 现在有三个地方可以存东西：

| Context Surface | 用途 | 持久性 | Context 消耗 |
|---------------|------|--------|------------|
| **Message History** | 模型需要推理的当前信息 | 当前 Session | 高（按 token 计）|
| **Filesystem** | 持久化 artifacts、笔记、中间文件 | 跨 Session | 低（序列化时消耗）|
| **Interpreter State** | 运行时变量、数组、对象、helper 函数 | 当前 Session | **几乎为零** |

Interpreter state 解决了「这些值我需要但还不想让模型看到」的存储问题。模型可以稍后查询 Interpreter 的某个变量，而不是在 context 里反复看到它的完整演化过程。

---

## 3. Programmatic Tool Calling：工具调用从模型动作变成代码调用

与 Interpreter 模式紧密相关的是 **Programmatic Tool Calling（PTC）**。这是 Anthropic 在 Claude Agent SDK 里引入的模式，LangChain Deep Agents 的 Interpreter 实现了同样的功能。

在传统模式里，工具调用是模型直接驱动的：

```
模型决定调用 fetch("https://example.com")
→ 模型等待结果 → 模型推理 → 模型决定调用 next tool
```

在 PTC 模式里，工具调用发生在 Agent 写的代码里：

```javascript
const topics = ["retrieval", "memory", "evaluation"];
const reports = await Promise.all(
  topics.map((topic) => tools.fetch(`https://docs.example.com/${topic}`))
);
const summaries = reports.map(r => tools.summarize(r));
```

工具通过 bridge 暴露给 Interpreter，Agent 以 `await tools.xxx()` 的方式调用它们。**每个工具都是 Interpreter global namespace 里的一个 async 函数。**

PTC 带来的工程变化是具体的：

**第一，减少模型 round trip。** 原来需要 20 次串行工具调用的工作流，现在可能变成一次代码执行，中间状态全在 Interpreter 里。模型只参与关键的决策点，而不是每次工具调用后的结果吸收。

**第二，中间的结构化数据不泄漏到 context。** `reports` 数组里的内容不需要序列化回 context，因为后续的 `.map()` 继续在 Interpreter 里处理。只有最终的 `summaries` 可能需要回到 context。

**第三，工具调用的确定性增强。** 串行模式下，模型的每次工具选择都有一定随机性（尤其是在中间结果模糊的情况下）。PTC 把选择权部分转移给了代码逻辑——循环、条件、分支都在代码里，模型提供的是高层指导而非每一步决策。

---

## 4. 受限是有意的：安全性和可预测性的来源

LangChain 在 Interpreter 设计里反复强调一个原则：**minimal by design, capabilities are added back deliberately**。这个设计选择背后有工程上的理由。

如果 Interpreter 是一个完整的 Python 环境，它会和沙箱产生重叠——都提供宽泛的主机访问，都需要进程级或 VM 级的隔离。Interpreter 的定位应该是**受限代码执行**，不是通用运行时。

受限设计的工程价值在于：

**更小的攻击面。** 沙箱的默认策略是「从宽泛权限开始，然后收紧」。Interpreter 的默认策略是「从最小权限开始，按需扩展」。Agent 拿到的不是一台「类似电脑的东西」，而是一个「语言运行时 + 显式桥接的 API」。没有文件系统、没有网络、没有 shell——除非你明确 bridge 这些能力。

这与 Cloudflare 的 Code Mode、Anthropic 的 PTC、以及 RLM-style workflows 在架构上是一致的：**给模型一个小的、受限的运行时，让它在受控边界内编程，而不是给它一台机器然后尝试限制它的行为。**

**更可预测的行为。** 一个固定的小运行时使得 Agent 的行为更容易评估。如果 Interpreter 有宽泛的主机访问或丰富的库表面，同一个目标可以通过许多不同的策略实现——输出的不一致性会更高，测试也会更困难。

LangChain 的原文表达了这个权衡的逻辑：

> "By keeping the default environment minimal and forcing extra capabilities to cross explicit bridges, you make the agent's action space narrower, the failure modes clearer, and the results more repeatable."

---

## 5. Harness 架构：Middleware 作为可组合单元

Interpreter 不是孤立存在的，它是 Agent Harness 的一部分。LangChain 在「How to Build a Custom Agent Harness」里描述的架构是：

```
Agent = Model + Harness
Harness = Middleware Stack
```

Harness 的职责是在每一步为模型提供正确的 context。Middleware 则是这个 harness 的可组合单元——每个 middleware 钩入 Agent Loop 的特定位置（before/after model call、before/after tool call、startup、teardown），处理一个关注点。

LangChain 的 prebuilt middleware 覆盖了常见的 harness 能力：

| 能力 | Middleware |
|------|-----------|
| 防止 context 溢出 | SummarizationMiddleware, ContextEditingMiddleware |
| 访问和更新记忆 | FilesystemMiddleware, MemoryMiddleware, SkillsMiddleware |
| 在环境中执行操作 | ShellToolMiddleware, FilesystemMiddleware, CodeInterpreterMiddleware |
| 委托子任务 | SubAgentMiddleware, TodoListMiddleware |
| 处理瞬态失败 | ToolRetryMiddleware, ModelRetryMiddleware, ModelFallbackMiddleware |
| 策略执行 | PIIMiddleware, HumanInTheLoopMiddleware |
| 控制成本 | ModelCallLimitMiddleware, PromptCachingMiddleware |

**Middleware 的价值主张是组合性。** 每个 middleware 处理一个隔离的 concern，可以自由组合。组织里一旦有了 battle-tested 的 middleware，新的 Agent 可以直接继承这些行为，而不需要每次重新实现一遍。

这与 Interpreter 的设计哲学是一致的：都是在**把复杂行为分解成可组合单元**。Middleware 组合的是 harness 级别的行为，Interpreter 组合的是 Agent 的运行时行为。

---

## 6. 可落地性与工程启示

Interpreter 模式不是学术概念，它指向的是具体的工程决策点：

**如果你的 Agent 涉及多步数据变换，考虑给它一个 Interpreter。** 当中间状态是结构化的（数组、对象），而不是文本性的（描述、总结），Interpreter 的价值尤其明显。模型处理结构化数据的效率远低于处理文本，但代码处理结构化数据的效率远高于模型。

**PTC 是给任何模型用的，不是特定模型的能力。** LangChain 的实现是通过 middleware 而不是模型提供者行为——这意味着 PTC 可以 enable 给任何模型，包括开源模型。工具被放进 Interpreter 的 global namespace 作为 async 函数，模型不需要知道底层实现。

**Middleware 是一种组织 harness 逻辑的方式。** 当你的 Agent 需要自定义 prompting、业务逻辑、guardrails 时，把它们做成 middleware。Harness 的复杂度不应该堆积在模型调用逻辑里，而应该分散到可测试、可复用的 middleware 里。

**三个 context surface 需要一起设计。** Message History、Filesystem、Interpreter State 不是三选一，而是需要根据每个数据的用途决定放在哪里：

- 模型现在就需要推理的 → Message History
- 需要跨 Session 持久化的 → Filesystem
- 模型暂时不需要但后续会用到的 → Interpreter State

---

## 结语

Interpreter 模式解决的核心问题，不是「Agent 能做什么」，而是「Agent 如何组织中间状态」。在 context window 有限且昂贵的约束下，把中间计算从 model context 转移到可控运行时，是一个根本性的工程解法。

这不是工具调用的增强版，而是一次组织结构的改变：模型提供高层决策和推理，代码负责流程控制和状态管理，middleware 负责 harness 级别的横切关注点。三者各司其职，Agent 才可能在复杂任务中保持可预测性和可调试性。

**所以你应该：先问你的 Agent 是否有中间状态管理的问题。如果有，Interpreter 模式值得认真考虑。**

---

**引用来源**：
- LangChain Engineering, "Give Your Agents an Interpreter" (https://blog.langchain.com/give-your-agents-an-interpreter)
- LangChain Engineering, "How to Build a Custom Agent Harness" (https://blog.langchain.com/how-to-build-a-custom-agent-harness)
