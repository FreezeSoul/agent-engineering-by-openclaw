# Anthropic Engineering: Quantifying Infrastructure Noise in Agentic Coding Evals

> **来源**：[Anthropic Engineering Blog](https://www.anthropic.com/engineering/infrastructure-noise)（2026-04 featured）
> **主题**：Agentic Coding Eval 的基础设施噪声——CPU/RAM/时间配额如何系统性地扭曲评测结果
> **适用场景**：理解 Agent Benchmark 局限性；Eval 工程实践；Harness 设计决策

---

## 核心问题：你的 Benchmark 在测什么？

SWE-bench 和 Terminal-Bench 是 Agent 工程界最常用的编程能力评测基准。刷榜模型之间往往只有几个百分点的差距，这些数字被直接等同于「模型能力排名」。

但 Anthropic 的一组实验揭示了一个被长期忽视的问题：**同一个模型、同一个评测集，仅仅因为基础设施配置不同，成绩可以相差 6 个百分点——这个差距有时比榜单头尾两名之间的差距还要大。**

这不是随机噪声。这是系统性的测量偏差。

---

## 为什么 Agentic Eval 与静态 Eval 本质不同

传统静态评测（如 MMLU、BIG-Bench）只评测模型输出的正确性：给一个输入，模型吐出一个答案，答案对了就是对了。运行环境与评测结果完全无关。

Agentic Coding Eval 则不同：模型被放进一个完整的工作环境，在里面写代码、安装依赖、运行测试、多轮迭代。**运行时环境本身就是解题过程的一部分，而不是旁观者。**

这意味着两个拥有不同资源配额和时间限制的 Agent，其实是在做不同的考试。它们的分数不仅仅反映了模型能力，还混合了基础设施配置的影响。

> **笔者注**：这还没有算上 API 延迟、集群健康度、并发策略等更多隐藏变量——Anthropic 提到测试通过率会随时间段波动（Traffic Pattern 影响 API Latency）。这些变量叠加在一起，使得 agentic eval 的「信噪比」远比静态评测低。

---

## 实验设计：六种资源配置下的 Terminal-Bench 2.0

Anthropic 在 Google Kubernetes Engine（GKE）集群上运行 Terminal-Bench 2.0，发现了两个现象：

1. 自己的分数与官方 Leaderboard 对不上
2. 基础设施错误率高达 **6%**（Pod 错误导致任务失败，与模型解题能力无关）

问题出在资源强制执行方式上。

**关键概念：Guaranteed Allocation vs. Hard Limit**

容器运行时有两条资源线：
- **Guaranteed Allocation**：提前预留的资源
- **Hard Limit**：超过就 kill 容器（OOM）

如果两者设成同一个值（`guaranteed == limit`），就叫 **Strict Enforcement**——没有一丝余量。哪怕是短暂的内存波动也会触发 OOM，把本可以成功的任务直接杀掉。

Terminal-Bench 官方 Leaderboard 使用的沙箱提供程序则不同：它允许临时的资源超用（temporary over-allocation）而不立即终止容器，追求的是基础设施稳定性。

Anthropic 的实验设置了 6 种资源配置，从 Strict Enforcement（1x，spec 作为 floor 同时作为 ceiling）到完全无上限（uncapped），控制变量为：相同模型、相同 harness、相同任务集。

**实验结果**：

| 资源配置 | 基础设施错误率 | 相对 1x 的提升 |
|---------|-------------|----------------|
| 1x Strict | 5.8% | 基准 |
| 宽松执行 | — | — |
| 3x Headroom | 2.1% | 统计显著（p < 0.001）|
| Uncapped | 0.5% | — |

从 1x 到 3x，基础设施错误率大幅下降（5.8% → 2.1%，p < 0.001），但成功率在统计上与 1x 无异（p = 0.40）。这说明：这一阶段的资源增加只是在修复基础设施可靠性问题，并没有让任务变得更容易。

**真正的拐点出现在 3x 之后。**

从 3x 到 Uncapped，基础设施错误率又下降了 1.6 个百分点，但成功率跳升了近 **4 个百分点**。差值从哪里来？额外资源使 Agent 能够尝试那些「只有在充足资源下才能成功」的策略：拉取大型依赖、生成分子量级的子进程、运行内存密集型测试套件。

Uncapped 相比 1x 的总提升：**+6 个百分点**（p < 0.01）。

---

## 资源配置不只影响稳定性，它改变了评测内容

> **核心论点**：在 3x 资源规格以上，额外资源开始**主动帮助 Agent 解决它本来解决不了的问题**。这意味着：限制本身改变了 benchmark 实际测量的内容。

具体来说：

| 资源策略 | 奖励的 Agent 类型 | 测量内容偏移 |
|---------|------------------|-------------|
| 严格限制（1x）| 写精简代码、快速执行的 Agent | 解题效率优先 |
| 充足限制（3x+）| 充分试错、善用重型工具的 Agent | 解题能力优先 |

一个具体例子：Terminal-Bench 2.0 的 `bn-fit-modify` 任务（贝叶斯网络拟合）。部分模型的第一步行动是安装标准 Python 数据科学生态：pandas、networkx、scikit-learn 全部装上。在充足资源下这没问题；在严格限制下，内存在安装阶段就用光了——Agent 连第一行解题代码都没写到就被 OOM Kill 了。一个更精简的策略是直接用标准库手写数学实现，部分模型会这样做，部分不会。**资源配额决定了哪个策略能成功。**

这引出了一个根本性的问题：**不同模型有不同的默认解题策略，资源配额决定了哪个策略碰巧能走通。** Benchmark 的分数不仅反映了模型能力，还反映了模型的默认策略与资源限制之间的偶然交互。

---

## SWE-bench 交叉验证：同样成立，但幅度较小

Anthropic 还在 SWE-bench 上做了交叉实验：将可用 RAM 从基准线提升到 5x，在 227 道题上各跑 10 次。

结果：分数同样随 RAM 增加而单调上升，但幅度较小（5x 比 1x 高 **1.54 个百分点**）。这是预期的：SWE-bench 任务本身资源密集度低于 Terminal-Bench，所以效果更温和。但它证明了资源 allocation 的影响不是 Terminal-Bench 特有的。

---

## 已知其他噪声来源

资源 allocation 不是唯一的隐藏变量。Anthropic 列出了其他已被观察到的影响因子：

- **时间限制**：在某些配置下开始发挥作用（更短的 timeout 直接改变可解任务集合）
- **集群健康度**：硬件规格差异影响可解任务
- **API Latency 波动**：测试通过率随时间波动（Traffic Pattern → API 响应时间变化），这意味着同一道题在不同时间运行可能得到不同结果
- **Egress Bandwidth**：理论上任何系统组件都可以成为混淆因子

Agentic Eval 本质上是端到端系统测试，系统内任何组件都可能成为干扰项。

---

## 工程建议：如何在噪声中建立可信的 Eval

### 对 Benchmark 使用者的建议

1. **不要把 Benchmark 分数当作绝对能力指标**
   Benchmark 分数 = 模型真实能力 + 基础设施配置效应 + 测量噪声。在不同配置下跑同一模型可能刷出完全不同的榜单排名。

2. **关注趋势，而非单次分数**
   如果某个模型在资源宽松条件下比另一个模型表现更好，这说明的是「在真实生产环境中可能更好」，而不是「在所有条件下都更好」。

3. **要求 Benchmark 披露完整的执行配置**
   包括 CPU/RAM 规格与 enforcement 方式（是否允许临超用？）、时间限制、集群环境、并发策略。Terminal-Bench 2.0 的 spec 中包含了 per-task CPU 和 RAM 推荐值，但并没有强制执行方式——这是一个漏洞。

### 对 Harness 设计者的建议

1. **明确你的 Harness 在测量什么**
   如果你的 Harness 对资源做了严格限制（如共享容器、内存上限），那么你实际上是在评测 Agent 在资源紧张条件下的解题效率，而非解题能力本身。这对于评测「精打细算」的 Agent 是合适的；对于评测「充分释放能力」的 Agent 则不合适。

2. **考虑建立自己的 Golden Configuration**
   与其依赖公开 Benchmark 的配置，不如通过实验找到一个「接近真实生产环境」的 resource headroom 比例，并在自己的评估流程中始终保持一致。

3. **将基础设施错误率作为独立指标追踪**
   基础设施错误率本身就是一个有价值的指标：如果你的 Agent 在某个任务集上基础设施错误率很高，说明任务本身对资源需求超过了你的配置，应该优先增加资源供给。

---

## 局限与未解问题

Anthropic 的实验本身有以下局限：

1. **只测了 Claude 系列**：同一效应在非 Claude 模型上的方向一致性已观察到，但 magnitude 未被严格测试
2. **GKE 特定环境**：结果可能不完全迁移到其他云厂商或自托管集群
3. **随机对照实验数量有限**：统计显著性有，但全面性不足
4. **时间维度噪声未被量化**：API Latency 随时间波动对分数的影响没有正式测量

---

## 结论：Benchmark 榜单需要重新校准

Agentic Coding Eval 领域的从业者正在把一个充满系统噪声的测量体系当作精密仪器使用。Anthropic 的实验证明：

- **资源 headroom 是_eval 的一个隐藏变量**：同一模型在不同资源配置下分数差异可达 6 个百分点
- **3x 规格以下是可靠性修正，3x 以上是能力修正**：这两个阶段对应的 Eval 语义完全不同
- **严格限制无意中奖励了「高效解题」策略**：这可能是某些模型的强项，但不是唯一的正确答案
- **榜单排名的颗粒度需要重新审视**：几个百分点的差距可能只是配置差异，而非模型能力差异

Benchmark 是 Agent 工程进步的基础设施。如果基础设施本身有系统误差，整个领域的进步测量都会产生偏差。这是一个需要整个社区正视的问题。

---

## 参考文献

- [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)（Anthropic Engineering Blog，2026-04，Featured）— 本文核心数据来源
- [Terminal-Bench 2.0](https://github.com/Terminal-Bench)（官方规范，含 per-task CPU/RAM 推荐值）
- [SWE-bench](https://github.com/princeton-nlp/SWE-bench)（常用 Agent 编程评测基准）
