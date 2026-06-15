# Solace Agent Mesh：事件驱动多 Agent 编排的生产级实践

> 当 Agent 之间的通信变成真正的消息流，而不是函数调用

---

## 核心命题

多 Agent 系统的协作通常被实现为函数调用或共享内存——一个 Agent 直接调用另一个 Agent 的方法，等结果返回。但在真实生产环境中，这种同步模式的问题在于：**任何一个 Agent 阻塞或崩溃都会级联影响整个系统**。

Solace Agent Mesh 的核心设计选择是把 Agent 之间的通信变成**事件驱动**的异步消息流。所有 Agent 通过 Solace Event Mesh 通信，每个 Agent 是独立的，不知道其他 Agent 的存在，只响应消息。Orchestrator Agent 负责任务分解和委托，但执行是真正解耦的——这是多 Agent 编排从「调用」走向「架构」的工程分界。

---

## 为什么这是真正的架构区别

大多数多 Agent 框架的「协作」本质上是这个模式：

```python
# 大多数框架的实现
result = agent_b.do_something(agent_a.get_context())
```

这是**同步 RPC 风格的协作**，Agent A 必须等待 Agent B 完成才能继续。它的问题在于：
- Agent B 慢，Agent A 就阻塞
- Agent B 崩溃，Agent A 没有备选路径
- 无法水平扩展——你不能把 Agent B 部署在另一台机器上

Solace Agent Mesh 的模式是：

```python
# SAM 的实现
# Agent A 发布任务事件到 Event Mesh
event_mesh.publish("task.database_query", payload)

# Agent B 订阅并异步处理
event_mesh.subscribe("task.database_query", handle_query)
# 不阻塞，立即返回
```

这带来了本质区别：**每个 Agent 都是独立的消费者/生产者，系统吞吐量由 Event Mesh 的容量决定，而不是最短板的那个 Agent**。

---

## 技术架构解析

SAM 的架构由三层组成：

**底层：Solace AI Connector (SAC)**
SAC 将 Solace Event Brokers 连接到 AI 模型和服务。它负责 broker 连接、配置加载和组件生命周期管理。这是整个系统的传输层。

**中间层：Google ADK**
ADK 提供 Agent 运行时、LLM 交互、工具执行和状态管理。每个 Agent 在 ADK 中定义其 LLM 模型、指令和工具。ADK 处理 ReAct 循环的具体实现。

**顶层：A2A Protocol**
Agent-to-Agent 协议是通信层。Agent 发现彼此，委托任务给对等方，通过 A2A 协议在 Solace 上通信。

```
┌─────────────────────────────────────────────┐
│            Solace Event Mesh                 │
│  (异步消息总线，Agent 之间的唯一连接点)        │
├─────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Orchestrator│  │Database  │  │Multimodal│  │
│  │  Agent   │  │  Agent   │  │  Agent   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │         │
│  Google ADK + Solace AI Connector (SAC)    │
└─────────────────────────────────────────────┘
```

**Orchestrator Agent** 是这个架构的调度核心。当用户提出复杂请求时：
1. Orchestrator 接收请求，理解任务
2. 将任务分解为子任务
3. 通过 Event Mesh 委托给相应的专业 Agent（Database Agent、Multimodal Agent 等）
4. 收集结果，聚合响应
5. 每个子 Agent 独立执行，不阻塞 Orchestrator

---

## A2A Protocol 的实际意义

SAM 实现的是 Agent-to-Agent (A2A) 协议，这是一种让 Agent 发现彼此并委托任务的标准化方式，不是 MCP（Model Context Protocol）或 Function Calling。

关键区别：

| 协议 | 用途 | 通信模式 |
|------|------|---------|
| **MCP** | Agent ↔ 工具/数据源 | 同步请求/响应 |
| **Function Calling** | Agent ↔ 模型 | 工具调用 |
| **A2A** | Agent ↔ Agent | 异步消息/事件 |

A2A 解决的是「Agent 生态」的问题：当你的系统里有 10 个不同团队开发的 Agent，如何让它们互相发现和通信，不需要每个 Agent 都硬编码知道其他 Agent 的存在？答案是通过 Event Mesh 做服务发现，每个 Agent 向 Mesh 注册自己的能力，其他 Agent 通过 Mesh 发现并委托。

---

## 快速开始：5 分钟跑起来

SAM 的安装和运行非常简洁：

```bash
# 创建虚拟环境
mkdir my-sam && cd my-sam
python3 -m venv .venv && source .venv/bin/activate

# 安装
pip3 install solace-agent-mesh

# 初始化并启动 GUI
sam init --gui
sam run

# 打开 http://localhost:8000 开始对话
```

添加新的专业 Agent 同样简洁：

```bash
sam add agent --gui
```

或者通过 YAML 配置（SAM 的设计哲学是配置优于代码）定义 Agent 的能力、LLM 模型和工具。

---

## 与上一轮 Article 的配对关系

| 维度 | Article | Project |
|------|---------|---------|
| **主题** | Harness Engineering：配置 > 模型 | Solace Agent Mesh：事件驱动的多 Agent 编排 |
| **关联性** | 讨论了 Planner/Generator/Evaluator 三分离、Hook 机制 | Orchestrator Agent 实现了 Planner 角色，专业 Agent 实现 Executor 角色 |
| **工程机制** | 三分离模式是设计原则 | SAM 的 Orchestrator + 专业 Agent 分离是工程实现 |
| **协作维度** | Hook 是单 Agent 内部的强制层 | A2A Protocol 是多 Agent 之间的事件驱动协作层 |

Article 解释了「为什么分离生成与评估Agent是好的设计」，Project 展示了「这种设计在事件驱动架构中如何落地」。

---

## 适用场景

**值得用 SAM 的场景：**
- 复杂任务需要多个专业 Agent 协作（数据库查询 + 图像生成 + 报告聚合）
- 需要真正的水平扩展——不同 Agent 部署在不同机器上
- 需要生产级的可靠性——Event Mesh 提供了消息持久化和重试
- 已经使用 Solace 作为企业消息中间件

**不需要 SAM 的场景：**
- 简单任务，单个 Agent 就能完成
- 小规模实验，原型阶段用同步调用更简单
- 团队没有使用或不想引入 Solace Event Broker

---

## 引用来源

> "Solace Agent Mesh is a framework that supports building AI applications where multiple specialized AI agents work together to solve complex problems. It uses the event messaging of Solace Platform for true scalability and reliability."
> — [SolaceLabs/solace-agent-mesh README](https://github.com/SolaceLabs/solace-agent-mesh)

> "SAM creates a standardized communication layer where AI agents can delegate tasks to peer agents, share data and artifacts, connect with diverse user interfaces and external systems, and execute multi-step workflows with minimal coupling."
> — [SolaceLabs/solace-agent-mesh README](https://github.com/SolaceLabs/solace-agent-mesh)

> "The result is a fully asynchronous, event-driven and decoupled AI agent architecture ready for production deployment. It is robust, reliable and easy to maintain."
> — [SolaceLabs/solace-agent-mesh README](https://github.com/SolaceLabs/solace-agent-mesh)

---

## 资源

- **GitHub**: https://github.com/SolaceLabs/solace-agent-mesh
- **文档**: https://solacelabs.github.io/solace-agent-mesh/
- **PyPI**: `pip3 install solace-agent-mesh`
- **License**: Apache 2.0