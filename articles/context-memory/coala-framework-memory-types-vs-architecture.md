# CoALA 框架：为什么记忆类型和记忆架构是两件必须分开理解的事

> **核心问题**：当你设计一个 Agent 的记忆系统时，你是否曾经在"用哪种数据库"和"用什么记忆模式"之间混淆过？CoALA 框架的核心贡献，就是把这两个问题拆开——记忆类型回答"存什么"，记忆架构回答"怎么存、怎么取、谁来管"。本文从一手论文出发，拆解 CoALA 的核心抽象，并用它重新理解当前主流 Agent 记忆系统的设计选择。

---

## 一个从业者最常踩的坑：把架构问题当作类型问题

假设你正在为客服 Agent 设计记忆系统。你的思考路径可能是这样的：

1. 用户说"Agent 需要记住对话历史" → 于是用向量数据库存储全部历史
2. 用户说"Agent 需要知道之前处理过的case" → 于是又加了一个知识图谱
3. 用户说"Agent 需要能执行固定流程" → 于是把流程写成静态代码

三个决策，三种存储介质，但它们都在解决同一个问题：**这个 Agent 的记忆系统应该长什么样**。你没有清晰框架，所以只能"头痛医头"。

CoALA 框架（ Cognitive Architectures for Language Agents，来自普林斯顿大学 Sumers、Yao、Narasimhan、Griffiths 2023 年的论文，arXiv:2309.02427，发表在 Transactions on Machine Learning Research）正是为了解决这个问题而生。它的核心命题是：

> **语言 Agent 的认知架构包含三个正交维度——记忆组件、动作空间、决策过程——它们必须被独立设计，然后才能组合。**

---

## CoALA 的核心抽象：三组件模型

CoALA 从认知科学和符号 AI 传统中借用了一个洞见：**人脑有不同的记忆系统，它们服务于不同的认知目的**。Classic AI 的智能体架构早有此区分（基于是 Sethumavan 等人的工作），CoALA 将其适配到 LLM-based Language Agent 语境。

### 组件一：记忆模块（Memory Modules）

CoALA 将 Agent 的记忆分为四类，它们是**内容层面的抽象**，与具体存储技术无关：

| 记忆类型 | 功能 | 类比 |
|---------|------|------|
| **Working Memory** | 当前上下文中的活跃信息，类似 CPU 寄存器 | 短期注意焦点 |
| **Episodic Memory** | 过去事件的具体记录，"我记得做过 X" | 个人经历 |
| **Semantic Memory** | 事实性和概念性知识，"X 是 Y" | 长期知识库 |
| **Procedural Memory** | 如何做事的知识，"我通过执行 Z 来完成 W" | 技能/习惯 |

这四类不是四选一，而是**可以同时存在的四层**。一个生产级 Agent 通常需要 Working + Episodic + Semantic 三层，Procedural 层对应的是 Agent 的工具调用能力本身。

> **笔者注**：CoALA 的记忆类型分类（特别是 Episodic vs Semantic）与心理学中经典定义一致。对于工程师来说，最实用的理解是：**Episodic 是时间线，Semantic 是知识网，Procedural 是动作库**。

### 组件二：动作空间（Action Space）

记忆模块是被动的——它们存储信息，但不会主动改变 Agent 的行为。动作空间定义了 Agent **能对记忆和外部环境做什么**。

CoALA 定义了一个结构化的动作空间，分为三类：

1. **外部行动（External）**：与真实环境交互——发送消息、调用 API、操作文件系统
2. **内部记忆行动（Internal Memory）**：读写、更新、遗忘记忆模块中的内容
3. **学习行动（Learning）**：从经验中更新记忆——从 Episodic 中提取模式写入 Semantic，或强化某类动作的触发权重

```
Agent 的动作选择范围：

┌─────────────────────────────────────────────────────┐
│  WORKING MEMORY（当前焦点）                          │
│    ↓ [内部记忆行动]                                  │
│  EPISODIC ← → SEMANTIC    （长期记忆）              │
│    ↓ [学习行动]                                     │
│  PROCEDURAL（如何做）                                 │
│    ↓ [外部行动]                                      │
│  EXTERNAL ENVIRONMENT（外部世界）                      │
└─────────────────────────────────────────────────────┘
```

