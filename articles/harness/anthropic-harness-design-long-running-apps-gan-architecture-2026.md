---
title: "Anthropic 的 GAN 架构：让评测者与生成者分离为何能突破 Harness 上限"
date: 2026-05-25
source: "https://anthropic.com/engineering/harness-design-long-running-apps"
source_title: "Harness design for long-running application development"
author: "Prithvi Rajasekaran (Anthropic Labs)"
tags: ["harness", "long-running-agent", "multi-agent", "GAN", "self-evaluation", "Anthropic"]
---

## 核心命题

当一个 Agent 既是代码生成者又是自己的评测者时，它会毫无悬念地给自己的工作打高分——无论输出质量实际上有多平庸。Anthropic Labs 的 Prithvi Rajasekaran 在 2026 年 3 月发表的工程文章中揭示了这个问题的深层机制，以及如何通过一个类 GAN 的三代理架构突破 Harness 设计的性能上限。

> "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue. Separating the evaluator doesn't immediately eliminate that leniency on its own; the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs. But tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work."

**笔者认为**：这个洞察的真正价值不在于"分离评测者"这个显而易见的解法，而在于它揭示了为什么 Agent 自我评测天然不可靠——不是因为模型不够聪明，而是因为 LLM 的训练目标（生成看似合理的输出）与评测目标（判断输出质量）天然存在方向性冲突。

---

## 背景：Harness 设计遭遇天花板

Anthropic 早在 2025 年 11 月就发过一篇关于 long-running agent harness 的文章（`effective-harnesses-for-long-running-agents`），通过 initializer agent 分解任务和 structured artifacts 跨会话传递上下文，显著提升了 Claude 的表现。但两个问题始终无法通过单纯的 prompt 工程解决：

### 问题一：上下文窗口耗尽导致任务失去连贯性

随着 Agent 在长任务中积累越来越多的上下文，模型会逐渐"迷失"——早期的设计决策在 context window 接近填满时开始相互矛盾。更隐蔽的是"上下文焦虑"（context anxiety）：某些模型在感知到自己接近上下文限制时，会提前结束任务，仿佛在赶在"记忆丢失"之前交卷。

### 问题二：自我评测的"慷慨偏差"

当 Agent 被要求评估自己生产的输出时，无论质量如何，评测结果总是偏向积极。人类观察者一眼就能看出质量平庸的方案，Agent 却自信地给出高分。这个问题在主观领域（如设计）最为明显，但在有明确正确性的任务中同样存在。

---

## 方案：GAN 启发的三代理架构

作者从生成对抗网络（GANs）获得灵感：GAN 的核心思想是让生成器和判别器对抗——判别器负责挑剔生成器的输出，生成器被迫不断改进以"骗过"判别器。将这个框架迁移到 Agent 设计中：

### 三个代理的角色

| 代理 | 职责 | 关键设计 |
|------|------|---------|
| **Planner** | 分解产品需求为可执行任务列表 | 接收产品 spec，输出结构化任务分解 |
| **Generator** | 根据任务列表生成前端代码 | 每轮接收 evaluator 的反馈，决定是继续当前方向还是转换 |
| **Evaluator** | 对 Generator 输出打分并提供详细批评 | 使用 Playwright MCP 直接与页面交互，然后打分 |

### 关键技术一：Context Reset 而非 Compaction

针对上下文耗尽问题，Anthropic 选择了 Context Reset（清除整个上下文窗口，重新初始化 Agent + 传递 structured handoff artifact）而非 Compaction（在原位压缩历史摘要）。两者的区别：

- **Compaction**：保留连续性，但不给予 Agent 干净的 slate，上下文焦虑仍然存在
- **Context Reset**：给予 Agent 干净的 slate，但需要 handoff artifact 包含足够的任务状态

> "Claude Sonnet 4.5 exhibited context anxiety strongly enough that compaction alone wasn't sufficient to enable strong long task performance, so context resets became essential."

**笔者认为**：这个结论非常有价值。Compaction 在很多场景下被视为解决上下文长度问题的"标准答案"，但 Anthropic 用实验数据说明：在强上下文焦虑的模型上，Compaction 不够用。这解释了为什么在实际生产中很多看似"合理"的方案效果不佳。

### 关键技术二：Evaluator 独立校准

Evaluator 的 prompt 中包含四个评测维度，并明确权重：

