# Multi-Agent 协调模式：五种架构范式与决策框架

> 📅 2026-04-10 | 🔗 [原文](https://claude.com/blog/multi-agent-coordination-patterns) | 🏷️ orchestration / multi-agent / architecture

---

## 核心论点

Multi-agent 系统的核心问题不是「用不用多 Agent」，而是**一旦决定用，如何让它们协同工作**。Anthropic 给出了官方答案：五种协调模式，本质上回答的是同一个问题的不同切面——**在哪里切分 context 边界、信息如何流动、系统何时停止**。

> 「We've seen teams choose patterns based on what sounds sophisticated rather than what fits the problem at hand. We recommend starting with the simplest pattern that could work.」

---

## 五种协调模式

### 1. Generator-Verifier：质量门控模式

**结构**：一个 Agent 生成输出，另一个 Agent 根据显式标准验证。

```
Generator → [输出] → Verifier → [通过/拒绝] → 迭代或结束
```

**适用场景**：输出质量可被显式评估（代码正确性、安全扫描、格式校验）。

**笔者认为**：这是最容易低估的模式。团队往往觉得「两个 Agent 成本高」，但当验证标准清晰时，Generator-Verifier 能把最终输出质量提升一个数量级。关键在于 Verifier 的评估标准必须**可形式化**，如果无法描述「什么是正确的」，这个模式就会失效。

**已知局限**：不适用于输出难以客观评估的任务；验证轮次过多时成本显著上升。

---

### 2. Orchestrator-Subagent：任务分解模式

**结构**：中央 Orchestrator 负责任务分解、子 Agent 分派、结果汇总；Subagent 专注执行被交付的子任务。

```
Orchestrator → [分解任务] → Subagent A / Subagent B / Subagent C
                    ↑                    ↓
              [汇总结果] ← [子任务完成] ←┘
```

**适用场景**：任务可层次分解为相互独立的子任务，每个子任务有清晰的输入输出边界。

**笔者认为**：这是目前最被滥用的模式。团队看到「Orchestrator」这个词就觉得高大上，结果把一个本该由单个 Agent 完成的任务强行拆成 Orchestrator + 5 Subagent，大幅增加系统复杂度和 token 消耗。**任务边界清晰且子任务相互独立**是这个模式成立的前提，不满足则必然失败。

**已知局限**：Orchestrator 成为单点瓶颈和 context 中心；任务无法良好分解时不适用。

---

### 3. Agent Teams：团队协作模式

**结构**：多个 Agent 实例并行运行，各自在独立 context 中工作，通过 Team Lead 协调。适合**并行、独立、长期运行**的子任务。

```
Team Lead
  ├── Agent A (并行, 独立 context)
  ├── Agent B (并行, 独立 context)
  └── Agent C (并行, 独立 context)
```

**适用场景**：同一父任务下的多个子任务确实相互独立、需要长时间运行、且结果之间无紧密依赖。

**笔者认为**：Claude Code 的 Agent Teams 就是这个模式的应用。相比 Orchestrator-Subagent，Team Lead 不做任务分解（假设任务已经分解好了），而是做**协调和分发**。适合「已经知道要做什么，只是需要多个worker并行执行」的场景。

**已知局限**：独立 context 意味着 Agents 之间无法直接共享中间状态；跨 Agent 的数据依赖需要额外的状态管理层。

---

### 4. Message Bus：消息总线模式

**结构**：Agents 通过共享的消息总线进行通信，信息流向不固定，任何 Agent 可以发布消息，任何 Agent 可以订阅。

```
Agent A ──→ [Message Bus] ←── Agent B
                ↑
                └── Agent C
```

**适用场景**：信息流拓扑复杂（非树形结构）、多个 Agents 需要异步响应事件、需要动态改变通信关系。

**笔者认为**：这是最灵活但也是最容易失控的模式。Message Bus 解决了「谁该告诉谁」的问题，但引入了新的问题——**消息 schema 演化、订阅关系的维护、以及调试时的消息溯源**。当系统规模增长时，Message Bus 的运维复杂度会显著上升。

**已知局限**：消息语义一致性需要严格的 schema 管理；系统可观测性（tracing）实现成本高。

---

### 5. Shared State：共享状态模式

**结构**：所有 Agents 读写一个共享的状态存储，状态是信息流的唯一 source of truth。

```
Agent A ──→ [KV Store / Shared State] ←── Agent B
                ↑
                └── Agent C
```

**适用场景**：多个 Agents 需要基于同一份上下文工作（代码库状态、任务看板、共享文档）；需要跨 Agent 的持久化和断点恢复。

**笔者认为**：这是最符合直觉但实现最复杂的模式。「共享状态」听起来简单，但**一致性保证、冲突解决、状态迁移**每一个都是分布式系统的经典难题。Shared State 模式的工程实现远不是「建个数据库」那么简单。

**已知局限**：状态一致性和冲突解决需要额外的工程投入；共享状态的粒度设计直接影响系统性能。

---

## 三问框架：选择协调模式的决策树

Anthropic 的五模式，本质上回答三个问题：

| 问题 | 回答方式 |
|------|---------|
| **在哪里切分 context？** | 每个 Agent 独立 context（Teams）、共享 context（Shared State via KV）、或通过消息传递（Message Bus） |
| **信息如何流动？** | 单向验证（Generator-Verifier）、树形分发（Orchestrator-Subagent）、广播（Message Bus）、共享读写（Shared State） |
| **系统何时停止？** | 验证通过（Generator-Verifier）、任务队列清空（Orchestrator-Subagent）、团队任务完成（Agent Teams）、无活跃消息（Message Bus）、状态达成目标（Shared State） |

**决策建议**：

```
任务是否需要显式质量门控？
  └─ 是 → Generator-Verifier
  └─ 否 → 子任务是否可独立分解？
              └─ 是 → 任务是否长期运行且并行？
                      └─ 是 → Agent Teams
                      └─ 否 → Orchestrator-Subagent
              └─ 否 → 信息流是否需要复杂拓扑？
                      └─ 是 → Message Bus
                      └─ 否 → Shared State
```

---

## 五模式的失败模式

| 模式 | 典型失败 |
|------|---------|
| Generator-Verifier | Verifier 标准模糊导致无意义的循环拒绝 |
| Orchestrator-Subagent | 任务分解粒度不当，Subagent 之间产生隐式依赖 |
| Agent Teams | Agents 独立 context 导致重复工作或状态丢失 |
| Message Bus | 消息 schema 演化后无向下兼容，系统级联失败 |
| Shared State | 状态竞争未处理，产生不一致的 Agent 决策 |

---

## 工程启示

1. **从 Generator-Verifier 开始**：最简单的模式验证任务是否适合 multi-agent，不要一开始就上 Orchestrator-Subagent。
2. **模式演进而非一步到位**：Anthropic 的建议是 watching where it struggles，然后演进到更复杂的模式。
3. **Shared State 是粘合剂**：当 Agents 需要协同但又不想引入 Message Bus 的复杂性时，Shared State（尤其是 KV Store）是最直接的方案。

---

## 关联项目

本文讨论的 Shared State 模式，对应一个真实的工程实现 → [nerudek/nats-agent-state-sharing](/articles/projects/nerudek-nats-agent-state-sharing-shared-state-pattern-10-stars-2026.md)：用 NATS JetStream KV 实现跨 Agent 共享状态，解决 400M token onboarding loop 的实际问题。

---

*本文是对 [Anthropic 官方博客](https://claude.com/blog/multi-agent-coordination-patterns) 的深度解读，所有模式分类和决策框架均来自该文。*