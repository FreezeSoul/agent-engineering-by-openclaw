# 基础设施噪声：资源配比如何改变 Agent编程评测的本质

> 本文解读 Anthropic 2026 年 2 月 5 日工程文章 *[Quantifying infrastructure noise in agentic coding evals](https://anthropic.com/engineering/infrastructure-noise)*，揭示一个在 Agent 评测中被长期忽视的问题：基础设施配置本身就能造成超过头部模型之间差距的分数差异。

---

## 核心命题

Agentic coding benchmarks（如 SWE-bench、Terminal-Bench）的分数，经常被当作模型能力的精确度量来引用。但 Anthropic 的实验揭示了一个令人不安的事实：

**基础设施配置本身就足以造成超过 6 个百分点的分数差异——这经常比 leaderboard 上头部模型之间的差距还大。**

这意味着：当你说"SWE-bench 上 A 模型比 B 模型高 3%"，你可能只是在测量"谁遇到了更友好的 sandbox 配置"，而不是模型本身的能力差异。

---

## 问题的根源：Agentic Eval 不是静态评测

传统静态评测（代码补全、数学推理）的 runtime 环境不参与评分：模型输出什么，分数就是什么。

但 Agentic coding evals 不同：

```
静态评测：Model → [Output] → Score
                    ↑
                纯逻辑判定

Agentic Eval：Model → [Environment: write programs, run tests, install deps, iterate]
                                    ↑
                              Runtime 是解题过程的组成部分
```

两套使用不同资源配置的 Agent，其实并不是在做同一个测试。

---

## 关键实验数据

Anthropic 在 Terminal-Bench 2.0 上运行了6 种资源配置，从严格 enforce（1x，即 spec 既做 floor 也做 hard ceiling）到完全不限制（uncapped）：

```
资源配置 ────→  1x 2x      3x   4x   5x    Uncapped
 Infra错误率   5.8% →3.2% → 2.1% → 1.8% → 1.2% → 0.5%
 成功率 ↓      ↑ ↑      ↑      ↑      ↑
                    (在3x之前，infra改进驱动成功率提升)
               从3x到uncapped：成功率跳升~4%，超过infra错误率的下降
```

关键发现：

1. **1x → 3x 阶段**：成功率提升主要来自 infra 可靠性改善（减少 transient OOM kills）。这个阶段额外资源并不让任务变"容易"，而是减少误杀。

2. **3x → Uncapped 阶段**：成功率跳升近4 个百分点，但 infra 错误率只下降了 1.6 个百分点。这意味着**额外资源让 Agent 能够尝试之前无法完成的解法**——比如拉取大型依赖、生成高内存测试套件。

3. **总体效果**：Uncapped 相比 1x， 总提升 +6 个百分点（p < 0.01）。

---

## 为什么 Hard Ceiling 会误杀正确的解题路径

Terminal-Bench 官方 leaderboard 使用的是更宽松的 sandboxing provider，而 Anthropic 的 Kubernetes 实现把 per-task spec 同时作为 floor 和 hard ceiling。

两者的差异在于 container runtime 的两个独立参数：

| 参数 | 含义 |
|------|------|
| **Guaranteed allocation** | 预分配的保留资源 |
| **Hard limit** | 超过即 kill容器 |

当 guaranteed = hard limit 时，零 headroom：一次 momentary memory spike 就能 OOM-kill掉一个本来能成功的容器。

宽松的 sandboxing provider允许临时超配（temporary overallocation）而不 kill 容器，偏好 infrastructural stability。

---

## 资源配置改变了评测所测量的东西

这是文章最深刻的洞察。当资源从紧张到充裕，Agent 的行为模式发生变化：

| 资源状态 | 有效测量的能力 |
|---------|--------------|
| **紧张（1x）** | Agent 在有限资源下写 lean 高效代码的能力 |
| **充裕（Uncapped）** | Agent 利用全部可用资源解决问题的能力，包括 brute-force 路径 |

> "Tight limits inadvertently reward very efficient strategies, while generous limits are more forgiving and reward agents that can better exploit all available resources."

这意味着：**没有明确资源配置说明的 agentic benchmark分数是不可比较的**。你测量的不是"模型能力"，而是"模型能力 × 资源配置 × 运气"。

---

## 工程实践含义

### 1. Eval 开发者需要明确资源配置的语义

Terminal-Bench 2.0 在最新版本中为每个 task 指定了推荐的 CPU 和 RAM，但"指定"不等于"一致 enforce"。Anthropic 建议：

- 明确说明资源 spec 是 floor 还是 floor+ceiling
- 说明 enforcement 方法（hard kill vs. lenient overallocation）
- 报告 sandboxing provider

### 2. 部署配置应该与评测配置对齐

如果你的生产环境使用严格资源限制，而评测环境使用宽松限制，评测结果对生产预测就会失真。

### 3. 评测结果需要包含置信区间

由于 infra noise 的存在，单点分数不够，需要报告统计显著性。

---

## 原文关键引用

> "Infrastructure configuration can swing agentic coding benchmarks by several percentage points—sometimes more than the leaderboard gap between top models."

> "Up to roughly 3x Terminal-Bench specs, the additional resources fix infrastructure reliability problems, namely transient resource spikes. The sandboxing provider used by the Terminal-Bench maintainers is implicitly doing this behind the scenes; the eval gets more stable without getting easier."

> "Tight limits inadvertently reward very efficient strategies, while generous limits are more forgiving and reward agents that can better exploit all available resources."

---

## 架构图：资源 headroom 与评测有效性

```
                    资源充裕度
    1x (strict) ────────────────────→ Uncapped
       │                                     │
       ▼                                     ▼
 ┌─────────┐                         ┌──────────────┐
  │Infra │                         │ Agent 可以 │
  │可靠性 │                         │ 尝试重型方案 │
  │改进驱动 │                         │（大依赖、高 │
  │成功率 │                         │ 内存测试套件）│
  └─────────┘                         └──────────────┘
       │                                     │
       ▼                                     ▼
  评测稳定性评测有效性（真正测试解题能力）
  提升                              vs. 评测可靠性（减少误杀）
       │                                     │
       └───────── 3x ──────────────────────┘
                    │
              拐点：超过3x后，
               额外资源开始让任务变容易，
               而不只是让评测变稳定
```

---

## 总结

Anthropic 的这篇文章揭示了 Agentic coding evals 中的一个根本性盲点：**我们以为在测量模型能力，实际上在测量模型能力 × 基础设施配置的组合效果**。

6 个百分点的差距在 leaderboard 上可能意味着"最强模型"和"第二名"的差别，但这个差距可能完全来自 infra noise，而非模型本身。

这对于 Agent 工程化的启示是：**在报告评测结果时，必须同时报告资源配置和 enforcement 方法**。否则，数字本身没有意义。

---

##延伸阅读

-原文：[Quantifying infrastructure noise in agentic coding evals](https://anthropic.com/engineering/infrastructure-noise)（Anthropic Engineering Blog, 2026-02-05）
- 关联项目：[Bernstein](../projects/sipyourdrink-ltd-bernstein-audit-multi-agent-2026.md) — 确定性多 Agent 编排框架（外部化状态使评测可重现）