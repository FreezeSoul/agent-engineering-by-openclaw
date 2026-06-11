---
title: OpenAI Harness Engineering：Codex 如何重新定义「人在环中」
date: 2026-06-12
tags: [harness-engineering, feedback-loop, openai, codex, agent-first]
category: harness
---

# OpenAI Harness Engineering：Codex 如何重新定义「人在环中」

> 本文深度解读 OpenAI 官方工程博客发布的 Harness Engineering 实验报告，揭示 AI Agent 工程中反馈循环设计的核心框架。

<!-- more -->

## 核心命题

**在 Agent-First 世界里，唯一真正稀缺的资源不是代码行数，而是人类的时间和注意力。**

这是 OpenAI 在过去五个月的内部实验中最深刻的认知转变。他们用 Codex 构建了一个拥有百万行代码的产品，而整个工程团队只有三名工程师驱动——不是写代码，而是**设计环境、指定意图、构建反馈循环**。

这不是关于 AI 能做什么的演示。这是关于**如何让 AI Agent 可靠工作**的工程框架。

## 为什么旧范式失效了

传统的软件开发范式是：**人类写代码，Agent 提供补全建议**。

在这个范式下，人类的角色是明确的：写代码、review PR、决定架构。Agent 是辅助工具。

但当 Codex 能够自主完成代码编写、测试、CI 配置、文档编写、基础设施配置——**所有代码都是 Agent 写的**——人类的角色就发生了根本性转变。

OpenAI 的实验记录了旧范式失效的方式：

> "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified."

环境未充分指定（underspecified）是 Agent 失效的主要原因。**不是 Agent 能力不够，而是人类没有设计好 Agent 工作所需的环境**。

笔者认为，这个认知转变是过去一年 Agent 工程领域最重要的范式转变：**从「让 Agent 学会做事」到「为 Agent设计做事的环境」**。

## Harness Engineering 的核心框架

OpenAI 将这个新的工程学科称为 **Harness Engineering**——挽具工程。这个名字很精准：**不是控制 Agent，而是设计让 Agent 能够可靠发挥能力的框架**。

### 1. 反馈循环设计：Ralph Wiggum Loop

Agent 工程中最重要的机制是**反馈循环**。OpenAI 记录了他们的核心做法：

> "To drive a PR to completion, we instruct Codex to review its own changes locally, request additional specific agent reviews both locally and in the cloud, respond to any human or agent given feedback, and iterate in a loop until all agent reviewers are satisfied."

这个循环被他们内部称为 **Ralph Wiggum Loop**（来自《辛普森一家》里一个不断重复自己话的角色）。Agent 提交 PR → Agent review 自己 → 响应反馈 → 循环直到所有 reviewer 满意。

关键设计点：
- **Stop Condition（停止条件）** 不是"尝试更多次"，而是"所有 Agent reviewer 都满意"
- 人类可能 review PR，但不是必须
- 最终推几乎所有的 review 工作到 Agent-to-Agent

这解决了什么问题？**笔者认为，这解决了长任务可靠性问题**。当一个任务需要多轮迭代时，没有明确停止条件的 Agent 会陷入无限循环或过早终止。Ralph Wiggum Loop 提供了一个可验证的停止条件。

### 2. 渐进式上下文：不是百科全书，而是目录

Context 是 Agent 最大的限制。当上下文窗口被填满时，Agent 无法处理更多信息。

OpenAI 的实验记录了 AGENTS.md 作为巨型指令文档的失败：

> "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs—so the agent either misses key constraints or starts optimizing for the wrong ones."

他们发现：
-巨型指令文件让 Agent 模式匹配局部，而不是全局导航
- 规则太多等于没有规则
- 单个 blob 难以机械检查（覆盖率、新鲜度、所有权），漂移不可避免

解决方案是**渐进式上下文**（Progressive Disclosure）：

```
AGENTS.md (100行) = 目录 → 指向 docs/ 里的深层文档
```

- Design文档：索引 + 验证状态 + 核心原则
- Architecture 文档：顶层领域和包分层图
- Quality 文档：产品域评级 + 架构层评级 + 差距跟踪
- Plans：临时轻量计划（小变更）+ 执行计划（复杂工作，带进度和决策日志）

