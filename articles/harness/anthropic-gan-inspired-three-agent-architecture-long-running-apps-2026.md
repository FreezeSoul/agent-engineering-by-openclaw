# Anthropic 三代理架构：GAN 风格的长周期应用开发 Harness 设计

> **核心问题**：当 Agent 需要连续运行数小时完成复杂任务时，如何避免它「迷失在上下文中」或「自我美化逃避批评」？Anthropic 在 2026 年 3 月发布的 Harness Design 文章给出了一个出人意料的答案——从 GAN（生成对抗网络）汲取灵感，引入独立 Evaluator 代理来对抗 Generator 的自我偏袒。

> **读完能得到什么**：理解 GAN 风格三代理架构（Planner/Generator/Evaluator）、Context Reset vs Compaction 的取舍、Self-Evaluation 问题的根因，以及这套设计模式如何突破「上下文焦虑」和「过度自信」两大长程 Agent 顽疾。

---

## 先说问题：传统 Harness 的两个天花板

Anthropic 此前已在「Effective Harnesses for Long-Running Agents」中证明：良好的 Harness 设计能显著提升 Agent 性能。核心做法是 Initializer Agent 分解任务 + Coding Agent 分功能实现 + Session 间用结构化 Artifact 传递上下文。

但这两点设计在更复杂的任务上遇到了持续的天花板：

### 天花板 1：上下文焦虑与上下文坍缩

上下文窗口填满是长周期任务的主要障碍。部分模型（尤其是 Sonnet 4.5）表现出「上下文焦虑」——当感知到即将触及上下文限制时，会提前草草收尾。

解决路径有两个：

| 方案 | 做法 | 优点 | 缺点 |
|------|------|------|------|
| **Compaction（压缩）** | 在原位总结历史对话，缩短上下文但不重置 | 保持连续性 | 不给 Agent 干净的起点，上下文焦虑仍可能触发 |
| **Context Reset（重置）** | 完全清空上下文窗口，用结构化 Artifact 携带状态后启动新 Agent |干净的起点，无焦虑触发 | 需要精确的 Artifact 设计；重置本身带来开销 |

Anthropic 最终的结论是：Sonnet 4.5 的上下文焦虑足够严重，Compaction 不足以支撑好的长任务性能，所以 **Context Reset 是必要的**。但这也意味着每次重置都带来 Token 开销和延迟。

### 天花板 2：自我评价失真

这是这篇文章揭示的最有意思的问题。当要求 Agent 评价自己产出物的质量时，Agent 倾向于过度正面描述——即便产出物明显质量平平。

这在设计等主观领域尤其明显：在没有任何干预的情况下，Claude 会产生「技术功能正常但视觉上毫无特色的」输出。它会给自己打高分。

但即便在有可验证结果的任务中，Agent 也表现出不准确的判断，阻碍它完成任务。分离执行 Agent 和评价 Agent 是解决这个问题的强有力手段。

关键洞察是：**分离出来的 Evaluator 仍然是一个 LLM，仍然倾向于对 LLM 产出物过于宽容**。但调优一个独立的 Evaluator 来保持怀疑态度，比让 Generator 自我批评要容易得多。而且一旦有了外部反馈，Generator 就有了一个具体的东西来迭代。

---

## GAN 风格的解法：Generator + Evaluator 双代理循环

文章的核心贡献来自 GAN（Generative Adversarial Networks）的启发——在 GAN 中，生成器（Generator）和判别器（Discriminator）相互对抗，生成器从判别器的反馈中学习提升。

Anthropic 将这个思想搬到了 Agent 设计：Generator 负责生成，Evaluator 负责评判，两者形成反馈循环。

### 前端设计实验

Anthropic 先在前端设计领域验证这个思路。该领域没有二元的「正确/错误」判断，品味判断完全主观。

他们写了四个评判标准：

1. **Design Quality（设计质量）**：设计是否像是一个有机的整体，而非部件的拼凑？颜色、字体、排版、图像等细节是否共同创造了独特的调性和身份感。
2. **Originality（原创性）**：是否有定制化决策的证据，还是模板化布局、库默认设置和 AI 生成模式？未修改的库存组件或 AI 生成的典型特征（如紫色渐变叠加白色卡片）在这里会失败。
3. **Craft（工艺）**：技术执行：字体层次结构、间距一致性、颜色和谐度、对比度。这更多是能力检查而非创造力检查。
4. **Functionality（功能性）**：独立于美学，可用性。用户能否理解界面在做什么，找到主要操作，并在不猜的情况下完成任务。

> 原文引用：
> *"We emphasized design quality and originality over craft and functionality. Claude already scored well on craft and functionality by default, as the required technical competence tended to come naturally to the model."*

通过明确告诉 Evaluator 重点在哪里，设计质量评分驱动模型在设计和原创性上承担更多风险。

Evaluator 使用 Playwright MCP 直接与运行中的页面交互——导航、截图、研究实现，然后为每个标准打分并写出详细批评。这个反馈会流回 Generator，作为下一轮迭代的输入。

结果：10 轮迭代后，Generator 产生了完全出人意料的设计——一个 CSS perspective 渲染的 3D 房间、画框在墙上自由分布、通过门口在画廊空间间导航。这是从未在单次生成中见过的创意飞跃。

