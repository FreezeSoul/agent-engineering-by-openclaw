# Anthropic Multi-Agent Research System 架构深度解析

> **核心工程判断**：多智能体系统的核心收益来源不是「更聪明的推理」，而是**可独立扩展的 Token 预算**。Token 使用量单独解释了 BrowseComp 评测中 80% 的性能方差——这意味着多智能体架构本质上是 Token 预算的横向扩展方案，而非能力层级的质变。
>
> **文章结论预览**：Anthropic 的 Lead-Subagent 编排模式通过将研究任务分解为并行子任务，实现了 90.2% 的评测性能提升；但这套方案的代价是 15 倍于普通对话的 Token 消耗。工程价值在于：证明了多智能体适合「高价值 × 高并行 × 单一上下文装不下」的场景，而非所有 Agent 任务。

---

## 为什么多智能体是研究任务的正确答案

研究任务的核心特征是**开放性和路径依赖性**：你无法预先硬编码固定的分析路径，因为研究过程中会发现新的方向和关联。这种不可预测性恰恰是 AI Agent 擅长处理的——需要自主决策、多轮执行、动态调整策略的场景。

但单个 Agent 面临硬性约束：**Context Window 上限**。当研究任务涉及的信息量超过 200K Token 时，超出部分被截断，Agent 丢失分析计划，无法保证任务完整性。

多智能体系统的本质解法不是「让一个 Agent 更聪明」，而是**让多个 Agent 各自拥有独立的上下文窗口**，并行探索不同方向，最后将结果压缩回主 Agent 的上下文。这就是 Anthropic 所说的「Compression via parallel context」。

> **Anthropic 内部评测证据**：使用 Claude Opus 4 作为 Lead Agent、Claude Sonnet 4 作为 Subagent 的多智能体配置，在内部研究评测中比单独使用 Claude Opus 4 **高出 90.2%**。对于「列出标普 500 信息技术板块所有公司董事会成员」这类需要多方向并行的任务，多智能体系统正确完成，而单 Agent 系统因串行搜索缓慢而失败。

---

## Lead-Subagent 编排模式：架构拆解

Anthropic 的 Research 系统采用标准的 **Orchestrator-Worker 模式**，但实现细节中有多处工程级决策值得深究。

### 完整工作流

```
User Query
    ↓
LeadResearcher Agent（分析问题 → 制定策略）
    ↓
[并行创建 N 个 Subagent]
    ↓
各 Subagent 独立执行：
  - Web 搜索（迭代式）
  - Interleaved Thinking（工具调用后评估结果）
  - 返回 findings 给 LeadResearcher
    ↓
LeadResearcher 综合结果（判断是否需要继续研究）
    ↓
[可选：创建新 Subagent 或调整策略]
    ↓
退出研究循环
    ↓
CitationAgent（处理文档 → 定位引用位置 → 生成带引用的报告）
    ↓
User
```

### Memory Checkpoint：防止上下文截断的机制

当 LeadResearcher 的上下文窗口接近 200K Token 阈值时，系统会**将分析计划保存到外部 Memory**。这是一个关键设计：

- 传统的 Context Window 满即截断 → Agent 丢失当前研究状态
- Anthropic 的方案：接近阈值时触发 checkpoint → 将计划序列化到外部存储 → Subagent 可以在后续从 Memory 中恢复完整上下文

这解决了多智能体系统中「Context 丢失」和「任务连续性」之间的矛盾。本质上，Memory 是第二个上下文层级——在 Agent 内部上下文之外的持久化上下文。

### CitationAgent：后处理的质量门

研究系统输出的不是原始搜索结果，而是经过引用的完整报告。CitationAgent 负责：

1. 处理所有 Subagent 返回的文档
2. 定位每个声明对应的具体来源
3. 生成带精确引用的研究报告

这将「研究质量」和「引用准确性」分离为独立的质量门——LeadResearcher 负责研究深度，CitationAgent 负责引用合规性。

---

## Token 预算：多智能体系统的核心度量

Anthropic 给出的一条关键数据将多智能体系统的设计逻辑提升到了理论层面：

> **在 BrowseComp 评测中，Token 使用量单独解释了 80% 的性能方差**。模型选择和工具调用次数是另外两个解释因素，三者共同解释了 95% 的方差。

这是一个反直觉但符合预期的结论：**更多的 Token 投入 = 更好的研究结果**。不是因为模型更聪明，而是因为更多的 Token 允许更深入的搜索、更广泛的探索、更完整的综合。

这条结论直接解释了为什么多智能体系统有效：

| 架构 | 单 Agent 上下文 | 总 Token 容量 |
|------|----------------|--------------|
| 单 Agent | 200K | 200K（上限） |
| 1 Lead + N Subagent | 200K × (N+1) | 200K × (N+1) |

