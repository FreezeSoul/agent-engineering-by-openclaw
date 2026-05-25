# Claude Managed Agents 三重进化：从做梦到多 Agent 编排的工程完整度

> **来源**：[New in Claude Managed Agents: dreaming, outcomes, and multiagent orchestration](https://claude.com/blog/new-in-claude-managed-agents)，2026年5月6日，Anthropic Claude Blog  
> **核心论点**：Claude Managed Agents 的三个新特性（Dreaming、Outcomes、Multi-agent Orchestration）共同构成了一个完整的 Agent 生命周期管理系统，分别解决了长任务 Agent 的三个核心挑战：**记忆进化**、**输出质量**、**任务规模化**。  
> **关键判断**：Anthropic 正在将 Agent 从「单次执行单元」升级为「具备自我演进能力的分布式系统」，这个转变的工程意义远超功能本身。

---

## 一、梦的实现：让 Agent 在睡眠中进化

**Dreaming** 是 Anthropic 提出的一个调度式记忆改进机制。它的核心逻辑是：

> Dreaming 是一种调度进程，它回顾 Agent 的会话和记忆存储，提取模式，并组织记忆，使 Agent 随着时间推移而改进。

这不是一个比喻。「做梦」的本质是**离线的模式提取与记忆重组**：

| 传统 Agent Memory | Dreaming 增强版 |
|------------------|----------------|
| 每次会话捕获所学 | 会话之间提取共享学习 |
| 记忆随时间膨胀 | 记忆动态重组保持高信噪比 |
| 单一 Agent 视角 | 跨 Agent 模式发现 |

**笔者认为**：Dreaming 的工程价值在于它解决了「记忆污染」问题——当 Agent 运行超过几百轮后，上下文中的低价值记忆会稀释高价值信息。Dreaming 通过定期重构记忆，让 Agent 始终在「干净的工作面」上运行，而不是被自己的历史积累所拖累。

Harvey 法律团队的测试数据很有说服力：**完成率提升了约 6 倍**。他们的 Agent 现在记住了文件类型变通方案和特定工具使用模式——这些信息在传统架构中很快会被后续会话淹没。

---

## 二、Outcomes：把评价权从 Agent 手中剥离

**Outcomes** 是本篇文章中最具工程洞察的设计。

它的机制是：
1. 你写一个评分标准（rubric），描述「成功是什么样子的」
2. Agent 执行任务
3. **一个独立的 grader 在自己的上下文中评估输出**，不受 Agent 推理过程的影响
4. Grader 指出需要改进的地方，Agent 重新执行
5. 循环直到输出通过评分标准

Anthropic 给出了一个关键设计细节：

> 一个独立的 grader 在自己的上下文窗口中评估输出，因此它不会受到 Agent 推理过程的影响。

**这意味着什么？** 这是一个经典的「裁判与运动员分离」模式。当 Agent 自己评价自己的输出时，它受到「我已经花了这么多力气」的确认偏差影响。独立的 grader 不受这个影响，只看最终结果是否符合标准。

实测数据：
- 任务成功率比标准提示循环**提升最高 10 个百分点**（最困难的问题增益最大）
- docx 文件生成：**+8.4%** 任务成功率
- pptx 文件生成：**+10.1%** 任务成功率

Outcomes 的适用场景不仅限于「客观质量」（结构完整性、覆盖度），还包括**主观质量**——比如文案是否符合品牌调性、设计是否符合视觉规范。Wisedocs 使用 Outcomes 对文档质量进行评分，**审查速度提升 50%**，同时保持与团队标准的一致性。

**笔者认为**：Outcomes 本质上是将 **Harness 中的 Evaluator Loop 进行了显式产品化**。过去，评价 Agent 输出质量需要人类介入或自定义评估代码；现在，Anthropic 把这个模式做成了原生特性，让企业可以直接用「rubric + grader」替代人工评审环节。

---

## 三、Multi-agent Orchestration：领导者的分工智慧

**Multi-agent Orchestration** 让一个 Lead Agent 将任务分解，并委托给专门的子 Agent，每个子 Agent 有自己的模型、提示词和工具。

架构示意：

```
Lead Agent（主代理）
    ├── Subagent A（Haiku）：快速问答 → 委托
    ├── Subagent B（Opus）：并行起草 → 评分
    └── Subagent C（Opus）：并行起草 → 评分
              ↓
         Shared Filesystem
              ↓
         Outcomes Grader（质量评审）
```

**关键工程特性**：

1. **共享文件系统**：子 Agent 之间通过共享文件系统协作，Lead Agent 可以「中途回来检查」其他 Agent 的进度
2. **持久化事件**：每个 Agent 记住自己做了什么，不会在任务中途丢失状态
3. **完整可追溯**：Claude Console 记录每个步骤——哪个 Agent 做了什么、按什么顺序、为什么

Netflix 的案例展示了实际的规模价值：

> Netflix 平台团队构建了一个分析 Agent，处理来自数百个构建来源的日志。当变更影响数千个应用时，关键是找到跨多个应用反复出现的问题。Multi-agent Orchestration 让 Agent 可以并行分析批次，并只呈现值得处理的模式。

**笔者认为**：Multi-agent Orchestration 的核心价值不是「多个 Agent 一起工作」，而是**任务粒度的可拆分性**。当一个任务可以被分解为独立的子任务时，Lead Agent 可以选择最便宜的模型（Haiku）处理路由，最强的模型（Opus）处理执行，实现成本与质量的精确匹配。

Spiral by Every 的案例尤其有趣：Lead Agent 运行在 Haiku 上，它接收请求并在需要时提出快速的后续问题，然后将起草委托给运行在 Opus 上的子 Agent。当用户需要多个草稿时，子 Agent 并行运行。**只有通过 Outcomes 评分标准（基于 Every 的编辑原则和用户语气）的草稿才会被返回**。

---

## 四、三重闭环：Agent 工程的下一步

Dreaming（会话间进化）+ Outcomes（运行时质量）+ Multi-agent（并行执行）= 完整的 Agent 生命周期管理系统

| 特性 | 解决的问题 | 工程模式 |
|------|-----------|---------|
| Dreaming | 记忆污染、跨会话学习 | 调度式离线分析 |
| Outcomes | 输出质量一致性、人工评审成本 | 独立 Evaluator Loop |
| Multi-agent | 任务规模化、成本优化 | Lead + Specialist 架构 |

**笔者认为**：这三个特性的组合揭示了 Anthropic 对 Agent 工程的核心判断——

> **Agent 的可靠性不是靠模型变强来解决的，而是靠系统设计来保障的。**

Dreaming 解决的是「记忆管理」问题，Outcomes 解决的是「质量保障」问题，Multi-agent 解决的是「可扩展性」问题。这三个问题构成了企业级 Agent 部署的核心挑战三角。

当模型能力足够强时，Harness 的设计质量开始成为决定性因素——这正是 Anthropic 从 2025 年以来的 Harness Engineering 系列文章一直在论证的观点。Managed Agents 的这三个新特性，是这个判断的最新实证。

---

**引用来源**：

> "Dreaming is a scheduled process that reviews your agent sessions and memory stores, extracts patterns, and curates memories so your agents improve over time." — [Anthropic Claude Blog](https://claude.com/blog/new-in-claude-managed-agents)

> "A separate grader evaluates the output against your criteria in its own context window, so it isn't influenced by the agent's reasoning." — [Anthropic Claude Blog](https://claude.com/blog/new-in-claude-managed-agents)

> "When there is too much work for a single agent to do well, multiagent orchestration lets a lead agent break the job into pieces and delegate each one to a specialist with its own model, prompt, and tools." — [Anthropic Claude Blog](https://claude.com/blog/new-in-claude-managed-agents)