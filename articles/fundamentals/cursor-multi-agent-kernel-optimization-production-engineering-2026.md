# Multi-Agent 系统从研究演示走向生产工程：CUDA 内核优化的 38% 加速意味着什么

> **这篇文章要回答的核心问题**：当一个 multi-agent 系统能在 3 周内解决需要顶级专家数月才能完成的 CUDA 内核优化问题时，multi-agent 系统在工程意义上的定位发生了什么变化？

## 从研究演示到生产工程工具

长期以来，multi-agent 系统给人的印象是"技术演示"——能跑 demo，但离生产级工程问题还有距离。Cursor 和 NVIDIA 合作的 CUDA 内核优化项目可能改变了这个认知。

这个项目用 multi-agent 系统处理了 235 个真实的 GPU 内核优化问题，来自 DeepSeek、Qwen、Gemma、Kimi、Stable Diffusion 等 124 个生产模型。3 周时间，38% 的几何平均加速，其中 19% 的优化超过 2 倍。

这不是在玩具数据集上跑 benchmark。这是真实的生产环境约束，问题是真实的，目标是追赶甚至超越人类专家的优化水平。

**笔者判断**：multi-agent 系统正在从「能做什么」转向「能稳定地做好什么」。CUDA 内核优化是一个特别硬的标尺——它需要硬件级别的推理能力、跨抽象层的工作能力（从 CUDA C 到 PTX 汇编），以及长时间自主运行的能力。这三个条件同时满足，才意味着 multi-agent 真正进入了生产工程工具的范畴。

## 为什么这个案例值得深挖

### 内核优化是multi-agent能力的硬测试

CUDA 内核优化是一个出了名的难题。传统的优化流程是：工程师把模型分解为单个数学操作，逐个调优。这个方法有效，但存在天花板——分块优化无法捕捉跨操作的整体优化空间。

更重要的是，这是一个**不知道正确答案**的问题。Cursor 团队选择这个领域的逻辑很清晰：给 multi-agent 系统一个开放式的优化问题，连他们自己都不知道最优解在哪里。如果系统能跑出来结果且真实有效，那才是真正的能力证明。

原文描述了这个实验的严谨性：

> "We also used SOL-ExecBench to benchmark multi-agent kernel solutions on 27 NVIDIA Blackwell 200 GPUs. SOL-ExecBench is an effective evaluator that compares kernel performance against existing software baselines and theoretical hardware performance limits. If agents use cheating tactics like caching and deliver performance beyond what a B200 can support, the pipeline invalidates the result."

防作弊设计是这类评测的关键。没有这个机制，结果的可信度会大打折扣。

### 跨越GPU抽象层的自主推理

实验的一个亮点是系统能够自主处理不同层次的 GPU 抽象：

- **CUDA C + 内联 PTX**：直接操作寄存器和 ISA 级别指令，要求系统理解硬件最底层
- **CuTe DSL**：高级可组合抽象，在公开训练数据中几乎不存在，要求系统从提供的文档中自学新 API

两个语言、两套抽象层、完全自主学习、没有人类介入干预。这是 multi-agent 系统适应能力的硬指标。

**笔者认为**：真正值得关注的不是 38% 这个数字本身，而是系统能在「跨越抽象层」这个维度上保持有效。当人类专家需要多年积累才能同时驾驭 CUDA C 和 PTX 时，一个 multi-agent 系统用 3 周做到了，这说明 agent 的学习能力已经超出了我们对「模仿式 AI」的预期。

## 解耦架构：Multi-Agent 的生产工程设计模式

这个项目的架构值得单独分析。系统的核心协调协议只在一个 markdown 文件里，规定了输出格式、规则和测试。benchmark 管道在运行过程中被系统自动调用，形成了一个持续的「测试→调试→优化」循环。

这不是一个预设工作流的执行，而是一个**自主发现并解决问题的系统**。

原文描述：

> "The entire coordination protocol lived in a single markdown file that specified the output format, rules, and tests. The multi-agent system independently learned to call the benchmarking pipeline during its runs, creating a loop where the system continuously tested, debugged, and optimized kernels without any developer intervention."

这种「单文件协议 + 自主循环」的设计模式，在生产工程中有重要价值：规则是可读的、可版本化的、可审计的——同时系统的行为是自主的、不需要人类介入每个决策点。

