# OpenAI Harness 工程实践：零手动代码的团队协同范式

> 本文解读自 OpenAI 工程博客 *Harness engineering: leveraging Codex in an agent-first world*（2026年2月）。
> 原文链接：https://openai.com/index/harness-engineering/

---

## 核心命题

**OpenAI 用 Codex 构建了一个完全由 AI 驱动的产品团队：0 行手动代码，5 个月交付百万行代码，系统核心是 Harness——一个将人类意图转化为可靠机器执行的工程框架。**

这不是概念验证。这是真实的生产系统，有内部用户、外部 alpha 测试者、CI 部署和真实流量。OpenAI 的工程师在其中的角色不是"写代码的人"，而是"设计环境、设计意图、构建反馈循环的人"。

---

## 背景：为什么 OpenAI 要做这件事

OpenAI 团队在 2025 年 8 月启动了一个实验：在没有预先存在的手写代码情况下，完全由 Codex 构建一个完整产品。约束是刻意的：**人类负责掌舵，Agent 负责执行。**

这个约束背后是一个更深的问题：当软件工程团队的主要工作不再是写代码，而是"设计环境、表达意图、构建反馈循环"时，**哪些旧的工程实践变得低效，哪些新的实践必须被发明出来？**

答案是：**几乎所有传统工程实践都需要被重新发明。**

---

## 一、工程师的新角色：从代码作者到系统架构师

OpenAI 团队第一个突破性的发现是：**早期进展比预期慢，不是因为 Codex 能力不足，而是环境描述不足。**

当人类工程师不再直接写代码，他们的工作变成了：

1. **深度优先地拆解目标**：把大目标分解成小的构建块（设计、代码、审查、测试等）
2. **为 Codex 构建工具和抽象**：Agent 需要内部结构才能向复杂目标推进
3. **问正确的问题**："什么能力缺失了？如何让它对 Agent 既清晰又可执行？"

> "The fix was almost never 'try harder.' Because the only way to make progress was to get Codex to do the work, human engineers always stepped into the task and asked: 'what capability is missing, and how do we make it both legible and enforceable for the agent?'"
>
> — OpenAI Engineering Blog

这句话揭示了 Harness 工程的本质：**当你的工具是 Agent 时，改进的路径不是催促它，而是改进它所依赖的环境。**

---

## 二、Ralph Wiggum Loop：Agent 审查链

OpenAI 团队发明了一个他们称为 **Ralph Wiggum Loop** 的工作流：

```
人类描述任务 → Codex 执行 → Codex 自己审查自己的变更 → 
请求额外的特定 Agent 审查（本地 + 云端）→ 响应人类/Agent 反馈 → 
迭代直到所有 Agent 审查者满意 → 合并 PR
```

关键设计：**人类可以审查 PR，但不是必须的。** 随着时间推移，团队将几乎所有审查工作推给了 Agent-to-Agent 流程。

这背后是一个工程经济学的判断：**在 Agent 吞吐量远超人类注意力的系统中，修正很廉价，等待很昂贵。**

---

## 三、仓库知识作为系统记录

Context 管理是 Agent 做大任务时的最大挑战之一。OpenAI 踩过了一个经典的坑：**"一本超大 AGENTS.md 说明书"方法。**

这个方法失败的四个原因：

| 问题 | 后果 |
|------|------|
| Context 是稀缺资源 | 超大指令文件挤占了任务、代码和关键文档 |
| 过度指导变成无指导 | 当所有事情都标注"重要"，就没有优先级可言 |
| 文档立刻腐化 | Agent 分不清哪些规则仍然有效，人类停止维护 |
| 难以验证 | 单个 blob 无法做机械检查（覆盖率、新鲜度、所有权）|

**正确的解法：AGENTS.md 是目录，不是百科全书。**

```
AGENTS.md（~100行）→ 入口地图
docs/（知识库）→ 系统记录
  ├── 设计文档（带验证状态）
  ├── 架构文档（顶层领域映射）
  ├── 质量文档（每个领域的评分和差距）
  └── 执行计划（版本化 + 共置）
```

Plans 被当做一等公民：轻量临时计划用于小改动，复杂工作使用执行计划（execution plans），活跃计划、已完成计划和已知技术债全部版本化并与代码共置。

**关键机制**：用 linter 和 CI job 强制知识库是最新的、交叉链接的、结构正确的。一个定期的"文档园丁"Agent 扫描过时或虚假文档，并提交修复 PR。

---

## 四、Agent 可读性是目标

因为代码库完全由 Agent 生成，代码**首先为 Codex 的可读性优化**，然后才是人类。

这带来一个重要的权衡取舍：**Agent 能访问的才存在。** 存在于 Google Docs、聊天记录或人类脑海中的知识，对 Agent 来说等于不存在。

解决方案是把更多信息推入仓库：**依赖和抽象必须能被完全内部化并在仓库内被推理**。技术上被称为"无聊"的技术栈（可组合性、API 稳定性、在训练集中的表示）往往更适合 Agent。

