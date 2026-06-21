# 从 Swarm 到 Agents SDK：OpenAI 的生产级 Agent 框架演进

> **核心论点**：Swarm 是 OpenAI 对轻量级多 Agent 编排的实验性探索，Agents SDK 是这个实验走向生产环境的成熟形态。两者共享相同的核心抽象（Agent + Handoffs），但 Agents SDK 通过内置 Sandbox、Guardrails、Tracing、Sessions 等机制，解决了 Swarm 无法跨越的生产级挑战。

---

## 一、引言：为什么这是一个值得研究的技术演进

2024 年 10 月，OpenAI 在 GitHub 上发布了 Swarm，一个「教育性质的多 Agent 编排框架」。彼时，Swarm 的 README 开宗明义地写道：

> "Swarm focuses on making agent coordination and execution lightweight, highly controllable, and easily testable."

半年后的 2025 年 3 月，OpenAI 正式发布 Agents SDK，并在 Swarm 的 README 中加入了醒目的声明：

> "Swarm is now replaced by the OpenAI Agents SDK, which is a production-ready evolution of Swarm. The Agents SDK features key improvements and will be actively maintained by the OpenAI team."

这个转变不是简单的版本迭代，而是 OpenAI 对「什么样的 Agent 框架才能真正用于生产」这一问题的系统性回答。

笔者认为，Swarm 的核心贡献在于它验证了 **Handoffs 模型**（委托模型）的有效性——让 Agent 可以将任务转交给其他 Agent，从而构建动态的多 Agent 协作网络。而 Agents SDK 的贡献在于，它在这个模型基础上加入了生产环境必需的工程机制：隔离执行、安全防护、可观测性、状态持久化。

---

## 二、Swarm 的设计哲学：轻量即正义

### 2.1 核心抽象

Swarm 的设计哲学浓缩为两个词：**轻量（Lightweight）和教育性（Educational）**。

它只有两个核心抽象：

```python
from swarm import Swarm, Agent

client = Swarm()

agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

def transfer_to_agent_b():
    return agent_b

agent_b = Agent(
    name="Agent B",
    instructions="Only speak in Haikus.",
)

response = client.run(
    agent=agent_a,
    messages=[{"role": "user", "content": "I want to talk to agent B."}],
)
```

在这个例子中，`transfer_to_agent_b` 函数的返回值是一个 `Agent` 对象。Swarm 的 `client.run()` 会检测到这个返回值，并将执行权转交给目标 Agent。这就是 **Handoffs 模型**的核心。

### 2.2 Swarm 的 Agent Loop

Swarm 的 `client.run()` 内部实现了一个简洁的循环：

```
1. 获取当前 Agent 的 LLM completion
2. 执行 tool calls 并追加结果
3. 如果需要，切换 Agent
4. 更新 context_variables
5. 如果没有新的 function calls，返回
```

这个循环是无状态的——**Swarm 不存储任何状态，每次 `client.run()` 都是独立的**。README 明确指出：

> "Swarm runs (almost) entirely on the client and, much like the Chat Completions API, does not store state between calls."

这意味着 Swarm 本质上是一个**客户端库**，而不是一个托管服务。开发者需要自己管理对话历史和 Agent 状态。

### 2.3 Swarm 的局限性

Swarm 的 README 列出了它的定位：

> "Swarm is an educational resource for developers curious to learn about multi-agent orchestration."

这不仅仅是谦辞，更是对自身局限性的诚实陈述：

| 局限性 | 影响 |
|--------|------|
| 无状态设计 | 无法处理长时任务或跨会话的复杂工作流 |
| 纯函数式工具 | 无法执行真正的文件操作、命令执行 |
| 无隔离执行 | Agent 的工具调用与真实环境直接交互，存在安全风险 |
| 无可观测性 | 没有内置的 tracing、eval、monitoring |
| 无生产级保障 | 没有错误恢复、重试机制、超时控制 |

笔者认为，这些局限性不是 Swarm 的缺陷，而是它的设计边界。Swarm 的目标不是成为生产框架，而是验证 Handoffs 模型和轻量级编排的可行性。

---

## 三、Agents SDK：从实验到生产的跨越

### 3.1 保留核心，升级runtime

Agents SDK 的官方文档明确说明了它的设计原则：

> "Enough features to be worth using, but few enough primitives to make it quick to learn."
> "Works great out of the box, but you can customize exactly what happens."

**Agent + Handoffs 的核心抽象被完整保留**。这是关键——OpenAI 没有重新发明轮子，而是在 Swarm 的核心设计上叠加了生产级组件。

```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion.")
print(result.final_output)
```

这个 Hello World 示例与 Swarm 如出一辙，但 `Runner.run_sync()` 的内部实现远比 Swarm 的 `client.run()` 复杂。

### 3.2 关键新特性：Sandbox Agents

Agents SDK 最大的升级是 **Sandbox Agents**——在隔离的沙箱环境中运行 Agent。

官方文档这样描述：

> "Sandbox agents: Run specialists inside real isolated workspaces with manifest-defined files, sandbox client choice, and resumable sandbox sessions."

这意味着 Agent 可以：
- 在隔离的工作区中执行真实的文件操作
- 运行命令、安装依赖、操作代码库
- 创建可恢复的会话状态