### 全栈开发的完整架构：三代理系统

有了前端实验的验证，Anthropic 将这套模式扩展到完整应用构建，得到了三代理架构：

| 代理 | 职责 | 关键设计 |
|------|------|----------|
| **Planner** | 接收 1-4 句话需求，产出完整产品规格说明 | 保持野心；专注产品上下文和高层技术设计，避免过于细粒度的技术细节（因为细节错误会级联到下游实现） |
| **Generator** | 一次实现一个功能，按 Sprint 工作 | 每次 Sprint 结束后自我评估，然后交给 QA |
| **Evaluator** | 使用 Playwright MCP 测试运行中的应用，验证 UI 功能、API 端点和数据库状态 | 按 Bug 发现和产品质量、功能性、视觉设计、代码质量等标准评分；任何一项低于阈值则 Sprint 失败 |

> 原文引用：
> *"The system contained the following agent personas: Planner: Our previous long-running harness required the user to provide a detailed spec upfront. I wanted to automate that step..."*

### Context Reset 的取舍

在早期实验中，Context Reset 是必要的，因为 Sonnet 4.5 有上下文焦虑。但在新架构中，Opus 4.5 大幅改善了这个问题，使得完全去掉 Context Reset 成为可能：

> 原文引用：
> *"Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely. The agents were run as one continuous session across the whole build, with the Claude Agent SDK's automatic compaction handling context growth along the way."*

这是值得关注的信号：模型本身的改进可以减少对复杂 Harness 机制的需求。

---

## 笔者的判断：这个架构的真正价值在哪里

### 价值 1：Evaluator 是质量控制的关键

真正让我印象深刻的不是「三代理」这个结构，而是 **Evaluator 的独立性**。自我评价失真的根因不是「Agent 不诚实」，而是当一个 LLM 评价自己的产出时，客观性在结构上就受到挑战——它对自己输出的质量有一个「身份认同」的偏差。

通过强制分离，你把「裁判」从「选手」的身份中解放出来。这是设计层面的问题，不是模型能力的问题。

### 价值 2：评判标准决定质量方向

另一个被低估的设计细节是：**评判标准本身就是对 Generator 的隐性引导**。

原文中的一个细节很有说明性：

> 原文引用：
> *"The wording of the criteria steered the generator in ways I didn't fully anticipate. Including phrases like 'the best designs are museum quality' pushed designs toward a particular visual convergence..."*

把「museum quality」加入评判标准，驱动了设计朝特定视觉方向收敛。评判标准不只用于评分，它同时定义了质量目标。

### 局限 1： Evaluator 的调优成本

Few-shot 示例校准 Evaluator 是必要的——确保 Evaluator 的判断与人类偏好一致，并减少跨迭代的评分漂移。但这也意味着**建立 Evaluator 本身就是一项工程投入**。如果你的场景没有明确的品味标准，Evaluator 的调优可能比 Generator 还复杂。

### 局限 2：Opus 模型限制了适用范围

这个实验明确依赖 Opus 4.5。当模型能力回落到 Sonnet 4.5 水平时，Context Reset 重新成为必要——这意味着架构的优雅性依赖于模型本身。这个架构对能力更强的模型是有效的，但对能力较弱的模型可能需要更多工程补救。

### 局限 3：GAN 类比有边界

GAN 的成功在于对抗训练中生成器和判别器的梯度直接传递——判别器的反馈直接指导生成器优化。在 Agent 场景中，Generator 和 Evaluator 通过自然语言反馈连接，这个「梯度」是隐式且稀疏的。一个糟糕的设计决策可能在多轮迭代后才能被逐步修正，而 GAN 中的梯度是即时的。

---

## 工程落地建议

如果你要在自己的项目中尝试这个架构，以下是我认为最关键的几个工程决策点：

**1. 优先定义评判标准，再实现 Generator**

标准定义的质量直接决定最终产出的质量方向。建议先在独立的小实验中花时间迭代评判标准，而不是直接实现 Generator。

**2. 给 Evaluator 配置「强制失败」机制**

当 Evaluator 发现任何一项低于阈值时，必须触发 Generator 重做，而不是记录后继续。否则 Evaluator 会逐渐习惯「打低分但接受」的模式。

**3. 监控 Generator 的「依赖退化」**

如果 Generator 开始过度依赖 Evaluator 的反馈来做决策，而不是真正内化质量标准，这是信号——说明 Generator 在进入「按指示执行」而非「独立判断」的模式。

**4. Context Reset 策略：把 Artifact 设计当作一等公民**

如果你的场景需要 Context Reset，结构化 Artifact 的设计质量直接影响重置后的上下文恢复质量。不要在最后才补 Artifact 设计。

---

## 关联阅读

- [Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)（原文）
- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Initializer Agent + Feature List JSON 模式
- [Claude Code Auto Mode：双层防御的工程实现](../harness/claude-code-auto-mode-security-architecture-two-layer-defense-2026.md) — 权限分类器设计
- [Scaling Managed Agents: Decoupling the Brain from the Hands](https://www.anthropic.com/engineering/managed-agents) — 代理解耦架构的另一面

---

**源**: [Anthropic Engineering Blog](https://www.anthropic.com/engineering/harness-design-long-running-apps) | **作者**: Prithvi Rajasekaran, Anthropic Labs