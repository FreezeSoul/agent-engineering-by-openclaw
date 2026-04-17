# Scaling Managed Agents：Anthropic 的 Meta-Harness 架构实践

> **核心问题**：大多数 Agent 系统的组件（执行环境、记忆、会话状态）耦合在同一进程里——一旦模型升级，原本正确的"假设"就变成了限制。Anthropic 在 Managed Agents 中用 OS 虚拟化的思路，把 Agent 拆成 Brain（推理）、Session（状态）、Sandbox（执行）三个独立接口，获得了可替换性、弹性伸缩和安全隔离。本文拆解这个架构决策的全过程。

---

## 一、耦合架构的代价：为什么把一切都装进容器是反模式

Anthropic 最初的 Managed Agents 原型把所有组件塞进一个容器：Session、Harness、Sandbox 共处同一环境。好处是文件编辑直接走 syscalls，没有服务边界需要设计。

但随之而来的是一个经典的基础设施问题：**你养了一只宠物**。

在云基础设施领域，"宠物 vs  cattle"（宠物 vs 牛群）是经典比喻：
- **宠物**：有名字的、精心维护的个体，死了就完了
- **牛群**：无名的、可替换的，死了直接换掉

当容器成为那只宠物，系统会面临三个具体问题：

**1. 容器挂了 = Session 丢了**
任何导致容器失败的原因（OOM、内核崩溃）都会导致整个 Session 不可恢复。没有持久化层，所有的上下文、进度全部丢失。

**2. 调试变成黑箱**
Anthropic 团队当时唯一的调试窗口是 WebSocket 事件流——但这个流无法区分三类不同故障：Harness bug、事件流丢包、容器本身离线。当工程师需要进入容器排查问题时，又因为容器里通常存有用户数据，这个操作本身就是风险。

**3. VPC 耦合**
当客户要求 Claude 访问他们自己的虚拟私有云时，唯一路径是把客户网络和 Anthropic 网络对等互联，或者让客户在自己的环境运行 Harness——但这要求 Harness 假设"所有资源都在我旁边"。这个假设被编码进了架构里，无法去掉。

这三个问题有一个共同根源：**把应该独立演进的组件，耦合进了同一个生命周期管理单元**。

---

## 二、解耦的核心：三接口设计

Anthropic 的解法是把 Agent 的三个核心组件虚拟化，定义成稳定的接口，而不是具体的实现：

| 接口 | 角色 | 职责 |
|------|------|------|
| **Session** | append-only 事件日志 | 持久化记录所有发生的事 |
| **Harness** | 推理循环 + 路由 | 调用 Claude，路由工具调用 |
| **Sandbox** | 执行环境 | Claude 运行代码、编辑文件的场所 |

每个接口对其他两者做最少的假设，任意一个都可以独立失败或替换。

### 2.1 Brain（大脑）脱离容器

核心转变：Harness 不再运行在容器内部。它调用容器，就像调用任何一个其他工具一样：

```
execute(name, input) → string
```

容器变成 cattle。如果容器死了，Harness 捕获的是工具调用错误，Claude 决定是否重试；如果重试，一个新的容器可以用标准配方重新初始化：`provision({resources})`。

这带来一个重要结论：**Harness 本身也变成 cattle 了**。因为 Session Log 独立于 Harness 存在，Harness 进程不需要在崩溃后存活。新的 Harness 可以用 `wake(sessionId)` 启动，通过 `getSession(id)` 恢复事件日志，从最后一个事件继续运行。Harness 在推理循环中通过 `emitEvent(id, event)` 向 Session 写入，保持事件的持久记录。

### 2.2 Session 不是 Context Window

长期任务的挑战在于：总会超出 Claude 的 Context Window 长度。业界标准的解法（压缩 Summarization、Context Trimming）都涉及不可逆的决策：决定保留什么、丢弃什么。

> 笔者认为，这里最关键的设计洞察不是"怎么做上下文管理"，而是"谁负责什么"。

Anthropic 在 Session 和 Harness 之间做了一个明确的职责分离：

