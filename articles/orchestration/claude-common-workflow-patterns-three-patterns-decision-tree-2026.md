# Claude 三大 Workflow Pattern 决策树 2026

> 原文：[Common workflow patterns for AI agents and when to use them](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)（2026年3月5日，Anthropic Claude Platform 博客）

## 核心论点

**Workflow Pattern 不是模板，是带反模式的渐进式复杂度决策树**。Anthropic 在与数十个团队合作构建 AI Agent 系统后，给出了一个反直觉但工程上极其实用的判断：**生产环境中能覆盖绝大多数用例的 pattern 只有三个：sequential、parallel、evaluator-optimizer**——而这三者之间有清晰的升级路径和明确的"何时不升级"判断。

---

## 一、为什么 Workflow 仍然必要：自治不是无政府

### 1.1 完全自治 Agent 的盲区

一个完全自治的 Agent 决定一切：用哪些工具、按什么顺序执行、何时停止。**这种模式在生产中几乎从不工作**——不是因为 Agent 不够聪明，而是因为：

- **可预测性丢失**：用户和下游系统无法预测 Agent 何时会调用某个工具
- **成本失控**：Agent 可能陷入无限循环
- **调试困难**：当 Agent 行为出错时，没有清晰的"流程图"可以回溯
- **协调失效**：多 Agent 协作时，缺乏全局视图来协调

### 1.2 Workflow 的本质：自治的结构化容器

Workflow 不取代 Agent 的自治，而是**塑造自治的边界**：

> *"A workflow provides structure: it establishes the overall flow, defines checkpoints, and sets boundaries for how agents operate at each step, while still allowing dynamic behavior within those boundaries."*

**关键洞察**：每个步骤内仍然可以用 Agent 的推理和工具调用能力，但整体编排遵循已定义路径。**Workflow pattern = 步骤内的 Agent 智能 + 跨步骤的可预测流程**。

### 1.3 制造业类比的工程含义

作者用了一个精辟的类比：**Workflow 就像制造业的装配线**——每个工位都有技术工人做出具体决策，但整体流程是预先设计的，即使单个步骤涉及路由、重试等动态决策。

> *"If you've managed a team, you already understand workflows."*

这种类比的工程含义是：**Workflow pattern 的选择，本质上是在做"流程的预先定义"vs"步骤内的动态决策"的边界划分**——定义过细会失去 Agent 的灵活性，定义过粗会失去可预测性。

---

## 二、三大 Pattern：渐进式复杂度决策树

### 2.1 Pattern 1 — Sequential Workflow（顺序工作流）

**定义**：任务以预定顺序执行。每个阶段的 Agent 处理输入、做决策、调用工具、然后将结果传递给下一阶段。

```
输入 → Agent₁ → 检查点 → Agent₂ → 检查点 → Agent₃ → 输出
```

**何时使用**：
- 任务能自然分解为有清晰依赖的独立阶段
- 单一 Agent 处理整个任务时精度不够
- 每个步骤涉及本质上不同的工作（如生成营销文案 → 翻译成另一种语言）

**何时避免**：
- 单一 Agent 能可靠处理整个任务时（**复杂度上溢**）
- Agent 需要协作而非顺序交接时（**协作场景误判**）
- 强行把任务拆成 sequential 步骤时（**人为割裂**）

**Pro Tip — 单一 Agent 优先原则**：

> *"First try your pipeline as a single agent, where the steps are just part of the prompt. If that's good enough, you've solved the problem without additional complexity."*

这是非常重要的工程哲学：**Sequential workflow 的默认起点是单一 Agent**——只有当单 Agent 的能力边界被突破时，才升级到多 Agent sequential。

**适用案例**：
- 文档处理流水线（提取 → 验证 → 分类 → 入库）
- 内容生成（大纲 → 检查大纲是否达标 → 写正文）
- 多阶段决策流程（资格审查 → 风险评估 → 终审）

---

### 2.2 Pattern 2 — Parallel Workflow（并行工作流）

**定义**：独立任务分布到多个 Agent 同时执行，**不是等一个完成才开始下一个**，而是 fan-out/fan-in。

