# Anthropic Claude Code 质量退化复盘：三个改动如何叠加摧毁了用户体验

> 原文：Anthropic Engineering Blog — [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem)（2026-04-23）

## 核心论点

2026年3-4月，Anthropic 收到了大量用户反馈：Claude Code 质量变差了。但这不是模型退化——是三个 Harness 层的产品改动在不同的时序上叠加，最终表现为用户感知到的"AI 变笨"。**这个案例揭示了一个关键工程现实：Harness 层（而非模型层）的改动，能以非线性的方式影响最终用户体验。**

---

## 一、事件全景：三个改动，三个时间点，三种失效模式

Anthropic 在调查后确认，用户的质量退化反馈来自三个完全独立的改动，每个改动在不同时间点、以不同机制影响了不同版本的 Claude：

| 时间 | 改动 | 影响版本 | 结果 |
|------|------|---------|------|
| 3月4日 | 默认 reasoning effort 从 high 降为 medium | Sonnet 4.6, Opus 4.6 | 用户感知到"AI 不够聪明了" |
| 3月26日 | Prompt caching 优化 bug：每次请求都清除历史 reasoning | Sonnet 4.6, Opus 4.6 | 遗忘、重复、无意义工具调用 |
| 4月16日 | System prompt 加入长度限制（≤25词/工具调用） | Sonnet 4.6, Opus 4.6, Opus 4.7 | 编码质量下降 3%（ ablation 证实）|

这三个改动在不同的 traffic slice 上生效，叠加后的aggregate effect 看起来像"全面的、不一致的质量退化"——这正是用户感知到的。

---

## 二、改动一：默认 Reasoning Effort 的错误权衡

### 背景

Claude Code 的 reasoning effort 参数控制模型在回答前的"思考"量。Opus 4.6 发布时，默认设为 high。但随后收到反馈：high 模式下模型思考时间过长，UI 有时会冻结。

> "In our internal evals and testing, medium effort achieved slightly lower intelligence with significantly less latency for the majority of tasks."
> — Anthropic Engineering Blog

### 决策过程

Anthropic 内部测试表明：medium effort 在大多数任务上"稍微低一点 intelligence + 明显更低的延迟"。他们把这个权衡理解为合理的工程取舍，并在 3月4日将默认值改为 medium。

### 为什么这是错的

用户反馈给出了截然不同的结论：**用户宁愿接受高延迟，也不愿意接受低智能**。模型思考时间长是一个可以容忍的不便，但输出质量下降是致命的。

Anthropic 在 4月7日 revert 了这个改动，恢复了 xhigh/high 的默认值。

### 工程教训

effort 参数的测试不能只看"平均任务"——少数高复杂度任务的失败会被"平均"掩盖，但这些任务往往是用户最在意的。

---

## 三、改动二：Prompt Caching 优化的 Bug

### 原始设计

Claude Code 使用 prompt caching 降低用户成本。当 session 空闲超过1小时后重新激活，Anthropic 做了一个优化：清理旧的 thinking sections，减少需要发送的 uncached tokens。

实现方式是使用 `clear_thinking_20251015` API header 配合 `keep:1`——只保留最近一个 reasoning block，其余清除。

### Bug 的本质

这个优化有一个致命实现错误：**不是"空闲1小时后清除一次"，而是"空闲1次后就每轮都清除"**。

> "Instead of clearing thinking history once, it cleared it on every turn for the rest of the session."
> — Anthropic Engineering Blog

这意味着：如果用户 session 在空闲后被重新激活，清除动作会触发一次，但随后**每次后续请求都继续执行这个清除逻辑**，导致：

- 每次工具调用后的 reasoning history 都被丢弃
- Claude 不知道自己为什么选了某个工具
- 行为表现为：遗忘、重复、无意义的选择

### 为什么内部测试没发现

Anthropic 事后分析发现了两个干扰因素：

1. **一个未公开的服务端实验**（与消息队列相关）掩盖了问题
2. **CLI 界面中对 thinking 的显示方式**掩盖了这个 bug 对大多数 session 的影响

更关键的是，这个 bug 只在一个 corner case 下触发（stale sessions），常规测试没有覆盖到。

### Opus 4.7 Code Review 发现了这个 Bug

有趣的是，调查过程中用 Opus 4.7 的 Code Review 功能对有问题的 PR 进行了 back-test：

> "When provided the code repositories necessary to gather complete context, Opus 4.7 found the bug, while Opus 4.6 didn't."
> — Anthropic Engineering Blog

