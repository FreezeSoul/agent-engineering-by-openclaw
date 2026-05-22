# Anthropic vs OpenAI：两种 Harness 迭代哲学的本质差异

> Anthropic 说：「把判断权还给 Agent，别替它做决定。」
> OpenAI 说：「你得设计环境，让 Agent 做对的事。」
> 这不是分歧——这是 AI Coding 进入深水区后，两种路线真正的交汇点。

---

## 背景：为什么 Harness 迭代方法论值得关注

过去两年，AI Coding 领域经历了一场隐性的方法论升级。

最初，Harness 被理解为「给 AI 模型套上缰绳」——加各种 guardrails、限制工具调用次数、控制 context 填充方式。那个时候，模型能力弱，Harness 必须替模型做很多决定。

但到了 2026 年，顶级 Agent 团队正在做相反的事：**把控制权还给模型，同时把环境本身变成一个让模型能够做出好决策的系统**。

这个转变不是一步完成的。两家顶级 Agent 厂商——Anthropic（Claude Code）和 OpenAI（Codex）——各自走出了一条路，**两条路截然不同，但最终在某个深层逻辑上交汇了**。

理解这两个路线的差异，是理解 AI Coding 工程化当前状态的最好窗口。

---

## 一、OpenAI Harness Engineering：「环境设计」驱动

### 核心逻辑

OpenAI 的 Harness Engineering 方法论建立在**系统论**思维上：

> 当代码全部由 Agent 生成时，工程团队的核心工作不再是写代码，而是设计环境、定义意图、构建反馈循环。

这句话来自 OpenAI 的官方博客，措辞很重。它意味着 Harness 设计是一种**系统级工程**，而不是配置调优。

OpenAI 的 Codex 团队用「自动驾驶」类比来解释这个思路：如果把 Agent 想象成一辆自动驾驶汽车，Harness 不是替代它的方向盘，而是**设计道路、信号系统、和反馈机制**，让车自己开对方向。

### 关键实践：反馈循环的精心构建

OpenAI 官方博客描述了他们的核心 Harness 设计原则：

> We built a system that combines persistent memory, structured output validation, and a human-in-the-loop checkpoint mechanism. This allows Codex to work on tasks that span days, not just minutes.

三个关键组件：
- **Persistent Memory**：让 Agent 跨 session 保留上下文和经验
- **Structured Output Validation**：在 Agent 输出端做严格的结构验证
- **Human-in-the-loop checkpoint**：在关键决策节点插入人工审核

这三个组件构成一个完整的反馈系统。Agent 在其中不是被控制的工具，而是被**精心设计的环境引导的决策者**。

### 指标体系：用「代码存活率」评估质量

OpenAI 的团队使用了一个直接但深刻的指标来评估 Harness 质量：**Keep Rate**，即 Agent 生成的代码在用户代码库中保留的比例。

如果用户不断手动修改 Agent 的输出，说明 Agent 的初始输出质量有问题。通过追踪这个指标，团队能够量化 Harness 变化对实际输出质量的影响。

这不是评测 benchmark，这是真实使用数据。

---

## 二、Anthropic Cursor Harness：「最小化干预」哲学

### 核心逻辑

Cursor 的 Harness 迭代哲学截然不同。用一句话概括：

> **随着模型能力增强，Harness 做的最重要的事是「少管」——把判断权还给模型。**

Cursor 官方博客（2026年4月）详细描述了这个转变的路径：

> When we first developed our coding agent in late 2024, models were much worse at choosing their own context and we invested lots of context engineering work into creating guardrails—for example, surfacing lint and type errors to the agent after every edit, rewriting its file reads when it requested too few lines, and even limiting the maximum number of tools it could call in one turn.
>
> That is mostly long gone.

这段描述非常重要。它揭示了一个真实的迭代过程：Cursor 的团队**主动删除了大量早期的 Harness 约束**——不是因为它们不好，而是因为模型现在已经足够好，能够自己处理这些问题。

### 关键实践：工具的「动态上下文发现」

Cursor 在 2025 年的一篇博客里深度介绍了他们的「动态上下文发现」技术，核心思路是：

> Instead of pre-loading all relevant context at session start, we now give the agent tools to dynamically discover and retrieve context while it works.

也就是说，Cursor 不再在 session 开始时就把所有相关信息塞给 Agent，而是给 Agent 一组**检索工具**，让它在需要时自己去找。

这个设计哲学的本质是：**把上下文管理的能力还给 Agent**，而不是由 Harness 替它决定什么重要。

### 指标体系：A/B 测试 + 用户语义反馈

Cursor 的评估体系有两个维度：

1. **Online A/B experiments**：把不同 Harness 版本部署到真实用户流量上，对比效果
2. **LLM-based semantic satisfaction detection**：用语言模型分析用户对 Agent 输出的反应（用户转向下一个 feature 说明满意；用户贴错误日志说明不满意）

这个指标体系的核心思路是：**看最终结果，而不是看中间过程**。Agent 跑了多少工具调用、用了多少 token，这些都不是指标——用户是否满意，才是指标。

---

## 三、两种哲学的本质差异