```
         → Agent₁ →
输入 →   → Agent₂ →   → 聚合 →
         → Agent₃ →
```

**何时使用**：
- 能分解为独立子任务且并行处理有收益
- 需要同一问题的多个视角（**多视角聚合**）
- **关注点分离**：不同工程师能独立拥有和优化单个 Agent 而不互相干扰
- 复杂任务中，每个考量用独立 AI 调用比一个调用处理所有更优

**何时避免**：
- Agent 需要累积上下文或必须建立在前一个 Agent 工作之上（**强依赖**）
- API 配额等资源约束使并发处理低效（**资源瓶颈**）
- 缺乏清晰的策略处理不同 Agent 的矛盾结果（**冲突无解**）
- 结果聚合太复杂或降低输出质量（**聚合失败**）

**Pro Tip — 聚合策略前置**：

> *"Design your aggregation strategy before implementing parallel agents. Will you take the majority vote? Average confidence scores? Defer to the most specialized agent?"*

**关键工程决策**：在写代码之前，先决定"如何合并结果"——多数投票？置信度平均？最专业 Agent 优先？**没有聚合策略的并行 = 收集无法解决的冲突输出**。

**类比分布式系统**：这与分布式系统中的 fan-out/fan-in 模式同构——你向多个 Agent 发送相同或相关工作，每个 Agent 独立处理，然后聚合或综合它们的输出。

**适用案例**：
- 多源数据并行提取（同时从 API、数据库、文件提取）
- 多角度分析（同一文档同时做摘要、关键点、风险分析）
- A/B 内容生成（同一 prompt 生成多个版本，选最优）

---

### 2.3 Pattern 3 — Evaluator-Optimizer Workflow（评估器-优化器工作流）

**定义**：两个 Agent 配对成迭代循环——一个生成内容，另一个根据特定标准评估，生成器基于反馈优化。**直到输出达到质量门槛或达到最大迭代次数**。

```
输入 → Generator → Evaluator → 反馈 → Generator → Evaluator → ... → 输出
        ↑__________________________|
```

**核心洞察**：

> *"The key insight is that generation and evaluation are different cognitive tasks. Separating them lets each agent specialize—the generator focuses on producing content, the evaluator focuses on applying consistent quality criteria."*

**生成与评估是不同认知任务**——分开让两个 Agent 各司其职，生成器专注产出，评估器专注一致的质量标准。

**何时使用**：
- 有清晰可衡量的质量标准，AI 评估器能一致应用
- 首次尝试与最终质量之间的差距值得额外的 tokens 和延迟
- 评估标准足够客观，能被 AI 评估器一致执行

**何时避免**：
- 首次尝试质量已满足需求（**无意义迭代**）
- 实时应用需要即时响应（**延迟敏感**）
- 简单常规任务如基础分类（**杀鸡用牛刀**）
- 评估标准过于主观，AI 评估器无法一致应用（**标准模糊**）
- 有确定性工具可用（如代码风格的 linter）——用 linter 而非 AI 评估器（**工具替代**）
- 资源约束超过质量改进（**ROI 负**）

**Pro Tip — 明确停止条件**：

> *"Set clear stopping criteria before you start iterating. Define maximum iteration counts and specific quality thresholds. Without these guardrails, you can end up in expensive loops where the evaluator keeps finding minor issues and the generator keeps tweaking, but quality plateaus well before you stop iterating."*

**反模式警告**：没有停止条件 → 评估器持续找小问题 → 生成器持续微调 → 质量 plateau 在停止前很久。**"知道'够好就是够好'"是 evaluator-optimizer 的核心心法**。

**适用案例**：
- 复杂代码生成（生成 → 静态分析 → 修复 → 重生）
- 研究报告（生成初稿 → 引用准确性检查 → 优化）
- 翻译质量保证（翻译 → 一致性评估 → 优化）
- 创意写作（生成故事 → 情节连贯性评估 → 优化）

---

## 三、决策树：从最简单开始

### 3.1 核心决策原则

> *"Start with the simplest pattern that solves your problem. Default to sequential. Move to parallel when latency is the bottleneck and tasks are independent and add evaluator-optimizer loops only when you can measure the quality improvement."*

