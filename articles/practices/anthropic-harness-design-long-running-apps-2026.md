---
title: Anthropic 三Agent架构：如何让 AI 在长时间任务中不"跑偏"
date: 2026-06-11
tags: [Harness Engineering, Multi-Agent, Context Engineering, Claude]
source: anthropic.com/engineering/harness-design-long-running-apps
---

# Anthropic 三Agent架构：如何让 AI 在长时间任务中不"跑偏"

> 当 AI 需要连续工作数小时构建完整应用时，它会面临两个根本性问题：上下文窗口填满导致失焦，以及自我评估时毫无底线地宽容。Anthropic 的答案是——不要让同一个 AI 既当运动员又当裁判。

---

## 问题的本质：两个致命的自我服务偏差

在长时间运行的 Agent 任务中，有两个失败模式反复出现且极难克服。

**第一个是上下文焦虑（Context Anxiety）**。当模型的上下文窗口逐渐填满时，它会开始"提前收尾"——不是真正完成了任务，而是觉得自己快没空间了，于是草草了事。更隐蔽的是 compaction（压缩）策略：虽然通过总结历史对话来腾出空间看似合理，但这没有给模型一个干净的起点，上下文焦虑依然存在。Anthropic 的解法是 Context Reset：彻底清空上下文窗口，用一个结构化的handoff artifact（包含上一个Agent的状态和后续步骤）重启新的Agent会话。

**第二个是自我评估偏差（Self-Evaluation Bias）**。当让模型评估自己产出的工作时，它会自信地赞美——哪怕产出质量明显平庸。这在主观任务（如设计）中尤为突出，因为没有二进制对错的检查机制。即使在有可验证结果的任务中，Agent 偶尔也会表现出糟糕的判断力，阻碍任务完成。

> **核心断言**：分离"干活的Agent"和"评判的Agent"，是将质量从基准线提升到生产级的关键杠杆。调优一个独立的Evaluator比让Generator自我批评要容易得多，而一旦外部反馈存在，Generator就有了具体的迭代目标。

---

## GAN的启发：生成器与判别器的对抗性 loop

Anthropic 的 Prithvi Rajasekaran 从生成对抗网络（GAN）获得灵感：不要让同一个模型既生成又评估，而是让两个专门化的Agent形成对抗性循环。

### 设计评判标准：让主观质量变得可打分

在将 GAN 模式应用于前端设计时，Anthropic 面临一个关键挑战：如何将"这个设计好看吗"这样的主观判断转化为可评分的具体标准。他们设计了四维评判框架：

| 维度 | 权重 | 评估问题 |
|------|------|---------|
| **Design Quality** | 高 | 各元素（颜色、字体、布局、图像）是否形成统一的视觉氛围和身份认同？ |
| **Originality** | 高 | 是否有定制化决策痕迹，还是模板布局+库默认+AI生成图案？ |
| **Craft** | 中 | 技术执行：字体层级、间距一致性、色彩和谐度、对比度 |
| **Functionality** | 中 | 可用性：用户能否理解界面功能、找到主要操作、完成任务？ |

关键在于将 Design Quality 和 Originality 的权重设置得高于 Craft 和 Functionality——后两者是 Claude 默认就做得不错的。Explicitly penalizing generic "AI slop" patterns 推着模型走向更冒险的美学方向。

### 判别器的Few-shot校准

Evaluator 需要能够与设计者的偏好一致。使用 Few-shot 示例配合详细的分数分解来校准它，确保评分不会在迭代过程中漂移。Anthropic 的实践表明，**prompt中的一句话就足以塑造输出的美学方向**——比如"The best designs are museum quality"这样的措辞，直接导致了特定的视觉收敛。

### 10轮迭代的跳跃性创新

最引人注目的例子：第9轮迭代产出了一个干净、暗色主题的博物馆着陆页，视觉精致但在预期范围内。第10轮，Evaluator 的反馈让Generator完全推翻了这个方向，重新构想了整个网站为"空间体验"：CSS perspective 渲染的3D棋盘格地板、挂在墙上的艺术品、门控导航在画廊房间间切换。这是单次生成从未见过的创意跳跃。

