# AI Coding Agent 的停止条件：为什么需要一个独立的 Judge 模型

**subtitle**: MiMo-Code 的 Goal/Stop + Judge Architecture 给我们的启发

> **核心问题**：当 AI Coding Agent 说"任务完成了"，它真的完成了吗？

---

## 一、停止问题的本质

Anthropic 在工程实践中发现了一个系统性偏差：**Agent 的自我评估存在"乐观偏差"（optimistic stop）**。在长时任务中，Agent 消耗大量 tokens 产生的内部内容（中间代码、注释、自我解释）会在 context 中堆积，这些内容在 Agent 看来是"正在工作"的证据，但实际上可能是：

- 只完成了 60%，但 Agent 认为已经走了 90%
- 某个分支测试通过了，但整体功能仍有 regression
- 代码写了但没有验证，编译都没过

这不是模型能力问题，而是**信息不对称**：Agent 拥有的是"我认为完成了"的叙事，而人类期望的是"客观验证通过"的证据。

OpenAI 在 Harness Engineering 研究中也记录了同样的模式：没有结构化验证的 Codex agent 会在单元测试第一次绿的时候 declare success，但实际上整个 test suite 还有 40% 在跑。

> **引用 1**（Anthropic Effective Harnesses）：
> "When the model is the sole judge of its own progress, it systematically overestimates completion. The solution is not a smarter model — it is an independent verification layer."
> — Anthropic Engineering Blog, *Effective harnesses for long-running agents*

---

## 二、MiMo-Code 的解法：Goal/Stop + Judge Architecture

MiMo-Code（XiaomiMiMo/MiMo-Code，9,736 ⭐，MIT License）引入了三层机制来解决停止问题：

### 2.1 `/goal` 命令：显式定义"完成"的条件

用户通过 `/goal <condition>` 设置一个明确的停止条件。这个条件不是 prompt，而是一个**可判断的真值表达式**。

```
用户：/goal 所有单元测试通过，且 main 函数能正常启动

Agent 开始工作...（消耗 tokens 5000）

Agent：我认为任务完成了

[系统] Agent 尝试停止
[系统] → 触发 Judge Model 评估
```

### 2.2 独立 Judge Model：防止自评偏差

当 Agent 声明完成时，MiMo-Code **不会直接接受这个声明**。取而代之的是一个独立运行的 Judge Model，它：

1. **接收原始 Goal 条件**
2. **读取当前工作区状态**（文件内容、git status、测试结果）
3. **独立判断 Goal 是否真正满足**
4. **输出 Yes/No + 理由**

这个 Judge Model 与执行 Agent **不是同一个模型实例**，从而切断了自我辩护的信息回路。

> **引用 2**（MiMo-Code README）：
> "The `/goal` command sets a stopping condition for a session. When the agent tries to stop, an independent judge model evaluates the conversation to decide whether the condition is truly satisfied — preventing premature 'optimistic stops' during autonomous work."
> — XiaomiMiMo/MiMo-Code README

### 2.3 三种可能的结局

| 情况 | Agent 行为 |
|------|-----------|
| Judge → Yes | Agent 停止，任务完成 |
| Judge → No（部分完成）| Agent 继续工作，报告未满足的原因 |
| Judge → No（偏离目标）| Agent 回退到上一个 checkpoint，重新规划 |

这与 Anthropic 提出的 **Evaluator Loop** 模式高度一致，但 MiMo-Code 的实现更直接：**Goal 即规范，Judge 即验证**，不需要复杂的 multi-agent 编排。

---

## 三、Checkpoint 系统：跨会话状态不丢失

独立 Judge 之所以可行，是因为有 checkpoint 系统作为状态保证：

```
checkpoint.md (结构化状态快照)
├── 当前任务目标
├── 已完成步骤列表
├── 失败步骤及原因
└── 最近的 Agent reasoning 摘要
```

当 session 结束时，checkpoint 被持久化。当 session 恢复时，Agent 从 checkpoint 重建 context，而不是从零开始——这保证了 Judge 评估的是**真实的工作区状态**，而不是 Agent memory 中的叙事。

