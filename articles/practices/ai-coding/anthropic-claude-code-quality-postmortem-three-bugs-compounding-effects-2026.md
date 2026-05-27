# 三起事故，一次复盘：Anthropic 如何从 Claude Code 质量回归中提取工程教训

> 来源：[Anthropic Engineering Blog - An update on recent Claude Code quality reports](https://anthropic.com/engineering/april-23-postmortem)（Published Apr 23, 2026）
> 标签：#harness #evaluation #Claude-Code #工程复盘

## 核心观点

三个独立的事故各自由一个表面合理的决策引发，却在组合后产生了难以排查的复合效应。Anthropic 的复盘不是为了解释「问题如何解决」，而是在追问：**什么样的工程过程本身就能预防这类问题**。

---

## 一、三个改动，一条时间线

2026 年 3-4 月间，Claude Code 用户反馈质量下降。调查结果是三个独立的改动叠加导致的：

| 时间 | 改动 | 原意 | 实际效果 |
|------|------|------|---------|
| 3月4日 | 将 Opus 4.6 默认 reasoning effort 从 high 调为 medium | 减少高强度推理的过长延迟 | 用户感知到智能度下降，4月7日回滚 |
| 3月26日 | 闲置超过1小时的会话在恢复时清除旧的 thinking history | 减少 API 成本和延迟 | Bug 导致每轮都清除，Claude 变得「健忘」，4月10日修复 |
| 4月16日 | 添加 system prompt 指令限制输出长度 | 配合 Opus 4.7 的冗长倾向 | 与其他改动叠加导致 coding 质量下降 3%，4月20日回滚 |

每个改动单独看都「有道理」。但三者在不同时间窗口影响了不同的流量切片，叠加后的效应看起来像是「模型整体变差」——而实际上每个问题根源完全不同。

---

## 二、最值得深挖的一个 bug：Caching 优化如何变成记忆丢失

3月26日的改动是最复杂的案例，值得单独拆解。

### 设计意图

Anthropic 使用 **prompt caching** 降低连续 API 调用的成本。当一个会话闲置超过 1 小时，cache 自然失效（evict）。设计者的想法是：在 cache miss 时，顺便修剪掉旧的 thinking blocks（因为下次请求本来就要重新加载），既能减少 token 用量，又能降低延迟。

实现方式使用了 `clear_thinking_20251015` API header 加 `keep:1` 参数。

### Bug 的本质

> 笔者认为，这个 Bug 的精妙之处在于：它的「正确路径」和「错误路径」在代码层面完全一样，区别只在于**执行次数**——应该执行一次，实际执行了无数次。

实现逻辑大概是：

```
if session.is_stale():
    clear_old_thinking_blocks()
```

问题在于：这个标志在会话恢复后**没有被重置**。所以一旦会话被判断为 stale，后续每一轮都认为自己是 stale，继续清除。思考历史以每次 +1 轮的速度丢失，最终 Claude 只能看到最近的 1-2 个 thinking block，不知道自己为什么要做刚才做的事。

### 为什么这么难发现

文中提到的两个干扰因素值得记录：

1. **内部服务器端的消息队列实验**（与改动无关）让内部 traffic 模式与外部用户不一致
2. **CLI 中 thinking 显示方式的正交改动**掩盖了 bug 在大多数 CLI 会话中的表现

> 原文引用：  
> *"The changes it introduced made it past multiple human and automated code reviews, as well as unit tests, end-to-end tests, automated verification, and dogfooding."*

这个细节极为重要。在 Claude Code 的内部复盘中，他们明确说出「所有测试都通过了，但线上还是出了问题」。这不是测试质量问题，而是 **corner case 复现难度** 导致的质量信任幻觉。

---

## 三、一个值得注意的调试工具发现：Opus 4.7 能找到 Opus 4.6 找不到的 Bug

复盘报告中出现了一个非常特别的观察：

> 原文引用：  
> *"As part of the investigation, we back-tested Code Review against the offending pull requests using Opus 4.7. When provided the code repositories necessary to gather complete context, Opus 4.7 found the bug, while Opus 4.6 didn't."*

这是文献中罕见的「更强模型能发现自身引入的 Bug」的直接证据。Opus 4.7 的推理能力让它能够在提供完整仓库上下文的情况下，发现那个导致 thinking 被持续丢弃的逻辑错误。

这引出了一个重要的工程推论：**更强的模型本身可以作为更好的测试资源**。Anthropic 的应对措施是将 Code Review 支持更多仓库作为上下文，这本质上是在将模型的推理能力转化为质量保障基础设施的一部分。

---

## 四、System Prompt 改动为什么「看起来安全，做起来危险」

4月16日的 system prompt 指令：

> 原文引用：  
> *"Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail."*

这是最典型的「看似无害」改动——加一行 prompt 来控制 verbosity。内部测试没有发现回归，多周的 ablations 通过了。

但关键问题是：**他们在 Opus 4.7 发布时同步做了这个改动**。多个变化同时发生时，无法区分是哪个变化导致了问题。

> 笔者认为，这里暴露的是 **bundle release 策略的风险**：当多个改动打包发布时，即使每个单独的改动都通过测试，它们的交互效应仍然无法被独立测量。正确的做法是对每个改动分别做灰度，而不是打包在一起做「全量通过」。

---

## 五、他们承诺的工程改进：不是修 Bug，是修过程

复盘报告中最有价值的部分不是「我们修了什么」，而是「我们以后怎么做」。Anthropic 宣布了四类工程改进：

### 5.1 更严格的 System Prompt 变更管控

- 每次改动的 ablations 必须在更广泛的 eval 套件上运行
- 对任何可能影响模型智能度的改动，强制经过 **soak period**（浸泡期）和**渐进式灰度发布**
- 新工具：prompt change 的 review 和 audit 工具链

### 5.2 强制内部团队使用与用户完全相同的 build

> 原文引用：  
> *"We'll ensure that a larger share of internal staff use the exact public build of Claude Code (as opposed to the version we use to test new features)"*

这是一个看似简单的工程决策，但执行成本极高——测试分支和生产分支的分离在大型工程团队中几乎是默认设置。打破这个默认需要明确的组织承诺。

### 5.3 Code Review 工具支持更多仓库上下文

这是对 5.1 的具体落地：用更强的模型能力武装质量保障流程。

### 5.4 Model-specific 改动必须 gate 到对应模型

这是针对「bundle release」问题的直接对策：每个模型有自己独立的改动 gate，不允许跨模型批量生效。

---

## 六、工程教训：什么比修 Bug 更重要

笔者认为，这次复盘最重要的观察不是三个 bug 本身，而是以下三点：

### 教训 1：Corner case 的复现难度是质量保障的盲区

这个 Bug 只在「会话 idle 后恢复且后续继续有交互」这个特定条件下触发。自动化测试很难覆盖这种「跨时间状态的边界条件」，因为大多数测试框架默认测试是即时的。真正的修复需要 **状态化测试**（stateful testing）或者在真实用户流量上的 shadow mode 验证。

### 教训 2：「通过测试」不等于「安全」

> 原文引用：  
> *"Combined with this only happening in a corner case (stale sessions) and the difficulty of reproducing the issue, it took us over a week to discover and confirm the root cause."*

「测试通过」是必要条件，不是充分条件。尤其当改动涉及有状态系统（session、cache、context）时，corner case 的复现难度可以让最严格的测试套件也失效。

### 教训 3：多个「合理改动」的组合效应是非线性的

三个改动各自由不同工程师在不同时间做出，单独看都通过 review。组合后的效应在用户层面才显现。这意味着 **code review 只能保证单个改动的质量，不能保证改动组合的质量**。这需要更高级别的流程保障（如上文提到的渐进灰度发布）。

---

## 结语

Anthropic 选择了公开承认三个独立事故的详细复盘，而不是用「我们修好了」一笔带过。这份复盘的价值在于它展示了：在 AI 产品的语境下，「工程过程」和「模型能力」之间的界限正在模糊——更强的模型本身成为了更好的测试工具，而模型的每一次推理能力提升，也意味着模型行为空间更大，需要更严格的 harness 和工程流程来兜底。

这不是 Claude Code 的问题。这是整个 Agent 时代工程质量的共同命题。

---

*本文基于 Anthropic Engineering Blog 原文写作，已验证内容的工程准确性。*