# 长程 Agent 的三层工程架构：有限上下文、无持久状态与自我验证

> 作者：Addy Osmani's Blog，2026-04-28
> 原文：https://addyosmani.com/blog/long-running-agents/
> 标签：#harness #长程执行 #架构模式 #Anthropic #Cursor #Google

---

## 核心结论

长程 Agent 工程的核心挑战不是让模型「更聪明」，而是**把模型无法持久化的状态全部外部化**——从上下文窗口到文件系统，从会话日志到记忆库。三个壁垒（有限上下文、无持久状态、无自我验证）驱动了整个行业在 Harness 层的工程收敛。

**一句话记住**：如果模型在对话窗口里「失忆」了，那是 Harness 的问题，不是模型的问题。

---

## 1. 「长程」到底是三个不同的东西

「长程 Agent」这个词在 2026 年被用烂了，但实际讨论的可能是三个完全不同的工程问题：

| 类型 | 核心挑战 | 解决主体 |
|------|---------|---------|
| **长程推理**（Long-horizon reasoning） | 模型在多步依赖的任务中保持连贯性，走了弯路能倒退 | **模型能力**（主要） |
| **长程执行**（Long-running execution） | Agent 进程跑几小时/几天，中途故障要能恢复 | **Harness 工程**（主要） |
| **持久化主体性**（Persistent agency） | Agent 有跨会话的身份，积累偏好和记忆 | **记忆系统**（主要） |

现实生产系统三者同时存在，但解决路径完全不同。混淆这三个类型是大多数架构讨论效率低下的根源。

