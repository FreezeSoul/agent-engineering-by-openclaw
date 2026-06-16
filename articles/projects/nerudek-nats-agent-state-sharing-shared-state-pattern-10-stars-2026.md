# NATS Agent State Sharing：让多 Agent 不再「盲目工作」

> ⭐ 10 | 🔨 MIT | 🐍 Python | 📂 [GitHub](https://github.com/nerudek/nats-agent-state-sharing) | 🏷️ orchestration / shared-state / multi-agent

---

## 核心命题

Multi-agent 系统里，每个 Agent 启动时对其他 Agents 在做什么、做了什么、将做什么**一无所知**。没有共享状态，Agents 重复劳动、丢失上下文、在最坏情况下触发级联失败——比如那个烧掉 **400M tokens** 的 onboarding loop。NATS Agent State Sharing 用 NATS JetStream KV 给每个 Agent 一个**单一真实来源**，让协作从「盲跑」变成「可见可控」。

> 「In a multi-agent system, every agent starts a session with zero knowledge of what other agents are doing. Without shared state, they duplicate work, miss context, and — in the worst case — trigger cascading failures.」

---

## 问题的本质

默认情况下，AI Agents 是**无状态**的。每次会话都是一座孤岛——它不知道其他 Agents 完成了什么、正在做什么、将会做什么。这在单 Agent 场景下不是问题，但在 multi-agent 场景下是灾难的根源：

| 症状 | 根因 |
|------|------|
| 两个 Agents 解决同一个问题 | 没有共享的任务状态，无法去重 |
| Agent A 发现了关键信息，Agent B 完全不知道 | 没有跨 Agent 的上下文传播机制 |
| Onboarding loop 无解，烧掉 400M tokens | 没有消息去重，Orchestrator 每次都发 WELCOME |

这些问题不是「Agent 不够聪明」，而是**架构层面缺乏共享状态基础设施**。

---

## 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                   Agent Ecosystem                       │
│  Agent A (orchestrator) ─┐                             │
│  Agent B (worker)         ├──→ NATS JetStream           │
│  Agent C (monitor)        ─┘                             │
└────────────────────────────┬────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  NATS JetStream  │
                    ├─────────────────┤
                    │  KV Store        │  state, config, sessions
                    │  Pub/Sub         │  events, heartbeats
                    │  Deduplication   │  防止重复消息
                    └─────────────────┘
```

**三层能力**：

1. **Key-Value Store**：写一次，所有 Agents 可见。任务状态、配置、会话信息都可以 kv 形式共享。
2. **Pub/Sub Event Bus**：Agents 发布事件（任务开始/完成/出错），其他 Agents 订阅并响应。
3. **Message Deduplication**：`bridge/dedup.py` 模块专门解决 onboarding loop 问题——这是那 400M token incident 的直接解决方案。

---

## 为什么是 NATS，而不是 Redis / HTTP API / SQLite

| 替代方案 | 问题 | 为什么会失败 |
|---------|------|-------------|
| **Redis** | 单点故障，需要独立基础设施 | 引入额外依赖，而 NATS 已经在消息场景跑着，KV 能力是免费的 |
| **HTTP REST API** | 请求/响应模式，无 push，无 streaming | Agents 只能 polling，浪费 cycles，延迟高 |
| **SQLite** | 无 pub/sub，无 clustering | 单机单 Agent 可以，多 Agent 协作完全无力 |
| **自定义 TCP 协议** | 重新发明轮子 | Auth、retry、序列化全要自己维护，NATS 34KB 二进制零依赖解决全部 |

**笔者认为**：NATS JetStream KV 在这里是一个「刚好够用」的选择——它不是功能最强大的（比不上专用的分布式数据库），但它是**运维成本最低且生产级别可靠**的方案。对于 multi-agent 系统来说，状态共享只是难题的一部分，过度工程化的基础设施会分散对核心协调逻辑的注意力。

---

## 快速上手

```bash
git clone https://github.com/nerudek/nats-agent-state-sharing
cd nats-agent-state-sharing

# 启动带 JetStream 的 NATS
nats-server -js &

# 运行带去重的 bridge
python3 bridge/dedup.py
```

---

## 在协调模式中的位置

本文直接对应 [Anthropic 的 Shared State 协调模式](/articles/orchestration/claude-multi-agent-coordination-patterns-five-architectures-2026.md)。五种协调模式中，Shared State 是最符合直觉但实现最复杂的——而 NATS Agent State Sharing 提供了**生产级别的最小化实现**，回避了过度工程化的问题。

---

*项目截图暂缺。README 原文引用：「Stop your agents from working blind.」*