这个结构的价值在于：**当你设计 Agent 时，你必须明确每个动作属于哪类**，而不是把所有逻辑混在一起。

### 组件三：决策过程（Decision Making）

有了记忆和动作，还需要一个**选择机制**来决定 Agent 在当前状态下应该执行哪个动作。

CoALA 没有指定必须用哪种决策算法（可以是 ReAct、Chain-of-Thought、自我反思，或者未来出现的新方法），它只是定义了一个决策循环的结构：

```
观察 (Observation) → 推理 (Reasoning) → 决策 (Decision) → 行动 (Action) → 反馈 (Feedback) → 学习 (Learning)
```

这个循环在每个时间步重复运行，而决策的输入是 Working Memory 的当前内容和外部环境的反馈。

---

## CoALA 如何重新解释"记忆类型 vs 记忆架构"

这是 CoALA 最重要的工程价值。

**记忆类型**（Memory Types）回答的是"内容是什么"——上文提到的四类。这是设计者的认知层抽象，与具体技术选型无关。

**记忆架构**（Memory Architecture）回答的是三件事的组合：

1. **存储介质**：Context Window、向量数据库、关系数据库、知识图谱、受控元数据目录
2. **检索机制**：全量上下文注入、Top-K 语义搜索、图遍历、函数调用
3. **控制模型**：Agent 被动接收注入的上下文，还是主动管理自己的记忆

Atlan 的文章（Agent Memory Architectures: 5 Patterns and Trade-offs 2026）正是从 CoALA 的这个区分出发，梳理出了生产环境中 5 种具体的架构模式。

### 五种架构模式的 CoALA 映射

| 架构模式 | 存储介质 | 检索机制 | 控制模型 | 对应 CoALA 组件 |
|---------|---------|---------|---------|----------------|
| **Pattern 0: Zero-Infra** | Context Window | 全量注入 | 被动 | 只有 Working Memory |
| **Pattern 1: Vector RAG** | 向量数据库 | Top-K 语义搜索 | 半主动 | Working + Semantic via retrieval |
| **Pattern 2: Graph Memory** | 知识图谱 | 图遍历 | 主动 | Working + Semantic + Episodic 结构化 |
| **Pattern 3: CoALA-Aligned** | 混合存储 | 选择性检索 | 主动管理 | 全四类记忆模块 |
| **Pattern 4: Enterprise Context** | 受控目录 + 图 | 混合检索 | 治理层管控 | 全四类 + 合规治理 |

这五种模式不是技术选型的结果，而是**由业务需求（准确率 vs 延迟 trade-off）+ 合规要求 + 团队能力**共同决定的架构选择。

---

## 为什么"context window 够大就不需要记忆系统"是错的

论文中一个关键的实验事实是：即使把完整对话历史注入 Context Window（全量上下文，Full-context），GPT-4 在 LOCOMO Benchmark（长期对话记忆评测）上的准确率只有 32.1 F1（人类基准 87.9 F1）。原因是：

**Context Window 是 Working Memory 的延伸，不是 Long-term Memory 的替代品。**

Working Memory 的设计目标是**处理当前上下文中的信息**，它的容量限制（即使扩展到 128K）解决的是"当前任务能看多长的上下文"，而不是"跨越 35 个会话后能否准确回忆关键信息"。

CoALA 的框架可以解释这个现象：从 Full-context 到准确回忆，需要经过"检索 → Working Memory → 推理 → 决策"这个完整的 CoALA 循环。但当 Working Memory 被 26,000 Token 的对话历史淹没时（Atlan 的数据显示 Full-context 方案中位数延迟 9.87s，p95 17.12s），这个循环本身就崩溃了。

**记忆架构的设计目标，不是扩大 Working Memory，而是让 Long-term Memory 的内容能够在需要时被高效调入 Working Memory。**

---

## CoALA 的工程实践价值

### 价值一：强制你做记忆需求分析

在动手写代码之前，CoALA 要求你先回答四个问题：

