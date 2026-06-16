# 人类决定 WHAT，Agent 决定 HOW — 40万 Sessions 实证

> Anthropic 对约 40 万个 Claude Code Sessions 进行了隐私保护分析，时间跨度为 2025 年 10 月至 2026 年 4 月。结论颠覆了关于"AI 会取代程序员"的叙事：**在 coding task 上，每种职业的成功率几乎相同，决定成功的是领域专业知识，而非编程能力**。

---

## 一、颠覆性发现：不是看你会不会写代码

长期以来，业界存在一个隐含假设：AI 编码工具的核心用户是软件工程师，非技术人员只能"打辅助"。Anthropic 这次用 40 万 sessions 的数据把这个假设击碎了。

**核心数据**：在需要验证的 coding task 上（以 passing tests 或 committed work 为成功标准），每种主要职业的成功率**几乎相同**——软件工程师并不比律师、会计师或生物学家更高。

这个结论的深层含义是：**Agent 协作者需要的是"知道自己要什么"的能力，而不是"知道怎么做"的能力**。一个从未写过 Python 的会计师，只要能精确告诉 Claude 哪些对账规则必须在脚本中执行、哪个边缘情况需要在月末结账时被捕捉——这个人在该任务上就是"expert"。

> **引用原文**：*"A session in which a lawyer builds a script to automatically flag missing clauses across a folder of contracts is mapped into Legal Occupations, even if the session's work is primarily software."*
> — Anthropic, [Agentic coding and persistent returns to expertise](https://www.anthropic.com/research/claude-code-expertise)

这不是在说编程不重要——而是说，**在 Agent 时代，编程能力被降维成了执行细节，而问题理解能力被升维成了核心资产**。

---

## 二、分工法则：70% 的 planning decision 由人类做出

报告给出了一个精确的分工数据（基于隐私保护决策归因分类器）：

| 决策类型 | 人类做出比例 | Agent 做出比例 |
|---------|------------|--------------|
| **Planning decisions**（做什么、什么方案、什么算完成）| ~70% | ~30% |
| **Execution decisions**（改哪个文件、什么代码、什么命令）| ~20% | ~80% |

**分工模式**：人决定 WHAT to build，Agent 决定 HOW to build it。

这个分工不是理论推断，而是从 40 万个真实 sessions 的对话记录中归纳出来的。在典型 session 中，用户发送一条 prompt，Claude 会触发平均约 10 个 action chain（有时超过 100 个），每次输出约 2400 词。

关键细节在于：**Claude 在每个 prompt 之间的自主程度，与谁在做决策强相关**：
- 当用户保持了 >80% 的 execution decisions 控制权时，Claude 每个 turn 约执行 8 个 action
- 当 Claude 保持了 >80% 的 planning decisions 控制权时，Claude 每个 turn 约执行 16 个 action（翻倍）

也就是说：**你越把 HOW 的决策权移交给 Agent，Agent 的自主工作量就越大**。这与"给 Agent 越多 autonomy，它就能完成越多工作"的直觉一致——但前提是人类先做出了 WHAT 的决策。

---

## 三、专业度放大效应：expert 用户的 Agent 产出是 novice 的 2.7 倍

报告中最有工程参考价值的数据是**专业度与 Agent 产出之间的关系**：

| 用户专业度 | 每 prompt 的 Claude actions | 每 prompt 的文字输出 |
|-----------|--------------------------|-------------------|
| **Novice**（泛泛指令，无领域背景）| ~5 actions | ~600 words |
| **Expert**（精确指令，含领域知识）| ~12 actions | ~3,200 words |

Expert 用户触发的 action 数量是 novice 的 **2.4 倍**，输出文字量是 **5.3 倍**。

这个差距出现在**每一种工作模式和每一个任务价值等级**中，具有统计显著性（p < 0.001，控制了工作模式、任务价值、月份和模型家族后仍显著）。这意味着：

**"你给 Agent 的领域上下文越精确，Agent 的自主工作能力就越强。"**

这不是因为 expert 用户更会"提示工程"，而是因为他们**知道自己要什么，并能精确表达约束条件**。这直接对应了我们在 Cursor Agent Best Practices 中提到的 Harness 设计原则——高质量的指令系统（Instructions）是 Harness 三层架构的核心。

---

## 四、七个月趋势：调试减少，端到端任务增加

时间维度的数据同样值得关注（2025年10月 → 2026年4月）：

| 变化维度 | 2025年10月 | 2026年4月 |
|---------|----------|----------|
| **调试类 session 占比** | 33% | 19%（下降 42%）|
| **操作系统/部署类 session** | 14% | 21%（上升 50%）|
| **构建+数据分析类 session** | ~10% | ~20%（翻倍）|
| **平均任务经济价值** | 基线 | +27%（提升）|

调试占比下降是最有意思的信号。这说明两件事：

1. **用户学会了更精确地表达需求**，减少了因指令模糊导致的 bug 引入
2. **Agent 能力提升**，在同一任务上犯的错误减少

而端到端任务（部署、运行代码、分析数据）的占比上升，则印证了"Agent 正在向上移动，承担更完整的价值交付"的趋势——这正是我们在 Harness Engineering 中讨论的"Agent 从工具到异步工作力"的转变。

---

## 五、工程含义：这对 Agent 开发者意味着什么

这份报告的工程含义是直接的：

### 1. **Harness 的指令系统是核心杠杆**

Expert 用户之所以能触发 2.7 倍于 novice 的 Agent 产出，根本原因在于指令质量。高质量的指令不是"更长的 prompt"，而是：

- **精确的约束条件**（哪些边界情况必须处理）
- **可验证的成功标准**（怎样算完成）
- **领域相关的验证逻辑**（能识别 Agent 的输出是否正确）

这与我们在 Cursor Best Practices 中提炼的 Harness 三层架构完全吻合——Instruction System 是第一层，也是撬动 Agent 能力的最大杠杆。

### 2. **Planning decision 的保留是安全关键**

报告数据表明，用户保留了 ~70% 的 planning decisions。这个比例不是偶然的——它是用户在"给 Agent 足够的 autonomy"和"保留对目标方向的最终控制"之间找到的平衡点。

对于 Harness 设计者，这意味着：**过于激进的 autonomy 会让 Agent 在错误的方向上走得更远，而适度的 human-in-the-loop 是保持任务正确性的必要条件**。

### 3. **非软件人员的采用是下一波浪潮**

增速最快的非软件职业群体是管理、销售和法律人员。这意味着：
- 未来的 AI Coding 工具需要更好地支持**非代码工作流**（文档分析、流程自动化、决策支持）
- 领域专业化（legal、finance、science）的 Agent 配置会成为差异化竞争点

---

## 六、与本仓库其他文章的关联

本文与以下文章形成完整的 Agent Engineering 知识闭环：

| 文章 | 关联点 |
|------|--------|
| [Cursor Agent 最佳实践：Harness Engineering 系统指南](./practices/ai-coding/cursor-agent-best-practices-harness-engineering-2026.md) | 方法论：Instruction System 是 Harness 三层架构的核心 |
| [repository-harness: 多 Agent 工作区管理](./projects/hoangnb24-repository-harness-agent-workspace-790-stars-2026.md) | 工程实现：如何将仓库变成 Agent-ready 工作区 |
| [Anthropic Claude Code Sandboxing](./deep-dives/anthropic-claude-code-sandboxing-containment-2026.md) | 安全机制：Agent 执行边界的工程实现 |

本文提供了**实证数据层**：为什么 Instruction System 重要（expert → 2.7x Agent 产出），为什么保留 Planning decision 重要（防止 Agent 在错误方向上 autonomy 过度），以及非软件人员的 Adoption 趋势意味着什么。

---

## 七、结论

这份报告给出了一个清晰的信号：

> **Agent 时代的能力方程式正在被改写：领域专业知识 × Agent 放大 = 工作产出。编程能力仍然是重要的工程技能，但它不再是从业者的唯一护城河。**

对于 Agent Engineering 实践者，这意味着：
- **投资你的领域知识**，而不是花时间学习更多"AI 提示技巧"
- **投资高质量的 Harness 指令系统**，这是放大 Agent 能力的最小成本路径
- **为非软件人员设计 Agent 工作流**，这是下一波采用的主要来源

这不是一个悲观的结论——它是给所有认真理解自己领域的人的一个机会：**只要你知道自己要什么，Agent 就能帮你把它构建出来。**

---

**引用来源**：Anthropic, *Agentic coding and persistent returns to expertise*, 2026. https://www.anthropic.com/research/claude-code-expertise