每个 Subagent 拥有自己的 200K Token 上下文，系统总容量随 Subagent 数量线性扩展。

### Token 消耗的经济账

但 Token 扩展是有代价的：

| 对话类型 | Token 倍数（相对单次对话） |
|---------|----------------------|
| 普通 Chat | 1×（基线） |
| 单 Agent（带工具）| 4× |
| 多智能体 Research | 15× |

这意味着多智能体系统只有在**任务价值足够高**时才值得投入。Anthropic 的判断是：高价值任务 × 强并行性 × 信息量超过单上下文窗口 = 多智能体系统的适用场景。

> **工程建议**：在评估是否引入多智能体架构时，先问三个问题：（1）任务失败的经济损失有多大？（2）问题是否可以分解为独立子任务？（3）所需信息量是否超过 200K Token？如果三个答案都是「是」，多智能体是合理的。

---

## 并行化策略：两种并行，三个数量级

Anthropic 在实践中实现了两种层级的并行化，直接将复杂查询的研究时间压缩了 90%：

### 第一层：Lead → Subagent 的并行创建

传统模式：Lead Agent 串行创建 Subagent，一个完成再创建下一个
优化后：Lead Agent **一次性创建 3-5 个 Subagent**，全部并行启动

### 第二层：Subagent 内部的工具并行

传统模式：Subagent 串行调用搜索工具，一次搜完再搜下一次
优化后：每个 Subagent **同时调用 3+ 个搜索工具**，并行抓取多个信息源

这两种并行叠加的效果：研究时间从「小时级」压缩到「分钟级」，同时覆盖的信息量超过顺序执行的任何单 Agent 系统。

---

## Prompt Engineering 的六条核心原则

多智能体系统的行为完全由 Prompt 驱动——每个 Agent 收到不同的指令集，行为协调完全通过自然语言完成。Anthropic 总结了六条关键原则：

### 1. Think Like Your Agents

要优化 Prompt，必须先理解 Prompt 对 Agent 的实际影响。Anthropic 的做法是用 Console 模拟真实系统，逐步观察 Agent 行为。这揭示了典型失败模式：
- Agent 在已获得充分结果时仍继续搜索
- 使用过于冗长的搜索查询
- 选择错误的工具

### 2. Teach the Orchestrator How to Delegate

Lead Agent 需要将查询分解为子任务，并**向 Subagent 提供详细的描述**——包括：
- 具体目标
- 输出格式要求
- 工具和来源指导
- 清晰的任务边界

早期版本中，Lead Agent 的指令过于简略（如「研究芯片短缺」），导致 Subagent 之间出现任务重叠或遗漏。加入详细的任务边界描述后，重复工作显著减少。

### 3. Scale Effort to Query Complexity

Agent 无法本能判断不同任务所需的工作量。Anthropic 在 Prompt 中嵌入了明确的规模规则：

| 任务类型 | Agent 数量 | 工具调用次数 |
|---------|----------|------------|
| 简单事实查询 | 1 个 | 3-10 次 |
| 直接对比 | 2-4 个 | 10-15 次/个 |
| 复杂研究 | >10 个 | 各自明确分工 |

### 4. Tool Design is Critical

Agent-Tool 接口的重要性等同于人机接口。Anthropic 给 Agent 提供了明确的工具选择启发式规则：

- 先检查所有可用工具
- 将工具用途与用户意图匹配
- 通用探索用 Web 搜索，专用信息用专业工具
- 优先选择专用工具而非通用工具

> **关键发现**：Anthropic 甚至创建了一个 **Tool-Testing Agent**——给定一个有缺陷的 MCP 工具，它尝试使用该工具，然后重写工具描述以避免失败。这个 Agent 对同一工具测试数十次，找到了关键细微差别和 bug。使用改进后的描述，未来 Agent 的任务完成时间**下降了 40%**。

### 5. Start Wide, Then Narrow

研究策略应该模拟人类专家的做法：**先广度探索，再逐步深入**。Agent 倾向于使用过于具体、冗长的搜索查询（导致结果稀少），因此 Prompt 中明确要求先进行短查询、评估可用信息，再逐步收窄焦点。

### 6. Guide the Thinking Process

Extended Thinking 模式可以作为可控的草稿纸。Lead Agent 用 Thinking 模式规划方法、评估工具适用性、判断查询复杂度并确定 Subagent 数量。测试表明 Extended Thinking 显著改进了指令遵循、推理和效率。Subagent 则在工具调用后使用 **Interleaved Thinking** 评估结果质量、识别缺口并优化下一步查询。

---

## 生产级工程挑战

### 状态持久化与错误恢复

Agent 是有状态的长时运行系统——每个工具调用都可能改变环境状态。与传统软件不同，Agent 中的错误会复合：一个步骤失败可能导致 Agent 探索完全不同的轨迹。