1. 这个 Agent 需要处理哪类记忆？（Episodic？Semantic？）
2. 这些记忆的存储介质是什么？（向量库？图数据库？）
3. Agent 需要对记忆执行哪些动作？（只读？也要写入？）
4. 谁控制记忆的读写？（Agent 自主？外部治理？）

这四个问题对应 CoALA 的三个组件，**任何一个答案的缺失都意味着架构会在某个维度出现盲区**。

### 价值二：诊断现有系统的架构缺陷

用 CoALA 的框架审视当前主流 Agent 框架：

| 框架 | 记忆模块 | 动作空间 | 决策过程 |
|------|---------|---------|---------|
| **LangChain Agent** | 依赖 Tool 的外部检索 | 外部行动为主 | ReAct / Plan-And-Execute |
| **AutoGPT** | 主要是 Working Memory | 大量外部行动 | 自主决策（无结构）|
| **MemGPT** | 四类记忆层次分明 | 显式记忆读写动作 | 层级调度 |
| **CrewAI** | 依赖共享上下文 | 多 Agent 协作动作 | Role-based 决策 |

MemGPT 是当前最接近 CoALA 框架的开源实现——它的架构设计直接体现了 CoALA 的四类记忆模块区分。

### 价值三：为多模态/多Agent场景提供统一语言

当多个 Agent 协作时，如果每个 Agent 的记忆架构不一致，协作就会出现问题。CoALA 提供了讨论多 Agent 记忆互操作性的统一框架：

- 每个 Agent 有自己的四类记忆模块
- Agent 之间的"共享记忆"对应 Semantic Memory 的某个子集
- 跨 Agent 的学习行动（Learning Actions）需要协调协议——这正是 A2A 协议和 MCP 协议在做的事

---

## 局限性：CoALA 不是银弹

CoALA 是一个**概念框架**，不是实现规范。它的局限性在于：

**第一，记忆类型到具体实现的映射不是唯一的。** CoALA 定义了四类记忆，但实际实现中，Episodic Memory 可以用向量数据库存储，也可以用时序数据库。CoALA 没有告诉你哪种更好。

**第二，决策过程是黑盒的。** CoALA 定义了决策循环的结构，但具体用什么算法做推理和决策，留给实现者。这既是灵活性，也是工程陷阱——框架没有防止你设计出一个自我循环的 Agent。

**第三，没有解决记忆一致性问题。** 当多个 Agent 共享某些 Semantic Memory 时，谁负责维护一致性？CoALA 没有给出答案。这需要额外的协调协议（如 A2A 的 shared memory 规范）。

**工程建议**：把 CoALA 当作设计检查清单，而不是实现模板。在设计任何 Agent 的记忆系统时，先用 CoALA 的三个组件做对照检查，识别出架构中缺失的维度。

---

## 总结：架构比类型重要

CoALA 框架的核心贡献，是**强迫从业者区分"记忆存什么"和"记忆怎么管"这两个维度**。

当前 Agent 工程中大多数记忆系统的失败，不是选错了向量库还是知识图谱，而是**没有先回答 CoALA 四个问题**：需要哪类记忆、存什么介质、执行什么动作、谁控制读写。

一旦这个框架被建立起来，技术选型就变成了有方向的搜索，而不是盲目试错。

---

## 参考文献

- [Cognitive Architectures for Language Agents (CoALA) - arXiv:2309.02427](https://arxiv.org/abs/2309.02427) — CoALA 框架原始论文，Princeton，Transactions on Machine Learning Research 2024
- [Agent Memory Architectures: 5 Patterns and Trade-offs (2026) - Atlan](https://atlan.com/know/agent-memory-architectures/) — 基于 CoALA 的五类架构模式，附 LOCOMO 基准数据
- [Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory - arXiv:2504.19413](https://arxiv.org/abs/2504.19413) — ECAI 2025，10 种记忆方案横向评测，评测方法基于 LOCOMO
- [LOCOMO: Long-term Conversation Memory Benchmark - ACL 2024](/articles/context-memory/locomo-benchmark-memory-systems-2026.md) — 长期对话记忆 Benchmark，GPT-4 纯 Context Window 仅 32.1 F1 的来源
- [Awesome Language Agents - GitHub](https://github.com/ysymyth/awesome-language-agents) — CoALA 官方维护的论文列表，按框架分类