# 上下文工程：Agent 的注意力经济学

> 平台：Anthropic Engineering | 字数：约3200字 | 调性：工程深度 + 架构视角

---

## 核心观点

**上下文是 Agent 唯一的货币——不是越多越好，而是越准越值钱。**

LLM 的上下文窗口是有限的经济资源。当 Agent 需要处理的任务跨越数万 Token 时，如何让最强的能力集中在最高价值的决策上，是上下文工程的核心命题。

Anthropic 的发现指向一个反直觉的结论：**最有效的 Agent 不是加载最多上下文的 Agent，而是能在正确时刻加载正确上下文的 Agent。**

---

## 问题：上下文不是线性资源

传统观点认为，更大的上下文窗口 = 更强的 Agent 能力。但实际运行中的数据说明这个等式不成立：

| 上下文策略 | 实际效果 | 原因 |
|-----------|---------|------|
| 一次性加载所有相关文档 | 上下文污染严重，LLM 难以区分噪声和信号 | 信息量超过注意力瓶颈 |
| 提前预处理所有数据 | 高计算成本，实时性差 | 预推理策略不符合动态需求 |
| 按需加载（Just-in-Time） | ✅ 最有效 | 动态加载，只在需要时进入上下文 |

**关键洞察**：上下文窗口不是存储空间，而是注意力带宽。进入上下文的每一个 Token 都在争夺 LLM 的注意力份额。

---

## 核心策略一：Just-in-Time 上下文

Anthropic 在文章中描述了一种与「预推理」相对的方法：

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools."

这个方法的核心是**用引用代替内容**：

| 传统方式 | Just-in-Time 方式 |
|---------|------------------|
| 预加载完整文档（100k tokens） | 只保留文件路径（10 tokens） |
| 在上下文窗口做检索 | 运行时用工具动态加载 |
| 一次性高成本 | 按需低成本的渐进式加载 |

Claude Code 的数据分析就是这种方法的典型应用：

> "The model can write targeted queries, store results, and leverage Bash commands like head and tail to analyze large volumes of data without ever loading the full data objects into context."

### 为什么 Just-in-Time 更符合人类认知

Anthropic 指出这个方法映射了人类大脑的工作方式：

> "This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."

人类的认知系统天然是「按需索引」而非「预加载」。我们用文件系统、书签、待办清单来管理信息，而不是把所有信息都记在脑子里。Agent 的上下文设计应该遵循同样的原则。

---

## 核心策略二：Compaction（上下文压缩）

当任务跨越多个上下文窗口时，Compaction 是关键技术：

> "For tasks that span tens of minutes to multiple hours of continuous work, like large codebase migrations or comprehensive research projects, agents require specialized techniques to work around the context window size limitation."

Compaction 的工作原理是：

1. **检测上下文窗口压力**：当历史信息接近上下文上限时触发
2. **提炼核心信息**：将长对话压缩为高密度的摘要
3. **保留关键决策点**：确保重要上下文不被丢弃
4. **继续任务**：Agent 在压缩后的上下文中继续工作

这与 Claude Agent SDK 的 `compact` 功能完全一致：

> "compact feature automatically summarizes previous messages when the context limit approaches, so your agent won't run out of context."

**重要区分**：

| 技术 | 用途 | 触发时机 |
|------|------|---------|
| Compaction | 管理对话历史的长度 | 上下文窗口快满时 |
| Just-in-Time | 管理特定时刻的上下文量 | 任务执行过程中 |

两者解决不同维度的问题，配合使用才能让 Agent 在超长任务中保持高效。

---

## 核心策略三：Subagent 架构

当单一 Agent 的上下文管理复杂度超出可控范围时，Subagent 提供了一个根本性的解法：

> "Sub-agent architectures provide another way around context limitations. Rather than one agent attempting to maintain state across an entire project, specialized sub-agents can handle focused tasks with clean context windows."

Subagent 的核心价值在于**上下文隔离**：

```
传统方式：
┌─────────────────────────────────────────┐
│  Main Agent（管理完整项目上下文）          │
│  - 风险：上下文膨胀后决策质量下降          │
│  - 噪声：子任务信息相互干扰               │
└─────────────────────────────────────────┘

Subagent 方式：
┌─────────────────────────────────────────┐
│  Orchestrator（高层计划 + 结果聚合）        │
├──────────────┬──────────────────────────┤
│ Subagent A   │ Subagent B               │
│ 独立上下文    │ 独立上下文               │
│ 专注搜索任务  │ 专注实现任务              │
│ 返回浓缩摘要  │ 返回浓缩摘要              │
└──────────────┴──────────────────────────┘
```

