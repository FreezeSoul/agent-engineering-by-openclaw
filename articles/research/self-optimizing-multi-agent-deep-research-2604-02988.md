# Self-Optimizing Multi-Agent Deep Research：多智能体系统的自优化范式

> **本质**：Zeta Alpha 提出将 AlphaGo 的 self-play 思想引入 Deep Research 系统——让多个 Agent 通过探索不同 prompt 组合自动优化自身，匹配或超越专家手工设计的质量。为解决 DR 系统"prompt  brittle、模型迁移即失效"的顽疾提供了量化路径。属于演进路径 Stage 8（Deep Research）× Stage 9（Multi-Agent）的交叉创新。

## 一、基本概念

### 1.1 问题：手工设计 DR 系统的三大困境

当前主流 Deep Research 系统依赖专家手工设计系统 prompt 和固定架构，存在三层困境：

**第一层：脆弱性（Brittleness）**

一套 prompt 在某 LLM 上表现良好，换一个模型（甚至同一模型的不同版本）质量可能显著下降。每次模型更新都需要重新调优，属于高维护成本的手工劳动。

**第二层：领域绑定（Domain Binding）**

专家 prompt 通常针对特定领域优化，迁移到新领域（从金融到医疗）效果折损严重。

**第三层：过程黑箱（Process Opacity）**

手工设计的 prompt 是静态规则，无法解释系统为何在某类查询上失败，也难以系统性地改进。

### 1.2 核心思想：将 Self-Play 引入 DR

这篇论文的核心贡献是**将 AlphaGo/AlphaZero 的 self-play 思想迁移到多 Agent DR 系统**：

- 不是让人类专家设计固定的 orchestrator/reader/writer prompt
- 而是让系统**自动探索不同的 prompt 组合**，通过反馈信号（evaluation metrics）迭代优化
- 最终产出的 agent 配置能够**匹配或超越专家手工设计**

本质上是将 prompt 和多 Agent 协作策略视为"可优化的参数"，用 LLM 本身作为优化算子。

## 二、核心技术：多 Agent DR 架构与自优化方法

### 2.1 基线架构：四组件 DR 系统

论文采用的多 Agent DR 架构包含四个核心组件：

| 组件 | 职责 | 说明 |
|------|------|------|
| **Orchestrator** | 规划与协调 | 理解用户查询，制定研究计划，协调其他 Agent |
| **Reader** | 信息获取 | 发出搜索查询，浏览搜索结果，提取相关段落 |
| **Aggregator** | 综合整理 | 合并多个 Reader 的输出，去重，识别信息缺口 |
| **Writer** | 输出生成 | 基于综合结果撰写报告，管理引用 |

这个架构与当前主流 DR 产品（如 Perplexity、ChatGPT Deep Research、Gemini Deep Research）的设计高度一致，说明论文的问题具有普适性。

### 2.2 自优化方法：探索策略

论文探索了多种自优化方法，核心机制是**让 LLM 在"候选 prompt 组合"的搜索空间中探索**，并根据 evaluation metric（答案质量评分）进行选择。

论文提到了多种优化方法的探索：

- **Prompt Self-Play**：让多个 Agent 实例用不同 prompt 运行，对结果互相评估，保留最优配置
- **Evolutionary Exploration**：类似遗传算法，通过"变异+选择"迭代优化 prompt
- **Gradient-like Optimization**：类似 TextGrad，用反馈信号指导 prompt 调整方向

具体哪种方法最有效，需要参考论文的实验结果部分。

### 2.3 与 DSPy 的关系

手工设计 DR prompt 的问题，在业界已有相关探索。**DSPy**（ khattab2024dspy ）提出了用"signatures"和"compilers"替代手工 prompt 的思路，将 prompt 视为可编译、可优化的组件。

本文的 self-play 方法与 DSPy 的编译器思路有相似之处，但本文专注于**多 Agent 协作场景下**的优化，且将优化对象扩展到了整个 Agent 系统的架构配置，而不仅是单个 prompt。

## 三、实验发现

### 3.1 核心结论

论文报告的关键发现：

> **多 Agent 自优化系统能够匹配或超越专家手工设计的 DR 质量，且对模型更换更鲁棒。**

这意味着：
- 自动化优化可以降低手工调优成本
- 优化后的配置对模型迁移的适应性更好
- Self-play 发现的策略有时能超越人类专家的直觉

### 3.2 局限性

论文也坦诚了当前方法的局限：

- **计算成本**：Self-play 需要大量探索，计算资源消耗显著
- **评估指标依赖**：优化的质量上限取决于评估 metric 的设计
- **泛化边界**：在极端开放性问题上，自优化系统的表现仍不稳定

## 四、与其他概念的关系（按演进路径）

### Stage 8（Deep Research）中的位置

```
手工设计 DR Prompts → DSPy 编译优化 → Self-Play 自动优化
      (现状)              (中间态)           (本文)
```

- **手工设计**（现状）：依赖专家经验，brittle，难以迁移
- **DSPy 编译**（中间态）：用签名和编译器替代部分手工，但组件独立优化
- **Self-Play**（本文）：将整个多 Agent 系统视为可优化整体，组件协同进化

### Stage 9（Multi-Agent）中的位置

本文的四组件 DR 架构（Orchestrator/Reader/Aggregator/Writer）是**任务分工型多 Agent**的典型案例。自优化方法为这类架构提供了一个**自动发现最优协作策略**的路径，而不是靠人工配置。

## 五、实践启示

### 5.1 对 Agent 开发者的意义

1. **Prompt 即负债**：手工 prompt 是技术债，模型一变就可能失效。需要从架构层面考虑可优化性
2. **评测先行**：没有好的 evaluation metric，就没有 self-play 的基础。投资建设 DR 评测体系是前置条件
3. **多 Agent 协作策略可优化**：Agent 间的协调策略（谁负责规划、谁负责执行）不是固定的，是可以通过实验优化的

### 5.2 工程路径建议

对于想在自己的 DR 系统中引入自优化的团队：

1. **建立评测体系**：先有可量化的质量指标（如 RACE+FACT 框架）
2. **小范围试点**：先在单一领域、单一 LLM 上验证 self-play 效果
3. **关注计算成本**：探索空间过大会导致成本爆炸，需要设计有效的搜索剪枝策略

## 六、局限性 & 未来方向

| 方向 | 当前状态 | 未来机会 |
|------|---------|---------|
| 计算效率 | 高成本探索 | 近似优化、few-shot 引导 |
| 跨模型迁移 | 有一定迁移性 | 零样本跨模型优化 |
| 长尾问题 | 开放性问题不稳定 | 混合架构（自优化+规则） |
| 实时适应 | 离线优化 | 在线持续优化 |

## 七、参考文献

- Câmara, A., Slot, V., & Zavrel, J. (2026). *Self-Optimizing Multi-Agent Systems for Deep Research*. ECIR 2026 Workshop on Conversational Search for Complex Information Needs. arXiv:2604.02988
