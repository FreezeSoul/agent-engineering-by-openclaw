---
title: "Cursor Auto-review 的工程真相：推理时分类器 + 6122条标注数据 + 反馈循环"
slug: cursor-auto-review-classifier-inference-time-eval-feedback-2026
date: 2026-06-15
source: https://cursor.com/blog/agent-autonomy-auto-review
cluster: harness
---

# Cursor Auto-review 的工程真相：推理时分类器 + 6122条标注数据 + 反馈循环

> **来源**：[Cursor Blog — Governing agent autonomy with Auto-review](https://cursor.com/blog/agent-autonomy-auto-review)，2026
> **分类**：harness
> **核心判断**：Auto-review 的本质不是「安全开关」，而是一个**推理时（inference-time）分类器**，用小模型 + Agentic 设计 + 反馈循环，在每一次工具调用前完成上下文感知的风险判断。这是 Harness Engineering 中「评估器循环」的具体工程实现。

---

## TL;DR

Auto-review 解决了 AI Coding Agent 权限系统的两极困境：Allowlist 太死，Run Everything 太野。Cursor 的解法是在每一次工具调用前插入一个**推理时分类器**，用小模型做上下文感知判断，配合 6122 条标注数据 + 合成数据训练，让「安全」变成可量化的工程问题而非非此即彼的开关。

---

## 一、问题：权限即极化的难题

Cursor 在设计 Auto-review 之前，Agent 的权限只有两种模式：

| 模式 | 行为 | 问题 |
|------|------|------|
| Allowlist | 白名单内命令自动执行，其余弹窗 | 频繁打断工作流 |
| Run Everything | 所有操作无脑执行 | 危险操作无约束 |

这个两极困境的本质是：**传统权限系统无法感知上下文**。同一个 `python script.py` 命令，在不同工作流中可能安全也可能危险，取决于脚本内容、用户意图和工作流上下文。

> "Whether an agent action poses risk depends on the situation. The same command can be harmless in one workflow and unacceptable in another."
> — [Cursor Blog: Governing agent autonomy with Auto-review](https://cursor.com/blog/agent-autonomy-auto-review)

---

## 二、Auto-review 的核心架构：推理时分类器

Auto-review 不是在 Agent 执行后进行检查，而是在**每一次工具调用前**插入一个分类器子 Agent：

```
用户请求
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Parent Agent                                                 │
│  ├─ 接收用户请求                                             │
│  ├─ 生成工具调用计划                                          │
│  └─ 在工具调用执行前：暂停 → 送入 Classifier                 │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  Classifier Agent（推理时）                                   │
│  ├─ 输入：当前工具调用 + 用户请求上下文 + 工作流状态         │
│  ├─ 工具：ReadFile / Grep / Glob / ListDir（可检查 workspace）│
│  ├─ 输出：allow / block（返回解释）/ retry                   │
│  └─ 位置：同一 RPC stream，无额外延迟                       │
└─────────────────────────────────────────────────────────────┘
    │
    ├── allow ──→ 工具调用执行
    ├── block ──→ 停止，返回解释给 parent agent
    └── retry ──→ parent agent 选择更安全的路径
```

**三个关键设计决策**：

### 2.1 小模型 + 足够推理，而非大模型全覆盖

传统思路会用一个强模型做全局判断，但 Cursor 选择**小模型 + 足够推理**：

> "One early surprise was that lower-reasoning models were not always faster. When a model struggled to understand the policy or the tool call, it could spend more time and tokens searching for what ultimately became a worse answer."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

关键洞察：推理能力不足的模型反而更慢——因为它会在错误的方向上搜索更久。最佳权衡是**一个小型模型，但有足够的推理能力做出干净判断**。

### 2.2 分类器是 Agentic 的

分类器不仅看命令本身，还能用工具检查工作区状态：

> "A command like `python script.py` might be safe or unsafe depending on what is inside the file, so the classifier can inspect the workspace with tools like ReadFile, Grep, Glob, and ListDir before deciding."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

这意味着分类器是**上下文感知的**——它不只是看 API 名称，而是看实际内容和执行上下文。

### 2.3 零额外延迟：同一 RPC Stream

Cursor 避免了一个独立分类 endpoint 带来的延迟，而是让分类器运行在**同一 RPC stream** 中，类似 subagents 的架构模式：

> "We avoided a separate classification endpoint, because an extra round trip would add latency directly before every reviewed tool call."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

---

## 三、反馈循环设计：block 不是终点

Auto-review 的一个关键设计原则：**block 不是终点，而是反馈的起点**。

当分类器 block 一个操作时，它返回的不只是一个「拒绝」信号，而是一个**解释**，告诉 parent agent 为什么这个操作有风险。Parent agent 收到反馈后，可以：

1. 选择一个更安全的路径继续执行
2. 请求用户提供更明确的上下文
3. 修改操作参数使其安全

> "The question is not whether an action looks risky in isolation. The question is whether the action is justified by what the user asked the agent to do."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

这个设计让 Auto-review 不会成为另一个「审批提示生成器」——它在保持安全边界的同时，让正常开发工作持续推进。

---

## 四、Eval 设计：6122 条标注 + 合成数据

Auto-review 的 Eval 设计是这篇文章最稀缺的部分。Cursor 用了两种数据：

### 4.1 内部真实数据（6122 条标注）

第一组数据来自内部开发者会话：

> "We started with roughly 12 hours of internal developer sessions, then cut that down and deduplicated common actions into 6,122 labeled rows."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

从 12 小时会话中提取、去重、标注，得到 6122 条标注数据。这是分类器的「正常baseline」——它必须能识别正常开发工作的模式，同时捕捉危险操作。

### 4.2 合成数据（最坏情况覆盖）

正常数据无法覆盖那些罕见但危险的场景：

> "We also needed synthetic data, because the worst cases do not appear often enough in normal usage. We generated cases where the agent might read secrets, touch production data, follow untrusted instructions, or take actions with large side effects."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

合成数据生成最坏情况：
- 读取 secret 的场景
- 访问 production 数据
- 执行不可信指令
- 有重大副作用的操作

**这两组数据共同作用**：真实数据保证正常工作的流畅度，合成数据保证危险场景的覆盖。

### 4.3 Policy 迭代：数据跟着政策变

一个重要的工程细节：**Policy 在变化，数据在随之调整**：

> "The policy changed as we learned, which made the data work more complicated."
> — [Cursor Blog](https://cursor.com/blog/agent-autonomy-auto-review)

当政策更新时，标注数据也需要相应调整。这是一个持续迭代的系统，而非一次性训练。

---

## 五、笔者判断：Auto-review 在 Harness 体系中的位置

### 5.1 评估器循环的具体实现

Auto-review 本质上是 Harness Engineering 中「评估器循环」的具体工程实现：

| 组件 | Anthropic Harness 术语 | Cursor Auto-review 实现 |
|------|----------------------|------------------------|
| 评估器 | Agent 判断下一步是否安全 | Classifier Agent |
| 反馈 | 评估器返回判断结果 | Block 返回解释 + 建议 |
| 重试 | 换路径继续 | Parent agent 选更安全的路径 |
| 环境状态 | Git commit / Progress File | Workspace 上下文 |

### 5.2 与 Claude Code Auto-mode 的比较

Claude Code 的 Auto-mode 分类器是**基于 transcript 的事后分类**（看完整对话 transcript 再判断），而 Cursor Auto-review 是**推理时的上下文感知分类**（每次工具调用前实时判断）。

两种路线的权衡：

| 维度 | Claude Code（事后）| Cursor（推理时）|
|------|------------------|----------------|
| 延迟 | 无额外延迟 | 分类器需运行（但在同一 stream）|
| 上下文 | 全局 transcript | 实时 workspace 状态 |
| 决策时机 | 操作完成后 | 操作执行前 |
| 误判代价 | 已执行，可能有副作用 | 未执行，安全边界更清晰 |

**笔者认为**：推理时判断是更安全的架构——错误决策的代价是「没有执行」而非「已造成影响」。但这对分类器的准确性要求更高。

### 5.3 开放问题

1. **小模型的推理上限**：当分类器遇到需要复杂推理的风险判断时，小模型是否会犯错？Cursor 的经验是「足够推理 > 最低推理」，但这个边界在哪里？

2. **Policy 迭代的成本**：每次 Policy 更新需要重新标注数据，这个成本是否可持续？

3. **跨工作流泛化**：一个工作流训练的分类器，在另一个工作流中是否仍然准确？

---

## 六、工程可复用性

Auto-review 的 Eval 设计和反馈循环架构可以复用到其他 Agent 的 Harness 设计中：

```python
# 简化分类器设计模式
class ClassifierAgent:
    def __init__(self, model, policy):
        self.model = model
        self.policy = policy

    def classify(self, tool_call, workspace_context, user_intent):
        # 小模型 + 足够推理
        context = self._build_context(tool_call, workspace_context, user_intent)
        judgment = self.model.reason(context)

        if judgment.risk_level <= self.policy.threshold:
            return Allow()
        elif judgment.can_retry:
            return Retry(feedback=judgment.explanation)
        else:
            return Block(explanation=judgment.explanation)

    def _build_context(self, tool_call, workspace_context, user_intent):
        # Agentic 分类器：可检查 workspace
        workspace_inspection = self._inspect_workspace(tool_call)
        return {
            "tool_call": tool_call,
            "user_intent": user_intent,
            "workspace_state": workspace_inspection,
            "policy": self.policy
        }
```

---

## 参考

- [Cursor Blog: Governing agent autonomy with Auto-review](https://cursor.com/blog/agent-autonomy-auto-review)
- [Cursor Auto-review Run Mode：评估器循环架构](articles/harness/cursor-auto-review-run-mode-classifier-evaluator-loop-2026.md)
- [Anthropic Harness Engineering: 评估器循环定义](articles/deep-dives/openai-harness-engineering-codex-agent-first-world-2026.md)
