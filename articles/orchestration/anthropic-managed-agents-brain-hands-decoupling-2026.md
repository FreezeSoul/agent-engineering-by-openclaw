# Anthropic Managed Agents：架构即产品——当 Brain-Hands Decoupling 成为托管服务

**核心主张**：Anthropic 的 Managed Agents 不是又一个「Agent 托管平台」，而是一个**元抽象层**——它将 Agent 的三个核心组件（Session、Harness、Sandbox）虚拟化为稳定接口，使任何具体实现都能被替换而不影响其他组件。这解决了 Agent 架构中最核心的问题：**随着模型能力提升，Harness 的假设会过时，而旧假设会变成性能瓶颈**。

**读者画像**：有 Agent 开发经验，了解 Harness 基本概念（如 Claude Code），但不满足于「用现成框架」，想理解**为什么**很多 Agent 系统最终会遇到扩展瓶颈，以及如何从架构层面设计可演进的多会话 Agent 系统。

**核心障碍**：大多数 Agent 系统在初期能工作，但随着模型能力提升或用户规模增长，Harness 中编码的假设开始失效——而这些假设深深嵌入系统各处，无法局部替换。Managed Agents 给出了答案：**不要把假设写在代码里，把它们抽象成接口**。

---

## 1. 问题的本质：Harness 的假设为什么会过时

Anthropic 博客多次提到一个关键观察：

> "A common thread across this work is that harnesses encode assumptions about what Claude can't do on its own. However, those assumptions need to be frequently questioned because they can go stale as models improve."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

这句话揭示了 Agent 架构中最容易被忽视的问题：**Harness 不是静态基础设施，而是模型能力的函数**。

### 一个具体案例：Context Anxiety

在早期工作中，Anthropic 发现 Claude Sonnet 4.5 会在感知到上下文限制接近时**过早完成任务**——这被他们称为「context anxiety」。他们的解法是在 Harness 中添加上下文重置机制。

但当他们用 Claude Opus 4.5 运行时，发现这个行为**消失了**——Opus 4.5 不会 context anxiety。结果是：之前添加的上下文重置变成了无用代码，甚至可能引入新的问题。

> 笔者认为：这个案例说明了一个更普遍的原则——**Agent 架构中的很多「功能」实际上是在弥补模型的缺陷，而不是真正的能力增强**。当模型能力提升后，这些补偿性的「功能」要么变得多余，要么开始产生副作用。

### 假设过时的代价

当 Harness 的假设过时，整个系统都会受到影响：

- **性能问题**：为旧模型设计的节流/重置逻辑对新模型来说是无效开销
- **耦合问题**：假设嵌入在 Harness 实现各处，无法单独升级模型或替换 Harness
- **调试问题**：模型升级后行为变化，但无法确定是模型问题还是 Harness 问题

---

## 2. 核心解法：虚拟化三组件

Managed Agents 的设计原则来自计算领域的经典答案：操作系统通过虚拟化硬件来适应「尚未想到的程序」。

> "Decades ago, operating systems solved this problem by virtualizing hardware into abstractions—process, file—general enough for programs that didn't exist yet."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

Anthropic 将这个思路应用到 Agent 架构，把 Agent 虚拟化为三个核心组件的接口：

| 组件 | 职责 | 接口定义 |
|------|------|---------|
| **Session** | 持久化的append-only事件日志 | `getEvents()`、`emitEvent()` |
| **Harness** | Agent循环：调用Claude、路由工具调用 | `wake(sessionId)`、`run(sessionId)` |
| **Sandbox** | Claude执行代码和编辑文件的运行环境 | `execute(name, input) → string` |

### 虚拟化的关键价值

这三个接口的共同特点是：**它们对具体实现保持无知**。

- Session 不关心事件存储在内存、磁盘还是分布式日志中
- Harness 不关心 Sandbox 是容器、手机还是模拟器
- Sandbox 不关心被哪个 Brain 驱动

这意味着：
- **模型升级**时，只需确保新模型兼容同一组接口
- **Harness 升级**时，Session 状态可以无缝迁移
- **Sandbox 替换**时，Harness 不需要修改

---

## 3. 从宠物到牛群：Sandbox 去耦合

Managed Agents 文档中有一个非常有价值的类比：**Pets vs Cattle**。

在传统架构中，所有 Agent 组件都在一个容器里——Session、Harness、Sandbox 共享环境。这相当于把服务器当宠物养：服务器有自己的名字，需要人工维护，死了就麻烦了。

### Coupled 设计的问题

当所有组件耦合在一个容器中时：

