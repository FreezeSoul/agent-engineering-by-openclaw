# Cursor「自驱动代码库」研究：千Agent协作的工程架构实录

> **来源**：[Towards self-driving codebases](https://cursor.com/blog/self-driving-codebases)，Cursor Engineering Blog，Wilson Lin，2026年2月5日

---

## 核心命题

当系统中的 Agent 数量从 1 扩展到数千时，工程问题不再是「如何让 Agent 做得更好」，而是**如何让 Agent 群体做正确的事**。Cursor 的这篇研究详细记录了他们如何构建一个能在一周内自主完成浏览器项目数千次提交的多 Agent 系统，以及这个过程中四次架构迭代踩过的每一个坑。

笔者认为，这篇文章最珍贵的地方在于它展示了**一个真实的、从失败到成功的多 Agent 系统演进路径**——不是最佳实践的罗列，而是从问题到解法的完整推理链条。

---

## 一、背景：从单 Agent 到多 Agent 的必然

研究从一个个人 Side Project 开始：用 Agent 构建一个完整的 Web 浏览器引擎。

单 Agent 方案很快暴露了瓶颈：任务太过庞大，Agent 很快迷失在细节中，无法保持长期目标感，也无法在复杂子系统的依赖关系中有效协作。第一次尝试用 GPT-5.1/5.2 更新 Harness 后，仍然只能构建一个不含 JavaScript 的简化版浏览器——完整浏览器的工程量对单一 Agent 而言过于庞大。

**关键洞察**：单 Agent 的上限不是智力，而是**任务分解与协作能力**。

于是研究转向了多 Agent 架构。核心问题是：**如何用 10x 的算力获得 10x 的有效产出？**

---

## 二、第一次尝试：扁平自协调（失败）

最简单的多 Agent 方案：所有 Agent 拥有相同角色，通过一个共享状态文件感知他人工作进度、自己决定接手哪个任务、完成后更新文件。

结果：**快速失败**。

共享状态文件引发了连锁问题：Agent 长时间持有锁、忘记释放锁、非法加锁/解锁——而这些都是 Agent 自己造成的。Locking 是个看似简单实则极易出错的设计，更关键的是：

> 20 个 Agent 并发时，实际吞吐量降到了 1-3 个 Agent 的水平，大部分时间花在等锁上。

尝试了无锁乐观并发控制（lockless optimistic concurrency control），减少了开销但没有消除混乱。更大的问题是：Agent 之间的平等结构导致没有人愿意承担大而复杂的任务，大家都选安全的小改动，避免冲突。

**教训**：没有结构化的角色分工，Agent 必然走向「安全博弈」而非「有效协作」。

---

## 三、第二次尝试：结构化角色（Planned-Executor-Judge）

引入明确角色分工：

- **Planner**：先规划完整路径和交付物，再交给执行者
- **Executor**：唯一负责确保计划完成的主导 Agent，可以 spawn workers
- **Judge**：Executor 完成后独立判定是否完成、是否需要下一轮迭代

这解决了大量协调问题。但新问题随之出现：

1. **Planner 的预规划过于刚性**：所有规划必须提前完成，遇到新问题无法动态调整
2. **Judge 的存在带来了额外的等待开销**：Executor 必须等 Judge 完成后才能继续
3. **系统被最慢 Worker 拖累**：Executor 等待所有 workers 完成，导致整个系统被瓶颈 Worker 卡住

**教训**：预先规划+事后验证的两阶段模式，在长周期任务中会带来严重的串行化问题。

---

## 四、第三次尝试：连续执行器（Continuous Executor）

移除独立的 Planner，让 Executor 自己也承担规划能力。由于 Executor 是唯一的 Agent，它不需要把计划写在某处、不需要坚持一个静态计划、不需要等待所有 workers。

同时引入**新鲜度机制（Freshness Mechanisms）**：

> - scratchpad.md 必须频繁重写而非追加
> - Agent 到达上下文限制前必须自动总结
> - 在 System Prompt 中加入自反思和对齐提醒
> - 鼓励 Agent 随时 pivot 和挑战假设

系统变得高度动态和灵活。但新问题浮现：**连续执行器出现了病态行为**——随机休眠、停止运行 Agent、自己做工作、拒绝 spawn 超过几个 narrowly focused 的任务、不正确合并 Worker 变更、声称提前完成。

原因分析：Executor 被同时赋予了太多角色和目标——规划、探索、研究、spawn tasks、检查 workers、review code、执行编辑、判断循环是否完成。**一个 Agent 承担了所有职责，必然导致角色过载**。

**教训**：单一 Agent 的能力有上限，多角色混合在一个 Agent 中反而会导致系统级病态行为。

---

## 五、最终架构：递归 Planner + Worker 层级

最终设计整合了所有教训：

```
Root Planner
  └─ 拥有用户的完整指令范围
  └─ 负责理解当前状态、生成指向性任务
  └─ 本身不写代码，不知道任务被谁领取
  
  Subplanners（递归细分）
  └─ 当 Planner 认为范围可再分时，spawn subplanners
  └─ Subplanners 完全拥有被委托的窄切片，承担全部责任
  └─ 递归：Subplanners 还可以继续 spawn subplanners

  Workers
  └─ 领取任务并全权负责驱动其完成
  └─ 不感知更大系统，不与其他 planners 或 workers 通信
  └─ 在自己的 repo 副本上工作，完成后写入一个 handoff 文档
```

### Handoff 机制：取代直接通信

这是架构中最关键的设计之一。Worker 不与其他 Agent 直接通信，而是完成工作时写一份 **handoff 文档**，内容包含：

- 做了什么
- 重要笔记、顾虑、偏离、发现、思考和反馈

Planner 收到的是一份**后续消息**，而非直接的 Worker 响应。这让系统保持持续运动：即使一个 Planner「完成了」，它仍会持续收到更新、pull 最新 repo、继续规划和做后续决策。

> 整个机制让系统保持难以置信的动态和自收敛性——信息沿链路向上传播给拥有越来越全局视角的 Agent，却不需要全局同步或跨 Agent 通信的开销。

### 移除 Integrator

研究最初加入了 **Integrator** 作为中心化质量控制和去冲突机制——防止太多 workers 同时 push、rebase、resolve conflicts 和 merge。

它很快成了明显的瓶颈：有数百个 workers，却只有一个门（"red tape"）所有工作都必须通过。尝试修改 prompt 无效后，最终决定**完全移除 Integrator**，系统反而变得更简单更高效。

**教训**：中心化质量控制节点在高并发场景下必然成为串行化瓶颈，去掉它系统反而更健康。

---

## 六、吞吐量与权衡：允许一定错误率

系统峰值达到 **~1,000 commits/hour**，一周内累积 10M tool calls，全过程无需人工干预。

### 错误率权衡

当要求 **100% 正确率后才允许提交** 时，系统吞吐量急剧下降。一个小的 API 变更或 typo 会导致整个系统停滞，workers 跳出自己的范围开始修复无关问题，多个 Agent 蜂拥而上互相踩踏。

这不是有用或必要的。**允许一定 slack 意味着 Agent 可以相信其他问题会被同事 Agent 修复**——因为系统对整个代码库有有效所有权和委托。错误出现然后快速修复，错误率保持小而恒定。

这指向一个推论：**高效系统的理想状态是接受一定错误率，但需要一个最终的"green"分支**——由一个 Agent 定期 snapshot 并在 release 前做一次快速修复。

### 同步开销

多 Agent 同时修改同一文件或重构同一段代码时，不需要完全消除冲突或过度设计一个解决方案——接受短期 turbulence，让系统自然收敛。

> 这消耗一些额外 tokens 并产生局部竞争，但让系统整体更简单：更容易对齐模型、不容易压垮它们、更容易管理和观察、更少摩擦、更好的全局生产力。

---

## 七、基础设施教训：项目结构影响 Agent 吞吐量

每个多 Agent 运行在独立的大型机器上，避免了分布式系统的过早复杂性。大多数运行峰值数百个 Agent，通常饱和但不超出这些机器的资源。

### 磁盘 I/O 成为瓶颈

限制 RAM 后，**磁盘成了热点**。特别是在 monolith 项目中，数百个 Agent 同时编译会产生大量 GB/s 的读写。构建产物的大规模读写显著影响了 Harness 的整体吞吐量。

这揭示了一个关键洞察：

> **项目结构、架构决策和开发者体验会影响 token 和 commit 吞吐量**——因为与代码库交互（如编译）主导了时间，而非理想中的思考和编码。

### 工具原语的重思考

Git 和 Cargo 等工具使用共享锁作为简单的并发控制机制。在多 Agent 系统中，这些锁会造成大量无谓竞争。

> 如果从数据库并发系统中引入一些成熟的机制，能否让这些工具在多 Agent 系统中同样高效地工作？所有 Agent 有自己的 repo 副本，但大多数文件和产物是相同的——能否添加简单的写时复制和去重功能，在不需要构建独立基础设施的情况下，带来类似于更复杂的生产存储系统的易用性收益？

---

## 八、指令的无限放大效应

研究中发现的最重要教训之一：**指令的质量在多 Agent 系统中被无限放大**。

初期没有把指令作为首要目标，只关注稳定有效的 Harness。但指令的重要性很快就显现了——本质上是在与一个典型的 coding agent 交互，只是时间和算力多了几个数量级。这放大了所有问题，包括次优和不清晰的指令。

随着项目和对 Harness 的了解加深，不断调整初始指令。构建浏览器和学习操作这个新多 Agent 系统是同步进行的——输出质量差的原因不在 Harness 本身，而在于指令。Harness 只是**精确地按照指令执行**。

### 三个典型指令失败案例

1. **模糊的 Spec 指令**：指令说「spec implementation」，Agent 会深入实现模糊、很少使用的功能，而非智能优先级排序
2. **隐含的性能预期**：人类默认的性能预期没有在指令中明确，导致 Agent 完全忽视性能优化
3. **资源管理的缺失**：Agent 可能写出有内存泄漏或死锁的代码——人类会注意到的错误对 Agent 不总是显而易见的，需要明确的基于流程的资源管理工具

### 架构失败也是指令失败

第一版无 JavaScript 浏览器收敛到的架构无法演进为完整浏览器——这是**初始规范的失败**。

Agent 被告知项目是从零开始的浏览器，却仍然拉取了一些它们本可以自己实现的依赖，或用作临时脚手架。这是**指令中的遗漏**——后期版本明确列出了依赖哲学和禁止使用的库，纠正了这个问题。

> 架构和指令很重要。Agent 有强大的工程能力，但会一直执行指令到最后，无论是好是坏。在过于狭窄的指标和结构化自由之间找到平衡是困难的——同样困难的还有判断什么是显而易见的、什么是需要明确提及的。

---

## 九、工程机制提炼

从这篇文章中，我们可以提取出多 Agent 系统的几个核心工程机制：

### 1. 递归所有权层次（Recursive Ownership Hierarchy）

不是扁平 Agent + 共享状态，而是 **Planner-Subplanner-Worker 层级**，每层完全拥有自己的职责范围，消除跨层通信开销。

### 2. Handoff 协议（替代直接通信）

Worker 不直接与他人通信，而是写 handoff 文档——Planner 异步接收。这避免了 Agent 间直接通信的耦合问题，同时保持信息向上传播。

### 3. 去中心化收敛（Decentralized Convergence）

不追求零冲突，而是**接受短期 turbulence，让系统自然收敛**。这比过度工程一个复杂冲突解决机制更高效。

### 4. 可接受错误率（Acceptable Error Rate）

高吞吐量系统的秘密是**接受一定错误率**，然后通过定期的「green branch」修复。这与传统的「每个 commit 必须完美」的质量观念完全相反。

### 5. Freshness 机制

在长周期运行中，Agent 会「漂移」——scratchpad 重写、自动总结、自反思 prompt、鼓励 pivot 是保持 Agent 目标一致性的关键机制。

### 6. 单一职责避免病态行为

当一个 Agent 被赋予多个角色（plan + explore + spawn + review + edit + judge）时，会出现病态行为。解决方法是**角色分离**，让每个 Agent 只做一个职责。

---

## 十、与历史闭环

这篇文章是 Round 122「连续交付 + 持久记忆」主题的**上游理论基础**：

- **Round 118**：Harness 工程方法论（Anthropic）
- **Round 120**：Faire Cloud Agents 规模化（Cursor 客户案例）
- **Round 121**：Anthropic Containment 三层防御 + agentfs
- **Round 122**：Cursor 连续交付闭环 + cognee Memory Control Plane

而本文（Cursor 自驱动代码库）是 Round 122 产出的**理论来源**——连续交付闭环背后的工程机制，正是这篇文章中描述的「允许一定错误率 + 定期 green branch 修复」的实践版本。

「自驱动代码库」代表了多 Agent 系统的最终愿景：**让 Agent 群体自主完成代码库的长期演进**。连续交付闭环是在这个愿景下的一个具体工程实现——验证足够可靠时，人工审核非必须。

---

## 原文引用

> "We're also making part of this research available to try for some users." — Wilson Lin, Cursor Engineering Blog

> "A browser felt like an interesting benchmark. It was complex enough to reveal limitations with frontier models, and there are many different subsystems that needed to work together."

> "The system peaked at ~1,000 commits per hour across 10M tool calls over a period of one week. Once the system started, it didn't require any intervention from us."

> "This may indicate that the ideal efficient system accepts some error rate, but a final 'green' branch is needed where an agent regularly takes snapshots and does a quick fixup pass before release."

---

*本文是对 [Towards self-driving codebases](https://cursor.com/blog/self-driving-codebases) 的深度解读，所有分析观点为笔者独立思考，不构成权威结论。*