# LangChain 的"最小化 Agent Harness"设计：两条路线的工程博弈

> 本文解析 LangChain 官方博客"How to Build a Custom Agent Harness"（Sydney Runkle, 2026-06-03）中的核心设计思想，分析当前 Agent Harness 的两条主流工程路线。

---

## 核心命题

**LangChain 的 `create_agent` 选择了一条与 Deep Agents 截然相反的路线：不做预装全家桶，而是把 harness 做成一个极简循环，把所有能力都抽成可插拔的 middleware。这不是设计上的"落后"，而是一种经过深思熟虑的工程立场。**

---

## 一、Agent 的重新定义：model + harness

LangChain 这篇文章给出了一个在工程上非常精确的定义：

> You can also define an agent as: **agent = model + harness**
>
> The harness is the scaffolding around the model that connects it to the real world.

这个定义的价值不在于"新"，而在于它**把 Agent 的关注点分离干净了**：model 负责推理，harness 负责把 model 连接到真实世界（工具、内存、context、sandbox）。两者各有各的演进节奏。

而 harness 本身的核心职责，LangChain 也说得很清楚：

> The job of a harness is to get the model the **right context** at the **right time** for the **given task**.

三个维度：内容（context）、时机（time）、任务适配（task）。这不是空话，这三个维度恰好是工程上最难处理的——做对了是 harness，做错了是"有 bug 的 AI"。

---

## 二、两条路线：Minimalist vs Opinionated

这是本文最有价值的部分。LangChain 把当前 Agent Harness 的设计路线分成两种：

### 路线 A：Opinionated（全装方案）

以 **Deep Agents** 和 **Claude Agent SDK** 为代表：

- 预装了 memory、context management、sandboxing 等中间件
- 开箱即用，适合大多数场景
- 适合"快速上手"和"标准场景"

原文说：

> Harnesses like Deep Agents and the Claude Agent SDK come pre-assembled with an opinionated middleware stack: memory, context management, sandboxing, and more. They're designed to get you to a production-ready agent fast, and they work well for most cases.

### 路线 B：Minimalist（最小化方案）

以 `create_agent` 为代表：

- 只实现核心 agent loop
- 把所有能力（memory、guardrails、自定义业务逻辑）抽成 middleware
- 通过 middleware 组合来满足特定需求

原文的哲学表述非常清晰：

> Our philosophy is similar to that of Pi, a highly configurable coding agent harness. create_agent just implements the core agent loop, and it exposes middleware as a primitive for customization.

**笔者认为**：这两条路线解决的是不同阶段的问题。Opinionated 路线适合"不知道需要什么"的初期探索阶段；Minimalist 路线适合"知道问题边界，需要精准控制"的工程落地阶段。它们不是竞争关系，而是演进关系。

---

## 三、Middleware：最小化方案的核心抽象

Middleware 是 `create_agent` 的灵魂。它在 agent loop 的每个关键节点提供钩子：

| 钩子时机 | 能力 |
|---------|------|
| **Before/After model calls** | prompt 动态修改、model 动态切换 |
| **Before/After tool calls** | 参数预处理、结果后处理 |
| **Agent startup/teardown** | 资源初始化、清理 |

Middleware 可以处理四类事情：

### 1. 确定性逻辑（Deterministic Logic）

业务策略、运行时控制——例如根据任务复杂度动态切换 model，或者在特定条件下强制终止 agent。这类的本质是"规则引擎"，不应该写在 prompt 里。

### 2. 工具生命周期管理（Tools）

不是把工具直接注册到 agent，而是让 middleware 接管工具的 setup/teardown/registration 流程。原文指出了这为什么重要：

> This matters when tools have dependencies, require initialization, or need to be torn down cleanly at the end of a run. It also keeps tool configuration close to the logic that governs it, rather than scattered across the agent definition.

### 3. 自定义状态（Custom State）

Middleware 可以扩展 agent 的状态，在多个 hook 之间共享数据。这解决了"跨步骤的全局状态"问题，比如计数器、标志位、累积结果。

### 4. 流处理（Stream Handlers）

