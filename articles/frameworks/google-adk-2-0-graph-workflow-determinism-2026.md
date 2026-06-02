# Google ADK 2.0：从层次化 Agent 执行器到图执行引擎 — 一个工程意义上的范式转移

> 本文解析 Google Agent Development Kit 2.0（2026年5月19日 GA）引入的 Graph-based Workflow Runtime，分析其与 ADK 1.x 层次化执行模型的本质差异，以及这对 Agent 工程化意味着什么。

---

## 核心命题

ADK 2.0 的发布不是一次功能迭代，而是一次**执行模型的替换**。

从 ADK 1.x 到 2.0，框架的核心变化是：Agent 从"独立执行单元"变成了"图中的节点"。这不是架构风格的选择，而是**可预测性（determinism）和可组合性（composability）优先**的工程决策——放弃 prompt 驱动的隐式循环，换来图定义的显式路由。

笔者认为，这个转变指向一个正在形成的行业共识：**当 Agent 进入生产环境，隐式控制流是奢侈品，显式控制流是必需品**。

---

## ADK 1.x 的执行模型：层次化的 Agent 树

ADK 1.x 采用的是**层次化（hierarchical）Agent 执行模型**：

```
Agent（根节点）
├── Tool A
├── Tool B
└── SubAgent
    ├── Tool C
    └── Tool D
```

在这个模型中：
- **Agent 是独立的执行器**，有自己的 `run()` 方法和 `generate_content()` 逻辑
- 控制流由 Agent 内部的 prompt 和工具调用决定，**外部无法直接干预**
- 状态（Session）通过 `context.session.events` 维护，开发者可以手动追加事件

这种设计的优点是**上手简单**：定义 Agent → 添加工具 → 运行，符合直觉。缺点是**当任务复杂时，控制流变得不可预测**——Agent 可能会在某个工具调用上反复循环，或者因为 context 溢出丢失关键状态。

更根本的问题是：**这种模型下，Agent 的执行路径是隐式的**，你无法在代码层面声明"先执行 A，再执行 B，如果 C 则走 D"，所有条件分支都需要塞进 prompt 里。

---

## ADK 2.0 的执行模型：图执行引擎

ADK 2.0 引入 **Workflow Runtime**，将整个框架的执行模型从层次化 Agent 树转变为**有向图（Directed Graph）**：

```
[START] → [FunctionNode] → [AgentNode] → [JoinNode] → [END]
              ↓                              ↑
         [ToolNode] ←────────────────────────┘
```

在图模型中：

- **所有组件都是节点（Node）**：Agent、Function、Tool、Human Input，甚至另一个 Workflow
- **边（Edge）定义执行路径**：显式声明数据流向和条件分支
- **Event 携带数据并在节点间传递**：每个节点接收来自前置节点的输出，生成新事件向后传递
- **JoinNode 等待所有并行分支完成**：支持 fan-out/fan-in 模式

ADK 2.0 的文档明确指出这种设计的优势：

