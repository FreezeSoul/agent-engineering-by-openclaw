# aden-hive/hive：零配置多 Agent 拓扑执行框架

> **核心观点**：Hive 解决了一个被长期忽视的问题——当多 Agent 系统从实验走向生产时，**拓扑编排、状态持久化、容错恢复**往往需要大量自研代码。Hive 通过「Objective → DAG 自动编译」的方式，让用户只定义目标，框架自动生成执行拓扑，填补了轻量级多 Agent 生产化工具的空白。

**关联 Article**：[Cursor 云端 Agent 四个被忽视的工程教训](./cursor-cloud-agent-four-engineering-lessons-2026.md)（持久化执行 + 状态解耦 + 工程环境是一等产品）

---

## 能解决什么问题

当你需要让多个 Agent 协同完成一个复杂任务时，通常面临：

- 手写编排逻辑（谁调谁、谁等谁、失败怎么办）
- 状态管理（每个 Agent 的中间结果怎么共享、怎么持久化）
- 容错处理（某个 Agent 超时/失败了，workflow 怎么恢复）

Hive 的答案是：**你只管说目标，DAG 执行拓扑自动生成**。

---

## 核心亮点

### 1. 零配置的多 Agent 拓扑生成

> "By simply defining your objective, the runtime compiles a strict, graph-based execution DAG that safely coordinates specialized agents to execute concurrent tasks in parallel."

你不需要写 workflow 配置文件，只需要描述目标。Hive 自动：
- 识别任务中的并行机会
- 生成 DAG 拓扑
- 协调 Agent 之间的数据流动

### 2. 持久化 Role-Based Memory

> "Backed by persistent, role-based memory that intelligently evolves with your project's context, OpenHive ensures deterministic fault tolerance, deep state observability, and seamless asynchronous execution across whichever underlying LLMs you choose to plug in."

每个 Agent 角色有自己的持久化 memory，且 memory 会随项目上下文进化。这意味着：
- Agent 重启后不丢失上下文
- 同一个工作流中断后可以恢复
- 不同 Agent 的 memory 可以隔离也可以共享

### 3. Model-Agnostic 设计

> "across whichever underlying LLMs you choose to plug in"

Hive 不绑定某个特定 LLM，你可以在同一个工作流里混用不同的模型（Claude / GPT / Gemini / DeepSeek），这对于需要不同能力组合的复杂任务很有价值。

### 4. 与 Cursor 云端 Agent 教训的呼应

Cursor 的四个工程教训在 Hive 中都有对应实现：

| Cursor 教训 | Hive 对应 |
|-----------|---------|
| 持久化执行层 | 内置 DAG 执行引擎 + 状态持久化 |
| 状态解耦 | Role-based memory 隔离 + 可配置共享策略 |
| 工程环境是一等产品 | 开箱即用的执行环境，不需要手动配置基础设施 |
| 知道什么时候「让开」| Objective → DAG 自动编译，用户只管目标不管执行细节 |

### 5. 与 Temporal 的定位差异

Cursor 选择了 Temporal 作为执行层（自研 + 外部依赖），Hive 选择了内置执行引擎。

| 维度 | Temporal | Hive |
|------|---------|------|
| 定位 | 通用工作流引擎 | 多 Agent 专用 |
| 配置方式 | YAML + SDK | Objective 自然语言 |
| Agent 感知 | 无（通用引擎）| 有（多 Agent 拓扑原生支持）|
| 学习成本 | 中高 | 低（零配置）|
| 适用场景 | 通用业务流程 | Agent 原生多智能体任务 |

---

## 技术架构

```
Objective（目标）
    ↓
Runtime（编译）→ DAG 执行拓扑
    ↓
Agent Pool（多种 LLM）
    ↓
Role-Based Memory（持久化 + 隔离）
    ↓
异步执行 + 容错恢复
```

**关键特性**：
- DAG 执行拓扑保证任务依赖关系正确
- 并行任务自动识别和调度
- 失败重试 + 中断恢复
- 状态可观测性（每步执行结果可查）

---

## 使用场景

Hive 特别适合：

1. **多 Agent 协作的研究原型**：快速验证多 Agent 方案，不需要写编排代码
2. **轻量级生产任务**：不需要 Temporal 的全部能力，但需要可靠的执行保障
3. **Model-Agnostic 场景**：同一工作流混用多个模型供应商

---

## 快速上手

```bash
pip install hive

# 定义一个目标
from hive import Hive

hive = Hive()
result = hive.run(
    objective="分析竞品并生成对比报告，需要 web research + 数据整理 + 报告生成三个子任务",
    agents=["researcher", "analyst", "reporter"]
)
```

---

## 引用

> "Hive is a zero-setup, model-agnostic execution harness that dynamically generates multi-agent topologies to complex, long-running business workflows without requiring any orchestration boilerplate."
> — [GitHub README](https://github.com/adenhq/hive)

> "By simply defining your objective, the runtime compiles a strict, graph-based execution DAG that safely coordinates specialized agents to execute concurrent tasks in parallel."
> — [GitHub README](https://github.com/adenhq/hive)

> "Backed by persistent, role-based memory that intelligently evolves with your project's context, OpenHive ensures deterministic fault tolerance, deep state observability, and seamless asynchronous execution."
> — [GitHub README](https://github.com/adenhq/hive)

---

*关联文章*：[Cursor 云端 Agent 四个被忽视的工程教训](./cursor-cloud-agent-four-engineering-lessons-2026.md) | *关联项目*：[obra/superpowers：让编码 Agent 真正学会软件工程方法论](./obra-superpowers-agentic-skills-software-development-methodology-2026.md)