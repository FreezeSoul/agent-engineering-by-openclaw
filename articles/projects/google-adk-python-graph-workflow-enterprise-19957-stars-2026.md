# google/adk-python：Google 原生 Agent 开发框架，19.9k Stars 的多语言选择

> 这个项目解决了一个长期困扰企业 Agent 开发的问题：如何在保持灵活性的同时，让 Agent 执行变得可预测、可审计、可组合。Google 给出的答案是「Graph-based Workflow Runtime + 多语言 SDK」。

---

## 核心命题

google/adk-python 不是另一个"又一个 Agent 框架"。它是 Google 内部多年 Agent 开发经验的产物，2025年4月开源，到2026年6月已积累 **19,957 Stars 和 3,490 Forks**，成为 GitHub Star 增长最快的官方 Agent 框架之一。

笔者认为，ADK 最大的差异化价值不在于"能做什么"，而在于**它解决了一类特定问题**：当你的 Agent 需要在生产环境中处理复杂业务流程（多步骤、有人工审批、出错恢复、审计追溯）时，ADK 2.0 的 Graph-based Workflow Runtime 提供了一种**显式控制流**的解决方案，而不是把所有逻辑都塞进 prompt 里。

---

## 为什么值得注意

### 多语言 SDK：一次学习，多处部署

ADK 目前覆盖 5 个语言：

| 语言 | 仓库 | 说明 |
|------|------|------|
| Python | [google/adk-python](https://github.com/google/adk-python) | 主力语言，2.0 GA（2026-05-19） |
| JavaScript/TypeScript | [google/adk-js](https://github.com/google/adk-js) | Web/Node.js 环境 |
| Go | [google/adk-go](https://github.com/google/adk-go) | 高性能场景 |
| Java | [google/adk-java](https://github.com/google/adk-java) | 企业 JVM 环境 |
| Kotlin | [google/adk-kotlin](https://github.com/google/adk-kotlin) | Android/JVM 生态 |

官方表示 ADK 2.0 是"code-first, production-grade"的框架。如果你已经在用 Google Cloud（Vertex AI、Gemini），ADK 的部署集成是开箱即用的——一行命令部署到 Cloud Run、GKE 或 Agent Runtime。

### Graph-based Workflow Runtime（2.0 核心）

这是 ADK 2.0 与 1.x 的本质差异。在 2.0 中，你的 Agent、Tools、Functions 都成为**图中的节点**，边声明执行路径和条件分支：

```python
# ADK 2.0: 显式图路由，而非 prompt 驱动
edges = [
    ["START", "validate_input"],
    ["validate_input", "process_task"],
    ["process_task", Route(
        condition=lambda ctx: ctx.get("needs_approval", False),
        then=["human_review"],
        else_=["auto_complete"]
    )],
    ["human_review", "finalize"],
    ["auto_complete", "END"],
    ["finalize", "END"],
]
```

这个设计带来了三个关键能力：

1. **确定性执行**：执行路径在代码层面声明，不是藏在 prompt 里的隐含逻辑
2. **Checkpoint/Resume**：图状态可持久化，Agent 可以在任意节点中断和恢复
3. **Fan-out/fan-in 并行**：JoinNode 支持并行执行多个子 Agent 后汇合，这是 1.x 极难实现的模式

### 与 Gemini 的原生集成

ADK 默认支持 Gemini 系列模型，但设计上不绑定——你可以接入任何支持 function calling 的 LLM provider。对于部署在 Google Cloud 的团队，ADK 提供了开箱即用的 Vertex AI 集成和 Cloud Trace 可观测性。

---

## 技术细节

**基础信息**：

- **Stars**: 19,957（2026-06-02）
- **Forks**: 3,490
- **License**: Apache 2.0
- **语言**: Python (96.8%), Jupyter Notebook (2.4%)
- **创建时间**: 2025-04-01
- **最新版本**: v1.34.2（2026-06-01）
- **贡献者**: 290 人

**核心特性**（来自 [GitHub README](https://github.com/google/adk-python)）：

> "An open-source, code-first Python toolkit for building, evaluating, and deploying sophisticated AI agents with flexibility and control."

- **Workflow Runtime**: Graph-based execution（2.0 核心）
- **Multi-agent Collaboration**: Task API 支持 Agent 间委托
- **Checkpointing**: 会话状态持久化，支持断点恢复
- **Human-in-the-Loop**: 人工审批节点
- **Observability**: Cloud Trace 原生集成
- **Deployment**: Cloud Run / GKE / Agent Runtime 一键部署

---

## 竞品对比

| 维度 | Google ADK | LangGraph | CrewAI |
|------|-----------|-----------|--------|
| **执行模型** | Graph-based workflow | Graph-based (DAG) | Process flow + Role-based |
| **多语言支持** | Python/JS/Go/Java/Kotlin | Python/JS | Python only |
| **Checkpoint/Resume** | 原生支持 | 支持（LangGraph checkpointing） | 部分支持 |
| **多 Agent 协作** | Task API（2.0） | Sub-graphs | Crew + Agents |
| **上手难度** | 中等（需要图思维） | 中等（类似 LangChain） | 低（直觉的 role 定义） |
| **云原生部署** | Cloud Run/GKE 一键 | 自行部署 | 自行部署 |
| **Stars（2026-06）** | 19,957 | ~126,000 | ~44,000 |

笔者的判断是：**ADK 不是 LangGraph 的直接竞品，它更像是一个「企业级选择」**——如果你在 Google Cloud 生态里，需要多语言支持和原生的可观测性，ADK 是一个值得认真考虑的选项。如果你在寻找最大社区支持和最低上手门槛，LangGraph 目前仍然是领先者。

---

## 适用场景

**推荐使用 ADK 的场景**：
- 复杂的多步骤业务流程，需要明确的执行路径和审计日志
- 需要 Human-in-the-Loop 审批的企业工作流
- 在 Google Cloud 生态中运行，需要原生集成（Vertex AI、Cloud Trace）
- 需要多语言 SDK 覆盖不同技术栈的团队
- 需要长任务中断/恢复能力的场景

**不推荐或需要权衡的场景**：
- 快速原型和实验性项目（ADK 2.0 仍有一定学习曲线）
- 非 Google Cloud 团队，且不需要多语言支持（LangGraph 社区更大）
- 极度轻量的单 Agent 场景

---

## 引用

1. [google/adk-python - GitHub](https://github.com/google/adk-python) — 官方仓库，Stars: 19,957，Apache 2.0
2. [Welcome to ADK 2.0 - Agent Development Kit](https://adk.dev/2.0/) — 2.0 GA 发布说明，2026年5月19日
3. [Google ADK Docs: Graph-based workflows](https://github.com/google/adk-docs/blob/main/docs/workflows/graph-routes.md) — 图工作流官方文档

---

*本文是 Agent 工程实践系列，结合 Google ADK 2.0 框架架构分析，形成「理论 → 框架 → 项目」的完整闭环。*