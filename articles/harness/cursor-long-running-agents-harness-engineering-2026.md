# Cursor Long-Running Agents：前端模型的 Harness 工程范本

> 原文：https://cursor.com/blog/long-running-agents
> 产出时间：2026-06-03

---

## 核心命题

**Cursor  Long-Running Agents 不是一个新的模型能力，而是一套经过系统性工程设计的 Harness 架构——它解决的问题不是"模型有多强"，而是"如何让强模型在长周期任务中稳定交付"**。

---

## 为什么长周期任务是 Agent 工程的关键难题

当一个任务需要 36 小时才能完成时会发生什么？Cursor 团队在用自主编码 Agent 构建浏览器的实验中发现，前沿模型在长周期任务上会以**可预测的方式失败**：

- 前期的一个小错误假设，在 36 小时后可能演变成完全错误的解决方案
- 模型会遗忘宏观目标，在局部细节中迷失
- 任务进行到一半就停止，只完成部分工作
- 代码质量参差不齐，缺乏系统性测试覆盖

这些失败模式指向一个核心矛盾：**tight prompt-response loop（紧密的提示-响应循环）适合监控短期任务，但无法支撑需要数小时乃至数天才能完成的复杂目标**。

---

## Cursor 的 Harness 核心设计原则

### 原则一：先规划，再执行（Plan Before Execution）

> "Long-running agents in Cursor propose a plan and wait for approval instead of immediately jumping into execution, recognizing that upfront alignment reduces the need for follow-ups."
> — Cursor Engineering Blog

传统的交互模式是"你说我做，做完再汇报"。Long-Running Agents 的模式是"你先告诉我你要做什么，我制定计划，你批准后再动手"。

这不是一个 UX 改进，而是一个**认知负荷重新分配**的工程决策：
- 模型在执行前必须显式化其对任务的理解
- 人类审批者在行动前能看到全局路径，而非被一个个碎片化的"是否允许执行"打断
- 减少了后期修正的成本——一个规划阶段的修正远比 30 小时后的返工便宜

### 原则二：Multi-Agent 交叉检查（Multiple Agents Checking Each Other's Work）

> "Following through on tasks: Frontier models can write great code, but often forget the big picture of their task, lose track of what they're doing, or stop at partial completion. Long-running agents use a plan and multiple different agents checking each other's work in order to follow through on larger, more complex tasks."
> — Cursor Engineering Blog

Cursor 没有依赖单一 Agent 独自完成整个任务，而是在 Harness 层引入了**多个 Agent 互相检查**的机制。这解决了单一 Agent 的几个核心问题：

1. **遗忘问题**：一个 Agent 负责执行，另一个 Agent 负责对照原始计划审视进度
2. **部分完成问题**：检查 Agent 可以识别"已经完成"和"需要继续"之间的差距
3. **质量一致性问题**：交叉检查比单 Agent 自审更能发现隐蔽的缺陷

这与 LangChain 的 [RubricMiddleware](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/harness/langchain-rubricmiddleware-evaluator-loop-self-improving-agents-2026.md) 形成了有趣的对比——RubricMiddleware 用一个独立的 Grader Sub-Agent 做判断，Cursor 用多个 Worker Agent 做交叉检查，两者都是"分离评估者"思路的工程实现。

### 原则三：让 Agent 能"跑完"（Following Through）

Cursor 的 Long-Running Agents 实验中最引人注目的数据是：

- **36 小时**：从零构建一个集成现有开源工具的聊天平台
- **30 小时**：基于现有 Web 应用实现一个移动端 App
- **25 小时**：重构认证和 RBAC 系统
- **151k 行代码**：一个用户用 52 小时任务产出了 15 万行合并代码

这些数字背后的工程意义是：Harness 必须能够支撑 Agent **不受人类干预地运行数十小时**，期间用户可以关闭笔记本、去开会、第二天回来看到已完成的工作。

这要求 Harness 具备：
- **状态持久化**：Agent 中断后能从断点恢复
- **文件系统边界**：防止 Agent 污染工作区之外的代码
- **进度追踪**：让人类能够理解 Agent 在哪个阶段、完成了多少

---

## 与 Claude Code 的 Auto Mode 有何不同