这说明更强大的模型能发现这类跨请求状态管理的 subtle bug。

---

## 四、改动三：System Prompt 长度限制

### 背景

Claude Opus 4.7 有一个行为特点：比前任模型更啰嗦（verbose）。这在难题上更聪明，但也意味着更多的 output tokens。

Anthropic 在 4月16日发布 Opus 4.7 时，在 system prompt 中加入了一条看似无害的指令：

> "Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail."

### 为什么这伤害了智能

经过内部 ablation（逐行移除 system prompt 以理解每行影响），Anthropic 发现：

> "One of these evaluations showed a 3% drop for both Opus 4.6 and 4.7. We immediately reverted the prompt as part of the April 20 release."
> — Anthropic Engineering Blog

这条长度限制与 Opus 4.7 的训练数据分布不匹配，强制压缩 reasoning 空间损害了模型的实际能力。

### 问题根源：多行 System Prompt 变化的叠加效应

System prompt 不是独立作用的——它在和其他 prompt 变化的组合下产生了非预期效果。单独测试时，这个限制的影响被低估了。

---

## 五、为什么这么多防线都失效了

这三个改动的共同特点是：**都通过了多重测试和审查，但最终都有问题**：

| 防线 | 是否有效 |
|------|---------|
| 人工 code review | ❌ 全部通过 |
| 单元测试 | ❌ 全部通过 |
| 端到端测试 | ❌ 全部通过 |
| 自动化验证 | ❌ 全部通过 |
| Dogfooding（内部使用）| ❌ 因干扰因素未发现 |
| 用户反馈 | ✅ 但最初被当作"正常波动" |

> "Neither our internal usage nor evals initially reproduced the issues identified."
> — Anthropic Engineering Blog

这说明：对于 subtle 的产品改动，常规的测试套件可能不足以发现用户体验层面的 regression。

---

## 六、工程教训：Harness 层的变化如何影响模型行为

### 1. Prompt Caching 是状态管理的黑盒

Prompt caching 在降低 latency 的同时，也引入了跨请求的状态依赖。当改动涉及"何时清除历史"时，实际上是在改变模型的"记忆范围"。这个范围边界的行为变化很难通过常规测试捕获。

### 2. System Prompt 的每行变化都可能影响模型能力

System prompt 不是"提示词"那么简单——它定义了模型的行为约束空间。当加入长度限制时，实际上是在约束模型的 reasoning 空间，而这个约束对某些任务类型的影响是非线性的。

### 3. Eval 套件需要覆盖"质量维度"，而不仅仅是"正确率"

如果 Anthropic 的 eval 套件只测功能正确性，可能无法发现 reasoning effort 降低带来的"主观质量下降"。用户感知的是 intelligence 的下降，而这可能不会在自动化评测中体现。

### 4. 多改动同时发生时，叠加效应难以预测

三个改动在不同的 traffic slice 上生效，但最终的 aggregate effect 看起来像是"全面的质量退化"。这种非线性叠加使得问题定位变得困难。

---

## 七、改进方向：Anthropic 承诺的改变

1. **更大比例的内部员工使用与公开版本完全一致的 Claude Code**（而非带有未发布功能的测试版）
2. **Code Review 工具升级**：支持更多仓库作为 context，让 Opus 4.7 能发现更多这类 bug
3. **System prompt 变更的更严控制**：对每次 prompt 变更执行 per-model eval 套件 + ablation + soak period + gradual rollout
4. **Model-specific 变更需要 gate 到特定模型**：避免跨模型的泛化影响

---

## 关联项目

本篇文章分析的三个改动都与 **Claude Code 的 harness 层状态管理** 相关。社区随后出现了多个针对这些问题的工具和分析：

- **[claude-code-cache-fix](https://github.com/cnighswonger/claude-code-cache-fix)**（226 ⭐）：社区修复了导致 resumed sessions 成本增加 20 倍的 prompt cache regression——直接对应本文描述的第二个改动
- **[claude-code-hidden-problem-analysis](https://github.com/ArkNill/claude-code-hidden-problem-analysis)**（108 ⭐）：量化分析了 Max 计划用户因 cache bug 导致的 10-20 倍 token 膨胀

这两个项目都是对 Anthropic 公开 postmortem 的直接响应，证明了**透明的事后分析能够激发社区的二次验证和改进**。

---

**引用来源**：

- [Anthropic Engineering Blog: An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem)
- Anthropic 公开承诺的改进措施（同一文章中）
