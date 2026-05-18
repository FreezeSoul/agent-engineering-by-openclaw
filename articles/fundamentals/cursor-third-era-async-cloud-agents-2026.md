# The Third Era of AI Software Development：异步云端 Agent 正在重新定义开发者的角色

> 原文：[The third era of AI software development](https://cursor.com/blog/third-era) | Cursor Blog | Feb 26, 2026

---

## 核心论点

Cursor 提出了一个明确的三段论：**Tab（补全）→ 同步 Agent → 异步云端 Agent**。第三代的本质变化不是「更快的代码生成」，而是**开发者从「逐行引导」转向「定义问题与验收标准」**——Agent 在云端 VM 上自主工作数小时，返回的是日志、视频、实时预览，而不是 diff。

笔者判断：**这不只是 Cursor 的产品路线图，而是整个 AI Coding 领域正在形成的共识方向**。理解第三代的核心机制，比争论哪家模型更强更有价值。

---

## 第一代到第三代：每次转变都是一次范式跃迁

### 第一代：Tab（补全）

Tab 解决的是**低熵、重复性工作**的自动化。开发者仍然控制每一行代码，只是让机器填充确定性高的空白。

这个时代持续了将近两年。直到 2025 年中，Cursor 的数据显示 Tab 用户仍然是 Agent 用户的 2.5 倍。

### 第二代：同步 Agent

模型能力跃升后，Agent 可以持有更多 context、使用更多工具、执行更长的 action 序列。开发者从「逐行写」转为「prompt-and-response 循环」——给 Agent 指令，等它返回结果，再给下一条指令。

Cursor 数据显示，这个转变极为迅速：**一年之内，Agent 用户超过 Tab 用户 2 倍**，Agent 使用量增长超过 15 倍。

但同步 Agent 有两个根本限制：
1. **实时交互的带宽**：开发者必须在每个步骤介入
2. **本地资源竞争**：同步运行多个 Agent 会消耗本地计算资源，实际上只能同时运行少数几个

### 第三代：异步云端 Agent（本文核心）

Cloud Agent 移除以上两个约束：
- 每个 Agent 运行在**独立虚拟机**上
- 开发者 handing off 任务后可以去做其他事
- Agent 工作数小时后返回**可审查的 artifact**（日志、视频、实时预览）

这使得**并行运行多个 Agent** 成为可能——因为 artifact 和预览提供了足够的上下文，你不需要重建每个 session 的完整过程。

> "The human role shifts from guiding each line of code to defining the problem and setting review criteria."
> — Cursor Blog

---

## 第三代的核心工程挑战

Cursor 坦诚地指出了当前第三代方案面临的真实问题：

### 1. 稳定性要求指数级上升

在工业规模下，单个开发者可以绕过的 flaky test 或 broken environment，在多个 Agent 并行运行时会成为**每个 Agent run 的阻断性 failure**。这要求更严格的测试覆盖、环境隔离和恢复机制。

### 2. Agent 需要完整的工具和 context 访问权限

Cursor 将「cloud agents」视为走向「self-driving codebases」的步骤之一：

> "We're building toward a future of self-driving codebases, where agents merge PRs, manage rollouts, and monitor production."

但这需要 Agent 能够访问完整的工具链、上下文和执行环境，而不仅仅是代码编辑器。

### 3. Human review 的形式发生根本变化

不再是 review diff，而是 review：
- Agent 执行的完整日志
- 测试执行视频
- 实时运行的应用预览
- 环境变化的记录

这要求新的 review 工具和验收标准。

---

## Cursor 的数据：内部已大规模采用

Cursor 内部的数据非常有说服力：

| 指标 | 数值 |
|------|------|
| 内部 PR 由 Agent 创建的比例 | **35%**（云端 VM 上自主运行的 Agent）|
| Agent 使用量年增长 | **>15x** |
| Tab vs Agent 用户比例变化 | 从 2.5:1（Tab 领先）→ 1:2（Agent 领先）|

> 这些是 Cursor **自己**的开发者使用数据，不是对外宣传的愿景数字。

---

## 笔者的判断：为什么这个转变比想象中更快

多数观察者低估了第三代落地的速度，原因在于**低估了 Artifact 机制的作用**。

当 Agent 运行在云端数小时后返回的不是一个代码 diff，而是一段视频、一个可点击的预览、一份完整日志时，开发者的 review 成本大幅降低——你不需要重建 session，只需要判断「这个输出是否符合预期」。

这种机制使得**多 Agent 并行**从理论变为实践：
- 一个 Agent 写前端
- 一个 Agent 写后端
- 一个 Agent 做测试
- 一个 Agent 做部署

开发者从「管理者」变成「验收者」。

---

## 与 OpenAI Codex 的分野：为什么 Cursor 的路径更值得关注

OpenAI 强调 Codex 的 **「Work with Codex from anywhere」**——强调的是**接入的便捷性**（远程 SSH、浏览器内代码执行）。

Cursor 强调的是**架构的转变**（从同步到异步，从单 Agent 到 fleet）。

这两条路径都在解决同一个问题：如何让 Agent 完成更大规模的任务。但：

- **OpenAI 的方案**：解决「如何把 Codex 用起来」的问题（接入层创新）
- **Cursor 的方案**：解决「如何让 Agent 真正自主工作数小时」的问题（架构层创新）

笔者认为，Cursor 的方向代表了更深层的范式转变——**第三代的门槛不是「能不能远程连接」，而是「Agent 能否在没有人介入的情况下完成一个完整的开发任务」**。

---

## 结论：开发者应该做什么

1. **接受这个转变的必然性**：第三代不是「更高级的工具」，而是工作方式的根本变化
2. **重新设计 review 流程**：从 review diff 转向 review artifact、logs、preview
3. **投资环境稳定性**：flaky test 在单 Agent 时代是小问题，在多 Agent 并行时代是灾难
4. **关注工具层的演进**：当 Agent 需要自主运行数小时，工具链的可靠性比模型能力更重要

Cursor 的判断是「一年后，绝大多数开发工作将由这类 Agent 完成」。这个预测激进，但考虑到 35% 的内部 PR 已经由这类 Agent 创建——这不是愿景，是已经发生的现实。

---

> **引用来源**：
> - "[The third era of AI software development](https://cursor.com/blog/third-era)", Cursor Blog, Feb 26, 2026
> - Cursor internal metrics (PR creation by autonomous cloud agents)