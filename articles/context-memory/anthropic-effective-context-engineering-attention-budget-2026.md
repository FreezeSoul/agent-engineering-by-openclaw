# Context Engineering for AI Agents：Attention Budget 与有限状态管理

## 核心问题

当 Agent 在多轮推理中运行时，上下文窗口中的信息不断膨胀——工具调用结果、文件内容、对话历史、检索到的文档。工程师通常的做法是"尽量往 context 里塞"，但 Anthropic 的工程团队指出这是根本性的误解：**LLMs 和人类一样，受限于有限的 attention budget，每新引入一个 token 都会消耗这个预算**。Context engineering 的本质是在有限的 budget 内做出取舍——这不是简单的"context 压缩"问题，而是关于**信息优先级**的系统性工程决策。

本文基于 Anthropic Engineering Blog 的深度分析，探讨 context engineering 的核心机制、context rot 的起因、以及"just-in-time retrieval"相比"pre-inference retrieval"的适用边界。

---

## 背景：为什么 prompt engineering 已经不够用了

Anthropic 在官方博客中明确指出了这层关系：

> "Prompt engineering refers to methods for writing and organizing LLM instructions for optimal outcomes. Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

两者不是替代关系，而是演进关系。Prompt engineering 处理的是"如何写好一条指令"（离散任务），而 context engineering 处理的是"如何在多轮交互中持续维护最优的 token 集合"（迭代过程）。

在 Agent 场景中，这个区别直接影响系统设计：

| 维度 | Prompt Engineering | Context Engineering |
|------|-------------------|-------------------|
| 任务类型 | 一次性分类/生成 | 多轮 Agent 循环 |
| 信息状态 | 静态（写完即用） | 动态（每轮都需重新评估） |
| 优化目标 | 单条 prompt 的效果 | 全局 context 的效率 |
| 时间尺度 | Inference-time | Turn-over-turn |

---

## Attention Budget：LLM 也有认知极限

Context engineering 重要性的根本原因在于 LLMs 自身的架构约束。Anthropic 详细解释了这一点：

> "LLMs are based on the transformer architecture, which enables every token to attend to every other token across the entire context. This results in n² pairwise relationships for n tokens. As its context length increases, a model's ability to capture these pairwise relationships gets stretched thin."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

这引出了"**context rot**"概念——当 context 长度增加时，模型准确召回信息的能力下降。Anthropic 引用了 needle-in-a-haystack 基准测试的研究结果：

> "Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

这个现象与人类的 working memory 限制高度相似：

> "Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**关键推论**：Attention budget 不是"context 越大效果越差"的线性衰减，而是每新增一个 token 都会对其他 token 的可及性造成稀释。当 Agent 处理 10 步任务时，第 1 步的信息在第 10 步时的有效权重已经显著降低。

---

## Context 的组成要素与工程原则

Anthropic 给出了各组件的 context engineering 指导原则：

### System Prompts：最小必要信息原则

> "We recommend organizing prompts into distinct sections (like <background_information>, <instructions>, ## Tool guidance, ## Output description, etc) and using techniques like XML tagging or Markdown headers to delineate these sections."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Anthropic 指出了两种常见失败模式：

1. **过度具体（Brittle if-else prompts）**：工程师将复杂的业务规则硬编码进 prompt，期望 Agent 按精确逻辑执行。这会导致脆弱性——规则增多后维护成本指数增长，且模型对边界情况的处理变得不可预测。

2. **过度抽象（Vague high-level guidance）**：提供模糊的方向，假设模型有"常识"。但 LLMs 的常识来自训练数据分布，无法保证与特定业务场景对齐。

正确的做法是在两者之间找到"Goldilocks zone"——**足够具体以给出有效指导，又足够抽象以提供鲁棒的启发式决策能力**。

> "Regardless of how you decide to structure your system prompt, you should be striving for the minimal set of information that fully outlines your expected behavior."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**最小化不等于最短**——有时候需要大量背景信息才能让 Agent 正确决策，但这些信息必须经过筛选，只包含"必要"的。

### Tools：最小可行集合原则

> "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

这与 Agent 设计的"最小可行工具集"原则完全一致。工具的返回值也需要考虑 token 效率——**一个返回 5000 token 的工具调用结果会直接消耗大量 attention budget**，因此工具设计时需要考虑：
- 返回信息的信息密度（高信号 vs 低噪声）
- 工具调用后 Agent 的预期行为路径（是否需要进一步处理，还是直接结束）

### Examples：多样性优于数量

> "We recommend working to curate a set of diverse, canonical examples that effectively portray the expected behavior of the agent. For an LLM, examples are the 'pictures' worth a thousand words."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

工程师常见的错误是用大量 edge case 填充 examples，希望"覆盖所有情况"。这反而会稀释核心行为的信号——模型需要从大量示例中推断模式，示例过多时反而丢失重点。

---

## 两种 Context 检索策略：Pre-inference vs Just-in-time

