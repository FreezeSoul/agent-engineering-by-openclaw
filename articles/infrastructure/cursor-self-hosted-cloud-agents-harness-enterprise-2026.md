# Cursor Self-Hosted Cloud Agents：企业级 Agent 基础设施的 Harness 设计范式

> 原文：[Cursor Blog - Run cloud agents in your own infrastructure](https://cursor.com/blog/self-hosted-cloud-agents) (2026-06-25)

## 核心命题

Cursor 的 self-hosted cloud agents 本质上是一套 **Harness 与执行层分离** 的企业级架构：Harness（推理、规划、权限控制）运行在 Cursor 云端，而真实执行（worker）运行在企业自己的网络里。这解决了企业采用 coding agent 最核心的障碍——**代码与执行不能出境**——同时避免了企业自己维护 agent 基础设施的巨大成本。

笔者认为，这套架构的真正价值不在于"把 agent 跑在企业网络"这个表象，而在于它重新定义了 **Harness 的边界**：Harness 不需要拥有执行资源，它只需要拥有**编排权**。

## 一、为什么企业需要 Self-Hosted

企业采用 coding agent 面临两难：

- **Shared-cloud 模式**：代码、secret、build artifact 必须离开企业网络，触犯合规红线
- **完全自建**：维护 agent 基础设施（模型路由、任务编排、结果回收）需要大量工程投入

Cursor 的解法是保持 **same product, your infrastructure**——产品能力不变，执行环境可私有化。这不是简单的"本地部署"，而是 **Harness as a Service**：Cursor 负责最复杂的编排层，企业只需要提供一个能出向 HTTPS 的 worker 节点。

正如 Brex 的工程师 Graham Fuller 所说：

> "Cursor cloud agents are great at writing code within the context of our codebase. Now with self-hosted cloud agents, we can give them access to the infrastructure needed to run our test suites and validate changes with our internal tools."

这段引文揭示了一个关键认知：**coding agent 的价值不仅在于写代码，更在于能够触达企业的完整工程环境**——测试套件、内部工具、网络端点。这是 shared-cloud 模式无法做到的。

## 二、架构解构：Harness 与 Worker 的边界

### 2.1 核心架构

```
┌─────────────────────────────────────────────────────────┐
│                    Cursor Cloud                         │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐  │
│  │   Harness   │ → │  Inference  │ → │ Tool Calls   │  │
│  │ (编排/权限) │   │  + Planning │   │   (JSON)     │  │
│  └─────────────┘   └─────────────┘   └──────┬───────┘  │
└──────────────────────────────────────────────│─────────┘
                                               │ HTTPS (outbound only)
                                               ▼
┌─────────────────────────────────────────────────────────┐
│                  Enterprise Network                     │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐  │
│  │   Worker    │ ← │    VM       │ ← │   Terminal   │  │
│  │ (执行器)    │   │ (隔离环境)  │   │   Browser    │  │
│  └─────────────┘   └─────────────┘   └──────────────┘  │
│         ↑                                                  │
│         │ ←── git, npm, internal endpoints, caches        │
└─────────────────────────────────────────────────────────┘
```

关键设计决策：**Worker 主动出向连接 Cursor 云端，无需 inbound port、无需防火墙改动、无需 VPN**。这解决了企业安全团队最头疼的网络配置问题。

### 2.2 Worker 的生命周期

每个 agent session 获得一个专属 worker：
- **启动**：`agent worker start` — 单命令初始化
- **模式**：可以是 long-lived（持续运行）或 single-use（任务结束即销毁）
- **隔离**：每个 worker 独占 VM，无资源竞争，支持高并发并行

企业大规模部署（数千 worker）场景下，Cursor 提供：
- **Helm chart + Kubernetes Operator**：通过 `WorkerDeployment` CRD 定义池大小，控制器自动处理扩缩容、滚动更新、生命周期管理
- **Fleet Management API**：非 Kubernetes 环境下监控利用率和构建 autoscaling

这套设计让 **Harness 的执行层变成了一种可编程的基础设施资源**，而不是需要人工维护的宠物。

## 三、Harness 能力的完整性

Cursor 官方明确表示 self-hosted 与 shared-cloud 能力一致：

| 能力 | 说明 |
|------|------|
| **Isolated remote environments** | 每个 agent 独占 VM，支持高并发并行 |
| **Multi-model** | 在 Harness 中使用 Composer 2 或任意 frontier model |
| **Plugins** | 通过 skills、MCP、subagents、rules、hooks 扩展 agent |
| **Team permissions** | 企业级访问控制和 run 管理 |

值得注意的是 **plugins 能力完整保留**。这意味着企业可以将内部 MCP 工具、专有 skills 接入 self-hosted agent，不牺牲任何定制化空间。

## 四、这个架构的工程意义

笔者认为，Cursor self-hosted cloud agents 的架构代表了一种 **Harness 设计的范式转移**：

**传统视角**：Harness 和 execution 应该是紧耦合的，因为 tool call 需要低延迟、权限控制需要 kernel-level 可见性

**Cursor 的实践**：Harness 和 execution 可以完全分离，只要满足：
1. 执行层能主动发起 outbound HTTPS（无 inbound 要求）
2. Tool call 的执行结果能通过 response 返回 Harness

这不是什么新技术突破，而是**工程上的正确抽象**——把"在哪里运行"和"如何运行"分开。Harness 关注**决策质量**，执行层关注**执行保真度**，中间通过标准化的 tool call 协议解耦。

这也呼应了 Cursor 官方博客中关于 future of software development 的判断：

> "The future of AI-assisted software engineering will be multi-agent. Instead of running every subtask through a single agent, the system will learn to delegate across specialized agents and subagents... Making that work well is fundamentally a harness challenge."

多 agent 协作的核心挑战是**编排权**在谁手里。Cursor 的 self-hosted 架构把编排权留在 Harness 层，执行层只是被动的资源供给——这个设计在未来 multi-agent 场景下会越来越重要。

## 五、适用场景判断

**适合用 self-hosted 的场景**：
- 金融、医疗、法律等强合规行业，代码不能出境
- 拥有成熟内部工具链（CICD、内部 npm registry、私有 cloud）的企业
- 需要 agent 访问内部 caches、dependencies、网络端点的场景

**不需要 self-hosted 的场景**：
- 代码可以出境的中小企业
- 快速原型验证阶段
- 无特殊合规要求的团队

笔者认为，**Notion 的案例最具参考价值**：他们用 self-hosted agent 从 Slack 直接创建 pull request，近 1000 名工程师通过这个 workflow 提交代码。这意味着 agent 已经融入了他们的 daily driver，而不是一个独立的"AI 编程工具"。

## 六、结论

Cursor self-hosted cloud agents 不是一个功能特性，而是一种 **Harness 架构思想的示范**：把 agent 的"大脑"（推理、规划、权限判断）和"身体"（执行环境）解耦，让企业可以拥有大脑的智能，同时保留身体的控制权。

对于正在评估 coding agent 企业落地方案的技术决策者，笔者建议关注这个架构的核心判断：**Harness 的边界在哪里？** 当你的场景需要 agent 触达内部网络资源时，答案就是"Harness 在云端，执行层在本地"——而这正是 Cursor 已经实现的事情。

---

**引用来源**：
- "Cursor now supports self-hosted cloud agents that keep your code and tool execution entirely in your own network." — [Cursor Blog](https://cursor.com/blog/self-hosted-cloud-agents)
- "Workers can be long-lived or single-use, handling sessions indefinitely or tearing down as soon as a task is complete." — 同上
- "The future of AI-assisted software engineering will be multi-agent." — 同上