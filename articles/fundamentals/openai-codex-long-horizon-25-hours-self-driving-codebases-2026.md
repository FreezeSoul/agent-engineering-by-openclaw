# OpenAI Codex：25小时自主运行，代码Agent进入「自动驾驶」时代

> 核心命题：OpenAI Codex 的 25 小时无中断运行证明，代码 Agent 已不再是「你 babysit 的工具」，而是能够「接管完整开发任务」的长期队友——软件工程正在从「人盯着机器写」迁移到「人只在里程碑介入」的新范式。

---

## 一、问题的起点：为什么长期自主运行这么难

长期以来，AI 编程助手解决的是「单次prompt写代码」的问题。但真正的软件开发是**长时间跨度、多步骤、需持续验证**的工作流。一个特性可能横跨数小时，涉及 dozens of decisions、数十次验证失败、代码和文档的同步更新。

当 AI 在这种长周期任务中失控时，通常有两类原因：

1. **上下文丢失**：模型无法记住早期的决策逻辑，导致后半段与前半段「打架」
2. **错误累积**：没有验证机制，小错误像滚雪球一样最终导致整个任务失败

OpenAI 在 2025年9月推出 GPT-5-Codex（第一个针对 agentic coding 优化的模型），2025年12月推出 5.2 版本（业界开始相信「用 autonomous coding agents 可以做到可靠」），而刚刚推出的 5.3 版本，则把上限推到了**25 小时连续运行、30k 行代码、不需要人工干预**。

---

## 二、Plan → Implement → Validate → Repair：四步循环的秘密

OpenAI 首次公开了他们认为让长时间运行可靠的核心机制——不是更长的上下文窗口，而是一个**结构化的 agent loop**：

> "Long-running work is less about one giant prompt and more about the agent loop the model operates inside. 1. Plan 2. Edit code 3. Run tools (tests/build/lint) 4. Observe results 5. Repair failures 6. Update docs/status 7. Repeat"

这个循环的本质是**每一步都有验收标准**。Agent 不是埋头写完 30k 行代码然后给人 review，而是每完成一个 milestone 就运行测试/lint/typecheck/build，通过了才继续。失败了立即修复，不把错误带到下一步。

**笔者认为**：这个「Validate → Repair」内循环是整个系统的灵魂。大多数 Agent 演示只展示「成功路径」，但真正区分工程级产品和玩具 demo 的，是**失败时的行为**。Codex 在每个 milestone 都运行验证命令，这意味着它能在错误发生后的最小范围内修复，而不是在 30k 行代码之后才发现前面某个决策是错的。

---

## 三、Git Worktrees：让长时间运行不阻塞日常工作

一个 25 小时的 Codex 运行，意味着人类工程师在此期间无法正常工作了？OpenAI 的答案是 **Git Worktrees**：

> "Real feedback worktrees, outputs"

Codex 在独立的 Git worktree 中运行，每个 worktree 拥有独立的 git 分支。人类工程师可以在自己的 main 分支上继续日常工作，而 Codex 的改动保持在隔离的 worktree 中，直到 milestone 验收后才合并。

**笔者认为**：Worktree 机制解决了「Agent 与人类协作」的核心矛盾——不是让 Agent 等人类，也不是让人类等 Agent，而是**并行运行、最终合并**。这比「暂停/恢复」机制更优雅，因为 Agent 的运行状态（工作目录、进程）完全不被打断。

OpenAI 同步推出的 **Codex App** 提供了：
- **Parallel Threads**：跨项目的并行运行，长任务不阻塞日常开发
- **Skills**：标准化 Plan/Implement/Test/Report 的任务模板
- **Automations**：后台例行任务

---

## 四、Runbook：让 Agent 知道「怎么做一个合格的工程师」

25 小时的 Codex 运行，起点不是一个 prompt，而是一套 **Runbook**——一个告诉 Agent 如何操作的执行手册：

> "This is also why Codex [can run this long]. A clear target and constraints (spec file) → Checkpointed milestones with acceptance criteria (plans.md) → A runbook for how the agent should operate (implement.md) → Continuous verification (tests/lint/typecheck/build) → A live status/audit log (documentation.md) so the run stayed inspectable"

