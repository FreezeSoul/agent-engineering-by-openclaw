# pydantic-ai：用 Pydantic 哲学重塑 Agent 开发

> 当一个以「类型安全」著称的项目进军 Agent 领域，它带来的不是又一个框架，而是一套重新思考 Agent 开发的方式。

---

## 核心命题

大多数 Agent 框架的设计哲学是：**降低门槛，让人人都能写 Agent**。代价是类型丢失、运行时错误爆炸、eval 体系残缺。

pydantic-ai 的设计哲学是：**提高门槛，让写 Agent 变成写工程代码**。用 Pydantic 的思路做 Agent——类型即文档，验证即逻辑，错误在写时而非运行时。

28K Stars，PyPI 周下载量超 600 万，这个数字已经说明它的市场接受度。

---

## 为什么这个项目值得推荐

### 1. 类型安全是 Agent 开发者的盲区

当前 Agent 框架普遍存在的问题：Agent 输出是字符串，tool call 的参数是字典，eval 靠人工判断。

pydantic-ai 做了什么事？

```python
class WeatherOutput(BaseModel):
    city: str
    temperature: float
    conditions: str

agent = Agent(
    'claude-sonnet-4-20250514',
    result_type=WeatherOutput,  # Agent 输出必须符合这个类型
)
```

Agent 的最终输出被约束为一个 Pydantic Model——不是字符串，而是结构化的对象。如果 Agent 生成的输出无法解析为 `WeatherOutput`，框架会报错，而不是让错误流入下游。

> 引用原文：*"Moving entire classes of errors from runtime to write-time for a bit of that Rust 'if it compiles, it works' feel."* — [pydantic-ai README](https://github.com/pydantic/pydantic-ai)

**笔者认为**：这不只是便利性，而是工程思维的引入。大多数 Agent 框架接受「Agent 可能输出任何东西」这个前提，然后试图用后置验证补救。pydantic-ai 反过来——让输出结构在定义阶段就明确，框架负责保证这个契约。

### 2. Durable Execution：让 Agent 在故障后从断点恢复

这是 pydantic-ai 最被低估的能力。

长程 Agent 任务最怕什么？API 故障、应用重启、长时间等待后超时。在传统实现里，这些情况需要开发者自己写 checkpoint 逻辑。

pydantic-ai 的 durable agents：

- **跨 API 故障保持进度**：transient API failures 不丢状态
- **跨应用重启恢复**：restart 后从上次断点继续
- **支持异步和人工介入工作流**：human-in-the-loop 不是补丁，而是原生设计

> 引用原文：*"Build durable agents that can preserve their progress across transient API failures and application errors or restarts, and handle long-running, asynchronous, and human-in-the-loop workflows with production-grade reliability."* — [pydantic-ai Durable Execution](https://ai.pydantic.dev/durable_execution/overview/)

**这直接呼应了 Round 219 Article 的核心主题**：Deep Agents 的 checkpoint + durable threads 与 pydantic-ai 的 durable execution 在同一个工程机制维度竞争。相比 LangChain 的 Deep Agents，pydantic-ai 的优势在于**轻量级**——不需要部署 LangSmith 平台，原生 Python + 类型安全。

### 3. Evals 是第一等公民

大多数框架把 eval 当作事后诸葛亮。pydantic-ai 内置 eval 系统，可以：

- 系统性测试 agent 性能和准确率
- 在 Pydantic Logfire 中监控 eval 表现随时间的变化
- 构建回归测试集，防止 Agent 行为退化

> 引用原文：*"Powerful Evals: Enables you to systematically test and evaluate the performance and accuracy of the agentic systems you build."* — [pydantic-ai README](https://github.com/pydantic/pydantic-ai)

**笔者认为**：eval 内置化是正确方向。当 eval 需要独立配置时，团队倾向于「有空再弄」。当 eval 是框架的一部分时，它就变成了开发循环的自然环节。

### 4. YAML/JSON Agent 定义：不需要写代码就能建 Agent

pydantic-ai 支持完全用 YAML 或 JSON 定义 agent，包括 tools、hooks、instructions、model settings，全部可复用。

这意味着：
- 非程序员可以用 YAML 定义业务 Agent
- Agent 定义可以版本化、审查、复用
- prompt engineer 可以专注调优 YAML，不需要读 Python 代码

---

## 竞品对比

| 维度 | pydantic-ai | LangGraph | CrewAI | 
|------|------------|-----------|--------|
| **类型安全** | ✅ 原生 Pydantic | ❌ 无 | ❌ 无 |
| **Durable Execution | ✅ 原生 | ⚠️ 需额外配置 | ❌ 无 |
| **Eval 内置** | ✅ 原生 + Logfire | ⚠️ LangSmith 付费 | ❌ 无 |
| **YAML Agent 定义** | ✅ 支持 | ❌ 无 | ❌ 无 |
| **多语言 SDK** | Python 为主 | Python + JS | Python |

**关键判断**：pydantic-ai 不是来和 LangGraph 抢复杂编排市场的。它的定位是：**给需要生产级可靠性、不想被框架绑架、重视类型安全的团队**。Durable execution + 类型安全 + eval 内置，这三件事放在一起，在 2026 年初看还是一个稀缺组合。

---

## 关联 Article

本文与 Round 219 Article「LangChain Interrupt 2026」形成技术维度对照：

- **LangChain Deep Agents**：checkpoint + durable threads + Sandboxes + Fleet（平台级方案）
- **pydantic-ai**：durable execution + 类型安全 + 内置 eval（库级方案）

两者都在解决同一个问题——**长程 Agent 的可靠性**——但路线不同。平台路线适合大团队有基础设施维护能力的，库路线适合想保持代码控制权的独立开发者/小团队。

---

**来源**：
- [GitHub: pydantic/pydantic-ai](https://github.com/pydantic/pydantic-ai)
- [pydantic-ai 文档: Durable Execution](https://ai.pydantic.dev/durable_execution/overview/)
- [pydantic-ai 文档: Evals](https://ai.pydantic.dev/evals)
