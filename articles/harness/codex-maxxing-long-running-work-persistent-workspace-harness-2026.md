# Codex-maxxing：让 AI 工作持续跨越单次提示

> 本文核心观点：Codex 的长时工作能力不是"更长的上下文窗口"，而是一套**持久化工作区架构**——通过 Durable Threads、Memory Vault、Thread Automations、Steering、Goals 等机制，将 AI Agent 从「响应单个提示」的模式，重构为「持续运行的工作空间」。这是 Harness Engineering 在生产级 AI 系统中的具体实现。

---

## 一、问题的本质：单次提示的瓶颈

长期以来，AI Coding Agent 的使用模式是：

```
人类写提示 → AI 响应 → 对话结束 → 重新开始
```

这个模式在简单任务上没问题，但在**真实的、多步骤的、需要跨越数小时甚至数天的复杂工作**面前，暴露了三个根本性问题：

1. **上下文丢失**：下次对话时，AI 不记得上次做到哪了
2. **状态不可追溯**：决策过程、已完成的步骤、打开的循环（open loops）全部丢失
3. **人类参与断点缺失**：当 AI 在执行一个需要 2 小时的任务时，人类无法中途介入校准方向

这三个问题的本质是：**AI 工作缺乏持久化的工作区（Persistent Workspace）**。

OpenAI 发布的白皮书 *Codex-maxxing for long-running work*（Jason Liu 实践整理）给出了完整的解决方案——不是让模型更强，而是**重新设计 AI 工作的架构**。

---

## 二、核心机制拆解

### 2.1 Durable Threads：给工作一个稳定的"家"

Codex 的 Durable Threads（持久化线程）不是简单的话题延续，而是**为重要工作流建立的专属上下文空间**。

> "For important workstreams, a pinned thread can become the home for the work: the place where context, preferences, old decisions, and open loops accumulate over time."
> — Codex-maxxing 白皮书

Durable Threads 的关键设计：

| 维度 | 说明 |
|------|------|
| **上下文积累** | 消息历史、偏好设置、已做决策、打开的循环（open loops）全部保留 |
| **记忆持久化** | 对话存储在 Memory Vault，不随会话结束消失 |
| **成本权衡** | 长线程携带更多上下文，运行成本高于全新短线程，但连续性价值更高 |
| **适用场景** | 首席助理（CoS）、开源维护、产品迭代、跨周期项目 |

Codex 给出了四个典型 Durable Thread 场景：

- **Chief of Staff**：消息、跟进、会议、open loops
- **OpenAI CLI**：命令规范、代码约定、repo 结构、review 偏好
- **Agents SDK**：示例、文档、常见问题、产品行为
- **Codex for open source**：issue、maintainer、贡献模式、release notes

笔者认为，这四个场景的共同点是**「工作有多个入口、需要跨时间积累上下文、决策需要可追溯」**——这三个条件恰好是大多数真实工作任务的特征。

### 2.2 Memory（Vault）：超越对话历史的记忆层

白皮书明确区分了两个存储概念：

```
Repositories hold code.
The vault holds rolling context around the work.
```

Memory（Vault）是**工作区上下文的外置存储层**，独立于对话历史而存在。它的核心价值是让上下文变得**可审查、可编辑、可对比（diff）**。

当 Vault 存在于 GitHub 中时，diffs 本身成为了记忆的审查面——你可以看到 Codex 认为什么值得记录。这比把上下文藏在 LLM 的上下文窗口里透明得多。

Memory 的记录原则（白皮书原文）：

> As people are mentioned, update the relevant people notes.
> As projects move forward, update the project page.
> As loops close, mark them closed.
> As decisions are made, write down the decision and why it matters.

这四条本质上是**结构化记忆更新协议**——不是让模型随意记忆，而是规定了「什么事件触发什么记录」。这种结构化的记忆管理，是让长时工作真正可持续的关键工程机制。

### 2.3 Thread Automations：让 Codex 主动回来

Thread Automations 是白皮书中最接近「评估器循环」的机制——它是**心跳式的定期唤醒**，让 Codex 在没有人类触发的情况下主动检查工作状态。

> "Thread automations are heartbeat-style recurring wake-up calls attached to the current thread. They tell Codex to return to the same conversation on a cadence, preserving the context instead of starting from scratch each time."
> — Codex-maxxing 白皮书

白皮书给出的具体示例：

> "Every 30 minutes, check Slack and Gmail for unanswered messages that may need attention. Research the context and draft replies, but do not send anything without approval."

这里的核心模式是：
- **Codex 执行**：轮询、检查、研究上下文、起草回复
- **人类决策**：审批后发送

这不是完全的自动化，而是**「AI 准备，人类决策」的分工模式**——评估器（人类）和执行器（Codex）的分离在时间维度上被拉长了。

### 2.4 Steering：实时介入正在执行的工作

Steering 是指**在 Codex 执行过程中，人类实时添加下一个指令**——修正方向、补充上下文、审批下一步、排队下一个行动。

白皮书中的 Steering 示例：

> "Make this smaller."
> "This copy is wrong."
> "Once this is done, open a PR."
> "Wait for the preview deployment."
> "Show me the preview link before anything is posted."

笔者认为，Steering 的本质是**评估器循环的在线版本**：不是等任务完成后才评估，而是在执行过程中持续评估、持续修正。这比「任务结束后的 code review」效率高得多，因为错误的代价在执行过程中就被纠正了。

### 2.5 Goals：让 Codex 有可验证的完成标准

白皮书用「弱目标 vs 强目标」的对比，揭示了一个关键的 Harness 设计原则：

