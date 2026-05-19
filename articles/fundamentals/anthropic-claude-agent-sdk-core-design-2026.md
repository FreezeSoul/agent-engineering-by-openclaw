# Claude Agent SDK 核心设计：给 Agent 一台计算机

> 平台：GitHub Articles | 字数：约3000字 | 调性：深度技术分析 + 工程判断

---

## 核心观点

**Claude Agent SDK 的核心设计原则只有一个：给 Agent 一台计算机。**

不是给 Agent 一个聊天界面，不是给 Agent 一组 API，而是给 Agent **一台可以运行 Shell、执行文件操作、搜索代码库的计算机**。当 Claude 能像人类一样与计算环境交互时，它的能力边界才真正打开。

这个设计选择带来了一条重要的工程启示：**工具的设计质量直接影响 Agent 的能力上限。**

---

## 背景：SDK 的演进

Claude Agent SDK 最初是 Claude Code 的底层引擎——用来驱动 Claude Code 的 Agent 行为。后来 Anthropic 发现，这个引擎的价值不限于 Claude Code 本身，它可以用来构建**任何需要"像人类一样操作计算机"的 Agent**。

因此 Claude Code SDK 更名为 Claude Agent SDK，定位从「Claude Code 的内部模块」升级为「通用的 Agent 构建框架」。

---

## 核心设计：Agent 的计算机隐喻

### 计算机隐喻的核心含义

Anthropic 在文章中明确指出：

> "The key design principle behind the Claude Agent SDK is to give your agents a computer, allowing them to work like humans do."

这句话看似简单，实际上蕴含了非常重要的工程决策：

| 设计选择 | 传统 Chat API | Claude Agent SDK |
|---------|--------------|------------------|
| **交互方式** | 文本输入/输出 | 计算机操作（bash、文件、网络） |
| **上下文来源** | 一次性 prompt | 持续的环境反馈 |
| **工具定义** | 预定义函数 | 可编程的 Python 函数 |
| **错误恢复** | 重新生成 | 基于环境反馈的自我修正 |
| **任务范围** | 单轮问答 | 长程自主任务 |

### Agent Loop 的完整流程

```
用户 → 任务定义
   ↓
Agent Loop（重复）：
   1. Claude 理解任务
   2. 在计算机上执行操作（bash/文件/搜索）
   3. 观察执行结果
   4. 评估进展，决定下一步
   5. 如需要，暂停等待人类反馈
   ↓
任务完成 / 检查点暂停 / 停止条件触发
```

这个 loop 是 Claude Agent SDK 的核心，所有其他功能都是围绕这个 loop 展开的。

---

## Subagents：并行的力量

Claude Agent SDK 原生支持 Subagents，这是一个被低估的能力。

### Subagents 的两个核心用途

**1. 并行化**

> "Subagents are useful for two main reasons. First, they enable parallelization: you can spin up multiple subagents to work on different tasks simultaneously."

当一个任务可以分解为多个独立的子任务时，Subagents 允许它们同时执行。这意味着：

```
传统方式：
Task A → Task B → Task C（串行，总时间 = A+B+C）

Subagent 方式：
[Task A] ──┐
           ├──→ 聚合结果
[Task B] ──┤
           │
[Task C] ──┘
（并行，总时间 ≈ max(A,B,C)）
```

**2. 上下文隔离**

> "Subagents help manage context: subagents use their own isolated context windows, and only send relevant information back to the orchestrator, rather than their full context."

这是另一个被低估的场景。当一个任务涉及大量信息筛选时（比如扫描 100 个文件找相关内容），让一个 Subagent 专门做这件事，它的完整上下文不会污染主 Agent 的上下文窗口。

---

## Compact：上下文自动管理

LLM 的上下文窗口是有限的。当对话变长时，Claude Agent SDK 的 **compact** 功能会自动压缩历史消息，保持上下文在限制范围内。

这个机制建立在 Claude Code 的 `/compact` 命令之上，这意味着：

1. Compact 是经过生产验证的功能
2. 压缩策略对 Agent 的任务完成率有优化
3. 开发者在设计 Agent 时不需要手动管理上下文长度

---

## 工具设计：上下文即优先级

