# Anthropic Claude Opus 4.7：自我验证为何是 Agent 可靠性的范式转移

## 核心命题

Opus 4.7 最值得关注的不是跑分数字，而是一个内生能力：**自我验证**——模型在行动前自发验证自己的假设，而不是等人类prompt它这么做。这不是 prompt engineering 的胜利，是模型层面的架构改变。

## 从「被要求验证」到「自发验证」

此前版本的 Claude 模型会验证假设，前提是你在 prompt 里明确要求它这么做。4.7 的不同之处在于：自我验证变成了模型的**默认行为**，而不是需要引导的技巧。

根据 Vercel 工程师 Joe Haddad 的报告，Opus 4.7 在开始工作前会先对系统代码做证明（proofs）——这件事没有出现在任何 prompt 里。模型自己决定要先验证，再动手。

类似的行为在多个合作伙伴的报告中重复出现：
- **Hex** 报告模型会主动标记缺失数据，而不是发明看似合理但实际错误的备选值
- **Devin CEO Scott Wu** 说 Opus 4.7 能连贯运行数小时，攻克难题而不是放弃
- **CursorBench** 从 58%（Opus 4.6）跃升至 70%（Opus 4.7），而在 CursorBench 这样设计来抵抗数据污染的 benchmark 上，这个数字更有说服力

笔者认为，这种范式转移的实质是：**模型开始将「验证」视为任务的一部分，而不是执行的附加步骤**。这要求模型对「什么是正确的」有足够强的内部判断，而4.7之前的能力边界还不足以支撑这种判断的可靠性。

## 为什么这比分数更重要

传统的模型能力提升通常表现为「更好的 benchmark 数字」或「更低的幻觉率」。这些固然重要，但不能改变一个根本问题：在 Agentic Coding 场景里，模型最终需要被人信任地委托任务。

信任的基础是什么？不是模型的单次准确率，而是**在没有监督的情况下，模型能否发现自己的错误**。

Claude Code 质量回归事件已经说明：即使模型本身没变，harness 参数的静默叠加也会导致用户体验到「模型退化」。反过来，当模型有了自我验证的内生能力，同样的 harness 参数叠加不会导致用户感知到的质量下降，因为模型能自己发现并纠正问题。

这才是 Opus 4.7 对 Agent 工程真正重要的原因。

## 自适应思考的第五档：xhigh

Opus 4.7 引入了 xhigh（extra high）作为自适应思考的第五档，位于 high 和 max 之间。Claude Code 将所有计划的默认努力级别提升到了 xhigh。

这不是一个简单的参数调整。xhigh 意味着模型在复杂任务上投入更多推理资源，同时在简单任务上保持较低消耗。这与 OpenAI o3 的「让模型自己决定思考时长」路线相似，但 Anthropic 选择的是更显式的档位控制而非完全自适应。

笔者认为，这个设计选择体现了两种路线的哲学差异：OpenAI 让模型自己决定思考量（黑盒），Anthropic 给用户保留档位选择权（白盒）。对于需要精细控制 token 成本的 Agent 应用来说，白盒方案更友好。

## Task Budgets：让模型自己控制任务粒度

4.7 引入的 Task Budgets 功能是一个常被忽视的重要的变化。这是一个 advisory cap（ advisory：模型能看到这个上限并据此调整行为，而不是硬性截断）。

关键参数：
- 最小值 20k tokens
- 模型自己决定如何分配：30k 用于探索，90k 用于写代码，40k 作为缓冲
- 不同于 max_tokens 的是，模型能感知到 budget 的存在并主动规划

这对于长时运行的 Agent 场景意义重大。一个 Agentic Coding loop 可能持续数小时，过程中有大量的工具调用和中间结果。如果没有 budget 控制，token 消耗是不可预测的；如果只是硬性截断（max_tokens），模型无法智能地在关键步骤上分配资源。

Task Budgets 的实质是：**给模型一个它能理解并主动响应的资源边界**，而不是给一个它看不见的硬天花板。

## 新的 breaking changes：必须知道才能迁移

Opus 4.7 有几个影响 Agent 应用的 API 变化：

### 1. Extended Thinking 变成了需要显式开启

之前带 thinking 参数的请求在 4.7 上会返回 400。无 thinking 字段的请求现在默认不运行思考。这是一个需要检查所有 API 调用代码的 breaking change。

### 2. 采样参数被移除

之前用于控制采样行为的参数（temperature、top_p 等）在 4.7 中被移除，必须用 prompting 来塑造行为。

### 3. 新 tokenizer 增加了 token 消耗

同样的输入内容在 4.7 上可能映射到 1.0-1.35 倍的 tokens（取决于内容类型）。对于已经有 token 预算控制的 Agent 系统，这个系数变化可能影响成本估算。

### 4. Prefill 被阻止

之前可以通过在 assistant 消息中 prefill 来引导输出格式，现在返回 400。

Anthropic 在 Claude Code 中内置了自动化迁移工具 `claude /claude-api migrate`，可以扫描代码库并自动应用必要的修改。对于有存量 Claude Code 配置的用户，这是第一步应该运行的东西。

## Opus 4.7 对 Agent 工程格局的影响

### 1. 基准测试需要重新校准

SWE-bench Verified 从 80.8%（Opus 4.6）提升到 87.6%（Opus 4.7），CursorBench 从 58% 提升到 70%。这两个数字的同时跃升表明这不是某个 benchmark 的过拟合，而是底层能力的系统性提升。

### 2. 「验证」从 Prompt 层下降到模型层

未来对 Agent 可靠性的优化，更多会转向 harness 设计（因为模型已经内生了验证能力），而不是 prompt 优化（因为 prompt 层已经无法教会模型自我验证）。

这与 Claude Code April 23 postmortem 的教训形成对照：harness 参数的静默叠加会破坏用户对「模型变好了」的感知，但 harness 参数的优化空间也因此变得更清晰了——因为模型层面的验证能力已经到位。

### 3. 企业级 Agent 部署更可行

「模型在长时间运行中自己发现并纠正错误」这个能力，使得将复杂任务委托给 Agent 的风险显著降低。对于之前因为不敢相信模型会自己停手而需要高密度人工监督的场景，Opus 4.7 提供了新的信任基础。

## 笔者的判断

Opus 4.7 不是又一个「分数更高」的传统模型升级。它代表了一个微妙的范式转移：**从「模型能做什么」到「模型默认做什么」的转变**。

自我验证作为默认行为而非需要 prompt 引导的技巧，这是质的不同。它意味着在设计 Agent 系统时，我们可以更少依赖「让模型按特定顺序执行验证步骤」的 prompt 层技巧，更多依赖模型自身的判断可靠性。

对于 Agent 工程的实际影响是：
- Prompt 层对「验证」的控制可以简化，模型会自发做
- Harness 设计变得更关键，因为模型层的可靠性已经提升，剩余的不确定性更多来自 harness 参数
- 长时运行的 Agent 应用场景现在有了更强的模型层保障

## 参考来源

- Anthropic 官方发布：https://www.anthropic.com/news/claude-opus-4-7
- CursorBench 数据：https://www.anthropic.com/claude/opus
- DEV Community 迁移指南：https://dev.to/speedy_devv/claude-opus-47-what-actually-changed-for-agentic-coding-4i27
- Cursor CEO Michael Truell 对 CursorBench 的评论：https://www.anthropic.com/news/claude-opus-4-7