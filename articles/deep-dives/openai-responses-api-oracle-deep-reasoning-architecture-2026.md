---
title: OpenAI Responses API 一周年：为什么「让模型专心推理」反而是 Agent 架构的最优解
date: 2026-06-08
source: "https://developers.openai.com/blog/one-year-of-responses"
tags:
  - Orchestration
  - Context-Memory
  - Deep-Dives
  - Architecture
  - Multi-Agent
---

> 本文是我在阅读 OpenAI 官方博客 "[From prompts to products: One year of Responses](https://developers.openai.com/blog/one-year-of-responses)" 后的一次深度分析。原始内容来自 OpenAI Developers Blog（2026-03-11），版权归 OpenAI 所有，本文仅做工程解读与结构化重述。

---

## 核心论点

大多数 Agent 系统试图让同一个模型同时完成两件事：**上下文收集**（搜索、检索、工具调用）和**深度推理**。这导致模型在两类任务之间反复横跳，上下文窗口被中间步骤填满，真正有价值的推理能力被稀释。

OpenAI  Responses API 的首批生产用户 Repo Prompt 给出了一个截然不同的答案：**用专用 Agent 负责上下文构建，把深度推理交给一个「不动工具」的 Oracle 模型**。这不是花哨的设计，而是经过大规模生产验证的架构选择。

---

## 背景：上下文窗口的两难

当一个 Agent 需要处理复杂任务时，常见的做法是让同一个模型一边执行工具调用获取信息，一边在同一个推理过程中分析这些信息。问题在于：

- 工具调用会污染推理的中间状态
- 上下文窗口在「收集 → 推理 → 再收集」的循环中快速膨胀
- 模型的推理能力被分散在信息检索任务上，无法专注于核心分析

一个常见的例子是代码库分析任务：模型 A 需要先遍历数千个文件找到相关代码，然后才能开始分析。但在这个过程中，它的推理窗口已经被文件路径和片段填满了。

---

## Oracle 架构：三层分离

Repo Prompt 的系统将任务拆解为三个明确阶段，每个阶段由不同的组件负责：

### 第一层：上下文构建 Agent

这个 Agent 的职责是**纯粹的上下文收集**：分析大型代码库或文档集合，识别与查询相关的文件、文档间的关联、以及关键段落。它使用 Responses API 的工具调用和推理能力完成这一步。

```python
# 上下文构建 Agent 的职责
context_agent = Agent(
    model="gpt-5.3-codex",
    tools=[file_search, web_search, code_search],
    role="curator"  # 不做分析，只做收集
)
context_package = context_agent.run(query)
```

其输出是一个**结构化的上下文包**（structured context package），包含：
- 相关的文件片段和位置信息
- 文档之间的关系图谱
- 关键段落的原始文本

这个上下文包成为下一阶段的唯一输入。

### 第二层：Oracle 深度推理模型

这是 Oracle 架构的核心设计：**Oracle 模型不执行任何工具调用**，它的全部注意力都用于分析提供的上下文。

```python
# Oracle 模型：不调用工具，只推理
oracle = Model(
    model="gpt-5.3-reasoning",
    tools=[]  # 禁止工具调用
)
analysis = oracle.analyze(context_package)
```

为什么这样设计更优？因为：

1. **注意力集中**：模型不需要在「工具调用」和「分析」之间切换注意力
2. **推理深度**：上下文窗口 100% 用于推理，不被中间步骤污染
3. **长时推理**：Oracle 可以运行数分钟甚至更长时间，专注于复杂关系分析
4. **成本可控**：推理模型只在最后阶段调用，前面的收集阶段成本更低

### 第三层：迭代研究与分析循环

单一推理过程可能不够——初始分析可能揭示需要进一步调查的方向。系统在 Oracle 输出后引入一个**评审 Agent**，决定是否需要新一轮上下文收集与推理。

```python
# 迭代循环
while analysis.requires_more_investigation:
    additional_context = context_agent.investigate(analysis.gaps)
    analysis = oracle.analyze(context_package + additional_context)
```

这种循环让系统能够执行**渐进式深度调查**，类似人类分析师的工作方式：初步结论 → 发现盲点 → 补充调查 → 更深结论。

---

## 这个架构为什么值得单独成文

Oracle 架构与现有的多 Agent 编排模式有一个关键区别：**它不是按角色分工（planner/executor），而是按认知功能分工（收集/推理）**。

| 维度 | 传统多 Agent | Oracle 架构 |
|------|------------|------------|
| 分工依据 | 角色（planner/worker）| 认知功能（收集/推理）|
| 信息流 | 工具调用结果直接进入推理 | 工具结果先汇聚为上下文包，再统一输入推理 |
| 模型注意力 | 被工具调用分散 | 专注在纯推理任务 |
| 适用场景 | 快速执行型任务 | 深度分析型任务 |

这不是说 Oracle 架构比传统多 Agent 更优越——而是它填补了一个特定的工程空白：**当任务需要深度推理时，收集和推理的分离是提升质量的有效手段**。

