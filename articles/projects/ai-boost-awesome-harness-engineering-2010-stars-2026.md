# Awesome Harness Engineering：可能是目前最完整的 Agent Harness 工程知识图谱

> **来源**：[github.com/ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | ⭐ 2010 Stars

## 核心命题

如果你认同 OpenAI 的判断——「Agent 工程的核心工作在 harness，不在模型」——那你迟早需要一个地方，帮你搞清楚这个领域里已经有哪些工具、模式、最佳实践。**awesome-harness-engineering 就是这个领域的精选地图**。

---

## 这个项目解决什么问题

Harness engineering 是一个新兴领域，2026 年之前几乎没有系统性的知识积累。OpenAI 的博文定义了问题域，但社区里大量的工具（context compaction、eval harness、MCP、permission systems、memory 等）散落在各处，没有人来整理。

这个项目的目标是：**成为你入门和深入 harness engineering 的首选资源库**，而不是让你去读十篇 Medium 博客来拼凑一个完整图景。

---

## 核心内容结构

根据 README，这个列表涵盖了以下主题域：

| 主题域 | 核心内容 |
|--------|---------|
| **Foundations** | 什么是 harness engineering 的定义性文章 |
| **Agent Loop** | Codex Agent Loop 拆解等核心循环机制 |
| **Planning & Task Decomposition** | Plan.md、Implement.md 等可执行 artifact |
| **Context Delivery & Compaction** | Context 压缩和按需传递 |
| **Tool Design** | 工具接口设计原则（Anthropic 官方指南） |
| **Skills & MCP** | MCP 协议相关资源和最佳实践 |
| **Permissions & Authorization** | Permission 系统设计（Anthropic 官方指南） |
| **Memory & State** | Agent 记忆和状态管理 |
| **Verification & CI Integration** | Eval harness 和 CI 集成 |
| **Observability & Tracing** | 可观测性和 trace 系统 |
| **Human-in-the-Loop** | 人类在环机制 |
| **Reference Implementations** | 参考实现 |

---

## 精选内容亮点

### 一、OpenAI 官方论文/博文全线收录

这个列表收录了目前关于 harness engineering 最权威的原始来源：

- [Harness Engineering](https://openai.com/index/harness-engineering/) — OpenAI 官方对 harness engineering 的定义
- [Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/) — Codex agent loop 逐层拆解
- [Run Long-Horizon Tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/) — 长周期任务执行实践指南

这三篇是 harness engineering 领域的**一手知识基线**，与今天我写的 Article 形成直接闭环。

### 二、Anthropic 官方工程指南体系

Anthropic 的工程博客提供了目前最完整的 harness 组件设计指南：

- **Building Effective Agents** — Agent 架构基础：workflow vs agent 的选择，以及如何组合基本组件
- **Harness Design for Long-Running Application Development** — 多会话开发任务的 harness 设计，关键洞察：「每个 harness 组件都基于模型做不了某件事的假设；这些假设会随着模型改进而过时」
- **Writing Effective Tools for Agents** — 工具接口设计：命名、schema、错误面，以及「工具设计就是 agent UX」
- **Beyond Permission Prompts** — 构建结构化 permission 和 authorization 系统，而非依赖自然语言 permission 文本
- **Demystifying Evals for AI Agents** — Agent 行为评测框架：测什么、怎么构建 harness eval，以及为什么单元测试风格的 eval 对 agent 不适用

### 三、IBM 和 Google 的补充视角

- IBM 的 [What is an AI Agent?](https://www.ibm.com/think/topics/ai-agents) — 用于锚定 harness 设计决策的 agent 定义
- Google 的 [Agent Development Kit](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/) — Google 的 multi-agent 应用构建框架设计动机

---

## 笔者的判断

awesome-harness-engineering 不是一个让你收藏了就完事的列表。它真正的价值在于：

**第一，它提供了一个认知框架。** 很多人以为 harness engineering = 安全防护 = permission prompts。但这个列表告诉我们：harness 包括了 context 压缩、tool 设计、memory 管理、可观测性、CI 集成——这些加在一起才构成让 agent 在长时间跨度上稳定工作的完整工程系统。

**第二，它的选材标准高。** 收录的不是「100 个 AI 工具列表」类型的资源，而是真正来自 OpenAI、Anthropic、Google 这些一手来源的工程实践指南，以及有明确工程价值的开源实现。

**第三，它与 OpenAI 的实验形成对照。** OpenAI 的博文描述了他们在真实产品中遇到的 harness 问题；这个列表告诉你，社区里已经有哪些工具和模式可以用来解决这些问题。

如果你正在构建 Agent 系统但不确定从哪里入手，这个列表是一个合理的起点——但笔者的建议是，不要停留在列表本身，用它来找到值得深入的主题，然后去读原文。

---

## 如何使用这个列表

1. **快速定位**：用目录找到你当前最关心的问题域（比如 "Context Delivery" 或 "Permissions"）
2. **追踪原文**：每个分类下列出的都是一手来源（OpenAI 官方博文、Anthropic 工程博客），优先读这些
3. **按图索骥**：列表本身就是一张知识地图，读完 Foundation 部分再进入具体主题，顺序不要乱

---

**引用来源**：
1. "Harness engineering is the discipline of designing the scaffolding — context delivery, tool interfaces, planning artifacts, verification loops, memory systems, and sandboxes — that surrounds an AI agent and determines whether it succeeds or fails on real tasks." — [ai-boost/awesome-harness-engineering README](https://github.com/ai-boost/awesome-harness-engineering)
2. "Every component here exists because the model can't do it alone — and the best harnesses are designed knowing those components will become unnecessary as models improve." — [ai-boost/awesome-harness-engineering README](https://github.com/ai-boost/awesome-harness-engineering)
3. [Harness Engineering - OpenAI](https://openai.com/index/harness-engineering/) — 列表收录
4. [Building Effective Agents - Anthropic](https://www.anthropic.com/research/building-effective-agents) — 列表收录
5. [Harness Design for Long-Running Application Development - Anthropic](https://www.anthropic.com/engineering/harness-design-long-running-apps) — 列表收录
