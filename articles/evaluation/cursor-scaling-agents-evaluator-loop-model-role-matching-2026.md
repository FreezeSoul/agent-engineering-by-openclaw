# Cursor 长时 Agent 的核心工程机制：Evaluator Loop 与模型角色匹配

> 本文深度分析 Cursor Scaling Agents 实验揭示的两个关键工程机制：（1）**Evaluator Loop** — 每轮结束时由 Judge Agent 判断是否继续，形成 Agent 长时工作的「心跳」机制；（2）**模型角色匹配** — 不同模型擅长不同角色，GPT-5.2 优于 Planner，GPT-5.1-Codex 优于 Worker。这两个机制共同解决了长时 Agent 工作流中最核心的两个问题：何时停止，以及谁来做什么。

## 核心论点

Cursor 的百人周并发 Agent 实验运行了数周，输出了百万行代码和万亿 Token。在这场规模实验中，最有价值的工程发现不是架构层面的「Planner/Worker/Judge」三角分工，而是两个更底层的机制：

1. **Evaluator Loop 是长时 Agent 的心跳**：每轮结束时，Judge Agent 判断是否继续下一轮。这不是简单的循环终止检查，而是 Agent 自我维持工作的核心机制——它让 Agent 能够在没有人类干预的情况下，决定「任务完成了多少、是否值得继续、以及接下来往哪走」。

2. **模型角色匹配决定系统上限**：不是所有模型都适合所有角色。GPT-5.2 在 Planner 角色表现优于专门为代码训练的 GPT-5.1-Codex。这个发现意味着 multi-agent 系统的瓶颈不只是架构，更是「角色-模型」的匹配质量。

---

## 一、Evaluator Loop：Agent 长时工作的「心跳」机制

### 1.1 问题：长时 Agent 何时停止？

人类开发者面临复杂任务时，会自然地判断：
- 这个任务做到什么程度算「完成」？
- 继续做下去的边际收益是否递减？
- 什么时候应该停下来等待人工review？

传统的 agentic coding 工具把这些问题完全抛给人类开发者。但 Cursor 的实验揭示，当 Agent 需要连续工作数周时，**人类无法持续提供这种判断**。Agent 必须能够自我评估工作状态，并决定是否继续。

### 1.2 Evaluator Loop 的工作方式

Cursor 的方案是每轮结束时引入一个 Judge Agent：

```
┌─────────────────────────────────────────────────────────┐
│  Planner → 生成 Task Queue                              │
│       ↓                                                 │
│  Workers → 抢接任务，并行执行                            │
│       ↓                                                 │
│  Judge Agent → 评估：「任务完成度如何？是否继续下一轮？」│
│       ↓                                                 │
│  继续？→ YES → 新一轮 Planner（带最新状态）             │
│  继续？→ NO  → 停止，输出最终状态                       │
└─────────────────────────────────────────────────────────┘
```

这与传统的 while 循环不同：
- **传统循环**：`while (hasMoreWork())` — Agent 自己判断是否有工作，退出条件是工作耗尽
- **Evaluator Loop**：`while (judge.shouldContinue())` — 独立的 Judge 评估整体状态，不仅是「有没有工作」，还包括「做得好不好」「值不值得继续」

### 1.3 为什么需要一个独立的 Judge？

Cursor 最初尝试让 Worker Agent 自己判断是否继续。但很快发现问题：Worker 会倾向于做「安全的小改动」而不是「困难的完整实现」。原因是：

- Worker 没有全局视野，不知道其他 Worker 在做什么
- Worker 的激励是「完成分配的任务」而不是「推动整体目标」
- 如果 Worker 能自己决定「做得够好了」，它就会停止，即使整体目标还差很远

独立的 Judge Agent 解决了这个问题：
- Judge 有全局视野，可以看到所有 Worker 的产出和整体进度
- Judge 的判断标准是「整体目标完成度」而不是「单个任务完成度」
- Judge 可以发现「虽然每个 Worker 都报告完成，但没有形成一个完整系统」这种分布式系统的典型失效模式

> 原文引用：
> "At the end of each cycle, a judge agent determined whether to continue, then the next iteration would start fresh. This solved most of our coordination problems and let us scale to very large projects without any single agent getting tunnel vision."
> — [Cursor Engineering Blog: Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)

