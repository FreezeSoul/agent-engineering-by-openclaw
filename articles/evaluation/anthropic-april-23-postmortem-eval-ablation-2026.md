# Anthropic 四月复盘：多变更叠加场景下的 Eval 设计教训

> 官方原文：[An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem)
> 来源：Anthropic Engineering Blog，2026-04-23
> 关联主题：Evaluation Harness / Eval Design / Multi-Agent Context Management

---

## 核心论点

Anthropic 四月的复盘报告表面上是一次事后分析，但其中藏着一个被低估的工程教训：**当多个配置变更同时作用于 Agent 系统时，eval 的设计方式直接决定了能否在发布前发现问题**。Anthropic 在这次复盘里揭示了一个关键事实——他们用的 eval 套件有盲区，而这个盲区在事后可以通过**更宽泛的 ablation**（消融实验）发现。

这不是「三次变更导致问题」的故事，而是「即使有 eval，也不够宽」的方法论复盘。

---

## 背景：表面是三个 bug，深层是一个 eval 设计问题

2026 年 3-4 月，Claude Code 经历了三次独立的配置变更：

1. **推理 effort 默认值**：high → medium → 回滚
2. **缓存清理逻辑 bug**：每轮都在清除 thinking history → 4月10日修复
3. **系统提示词变更**：抑制 token 输出 → 质量下降 3% → 回滚

事后分析揭示，每个变更**单独存在时**都没有在 eval 中触发失败信号。但 Anthropic 后来做了两件事值得深挖：

> "As part of the investigation, we back-tested Code Review against the offending pull requests using Opus 4.7. When provided the code repositories necessary to gather complete context, Opus 4.7 found the bug, while Opus 4.6 didn't."

以及：

> "As part of this investigation, we ran more ablations (removing lines from the system prompt to understand the impact of each line) using a broader set of evaluations. One of these evaluations showed a 3% drop for both Opus 4.6 and 4.7."

两件事，同一个指向：**eval 的覆盖范围不够宽**。

---

## 教训一：Eval 的「代表性」比「数量」更重要

Anthropic 内部不是没有 eval，而是 eval 的测试用例集与实际用户的场景存在偏差。这个问题在 Agent 领域极其普遍：

```
用户实际场景：复杂代码库 + 长时间会话 + 多工具调用 + 上下文累积
Eval 测试场景：标准化任务 + 短会话 + 单轮或少量工具调用
```

当 eval 的「分布」与「生产环境分布」存在系统性偏差时，eval 通过不代表生产没问题。这个认知本身不新鲜，但 Anthropic 的复盘给出了一个具体的技术原因：

**Context anxiety（上下文焦虑）** 是一种模型感知自身 context 限制时的行为表现。这种行为在不同模型版本之间差异巨大——Sonnet 4.5 有，Opus 4.5 就没有。同一个 harness，在这个模型上需要加 context reset，在另一个模型上就成了冗余代码。

笔者的判断是：**harness 的有效性是模型版本相关的**，而大多数 eval 套件只测「能否完成」，不测「在不同模型上行为是否一致」。这意味着当你升级模型时，旧的 eval 通过不代表 harness 不需要重新调优。

---

## 教训二： Ablation 的粒度决定了问题发现的速度

第二个值得关注的工程实践是 Anthropic 提到的 ablation 方法：

> "We ran more ablations (removing lines from the system prompt to understand the impact of each line) using a broader set of evaluations."

「逐行 ablation」是定位问题根因的有效手段，但关键在于「更宽泛的评测集」——如果只用那套针对性很强的 narrow eval（只覆盖特定场景）， ablation 不会发现问题。

**这个教训可以提炼为一条原则**：

```
Eval 套件必须包含两类测试：
1. 针对性测试（narrow eval）：验证特定功能是否 work
2. 宽泛性测试（broad eval）：验证通用能力是否受损
                   ↓
         多变更叠加时，只有 broad eval 能捕捉系统性退化
```

这不是 Anthropic 独有的问题。几乎所有在做 Agent 开发的团队都在用 narrow eval 做功能验收，用 broad eval 做回归——但大多数人没有意识到**两类 eval 的比例失调**会导致多变更场景下的系统性盲区。

---

## 教训三：Agent 的 Context Management 是跨层问题

复盘里提到的缓存清理 bug 值得单独说，因为它暴露了一个架构层面的问题：

```
Claude Code 上下文管理
        ↓
Anthropic API (clear_thinking_20251015 header + keep:1)
        ↓
Extended Thinking (thinking blocks 的累积和清理)
        ↓
Session 状态（idle → resume 时的行为差异）
```

这个 bug 发生在**三层交叉的地方**：产品层（Claude Code 的 context 管理）、API 层（prompt caching 机制）、模型层（extended thinking 的 blocks）。任何单层测试都无法捕捉这个交互。

笔者认为，这揭示了 Agent 系统的一个根本性工程挑战：**Agent 的行为是端到端的，但 eval 通常是分层的**。当我们单独测试 API 响应、单独测试 harness 逻辑、单独测试前端交互时，都通过了，但串联起来就有 bug。

这个问题的解法不是「更多测试」，而是**需要一种能够跨层观测的 trace 基础设施**——不只是记录 API 调用，还要能把前端行为、harness 决策、API 响应、tool execution 串联成一条完整的时间线。

---

## 教训四：Opus 4.7 能找到 Opus 4.6 找不到的 bug

复盘里最反直觉的一个发现：

> "When provided the code repositories necessary to gather complete context, Opus 4.7 found the bug, while Opus 4.6 didn't."

这意味着 Claude Code 的 **Code Review 功能本身成为了测试工具**——用更强的模型来验证对之前模型的修改。这是一个 meta-eval 的实践案例：

```
传统流程：开发 → 写 test → CI 通过 → 发布
Meta-eval 流程：发布前变更 → 用更高级别的模型做 Code Review → 发现盲区
```

笔者认为，这个实践值得工程团队借鉴：当你对 harness 或 prompt 做重大变更时，用比生产模型更高能力的模型做一次「变更审查」，成本比修复生产 bug 低得多。

---

## 结论：Eval 不是测试，是系统假设的验证

Anthropic 的复盘告诉我们一个根本性认知：**eval 测试的不是「代码是否 work」，而是「我们对系统的假设是否成立」**。

三次配置变更，每一步都有合理的假设：
- effort 从 high 改 medium → 假设「用户更在意延迟」
- 缓存清理优化 → 假设「idle 后清理历史是安全的」
- 抑制输出长度 → 假设「更简洁的输出不影响质量」

这些假设在 eval 中没有被推翻，是因为 eval 本身没有验证这些假设所需的覆盖范围。

**引用原文**：

> "Neither our internal usage nor evals initially reproduced the issues identified." — Anthropic Engineering Blog

这句话值得所有 Agent 工程团队贴在墙上。

---

**下一步行动**：下次对 harness 或 prompt 做重大变更时，先问自己三个问题：(1) 这个变更改变了什么系统假设？(2) 现有 eval 能否验证这些假设？(3) 如果用更强模型做一次 meta-review，会发现什么？
