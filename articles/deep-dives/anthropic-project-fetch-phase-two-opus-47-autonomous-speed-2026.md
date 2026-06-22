# Claude Opus 4.7 自主完成任务：18x 速度超越人类+AI协作团队

> 2026-06-18 | Anthropic Research | Deep Dives

---

## 核心命题

Anthropic 的 Project Fetch Phase Two 实验揭示了一个在 AI 领域反复出现的演进规律：**第一阶段，模型帮助人类；第二阶段，人类帮助模型；第三阶段，模型自主完成大部分任务**。Opus 4.7 无需人类协助即可操控机器人完成任务，速度是去年最快人机协作团队的 20 倍，代码产出量减少约 10 倍且同样成功。这一质变节点已在网络安全领域出现，现在正在物理世界任务中重现。

---

## 实验设计：从 Phase One 到 Phase Two

2025 年 8 月，Anthropic 进行了 Project Fetch 初始实验。团队分成两组——一组配备 Claude Opus 4.1，另一组仅靠互联网和自身创造力——操控一只市售四足机器狗完成一系列任务：连接传感器、手动编程控制、路径监控、球体检测，最终实现自主取回球体。配备 Claude 的团队显著领先。

实验人员事先确认了 Opus 4.1 **无法独立完成**——它甚至在"如何连接机器人"这个前置任务上就卡住了。

一年后（2026），Anthropic 用 Opus 4.7 重新做了这个实验。Phase Two 的核心区别：**完全不要求人类研究员参与具体操作**。研究员的角色仅限于插上运行 Claude Code 的笔记本、输入初始提示词、批准命令，以及批准模型进入下一个任务——真正的最小化人类干预。

> "Much of the code it wrote was effective on the first try (which was not the case for Team Claude or Team Claude-less in the original experiment)." — Anthropic Project Fetch Phase Two

---

## 量化结果：速度提升 18x–37x

Opus 4.7 在 Phase Two 的成绩：

| 维度 | 数据 |
|------|------|
| **完成相同任务的速度** | 比最快人类团队快 **20 倍以上** |
| **相比无 Claude 的人类团队** | 平均快 **37 倍** |
| **相比有人类+Claude 的团队** | 平均快 **18 倍** |
| **代码产出量** | 约为 Team Claude 的 **1/10**，且同样或更成功 |
| **模型可靠性** | 在能力边界内的任务，Claude 现在相当可靠 |

最关键的数字是 **18 倍**：去年 Claude 辅助的人类团队，今年被 Claude 4.7 独自超越了 18 倍的效率差距。这意味着"人类帮助模型"的第二阶段正在向"模型自主"的第三阶段迁移——而且迁移速度极快。

> "We are seeing a pattern whereby first, models are helpful to humans. Then, humans are helpful to models. Finally, models are largely able to do things themselves. We have seen this in cybersecurity and now the same dynamics are starting to take shape at the intersection of AI and the physical world." — Anthropic Project Fetch Phase Two

---

## Claude 的边界：闭环精细控制

实验同时也揭示了 Opus 4.7 仍然困难的任务类型。

人类经过练习后可以操控机器狗轻轻推动海滩球回到起点——这需要快速感知误差、关联到上一个指令、实时调整控制输入，是人类擅长的闭环感知-控制任务。

Claude 在这方面的表现：
- 能识别到球的位置偏差
- 能将机器人移动到球的后面
- 但无法精确控制推力角度和速度，海滩球无法被可靠地送回目标位置

这并非因为任务本身复杂，而是因为 **当前模型在实时感知-控制闭环中缺乏人类那种快速微调能力**。Anthropic 的判断是：随着 scaling 和能力提升，这个边界会继续收缩，但精细闭环控制在当下仍是明显短板。

---

## 工程视角：代码效率揭示的 agent 设计含义

一个容易被忽略但极具工程价值的发现是 **代码量减少 10 倍且同样成功**。