这是一个让 Agent **从一个小而稳定的入口开始，然后学会在哪里寻找更多信息**的设计，而不是一开始就灌输所有信息。

### 3. 工作区状态管理：计划作为一等公民

OpenAI 另一个关键设计是**将计划作为一等公民**（First-class Artifacts）：

> "Active plans, completed plans, and known technical debt are all versioned and co-located, allowing agents to operate without relying on external context."

计划被版本化管理，与代码放在一起，而不是在外部工具里。这意味着：
- Agent 可以看到历史的计划和决策
- Agent 可以从完成的任务中学习
- 不依赖外部上下文，Agent 独立工作

笔者认为，这个设计解决了**跨 Session 记忆问题**。大多数 Agent 框架关注的是单次会话内的记忆，但 OpenAI 的方案是通过**版本化的工作产物**来实现跨 Session 的连续性。

### 4. Agent 自主维护：Doc-gardening Agent

最令人印象深刻的机制之一是 **Doc-gardening Agent**：

> "A recurring 'doc-gardening' agent scans for stale or obsolete documentation that does not reflect the real code behavior and opens fix-up pull requests."

一个定期运行的 Agent 扫描过时文档，并提交 PR 来修复。

这不是一个锦上添花的特性。**这是让 Agent 工程系统可持续运转的核心机制**——因为文档腐化是所有大型代码库的宿命，而如果 Agent 自己维护文档，这个负担就不会压在人类身上。

## 三层 Harness架构

综合 OpenAI 的实验和 Anthropic 的 containment 实践（见《How we contain Claude across products》），笔者认为 Agent 工程中的 Harness 架构分为三层：

| 层次 | 机制 | 作用 |
|------|------|------|
| **反馈循环层** | Evaluation Loop + Stop Condition | 让 Agent 知道何时停止、如何迭代 |
| **上下文层** | Progressive Disclosure + 知识分层 | 让 Agent 在有限上下文内获取所需信息 |
| **维护层** | Doc-gardening + Self-healing | 让 Agent 系统可持续运转而不需人工干预 |

三层缺一不可：
- 没有反馈循环层 → Agent 无法可靠完成长任务
- 没有上下文层 → Agent 被上下文窗口限制
- 没有维护层 → 系统随时间腐化

## 数据验证

OpenAI 的实验给出了具体的工程数据：

- **产出速度**：3.5 PRs/工程师/天（从第1 天到第 5 个月，吞吐量持续增长）
- **代码总量**：约 100 万行代码
- **PR 总量**：约 1,500 个 PR
- **团队规模**：从 3 名工程师增长到 7 名工程师
- **单次运行时长**：单个 Codex 运行可工作6 小时以上（通常在人类睡觉时）

**笔者认为**，3.5 PRs/工程师/天这个数字最有说服力。它意味着人类工程师从"执行者"转变为"系统设计者"后的实际产出——不是更少，而是更多。

## 给我们的工程启示

1. **从"写代码"到"设计环境"的转变需要刻意练习**。大多数团队失败的原因是直接让 Agent写代码，却没有先设计好 Agent 工作所需的环境。

2. **Stop Condition 是工程问题，不是提示词问题**。"Keep working until done" 不是一个有效的指令；需要明确可验证的停止条件。

3. **上下文管理是核心工程挑战**。渐进式上下文不是一个技巧，而是整个 Agent 工程系统的基础架构。

4. **Agent 维护 Agent 是可行的**。Doc-gardening Agent证明了 Agent 可以负责自己的文档维护，而不是依赖人类。

---

## 原文引用

1. "Humans steer. Agents execute." — [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
2. "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified." — [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
3. "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs." — [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
4. "Active plans, completed plans, and known technical debt are all versioned and co-located, allowing agents to operate without relying on external context." — [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
5. "A recurring 'doc-gardening' agent scans for stale or obsolete documentation." — [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)

---

**相关工程机制**：Ralph Wiggum Loop（反馈循环）| Progressive Disclosure（渐进式上下文）| First-class Artifacts（工作区状态管理）| Doc-gardening（自主维护）