# Anthropic 四月事故复盘：为什么说"Harness 是模型能力的函数"

> **来源**: [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) (2026-04-23)
> **核心论点**: Claude Code 近期质量下降源于三次独立变更，而它们的共同问题是——没有充分考虑"模型能力进化后，harness 参数需要重新校准"这一核心原则。
> **关键词**: harness governance, eval awareness, reasoning effort, prompt caching, system prompt change management

---

## 先说结论：Harness 是模型能力的函数，不是固定配置

Anthropic 这次的复盘有一个隐含但极其重要的工程认知：

> 当模型能力进化时，原本经过验证的 harness 参数会变得不再适用。如果不重新校准，harness 会从"放大模型能力"变成"抑制模型能力"。

这不是 Claude Code 独有的问题——它是所有 Agent 系统在模型迭代周期中都会遇到的挑战。本篇文章从这次事故的三条根因出发，拆解 Harness 治理的核心教训。

---

## 三次变更，三种失效模式

### 1. 推理努力默认值：从 High 降为 Medium

**背景**：Opus 4.6 发布时将默认推理努力设为 High，但用户反馈高努力模式有时延迟过长（UI 看起来像冻住了），于是团队将其改为 Medium。

**决策依据**：
> "In our internal evals and testing, medium effort achieved slightly lower intelligence with significantly less latency for the majority of tasks."

**结果**：用户报告 Claude Code "感觉不如以前聪明"。团队花了数周做设计迭代（启动提醒、内联 effort 选择器、恢复 ultrathink），但大多数用户保留了 Medium 默认值。直到 4 月 7 日才完全回滚。

**关键问题**：内部 evals 和用户实际使用之间存在 eval 盲点。Internal evals 侧重基准测试覆盖的任务分布，而用户在实际 coding 场景中的任务复杂度分布与 evals 不一致。

**工程教训**：当调整影响"模型聪明程度"的参数时，soak period 和 gradual rollout 是必要的——不能只依赖内部 evals 决定默认值的变更。

---

### 2. 缓存优化逻辑：清空 thinking 历史的 bug

**背景**：团队在 3 月 26 日做了一个"优化"：当 session 空闲超过一小时后，清除旧的 thinking sections 以减少恢复时的 token 开销。

**实现方式**：使用 `clear_thinking_20251015` API header 配合 `keep:1`，期望只在第一次恢复时清除历史，之后继续发送完整 reasoning。

**实际 bug**：由于实现错误，这个逻辑在每次请求时都会触发，而不是只在第一次恢复时触发。结果是：超过一小时空闲后，每个请求都会丢弃之前的 thinking blocks，导致 Claude 越来越"失去记忆"。

> "Claude would continue executing, but increasingly without memory of why it had chosen to do what it was doing. This surfaced as the forgetfulness, repetition, and odd tool choices people reported."

**触发条件苛刻**：这个 bug 只在 corner case（stale sessions）发生，而且两个无关的内部实验（message queuing 实验 + thinking 显示的改动）压制了这个 bug 在大多数 CLI session 中的可见性，导致即使测试外部构建也未能发现。

**发现过程**：Anthropic 用 Opus 4.7 的 Code Review 功能对有问题的 PRs 进行 back-test，发现 4.7 能找到这个 bug，而 4.6 不能。这说明更强的模型在复杂 context 下有更好的推理能力。

**工程教训**：
1. 跨 API + context management + extended thinking 的交叉逻辑是脆弱的，需要更严格的测试覆盖
2. 强模型可以作为"辅助 code reviewer"发现这类 corner case bug

---

### 3. System Prompt 改动：长度限制导致智能下降

**背景**：Opus 4.7 发布时有一个已知的行为特点——比前身更啰嗦（因为更聪明）。团队在准备 4.7 的 harness 时加入了这条 system prompt：

> "Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail."

**验证过程**：多周内部测试 + 一系列评估测试，未发现回归。

**实际问题**：作为调查的一部分，团队用更广泛的评估集做了 ablation（逐行移除 system prompt 以理解每行的影响）。结果发现这条限制对 Opus 4.6 和 4.7 都造成了 3% 的智能下降。

**关键问题**：这条 rule 在简单任务上效果不错，但在需要深度 reasoning 的复杂任务上，它阻止了模型展现完整的推理链。模型会为了满足"≤25 words"的限制而跳过关键推导步骤。

**回滚**：发现后立即在 4 月 20 日回滚。

**工程教训**：
1. "减少 verbose" 和 "保持智能" 之间的权衡在模型间不一致，且取决于任务难度
2. System prompt 的每一条改动都需要对每个模型版本做独立评估，不能跨模型版本继承

---

## 共性问题：Harness Governance 的缺失

三次变更有一个共同的结构性问题：

```
变更 → 内部 evals 通过 → 灰度发布 → 用户反馈暴露问题 → 回滚
```

这个链条暴露了三个治理缺陷：

| 维度 | 问题 |
|------|------|
| **Eval 覆盖** | 内部 evals 未能覆盖用户实际任务分布，特别是复杂 coding 任务 |
| **跨版本假设** | System prompt 改动在不同模型版本间没有独立验证 |
| **渐进发布** | 默认值变更（reasoning effort）没有梯度验证机制 |

Anthropic 提出的改进行动：

> "We will run a broad suite of per-model evals for every system prompt change to Claude Code, continuing ablations to understand the impact of each line, and we have built new tooling to make prompt changes easier to review and audit."

这说明 **per-model eval** 和 **prompt change audit trail** 是 Agent 系统 harness governance 的基础设施级需求。

---

## 核心判断：为什么模型进化时 harness 要跟着变

这次事故有一个深层原因没有被明确说出，但贯穿全文：

**模型能力进化时，harness 参数的最优值会漂移。**

举例：
- 模型更强时，推理努力 High 的收益变大，Medium 的代价也变大（损失更多智能）
- 模型更聪明时，verbose 的收益是更完整的推理链，抑制 verbose 的代价是更大的信息损失
- 模型 context 处理能力变强时，之前为节省 token 设计的缓存清理策略可能反而损害性能

这意味着：

> **Harness 不是一次性配置，而是随模型版本动态校准的参数空间。**

从工程角度，这意味着：
1. 每个模型版本需要自己的 harness eval baseline
2. 模型升级时，harness 参数的回归测试是必须的
3. 改变默认 harness 参数（如 reasoning effort）需要当作"半个模型发布"来处理

---

## 与之前文章的关联

本文与 [Opus 4.6 如何重塑 Harness 设计哲学](./anthropic-opus-4-6-harness-simplification-model-capability-2026.md) 形成了深层呼应。那篇文章的核心观点是"当模型变强，有些 harness 可以简化"——而本文的教训是"简化的前提是重新校准，不是直接删除"。

两篇文章合在一起，给出了完整的 picture：
- **Opus 4.6**：模型变强 → 可以删减哪些 harness
- **April 23 Postmortem**：删减/变更 harness 时如何避免踩坑

---

## 引用

1. Anthropic Engineering: "An update on recent Claude Code quality reports" — https://www.anthropic.com/engineering/april-23-postmortem
2. Claude Code Prompt Caching: "Lessons from building Claude Code: Prompt caching is everything" — https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything
3. Claude Code Review Documentation: https://code.claude.com/docs/en/code-review

---

**标签**: #harness #eval #model-capability #claude-code #anthropic
**分类**: fundamentals
**写作时间**: 2026-05-17