---
title: Anthropic「当 AI 建造自己」：代码即基础设施的工程拐点
date: 2026-06-23
source: https://www.anthropic.com/institute/recursive-self-improvement
author: Anthropic Institute
tags: [anthropic, recursive-self-improvement, coding-agent, harness, autonomous-agent, swe-bench, metr]
topics: [AI Coding, Autonomous Agents, Engineering Harness, Code Authorship]
description: Anthropic 内部数据显示 80% 的代码已由 Claude 生成，8x 工程效率提升背后的核心不是模型本身，而是那套让模型能够自主工作多小时的工程 Harness——自动审查、成功率达标的反馈循环、跨 Agent 任务委托。
length: 3800
cluster: deep-dives
cluster_role: anchor
round: 495
---

# Anthropic「当 AI 建造自己」：代码即基础设施的工程拐点

> 原文：[When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement)（Anthropic Institute，2026 年 6 月）

## 核心命题

Anthropic 公布的数字令人震惊：截至 2026 年 5 月，Claude 参与了 Anthropic 自身代码库 **80%** 的代码合并。工程师人均产出（按代码行数计）在 2024 至 2026 年间提升了 **8 倍**。这不是因为模型突然变聪明了——而是因为一套被称为 **Harness** 的工程机制，终于让模型能够在长时任务中稳定自主运行。

笔者认为，这篇文章最重要的贡献不是数据本身，而是揭示了一个被低估的工程事实：**让 AI 稳定地产出代码，不只是「给个 prompt」这么简单**。真正的杠杆是那套围绕模型的反馈循环、审查机制和任务委托架构。

---

## 一、三个拐点：代码生成到代码建造的演变

Anthropic 内部把 AI 编程能力的演进划分为三个阶段——每个阶段都对应一次工程机制的跃迁，而非仅仅是模型能力的提升。

### 第一拐点（2021-2023）：人类驱动

> "People writing code and docs on laptops."

这是传统软件工程的常态：人类写代码，AI 提供建议。这个阶段的 AI 辅助工具（Copilot 早期版本）本质上是**增强型自动补全**，不改变工程师与代码的根本关系。

### 第二拐点（2023-2025）：AI 辅助执行

> "People used early chatbots to help with parts of the process, like generating short code snippets and copying the output into text editors."

LLM 开始被用于生成完整的代码片段，但人类负责整合、审查和部署。这个阶段的核心工程挑战是**上下文窗口限制**——模型无法保持对大型代码库的理解，导致输出的代码与整体架构脱节。

### 第三拐点（2025-2026）：Coding Agent

> "As the agents became more capable, they were able to write and edit code on their own, sometimes entire files."

Claude Code 发布后，Agent 能够自主读写文件、运行测试、执行多步骤调试循环。但这个阶段的关键工程问题是什么？**Harness 的缺失**。早期的 Agent 在复杂任务中极易迷失——没有清晰的反馈机制，没有成功率追踪，任务一旦遇到意外就无法恢复。

### 第四阶段（今天）：自主 Agent

> "Agents can now run code themselves and delegate hours of work to other agents."

这是当前阶段的标志：Agent 不再只是执行单任务，而是能够把任务委托给其他 Agent，形成**任务传递链**。这要求工程系统具备：任务状态持久化、跨 Agent 通信协议、以及一套让人类能够审计 Agent 决策的审查机制。

```
人类设定目标
    ↓
Claude Agent 自主执行（多步骤、跨文件）
    ↓
自动 Claude Reviewer 审查（Bug/安全/缺陷）
    ↓
成功则合并；失败则反馈循环重试
    ↓
复杂任务 → 委托给子 Agent（跨 VM/云端）
```

---

## 二、80% 代码 authorship 的工程真相

80% 这个数字听起来像是「AI 替代了人类」，但 Anthropic 的原始描述更为精确：

> "The code that Claude writes, with the engineer directing and reviewing, rather than typing it themselves."

这不是「AI 写代码，人类审查」——而是「人类设定目标，AI 负责实现」。关键的区别在于**目标的表述和验证**仍然由人类主导，而**实现路径的选择和执行**已由 AI 控制。

### 为什么是 8x，而不是 10x 或 100x？

笔者认为，8x 这个数字反映的是当前 Harness 的上限，而非模型能力的上限。具体而言：

| 瓶颈 | 说明 |
|------|------|
| **目标描述成本** | 人类仍需将模糊的产品需求转化为可验证的工程目标，这一步无法自动化 |
| **审查深度** | 自动 Claude Reviewer 能捕捉 Bug 和安全漏洞，但无法判断「这是否符合产品意图」 |
| **复杂调试** | 当任务涉及多系统耦合（如分布式训练集群的 Debug），Agent 仍需大量人工引导 |

Anthropic 的内部数据也印证了这一点：在最开放式的任务（无清晰规格说明）上，Claude 的成功率在 2026 年 5 月达到了 **76%**，较六个月前提升了 50 个百分点。这意味着仍有 24% 的高端任务需要人类深度介入。

---

## 三、Engineering Harness：让 AI 稳定工作的核心机制

这篇文章最值得深入分析的不是 productivity 的数字，而是 Anthropic 围绕 Claude Code 构建的那套 **Harness 机制**——这是真正让 AI 从「辅助工具」升级为「协作者」的关键。

### 3.1 自动 Claude Reviewer

Anthropic 在代码合并流程中引入了强制性的自动 Claude Reviewer：

> "Proposed changes to our codebase are now read by an automated Claude reviewer that looks for bugs, security flaws, and other defects before it can merge."