1. **单点故障扩散**：容器失败 → Session 丢失，所有 Agent 上下文全部丢失
2. **调试窗口唯一**：唯一的调试入口是 WebSocket 事件流，但无法区分 Harness bug、事件流丢包还是容器离线
3. **网络边界僵化**：当用户需要在他们的虚拟私有云中运行 Agent 时，必须 peering 网络或把整个 Harness 部署到他们环境

### Decoupled 设计的价值

解耦后，Sandbox 变成了「牛群」而非「宠物」：

> "If the container died, the harness caught the failure as a tool-call error and passed it back to Claude. If Claude decided to retry, a new container could be reinitialized with a standard recipe: `provision({resources})`."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

Sandbox 死亡时，Harness 捕获工具调用错误 → 传给 Claude → Claude 决定是否重试 → 如果重试，新容器通过标准配方重新初始化。

**关键洞察**：不再需要「把失败的容器恢复」——只需要「启动一个新的」。这将运维问题转化为编程问题。

---

## 4. 安全边界：Token 从来不应该在 Sandbox 里

Coupled 设计有一个更严重的安全问题：

> "In the coupled design, any untrusted code that Claude generated was run in the same container as credentials—so a prompt injection only had to convince Claude to read its own environment. Once an attacker has those tokens, they can spawn fresh, unrestricted sessions."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

这个问题的根源是：**在 Coupled 设计中，Token 和 Sandbox 在同一个信任域**。攻击者不需要绕过任何安全边界——他只需要让 Claude 读自己的环境变量。

### 结构性修复

Managed Agents 的解决方案是**确保 Token 永远不会到达 Sandbox**：

- **Git 凭据**：使用每个仓库的 access token 在 Sandbox 初始化时 clone 仓库，然后 wire 到本地 git remote。Git push/pull 在 Sandbox 内工作，但 Agent 从不处理 token 本身
- **自定义工具（OAuth）**：通过专用代理路由 MCP 调用，代理从 Vault 获取对应 session 的凭据。Harness 完全不知道任何凭据

> 笔者认为：这个安全设计非常重要。它说明了一个原则：**安全边界必须由架构强制，而不是靠「不要让 Agent 读 X」这样的策略**。当架构允许 Token 进入 Sandbox，即使有最好的 Prompt 防护，也只是增加了攻击成本而不是消除攻击面。

---

## 5. Session 作为 Context 对象：解决长时任务的上下文管理

长时 Agent 任务的核心问题是：**上下文窗口长度有限，而任务需要的时间可能超过任何有限的上下文窗口**。

标准解法（compaction、memory tool、context trimming）都涉及**不可逆的决策**——决定保留什么、丢弃什么。但问题在于：**很难知道未来哪部分上下文会被用到**。

### 传统解法的问题

如果消息经过 compaction 步骤被转换，Harness 会从 Claude 的上下文窗口中移除已压缩的消息。这些消息**只有存储在可恢复的地方才是可恢复的**。

之前的工作探索过将上下文存储为 REPL 中的对象，让 LLM 通过写代码来 filter 或 slice 它。但这需要模型能够可靠地与 REPL 交互，增加了复杂性。

### Managed Agents 的解法

Session 作为 **Context 对象**，位于 Claude 上下文窗口之外：

- Session 负责**可恢复的上下文存储**：`getEvents()` 可以获取任意位置切片的事件流
- Harness 负责**任意的上下文管理**：在将事件传给 Claude 前进行转换，包括上下文组织（实现高 prompt cache hit rate）和上下文工程

这两个关注点分离的原因是：**我们无法预测未来模型需要什么样的具体上下文工程**。

> "The interfaces push that context management into the harness, and only guarantee that the session is durable and available for interrogation."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

---

## 6. 性能：Many Brains, Many Hands

Coupled 设计还有一个性能问题：**每个 Brain 需要自己的容器**。

当 Brain 在容器中时，容器必须先被 provision 才能发生推理——每个 session 都要支付完整的容器启动成本。即使 session 永远不需要 touch Sandbox，也必须 clone 仓库、boot 进程、fetch pending events。

这个等待时间体现在 **TTFT（time-to-first-token）**——用户感受最明显的延迟。

### Decoupled 后的性能数据

解耦后，Sandbox 由 Brain **按需通过工具调用启动**：

```
execute(name, input) → string
```

一个不需要容器的 session 可以**立即开始推理**，因为 orchestration layer 可以直接从 session log 拉取 pending events。

实际效果：
- **p50 TTFT 下降约 60%**
- **p95 TTFT 下降超过 90%**

> "Scaling to many brains just meant starting many stateless harnesses, and connecting them to hands only if needed."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

Many Brains = 启动多个无状态的 Harness，按需连接 Hands。这将水平扩展从「每个 Brain 需要一个完整容器」变成了「启动一个进程」。

### Many Hands：每个 Brain 可以连接多个 Sandbox