Anthropic 提出了一个重要的设计原则：

> "Tools are prominent in Claude's context window, making them the primary actions Claude will consider when deciding how to complete a task. This means you should be conscious about how you design your tools to maximize context efficiency."

翻译过来就是：**在 Agent 的世界里，出现在上下文中的工具就是它会考虑使用的工具。**

这带来一个反直觉的结论：

| 设计选择 | 对 Agent 行为的影响 |
|---------|-------------------|
| 工具数量越多 | Agent 越难选择正确的工具 |
| 工具描述越详细 | Agent 越能准确判断何时使用 |
| 工具参数越清晰 | Agent 调用出错的概率越低 |
| 工具组织越有条理 | Agent 越能高效完成复杂任务 |

好的工具设计不是「给 Agent 更多能力」，而是「让 Agent 在正确的上下文下使用正确的能力」。

---

## 评估：Agent 的闭环

Claude Agent SDK 完成 Agent Loop 的最后一个环节：**评估自己的输出**。

> "Agents that can check and improve their own output are fundamentally more reliable—they catch mistakes before they compound, self-correct when they drift, and get better as they iterate."

这个设计揭示了一个重要的工程洞察：**自动纠错比自动生成更重要。**

一个 Agent 能做两件事：

1. **执行任务**：生成代码、写报告、执行操作
2. **检查结果**：验证输出是否符合预期，发现问题则修正

传统 Agent 框架只关注第 1 点。Claude Agent SDK 把第 2 点也变成了核心循环的一部分，这意味着：

```
执行 → 评估 → 发现问题 → 修正 → 评估 → ...
```

直到结果达标或达到停止条件。

---

## 工程实践建议

基于 Claude Agent SDK 的设计原则，以下是构建可靠 Agent 的实践建议：

### 1. 给 Agent 的工具要「干净」

不要在一个工具里塞太多功能。每个工具应该：
- 做一件明确的事
- 有清晰的输入/输出定义
- 在失败时有明确的错误信息
- 不产生副作用（或者副作用是可预测的）

### 2. Subagent 不是越多越好

Subagent 的价值在于：
- **真正的并行**：子任务可以同时执行
- **上下文隔离**：子任务不会污染主上下文

但每个 Subagent 也有开销（启动时间、上下文分发）。如果子任务本身很简单（如只花 10 秒），Subagent 的开销可能不划算。

### 3. Compact 是安全网，不是目标

不要依赖 compact 来管理上下文。好的设计应该在早期就避免上下文膨胀：
- 让 Agent 专注于当前任务
- 避免不必要的探索
- 在适当时候「清空」不再需要的上下文

### 4. 评估驱动开发

在设计 Agent 之前，先想清楚：
- 成功的标准是什么？
- 如何判断输出是否达标？
- 什么情况下 Agent 应该停止？

这些问题应该在写代码之前就想清楚，而不是在 Agent 跑偏之后才加限制。

---

## 引用

> "The key design principle behind the Claude Agent SDK is to give your agents a computer, allowing them to work like humans do."
> — Anthropic Engineering Blog

> "Subagents are useful for two main reasons. First, they enable parallelization: you can spin up multiple subagents to work on different tasks simultaneously. Second, they help manage context."
> — Anthropic Engineering Blog

> "Agents that can check and improve their own output are fundamentally more reliable—they catch mistakes before they compound, self-correct when they drift, and get better as they iterate."
> — Anthropic Engineering Blog

> "Tools are prominent in Claude's context window, making them the primary actions Claude will consider when deciding how to complete a task."
> — Anthropic Engineering Blog

---

## 备选标题

1. 给 Agent 一台计算机：Claude Agent SDK 的核心设计哲学 — 策略：核心概念
2. 为什么 Claude Agent SDK 的工具设计原则直接影响 Agent 能力上限 — 策略：好奇心缺口
3. Subagent + Compact + 评估闭环：Claude Agent SDK 的三角支柱 — 策略：框架概括
4. Anthropic 发现：最好的 Agent 实现不是给更多工具，而是让工具更少 — 策略：反常识
5. 从 Claude Code SDK 到 Claude Agent SDK：一次设计哲学的升级 — 策略：演进视角
