# Claude Code Dynamic Workflows：模型自驱编排时代的真正到来

**核心命题**：Anthropic 发布的 Dynamic Workflows 不只是「让 Claude Code更容易用」——它的真正意义是宣告了**模型自驱编排**（Model-Driven Orchestration）时代的到来。过去的编排责任在开发者手里（LangGraph、CrewAI、自定义状态机），现在模型自己就能把任务分解成数百个并行 subagent，再验证结果后回报给用户。

---

## 背景：编排曾是开发者的事

在 Dynamic Workflows 之前，多 Agent 协作的编排责任一直落在开发者肩上：

- 用 LangGraph 定义节点和边
- 用 CrewAI 配置 Agent 角色和任务路由
- 或者自己写一套状态机来管理子 Agent 的生命周期

这套架构的本质是：**人类的编程智慧在弥补模型无法自主协调的缺陷**。你定义了工作流，模型只在节点内执行。

笔者认为，这是合理的——早期的模型确实不擅长自主规划、协调和验证。但这个局限正在被 Dynamic Workflows 打破。

---

## Dynamic Workflows 做了什么

官方描述是：Claude 可以自主规划任务，然后在一个 session 内运行**数百个并行 subagent**，最后验证输出再回报用户。

拆开看，有三个关键词值得深挖：

### 1. 自主规划（而非执行预定流程）

过去的 Claude Code 可以执行多步任务，但每一步仍然是在当前上下文中顺序执行的。你告诉它「先做 A，再做 B」，它就按你的顺序来。

Dynamic Workflows 的不同在于：**规划本身就是模型的工作**。你给一个高层目标（比如「把整个代码库从 Zig 迁移到 Rust」），模型自己决定：

- 任务如何分解
- 哪些子任务可以并行
- 以什么顺序执行
- 如何验证每个子任务的完成度

这意味着模型的输出不只是代码，而是一个**执行计划 + 协调层**。

### 2. 数百个并行 subagent

这是最令人印象深刻的部分。并行 subagent 不是新概念——LangGraph 的 `Send` API 早就支持图内并行消息传递；CrewAI 的 `parallel` 任务执行也早就存在。但这些都依赖开发者显式配置。

Dynamic Workflows 的不同在于：这些 subagent 是模型**在运行时动态生成**的，数量可达数百个。

> "Work you'd normally plan in quarters now finishes in days. Claude dynamically writes orchestration scripts that run tens to hundreds of parallel subagents in a single session, checking its work before anything reaches you."

——Anthropic 官方博客原文

Bun 从 Zig 到 Rust 的迁移案例最能说明问题：99.8% 测试通过率、约 75 万行 Rust、11 天完成——这在传统工作流里是不可想象的。

### 3. 验证层（Generator-Evaluator Loop）

并行执行最大的风险是：如何保证子任务的输出质量？Anthropic 的方案是加入**验证层**——模型在生成输出后自己检查结果是否满足预期，而不是直接交付。

这种模式在学术圈有更正式的名字：**Generator-Evaluator Loop**。Anthropic 自己的 Harness Design 文章里也详细描述过这个架构在长任务中的应用。但 Dynamic Workflows 把这个能力变成了内置的原生特性。

笔者认为，这个设计选择非常关键——它说明 Anthropic 意识到，在「让模型自主工作」的场景里，**验证比规划更重要**：如果模型无法判断自己做得对不对，自主运行就变成了盲目运行。

---

## 为什么这代表了范式转变

### 从「人在编排」到「模型在编排」

这个转变的影响不只是少写几行配置代码。它的深层含义是：**Agent 的协调层次发生了上移**。

过去我们是这样设计 Agent 系统的：

```
人类开发者 → 编排层（LangGraph/CrewAI/自定义状态机）→ Agent 执行
```

Dynamic Workflows 把编排层本身交给了模型。人类开发者只需要给目标——实现细节（任务分解、并行策略、验证方式）全由模型决定。

### 开发者角色的重新定位

如果模型能自己编排，那开发者在 Agent 系统里的角色是什么？

