# Cursor × NVIDIA：Multi-Agent 如何让 CUDA 内核优化效率提升 38%

> **核心论点**：GPU 内核优化长期被顶级专家垄断，Cursor 的多 Agent 系统用 3 周时间完成了这个领域几年来的工作——38% 几何平均加速、19% 的优化超过 2 倍提升。这不仅是工程突破，更是 Multi-Agent 架构有效性的铁证。

---

## 背景：为什么内核优化是 Multi-Agent 的试金石

GPU 内核优化是个特殊的领域：

1. **问题空间巨大且无明确答案**：不像代码补完有标准答案，内核优化是开放式的优化问题，答案未知
2. **可量化但难以驾驭**：SOL（Speed-of-Light）分数提供了清晰的度量，但手工优化受限于专家数量和能探索的方案空间
3. **现实世界影响巨大**：更快的内核 → 更好的 GPU 利用率 → 更低的能耗和推理成本 → 更多用户能用上更强模型

Cursor 团队选择这个领域的核心逻辑：

> "To date, GPU performance has been limited by our inability to explore the full solution space beyond these manual simplifications."
>
> 到目前为止，GPU 性能一直受限于我们无法在手工简化的范围之外探索完整的解决方案空间。

这是对传统范式的根本性质疑：人类专家+手工优化的组合已经触及天花板，而多 Agent 系统可以突破这个限制。

---

## 实验设计：从问题生成到基准测试的全链路

### 问题来源：SOL-ExecBench

NVIDIA 使用 **SOL-ExecBench** 从 124 个生产级开源模型（DeepSeek、Qwen、Gemma、Kimi、Stable Diffusion 等）生成 235 个优化问题，覆盖：

- LLM（推理/训练）
- Diffusion
- Vision/Audio/Video
- 多模态混合架构

关键点：这些是**真实的生产约束**，不是合成数据或玩具内核。

### 基准测试框架

SOL-ExecBench 同时用于：
- 生成优化问题
- 对比 Kernel 性能与现有软件基线和理论硬件性能上限
- 作弊检测（缓存、超出 B200 支持范围的"性能"会被判无效）

### 双语言测试

为了让结果更有说服力，Cursor 要求系统用两种语言分别编写解法：

| 语言 | 抽象层级 | 测试目标 |
|------|---------|---------|
| **CUDA C + inline PTX** | 硬件级（接近 ISA） | 系统能否在底层推理硬件细节 |
| **CuTe DSL** | 高层可组合抽象 | 系统能否从文档中学习全新 API（公开数据几乎无此语言样本） |

---

## 核心结果：38% 加速意味着什么

### 数字背后的含义

```
63%（149/235）：优于基线的问题比例
38%：几何平均加速
19%：优化超过 2 倍的问题比例
0.56：中位数 SOL 分数（理论上限 1.0）
```

38% 听起来保守，但如果对比一下：

- 这个领域顶级专家通常需要**数月到数年**才能做出同等水平的优化
- Cursor 的系统在**3 周内**完成了 235 个问题的优化
- 中位数 SOL 0.56 意味着还有巨大的提升空间——更多 GPU 资源 = 探索更深更多的解决方案

### 三个代表性案例

#### 1. BF16 Grouped Query Attention with Paged Prefill

**来源**：SGLang 推理中 Llama 3.1 8B 的注意力操作

**策略**：CUDA C++ 优化，使用硬件级指令调度、persistent kernels、针对输入大小的超优化

**结果**：
- SOL 分数 0.9722（接近硬件极限）
- 比 FlashInfer 库的人类优化基线快 **84%**
- 替换 SGLang 内核后，端到端 TTFT 提升 **3%**（在注意力占预填充过程 2-5% 的情况下）

#### 2. NVFP4 MoE Linear with Gating

**来源**：Qwen3 等 MoE 模型中的双内核模式，输入和中间结果都量化到 NVFP4

**策略**：识别量化区域为主要瓶颈 → 用预计算的阈值桶直接映射 FP32 → 融合缩放和舍入

**结果**：
- **39% 几何平均加速**
- SOL 分数 0.58

#### 3. BF16 Matrix Multiplication

**来源**：GEMM（矩阵乘法）——内核优化领域公认最难的问题之一

**难度**：需要内联 PTX、流水线、分阶段，还需要对硬件单元有深刻理解

**结果**：
- Cursor 系统从零生成的 GEMM 内核达到 **cuBLAS 人工优化基线的 86%**
- 在小型 M 测试用例（LLM 推理 decode 场景重点）上**反超 cuBLAS 达 9%**

