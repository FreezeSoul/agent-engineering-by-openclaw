# Anthropic 最新实践指南：六种 Agent 模式的选择树

> 本文解读 Anthropic 2026 年 6 月发布的官方工程博客 *Building Effective AI Agents*，剖析其提出的六种 Agent 架构模式，以及背后最被忽视的设计原则：**从最简单的开始，只在必要时增加复杂度**。

---

## 反直觉的发现：最成功的团队不用复杂框架

过去一年，Anthropic 与数十个团队合作构建 LLM Agent 系统后发现了一个反直觉的事实：

> *"Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."*

这个结论来自一线工程实践，不是论文假设。Anthropic 明确指出：很多团队在引入复杂框架之前，根本没有充分挖掘简单模式的潜力。

本文的核心论点不是介绍这六种模式——官方文档已经写得很清楚。本文的独特价值在于：**剖析这套模式背后的决策逻辑，以及为什么"从简单开始"是 Agent 工程中最难遵守的原则**。

---

## 六种模式的层次结构

Anthropic 提出的不是一张平铺的菜单，而是一棵**从简单到复杂的决策树**。每一层增加的能力都对应着前一层无法解决的场景。

### Level 0: Augmented LLM —— 所有模式的基础

无论选择哪种模式，起点都是同一个：**增强版 LLM**。

增强的三个维度：
- **检索**（Retrieval）：从外部知识源获取相关上下文
- **工具**（Tools）：调用外部 API、执行代码、操作文件系统
- **记忆**（Memory）：在多次交互中积累状态

Anthropic 特别提到了 MCP（Model Context Protocol），认为这是连接第三方工具生态的标准接口。这句话的工程含义是：**工具接口的标准化比工具本身更重要**。

笔者认为：大多数 Agent 项目在还没有定义清楚"我的 Agent 需要哪些工具能力"之前，就急于选择框架。Augmented LLM 的三维度框架提供了一个低成本的检验清单。

---

### Level 1: Prompt Chaining —— 可分解任务的精确匹配

**适用场景**：任务可以干净地分解成固定序列的子任务，每个子任务输出是下一个的输入。

```
输入 → LLM1 → 检查点 → LLM2 → 检查点 → LLM3 → 输出
```

典型案例：
- 生成营销文案 → 翻译成另一种语言
- 写大纲 → 检查大纲是否达标 → 写正文

**工程含义**：当任务边界清晰时，Prompt Chaining 的延迟增加是明确的，每次 LLM 调用都在一个更容易的子任务上，因此准确率更高。Anthropic 用"trade latency for higher accuracy"描述这种权衡——这是可预测的性能交换。

**笔者认为**：Prompt Chaining 是最被低估的模式。大多数人觉得它太简单，但实际上它覆盖了大多数企业知识管理场景（文档处理、内容生成、数据转换）。只有在 Prompt Chaining 明确无法满足需求时，才有理由进入下一层。

---

### Level 2: Routing —— 分类驱动的资源优化

**核心思想**：不同类型的输入应该分发到不同的专用处理路径，而不是经过同一个通用的 LLM 流水线。

```
输入 → 分类器 →专用路径A（小型廉价模型）
                  → 专用路径B（大型高能力模型）
                  → 专用路径C（另一个专用模型）
```

典型案例：
- 客服场景：退款请求 → 退款专用流程；技术问题 → 技术支持流程；通用问题 → FAQ 流程
- 模型分层：小问题用 Haiku 4.5，复杂问题用 Sonnet 4.5

**关键工程决策**：分类器的准确率是整个 Routing系统的瓶颈。Anthropic 指出可以用 LLM 做分类，也可以用传统 ML 模型——选择取决于场景对分类准确率的敏感度。

**笔者认为**：Routing 的真正价值不是省钱，而是**解耦不同任务对模型能力的需求差异**。一个客服 Agent 如果对所有输入都调用最强模型，成本会很高，但更重要的是：小任务被过度处理可能导致不必要的复杂输出。在 Agent 场景中，"正确的模型处理正确的任务"比"最强的模型处理所有任务"更符合工程经济学。

---

### Level 3: Parallelization —— 并行化以换质量和速度

Anthropic 区分了两种并行化：

**Sectioning（分区）**：将一个任务分解为独立的子任务，并行执行后聚合结果。
- 适用：一个 LLM 调用难以同时处理多个正交维度的复杂输入
- 案例：Guardrail 场景——一个 LLM 处理用户查询，另一个 LLM 并行审查输入内容是否涉及敏感操作

**Voting（投票）**：用相同的任务多次执行，获得多样化的输出结果。
- 适用：需要高置信度或需要覆盖多种视角的场景
- 案例：代码安全审查——多个不同提示词对同一段代码进行漏洞扫描，任何一个发现问题即标记

