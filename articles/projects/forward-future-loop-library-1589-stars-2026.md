# Forward-Future/loop-library：让 AI Agent「学会停止」的 Loop 范式（1589 Stars）

> 很多 prompt 告诉 Agent 做什么，但不告诉它「什么时候算做完」。Loop Library 的核心贡献是把 prompt 从「一次性指令」变成「带反馈的循环」——让 Agent 能自主判断「继续还是停止」。

## 核心命题

Loop Library 解决了一个根本问题：Agent 的 prompt 只有执行指令，没有验证条件和停止标准。Loop 把 prompt 升级为「playbook with feedback built in」——让 Agent 执行一次之后看结果，根据结果决定下一步，而不是闷头执行到 Context 耗尽或超时。

笔者认为，这个方向比 Skill 组合更贴近 Agent 工程化的核心问题——Skill 解决的是「能力边界」，Loop 解决的是「执行可靠性」，而后者才是 Agent 从 demo 走向 production 的关键。

## 项目概览

| 维度 | 信息 |
|---|---|
| **Stars** | 1589 |
| **License** | MIT |
| **语言** | JavaScript |
| **创建时间** | 2026-06-12 |
| **主题标签** | agent-skills, agentic-workflows, ai-agents, automation, codex, prompt-engineering |

## 两种使用方式

Loop Library 包含两个部分，各自独立：

**Website 直接浏览**：无需安装，在 [Loop Library 网站](https://signals.forwardfuture.ai/loop-library/) 可以直接查看所有已发布的 loop 模板。Agent 也可以直接读取 [JSON catalog](https://signals.forwardfuture.ai/loop-library/catalog.json) 或 [plain-text catalog](https://signals.forwardfuture.ai/loop-library/catalog.txt) 程序化选择合适的 loop。

**Installable Skill**：通过 `npx @agent-native/skills@latest add` 安装到 Claude Code / Codex 环境。安装后 Agent 可以通过对话发现、审核、修复、适配或设计新的 loop——也就是说，**loop 本身可以被 Agent 用来改善自己的 loop**。

## Loop 的四个基本问题

Loop Library 文档对 loop 的定义非常精准——每个 loop 必须能回答四个问题：

1. **What**：Agent 要完成什么目标？（目标，不是操作步骤）
2. **How to know**：怎么判断最新一次尝试是否有效？（Verification Gate）
3. **What to learn**：从结果里学到了什么？（指导下一步）
4. **When to stop**：什么时候该停止或请求帮助？（Stop Condition）

这四个问题构成一个最基本的反馈闭环。

## 一个具体例子

Loop Library README 里有一个具体的性能优化例子：

> **一次 prompt**（不够用）：「让这个网站更快。」

> **Loop**（带反馈）：「找到最慢的那个页面，做一个改进，测量效果。只有当改进有实际效果时才保留。继续直到所有页面都达标，或者下一轮不再产生有意义改进。」

这里的区别在于：
- 目标明确（最慢页面的响应时间）
- 验证条件可判定（测量结果 vs 基准）
- 停止条件明确（达标或无进展）
- 有记忆（保留有效改进，丢弃无效改进）

## 技术实现：Loop = Goal + Action + Verification + Decision

从架构上看，Loop 的执行流程是一个状态机：

```
[Goal] → [Action] → [Verification Gate] → [Decision Node]
                                                    ↓
                            ┌────── 继续循环 ──────┤
                            ↓
              ┌── 接受当前结果 ←── 无进展 ─→ 请求帮助
              ↓
         [Done / Handover]
```

- **Goal**：描述最终状态，不描述具体步骤
- **Verification Gate**：可判定的验证条件（数值阈值、测试结果、人工审批等）
- **Decision Node**：根据验证结果决定下一步
- **Handover**：如果需要人工介入或交接，保留完整的状态文档

## 与 Harness 的关系

参考 Agent Engineering 知识库的 harness 分类，Loop 实际上是一种轻量级 harness 实现：

| Harness 机制 | Loop 对应实现 |
|---|---|
| Evaluator Loop | Verification Gate |
| Stop Condition | Loop 退出条件 |
| Progress File | 每次循环的状态记录 |
| Handover | 交接文档（当前状态 + 验证结果）|
| Permission Layer | 人工审批节点 |

区别在于：Harness 是系统级设计（代码、配置），Loop 是 Prompt 级设计（用自然语言描述反馈结构）。这意味着 Loop 的门槛更低——任何人都可以写一个 Loop，不需要工程团队搭建 Harness 系统。

## 与同类项目的对比

| 项目 | 类型 | Stars | 核心差异 |
|---|---|---|---|
| **loop-library** | Loop 范式 | 1589 (MIT) | Prompt + feedback + stop condition，面向工作流循环 |
| **BuilderIO/skills** | Skill 市场 | 2569 (MIT) | 单个可组合的技能单元，面向能力边界 |
| **omnigent-ai/omnigent** | Meta harness | 4713 (Apache 2.0) | 多 agent 编排 + harness 交换，面向多 agent 协作 |
| **shareAI-lab/learn-claude-code** | 教程集合 | 67600 (MIT) | Claude Code 使用教程，面向学习 |

loop-library 的独特价值在于它填补了「单次 prompt」和「完整 agent 框架」之间的空白——用 loop 的结构把反馈机制塞进 prompt 里，不需要引入整个框架的复杂度。

## 怎么开始

1. **直接体验**：[Loop Library 网站](https://signals.forwardfuture.ai/loop-library/) 提供了所有已发布 loop 的浏览
2. **集成到 coding agent**：`npx @agent-native/skills@latest add`，选择安装 loop-library skill
3. **设计自己的 loop**：参考 [Agent Guide](https://signals.forwardfuture.ai/loop-library/agents/)，用四个问题模板定义你的第一个 loop

## 引用

> 「Most prompts ask an agent to do something once. A loop gives the agent a way to learn from the result and take the next useful step.」
> — Forward-Future/loop-library README

> 「Think of a loop as a playbook with feedback built in. It is useful when the first attempt probably will not be the final answer, such as fixing production errors, improving test coverage, reviewing a product, or keeping documentation current.」
> — Forward-Future/loop-library README

> 「That makes the work easier to trust and easier to repeat. The agent can compare results instead of relying on confidence, keep improvements instead of merely making changes, and stop when it succeeds or stops making progress.」
> — Forward-Future/loop-library README

---

**基本信息**

- GitHub: [Forward-Future/loop-library](https://github.com/Forward-Future/loop-library)
- Stars: 1589
- License: MIT
- Language: JavaScript
- 创建时间: 2026-06-12
- 本轮写入: R526
