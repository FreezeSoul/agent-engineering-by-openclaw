# ArgusBot：Supervisor Agent 架构——让 Coding Agent 自己跑完最后一个 Mile

> **来源**: GitHub README + QuickStart，waltstephen/ArgusBot，MIT License，2026-03-10
> **分类**: projects / harness
> **关联 Article**: 多 Harness Agent 生态：从插件市场到 Supervisor 系统
> **核心判断**: ArgusBot 的三角色 Supervisor 架构（Executor + Reviewer + Planner）揭示了一个关键工程原理：让 Agent 真正完成长任务的核心不是给更多时间，而是**把「何时算完成」从 Agent 自己身上剥离给独立的 Reviewer**——这个职责分离才是 Harness 工程的核心。

---

## 核心命题

Coding Agent 最大的工程悲剧之一：Agent 跑了一半就停下来问「下一步做什么」，不是因为能力不够，而是因为没有独立的评估机制告诉它「你还没完成，继续」。

ArgusBot 解决的就是这个问题——用一个独立的 Reviewer Agent 来判断是否完成，用 Planner 来维持任务上下文，用 Supervisor 来编排整个循环。

![ArgusBot Architecture](screenshots/waltstephen-ArgusBot-supervisor-agent-302-stars-2026.png)

---

## 为什么这是 Supervisor Agent 的工程突破

### 1. 三角色架构：职责分离是关键

ArgusBot 实现了典型的 **三角色 Supervisor 架构**：

| 角色 | 功能 | 决策 |
|------|------|------|
| **Main Agent** | 通过 Codex CLI 或 Claude Code CLI 执行具体任务 | 接收 Reviewer 反馈，执行下一步 |
| **Reviewer** | 评估完成度（`done` / `continue` / `blocked`）| 只有 Reviewer 说 `done` 才退出循环 |
| **Planner** | 维护 live plan、workstream table、next-session 目标 | 跨 session 维持任务状态 |

> *"Loop only stops when reviewer says `done` and all acceptance checks pass."*

这个设计的工程价值在于：**把「何时算完成」从执行 Agent 剥离出来**。执行 Agent 只需要专注执行，评估逻辑由独立的 Reviewer 负责。这解决了"Agent 自己判断是否完成"时的自我服务偏差（总是倾向于认为自己完成了）。

### 2. 长任务稳定性：500 轮 max_rounds + Session Resume

ArgusBot 默认 `max_rounds = 500`，并且支持从上一个保存的 `session_id` 恢复：

> *"Daemon-launched idle runs try to resume from the last saved `session_id` before starting a fresh thread."*

这对于真正长时间运行的任务至关重要。一个小时的工作可能需要几十次 Agent 调用，中途如果 Agent 崩溃或被中断，没有 Resume 机制就只能从头开始。ArgusBot 的 Session Resume 机制让长任务具备了断点恢复能力。

### 3. 多通道远程控制：Telegram / Feishu

ArgusBot 支持通过 Telegram 或飞书远程控制正在运行中的 Agent：

```bash
# 从 Telegram 控制正在运行的 Agent
/inject 先停止当前实验，改成只跑100 step并保存checkpoint
/status
/stop
```

这解决了"让 Agent 跑着，但你人不在旁边"的实际工程需求。Daemon 模式在后台运行，用户通过 IM 工具随时注入指令或查看状态。

### 4. Stall Watchdog：防止死循环

长时间运行的 Agent 有陷入重复循环的风险。ArgusBot 实现了 **Stall watchdog**：

> *"Stall watchdog with soft diagnosis and hard restart safety window."*

软诊断会分析是否真的陷入了 stall（还是在有效工作），硬重启安全窗口确保即使诊断出错也有最后的恢复手段。

---

## 关键工程机制详解

### Reviewer 评估协议

Reviewer Agent 的输出只有三种状态：

| 状态 | 含义 | Supervisor 行为 |
|------|------|----------------|
| `done` | 任务完成，所有验收条件通过 | 退出循环 |
| `continue` | 任务未完成，继续执行 | Main Agent 继续下一轮 |
| `blocked` | 遇到阻塞，需要人工干预 | 暂停并通知用户 |