> "By defining the overall process workflow in code, you gain more control over how tasks are routed and executed. This structured node definition improves the predictability of agents and enhances reliability for complex tasks that require defined steps and process management."
> — [Google ADK Docs: Graph-based workflows](https://github.com/google/adk-docs/blob/main/docs/workflows/graph-routes.md)

### 图定义的语法：从 prompt 驱动到 edges 声明

在 ADK 1.x 中，Agent 的行为由系统 prompt 和 few-shot examples 决定。在 ADK 2.0 中，行为由 `edges` 数组声明：

```python
# ADK 2.0: 显式图路由
edges = [
    ["START", "process_input"],      # 起点
    ["process_input", "analyze"],    # 顺序执行
    ["analyze", Route(               # 条件分支
        condition=lambda ctx: ctx.get("needs_review", False),
        then=["human_review"],
        else_=["auto_approve"]
    )],
    ["human_review", "final_decision"],
    ["auto_approve", "END"],
    ["final_decision", "END"],
]
```

每一行都是**可审计的代码**，不是藏在 prompt 里的隐含逻辑。

### 并行执行：JoinNode 的 fan-out/fan-in

ADK 2.0 支持并行分支 + 汇合，这是 1.x 极难实现的能力：

```python
# 并行执行多个子任务
edges = [
    ["START", "task_dispatcher"],
    ["task_dispatcher", "parallel_agent_1"],
    ["task_dispatcher", "parallel_agent_2"],
    ["task_dispatcher", "parallel_agent_3"],
    ["parallel_agent_1", "join_node"],
    ["parallel_agent_2", "join_node"],
    ["parallel_agent_3", "join_node"],
    ["join_node", "aggregate_results"],
    ["aggregate_results", "END"],
]
```

`JoinNode` 自动等待所有上游节点完成，收集输出后传递给下游。这是**工作流引擎的标准模式**，首次出现在 Google 的 Agent 框架中。

### 动态工作流：代码逻辑驱动的条件分支

对于需要复杂条件判断的场景，ADK 2.0 提供**动态工作流（Dynamic Workflows）**，允许用 Python 代码定义路由逻辑：

```python
# 动态路由：用 Python 函数决定下一跳
edges = [
    ["START", "evaluate_task"],
    ["evaluate_task", Route(
        dynamic_fn=decide_next_step,
        description="根据任务复杂度决定执行路径"
    )],
]
```

这比 LangChain 的 Runnable 语法更接近传统工作流引擎（如 Temporal、Camelot）的表达方式。

---

## Breaking Changes：从 1.x 迁移的真实代价

ADK 2.0 不是一个向后兼容的升级。官方文档列出了几个**关键 Breaking Changes**，每个都对应真实的工程踩坑点：

### 1. Event Schema 新增字段

ADK 2.0 的 Event 新增了 `node_info` 和 `output` 字段，用于追踪图状态和输出。如果你有自定义的 Session 存储（尤其是将 Event 映射到固定数据库列的 ORM 实现），**必须更新 schema**。官方原话：

> "If your custom session service stores events as serialized JSON blobs rather than mapping them to explicit columns, you do not need to update your schema." — [ADK 2.0 Breaking Changes](https://adk.dev/2.0/)

这意味着：**JSON blob 存储是安全的选择，结构化列映射需要迁移**。

### 2. Agent 不再是执行主体，而是节点

ADK 1.x 中，你继承 `BaseAgent` 并 override `run()` 或 `generate_content()` 来自定义执行逻辑。在 ADK 2.0 中：

> "Custom overrides of 1.x abstract methods, such as `_run_async_impl()` or `generate_content()`, are no longer the correct way to drive execution. The Workflow Graph completely bypasses these legacy overrides." — [ADK 2.0 Breaking Changes](https://adk.dev/2.0/)

如果你在 1.x 中通过 override `_run_async_impl()` 注入了自定义 telemetry 或状态管理，这些代码在 2.0 中会被**静默忽略**。正确的方式是使用 `BeforeAgentCallback` 和 `AfterAgentCallback`。

### 3. 禁止直接操作 Session Events

在 ADK 1.x 中，常见模式是：

```python
# ADK 1.x（危险但常见）
context.session.events.append(custom_event)
```

在 ADK 2.0 中，这种做法会**破坏图的确定性**，因为 Workflow Runner 需要严格控制事件发射来管理状态和路由。正确做法是从节点内部 yield 事件。

### 4. Exception 处理的新规则

ADK 2.0 框架现在会自动捕获异常来实现自动重试和 HITL（Human-in-the-Loop）暂停。**如果你在工具里写了 `except Exception:` 来防止崩溃，实际上会阻止框架的重试机制**。更糟糕的是，捕获 `BaseException` 会破坏 HITL 暂停能力。

官方建议：**让异常自然向上传播，让框架的 RetryConfig 处理重试逻辑**。

---

## 为什么这重要：框架演进的一个侧面

ADK 2.0 的变化不是孤立的。看看 2026 年主要的 Agent 框架在做什么：

| 框架 | 核心变化 | 年份 |
|------|---------|------|
| LangChain | 从 Chain 到 LangGraph，引入 checkpointing | 2024-2025 |
| CrewAI | 1.0 GA，强调 role-based + process flow | 2026 |
| **Google ADK** | **从层次化执行器到图执行引擎** | **2026** |
| AutoGen | 2.0，完全重构为 async-first | 2026 |

这些变化都在指向同一个方向：**Agent 框架正在从"用 prompt 描述流程"演进到"用代码定义流程"**。图执行模型、工作流引擎式的路由声明、checkpointing 持久化——这些不是新概念，但它们正在成为 Agent 框架的标配。

笔者认为，这个演进背后的驱动力不是学术，而是**生产环境的倒逼**：

- 当 Agent 处理长任务（多步骤、跨天、涉及人工审批）时，隐式控制流无法满足审计要求
- 当 Agent 需要在出错后恢复执行状态时，需要显式的 checkpoint 和 resume 能力
- 当 Agent 组合多个子 Agent 时，需要可预测的并发和汇合模型

Graph-based workflow 不是答案的全部，但它提供了一种**可预测、可组合、可审计的执行模型**，这正是生产级 Agent 系统需要的。

---

## 引用

1. [Welcome to ADK 2.0 - Agent Development Kit](https://adk.dev/2.0/) — ADK 2.0 GA 发布说明，2026年5月19日
2. [Google ADK Docs: Graph-based workflows](https://github.com/google/adk-docs/blob/main/docs/workflows/graph-routes.md) — 图工作流官方文档
3. [Google ADK Python: GitHub Repository](https://github.com/google/adk-python) — v1.34.2，2026-06-01 更新，19,957 Stars
4. [Google ADK 2.0 Alpha: A Workflow Runtime That Treats Agents Like...](https://www.linkedin.com/pulse/google-adk-20-alpha-workflow-runtime-treats-agents-jin-tan-ruan-z7w9e) — LinkedIn 技术分析

---

*本文属于「框架架构分析」系列，分析主流 Agent 框架的架构决策与工程权衡。*