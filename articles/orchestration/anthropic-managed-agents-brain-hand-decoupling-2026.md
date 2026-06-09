# Anthropic Managed Agents：把操作系统思想引入 Agent 架构

> 本文解读 Anthropic Engineering Blog 文章 —— "Scaling Managed Agents: Decoupling the brain from the hands"
> 原文：https://www.anthropic.com/engineering/managed-agents

---

## 核心命题

Anthropic 在构建 Managed Agents 时，做了一件反直觉的事：把 decades-old 的操作系统虚拟化思想引入 Agent 架构。

这不是在已有系统上打补丁，而是从第一性原理出发，重新思考"当模型能力快速演进时，Agent 系统的哪些部分应该稳定，哪些部分应该可以替换"。答案是：接口稳定，实现灵活——如同 `read()` 不关心底层是磁盘还是 SSD，Managed Agents 的接口不关心 harness 是 Claude Code 还是其他实现。

**这篇文章要回答的问题是**：当模型能力每隔几个月就发生质变时，如何设计一个能持续演进而无需重写的 Agent 基础设施？

---

## 从"养宠物"到"养牛"

Anthropic 的第一个架构版本，把所有组件塞进同一个容器：session、harness、sandbox 全都共享环境。好处是文件编辑是直接 syscall，没有服务边界需要设计。

坏处是：他们"领养了一只宠物"。

在 pets vs. cattle 的经典类比里，宠物是 named、hand-tended、不可失去的个体；牛则是 interchangeable 的。在他们的场景里，那台服务器就是宠物——容器一挂，session 就丢了；容器一卡，就得手动干预恢复。

**笔者认为，这个 pet problem 是大多数自建 Agent 系统的必经陷阱**：一开始图省事耦合在一起，之后为每个故障节点单独打补丁，最终系统变成一座脆弱的宠物屋。

他们的解法是把三个组件彻底解耦：

- **Brain**：Claude + harness（控制循环）
- **Hands**：sandbox（代码执行、文件编辑等动作执行环境）
- **Session**：append-only event log（持久化的事件记录）

每个组件只通过少量接口交互，接口不关心对方内部实现，任一方故障或替换都不影响其他方。

---

## 接口设计：execute(name, input) → string

解耦的关键，是一个极简的调用接口：

```
execute(name, input) → string
```

Brain 调用 sandbox，就像调用任何一个工具一样。sandbox 返回一个字符串。不关心 sandbox 是容器、手机，还是某种模拟器。

这个设计解决了两类问题：

**1. 容器故障不再是灾难**

容器死了，harness 捕获到的是一次工具调用错误。Claude 看到错误，自主决定是否重试。如果重试，新容器用标准配方初始化：`provision({resources})`。不再需要手动" nursing failed containers back to health"。

**2. Harness 本身也可以是 cattle**

因为 session log 独立于 harness 存在，harness 不需要保存任何状态。harness 挂了？重启一个，用 `wake(sessionId)` 恢复，用 `getSession(id)` 拉取 event log，从上次中断的位置继续。harness 在 emitEvent(id, event) 写入 session，保持 durable record。

> 原文："When one fails, a new one can be rebooted with wake(sessionId), use getSession(id) to get back the event log, and resume from the last event."

**笔者认为，这个设计值得所有长时运行的 Agent 系统借鉴**：把"状态"从 harness 驱逐出去，让它变成 stateless 的编排层。状态只在 session log 里，而 session log 是 durable 的。

---

## 凭证隔离：结构上杜绝 prompt injection

传统耦合架构的另一个安全隐患：Claude 生成的不可信代码和 credentials 在同一个容器里运行。prompt injection 攻击只需要说服 Claude 读取自己的环境变量，就能拿到 token。

常见的缓解手段是"narrow scoping"——缩小 token 权限。但 Anthropic 指出了这个方法的问题：**它建立在"Claude 无法用受限 token 做坏事"的假设上，而 Claude 正在变得越来越聪明**。

结构上的解法是：**让 token 永远不可达 sandbox**。

他们用了两层模式：

- **Git 凭证**：每个仓库的 access token 在 sandbox 初始化时注入本地 git remote，push/pull 都在 sandbox 内工作，但 agent 永远不接触 token 本身
- **MCP 工具的 OAuth**：token 存在 vault 里，Claude 调用 MCP 工具时走 dedicated proxy，proxy 从 vault 取 credentials 对接外部服务，harness 永远不知道任何 credentials

> 原文："The structural fix was to make sure the tokens are never reachable from the sandbox where Claude's generated code runs."

