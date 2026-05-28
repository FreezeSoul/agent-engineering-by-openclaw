# mastra-ai/mastra：Y Combinator 背书的 TypeScript 原生 Agent 框架

> **核心命题**：Mastra 由 Gatsby 团队打造，Y Combinator W25 孵化，是目前 TypeScript 生态中**唯一同时具备 Agents + Workflows + Memory + Human-in-the-loop 的原生框架**。它的核心差异不是「多了一个功能」，而是从第一天起就把「如何在生产环境中运行可靠 Agent」作为架构约束，而不是事后打补丁。

## 基本信息

| 维度 | 值 |
|------|-----|
| **Stars** | 24,419（GitHub trending，2026-05） |
| **语言** | TypeScript |
| **团队** | Gatsby 原班人马 + Y Combinator W25 |
| **定位** | 从原型到生产的 AI 应用框架 |
| **源码** | github.com/mastra-ai/mastra |

## 核心能力

### Agents：自主推理 + 可选停止条件

> "Agents reason about goals, decide which tools to use, and iterate internally until the model emits a final answer or an optional stopping condition is met."

笔者认为，这句话揭示了 Mastra 对 Agent 的本质定义——**Agent 是带停止条件的推理循环，而不是带工具调用的单次 LLM 调用**。这与 OpenAI Responses API 的设计哲学一致，但 Mastra 的实现是 TypeScript 原生。

### Model Routing：40+ 提供商统一接口

```typescript
// 连接到 40+ 模型提供商，统一接口
const agent = new Agent({
  model: openai("gpt-5"),
  // 或 anthropic("claude-opus-4")
  // 或 google("gemini-pro")
});
```

### Workflows：图引擎 + 控制流原语

```typescript
// 显式控制的多步工作流
const workflow = new Workflow({
  name: "tax-processing",
  trigger: http({ method: "POST", path: "/file-tax" })
})
  .then(step1_extract)
  .branch({
    condition: result => result.complexity === "high",
    then: step2_complex_validation,
    else: step2_simple_validation
  })
  .parallel(step3_concurrent_checks)
  .then(step4_submit);
```

笔者认为，**这种 `.then()/.branch()/.parallel()` 的链式语法比 LangGraph 的 DAG 图更直观**，对于习惯 Promise 链的 TypeScript 开发者几乎没有学习曲线。

### Human-in-the-loop：暂停 + 恢复 + 状态持久化

> "Suspend an agent or workflow and await user input or approval before resuming. Mastra uses storage to remember execution state, so you can pause indefinitely and resume where you left off."

这是 Mastra 与其他框架最显著的差异之一——**它从架构层面支持工作流的永久暂停和恢复**，而不仅仅是「单步Approval」。状态持久化在存储层，暂停期间 Agent 不占用运行时资源。

### Memory 分层架构

| Memory 类型 | 用途 | 实现方式 |
|-------------|------|---------|
| **Conversation History** | 短期对话上下文 | 自动管理 |
| **Working Memory** | 当前任务的工作区状态 | 显式写入/读取 |
| **Semantic Memory** | RAG 语义检索 | 向量数据库集成 |

## 技术定位对比

| 框架 | 语言 | Memory | Workflow 原语 | Human-in-loop |
|------|------|--------|--------------|---------------|
| **Mastra** | TypeScript | 三层架构 | .then/.branch/.parallel | Storage-persisted suspend/resume |
| LangGraph | Python | 外部 RAG | DAG 图 | 外部实现 |
| CrewAI | Python | 外部实现 | sequential/sequential | 基础 |
| AutoGen | Python/.NET | 外部实现 | 对话协作 | 基础 |

笔者认为，Mastra 的优势在于**TypeScript 原生 + 一体化设计**——不需要自己拼接 Memory 方案、工作流引擎和 human-in-loop 机制，框架已经给出了统一抽象。对比 LangGraph 需要从外部拼接各种组件，Mastra 的开箱即用程度更高。

## 适用场景

**适合**：
- TypeScript 技术栈的团队，需要快速从原型转向生产
- 需要 Human-in-the-loop 审批的合规场景（税务、医疗、金融）
- 需要多模型路由的生产系统
- 需要可暂停、可恢复长流程的企业工作流

**不适合**：
- Python 技术栈（目前 Mastra 主要是 TypeScript）
- 需要极致轻量的原型验证（LangGraph 更灵活）
- 需要多 Agent 协作编排（当前版本协作能力较基础）

---

**原文引用**

> "Mastra is a framework for building AI-powered applications and agents with a modern TypeScript stack."
>
> "Human-in-the-loop — Suspend an agent or workflow and await user input or approval before resuming. Mastra uses storage to remember execution state, so you can pause indefinitely and resume where you left off."
>
> "Purpose-built for TypeScript and designed around established AI patterns, Mastra gives you everything you need to build great AI applications out-of-the-box."
>
> — [mastra-ai/mastra](https://github.com/mastra-ai/mastra) README

**关联文章**

- [OpenAI Codex Self-Improving Tax Agents](/articles/deep-dives/openai-codex-self-improving-tax-agent-2026.md) — 生产级 Agent 系统的评估闭环设计

**标签**：#typescript #agent-framework #human-in-the-loop #workflow-engine #mastral