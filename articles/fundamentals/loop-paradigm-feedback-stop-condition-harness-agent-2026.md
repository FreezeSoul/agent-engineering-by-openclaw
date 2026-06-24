# Loop：让 AI Agent「知道什么时候停」的工程机制

## 核心论点

2026 年的 AI Agent 困境不是「Agent 能力不够」，而是「Agent 不知道什么时候停」。大多数 Agent prompt 告诉模型「做什么」，但不告诉它「怎么做才算完成」和「什么时候该放弃」。Loop Library 提出的 Loop 范式——把 prompt 从「一次性指令」变成「带反馈的循环」——是解决这个问题的最小化、工程化路径，笔者认为它比引入完整的 Agent 框架更实用，比 Skill 组合更贴近工程核心问题。

## 一、问题：一次 Prompt 的根本局限

当我们给 Agent 一个开放式目标——「优化这个网站的性能」「持续改进这个代码库」「把这个功能做完」——我们实际上假设了模型第一次输出就是正确答案。这个假设在简单任务上成立，在复杂长任务上却频繁失效。

真实场景里的两种典型失败模式：

**过度工作**：Agent 不断修改，每次都觉得还能更好，直到超时或 Context 耗尽。Model 的「自信度」并不能可靠地指示「任务完成度」。

**过早放弃**：Agent 完成了一个明显不完整的方案就停下来，因为 prompt 里没有告诉它「什么才算够好」。

这两种失败都源于同一个问题：**prompt 只有执行指令，没有验证条件，没有停止标准**。

## 二、Loop 的结构：四个问题的循环

Loop Library 对这个问题的形式化很简洁——每个 loop 必须能回答四个问题：

**1. What is the agent trying to accomplish?**

描述最终目标，而非操作步骤。「让所有 API 响应时间低于 200ms」是目标，「写一个缓存函数」是操作步骤。目标明确，验证才有可能。

**2. How will it know whether the latest attempt worked?**

这是 Loop 的核心创新：Verification Gate。一个有效的验证条件必须是**可判定的**，而不是模型自我感觉良好。可判定的验证意味着：

- 数值阈值：API 响应时间 < 200ms
- 测试用例：所有新增测试通过
- 回归检查：现有功能没有被破坏
- 人工审批节点：提交变更前需要人类确认

**3. What should it do with what it learned?**

每次循环的结果应该改变下一次的行为。如果一次尝试没有产生有意义的改进，下一次应该有不同的策略或者直接停止。如果产生了改进，下一次应该在此基础上继续。

**4. When should it finish or ask for help?**

没有明确的停止条件，Agent 就会一直运行直到资源耗尽。Loop 必须定义清楚退出条件：目标达成、验证不再通过、资源耗尽、或者需要人工介入。

## 三、Loop 与 Harness：同一问题的不同抽象层级

Harness（参考 Agent Engineering 知识库的 harness 工程分类）是 2025-2026 年 Agent 工程化的核心议题。它的核心问题是：如何在给予 Agent 足够自主性的同时，保证工作质量和工作边界？

Loop 实际上是一种**轻量级 Harness**，它的特点在于把 Harness 的核心机制用 Prompt 语言表达出来，不需要额外的框架或代码：

| Harness 机制 | Loop 的表达方式 |
|---|---|
| Evaluator Loop | Verification Gate |
| Stop Condition | Loop 退出条件 |
| Progress File | 每次循环的状态记录 |
| Handover | 交接文档（当前状态 + 验证结果）|
| Permission/Gate | 人工审批节点 |

区别在于：Harness 通常是系统级设计（代码、配置、评估框架），Loop 是 Prompt 级设计（用自然语言描述反馈结构）。这意味着 Loop 的门槛更低——任何人都可以写一个 Loop，不需要工程团队搭建 Harness 系统。

## 四、为什么 Loop 比 Skill 更接近工程核心

Skill（参考 BuilderIO/skills）是能力单元，它解决的是「Agent 能做什么」的问题。Skill 组合可以扩展 Agent 的能力边界，但 Skill 本身不解决「任务怎么才算完成」的问题。

举例：在一个「持续集成代码审查」的 Agent 工作流里，Skill 是「静态分析」「代码风格检查」「安全扫描」这些功能单元。而 Loop 是让这些 Skill 持续运行的「工作流编排」——每次扫描之后验证结果，根据结果决定是继续修复还是接受当前状态。

没有 Loop 的 Skill 组合，是一系列「做一次就结束」的操作。有 Loop 的 Skill 组合，才是真正能处理长任务的 Agent 工作流。

## 五、Loop 的工程实践建议

基于 Loop Library 的设计原则，笔者对引入 Loop 范式有以下实践建议：

**从简单场景开始**：不要试图一开始就给所有任务都设计 Loop。先从「第一次大概不是最终答案」的场景开始——比如性能优化、测试覆盖改进、文档同步。

**Verification Gate 必须可判定**：如果验证条件依赖模型的「自我感觉」，Loop 就不成立。必须找到可测量的验证标准，或者明确使用人工审批节点。

**Loop 本身也可以被 Agent 优化**：Loop Library 提供的 skill 可以帮助 Agent 发现、评估和修复 Loop。这意味着 Loop 可以成为 Agent 自我改进的工具——让 Agent 能够反思自己的执行策略并调整。

**保持 Loop 的原子性**：一个 Loop 应该专注于一个目标。复杂任务通过多个 Loop 的组合来实现，而不是设计一个无所不包的巨型 Loop。

## 结语

Loop Library 的核心贡献不是提供了一个工具，而是提出了一个思维方式：把「反馈」和「停止条件」作为 Agent 任务设计的核心要素，而不是事后补加的机制。

笔者认为，2026 年 Agent 工程化的真正突破不会来自「更强大的模型」，而是来自「更好的 Agent 工作流工程」。Loop 范式是这条路上最务实的第一步——它不需要改变底层模型，不需要引入复杂的框架，只需要改变 prompt 的结构。

**好的 prompt 不是告诉 Agent 做什么，而是告诉 Agent 怎么判断做够了。**

## 引用

> 「Most prompts ask an agent to do something once. A loop gives the agent a way to learn from the result and take the next useful step.」
> — Forward-Future/loop-library README

> 「A loop as a playbook with feedback built in. It is useful when the first attempt probably will not be the final answer.」
> — Forward-Future/loop-library README

> 「That makes the work easier to trust and easier to repeat. The agent can compare results instead of relying on confidence, keep improvements instead of merely making changes, and stop when it succeeds or stops making progress.」
> — Forward-Future/loop-library README
