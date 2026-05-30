# Anthropic Dynamic Workflows：当模型开始编排自己的 Agent 舰队

**核心命题**：Claude Opus 4.8 带来的 Dynamic Workflows 不只是一个功能，它宣告了「模型自驱编排」时代的到来——过去需要开发者用 LangGraph/CrewAI 手动编排的 Agent 协作，现在模型自己就能搞定。

---

## 背景：编排曾是开发者的活儿

在 Dynamic Workflows 出现之前，多 Agent 协作的编排责任一直落在开发者肩上。你需要：

- 用 LangGraph 定义节点和边
- 用 CrewAI 配置 Agent 角色和任务路由
- 或者自己写一套状态机来管理子 Agent 的生命周期

这套架构的本质是：**人类的编程智慧在弥补模型无法自主协调的缺陷**。你定义了工作流，模型只在节点内执行。

这是合理的——早期的模型确实不擅长自主规划、协调和验证。但这个局限正在被 Dynamic Workflows 打破。

---

## Dynamic Workflows 做了什么

Anthropic 的官方描述是：Claude 可以自主规划任务，然后在一个 session 内运行**数百个并行 subagent**，最后验证输出再回报用户。

这个描述里有几个关键词值得拆开看：

### 1. 自主规划（而非执行预定流程）

过去的 Claude Code 可以执行多步任务，但每一步仍然是在当前上下文中顺序执行的。你告诉它「先做 A，再做 B」，它就按你的顺序来。

Dynamic Workflows 的不同在于：**规划本身就是模型的工作**。你给一个高层目标（比如「把整个代码库从 JavaScript 迁移到 TypeScript」），模型自己决定：

- 任务如何分解
- 哪些子任务可以并行
- 以什么顺序执行
- 如何验证每个子任务的完成度

这意味着模型的输出不只是代码，而是一个**执行计划 + 协调层**。

### 2. 数百个并行 subagent

这是最令人印象深刻的部分。并行 subagent 不是新概念——LangGraph 的 `Send` API 早就支持图内并行消息传递；CrewAI 的 `parallel` 任务执行也早就存在。但这些都依赖开发者显式配置。

Dynamic Workflows 的不同在于：这些 subagent 是模型**在运行时动态生成**的，数量可达数百个，且每个 subagent 都可以在 Opus 4.8 上运行更长时间。

> "Claude Code with Opus 4.8 can now carry out codebase-scale migrations across hundreds of thousands of lines of code from kickoff to merge, with the existing test suite as its bar."

——Anthropic 官方博客原文

这个尺度（数十万行代码的迁移）以前只有 Devin 这类专注于 Software Agent 的产品敢承诺。

### 3. 验证层（自验证输出）

并行执行最大的风险是：如何保证子任务的输出质量？Anthropic 的方案是加入**验证层**——模型在生成输出后自己检查结果是否满足预期，而不是直接交付。

这种模式在学术圈有更正式的名字：**Generator-Evaluator Loop**。Anthropic 自己的 Harness Design 文章（2026年3月）里也详细描述过这个架构在长任务中的应用。但 Dynamic Workflows 把这个能力变成了内置的原生特性，而不是需要开发者自己搭建的 scaffold。

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

Anthropic 自己的说法是：**设计环境、定义意图、构建反馈循环**。换句话说，开发者不再写「怎么做」，而是定义「做到什么算完成」和「在什么条件下算失败」。

OpenAI 在 Harness Engineering 文章里表达过类似的观点：人类的角色变成了「描述任务 → 运行 Agent → 验收 PR」，中间的执行细节全由 Agent 主导。这个趋势在 Dynamic Workflows 这里进一步加速。

### 对现有 Agent 框架的影响

这里需要区分两类框架：

**编排框架**（LangGraph、CrewAI、AutoGen）：这些框架的核心价值一直是「帮开发者管理 Agent 之间的协作关系」。Dynamic Workflows 直接侵蚀了这层价值——如果模型能自主编排，为什么还需要 LangGraph 的图结构来显式定义？笔者认为，对于需要模型自驱编排的场景，这类框架的必要性正在下降。

