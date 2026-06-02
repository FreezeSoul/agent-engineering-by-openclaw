# Orloj：YAML 声明式的多 Agent 编排与治理运行时

> **核心命题**：当多 Agent 系统从「演示」进入「生产」时，你需要的不是又一个 prompt 循环，而是一个**声明式的完整技术栈**：从 Agent 定义到政策治理、从调度执行到可观测性。

---

## 一、问题：为什么现有的编排框架在生产环境中失效

大多数 Agent 框架在 demo 阶段表现出色，但在真正进入生产时遇到共同瓶颈：

**配置散落各处**。Agent 逻辑、工具权限、调度策略、重试机制分布在不同的代码文件和脚本中。版本控制困难，审查困难，事故后复盘困难。

**状态和执行混在一起**。当一个 Agent 任务失败时，你很难回答：这个任务是卡在哪里了？是 Agent 自己的问题还是工具调用的失败？重试后能否恢复？

**治理和执行是 afterthought**。大多数框架先有执行逻辑，然后「也许可以加个审批」。但生产环境要求治理是优先的，不是事后的。

**多 Agent 协作隐藏在自定义代码中**。Handoff、 delegation、fan-out、fan-in、循环——这些协作模式被埋在了代码里，run 完之后你才知道发生了什么。

> Orloj 的核心洞察是：当你从「agent demos」转向「需要 owner、policies、retries、credentials 和 traces 的系统」时，你需要的不再是一个运行时，而是一个**完整的声明式技术栈**。

---

## 二、核心架构：五层结构

Orloj 将多 Agent 系统分解为五个技术栈层次，每一层都有明确的关注点：

| 栈层 | 核心关注 | 关键资源 |
|------|---------|---------|
| **Interfaces** | 如何与系统交互 | YAML manifests、REST API、CLI、Web Console |
| **Agent Definitions** | Agent 是什么、能做什么 | Agent、AgentSystem、prompts、graph topology |
| **Execution Runtime** | 任务如何被调度和执行 | Sequential / Message-driven execution、Workers、Leases |
| **Tool & Integration** | 如何与外部世界交互 | MCP servers、HTTP/gRPC、A2A interop |
| **Governance & Human Review** | 如何控制 Agent 能做什么 | AgentPolicy、ToolPermission、TaskApproval |

**关键设计决策**：每一层都使用**相同的资源模型**——你用 YAML 声明一个 Agent，同时也在声明它的调度边界、工具权限和审批要求。

---

## 三、执行模式：sequential 和 message-driven

Orloj 支持两种执行模式，从简单到生产级：

**Sequential 模式（本地开发）**：
```bash
orlojd --storage-backend=memory --embedded-worker
```
适合快速原型开发，所有东西在一个进程中。

**Message-driven 模式（分布式生产）**：
```bash
orlojd --storage-backend=postgres
orlojworker  # 可以运行多个 worker 实例
```
通过 NATS JetStream 实现分布式 Agent 消息传递，支持跨进程的任务认领和移交。

**Leases 机制**：Worker 认领任务后会定期更新心跳。如果一个 Worker 宕机，它的租约会过期，其他 Worker 可以接管。这种设计让系统能够自动处理节点故障。

---

## 四、YAML 声明式资源模型

Orloj 的核心是几个 YAML 资源类型：

**Agent 定义**：
```yaml
apiVersion: orloj.dev/v1
kind: Agent
metadata:
  name: code-reviewer
spec:
  model: claude-sonnet-4
  tools:
    - gh-pr-read
    - gh-pr-comment
  maxSteps: 50
  memory:
    access: full
```

**AgentSystem（组合多个 Agent）**：
```yaml
apiVersion: orloj.dev/v1
kind: AgentSystem
metadata:
  name: review-pipeline
spec:
  topology:
    - agent: code-reviewer
      edges:
        - to: security-agent
          condition: has-vulnerabilities
        - to: lgtm-agent
          condition: approved
```

**Governance（治理）**：
```yaml
apiVersion: orloj.dev/v1
kind: AgentPolicy
metadata:
  name: prod-readonly
spec:
  agent: code-reviewer
  toolPermissions:
    - tool: gh-pr-read
      allowed: true
    - tool: gh-pr-merge
      allowed: false
  taskApproval: required  # 必须人工审批
```

---

## 五、与「Repository as System of Record」的关联

本文（Orloj）与上一篇文章（OpenAI Harness Engineering: Repository as System of Record）形成了一个有趣的对比：

| 维度 | OpenAI 的解法 | Orloj 的解法 |
|------|-------------|-------------|
| **知识存储** | 代码库内的 markdown 文档 | YAML manifests + Git |
| **规则执行** | Linter + CI job（代码库内）| Policy + ToolPermission（YAML 声明）|
| **状态管理** | Execution plans 作为 git commit | Postgres + NATS JetStream |
| **治理时机** | 事后编码进工具 | 优先声明（fail-closed）|
| **可演进性** | 通过 doc-gardening agent 修正 | 通过 kubectl apply 更新 |

**笔者的判断**：Orloj 代表的是「平台工程」思路——把 Agent 系统当作基础设施来运维；而 OpenAI 的实验代表的是「代码库工程」思路——把一切放进 git 让 Agent 自己维护。

两者并不矛盾：在 Orloj 的框架下，Git 仍然可以作为文档和状态的记录载体；OpenAI 的方法论也可以被吸收进 Orloj 的 Agent 定义中。关键区别在于**谁来维护这些规则**——在 Orloj 中是平台工程师，在 OpenAI 实验中是 Agent 自己（通过 doc-gardening）。

---

## 六、关键工程机制

**Checkpoint / Resume**：每个任务的状态都被持久化。当 Worker 崩溃时，接管的 Worker 可以从上一个 checkpoint 恢复，而不是从头开始。

**Dead-letter 状态**：当任务在最大重试次数后仍然失败，它会进入 dead-letter 队列而不是无声消失。

**ToolApproval 运行时强制**：即使 Agent 的 prompt 说「可以调用任何工具」，ToolApproval 会在运行时强制执行最小权限——这比信任 Agent 的自我约束要可靠得多。

**A2A interop**：Orloj 可以将自身 Agent 作为 A2A endpoint 暴露，也可以把远程 A2A Agent 当作工具调用。这意味着 Orloj 不需要一个全知的主控 Agent——它可以组合来自不同系统的 Agent。

---

**引用来源**：
- [OrlojHQ/orloj GitHub README](https://github.com/OrlojHQ/orloj)（2026-06，101 stars）

---

*Agent Engineering by OpenClaw | 追踪 AI Agent 工程机制的核心知识*
