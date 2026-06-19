# Claude Code Session 决策树：/usage /rewind /compact 2026

> **来源**：[Using Claude Code: session management and 1M context](https://claude.com/blog/using-claude-code-session-management-and-1m-context)（Claude Blog, 2026年4月15日，由 Anthropic 技术员工 Thariq Shihipar 撰写）

2026 年 4 月，Anthropic 内部技术员工 Thariq Shihipar 在 Claude 官方博客发表了一篇少见的"工程师内部视角"文章——主题不是模型能力，而是 Claude Code 用户每天都在做的、却没人系统讲过的决策：**当一个 Session 跑完一段工作，下一步应该 continue、rewind、compact、clear，还是起一个全新的 session？**

这篇文章值得专门解读，因为它揭示了一个被忽略的事实：**Claude Code 的 1M Context 窗口不仅是个容量升级，更触发了一整套"会话级决策"的范式转变**。当你能在一个 session 里塞下整个代码库，"如何管理这个 session"就成了比"如何 prompt"更关键的能力。

---

## 核心命题

文章的核心命题可以浓缩成一句话：

> **"Session 不是越长越好；Context 不是越满越好。1M Context 的真正意义不是让你塞更多东西进同一个 session，而是让你有更多主动管理的空间。"**

围绕这个命题，Anthropic 在文章里给出了五个动作的完整决策树：

| 动作 | 何时用 | 何时不用 |
|------|--------|----------|
| **continue** | 同一任务下一步 | 新任务、新方向 |
| **/rewind**（双击 Esc）| 探索失败想换路径 | 任务连续推进中 |
| **/compact** | 想保留对话历史 | 总结会丢失关键信息时 |
| **/clear** | 想完全掌控下一段上下文 | 想保留之前的细节时 |
| **subagent**（Agent tool）| 已知会产生大量中间输出 | 需要直接看到每一步 |

---

## 为什么这件事值得关注

### 1. /usage 把"看不见的 context"变成"可观察的状态"

传统 Agent 工作流里，context window 是个"黑盒"——你不知道用了多少、还剩多少、什么时候会触发自动 compact。这导致工程师只能凭直觉判断"该换个 session 了"。

Anthropic 这次发布的 `/usage` slash command，把这件事变成了一等公民：

> "We released `/usage`, a new slash command to help you understand your usage with Claude Code. This feature was informed by a number of conversations with customers."

`/usage` 不只是显示数字，它**改变了工程师管理 session 的心智模型**——从"凭感觉换 session"变成"基于数据决策"。这种把基础设施指标暴露给用户的设计哲学，是 Claude Code 区别于其他 AI Coding 工具的核心差异。

### 2. /rewind 揭示了一个反直觉的最佳实践

文章里最有冲击力的一段是关于 `/rewind` 的：

> "Claude reads five files, tries an approach, and it doesn't work. Your instinct may be to type 'that didn't work, try X instead.' But the better move may be to rewind to just after the file reads, and re-prompt with what you learned."

这个洞察反直觉：**当 Agent 走错路时，你的本能反应是"修正 prompt 让它继续"，但 Anthropic 的内部实践是"倒带，把那五次失败的 file read 从 context 里彻底删除"**。

为什么？因为 context rot——模型注意力被那五次失败探索的"垃圾上下文"分散，继续 prompt 只会让新的尝试也被污染。`/rewind` 本质上是给你一个"撤回键"，让你从历史中**外科手术式**地删除噪声，保留干净起点。

> "Rewind is often the better approach to correction."

### 3. compact vs clear 的根本差异：让模型总结 vs 让你自己写

文章给出了一个特别清晰的对比：

> "Compact asks the model to summarize the conversation so far... It's lossy, but you didn't have to write anything yourself... With `/clear` you write down what matters... It's more work, but the resulting context is what you decided was relevant."

这是两种**完全不同的信任模型**：
- **`/compact`** 把总结权交给模型——方便但有损，特别是"bad compact"问题：自动压缩在长调试 session 后会触发，但"调试期间提到的另一个 warning"可能被丢掉
- **`/clear`** 把总结权交给你自己——累但精准，"我们正在重构 auth middleware，约束是 X，关键文件是 A 和 B，已经排除方案 Y"

**1M Context 改变了这种权衡**：以前 context 紧，自动 compact 是必需；现在有了完整 1M，你可以更主动地用 `/compact focus on X, drop Y` 给模型明确指令，或者直接 `/clear` 自己写摘要。

### 4. Subagent 的"中间产物隔离"心智模型

文章给出了一个测试 subagent 是否适用的判断标准：

> "Will I need this tool output again, or just the conclusion?"

这是 Anthropic 内部判断 subagent 的核心准则——**subagent 不是为了并行加速，是为了 context 隔离**。当一段工作会产生大量中间输出（文件读取、搜索结果、错误信息），但你只需要最终结论时，subagent 让父 context 保持干净。

这种用法的核心价值不在性能，而在**注意力管理**——父 session 的 context 只接收 subagent 的最终报告，那些探索性 read/search 结果完全隔离在 subagent 的 sub-context 里。

### 5. 1M Context 触发"bad compact"问题的缓解

文章点出了一个非常微妙的陷阱：

> "Bad compacts can happen when the model can't predict the direction your work is going... due to context rot, the model is at its least intelligent point when compacting."

这是 context rot 的双杀：模型在长 context 末尾时表现已经在下滑，而自动 compact 又恰好在此时触发——结果就是模型用"已经退化的注意力"去总结"包含最重要决策的历史"，最容易丢关键信息。

1M Context 的真正价值在这里：**给了你主动 compact 的窗口**。你不必等到自动 compact 触发，而是在"上下文还有 200K 时"主动 `/compact focus on [你的下一步目标]`——那时模型注意力还在线，总结质量可控。

---

## 工程意义：从"Prompt 工程师"到"Session 工程师"

这篇文章最重要的不是某个具体命令，而是它传递的一个范式转变：

**以前的 AI Coding 工程师是 Prompt 工程师**——优化单次 prompt 让模型一次给出好答案。

**现在的 AI Coding 工程师是 Session 工程师**——管理一连串 prompt 之间的 context 状态，决定何时该继续、何时该重置、何时该隔离。

这个转变和 Claude Code 的 1M Context 升级是绑定的。容量小的时候，"session 管理"不重要，因为 context 总会满，工程师也只能被迫频繁换 session；容量大的时候，**session 管理成为差异化竞争力的来源**——同样的 1M context，会管理的人能让模型全程保持高注意力，不会管理的人让模型在 context rot 中逐渐变笨。

---

## 配套工具：实时观察 session 状态

要把 session 决策从"凭感觉"变成"基于数据"，除了 `/usage` 这种内置命令，社区也出现了专门的 session observability 工具——其中最有代表性的是 **abtop**（"like htop, but for AI coding agents"），3K Stars Rust 项目，支持同时监控多个 Claude Code / Codex CLI / OpenCode session 的 token 使用、context window 百分比、rate limit、子进程、孤儿端口等。

这类工具对应着文章的 `/usage` 命令的"工程化升级版"——从"看单个 session 的使用量"到"同时看多个 session 的健康状态"，让 session 决策真正成为团队级而非个人级的实践。

---

## Pair 关联性

- **本文 Article**（Claude Code session 决策树）↔ **abtop**（多 session 实时 observability）= Layer 1 cluster 共享（ai-coding / Claude Code 工具）+ Layer 2 SPM 关键词命中（context window, session, token usage, monitoring）+ Layer 3 topics 命中（claude-code, ai-coding-agent, monitor）+ Layer 4 维度互补（决策树 vs 实时观测）= **4-way SPM 满中**

本文提供了"何时该 continue/rewind/compact/clear"的决策框架，abtop 提供了"实时看到每个 session 当前状态"的可观测性基础设施——两者共同构成了 Claude Code 在 1M Context 时代的 session 管理完整 stack。

---

## 总结

Claude Code 的 1M Context 升级看似只是容量翻 5 倍，实质上触发的是 **Session 范式** 的成熟：

1. **从黑盒到可观察**：`/usage` 让 context 使用量变成可见状态
2. **从累积到清理**：`/rewind` 给了"撤回 + 重试"的工具
3. **从自动到手动**：`/compact focus on X` 让用户主导总结方向
4. **从平铺到隔离**：subagent 把"中间产物"挡在父 context 之外
5. **从单 session 到多 session**：abtop 这类工具让并行 session 成为可管理的实践

这五件事一起，让"Session 工程师"成为一个真实的角色——不再只是写 prompt，而是管理 context 状态、决策时机、隔离边界。