**行业趋势**：METR 的时间范围指标（TH1.1，2026 年初更新）显示，边界模型的 50% 可靠任务时长[大约每七个月翻一倍](https://metr.org/time-horizons/)。按这个曲线，2028 年前后边界 Agent 能完成「天」级任务，2034 年前后能完成「年」级任务。这个数字决定了今天该在哪个层次投入工程资源。

---

## 2. 三个壁垒：为什么 demo 能跑，生产就挂

AddyOsmani 梳理了行业共识，三个壁垒在任何长程 Agent 系统的 write-up 中反复出现：

### 2.1 有限上下文

即使 1M token 的上下文窗口也装不下 24 小时的任务。更关键的是 [Context Rot](https://addyosmani.com/blog/agent-harness-engineering/)——上下文窗口接近满载时，模型推理质量会持续下降，远在硬限制到来之前性能就已经开始恶化。

这不是靠换更大模型的窗口能解决的。

### 2.2 无持久状态

新会话从零开始。Anthropic 在[科学计算长程 Claude 论文](https://www.anthropic.com/research/long-running-Claude)里的描述是最清晰的版本：

> 「想象一个软件项目由轮换的工程师维护，每个新工程师来的时候对上一个班次发生的事毫无记忆。」

没有显式的持久化机制，每次交接都是生产力灾难。

### 2.3 无自我验证

模型在评价自己的工作时系统性地过度乐观。被问到「你完成了吗」，回答「是的」的频率远高于实际完成的比例。没有独立的验证信号，系统会在完成度只有 30% 的时候自信交付。

---

## 3. 行业解决方案对比

### 3.1 Ralph Loop：最低成本的可行方案

[Ralph Loop](https://ghuntley.com/ralph/)（Geoffrey Huntley 和 Ryan Carson 推广）本质上是一个 bash 脚本的循环：

```bash
while true; do
  TASK=$(jq -r '(.tasks[] | select(.status != "done") | .id)' prd.json)
  CONTEXT=$(cat task-context.md progress.txt)
  RESPONSE=$(claude --prompt "Task: $TASK\nContext: $CONTEXT")
  echo "$RESPONSE" >> progress.txt
  update_task_status prd.json
  sleep 5
done
```

真正起作用的不是脚本本身，而是**状态在模型上下文之外**这个设计：prd.json 是任务列表，progress.txt 是实验记录，AGENTS.md 是动态规则本。Agent 本身是失忆的，但文件系统不是。每次迭代从磁盘读取足够的状态，在新上下文窗口里继续推进。

> 「一个晚上就能用 bash 脚本和 JSON 文件搭出一个可用的长程 Agent。」

Anthropic、Cursor 和 Google 在生产环境 productize 的，是让这个模式变得可恢复、安全和可观测。

### 3.2 Anthropic：Harness→Brain/Hands/Session 三层解耦

Anthropic 在两篇重要工程博客里描述了他们的架构进化：

**第一层：双 Agent Harness**（["Effective harnesses for long-running agents"](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)）

- **Initializer Agent**：项目启动时运行一次，负责建立环境、把提示词扩展为结构化的 feature-list.json、写入 init.sh 供后续会话启动时运行
- **Coding Agent**：被反复唤醒，每次只推进一个 Feature，运行测试，在 claude-progress.txt 里留下笔记，然后 commit
- **Test Ratchet**：Prompt 里写入「删除或修改测试是不可接受的，因为这会导致功能缺失或 Bug 被掩盖」——直接对抗最常见的「删测试让测试通过」失败模式

**第二层：Brain/Hands/Session 解耦**（["Scaling Managed Agents: Decoupling the brain from the hands"](https://www.anthropic.com/engineering/managed-agents)，对应 Claude Managed Agents）

```
┌─────────────────────────────────────────────────────┐
│                    Brain                            │
│  Model + Harness Loop（推理 + 决策）                  │
├──────────────┬──────────────────┬──────────────────┤
│   Hands      │   Session       │   Sandbox         │
│  (Ephemeral) │  (Append-only)  │  (On-demand)     │
│  工具执行    │  事件日志        │  隔离执行环境     │
└──────────────┴──────────────────┴──────────────────┘
```

Anthropic 的关键表述：

> 「Harness 里的每个组件都编码了一个关于模型自身不能做什么的假设。当这些假设变得过时，整个系统必须一次性改变。当解耦之后，Harness 变成无状态的，Sandbox 变成 cattle 不是 pets，Brain 崩溃不丢运行数据。」

新容器调用 `wake(sessionId)` 从会话日志恢复状态。Anthropic 报告冷启动延迟数据：**p50 降低 ~60%，p95 降低 ~90%**——原因是推理可以在 Sandbox 就绪之前就开始。

**笔者认为**：Brain/Hands/Session 三层解耦是 2026 年 Agent 架构最重要的设计决策，比选什么模型、搭什么工具有更长的寿命。

### 3.3 Cursor：Planner/Worker/Judge 三角色

Cursor 在["Scaling long-running autonomous coding"](https://cursor.com/blog/scaling-agents)里描述了三次设计迭代：

| 版本 | 设计 | 遇到的问题 |
|------|------|-----------|
| 第一版 | 平铺协调：平等 Agent 写共享文件，有文件锁 | 瓶颈 + Agent 规避风险，空转不提交 |
| 第二版 | 乐观并发控制 | 解决了瓶颈但没解决协调问题 |
| **第三版（生产）** | Planner/Worker/Judge 解耦 | — |

**第三版设计**：
- **Planner**：持续探索代码库，递归产出子任务，可以递归spawn子 Planner
- **Worker**：专注执行，不做协调，不担心全局状态
- **Judge**：判断当前迭代是否完成，决定何时重启

Cursor 报告了两个值得注意的发现：

1. 「系统行为很大程度上取决于如何给 Agent 下 prompt」，而不是 Harness 或模型本身
2. **不同模型适合不同角色**：GPT 在长时间自主工作中比 Opus 表现更好，因为 Opus 倾向于提前停止并走捷径。模型-角色匹配正在成为新的设计维度

**笔者认为**：Cursor 发现「GPT 比 Opus 适合某些角色」这件事很重要——这意味着 Agent 架构设计里，模型路由（routing）正在从隐式变显式，成为 Harness 的一部分。

### 3.4 Google：企业级「三分离」产品化

Google Cloud 在 Cloud Next '26 发布的 [Gemini Enterprise Agent Platform](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform) 将 Anthropic 和 Cursor 的模式 unbundle 为有 SLA 的命名服务：

| 组件 | Google 产品 | 对应模式 |
|------|-----------|---------|
| 执行层 | Agent Runtime | Brain/Hands 分离 |
| 会话持久化 | Agent Sessions | Append-only Event Log |
| 长期记忆 | Agent Memory Bank | 跨会话 Memory |
| 沙箱 | Agent Sandbox | Ephemeral Hands |
| 编排 | A2A Orchestration | Multi-Agent 协作 |
| 治理 | Agent Registry + RBAC | 主体性与权限控制 |
| 监控 | Agent Observability | 可观测性 |

**Agent Memory Bank** 的落地案例：Payhawk 报告通过 Memory Bank 驱动的 Agent 自动提交费用，**处理时间降低 50%**。关键在于 Agent 的状态和业务状态共存于同一系统，而不是孤立的 AI 存储。

> 「三年前这个全是你自己写的。现在你选哪个版本的『解耦 Brain、Hands、Session』来租。」

**笔者认为**：Google 的产品化思路代表了一个趋势——Harness 工程正在从定制开发变成可采购的 infrastructure。当这个转变完成，「用 Harness 竞争」就变成了「用 Harness 配置竞争」，壁垒会迅速降低。

---

## 4. 五大生产设计模式

AddyOsmani 和 Google Cloud 团队总结了五个从 demo 到生产必须落地的设计模式：

### 模式 1：Checkpoint-and-Resume

**问题**：Agent 处理 200 个文档，4 小时后在第 201 个出错，没有 checkpoint 从头开始。

**方案**：把 Agent 当作长时运行的服务进程，每 N 个工作单元写一次中间状态到磁盘。Agent Runtime Sandbox 提供持久文件系统，checkpoint 粒度（不要每步都做，也不要只在最后做）需要根据任务特性配置。

### 模式 2：Human-in-the-Loop（Delegate Approval）

**问题**：大多数「人工介入」实现是：把状态序列化为 JSON，发 webhook，希望有人回复。状态过期，通知被淹没，Agent 恢复时进入一个略微不同的世界。

**正确方案**：Agent 在原地暂停，保留完整的推理链、工作内存、工具历史和待处理动作。人类响应期间 Agent 零计算消耗，恢复延迟亚秒级。Mission Control 是 Google 的收件箱。这个模式不依赖任何特定供应商。

### 模式 3：Memory-Layered Context

**问题**：7 天 Agent 需要超过会话状态的信息。长期积累的 Agent 记忆是最有价值的数据，但同时也是最危险的数据——Agent 会从少数非典型交互中学到程序性捷径，然后广泛应用（memory drift）。

**笔者认为**：记忆治理和数据治理是同一件事。Agent Identity 控制谁可以读写哪个记忆库。Agent Registry 追踪哪个版本的 Agent 在跑。Agent Gateway 在传输层执行策略。审计问题从「我的 Agent 在做什么？」变成「我的 Agent 在记住什么？这些记忆如何改变它们的行为？」

### 模式 4：Ambient Processing

部分长程任务不需要人类参与，也不需要持续向用户推送状态。它们在后台静默运行，检测条件满足后触发动作。这对应 Google 的 Scheduled Jobs + Cron 集成。

### 模式 5：Multi-Agent 协作编排

Planner/Worker/Judge 三角是最小化的多 Agent 协作单元。A2A（Agent-to-Agent）协议解决的是让多个 Agent 通过共享文件系统协调工作——而不是通过共享数据库或消息队列。

---

## 5. 跨越 2026 年的工程启示

### Context Compression 正在成为独立工程领域

[headroom](https://github.com/chopratejas/headroom)（39K Stars，60-95% token 压缩比）这类工具的出现说明：Context 管理已经从「给模型更多 token」的工程问题，变成一个独立的设计领域。

### 模型能做多少，Harness 就要相应减少多少

Anthropic 在 Claude Sonnet 4.5 公告里给出了具体数字：内部测试中 30+ 小时自主编码，其中包括一次产生了 11,000 行 Slack 风格应用的运行。这个数字决定了「我该不该把这件事委托给 Agent」的答案不再是显而易见的「否」。

### 核心工程判断：状态在模型之外

Anthropic/Cursor/Google 的方案表面不同，但底层逻辑一致：**模型上下文窗口里的东西是易失的，窗口外的东西才是持久的**。所有长程 Agent 工程都是围绕这个事实设计边界。

这个判断的推论是：**Harness 的设计表面不是模型本身，而是模型与所有外部系统的边界**。Harness 工程就是设计、拥有和运维这个边界的工程学科。

---

## 6. 与 R457-R459 的关系

本文是 R457（Anthropic Effective Harnesses）、R458（Cursor Scaling Agents）和 R459（Builder.io AI Restraint）构建的 Harness 工程知识链的最新节点：

- R457 描述了 Harness 的目的（防止 Agent 提前停止）
- R459 描述了 AI Restraint 作为 Harness 的质量信号
- **本文**描述了所有这些方案背后的统一工程逻辑——**把状态放在模型之外**

---

## 原文引用

1. 「For two years the dominant image of an 'AI agent' has been a chat window with a clever loop in it. [...] That paradigm got us a long way, but it has a ceiling.」— AddyOsmani, Long-running Agents, 2026

2. 「every component in a harness encodes an assumption about what the model can't do on its own.」— Anthropic, Scaling Managed Agents, 2026

3. 「time-to-first-token dropped ~60% at p50 and over 90% at p95」— Anthropic, Scaling Managed Agents, 2026

4. 「The Ralph Loop is a harness pattern that intercepts the model's exit attempt via a hook and reinjects the original prompt in a clean context window, forcing the agent to continue its work against a completion goal.」— LangChain Blog, Anatomy of an Agent Harness, 2026