对比 Swarm 的「纯函数调用」，Sandbox Agents 第一次让 Agent 能够真正地「工作」，而不只是「回答」。

### 3.3 关键新特性：Guardrails

Guardrails 是 Agents SDK 的另一个核心新增：

> "Guardrails: Run input validation and safety checks in parallel with agent execution, and fail fast when checks do not pass."

在 Swarm 中，所有的输入输出验证都需要开发者手动实现。Agents SDK 将这一需求内置为框架级特性，允许开发者在 Agent 执行过程中并行运行多个安全检查。

### 3.4 关键新特性：Tracing 与可观测性

Agents SDK 集成了 OpenAI 的全套可观测性工具：

> "Tracing: Built-in tracing for visualizing, debugging, and monitoring workflows, with support for the OpenAI suite of evaluation, fine-tuning, and distillation tools."

这意味着开发者可以：
- 可视化 Agent 的执行流程
- 调试复杂的多 Agent 协作
- 评估 Agent 性能并据此微调模型

### 3.5 关键新特性：Sessions

> "Sessions: A persistent memory layer for maintaining working context within an agent loop."

Sessions 解决了 Swarm 无状态设计的核心痛点。它提供了跨 turns 的状态持久化，使得 Agent 能够处理真正长时的复杂任务。

---

## 四、核心差异对比

| 维度 | Swarm | Agents SDK |
|------|-------|------------|
| **设计目标** | 教育/实验 | 生产级 |
| **状态管理** | 无状态 | Sessions 持久化 |
| **执行环境** | 纯函数调用 | Sandbox 隔离执行 |
| **安全机制** | 无内置 | Guardrails |
| **可观测性** | 无 | 内置 Tracing + Eval |
| **维护状态** | 停止维护 | 官方主动维护 |
| **Handoffs 模型** | ✅ 保留 | ✅ 保留 |
| **Agent 核心抽象** | ✅ 保留 | ✅ 保留 |

---

## 五、什么时候选择什么框架

### 5.1 选择 Swarm 的场景

笔者认为，Swarm 仍然有它的价值，但只限于以下场景：

- **学习多 Agent 编排**：Swarm 的代码简洁，是理解 Handoffs 模型的绝佳教材
- **快速原型验证**：当你想验证一个多 Agent 协作的 idea，Swarm 的上手成本最低
- **无状态短任务**：任务是一次性的，不需要跨会话状态

### 5.2 选择 Agents SDK 的场景

对于任何接近生产的项目，笔者的建议是明确的：**直接选择 Agents SDK**。

> "We recommend migrating to the Agents SDK for all production use cases."
> — Swarm README

以下场景必须使用 Agents SDK：

- 需要真实的工作区操作（文件、命令、代码编辑）
- 需要处理长时复杂任务（跨小时/天的会话）
- 需要企业级安全治理（权限控制、审计）
- 需要可观测性和调试能力

### 5.3 混合使用是可能的

官方文档指出了一个关键事实：

> "You do not need to choose one globally. Many applications use the SDK for managed workflows and call the Responses API directly for lower-level paths."

这意味着可以在同一个应用中混合使用：
- Agents SDK 管理复杂的多 Agent 工作流
- Responses API 处理简单的单步调用

---

## 六、OpenAI 的框架演进告诉我们什么

笔者认为，OpenAI 从 Swarm 到 Agents SDK 的演进，揭示了 Agent 框架发展的几个重要趋势：

**1. Handoffs 模型是有效的**
这个模型被完整保留在 Agents SDK 中，说明 OpenAI 认为让 Agent 能够动态委托任务是正确方向。

**2. 隔离执行是生产级框架的必备能力**
Sandbox Agents 的引入，意味着 Agent 不只是「回答问题」，而是要真正「执行任务」。

**3. 可观测性是工程化的起点**
内置 Tracing 和 Eval 工具，表明 OpenAI 将评估和调试能力视为 Agent 系统工程化的基础设施。

**4. 安全与治理不能是事后补丁**
Guardrails 的内置设计，说明安全机制需要在框架层面解决，而不是留给开发者自己实现。

---

## 七、结论

从 Swarm 到 Agents SDK 的演进，本质上是 OpenAI 对「什么样的 Agent 框架能够用于生产」这一问题的系统性回答。

Swarm 验证了 Handoffs 模型的可行性，证明了轻量级的多 Agent 编排框架能够工作。Agents SDK 在这个基础上，加入了生产环境必需的工程机制：Sandbox 隔离、Guardrails 安全、Tracing 可观测性、Sessions 状态持久化。

对于开发者而言，这意味着：**学习 Swarm 理解原理，使用 Agents SDK 构建生产系统**。

笔者认为，这个演进路径对于整个 Agent 框架生态都有参考价值——轻量级抽象是好的开始，但最终需要工程化才能真正落地。

---

**引用来源**：
- OpenAI Agents SDK 官方文档：https://openai.github.io/openai-agents-python/
- OpenAI Swarm GitHub：https://github.com/openai/swarm
- Agents SDK GitHub：https://github.com/openai/openai-agents-python

---

*本文属于 Agent Engineering 知识体系，归档于 `fundamentals/` 目录。*
