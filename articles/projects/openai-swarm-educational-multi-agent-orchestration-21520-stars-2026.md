# OpenAI Swarm：轻量级多 Agent 编排的教育级框架

> **Stars**：21,520（GitHub）
> **来源**：https://github.com/openai/swarm
> **技术栈**：Python 3.10+，基于 Chat Completions API

---

## 背景：Swarm 是什么

OpenAI Swarm（2024）是 OpenAI 解决方案团队维护的**教育级框架**，用于探索轻量级、多 Agent 编排模式。虽然已在文档中明确标注为实验性、教育性资源，但它奠定了多 Agent 编排的核心概念基础。

**关键声明**：Swarm 已被 [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) 取代，后者是 Swarm 概念的生产级进化版本。

---

## 核心抽象：Agent + Handoff

Swarm 的强大之处在于用两个原语抽象表达复杂的多 Agent 协调：

### Agent

```python
from swarm import Swarm, Agent

client = Swarm()

agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)
```

一个 Agent 包含：
- **instructions**：Agent 的行为指令
- **tools**：Agent 可调用的函数
- **functions**：允许 Agent 将对话转交给另一个 Agent 的函数

### Handoff（交接）

Agent 在任何时刻都可以选择将对话转交给另一个 Agent：

```python
def transfer_to_agent_b():
    return agent_b

agent_a = Agent(
    name="Agent A",
    instructions="You are a helpful agent.",
    functions=[transfer_to_agent_b],
)

agent_b = Agent(
    name="Agent B",
    instructions="Only speak in Haikus.",
)
```

这类似于 Agent 层面的「路由」机制——不是中心化的调度器，而是一个分布式的交接协议。

---

## 架构哲学：无状态 + 轻量级

**Swarm 运行（几乎）完全在客户端**，与 Chat Completions API 类似，**状态不在调用之间存储**。

这意味着：
- 每个 `client.run()` 调用是独立的
- Agent 的记忆和状态由开发者自己管理
- 没有内置的持久化、会话管理或多轮对话支持

**这正是它的教育价值所在**：Swarm 揭示了多 Agent 编排的本质——handoff 模式 + 无状态调用 + 函数作为交接机制——而不被复杂的运行时基础设施掩盖。

---

## Swarm vs Agents SDK

| 维度 | Swarm | Agents SDK |
|------|-------|------------|
| **定位** | 实验性、教育性 | 生产级 |
| **状态管理** | 无状态 | 内置内存和会话管理 |
| **维护状态** | OpenAI 解决方案团队（非活跃维护） | OpenAI 官方活跃维护 |
| **适用场景** | 学习多 Agent 编排概念 | 生产环境部署 |

---

## 应用场景示例

Swarm 的 examples 目录包含多个有价值的场景：

### 分诊 Agent（Triage Agent）
```python
# 基础的分诊步骤，将用户转交给正确的 Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="Determine which agent is best suited to help.",
    functions=[transfer_to_sales, transfer_to_support],
)
```

### 航空公司客服（Airline）
多 Agent 设置，处理不同的客户服务请求（改签、投诉、退款等）。

### 个人购物（Personal Shopper）
可帮助完成销售和退款订单的个人购物 Agent。

---

## 核心洞察

**Swarm 的价值不在于它是一个生产框架，而在于它揭示了多 Agent 编排的最小原语**：Agent 定义 + 函数交接 + 无状态调用。这套模式成为了后续 OpenAI Agents SDK 的概念基础。

如果想学习多 Agent 系统的核心机制，Swarm 仍是最好的起点之一——它的源代码简单、可读，概念清晰，没有隐藏的基础设施复杂性。

---

> **引用来源**：
> - "Swarm focuses on making agent coordination and execution lightweight, highly controllable, and easily testable" — GitHub README
> - "Swarm Agents are not related to Assistants in the Assistants API... Swarm is entirely powered by the Chat Completions API and is hence stateless between calls" — GitHub README
> - "Swarm is an educational resource for developers curious to learn about multi-agent orchestration" — GitHub README