**笔者判断**：这可能是未来 multi-agent 生产系统的标准架构形态。不是预设一个复杂的工作流，而是用自然语言协议描述目标约束，让系统在约束内自主探索。把「怎么做」的决策权还给 agent，把「做什么」的边界留给人类工程师。

## 三个具体案例：系统如何自主找到不同的优化策略

### BF16 Grouped Query Attention + Paged Prefill

这是一个常见的 LLM 推理阶段的 prompt 优化问题。系统使用了 CUDA C++ 优化，采用了：
- 针对内存加载和数学运算的特定硬件指令
- 通过 persistent kernels 改进调度
- 针对输入尺寸的超优化

结果是 SOL 得分 0.9722（非常接近硬件极限），相比 FlashInfer 的人类优化基线，84% 几何平均加速。在 SGLang 中替换该内核后，Llama 3.1 8B 的首 token 时间（TTFT）提升了 3%。

### NVFP4 MoE Linear with Gating

混合专家模型中常见的两内核模式，但输入张量和中间乘法输出被量化到了 NVFP4（4-bit 浮点）。

系统正确识别量化区域是主要瓶颈，然后做了融合优化：把缩放计算和取整合并，而不是先缩放再取整。原因是 NVFP4 只有 16 个可能的值，可以直接用预计算的阈值桶将 FP32 值映射到 FP4 编码。

39% 几何平均加速，SOL 0.58。

### BF16 Matrix Multiplication

GEMM（通用矩阵乘法）是最难的优化问题之一。完全高效的 GEMM 需要内联 PTX（类似汇编语言）、流水线和对齐分级。历史上这是高度专业化的内核工程师的地盘。

Multi-agent 系统从零生成专门的 CUDA C++ GEMM 内核，达到了 NVIDIA cuBLAS 精心调优基线的 86%。在小矩阵测试用例上（这对 LLM 推理解码特别重要），系统甚至超过了库的实现，最多达到 9% 的领先。

**笔者认为**：这三个案例的共同点是：系统在每种情况下都自主发现了一个**与问题特性匹配**的优化策略，而不是套用一个通用模板。这意味着规划 agent 真正理解了「不同问题需要不同方法」这个工程直觉，并将其转化为了可执行的工作分配决策。

## 局限性：哪些问题还没有解决

坦诚地说，这个系统也有明显的局限：

1. **中位数 SOL 得分仍然只有 0.56**，距离硬件极限还有很大空间
2. **只有 63% 的问题超越了基线**，意味着有 37% 的问题系统处理得不够好
3. 需要大量计算资源（235 个问题并行处理 3 周）

原文的态度很诚实：

> "We believe that multi-agent solutions can be vastly improved with more compute, as we had hundreds of GPUs available for this work but were limited by agent-hours."

**笔者认为**：这不是弱点，这是这个阶段的正常状态。值得注意的关键是：这些问题是「之前认为不适合自动化的问题」，现在已经在被攻克了。当 63% 的问题能被 multi-agent 超越基线时，这个比例会随着工程改进继续上升。

## Multi-Agent 系统正在成为平台化工具

这个项目的另一个意义是：Cursor 把 multi-agent 系统从一个研究项目变成一个**可复用的优化平台**。同样的系统架构、同样的协调协议，可以处理不同领域的复杂优化问题。

原文提到：

> "Over the past few months, we've been developing a multi-agent system that can build, maintain, and deploy complex software autonomously. As part of that work, we've been testing the system in a variety of domains, including having it build a browser from scratch and solve a research-level math problem on the First Proof benchmark."

这是关键认知：当 multi-agent 系统能够自主发现问题和优化方向时，它的价值不是「替代某个特定工作」，而是**成为组织的基础设施能力**——一种可以跨领域部署的计算资源。

**笔者判断**：接下来 1-2 年，会看到更多这类案例。Multi-agent 系统会进入需要长时间自主决策的领域：芯片设计、系统优化、科学计算。人类专家的角色会从「执行优化」转向「定义问题边界和评估约束」。

## 引用来源

- Cursor Blog: "Speeding up GPU kernels by 38% with a multi-agent system" — https://cursor.com/blog/multi-agent-kernels
- GitHub: "anysphere/kernel-optimization-results" — https://github.com/anysphere/kernel-optimization-results