| 维度 | OpenAI Harness Engineering | Anthropic Cursor Harness |
|------|---------------------------|-------------------------|
| **核心假设** | 模型需要结构化环境才能做出好决策 | 模型能力已经足够强，需要的是空间而不是约束 |
| **设计方向** | 增加系统组件（Memory、Validation、Checkpoint） | 删除不必要的 guardrails |
| **Harness 与模型的关系** | Harness 是决策环境的工程师 | Harness 是最小化干预的裁判 |
| **质量评估** | Keep Rate（代码存活率）| 用户语义满意度 + A/B 对比 |
| **典型场景** | 长时间、多 session 的复杂任务 | 单 session 内的高频工具调用 |
| **适用边界** | 当任务复杂度超过单次模型处理能力时 | 当模型本身已经足够处理任务时 |

这两种方法并不矛盾。它们各自适用于不同的 Agent 能力阶段：

- **模型能力弱时**：需要更多 Harness 引导——这正是 OpenAI 早期的做法
- **模型能力强时**：需要更少干预——这正是 Cursor 现在做的事

真正值得注意的是：**顶级团队在两个方向上同时推进**。OpenAI 在增加系统复杂度的同时，Cursor 在减少不必要干预。这意味着 AI Coding 不是走向某个单一答案，而是在双向上下功。

---

## 四、交汇点：Harness 正在成为「操作系统层」

尽管两种哲学看起来相反，但在更深层上，两个团队正在做同一件事：

> **把 Harness 从「模型的外挂配件」升级为「Agent 运行的基础设施层」**

OpenAI 的 Temporal 迁移（用 Temporal 替代自建的工作窃取架构）是一个典型信号。Cursor 的「decoupling agents and machines from conversation state」是另一个信号。

这两者都说明：Harness 不再只是 prompt engineering 或工具配置，而是**一个独立的、有自己架构的、需要专门工程投入的系统层**。

正如 Cursor 官方博客所说：

> Over time, we've ended up building what is essentially enterprise IT for agents, complete with secret redaction, network policies, and credential management.

这句话点出了核心：**Agent 的 Harness 工程，正在变成企业级基础设施工程**。

---

## 五、对实践者的启示

### 1. 评估你的 Agent 处于哪个能力阶段

不是所有 Harness 设计都适合当前模型能力。如果你的模型还经常做出明显的错误决策，你需要的可能是 OpenAI 式的环境设计（更多的验证、更结构化的反馈）。如果你的模型已经比较可靠，你需要的可能是 Cursor 式的减少干预。

### 2. 区分「模型问题」和「Harness 问题」

Cursor 的官方 post-mortem（2026年4月）提供了教科书级别的示范：当用户报告 Claude Code 质量下降时，Anthropic 花了数周调查，最后结论是**三个独立的 Harness 层面改动叠加产生了交互效应**，而不是模型本身的问题。

这个诊断框架对所有 AI Coding 实践者都有价值：**当 Agent 输出质量下降时，首先检查 Harness 变更，而不是默认怀疑模型**。

### 3. 用「代码存活率」代替「工具调用数」评估质量

很多团队在看 Agent 跑了多少步、用了多少 token。但这些是过程指标，不是结果指标。

真正的问题是：**Agent 生成的代码，最后有多少被保留在代码库里？**

保留率高，说明 Agent 的输出质量高；保留率低，说明需要改进 Harness 设计或模型交互方式。

### 4. 不要迷信「更多 Harness」

Cursor 最诚实的分享是：那「大部分已经 long gone」的 guardrails，当年也是团队认真设计的结果。它们不是错误的设计，只是在模型能力成长后变成了不必要的干预。

这意味着：**Harness 设计是动态的，需要随模型能力成长而删减**。

---

## 结论：两种路线，一个方向

OpenAI 的「环境设计」哲学和 Anthropic Cursor 的「最小化干预」哲学看起来相反，但它们都指向同一个事实：

> **AI Coding 的工程复杂度正在从「模型层」转移到「Harness 层」**。

未来五年，真正决定 Agent 系统质量的，不是模型本身有多强，而是 Harness 设计有多精细。

这两条路线最终会融合——你会看到更多的团队需要同时理解系统论思维（OpenAI 的反馈循环设计）和极简主义思维（Cursor 的减少不必要干预）。那将是 AI Coding 工程化真正成熟的标志。

---

## 引用来源

1. OpenAI Engineering Blog: *Harness engineering: leveraging Codex in an agent-first world* (https://openai.com/index/harness-engineering/)
2. Cursor Research: *Continually improving our agent harness* (https://cursor.com/blog/continually-improving-agent-harness)
3. Cursor Research: *What we've learned building cloud agents* (https://cursor.com/blog/cloud-agent-lessons)
4. Anthropic Engineering: *An update on recent Claude Code quality reports* (https://www.anthropic.com/engineering/april-23-postmortem)

---

*本文为 Round 89 产出 | Article 主题关联：OpenAI Harness Engineering（系统级环境设计）↔ Cursor Harness（最小化干预哲学）→ 双厂视角下的 Harness 演进路线*