**默认路径**：
1. **首先尝试单 Agent**（最简单）
2. 失败 → **Sequential**（清晰依赖）
3. 性能瓶颈 + 任务独立 → **Parallel**（加速）
4. 质量门槛 + 可衡量 → **Evaluator-Optimizer**（精度）

### 3.2 决策流程图

```
                ┌──────────────────────┐
                │ 任务能用单 Agent 解决？│
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │ YES                    │ NO
              ↓                         ↓
        ┌──────────┐         ┌──────────────────────┐
        │ 单 Agent │         │ 任务有清晰阶段依赖？  │
        └──────────┘         └──────────┬───────────┘
                                        │
                           ┌────────────┴────────────┐
                           │ YES                    │ NO
                           ↓                         ↓
                    ┌────────────┐         ┌──────────────────┐
                    │ Sequential │         │ 任务能并行独立？  │
                    └────────────┘         └──────────┬───────┘
                                                    │
                                       ┌────────────┴────────────┐
                                       │ YES                    │ NO
                                       ↓                         ↓
                                ┌──────────┐         ┌────────────────┐
                                │ Parallel │         │ 需质量迭代？    │
                                └──────────┘         └───────┬────────┘
                                                              │
                                                 ┌────────────┴────────────┐
                                                 │ YES                    │ NO
                                                 ↓                         ↓
                                       ┌──────────────────┐        ┌────────────┐
                                       │ Evaluator-       │        │ 回到单     │
                                       │ Optimizer        │        │ Agent 重新 │
                                       └──────────────────┘        │ 设计      │
                                                                  └────────────┘
```

### 3.3 模式组合：可嵌套

**三大 Pattern 不是互斥的，可以嵌套**：

> *"You can nest them as complexity demands. A sequential workflow can incorporate parallel processing at bottleneck stages. An agentic approach can add evaluation when quality standards tighten."*

**实际案例**：
- Sequential 整体流程中，并行处理某个瓶颈阶段
- Sequential 后接 Evaluator-Optimizer（sequential 完成基础工作，evaluator-optimizer 优化质量）
- Parallel 多个分支各自接 Evaluator-Optimizer

**关键工程心法**：

> *"The key is matching pattern complexity to actual requirements. Don't add parallel processing because you can—add it when concurrent execution provides clear benefits. Don't implement evaluator-optimizer loops unless they improve output quality in a way you can measure."*

**复杂度匹配实际需求，不是能力越多越好**。

---

## 四、Pattern 选择的工程陷阱

### 4.1 过度复杂化（Over-engineering）

**症状**：使用 Parallel + Evaluator-Optimizer 组合，但任务用 Sequential 就能解决。

**根因**：开发者从"框架能做什么"出发，而非"问题需要什么"出发。

**对策**：强制从单 Agent 起步，逐步升级；每升一级要能明确"上一级哪里不够"。

### 4.2 评估器失效（Evaluator Failure）

**症状**：Evaluator-Optimizer 陷入"评估器持续找小问题，生成器持续微调"的死循环。

**根因**：缺少明确的停止条件（最大迭代次数 + 质量门槛）。

**对策**：开始迭代前定义 stopping criteria（max iterations + quality threshold）；同时监控 token 消耗与质量改进的 ROI。

### 4.3 并行冲突无解（Unresolvable Parallel Conflicts）

**症状**：Parallel 模式中，多个 Agent 返回相互矛盾的结果，无法合并。

**根因**：缺少聚合策略，或聚合策略本身过于复杂。

**对策**：实现前明确聚合策略（多数投票/置信度平均/最专业 Agent 优先）；如果无法定义清晰的聚合策略，**任务本身可能不适合 Parallel 模式**。

### 4.4 Sequential 人为割裂（Artificial Decomposition）

**症状**：把本应一气呵成的任务强行拆成多个 sequential 步骤。

**根因**：开发者预设"多 Agent = 更强大"。

**对策**：尝试单 Agent 路线；只有在单 Agent 确实无法处理时，才升级到 sequential。

---

## 五、与现有 Agent 框架的关系

### 5.1 LangGraph / AutoGen

