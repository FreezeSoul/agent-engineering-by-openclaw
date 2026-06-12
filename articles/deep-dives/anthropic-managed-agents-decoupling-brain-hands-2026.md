# Anthropic Managed Agents：把「大脑」从「手」上解耦出来

> 本文是对 Anthropic 2026 年 4 月 8 日工程文章 "[Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)" 的深度解读。
> 原文发布于 Claude Managed Agents 公开上线前一天（2026 年 4 月 9 日），是少见的、来自厂商内部的架构决策复盘。

---

## 核心命题

**一个 AI Agent 不是一台 monolithic 的机器，而是三个独立演化组件的组合：**

| 组件 | 职责 | 演化速度 |
|------|------|---------|
| **Brain**（模型）| 推理、决策 | 跟随模型升级（几个月一次）|
| **Hands**（执行沙箱）| 调用工具、操作资源 | 跟随容器运行时升级 |
| **State**（状态）| 会话、记忆、checkpoint | 跟随存储后端升级 |

Anthropic 的核心论点是：**这三个组件必须被设计成可以相互替换的**，因为它们各自在不同的时钟上演化。Model 变了，不应该影响沙箱配置；存储后端换了，不应该要求重训模型。

这个原则听起来简单，但真正落地时意味着什么？

---

## 问题的起源：VPC 客户投诉

Anthropic 透露了一个真实的客户痛点：

> "当团队想让 Claude 操作他们自己 VPC 里的资源时，唯一的路径是把他们的网络和我们的网络对等互联——因为当时的 harness 容器假设所有资源都在它旁边。"

这是经典的**紧耦合架构**：harness（即 Hands）不仅负责执行，还隐式地绑定了网络位置。当客户的环境和 Anthropic 的环境不在同一个网络时，要么走复杂的网络对等，要么客户就根本无法使用。

解耦之后，Brain（即模型推理）可以通过 API 调用远程执行，而 Hands（沙箱）可以部署在客户自己的 VPC 里。Brain 和 Hands 之间通过标准化接口通信，和具体在哪个网络无关。

---

## 三层解耦的工程含义

### 1. Brain / Hands 解耦

关键设计：**工具调用不再内嵌在模型推理进程中，而是通过独立的执行层完成**。

这意味着：

- **同一个 Agent 可以有不同的 Hands**：测试用轻量沙箱，生产用高安全隔离沙箱
- **Brain 升级不影响 Hands 配置**：换模型不需要重新调试工具权限
- **跨云/跨网络执行成为可能**：Hands 可以部署在任何有网络连接的地方

从工程角度，这种模式和微服务架构中的「计算与网络解耦」完全一致。只不过这里「计算」是 LLM 推理，「网络」是工具调用通道。

### 2. State 外置

Managed Agents 的状态（会话历史、working memory、checkpoint）不再存在 Agent 进程内部，而是外置到独立的存储层。

这解决了三个实际问题：

- **跨会话恢复**：Agent 重启后可以恢复到上一个 checkpoint
- **多实例一致**：同一个 Agent 的多个并发实例共享状态
- **存储后端可替换**：PostgreSQL 换成 Redis，Agent 代码不需要改

### 3. 接口固化

Anthropic 没有在文章里明说，但暗示了一个关键原则：**Brain / Hands / State 之间的接口是 stable 的**，不应该随着实现变化而变化。

就像 IBM PC 时代，应用程序依赖的是 DOS API，而不是某块具体的内存芯片。API 是稳定的，实现是可以替换的。

> "History does not repeat itself identically, but every technology revolution produces the same illusion: that the infrastructure of the moment is solid enough to become the foundation of the next product generation."
>
> — 这个观察直接指出了为什么接口设计比具体实现更重要。

---

## 这和以前的架构有什么区别？

### 传统 Agent 架构（monolithic）

```
┌─────────────────────────────┐
│      Agent Process          │
│  ┌─────────┬──────────┐    │
│  │  Model  │  Tools   │    │
│  │ (Brain) │ (Hands)  │    │
│  └─────────┴──────────┘    │
│         │                   │
│    State (in-memory)        │
└─────────────────────────────┘
         │
    Customer VPC（无法访问）
```

问题：Model + Tools + State 全在一个进程里。任意一个组件的变化都影响其他组件。

### 解耦后的 Managed Agents 架构