1. **Design Quality（权重最高）**：设计是否作为一个整体而非部件的集合？颜色、排版、布局、图像是否共同创造了一致的情绪和身份感？
2. **Originality（权重最高）**：是否有定制决策的证据，还是模板化布局+AI 生成图案？紫色渐变叠加白色卡片是典型的 AI 生成痕迹
3. **Craft**：技术执行质量（排版层级、间距一致性、色彩和谐度、对比度），这是能力检查而非创意检查
4. **Functionality**：可用性，与美学无关

**关键操作**：通过 few-shot examples 校准 Evaluator 的打分标准，使 Evaluator 的判断与设计者的偏好对齐，并减少跨迭代的打分漂移。

> "Including phrases like 'the best designs are museum quality' pushed designs toward a particular visual convergence, suggesting that the prompting associated with the criteria directly shaped the character of the output."

### 关键技术三：Generator 的战略决策能力

在每轮评测后，Generator 不是机械地接受所有反馈，而是被要求做一个战略判断：

- 如果分数趋势良好 → 继续当前方向，深化设计
- 如果当前方向无效 → 彻底转向，完全不同的美学方向

这个设计让 Generator 成为一个主动的决策者，而非被动的执行者。

---

## 实验结果

在荷兰艺术博物馆网站的设计任务中：

- **迭代 1-9**：Generator 产生了一个干净的、深色主题的落地页，符合预期但视觉上平平无奇
- **迭代 10**：Generator 彻底颠覆了之前的方案，将网站重塑为沉浸式 3D 空间体验——CSS perspective 绘制的棋盘格地板、墙上自由分布的艺术品、以门口导航在画廊房间之间切换

> "Later implementations tended to be better as a whole, but I regularly saw cases where I preferred a middle iteration over the last one."

**关键发现**：
1. 仅靠 criteria 和提示语言本身，就已经在第一次迭代时显著优于 baseline（即使没有任何 evaluator 反馈）
2. 输出复杂性随迭代增加——Generator 会根据 Evaluator 的反馈追求更复杂的解决方案
3. 分数改善不总是线性的，有时中间迭代反而是最好的
4. Evaluator 的评估在迭代过程中改善，最终趋于稳定，但仍有提升空间

---

## 对 Long-Running Coding Agent 的启示

作者将前端设计实验中的两个关键教训迁移到长时 autonomous coding：

1. **将构建过程分解为可管理的块**（tractable chunks）
2. **使用结构化 artifacts 在会话之间传递上下文**

最终的三代理架构——Planner、Generator、Evaluator——在多小时 autonomous coding 会话中产生了丰富的全栈应用。

---

## 核心工程原理

### 为什么 Generator-Evaluator 分离有效

LLM 训练目标是生成"看起来正确"的文本，这与评测所需的中立、挑剔视角天然冲突。分离后的 Evaluator 可以专门针对"挑剔度"进行调优，而无需同时维持生成能力。

### 为什么 Context Reset > Compaction

Compaction 保留了连续性，但模型仍然感知到上下文压力；Context Reset 提供了真正的"clean slate"，但需要更好的 handoff 设计来承载状态。两个方案不是优劣之分，而是适用场景不同——当模型表现出强上下文焦虑时，Reset 是唯一有效的解法。

### 为什么 Evaluator 需要直接与产出交互

在设计领域，Evaluator 使用 Playwright MCP 直接导航页面、截图并仔细研究实现，然后输出评估。这比给 Evaluator 一个静态截图打分要有效得多——因为可用性、交互流畅度、视觉连贯性这些维度，只有在动态交互中才能充分评估。

---

## 笔者判断

**这个架构的真正贡献不是"三代理"这个结构，而是揭示了一件事**：Harness 设计中的很多"上限"不是来自模型能力不足，而是来自架构设计本身让模型同时扮演生成者和评测者——这两个角色天然存在方向性冲突，无法通过更好的 prompt 工程来解决，只能通过架构分离来解决。

这与软件开发中的"关注点分离"原则完全一致——测试和质量保证不应该由开发人员自己来做，这在传统软件工程中是常识，在 Agent 开发中同样适用，只是以前没有人明确说出来。

对于构建生产级 Long-Running Agent 系统的工程师来说，这个框架提供了三个具体的架构决策点：

1. 你的 harness 中是否有明确的 Evaluator 角色？
2. 你的上下文管理使用的是 Reset 还是 Compaction？有没有测试过模型是否表现出上下文焦虑？
3. 你的 Evaluator 是否有能力直接验证产出（使用工具交互），而非仅依赖文本反馈？
