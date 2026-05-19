# Cursor 第三时代：代码即工厂，云端 Agent 舰队正在重塑软件开发

> **核心论点**：软件开发正在从「自己写代码」转向「构建代码工厂」——而这个工厂的核心员工，是云端 autonomous agents，它们不再向你汇报每一行改动，而是带着成品回来让你验收。

---

## 从 Tab 到 Agent，再到 Autonomous Agent

Cursor 博客的一篇文章把 AI 软件开发划分为三个时代：

| 时代 | 交互方式 | 人类角色 | 时间跨度 |
|------|---------|---------|---------|
| **第一时代：Tab** | 逐字符补全 | 「监督者」——决定是否 tab | ~2年 |
| **第二时代：同步 Agent** | Prompt-Response 循环 | 「指挥者」——逐指令引导 | <1年 |
| **第三时代：Autonomous Cloud Agent** | 异步长程任务 | 「工厂主」——设定目标，审核成品 | 现在 |

第二时代的典型特征：Agent 在你的本地机器上运行，需要同步交互，资源竞争限制了并行度。Cursor 的数据说明了这个转变有多快：

> **"In March 2025, we had roughly 2.5x as many Tab users as agent users. Now, that is flipped: we now have 2x as many agent users as Tab users."** — Cursor 博客

Agent 使用量一年增长 **15 倍**，而这个数字仍在被第三时代继续改写。

---

## 第三时代的本质：Artifact 取代 Diff

第二时代的开发者与 Agent 的交互单位是「diff」——每个 Prompt-Response 循环返回一个代码改动，你需要逐个审查。

第三时代的交互单位变成了 **Artifact**：

> **"The agent works through it over hours, iterating and testing until it is confident in the output, and returns with something quickly reviewable: logs, video recordings, and live previews rather than diffs."** — Cursor 博客

Agent 在云端虚拟机上运行数小时，迭代、测试，直到自信产出，然后交付给你的是：
- **日志**：完整的执行轨迹
- **视频录制**：Agent 操作界面的屏幕记录
- **Live Previews**：可直接查看的效果

你不再逐行审查代码，而是审查成品——就像产品经理验收功能，而不是 review 每一行实现细节。

这意味着人类的角色发生了根本性位移：**从「逐行引导」到「定义问题与验收标准」**。

---

## 软件工厂：Cursor 对第三时代的定义

Cursor 对这个转变的核心表述值得原文引用：

> **"Cursor is no longer primarily about writing code. It is about helping developers build the factory that creates their software. This factory is made up of fleets of agents that they interact with as teammates: providing initial direction, equipping them with the tools to work independently, and reviewing their work."** — Michael Truell, Cursor 创始人

这个定义揭示了几个关键设计决策：

### 1. Fleet（舰队）而非单体

工厂不是一台机器，而是一个舰队。你同时运行多个 agents，每个在你的云端虚拟机上独立运行。你不再逐一引导一个 agent 完成，而是向整个舰队下发任务，然后对结果进行并行审查。

### 2. Teammate 而非 Tool

Cursor 明确将 agents 定位为「teammates」而非工具。这意味着：
- 你给的是初始方向（initial direction），而不是逐条指令
- 你装备它们工具，让它们独立工作（equipping them with the tools to work independently）
- 你审查它们的成果（reviewing their work）

这不是「用 Agent 写代码」，这是「把 Agent 当成同事来管理」。

### 3. Artifact 驱动的验收模式

不同于第二时代的 diff review，第三时代的验收是成品导向：视频、日志、预览。你不用重建每个 session 的上下文，因为 artifact 已经把足够的信息压缩进了可检查的形式里。

---

## Cursor 内部数据：35% 的 PR 由 Autonomous Agents 创建

这个数字值得单独拿出来分析：

> **"Thirty-five percent of the PRs we merge internally at Cursor are now created by agents operating autonomously in cloud VMs."** — Cursor 博客

35% 意味着**超过三分之一的代码改动完全不需要人工逐行参与**。这不是在测试环境下的小规模实验，而是 Cursor 自己每天在生产中运行的数字。

而且 Cursor 的判断是：**"A year from now, we think the vast majority of development work will be done by these kinds of agents."**

这不是乐观的愿景，而是基于当前轨迹的外推。

---

## 第三时代的工程挑战

Cursor 也坦诚指出了这个范式面临的工程问题：

> **"At industrial scale, a flaky test or broken environment that a single developer can work around turns into a failure that interrupts every agent run."** — Cursor 博客

第二时代里，一个 flaky test 可以由开发者在 prompt 中忽略或绕过。但在第三时代的工厂模式下：
- 你同时运行多个 agents
- 每个 agent 独立迭代数小时
- 任何不稳定性都会被放大

这意味着**环境可靠性从「开发者的个人问题」变成了「工厂的停机问题」**。这也是为什么 Cursor 在同一时期发布了 cloud agent development environments 的能力——因为 agents 的能力上限取决于它们运行的环境。

---

## 笔者观点：第三时代的核心转变是「信任模型」

第二时代到第三时代的最大跳跃，不是技术，而是**信任模型**。

第二时代的开发者与 Agent 之间是「紧控制」模式：
- Agent 每一步都向你汇报
- 你随时可以打断、重定向
- 你的角色是持续的质量门禁

第三时代变成了「委托-验收」模式：
- 你把任务交给 Agent，Agent 独立完成
- 你只对最终成品进行审查
- 你的角色是定义目标和验收标准，而不是控制过程

**这种信任模型的前提，是 Agent 必须能够在没有实时反馈的情况下自我纠正**。这就是为什么第三时代的 agents 需要更强的好奇心驱动、更长的上下文、以及更鲁棒的错误恢复机制——它们不能在你每次皱眉时就停下来问你该怎么办。

如果你还在用第二时代的思维使用 Agent（逐 prompt 引导、实时监控每一步），那你已经落后于这个转变了。

---

## 关联项目

与本文主题「Autonomous Cloud Agent 工厂模式」高度关联的 GitHub 项目：

- **[duraikannan1992/open-swe](https://github.com/duraikannan1992/open-swe)**：开源的异步 Coding Agent，基于 LangGraph 构建，支持从 GitHub Issue 直接启动任务，Agent 在云端沙盒中独立完成代码修改和 PR 创建
- **[aws-samples/sample-autonomous-cloud-coding-agents](https://github.com/aws-samples/sample-autonomous-cloud-coding-agents)**：AWS 开源的自托管 Autonomy Coding Agent 平台样本，基于 AWS CDK 构建，包含 durable orchestrator、tiered memory system 和 isolated MicroVM 运行环境

---

**引用来源**：
- [The third era of AI software development - Cursor](https://cursor.com/blog/third-era)
- [Development environments for your cloud agents - Cursor](https://cursor.com/blog/cloud-agent-development-environments)