```
Sectioning:  [任务] → [并行子任务A] → [并行子任务B] → [聚合]
                             ↘ ↗
Voting:      [任务] → [执行1] → [执行2] → [执行3] → [多数票/全票]
```

**笔者认为**：Parallelization 的核心工程洞察是"LLM 在处理单一专注维度时表现更好"。这解释了为什么 Sectioning 比让一个 LLM 同时处理多个关注点更有效——LLM 的注意力机制在单一维度上有更好的推理质量，多维度的混合会导致推理质量稀释。Voting 则是在高风险场景中用冗余换确定性的工程手段。

---

### Level 4: Orchestrator-Workers —— 不可预测任务的动态分解

这是第一个真正需要"Agent"能力的模式。Orchestrator-Workers 的核心区别于 Parallelization：**子任务不是预先定义的，而是由中心 LLM 根据输入动态决定的**。

```
输入 → Orchestrator LLM → [动态子任务1] → [动态子任务2] → [动态子任务3]
                        ↓（由 Orchestrator 决定）
                    Worker LLM 1  Worker LLM 2  Worker LLM 3
                                          ↓
                                    结果聚合
```

典型案例：
- 复杂代码修改任务——需要修改的文件数量和每个文件的修改内容在任务开始前无法预测
- 多源信息收集与分析——需要收集哪些来源取决于对信息的实时评估

**与 Parallelization 的关键区别**：Parallelization 的子任务是预先知道的（Sectioning）或可以穷举的（Voting）；Orchestrator-Workers 的子任务是动态生成的，取决于 LLM 对输入的理解深度。

**笔者认为**：Orchestrator-Workers 模式是最容易被"过度设计"的。许多团队在任务可以预测时就已经引入这个模式，造成不必要的系统复杂性。判断标准很简单：**你能枚举出这个任务的所有子任务吗？能枚举则用 Parallelization，不能则用 Orchestrator-Workers**。

---

### Level 5: Evaluator-Optimizer —— 带评估的迭代改进

**核心思想**：一个 LLM 生成响应，另一个 LLM 在循环中提供评估和反馈，直到满足明确的质量标准。

```
生成 LLM → 输出 → 评估 LLM → 反馈 → [循环直到达标]
                          ↓
                    质量达标 → 终止
```

适用场景的两个明确信号：
1. **LLM 响应可以被人类反馈明确改进**——这意味着质量标准是可表述的
2. **LLM 能够提供这样的反馈**——这意味着评估标准是 LLM 能理解的

典型案例：
- 文学翻译（第一稿通常捕捉不到细微语气，需要迭代打磨）
- 复杂搜索任务（需要多轮搜索-分析-再搜索，直到评估 LLM 认为信息充分）

**与 SWE-bench 等 Benchmark 的关系**：Anthropic 指出 Evaluator-Optimizer类似于人类的迭代写作过程。这个模式的工程化实现通常依赖明确的评估标准（如代码正确性测试、格式验证规则），这些标准的可执行性决定了循环能否自动终止。

**笔者认为**：Evaluator-Optimizer 是目前最被混淆的模式。很多人把它等同于"Agent 自我反思"，但 Anthropic 明确指出这是两个不同的机制：自我反思是单个 LLM 在推理过程中的元认知操作，而 Evaluator-Optimizer 是两个独立 LLM（生成和评估）之间的结构化循环。前者是推理能力，后者是工程架构。

---

### Level 6: Agents —— 真正的自主性

Anthropic 的 Agent 定义简洁而精确：

> *"Agents are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."*

关键特征：
- **自主决策**：LLM 控制工作流执行，决定何时完成任务或主动纠正错误
- **工具驱动**：通过环境反馈（工具调用结果、代码执行结果）评估进展
- **检查点机制**：在检查点暂停等待人类反馈，或在遇到阻塞时转移控制权
- **终止条件**：包含最大迭代次数等控制条件

典型案例：
- SWE-bench 任务（多文件修改，每次修改后从环境获取 ground truth）
- Computer Use 参考实现（Claude 操作计算机完成复杂任务）

```
Agent 工作流：
开始 → LLM 规划 → 工具调用 → 环境反馈 → 评估进展
         ↑ ↓
         └──── [检查点/终止条件] ←──── [达标/超限]
```

**Agent 的核心工程代价**：自主性意味着更高的成本和**错误叠加的风险**。Anthropic 明确建议在沙箱环境中充分测试，并配置适当的 Guardrails。

---

##模式选择的决策树

把六种模式整合成一棵决策树，核心判断标准是**任务的可预测性**：