Anthropic 的说法是：**设计环境、定义意图、构建反馈循环**。换句话说，开发者不再写「怎么做」，而是定义「做到什么算完成」和「在什么条件下算失败」。

笔者认为，这个转变的核心是**从「执行者」到「裁判员」的角色转换**——人类负责定义规则，模型负责在规则内自主执行。

### 对现有 Agent 框架的影响

这里需要区分两类框架：

**编排框架**（LangGraph、CrewAI、AutoGen）：这些框架的核心价值一直是「帮开发者管理 Agent 之间的协作关系」。Dynamic Workflows 直接侵蚀了这层价值——如果模型能自主编排，为什么还需要 LangGraph 的图结构来显式定义？笔者认为，对于需要模型自驱编排的场景，这类框架的必要性正在下降。

**非编排框架**（Pydantic AI、SmolAgents、AgentSDK）：这些框架更专注于单个 Agent 的能力边界（工具调用、Memory、Session 管理），受 Dynamic Workflows 的冲击较小。但它们的工具层需要能支持 Dynamic Workflows 的上下文需求。

---

## 技术细节：它实际上是怎么工作的

Anthropic 没有公开 Dynamic Workflows 的完整实现细节，但从公开信息可以推断几个技术约束：

### 上下文窗口的管理

数百个并行 subagent 意味着模型需要同时维护多个执行上下文。Claude Opus 4.8 扩展的 context window 是前提条件，但更重要的是**如何在长上下文内保持任务分解的连贯性**。

Dynamic Workflows 采用了**计划-执行-验证**的三段式结构，而非实时的连续协调。这说明 subagent 之间不需要高频通信——模型先制定完整计划，再分发任务，最后统一验证。这种设计降低了 subagent 之间的协调复杂度，但也意味着整个系统的行为更接近「批量处理」而非「实时流式协作」。

### 验证机制

验证是 Dynamic Workflows 的核心环节。验证基于**预设的测试套件或明确的完成标准**。这意味着 Dynamic Workflows 适用于「结果可量化」的场景（如代码迁移有测试用例），而不适合「质量主观」的场景（如创意写作、UI 设计）。

### 与 Claude Agent SDK 的关系

Claude Agent SDK 已经支持多 session 管理和跨 session 的上下文传递（compaction）。Dynamic Workflows 很可能是在这个基础上增加了动态任务分解和并行调度的能力。

---

## Dynamic Workflows 的适用边界

笔者认为，以下场景是 Dynamic Workflows 的**最佳适用场景**：

1. **大规模代码迁移**：Framework 升级、语言迁移，跨越数千个文件，有明确的质量标准（测试套件）
2. **全代码库审计**：Bug Hunt、安全审计、Code Review，需要多角度并行验证
3. **临界工作需要两次确认**：当错误代价高时，工作流给 Claude 独立尝试的机会

以下场景**不太适合** Dynamic Workflows：

1. **快速原型和小任务**：workflow 的开销对于简单任务来说不划算
2. **创意/主观质量工作**：无法用测试套件量化质量
3. **需要人工介入的中途决策**：Dynamic Workflows 设计为自主运行到完成，中途人工干预的接口有限

---

## 对 Harness 工程的影响

笔者认为，Dynamic Workflows 的出现对 Harness 工程有双重影响：

**正面影响**：验证层内置意味着开发者不需要自己搭建 Generator-Evaluator Loop，Harness 的核心工程负担（状态管理、checkpoint、恢复机制）可以被 Dynamic Workflows 吸收。

**新的工程挑战**：当模型自己负责编排时，开发者如何**监督和干预**一个正在自主运行的 workflow？这需要一个新型的「mission control」界面——让人类在模型自主运行的同时保持可见性，并在必要时介入。这是当前 Dynamic Workflows 还没有完整解决的问题。

---

## 引用来源

- Introducing Dynamic Workflows in Claude Code: https://claude.com/blog/introducing-dynamic-workflows-in-claude-code
- Harness Design for Long-Running Application Development: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Building a C Compiler with a Team of Parallel Claudes: https://www.anthropic.com/engineering/building-c-compiler