# Looper：Claude Code 的循环设计层 — 在 /goal 和 /loop 之间填补的设计空白

> **核心命题**：Claude Code 自带了 /goal（持久化目标）和 /loop（定时调度），但两者都是**执行层工具**——它们不帮助你设计一个值得运行的循环。Looper 填补了这个空白：它是一个**设计层工具**，在运行之前先确保你的循环设计是严谨的、有可验证标准的、有第二模型把关的。
>
> **一句话推荐**：如果你用 Claude Code 做复杂任务，Looper 让你的 /goal 变得更可靠；如果你担心 /loop 跑偏，Looper 让调度有了设计保障。

---

## 这个项目解决什么问题

Claude Code 的 /goal 和 /loop 是行业里被广泛使用的两个命令。

**/goal** 的能力：设置一个持久化目标，让 Claude Code 在每个动作后检查当前状态是否满足目标，持续工作直到满足为止。这解决了「每次只做一个步骤」的问题。

**/loop** 的能力：把一个任务变成定时任务，让它按 cron 间隔反复运行——适合监控 CI、观察部署、检查后台任务。

但两者都有盲区，而且这两个盲区恰好互补：

**/goal 的三个盲区**：
1. **无 coaching**：/goal 接受任何输入，不会告诉你「这个目标不可证伪」或「'完成'从未被定义」
2. **单模型自评**：目标条件由执行任务的同一个模型判断——这正是「自己给自己的作业打分」的盲区
3. **无结构复用**：目标存在于会话中，不是一个可版本化、可检查的 artifact

**/loop 的盲区**：
/loop 是一个 scheduler，不是设计工具。它不帮助你决定「什么该跑」「成功标准是什么」「谁来检查工作质量」。

Looper 的定位就是：**设计层优先于执行层**——先确保循环值得运行，再交给 /goal 或 /loop 执行。

---

## 核心机制：六步访谈设计法

Looper 的设计流程通过 `/looper` 命令启动，执行一个六步访谈：

**Step 1 — Goal（目标）**：你陈述目标，Looper 批判性地审视它，检查它是否可证伪、是否有明确的完成定义。Looper 不会接受模糊目标。

**Step 2 — Context（上下文）**：哪些文件、命令、issues 或外部数据源可以被这个循环访问。循环的上下文边界在这里被明确。

**Step 3 — Actions（行动）**：哪个模型、哪些工具、哪些命令可以改变状态。这里的关键决策是选择 host model（驱动循环的模型）。

**Step 4 — Council（评审团）**：这是 Looper 与 /goal 最大的差异化设计——**默认使用不同模型家族的 reviewer/judge**。Looper 明确建议 host model 和 reviewer 使用不同模型家族，并解释原因：同一模型在「生成」和「评审」时使用相同的内部表征，容易产生确认偏误。

**Step 5 — Gates & Control（门控与控制）**：在哪里设置 review 节点、revision 和 iteration 的上限、无进展信号识别、预算限制、人工检查点，以及执行边界。Looper 不会发出没有终止保护的循环。

**Step 6 — Confirm（确认）**：Looper 生成一个 ASCII 流程图预览，让你在实际运行前确认循环结构。

关键的是：Looper 生成的输出包括：
- `RUN_IN_SESSION.md`：同一会话内的执行交接文档
- `loop.yaml`：Portable、版本可控的循环规范
- `loop.resolved.json`：编译后的规范
- `run-loop.py`：可选的 Python 执行器（可在另一个终端或 LLM 会话之外运行）

---

## 为什么这是 Claude Code 生态的重要补全

Claude Code 自身对循环设计的支持分散在两个命令中，Looper 通过一张清晰的对比表说明了这个问题：

| 维度 | /goal | /loop | Looper |
|------|-------|-------|--------|
| **层级** | 执行（会话内）| 执行（调度）| **设计（飞行前）** |
| **Coaches your goal** | ❌ | ❌ | ✅ |
| **Typed, checkable verification** | ❌ | ❌ | ✅（programmatic / judge / human）|
| **Reviewer model** | same model（自评）| none | **different model, by default** |
| **Explicit review gates** | implicit | none | ✅（plan gate + delivery gate）|
| **Termination guards** | goal-condition only | interval / until | ✅（iteration + revision + no-progress + budget caps）|
| **Portable, versionable artifact** | ❌ | the cron job | ✅（loop.yaml + resolved spec）|