### 1.4 Evaluator Loop 的工程挑战

Cursor 指出这个机制仍然不完美：

- **Judge 本身也可能疲劳**：连续运行数周后，Judge 的评估标准可能漂移
- **Agent 有时会跑太久**：Judge 没有有效干预，导致 Agent 在错误方向上走得太远
- **需要定期重启来对抗 drift**：即使有 Judge，仍然需要「定期清空上下文，重新开始」来对抗累积的状态漂移

这说明 **Evaluator Loop 不是银弹**——它是长时 Agent 工作的必要但不充分条件。

---

## 二、模型角色匹配：不是所有模型都适合所有角色

### 2.1 意外的发现

Cursor 实验中最反直觉的发现是：**模型角色匹配比模型整体能力更重要**。

他们测试了多个模型组合，发现：
- GPT-5.2 作为 Planner 优于 GPT-5.1-Codex（尽管后者专门为代码训练）
- GPT-5.2 在长时自主工作中表现更好：遵循指令、保持专注、避免 drift、准确完整地实现
- Opus 4.5 更容易提前放弃、走捷径、快速交还控制权

这意味着：

> 原文引用：
> "We now use the model best suited for each role rather than one universal model."
> — [Cursor Engineering Blog: Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)

### 2.2 为什么 Planner 需要不同的模型？

Planner 的核心能力是：
- **全局理解**：理解整个项目的目标、当前状态、剩余路径
- **长期规划**：制定跨越多轮、多人的任务分解策略
- **上下文保持**：在数周的任务中保持目标不漂移

Worker 的核心能力是：
- **局部执行**：准确完成分配的子任务
- **代码质量**：生成的代码符合项目规范
- **高效执行**：快速完成，不在细节上过度纠缠

这两种能力有冲突：一个擅长「想清楚再做」的模型，可能在「快速执行」上做权衡；一个擅长「边想边改」的模型，可能缺乏全局视野。

### 2.3 对 Agent 系统设计的启示

这个发现对 multi-agent 系统设计有深远影响：

| 设计维度 | 传统做法 | 新认识 |
|---------|---------|--------|
| **模型选择** | 选最强的通用模型 | 根据角色选最匹配的模型 |
| **角色分配** | 统一使用相同模型 | Planner/GPT-5.2, Worker/GPT-5.1-Codex |
| **成本优化** | 统一模型成本可预测 | 不同角色 Token 成本差异显著 |
| **扩展方向** | 增加更多 Worker | 优化模型-角色匹配比增加数量更有效 |

### 2.4 实践中的模型角色配置

Cursor 的做法是显式地为不同角色配置不同模型：

```
Planner: GPT-5.2 (强规划、长时专注、避免 drift)
Worker:  GPT-5.1-Codex (代码专用、快速执行)
Judge:   GPT-5.2 (全局评估、长期判断)
```

这与传统的「选一个最强模型做所有事」思路完全不同。在资源允许的情况下，这种角色匹配可能是未来 multi-agent 系统的标准配置。

---

## 三、从失败中学习：Lock 机制为什么失败

Cursor 的实验过程中经历了多次失败，这些失败本身揭示了 multi-agent 协作的深层挑战。

### 3.1 Lock 机制的失效

最初方案使用文件锁来实现任务分配的互斥：

- Agent 先获取锁，再修改共享状态文件
- 防止两个 Agent 同时认领同一任务

这个方案失败了，原因包括：

1. **锁持有时间过长**：Agent 在执行任务时被阻塞，锁无法释放
2. **Agent 崩溃导致死锁**：持有锁的 Agent 失败后，锁无法被回收
3. **性能瓶颈**：20 个 Agent 的并发实际变成了 2-3 个的吞吐率

### 3.2 乐观并发控制也不够

Cursor 随后尝试了乐观并发控制（OCC）：
- 读取状态不需要锁
- 写入时检查状态是否变化，变化则重试

这比悲观锁更简单也更健壮，但仍然无法解决根本问题：

> "With no hierarchy, agents became risk-averse. They avoided difficult tasks and made small, safe changes instead."

