# 从 Claude Code 质量事件看 Agent 工程的核心教训：问题不在模型，在 Harness

> **核心观点**：Anthropic 公开披露的 Claude Code 质量回退事件，是一堂关于 Agent Harness 工程的必修课。三个看似合理的优化（reasoning effort 默认值、thinking 缓存清理、输出长度控制），通过不当交互产生了复合效应，让用户感觉模型"变笨了"——但模型本身没有变化，变化的是 harness 层。这是一个至今仍在发生的设计陷阱。

## 一、事件还原：三个变化如何叠加成"模型退化"

2026年3月到4月间，Anthropic 陆续收到用户反馈：Claude Code 的响应质量出现了广泛且不一致的下降。用户描述的现象包括"模型变得健忘"、"输出重复"、"任务中途卡住"等。

调查的结论出乎意料：**模型 API 本身没有任何问题**。问题来自三个各自独立看似合理的 harness 层改动，它们在不同的流量切片上于不同时间生效，叠加后呈现出一种"全面退化"的假象。

### 1.1 第一个变化：Reasoning Effort 默认值从 High 降到 Medium

**背景**：2026年2月 Anthropic 发布 Opus 4.6，将 Claude Code 的默认 reasoning effort 设置为 high。这带来了更好的输出质量，但部分用户反馈高推理强度导致 UI 出现"冻结"感，延迟过高。

**决策逻辑**：Anthropic 的内部测试表明，medium effort 在大多数任务上只损失少量智能，但显著降低了延迟和 token 消耗。他们在3月4日将默认值改为 medium，并在产品内提供了解释对话框。

**问题**：用户实际体验与预期不符。社区反馈表明多数用户宁愿接受更高延迟也不愿接受质量下降。Anthropic 在4月7日回滚了这一决策。

> 引用原文："In our internal evals and testing, medium effort achieved slightly lower intelligence with significantly less latency for the majority of tasks... We rolled out a change making medium the default effort, and explained the rationale via in-product dialog." — Anthropic Engineering Blog

**教训**：effort 参数本质上是"智能 vs 延迟"的二元权衡，不同用户有不同的偏好，且偏好因任务而异。在没有充分数据支撑的情况下改动全局默认值，等于对所有用户强制执行一种固定偏好——这是高风险操作。

### 1.2 第二个变化：Thinking 缓存清理逻辑的 Bug

**背景**：Anthropic 使用 Prompt Caching 降低用户成本。当会话空闲超过一小时，API 会清空缓存以释放空间。原本的设计意图是：如果会话空闲超过一小时，清除旧的 thinking 内容（因为请求本身会 cache miss），从而减少发送到 API 的未缓存 token 数。

**实现逻辑**：他们使用了 `clear_thinking_20251015` API header 配合 `keep:1`，即只保留最近一个 thinking 块。

**Bug**：实现中有一个致命缺陷——清理逻辑不是只执行一次，而是**每一轮都执行**。一旦会话跨越了空闲阈值，之后的每一次请求都会清除所有历史 thinking，只保留最近一块。这导致：

1. Claude 失去了对"为什么这样做"的理解，执行变得没有连贯性
2. 每轮请求都是 cache miss（因为每次都修改了 context）
3. 用户感觉模型"越来越健忘"，越来越重复

> 引用原文："Instead of clearing thinking history once, it cleared it on every turn for the rest of the session. After a session crossed the idle threshold once, each request for the rest of that process told the API to keep only the most recent block of reasoning and discard everything before it. This compounded..." — Anthropic Engineering Blog

**关键**：这个 bug 在代码审查、单元测试、端到端测试、自动化验证和内部 dogfooding 中都**没有**被发现。原因：它只发生在"会话空闲超过1小时后的第一轮请求"这个corner case，且有两个独立的内部实验（消息队列实验 + thinking 显示逻辑改动）恰好抑制了这个 bug 在大多数 CLI 环境中的可见性。

### 1.3 第三个变化：系统提示词的长度限制指令

**背景**：Opus 4.7 有一个已知的行为特征：相比前代模型，输出更冗长（verbose）。这是因为更长的输出对应更强的智能——它是模型训练的副作用，不是 bug。但对于实际使用场景，冗长的输出意味着更高的 token 消耗和更慢的响应。

**决策**：Anthropic 在4月16日发布 Opus 4.7 时，在系统提示词中增加了一条指令：

> "Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail."

**问题**：这条指令与产品中其他提示词变更结合后，产生了超预期的副作用——在某些评测中导致3%的智能下降。这是一个典型的"prompt 耦合效应"：单独测试每条指令时没有发现问题，但多条指令组合后产生了意外的交互。

这条指令在4月20日被回滚。

## 二、复合效应的工程教训：Harness 的三大陷阱

### 2.1 陷阱一：多改动在不同流量切片上独立生效——"静默叠加"

三个变化不是在同一时间、同一流量切片上发生的：

| 变化 | 生效时间 | 影响模型 | 影响切片 |
|------|---------|---------|---------|
| Medium effort 默认 | 3月4日 | Opus 4.6, Sonnet 4.6 | 全部用户 |
| Thinking 缓存 bug | 3月26日 | Opus 4.6, Sonnet 4.6 | 会话空闲>1h的用户 |
| 长度限制指令 | 4月16日 | Opus 4.6, 4.7, Sonnet 4.6 | 全部用户 |

