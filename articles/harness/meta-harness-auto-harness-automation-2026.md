# Meta-Harness + AutoHarness：Harness 自动合成的两条技术路线

> **核心问题**：传统 Harness Engineering 依赖工程师手工调优——观察失败、手动改 Prompt、再观察。这是试错式的，效率低，且无法规模化。Stanford 的 Meta-Harness 和 DeepMind 的 AutoHarness 给出了两条不同的自动化路线。
>
> **读完能得到什么**：理解两条路线的核心差异（Filesystem-based Proposer vs Environment Feedback Loop）、各自的适用场景、以及"让 Agent 自己优化 Harness"这一范式转变的工程意义。

---

## TL;DR

| 方法 | 核心机制 | 关键创新 | 主要成果 |
|------|---------|---------|---------|
| **Meta-Harness**（Stanford） | Filesystem-based Proposer | 10M tokens/iter 诊断上下文 | TerminalBench-2 Opus #2，Haiku #1 |
| **AutoHarness**（DeepMind） | Environment Feedback Loop | 小模型合成 custom harness | 145 游戏零非法动作，超越大模型 |

---

## 一、问题：为什么 Harness 需要自动化

传统 Harness Engineering 是手工的：

1. 工程师观察 Agent 失败案例
2. 手工修改 Prompt 或工具描述
3. 重新测试
4. 循环往复

这在原型阶段勉强能用。但当 Agent 进入生产，Harness 的"参数空间"（System Prompts、工具集、Middleware、Memory 配置……）变得巨大，手工调优无法覆盖所有边界情况。

**更好的思路：让 Harness 自己能变好。**

这个方向有两篇重要论文给出了不同的解答：Meta-Harness（Stanford）和 AutoHarness（DeepMind）。

---

## 二、Meta-Harness：Filesystem-based Proposer

### 2.1 核心创新：全量历史上下文

现有 LLM 优化方法（OPRO、Self-Refine、TextGrad、MIPRO、AlphaEvolve 等）都将历史信息压缩成简短格式：

| 方法 | 上下文量 |
|------|---------|
| Self-Refine | 0.001 tokens/iter |
| OPRO | 0.002 tokens/iter |
| MIPRO | 0.003 tokens/iter |
| AlphaEvolve | 0.022 tokens/iter |
| GEPA | 0.008 tokens/iter |
| **Meta-Harness** | **10,000,000 tokens/iter** |

Meta-Harness 的关键创新：给 Proposer 一个**文件系统**，包含所有先前 candidates 的：
- 源代码
- 评估分数
- **完整执行 traces**（prompts、model outputs、tool calls、errors）

Proposer 是一个 coding agent（Claude Code），通过 grep、cat 等标准工具读取需要的内容。这实现了**按需访问**而非压缩。

### 2.2 为什么全量 traces 重要

Harness 工程的失败往往无法从标量分数诊断——需要看到原始执行 trace 来追溯具体是哪个 Harness 决策导致了失败。

例如，一个代码生成 Agent 在 10 个任务中失败了 3 个。分数告诉你"30% 失败率"，但只有完整的执行 trace 才能告诉你：失败是因为 Terminus-KIRA 的 completion-checking logic 在某个边界条件下误判成功，还是因为 system prompt 中的某个指令让 Agent 在遇到网络超时时选择了错误的 fallback。

### 2.3 搜索闭环

```
(1) Agent 读取 filesystem（所有先前 candidates 的源码、traces、分数）
(2) 提出新的 harness candidate
(3) 在 held-out tasks 上评估
(4) 所有 logs 写回 filesystem
(5) 循环
```

### 2.4 实验结果

**Text Classification（法律、医学、专利数据集）**

| Method | USPTO | S2D | Law | Acc |
|--------|-------|-----|-----|-----|
| Zero-shot | 12.0 | 63.2 | 7.0 | 27.4 |
| Few-shot (N=32) | 13.0 | 72.2 | 21.0 | 35.4 |
| ACE | 16.0 | 77.8 | 29.0 | 40.9 |
| **Meta-Harness** | **14.0** | **86.8** | **45.0** | **48.6** |

最佳发现的 harness（Label-Primed Query）比 ACE 高 **+7.7 points**，且上下文 tokens 少 **4×**。

**TerminalBench-2（Agentic Coding）**

| Claude Opus 4.6 | Pass % |
|-----------------|--------|
| Terminus-KIRA | 74.7 |
| Capy | 75.3 |
| **Meta-Harness** | **76.4** |
| ForgeCode | 81.8 |

| Claude Haiku 4.5 | Pass % |
|------------------|--------|
| Goose | 35.5 |
| **Meta-Harness** | **37.6** |

Meta-Harness 在 Opus 4.6 上排名第 2，在 Haiku 4.5 上排名第 1。

---

## 三、AutoHarness：Environment Feedback Loop

### 3.1 核心问题

LLM Agent 常尝试被外部环境禁止的动作。论文给出的极端案例：

> Kaggle GameArena 棋类比赛中，**78% 的 Gemini-2.5-Flash 损失**源于非法动作。

这不是模型能力问题，而是 **Harness 问题**——Agent 没有被正确约束。

### 3.2 核心创新：小模型合成 Custom Harness

AutoHarness 的方法：

1. 给 Gemini-2.5-Flash 少量样例（seed harness + 失败案例）
2. 模型自动生成 code harness（约束规则）
3. 在环境中测试
4. 根据环境反馈迭代 refinement
5. 直到在 145 个不同 TextArena 游戏中消除所有非法动作