---

## 生产佐证：Responses API 的三个关键能力

Repo Prompt 的 Oracle 架构依赖 Responses API 的三项核心能力：

> "The platform uses the OpenAI Responses API to orchestrate long-running agent workflows and reasoning jobs for workflows, including: Large codebase analysis and architecture planning, Deep code review workflows, Research analysis on large document collections, Medical and scientific document analysis."

### 1. Background Jobs（后台作业）

长时推理任务需要能够执行分钟级甚至小时级的运算，不能因为连接断开而中断。Background Jobs 提供了一种将任务挂起和恢复的机制。

### 2. Agent Orchestration（Agent 编排）

协调上下文构建、推理、验证等多个 Agent 之间的循环，需要可靠的编排能力。Responses API 原生支持这种多阶段工作流。

### 3. Observability（可观测性）

监控长时运行的推理工作流，了解任务进展和状态，是让这类架构可运维的前提。

---

## 关联案例：三层监控与多 Agent 管道的工程支撑

Oracle 架构不是孤立的。同一篇文章中，Raindrop AI 和 Hexagon 的案例从不同角度印证了「分离关注点」的工程价值：

### Raindrop AI：三层监控架构

Raindrop AI 解决了 Agent 生产运维中的可观测性问题。其三层监控架构是 Oracle 架构的运维补充：

1. **Agent 行为监控**：持续评估 Agent 是否按预期工作
2. **失败检测与告警**：发现异常时即时通知，并附上根因上下文
3. **调试工具**：帮助开发者将「发现失败」和「修复问题」连接起来

> "The platform focuses on three core systems: Agent behavior monitoring, Failure detection and alerting, Developer investigation and debugging tools."

Raindrop AI 用 Responses API（通过 Vercel AI SDK）驱动所有长时后台分析工作流，实现跨模型提供商的监控。这说明 Responses API 的编排能力不仅适用于前台任务，也适用于后台监控逻辑。

### Hexagon：多 Agent 内容生成管道

Hexagon 使用四 Agent 架构执行内容优化管道，每个 Agent 专注于一个特定步骤，最终产出传给下一阶段，直到生成最终内容并发布。关键的是**非确定性循环**——Agent 之间通过迭代式精炼而非固定流程传递信息。

> "The agents communicate through non-deterministic loops for iterative refinement before publishing."

这种模式与 Oracle 架构的迭代循环（上下文 → 推理 → 评审 → 补充调查）形成呼应：都是在「固定流程」和「完全自由」之间选择了一个更有结构的中间态。

---

## 工程启示

### Oracle 架构的适用边界

**适合用 Oracle 架构的场景**：
- 代码库深度分析、架构评审
- 大型文档集合的研究分析
- 医学/科学文献的综合分析
- 需要数分钟以上深度推理的任务

**不适合用 Oracle 架构的场景**：
- 快速问答、即时工具执行类任务（Oracle 的启动开销不划算）
- 工具调用本身是任务核心的情况（此时工具调用即是推理）
- 上下文体量小、不需要专门构建的场景

### 实现要点

如果要在自己的系统中实现 Oracle 架构，有几个关键的技术决策点：

1. **上下文包的格式设计**：结构化程度直接影响 Oracle 的推理质量
2. **评审 Agent 的判断标准**：何时停止迭代（成本 vs. 质量权衡）
3. **背景作业的挂起与恢复**：长时推理需要幂等的任务状态管理
4. **可观测性**：Oracle 的推理过程黑盒，需要 trace 机制辅助调试

---

## 原文引用

> "Rather than letting the reasoning model waste its context window navigating context during planning or reviews, we leverage a separate agent to curate context ahead of time, to let our reasoning model dedicate as much of its reasoning as possible to solving our task."

> "Unlike the context-building agents, the 'Oracle' model (the deep reasoning model) does not perform tool calls or additional information retrieval. Instead, it focuses entirely on analyzing the curated context provided to it."

---

## 总结

Oracle 架构的核心洞察是：**让模型「专心」比让模型「全能」更能发挥其推理能力**。这不是一个学术假设，而是来自大规模生产环境的工程验证。

当你的 Agent 任务需要深度分析时，考虑：
1. 引入一个专门的上下文构建 Agent
2. 将收集到的上下文打包为结构化输入
3. 交给一个「不动工具」的 Oracle 模型专注推理
4. 通过评审循环处理复杂的迭代调查需求

Responses API 的 Background Jobs + Agent Orchestration + Observability 组合，为这类架构提供了生产级的基础设施支持。

---

**关联阅读**：
- [Anthropic Multi-Agent Research System：Orchestrator-Worker 模式](../orchestration/anthropic-multi-agent-research-system-orchestrator-worker-pattern-2026.md)
- [OpenAI Codex Agent Loop Harness 架构解析](../harness/openai-codex-agent-loop-harness-architecture-2026.md)
- [LangSmith Engine Self-Healing Eval Loop](../evaluation/langsmith-engine-self-healing-eval-loop-2026.md)
