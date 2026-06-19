# agent-substrate/substrate：Google 的 Agent 原生基础设施层

> Google | Apache-2.0 | 566 Stars | 104 Forks | Go

---

## 核心命题

**如果把 Kubernetes 的调度能力看作 OS 级别的资源管理，Agent Substrate 就是在 Kubernetes 之上构建的 Agent 级别操作系统——它把大量"准空闲"的 Agent 状态映射到少量真实 Pod 上，实现 30 倍以上的资源复用，同时保持每个 Agent 独立的状态和文件系统。**

笔者认为，这个项目解决了一个 Google 内部真实存在的问题：Agent 类工作负载和普通微服务 workloads 的行为模式截然不同——Agent 大部分时间在等待用户输入或外部系统响应，实际计算只占极小比例。让 Kubernetes 按微服务的标准来调度 Agent 是一种错配，Agent Substrate 正是对这种错配的修正。

---

## 这个项目解决什么问题

### Kubernetes 对 Agent 不够友好

传统的 Kubernetes 调度是面向 long-running 服务的：
- Pod 是调度的基本单位
- 一个 Pod 通常运行一个服务实例
- 扩缩容以副本数为基础

但 Agent workloads 的行为模式完全不同：
- **大量时间在 idle**（等待用户、等待外部 API、等待模型响应）
- 实际计算时间只占总时间的很小比例
- 状态（内存、文件系统、会话）是核心资产

把这种 workloads 跑在标准 Kubernetes 上，要么造成资源浪费（Pod 常驻但利用率极低），要么造成调度低效（频繁创建/销毁 Pod 的延迟）。

### Agent Substrate 的设计思路

Agent Substrate 的核心观察：

> "Agent-like applications tend to be idle most of the time. It builds on top of Kubernetes features like Pods and Pod autoscaling, but takes the Kubernetes control-plane out of the critical path to achieve lower latency."

关键设计：
1. **Actor 模型**：每个 Agent 是一个"Actor"，运行在 Substrate 的逻辑抽象上，不直接绑定到某个 Pod
2. **Worker Pool**：少量 Kubernetes Pod 作为"Worker"，承载大量 Actor 的实际执行
3. **Multiplexing**：利用 Agent 大量 idle 的特性，在少量 Worker 上 multiplex 大量 Actor，实现 30 倍以上的资源复用

---

## 核心技术能力

### 1. 即时会话迁移（Instant Session Teleport）

Agent Substrate 能在亚秒级时间内将 Actor suspend 到某个 Worker，然后 resume 到另一个 Worker：

```
Actor A on Worker-1 → suspend (保存完整状态) → Worker-2 resume
```

这个能力对于长时 Agent 至关重要——当某个 Worker 需要维护或扩缩容时，运行在上面的 Agent 可以无缝迁移，不丢失状态。

### 2. 状态持久化

每次 hibernation 会保存 Actor 的完整状态：
- **volatile RAM**（工作内存）
- **filesystem state**（文件系统）

恢复时 Actor 从上一个检查点完整恢复，就像什么都没发生过。

### 3. 框架无关（Framework Agnostic）

Agent Substrate 不绑定特定 Agent 框架或 Harness：

> "It can run on any Kubernetes cluster and does not inhibit 'regular' use of Kubernetes in any way."

支持的框架：
- **Google ADK**：原生的 session identity 和 persistent working memory
- **LangChain**：适合 long-running、stateful 的 LangChain Agent
- **Claude Code & Codex**：高密度有状态的 coding 环境，保留 terminal 和 filesystem 状态
- **MCP**：MCP 服务器可以作为 Substrate Actor 部署，提供持久的工具服务
- **Google Agent Executor**：分布式 Agent runtime 构建在 Agent Substrate 上

---

## 架构解析

```
┌─────────────────────────────────────────────┐
│         Agent Substrate Control Plane        │
│  ┌─────────────┐  ┌──────────────────────┐ │
│  │   Actor     │  │   Scheduler           │ │
│  │   Registry  │  │   (not K8s control   │ │
│  │             │  │    plane in critical  │ │
│  │  250 actors │  │    path)             │ │
│  └─────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────┘
           │                    │
           ▼                    ▼
    ┌────────────┐      ┌────────────┐
    │  Worker-1  │ ...  │  Worker-N  │
    │  (Pod)     │      │  (Pod)     │
    │            │      │            │
    │  Actor A   │      │  Actor X   │
    │  Actor B   │      │  Actor Y   │
    │  Actor C   │      │            │
    └────────────┘      └────────────┘
```

关键点：**Kubernetes 提供基础设施和生命周期管理，Agent Substrate 提供 Agent 特定的调度和状态管理**。两者各司其职，不相互干扰。

---

## 与 Rovo Long Horizon 的关联

Atlassian 的 Rovo Long Horizon 解决了"Agent 如何在长时任务中保持推理连贯性"（单 LLM、单上下文、150 次迭代循环）。

Agent Substrate 解决了另一个维度的问题：**当 Agent 需要运行数小时甚至数天时，基础设施如何保证其状态不丢失、调度不中断**。

两者共同指向一个更大的趋势：**2026 年的 Agent 工程正在从"让 Agent 能跑"演进到"让 Agent 能长期稳定地跑"**——短时任务（几分钟）和长时任务（数天）对架构的要求有着本质差异。

---

## 适用场景

✅ **需要跑大量并发 Agent 的平台**：如 Agent marketplace、企业内部 Agent 平台  
✅ **需要 Agent 状态跨会话保持的生产环境**：不丢失用户上下文  
✅ **需要弹性伸缩 Agent 计算资源的场景**：根据负载动态调整 Worker 数量  
❌ **不需要保持状态的短时任务**：Overkill  
❌ **需要极低延迟响应的实时交互**：suspend/resume 有毫秒级延迟  
❌ **v0.x 早期阶段**：项目明确表示 API 不保证向后兼容  

---

## README 原文引用

> "Agent Substrate maps a larger set of 'actors' (applications such as agents) onto a smaller set of ready 'workers' (Kubernetes Pods), relying on the fact that agent-like applications tend to be idle most of the time to achieve heavy multiplexing."

> "It provides functionality to manage an actor's lifecycle (e.g. create/destroy, suspend/resume), to assign actors to workers in real time, and to route incoming traffic to them."

---

## 快速上手

```bash
# 安装 Substrate
kubectl apply -f https://raw.githubusercontent.com/agent-substrate/substrate/main/deploy/substrate.yaml

# 运行 Counter Demo
kubectl apply -f https://raw.githubusercontent.com/agent-substrate/substrate/main/demos/counter/demo.yaml

# 查看 Actor 状态
substratectl actors list
```

---

## 总结

Agent Substrate 是一个在正确时间出现的正确项目——当 Agent 从实验走向生产，从单次调用走向持续运行，基础设施层面的调度创新就成了刚需。

笔者认为，这个项目的意义不在于它当前的状态（v0.x，very early），而在于它提出的问题：**Kubernetes 能满足 Agent  workloads 的需求吗？还是需要 Agent Native 的调度层？** 这个问题随着 Agent 的大规模生产部署会变得越来越重要。