由于每个变化影响不同的用户子集，且在不同时间发生，Anthropic 早期收到的报告是零散的、不成模式的。他们在3月初就开始调查，但内部评测没有复现问题——因为评测没有覆盖"空闲会话恢复"这个具体场景。

**工程教训**：当你在 harness 层做优化时，要假设**多个优化会同时生效**，并测试它们之间的交互。单元测试通过不等于集成测试通过，更不等于生产环境行为符合预期。

### 2.2 陷阱二：优化目标（延迟/成本）与核心价值（智能）产生冲突

三个变化的核心动机都是**降低延迟或token消耗**：

- Medium effort → 减少推理时间
- 缓存清理 → 减少 cache miss 带来的成本
- 长度限制 → 减少输出 token 数

这些优化目标本身没有问题，但当它们叠加在"智能"这个核心价值上时，产生了权衡失衡。Anthropic 在调查后承认："Medium effort 是错误的权衡"——他们优先了延迟而损失了智能，且没有充分认识到这个决策的代价。

**工程教训**：在 Agent 系统中，"速度"和"智能"之间的权衡比传统软件更尖锐。当你在 harness 层做优化时，要明确问：**这个优化对"任务完成质量"的影响是什么**？不能只看 P50 延迟，要看 P95/P99 质量。

### 2.3 陷阱三：Prompt 中的"长度控制"是最危险的干预点

"Length limits: keep text between tool calls to ≤25 words"这条指令揭示了一个深层问题：**你越明确地告诉模型"少输出"，模型在复杂任务上的判断力就越受限**。

模型之所以在 Opus 4.7 上更冗长，是因为它在做复杂推理时需要展开中间步骤。当你强制压缩输出到25词以内，你实际上是在告诉模型"不要展开思考"——这与"更聪明的模型"之间存在根本性冲突。

**工程教训**：任何试图通过 prompt 指令控制输出长度的做法，都要极其谨慎地评估其对智能的影响。这与模型的能力边界紧密相关：简单任务可以接受长度限制，但复杂任务的推理质量与中间步骤的展开程度正相关。

## 三、Anthropic 的修复方案：系统性防御

Anthropic 在事件后宣布了四项系统性改进：

### 3.1 大幅扩大内部测试覆盖范围

> "We are going to ensure that a larger share of internal staff use the exact public build of Claude Code (as opposed to the version we use to test new features)" — Anthropic Engineering Blog

内部测试环境与用户环境的差异，是这个 bug 没有被提前发现的核心原因。他们现在要求更多内部员工使用与用户完全相同的构建版本。

### 3.2 系统提示词变更的 per-model 评测 + Ablation 分析

> "We will run a broad suite of per-model evals for every system prompt change to Claude Code, continuing ablations to understand the impact of each line" — Anthropic Engineering Blog

"ablations"（消融实验）是机器学习中的标准做法——逐一移除系统提示词中的指令，测量每条指令对最终输出的影响。他们现在将这个方法系统化地应用于每次 prompt 变更。

### 3.3 模型特定变更必须精确限定目标模型

> "We've additionally added guidance to our CLAUDE.md to ensure model-specific changes are gated to the specific model they're targeting." — Anthropic Engineering Blog

长度限制指令影响的是 Opus 4.6、4.7 和 Sonnet 4.6，但调整本身只需要针对某个模型。这个教训推动了他们建立模型变更的隔离机制。

### 3.4 高风险变更的 Soak Period + Gradual Rollout

> "For any change that could trade off against intelligence, we'll add soak periods, a broader eval suite, and gradual rollouts so we catch issues earlier." — Anthropic Engineering Blog

关键认知：**任何可能影响智能的变更，都不能直接全量发布**。需要灰度、监控和快速回滚机制。

## 四、这个事件对 Agent 工程的普遍意义

Claude Code 质量回退事件，本质上不是"模型变差了"，而是**Harness 层对模型行为的影响被系统性低估了**。三个看似独立的优化通过 harness 层产生了非预期的耦合效应，最终表现为用户感知到的"模型退化"。

对于构建 Agent 系统的工程师，这个事件提供了几个可复用的设计原则：

**1. Harness 层变更必须有完整的质量门禁**
不是单元测试通过就行，而是要在实际用户场景中验证智能不下降。这意味着需要建立"任务完成质量"的评测集，而非只测延迟和 token 消耗。

**2. 多优化同时生效时要测试交互效应**
当你同时调整 effort、缓存策略和 prompt 指令时，要假设它们可能产生非预期交互。单独看都没问题，组合起来可能产生复合效应。

**3. "长度控制"类 prompt 是高危操作**
任何强制模型压缩输出的指令，都要单独评估其对复杂任务的影响。简单任务可能完全不受影响，复杂任务的推理质量却可能显著下降。

**4. 优化延迟和成本不能以牺牲智能为代价**
Anthropic 在事后承认 medium effort 是"错误的权衡"。这个判断的代价是用户信任。在 Agent 系统中，用户的核心期望是"任务能完成"，而不是"响应要快"。

---

**引用来源**：
- [An update on recent Claude Code quality reports - Anthropic Engineering](https://www.anthropic.com/engineering/april-23-postmortem)（发布于2026年4月23日）
- [Lessons from building Claude Code: Prompt caching is everything - Anthropic Blog](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)
- [Claude Code - Best practices for agentic coding - Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-best-practices)

**标签**：`harness-engineering` `claude-code` `agent-engineering` `quality-regression`
**分类**：`harness/`