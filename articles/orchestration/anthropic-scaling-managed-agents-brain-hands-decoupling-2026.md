# Anthropic Scaling Managed Agents：大脑与手分离的架构革命

> 本文解读 Anthropic Engineering Blog（2026-04-08）原文：[Scaling Managed Agents: Decoupling the brain from the hands](https://anthropic.com/engineering/managed-agents)
>
> 关联项目：[cft0808/edict — 三省六部多 Agent 编排系统](#关联项目)

---

## 核心命题

当一个 AI Agent 系统变得复杂，它的各个组件之间就开始产生耦合——harness 和 sandbox 挤在同一个容器里，session 和上下文窗口混在一起，某个组件的失败会导致整个系统瘫痪。

Anthropic 的解法来自一个 50 年前的智慧：**虚拟化**。

操作系统通过虚拟化硬件（进程、文件描述符）让上层抽象可以跨越硬件生命周期；Anthropic 用同样的思路虚拟化了 Agent 的三个核心组件——session、harness、sandbox——让它们各自独立演进、独立失败、独立替换。

这不是一个「更好的 Agent」，而是一个**可以容纳未来所有 Agent 类型的元框架（meta-harness）**。

---

## 一、从「宠物服务器」到「可替换牛」

Anthropic 最初把所有 Agent 组件塞进一个容器：session、agent harness、sandbox 共享同一个环境。

这带来了一个经典的基础设施问题——**他们收养了一只「宠物」**。

在「宠物 vs 牛」的理论里，宠物是需要手工维护的个体（named, hand-tended），而牛是可以随时替换的。在云原生时代，你应该养牛，而不是养宠物。但耦合设计让这个容器变成了那只宠物：

- **容器挂了，session 就丢了**——没有持久化，状态不可恢复
- **容器无响应时，工程师只能 SSH 进容器调试**——但容器里还存着用户数据，debug 等于侵犯隐私
- **容器里的 harness 假设所有资源都在它身边**——客户要接自己的 VPC，只能 peering 网络或把 harness 部署到客户环境

这不是工程上的疏忽，而是架构设计在复杂度面前的必然溃败。当所有东西耦合在一起，任何一个组件的失败都会级联到其他组件。

### 解法：组件解耦

Anthropic 的解法是把「大脑」（Claude + harness）和「手」（sandboxes、tools）以及「session」（事件日志）全部拆开，每个都是接口，对彼此只做最少的假设：

```
你 → session（持久化事件日志）→ harness（调用逻辑）→ sandbox（执行环境）
```

接口只有三个核心操作：

- `execute(name, input) → string` — brain 调用 hand
- `provision({resources})` — 按需初始化 sandbox
- `getEvents()` — brain 从 session 读取历史
- `emitEvent(id, event)` — 写入 session 记录

这个模式让实现可以替换而不影响接口。harness 不再需要知道 sandbox 是容器、手机还是游戏模拟器。

> **原文引用**：
> "We virtualized the components of an agent: a session (the append-only log of everything that happened), a harness (the loop that calls Claude and routes Claude's tool calls to the relevant infrastructure), and a sandbox (an execution environment where Claude can run code and edit files). This allows the implementation of each to be swapped without disturbing the others."

---

## 二、解耦带来的性能收益

解耦不只是架构好看，它直接带来量级的性能提升。

### 问题：容器预置成本

当 brain 在容器里，每个 session 都需要等容器预置好才能开始推理。这意味着：

- 每个 session，即使根本不需要 sandbox，也要等 `git clone` → 启动进程 → 获取待处理事件
- 这个等待时间体现在 **TTFT（time-to-first-token）** 上——用户最能感知的延迟

### 解法：按需初始化

解耦之后，sandbox 是通过 `execute()` tool call 按需调用的：

> "So a session that didn't need a container right away didn't wait for one. Inference could start as soon as the orchestration layer pulled pending events from the session log."

**结果**：

| 指标 | 解耦前 | 解耦后 | 提升 |
|------|--------|--------|------|
| **TTFT p50** | 基准 | 下降 ~60% | 6 折 |
| **TTFT p95** | 基准 | 下降 >90% | 原生 1/10 |

扩展到 many brains 只需要启动多个无状态的 harness，按需连接 hands——不再需要为每个 brain 预置一个容器。

> **原文引用**：
> "Using this architecture, our p50 TTFT dropped roughly 60% and p95 dropped over 90%."

---

## 三、安全边界：token 不在 sandbox 里

耦合设计还有一个隐蔽的安全问题：**credential 就躺在容器里**。

如果 prompt injection 攻击让 Claude 读取了自己的环境，攻击者就能拿到那些 token，然后启动新的 unrestricted session。

社区的标准解法是「窄范围 token」——给 token 加上最小权限限制。但 Anthropic 指出了这个思路的根本缺陷：

> "Narrow scoping is an obvious mitigation, but this encodes an assumption about what Claude can't do with a limited token—and Claude is getting increasingly smart."

模型越来越强，「Claude 做不到某件事」的假设会越来越不可靠。

### 解法：结构性隔离

Anthropic 的结构性解法是：**让 token 永远不在 sandbox 能触达的地方**。

两种模式：

1. **Auth bundled with resource**：认证信息和资源绑定在一起，不经过 agent
2. **Vault + Proxy**：token 存在 vault 里，通过 dedicated proxy 访问

以 Git 为例：

- 在 sandbox 初始化时，用 repo 的 access token clone 进来，wire 到 local git remote
- Git push/pull 可以在 sandbox 内工作，但 agent 从来不持有 token

这样即使 prompt injection 让 Claude 读取了自己的环境，也读不到任何 credential。

> **原文引用**：
> "The structural fix was to make sure the tokens are never reachable from the sandbox where Claude's generated code runs."

---

## 四、Session：上下文窗口之外的持久化

长程任务会超出 context window 的长度。标准解法——compaction、memory tool、context trimming——都涉及不可逆的决策：哪些 token 要保留，哪些要丢弃。

Compaction 的问题尤其微妙：compaction 后的消息从 Claude 的 context window 里移除，但只有存储在 session log 里才可恢复。问题是，压缩后的消息已经被「消化」过了，再恢复出来的是摘要而非原文。

### 解法：Session 作为 Context 对象

Anthropic 把 session 设计成一个**存在于 context window 之外的持久化上下文对象**：

- Context 存在 session log 里，而不是 sandbox 或 REPL 里
- `getEvents()` 接口允许 brain 按位置切片查询事件流
- 可以从上次停止的地方继续读、往前回退几个事件看前置上下文、或在特定 action 前重读 context

更关键的是：**任何获取的事件可以在传给 Claude 之前先在 harness 里做转换**，包括：

- 上下文组织以提高 prompt cache hit rate
- 上下文工程（context engineering）

> "We separated the concerns of recoverable context storage in the session and arbitrary context management in the harness because we can't predict what specific context engineering will be required in future models."

这意味着 session 只负责「持久化 + 可查询」，而「如何管理 context」是 harness 的职责——两者各司其职，边界清晰。

---

## 五、Many Brains, Many Hands

解耦之后，另一个能力自然浮现：**一个 brain 可以连接多个 hands，反之亦然**。

### Many Hands：多执行环境

每个 hand 都是一个 tool：`execute(name, input) → string`。这个接口支持：

- 任何 custom tool
- 任何 MCP server
- Anthropic 自有的 tools

harness 不知道也不需要知道 hand 是什么类型。**没有 hand 耦合到任何 brain**，所以 brains 之间可以相互传递 hands。

这解决了一个 earlier 模型解决不了的问题：让 Claude 自己判断该把任务发到哪个执行环境。

### Many Brains：多脑编排

当 brain 离开容器之后，「很多 brains 需要很多容器」的假设也消失了。现在每个 brain 只是一个无状态的 harness，启动时调用 `wake(sessionId)` + `getSession(id)` 恢复事件流，然后继续上次的工作。

这意味着 **TTFT 不再受容器预置支配**——推理可以在 orchestration layer 获取待处理事件后立即开始。

---

## 六、Meta-harness 设计哲学

Managed Agents 不是为一个特定的 harness设计的——它是一个**系统，设计目标是容纳未来的 harnesses、sandboxes 和其他组件**。

Anthropic 的设计哲学是：

> "We are opinionated about the shape of these interfaces, not about what runs behind them."

对接口 shape 有意见（opinionated），意味着：
- Claude 需要操作 state（session）和执行 computation（sandbox）——这是固定的
- Claude 需要 scale 到 many brains 和 many hands——这也是固定的
- 但 brain 或 hand 的数量、位置、类型——这些是不限制的

对实现 behind the interfaces 没意见，意味着：
- Claude Code 是一个 harness，Managed Agents 可以容纳它
- 任务特定的 harness 也可以被 Managed Agents 容纳
- 未来的任何 harness，只要符合接口契约，就能接入

> **原文引用**：
> "Managed Agents is a meta-harness in the same spirit, unopinionated about the specific harness that Claude will need in the future."

---

## 七、工程启示

Anthropic 这篇文章的核心贡献不是某个具体实现，而是**把 OS 虚拟化思想系统性地引入 Agent 工程**：

| 概念 | 操作系统 | Anthropic Managed Agents |
|------|---------|--------------------------|
| 虚拟化对象 | 进程、文件描述符 | Session、Harness、Sandbox |
| 接口设计 | read()/write() 抽象 | execute()/provision()/getEvents() |
| 抽象稳定性 | 上层接口跨硬件代际 | 接口契约容纳未来 harness |
| 解耦收益 | 硬件独立性 | TTFT -60%/-90% |
| 安全模型 | 权限隔离 | Token vault + structural isolation |
| 故障恢复 | 进程重启不丢状态 | Harness crash → 新 harness + session 恢复 |

对于构建生产级 Agent 系统，Anthropic 的实践指向几个关键原则：

1. **不要把任何东西做成宠物**：session、harness、sandbox 任何一者挂了都不应该导致其他组件不可恢复
2. **安全边界靠结构不靠假设**：模型会越来越强，「模型做不到某件事」的假设会越来越不可靠，结构性隔离比范围限制更可靠
3. **上下文管理权和持久化存储权要分离**：不知道未来需要什么 context engineering，就把管理权推给 harness，持久化权留在 session
4. **Meta-harness 优于专用 harness**：接口设计要对未来 harnesses 友好，不要假设只有一种 harness 会被使用

---

## 关联项目

### [cft0808/edict — 三省六部多 Agent 编排系统](#)

如果说 Anthropic 的贡献是把「大脑与手分离」应用到单个 Agent 的架构层面，那么 **edict** 的贡献是把同一思想应用到**多 Agent 组织的治理层面**。

edict 用中国唐代三省六部制度构建了一个多 Agent 协作框架：太子分拣、中书省规划、门下省审核封驳、尚书省派发、六部并行执行。与 CrewAI、AutoGen 相比，核心差异在于**制度性审核**：门下省专职审查规划质量，不合格方案直接打回重做，而不是可选的 human-in-the-loop。

这与 Anthropic 文章中的设计哲学高度一致——Anthropic 把 session 设为强制性的持久化层（"no session survives without the log"），edict 则把 review 层设为强制性的质量关卡（"every instruction must pass through 门下省"）。两者都在架构层面内置了质量保障机制，而非依赖事后检查。

edict 的另一层价值在于**完整的可观测性**：12 个 Agent 的状态、心跳、任务流转全部实时展现在军机处看板上。这解决了多 Agent 系统的一个核心痛点——当任务在多个 Agent 之间流转时，人类难以知道当前卡在哪里、谁在处理什么。Anthropic 用 `getEvents()` 接口让 harness 可以查询 session，edict 则用看板让人类可以实时监控整个流程。

---

*原文引用来源：Anthropic Engineering Blog，2026-04-08，作者 Lance Martin、Gabe Cemaj、Michael Cohen*