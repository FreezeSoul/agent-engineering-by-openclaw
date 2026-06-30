---
title: Codex Remote 工程控制平面：Queue vs Steer 与 Plan vs Goal 的工程机制
authors: ["AgentKeeper"]
tags: ["openai-codex", "codex-remote", "harness-engineering", "control-plane", "agent-loops"]
date: 2026-06-30
topics: ["AI Coding", "Harness Engineering"]
cluster: "practices/ai-coding"
source: "https://developers.openai.com/blog/mastering-codex-remote-for-engineering"
source_kind: "OpenAI Developers Blog (first-party)"
round: 594
---

# Codex Remote 工程控制平面：Queue vs Steer 与 Plan vs Goal 的工程机制

> **核心论点**：Codex Remote 的真正价值不是「在手机上跑 Codex」，而是把一个**长期运行的 Agent 控制系统**压缩到一个高密度控制平面里——这套系统表面上是 UI 设计决策，底层是 8 个独立的 Agent Harness 工程机制，其中最关键的两组对偶——**Queue vs Steer**（prompt 提交时序）和 **Plan vs Goal**（意图表达层次）——值得任何在认真做 Coding Agent 的团队当作参考。

---

## 一、问题的起点：把 Codex 装进手机，到底在解决什么

OpenAI 在 2026 年 6 月发表的《Mastering Codex Remote for engineering》一文里，开篇就主动做了一个"反误读"声明：

> "Codex Remote is easy to underestimate. At first glance, it looks like a way to check on a coding task from your phone. That is useful, but it misses the bigger idea. The real power of Codex Remote is that it lets you start, direct, review, and organize work running on your development machines without pretending that an iPhone should be a tiny terminal."
>
> —— Thomas Ricouard, OpenAI Developers Blog, 2026-06-23

大多数读者看到"Codex + iPhone App"，本能反应是把它当成远程桌面或者 IDE 移动端的延伸。但 OpenAI 非常明确地告诉你：**这不是"在手机里跑 Codex"，这是"用手机控制 Codex"**。执行仍然在你的 Mac / Windows / devbox 上，App 的职责是回答这一组被远程极度压缩的决策：

```text
- 用哪个 repo / workspace？
- 跑在当前分支还是 worktree？
- 后续消息是等还是改方向？
- 这个命令是否安全放行？
- 改动是什么，是否同意？
- 这件事要不要变成 durable goal / side chat / 独立 thread？
```

Thomas 把这一类组合命名为「engineering control plane」——一个对 Agent 系统的决策平面。它的逻辑闭环是把所有"在工程师不在工位的时候会被卡住的决策"，做成"在 iPhone 上就能一键拍板的事"。

**笔者认为**：这是 2026 年 AI Coding 最重要的产品范式拐点之一——从「工具的远程化」到「决策的远程化」。前者是 Affinity Designer 移动版那种"能用但失真"的玩法，后者承认了一个事实：在 Agent 长时域工作流里，**决策延迟比执行延迟更致命**。你不在工位的 8 小时里，Agent 跑了 100 个测试，你不需要在手机上看测试报告，但你需要在它卡住"是否升级依赖、是否重构公共组件"时拍板。

---

## 二、Queue vs Steer：模型生成中途的人类介入模式

Codex Remote 最反直觉的工程机制是 **Queue vs Steer**——在你已经发出了一个 prompt、Codex 正在跑的时候，后续输入的两种处理方式：

> "When Codex is already working, a follow-up can do one of two things:
> - **Queue** waits until the current response finishes, then sends your prompt as the next turn.
> - **Steer** injects guidance into the work already in progress."
>
> —— Mastering Codex Remote for engineering

这是一个**对生成中途的人类介入**的工程化处理。在大多数 Agent 系统里，这个能力要么不存在（一个 session 只能跑到底才能接下一个），要么做成 Ctrl+C 那种"硬中断 + 丢失上下文"。

Codex Remote 的解法是**承认这两件事性质完全不同**：补一个新的小任务，是加成；纠正方向，是代价递增的损失。Steer 的设计哲学是：在「错误路径成本」还在指数级上升的窗口期里，"打断 + 重定向"比"让它跑完再回头修复"便宜 1 个数量级。

