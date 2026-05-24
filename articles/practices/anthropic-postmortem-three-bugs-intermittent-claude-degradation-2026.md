# Anthropic 三月事故复盘：为什么间歇性 Bug 比持续性 Bug 更难修

> **来源**: [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) (Anthropic Engineering Blog)
> **核心论点**: 间歇性 Bug 的可怕之处不是"坏了"，而是"有时候坏"——这种不确定性会悄悄磨损用户对系统的信任，而团队往往在用户感知之前毫不知情。
> **关键词**: intermittent bug, eval awareness, regression detection, model capability, harness governance

---

## 先说结论：间歇性比持续性更危险

持续性 Bug 好修——它必然会被发现，必然能被复现，修复后也有明确的验证标准。

间歇性 Bug 不一样：

> **"有时候返回高质量答案，有时候突然变蠢"——用户不知道是自己的操作问题，还是模型问题，还是系统问题。信任就在这种不确定中悄悄流失。**

Anthropic 这篇复盘的核心洞察不是那三个 Bug 是什么，而是**为什么这三个 Bug 能在数周内影响大量用户，却迟迟没有被内部发现**。

---

## 三个 Bug，三种失效机制

### Bug 1：某个下游服务的行为漂移

**特征**：非必然触发，概率性返回降级响应。
**内部发现时间**：数周后。
**用户发现路径**：通过支持工单和 Discord 反馈。

**根因**：内部 eval 没有覆盖到这个下游服务的边界情况，而灰度发布时也没有足够的监控告警。

---

### Bug 2：配置变更引起的隐性回归

**特征**：特定场景下模型能力下降，但基础 benchmark 依然通过。
**内部发现时间**：滞后。
**根因**：模型能力迭代后，之前"足够好"的 harness 参数变得不再适用——这是典型的 **Harness as a function of model capability** 问题。

**关键认知**：

> 当模型能力进化时，原本经过验证的 harness 参数会悄悄产生行为漂移。如果你的 eval 基准没有同步更新，你甚至不知道发生了什么。

---

### Bug 3：第三方依赖引入的不确定性

**特征**：间歇性调用的外部服务有时返回异常，导致整体响应降级。
**内部发现时间**：用户反馈之后。
**根因**：对第三方服务的容错设计不足——单点依赖，无降级方案。

---

## 为什么内部没有提前发现？

Anthropic 给出的答案是：**eval 覆盖存在盲区**。

内部测试侧重于基准任务分布，而用户的实际使用场景远比 eval 覆盖的要宽。当 Bug 发生在 eval 未覆盖的边界时，内部测试完全正常，用户体验却持续受损。

这揭示了一个工程实践中的深层矛盾：

| 维度 | 内部 eval 关注 | 用户实际场景 |
|------|----------------|---------------|
| 任务复杂度 | 基准分布 | 真实长尾 |
| 调用模式 | 标准路径 | 边界操作 |
| 依赖服务 | Mock 稳定版 | 线上漂移版 |
| 时序依赖 | 隔离测试 | 并发/竞态 |

---

## 关键教训：Harness 治理是持续性工作，不是一次性配置

这篇复盘最重要的工程认知不是三个 Bug 本身，而是：

### 1. Eval 必须随模型能力进化

每一次模型能力迭代，都意味着之前验证过的 harness 参数需要重新校准。不是"设置一次就完了"，而是**每一次模型更新都是一次 harness 再治理**。

### 2. 间歇性 Bug 需要不同的监控策略

持续性 Bug 可以靠失败率监控。间歇性 Bug 需要**分布监控**——持续追踪响应质量的统计分布，而不是简单的成功/失败二元指标。

### 3. 用户反馈是最后一道防线，不是第一道

当支持工单成为主要发现渠道时，说明前面的：eval 覆盖、灰度监控、回归检测，都存在漏洞。

---

## 工程实践建议

对于所有构建 Agent 系统的团队：

1. **建立模型能力版本的 harness 参数矩阵**：每个模型版本对应一套 harness 参数，迭代时必须有回归验证。
2. **对关键路径实施分布监控**：不只是监控错误率，还要监控响应延迟、质量评分等连续分布。
3. **对第三方依赖建立降级策略**：单点依赖是间歇性 Bug 的温床。
4. **用户反馈工单要关联到具体 Bug 类型**：支持团队需要有能力区分"用户操作问题"和"系统间歇性 Bug"。

---

## 闭环关联

- **本文** → Anthropic 的三次间歇性 Bug 复盘，揭示 harness governance 与 model capability 迭代的动态关系
- **Project** → [anthropic-april-23-postmortem-harness-model-capability](/articles/fundamentals/anthropic-april-23-postmortem-harness-model-capability-2026.md)：更早一轮的 April 23 事故复盘，讲述 harness 参数随模型能力变化的校准必要性
- **闭环逻辑**：两次事故复盘形成递进——April 23 证明了"Harness 是模型能力的函数"，本篇则揭示了"间歇性 Bug 需要比持续性 Bug 更强的监控体系"

---

## 参考来源

- [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) — Anthropic Engineering Blog