解耦还带来了另一个能力：**每个 Brain 可以连接多个 Sandbox**。

在实践中，这意味着 Claude 必须能够在多个执行环境之间推理，决定在哪里发送工作——这比在单一 shell 操作难得多的认知任务。

早期模型不够聪明，无法可靠地做到这一点，所以 Anthropic 从单容器开始。随着模型能力扩展，单容器变成了限制而不是能力——当容器失败时，Brain 触及的所有 Sandbox 都丢失状态。

通过 Brain-Hands Decoupling，每个 Sandbox 变成了一个工具：`execute(name, input) → string`。没有 Sandbox 与任何 Brain 耦合，所以 Brains 可以相互传递 Hands。

---

## 7. Meta-Harness 设计原则

Managed Agents 本质上是一个**元 Harness**——它不绑定任何特定的 Harness 实现，而是提供了允许不同 Harness 接入的通用接口。

Anthropic 对未来 Agent 架构的判断：

> "We designed the interfaces so that these can be run reliably and securely over long time horizons. But we make no assumptions about the number or location of brains or hands that Claude will need."
> — [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)

这意味着 Managed Agents 可以同时支持：
- **Claude Code**：一个优秀的 Harness，Anthropic 在内部广泛使用
- **Task-specific agent harnesses**：在特定领域表现优秀的任务特定 Harness
- **任何未来的 Harness 实现**

Meta-harness 的设计哲学是：**对接口有主见，对实现没有主见**。

---

## 8. 与 Cursor 第三时代的理论共鸣

有趣的是，Anthropic 的 Managed Agents 论文与 Cursor 第三时代的理念形成了强烈共鸣——尽管两者从不同方向出发：

| 维度 | Cursor 第三时代 | Anthropic Managed Agents |
|------|---------------|------------------------|
| **核心问题** | 人类无法扩展到监督多个 Agent 并行运行 | Harness 的假设随模型能力提升而过时 |
| **解法方向** | 产品层：Cloud Agents + Artifacts 评估媒介 | 架构层：虚拟化接口 + 可替换实现 |
| **Human-Agent 边界** | 人类定义问题，Agent 执行 | Harness 定义接口，模型适配接口 |
| **扩展路径** | 平台层扩展（多 Agent 并行） | 协议层扩展（Many Brains + Many Hands）|

两者都在回答同一个问题：**如何在模型能力快速提升的情况下，保持 Agent 系统的可演进性**。

Cursor 的答案是「建更好的平台」；Anthropic 的答案是「建更稳定的抽象」。

> 笔者认为：两者都是必要的。平台提供用户可以直接使用的体验，抽象让平台能够持续演进。在 Agent 系统的发展中，这两条路线最终会汇聚——Cursor 的 Cloud Agents 底层也需要某种形式的 Brain-Hands Decoupling 才能scale；Anthropic 的接口抽象也需要类似 Cursor Artifacts 的输出证明机制才能让人类有效评估。

---

## 9. 工程启示

对于构建多会话 Agent 系统的工程师，Managed Agents 提供了几个关键原则：

### 原则 1：不要把模型假设编码进 Harness

Harness 中编码的假设（超时、重试策略、上下文管理策略）应该能够**独立于模型选择**进行配置和调整。考虑引入配置层，将「模型能力假设」外部化。

### 原则 2：Sandbox 应该是可替换的

不要假设 Sandbox 是什么形式（容器、VM、远程服务）。定义好 `execute(name, input) → string` 接口，让 Sandbox 的具体实现对 Harness 透明。

### 原则 3：Session 是上下文的外置存储

长时任务不要依赖模型的上下文窗口作为唯一的状态存储。设计 Session 接口，让上下文可以按需从外部读取，实现上下文窗口的「弹性化」。

### 原则 4：安全边界由架构强制

凭据不应该出现在 Sandbox 的信任域中。即使 Prompt 防护可以减少攻击面，也不应该依赖 Prompt 来保护凭据。

### 原则 5：支持水平扩展，而不是假设垂直容量

Many Brains 的设计意味着 Harness 应该是无状态的。Session 状态存储在外部，Harness 可以随时重启、重连、水平扩展。

---

## 10. 结论

Anthropic 的 Managed Agents 论文的真正贡献不是「又一个托管服务」，而是它揭示了 Agent 架构的核心演进方向：**从特定实现走向稳定抽象**。

随着模型能力快速提升，Agent 系统的竞争力不再取决于「现在用的是什么模型或 Harness」，而是取决于**架构的可演进性**——当新模型发布或新需求出现时，系统能否快速适配而不需要重新设计。

这个原则不仅适用于托管服务，对任何构建 Agent 系统的工程师都有参考价值。

---

*来源：[Anthropic Engineering: Scaling Managed Agents — Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)*