| 类型 | 示例 | 问题 |
|------|------|------|
| **弱目标** | "Implement the plan in this Markdown file." | 无法判断是否完成 |
| **强目标** | "Port this library, keep the public API compatible, and use the original unit tests as the success check. The work is ready for review when the same tests pass and the differences are documented." | 验证标准明确 |

强目标的设计原则是**给 Codex 可测试的验收条件**：预期行为、review 标准、约束条件、done 的明确定义。

白皮书中 Rich-to-Rust 迁移的案例非常有说服力：目标不是「移植这个库」，而是「以能通过原始单元测试的方式移植」。**测试套件给了运行一个真实的标准**——工作直到新实现通过相同测试才算完成。

这正是 Harness Engineering 中「evaluator loop」的核心理念：**执行器和验证器分离，验证器给出客观的完成标准**。

### 2.6 Remote Control + Side Panel：让工作区可随时访问

Remote Control 的设计解决了「人在别处但工作在进行」的问题：

> "Start the task at your desk. Walk away. Review the next decision point from your phone. Approve, redirect, or ask for a different pass."
> — Codex-maxxing 白皮书

Side Panel 则让 artifact（生成的产物）成为对话的一部分——Markdown、spreadsheets、CSVs、PDFs、slides 都可以在对话中直接查看、评论、修改。

这两个机制共同实现了**「工作区无处不在，随时可介入」**的状态——这是持久化工作区的最终目标。

---

## 三、三种实际工作循环

白皮书给出了三个具体的 loop 实现：

### Loop 1：Chief of Staff
- Codex 按计划检查 Slack 和 Gmail
- 找到可能需要处理的消息，研究上下文，起草回复
- **人类决策**：审批、语气、时机、最终决定

### Loop 2：Monitor for Feedback
- Codex 监控 Slack 线程的反馈
- 更新 Remotion 项目，重新渲染，准备修订
- **跨越工具**：Slack 收集反馈 → Remotion 渲染 → Computer Use 处理 GUI

### Loop 3：Get a Refund
- Codex 检查客服是否已加入，准备下一轮回复
- **任务可在用户离开时继续，但行动始终有边界**

这三个 loop 的共同模式：**Codex 准备，人类决策；Codex 执行检查，人类掌控不可逆操作**。

---

## 四、工程意义：Harness Engineering 的生产级实现

Codex 的长时工作设计，本质上是一套完整的 **Harness Engineering 框架**：

| Harness 组件 | Codex 实现 |
|-------------|-----------|
| **Evaluator Loop** | Goals（强目标）+ Thread Automations（定期检查）+ Steering（实时修正）|
| **持久化状态** | Durable Threads + Memory Vault |
| **工作区管理** | Remote Control + Side Panel |
| **Human-in-loop** | Steering + 审批节点 |
| **权限分层** | Connectors（browser/chrome/computer/connectors/skills 的分层访问控制）|

白皮书序言中有一句话精确概括了这套架构的设计哲学：

> "Codex is becoming a place where work can start, keep going, and become real output."
> — source Jason Liu

**工作需要一个居所（a place to live）**——这个 place 就是持久化工作区。Codex 不再只是一个「回答问题的工具」，而是「工作发生的地方」。

笔者认为，这是 2026 年 AI Coding Agent 最重要的范式转变：从**「工具」到「工作区」**。这个转变要求我们用「系统架构」的思维来设计 AI 工作流程，而不是用「单次提示」的思维。

---

## 五、与既有 harness 框架的对照

R529 轮次中，我们分析了 OpenAI Daybreak（安全工程的 evaluator loop）和 Chi-kwan Chan × Codex（科学发现的 evaluator loop）。Codex-maxxing 白皮书补充了一个新的维度：**个人生产力维度的 harness**。

| 案例 | 验证标准 | 执行器 | 验证器 | 时间尺度 |
|------|---------|--------|--------|---------|
| **Daybreak** | CyberGym 通过率 | Codex（漏洞发现）| 自动化评测 + 人工复审 | 分钟级 |
| **Black-Holes** | 物理合理性 | Codex（算法生成）| Chan（科学家人工验证）| 小时-天级 |
| **AI-Scientist** | LLM Reviewer 评分 | 自动实验流程 | LLM Reviewer | 天-周级 |
| **Codex-maxxing** | Goals（强目标）+ 人工审批 | Codex（准备+执行）| 人类（决策+审批）| 分钟-周级 |

**Codex-maxxing 的独特价值**：它展示了「最轻量级的 harness 如何在个人工作流中落地」——不需要企业级基础设施，不需要复杂的评测系统，只需要一个持久化线程 + 一个强目标 + 人类的持续介入。

---

## 六、核心工程原则总结

从 Codex-maxxing 白皮书中提取的 6 条核心工程原则：

1. **工作需要居所**：Durable Threads 让工作有地方积累上下文，不随会话消失
2. **记忆必须外置**：Memory Vault 让上下文可审查、可编辑、可对比
3. **执行与决策分离**：Codex 准备 + 人类决策，而不是 AI 全权执行
4. **目标必须可验证**：强目标给出测试标准，弱目标无法驱动完成
5. **实时介入优于事后修复**：Steering 是在执行过程中纠正，而不是结束后来 code review
6. **工作区无处不在**：Remote Control 保证人在物理位置变化时依然保持对工作的控制

---

**引用来源**：
- OpenAI 白皮书：*Codex-maxxing for long-running work*（Jason Liu 实践整理），CDN: `https://cdn.openai.com/pdf/8a9f00cf-d379-4e20-b06f-dd7ba5196a11/OAI_WhitePaper_Codex-maxxing26.pdf`
- Jason Liu（Creator），OpenAI 2026-06-22