**非编排框架**（Pydantic AI、SmolAgents、AgentSDK）：这些框架更专注于单个 Agent 的能力边界（工具调用、Memory、Session 管理），受 Dynamic Workflows 的冲击较小。但它们的工具层需要能支持 Dynamic Workflows 的上下文需求，比如更长的 session 生命周期和更丰富的子 Agent 通信机制。

---

## 技术细节：它实际上是怎么工作的

Anthropic 没有公开 Dynamic Workflows 的实现细节，但从公开信息可以推断几个技术约束：

### 上下文窗口的管理

数百个并行 subagent 意味着模型需要同时维护多个执行上下文。Claude Opus 4.8 扩展的 context window 是前提条件，但更重要的是**如何在长上下文内保持任务分解的连贯性**。

从 Towards AI 的报道来看，Dynamic Workflows 采用了**计划-执行-验证**的三段式结构，而非实时的连续协调。这说明 subagent 之间不需要高频通信——模型先制定完整计划，再分发任务，最后统一验证。这种设计降低了 subagent 之间的协调复杂度，但也意味着整个系统的行为更接近「批量处理」而非「实时流式协作」。

### 验证机制

验证是 Dynamic Workflows 的核心环节。从公开材料来看，验证基于**预设的测试套件或明确的完成标准**。这意味着 Dynamic Workflows 适用于「结果可量化」的场景（如代码迁移有测试用例、API 迁移有对照测试），而不适合「质量主观」的场景（如创意写作、UI 设计）。

### 与 Claude Agent SDK 的关系

Claude Agent SDK 已经支持多 session 管理和跨 session 的上下文传递（compaction）。Dynamic Workflows 很可能是在这个基础上增加了动态任务分解和并行调度的能力，但具体实现细节 Anthropic 没有披露。

---

## 适用边界

Dynamic Workflows 不是万能药。它的适用性取决于以下几个维度：

| 场景 | 适合 Dynamic Workflows | 不适合 |
|------|----------------------|--------|
| 代码迁移 | ✅ 大规模、有测试覆盖 | ❌ 缺乏测试的小型项目 |
| 数据处理 | ✅ 规则明确、可自动化验证 | ❌ 依赖人工判断的数据清洗 |
| 研究任务 | ✅ 多源信息收集、可对照验证 | ❌ 开放式写作、创意生成 |
| API 重构 | ✅ 有完整集成测试 | ❌ 无测试覆盖的遗留系统 |

笔者认为，Dynamic Workflows 最有价值的场景是**代码库级别的重构和迁移**——这类任务以前只能靠 Devin 这样的专用 Agent，现在 Claude Code 也有了同等能力。

---

## 结论：编排上移的下一步

Dynamic Workflows 代表的方向很清楚：**模型的协调能力在增强，开发者的编排负担在下降**。这不是说 LangGraph 这类框架会消失——对于需要精确控制执行顺序、需要多轮人工审批、需要跨系统集成的复杂工作流，显式编排仍有价值。

但对于「模型能自己搞清楚怎么干」的场景，Dynamic Workflows 已经把开发者从编排代码里解放出来。下一步的问题是：**当模型能自主编排 Agent，Agent 框架的核心价值会变成什么？**

答案很可能是：工具生态（Tool Mesh）和评估体系（Harness/Evals）。这两层不受编排方式影响，是 Agent 系统里真正持久的基础设施。

> "What it is, instead, is the first release in a while that actually shrinks the gap between what frontier models can do in a single call and what agent frameworks have been bolting on top of them."
> 
> ——Rajesh Vishnani, Towards AI

---

**引用来源**：
- Anthropic 官方公告：https://www.anthropic.com/news/claude-opus-4-8
- Towards AI 深度分析：https://pub.towardsai.net/what-claude-opus-4-8-actually-changes-if-youre-building-agents-413538e8910c
- Anthropic Harness Design 文章：https://www.anthropic.com/engineering/harness-design-long-running-apps（已归档至 `harness/anthropic-harness-design-long-running-apps-2026.md`）