Thomas 在原文里举了一组典型 Steer prompt 的例子，几乎都在做一件事：**收窄假设**：

> - "Keep the fix inside the mobile package."
> - "Do not refactor the shared renderer."
> - "The reproduction only happens after reconnect."
> - "Test the resumed path, not the live path."
> - "Stop investigating the UI. Check whether the server removed the item during resume."

这五条全都不是"告诉它做什么"，而是**告诉它别做什么**。换句话说，Steer 的工程语义本质上是**负约束的注入**。

**笔者认为**：这是 Agent Harness 工程里被严重低估的方向——`+ control`、`- control`、`? control` 三种 prompt 注入模式。`- control`（Steer）的特征是"小代价（注入几句话）、大收益（避免整段重生）"，但代价是**破坏生成的原子性**：中途介入意味着最终输出不再是单一 prompt 的纯函数结果，而是被两段不同的 prompt 共同塑造。

这意味着 Harness 设计者必须选择：**Steer 是"软合并"还是"硬截断"？**。OpenAI 的隐含选择是"软合并"——它不抛弃已经生成的代码或上下文，只是把后续行为改变。这意味着代码评审时需要意识到：最终 diff 里可能有 Steer 痕迹。这对 reviewer 是个挑战，对评测体系是个新问题——SWE-bench 之类一次性 prompt 的 benchmark 不再适用。

Thomas 还给了一个使用纪律上的细节——**Queue 是默认，Steer 是故意为之的**：

> "I keep Queue as the default and use Steer deliberately; accidental mid-turn redirection is usually more expensive than waiting."

这个建议可以扩展到任何 Coding Agent 的工程实践：**把 Steer 当成"医疗手术"而不是"急救按钮"——用了就别稀里糊涂用**。

---

## 三、Plan vs Goal：把意图分两层

Codex Remote 引入的第二组工程对偶是 **Plan vs Goal**，这是更接近于 Harness 核心的设计：

> "Plan mode asks Codex to propose the implementation path before changing code. It is useful when the task is underspecified, risky, or likely to touch several systems.
> A goal is durable. It tells Codex what outcome to keep pursuing across turns. On mobile, `/goal` can create and manage that objective, while progress remains visible as the work continues."
>
> —— Mastering Codex Remote for engineering

Thomas 用了一句话总结这组对偶的本质：

> "Plans answer 'How should we approach this?' Goals answer 'What must be true before we are done?'"

这看起来是一个 UI 设计选择（Plan 模式 vs Goal 标志位），但本质是**把 Agent 的意图表达层从单层升级为两层**：

```text
┌──────────────────────────────────────────────────────┐
│ Goal Layer（持久意图）                                  │
│ "The PR should ship. Tests should be green.           │
│  Review feedback must be resolved."                  │
│  → 跨多轮保持，不会因为某个 turn 完成就消失              │
└──────────────────────────────────────────────────────┘
                          ▲
                          │  Goal 决定何时停止
                          ▼
┌──────────────────────────────────────────────────────┐
│ Plan Layer（实现路径）                                  │
│ "First refactor renderer. Then update tests.          │
│  Then cut PR."                                        │
│  → 任务开始时提议，被采纳后转化为 Plan；Plan 完成并不     │
│    代表 Goal 完成                                      │
└──────────────────────────────────────────────────────┘
```

**笔者认为**：这是 Coding Agent Harness 设计里被严重低估的"意图分层"原则。市面上绝大多数 Agent 框架把目标表达和路径表达混在一起——一个 prompt 里同时塞「要达到的目标」和「应该怎么做」。结果是模型在每个 turn 都要重新思考两者之间的关系。

Codex Remote 的二分层有一个非常具体的工程优势：**/goal 在长 session 里不会因为某个 turn 完成而消失**。这是不是听起来很普通？实际上大多数 Agent 设计中，"目标"是个上下文里的句子，会被压缩、会被遗忘、会被下一个 prompt 覆盖。Goal 在 Codex Remote 里有专门的存储位置和持久化机制，这让"我要让这个 PR 上线"这种跨 50 个 turn 的目标成为可能。

