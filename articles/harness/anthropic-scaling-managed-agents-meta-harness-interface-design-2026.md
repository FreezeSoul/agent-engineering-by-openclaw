# Anthropic Scaling Managed Agents 深度解析：Meta-Harness 设计范式

## 核心主张

Anthropic 2026 年 4 月发布的 Scaling Managed Agents 揭示了一个被大多数 Agent 框架忽视的关键洞察：**Harness 本质上是「尚不存在之程序」的构建方案**——而任何特定实现（无论是一个 Python 循环还是一组 MCP 服务器）都会在模型能力跃升时成为瓶颈。Managed Agents 的答案是将 Agent 分解为三个稳定的抽象接口：Session（持久化事件日志）、Harness（无状态控制平面）、Sandbox（可替换执行环境），让实现细节可以从接口下自由替换。这不是微服务拆分，而是操作系统虚拟化思想在 Agent 时代的首次系统应用。

---

## 问题：耦合的代价——Harness 成为「宠物」

Anthropic 最初将所有 Agent 组件塞进同一个容器：Session、Harness 和 Sandbox 共处一室。这带来了显而易见的问题：文件操作是直接的系统调用，不存在跨服务边界的设计负担。但代价同样清晰——**这个服务器变成了「宠物」**：容器崩溃意味着 Session 丢失，容器无响应时工程师必须 SSH 进容器内部调试，而容器内往往还存放着用户数据。

更隐蔽的是耦合对扩展性的限制。当团队希望 Claude 连接到客户自建的 VPC 时，唯一的选择是让客户的网络与 Anthropic 的网络建立对等连接——因为 Harness 假设每个资源都「坐在它旁边」。这个假设从第一天起就被刻进了架构里。

笔者认为，这里暴露了大多数自建 Harness 的共同盲区：**我们在设计 Harness 时默认了共置（co-location），却从未质疑这个假设**。当模型能力提升，这些假设会以「配置变更」的形式反咬你一口。

---

## 解法：虚拟化组件，接口凌驾于实现之上

Managed Agents 的解法借鉴了操作系统的经典思路。几十年前，操作系统通过将硬件虚拟化为通用抽象（进程、文件描述符）来解决「为尚未出现的程序设计系统」的问题。`read()` 系统调用不关心底层是 1970 年代的磁盘组还是现代 SSD。

Anthropic 将这个思路移植到 Agent 架构：虚拟化 Agent 的三个核心组件——Session（append-only 事件日志）、Harness（调用 Claude 并路由工具调用的循环）、Sandbox（Claude 运行代码和编辑文件的执行环境）。每个组件都是**只有最少假设的接口**，可以独立失败或被替换。

