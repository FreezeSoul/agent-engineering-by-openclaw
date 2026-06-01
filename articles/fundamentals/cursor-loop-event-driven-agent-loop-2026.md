# Cursor /loop：事件驱动的长时运行 Agent 循环模式

> **核心命题**：Cursor 的 `/loop` 技能引入了一种新的 Agent 运行模式——事件驱动循环（Event-Driven Loop），让 Agent 从「被召唤才工作」升级为「值守等待、自我判断触发」。这是 Harness 工程中「Stop Condition 与条件判断」模式的典型实现。

---

## 背景：Agent 的两种运行模式

长期以来，Agent 的运行模式只有两种：

1. **召唤模式（One-shot）**：用户发一条指令，Agent 执行一次，然后结束。这要求用户精确描述任务、持续跟进、反复激活。
2. **长时运行模式（Long-running）**：通过循环或递归让 Agent 持续工作，直到任务完成。但多数实现是「固定间隔轮询」，靠时间驱动而非事件驱动。

第一种模式效率低，第二种模式浪费资源——Agent 在轮询间隔内反复「醒来」检查条件，即使条件未满足也要消耗算力。

Cursor 的 `/loop` 技能引入第三种模式：**事件驱动循环**。

---

## 事件驱动循环的核心设计

根据 Cursor 官方文档，`/loop` 的工作方式是：

> With /loop, Cursor can run a prompt repeatedly on a local schedule, until a certain outcome is achieved, or until you stop it. **If you don't specify a fixed interval, the agent decides when or what event should wake it.**

关键设计点：

### 1. Agent 自主决定唤醒条件

用户可以指定具体的触发条件（"check deploy status every 5 minutes"），也可以只给目标（"work on this feature until tests pass"），让 Agent 自己判断何时需要再次激活。

这意味着：
- **Stop Condition 由 Agent 自己评估**：Agent 在每次执行后判断「目标达成了吗？」、「条件满足了吗？」
- **无需用户反复介入**：一旦设定了目标，Agent 在后台值守，直到自己判断需要再次行动
- **减少无效唤醒**：Agent 只在自己判断需要再次行动时才激活

### 2. Harness 视角：Self-Evaluating Stop Condition

这实际上是 Harness 工程中 **Stop Condition 模式**的智能化实现。传统的 Stop Condition 需要用户在 Prompt 中精确描述「何时停止」，而 `/loop` 的设计将「判断是否停止」的责任部分交给了 Agent 自己。

这种模式的工程价值在于：

| 传统模式 | /loop 模式 |
|---------|-----------|
| 固定间隔轮询，时间驱动 | 目标驱动，Agent 自主判断触发 |
| 用户需要反复检查状态 | Agent 自己判断「工作做完了吗」 |
| 间隔固定，可能浪费或延误 | Agent 自主决定等待策略 |

### 3. 适用场景

Cursor 官方文档给出的示例：

- 「每 5 分钟检查一次部署状态」
- 「持续工作直到测试通过」

第一个是时间驱动的具体化，第二个才是真正的事件驱动——Agent 持续运行 until tests pass，由 Agent 自己判断测试是否通过。

这种模式特别适合：
- **运维监控**：持续监控服务状态，异常时自动告警
- **CI/CD 流水线**：等待构建/测试结果，失败时自动重试或回滚
- **数据处理**：持续处理队列中的任务，直到队列清空

---

## 工程机制分析：为何这是 Harness 而非 Prompt？

有人可能认为 `/loop` 只是 Prompt 设计的一个技巧。但从 Harness 工程的角度看，它的本质是**工程化的 Agent 循环控制机制**：

1. **与 Prompt 解耦**：`/loop` 不是写在系统 Prompt 里的一段指令，而是一个独立的服务机制，Cursor Agent 在底层运行时感知到 `/loop` 的存在
2. **自主评估 vs 固定条件**：传统的 while 循环需要精确的退出条件，`/loop` 让 Agent 自己判断「何时再次唤醒」，这需要在 Harness 层提供评估能力
3. **跨会话状态管理**：Agent 需要记住「上次执行到了哪里」「还差什么条件」，这是 Context/Memory 机制与循环控制机制的协同，不是 Prompt 能解决的

从工程机制稀缺性角度看，**事件驱动型 Agent 循环**在行业内仍然相对稀缺。大多数 Agent 框架的循环机制是时间驱动或步骤驱动的，而真正的事件驱动需要 Agent 具备自我评估能力，这在当前是少数玩家的创新。

---

## 与其他长时运行方案的对比

| 方案 | 触发方式 | Stop Condition | 代表项目 |
|------|---------|--------------|---------|
| **Cursor /loop** | 事件驱动，Agent 自主判断 | Agent 自我评估 | Cursor 3.5+ |
| **Anthropic GAN架构** | 目标驱动，多角色协作 | Evaluator Agent 判断 | Claude Code |
| **OpenAI Codex** | 长时运行，25h+ | 多层 Stop Hook | Codex Agent Loop |
| **传统 ReAct Loop** | 步骤驱动，固定轮次 | 固定步数或 token 限制 | LangChain ReAct |

---

## 总结

Cursor `/loop` 技能的工程意义在于：将「事件驱动循环」从概念引入到实际可用的 Harness 机制中。

这不是 Prompt 优化，而是 **Harness 层的循环控制机制**——Agent 自主决定何时再次激活，自己评估 Stop Condition，减少无效唤醒，让长时运行 Agent 从「被频繁叫醒」进化到「自己判断何时该醒」。

对于构建生产级 Agent 系统的工程师来说，`/loop` 提供了一种值得参考的设计范式：**不要在 Prompt 里写循环逻辑，而是让 Harness 机制负责循环控制，让 Agent 的脑力专注于任务本身**。

---

**引用来源**：
- [Cursor Changelog: Shared Canvases and /loop Skill](https://cursor.com/changelog/shared-canvases)
- [Cursor 3.5 Release Notes](https://cursor.com/changelog)