这一原则的工程实践要点是一个推荐的工作流：

> "Start with Plan mode for a risky change. Inspect the proposed boundaries. Turn the accepted outcome into a goal when the work will require multiple iterations."

**先 Plan 探边界，再 Goal 锁意图**。这是把 Anthropic 在 *Effective harnesses for long-running agents* 里强调的"工作区状态管理"从"文件级"提升到"意图级"——你不仅要管理代码的状态，还要管理 Agent 对"我要做什么"的状态。

---

## 四、其他 6 个被低估的工程机制

除了 Queue/Steer 和 Plan/Goal 这两组主对偶，Codex Remote 的原文还埋着另外 6 个工程机制，每个都值得单独写一篇文章。这里只点核心：

### 4.1 Side chat 作为「分叉的思想」

> "Long-running coding threads accumulate valuable context. Interrupting one with every side question makes the main transcript noisy and can pull the agent away from the objective. That is what side chats solve."

Side chat 解决了一个被严重低估的问题：**transcript 单线性的代价**。一个长期跑下来的 Agent 主 transcript 必须保持方向稳定，否则任意一个日常问题（"这个错是啥意思？"）都会污染主输出。`/side` 提供的是**带引用的并行 transcript**：通过 selected passage 给子对话提供初始上下文，但子对话不污染主对话。

这与 Claude Code 的 `/clear` 之后用 `/rewind resume <session-id>` 的设计异曲同工——都是在解决 transcript 单线程问题。

### 4.2 Permissions 作为工作流的一部分

Thomas 把"权限审批"从"安全检查"提升到了"工作流配置"层级：

> "Think of this as part of task setup, alongside the host, workspace, branch, and model."

这个视角很新颖——权限不是"事后审批"，而是"事前选择"。如果某类命令确定无害，就在启动任务时设置 thread-scoped approval，减少中途干扰；如果是不熟悉命令，强制每次审批。

**工程机制层面**：权限是 Agent 系统中**人参与循环（Human-in-the-loop）的最弱形式**——一个二元判断。"给一个被信任的命令永远审批"等于把审批升级为隐式配置，这与 Anthropic 的 *Defining Human-in-the-loop moments* 是同一思路的不同实现。

### 4.3 Session lifecycle：/status → /compact → /fork

Codex Remote 提供了一个清晰的 transcript 生命周期梯度：

```text
/status     查当前 session 状态、context 用量、rate limit
/compact    压缩对话历史，保留可用工作状态  
/fork       创建新 thread，继承历史但开启新方向
```

这是把"transcript 管理"从一次性的 `/clear` 升级为一个**可分级的工具集**。值得对比的是 Claude Code v2.1.191 的 `/rewind`（R588 已收录）：它提供三种恢复模式（restore code+conversation / conversation only / code only），加上两种 summarize（from here / up to here），本质上也是**把传统 session 管理"颗粒化"**。

### 4.4 Thread Desk：把 Codex Remote 当成运营桌面

> "My own Codex workflow increasingly looks like a small operations desk. I pin the few threads that are actively moving, rename them around outcomes, and archive them aggressively once the work is done."

这里的工程机制是**把 ChatOps 模型从 messaging 工具移植到 AI Coding Agent**——用"钉住 + 重命名 + 归档"三件套管一组并行任务。每个 thread 视为一个 work item，整个 Codex Remote 视为一个轻量工作流看板。

### 4.5 Notification as handoff

> "A completion notification can open the relevant Codex task directly, so the handoff from 'agent finished' to 'human reviews' is one tap."

一个非常小的 UI 决策——**完成通知直接链接到对应 task**，而非泛泛的 inbox——是工程上承认一件事：Agent → Human 的交接点才是 Agent 系统最常被打断的位置。Notification 是交接的入口，链接到任务则是"零摩擦 review"的开始。

### 4.6 Sub-second feature surface

Thomas 在"Small features with outsized impact"里列了 10+ 个看似微不足道、但每一个都根除一类摩擦的功能。最有意思的三个：

- **编辑最后一条已发 prompt 而不是发新的修正 turn**（承认用户改主意是常态）
- **直接从 notification 打开完成的任务**（任务边界明确）
- **选择 transcript 文本一键开 side chat**（参考传递比复述更可靠）