Cursor 的 Long-Running Agents 与 Anthropic 的 [Claude Code Auto Mode](https://www.anthropic.com/engineering/claude-code-auto-mode) 解决的是同一个问题——减少人类在 Agent 执行过程中的频繁审批——但路径不同：

| 维度 | Claude Code Auto Mode | Cursor Long-Running Agents |
|------|----------------------|----------------------------|
| **核心思路** | 让模型自己判断何时需要人类批准 | 让人类先批准计划，模型按计划执行 |
| **交互模式** | 事后审批（执行中/后） | 事前审批（执行前） |
| **任务粒度** | 单个 Action | 完整 Feature/Refactor |
| **多 Agent** | 不涉及 | Planner/Worker/Checker 协作 |
| **适用场景** | 开发者日常编码 | 复杂长周期项目 |

从 Harness 设计的角度看，Claude Code Auto Mode 是**在模型层（Model Layer）解决审批疲劳问题**——通过让模型自己判断安全性来减少人类的决策负担。Cursor 的 Plan-Before-Execution 是**在环境层（Environment Layer）解决对齐问题**——通过提前对齐减少模型偏离目标的可能性。

两者并不矛盾，而是互补的防御深度。

---

## Long-Running Agents 的工程挑战

Cursor 团队坦诚分享了长周期 Agent 面临的实际工程问题：

### 1. 代码质量管控

> "The magical part of the new harness is allowing the same model to make something production-ready. I tested the same bug-fix prompt locally vs. with a long-running agent, both with Codex 5.3. The local agent fixed it fairly quickly, but the long-running one went further to find edge cases, fix similar occurrences, and create high-coverage tests."
> — Tejas Haveri, CTO, DevAccel-Labs

长运行时 Agent 的一个反直觉发现是：**它们产生的代码比同步短任务 Agent 的代码更接近生产级**。原因是 Agent 有更多时间探索边界情况、增加测试覆盖、自检代码质量。

但这要求 Harness 提供足够的 Token 预算和上下文管理能力，否则 Agent 会在中途"耗尽注意力"。

### 2. 工具调用准确性

对于需要 Sudo 的系统管理任务，Agent 面临的挑战是：**一旦遇到权限问题，整个任务链就会中断**。Cursor 的解决方案是让 Long-Running Agent 实现了一个 Secure Sudo Password Prompting 机制——在遇到需要提权的命令时，Agent 能够正确地处理 Unix 认证流程，而不是直接失败或尝试绕过安全机制。

### 3. 自我修复的边界

Long-Running Agent 会尝试自我修复，但这有一个隐含的边界：**如果原始计划本身是错误的，Agent 的自我修复只会让它更快地完成一个错误的目标**。这正是"Plan Before Execution"原则如此重要的原因——在计划阶段的对齐能防止后续所有工作都偏离正确方向。

---

## 对 Harness Engineering 的启示

Cursor 的实践揭示了一个重要的行业趋势：**2026 年的 Agent 竞争，已经从"模型能力"扩展到了"Harness 工程能力"**。

当所有主要模型厂商的能力都在快速追赶时，如何让一个强模型在 36 小时的长周期任务中稳定工作，成为了区分产品体验的关键。这要求 Harness 在以下维度系统性地设计：

1. **规划层**：任务分解 → 计划审批 → 执行监控
2. **记忆层**：跨会话状态持久化，进度可恢复
3. **检查层**：多 Agent 协作，交叉验证完成度
4. **安全层**：沙箱隔离、权限控制、Sudo 处理
5. **资源层**：Token 预算管理、上下文压缩、长期记忆卸载

LangChain 的 [Deep Agents](https://github.com/langchain-ai/deepagents)（后文项目推荐会详细展开）是目前最完整的开源 Harness 实现之一，它将 Cursor 博客中描述的这些工程决策系统化地落地为了开源代码——Sub-agents、Context management、Persistent memory、Human-in-the-loop、Skills，每一个特性都对应着 Long-Running Agents 揭示的某个工程维度。

---

## 结语

> "We are working on improving collaboration across long-running agents so they can break up bigger projects into parallel work streams and take on even more ambitious projects with less human intervention."
> — Cursor Engineering Blog

Cursor 的 Long-Running Agents 揭示的不是一个功能，而是一个**工程级别的认知转变**：Agent 的价值不仅在于"能做什么"，更在于"如何在人类不全程监控的情况下完成复杂任务"。

这个转变要求我们把 Agent 视为一个需要系统性工程的系统，而非一个只需要强大模型的单点问题。

---

**关联项目**：推荐阅读 [LangChain Deep Agents：开源的"Batteries-Included"Agent Harness](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/projects/langchain-deepagents-harness-framework-2026.md)，了解如何用开源代码实现 Cursor 博客中描述的 Harness 设计。
