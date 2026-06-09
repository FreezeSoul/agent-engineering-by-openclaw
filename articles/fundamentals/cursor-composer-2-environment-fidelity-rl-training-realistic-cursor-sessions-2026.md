# Cursor Composer 2 环境忠诚度：RL 训练为何要在真实编码会话中进行

> **核心论点**：Coding Agent 的能力上限，不取决于模型参数规模，而取决于**训练环境与部署环境的等价程度**。Cursor Composer 2 的技术报告揭示了一个反直觉的结论：用真实 Cursor 会话训练，比用任何公开 benchmark 训练，效果都好出一个数量级。

> **一手来源**：[Cursor Blog — A technical report on Composer 2](https://cursor.com/blog/composer-2-technical-report)（Sasha Rush，2026-03-27）

---

## 一、问题的起点：Benchmark 不等于真实工作

构建 coding 模型的人都知道一个痛点：公开 benchmark 上的高分，往往不等于实际使用中的好体验。

Cursor 团队在报告中直接点出了这个问题：

> "A core challenge in building coding models is that public benchmarks often don't reflect the work developers actually do. Tasks are over-specified, solutions are narrow, and the codebases are small."

这是 engineering 层面的实话。SWE-bench 的代码库太小，HumanEval 的任务太独立，真实开发者面临的是跨越多个文件、依赖模糊、需求不完整的复杂情境。模型在这些 benchmark 上学到的「解题能力」，无法迁移到真实的 12.5M 行代码库（如 Rakuten 在 vLLM 上的测试案例）。

**笔者认为**：Benchmark 的问题不只是「太简单」，而是「反馈信号失真」——模型在 benchmark 上优化的是「如何解这道题」，而不是「如何在真实工作中找到正确的题」。

---

## 二、Composer 2 的训练哲学：同构训练

Composer 2 的训练分为两个阶段：

### 阶段一：持续预训练（Continued Pretraining）

基于 Kimi K2.5（开源基础模型），在代码密集的数据混合上进行持续预训练。Cursor 的发现是：

> "reducing pretraining loss improves downstream RL performance, with better base knowledge reliably translating into a better agent."

这与一些「跳过预训练、直接上 RL」的激进路线相反。Cursor 选择先夯实基础，再上 RL。基础不牢，RL 的上限也高不了。

### 阶段二：大规模强化学习（RL）

这是关键所在。Composer 2 的 RL 训练发生在**真实的 Cursor 会话**中：

> "Composer 2 RL training occurs in realistic Cursor sessions with the same tools and harness the deployed model uses, applied to a problem distribution that reflects the full range of what developers ask Composer to do."

不是模拟环境，不是 API 调用的日志，是真正的 Cursor IDE——包括 Agent 的工具链（代码补全、搜索、重写）、用户交互模式、以及 Agent 感知到的完整 harness。

这意味着训练时的反馈信号，与用户实际使用时的反馈信号，是**同构**的。

---

## 三、环境忠诚度（Environment Fidelity）的工程实现

「在真实会话中训练」说起来简单，工程上却需要一套完整的基础设施。Cursor 披露了三个关键组件：

### 3.1 Anyrun：百万级沙箱编码环境

Cursor 训练时需要同时运行「数十万个」沙箱编码环境，每个环境都是真实的代码编辑上下文（而非轻量模拟）。这是 Anyrun 的核心职责：

- **并发规模**：支持数十万量级的并行沙箱实例
- **环境隔离**：每个 Agent 的操作不会互相干扰
- **状态捕获**：记录完整的工具调用序列、文件变更、错误状态

**笔者认为**：Anyrun 的本质，是把「真实 Cursor IDE」做成了一个可大规模复制的训练基础设施。这不是简单的 sandboxing，而是把 IDE 变成了一个 RL 环境。

### 3.2 自定义低精度内核（Custom Low-Precision Kernels）

Composer 2 是 MoE（混合专家）模型，训练在 Blackwell GPU 上进行。Cursor 为此开发了自定义的低精度计算内核，以高效支持 MoE 的大规模并行计算。

这与模型架构选择直接相关——MoE 能在保持高质量的同时降低推理成本，但对训练基础设施的要求更高。

### 3.3 异步 RL 管道（Fully Asynchronous RL Pipeline）

跨多区域的完全异步 RL 管道。训练数据生成（Agent 在沙箱中产生轨迹）与模型权重更新是解耦的——不需要等所有环境跑完才能更新模型，实现高 GPU 利用率。

---

## 四、RL 训练的实际效果：平均与最优双提升

Cursor 报告的一个关键发现是：

> "RL training improves both average and best-of-K performance, suggesting the model is learning new solution paths rather than just concentrating on known ones."

这意味着 RL 训练不仅让 Composer 2 在典型任务上做得更好，还让它在难题上有更多「灵光一现」的时刻——学到了新的解决路径，而非把答案压缩到少数几条常见路线上。

**笔者认为**：这对 AI Coding 工具的开发者是一个重要提醒：如果 Agent 只能在你预期的问题上做得好，那它本质上是一个「记住了解题步骤的模型」，而不是一个真正能处理未知问题的 coding partner。

---

## 五、Agent 行为塑造（Agent Behavior Shaping）

报告中提到了「agent behavior shaping」这一维度，但没有详细展开技术细节。这是 RL 训练中的核心挑战之一：

- 如何让 Agent 在长时间运行的复杂任务中保持正确的方向感？
- 如何平衡「探索新方案」和「执行已知有效路径」？
- 如何处理 Agent 在工具调用失败后的恢复行为？

从 `cursor.com/blog/composer-2-5`（2026-05-18）补充信息来看，Cursor 在 Composer 2.5 中使用了**特征删除（Feature Deletion）**合成任务方法：给 Agent 一个包含完整测试套件的代码库，要求删除部分代码使得特定功能消失但代码库仍可运行，然后 Agent 需要重新实现被删除的功能。这本质上是在训练 Agent 的**代码理解与重构能力**——而非单纯的功能实现能力。

**这与 RL 训练环境忠诚度是同一个工程思想的两面**：训练任务设计得越接近真实情境，Agent 学到的能力越能迁移到实际工作中。

---

## 六、与 OpenAI Harness Engineering 的对比

值得注意的是，OpenAI 的 [Harness Engineering](https://openai.com/index/harness-engineering) 也在强调「Repository as System of Record」——把仓库代码、文档、execution plans 作为 Agent 的知识来源和行动依据。

两篇文章在核心思想上形成了呼应：

| 维度 | Cursor Composer 2 | OpenAI Harness Engineering |
|------|-------------------|---------------------------|
| **核心主题** | 训练环境 = 部署环境 | 知识存储 = 仓库本身 |
| **关键机制** | Anyrun 沙箱 + RL | Progress logs + Execution plans |
| **Agent 视角** | 训练时感知到的就是生产时的一切 | 仓库里的知识才能被 Agent 访问 |
| **共同结论** | **环境忠诚度决定能力上限** | **知识忠诚度决定行动质量** |

**笔者的判断**：两条路线都在说同一件事——Coding Agent 的能力瓶颈，不是模型不够大，而是「训练/运行时环境」与「真实工作环境」之间的 fidelity gap。Cursor 解决的是训练侧，OpenAI 解决的是知识侧。

---

## 七、CursorBench：重新定义 coding 模型评估

为了克服公开 benchmark 的局限性，Cursor 构建了自己的评估套件 CursorBench。这个评估体系的核心设计原则是：

- **任务来自真实开发场景**，而非人工构造的简化问题
- **代码库规模与真实项目相当**，而非小型独立文件
- **解决方案不唯一**，允许 Agent 用不同路径达到目标

> "A core challenge in building coding models is that public benchmarks often don't reflect the work developers actually do."

CursorBench 的存在，本身就是「环境忠诚度」思想的延伸——评估环境也要忠实于真实工作情境。

---

## 八、工程启示

### 核心结论

**训练环境的等价程度，是 coding agent 从「玩具」走向「生产力」的关键变量。**

Cursor 的实践证明：
1. 用真实 Cursor 会话训练 > 用 benchmark 训练
2. 预训练基础扎实 → RL 效果更好
3. RL 提升平均性能和最优性能（而非仅优化均值）
4. 评估体系本身也需要「环境忠诚度」

### 实践建议

对于构建内部 coding agent 或 AI coding 工具的团队：

1. **评估优先**：先建立能反映真实工作场景的评估集，而非依赖公开 benchmark
2. **训练环境匹配**：如果 agent 在沙箱中运行，训练时就要用同样的沙箱环境
3. **工具链一致性**：训练时 Agent 使用的工具接口，必须与生产时完全一致
4. **合成数据设计**：用「特征删除」「需求重构」等方法设计训练任务，而非单纯收集成功轨迹

### 已知局限

报告没有详细披露：
- CursorBench 的具体评估指标和数据来源
- Anyrun 的具体架构和容错机制
- RL 训练中的 reward shaping 策略细节

这些是 arXiv 完整技术报告覆盖的内容，值得进一步研究。

---

## 参考文献

1. Sasha Rush, "A technical report on Composer 2", *Cursor Blog*, March 27, 2026. https://cursor.com/blog/composer-2-technical-report
2. Cursor Team, "Introducing Composer 2.5", *Cursor Blog*, May 18, 2026. https://cursor.com/blog/composer-2-5
3. OpenAI Engineering, "Harness engineering: leveraging Codex in an agent-first world", *OpenAI Index*, February 11, 2026. https://openai.com/index/harness-engineering
4. Anthropic, "2026 Agentic Coding Trends Report", *Anthropic Resources*, 2026. https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf