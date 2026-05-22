# Anthropic Engineering：AI 时代的面试题设计——三次迭代仍被 Claude 超越

> **来源**：[Anthropic Engineering Blog](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations)（2026-01-21）
> **主题**：Anthropic 性能工程面试题经历三个版本仍被 Claude Opus 4.5 攻克——评估设计如何应对 AI 能力进化
> **适用场景**：招聘评估设计；AI 辅助面试；人类与 AI 能力边界探索

## 核心论点

随着 Claude 模型能力提升，Anthropic 用于筛选性能工程师的面试题经历了三轮迭代：从"模拟加速器代码优化"→"更奇异的约束指令集"→"Zachtronics 风格的极简指令拼图"。即便如此，Claude Opus 4.5 在延长时间后仍能匹配最佳人类候选人的表现。这一经历揭示了一个根本性挑战：**当 AI 在限定时间内超越人类，评估设计需要从根本上重构**。

## 背景：SWE-bench 之外的评估困境

Anthropic 的性能工程团队负责从 TPU/GPU/Trainium 集群的调度优化到模型训练效率的一切工作。这类工作既需要扎实的系统知识，又需要对具体硬件有深入理解。2023 年底，团队需要大规模筛选候选人，于是设计了一个模拟加速器上的代码优化 take-home 测试。

原始设计（v1）的核心挑战是：在模拟加速器上优化一段矩阵转置代码，要求在 4 小时（后压缩到 2 小时）内找到最优解。这个任务足够真实、能区分人类能力高低、且可以借助 AI 工具完成。

## 三轮迭代：Claude 如何逐一攻克

### v1：Claude Opus 4 追平人类顶尖水平

原始任务的最佳人类解法约 1790 cycle，Claude Opus 4 在标准测试时间（2 小时）内就能达到类似水平。这意味着评估还能区分最强的人类候选人——但 Claude Opus 4.5 改变了这一切。

### v2：Claude Opus 4.5 匹配最佳人类候选人

当给 Claude Opus 4.5 更多测试时间计算（test-time compute），它甚至能找到比最佳人类提交更优的解法：1487 cycles vs 人类最优的 1790 cycles。更关键的是，Claude 发现了工程师从未想到的优化策略——将整个计算转置而非逐元素处理。

Anthropic 不得不用补丁堵住这个"意外解法"，但即使堵掉后，Claude 的 ultrathink 模式仍然在更长时间后解决了问题。

### v3：Zachtronics 风格极简指令集

第三轮迭代 Tristan Hume 转向了高度约束的极简指令集拼图，灵感来自 Zachtronics 的编程解谜游戏（如 Shenzhen I/O）。这类问题的特点是：

- **指令集极简**：每个芯片只有约 10 条指令，1-2 个状态寄存器
- **解法多样**：需要将状态编码进指令指针或分支标志
- **AI 难以迁移**：与标准编程任务差异足够大，Claude 训练数据中很少见

Claude Opus 4.5 在这个版本上失败了。Anthropic 仍在使用这个版本进行招聘。

## 关键洞察：什么让评估对 AI 保持鲁棒

| 策略 | 效果 | 代价 |
|------|------|------|
| 更难的问题 | 部分有效，但 Claude 终会攻克 | 任务可能失去区分度 |
| 极简/奇异指令集 | 短期内有效，Claude 无法迁移 | 失去与真实工作的相似性 |
| 缩短时间限制 | 只能延缓，无法根本解决 | 对人类也不公平 |
| 开放时间（无限制） | 人类仍有优势，但失去实际可操作性 | 面试流程不可行 |

核心发现：**AI 与人类的能力边界在于时间尺度**。在无限时间下，人类专家仍能在某些任务上超越最强模型。但面试场景的时间限制（2-4 小时）越来越难以区分人类与 AI 输出。

## 工程意义

1. **评估设计必须演进**：随着 AI 能力提升，"对人类有区分度"的标准在持续变化
2. **AI 辅助是双刃剑**：允许候选人用 AI 工具会进一步压缩人类优势窗口
3. **真实感 vs 鲁棒性的权衡**：越真实的任务越快被 AI 攻克，越奇异的任务越脱离实际工作
4. **Test-time compute 改变格局**：Claude 的 ultrathink 能力意味着"给 AI 足够时间"几乎总能找到更优解

## Anthropic 的开放挑战

Anthropic 将原始 v1/v2 的 take-home 公开为 [open challenge](https://github.com/anthropics/original_performance_takehome)。目前 Claude Opus 4.5 的最佳成绩是 1363 cycles（经过大量 test-time compute），而人类最快提交是 1790 cycles（标准时间）。如果你能在无限时间内超越 1363 cycles，Anthropic 愿意直接联系你。

## 与 Eval 基础设施噪声的闭环

[Anthropic 的另一篇文章](/articles/evaluation/infrastructure-noise-agentic-coding-evals-2026.md) 指出，基础设施配置可以让 SWE-bench/Terminal-Bench 的分数波动高达 6 个百分点。结合本文的发现：**Agent 评测的不确定性来自两层——既来自运行时的资源配额（Eval Infrastructure），也来自模型能力本身的快速进化（AI-resistant Design）**。这两层叠加，使得"用 Benchmark 衡量模型能力"这件事的可靠边界越来越模糊。
