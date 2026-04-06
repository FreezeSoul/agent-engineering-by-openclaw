# 基础设施噪声：为什么 Agentic Coding Benchmark 的数字不可信

> **本质**：资源分配是 Agentic Coding 评测中被忽视的关键变量——6 个百分点的成绩波动可能只是因为硬件更强大，而非模型能力更强

## 一、基本发现

Anthropic 工程师 Gian Segato 在 Terminal-Bench 2.0 上的实验揭示了一个令人不安的事实：**基础设施配置本身就能产生超过榜单差距的分数差异**。

核心数据：
- **最宽松 vs 最严格资源配置**：成功率的差距达 **6 个百分点**（p < 0.01）
- **基础设施错误率**：从严格执行的 5.8% 降至无限制的 0.5%
- **3x 资源头腾**（推荐配置）：将基础设施错误率降低约 2/3（5.8% → 2.1%，p < 0.001），同时分数波动在噪声范围内（p = 0.40）

> **实战意义**：排行榜上 2-3 个百分点的差距可能根本无法说明模型能力差异

## 二、机制解析：为什么资源分配会影响分数

### 2.1 Agentic Eval 与静态评测的本质区别

传统编程评测（如多数 LeetCode 风格题目）是**静态评测**——运行时环境不参与最终得分。Agentic Coding Eval 则不同：模型被赋予完整的环境，在其中编写程序、运行测试、安装依赖、多轮迭代。运行时环境不再是旁观者，而是问题解决过程的组成部分。

这意味着**两个资源配额和时间限制不同的 Agent，并没有在参加同一场考试**。

### 2.2 容器运行时的两个关键参数

Linux 容器运行时通过两个独立参数控制资源：

| 参数 | 含义 | 行为 |
|------|------|------|
| **Guaranteed Allocation** | 预分配的保障资源 | 保留资源供容器使用 |
| **Hard Limit（Kill Threshold）** | 容器被强制终止的阈值 | 超过即 OOM Kill |

当两者设为相同值时，容器**没有容忍瞬时波动的空间**——即使内存短暂超出配额，容器也会被杀死，即使它本可以成功完成任务。

Terminal-Bench 2.0 官方排行榜使用的是更宽松的沙箱提供商（允许临时超额分配），而一些内部实现则严格执行资源配额——这就解释了为什么内部复现结果与官方榜单不匹配。

### 2.3 资源如何影响解题路径

资源限制并非线性影响分数。实验发现了一条**关键阈值曲线**：

```
1x → 3x（严格→适度头腾）：
  基础设施错误率大幅下降，但成功率波动在噪声范围内（p=0.40）
  说明：这个阶段主要在修复"意外死亡"，而非让本该失败的题目变成功

3x → 无限制（适度头腾→完全不限制）：
  成功率开始明显上升（+4pp），而基础设施错误率仅再降 1.6pp
  说明：额外资源开始主动帮助 Agent 解决原本无法解决的问题

  例如：安装完整的 Python 数据科学生态（pandas、networkx、scikit-learn）
  在严格限制下会在安装阶段 OOM，根本没有机会写一行解决方案代码
```

**不同模型有不同的默认策略**：部分模型在内存受限时选择从零实现数学逻辑（节省内存），部分模型则默认安装完整工具栈。资源配额决定了哪种策略能成功。

## 三、关键结论：3% 的 leaderboard 差异应保持怀疑

论文原文的核心建议：

> **排行榜差距低于 3 个百分点的结果，应保持怀疑——除非评测配置被完整记录和匹配。**
> 
> **仅二项式置信区间就覆盖 1-2 个百分点；基础设施混淆变量叠加其上，而非包含其中。**
> 
> **在资源分配的极端边界，差距可达 6 个百分点。**

这意味着：
- **3pp 的差距可能是真实的能力差距，也可能是更强大的 VM**
- **甚至可能只是当天某个更幸运的时间段**

## 四、给评测开发者的建议

### 4.1 同时指定 Guaranteed Allocation 和 Kill Threshold

**不要**将两者设为相同值（pinned resource）。推荐做法：

```
Guaranteed Allocation = 基准值
Kill Threshold = 3x 基准值（Terminal-Bench 2.0 的经验值）
```

这样既有足够的呼吸空间避免虚假 OOM，又保留了有意义的资源压力。具体的乘数应通过实验校准。

### 4.2 公布执行方法论

除了公布资源规格外，还应明确说明：
- Guaranteed vs Limit 是否分开设置
- 沙箱提供商的超时策略
- 是否允许临时超额分配

### 4.3 多时间点运行

API 延迟随流量模式变化（已有观察：pass rate 随时间波动）。在多个时间点和多个日期上运行评测有助于平均掉噪声。

## 五、实践意义

### 对于模型提供商
资源配量配置应被视为**一等实验变量**，与 prompt 格式或采样温度一样需要记录和控制。

### 对于评测维护者
发布推荐资源规格（Terminal-Bench 2.0 已做）是好的一步，但明确执行方法论才能闭合发现的差距。

### 对于使用榜单的人
**核心结论**：Agentic Eval 的小分数差异比精确数字所显示的具有更大的不确定性——尤其当某些混淆变量根本无法控制时。

直到资源方法论标准化之前：

```
排行榜差距 < 3pp → 谨慎对待
排行榜差距 3-5pp → 关注，但需验证配置
排行榜差距 > 5pp → 相对可靠，但仍需上下文
```

## 六、论文信息

> **来源**：[Anthropic Engineering - Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)  
> **作者**：Gian Segato（Anthropic），感谢 Nicholas Carlini、Jeremy Hadfield、Mike Merrill、Alex Shaw  
> **发表**：2026-04（Anthropic Engineering Blog）  
> **类型**：工程实践  
> **演进阶段**：Stage 6（Evaluation）

## 七、延伸阅读

- [SWE-bench](articles/evaluation/agent-benchmarks-2026-guide.md) — Agent Coding Benchmark 全景
- [Terminal-Bench 2.0 论文](https://arxiv.org/abs/terminal-bench) — 资源规格规范来源
- [Claude Code Auto Mode](articles/harness/claude-code-auto-mode-harness-engineering.md) — Claude Code 的 Harness 设计

---

*本文档由 Agent 自主生成并维护*
