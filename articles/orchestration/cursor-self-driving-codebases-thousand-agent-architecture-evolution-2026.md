# Cursor「自驱动代码库」复盘：千Agent协作的架构演进实录

> 🔴 **本文来源**：Cursor Engineering Blog — [Towards self-driving codebases](https://cursor.com/blog/self-driving-codebases)（2026-02-05）
> 作者：Wilson Lin | 19 min read

---

## 核心论点

Cursor 的研究团队在 2026 年初完成了一个人类旁观、Agent 主导的代码库构建实验：数千个 Agent 协同工作数周，向一个浏览器仓库提交了绝大多数 commit。这个结果本身不稀奇——但**到达这个结果的路径**值得深挖：它不是一次设计出来的，而是经历了几轮失败的结构演化，每一次失败都揭示了多 Agent 协作中某种结构失效的机制。

笔者认为，这篇文章最有价值的部分不是最终的三层架构，而是**过程中的每一个「为什么失败」**——它们构成了多 Agent 协作工程化的真实知识体系。

---

## 一、起点：单 Agent 的天花板

项目开始于 Wilson Lin 的个人研究：用 Opus 4.5 构建一个完整的浏览器引擎。初始方案很简单：**prompt → 模型写代码 → 人工持续 nudging**。

结果不出意外地失败了。模型很快丢失任务线索、频繁宣告成功（实则远未完成）、在复杂实现细节上陷入循环。

> 「它展现出了深层知识和智能的迹象。它能在小块代码中写出好东西。但任务是毁灭性的。」

这句话的潜台词是：模型的能力上限不是问题，**任务的分解与上下文管理才是**。

---

## 二、第一轮演化：多 Agent 并行（失败）

解决方案很自然：拆解依赖图，并行启动多个 Agent。Wilson Lin 手动为每个任务生成 Agent，在 Agent 停止时 nudging。

这个方案提升了吞吐量，但结果仍然糟糕。核心问题：Agent 之间无法通信、无法感知项目整体状态、无法相互反馈。系统需要更动态的协调机制。

### 2.1 协作文件的失败

第一版多 Agent 协作方案是「共享状态文件」：所有 Agent 能看到谁在做什么、决定接下来做什么、写入状态更新。

这几乎是所有多 Agent 系统的直觉起点——然后它迅速崩溃了：

- **锁竞争**：20 个 Agent 实际吞吐量降至 1-3 个，大量时间在等锁
- **锁管理错误**：Agent 忘记释放锁、尝试非法解锁
- **任务碎片化**：没有 Agent 愿意承担大而复杂的任务，都倾向于做小而安全的变更

> 「Locking is easy to get wrong and narrowly correct, and more prompting didn't help.」

这句话直接点出了核心教训：**当系统需要协调时，prompt 不是解药，需要引入结构**。

---

## 三、第二轮演化：引入角色分层（成功）

放弃共享状态文件后，团队引入了一个明确的三层角色架构：

| 角色 | 职责 | 特点 |
|------|------|------|
| **Planner** | 将用户指令拆解为精确的任务步骤和交付物 | 规划前置，结构化输出 |
| **Executor** | 唯一的主责 Agent，负责确保计划被完整执行，可生成 Worker 子任务 | 单一责任 + 唯一 Owner |
| **Worker** | 执行被分配的子任务，提供线性扩展的吞吐量 | 窄任务，并行执行 |
| **Judge**（独立角色）| Executor 完成后，评判是否完成、是否需要新一轮迭代 | 独立的验证者 |

### 3.1 为什么这个结构有效

关键洞察是：**单一角色对整体结果负责，消除了一线执行者的协调负担**。

Worker 只需要专注于自己的子任务，不需要知道其他 Worker 在做什么、不需要担心全局状态、不需要决定是否有人占了冲突的模块。协调责任被集中到了 Executor，Judge 解决了「谁来定义完成」的问题。

这个模式后来在 Cursor 内部的 [scaling agents](https://cursor.com/blog/scaling-agents) 研究中进一步被验证：**Planner-Executor-Judge 的扁平三层结构**比完全扁平的多 Agent 网络更适合长时任务。

---

## 四、第三轮：连续执行器与稳定性工程

架构确定后，团队面临的下一个问题是：**如何在没有人干预的情况下，让系统在数天、数周内稳定运行**。

Cursor 团队实现了一个「连续执行器」（Continuous Executor），其核心工程机制包括：

### 4.1 Commit 正确性保障

> 「We implemented a 'commit correctness' check...」

系统在每次 Agent commit 前运行一套验证：代码是否可以编译、测试是否通过、是否有明显的路径冲突。这解决了一个在多 Agent 并行环境下极其常见的问题——**多个 Agent 同时修改同一模块导致的合并灾难**。

### 4.2 同步开销管理

> 「Synchronization overhead was reduced by...」

随着 Agent 数量增长，进程间的同步成本成为了新的瓶颈。团队通过减少不必要的状态同步频率、批量处理协调消息来控制开销。这里的工程权衡值得注意：**不是完全去掉同步，而是让同步只在必要时发生**。

### 4.3 基础设施的观测性

> 「We spent more time up front on proper observability into the system. We logged all agent messages, system actions, and command outputs, with timestamps so we could analyze and replay sessions.」

这条看似简单，但笔者认为这是整个系统最被低估的投资：**全量日志 + 可重放会话**使得用 Cursor 本身分析 Cursor 成为了可能——团队将日志喂入 Cursor，用 AI sifting 大规模数据，快速定位问题模式。

---

## 五、架构演进的总结性教训

Cursor 团队在文章结尾给出了一个架构演进的流程图，核心逻辑是：

```
扁平协作（失败）→ 共享状态文件（锁竞争）→ 
Planner-Executor-Workers-Judge（结构化角色）→ 
Continuous Executor（长时稳定性工程）
```

这不是一个预先设计好的架构图，而是一系列失败的堆叠——每一层失败都迫使架构向更清晰的角色分离方向演化。

**笔者认为最重要的工程洞见是**：多 Agent 系统中最难解决的协调问题，无法通过「更好的 prompt」来解决，必须通过**引入结构**（角色分层、职责边界、验证机制）来解决。Planner-Executor-Judge 的成功，不是因为这个结构本身有多优雅，而是因为它**将「协调」这个复杂问题集中到了一个 Agent（Executor + Judge）身上**，让 Worker 可以真正专注于窄任务执行。

---

## 六、与已有知识的关联

这篇文章的架构模式与多个已有知识体系形成了呼应：

1. **Anthropic 的 initializer + coding agent 模式**（`effective-harnesses-for-long-running-agents`）：两者都引入了「初始化 Agent」和「执行 Agent」的分离，不同的是 Cursor 在此基础上加入了 Judge 角色来处理「完成」的判断问题。

2. **Stripe 的「pre-push hooks」工程原则**：两者都强调了**验证前移**的价值——在 commit/push 阶段做检查，比在人工 review 阶段做检查成本低得多。

3. **Cursor 自己的 scaling agents 研究**：Planner-Executor-Judge 的三层模式在这篇「自驱动代码库」文章中得到了更完整的验证和解释。

---

## 结论

Cursor 的「自驱动代码库」实验，最有价值的内容不是「它成功了」，而是**「它是如何失败的，然后如何修正的」**。

多 Agent 协作的工程化，当前阶段最大的障碍不是模型能力，而是**结构设计能力**：如何设计角色、如何定义边界、如何引入验证、如何管理同步开销。Cursor 的这篇文章给出了一个真实的、带有失败记录的演进路径，而非一个「设计良好的架构图」。

**金句**：*「Locking is easy to get wrong and narrowly correct, and more prompting didn't help.」*——这句话几乎可以成为多 Agent 系统设计的警示铭文。

---

> **引用来源**：
> - Cursor Engineering Blog: "[Towards self-driving codebases](https://cursor.com/blog/self-driving-codebases)" by Wilson Lin, Feb 5, 2026
> - Cursor: "[Scaling agents research](https://cursor.com/blog/scaling-agents)" (相关背景)
> - Anthropic: "[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)" (Nov 2025)