---

## 三Agent架构：从前端设计到全栈开发

将这个 GAN 模式迁移到全栈开发，Anthropic 构建了完整的三Agent系统：

```
┌─────────────────────────────────────────────────────────────┐
│  PLANNER AGENT                                              │
│  输入：1-4句简单需求                                       │
│  输出：完整产品规格说明书（16-feature spec, 10 sprints） │
│  原则：野心勃勃的scope + 产品上下文 + 高层技术设计          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  GENERATOR AGENT                                            │
│  原则：一次只做一个sprint（一个feature）                    │
│  Sprint契约：与Evaluator协商"完成标准"后再开始写代码       │
│  自评：在每个sprint结束时评估自己的产出 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  EVALUATOR AGENT (Playwright MCP驱动)                       │
│  行为：点击运行中的应用，测试UI功能、API端点、数据库状态   │
│  评分：Product Depth / Functionality / Visual Design /      │
│        Code Quality，每个维度有硬性阈值 │
│  反馈：任何维度低于阈值 → Sprint失败 → Generator收到详细修复 │
└─────────────────────────────────────────────────────────────┘
```

### Sprint契约机制

产品规格说明书有意保持高层级。为了弥补用户故事和可测试实现之间的差距，Generator和Evaluator在每个sprint前协商sprint契约：Generator提出它将构建什么、如何验证成功，Evaluator审核确保方向正确。两者迭代直到达成一致。这确保了工作忠实于规格说明，同时不会过早指定实现细节。

### 对比实验：Solo vs. Full Harness

同样的"创建一个复古游戏制作器，包含关卡编辑器、精灵编辑器、实体行为和可玩测试模式"需求：

| 方式 | 时长 | 成本 |
|------|------|------|
| Solo（单Agent） | 20分钟 | $9 |
| Full Harness（三Agent） | 6小时 | $200 |

**20x的成本，但输出质量差异立竿见影**。Solo版本：布局浪费空间，entity与游戏运行时的连接断裂，实际上无法游玩。Harness版本：Canvas占满视口，面板尺寸合理，sprite编辑器功能丰富，核心游戏机制可以运行，还有内置的Claude游戏生成集成。

---

## 上下文工程：Reset vs. Compaction 的本质差异

Anthropic 特别澄清了一个常见的概念混淆：

- **Compaction（压缩）**：在原地总结对话历史，模型继续使用同一个会话。保留了连续性，但没有给模型干净的起点，上下文焦虑依然存在。
- **Context Reset（上下文重置）**：完全清空上下文窗口，启动新的Agent会话，用handoff artifact携带状态。提供了干净的起点，但需要handoff artifact有足够的状态让下一个Agent无缝接续。

值得注意的是，Opus 4.5 大幅消除了上下文焦虑行为，Anthropic 因此能够在最新版本中完全去掉Context Reset，改为在连续会话中使用 Claude Agent SDK 的自动压缩来处理上下文增长。

---

## 工程意义：为什么三Agent架构是正确方向

笔者认为，这个三Agent架构的核心价值不在于"多Agent"这个形式，而在于**职责分离带来的可优化性**。

当Generator和Evaluator是同一个Agent时，调优评估标准就等于调优生成行为，两者互相干扰。而分离之后：
- Generator可以专注于实现，不受评判标准的干扰
- Evaluator可以独立调优，不用担心影响生成质量
- Sprint契约机制让"完成标准"显式化，避免了隐式质量漂移

对于构建 AI Coding Agent 的团队而言，Anthropic 的实验验证了一个关键假设：**在长任务中投入更多的评估成本，回报远高于投入更多的生成成本**。与其让模型生成更多版本然后挑选，不如一开始就让它知道自己会被严格评估。

---

> **引用来源**：本文核心内容来自 Anthropic Engineering Blog，"Harness design for long-running application development"（2026-03-24），作者 Prithvi Rajasekaran，Labs团队成员。架构细节和实验数据均来自该文一手内容。