Anthropic 的解法：
- **可恢复执行**：系统在错误发生后从 Agent 停止的位置继续，而非从头开始
- **智能错误处理**：当工具失败时，通知 Agent 并让它自主适应（而非强制终止）
- **模型智能 + 确定性保障**：AI Agent 的自适应能力 + 重试逻辑 + 定期 Checkpoint

### Rainbow Deployments

Agent 系统高度有状态，每次部署时系统中可能运行着处于任意状态的 Agent。不能同时将所有 Agent 更新到新版本。Anthropic 采用了 **Rainbow Deployments**：新旧版本同时运行，流量逐步从旧版本切换到新版本，避免中断正在执行的 Agent。

### 同步执行瓶颈

当前架构中 Lead Agent 以**同步方式**等待 Subagent 完成后才继续。这简化了协调，但创造了信息流瓶颈：Lead Agent 无法动态引导 Subagent，Subagent 之间无法直接协调，整个系统在等待某个 Subagent 时会阻塞。

**异步执行**是未来的优化方向：Agent 并发工作，在需要时动态创建新 Subagent。但异步带来了结果协调、状态一致性和错误传播的新挑战。

---

## 评估方法：Outcome-Based 而非 Process-Based

多智能体系统的评估比单 Agent 复杂得多——即使起点相同，Agent 也可能采取完全不同的有效路径到达目标。传统评测检查「是否遵循了预设步骤」，但这不适用于多智能体场景。

### 小样本快速启动

早期 Agent 开发中，Prompt 调整往往带来巨大影响（30% → 80% 成功率）。这种效应量下，**20 个真实使用模式查询**就足以清晰看到变化。Anthropic 的建议：不要等到建立大型评测集再启动，用少量样本立即开始测试。

### LLM-as-Judge 的正确用法

研究输出难以程序化评估（自由文本、无单一正确答案）。Anthropic 使用 LLM Judge，评估标准包括：
- 事实准确性（声明是否与来源匹配？）
- 引用准确性（引用的来源是否与声明对应？）
- 完整性（所有请求的方面都覆盖了吗？）
- 来源质量（是否优先使用了一手来源？）
- 工具效率（工具使用次数是否合理？）

**最有效的配置**：单一 LLM 调用 + 单一 Prompt + 输出 0.0-1.0 的分数 + 通过/失败判定。这比多 Judge 协作更一致，且与人类判断对齐良好。

### End-State Evaluation for Stateful Agents

对于修改持久状态的多轮 Agent，Anthropic 采用**终态评估**而非逐轮分析：
- 不验证 Agent 是否遵循了特定过程
- 验证 Agent 是否达到了正确的最终状态
- 对复杂工作流，设置离散 Checkpoint，验证特定状态变化是否在每个 Checkpoint 发生

---

## 与现有架构的对比

| 维度 | Anthropic Research | AutoGen | LangGraph |
|------|-------------------|---------|-----------|
| 编排模式 | Lead-Subagent | Agent-to-Agent | Graph-based |
| 上下文策略 | Memory Checkpoint | 共享状态 | 状态图 |
| 并行粒度 | Subagent 级别 | 消息级别 | 节点级别 |
| Token 效率 | 15× chat | 取决于配置 | 取决于配置 |
| 生产成熟度 | 自研生产系统 | 开源框架 | 开源框架 |

Anthropic 的方案是**自研生产系统**，不是开源框架。其设计决策反映了在生产环境运营多年积累的经验，尤其是 Rainbow Deployments、可恢复执行、Memory Checkpoint 这些在原型阶段不会遇到的问题。

---

## 核心工程判断

**多智能体系统的价值有明确的边界条件**：

适合的场景：
- 高价值任务（值得 15× Token 投入）
- 可并行分解的研究任务（无强依赖关系）
- 信息量超过单上下文窗口（>200K Token）
- 需要多方向同时探索

不适合的场景：
- 需要所有 Agent 共享同一上下文（强依赖关系）
- 大部分编码任务（并行化程度低）
- 实时协调要求高的场景（异步协调的复杂性当前过高）

**最重要的反直觉结论**：Token 预算扩展是多智能体系统的核心价值，而非「更智能的推理」。这条结论将多智能体架构从「AI 能力的涌现」降格为「系统工程问题」——扩展计算资源以解决更大规模的问题。

---

## 参考文献

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic 官方工程博客，一手来源
- [Multi-Agent Research System Cookbook](https://platform.claude.com/cookbook/patterns-agents-basic-workflows) — Anthropic 官方开源 Prompt 示例
- [Clio: What people use Claude Research for](https://www.anthropic.com/research/clio) — Research 功能使用数据分析
- [BrowseComp Evaluation](https://openai.com/index/browsecomp/) — OpenAI BrowseComp 基准评测
