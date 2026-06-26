# Microsoft Agent Framework BUILD 2026：CodeAct 引擎与 Harness 生产级突破

> 核心论点：MAF 1.0 GA 建立框架基座，BUILD 2026 的实质突破在于两个工程维度——CodeAct 将多步工具调用压缩为单次程序执行（52.4% 延迟降低、63.9% Token 节省），而增强的 Harness 层则将生产级模式（Context 压缩、指令合并、Session 恢复）变为开箱即用的构建块。这是 2026 年中企业 Agent 基础设施从「能跑」到「能 production」的关键一步。

---

## 背景：1.0 GA 之后的工程缺口

MAF 在 2026 年 4 月达到 1.0 GA，完成 AutoGen + Semantic Kernel 的架构收敛。框架层面的统一已经完成，但工程团队面临的核心问题并未解决：

1. **工具调用开销**：Agent 在长链条任务中，每个小工具调用都是一次独立模型往返，延迟和 Token 成本线性累积
2. **Harness 碎片化**：生产级 Agent 需要的 Context 管理、Session 恢复、指令分层等能力，每家企业各自实现，重复造轮子
3. **多 Agent 编排的脆弱性**：路由器转发模式在遇到「需要反问」「需要同事上下文」「发现自己判断错了」时就中断

BUILD 2026 的更新直击这三个缺口。

---

## CodeAct：从多步工具链到单次程序执行

### 问题本质

传统 Agent 的工具调用循环：

```
模型 → 选择工具 → 等待执行 → 接收结果 → 模型 → 选择下一个工具 → ...
```

每个工具选择都是一次独立模型调用。对于「跨多个数据源汇总报表」这类任务，可能产生数十个模型往返，每次往返的延迟叠加加上每次往返携带的 Context 传递成本，成为显著的瓶颈。

### CodeAct 的解法

CodeAct 的核心思想是：**让模型写一段短 Python 程序，通过 `call_tool()` 调用多个工具，一次运行返回聚合结果。**

```python
# 模型生成并执行这样的程序
result = call_tool("get_weather", city="Seattle")
result2 = call_tool("get_weather", city="Amsterdam")
# 对比逻辑
...
```

这将原来可能需要 10+ 次模型往返的任务压缩为 1 次。关键的支持技术是 **Hyperlight**——Microsoft 开源的 micro-VM，每个 `call_tool()` 调用运行在独立的 Hyperlight 隔离环境中，程序执行完毕即销毁，实现强隔离的同时几乎没有冷启动开销。

### 性能数据

官方基准测试（多用户订单汇总场景，数十次工具调用）：

| 指标 | 传统模式 | CodeAct | 改善幅度 |
|------|---------|---------|---------|
| 执行时间 | 27.81s | 13.23s | **52.4%** |
| Token 消耗 | 6,890 | 2,489 | **63.9%** |

笔者认为，这个改善幅度在生产环境中意义显著。以一个日均处理 10,000 次多步任务的 Agent 服务为例，63.9% 的 Token 节省直接转化为成本下降，而 52.4% 的延迟改善则直接影响用户体验和任务完成率。

### 局限性

CodeAct 并非万能药。对于以下场景，传统工具调用链仍然是更优选择：

- **需要实时交互的探索性任务**：模型在执行过程中需要根据中间结果调整策略，单次程序执行无法支持这种迭代
- **工具副作用不确定的场景**：CodeAct 适合「模型生成程序、执行、返回结果」的确定性场景；对于有外部状态依赖的工具，隔离环境可能导致行为不一致
- **调试复杂度**：单次程序执行比逐步工具调用更难追踪和复现问题

笔者认为，CodeAct 的正确用法是：**针对已知模式的、结构化的多步骤任务，使用 CodeAct 优化性能；对于开放式的探索性任务，保留传统工具调用链。**MAF 的设计允许两者并存，这是合理的工程选择。

---

## Agent Harness：生产级模式的开箱化

### 什么是 Harness 层

在 MAF 架构中，Harness 是「模型推理与真实执行之间的连接层」。它解决的问题是：模型生成的输出如何可靠地转化为文件系统操作、Shell 执行、审批流程和跨长会话的 Context 管理。

1.0 GA 的 Harness 已经包含了基础模式，BUILD 2026 的更新将这些模式扩展为更完整的构建块集合。