```
任务是否需要动态决定子任务？
├─ 否 → 任务是否可分解为固定序列？
│ ├─ 是 → Prompt Chaining
│     └─ 否 → 输入是否需要分类处理？
│           ├─ 是 → Routing
│           └─ 否 → 是否有多个独立子任务需要并行？
│                 ├─ Sectioning（独立但并行）
│                 └─ Voting（同任务多次执行，换高置信度）
└─ 是 → 是否有明确的评估标准？
      ├─ 是 → Evaluator-Optimizer
      └─ 否 → Agents
```

**Anthropic 的核心工程原则**在这棵决策树中体现得很清楚：**永远从树的最顶层开始，只有当当前层明确无法满足需求时才进入下一层**。

---

## 三条核心设计原则

Anthropic 在文章结尾总结了三条设计原则，笔者认为这是整篇文章最有工程价值的部分：

### 1. 保持简单（Maintain Simplicity）

> *"Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short."*

这条原则的工程含义是：每一次增加复杂度都必须有明确的性能提升作为论据，而不是因为"这个框架很流行"。

### 2. 优先透明（Prioritize Transparency）

Agent 的规划步骤必须显式展示，而不是让推理过程隐藏在黑箱中。这对于调试和维护至关重要。

### 3. 精心设计 Agent-Computer Interface（ACI）

这是 Anthropic 提出的一个独特概念。工具的文档和测试方式决定了 Agent 能否可靠地使用它们。ACI 的设计质量直接影响 Agent 的工具调用准确率。

> *"We expand on best practices for tool development in Appendix 2 ('Prompt Engineering your Tools')."*

---

## 为什么这个框架比任何框架对比都重要

Agent 领域有大量的"框架横评"文章，但这些文章往往在错误的问题上竞争：哪个框架功能更丰富，哪个框架支持的模式更多。

Anthropic 的框架提出了一个更根本的问题：**你的任务到底需不需要这些模式？**

| 模式 | 延迟代价 | 成本代价 | 质量潜力 | 适用任务类型 |
|------|---------|---------|---------|-----------|
| Prompt Chaining | 中等（序列） | 累加（每步） | 很高 | 固定序列，可分解 |
| Routing | 低 |降低（模型分层） | 持平 | 多类型输入，资源敏感 |
| Parallelization | 降低（并行） | 增加（并行） | 提高（冗余）或持平 | 独立子任务或需多视角 |
| Orchestrator-Workers | 增加（动态分解） | 增加（动态子任务） | 很高 | 不可预测子任务集 |
| Evaluator-Optimizer | 很高（循环） | 很高（多次迭代） | 很高 | 有明确评估标准 |
| Agents | 最高（自主运行） | 最高（长时运行） | 视任务 | 开放目标，长时执行 |

**笔者的核心判断**：这张表格的工程价值远大于任何框架对比帖。原因在于它让决策变得可量化——当你在设计一个 Agent 系统时，首先要问的不是"用哪个框架"，而是"我的任务在哪个层次，对应的延迟和成本代价是什么"。

---

## 框架的正确用法

Anthropic 并不反对使用框架，但给出了明确的使用指南：

> *"These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug."*

**框架的正确用法**：用框架快速启动 → 理解底层机制 → 根据需要逐步减少抽象层。

这个建议对于正在评估 CrewAI、LangGraph、AutoGen 等框架的团队有直接的工程指导意义：框架是学习工具，不是生产依赖。一旦你对底层机制（LLM 调用、工具定义、状态管理）有了清晰理解，框架的抽象层就成了可选的——可以保留简化维护，也可以剥离直接用 API。

---

## 结语

Anthropic 这篇文章的价值不在于提供了六种新模式——这些模式在业界已被广泛讨论。它的真正价值在于提供了一套**决策框架**，让团队能够理性地回答"我需要哪种复杂度"这个问题。

笔者认为这篇文章最重要的贡献是**把"Agent"从一种系统类型重新定义为一个能力层次**。不是所有的 Agent 系统都需要从 Level 6 开始；大多数场景下，Level 1-3 的组合已经足够好。复杂度不是能力，合适的复杂度才是。

**所以你应该**：
1. 先评估任务是否真的需要 Agent（大多数单步 LLM 调用就足够了）
2. 按照决策树逐层判断，从 Prompt Chaining 开始
3. 每次升级复杂度前，明确记录"为什么当前层级无法满足"
4. 选择框架时，优先选择能让你看清底层机制的工具

---

## 参考来源

- *[Building Effective AI Agents](https://www.anthropic.com/research/building-effective-agents)*，Anthropic Engineering Blog，2026年6月
- *[Model Context Protocol](https://modelcontextprotocol.io/)*，MCP 官方文档
- *[Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)*，Anthropic 官方 Agent SDK