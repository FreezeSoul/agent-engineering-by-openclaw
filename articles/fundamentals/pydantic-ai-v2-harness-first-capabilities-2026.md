# Pydantic AI v2.0：Harness-First 设计范式的确立

## 核心命题

**Pydantic AI v2.0（2026-06-23）确立了一个明确的方向：Agent 框架的核心抽象应该是 Harness，而不是 Agent 本身。** 通过引入 Capabilities 作为核心原语，Pydantic AI 将工具、Hooks、指令、模型配置打包成可复用的单元，让 Harness 的构建从「配置堆砌」变成「单元组合」。

---

## 为什么这重要

大多数 Agent 框架的演进路径是：先有 Agent 概念，再围绕它添加工具、记忆、安全防护。这些框架的隐含假设是 **Agent 是核心，Harness 是附件**。

Pydantic AI v2.0 反过来了：**Harness 是核心，Agent 是 Harness 的执行上下文**。

> "V2 leans into a harness-first design with capabilities as a core primitive — a single composable unit that bundles an agent's tools, hooks, instructions, and model settings, reaching every layer of the agent through one concept."
> — [Pydantic AI v2.0 Release Notes, GitHub](https://github.com/pydantic/pydantic-ai/releases/tag/v2.0.0)

笔者认为，这个转变的意义在于：它让「如何组织一个 Agent 的所有控制逻辑」这个问题有了统一的答案。过去的方案是构造函数参数列表越来越长（tools=..., hooks=..., instructions=..., model_settings=...），v2.0 的方案是**把这些东西封装成一个 Capability，然后像搭积木一样组合**。

---

## Capabilities：Harness 的原子化

### 什么是 Capability

Capability 是 Pydantic AI v2.0 提出的核心概念。它是一个**可复用、可组合的单元**，将一个 Agent 所需的全部控制要素打包在一起：

- **工具集（Tools）**：Agent 能执行的操作
- **Hooks**：Agent 运行时的行为拦截点（类似于 Web 框架的中间件）
- **指令（Instructions）**：静态的系统提示词
- **模型配置（Model Settings）**：温度、max_tokens、推理模式等

```python
from pydantic_ai import Agent
from pydantic_ai.capabilities import Thinking, WebSearch

agent = Agent(
    'anthropic:claude-sonnet-4-6',
    instructions='Be concise, reply with one sentence.',
    capabilities=[Thinking(), WebSearch()],
)
```

这段代码展示了 Capability 的用法：**不再需要分别传入 tools=[...]、hooks=[...]、model=...，一个 Capability 对象封装了所有这些**。

### 为什么这样设计更好

笔者认为，传统的「传一堆参数」方式的根本问题是：**当你需要复用部分配置时，没有办法只复用一部分**。

例如，你可能想复用「Web 搜索工具集 + 相关 Hooks」，但换一个不同的指令和模型配置。传统方案做不到，Capability 方案可以。

更关键的是，Capability 可以在不同 Agent 之间共享，也可以从第三方包安装：

> "Build agents from composable capabilities that bundle tools, hooks, instructions, and model settings into reusable units. Use built-in capabilities for web search, thinking, and MCP, pick from the Pydantic AI Harness capability library, build your own, or install third-party capability packages."
> — [Pydantic AI Capabilities Docs](https://ai.pydantic.dev/capabilities/)

这实际上是在说：Harness 的构建正在从「手写」走向「组装」。

---

## Durable Execution：Checkpoint/Resume 的生产级实现

v2.0 的另一项核心特性是 **Durable Execution（耐久执行）**。

> "Enables you to build durable agents that can preserve their progress across transient API failures and application errors or restarts, and handle long-running, asynchronous, and human-in-the-loop workflows with production-grade reliability."
> — [Pydantic AI v2.0, PyPI](https://pypi.org/project/pydantic-ai/2.0.0/)

这个描述里有几个关键词值得注意：

1. **preserve progress across failures/restarts**：Agent 的执行状态可以被持久化，API 失败或应用重启后从断点恢复
2. **long-running, asynchronous**：支持长时运行的工作流，不是那种「发起请求-等待响应-结束」的短任务
3. **human-in-the-loop**：人类可以在 Agent 运行过程中介入（Tool Approval 机制）
4. **production-grade reliability**：这是 Pydantic 团队明确的生产级承诺，不是实验性功能

笔者认为，Pydantic AI 选择在这个版本把 Durable Execution 做成一级特性，说明 **长时运行 Agent 的状态管理问题已经开始被主流框架正视**。过去这更多是 Harness 设计层面的讨论，现在它变成了框架的内置能力。

结合 Capability 来看，Durable Execution 的实现逻辑很可能是：每个 Capability 的执行结果可以被 checkpoint，下一次运行时从最近的成功状态恢复。

---

## Graph Support：多 Agent 编排的新方式

v2.0 还引入了 Graph 支持：

> "Provides a powerful way to define graphs using type hints, for use in complex applications where standard control flow can degrade to spaghetti code."
> — [Pydantic AI v2.0, PyPI](https://pypi.org/project/pydantic-ai/2.0.0/)

「spaghetti code」这个描述精准地点出了多 Agent 编排的问题：当 Agent 之间的交互逻辑复杂到一定程度，用 if-else 和回调函数会变成一团乱麻。

基于类型提示的 Graph 定义意味着：你可以在代码层面用静态类型声明 Agent 之间的拓扑关系，而不是用字符串或配置文件。这对 IDE 自动补全和类型检查都是友好的。

笔者认为，Graph + Capability 的组合值得关注：Capability 定义单个 Agent 的行为边界，Graph 定义 Agent 之间的协作拓扑。两者结合提供了一个完整的多 Agent 工程框架。

---

## 与其他框架的对比

| 特性 | Pydantic AI v2.0 | LangChain | CrewAI | OpenAI Agents SDK |
|------|-----------------|-----------|--------|-------------------|
| **核心抽象** | Capability (Harness-first) | Chain/Agent | Task/Agent | Agent/Harness |
| **状态持久化** | Durable Execution (内置) | 有限 | 无 | 通过 Checkpoint |
| **多 Agent 编排** | Graph (类型提示) | LangGraph | Crew | 基础 |
| **可复用控制单元** | Capability（官方库） | LangChain Hub | Community Skills | 有限 |
| **上线时间** | 2026-06-23 | 持续迭代 | 持续迭代 | 持续迭代 |

---

## 关键判断

**Pydantic AI v2.0 代表的趋势是：Harness 的工程化程度正在加深。** 具体体现在三个层面：

1. **抽象层级的提升**：从「一堆配置参数」到「可命名的能力单元」，让 Harness 的组成可以跨项目复用
2. **状态管理的内置化**：Durable Execution 把原本需要手写的 checkpoint/resume 逻辑变成了框架级支持
3. **编排的结构化**：Graph 支持用类型系统约束 Agent 拓扑，避免多 Agent 场景下的控制流混乱

笔者认为，Pydantic AI 的这个方向值得关注，因为它**从框架层面确立了「Harness 是核心工程问题」这一认知**。当框架开始把资源投入在 Capabilities 生态和 Durable Execution 上，说明社区已经不再满足于「能跑起来」的 Agent 框架，开始追求「能长期稳定运行」的工程基础设施。

---

## 原文引用

1. [Pydantic AI v2.0 Release Notes](https://github.com/pydantic/pydantic-ai/releases/tag/v2.0.0) — GitHub, 2026-06-23
2. [Pydantic AI Capabilities Documentation](https://ai.pydantic.dev/capabilities/) — Pydantic AI Docs
3. [Pydantic AI v2.0 on PyPI](https://pypi.org/project/pydantic-ai/2.0.0/) — 2026-06-23

---

## 附：标题备选

1. **Pydantic AI v2.0：Harness-First 框架的成熟信号** — 策略：事件型，标志性版本发布（≤30单位 ✅）
2. **Capabilities = Agent 控制逻辑的单元化复用水准** — 策略：技术判断，差异化理解（≤30单位 ✅）
3. **Durable Execution + Graph：Pydantic AI 的工程完整度升级** — 策略：功能堆叠，覆盖主要新特性（≤30单位 ✅）

---

*归档目录：`fundamentals/` | 来源：GitHub Releases / PyPI / 官方文档 | 2026-06-24*