**笔者认为这个设计原则超越了安全本身**——它示范了什么叫"接口即权限边界"。不靠政策规定 agent 不能做什么，而在架构上让"不能做"变成物理上的不可能。

---

## 性能收益：60% / 90% 的 TTFT 改善

解耦的直接收益体现在延迟上。

原来每个 session 启动时，无论是否需要 sandbox，都要等待容器完全初始化：clone repo、boot process、fetch pending events。TTFT（time-to-first-token，即用户感受到的首次响应延迟）被这些"死时间"拉高。

解耦后，容器按需启动：Brain 通过 `execute(name, input)` 按需调用 sandbox，不需要的 session 跳过容器等待，直接从 session log 取 pending events 开始推理。

结果：
- **p50 TTFT 降低约 60%**
- **p95 TTFT 降低超过 90%**

> 原文："Using this architecture, our p50 TTFT dropped roughly 60% and p95 dropped over 90%."

**笔者认为这个数字值得深思**：一个架构决策（按需初始化 vs. 预热所有组件）产生了如此量级的延迟收益，说明大多数 Agent 系统的 TTFT 问题不是模型推理慢，而是架构设计导致的等待。

---

## Many brains, many hands

解耦还解锁了一个新能力：**多 brain 共用一组 hands**。

在单容器架构里，一个 brain 故障意味着所有它正在操作的 hands 状态全丢。解耦后，hands 是独立的工具接口，brains 可以互相传递 hands 的引用——一个 brain 可以把某个执行环境交给另一个 brain，继续操作。

这对企业场景尤为重要：当 Claude 需要同时操作多个 VPC 资源时，不需要每个 brain 都配一套完整的环境，而是可以动态路由到已有的 hand 上。

---

## Meta-harness：接口即宪法

Managed Agents 的本质是一个 **meta-harness**——一个不预设具体 harness 实现的系统，只规定接口规范。Claude Code 是一个 harness，任务专属的 narrow agent 也是一个 harness，Managed Agents 都可以承载。

Anthropic 明确表示：**他们期望 Claude 的能力会持续演进，具体的 harness 实现会过时，但接口需要稳定**。这和 OS 设计完全一致——`read()` / `write()` 接口几十年不变，底层硬件换了无数代。

> 原文："Rather, it is a system with general interfaces that allow many different harnesses. For example, Claude Code is an excellent harness that we use widely across tasks."

**笔者认为，这个"meta-harness"思路，是 Agent 系统架构的正确抽象层级**：不应该把 Claude Code 本身当作产品，而应该把 Managed Agents 的接口当作产品——Claude Code、Auto Mode、未来的新 harness 都是这个接口的不同实现。这样才能在模型能力快速演进的周期里，保护基础设施投资。

---

## 与 Dynamic Workflows 的闭环

这篇文章和上轮的 Claude Code Dynamic Workflows 形成了一个有趣的对照：

- **Dynamic Workflows** 是模型主导的编排——模型自主规划任务、分解为数百个并行 subagent、Generator-Evaluator Loop 验证
- **Managed Agents** 是基础设施层面的编排——Brain（harness）和 Hands（sandbox）分离，Session 作为持久化上下文，支撑模型在长时任务中的韧性

两者的共同命题是：**模型越来越自主，系统如何给模型提供稳定、可组合、有边界的工作环境？**

Dynamic Workflows 回答了"模型自主工作时内部怎么跑"，Managed Agents 回答了"平台如何承接模型的自主性同时保证可运维性"。这是同一问题的两个层次。

---

## 三条可复用的工程原则

1. **Pet → Cattle**：任何可能失败的组件，都应该设计成可替换的。不要让容器成为不可失去的宠物，让 harness 成为 stateless 的编排层
2. **Token 不可达 sandbox**：安全边界不是靠假设模型做不到什么，而是靠架构让"做不到"变成物理属性
3. **接口稳定，实现灵活**：设计接口时问自己——这个接口在模型能力发生质变后还能用吗？

---

## 结语

Managed Agents 不是一个新功能，而是一个架构宣言：Agent 系统的未来在于接口设计，而非具体实现。把 decades of OS engineering 的智慧引入 AI infrastructure，是一件正确但少有人做对的事。

**你目前在构建的 Agent 系统里，哪些组件是"宠物"，哪些应该变成"牛"？**

---

*来源：Anthropic Engineering Blog, "Scaling Managed Agents: Decoupling the brain from the hands" — https://www.anthropic.com/engineering/managed-agents*