# Anthropic GAN 架构三要素：长时运行 Agent 的 Harness 设计新范式

> **核心判断**：Anthropic 的最新实验表明，Generator-Evaluator 分离 + Context Reset 组合能有效突破长时 Agent 的两大天花板——上下文漂移和自我评价失真——这才是真正面向生产的 Agent 架构。这不是对现有框架的增量改进，而是对 Agent 自我盲点的根本性重构。

---

## 背景：为什么长时 Agent 容易「脱轨」

Anthropic 在 2026 年 3 月发布的文章 *Harness design for long-running application development* 中，工程师 Prithvi Rajasekaran 指出了一个困扰行业许久的问题：

> "For more complex tasks, **the agent still tends to go off the rails over time**. While decomposing this issue, we observed two common failure modes with agents executing these sorts of tasks."

两个核心失效模式：

1. **上下文窗口饱和导致连贯性丧失**：模型在处理长序列时，上下文积累到一定程度后，开始丢失前期信息或产生矛盾推理。
2. **自我评价失真**：Agent 对自己产出的评价显著偏正面，无法有效识别质量缺陷——尤其是主观质量（设计品味、创意独特性）。

---

## 第一个设计决策：Context Reset 而非 Compaction

传统做法是 **Compaction**（上下文压缩）——将历史对话摘要压缩后保留在同一 Agent 的上下文中。Anthropic 通过实验发现，Compaction 对某些模型（如 Claude Sonnet 4.5）存在「上下文焦虑」问题：模型会预判自己即将达到上下文上限，从而过早收束工作。

Anthropic 的解法是 **Context Reset**：

> "Context resets—clearing the context window entirely and starting a fresh agent, combined with a structured handoff that carries the previous agent's state and the next steps—addresses both these issues."

关键差异：

| 机制 | Compaction | Context Reset |
|------|-----------|---------------|
| 上下文状态 | 在同一 Agent 内压缩保留 | 彻底清空，新 Agent 接手 |
| 上下文焦虑 | 无法消除 | 完全消除 |
| 状态连续性 | 自然保持 | 依赖 handoff artifact 传递 |
| Token 开销 | 渐进累积 | 每次 Reset 有固定开销 |

Anthropic 明确指出，这不是替代 Compaction，而是针对特定场景的补充方案。当任务足够长、模型表现出上下文焦虑时，Reset 提供的「干净白板」效果是不可替代的。

---

## 第二个设计决策：Generator-Evaluator 分离

更关键的设计来自对 **自我评价问题** 的分析。Anthropic 指出：

> "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre."

这个现象在主观质量领域（UI 设计、创意写作）尤为突出，但在有可验证输出的任务中同样存在。传统做法是让同一个模型同时负责生成和评价，但 Anthropic 发现这产生了结构性盲点——模型对 LLM 生成的内容存在系统性宽容偏差。

分离后的架构优势：

> "Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue."

Evaluator 不再是生成者的「影子」，而是独立的质量把关角色。Anthropic 强调：

> "Tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work, and once that external feedback exists, the generator has something concrete to iterate against."

---

## 落地：面向前端设计的三要素评分体系

Anthropic 在前端设计任务中验证了这套架构，设置了四层评分标准，并**明确将 Design Quality 和 Originality 权重置于 Craft 和 Functionality 之上**：

| 评分维度 | 核心问题 | 设计动机 |
|---------|---------|---------|
| **Design Quality** | 设计是否形成统一整体而非部件堆砌？ | Claude 默认倾向于安全的「AI 风格」，需要强制引导 |
| **Originality** | 是否存在定制化决策，还是模板化输出？ | 明确惩罚「紫色渐变 + 白色卡片」等 AI 生成痕迹 |
| **Craft** | 技术执行（排版、间距、色调和谐） | Claude 在这维度本已表现良好，权重最低 |
| **Functionality** | 可用性（用户能否完成任务） | 同上，基础能力不需要过度强调 |

这个评分体系本身就揭示了一个重要洞察：**Claude 的能力短板不在技术实现层，而在审美判断和原创性层**。因此，评价体系的设计必须「扬长补短」，而非面面俱到。

---

## 最终架构：Planner-Generator-Evaluator 三 Agent 协同

基于以上两个设计决策，Anthropic 构建了三 Agent 架构：

```
[Planner Agent]
  → 将产品需求分解为任务列表 + 结构化 Handoff Artifact

[Generator Agent]
  → 基于 Artifact 执行具体编码/设计任务
  → 输出到 Evaluator

[Evaluator Agent]
  → 独立评价输出质量
  → 不宽容，给出具体的改进意见
  → 驱动 Generator 迭代优化
```

这是一个 GAN-inspired（生成对抗网络启发）的架构——Generator 的对手不是判别器（Discriminator），而是独立的 Evaluator Agent。两者通过多轮反馈循环持续优化输出质量。

---

## 工程含义：对现有 Agent 框架的挑战

Anthropic 的实验结果对当前主流 Agent 框架设计有直接启示：

**不是所有任务都需要三层 Agent**。对于简单的一次性任务，单 Agent + 工具调用的模式完全足够。但对于：
- 长时间跨度的多会话任务
- 主观质量重要的创作类任务  
- 需要自我纠错能力的复杂编码

三 Agent 架构提供了可复用的设计模式。

**Context Reset 的工程代价需要被接受**。每次 Reset 意味着重新初始化 Agent 状态、生成 handoff artifact、以及在下一个 Agent 中恢复上下文。这是可量化的 Token 开销和延迟增加，但换来的是可预测的执行质量。

**Evaluator 的「不宽容」是可调节的**。Anthropic 通过 few-shot 校准让 Evaluator 的判断与人类偏好对齐，而非让其盲目严苛。这意味着 Evaluator 的 prompt 设计本身是生产级调优的关键。

---

## 笔者的判断

Anthropic 这篇文章的核心贡献，不是提出了一个新框架，而是通过**解构长时 Agent 失效模式**找到了两个根本原因，并给出了有实验支撑的解法。

Context Reset 解决的是 Agent 与生俱来的「记忆焦虑」问题——这在单 Agent 架构里几乎无法消除。Generator-Evaluator 分离解决的则是 LLM 自我评价的系统性偏差——这个问题在社区实践中被反复观察到，但缺乏像样的系统性分析。

笔者认为，这套三要素架构的影响会持续到 2027 年。对比当前主流的单 Agent 方案，它的额外工程复杂度是真实的——Planner 的分解质量、Artifact 的状态携带能力、Evaluator 的校准精准度，每一环都需要独立维护。但对于需要真正自主完成数小时级任务的场景，这个复杂度是值得的。

原文链接：[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)（Anthropic Engineering Blog, 2026-03-24）