### 核心新增构建块

**Context 压缩（Automatic Context Compaction）**

传统 Agent 在长对话中面临 Context 窗口溢出的问题。常见解法是外部实现截断逻辑，或者依赖模型的隐式摘要能力。

MAF 的内置方案是：**监控 Token 使用量，在达到阈值时自动压缩 Chat 历史，同时保留关键指令和最新上下文。**

这解决了一个工程实践中频繁出现的痛点——不是「能不能压缩」的问题，而是「谁来写这段压缩逻辑、压缩策略是什么、压缩后是否影响后续推理」的问题。内置意味着开箱即用且策略经过验证。

**指令合并（Instruction Merging）**

生产 Agent 通常有多层指令：框架级默认指令、应用级指令、任务级指令。传统的实现是字符串拼接或者模板继承，容易出现优先级混乱或者指令冲突。

MAF 的设计是 **Harness 指令始终优先出现，随后是自定义 Agent 指令**。这种顺序保证了一致性：框架级的安全约束不会被应用指令意外覆盖。

**Session 级 Provider 矩阵**

| Provider | 功能 | 典型场景 |
|----------|------|---------|
| FileMemoryProvider | Session 级别的文件持久化笔记 | 跨会话记忆关键决策和上下文 |
| TodoProvider | 任务清单管理 | 多步骤任务的状态跟踪 |
| AgentModeProvider | Plan/Execute 模式切换 | 规划阶段不执行，执行阶段不复查 |
| AgentSkillsProvider | 文件系统技能发现和加载 | 模块化的能力注入 |
| BackgroundAgentsProvider | 并行子 Agent 委托 | Fan-out 型任务分解 |

笔者认为，**这个 Provider 矩阵的设计思路值得注意**：它没有选择「一个大而全的 Memory 系统」，而是将不同维度（文件、任务、模式、技能、子 Agent）拆分为独立可插拔的 Provider。这种设计降低了复杂度，也使得企业可以针对自己的场景替换特定 Provider（例如用 Redis 替代 FileMemoryProvider 的文件系统存储）。

**审批规则的「不再询问」模式**

ToolApprovalAgent 支持「don’t ask again」规则——对于特定工具或者特定条件下的工具调用，一次审批后自动通过。这解决了 Human-in-the-loop 在批处理场景中的体验问题。

笔者认为，这个功能的工程意义在于：**它将审批决策从运行时问题转化为配置问题**。企业可以在部署前定义好审批策略，而不是在运行时动态判断。这对于合规要求明确但人工审批成本高的场景（如金融、医疗）尤为重要。

---

## Foundry Hosted Agents：Session 恢复的生产化

MAF 本地运行和 Foundry 部署之间的一致性是 BUILD 2026 强调的工程价值。几个关键特性：

**Scale-to-Zero + 有状态恢复**

传统 Serverless 函数的冷启动问题是 Agent 的特殊挑战——一个长任务执行到一半被缩容到零，再次启动时需要恢复完整的执行上下文，成本极高。

Foundry Hosted Agents 的方案是：**Session 级别的文件系统持久化**。Agent 缩容后，文件系统状态（磁盘内容、工作目录）被保留；再次扩容时，Agent 看到的是「磁盘状态完好、可以从中断点继续」的工作环境。

笔者认为，这解决了长任务 Agent 的一个核心工程障碍：**检查点（Checkpoint）不再是应用层需要自己实现的东西**，而是平台基础设施的一部分。这对于需要数小时甚至数天完成的长周期任务（如代码库重构、大规模数据处理）意义重大。

**Per-Session 隔离**

每个 Session 运行在独立 VM 隔离环境中，Session 之间完全隔离。这解决了多租户场景下的安全和稳定性问题——一个 Session 的资源消耗或者异常行为不会影响其他 Session。

---

## Handoff 模式：多 Agent 编排的工程化

### 传统路由器模式的问题

常见的多 Agent 系统从「路由器 + 专家 Agent」模式开始：

```
用户请求 → 路由器判断类型 → 转发到 Billing Agent / Tech Agent → 返回结果
```

这个模式在「请求类型明确且单一」时工作良好，但在以下场景失效：

