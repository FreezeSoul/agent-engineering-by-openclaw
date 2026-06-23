# Intent：spec-first 多 Agent 协作的新架构

> **核心判断**：Intent 解决的不是「Agent 跑得慢」的问题，而是「多 Agent 并排跑时，谁来保证它们不会各做各的」的问题。这比任何模型升级都更根本。

---

## 背景：多 Agent 的协作幻觉

过去一年，业界最常见的「多 Agent」实现是这样的：同时跑两个 Agent，一个写前端，一个写后端，各自拿一部分上下文，各自跑，跑完拼起来。这种模式在 Demo 里看起来很美，真实场景下却问题重重：

- **上下文割裂**：两个 Agent 各自只知道自己的 prompt 里写了什么，不知道对方改了什么
- **Spec 漂移**：产品需求变了，但正在跑的 Agent 还在按旧逻辑写代码
- **冲突无人仲裁**：两个 Agent 同时改了同一个文件，merge 靠人肉处理
- **无法中断恢复**：跑了一半想改需求，只能从头来

这些问题的根源不是模型不够强，而是**协作架构根本不对**。大多数工具把「多 Agent」当成了「并排跑的单 Agent」，而不是真正的团队协作。

---

## Intent 的核心解法：Spec-first Orchestration

[Intent](https://www.augmentcode.com/blog/intent-a-workspace-for-agent-orchestration) 是 Augment Code 在 2026 年 6 月 23 日发布的多 Agent 协作工作区。它的核心设计思路用一句话概括就是：**先有 Spec，再有 Agent；Agent 执行，Spec 仲裁**。

### 三 Agent 默认架构

Intent 的默认配置是三个有明确角色的 Agent：

| Agent | 职责 | 关键能力 |
|-------|------|---------|
| **Coordinator** | 理解任务，起草计划为 Spec | 调用 Augment Context Engine 理解完整代码库上下文 |
| **Implementor(s)** | 执行计划，写代码 | 多个，可以并行，按 Spec 分工 |
| **Verifier** | 对照 Spec 验证结果 | 检查代码变更是否符合 Spec，标记不一致和 Bug |

这三者的关系是：**Coordinator 生成 Spec → 你审批 → Implementors 执行 → Verifier 验收 → 你最终审查**。这不是流水线，是有反馈回路的闭环。

### Git Worktree 隔离的工作区

每个 Intent Workspace 背后是一个独立的 Git Worktree。这意味着：

- 每个 Workspace 的代码修改是物理隔离的，不会互相干扰
- 可以随时暂停、切换、恢复，不丢上下文
- Workspace 之间可以并行，同时跑多个任务

这解决了多 Agent 并排跑时的「状态污染」问题——当 Agent A 在写 UserService 时，Agent B 不应该看到未完成的中间状态。

### Living Spec：随代码演进的 Spec

传统的 AGENTS.md 是一个静态文件，写完就过期。Intent 的 Living Spec 是动态的：

> "As code changes, agents read from and update the spec so every human and agent stays aligned."

这意味着 Spec 不是一次性文档，而是**与代码变更同步更新的协调层**。当 Implementor 写完一段代码，Verifier 验证通过后，Spec 会记录这次变更，使得下一个任务开始时，新 Agent 能看到之前的上下文。

---

## 为什么 Intent 比「并排跑 Agent」更优

### 竞品对比

| 方案 | 协调方式 | Spec 角色 | 隔离机制 | 反馈回路 |
|------|---------|-----------|---------|---------|
| **Claude Code Swarm** | Agent 各自跑，人肉协调 | 无（靠 prompt） | 无（共享 context）| 弱 |
| **Codex Parallel Agents** | 共享 prompt，分片执行 | 无 | 无 | 弱 |
| **Cursor Automations** | 触发器驱动，规则化 | 模板化 | 云端隔离 | 中 |
| **Intent** | Spec 驱动，Coordinator 协调 | 核心仲裁层 | Git Worktree | 强 |

笔者认为，Intent 的关键优势不在于「Agent 跑得更好」，而在于**引入了明确的协调层级**。当只有一个 Spec 仲裁者（Coordinator），所有 Agent 都向 Spec 负责，而不是各自为战时，多 Agent 协作才真正成为可能。

### 架构设计的工程启示

Intent 的设计揭示了一个重要的工程原则：

> **当 Agent 数量 > 1 时，协调机制的重要性 > 单 Agent 能力。**

这与分布式系统的 CAP 定理有相似之处：单 Agent 场景下，我们追求的是模型能力（正确性）；多 Agent 场景下，我们首先要解决的是一致性（对齐）问题，而一致性往往需要牺牲一些并行度。

Intent 选择了牺牲并行度（通过 Coordinator 串行化计划阶段），来保证执行阶段的正确性。这是一种工程权衡，不是技术缺陷。

---

## 与其他 Orchestration 范式的本质区别

### Anthropic Dynamic Workflows

Anthropic 的 [Dynamic Workflows](https://www.anthropic.com/engineering/harness-design-long-running-apps) 通过模型实时判断下一步做什么，适合单 Agent 场景下的长程任务。它的决策主体是模型本身。

Intent 的决策主体是 **Spec + Coordinator**，模型执行 Spec 定义的计划。模型不负责决定「下一步做什么」，只负责「怎么做」。

### Cursor Automations

Cursor 的 [Automations](https://cursor.com/blog/automations) 是触发器驱动的：Webhook 来 → Agent 跑 → 做完发 Slack。这种模式适合自动化流水线，但不适合需要多层协作的复杂任务。

Intent 适合的是**需要规划 → 执行 → 验证多轮迭代的任务**，而不是简单的「事件 → 响应」。

---

## 适用边界：Intent 不是银弹

Intent 有它的适用场景，也有它的边界。

**Intent 擅长的**：
- 需要多 Agent 协作的中大型任务（如实现一个新功能模块）
- Spec 清晰、可结构化的任务
- 需要保留中间状态、随时可中断恢复的任务

**Intent 不擅长的**：
- 单 Agent 能完成的简单任务（引入 Coordinator 开销不划算）
- 探索性、需求不清晰的任务（没有 Spec 可写）
- 需要实时调整计划的高度不确定性任务

笔者认为，Intent 的出现代表了一个更大的趋势：**多 Agent 协作正在从「能力问题」变成「架构问题」**。当业界开始认真思考如何让 Agent 作为一个团队而不是一群个体工作的时候，Spec-first orchestration 就成了一个必然选择。

---

## 结论

Intent 解决的不是「如何让 Agent 写得更快」，而是「如何让多 Agent 不各做各的」。它的核心贡献是引入了 **Spec 作为协调层** + **Git Worktree 隔离** + **Verifier 反馈回路** 的组合。

这比单纯的模型升级更根本。当你的团队开始认真使用多个 Agent 同时工作时，你会发现真正的问题不是「Agent 够不够聪明」，而是「谁来保证它们在一个方向上」。

Intent 给了一个答案：不是人肉协调，是 Spec。

---

## 原文引用

> "Intent treats multi-agent development as a single, coordinated system: agents share a living spec and workspace, stay aligned as the plan evolves, and adapt without restarts."
> — [Intent: A workspace for agent orchestration](https://www.augmentcode.com/blog/intent-a-workspace-for-agent-orchestration), Augment Code, 2026-06-23

> "You define the spec, approve the plan, and let agents work in parallel, without juggling terminals, branches, or stale prompts."
> — 同上

> "The bottleneck has moved. The problem isn't typing code. It's tracking which agent is doing what, which spec is current, and which changes are actually ready to review."
> — 同上

---

**关联阅读**：
- [Anthropic Dynamic Workflows：模型驱动的 Agent 自主编排](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/orchestration/anthropic-dynamic-workflows-claude-code-on-the-fly-harness-2026.md)
- [Cursor Automations：always-on Agent 软件工厂](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/harness/cursor-automations-always-on-agent-software-factory-2026.md)
