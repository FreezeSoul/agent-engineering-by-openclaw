# 多 Agent 系统解决硬核工程问题：三次实践的深度解析

## 核心观察

2026 年，三个顶级 AI 团队（Anthropic、Cursor、Meta）都在用多 Agent 系统解决超出单 Agent 能力上限的工程问题。

这是偶然的吗？不是。这是 AI 工程化的关键信号——当问题足够难，单个 Agent 的能力有上限，多 Agent 协作是突破这个上限的正确路径。

## 三个案例的共同模式

### Anthropic：Harness 架构做能力扩展

Anthropic 的方法论是构建更好的 Agent Harness（框架），而不是让单个 Agent 更强。

核心思路：给 Agent 提供更好的工具、更好的上下文管理、更好的评估体系。Agent 的能力来自于它所处的系统，而不只是模型本身。

代表成果：Claude Code 的长期运行 Agent（weeks 级）、多窗口架构、Skills 系统。

### Cursor：扁平并行搜索

Cursor 的方法是 Planner + 多 Workers 并行。

> "The multi-agent system solved all 235 GPU kernel optimization problems in a single run by deploying a planner agent that distributed and rebalanced work across autonomous workers."

关键设计：一个 Markdown 文件定义协作规则，Planner Agent 负责任务分配和负载均衡，Workers 独立执行自己子任务。

**成果**：3 周内解决 235 个 CUDA Kernel 优化问题，38% geomean 加速，19% 的优化超过 2x 加速。这个速度通常需要资深 kernel 工程师数月的工作。

### Meta：分层专业分工 + 硬件反馈

Meta 的方法是更复杂的分层架构，每个 Agent 有明确的专门职责。

```
ProfilerAgent → DiagnoseAgent → AnalyzerAgent → OrchestratorAgent → OptimizationManager → BenchmarkAgent
```

不是扁平并行，而是流水线式的专业分工。每个 Agent 专注于一个具体阶段，通过共享记忆协调。

**成果**：2.02x 超越上一代，1.56x vs torch.compile 默认值，H100 上达到 89% roofline efficiency。

## 三种架构的本质对比

| 维度 | Anthropic Harness | Cursor Planner+Workers | Meta 分层流水线 |
|------|------------------|------------------------|----------------|
| **设计哲学** | 扩展 Agent 能力边界 | 并行探索解空间 | 专业分工流水线 |
| **任务分配** | Agent + 工具/上下文 | Planner 动态分配 | 固定阶段分工 |
| **通信机制** | 共享上下文窗口 | 单个 Markdown 协调文档 | 结构化输出传递 |
| **容错方式** | Agent 自主重试 | Workers 独立探索 | 并行 Beam Search |
| **学习机制** | 评估体系驱动 | 无（每次重新搜索）| Reflexion 历史反馈 |
| **适用场景** | 开放性长任务 | 大量独立子任务 | 诊断驱动的优化 |

## 关键洞察

### 1. 多 Agent 的核心价值是突破单 Agent 的能力上限

> "The most ambitious tasks in software are open-ended, without a clear solution. Single agent systems struggle here because models are best at narrowly scoped tasks they have seen during training."

单个模型再强，也有它没见过的任务。多 Agent 系统通过协作可以探索单个 Agent 探索不了的解空间。

### 2. 任务分解方式决定架构形态

**独立子任务** → Cursor 的扁平并行（每个 Worker 独立解决一个问题）

**渐进式优化** → Meta 的分层流水线（每个阶段依赖上一个阶段的输出）

**开放性探索** → Anthropic 的 Harness（给 Agent 更强的工具和上下文）

### 3. 协作规则是关键工程问题

三个系统都在解决同一个问题：Agent 之间如何协调？

- Cursor 用一个 Markdown 文件定义协作协议
- Meta 用结构化输出和共享记忆传递状态
- Anthropic 用工具和上下文的精心设计减少协调需求

### 4. 多 Agent 系统已经开始替代专家级人工

38% 加速、2x 加速、3 周完成原本需要数月的工作——这不是在demo，这是已经发生的生产级成果。

> "These levels of performance improvement are typically only found through months or years of work from highly experienced kernel engineers. The multi-agent system accomplished it in weeks."

## 工程启示

**如果你要构建多 Agent 系统，先想清楚你的任务属于哪一类**：

1. **大量独立子任务** → 扁平并行，参考 Cursor
2. **诊断驱动的迭代优化** → 分层流水线，参考 Meta
3. **开放性长任务** → 强化 Harness，参考 Anthropic

**不要过度设计**：Cursor 的成功部分来自极简的协调机制——只有一个 Markdown 文件定义规则。这比复杂的 Agent 间通信协议更实用。

**衡量真正的价值**：多 Agent 系统的价值不只是「更快」，而是「解决原本不可能解决的问题」。Cursor 的 235 个 kernel 优化问题，传统的工程师团队不可能在 3 周内全部解决。

## 一手资料

- [Cursor Multi-Agent Kernels Blog](https://cursor.com/blog/multi-agent-kernels)
- [PyTorch Blog: KernelAgent](https://pytorch.org/blog/kernelagent-hardware-guided-gpu-kernel-optimization-via-multi-agent-orchestration/)
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering)