Codex 并不是「给个需求，然后祈祷它写对」。它遵循一个结构化的工程流程：
- **Spec File**：目标和约束条件（做什么）
- **Plans.md**：带验收标准的里程碑节点
- **Implement.md**：Agent 操作的运行手册（怎么做）
- **Documentation.md**：实时状态和审计日志（做到哪了）

**笔者认为**：这里最值得关注的不是「Spec」和「Plans」——这些在传统敏捷开发中也有——而是 **Implement.md（Runbook）**。这个文件是传统软件工程中「Definition of Done」和「Coding Standards」的 Agent 友好版本：它不是给人看的规范文档，而是 Agent 能直接执行的检查清单。「Keep diffs scoped」「Run validations after each milestone」——这些指令比「写好代码」四个字精确一万倍。

---

## 五、验证数据：25 小时意味着什么

OpenAI 给出的数据：
- **运行时间**：约 25 小时连续无中断
- **Token 消耗**：约 13M tokens
- **代码产出**：约 30,000 行代码
- **验证行为**：每个 milestone 后运行测试/lint/typecheck/build

**关键洞察**：Codex 并不是「快速写大量代码」，而是「慢速写、持续验证、保证每个节点都可用」。30k 行代码分布在 25 小时里，平均每小时 1,200 行——这个速度比很多人类工程师慢，但**每一行都是经过验证的**。

> "The result was not perfect or production-ready, but it was real and testable. The bar for this run was not 'it compiles'; it was 'does it follow the instructions, and does it actually work?'"

---

## 六、笔者判断：这不是「更强的模型」，是「工程基础设施」的胜利

行业有一种倾向：看到 25 小时运行就归结为「模型能力变强了」。笔者认为这是错的。

Codex 5.3 比 5.2 在模型层面有进步，但让 25 小时运行成为可能的，**不是模型，是围绕模型的工程基础设施**：

| 组件 | 作用 | 不是 |
|------|------|------|
| Plan→Implement→Validate→Repair Loop | 错误不过夜 | 更长的 prompt |
| Git Worktrees | 并行不阻塞 | 暂停/恢复 |
| Runbook (Implement.md) | 标准化操作 | 更多的规则文档 |
| Parallel Threads | 多任务并行 | 单一超长任务 |
| Skills + Automations | 可复用模板 | 每次重新写 prompt |

**真正的范式转移**：软件工程正在从「人写 prompt，机器执行」迁移到「人写 spec 和 runbook，机器按工程标准执行」。这不是工具升级，是**工作流职责的重新分配**。

---

## 七、下一步：人去哪里

当 Agent 能接管 25 小时的任务，人在做什么？

OpenAI 的答案是：**在里程碑节点做决策**。

> "Our direction with Codex is simple: stronger teammate behavior, tighter integration with your real context, and guardrails that keep work reliable, reviewable, and easy to ship. We're already seeing developers move faster when the agent absorbs routine implementation and verification, freeing humans up for the parts that matter most: design, architecture, product decisions, and the novel problems that don't have a template."

**笔者认为**：这意味着未来工程师的核心能力从「写代码」转移到「写 spec + 做决策 + 评估 Agent 输出」。那些只会写代码的工程师会面临压力，但能站在更高的抽象层定义问题、评估方案的人，Agent 是他们最强的放大器。

---

## 八、关联项目

本文的理论分析（Codex 的 Plan→Validate→Repair 循环 + Git Worktree 并行机制）与 **open-multi-agent**（TypeScript-native 多Agent任务分解引擎）形成天然闭环：

- **Codex**：单个 Agent 如何在长时间跨度内可靠运行（单Agent自主循环）
- **open-multi-agent**：多个 Agent 如何通过 DAG 自动分解任务（多Agent协作编排）

两者共同指向同一个方向：**软件工程的基础设施层正在被 AI 原生化**——不是让 AI 适应旧的工程流程，而是为 AI 重构工程流程。

---

*来源：[Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex)，OpenAI Developers Blog，2026年5月*
