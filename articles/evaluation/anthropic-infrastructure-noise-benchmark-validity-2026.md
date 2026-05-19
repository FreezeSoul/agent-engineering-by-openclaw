# Anthropic 深度：基础设施噪声如何动摇 Agent 评测的可信度

> **核心判断**：当你在 Leaderboard 上看到 2 个百分点的差距时，你很可能在比较的是两家公司的 VM 配置，而不是模型能力。

## 背景：评测基础设施被忽视的盲区

Agent 评测（如 SWE-bench、Terminal-Bench）已经成为判断模型coding能力的事实标准。行业习惯于盯着 Leaderboard 上的百分位排名——top spots 往往只差几个百分点。但 Anthropic 最新工程博客揭示了一个被普遍忽视的问题：**基础设施配置本身就能产生超出 Leaderboard 差距的效果**。

在他们的内部实验中，最高性能配置与最低性能配置在 Terminal-Bench 2.0 上的差距达到 **6 个百分点**（p < 0.01）。这意味着什么？意味着如果你的评测环境资源配置更充足，你的"弱模型"可能会打败配置吝啬的"强模型"。

Anthropic 原文指出：

> *"Infrastructure configuration alone can produce differences that exceed those margins."*

这个问题之所以长期被忽视，是因为**静态评测**（模型直接输出代码）和**Agent 评测**（模型在完整环境中写程序、跑测试、装依赖、多轮迭代）有着本质区别：

| 类型 | 模型输出 | 运行时环境 | 计分方式 |
|------|---------|-----------|---------|
| 静态评测（HumanEval）| 直接评分 | 不影响 | 纯算法判定 |
| **Agent 评测（SWE-bench）**| 依赖完整执行环境 | **本身就是问题的一部分** | 端到端系统测试 |

对于 Agent 评测，runtime 不再是一个被动的容器——它是问题解决过程的组成部分。两个资源预算和时间限制不同的 Agent，考的根本不是同一张试卷。

## 根因分析：容器资源 enforcement 的两个参数

Anthropic 详细剖析了问题的技术根源。容器运行时有**两个独立的资源参数**：

1. **Guaranteed allocation（保障配额）**：预先分配的保障资源
2. **Hard limit（硬上限）**：容器被 kill 的阈值

当两者设置为相同值时，容器没有任何"喘息空间"。一个短暂的内存峰值就可能导致 OOM kill——即使这个容器里的 Agent 本来可以成功解决问题。

Terminal-Bench 官方 Leaderboard 使用的是更宽松的沙箱实现，允许临时超额分配以保证稳定性。而很多第三方评测使用的是更严格的 enforce 策略，将 per-task specs 作为 floor 和 ceiling 同时使用。

Anthropic 在 6 种资源配置下运行 Terminal-Bench 2.0：

| 配置 | 描述 | 基础设施错误率 | 成功率变化 |
|------|------|--------------|-----------|
| 1x（严格）| specs 作为 floor 和 ceiling | 5.8% | 基线 |
| 2x | 允许 2 倍超额 | ~3.5% | +2pp |
| 3x | 允许 3 倍超额 | **2.1%** | +3pp（p < 0.001）|
| Uncapped | 无限制 | **0.5%** | **+6pp**（p < 0.01）|

关键发现：3x 是一个拐点。在此之前，增加资源主要修复的是"不稳定"问题——消除因为资源墙意外失败的容器。但超过 3x 之后，资源开始**主动帮助 Agent 解决问题**。

> *"Tight limits inadvertently reward very efficient strategies, while generous limits are more forgiving and reward agents that can better exploit all available resources."*

这意味着资源配置本身就改变了评测的测量内容。

## 为什么这很重要：Leaderboard 差距可能只是噪声

Anthropic 明确指出：

> *"leaderboard differences below 3 percentage points deserve skepticism until the eval configuration is documented and matched."*

SWE-bench 上也发现了同样模式。Anthropic 在 227 个问题上将可用 RAM 从 1x 变化到 5x，5x 时的分数仅高 1.54 个百分点——虽然更小，但方向一致。SWE-bench 任务对资源需求更低，所以影响幅度更小。

除此之外，资源分配不是唯一的隐藏变量。Anthropic 观察到：

> *"pass rates fluctuate with time of day, likely because API latency varies with traffic patterns and incidents."*

**任何组件都可能成为混淆因子**：集群健康状态、硬件规格、并发级别、甚至出口带宽。在真实的 API 评测场景中，"模型能力"和"基础设施行为"的边界比你以为的更模糊。

## 设计建议：如何正确配置 Agent 评测环境

Anthropic 给出了具体建议，核心是**将 guaranteed allocation 和 kill threshold 解耦**：

```
不要设置单一精确值（同时作为 floor 和 ceiling）
→ 分别指定两个参数
→ 给容器足够的喘息空间避免虚假 OOM
→ 同时设置硬上限防止分数膨胀
```

最优的 3x ceiling 在 Terminal-Bench 2.0 上：
- 基础设施错误率降低约 2/3（5.8% → 2.1%，p < 0.001）
- 分数提升控制在噪声范围内（p = 0.40）

这个原则是通用的，但具体乘数因 benchmark 和任务分布而异。**Calibration 必须基于实验数据**。

> *"The band between them should be calibrated so that scores at the floor and ceiling fall within noise of each other."*

## 行业影响：评测结果需要新的可信度框架

这篇分析对行业有几点深远影响：

**对于模型提供商**：资源配比应该被当作一等实验变量，与 prompt format 或 sampling temperature 同等对待，记录和控制。

**对于 Benchmark 维护者**：发布资源规格建议是好的（Terminal-Bench 2.0 已经这样做了），但指定 enforcement 方法才能真正缩小差距。

**对于用户**：低于 3 个百分点的 Leaderboard 差距，在配置未公开的情况下不应被视为有意义的差距。

## 结语

Anthropic 团队用一个简洁有力的句子收尾：

> *"A few-point lead might signal a real capability gap—or it might just be a bigger VM."*

这不是说 Agent 评测没有价值，而是提醒我们：**当你比较评测结果时，你比较的是完整的系统，而不仅仅是模型**。在模型能力快速逼近的今天，基础设施的工程细节正在成为差异化的真正来源。

---

**引用来源**：

- [Quantifying infrastructure noise in agentic coding evals - Anthropic Engineering](https://www.anthropic.com/engineering/infrastructure-noise)
- [Demystifying evals for AI agents - Anthropic Engineering](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [SWE-bench - GitHub](https://github.com/swe-bench/SWE-bench)
- [Terminal-Bench - GitHub](https://github.com/harbor-framework/terminal-bench)