```
┌──────────┐      API       ┌───────────┐
│  Brain   │ ←───────────→ │   Hands   │
│ (Model)  │   standardized │ (Sandbox)│
└──────────┘      interface  └──────────┘
                                    │
                             Customer VPC（可访问）
                                    │
                              ┌──────────┐
                              │  State   │
                              │(Storage) │
                              └──────────┘
```

关键变化：Brain 和 Hands 之间通过「标准化的 tool calling 协议」通信，不关心对方在哪里、不关心对方用什么具体技术实现。

---

## 笔者认为：这个架构的真正价值不在于「解耦」，而在于「接口 survivability」

很多架构文章讲「解耦」讲得很好，但往往停在「模块化」这个层面。Anthropic 这篇文章更进一步：**它明确提出了接口的 survivorship 问题**。

什么意思？

- Model 供应商会变（Claude 3.5 → Claude 3.7 → 未来的 Claude 4）
- 沙箱技术会变（现在的容器 → 未来可能有 VM、WebAssembly 隔离）
- 存储后端会变（PostgreSQL → 分布式 KV store）

**如果你的 Agent 架构设计正确，这些变化应该只影响具体实现，不影响使用这些组件的应用。** 这就是「接口 survivability」。

对于 build 在 Claude 上层的开发者来说，这意味着：

1. **不要假设 Agent 的内部结构是透明的** — 你依赖的应该是 tool calling 接口，而不是 Agent 进程的内部状态
2. **关注接口稳定性，而不是实现细节** — 当 Anthropic 升级模型时，你的工具调用应该继续工作；当他们换存储后端时，你的会话应该继续恢复
3. **用标准协议而非私有 API** — MCP 协议的价值不仅在于「让 Agent 调用工具」，更在于它是一个稳定的、跨实现的接口契约

---

## 和已有工作的关联：Dreaming、Orchestration、Webhooks

Anthropic 同一时期还发布了其他几个工程文章，它们共同构成了 Managed Agents 的完整架构图谱：

| 文章 | 主题 | 与本文关系 |
|------|------|-----------|
| "Dreaming" 架构 | State 层的 sleeping/wake 机制 | State 外置的具体实现模式 |
| Multi-agent orchestration | 多 Agent 协作协议 | Brain/Hands 解耦后，多 Brain 可以共享同一套 Hands |
| Webhooks | 外部系统的回调集成 | Hands 解耦后，工具可以触发外部 webhook，不需要暴露内部 Agent 状态 |

这三者加上 Brain/Hands/State 解耦，共同构成了一套**接口驱动的 Agent 架构方法论**。不是某一个酷炫的新技术，而是一套让 Agent 系统能够长期演化的设计哲学。

---

## 引用

> "Decoupling the brain from the hands solved one of our earliest customer complaints. When teams wanted Claude to work against resources in their own VPC, the only path was to peer their network with ours, because the container holding the harness assumed every resource sat next to it."
>
> — Anthropic Engineering, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents), April 8, 2026

> "An AI agent is not a single monolithic thing. It is a brain that reasons (the model), hands that execute (sandbox and tools), and a memory that persists state (sessions, logs, checkpoints). Anthropic argues that each piece must be designed to be replaced without throwing away the rest, because each one evolves on a different clock."
>
> — Pasquale Pillitteri 的分析文章引用的 Anthropic 核心论点

---

## 结论

Anthropic 这篇文章的核心贡献不是某个新工具或新协议，而是一种**架构哲学的明确表达**：Agent 系统应该围绕 stable interfaces 设计，而不是围绕具体实现。

对于 Agent 工程师来说，这意味着：

- **设计工具时**：优先使用标准协议（MCP），而不是私有 API
- **设计 Agent 架构时**：把 Brain / Hands / State 当作三个独立的组件，定义它们之间的接口
- **评估供应商时**：问的不是「模型有多强」，而是「接口有多稳定」

这不是一个马上能上手的技巧，但这是一套让 Agent 系统在接下来 3-5 年内不会因为技术变化而需要重写的设计原则。

---

**关联 Project**: [Headroom — 上下文压缩层](/articles/projects/chopratejas-headroom-context-compression-24534-stars-2026.md) — Brain/Hand 解耦后，State（会话上下文）的体积管理成为新瓶颈，Headroom 正是解决这个问题的工程工具。