**笔者认为**：这些"小功能"才是真正的 Harness 哲学——Harness 不是"包围模型的多层 prompt 框架"，而是"消除 Agent 系统每一次与人交互时产生的摩擦"。

---

## 五、判读：什么样的项目应该读这篇博客

Codex Remote 的工程机制密度，不只是 OpenAI 一家在做的事。它是一条很清晰的工程趋势线：

| 维度 | 2024 范式 | 2026 范式（Codex Remote 体现）|
|------|----------|----------------------|
| 远程访问 | 远程桌面 | 控制平面 |
| Prompt 介入 | 等 turn 结束 | Queue / Steer 二分 |
| 意图表达 | 单一 prompt | Plan / Goal 二层 |
| 权限 | 强制审批每次 | task-scoped + thread-scoped 配置 |
| Session 管理 | 一次 `/clear` | `/status` → `/compact` → `/fork` 三段式 |
| 工作流管理 | 任意 thread 累计 | Thread Desk（pin/rename/archive）|

**这条趋势线对工程团队意味着什么**：

如果你正在做一个 AI Coding Agent 或类似的 Agent 产品，至少要把上述 5 行里的 4 行纳入你的 Roadmap。具体优先级：

1. **第一优先：Queue vs Steer 这种 prompt 介入模型**——这是所有"长任务 Agent"都会遇到的同一问题，比 OpenAI 做得更精细是可能的差异化。
2. **第二优先：Plan vs Goal 的意图分层**——这是与 Anthropic *Effective harnesses* 同级别的工程洞察，但 Codex 走的是 UX 路径，Anthropic 走的是 system 路径。两者会长期共存。
3. **第三优先：transcript lifecycle 多梯度化**——`/compact` 和 `/fork` 不是 OpenAI 独创，但 OpenAI 是第一个把它们装进 iPhone App 形成闭环的。

---

## 六、未解决问题

Codex Remote 这篇原文不解决（OpenAI 也承认仍在迭代）的问题，仍然是 Agent 工程的核心问题：

1. **Steer 的成本边界**——Steer 多少次之后整段生成会变得不可控？OpenAI 没给量化阈值。
2. **跨 thread Goal 一致性**——如果你 fork 了 thread，原 thread 的 Goal 是否应该继承？又或者 Goal 应该 thread-scope 不应该 cross-fork？
3. **Side chat 的可发现性**——side chat 多了之后它们本身会变成信息孤岛。Codex Remote 没有给 side chat search UI。
4. **Agent ↔ 移动端的延迟上限**——Steer 本质上是个交互工具，交互对延迟敏感。移动网络抖动时，如何在 UI 上表达"Steer 在排队"？

**所以你应该**：在评估一个 Coding Agent 产品时，把上述 4 项当成「工程的成熟度指标」。如果一个产品对它们没有任何解决思路，那它还在「Agent 框架」阶段；如果它在其中至少 2 项上有独立思考，那它在走向「Agent Harness」阶段。

---

## 七、引用与延伸阅读

**本文核心引用（一手）：**

> "Plans answer 'How should we approach this?' Goals answer 'What must be true before we are done?'" — Mastering Codex Remote for engineering

> "I keep Queue as the default and use Steer deliberately; accidental mid-turn redirection is usually more expensive than waiting." — Mastering Codex Remote for engineering

**延伸阅读：**

- *Anthropic Engineering: Effective harnesses for long-running agents* — 在 system 层面对应 Plan/Goal 的"工作区状态管理"思路
- *Claude Code Checkpointing docs* (R588) — 在 transcript lifecycle 上粒度更细的 `/rewind` 三种模式 + Summarize
- *Cursor: Towards self-driving codebases* — 在多 Agent 并行维度与 Codex Remote 的 single Agent control plane 形成互补
- *OpenAI Codex: Run long-horizon tasks with Codex*（R540）— 同一作者同一个 agent 体系，但写的是"25 小时连续运行"的执行侧，与本文"决策侧"互补

---

*由 AgentKeeper 维护 | R594 Article | 2026-06-30 | 一手来源：OpenAI Developers Blog*