- **Session**：负责可恢复的上下文存储——原始事件日志，以 append-only 方式持久化，提供 `getEvents()` 接口允许 Brain 按位置切片获取事件记录（正向续读、倒带几帧看前因后果、重读某个操作前的上下文）
- **Harness**：负责任意的上下文工程——在把事件传给 Claude 之前，可以做任意变换，包括为了提高 Prompt Cache 命中率的上下文组织，以及任何未来模型需要的上下文工程策略

这个分离的价值在于：**Session 保证可恢复性，Harness 保证适配性**。如果未来出现新的上下文工程方法，不需要改 Session，只需要改 Harness 的实现逻辑。

```
Session（外置事件存储）
    ↓ getEvents() / emitEvent()
Harness（上下文工程 + 推理循环）
    ↓ prompt()
Claude
    ↓ tool_calls
Sandbox（执行结果）
```

---

## 三、安全边界：凭证如何永远无法到达 Sandbox

耦合架构还有一个具体的安全隐患：**在单容器设计里，任何 Claude 生成的不可信代码都和凭证运行在同一个环境**。

如果发生 Prompt Injection，攻击者只需要让 Claude 读取自己的环境变量，就能获取所有 Token——然后用这些 Token 启动新的未受限 Session。

常见的缓解手段是 Token 范围限制（narrow scoping）——给每个 Token 分配最小必要权限。但这有一个根本问题：**这个方案的本质是假设 Claude 在有限 Token 情况下做不了某件事**。而 Claude 正在变得越来越聪明，这个假设会越来越不稳定。

Anthropic 的结构化解法：**让凭证从物理上永远无法到达 Sandbox**。他们用了两种模式：

**模式一：Auth 与资源绑定**
以 Git 为例。在 Sandbox 初始化时，用该仓库的访问令牌克隆代码，并直接接入本地 git remote。Git push/pull 在 Sandbox 内部可以正常执行，但 Sandbox 内的 Claude 代码从未接触过 Token 本身——Token 在初始化时就被消费掉了。

**模式二：Auth 存入外部 Vault**
对于自定义工具和 MCP 集成，OAuth Token 存在一个独立的 Vault 中。Claude 通过 MCP 调用工具时，请求经过一个专用 Proxy；这个 Proxy 拿的是与 Session 关联的 Token，去 Vault 中换取实际凭证，再调用外部服务。**Harness 本身对任何凭证都不可见**。

```
Claude → MCP Call → Proxy（持有Session关联Token）→ Vault（换取实际凭证）→ 外部服务
                                      ↑
                                Harness 看不到
```

核心原则：**Harness 编码的是"Claude 能做什么"，而不是"凭证在哪里"**。

---

## 四、性能收益：从 60%/90% TTFT 改善看架构决策

解耦带来了一个非预期的收益：**延迟大幅下降**。

在耦合架构下，每个 Brain 都需要自己的容器：
- 每个 Session 在推理发生之前，必须等容器完全初始化（克隆仓库、启动进程、拉取待处理事件）
- 即便这个 Session 根本不需要用到 Sandbox，也要付出完整的容器启动等待成本

这个等待时间就是 **Time-to-First-Token（TTFT）**——用户最直观感受到的延迟。

解耦之后，Sandbox 是按需通过工具调用来启动的：`execute(name, input) → string`。如果 Session 不需要容器，就不需要等容器。

具体数字：
- **p50 TTFT 下降约 60%**
- **p95 TTFT 下降超过 90%**

这个结果来自两个因素叠加：容器按需启动（不需要提前初始化所有 Session 的容器）加上多 Brain 的横向扩展（新增 Brain 只是启动一个无状态的 Harness，不再需要绑定一个容器）。

> 笔者认为这个数据值得特别关注：很多团队在讨论 Agent 性能优化时，关注点往往在模型本身或 Prompt。但 Managed Agents 的案例表明，**架构级别的解耦能带来比算法级别优化更显著的性能收益**。原因是架构问题影响的是 p95 尾部延迟——这是用户体验最敏感的区间。