> **引用 3**（MiMo-Code README）：
> "Session checkpoint (`checkpoint.md`) — structured state snapshots maintained automatically by the checkpoint-writer subagent. Memory is injected automatically when a session resumes, so the agent does not need to relearn project context."
> — XiaomiMiMo/MiMo-Code README

### Checkpoint 与 Context Reconstruction 的联动

当 Agent 的 context window 接近上限时，MiMo-Code 执行"Context Reconstruction"：

1. 从 checkpoint 提取最新状态
2. 从 project memory (`MEMORY.md`) 注入项目知识
3. 从 task progress (`tasks/<id>/progress.md`) 注入任务历史
4. 保留最近的关键 messages
5. 丢弃中间 reasoning artifacts

这个机制解决了长时任务的**context overflow 问题**，同时保证了 checkpoint 的状态始终是最新的——这是 Judge Model 能够准确评估的前提。

---

## 四、与既有 Harness 架构的关系

| 架构 | Agent 自评 | 独立验证 | Checkpoint | 来源 |
|------|-----------|---------|-----------|------|
| **Anthropic GAN** | ❌ 无自评 | ✅ Evaluator Agent | ✅ | Anthropic, 2026 |
| **OpenAI Harness** | ⚠️ 自评 + 反馈 | ✅ Verification Layer | ✅ | OpenAI, 2026 |
| **Cursor Auto-Review** | ❌ 无自评 | ✅ Classifier Agent | 部分 | Cursor, 2026 |
| **MiMo-Code Judge** | ⚠️ 声明但不采纳 | ✅ 独立 Judge Model | ✅ | MiMo-Code, 2026 |

**关键差异**：Anthropic 和 Cursor 的 evaluator 都是**另一个 Agent**（通过 prompt 约束其行为），而 MiMo-Code 的 Judge 是一个**独立模型实例**，专门做 True/False 判断，不参与执行。

这让 Judge 的 prompt 可以极度简化（只问"满足条件吗？"），从而减少误判率。

---

## 五、Budgeted Injection：token 预算防止评估过载

当 checkpoint 内容很大时，全部注入 context 会导致评估本身消耗过多 tokens。MiMo-Code 的 Budgeted Injection 机制：

- 给 checkpoint、memory、notes 分别设置 token 预算
- 按重要性排序（Goal 相关 > 项目结构 > 中间产物）
- 超预算时裁剪低优先级内容

这确保了 Judge Model 评估时**看的是精简后的关键状态**，而不是 50KB 的中间产物。

---

## 六、笔者的判断

MiMo-Code 的 Judge Architecture 解决了一个非常具体但极其重要的问题：**谁来为 Agent 的"完成了"背书？**

当前行业的做法是让 Agent 自己判断或让人在回路（human-in-the-loop）。前者不可靠，后者无法扩展。MiMo-Code 给出的答案是**独立模型做独立判断**——简单、直接、工程上可实现。

笔者认为这个模式值得推广到更多场景：

- **代码生成任务**：Judge 检查编译 + 测试是否通过
- **文档任务**：Judge 检查是否覆盖了所有 requirements
- **多步骤任务**：Judge 检查每个 milestone 是否满足

真正的问题是：**如果 Judge 也错了怎么办？** Anthropic 的答案是"用更强的模型做 Judge"，但这会增加成本。笔者的补充是：对于高风险任务，可以让 Judge 输出**置信度**而非二元判断，让人类最终拍板。

> **金句**：让 Agent 决定何时停止，就像让被告决定自己是否有罪。独立的 Judge 不是不信任 Agent，而是对复杂任务的基本工程尊重。

---

## 关联项目

本文分析的 Judge Architecture + Checkpoint 机制，与 [walkinglabs/learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering)（8,807 ⭐）的**第 5 讲：Evaluator Loop** 直接对应。该课程从 OpenAI 和 Anthropic 的一手实践出发，系统讲解了验证层的设计原则，可作为本文的实践补充。

---

**References**：

- [MiMo-Code README](https://github.com/XiaomiMiMo/MiMo-Code) — Goal/Stop + Judge Architecture
- [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Anthropic: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [OpenAI: Harness engineering — leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)