每个 Subagent 的工作方式：

1. **探索阶段**：使用大量 Token（可能数万）深入研究
2. **提炼阶段**：将探索结果压缩为 1,000-2,000 Token 的摘要
3. **返回阶段**：只将摘要返回给 Orchestrator

> "Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."

这样 Orchestrator 收到的永远是最浓缩、最有价值的信息，而不是 Subagent 的完整工作记录。

---

## 核心策略四：工具作为上下文调节器

工具设计直接影响上下文效率。Anthropic 指出了一个关键原则：

> "Tools are prominent in Claude's context window, making them the primary actions Claude will consider when deciding how to complete a task."

这句话的含义是：**在 Agent 的决策空间中，工具是第一批被考虑的选项。**

这带来一个重要的工程结论：

| 工具设计决策 | 对 Agent 行为的影响 |
|------------|---------------------|
| 工具数量越多 | Agent 需要在更多选项中选择，上下文竞争加剧 |
| 工具描述越精确 | Agent 能更准确地判断何时使用 |
| 工具粒度越合理 | Agent 能更高效地组合完成复杂任务 |

好的工具设计不是「给 Agent 更多能力」，而是**让 Agent 在有限的注意力预算内做出最优决策**。

---

## 实践框架：上下文工程的四个层次

基于 Anthropic 的分析，上下文工程可以从四个层次实施：

### 层次一：上下文选择

**问题**：哪些信息应该进入上下文？

**策略**：
- 不预加载，使用 Just-in-Time 加载
- 用引用代替完整内容
- 根据任务相关性动态过滤

### 层次二：上下文压缩

**问题**：如何管理历史上下文的长度？

**策略**：
- 当接近上下文上限时触发 Compaction
- 保留决策点，压缩过程信息
- 维持关键上下文片段的完整性

### 层次三：上下文分发

**问题**：如何避免单一 Agent 的上下文过载？

**策略**：
- 使用 Subagent 进行并行探索
- 每个 Subagent 独立压缩结果
- Orchestrator 只聚合最终摘要

### 层次四：工具设计

**问题**：如何通过工具设计优化上下文效率？

**策略**：
- 工具数量控制在合理范围（避免选项过载）
- 工具描述精确，帮助 Agent 准确判断
- 工具粒度适中，支持灵活组合

---

## 反直觉的工程结论

上下文工程的反直觉之处在于：**减少上下文有时等于增强能力。**

| 选择 | 效果 |
|------|------|
| 加载所有相关文档 | Agent 决策质量下降，因为噪声淹没了信号 |
| 只加载当前任务所需的最小集 | Agent 决策质量提升，因为注意力集中在高价值信息上 |
| Compaction + Subagent | 长任务中保持稳定的高质量输出 |

> "The techniques we've outlined will continue evolving as models improve. But even as capabilities scale, treating context as a precious, finite resource will remain central to building reliable, effective agents."

当模型能力提升时，更聪明的模型确实需要更少的 prescriptive 工程。但「上下文是有限资源」这个认知不会改变——因为模型的注意力始终是瓶颈。

---

## 金句设计

> **「上下文不是仓库，而是带宽——不是越多越好，而是越准越值钱。」**

> **「给 Agent 一台计算机解决的是执行问题；给 Agent 正确的上下文解决的是决策质量问题。」**

> **「Subagent 的精髓不是并行加速，而是通过上下文隔离，让每个 Agent 都在干净的认知环境中做决策。」**

---

## 引用

> "Rather than pre-processing all relevant data up front, agents built with the 'just in time' approach maintain lightweight identifiers and use these references to dynamically load data into context at runtime using tools."
> — Anthropic Engineering

> "This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems to retrieve relevant information on demand."
> — Anthropic Engineering

> "Context engineering represents a fundamental shift in how we build with LLMs. As models become more capable, the challenge isn't just crafting the perfect prompt—it's thoughtfully curating what information enters the model's limited attention budget at each step."
> — Anthropic Engineering

---

## 备选标题

1. 上下文工程：Agent 的注意力经济学 — 策略：核心比喻
2. 为什么给 Agent 更多上下文不等于让 Agent 更聪明 — 策略：反常识
3. Just-in-Time + Compaction + Subagent：Anthropic 的三段式上下文解决方案 — 策略：框架概括
4. 从预推理到按需加载：上下文设计的范式转移 — 策略：技术演进视角
5. 当 LLM 的注意力成为瓶颈：上下文工程的四个层次 — 策略：层级递进