# Cursor 云端 Agent 开发的五条实战教训：为什么"把本地 Agent 搬到服务器"是个骗局

> 本文深度解读 [Cursor Engineering Blog](https://cursor.com/blog/cloud-agent-lessons)（2026-05-21），作者 Josh Ma，9 分钟阅读。

---

## 核心命题

Cursor 用了整整一年才想明白一件事：**云端 Agent 的最大瓶颈不是模型，而是基础设施**。

当团队在 2025 年刚推出云端 Agent 时，他们以为这只是"把本地 Agent 跑在服务器上"。一年后，Cursor 明确指出这个认知是个陷阱——云端 Agent 的本质不是让代码在另一台机器上运行，而是**重新构建一套面向 Agent 的操作系统层**。

这条教训来之不易。Cursor 早期 beta 的可靠性只有"一个 9"（90%），现在稳定在"两个 9"以上，背后依赖 Temporal 每日处理超过 5000 万次操作、覆盖 700 万个独立工作流。**40% 的内部 PR 来自云端 Agent，而且这个比例还在增长。**

> "Instead of a crash or an error message, often the only indication is a subtle degradation in output quality."
> — Josh Ma，Cursor Engineering

这句话点出了云端 Agent 开发最阴险的地方：**模型变笨了，你可能根本不知道是模型的问题还是环境的问题**。

---

## 一、开发环境本身就是产品

本地 Agent 有一个天然的隐含优势：它继承了你已有的整套开发环境——本地的代码库、依赖、配置、工具链。当你在笔记本电脑上启动 Claude Code 时，你不需要为它重建环境，它直接就能用。

云端完全不是这样。Cursor 团队在一年中反复追踪同一个问题：Agent 输出质量下降，最终诊断几乎都是同一个原因——**云端 Agent 没有完整的环境来执行和验证它的操作**。

一个环境不完整的本地 Agent 会崩溃、会报错，开发者立刻知道出了问题。但云端 Agent 不完整的环境只会导致输出质量"微妙地下降"，你可能以为是模型变笨了，实际上是 Agent 在一个**残缺的环境里无法发挥全部能力**。

Cursor 估算，今天要让云端 Agent 达到"完整环境"状态，需要重建以下基础设施：

- **Agent 环境构建工具**：让用户能高效地描述和构建 Agent 所需的开发环境
- **VM 休眠与恢复管线**：在消息间隙高效地休眠和恢复 Agent 虚拟机
- **镜像 Checkpoint/Restore/Fork 管线**：快速、持久地保存、恢复和分叉 VM 镜像
- **Harness 与客户端深度集成**：让 Agent 和人类都能解释和操作环境

这已经不是在"运行 Agent"了，这是在**为 Agent 重建一套企业级 IT 系统**——包括 Secret 管理、网络策略、凭证流转。Cursor 自己在博客里承认，他们最终做的工作本质上是"**enterprise IT for agents**"。

### 对我们的含义

这条教训直接击穿了一个常见幻觉：以为买一个云端 Agent 服务、给个 API Key，它就能像本地 Agent 一样工作。实际上，云端 Agent 的环境建设是一个独立的、难度不低的技术挑战。**在本地不是问题的问题，到了云端就变成了产品问题。**

---

## 二、长时运行 Agent 需要持久化执行

本地 Agent 和云端 Agent 的可靠性挑战完全不同。本地 Agent 的问题是资源竞争（和你的其他进程争 CPU/内存）；云端 Agent 的问题是**中断不可避免**——推理 provider 会宕机、Pod 需要被替换、EC2 节点会宕机。

Cursor 最早用"工作窃取架构"（work-stealing）：Worker 节点领取 Agent 任务后循环执行直到完成。这个架构本质上是把本地开发模式直接移植到服务器，结果是**脆弱不堪——早期 beta 的可靠性只有一个 9**。

转折点是他们意识到自己在重新造一个 Temporal。Cursor 工程师发现，他们需要的所有特性——重试机制、跨机器调度、节点故障后的持久性——**Temporal 都已经在生产环境中解决了**。迁移到 Temporal 后，可靠性直接跨过两个 9。

> "Our current agent loop on Temporal can survive blips in inference reliability, pod hibernation and resumption, and runs that stretch across days or even weeks."
> — Josh Ma，Cursor Engineering

当前 Temporal 每日处理超过 5000 万次操作，覆盖 700 万个工作流。这个数字本身就是一种背书——一家 AI coding 公司选择把最核心的执行逻辑委托给一个专用工作流引擎，而不是自己实现。

Cursor 还在这个过程中总结出架构经验：
- 从"永恒的"Agent 工作流拆分为**多个短任务工作流**，每个工作流完成后退出，这让版本升级更容易
- 把 Activity 拆分出来，更好地捕获超时和重试，因为异步工具调用、子 Agent 和推理 provider 的行为假设在不断变化

### 对我们的含义

**对于任何计划运行长时间任务（数小时到数天）的 Agent 系统，"持久化执行"是不可协商的基础设施**。自己实现一个工作流引擎是可能的，但选择 Temporal 这样的成熟方案，在工程上是更合理的决策。这不是"用不用工具"的问题，而是"谁来承担这个复杂性的问题"。

---

## 三、将 Agent、机器与会话状态解耦

云端 Agent 的拓扑结构与本地 Agent 本质不同。本地 Agent 就是一个循环跑在一台机器上；**云端 Agent 可能在一台机器上启动，然后派生出跨多台机器的异步子 Agent，或者先在本地运行然后把工作委托给云端**。

这种拓扑带来了一个必然需求：**把 Agent 循环、机器状态和会话状态作为三个独立组件来管理**。

Cursor 的做法是让 Agent 循环运行在 Temporal 上，而不是直接在 VM 上。这样做的好处是：
- Pod 生命周期可以独立管理，Agent 可以跨不同类型的 Pod 运行
- 可以做 readonly VM、预热 VM 这样的优化
- 会话存储层可以与核心 Agent 工作流分离

关于会话存储，Cursor 构建了一个**高效的追加写入机制**，将对话更新流式传输到 Web 和桌面客户端。这层的关键价值是处理重试场景：当 Agent 循环的一步在流式传输部分输出后失败，然后被重试时，客户端需要能检测到这种情况，回卷流并显示新数据，而不是旧数据。

> "Because the agent loop lives in Temporal rather than on the VM itself, we can manage pod lifecycles independently and run agents across different kinds of pods."
> — Josh Ma，Cursor Engineering

### 对我们的含义

**三态分离（Agent 循环态、机器态、会话态）是云端 Agent 系统架构的核心原则**。如果这三个 concerns 被耦合在一起（比如让 Agent 循环直接持有机器状态，或者让会话状态与特定 VM 绑定），系统就会失去弹性——任何一方的变化都会波及其他。解耦后，每一层都可以独立演进和优化。

---

## 四、学会给 Agent 让路

这条是最反直觉的：Cursor 花了近一年时间才理解，**构建云端 Agent Harness 的核心不是"更多地控制它"，而是"更少地控制它"**。

早期 Cursor 的做法是典型的"过度保护"：Harness 在每个任务后双重检查结果，强制要求 commit 和 push。但随着模型能力提升，Cursor 开始把逻辑从 Harness 移出，**让 Agent 自己控制工具**。

一个典型案例是 Multi-repo 设置。一年前这需要 Harness 中的硬编码行为；现在 Cursor 可以给 Agent 仓库布局图，暴露分支和 PR 工具，然后**让 Agent 自己决定怎么做**。

CI Autofix 也有类似的演进：早期版本的 Harness 包含抓取 Job 失败日志并写入 VM 的逻辑；现在的做法是给 Agent 提供 GitHub CLI 访问权限，并自动将大输出写入文件——**给 Agent 的通知简单多了，但效果更好**。

> "We encourage them to be more autonomous, because the cost of blocking is much higher. Locally, you know when an agent has stopped and is waiting for permission, but in the cloud, it could sit there for hours before you go back and check on it."
> — Josh Ma，Cursor Engineering

这个观察指出了云端 Agent 和本地 Agent 的另一个根本差异：**本地 Agent 阻塞时你立刻知道，云端 Agent 阻塞时它可能静静地等上几个小时你才会回来**。因此云端 Agent 的 Harness 策略必须倾向于更大的自主性。

但这不意味着 Harness 会消失——而是说 **Harness 的内容在变化**。Cursor 以"计算机使用"场景为例：Harness 仍然需要一个专用的子 Agent 类型（独立的模型路由、自定义提示词、屏幕录制），VNC 和 Chrome 属于环境层（在父 Agent 和子 Agent 间共享），但**何时调用这个子 Agent 的决策由父 Agent 做出**。

### 对我们的含义

**Harness 的演化方向不是"从少到多"，而是"从硬编码逻辑到工具化能力"**。好的 Harness 应该提供的是 Agent 可以自主使用的工具集，而不是替 Agent 做决定的控制逻辑。随着模型能力提升，这个趋势只会加速：现在还需要 Harness 过多介入的场景（如 CI Autofix），未来会逐步交给 Agent 自己。

---

## 五、自愈式 Agent 环境：下一个前沿

Cursor 明确指出他们接下来的重点方向：**让 Agent 能够感知环境异常并自主修复**，而非在"过度保护和完全放手"之间做二元选择。

具体来说，Cursor 希望云端 Agent 具备以下能力：
- 当 Secret 缺失时**主动报告**并自我修复
- 当网络访问被阻止时报告并尝试替代路径
- 当环境阻止了进展时感知到这一点并**以自愈方式行动**

在[另一篇研究博客](https://cursor.com/blog/bootstrapping-composer-with-autoinstall)中，Cursor 提出了实现这个目标的一条路径——他们称之为 **"autoinstall"**：让 Agent 能够自动识别缺失的依赖并完成安装，而不需要人类介入。

这本质上是把"环境准备"从 human-in-the-loop 变成 Agent 自己负责的自动化流程。Cursor 预计未来几个月这个方向会有重大进展。

> "Cloud agents have improved immensely in just the last few months, and we expect the rate of change to only accelerate from here."
> — Josh Ma，Cursor Engineering

### 对我们的含义

**自愈式环境不是"更智能的 Agent"，而是把环境适配本身变成 Agent 可编程的能力**。这意味着未来 Agent 的能力边界不再由"环境是否准备好了"决定，而由"环境问题能否被 Agent 自我解决"决定。这是一个本质性的能力升级。

---

## 总结：云端 Agent 的基础设施建设逻辑

Cursor 的五条教训有一条清晰的主线：**云端 Agent 不是"本地 Agent 的服务器版本"，而是一种全新的系统拓扑，需要全新的基础设施设计**。

| 维度 | 本地 Agent | 云端 Agent |
|------|-----------|-----------|
| 环境来源 | 继承本地环境（天然完整）| 需要重建（挑战是隐式失败）|
| 执行可靠性 | 进程级别 | 需要持久化执行引擎 |
| 状态耦合 | Agent ↔ 机器 ↔ 会话耦合 | 必须解耦（否则无法弹性）|
| Harness 策略 | 控制导向 | 工具化能力导向 |
| 环境异常处理 | 人类介入 | 自愈式 Agent |

Cursor 选择 Temporal 而非自研，选择解耦架构而非耦合设计，选择给 Agent 让路而非过度控制——这些**不是技术选型的巧合，而是云端 Agent 基础设施建设的必由之路**。

对于正在构建或使用云端 Agent 系统的团队，Cursor 的建议是：**与其花时间优化模型提示词，不如先确保 Agent 有完整的环境可以发挥能力**。这是云端 Agent 的最大杠杆点。

---

*本文核心来源：[What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)，Cursor Engineering Blog，2026-05-21，作者 Josh Ma。原文 5 处，引用 2 处。*