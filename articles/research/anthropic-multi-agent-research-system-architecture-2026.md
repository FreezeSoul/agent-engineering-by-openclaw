# Anthropic 多 Agent 研究系统架构：Lead Agent + Subagent 并行架构的工程实践

## 核心论点

Anthropic 的 Claude Research 功能采用「Lead Agent 协调 + Subagent 并行执行」的架构，在开放性研究任务上比单 Agent 强 90.2%。这篇博客揭示了多 Agent 系统的核心工程洞察：**Token 用量是性能的主要驱动因素**（解释 80% 方差），而多 Agent 架构本质上是一种**横向扩展 Token 预算**的工程手段。

## 背景：为什么研究任务需要多 Agent

研究工作的本质是**开放性压缩**——从海量信息中提炼洞见。这类任务有两个关键特征：

1. **过程不可预测**：无法预先定义固定路径，必须根据中间发现动态调整方向
2. **上下文窗口容易溢出**：深度研究涉及数百次工具调用，单一上下文窗口装不下

Anthropic 的实验数据揭示了一个反直觉的结论：

> 在 BrowseComp 评测（测试 Agent 定位稀有信息的能力）中，**Token 用量单独解释了 80% 的性能方差**，工具调用次数和模型选择是另外两个解释因素。

这意味着，对于需要深度探索的研究任务，**增加 Token 投入是提升性能最直接的杠杆**。而多 Agent 架构正是横向扩展 Token 预算的手段——每个 Subagent 拥有独立的上下文窗口，可以并行探索不同方向，最后将压缩后的发现汇报给 Lead Agent。

## 架构设计：Lead Agent + Subagent 模式

Claude Research 的架构采用标准的 **Orchestrator-Worker 模式**：

- **Lead Agent**：负责任务规划、方向调度和结果整合
- **Subagent**：在独立上下文中并行执行专项搜索，返回压缩后的发现

```
User Query
    ↓
Lead Agent（规划 + 协调）
    ↓ [并行分发]
Subagent A → 独立上下文窗口 → 搜索方向 A
Subagent B → 独立上下文窗口 → 搜索方向 B  
Subagent C → 独立上下文窗口 → 搜索方向 C
    ↓ [结果压缩汇报]
Lead Agent 整合 → 最终答案
```

关键设计决策：**Subagent 的输出直接写文件系统，而非通过 Lead Agent 中转**。这避免了多级传递带来的信息损失（Anthropic 称之为「传话游戏」问题）。

## 性能数据

| 配置 | 相对性能 |
|------|---------|
| 单 Agent Claude Opus 4 | 基准 |
| **Multi-Agent（Opus 4 Lead + Sonnet 4 Subagents）** | **+90.2%** |

多 Agent 系统在「广度优先」查询（需要同时追踪多个独立方向）上优势明显。例如，要求列出标普 500 信息技术板块所有公司的董事会成员时，单 Agent 因顺序搜索而失败，多 Agent 则通过并行子任务成功。

## Token 经济学

| 类型 | Token 相对用量 |
|------|--------------|
| 普通对话 | 1× |
| 单 Agent（chat 模式） | ~4× |
| 多 Agent 研究系统 | ~15× |

多 Agent 系统的 Token 投入是普通对话的 15 倍。因此该架构适用于**任务价值足够高**的场景——Research 功能帮助用户发现了此前未曾考虑的商业机会、复杂的医疗方案、棘手的技术问题，节省了数天工作量。

不适用的场景：需要所有 Agent 共享同一上下文、Agent 间存在大量依赖的编码任务（目前 LLM Agent 在实时协调和委托方面仍不成熟）。

## 工程挑战与解决方案

### 1. 评估：最终状态评估法

对于**跨多轮修改持久状态的 Agent**，传统的过程追踪评估方法失效。Anthropic 的解法是**最终状态评估**——不评判 Agent 是否遵循了某个特定过程，而是评判它是否达到了正确的最终状态。

对于复杂工作流，进一步拆分为离散的检查点，在特定检查点验证状态是否按预期变化，而非试图验证每一个中间步骤。

### 2. 长程对话管理

生产级 Agent 经常涉及数百轮对话。标准上下文窗口很快不够用。Anthropic 的应对策略：

- **分阶段摘要**：Agent 在进入新阶段前，总结已完成工作并将关键信息存入外部记忆
- **上下文接近上限时的 Subagent 刷新**：在上下文耗尽前，生成新的 Subagent（干净上下文），通过外部记忆恢复之前状态

### 3. 最小化「传话游戏」

Subagent 的原始输出直接进入人工产物系统（Artifact），而非全部经过 Lead Agent 中转。这带来了两个好处：

- **保真度**：避免了 Lead Agent 在中转时的信息损失
- **性能**：减少了将大输出拷贝进对话历史的 Token 开销

## 关键洞察：Token 是核心杠杆

Anthropic 的数据揭示了一个关于 LLM Agent 能力的根本性洞察：

> **Token 用量解释了 80% 的性能方差。**

这意味着当前 LLM Agent 的能力边界在很大程度上是**上下文窗口和推理预算的边界**。多 Agent 架构之所以有效，不是因为它带来了某种「群体智能」，而是因为它通过并行的独立上下文窗口，**有效增加了总 Token 投入量**。

从工程角度看，这意味着 Agent 系统设计的核心杠杆是：
1. **最大化有效 Token 用量**（而非单纯增加步数）
2. **减少 Token 浪费**（无关上下文、重复推理）
3. **按需扩展**（为高价值任务分配更多 Token 预算）

## 引用来源

- 「How we built our multi-agent research system」，Anthropic Engineering Blog，2025年6月13日：https://www.anthropic.com/engineering/multi-agent-research-system
- BrowseComp 评测：OpenAI 研究，https://openai.com/index/browsecomp/
