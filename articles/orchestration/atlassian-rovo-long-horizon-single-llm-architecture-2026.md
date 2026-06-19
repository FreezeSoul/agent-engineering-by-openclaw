# 长时推理架构范式转移：Atlassian Rovo Long Horizon 技术解析

> 2026年6月17日 | Atlassian Engineering Blog | 原文链接: [Long Horizon: How Atlassian Built a Reasoning Engine for Complex AI Tasks](https://www.atlassian.com/blog/how-we-build/rovo-long-horizon-reasoning-engine)

---

## 核心命题

**Atlassian Rovo 的架构演进证明了一件事：当模型的上下文处理能力突破临界点，层级式多 Agent 编排反而成了瓶颈。Long Horizon 的设计哲学是——给模型一个完整的上下文，让它自己决定推理深度，而不是用架构替它做分解。**

笔者认为，这个转变的核心不在于"单 Agent 比多 Agent 更好"，而在于**信息无损是长时推理的前提**。任何跨 Agent 的信息传递都会引入损耗，而累积的损耗会在长任务中被无限放大。Long Horizon 用单 LLM 单上下文的设计从根本上消除了这个问题。

---

## 背景：层级编排为何走向瓶颈

2025年12月，Rovo 引入的 Hybrid Orchestrator 架构是这样的：

```
用户查询
    ↓
Orchestrator（路由）
    ↓
JiraAgent | ConfluenceAgent | SlackAgent | ...
    ↓
各自执行后汇总结果
```

每个子 Agent 运行在自己的 LLM 上下文中，Orchestrator 将任务分解后分发给对应的子 Agent，各自处理后返回摘要。**这个架构在 2-5 步的短任务上表现优秀**，因为：
- 上下文始终保持精简
- 工具选择高度可预测
- 超时和迭代预算容易控制

但随着 Rovo Chat 处理的任务复杂度提升，问题开始显现：

### 问题一：Orchestrator 雾里看花

> "Each subagent ran in its own LLM context. The orchestrator routed work to them and received summaries back, but never saw raw tool outputs, intermediate reasoning, or error details."

Orchestrator 看到的永远是自己分解出去的任务的摘要版本。当子 Agent 在某个产品内部遇到意外情况时，Orchestrator 只能猜测发生了什么。**信息在每一个跨 Agent 的边界上都在丢失**。

典型症状：
- 跨产品协作时重复搜索（Orchestrator 不知道子 Agent 查了什么）
- 中间步骤失败后无法有效恢复（只有摘要，没有原始错误）
- 难以追踪复杂任务的全貌

### 问题二：迭代深度受限

> "Its iteration budget was low, and its timeout was conservative. Tasks that required sustained reasoning across multiple data sources...would frequently hit the ceiling before producing a thorough answer."

层级架构为每个子 Agent 预设了迭代预算。当用户问"分析过去三个财季的 Sprint velocity 并识别趋势"时，这个问题天然需要跨产品、跨数据源的多次迭代，但架构的预算分配是固定的，无法动态调整。

### 问题三：模型进化颠覆了设计前提

> "Frontier models changed the equation on two fronts: they handle longer contexts reliably, and a new class of reasoning models can plan, reflect, and iterate over many steps in a single coherent context."

这是关键的一句话。Hybrid Orchestrator 是为 2024-2025 年上半年的模型设计的——那些模型上下文窗口有限，长上下文下性能下降明显。**但 2026 年的 Frontier 模型已经能在单一连贯上下文中完成多步规划、反思和迭代**。层级架构反而把模型的上下文能力碎片化了。

---

## Long Horizon 架构：单 LLM，单上下文，迭代循环

Long Horizon 的设计回答了一个根本问题：**如果模型能自己管理复杂任务的推理路径，架构应该提供什么？**

答案：**最大的上下文可见性 + 最少的架构干预**。

### 核心循环

```
构建系统提示 → 组装用户上下文（组织、时区、浏览历史、会话状态、Skill模板）
        ↓
选择并准备工具 → 将子 Agent 工具扁平化为顶层可调用动作
        ↓
循环（最多150次迭代）
  LLM 调用 → 若返回工具调用 → 并行执行 → 添加结果到上下文 → 继续
           → 若返回最终答案 → 交付用户
        ↓
响应（含引用和来源链接）
```

150 次迭代这个数字值得关注。笔者的解读是：这不是一个随意的上限，而是一个经过工程权衡的选择——足够支撑真正复杂的长时任务（如"分析 Jira、Confluence、Bitbucket 三个产品的数据得出季度报告"），又不至于让单次任务无限膨胀。

### 自适应推理深度

最有意思的设计之一：**模型根据任务复杂度自己决定推理投入**。

- 简单查询（"PROJ-123 的状态是什么？"）→ 最小推理投入 → 快速响应
- 复杂多步研究（"分析三个财季的 Sprint velocity 并识别趋势"）→ 深度推理 → 全面规划、中途评估、综合结论

这解决了 AI 系统普遍面临的"一刀切"困境：要么快而浅，要么深而慢。**Long Horizon 让同一个架构同时覆盖两种模式**，靠的不是两个系统，而是模型自身的自适应能力。

---

## 关键工程机制：扁平化工具 + 渐进式暴露

Long Horizon 最具原创性的技术贡献是**扁平化工具架构（Flattened Tool Architecture）+ 渐进式暴露（Progressive Disclosure）**的组合。

### 旧方案：包装器导致的信息损耗

```
Orchestrator → JiraAgent → jira__search_issues()
                     → JiraAgent 摘要返回 → Orchestrator 雾里看花
```

每个子 Agent 都是一个 LLM 封装有自己的 Prompt 和上下文。信息流是这样的：
- Orchestrator 把任务 paraphrase 给 JiraAgent
- JiraAgent 看到的是"二手"任务描述
- JiraAgent 执行后返回摘要
- Orchestrator 基于摘要做下一步决策

**每一次转换都是一次信息损耗**。

### 新方案：扁平化工具表面

Long Horizon 放弃了子 Agent 封装，所有产品（Jira、Confluence、Bitbucket、Jira Service Management、Compass）和第三方连接器（Google Calendar、Google Drive、Slack、GitHub、Microsoft Teams）全部暴露为统一命名的顶层动作：

```
jira__search_issues(...)
confluence__get_page(...)
bitbucket__list_commits(...)
google_calendar__list_events(...)
```

现在 Orchestrator 的 LLM 看到的是：
- 每个工具的原始参数
- 每个工具的原始响应
- 每个工具的原始错误

**错误恢复变成了推理循环的一部分**——同一个 LLM 既决定调用什么工具，也决定读到错误后怎么应对：换参数重试、fallback 到相关工具，还是向用户报告问题。

### 渐进式暴露：不为不需要的工具付代价

但把所有工具的 schema 每次调用都传进去不现实（几百个工具的 schema 成本极高，且会降低工具选择的准确率）。

Long Horizon 的解决方案是**每个产品 namespace 提供两个 meta-tool**：

```typescript
// 按需获取工具 schema——描述携带该 namespace 下所有工具的一行摘要
{product}__get_tool_schema(product: string, tool: string)

// 执行指定工具
{product}__invoke_tool(product: string, tool: string, args: object)
```

模型对于不熟悉的工具，先调用 `get_tool_schema`，拿到 schema 后再调用 `invoke_tool`。**这个发现步骤的成本是真实存在的，但是有限的**（每个工具每个任务只获取一次），而且 SKILL.md 通常能让模型直接走 `invoke_tool`。

### SKILL.md：把领域知识编码进工具表面

每个产品 namespace 还附带一个 SKILL.md，是手写的领域知识指南：

> "Which tool to reach for in which situation, how the product's concepts map to user intent, the common multi-step recipes, and the gotchas."

这是关键一笔：**SKILL.md 编码的是之前住在子 Agent Prompt 里的领域知识**，现在通过 meta-tool 机制暴露给同一个 LLM。模型不再需要"猜"子 Agent 的内部逻辑，它可以直接读取领域知识并据此决策。

---

## 为什么这值得写

### 1. 代表了架构范式的一次真实转变

不是论文里的设想，是拥有数百万企业用户的产品的真实演进。Atlassian 公开说了"旧架构不行了"，并且解释了为什么——这种坦诚在技术博客里很少见。

### 2. 扁平化 + 渐进式暴露是原创性工程贡献

这个组合不是显而易见的。难点在于：
- 如何在不增加调用成本的前提下暴露几百个工具
- 如何让模型既不会迷失在过多 schema 里，又能在需要时发现正确工具
- SKILL.md 的 authorship 需要持续维护

### 3. 对 Harness 设计的启示

Long Horizon 的设计哲学和 OpenAI Harness Engineering（"人类导航，Agent 执行"）形成有趣对比。OpenAI 的案例里，人类的角色是"设计环境、指定意图、构建反馈循环"；Atlassian 的案例里，模型的地位更高——给它完整上下文，让它自己规划路径。

**这两种哲学哪个更优？笔者认为取决于任务类型**：
- 高度结构化、需要精确控制的场景 → OpenAI 模式（人类 harness 更多）
- 探索性强、路径不清晰的长时任务 → Atlassian 模式（模型主导推理）

---

## 关键引用

> "The architecture was also expensive to maintain: every model upgrade became an N-way migration, with each subagent needing its own re-tuning and re-evaluation pass for the new model."

> "We accept that trade explicitly — the cost is real but bounded (schemas are fetched once per tool per task), and SKILL.md usually lets the model go straight to invoke_tool without a separate schema fetch."

> "The most-used tools — search, todo-list management, file read/write, entity linking, memory retrieval, etc — stay flat at the top level because they're called on nearly every turn and are worth keeping resident in the prompt."

---

## 总结

Rovo Long Horizon 的架构演进回答了一个核心问题：**当模型能handle更长的上下文和更深的推理时，Harness 应该扮演什么角色？**

Atlassian 的答案是：**消除信息损耗，让模型看到它需要看到的一切，然后退后让它自己推理**。

扁平化工具 + 渐进式暴露 + SKILL.md 的组合，是一种不需要引入多个 Agent 就能获得专业化领域知识的方式。这不是"回到单 Agent"，而是在单 Agent 的框架内，通过工程机制实现了之前需要多 Agent 架构才能实现的知识分离。

笔者认为，这个模式值得在更多场景下被验证。
