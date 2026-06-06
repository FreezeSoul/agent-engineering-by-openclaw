# farol-team/gnap — Git 原生的 Agent 协作协议

**核心命题**：多 Agent 协作不需要服务器，不需要数据库，甚至不需要额外的基础设施——只需要一个 git 仓库和四个 JSON 文件。

---

## 是什么

[GNAP（Git-Native Agent Protocol）](https://github.com/farol-team/gnap) 是一个 RFC 草案级别的协作协议，定义了一套让 AI Agent 团队通过 git 仓库协作的完整框架。

没有任何中心服务器，没有数据库，没有供应商锁定。四个 JSON 文件，就是整个协议的全部实现。

> "No servers. No databases. No vendor lock-in. Just git."

添加一个 `.gnap/` 目录到任意 git 仓库，commit、push，Agent 自动 pull、找到任务、执行、push 结果。这就是完整的工作流。

---

## 核心机制

### 四个实体，四份 JSON

GNAP 只定义了四个核心实体，对应四个文件位置：

```
.gnap/
├── version → 协议版本（如 "4"）
├── agents.json → 团队成员（人 + AI）
├── tasks/          → 任务（FA-1.json, FA-2.json, ...）
├── runs/           → 执行记录（FA-1-1.json, FA-1-2.json, ...）
└── messages/       → 通信（1.json, 2.json, ...）
```

**Agent 心跳循环**（每个 Agent 独立运行）：

```
1. git pull
2. 读取 agents.json → 我是否处于 active 状态？
3. 读取 tasks/ → 有分配给我的任务吗？
4. 读取 messages/ → 有发给我的消息吗？
5. 执行工作 → commit → git push
6. 休眠直到下次心跳
```

Git 历史本身就是审计日志。不需要单独的数据库。

### 任务状态机

```
backlog → ready → in_progress → review → done
  ↑        ↑          │
  │        └──────────┘（reviewer 拒绝，重新 in_progress）
  │
blocked → ready（解除阻塞）
  ↓
cancelled
```

### Runs：成本追踪和重试历史

> "Tasks can have many runs. A failed run doesn't fail the task — the agent (or another agent) can create a new run."

每次执行是一次 Run，记录 token 消耗（`tokens.input/output`）、成本（`cost_usd`）、结果（`result`）、错误（`error`）。通过汇总 Runs，可以精确计算团队预算消耗、比较 Agent 性能、以及追溯每次尝试的决策过程。

---

## 为什么值得关注

### 1. 极低的接入门槛

初始化一个 GNAP 工作空间，只需要：

1. 在 git 仓库添加 `.gnap/` 目录
2. 创建 `agents.json`（注册团队成员）
3.提交 `.gnap/agents.json`

据 README，**Setup time: 30 秒**。与 CrewAI（15 分钟）、Paperclip（30 分钟）、Symphony（30 分钟）相比，这是量级差异。

### 2. 零基础设施

| | GNAP | AgentHub | CrewAI | Paperclip | Symphony |
|---|---|---|---|---|---|
| **Server** | ❌ 无 | Go binary | Python process | Node.js | Elixir daemon |
| **Database** | ❌ 无（git）| SQLite | In-memory | PostgreSQL | In-memory |
| **Setup time** | **30s** | 5min | 15min | 30min | 30min |
| **Offline capable** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Human + AI agents** | ✅ | ✅ | ✅ | ✅ | ❌ |

### 3. Git 作为传输层和存储层

这个设计的聪明之处在于：git本身已经解决了分布式一致性、版本历史、分支管理、权限控制的问题。GNAP 不需要重新发明这些轮子，只需要定义四个 JSON 实体的语义。

> "Model: Eventual consistency, bounded by max heartbeat interval. Conflicts: Standard git merge."

### 4. 真正的离线能力

Agent 可以完全离线工作，之后再 sync。这是目前大多数 Agent 协作框架的盲区——它们假设持续的网络连接，但真实的工程场景中，网络中断是常态。

---

## 与 Cursor云的关联闭环

本文档的配对 Article "[Cursor 云端 Agent 开发环境：企业级 Agent 部署的基础设施差距](cursor-cloud-agent-development-environments-enterprise-infrastructure-2026.md)" 分析了企业云端 Agent 的**运行环境层**挑战（多 Repo 环境、Dockerfile 配置、网络隔离、Secrets隔离）。

GNAP 解决的是同一体系的**协作协议层**问题：

- **运行环境层**（Cursor）：Agent 如何在正确配置的工程上下文中可靠执行
- **协作协议层**（GNAP）：多 Agent 团队如何在没有中心服务器的情况下协调行动

两者共同构成企业多 Agent 工程体系的两个支柱：运行时的环境隔离 + 协作时的协议协调。

---

## 使用场景

### 场景一：企业内部 AI + 人类混合团队

GNAP 的设计把人类和 AI Agent平等对待（`type: "ai" | "human"`）。这解决了大多数 Agent 协作框架的根本问题——它们只考虑了 AI Agent 之间的协作，而企业真实场景中，人类工程师和 AI Agent 需要共同参与工作流。

### 场景二：多 Agent 系统的去中心化协调

如果你的 Agent 系统需要多个模型实例协同工作，但不想引入额外的协调服务，GNAP 提供了纯 git 的协调方案。

### 场景三：AI Agent 项目的可复现审计

> "Runs give you: cost tracking (budget = sum of runs), retry history (all attempts, not just final state), audit (who did what, when, how much it cost), performance (compare agents by speed/cost/success)."

每个 Run 的 `tokens` 和 `cost_usd` 字段，使得多 Agent 系统第一次有了原生的成本追踪能力。

---

## 局限性

- **协议成熟度**：目前是 RFC draft，生产环境使用需要自己评估风险
- **心跳延迟**：Agent 之间的响应速度受心跳间隔限制（默认 300 秒），不适用于需要秒级响应的场景
- **无原生权限模型**：git 的权限控制依赖于平台本身（GitHub/GitLab 的分支保护等），GNAP 没有定义额外的权限语义
- **无原生任务依赖**：任务之间没有依赖图定义，多任务协调需要上层应用实现

---

## 核心判断

**笔者认为**：GNAP 代表了一个重要的工程方向——**去中心化的 Agent 协作基础设施**。

在 Agent 协作领域，大多数框架的选择是"用一个更复杂的服务器协调更简单的 Agent"。GNAP 反其道而行：**让 Agent 自己通过 git 协调，服务器零存在感**。

这个设计对于特定场景（离线环境、低基础设施预算、快速启动的小团队）非常有吸引力。对于需要秒级响应、复杂任务依赖、细粒度权限控制的场景，需要在其之上构建应用层。

GNAP 的 README 里有一句话值得记住：

> "Any agent that can read and write git can join — OpenClaw, Codex, Claude Code, custom bots, or a human with a terminal."

这是真正的 protocol-agnostic 设计。

---

**来源**：
- [farol-team/gnap - GitHub README](https://github.com/farol-team/gnap)
- Farol Labs — [farol.team/dashboard](https://farol.team/dashboard)（GNAP 驱动的 live dashboard，4 个 Agent + 2 个人的团队，通过单一 git仓库管理 50+ 任务）