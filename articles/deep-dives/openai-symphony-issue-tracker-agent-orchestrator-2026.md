# OpenAI Symphony：把 Issue Tracker 变成 Agent 编排控制台

> 本文深度解读 OpenAI Engineering Blog：[An open-source spec for Codex orchestration: Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/)（Alex Kotliarskyi, Victor Zhu, Zach Brock，2026-04-27）

---

## 核心命题：人成了 Agent 的瓶颈，而不是 Agent

OpenAI 团队用六个月做了一件极端的实验：整个代码仓库全部由 Codex 生成，不留一行人写代码。但当 Agent 能力提上来之后，他们发现了新的瓶颈——不是模型，是人。

> "We had effectively built a team of extremely capable junior engineers, then assigned our human engineers to micromanaging them."

这是整篇文章最重要的一句话。每个工程师能同时管理的 Codex 会话不超过 3-5 个，再多就开始「认知地狱」——分不清哪个 Tab 在做什么，在多个终端之间跳来跳去，调试中途卡住的任务。人从 Agent 的使用者退化成了 Agent 的保姆。

Symphony 的解决思路非常反直觉：不再围绕「编码会话」组织工作流，而是围绕「任务」本身。把 Linear（他们的项目管理工具）当成 Agent 的控制台，每个 open 状态的任务对应一个持续运行的 Agent workspace。

---

## 为什么这是 Agent 编排的范式转移

当前 Agent 社区的主流范式有两种：

### 范式 1：CLI/IDE 内的交互式会话
Claude Code、Cursor Tab、Ghost Browser 都属于这个模式。人在终端或 IDE 里和 Agent 对话，给指令、审代码、决定下一步。本质上是「人驱动 Agent」。

### 范式 2：单一 Agent 控制流（ReAct / Plan-and-Execute）
LangChain Agent、CrewAI 属于这个模式。一个 Orchestrator 给多个 Worker Agent 分配子任务，通过消息传递协作。本质上是「Agent 驱动 Agent」，但控制流还是集中式的。

Symphony 走的是第三条路：**去中心化的任务池模式**。整个系统以 Linear 的 ticket 状态机为驱动，Agent 不是被「调用」而是被「唤醒」——Symphony 持续监听任务队列，任何新 open 的 ticket 都会被分配一个 workspace，Agent 在里面自主运行直到完成或阻塞。

关键洞察在于：他们把**工作单元**从「会话」抽象到了「任务」。一个会话可以产生多个 PR，一个任务可以永远不碰代码库（纯调研），这意味着 Agent 可以承接更大粒度、更模糊的工作。

---

## 技术架构：Elixir + Linear 状态机

Symphony 使用 Elixir 构建，选型本身就很有意思。Elixir 的 Actor Model 和 Erlang VM 的容错能力天然适合这种「长时间运行、状态机驱动」的场景。具体架构：

```
Linear (状态机) ←→ Symphony (调度器) ←→ Codex Agent Pool (执行器)
     ↑                        ↓
  ticket 状态           agent workspace 生命周期
```

- **Ticket = Task**：每个 open 状态的 Linear Issue 自动创建 Agent Workspace
- **Symphony = Supervisor**：监控所有 workspace，重启崩溃/卡住的 Agent，自动推进 DAG 依赖
- **Agent = Worker**：持续运行，直到 ticket 进入「Done」状态

特别值得注意的是他们对「阻塞」的处理。Symphony 支持任务依赖 DAG——如果 React 升级被标记为「blocked by」Vite 迁移，Agent 会在 Vite 迁移完成前完全不启动这个任务。这解决了一个实际问题：多 Agent 并行执行时，错误的启动顺序会导致大量的无效尝试和代码冲突。

> "Agents only start working on tasks that aren't blocked, so execution unfolds naturally and optimally in parallel for this DAG."

---

## 500% PR 增长背后的经济学

OpenAI 宣称某些团队 LANDED PR 数量增长了 500%。但比数字更重要的是这个增长背后的经济学变化。

传统的 Agent 协作方式有一个隐性成本：人必须「持有」一个任务才会推进它。把任务交给 Agent 也是一种投入，你需要监督、review、debug、重新指导。每一次干预都有成本，所以人们倾向于把任务攒大了再提交，减少「交接摩擦」。

Symphony 把这个成本降到了接近零：

> "If the agent gets something wrong, that's still useful information, and the cost to us is near zero. We can very cheaply file tickets for the agent to go prototype and explore, and throw away any explorations we don't like."

任务的启动成本从「评估是否值得人花时间」变成了「评估是否值得放进 ticket queue」。这直接改变了行为模式——他们开始把很多探索性的、验证性的、小规模的重构扔给 Agent，这些工作在传统模式下根本不会立项。

更有意思的是，这改变了「谁可以发起工作」。PM 和 Designer 不需要 checkout 代码库，不需要管理 Codex session，直接在 Linear 里描述功能，Agent 完成之后他们收到一个包含视频 walkthrough 的 review packet。

---

## 为什么不是 LangChain/CrewAI/AutoGen？

Orchestration 框架已经有很多了。Symphony 和这些框架的核心区别在于**控制粒度**：

| 框架 | 控制对象 | 工作单元 |
|------|---------|---------|
| LangChain | Tool/Chain | 单次 LLM 调用 |
| CrewAI | Agent Role | 单轮任务 |
| AutoGen | Agent Pair | 对话级别 |
| Symphony | **Ticket/Project** | **长期迭代任务** |

Symphony 的工作单元是 Issue，Issue 可以存在几小时甚至几天，产生多个 PR，跨越多个代码仓库。传统 Agent 框架里的「Orchestration」通常是几秒到几分钟的短时任务。Symphony 处理的粒度完全不同——它是一种「项目管理 Agent」，而不是「代码生成 Agent」。

---

## 笔者的判断：Symphony 预示了 Agent 的下一步

Symphony 最有价值的地方不是技术实现，而是它揭示的方向：**当 Agent 能力足够强时，人类应该从「Agent 操作者」变成「任务定义者」**。

现在的 Agent 产品（Claude Code、Cursor Tab）还在要求人类「操作」Agent——你要开 Tab，你要写 prompt，你要决定下一步。Symphony 的实验说明，当 Agent 能自主完成完整任务时，「管理任务」会比「操作会话」效率高一个数量级。

但这个方向有一个核心挑战：**任务定义的质量**。在 Symphony 的模式里，人类的主要工作从「写代码 review PR」变成了「写好 ticket 描述」。这是另一种形式的 prompt engineering，但粒度更大、反馈更慢、错误代价更高。

笔者认为，Symphony 代表的是 Agentic Coding 的下一个主流范式：**LLM-first Workflow**——不是让 LLM 适应人类的工具链，而是为 LLM 重新设计整个工作流基础设施。Linear 在这个模型里不是工具，而是 Agent 和人类共同使用的「共享记忆」。

---

## 引用

> "We realized we were optimizing the wrong thing. We were orienting our system around coding sessions and merged PRs, when PRs and sessions are really a means to an end. Software workflows are largely organized around deliverables: issues, tasks, tickets, milestones."

> "Because the orchestrator runs on devboxes and never sleeps, we can add tasks from anywhere and know an agent will pick it up."

> "After implementing Symphony, we delegate more work to agents and focus on harder, more exploratory work."

---

*本文是「OpenAI Agent 工程实践系列」的第三篇。前两篇：[OpenAI Codex 企业安全五大支柱](openai-codex-enterprise-security-five-pillars-2026.md) / [Building a safe, effective sandbox to enable Codex on Windows](openai-codex-windows-sandbox-architecture-2026.md)*