这是文章最核心的洞见之一。Anthropic 描述了行业正在发生的范式转移：

> "Today, many AI-native applications employ some form of embedding-based pre-inference time retrieval to surface important context for the agent to reason over. As the field transitions to more agentic approaches, we increasingly see teams augmenting these retrieval systems with 'just in time' context strategies."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### Pre-inference Retrieval（推理前检索）

当前主流做法：在 Agent 运行前，通过 embedding 相似度匹配将"可能相关"的文档全部注入 context。

**优点**：延迟低，检索在 Agent 运行前完成  
**缺点**：
- 信息可能过时（index 与实况不同步）
- 对复杂语法结构（如代码的 AST）的检索效果差
- 一次性加载大量 context，消耗大量 attention budget

### Just-in-time Retrieval（运行时检索）

Anthropic 描述的进阶做法：Agent 维护轻量级引用（文件路径、存储查询、网页链接），在需要时动态加载。

> "Claude Code uses this approach to perform complex data analysis over large databases. The model can write targeted queries, store results, and leverage Bash commands like head and tail to analyze large volumes of data without ever loading the full data objects into context. This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

**优点**：
- 无陈旧索引问题
- 只在 attention budget 中保留高相关性的信息
- 支持渐进式探索（Agent 可以通过探索发现新信息）

**缺点**：
- 运行时检索有延迟成本
- 需要正确的工具和启发式引导，否则 Agent 可能滥用工具

### 元数据作为隐式上下文

Anthropic 提到了一个有趣的现象：Agent 可以从元数据中推断信息，而不需要显式加载完整内容：

> "To an agent operating in a file system, the presence of a file named test_utils.py in a tests folder implies a different purpose than a file with the same name located in src/core_logic/. Folder hierarchies, naming conventions, and timestamps all provide important signals that help both humans and agents understand how and when to utilize information."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

这意味着 Agent 的 context 不需要包含文件内容本身——文件路径和目录结构已经提供了重要的语义信号。这是"最小化 context 占用"的高级形式。

---

## Hybrid 策略：最优解取决于任务特征

Anthropic 明确指出了 hybrid 策略的合理性：

> "In certain settings, the most effective agents might employ a hybrid strategy, retrieving some data up front for speed, and pursuing further autonomous exploration at its discretion. The decision boundary for the 'right' level of autonomy depends on the task."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Claude Code 是 hybrid 策略的具体实现：
- **Up-front retrieval**：`CLAUDE.md` 文件在开始时被直接注入 context
- **Just-in-time retrieval**：`glob` 和 `grep` 等工具允许 Agent 在需要时动态加载文件

对于动态性较低的场景（如法律文档分析、财务审计），pre-inference 检索更合适——数据的静态性允许提前构建高质量索引。

---

## Long-horizon Tasks 的特殊挑战

文章专门讨论了长时间跨度的任务对 context engineering 的影响。Agent 运行时间越长，累积的中间结果越多，这些中间结果可能在后续步骤中仍然相关，但同时也会消耗 attention budget。

Anthropic 的建议是：
- 维护**外部化的 notes**（不是全存在 context 中）
- Agent 使用**渐进式披露**——每个 turn 只加载必要的信息，而不是一次性全部加载
- 利用**元数据筛选**而非全文匹配来定位相关信息

---

## 对 Agent 架构设计的启示

Anthropic 这篇文章对 Agent 架构设计的核心启示是：

1. **Context 是有限的资源，不是无限的空间**。每个 token 都有成本，工程师必须主动管理这个 budget。

2. **工具设计必须考虑 token 效率**。一个设计糟糕的工具调用可能返回 10000 token 的内容，直接"吃掉" Agent 的大量 attention budget。

3. **检索策略需要与任务动态性匹配**。静态场景用 pre-inference 检索（可提前索引），动态场景用 just-in-time 检索（避免陈旧和语法结构问题）。

4. **混合策略是长期趋势**。未来更智能的模型可以承担更多自主探索任务，human curation 会越来越少。

> "Given the rapid pace of progress in the field, 'do the simplest thing that works' will likely remain our best advice for teams building agents on top of Claude."
> — [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

## 结论

Context engineering 是 Agent 工程化的关键转折点：从"如何写好 prompt"到"如何在多轮交互中持续维护最优信息集"。Attention budget 的有限性决定了 context 不是可以无限膨胀的资源，而是需要主动管理的约束条件。

对于 Agent 开发者而言，这意味着：
- **架构层面**：需要在 agent harness 中实现 context budget 监控和动态管理机制
- **工具层面**：每个工具的返回值设计必须考虑 token 效率，不能只管功能完整性
- **检索层面**：根据任务的数据动态性选择 pre-inference 或 just-in-time，或两者结合的 hybrid 策略

Context engineering 不是一次性的设计决策，而是贯穿 Agent 整个生命周期持续进行的工程实践。