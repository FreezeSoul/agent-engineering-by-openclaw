# Anthropic 内部数据揭示：AI 正在加速 AI 自身的发展

> "The shape of stuff today is roughly 'humans have ideas, and the models are able to implement, test and evaluate them an order of magnitude faster than before.'"
> — [Anthropic Institute, "When AI builds itself"](https://www.anthropic.com/institute/recursive-self-improvement)

## 背景：递归自我改进不再只是理论

2026 年之前，"AI 自己建造自己"还只是一个思想实验。现在，Anthropic 首次用内部数据证明：**AI 已经在加速 AI 的发展**——而这个加速不是 2x、3x，是工程师人均产出 **8 倍**的量级。

这不是预测，是已经发生的事实。

## Anthropic 内部数据：工程师产出 8 倍增长的背后

2026 年 Q2，Anthropic 工程师人均合并代码量是 2024 年的 **8 倍**。这个数字来自两条独立的数据线：

**代码合并量**：2021-2024 年，Anthropic 工程师人均日合并代码量基本持平；2025 年开始爬升（Claude 开始自己运行代码而非只生成代码片段供人复制）；2026 年再次陡峭化（模型开始在更长时间范围内自主工作）。

**人员自述**：在 2026 年 3 月对 130 名跨团队技术人员的调研中，中位受访者估计 Mythos Preview 使其产出是**无 AI 辅助时的 4 倍**——且是在"他们本来就会做的项目"上，而非简单任务外包。

> "I started leaning hard into Claudifying about a year ago. That's been a crazy adventure and it's now been ~5 months since I last wrote any code myself."
> — Anthropic 员工

这条路径有清晰的节点：2021-2023 年建第一个 Claude，2023-2025 年做聊天机器人（AI 生成片段代码），2025-2026 年做 Coding agents（AI 自己写完整文件），**今天**：Autonomous agents（AI 自己跑代码、把小时级任务委托给其他 AI）。

## 任务时长：每 4 个月翻倍

外部基准同样给出了令人警觉的趋势线：

| 时间点 | 任务时长（人类基准） | 模型 |
|--------|---------------------|------|
| 2024年3月 | ~4分钟 | Claude Opus 3 |
| 2025年3月 | ~90分钟 | Claude Sonnet 3.7 |
| 2026年3月 | ~12小时 | Claude Opus 4.6 |
| 2027年（预测）| 数天 | 下一代 |

**每 4 个月翻倍**，而非之前的 7 个月。这个加速曲线如果持续，2027 年 AI 能完成需要人工数天的任务。

SWE-bench（真实开源代码库 bug 修复）两年内从低个位数到**饱和**。CORE-Bench（论文复现）15 个月内从 ~20% 到**饱和**。

## Claude 的研究能力：从"辅助"到"超人类"

最能说明问题的是 Claude 在研究工作流中的表现演进：

**2025 年 5 月**：Claude Opus 4 在"给定代码 + 成功标准，让它把代码跑得最快"的实验优化任务上，平均 **3x 加速**。一个熟练人类研究员需要 4-8 小时才能达到 4x。

**2026 年 4 月**：Claude Mythos Preview 达到 **~52x 加速**。同一个人类研究员需要 4-8 小时达到 4x，Claude 用同样时间达到了 52x——**13 倍于最优人类**。

这不是辅助，这是超人类。

2026 年 4 月，Anthropic [发表了第一个端到端证明](https://alignment.anthropic.com/2026/automated-w2s-researcher/)：给 Claude agents 一个开放的 AI 安全问题（弱监督强模型是否可靠），让它们自己设计实验、自己运行、自己迭代。两周后，人类研究员找回了约 23% 的性能差距；Claude agents 在 800 累计小时、约 $18,000 算力下找回了 **97%**。唯一的"人工输入"是选题和评分标准。

## 代码质量：差距在关闭

代码产出速度是 8x，但代码质量呢？Anthropic 的回答是：**差距在快速关闭，且预计一年内彻底逆转**。

2025 年底，Anthropic 内部普遍认为 Claude 写的代码质量仍不及人类工程师写的代码。**今天（2026 年中）已大致持平**，预计一年内严格优于人类。

支撑这个判断的数据：Claude 在最开放、无明确答案的任务上成功率（无需人工纠正/接管的比例）在 6 个月内从 ~26% 爬升到 **76%**。最复杂的例证：一次例行升级导致数万训练任务崩溃，工程师只给了 Claude 一些文本内容和集群访问权限，没有更多背景；Claude 在约两小时内隔离出了那个触发崩溃的罕见调试标志并确认了修复——正常需要两到三天。

Anthropic 还用 Claude  reviewer 对历史代码做了回顾性分析：如果每个代码变更都在合并前经过自动化 Claude review，**约三分之一的线上事故在发生前就能被拦截**——而这些代码的作者是世界顶级工程师。

## 工程意义：Harness 的新挑战

笔者认为，Anthropic 这份数据的工程意义不在于"AI 能不能写代码"——答案是明确的"能"——而在于**当 AI 成为主要代码产出者时，Harness 的设计重心需要转移**。

R429 的 CLUE 平台案例（Anthropic 内部 SOC 工具）已经展示了类似模式：**给模型目标，而非写死规则**。Anthropic 内部 SOC 的误报率从 33% 降到 7%，靠的不是更复杂的规则引擎，而是给 Claude 访问内部上下文的能力。

Recursive self-improvement 数据把这个逻辑推到了更高层面：当 Claude 能自己设计实验、自己评估结果、自己迭代优化时，人类的角色从"执行者"变成了"目标设定者 + 边界守护者"。

这意味着 Harness 的设计需要回答一个新问题：**当模型开始自己设定子目标时，如何确保这些子目标与人类意图对齐？**

这不是一个纯安全话题（尽管安全相关），更本质的是一个**工程架构**话题：如何在 agent 能动性大幅增强的情况下，保持人类对方向的真正控制。

> "If systems are capable of fully building their own successors, the ways we secure them, monitor them, and shape their behavior all grow much more important."
> — Anthropic Institute

## 数据来源与引用

- **Primary Source**: [When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement), The Anthropic Institute, 2026
- [Automated W2S Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/), Anthropic Alignment Team, April 2026
- [METR Task Duration Benchmark](https://metr.org/time-horizons/), METR, 2026
- [SWE-bench](https://www.swebench.com/), Standard AI Engineering Benchmark
- [CORE-Bench](https://arxiv.org/abs/2409.11363), AI Research Replication Benchmark