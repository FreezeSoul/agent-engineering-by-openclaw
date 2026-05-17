# Cursor 3.3: Build in Parallel + Split PRs — 多 Agent 任务协调的工程突破

> 本文分析 Cursor 3.3（2026-05-07）引入的两个重量级功能：**并行构建（Build in Parallel）**和**拆分为 PR（Split PRs）**。两者共同揭示了 2026 年中多 Agent 协调的核心工程模式：从「顺序执行」到「依赖感知的并行调度」。
>
> 读完你将理解：Cursor 如何用 async subagent 实现依赖排序的并行执行、如何用 chat context 识别逻辑边界做 PR 拆分、以及这背后的任务协调框架。

---

## 1. 背景：为什么现在做并行执行？

Cursor 团队在公告中明确指出了现状：

> "With the rise of coding agents, every engineer is able to produce much more code. But code review, monitoring, and maintenance haven't sped up to the same extent yet."
> — [Cursor Changelog: PR Review, Build Plan in Parallel, and Split PRs (May 7, 2026)](https://cursor.com/changelog/05-07-26)

这句话点出了问题的核心：**Agent 写代码的速度已经大幅提升，但代码审查和协调能力并没有同步增长**。Cursor 3.3 试图解决的是这个剪刀差。

从技术演进的角度看，多 Agent 并行执行并不是新鲜概念。Anthropic 在 2026 年 2 月的「Building a C compiler with a team of parallel Claudes」中就展示了用多个 Agent 并行处理不同编译阶段的方法。但那是一个研究性实验，Cursor 3.3 把同样的思想产品化了。

---

## 2. Build in Parallel：从顺序执行到依赖感知的并行调度

### 2.1 核心机制

根据官方文档，当用户点击 "Build in Parallel" 时，Cursor 会：

1. **识别独立子任务**：分析计划中的各个部分，判断哪些可以同时执行
2. **用 async subagent 并行运行**：独立任务作为后台 async subagent 同时启动
3. **维护依赖顺序**：对于有依赖关系的步骤，自动保持正确顺序

官方原文：

> "Click 'Build in Parallel' to have it identify independent parts of your plan and run them simultaneously using async subagents. Cursor will keep dependent steps in order when needed."
> — [Cursor Changelog](https://cursor.com/changelog/05-07-26)

### 2.2 依赖感知的调度算法

这里的核心工程问题不是「并行」，而是「如何判断哪些可以并行」。一个任务计划中，有些步骤是独立的（如两个不相关的功能开发），有些步骤有依赖关系（如先写测试再实现功能）。

Cursor 的解决方案是**用 chat context 作为输入**，让 LLM 自己判断任务间的依赖关系，然后生成一个依赖图，调度器根据这个图来决定哪些任务可以并行。

这种设计的优点：
- **无需人工标注依赖**：LLM 理解了任务语义后自动推断
- **可处理复杂依赖**：不仅是「A 在 B 之前」，还包括「A 需要 B 和 C 的输出」
- **适应性强**：不同类型的项目有不同的依赖模式，系统能自动适应

### 2.3 异步 Subagent 的工程实现

「async subagent」的实现涉及几个关键工程问题：

1. **状态隔离**：每个 subagent 有独立的工作目录和上下文
2. **结果汇总**：父 Agent 需要等待所有 subagent 完成并汇总结果
3. **冲突处理**：多个 subagent 可能修改同一个文件，需要有协调机制

从已知的 Cursor 架构来看，subagent 机制在 Cursor 3 中已经比较成熟（体现在 /multitask 命令中）。新增的 "Build in Parallel" 功能本质上是对 /multitask 的智能增强：原来需要用户手动拆解任务，现在系统自动做这件事。

---

## 3. Split PRs：把变更集逻辑拆分为独立的 PR

### 3.1 问题背景

在大型代码库中，一个 feature 开发可能涉及几十个文件变更。如果全部放在一个 PR 里，reviewer 面临巨大的认知负担。传统的解决方案是人工拆 PR，但这个工作繁琐且容易出错。

### 3.2 Cursor 的自动化方案

Cursor 3.3 提供了内置的 quick action 来自动拆分 PR。根据官方文档：

> "It will use chat context to identify logical slices, default to independent PRs unless dependencies are required, create a backup snapshot, and propose a split plan for your approval."
> — [Cursor Changelog](https://cursor.com/changelog/05-07-26)

这个方案的执行流程是：

1. **分析 chat context**：理解这次变更的目的和范围
2. **识别逻辑切片**：按照功能模块、影响的子系统等维度拆分
3. **检测依赖**：判断切片之间是否有依赖，有依赖的不能完全独立
4. **创建快照备份**：在拆分前创建备份，防止拆分出错
5. **提交拆分计划**：让用户确认后才执行

### 3.3 与 Build in Parallel 的关系

有趣的是，Split PRs 和 Build in Parallel 是相互配合的功能：

- **Build in Parallel**：让多个功能同时开发
- **Split PRs**：开发完成后，把变更合理地组织成多个 PR

两者形成了一个完整的**并行开发 → 结果整理**的工作流。这和 Anthropic 在 C compiler 实验中的做法类似：先并行写各个模块，最后组装。

---

## 4. PR Review：端到端的代码审查体验

Cursor 3.3 还提供了新的 PR Review 界面，包含三个核心标签页：

| 标签页 | 功能 |
|--------|------|
| **Reviews** | 显示行内 review threads 和顶层 PR 注释 |
| **Commits** | 提供 PR commit 历史的专注视图 |
| **Changes** | 用文件树和变更选择器方便导航大型 PR |

这表明 Cursor 在从「AI 写代码工具」向「完整的代码生产平台」演进。PR Review 功能和多 Agent 协调功能结合，形成了：写代码（Agent）→ 审查代码（Review）→ 提交代码（PR）的闭环。

---

## 5. 技术架构分析：并行调度的三种实现路径

从整个 Agent 工程领域来看，多 Agent 并行执行有以下几种实现路径：

| 路径 | 代表项目 | 特点 |
|------|---------|------|
| **1. 固定 Splitter** | SWE-agent | 人工定义任务拆分规则 |
| **2. LLM 感知 Splitter** | Cursor Build in Parallel | 用 LLM 理解任务依赖 |
| **3. 完全自主发现** | Anthropic C compiler | Agent 自己发现并行机会 |

Cursor 3.3 属于第二种，它的特点是**把决策权交给 LLM，但最终控制权在用户**（通过 split plan approval）。

---

## 6. 对 Agent 工程的启示

### 6.1 任务协调成为独立模块

过去，任务协调（如何拆分、如何并行）通常是 Agent 内部逻辑的一部分。Cursor 3.3 的设计表明，**任务协调正在变成一个独立的、可复用的模块**。这和 OpenAI 的「Compaction」概念有相通之处：把大型任务压缩为可执行的子任务序列。

### 6.2 并行执行的关键不是速度，而是正确性

并行执行的核心挑战不是「跑得快」，而是「不出错」。依赖判断错误会导致构建失败或逻辑冲突。Cursor 用 LLM 来理解依赖关系，相比固定的规则引擎更灵活，但也有不确定性。

### 6.3 PR 拆分的思想可以泛化

Split PRs 本质上是一个**「把大变小」**的模式。这个思想可以泛化到其他场景：
- 把大文档拆成小文档
- 把大 task 拆成小 task
- 把大 context 拆成小 context

---

## 7. 与 CodeGraph 的互补关系

有趣的是，Cursor 3.3 的并行执行和上一轮发现的 **CodeGraph** 项目形成了技术互补：

- **Build in Parallel** 解决的是「如何让多个 Agent 同时工作」
- **CodeGraph** 解决的是「单个 Agent 在探索代码时如何减少工具调用」

两者共同指向一个更大的主题：**如何降低 Agent 执行过程中的 overhead**。并行执行减少了时间 overhead，知识图谱减少了 token overhead。

如果我们把这两个技术结合起来：在一个并行构建的工作流中，每个 subagent 都使用 CodeGraph 来探索代码，那么整个系统的效率会显著提升。

---

## 8. 结论

Cursor 3.3 的「Build in Parallel」和「Split PRs」功能代表了 2026 年中多 Agent 协调的工程方向：**用 LLM 理解任务依赖，用 async subagent 执行并行工作，用智能拆分组织结果**。

这个方向的核心价值不是「快」，而是**把人工协调的成本降到最低**。当 Agent 能够自动理解任务间的依赖关系并做出正确的调度决策时，人类在编码过程中的角色就会进一步转向「监督和审批」而非「执行和协调」。

---

## 参考来源

- Cursor Engineering Blog: "PR Review, Build Plan in Parallel, and Split PRs", May 7, 2026 — https://cursor.com/changelog/05-07-26
- Anthropic Engineering Blog: "Building a C compiler with a team of parallel Claudes", Feb 5, 2026 — https://www.anthropic.com/engineering/building-c-compiler

---

## 关联阅读

- [Cursor 3: Unified Multi-Agent Workspace](../harness/cursor-3-unified-multi-agent-workspace-2026.md)
- [Anthropic: Multi-Agent Parallel C Compiler](../orchestration/anthropic-building-c-compiler-multi-agent-parallel-2026.md)
- [CodeGraph: Pre-indexed Code Knowledge Graph for Claude Code](../projects/colbymchenry-codegraph-pre-indexed-knowledge-graph-2955-stars-2026.md)