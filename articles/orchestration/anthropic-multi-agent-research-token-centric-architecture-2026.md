# Anthropic 多 Agent 研究系统：95% 性能差异来自 Token 消耗

> 领域：Orchestration / Multi-Agent | 优先级：🔴 一手来源 | 产出：anthropic.com/engineering/multi-agent-research-system

---

## 核心命题

多 Agent 系统的性能差异，**80% 可以被 Token 消耗量单独解释**——这不是观点，是数据。

Anthropic 在他们内部 Research 功能的复盘中披露了一个反直觉的发现：在 [BrowseComp](https://openai.com/index/browsecomp/) 评估中（测试 AI 浏览 Agent 定位难以找到的信息的能力），三个因素解释了 95% 的性能差异：

1. **Token 消耗量**（解释 80% 的方差）
2. **Tool Call 数量**
3. **模型选择**

这个发现对 Agent 架构设计有根本性的冲击。

---

## 背景：多 Agent 系统为什么有效

Research 功能是 Anthropic 在 Claude 中推出的一个能力——让 Agent 根据用户查询规划研究流程，然后并行创建子 Agent 同时搜索信息。团队从原型到生产的旅程揭示了多 Agent 系统工程化的关键挑战。

研究工作的本质是**压缩**——从海量语料中提炼洞察。子 Agent 通过并行运作实现这种压缩：每个子 Agent 拥有独立的上下文窗口，同时探索问题的不同方面，最后将最重要的 Token 压缩后传回给主 Agent。

Anthropic 的内部评估显示，多 Agent 研究系统在**广度优先查询**（同时追踪多个独立方向）上表现优异。一个多 Agent 系统（以 Claude Opus 4 为主 Agent，Sonnet 4 为子 Agent）在内部研究评估中比单 Agent Opus 4 的性能高出 **90.2%**。例如，当被要求识别信息科技 S&P 500 中所有公司的董事会成员时，多 Agent 系统通过分解任务给子 Agent 找到了正确答案，而单 Agent 系统则因缓慢的顺序搜索而失败。

---

## 核心洞察：Token 是性能的主因

> "We found that token usage by itself explains 80% of the variance, with the number of tool calls and the model choice as the two other explanatory factors."

这句话的分量在于：当我们谈论「多 Agent 比单 Agent 更好」时，真正的原因不是 Agent 数量本身，而是**Token 消耗量的增加**。

多 Agent 系统让 Claude 能够探索更多方向、调用更多工具、生成更多思考——这些行为的叠加体现为 Token 消耗量的上升，而 Token 消耗量的上升直接关联性能提升。

三个推论：

### 推论 1：扩大 Token 预算比优化架构更有效

如果 80% 的性能差异来自 Token 消耗，那么提高性能最直接的方式是**增加 Token 消耗上限**，而不是设计更精巧的 Agent 协作协议。这与当前行业热衷于设计复杂编排协议的潮流相悖——在很多场景下，简单地让 Agent 多跑几轮比重新设计架构更有效。

### 推论 2：模型升级比框架升级更重要

> "The latest Claude models act as large efficiency multipliers on token use, as upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget on Claude Sonnet 3.7."

Anthropic 明确指出，升级模型带来的 Token 效率提升，大于在相同模型上翻倍 Token 预算。这意味着对于多 Agent 系统，**模型选择是杠杆最大的决策变量**。

### 推论 3：多 Agent 本质是 Token 预算的规模化

多 Agent 架构之所以有效，不是因为 Agent 之间的协作协议设计精巧，而是因为它有效地**扩大了总 Token 消耗容量**——每个子 Agent 有自己的上下文窗口，可以并行探索，互不干扰，最终通过压缩机制将关键信息传回主 Agent。

---

## 工程实践：从原型到生产的三个关键挑战

Anthropic 总结了从原型到生产过程中学到的关键工程教训：

### 挑战 1：状态累积与错误复合

> "Agents are stateful and errors compound. Agents can run for long periods of time, maintaining state across many tool calls."

Agent 是有状态的，这意味着错误会复合。与单轮对话不同，如果中间某一步失败，不能简单地从开头重启——重启代价高昂且令人沮丧。

Anthropic 的解法：构建能够**从 Agent 错误发生位置恢复**的系统，并利用模型的智能让 Agent 优雅地处理问题——例如告知 Agent 某个工具正在失败，让它自适应调整。

### 挑战 2：部署需要精细协调

> "Agent systems are highly stateful webs of prompts, tools, and execution logic that run almost continuously. This means that whenever we deploy updates, agents might be anywhere in their process."

Agent 系统的高度有状态性意味着：部署更新时，不能同时更新所有 Agent——因为 Agent 可能正处于某个长流程的中间。Anthropic 使用 **Rainbow Deployments** 策略，让新旧版本同时运行，逐步将流量从旧版本迁移到新版本，避免打断正在运行的 Agent。

### 挑战 3：同步执行是瓶颈

> "Currently, our lead agents execute subagents synchronously, waiting for each set of subagents to complete before proceeding."

当前的主 Agent 以同步方式执行子 Agent——等待每一批子 Agent 完成后再继续。这简化了协调，但造成了信息流动的瓶颈：主 Agent 无法 steering 子 Agent，子 Agent 之间无法协调，且整个系统可能在等待单个子 Agent 完成时阻塞。

Anthropic 的下一步是探索**异步执行**：Agent 并发工作，在需要时创建新子 Agent。但这增加了结果协调、状态一致性和错误传播的复杂性。Anthropic 认为，随着模型处理更长、更复杂研究任务的能力提升，性能收益将证明这些复杂性的代价是值得的。

---

## 生产经济学：15 倍 Token 成本换 90% 性能提升

> "In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."

关键数字：
- 单 Agent：约 **4 倍**普通聊天的 Token 消耗
- 多 Agent 系统：约 **15 倍**普通聊天的 Token 消耗

换来的是 90.2% 的性能提升。这是多 Agent 系统的「消费-收益比」，它意味着：

1. **高价值任务才值得多 Agent**：对于简单的问答任务，15 倍 Token 成本换来的性能提升可能不值；但对于需要深度研究的复杂问题，这是划算的交易
2. **任务价值决定架构选择**：如果任务价值不够高，不应该盲目上多 Agent 系统
3. **某些领域不适合多 Agent**：需要所有 Agent 共享同一上下文、或 Agent 之间有大量依赖的场景，当前的多 Agent 架构并不适合

---

## 对 Agent 架构设计的启示

Anthropic 的这篇复盘对 Agent 工程实践有几点关键启示：

### 1. Token 效率是架构评估的核心指标

当你评估一个 Agent 架构时，Token 消耗量应该成为核心评估维度——而不是只看「用了几个 Agent」或「支持多少工具」。一个高效的单 Agent 系统可能比一个低效的多 Agent 系统用更少的 Token 达到更好的效果。

### 2. 并行化是扩大 Token 消耗的主要手段

多 Agent 的核心价值在于**并行化带来的 Token 消耗容量扩展**。如果你无法并行执行（例如任务之间有强依赖），多 Agent 架构的优势将大打折扣。

### 3. 错误恢复要从「重启」思维转向「继续」思维

传统软件工程的错误处理是「重启」——从已知良好状态重新开始。但 Agent 的状态累积特性使得「继续」思维更重要：设计能够从错误发生点恢复的系统，而不是每次都从头开始。

### 4. 生产 Agent 需要状态持久化和检查点机制

长时运行的 Agent 需要能够在任意时刻保存状态，并在恢复时从这个状态继续。这意味着需要类似数据库事务日志的检查点机制，以及在崩溃后的恢复路径。

---

## 关键引用

来自 Anthropic Engineering Blog：

> "We found that token usage by itself explains 80% of the variance, with the number of tool calls and the model choice as the two other explanatory factors."

> "The latest Claude models act as large efficiency multipliers on token use, as upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget on Claude Sonnet 3.7."

> "Agents are stateful and errors compound. Agents can run for long periods of time, maintaining state across many tool calls. This means we need to build systems that can resume from where the agent was when the errors occurred."

> "In our data, agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats."

---

## 总结

Anthropic 的多 Agent 研究系统复盘揭示了一个反直觉但数据支持的事实：**Token 消耗量是解释多 Agent 系统性能差异的第一因素**。

这不是说 Agent 协作协议设计不重要，而是提醒我们：在追求更精巧的编排协议之前，先确保 Token 消耗的策略是合理的。

对于 Agent 架构设计者来说，这意味着：
- **评估架构时看 Token 效率**，而不是只看 Agent 数量
- **模型选择是杠杆最大的变量**——升级模型可能比优化架构更有效
- **并行化是核心**——无法并行执行的任务，多 Agent 优势不明显
- **长时 Agent 需要错误继续能力**，而不是重启能力

当模型能力继续提升，Token 效率继续改善，我们可以预期多 Agent 系统将成为解决更复杂任务的标准方式——但前提是我们理解了其本质：**用 Token 换性能**。

---

*推荐依据：Anthropic Engineering Blog 原文 | anthropic.com/engineering/multi-agent-research-system*