没有层级结构的 Agent 群体会出现「公地悲剧」——每个 Agent 都倾向于做安全的任务，回避困难任务，因为困难的任务失败概率高，会影响自己的「绩效」。

### 3.3 层级结构的必要性

最终的解决方案是引入明确的层级：

- **Planner**：有全局视野，负责制定任务分解策略
- **Worker**：只负责执行，不需要理解整体目标
- **Judge**：独立的评估者，判断是否继续

这种层级结构与人类的组织设计原则惊人地相似：
- 管理者（Planner）看全局、定方向
- 执行者（Worker）专注局部、高效率执行
- 审计者（Judge）独立评估、控制质量

> 笔者认为，这个类比不是巧合——multi-agent 系统的协作问题，本质上是分布式系统的组织问题，而人类在数百年的组织设计实践中已经积累了大量可迁移的经验。

---

## 四、对 Agent 工程实践的启示

### 4.1 长时 Agent 必须有 Evaluator Loop

如果你要构建一个需要连续工作超过几小时的 Agent 系统，必须考虑：

- **退出条件**：谁来判断任务是否完成？判断标准是什么？
- **健康检查**：Agent 跑偏了怎么办？谁来发现？
- **状态重置**：长时间运行后上下文膨胀怎么办？多久重置一次？

Cursor 的答案是：每轮有一个 Judge Agent 做判断，定期重置上下文。

### 4.2 模型选型要看角色匹配

不要只比较模型的基准测试分数，要问：

- 这个模型在「长时间保持专注」上表现如何？
- 这个模型在「理解复杂全局目标」上表现如何？
- 这个模型在「快速执行明确任务」上表现如何？

不同的角色需要不同的能力，选择模型时要匹配角色的需求。

### 4.3 简单的架构不一定是最差的

Cursor 的一个关键发现是：

> "Many of our improvements came from removing complexity rather than adding it."

他们最初设计的 Integrator 角色（专门做质量控制和冲突解决）反而创造了更多瓶颈。Worker 本身就能处理冲突，Integrator 只是在增加延迟。

这提示我们：**在加入新组件之前，先测试现有组件是否能自己解决这些问题**。

### 4.4 Multi-Agent 的瓶颈不在线性扩展

传统的观点是：增加更多 Agent，吞吐量线性增加。

Cursor 的实验表明：
- 20 个 Agent 可能只有 2-3 个的有效吞吐
- 真正的瓶颈是协调机制，不是 Agent 数量
- 在协调机制解决之前，增加更多 Agent 只是增加更多等待时间

---

## 五、结论：长时 Agent 的两个工程支柱

Cursor 的 Scaling Agents 实验揭示了长时 Agent 系统必须解决的两个核心工程问题：

**第一支柱：Evaluator Loop — Agent 的心跳机制**

没有心跳，Agent 要么永远不停（耗尽资源），要么永远不跑（等待人类指令）。Evaluator Loop 提供了第三种可能：Agent 自我评估当前状态，决定是否继续。这个机制不完美（Cursor 仍然需要定期重启来对抗 drift），但它是让 Agent 能够连续工作数周的基础。

**第二支柱：模型角色匹配 — 不是最强模型，是最合适的模型**

GPT-5.2 作为一个通用模型，在 Planner 角色上打败了专门为代码训练的 GPT-5.1-Codex。这说明 multi-agent 系统的瓶颈不只是架构设计，更是「谁来做这个角色」的选型问题。未来，agent 系统设计者可能需要为每个角色专门测试和选型，而不是选一个通用最强模型。

这两个机制共同回答了长时 Agent 的核心问题：**谁来做什么，以及做到什么时候**。这两个问题不解决，Agent 就只能做短时任务，无法真正实现持续工作。

---

## 备选标题

1. **Cursor 百人周 Agent 实验：Evaluator Loop 是长时工作的心跳** — 策略：好奇心缺口（28 单位）✅
2. **为什么 GPT-5.2 比 Codex 更适合当 Planner** — 策略：反直觉数据冲击（26 单位）✅
3. **长时 Agent 的两个工程支柱：心跳机制 + 角色匹配** — 策略：痛点共鸣（28 单位）✅