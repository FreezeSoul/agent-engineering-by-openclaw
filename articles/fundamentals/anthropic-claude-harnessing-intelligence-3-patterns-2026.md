# Claude 的 Harness 设计：3 个让 Agent 随模型进化而不崩的工程模式

> 原文：[Harnessing Claude's Intelligence | 3 Key Patterns for Building Apps](https://claude.com/blog/harnessing-claudes-intelligence)
> 来源：Anthropic Claude Blog
> 产出时间：2026-06-10

---

## 核心命题

Anthropic 在 2026 年 6 月发布的这篇文章，给出了一个重要的工程判断：**Agent Harness 的设计假设会随着模型能力进化而失效**，但这不意味着我们要减少 harness 的设计，而是要建立一种"随模型能力收缩边界"的设计哲学。

笔者认为，这篇文章的核心贡献不在于提出了三个模式，而在于揭示了一个反直觉的事实：**更好的模型会废除你之前为弥补其缺陷而设计的工程机制**。当你还在为 Sonnet 4.5 的"context anxiety"添加 context reset 时，Opus 4.6 已经不需要这些补偿了。

---

## 背景：为什么 Harness 设计会过时

Anthropic 联合创始人 Chris Olah 有一个观点：生成式 AI 系统是"生长出来的，而非构建出来的"。研究者设定条件引导生长，但具体的能力结构和涌现模式并不完全可预测。

这对 Agent 工程意味着：**Harness 编码了关于 Claude"不能独立完成什么"的假设，但这些假设会随着模型升级而迅速过时**。即使是我们自己分享的工程经验，也需要频繁重新审视。

> "Even lessons shared in articles like this deserve frequent revisiting." — Anthropic Engineering Blog

这是一个让很多团队头疼的问题：当模型升级后，原本为了"补偿模型缺陷"的 hack 会变成性能瓶颈。

---

## 模式一：使用 Claude 已经理解的工具

Anthropic 的建议是：**使用 Claude 本身就很熟悉的工具来构建应用**。

2024 年底，Claude 3.5 Sonnet 在 SWE-bench Verified 上达到 49% 的准确率（当时的世界前沿），但它使用的工具只有两个：bash 工具和文本编辑器（用于查看、创建和编辑文件）。Claude Code 同样基于这些工具构建。

这背后的逻辑是：

- Bash 并非为 Agent 设计，但它是一个 Claude 知道如何使用的工具，而且 Claude 在使用它的过程中会越来越好
- 当你给 Claude 一个它不熟悉的工具时，Agent 需要额外的上下文工程来弥补
- **工具越接近 Claude 的训练分布，Harness 需要做的补偿就越少**

```python
# 好的 Harness 设计：使用 Claude 原生支持的工具
tools = [
    "bash",      # Claude 深度训练的工具
    "edit",      # 文件编辑，Claude Code 的核心
    "glob",      # 文件发现
    "grep",      # 代码搜索
]

# 不好的设计：引入大量 Claude 不熟悉的 API 工具
# 每个新工具都增加上下文负担，需要详细的 description engineering
```

笔者认为，这个原则的深层含义是：**工具的简洁性 > 工具的功能性**。一个 Claude 深度理解的 bash 工具，远比 10 个需要详细描述的 custom tools 更有效。

---

## 模式二：持续问"我可以停止做什么"

这是文章中最反直觉的一个模式：Anthropic 在多个案例中发现，**更好的模型会废除你之前为弥补其缺陷而设计的工程机制**。

### 案例：Context Reset 的废除

Anthropic 曾经为长时程任务构建过一个 Agent，Sonnet 4.5 在感知到 context limit 接近时，会过早地结束任务（他们称之为"context anxiety"）。团队通过添加 context reset 来解决这个问题。

但当切换到 Opus 4.5 后，这个行为消失了——Opus 4.5 不再有"context anxiety"，之前补偿性的 context reset 变成了 harness 中的 dead weight。

> "Removing this dead weight is important because it can bottleneck Claude's performance. Over time, the structure or boundaries in our applications should be pruned based the question: what can I stop doing?"

### 案例：记忆系统的演进

另一个例子是记忆系统。Anthropic 早期尝试通过 retrieval infrastructure 来增强模型的记忆能力。但随着 Claude 版本演进，Claude 自己学会了选择要持久化什么内容。

在 BrowseComp（一个 agentic search 任务）上：
- Sonnet 4.5 在不同压缩预算下都保持在 43% 的准确率
- Opus 4.5 扩展到了 68%
- Opus 4.6 在相同设置下达到了 84%

这说明**外部记忆检索系统的价值会随着模型本身记忆能力的提升而下降**。

### 实践原则

笔者认为，这个模式对 Harness 工程的启示是：

1. **定期审计你的补偿性设计**：每当我们为模型缺陷添加了一个 hack，就应该在模型升级后重新评估这个 hack 是否还需要
2. **建立能力基线测试**：当模型通过某个基准测试后，删除为该缺陷设计的补偿机制
3. **拥抱"最小化 Harness"哲学**：Harness 中的每个元素都应该被问一个问题："如果没有这个，模型本身能处理吗？"

---

## 模式三：谨慎地设置边界

Agent Harnesses 通过结构来约束 Claude 的行为，以满足 UX、成本或安全需求。但这里有一个重要的工程判断：**边界的设置应该跟随模型能力成长，而不是一开始就设限**。

### Context Caching 的 Harness 设计

由于 Messages API 是无状态的，Claude 无法看到之前轮次的对话历史。这意味着 Agent Harness 需要在每一轮中将所有过去的操作、工具描述和指令与新上下文一起打包。

Anthropic 的关键发现是：**Prompt 可以基于断点（breakpoints）被缓存**。Claude API 将上下文写到断点为止，然后检查该上下文是否匹配任何先前的缓存条目。由于缓存 token 的成本是基础输入 token 的 10%，Harness 设计应该最大化 cache hits。

文章给出了几个原则：
- 识别哪些上下文是"相对静态的"（如工具描述、系统指令），这些可以被缓存
- 识别哪些是"动态的"（如中间结果、工具输出），这些不应该进入缓存
- **缓存友好的 Harness 设计本身就是一种优化**

### Subagents 与新鲜上下文窗口

Anthropic 提到的另一个重要设计是 subagents：当任务需要隔离工作时，可以 fork 到一个新的上下文窗口。

> "With Opus 4.6, the ability to spawn subagents improved results on BrowseComp by 2.8% over the best single-agent runs."

这是一个重要的架构信号：**模型的子 Agent 能力正在成为长时程任务的关键工程手段**。

### 边界设计的反模式

笔者认为，常见的边界设计反模式是：

1. **过早限制**：在模型还没展示某个能力之前就假设它做不到，从而设置不必要的边界
2. **过度工程**：为小概率场景设计复杂的权限系统，增加 Harness 的复杂度
3. **静态边界**：边界设置后不跟随模型升级重新评估

---

## 范式跃迁：从"Harness 补偿"到"Harness 收缩"

笔者认为，这篇文章最深刻的工程洞察是揭示了一个范式跃迁：

**旧的范式**：Harness = 补偿模型缺陷的工程机制
**新的范式**：Harness = 随着模型能力成长而收缩边界的动态系统

这意味着 Agent 工程的角色正在从"补偿者"转变为"裁剪者"：

| 阶段 | Harness 的角色 | 工程行为 |
|------|---------------|---------|
| 模型早期 | 补偿缺陷 | 添加大量的 context reset、tool description、fallback logic |
| 模型成熟 | 收缩边界 | 删除补偿性设计，让模型能力直接发挥 |
| 模型超预期 | 最小化 Harness | 只保留必要的边界（UX/成本/安全），其他全部移除 |

这个范式跃迁对团队提出了新的要求：**你需要持续追踪模型能力的变化，并相应地裁剪 Harness**。这与传统软件工程中"添加功能"的逻辑正好相反。

---

## 工程落地建议

基于文章内容，笔者提炼出以下 Harness 设计的工程检查清单：

### 每次模型升级后

- [ ] 运行能力基线测试，确认之前补偿的缺陷是否已修复
- [ ] 删除不再需要的 context reset、fallback logic
- [ ] 重新评估工具描述的详细程度（模型可能已经更理解了）
- [ ] 检查缓存策略是否仍然高效

### 持续监控

- [ ] 追踪 Claude 在各 benchmark 上的表现变化
- [ ] 当模型超过某个阈值（如 Opus 4.6 > 84% on BrowseComp），触发 Harness 收缩评审
- [ ] 建立"补偿性设计"的 catalog，记录每个 hack 的来源和失效条件

### 架构设计原则

- [ ] 优先使用 Claude 深度训练的工具（bash, edit, glob, grep）
- [ ] 将补偿性设计标记为"待删除"，而非永久保留
- [ ] Context caching 设计时，分离静态上下文（可缓存）和动态上下文（不可缓存）
- [ ] 评估 subagents 的使用场景，特别是长时程任务的隔离需求

---

## 金句

> "Over time, the structure or boundaries in our applications should be pruned based the question: what can I stop doing?"

笔者认为，这句话应该成为每一个 Agent Harness 工程师的座右铭。**好的 Harness 不是添加更多，而是持续删除**。

---

## 引用来源

1. Anthropic Engineering Blog: "Harnessing Claude's Intelligence" (2026-06)
2. SWE-bench Verified: Claude 3.5 Sonnet 49% (2024)
3. BrowseComp: Opus 4.6 达到 84% (与 Sonnet 4.5 的 43% 对比)
4. BrowseComp-Plus: Sonnet 4.5 + memory folder 从 60.4% 提升到 67.2%