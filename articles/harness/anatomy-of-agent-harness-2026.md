# Agent = Model + Harness：Harness 的第一性原理分析

> **来源**: [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)，Vivek Trivedy，LangChain Blog，2026
> **分类**: harness
> **核心判断**: Agent 系统的一切非模型部分 = Harness；Harness 是连接模型能力与实际工作之间的所有工程基础设施；理解 Harness 的组件边界是设计 Agent 架构的前提

---

## TL;DR

> 如果你不是模型，你就是 Harness。
> Agent = Model + Harness。模型提供智能，Harness 将智能转化为实际的工作引擎。

---

## 1. 什么是 Harness？

LangChain 的 Vivek Trivedy 给出了最干净的 Harness 定义：

> **Harness = 模型之外的所有代码、配置和执行逻辑。**

一个裸模型（raw model）本质上只是"输入文本，输出文本"。它无法做到：
- 跨交互维护持久状态
- 执行代码
- 访问实时知识
- 搭建环境、安装依赖来完成工作

这些都是 Harness 层面的能力。

### Harness 的核心组成部分

```
Harness
├── System Prompts              # 行为指令层
├── Tools, Skills, MCPs         # 工具与扩展能力
├── Bundled Infrastructure      # 文件系统、沙箱、浏览器
├── Orchestration Logic        # 子 Agent 调度、Handoff、模型路由
└── Hooks/Middleware            # 确定性执行：压缩、连续性检查、Lint
```

这个分解框定了 Agent 工程的所有工作边界。

---

## 2. 为什么从模型视角推导 Harness？

Vivek 的方法论值得注意：他不是从"Agent 应该做什么"来列举功能，而是**从模型的固有局限出发**，反推 Harness 必须提供什么。

**模型的本质限制**：
- 输入/输出：文本（或图片/音频/视频的 token 化表示）
- 无状态：每次调用是独立的
- 无执行能力：不能运行代码、访问网络、操作文件系统
- 无实时知识：知识截止于训练数据

这个视角让 Harness 的组件选择变得有原则，而不是堆砌功能。

---

## 3. 核心 Harness 组件的架构分析

### 3.1 文件系统：持久化与上下文管理的基础设施

**问题**：模型的上下文窗口是有限的，且无法持久保存工作进度。

**Harness 解决方案**：提供文件系统抽象，让 Agent 可以：
- 在工作空间读写代码、数据和文档
- 将中间结果外存而非全部塞进上下文
- 跨会话保持状态（重启后继续工作）
- 支持多 Agent 和人类的协作（通过共享文件）

文件系统还是其他 Harness 特性依赖的基础原语（如 Git 版本控制）。

**架构意义**：文件系统是 Harness 最基础的原语（primitives），它将"上下文窗口的有限性"这个问题转化为了"持久化存储管理"。

### 3.2 Bash + Code 执行：通用问题解决工具

**问题**：预定义工具数量有限，无法应对 Agent 面对的所有未知任务。

**Harness 解决方案**：给 Agent 一个通用执行工具（Bash/代码执行），让它能够**自己设计工具**。

典型模式是 ReAct Loop（Reason + Act + Observe + Repeat）：模型推理 → 调用工具 → 观察结果 → 重复。代码执行让这个模式真正通用化：Agent 可以动态构造任何它需要的工具，而不是被固定工具集约束。

**架构意义**：Code Exec 使 Agent 从"使用预定义工具"进化到"自主创造工具"，这是从"工具使用者"到"工具创造者"的关键一步。

### 3.3 沙箱：安全执行环境

**问题**：在本地执行 Agent 生成的代码是危险的，且单一本地环境无法 scale。

**Harness 解决方案**：提供隔离的云端执行环境。

- 安全隔离：错误影响范围可控，不会破坏生产系统
- 可扩展：按需创建、并行分发、完成后销毁
- 可配置的网络隔离和命令白名单
- 预装语言运行时、CLI 工具（git、测试框架）、浏览器等

沙箱还给 Agent 提供了**观察和验证能力**：浏览器、日志、截图、测试运行器——让 Agent 看到自己工作的结果，形成自我验证闭环。

**架构意义**：沙箱是 Enterprise Agent 的必备基础设施。没有沙箱，就没有安全的企业级 Agent 部署。

### 3.4 Memory & Search：持续学习

**问题**：模型权重无法更新，知识截止于训练数据，无法从生产经验中学习。

**Harness 解决方案**：通过上下文注入实现"记忆"和"实时知识"。

- **短期记忆**：当前会话内的状态维护（ReAct Loop 的 state）
- **长期记忆**：向量数据库、RAG、持久化存储
- **实时知识**：搜索引擎、API 调用获取最新信息

这与"你的 Harness 就是你的 Memory"（LangChain Blog，2026-04-11）一文形成完整呼应：Memory 是 Harness 的子组件，选择哪个 Harness = 选择哪种 Memory 架构。

---

## 4. 为什么这个定义重要

### 4.1 它统一了行业术语

市面上关于"Agent"、"Harness"、"Framework"、"Platform"的讨论充满歧义。这个定义提供了一个清晰的二分法：**模型 vs. 非模型**。任何讨论都可以用这个透镜来澄清边界。

### 4.2 它指导架构决策

知道"Harness 负责什么"意味着：
- 当 Agent 行为异常时，先排查 Harness 而不是模型
- 评估一个新工具/框架时，首先问：它修改了 Harness 的哪个组件？
- 选择模型时，Harness 的兼容性应该是关键考量

### 4.3 它解释了为什么"用哪个 Harness"比"用哪个模型"更关键

在模型能力趋同的背景下（HCL 评测显示 GLM-5、MiniMax M2.7 等开放模型已接近封闭前沿模型），**Harness 的质量成为差异化因素**。这与"开放 Harness 赢得 Agent 记忆战"一文的判断一致：Harness 层才是架构竞争的主战场。

---

## 5. 与其他文章的关系

| 文章 | 关系 |
|------|------|
| [开放 Harness 赢得 Agent 记忆战](harness/open-harness-memory-lock-in-2026.md) | 续篇：Memory 是 Harness 的子组件；封闭 Harness = 封闭 Memory 架构 |
| [Better Harness：Eval-Driven Agent 迭代优化](harness/better-harness-eval-driven-agent-iterative-optimization-2026.md) | 并列：Harness 的不同维度（Eval vs. Architecture） |
| [GAN 启发的 Agent Harness](harness/gan-inspired-agent-harness-long-running-2026.md) | 并列：Harness 的具体工程实现 |

---

## 6. 核心要点

1. **定义边界清晰**："不是模型 = 就是 Harness"是架构分析的最基本划分
2. **第一性推导**：从模型局限出发推导 Harness 组件，比枚举功能更有原则性
3. **四大组件**：文件系统（持久化）、代码执行（通用工具）、沙箱（安全执行）、Memory/Search（持续学习）
4. **Harness > Memory**：Memory 是 Harness 的子组件，选择 Harness = 选择 Memory 架构
5. **模型同质化时代**：当模型能力趋同时，Harness 质量成为 Agent 系统竞争力的决定性因素

---

_本文是对 LangChain Blog "The Anatomy of an Agent Harness" 的深度解读与架构分析。_
