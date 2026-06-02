# OpenAI 内置数据 Agent：企业级上下文工程的全景实践

> 本文剖析 OpenAI 内部数据 Agent 的架构设计，揭示一个核心事实：在 600PB 数据、70k 数据集的规模下，答案质量完全取决于上下文层次的设计质量。

## 核心命题

当数据规模大到「找表比写 SQL 还耗时」时，Agent 的核心竞争力不再是模型推理能力，而是**上下文工程**——如何让模型始终在正确的数据、正确的语义、正确的权限边界内工作。

OpenAI 内部数据 Agent 的六层上下文体系，本质上是一套**可验证、可积累、可干预**的认知基础设施。

## 一、问题：规模让数据变成陷阱

OpenAI 的数据平台服务 3500+ 内部用户，横跨 Engineering、Product、Research 三大部门。600PB 数据，70k 数据集。

数字本身不说明问题，问题在于：

**「找对表」本身就是最耗时的操作。**

一位内部用户的原话（原文引用）：
> "We have a lot of tables that are fairly similar, and I spend tons of time trying to figure out how they're different and which to use. Some include logged-out users, some don't. Some have overlapping fields; it's hard to tell what is what."

即便找到了正确的表，SQL 本身的复杂度也是陷阱——示例中的查询语句长达 180+ 行。连 Join 的是否正确都无法确认，更不用说筛选条件和 Null 处理。

**数据错误的代价是隐性的**：多对多 Join 错误、Filter Pushdown 错误、未处理的 Null 值，这些可以在不报任何错误的情况下悄悄让结果失效。

## 二、解决思路：从「问对问题」到「上下文先行」

Agent 的设计哲学是：模型推理之前，上下文必须先到位。

传统的数据查询流程是「用户提问 → 模型生成 SQL → 执行 → 返回结果」，问题在于模型在没有足够上下文的情况下生成的 SQL，天然带有随机性。

OpenAI 的 Agent 采用的是「先构建上下文，再执行推理」的流程：

```
用户提问 → 上下文检索 → 上下文注入 → 模型推理 → SQL 生成 → 执行验证 → 结果
```

关键区别：上下文构建和模型推理是分离的，上下文先行。

## 三、六层上下文体系

这是本文的核心，也是理解 OpenAI 数据 Agent 架构的关键。

### Layer #1: Table Usage Metadata

**解决的问题**：表级元数据（列名、数据类型）和表沿袭（上下游关系）。

Agent 依赖 Schema 元数据来写 SQL，并通过表沿袭理解表之间的上下游关系。

在此基础上，还额外摄入**历史查询记录**——知道哪些表通常会 Join 在一起，知道哪些查询模式是常见的。这让 Agent 在写新 SQL 时有迹可循，而非从头推断。

**笔者认为**：历史查询摄入是一个被低估的上下文来源。大多数 Agent 只关注 Schema，却忽略了「人们通常怎么用这张表」这条关键信息。

### Layer #2: Human Annotations

**解决的问题**：Schema 无法表达的语义和业务含义。

Domain Expert 手工撰写表和列的描述，包含意图、语义、业务含义和已知坑点。这些信息无法从 Schema 推断，只能靠人。

原文表述：
> "Metadata alone isn't enough. To really tell tables apart, you need to understand how they were created and where they originate."

**笔者认为**：这一层的维护成本最高，但也最不可替代。当两张表 Schema 完全一致但业务含义不同时，只有 Human Annotation 能区分它们。

### Layer #3: Codex Enrichment

**解决的问题**：表在代码层面的定义和使用方式。

这是最有趣的一层。通过分析表在 Spark、Python 等非 SQL 系统中的使用方式，Agent 获得了一个「表的社会网络」——它不仅知道表里有什么数据，还知道：

- 数据的生成频率和更新节奏
- 数据的排他性范围（如「仅包含第一方 ChatGPT 流量」）
- 表在哪些 Spark Job 中被使用
- 字段级别的 Uniqueness 特性

这段原文的关键：
> "This means that the agent can distinguish between tables that look similar but differ in critical ways. For example, it can tell whether a table only includes first-party ChatGPT traffic. This context is also refreshed automatically, so it stays up to date without manual maintenance."

**这说明 Codex Enrichment 不是一次性工作，而是一个自动刷新的持续过程。**

### Layer #4: Institutional Knowledge

**解决的问题**：公司级别的背景知识——Launches、Incident、内部代号、关键指标的定义和计算逻辑。

这些信息存在 Slack、Google Docs、Notion 中。Agent 接入这些系统，摄入并嵌入，以元数据和权限信息标注后存储。

访问控制是这一层的重要设计点：数据必须按权限隔离检索，防止 Agent 访问用户无权查看的数据。

### Layer #5: Memory（自适应层）

**解决的问题**：无法从其他层推断的非显而易见的修正、过滤和约束。