这个对比清晰地说明：**Looper 不是要替代 /goal 或 /loop，而是给它们更好的输入**。

---

## 工程机制分析

### 循环状态的持久化

Looper 在循环工作区中维护两个状态文件：

- **`state.json`**：当前循环状态（当前阶段、iteration 计数、revision 计数）
- **`run-log.md`**：执行日志，记录每次 review 的决策和结果

这两个文件构成了循环的「黑匣子」——即使循环中断，也能从断点恢复，并完整追踪执行历史。

### 双门控设计：Plan Gate + Delivery Gate

Looper 的循环有两个明确的 review gate：

**Plan Gate（计划门控）**：在 agent 开始执行之前，reviewer 评估 plan.md 是否合理、是否可达成、是否满足目标。这防止了「用正确的方法做错误的事」。

**Delivery Gate（交付门控）**：在 agent 提交交付物时，programmatic check + judge 共同评估交付物是否满足质量标准。这防止了「做完了但质量不合格」。

每个门控有独立的 revision 上限（默认 ≤ 3 次 revision），超过上限后循环进入失败状态。

### 终止保护机制

Looper 明确提供了四种终止保护：

1. **Max iterations**：防止无限循环
2. **Revision caps per gate**：防止在某个阶段卡死
3. **No-progress signals**：检测连续无进展的迭代
4. **Budget caps**：token/USD 预算限制（操作员可见的 advisory limits）

这四种机制共同确保了 Looper 不会成为一个「无法停止的循环」——这是长时间运行 Agent 的关键安全保障。

### Reviewer/Judge 的模型隔离原则

Looper 明确建议使用**不同模型家族**作为 host model 和 reviewer/judge，并给出解释：同一模型在「生成」和「评判」时存在内在的确认偏误。

这个设计原则与行业最佳实践一致（参见仓库中 `harness-engineering-mitchell-hashimoto-agent-framework-2026.md` 提到的「第二模型检查」机制）。Looper 在设计层就把这个原则变成了默认配置，而非可选特性。

---

## 竞品定位

Looper 填补的是 Claude Code **设计层**的工具空白。它的竞品不是其他 Agent 框架，而是 Claude Code 内置的 /goal 和 /loop 命令。

从这个角度看，**Looper 是 Claude Code 用户的必装技能**——它让 /goal 和 /loop 变得更有保障，而不是替代它们。

---

## 适用场景

**Looper 适合**：
- 复杂的多步骤任务，需要明确的完成标准和验证机制
- 需要第二模型把关的长循环任务
- 希望将循环设计变成可复用 artifact 的团队
- 需要在 Claude Code 会话之间保持循环执行一致性的场景

**Looper 不适合**：
- 简单的单步任务（直接用 /goal 即可）
- 纯粹的定时监控场景（直接用 /loop 更简单）
- 需要多 Agent 协作或跨 Agent 通信的场景（这是 orchestration 层的问题）

---

## 快速上手

```bash
# macOS/Linux 安装
curl -fsSL https://raw.githubusercontent.com/ksimback/looper/main/install.sh | bash

# Windows PowerShell 安装
irm https://raw.githubusercontent.com/ksimback/looper/main/install.ps1 | iex

# 在 Claude Code 中启动
/looper
# 或指定输出目录
/looper client-onboarding-loop
```

安装后，Looper 会创建一个私有的 `.venv`（在 skill 目录内），包含 PyYAML 依赖，并注册 `/looper` 斜线命令。

---

## 引用

> "The honest summary: if you already know your loop is well-designed and you just need it to persist or to fire on a schedule, /goal and /loop are the right reach. Looper exists for the part those don't touch — making sure the loop is worth persisting before you hand it off, and making sure something other than the author is checking the work."
>
> ——[ksimback/looper README](https://github.com/ksimback/looper)

---

## 元信息

| 项目 | 值 |
|------|------|
| **Stars** | 493 ⭐ |
| **License** | MIT |
| **Language** | Python |
| **Maintainer** | Kevin Simback [@ksimback](https://github.com/ksimback) |
| **Related Article** | *Harness Engineering 三维框架：Böckeler 的 Feedforward/Feedback 体系解读* |

---

*来源：[ksimback/looper](https://github.com/ksimback/looper) · GitHub, 2026*