这不是普通的 Lint 工具或静态分析——这是一个专门针对 Claude 生成代码特点训练的审查模型。Anthropic 用这个工具做了回溯分析，发现如果历史上每个 PR 都经过 Claude Reviewer 审查，本可以捕获约 **三分之一** 的线上事故 Bug。

笔者认为，这揭示了一个重要的设计原则：**AI 生成的代码需要 AI 级别的审查**。传统的人工 Code Review 在面对 AI 生成代码的高产量时是不可扩展的——当 AI 以 8x 的速度产出代码时，人类无法以同等速度审查每一行。

### 3.2 成功率反馈循环

Anthropic 内部追踪了 Claude Code Agent 在不同难度任务上的成功率，并将其作为模型迭代的核心指标：

> "Changes in workloads can lead to short-term fluctuations in success rates."

关键设计：成功率的判定是由 Claude Judge 完成的——即用另一个模型评估当前模型在任务中的表现。这形成了一个**自我评估的反馈循环**：

```
任务执行 → Claude Judge 评分 → 反馈给模型 → 调整策略 → 重新执行
```

这个机制解决了 AI Coding Agent 的一个核心问题：**如何判断任务完成了？** 传统做法是人工验证，但在长时任务中，人工验证的频率本身就是瓶颈。

### 3.3 任务委托与跨 Agent 协作

Anthropic 提到的最高级能力是 Agent 向其他 Agent 委托任务：

> "Agents can now run code themselves and delegate hours of work to other agents."

这对应了多 Agent 协作中的 **A2A（Agent-to-Agent）协议**雏形。在 Anthropic 的内部实践中，这意味着：
- 主 Agent 接收人类的工程目标
- 主 Agent 将任务分解为子任务
- 子 Agent 在独立环境中执行（如独立 VM）
- 主 Agent 汇总结果并向人类汇报

这不是简单的并行处理——它要求系统具备**跨会话状态传递**、**信任边界划分**和**任务接力的恢复机制**。

---

## 四、Benchmark 视角：能力上限在哪里？

Anthropic 引用了几个关键 benchmark 来论证 AI 能力的加速趋势：

| Benchmark | 起点（2024） | 当前（2026） | 意义 |
|-----------|------------|-------------|------|
| **SWE-bench** | 低个位数 | 接近饱和 | 模型已能在真实开源代码库中独立修复 Bug |
| **CORE-Bench** | ~20% | 接近饱和 | AI 已能复现已有论文的研究结果 |
| **METR（长任务）** | ~4 分钟人类等效 | ~12 小时人类等效 | Agent 工作时间窗口扩展了 180 倍 |

笔者认为，这些数字的意义不在于「AI 已经很强」——而在于**工程化的障碍已经被突破**。SWE-bench 饱和意味着在软件工程这个特定领域，AI 已经具备了独立解决真实问题的基础能力。下一步的竞争不在于 benchmark 分数，而在于**如何把这种能力产品化并可靠地交付给开发者**。

---

## 五、笔者观点：Harness 是下一个工程前沿

读完这篇文章后，笔者认为最被低估的信息是：**Anthropic 的核心竞争力不是模型本身，而是那套围绕模型的工程系统**。

当行业讨论「AI Coding」时，大部分注意力集中在模型能力（GPT-5、Claude 4.5、o4-mini）。但 Anthropic 的实际产出逻辑是：

1. **模型能力**提供了可能性的边界
2. **Harness 工程**决定了这个边界被实现的效率
3. **组织文化**决定了新工具有多快被采纳

> "We don't reward people for how many lines of code they write; rather, team members are producing more code simply because they're using AI systems to write more code."

这句话透露了一个关键信号：Anthropic 不是在用 AI 替代工程师，而是在用 AI **放大工程师的判断力**。工程师的核心价值从「写代码」转移到了「设定目标、验证结果、做出判断」。

---

## 六、工程启示

对于正在构建 AI Coding 能力的团队，笔者认为有几个关键启示：

**1. 代码 authorship 80% 是结果，不是目标**

追求「让 AI 写 80% 的代码」本身没有意义。真正的杠杆是那套让 AI 能够稳定工作的 Harness——没有反馈循环和审查机制，提高 authorship 只会引入更多技术债。

**2. 反馈循环的密度决定 AI 产出质量**

Anthropic 的成功很大程度上依赖于高频的反馈循环（Automated Reviewer + Success Rate Tracking + Claude Judge）。这意味着**评估基础设施和模型能力同等重要**。

**3. Agent 委托是下一个工程难题**

当 Agent 能够自主委托子任务时，工程系统的复杂度从「管理单个 Agent」升级为「管理多 Agent 协作网络」。这要求新的工具链：任务分解、状态传递、信任边界、审计日志。

**4. 安全审查需要 AI 原生化**

Claude Reviewer 的回溯分析揭示：如果用 AI 审查 AI 生成的代码，可以捕获三分之一的历史线上事故。这不是说 AI 审查比人工审查更好——而是**当代码量和复杂度超过人类审查能力时，AI 审查是唯一可扩展的选项**。

---

## 结语

Anthropic 的这篇文章提供了一个难得的第一手视角：不是外部观察者的分析，而是亲历者的数据和方法论总结。

最让笔者印象深刻的不是 8x 的 productivity 数字，而是这句话：

> "I started leaning hard into Claudifying about a year ago. That's been a crazy adventure and it's now been ~5 months since I last wrote any code myself." — Anthropic employee

这不只是一个工程师的 productivity 故事。这是软件开发历史上，第一次有顶级 AI 公司的工程师公开宣布「我已经 5 个月没写代码了」——而他们的产出却在加速增长。

当「写代码」不再是工程师的核心活动时，工程师这个角色的定义正在被改写。而那套让这一切成为可能的 Harness 工程，正在成为 AI 时代最重要的工程学科之一。