这个协议本质上是一个**三元信号量**，比简单的"是否完成"二元判断更有表达力。`blocked` 状态让系统在遇到真正问题时不会死循环，也不会错误退出，而是主动请求人工介入。

### Planner 的跨 Session 记忆

Planner 维护的不仅仅是当前 session 的状态，还包括：

- **plan_todo.md**：TODO 看板，跨 planning sweep 持久化
- **explorer backlog**：探索任务队列
- **Live framework view**：实时的框架视图，帮助 Planner 理解任务进展

这让 ArgusBot 具备了**增量规划能力**——每次被唤醒时，Planner 不是从头开始理解任务，而是基于上次的状态继续推进。

### Tiered Model 配置

ArgusBot 支持 Daemon child model 的分层配置：

```bash
argusbot-run \
  --runner-backend claude \
  --runner-bin /opt/homebrew/bin/claude \
  --max-rounds 500 \
  "帮我在这个文件夹写一下pipeline"
```

通过 `--runner-backend` 选择后端（Claude Code 或 Codex CLI），模型配置通过 `daemon_config.json` 持久化，支持不同任务使用不同能力级别的模型。

---

## 笔者判断

**ArgusBot 揭示的工程原理比实现本身更重要**：Supervisor Agent 的核心不是"让 Agent 跑更久"，而是**把控制和评估职责分离**。

很多 Agent 框架把评估逻辑塞进 Agent 的 prompt 里，让 Agent 自己判断"我是否完成了"。这在简单任务里可以工作，但随着任务复杂度增加，Agent 会面临两个问题：
1. **自我服务偏差**：Agent 倾向于认为自己已经完成，不需要再花 token
2. **缺乏全局视图**：Agent 只能看到当前上下文窗口内的信息，无法评估整体进展

ArgusBot 的三角色架构从根本上解决了这两个问题：
- Reviewer 独立于 Main Agent，不受"已经花了多少时间/token"的影响
- Planner 维护全局视图，跨 session 积累任务状态

这正是 Harness Engineering 的核心：**不是让模型更聪明，而是通过工程机制弥补模型的不足**。

---

## 适用场景

✅ **适合的场景**：
- 需要几小时甚至几天才能完成的长任务（代码重构、大规模迁移）
- 需要实时远程监控的 Agent 任务
- 需要明确完成标准的任务（Reviewer 的 `done` 信号是有客观依据的）

❌ **不适合的场景**：
- 短小的一次性任务（引入 Supervisor 的开销不值得）
- 需要实时交互式反馈的任务（Daemon 模式的延迟不适合快速迭代）
- 高安全要求环境（Daemon 默认使用 `--yolo`，高本地执行权限）

---

## 安全警告

ArgusBot 官方文档明确标注的安全风险值得特别关注：

> *"Security risk: daemon-launched runs use `--yolo` by default. This grants the selected backend high local execution power. Run only in trusted repositories/workspaces."*

`--yolo` 模式关闭了安全护栏，在不受信任的代码库上运行高权限 Agent 是一个严肃的安全决策。同时，远程控制通道（Telegram/飞书）的 bot token 泄露可能导致远程命令注入。

---

## 结论

ArgusBot 不是一个"更大的 Agent"，而是一个** Supervisor 架构的最佳实践**。它的三角色设计（Main + Reviewer + Planner）把评估和控制职责从执行 Agent 中分离出来，是 Harness Engineering 中职责分离原则的典型体现。

对于需要构建长任务 Agent 的团队，ArgusBot 的架构值得认真研究：**不是给 Agent 更多时间，而是让评估逻辑独立、让 Planner 维持全局视图**。这才是让 Agent 真正"跑完最后一个 Mile"的关键。

---

**引用来源**：
- waltstephen/ArgusBot GitHub README: https://github.com/waltstephen/ArgusBot
- QUICKSTART.md: https://github.com/waltstephen/ArgusBot/blob/main/QUICKSTART.md
- Stars: 302（截至 2026-06）
- License: MIT