> "Pulling more of the system into a form the agent can inspect, validate, and modify directly increases leverage—not just for Codex, but for other agents that are working on the codebase as well."
>
> — OpenAI Engineering Blog

---

## 五、通过架构强制执行品味

没有机制保证，完全由 Agent 生成代码库会失去一致性。OpenAI 的解法是：**通过不变量强制执行，而不是微观管理实现。**

每个业务领域被划分为固定的一组层，强制验证依赖方向和允许的边缘集合：

```
Types → Config → Repo → Service → Runtime → UI
```

跨领域关注点（认证、连接器、遥测、功能开关）通过单一显式接口进入：**Providers**。其他一切都不允许，并通过自定义 linter 和结构测试强制执行。

**为什么这很重要**：这种架构通常是有数百名工程师时才考虑的。但有了编码 Agent，它是早期的前置条件：**约束是允许速度而不衰减或不漂移的东西。**

OpenAI 将 taste invariants 编码为机械规则：结构化日志、命名约定、schema 类型、文件大小限制、平台特定可靠性要求。关键在于：**linter 的错误消息被设计为将修复指令注入 Agent context**。

> "In a human-first workflow, these rules might feel pedantic or constraining. With agents, they become multipliers: once encoded, they apply everywhere at once."
>
> — OpenAI Engineering Blog

---

## 六、吞吐量改变了合并哲学

随着 Codex 吞吐量增加，许多常规工程规范变得适得其反。

OpenAI 的仓库以**最小化阻塞合并门控**运作。PR 生命周期很短。测试 flake 通常通过后续运行解决，而不是无限期阻塞进度。

背后的逻辑：在 Agent 吞吐量远超人类注意力的系统中，**修正很廉价，等待很昂贵**。

这在低吞吐量系统中是不负责任的。但当 3.5 个 PR/工程师/天 的吞吐量成为常态时，传统的等待 gate 反而成了瓶颈。

---

## 七、与传统 Harness 工程的关联

这篇 OpenAI 文章实际上是 Harness 工程方法论的一个**大规模生产验证**。几个关键关联：

### 1. 反馈循环设计

OpenAI 的 Ralph Wiggum Loop 本质上是一个**多 Agent 评估循环（evaluator loop）**的实现：

- Codex 执行 → Agent 审查者评估 → 不满意则返回重做
- 等待廉价 → 纠正成本低
- 人工审核不是必须的

### 2. 上下文工程

AGENTS.md 作为目录而非百科全书的方法，与 context-memory 章节的 **RAG 与语义缓存** 原则完全一致：让 Agent 从小、稳定、可发现的入口开始，然后向更深层引导。

### 3. 架构即约束

OpenAI 发现：**约束在人类工程中感觉是微观管理，在 Agent 工程中是乘数。** 这与 Harness 设计中"安全防护即乘数"的观点呼应。

### 4. 长期运行与恢复

OpenAI 的架构支持 Codex 单次运行工作超过六小时（通常在人类睡眠时）。这需要健壮的 checkpoint 和进度持久化机制——与"接力/恢复机制"维度直接相关。

---

## 八、为什么这对 Agent 工程师重要

OpenAI 这篇文章之所以重要，不是因为它描述了一个 AI 编码工具，而是因为它揭示了**当 Agent 成为主要执行者时，工程实践必须如何改变**：

| 传统实践 | Agent-First 实践 |
|---------|----------------|
| 人类写代码，Agent 辅助 | 人类设计环境，Agent 执行 |
| 代码是主要交付物 | 环境/流程/约束是主要交付物 |
| Context 文档是百科全书 | Context 文档是目录索引 |
| 架构是后期考虑 | 架构是 Agent 效率的前置条件 |
| 合并门控保守 | 合并门控激进（修正廉价，等待昂贵）|

---

## 九、OpenClaw 的位置

值得注意的是，OpenAI 的实践与 OpenClaw 的设计哲学高度一致：

- **Structured docs/ 作为知识库**：OpenClaw 使用 SOUL.md、USER.md、AGENTS.md 作为结构化知识记录
- **反馈循环驱动**：OpenClaw 的 heartbeat 机制本质上是一个轻量级的 harness loop
- **环境即乘数**：OpenClaw 的 skill 机制将环境能力封装为可复用单元

Harness 工程不是一个框架，而是一种**以环境设计为中心的新工程范式**。OpenAI 的实验证明了这种方法在百万行代码规模上的可行性。

---

## 原文引用

> "Over the past five months, our team has been running an experiment: building and shipping an internal beta of a software product with 0 lines of manually-written code."
>
> "Humans steer. Agents execute."
>
> "Because the only way to make progress was to get Codex to do the work, human engineers always stepped into the task and asked: 'what capability is missing, and how do we make it both legible and enforceable for the agent?'"
>
> "In a human-first workflow, these rules might feel pedantic or constraining. With agents, they become multipliers: once encoded, they apply everywhere at once."
>
> — OpenAI Engineering Blog, *Harness engineering: leveraging Codex in an agent-first world*

---

**相关主题**：[Harness 工程](../harness/) | [多 Agent 编排](../orchestration/) | [AI Coding 实践](../../practices/ai-coding/)