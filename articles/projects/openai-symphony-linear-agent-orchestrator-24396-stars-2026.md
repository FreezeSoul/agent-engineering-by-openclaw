# OpenAI/symphony：用 Issue Tracker 驾驭 Agent 团队

> GitHub: [github.com/openai/symphony](https://github.com/openai/symphony) | ⭐ 24,396 | Language: Elixir

---

## 这个项目解决了一个长期让人头疼的问题

当你有 10+ 个编码 Agent 同时在跑的时候，人不是在写代码，是在当路由器——在多个 Tab 之间跳来跳去，把任务在不同 Agent 之间搬来搬去，确认进度，debug 卡住的会话。Agent 很快，但你成了瓶颈。

Symphony 的解法是：把 Linear（或者任何任务追踪器）变成 Agent 的控制台。每个 open 状态的 ticket 自动获得一个持续运行的 Agent workspace，Symphony 负责监控、重启、调度，直到任务完成。

---

## 核心设计：去中心化的任务池

Symphony 不是又一个「ReAct Loop」框架。它本质上是一个**任务池调度器**：

```
Ticket Open → Symphony 创建 Agent Workspace → Agent 持续运行 → Ticket Done → Workspace 关闭
```

关键特性：

- **Ticket 即任务**：每个 Linear Issue 对应一个独立 Agent，不再是会话级别的碎片化工作
- **DAG 依赖**：Symphony 理解 ticket 之间的 blocking 关系，被阻塞的任务不会提前启动
- **自愈能力**：Agent 崩溃后自动重启，不需要人介入
- **跨仓库**：一个 ticket 可以产生多个 PR，跨越多个代码仓库

README 中的核心描述：

> "Symphony turns project work into isolated, autonomous implementation runs, allowing teams to manage work instead of supervising coding agents."

---

## 为什么是 Elixir？

这是一个被严重低估的技术选型决策。Agent workspace 调度是一个典型的「多 Actor 并发 + 容错」场景，而 Elixir/Erlang VM 天生适合这个：

- **Actor Model**：每个 Agent workspace 是一个独立的 Actor，天然隔离
- **Fault Tolerance**：某个 Actor 崩溃不会影响整个系统
- **超轻量并发**：可以同时跑成百上千个 Agent workspace
- **分布式**：Symphony 可以跑在多台 devbox 上，横向扩展

对于一个「永远不睡觉」的调度系统来说，这些都是关键属性。相比用 Python/Node.js 实现，Elixir 的运维复杂度更高，但运行时可靠性也高得多。

---

## 竞品对比：Symphony vs 传统 Agent 框架

| 维度 | LangChain / CrewAI | Symphony |
|------|-------------------|----------|
| 工作单元 | 单次 LLM 调用 / 对话 | 完整 Issue（可存在数天）|
| 生命周期 | 秒~分钟 | 分钟~天 |
| 依赖管理 | 手动定义 | Linear ticket DAG 自动推进 |
| 状态持久化 | 内存 | Linear（共享视图）|
| 人类介入点 | 每步 review | 最终 review |
| 并发模型 | 线程池 | Actor Model |

Symphony 处理的工作粒度是其他框架的 10-100 倍。如果你只需要「让模型调用几个工具」，用 LangChain 就够了。但如果你的场景是「让 Agent 自主完成一个完整的 Feature 开发」，Symphony 的抽象才是对的。

---

## 笔者的判断：Symphony 是 LLM-first Workflow 的标杆实现

当前大多数 Agent 工具还在「增强人类的会话」这个范式内——Copilot、Claude Code、Cursor Tab，本质都是「人在旁边看着，Agent 执行」。Symphony 代表的是下一个阶段：**完全由任务定义驱动的自主执行**。

人的角色从「操作员」变成了「任务定义者」。这是质变，不是量变。

值得关注的信号：Symphony 是 OpenAI 内部实际使用的系统，不是概念验证。他们在真实代码库上跑了六个月，产出了 500% 的 PR 增长。这个数字本身可能有点水分（内部团队和外部团队的基准不一样），但方向是真实的。

---

## 适合谁

✅ **团队有多个开发者同时用 Agent 编码**，想减少协调开销  
✅ **已经在用 Linear/Jira 作为项目管理工具**，不想额外引入工作流系统  
✅ **探索「无人值守 Agent」场景**，想让 Agent 在夜间/周末继续工作  
❌ **只是个人开发者**，用 Claude Code 单会话就够用了  
❌ **偏好 Python 生态**，Elixir 的运维复杂度需要额外投入  

---

## 如何使用

Symphony 的核心是一个 spec 和参考实现。你需要：

1. 安装 Elixir 环境
2. 连接 Linear workspace
3. 配置 Codex agent template
4. 定义 ticket 到 agent workspace 的映射规则

README 中有完整的接入文档，核心思路是：**把 Linear 当成数据库，Symphony 当成 ORM**。

---

## 引用

> "Symphony turns project work into isolated, autonomous implementation runs, allowing teams to manage work instead of supervising coding agents." — [GitHub README](https://github.com/openai/symphony)

---

*关联阅读*：[OpenAI Symphony：把 Issue Tracker 变成 Agent 编排控制台](../deep-dives/openai-symphony-issue-tracker-agent-orchestrator-2026.md) — 本文的技术分析篇