# Context Engineering：Agent 的注意力管理之道

## 核心问题

LLM 的上下文并非无限资源——随着 token 数增加，模型的信息召回能力逐渐下降，这种现象被称为 **context rot**。Context Engineering 解决的正是这个问题：如何在有限的注意力预算内，精准投放最高价值的上下文 token，让 Agent 在多轮推理和长时任务中始终保持高效。

本文基于 Anthropic Engineering Blog 的最新文章，系统梳理 Context Engineering 的核心原则与工程实践。

---

## 一、从 Prompt Engineering 到 Context Engineering

### 1.1 两者本质差异

Prompt engineering 的核心是**写好一条指令**——关注措辞、格式、示例，属于一次性动作。

Context engineering 的核心是**管理一个状态**——在每个推理周期决定往 context 里放什么、扔什么，属于持续性的迭代决策。

> "In contrast to the discrete task of writing a prompt, context engineering is iterative and the curation phase happens each time we decide what to pass to the model."
> — [Anthropic Engineering: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Anthropic 明确指出，Context Engineering 是 Prompt Engineering 的**自然演进**：当 Agent 需要跨多轮推理和更长时域操作时，单纯优化单条 prompt 已经不够——必须管理整个上下文状态（system instructions、tools、MCP、external data、message history 等）。

### 1.2 为什么 Agent 必须关注 Context

LLM 基于 Transformer 架构，每个 token 都要与 context 中所有其他 token 计算注意力关系。n 个 token 产生 n² 个 pairwise relationships。

随着 context 增长，模型捕捉这些关系的能力被稀释。更关键的是，模型在训练数据中短序列远多于长序列，因此**缺乏处理长程依赖的专门参数**。

这造成了根本张力：**context 越长，有效注意力密度越低**。

> "Context, therefore, must be treated as a finite resource with diminishing marginal returns. Like humans, who have limited working memory capacity, LLMs have an 'attention budget' that they draw on when parsing large volumes of context."
> — [Anthropic Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

这意味着 Context Engineering 不是可选项，而是构建 capable agents 的必要条件。

---

## 二、有效 Context 的解剖学

### 2.1 System Prompts：黄金海拔原则

System prompts 决定 Agent 的行为基线。Anthropic 提出的设计原则是**黄金海拔（Goldilocks zone）**——在两个极端之间找到平衡：

| 极端 | 问题 | 表现 |
|------|------|------|
| 过度具体 | 脆弱的 if-else 逻辑，复杂且难维护 | hardcoded brittle prompts |
| 过度抽象 | 缺乏具体信号，假设共享背景 | vague, high-level guidance |

正确做法是：足够具体以引导行为，同时保持灵活以提供强启发式。

**结构化优于格式化**：推荐将 system prompt 分成 `<background_information>`、`<instructions>`、`## Tool guidance`、`## Output description` 等明确 sections，使用 XML tags 或 Markdown headers 分隔。尽管随着模型能力提升，具体格式可能变得不那么重要，但结构化本身始终有价值。

**Minimal sufficient 原则**：先测试最小化 prompt，在实际任务上失败后再逐步增加指令。不要提前塞入大量边界情况——用 failure modes 驱动 prompt 演化。

### 2.2 Tools：最小化与自包含

Tools 是 Agent 与环境交互的接口。Anthropic 的核心原则是**minimal viable tool set**：

> "If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better."

工具设计的三个标准：
- **自包含**：工具应当独立完整，不依赖其他工具的状态
- **抗错**：robust to error，有清晰的错误处理
- **意图明确**：功能边界清晰，不过度重叠

Token 效率是另一个关键考量：工具返回的信息应当 token 高效，同时引导 Agent 产生高效行为。冗余的 tool set 不仅造成决策模糊，还会增加 context 负担——这一点在长时任务中尤为关键。

### 2.3 Few-shot Examples：典型优于堆砌

Examples 对 LLM 而言是"一图胜千言"的价值。Anthropic 建议：

- 提供 **diverse, canonical examples** 而非穷举所有边界情况
- 边界情况堆砌反而会稀释核心行为模式
- examples 应当展示**期望行为**而非所有可能的错误

---

## 三、Context 检索策略：预推理 vs 即时

### 3.1 两种范式的根本差异

| 策略 | 机制 | 优势 | 劣势 |
|------|------|------|------|
| Pre-inference retrieval | 推理前预先加载所有相关数据 | 速度快，延迟低 | 索引可能过时，syntax tree 复杂 |
| Just-in-time retrieval | 运行时通过工具动态加载数据 | 数据总新鲜，无语法树复杂度 | 延迟高，需要正确的导航工具 |

Anthropic 给出了关键判断：**Just-in-time 策略更接近人类认知**——我们不记忆整个语料库，而是依赖外部组织系统（文件系统、收件箱、书签）来按需检索。

### 3.2 Claude Code 的混合策略

Claude Code 采用了混合模型：

1. **CLAUDE.md 文件**通过 naive drop 预先加载到 context
2. **glob/grep 等工具**允许 Agent 按需导航环境，实时检索文件

> "This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand."

这种设计的精妙之处在于：文件名、路径、文件夹层级本身都是元数据——`tests/test_utils.py` 和 `src/core_logic/test_utils.py` 的含义差异无需显式说明，路径本身就传递了意图信号。

### 3.3 Agent 自主导航的价值

让 Agent 自主探索还能实现**渐进式发现（Progressive Disclosure）**：每个交互产生的上下文指引下一步决策。文件大小暗示复杂度，命名约定暗示目的，时间戳可以充当相关性的代理。

这本质上是**layer by layer 的理解构建**——Agent 只在 working memory 中保留必要信息，通过 note-taking 策略实现额外持久化。

当然，这种策略有代价：runtime exploration 显著慢于预计算数据；需要深思熟虑的工程确保 LLM 有正确的工具和启发式来有效导航。

对于动态内容较少的场景（如法律或金融），混合策略可能更合适。随着模型能力提升，Agentic 设计将趋向于让智能模型自主行动，所需的人类策展越来越少。

---

## 四、长时任务中的 Context 管理

### 4.1 核心挑战

长时任务中 Context 的累积会带来三个问题：
1. **Context rot**：历史信息过多导致关键信息召回率下降
2. **Attention 稀释**：有效 token 密度降低
3. **Staleness**：预先检索的数据可能过时

### 4.2 自管理 Context Window

Anthropic 建议 Agent 采用**自管理策略**：
- 在 working memory 中只保留相关子集
- 通过 note-taking 策略实现额外持久化
- 按需动态加载历史上下文而非全量保留

这与 MemGPT 等 external memory 架构的思路一致：把 memory 层视为 LLM attention 的扩展，用更结构化的方式管理长期信息。

### 4.3 工具集最小化的连锁价值

前面提到的 minimal viable tool set 原则，在长时任务中产生了额外价值：更少的工具意味着更可靠的内容裁剪和维护。当工具功能重叠时，Agent 的选择会模糊，Context 会膨胀。最小化工具集让 Agent 能更专注，也降低了长时任务中的维护复杂度。

---

## 五、工程实践检查清单

基于以上分析，以下是 Context Engineering 的核心检查点：

| 维度 | 检查项 | 优先级 |
|------|--------|--------|
| System Prompt | 是否处于黄金海拔（不过度 hardcode，不过度抽象）？ | 🔴 必须 |
| System Prompt | 是否采用结构化 sections（XML/Markdown）？ | 🟡 推荐 |
| System Prompt | 是否采用 minimal sufficient 原则（先少后加）？ | 🔴 必须 |
| Tools | 工具集是否 minimal（人类能明确决策每个工具的适用场景）？ | 🔴 必须 |
| Tools | 工具是否自包含、意图明确、抗错？ | 🔴 必须 |
| Examples | 是否提供 diverse canonical examples 而非边界情况堆砌？ | 🟡 推荐 |
| Retrieval | 是否有明确的 pre-inference vs just-in-time 策略选择？ | 🟡 推荐 |
| Retrieval | 是否考虑了 hybrid 策略（Claude Code 模式）？ | 🟡 推荐 |
| Long-horizon | 是否有 context 裁剪/压缩机制？ | 🔴 必须 |
| Long-horizon | Agent 是否能自主管理 attention 分配？ | 🟡 推荐 |

---

## 六、结论

Context Engineering 的本质是**注意力资源管理**——在有限的 attention budget 内最大化有效 signal。

核心原则：
1. **Minimal sufficient**：context 不是越多越好，而是刚好够用
2. **Just-in-time > pre-loading**：数据新鲜度 > 预计算速度
3. **Tools shape behavior**：工具集决定 Agent 的决策空间
4. **Self-managed window**：Agent 应能自主管理 attention 分配

> "Given the rapid pace of progress in the field, 'do the simplest thing that works' will likely remain our best advice for teams building agents on top of Claude."

这不仅是工程建议，更是认知框架：在 context engineering 领域，最有效的方案往往是最小化、最直接的方案。

---

**引用来源**：
- [Anthropic Engineering: Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic Research: Building effective AI agents](https://www.anthropic.com/research/building-effective-agents)