这些框架提供 Pattern 1-3 的实现原语：
- **Sequential** = 节点 + 边（edges）
- **Parallel** = 多个 Send 边 + 聚合节点
- **Evaluator-Optimizer** = 条件边 + 循环

**关键差异**：Anthropic 的 pattern 分类是**业务层抽象**（"为什么用哪种"），而 LangGraph / AutoGen 是**实现层抽象**（"如何用代码画流程图"）。

### 5.2 Anthropic Building Effective Agents 的延伸

Anthropic 之前的 `building-effective-agents` 提出了**五种架构模式**（prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer），而 `common-workflow-patterns` 是**更精简的三大 pattern**——这一精简反映了 Anthropic 与"数十个团队"合作后的实战提炼：

- 实际生产中**最常用**的就是 sequential + parallel + evaluator-optimizer
- 其他模式（orchestrator-workers、routing）可视为这三大 pattern 的**嵌套或变体**

### 5.3 与 Skills、Subagent、MCP 的协同

- **Sequential + Skills**：每个 sequential 阶段可以挂载特定 skills（如金融分析 → 法务审查 → 合规检查）
- **Parallel + Subagent**：每个并行分支可以是一个 subagent（隔离 context）
- **Evaluator-Optimizer + MCP**：评估器可以通过 MCP 调用确定性工具（linter、test runner）来执行评估

---

## 六、实战决策清单（Decision Checklist）

在选择 Workflow Pattern 时，按以下顺序回答：

- [ ] **Q1**: 任务能用单一 Agent 解决吗？
  - 是 → 单 Agent（不引入 workflow）
  - 否 → 进入 Q2

- [ ] **Q2**: 任务能自然分解为有清晰依赖的阶段吗？
  - 是 → Sequential workflow
  - 否 → 进入 Q3

- [ ] **Q3**: 任务能分解为独立子任务，且并发有收益吗？
  - 是 + 能定义清晰聚合策略 → Parallel workflow
  - 否 → 进入 Q4

- [ ] **Q4**: 有清晰可衡量的质量标准，且首次质量不达标吗？
  - 是 + 能定义 stopping criteria → Evaluator-Optimizer
  - 否 → 重新设计任务（可能任务本身定义不清）

- [ ] **Q5**: 三大 pattern 的某种嵌套能解决吗？
  - 是 → 嵌套组合（如 sequential + parallel 在瓶颈处）
  - 否 → 可能需要重新审视任务边界

---

## 七、总结：Pattern 选择的"反共识"哲学

Anthropic 的核心反共识：**在生产环境中，最成功的实现不是用最复杂的框架，而是用最简单的 pattern**。三大 workflow pattern（sequential / parallel / evaluator-optimizer）能覆盖绝大多数用例。

**心法总结**：
1. **从最简单开始**：单 Agent 优先，逐步升级
2. **Pattern 是路径而非模板**：根据瓶颈选择（sequential → parallel → evaluator-optimizer）
3. **复杂度匹配实际需求**：不是 framework 能做什么，而是问题需要什么
4. **嵌套而非互斥**：三大 pattern 可组合，但每加一层要能解释为什么
5. **明确停止条件**：evaluator-optimizer 必须有 max iterations + quality threshold

> *"The right workflow pattern depends on your task structure, quality requirements, and resource constraints."*

**Workflow Pattern 的选择 = 在"自治灵活性"与"结构可预测性"之间的精确工程权衡**。这个权衡的答案不是固定的，而是取决于具体任务的依赖结构、性能要求、质量门槛三者的交集。

---

## 参考资源

- 原文：[Common workflow patterns for AI agents and when to use them](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)
- Anthropic 完整白皮书：[Building effective AI agents: architecture patterns and implementation frameworks](https://www.anthropic.com/engineering/building-effective-agents)
- 工具设计哲学对比：R393.5 Seeing Like an Agent 文章（`articles/fundamentals/claude-seeing-like-an-agent-tool-design-philosophy-2026.md`）
- Sequential 实战案例：LangChain LangGraph
- Evaluator-Optimizer 实战案例：Cursor Auto-Review（R391）
