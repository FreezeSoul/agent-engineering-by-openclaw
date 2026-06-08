# LangChain Middleware 设计解析：让 Harness 变成可插拔的定制系统

> **来源**: [How Middleware Lets You Customize Your Agent Harness](https://www.langchain.com/blog/how-middleware-lets-you-customize-your-agent-harness)，LangChain Blog，2026
> **分类**: harness
> **核心判断**: Middleware 是 Agent Harness 的「钩子系统」——它让非智能逻辑（业务策略、合规检查、上下文管理）从 Prompt 中剥离出来，变成可测试、可复用、可组合的独立组件。这是 Agent 工程化的关键一步。

---

## TL;DR

> Agent 的核心循环简单到令人意外：一个 LLM，在一个循环里，调用工具。但真正让 Agent 进入生产的，不是这个循环，而是围绕它构建的所有「非智能」逻辑——PII 检测、重试策略、上下文压缩、动态工具选择。
>
> LangChain 的答案是：把这些逻辑全部抽象成 Middleware，让它们变成 Harness 的可插拔组件。

---

## 一、问题：为什么 Harness 需要 Middleware

传统 Agent 开发中，非智能逻辑往往散落在两个地方：

**1. Prompt 里**：「如果检测到用户输入包含身份证号，请先脱敏再处理」——这种逻辑写进 Prompt，测试困难，运行时不可控，Prompt 长度还不断膨胀。

**2. 业务代码里**：在 Agent 循环外层写一堆 if-else，每次换项目就得重写，无法复用。

当 Agent 进入生产，这两个地方的弊端暴露无遗：

| 问题 | Prompt 里的表现 | 业务代码里的表现 |
|------|----------------|----------------|
| **合规性** | HIPAA 要求每次都执行 PII 检测，Prompt 无法保证强制执行 | 每次都调用检测函数，但逻辑分散，难以审计 |
| **可测试性** | Prompt 的「脱敏」行为无法自动化测试 | 需要构造各种边界输入才能覆盖 |
| **可复用性** | 同一个 PII 检测逻辑，在不同 Agent 里要复制粘贴 | 不同项目里各自实现，缺乏统一抽象 |
| **上下文污染** | 合规逻辑塞进 Prompt 消耗上下文额度 | 无处放置，干脆忽略 |

LangChain 的 Middleware 抽象，就是为了解决这些问题。

---

## 二、核心抽象：Middleware 作为 Hook 系统

LangChain 的 Middleware 本质上是一个 **Hook 系统**。它围绕 Agent 的核心循环，在关键节点提供插入点：

```
Agent Loop:
  ┌─────────────────────────────────────┐
  │ before_model (hook)                 │
  │   → 拦截 model 调用，可修改输入      │
  ├─────────────────────────────────────┤
  │   [LLM runs here]                   │
  ├─────────────────────────────────────┤
  │ after_model (hook)                  │
  │   → 拦截 model 输出，可修改或拒绝    │
  ├─────────────────────────────────────┤
  │ after_tool (hook)                   │
  │   → 拦截工具输出，可做后处理        │
  └─────────────────────────────────────┘
```

每个 Hook 都可以：
- **修改数据**：在 `before_model` 里对输入做脱敏，在 `after_model` 里截断输出
- **拒绝操作**：在 `after_model` 里抛出 `PIIDetectionError` 中止流程
- **注入状态**：在任意 Hook 里向 Agent 注入额外工具或修改系统 Prompt

这种 Hook 机制的关键价值在于：**它把「什么时候做什么」的判断从 LLM 转移到了确定性代码**。LLM 不再需要「记得」做 PII 检测，代码保证每次都执行。

---

## 三、Middleware 的四种典型场景

LangChain 文档总结了 Middleware 最常见的四种用途：

### 1. 业务逻辑与合规（Business Logic & Compliance）

> 「这类东西不能写在 Prompt 里，比如 PII 检测和内容审核。这些是确定性策略，每次都必须执行。你没法靠 Prompt 做到 HIPAA 合规。」

LangChain 的 `PIIMiddleware` 实现了 `before_model` 和 `after_model` 两个 Hook：
- 对 model 输入、输出、工具输出做掩码/脱敏/哈希
- 在严重 PII 泄露时抛出 `PIIDetectionError`

```python
# PIIMiddleware 的使用方式
agent = create_agent(
    model="claude-sonnet-4",
    middleware=[PIIMiddleware()]
)
```

这背后的设计原则很清晰：**合规逻辑必须是强制执行的，而不是「尽量遵守」的**。把检测逻辑放在 Prompt 里，LLM 可能因为上下文不足而跳过；放在 Middleware 里，代码保证每次都运行。

### 2. 动态工具选择（Dynamic Tool Selection）

LangChain 的 `LLMToolSelectorMiddleware` 在 `wrap_model_call` 时运行一个快速 LLM，判断当前请求需要哪些工具，然后只绑定这些工具到主模型调用——避免上下文因为无关工具而膨胀。

这个设计的精妙之处在于：**它把工具选择这个「智能决策」也委托给了模型，但只用于决策，不用于执行**。快速小模型做工具选择，主模型拿到精简后的工具列表。

### 3. 上下文管理（Context Management）

模型的效果取决于输入的上下文质量。Middleware 让上下文管理变成运行时问题，而非一次性 Prompt 问题：

- **接近 token 限制时自动 summarization**
- **裁剪噪声工具的输入/输出**
- **动态注入相关文档片段**

这解决了「Prompt 工程是一锤子买卖」的困境——上下文管理是持续发生的，而不是在开始时一次性配置。

### 4. 动态 Agent 控制（Dynamic Agent Control）

Middleware 可以在运行时重塑 Agent：
- 根据当前状态注入工具
- 任务中途切换模型
- 当上下文演变时更新 System Prompt

这是最激进的一种用法——Agent 的行为在运行时不是静态的，而是被 Middleware 持续调整的。

---

## 四、为什么 Middleware 是正确的抽象

LangChain 观察到一个关键趋势：

> 「自从 LangChain v1 发布，我们看到 Middleware 让不同团队可以各自拥有不同关注点，保持业务逻辑与核心 Agent 代码解耦，并且使得跨组织复用变得容易。」

这背后的工程直觉是：**Agent 的「智能」部分（LLM）和「工程」部分（合规、上下文、工具选择）有不同的变化节奏**。

- LLM 层面的变化（比如换成更强大的模型）应该只影响核心循环
- 合规要求的变化（比如新增一个合规地区）应该只影响 Middleware 层

如果这两层混在一起（比如把 PII 检测写在 Prompt 里），换模型时就得重新测试合规逻辑，换合规规则时就得重新 Prompt。

Middleware 提供了 **关注点分离（Separation of Concerns）**：智能归智能，工程归工程。

---

## 五、Middleware 的组合性

LangChain 强调 Middleware 是 **可组合的**：

```python
agent = create_agent(
    model="claude-sonnet-4",
    middleware=[
        PIIMiddleware(),           # 合规优先
        ToolSelectorMiddleware(), # 动态工具选择
        ContextManagerMiddleware(), # 上下文压缩
    ]
)
```

组合顺序很重要——`PIIMiddleware` 应该最靠前，确保脱敏在一切之前；`ContextManagerMiddleware` 应该靠后，在其他处理完后再压缩上下文。

这种组合性带来了几个实际好处：

1. **团队分工**：不同团队可以负责不同 Middleware，合规团队管 PIIMiddleware，上下文团队管 ContextManagerMiddleware
2. **测试隔离**：每个 Middleware 可以独立测试，不需要启动完整 Agent
3. **渐进采用**：从零开始时先加 `PIIMiddleware`，业务大了再加 `ToolSelectorMiddleware`，按需扩展

---

## 六、Middleware 与 Deep Agents 的关系

LangChain 的 Deep Agents 完全建立在 Middleware 之上：

> 「Deep Agents 是我们构建过最稳健的 Agent Harness，而它完全基于 Middleware 实现。这说服了我们相信这就是正确的抽象。」

Deep Agents 的开箱即用能力（Planning、Self-Verification、Memory、Sub-Agent Orchestration）全部通过 Middleware 实现。这意味着：

- 每个能力都是可插拔的
- 每个能力都可以被替换或扩展
- 新增能力不需要修改核心循环

这是 Middleware 抽象价值的最好证明：**它不是添加一层复杂度，而是让复杂度变得可管理**。

---

## 七、与其他框架的 Middleware 对比

| 框架 | Middleware 形式 | 可组合性 | 典型用途 |
|------|---------------|---------|---------|
| **LangChain** | `AgentMiddleware` class + Hooks | ✅ 高 | PII 检测、工具选择、上下文压缩 |
| **Anthropic Claude Agent SDK** | 权限分类器 + before/after hooks | ✅ 中 | 权限控制、输出审查 |
| **OpenAI Agents SDK** | sandbox + handoffs | ⚠️ 低 | 沙箱隔离、任务交接 |
| **CrewAI** | Task 输出处理 | ❌ 弱 | 固定后处理流程 |

LangChain 的 Middleware 是其中最通用、最可组合的抽象——它不绑定特定场景（PII、合规），而是提供通用 Hook 机制，让开发者自己决定插什么。

---

## 结论

Middleware 不是一个新概念（Web 开发里的 Express middleware 几乎是同义词），但把它引入 Agent Harness 是一个正确的工程判断。

它的核心价值是：**把「必须每次都做」的确定性逻辑从 Prompt 转移到代码，让 Agent 的非智能部分变得可测试、可复用、可组合**。

对于正在构建生产级 Agent 的团队，笔者的建议是：**先把 PIIMiddleware 加进去**——这是最容易验证效果、也最不容易出错的 Middleware。一旦尝到甜头，动态工具选择和上下文管理的价值就会自然显现。

---

## 关联项目

本文讨论的 Middleware 模式在 [LangChain Deep Agents](https://github.com/langchain-ai/deepagents)（MIT 协议，完全开源）中有完整实现。Harness 层不绑定任何模型或沙箱，Agent 指令使用 AGENTS.md（开放标准），通过 MCP、A2A、Agent Protocol 等开放协议暴露。