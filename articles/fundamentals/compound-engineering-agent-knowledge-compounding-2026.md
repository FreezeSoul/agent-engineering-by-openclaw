# Compound Engineering：当每个工程动作都让下一个更容易

> 大多数工程团队的工作模式是积累债务——每个功能都增加复杂性，每个 bug 修复都留下更多需要重新发现的本地知识。但 Compound Engineering 的思路完全相反：**每个工程动作都应该让后续动作更容易，而不是更难**。

这是 Every Inc. 在 18,380 Stars 的 [Compound Engineering 插件](https://github.com/EveryInc/compound-engineering-plugin) 里提出的核心理念，也是一个在 Claude Code / Cursor / Codex 三个平台同时运行的完整工程框架。

---

## 一、核心命题：为什么传统开发在积累债务

传统软件开发有一个内建的熵增机制：

- 每加一个功能，代码库变大，上下文更难把握
- 每个 bug 修复都留下一些「本地知识」——谁知道为什么这样改，谁知道这个模块的坑
- 代码审查 Catch 了 bug，但没有 Catch 模式
- 下一个接手的人要从头学一遍同样的教训

这在人类工程师时代就已经是个问题。到了 Agent 时代，这个矛盾更加尖锐：Agent 没有长期记忆，每次新任务都要重新建立上下文。如果没有一个机制把「学到的教训」积累下来，每次 Agent 介入都是在重复同样的学习过程。

Compound Engineering 试图解决这个问题。它的方法是：**把工程工作流程变成一个知识积累的循环**——每个环节的输出物不只是「代码」，还包括「可复用知识」。

---

## 二、核心工作流：Plan 80%，Execute 20%

Compound Engineering 把工程活动重新分配：

```
80% = 规划 + 审查 + 知识编纂
20% = 执行
```

完整循环：

```
/ce-strategy   →  维护 STRATEGY.md（产品目标、问题、指标）
    ↓
/ce-ideate     →  可选：生成并批判性评估想法（不上来就写需求）
    ↓
/ce-brainstorm →  Q&A 式思考，产出需求文档
    ↓
/ce-plan       →  需求文档 → 详细实现计划
    ↓
/ce-work       →  按计划执行（使用 worktrees + 任务追踪）
    ↓
/ce-code-review→  多 Agent 代码审查
    ↓
/ce-compound   →  把学到的东西文档化（供下一个 Agent 使用）
    ↓
repeat → 循环次数越多，上下文越丰富
```

关键在于 `/ce-compound` 这个环节。不是写注释，而是写**可在未来复用的知识片段**。下一个 Agent 进入同一个项目时，这些知识片段是可被读取的上下文，而不是藏在代码注释里的隐含信息。

---

## 三、STRATEGY.md：跨越会话的持久锚点

Compound Engineering 的另一个关键设计是 **STRATEGY.md**——一个在上游的、跨会话的策略锚点。

大多数工程项目的上下文是散乱的：README、issue、slack 消息、会议记录，各自孤立。STRATEGY.md 把这些东西汇聚成一个简短的、持久的产品上下文：

- 目标问题是什么
- 解决方案的核心思路
- 用户画像
- 关键指标
- 当前 tracks（进行中的工作）

`/ce-ideate`、`/ce-brainstorm`、`/ce-plan` 都会主动读取 STRATEGY.md 作为 grounding。这意味着**策略选择会自然地流入功能构思、优先级排序和规格制定**，而不是每次都是从零开始的。

这本质上是一种**选择性记忆**——不是把所有上下文都塞给 Agent，而是把最重要的策略上下文持久化，让 Agent 每次都能获取到真正影响决策的信息。

---

## 四、跨平台：为什么这很重要

Compound Engineering 同时支持 Claude Code、Cursor 和 Codex。这是一个被大多数插件忽略的维度——大多数 Claude Code 插件只在 Claude Code 里工作。

跨平台支持的实际意义不只是「用户可以在不同 IDE 里用同一套工具」。更深层的意义是：**不同平台的 Agent 可以在同一个项目里用同一套工程规范工作**。

当你有一个 Claude Code 团队负责后端，用 Cursor 的团队负责前端，用 Codex 做 code review——如果他们共用同一套 Compound Engineering 的 skills 和 workflow，他们实际上在共用同一套工程语言：相同的策略锚点、相同的计划格式、相同的代码审查标准、相同的知识编纂机制。

---

## 五、37 Skills + 51 Agents：规模本身说明问题

Compound Engineering 不是一个小工具。它有 **37 个 skills 和 51 个 agents**。完整列表见 [Full component reference](https://github.com/EveryInc/compound-engineering-plugin/blob/main/plugins/compound-engineering/README.md)。

这个规模意味着什么？意味着 Every Inc. 在实际工程中已经用 Agent 替代了大量原本需要人类工程师做的重复性工作，并把这些工作流程固化成可复用的 skills。37 个 skills 不是一夜之间设计出来的，是在一个真实工程环境里逐步积累出来的。

特别值得注意的几个：

| Skill | 用途 |
|-------|------|
| `/ce-product-pulse` | 读操作：生成时间窗口式的用户数据报告，保存到 `docs/pulse-reports/`，形成可浏览的历史时间线 |
| `/ce-debug` | 系统性复现失败 → 追溯根本原因 → 实施修复 |
| `/ce-code-review` | 多 Agent 代码审查（不是人类审查，是 Agent 之间的交叉审查）|
| `/ce-compound` | 文档化学到的东西，供未来的 Agent 使用 |

---

## 六、`/ce-compound`：团队级选择性记忆的实现

「每个工程动作让下一个更容易」这个理念需要一个具体的实现机制。`/ce-compound` 就是这个机制。

大多数 skill 系统关注的是「怎么让 Agent 更好地完成任务」——更好的 prompt、更好的工具、更好的上下文管理。Compound Engineering 关注的是另一个维度：「怎么让关于这个项目的知识跨 Agent 复用」。

当一个 Agent 完成了 `/ce-work` + `/ce-code-review` 之后，`/ce-compound` 的输出物不是代码，而是**对这个项目有长期价值的知识片段**——踩过的坑、发现的模式、重要的决策原因。这些内容是结构化的，可以被未来的 Agent 读取，而不是散落在代码注释或 PR 描述里的隐含信息。

这个设计思路和 Anthropic 的「Progressive Disclosure of Agent Skills」以及「Harness with structured artifacts」有直接的呼应。都是关于**如何让 Agent 在长任务中保持上下文连续性**，只是角度不同：Anthropic 的方案是从 Skill 级别，Compound Engineering 的方案是从项目知识级别。

---

## 七、笔者的判断

Compound Engineering 最值得注意的不是 37 个 skills，不是跨平台支持，而是它的**工程哲学**：每个工程动作都应该让下一个更容易。

这个理念本身不新，XP 时代就有「虚假敏捷」和「持续重构」的讨论。但把它放在 Agent 时代的语境下，它变成了一个具体的设计问题：**当 Agent 每次介入都要重新建立上下文时，什么机制能让「学到的教训」真正跨会话复用？**

STRATEGY.md 作为策略锚点、`/ce-compound` 作为知识编纂机制、`/ce-product-pulse` 作为用户数据的时间线——这三者共同构成了一个「项目级记忆系统」，它不是存储所有上下文，而是存储对未来 Agent最有价值的决策上下文。

**适用场景**：需要跨多个 Agent（不同平台或不同任务）维护工程一致性的团队；希望在代码之外积累项目知识的团队。

**不适用场景**：个人简单项目（维护这一套流程本身的成本可能超过收益）；没有固定团队的探索性项目。

> Compound Engineering 的真正贡献不是 37 个 skills，而是提出了一个问题：在 Agent 时代，「每个工程动作让下一个更容易」的机制应该长什么样？答案不是一个 skill，而是一整套知识积累的工作流。

---

## 附录：项目信息

| 项目 | 信息 |
|------|------|
| **Stars** | 18,380 |
| **支持平台** | Claude Code · Cursor · Codex |
| **Skills / Agents** | 37 / 51 |
| **核心哲学** | 每个工程动作让下一个更容易 |
| **安装** | `/plugin marketplace add EveryInc/compound-engineering-plugin` + `/plugin install compound-engineering` |
| **License** | GitHub (见仓库) |
| **官方文档** | [GitHub](https://github.com/EveryInc/compound-engineering-plugin) · [Every.to 博客](https://every.to/chain-of-thought/compound-engineering-how-every-codes-with-agents) |

---

*关联阅读*：
- [Anthropic Progressive Disclosure of Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)（Skill 的渐进式披露机制，Compound Engineering 的 skill 体系同构）
- [Anthropic Harness Design: GAN-inspired three-agent architecture](https://www.anthropic.com/engineering/harness-design-long-running-apps)（Planner-Generator-Evaluator 三角色与 Compound Engineering 的 brainstorm-plan-work-review-compound 循环同构）
- [revfactory/harness：Team-Architecture Factory](https://github.com/revfactory/harness)（Claude Code 生态的 L3 Meta-Factory，6 种 Agent Team 架构模式）