### 3.3 关键发现：Small Model > Large Model

最反直觉的结果：

> **使用 Gemini-2.5-Flash 合成 custom code harness，可以让同一个 Flash 模型胜过 Gemini-2.5-Pro。**

更进一步：将整个 policy 写成代码，**决策时完全不需要 LLM 调用**。这样得到的 code-policy 在 16 个 TextArena 1-player 游戏中获得的平均 reward 高于 Gemini-2.5-Pro 和 GPT-5.2-High。

**这意味着**：在某些场景下，"学会约束"比"学会推理"更有效。

### 3.4 Code-Policy 的优势

| 特性 | LLM Policy | Code-Policy |
|------|-----------|-------------|
| 推理成本 | 每次决策一次 LLM 调用 | 零 LLM 调用 |
| 确定性 | 有随机性 | 完全确定性 |
| 可解释性 | 隐式 | 显式代码逻辑 |
| 泛化能力 | 依赖 prompt | 依赖规则覆盖度 |

---

## 四、两条路线的对比

### 4.1 机制对比

| 维度 | Meta-Harness | AutoHarness |
|------|-------------|-------------|
| **反馈来源** | Held-out evals（离线评估） | Environment feedback（在线执行） |
| **Proposer** | Coding agent（filesystem 导航） | LLM（直接代码生成） |
| **上下文量** | 10M tokens/iter | 种子 harness + 少量示例 |
| **搜索空间** | System prompts、工具定义、checking logic | Code harness constraints |
| **适用场景** | 复杂多步骤任务（coding、retrieval） | 有明确环境约束的游戏/工具场景 |

### 4.2 互补性

这两条路线解决不同层面的问题：

- **Meta-Harness**：解决"Harness 的哪些组件需要改"
- **AutoHarness**：解决"如何让约束规则自动生成"

可以想象一个组合系统：AutoHarness 负责生成初始约束，Meta-Harness 负责在更大范围内优化整个 Harness 配置。

### 4.3 与 Better Harness 的关系

[Better Harness](../harness/better-harness-eval-driven-agent-iterative-optimization-2026.md) 是人工驱动的迭代优化（Human-in-the-loop）：

```
人工选择改动方向 → Eval 验证 → 循环
```

Meta-Harness 和 AutoHarness 是**全自动**的迭代优化：

```
Proposer 自主提出改动 → 评估/环境反馈 → 循环
```

三者的演进路径：

```
手工调优 → Better Harness（人主导）→ Meta-Harness/AutoHarness（AI 主导）
```

---

## 五、工程启示

### 5.1 Harness 是可优化的系统

这三个工作（Better Harness、Meta-Harness、AutoHarness）共同揭示了一个范式转变：

> **Harness 不是静态配置，而是可优化的系统。**

传统思维：Harness 是工程师手工设定的"超参数"。
新思维：Harness 是可以通过 Evals 和反馈自动改进的系统。

### 5.2 全量 Traces > 标量分数

Meta-Harness 最重要的工程 insight：

> ** Harness 失败需要全量 traces 才能诊断。**

标量分数告诉你"失败了"，traces 告诉你"为什么失败"以及"怎么修"。这对生产环境的 Harness 调试有直接指导意义。

### 5.3 Code-Policy 的工程价值

AutoHarness 揭示了一个反直觉但重要的 insight：

> **在某些场景下，代码规则比 LLM 推理更可靠。**

这不意味着 LLM 不重要，而是说：**LLM 的价值可以体现在"生成可靠的约束规则"，而不只是"直接做决策"**。

对于需要确定性、可审计性的生产系统，code-policy 可能是比纯 LLM policy 更稳妥的选择。

### 5.4 成本权衡

AutoHarness 的结果显示：小模型 + custom harness 可以胜过裸大模型。

这意味着：
- **推理成本**：code-policy 推理时零 LLM 调用
- **合成成本**：需要一次性的 harness 合成（可以用小模型做）
- **质量**：可以匹敌甚至超过大模型

对于高频、低延迟、确定性的场景，这可能是更经济的架构。

---

## 六、核心 insight

1. **Harness 优化的三个层次**：手工调优 → Better Harness（人主导） → Meta-Harness/AutoHarness（AI 主导）
2. **全量 traces 是诊断的关键**：10M tokens vs 0.002 tokens 的差距说明了为什么之前的自动化方法效果有限
3. **Code-policy 可以超越 LLM policy**：AutoHarness 展示了约束规则合成可能是比端到端 LLM 推理更有效的路径
4. **两条路线互补**：Meta-Harness 擅长复杂多步骤任务的全栈优化，AutoHarness 擅长有明确环境约束的规则生成

---

## 七、相关阅读

| 文章 | 关系 |
|------|------|
| [Better Harness：Eval-Driven Agent 迭代优化](../harness/better-harness-eval-driven-agent-iterative-optimization-2026.md) | 同属 Harness 优化范畴，但为人主导的方法 |
| [Anatomy of Agent Harness](../harness/anatomy-of-agent-harness-2026.md) | Harness 的第一性原理分析，定义边界 |
| [Harness Engineering：深度约束下的 Agent 能力最大化](../harness/harness-engineering-deep-dive.md) | Harness Engineering 的基础框架 |

---

> **来源**：
> - [Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052)，Stanford，2026
> - [AutoHarness: improving LLM agents by automatically synthesizing a code harness](https://arxiv.org/abs/2603.03329)，DeepMind，2026
