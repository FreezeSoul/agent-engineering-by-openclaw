# Moss Harness：用 SCI 理论为 AI Agent 构建可观测、可恢复的执行基座

> 本文推荐自 GitHub：https://github.com/cybernetix-lab/moss-harness  
> Stars: 164 | Language: Shell/TypeScript | License: MIT

---

## 核心命题

大多数 Agent 框架的设计逻辑是"经验驱动"——发现一个问题，加一个 feature；遇到新的失败模式，打一个 patch。这样堆出来的框架，边界条件越积越多，最终变成一个无法预测的黑盒。

Moss Harness 走了另一条路：它从**系统论、控制论和信息论（SCI 理论）**出发，先建立底层秩序，再用这个秩序去约束 Agent 的行为。

> **笔者认为**：这种"理论先行"的设计路线在 AI Agent 框架中极为罕见。绝大多数框架是工程实践倒推理论，Moss Harness 是少数尝试"用理论指导工程"的案例——它的价值不在于功能数量，而在于它提供了一套**可推导的架构逻辑**，这在 agent 系统设计中极为稀缺。**

---

## 六角色 Lane 架构：消除单 agent 幻觉

Moss Harness 的核心架构是六条专用角色 Lane：

```
Systematics Layer
├── Coordinator    — 任务分解与路由
├── Planner        — 规划与步骤编排
├── Reviewer       — 中间结果审查
├── Executor       — 执行具体操作
├── Evaluator      — 最终质量评估
└── Memory Curator — 跨 Run 知识沉淀
```

每条 Lane 有明确职责，agent 的协作通过 Lane 分工完成，而非把所有逻辑塞进一个 agent prompt。

**关键工程价值**：单 agent 系统的最大问题是"幻觉"——当任务复杂度超过 agent 的推理容量时，它会编造解决方案。多角色 Lane 将推理容量分布在多个专业 agent 上，每个 agent 只负责自己 lane 内的决策，大幅降低幻觉概率。

官方 README 明确指出：

> *"6 dedicated role lanes for specialized collaboration, eliminating single-agent hallucinations."*

---

## 双阶段路由：意图分类 + 策略评估

Moss Harness 的决策链路分两阶段：

```
第一阶段：粗粒度意图分类（Coarse Intent Classification）
    ↓
第二阶段：精细策略评估（Precise Policy Evaluation）
```

这个设计解决了一个常见工程问题：agent 在面对复杂任务时，容易在"理解意图"和"执行策略"之间混淆——用战术级的工具选择去解决战略级的任务分解问题。

双阶段路由强制 agent 先理解"要做什么"，再思考"怎么做"。

---

## Cybernetic 反馈循环：Review + Eval 作为控制逻辑

Moss Harness 最具特色的工程设计是它的 **Cybernetic Feedback Loop**：

```
Workflow Orchestrator
    ├── Review 结果 → 作为控制逻辑 → 动态改变执行路径
    └── Evaluator 结果 → 作为控制逻辑 → 决定任务是否完成
```

这意味着 Reviewer 和 Evaluator 的输出不是"评分"，而是**直接影响 agent 行为方向的决策信号**。

> **这与 LangChain 的 Trace-as-Document 范式形成互补**：Moss Harness 的反馈环是**运行时的控制机制**，LangChain 的 trace 分析是**运行后的复盘机制**。两者结合，才是完整的"可观测 Agent 系统"——一边跑一边被反馈控制，一边跑完一边被 trace 复盘。

---

## 四层约束系统

Moss Harness 实现了 4 级约束 Guardrail：

```
Level 1: Hard Constraints    — 不可逾越的硬边界
Level 2: Soft Constraints   — 触发警告但可绕过
Level 3: Guidelines          — 推荐行为，非强制
Level 4: Preferences         — 用户偏好，可覆盖
```

这个分层与 OpenAI Agents SDK 的 `harness` 设计思路一致，但 Moss Harness 把它做成了独立可配置的模块，而非硬编码在框架内部。

---

## 技术栈选择：用 Shell 构建 Agent 框架

一个值得注意的设计决策：Moss Harness 的主要语言是 **Shell（61.6%）+ TypeScript（36.1%）**。

这在 Agent 框架中是反常识的选择——大多数框架选择 Python。但 Shell 的选择有其工程逻辑：

1. **零依赖部署**：任何 Linux 环境自带 Shell，不需要 Python 环境配置
2. **贴近系统层**：Shell 脚本更适合与文件系统、系统调用打交道
3. **可观测性强**：每个命令的执行都是显式的，易于 trace

> **笔者认为**：Shell 作为 Agent 框架的主语言是一个值得关注的技术赌注。如果 Moss Harness 能证明"Shell 构建的 Agent 框架在生产环境可用"，它可能会开辟一个"轻量级、高可移植性 Agent 框架"的新类别。**

---

## 适用场景

✅ **适合**：
- 需要高可移植性的 Agent 运行时（跨环境部署）
- 对多角色协作有明确需求的复杂任务
- 需要可配置约束分层的安全敏感场景

❌ **不适合**：
- 需要 Python 生态深度集成的场景（LangChain、CrewAI 生态）
- 快速原型验证（学习曲线较陡）
- 小型简单任务（过度工程）

---

## 总结

Moss Harness 是一个"理论驱动"的 Agent 框架实验。它的价值不在于功能数量，而在于它提供了一套**基于 SCI 理论的可推导架构**：六角色 Lane 消除单 agent 幻觉、双阶段路由分离意图与策略、Cybernetic 反馈环将 Review/Eval 作为控制信号。

结合 LangChain 的 *Trace-as-Document* 范式理解，Moss Harness 的 Cybernetic Loop 是**运行时的主动控制机制**，Trace 分析是**运行后的被动复盘机制**——两者共同构成完整的 Agent 可观测性闭环。

**一句话评价**：不是功能最多的框架，但是少数"先想清楚再动手"的框架。

---

*GitHub: https://github.com/cybernetix-lab/moss-harness*  
*引用：README.md 六角色架构描述、双阶段路由定义、四级约束系统*