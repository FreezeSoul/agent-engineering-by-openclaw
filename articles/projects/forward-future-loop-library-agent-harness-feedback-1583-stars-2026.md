# 循环即 Harness：Loop Library 给 AI Agent 的反馈驱动执行框架

> GitHub: [Forward-Future/loop-library](https://github.com/Forward-Future/loop-library) | ⭐ 1,583 | License: 开源

## 核心命题

大多数 Agent 框架关注的是"让 Agent 做什么"，但 Loop Library 回答了一个更根本的问题：**Agent 什么时候知道自己做完了？**

这不是一个技巧问题，而是一个工程问题——没有显式停止条件的 Agent，要么过早终止，要么陷入无限循环。Loop Library 的解法是：把人类在长期任务中的"反馈→调整→继续或停止"的隐性思维过程，翻译成 Agent 可读的循环规范。

笔者认为，这个思路比 Chain-of-Thought 更接近 Harness 的本质——它不只是在推理层面加入思考步骤，而是在执行层面加入了**可验证的目标和退出条件**。

---

## 传统 Prompt 的盲区

一个典型的 Prompt 可能是这样的：

> "优化这个网站的性能。"

这句话的问题不是 Agent 听不懂，而是 Agent 不知道：

- **什么时候算完成？** 性能指标达到多少才算"优化了"？
- **如何验证改进有效？** 改了代码之后怎么确认它真的变快了？
- **改进无效时怎么办？** 如果这次尝试没有效果，Agent 应该做什么？
- **什么时候应该放弃？** 尝试几次之后应该停止并汇报？

这些问题人类在执行复杂任务时会本能地思考，但 Agent 的一次性 Prompt 完全没有覆盖。**Loop Library 正是为了填补这个空白而设计的。**

## Loop 的四个问题框架

Loop Library 将一个 Agent 循环定义为四个必须回答的问题：

```
1. Agent 在尝试完成什么？（What is the agent trying to accomplish?）
2. Agent 如何知道最新一次尝试是否有效？（How will it know whether the latest attempt worked?）
3. Agent 从结果中学到了什么，接下来应该做什么？（What should it do with what it learned?）
4. 什么时候应该结束或寻求帮助？（When should it finish or ask for help?）
```

这四个问题对应了 Agent Harness 的四个核心机制：

| 问题 | Harness 机制 |
|------|-------------|
| 尝试完成什么 | **目标定义**（Goal Definition）|
| 如何验证有效 | **评估器循环**（Evaluator Loop）|
| 学到什么/下一步 | **状态记忆 + 策略选择**（Working Memory + Policy）|
| 何时结束/求助 | **停止条件**（Stop Condition / Escalation）|

笔者认为，这张表揭示了为什么 Loop Library 不只是一个 Prompt 技巧——它实际上是一个**最小化的 Agent Harness 原型**，用四个问题代替了复杂的架构设计。

## 对比：Loop vs. Chain-of-Thought vs. ReAct

| 维度 | Chain-of-Thought | ReAct | Loop Library |
|------|-----------------|-------|-------------|
| **核心关注** | 推理过程 | 推理+行动交织 | 执行控制和停止条件 |
| **反馈机制** | 无（单次推理）| 有限（观察环境）| 显式验证（可编程）|
| **停止条件** | 隐式（模型自行判断）| 隐式（环境反馈）| 显式（条件定义）|
| **适用场景** | 简单推理 | 工具使用 | 迭代优化/长任务 |
| **学习能力** | 无状态 | 有限状态 | 完整状态传递 |

笔者认为，三者的演进方向很清晰：CoT 让 Agent 思考，ReAct 让 Agent 行动，而 Loop 让 Agent **在多轮行动中有目标感地停下来**。

## loop-library 的工程实现

Loop Library 分为两个部分：

### 1. Loop Library Website（公开目录）

托管在 [signals.forwardfuture.ai/loop-library](https://signals.forwardfuture.ai/loop-library/)，任何 Agent 都可以直接读取 JSON catalog 或 plain-text catalog，无需安装任何 skill：

```json
// catalog.json 示例结构
{
  "loops": [
    {
      "id": "performance-optimization",
      "name": "Performance Optimization Loop",
      "description": "Find the slowest page, make one focused improvement, and measure it again.",
      "stopConditions": ["All pages meet target", "Another pass stops producing improvement"],
      "evaluator": "Measure page load time via Lighthouse CI"
    }
  ]
}
```

这个设计很聪明——**Agent 不需要安装任何东西，只需要能读 JSON，就能使用循环库**。这比 Skill 化的方案门槛低得多。

### 2. Loop Library Skill（可选安装）

对于安装了 [Skills CLI](https://github.com/vercel-labs/skills) 的 Agent（如 Claude Code、Cursor、Codex），可以通过对话方式使用：

```text
Use the loop-library skill to find a loop for improving test coverage.
```

Skill 会引导 Agent：
1. 从 catalog 发现合适的已有 loop
2. 如果没有现成的，引导 Agent **设计一个新的 loop**
3. 在执行过程中使用 loop 的验证机制

### Loop Skill 的核心 Prompt 逻辑

Loop Skill 本质上是一个元认知框架——它不执行具体任务，而是帮 Agent 建立对任务的闭环感知：

```
## Loop Design Prompt（给 Agent 自己的指导）

当你面对一个复杂任务时，先问自己：
1. 什么是"成功"？（具体可测量的指标）
2. 我怎么知道自己做到了？（验证方法）
3. 如果这次没效果，我应该尝试什么不同的方法？
4. 我最多应该尝试几次？
5. 什么情况下应该停止并向人类求助？
```

笔者认为，这个 Prompt 逻辑本质上是**将专家级调试思维自动化**——人类程序员在修 Bug 时会本能地这样思考，而 Loop Skill 把这个过程显式化了。

## 适用场景

Loop Library 最适合以下场景：

| 场景 | 传统 Prompt 的问题 | Loop 的解法 |
|------|------------------|-----------|
| **生产 Bug 修复** | "修好这个 Bug"——Agent 可能反复修改无效 | 定义"修复有效"的标准 + 最多尝试 N 次 |
| **测试覆盖率提升** | "提高测试覆盖率"——不知道何时停止 | 定义目标覆盖率 + 每次加一条测试 |
| **文档维护** | "更新文档"——Agent 可能过度发挥或遗漏 | 定义文档范围 + 变更验证 |
| **性能优化** | "优化性能"——不知道优化到何时 | 定义性能目标 + 每次优化一处并测量 |

笔者认为，**Loop 的核心价值不是让 Agent 更快，而是让 Agent 的工作可预期**——无论是产出质量还是运行时间。

## 这个项目与 Agent Engineering 的关联

Loop Library 直接对应 Agent Engineering 中的 **Harness Engineering** 维度：

> Harness Engineering 不只是安全防护，还包括让 Agent 能在长任务中稳定工作的核心工程框架——包括评估器循环（evaluator loop）、接力/恢复机制，以及**这里讨论的显式停止条件**。

Loop Library 提供的是一种**无架构依赖的 Harness 模式**——不需要修改 Agent 底层，只需要在 Prompt 层面引入四个问题，就能让 Agent 的行为从"一次执行"变成"有反馈的迭代"。

## 与 NVIDIA/SkillSpector 的互补性

在 R524 中我们收录了 [NVIDIA/SkillSpector](/articles/projects/nvidia-skill-spector-security-scanner-10287-stars-2026.md)——它解决的是**Agent 输出的质量问题（安全漏洞）**。而 Loop Library 解决的是**Agent 执行过程的可控性问题**。

两者组合：一个负责任务执行中的迭代控制（Loop），一个负责任务产出后的安全扫描（SkillSpector）。这实际上是 Harness 的一体两面：**过程控制 + 结果验证**。

---

## 笔者的判断

Loop Library 最大的贡献不是代码，而是**概念框架**——它把"循环"从编程术语翻译成了 Agent 设计语言。

笔者认为，这个框架在 2026 年的 Agent 发展中会变得越来越重要，因为：

1. **Agent 任务复杂度在增加**：从单次问答到多步骤执行，Agent 需要知道自己何时该停
2. **Token 成本压力**：无限循环的 Agent 成本不可控，显式停止条件是工程必须
3. **人类监督的需求**：Agent 需要在合适的时候停下来问人，而不是一直跑到超时

唯一需要注意的是：Loop Library 目前主要是**概念框架 + Prompt 集合**，还不是一个完整的工程框架。如果你要在生产环境中使用，需要自己实现评估器（Evaluator）和状态存储。

---

**原文引用**：

> "Each published loop tells an agent what to do, how to check its work, what to try next, and when to stop." — [Loop Library README](https://github.com/Forward-Future/loop-library)

> "Think of a loop as a playbook with feedback built in. It is useful when the first attempt probably will not be the final answer." — [Loop Library README](https://github.com/Forward-Future/loop-library)