- **需要反问**：Billing Agent 发现用户的问题实际上技术问题，需要转回路由器再路由
- **需要同事上下文**：Tech Agent 需要 Billing Agent 的某次会话历史来理解用户的背景
- **发现自己错了**：路由器判断失误，转到了错误的 Agent，Agent 需要主动转移

### Handoff 模式的设计

MAF 的 Handoff 编排将「拓扑和护栏」与「路由决策」分离：

```python
# 开发者声明拓扑和护栏
workflow = HandoffBuilder(participants=[triage, billing, tech])
    .with_start_agent(triage)
    .add_handoff(triage, [billing, tech])
    .build()
```

```csharp
// C# 等价
var workflow = AgentWorkflowBuilder
    .CreateHandoffBuilderWith(triage)
    .WithHandoff(triage, billing)
    .WithHandoff(triage, tech)
    .Build();
```

框架自动为每个 Agent 注入 Handoff 工具，Agent 在运行时可以主动调用 `handoff` 工具将控制权转移给其他 Agent，同时可以选择性地传递上下文（会话历史、关键变量、用户意图摘要）。

**路由决策交给 Agent，拓扑和护栏留给开发者。** 这是关键的设计哲学转变——不再是「中心路由器决定一切」，而是「Agent 在明确规则下有自主转移权」。

笔者认为，这个设计比简单的路由器模式更接近真实企业的多 Agent 协作逻辑。企业中的部门协作本来就不是「一个前台决定所有分配」，而是「各部门在规则内自主协作，同时有明确的升级和协同机制」。

---

## 与 Cursor Composer 2.5 的关联：训练方法论的收敛

值得注意的是，MAF BUILD 2026 的 Bugbot 章节提到了这样的技术细节：

> 「These performance gains are made possible by harness improvements and progress we've made training Composer 2.5」

MAF 的团队提到 Bugbot 的性能提升部分来自于 Composer 2.5 模型的进步，而 Composer 2.5 的技术博客中也提到：

> 「Composer 2.5 is trained with 25x more synthetic tasks than Composer 2... unexpected reward hacking... we were able to find and diagnose these problems using agentic monitoring tools」

两篇官方博客在同一天发布，却交叉引用了彼此的技术进步。这说明 **2026 年中，主要 Agent 工程团队已经在内部形成了「训练 + Harness 协同优化」的闭环方法论**——不是单纯靠更大模型，也不是单纯靠更好的工程，而是在模型训练阶段就使用 Agent 工具进行课程学习和对抗性测试，再用改进后的模型驱动更好的 Harness 表现。

笔者认为，这个交叉引用本身就是一个值得关注的信号：**顶级 Agent 工程团队之间的技术路线正在收敛到同一个框架**，而这个框架的核心不是某个具体算法，而是「如何让模型能力和工程基础设施协同进化」的系统性方法。

---

## 总结：2026 H2 的工程主线

MAF BUILD 2026 的更新可以用三个关键词概括：

1. **CodeAct**：通过程序化执行压缩工具调用开销，将性能优化从配置层推到执行模型层
2. **Harness 生产化**：将原本需要企业自研的 Context 管理、Session 恢复、审批策略等能力变为平台内置构建块
3. **Handoff 编排**：将多 Agent 协作从「中心路由」升级为「规则约束下的自主协同」

这三个方向分别对应了 2026 年 Agent 工程的三条主线：**执行效率、生产可信赖性、协作规模化**。MAF 的价值在于，它不是提出新概念，而是将这三个方向上已经验证的工程模式变成了统一 SDK 中的第一公民（First-class）能力。

对于已经在使用 MAF 的团队，BUILD 2026 的更新意味着可以从「自己实现 Harness」转向「直接使用内置构建块」，工程成本显著降低。对于还在选型的团队，这些更新的组合拳代表了 2026 年企业级 Agent SDK 的主流工程方向。

---

**引用来源**：

- [Microsoft Agent Framework at BUILD 2026: Agent Harness, Hosted Agents, CodeAct, and more](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/) (2026-06-03)
- [Agent Harness in Agent Framework](https://devblogs.microsoft.com/agent-framework/agent-harness-in-agent-framework/)
- [CodeAct in Agent Framework](https://devblogs.microsoft.com/agent-framework/codeact-with-hyperlight/)
- [A Tour of the Handoff Orchestration Pattern](https://devblogs.microsoft.com/agent-framework/a-tour-of-handoff-orchestration-pattern/)