拦截和转换 agent 的输出流：过滤事件、注入元数据、把不同类型的事件路由到不同的消费者（UI 接收 token delta，审计日志接收 tool calls，监控系统接收延迟数据）。

**笔者认为**：流处理这个能力被大多数 harness 设计低估了。生产环境里不同 consumer 的需求差异巨大，把这个能力做在 harness 层面，而不是让每个 consumer 自己解析完整事件流，是正确的抽象位置。

---

## 四、Capability → Middleware 对照表：LangChain 的设计精华

这是文章最值得收藏的部分。LangChain 直接给出了"做什么能力 → 用什么 middleware"的对照表：

| 需求 | 解决方案 |
|------|---------|
| **防止 context 溢出** | `SummarizationMiddleware`, `ContextEditingMiddleware` |
| **访问和更新 memory** | `FilesystemMiddleware`, `MemoryMiddleware`, `SkillsMiddleware` |
| **在环境中执行动作** | filesystem + execution tools via middleware |
| **权限控制和安全边界** | `SandboxMiddleware`（隔离执行）|

这个表的工程价值在于：它把"能力"和"实现手段"解耦了。开发者看到需求，能快速定位到具体的 middleware，而不是从零开始设计。

**笔者认为**：这张表实际上是一个"harness 设计模式目录"——当你的 agent 需要某个能力时，你知道middleware 这个抽象层次已经有人帮你抽象过了。这也是 Minimalist 路线的真正价值：**不是让你从零搭 harness，而是让你从已有的 middleware 块里组合**。

---

## 五、LangChain 的 Prebuilt Middleware：复用哲学

LangChain 明确提到了"组织级复用"：

> Because each piece is isolated, the same middleware can be reused across every agent in an organization so that new agents inherit battle-tested behavior without rebuilding it.

这句话背后的工程思想是：**middleware 是组织内的标准能力单元**。当一个团队调试出一个好用的 `AuthMiddleware`，它可以无差别地应用到所有 agent，而不是每个 agent 重新实现一遍。

这个复用模型比"继承一个 base agent class"更灵活，因为 middleware 可以自由组合，不同 agent 可以有不同的 middleware 堆叠。

---

## 六、与 Deep Agents 的对比：一个关键分歧

在[R230 的 Deep Agents 分析](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/master/articles/projects/langchain-deepagents-harness-framework-2026.md)中，我们看到 Deep Agents 的路线是"batteries-included"——预装所有你需要的东西，让 agent 直接可用。

而 `create_agent` 的路线是"atomic primitives + composition"——给你最小的循环和可组合的 middleware 块，让你按需构建。

**根本分歧在于**：Deep Agents 认为"大多数场景需要的 harness 能力是固定的"，而 `create_agent` 认为"不同场景的需求差异太大，固定预设反而是负担"。

**笔者认为**：这个分歧没有绝对对错，而是取决于 Agent 落地的发展阶段。当行业还在探索"标准场景"时，Deep Agents 的预装方案更省力；当行业进入"精准定制"阶段时，`create_agent` 的组合方案更灵活。LangChain 在这篇文章里实际上是在说：**我们进入了后一种阶段**。

---

## 七、工程启示

1. **设计 harness 时，先问三个问题**：context 对吗？时机对吗？适配任务吗？不是功能多不多，是这三个维度做对没有。

2. **Middleware 是 harness 的最小化扩展单元**：不要在 harness 层面硬编码能力，而是通过 middleware 插入。LangChain 的 prebuilt middleware 目录值得先看一遍，可能你需要的已经有人写了。

3. **两条路线按阶段选用**：探索期用 Deep Agents，落地期用 `create_agent` + 自定义 middleware。它们可以在同一个组织的不同场景里并存。

4. **流处理能力不能忽视**：生产环境的 event consumer 多样性很高，把流处理做在 harness 层可以避免下游的重复解析工作。

---

> **引用来源**：LangChain Blog - *How to Build a Custom Agent Harness* by Sydney Runkle, June 3, 2026 (https://www.langchain.com/blog/how-to-build-a-custom-agent-harness)