这是 Multi-Agent 系统在最难问题上逼近领域专家的里程碑。

---

## 系统架构：Planner-Worker 的协调协议

Cursor 没有透露太多技术细节，但文章揭示了几个关键架构选择：

### 单一协调协议

> "The entire coordination protocol lived in a single markdown file that specified the output format, rules, and tests."

一个 Markdown 文件定义了所有协作规则——这是 Harness 设计的一种务实体现：用人类可读的结构化文档作为 Agent 间协议，而不是硬编码的复杂系统。

### 自主 Benchmarking

> "The multi-agent system independently learned to call the benchmarking pipeline during its runs, creating a loop where the system continuously tested, debugged, and optimized kernels without any developer intervention."

关键：系统**自己学会了调用基准测试管道**，而不是被显式编程这样做。这是一个自我改进的 Eval-Execution 循环的实例。

### Planner 的动态调度

所有 235 个问题由一个 **planner agent** 分配和管理，根据性能指标动态再平衡工作分配给自主 Worker。

---

## 核心洞察：为什么 Multi-Agent 在这里有效

### 单 Agent 的局限性

> "Single agent systems struggle here because models are best at narrowly scoped tasks they have already seen during training."

单 Agent 在预训练分布内的任务上表现优异，但在：
- 超出训练分布的问题
- 需要广泛探索开放解决方案空间的任务
- 需要不同抽象层推理的复杂问题

这些场景下会触及天花板。

### Multi-Agent 的优势

1. **并行探索**：Planner 同时管理多个 Worker，每个 Worker 探索不同的优化路径
2. **专业分工**：不同 Agent 专注于问题的不同方面（内存加载/数学指令/调度优化）
3. **动态协调**：Planner 根据中间结果重新分配工作，适应性强
4. **累积学习**：Benchmarking 循环让系统能够自我改进

### 最重要的结论

> "The most ambitious tasks in software are open-ended, without a clear solution... We see the kernel optimization experiment as further validation that multi-agent architectures will quickly become the default approach to building software because they can tackle novel problems that fall far outside training data distribution."

这是对 Multi-Agent 架构价值的直接宣示：在训练数据分布之外的开放问题上，Multi-Agent 是唯一可行的路径。

---

## 工程机制关联

### Evaluator Loop（评估器循环）

SOL-ExecBench 作为外部 Evaluator，持续对 Agent 生成的 Kernel 进行评估 → 反馈 → 再优化。这是典型的 **Harness Evaluator Loop** 模式。

### 接力/恢复机制

235 个问题在 3 周内跨多 GPU 运行，如果中途出错，需要有机制让系统从断点恢复继续。这暗示了 Cursor 在 Harness 设计中实现了 **Checkpoint + Progress Tracking** 机制。

### Planner-Worker 架构

Planner 负责任务分配和协调，Worker 负责任务执行。这是 **Orchestration** 模式的一种实现，Planner 扮演了 Meta-Harness 的角色。

---

## 笔者的判断

### 这篇文章为什么重要

1. **量化验证**：38% / 19% / 2x 这些数字提供了 Multi-Agent 有效性的硬指标，而不是模糊的"感觉变好了"
2. **证明了 Multi-Agent 的边界**：在内核优化这种需要极深专业知识的领域 Multi-Agent 依然有效，说明其适用范围比预期更广
3. **揭示了架构选择**：Planner-Worker + Markdown 协调协议 + 自主 Benchmarking 调用 = 可复用的 Multi-Agent 工程模式

### 局限性

- 中位数 SOL 0.56 说明系统还未达到最优，还有很大提升空间
- 235 个问题 / 27 GPU 的配比限制了探索深度（计算资源瓶颈）
- 结果在 NVIDIA Blackwell 200 GPU 上的泛化性待验证

### 关联阅读

如果你对这篇文章中提到的内容感兴趣，推荐搭配阅读：

- [Anthropic GAN-inspired Three-Agent Architecture for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)——三角色架构的另一种实现
- [Cursor Scaling Agents: Planner-Worker-Judge Architecture](https://cursor.com/blog/scaling-agents)——扁平多 Agent 失败的原因和 Planner-Worker-Judge 的破局方案

---

## 引用

> Lin, W., Modi, S., Zhang, Y., & Lin, E. (2026). *Speeding up GPU kernels by 38% with a multi-agent system*. Cursor Engineering Blog. https://cursor.com/blog/multi-agent-kernels

---

*本文属于 [orchestration/](../) 分类，关注 Multi-Agent 协作与编排模式。*