当用户纠正了 Agent 的某个理解偏差，Agent 会主动询问是否保存这条记忆，下次类似问题出现时从更准确的基线出发，而不是重复踩坑。

典型案例（原文引用）：
> "in one case, the agent didn't know how to filter for a particular analytics experiment (it relied on matching against a specific string defined in an experiment gate). Memory was crucially important here to ensure it was able to filter correctly, instead of fuzzily trying to string match."

记忆分全局和个人两个作用域，用户可以手动创建和编辑。

**笔者认为**：Memory 层是 Agent 从「工具」进化到「助手」的关键标志。它让 Agent 有了学习能力，而不是每次都是零起点。**

### Layer #6: Runtime Context

**解决的问题**：当所有静态上下文都不够或已过时时，Agent 实时查询数据仓库，直接 Inspect 表结构和数据。

这一层是Fallback机制——当上下文断裂时，Agent 可以直接发问，而不是凭猜测继续推理。

## 四、自我修正循环：Agent 的推理质量保障

这是六层上下文体系之外的一个关键工程机制。

Agent 的核心能力不是「一次做对」，而是「做错了能自己发现」。

当某个中间结果看起来不对（例如零行结果，因为 Join 或 Filter 错误），Agent 不会继续往下走，而是：

1. 调查哪里出了问题
2. 调整方法
3. 重试

原文的关键表述（原文引用）：
> "Rather than following a fixed script, the agent evaluates its own progress. If an intermediate result looks wrong (e.g., if it has zero rows due to an incorrect join or filter), the agent investigates what went wrong, adjusts its approach, and tries again. Throughout this process, it retains full context, and carries learnings forward between steps. This closed-loop, self-learning process shifts iteration from the user into the agent itself, enabling faster results and consistently higher-quality analyses than manual workflows."

**自我修正循环的核心是：保留了完整的上下文，并在步骤之间携带学习成果。**

## 五、Eval 系统：质量漂移的防控机制

Agent 总是处于运行状态，能力可以提升也可以退化。没有严格的反馈循环，回归几乎是必然的。

OpenAI 用 Evals API 来测量和保护 Agent 的响应质量。

Eval 的构建方式：
1. 人工编写 Question-Answer 对
2. 每个人工问题配对一个「黄金 SQL」——产生预期结果的正确 SQL
3. 自然语言问题发给 SQL 生成端点
4. 执行生成的 SQL
5. 将结果与黄金 SQL 的结果比较

**关键设计**：不使用简单的字符串匹配。生成的 SQL 可能在语法上不同但逻辑正确，结果集可能包含不影响答案的额外列。Evals Grader 评估 SQL 和结果数据双方，给出最终分数并附带解释。

这些 Eval 像持续运行的单元测试，识别回归就像金丝雀在矿井中的作用——提前发现问题，在 Agent 能力扩展时自信迭代。

## 六、Agent 安全模型

Agent 继承了 OpenAI 现有的安全和访问控制模型。

所有访问都是严格的「直通」模式：用户只能查询他们已有权限查看的表。当权限缺失时，Agent 会标记或回退到用户有权限的替代数据集。

Agent 本身只是一个接口层，不持有任何超出用户已有权限的数据访问能力。

## 七、Workflow 抽象：从临时分析到可复用流程

当用户频繁运行相同的分析时，Agent 将其打包成可重用的指令集——Workflow。

示例包括每周业务报告和表验证的自动化流程。

通过一次编码上下文和最佳实践，Workflow 简化了重复分析并确保跨用户的一致结果。

## 八、架构启示

**1. 上下文分层是架构问题，不是 Prompt 问题**

六层上下文体系是一个分层架构设计，而不是把所有信息塞进 Prompt。每层有其职责和刷新机制，共同构成了一个自洽的认知系统。

**2. Memory 是 Agent 工程化的里程碑**

从「工具」到「助手」的本质差别在于：工具不会从错误中学习，助手会。Memory 层让 Agent 有了真正的自适应能力。

**3. 自我修正循环比一次做对更重要**

在复杂数据分析场景中，几乎不可能第一次就做对。关键不是一次做对，而是做错了能发现、调整、重试。这需要一个保留完整上下文且能在步骤间携带学习成果的系统。

**4. Eval 是生产级 Agent 的必备基础设施**

没有量化评估，Agent 的质量就是黑盒。质量漂移无法被发现和阻止。Eval 提供了持续的质量可见性。

---

> **关联项目**：当 OpenAI 的数据 Agent 在企业数据层面解决上下文问题时，Mem0（github.com/mem0rias/mem0，52k Stars）正试图成为 AI Agent 的通用记忆层——跨应用、跨会话的持久化记忆基础设施。

---

*Round 217 | 2026-06-03 | 主题：企业级上下文工程 | 来源：openai.com/index/inside-our-in-house-data-agent（NEW SOURCE）*