> "We designed the interfaces so these can be run reliably and securely over long time horizons. But we make no assumptions about the number or location of brains or hands that Claude will need."
> — [Anthropic Engineering: Scaling Managed Agents](https://anthropic.com/engineering/managed-agents)

这意味着：无论未来的 Claude 需要什么形态的 Harness、Sandbox 或其他组件，当前设计的接口都能承接。接口是稳定的，实现是流动的。

---

## 核心设计：Brain-Hands 解耦

### 从「脑在箱中」到「脑调用箱」

解耦的核心动作是：**让 Harness 离开容器**。Harness 不再存在于容器内部，而是通过一个极简接口调用容器：

```
execute(name, input) → string
```

一个名字 + 输入进去，一个字符串返回。Harness 不需要知道另一端是容器、远程服务、MCP 服务器还是客户 VPC 内的工具环境。它调用动作，获取结果，仅此而已。

这带来了一个根本性的范式转换：**容器变成了「cattle」而非「pet」**。如果容器死了，Harness 将失败捕获为工具调用错误，传回给 Claude。Claude 决定重试时，新的容器可以用标准配方重新初始化：`provision({resources})`。不再需要「把失败的容器护理回来」。

同样地，Harness 本身也变成了 cattle。因为 Session 日志独立于 Harness 而存在，Harness 崩溃时，新的 Harness 可以用 `wake(sessionId)` 启动，调用 `getSession(id)` 获取事件日志，从最后一个事件恢复执行。Harness 不需要存活下来才能恢复工作。

### 安全的结构性修复

在耦合设计中，Claude 生成的任何不受信任的代码都运行在存放凭证的同一容器内——一次 Prompt 注入只需说服 Claude 读取自己的环境就能获取令牌。Anthropic 的结构性修复方案是：**确保令牌永远无法被 Claude 生成代码执行的沙箱触及**。

两个模式：
1. **Git 认证**：使用每个仓库的访问令牌在沙箱初始化期间克隆仓库，并将其接入本地 git remote。Git push 和 pull 在沙箱内部正常工作，而 Agent 从不接触令牌本身。
2. **MCP OAuth**：OAuth 令牌存储在沙箱外的安全 Vault。Claude 通过专用代理调用 MCP 工具；代理持有与会话关联的令牌，从 Vault 获取相应凭证后执行调用。Harness 完全不知道任何凭证的存在。

### Session：不是 Context Window

长时任务通常超过 Claude 的上下文窗口。常见的解决方案（压缩、Memory 工具、上下文修剪）都涉及对保留或丢弃什么的**不可逆决策**。

Anthropic 的方案是让 Session 充当一个存在于 Claude 上下文窗口之外的上下文对象。`getEvents()` 接口允许 Brain 选择事件流的任意位置切片：可以从上次停止的地方继续读取，可以在特定时刻前回退几格查看前置准备，也可以重读某动作前的上下文。任何获取的事件也可以在传入 Claude 上下文窗口前在 Harness 中转换——包括上下文组织（实现高 prompt cache 命中）和上下文工程。

这将「可恢复上下文存储」和「任意上下文管理」两个关注点分离了。因为无法预测未来模型需要什么特定的上下文工程，所以这个职责被推入 Harness，而 Session 只保证事件的持久化和可查询性。

---

## 性能跃升：懒 provisioning 带来的 TTFT 革命

当 Brain 最初在容器内时，很多 Brain 需要很多容器。每一个 Brain，在容器准备就绪前无法发生推理；每一个 Session，即使永远不会触碰沙箱，也必须克隆仓库、启动进程、从服务器获取待处理事件。

这个等待时间体现在 TTFT（Time-to-First-Token）上——即 Session 接受工作到产出第一个响应令牌之间的时间。这是用户感知最敏感的延迟指标。

将 Brain 从容器中解耦后，**容器由 Brain 通过工具调用按需 provision**：不需要容器的 Session 无需等待容器。推理可以在编排层从 Session 日志拉取待处理事件的那一刻立即开始。

使用这个架构后，Anthropic 的 p50 TTFT 下降了约 **60%**，p95 下降了超过 **90%**。扩展到很多 Brain 只需要启动很多无状态的 Harness，在需要时才将它们连接到 hands。

---

## Many Brains, Many Hands

解耦 Brain 和 Hands 解决了最早的客户投诉之一。当团队希望 Claude 使用客户自己 VPC 中的资源时，不再需要网络对等连接——因为 Harness 不再在容器内，每个资源不再假设「坐在它旁边」。

这个变化还带来了性能收益：当 Brain 在一个容器时，容器必须在会话开始时 provision。即使会话永远不需要沙箱，也必须支付完整的容器启动成本。解耦后，容器由 Brain 按需启动，推理与容器准备并行发生。

更重要的是，**Many Hands 架构**成为可能。Anthropic 最初将 Brain 放在单个容器内，因为早期模型没有能力管理多个执行环境。但随着模型能力提升，单个容器反而成为限制——当该容器失败时，Brain 连接到的每个 Hand 的状态都丢失了。

解耦后，每个 Hand 都是一个工具：`execute(name, input) → string`。这个接口支持任何自定义工具、任何 MCP 服务器和 Anthropic 自有的工具。Harness 不知道也不需要知道沙箱是容器、手机还是宝可梦模拟器。因为没有 Hand 耦合到任何 Brain，**Brain 可以将 Hands 互相传递**——一个 Brain 可以将工作委托给另一个 Brain，后者持有不同的执行环境。

---

## Meta-Harness 设计哲学

Managed Agents 实际上是一个 **Meta-Harness**：对特定 Harness 本身持中立态度，但对 Claude 周围的接口持明确立场。

Anthropic 的判断是：Claude 需要操作状态的能力（Session）和执行计算的能力（Sandbox）。Claude 还需要扩展到多个 Brain 和多个 Hands 的能力。这些接口应该能够长期可靠且安全地运行。但接口不关心 Brain 或 Hands 的数量或位置——那是实现细节。

> "Meta-harness design means being opinionated about the interfaces around Claude: we expect that Claude will need the ability to manipulate state (the session) and perform computation (the sandbox). We also expect that Claude will require the ability to scale to many brains and many hands."
> — [Anthropic Engineering: Scaling Managed Agents](https://anthropic.com/engineering/managed-agents)

这个哲学的核心是：**接口是稳定的，实现是脆弱的**。Harness 会过时，但接口可以设计得足够通用，以容纳尚未构想出的实现。这与操作系统处理「为尚不存在的程序设计系统」问题的方式完全相同。

---

## 与传统 Harness 设计的本质区别

自建 Harness 的典型问题是**假设耦合**：Harness、容器、凭证、文件系统、工具路由全部绑定在一起。当模型能力提升或业务需求变化时，这些耦合假设会以级联失效的方式反咬你。

Managed Agents 的核心教训是：**把 Agent 当作「程序」而非「进程」来设计**。进程与特定运行时绑定；程序只与稳定的 API 绑定。Claude Agent 的 Harness 是 Agent 的运行时——而这个运行时应该可以通过新的实现自由替换，只要接口语义不变。

笔者认为，这给所有正在构建 Agent 平台的团队提了一个醒：如果你的 Harness 代码里有任何「我知道 Claude 会怎么调用这个工具」的假设，这些假设正在积累技术债。模型能力提升的速度远超我们的预期，而耦合假设是第一批受害者。

---

## 总结

Anthropic Scaling Managed Agents 的核心贡献不是一个托管的 Agent 服务，而是一套**接口设计哲学**：

1. **Brain-Hands 解耦**：Harness 是控制平面，Sandbox 是可替换的工具。两者通过极简接口通信，独立失败和恢复。
2. **Session 作为外部化状态**：事件日志不绑定在任何容器或进程上，而是作为可查询的持久化对象存在于 Claude 上下文窗口之外。
3. **懒 provisioning**：推理与容器准备并行，TTFT 压缩的核心机制。
4. **Meta-Harness 立场**：对接口明确，对实现中立。让接口经受住未来模型能力跃升的考验。

如果你在构建 Agent 平台，核心问题不是「我用什么框架」，而是「我的接口设计能经受住接下来三次模型能力跃升吗」。

---

## 参考文献

- [Scaling Managed Agents: Decoupling the brain from the hands](https://anthropic.com/engineering/managed-agents) — Anthropic Engineering Blog, Apr 08, 2026
- [Building Effective AI Agents](https://anthropic.com/engineering/building-effective-agents) — Anthropic Engineering Blog
- [Effective harnesses for long-running agents](https://anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Anthropic Engineering Blog
- [Effective context engineering for AI agents](https://anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic Engineering Blog