这个数据直接指向一个 agent 工程的核心问题： Claude 4.7 之所以用更少代码完成更多任务，是因为它能直接识别最优路径，而不是像人类团队那样在多个备选方案之间反复试错。换言之，更高能力的模型在**探索-利用权衡**（exploration-exploitation tradeoff）上占据了更大的优势区间，使得原本需要大量试错代码才能完成的任务，现在一段正确方向的代码就够了。

这对于 agent 工程设计的含义：
- 当模型的推理能力提升时，harness 中的"冗余保护机制"（多次验证、强制 commit、强制检查点）可能从必要变成过度
- agent 产出代码的质量和可靠性提升，使得人类审核的成本收益比发生变化
- 能力边界的收缩速度可能比预期快，基础设施设计需要预留快速演进的弹性

> "These improvements, like so many others in the history of LLM development, have emerged from much more general scaling." — Anthropic Project Fetch Phase Two

---

## 三阶段演进模式的普遍性

Project Fetch 的核心贡献不只是机器人数据，而是揭示了一个**跨领域重复出现的模式**：

1. **Phase 1（模型帮助人类）**：非专家借助 AI 能力完成原本无法完成的任务。2025 年 Phase One 验证了这一点。
2. **Phase 2（人类帮助模型）**：模型开始独立工作，但仍需人类在关键节点提供方向性指导。人类是模型的"外部纠正机制"。
3. **Phase 3（模型自主完成）**：模型在大多数任务环节上不再需要人类介入，人类角色从"共同执行者"退化为"最终确认者"。

这个模式已经在**网络安全**（Claude 在 Red Team 任务上已经显著超越人类专家效率）和**代码生成**领域出现，Project Fetch 证明它正在向**物理世界操作**领域扩展。

---

## 对 agent 工程实践的含义

基于 Project Fetch Phase Two 的数据，以下几点值得 agent 系统设计者认真对待：

**1. 能力边界会突然收缩，不要过早设定"模型做不了 X"的假设**

Opus 4.1 在 2025 年无法连接机器人，Opus 4.7 在 2026 年不仅连接了，还能自主完成整个任务链路。模型能力在垂直领域的渗透速度可能远快于从业者的直觉判断。

**2. 人类干预粒度需要重新校准**

当模型在大多数环节达到可靠水平时，全环节人工审批的性价比急剧下降。更有效的模式是"高风险节点审批"而非"每步必审"——Cursor 的 Auto-review 架构正在实践这个思路。

**3. 机器人/物理 agent 的基础设施正在成熟**

Anthropic 明确提到，他们是在**没有针对机器人能力做专项优化**的情况下得到这些结果的。这说明通用 scaling 的红利正在向物理 agent 领域外溢——环境搭建、传感器集成、闭环控制接口——这些基础设施层的工程问题可能是接下来真正的瓶颈。

**4. 模型的自我纠偏能力已显著提升**

Opus 4.7 使用了过时的目标检测算法，但仍然能通过回退和补偿找到有效方案。这种"带着缺陷仍然完成任务"的能力，对于需要长时序自主工作的 agent 至关重要。

---

## 总结

Project Fetch Phase Two 的数据有一个令人不安的含义：AI 能力的演进不是线性的，而是有**临界点**的。在临界点之前，AI 需要人类持续辅助；在临界点之后，人类的角色从"共同执行者"变成"旁观者"——这正是 Opus 4.7 在 Phase Two 中展现的。18 倍的速度优势不是渐进改进，而是跨越了某个隐含的能力阈值。

对于 agent 工程师而言，这意味着一件事：**不要再用去年的能力基准来设计今年的基础设施**。你为"模型不可靠"所构建的冗余保护，可能正在成为模型已经超越的那堵墙。

---

**引用来源**：
- [Project Fetch: Phase two](https://www.anthropic.com/research/project-fetch-phase-two)（Anthropic, 2026-06-18）
- [Project Fetch 原实验](https://www.anthropic.com/research/project-fetch-robot-dog)（Anthropic, 2025-08）