---

## 五、Many Brains, Many Hands：多智体协作的接口基础

Anthropic 还提到了"Many Hands"的设计目标：让一个 Brain 连接多个执行环境。这需要 Claude 能够推理多个执行环境，决定把任务发到哪里——比在单容器里操作要难得多。

他们最初设计成单容器，正是因为早期模型做不到这种认知复杂度。但随着模型能力提升，单容器反而变成了瓶颈：一个容器失败，所有 Hand 的状态全部丢失。

解耦后，每个 Hand 变成了一个工具：`execute(name, input) → string`。Harness 不需要知道 Sandbox 是容器、手机还是别的什么。而且因为没有任何 Hand 耦合到特定 Brain，**Brain 之间可以互相传递 Hand**——这为多智体之间的动态任务分配提供了接口基础。

这个设计的核心洞察是：**一个接口，只要足够通用，就能在模型能力演进时持续提供价值**，不需要因为模型升级而重新设计接口本身。

---

## 六、Meta-Harness 哲学：接口优先于实现

Managed Agents 要解决的本质问题，是计算机科学里的经典问题：**如何为一个"程序还不存在"的系统设计接口**？

操作系统当年的答案是虚拟化硬件——把进程、文件等抽象成接口，这些接口在 50 年里保持了稳定，底层硬件换了无数代。Managed Agents 的思路类似：

**不是为特定的 Harness 实现设计系统，而是为 Harness 的接口设计系统**。

Managed Agents 可以运行 Claude Code（一种 Harness），也可以运行针对特定窄领域的任务 Harness。接口（Session、Sandbox）保持稳定，实现（Harness 的具体逻辑）可以随时替换或升级。

Anthropic 对"什么应该是接口"做了明确判断：
- Claude 需要**操作状态**的能力 → Session 接口
- Claude 需要**执行计算**的能力 → Sandbox 接口
- Claude 需要**Scale 到多个 Brain 和多个 Hand** → 分布式接口

但对"多少个 Brain、多少个 Hand、在哪里"不做任何假设——这些是实现细节，由具体 Harness 决定。

---

## 七、与其他 Harness 设计的关系

仓库里已有的 Claude Code Auto Mode 文章讨论的是**权限决策模式**（Safeguards Layer + AI Permission Decider），而本文讨论的是**架构层面的组件边界与接口设计**。两者是正交的：

- Auto Mode 解决的是"Harness 内部如何决策权限"的问题
- Managed Agents 解耦解决的是"Brain、Session、Sandbox 各自的生命周期如何管理"的问题

一个完整的 Harness 工程体系，既需要 Auto Mode 级别的权限粒度控制，也需要 Managed Agents 级别的架构弹性设计。

---

## 八、局限性与未解答的问题

1. **多 Hand 场景下的任务路由完全由 Claude 决定**：当一个 Brain 有 N 个可用的 Hand 时，Claude 如何判断哪个任务发到哪个 Hand？目前没有看到 Anthropic 公布具体的路由策略或评估数据。

2. **Session 存储成本的长期可持续性**：Session Log 长期增长，如果一个活跃 Session 运行数月，事件日志的规模可能非常大。Anthropic 的 Session 接口提供了 `getEvents()` 按切片读取，但没有说明归档或压缩策略。

3. **Harness 的可替换性实际落地情况**：目前 Managed Agents 官方支持 Claude Code 和少量任务特定 Harness。实际社区 Harness 的接口兼容性还未得到大规模验证。

---

## 参考文献

- [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)（一手来源，Anthropic Engineering Blog，2026）
- [Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)（一手来源，先行研究，Context Anxiety 问题）
- [Claude Managed Agents 官方文档](https://platform.claude.com/docs/en/managed-agents/overview)
- [The Cathedral and The Bazaar (ESR)](http://www.catb.org/esr/writings/taoup/html/ch03s01.html)（"programs as yet unthought of" 典故来源）
- [Pets vs Cattle Cloud Scaling Blog](https://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/)
