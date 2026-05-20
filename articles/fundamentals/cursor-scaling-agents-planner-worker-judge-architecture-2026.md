# Cursor 如何用 Planner-Worker-Judge 三角色架构突破多Agent扩展瓶颈

> 本文深度解读 Cursor 最新的多Agent编排研究成果，核心观点：**当数百个Agent并行协作时，扁平结构的锁竞争是性能杀手，而 Planner-Worker-Judge 三角色分离才是扩展关键。**

---

## 一、问题：扁平多Agent协作为何走向崩溃

Cursor 团队在探索让Coding Agent长时间自主运行时，遇到了一个直觉上不那么显然的瓶颈：**多Agent不是人越多越好**。

他们的第一反应是让Agent动态协作——共享一个文件，每个Agent检查谁在做什么、认领任务、更新状态。为了防止两个Agent抢同一个任务，他们加了锁机制。

结果很有意思：

- Agent持有锁的时间太长，甚至忘记释放。即便是锁正常工作，20个Agent也会慢到只有2-3个的有效吞吐量，大部分时间在等锁。
- 系统脆弱：Agent可能在持有锁时失败、重复申请已持有的锁，或者根本不申请锁就写入状态。

换成乐观并发控制（读自由，写失败检测）后更健壮了一些，但问题更深层：**没有层级结构时，Agent变得风险规避**——它们回避困难任务，只做小的、安全的改动。没有人对硬问题负责，也没有人对端到端实现负责。结果是长时间空转，没有实际进展。

这才是多Agent协作真正的墙：**不是协调的技术难题，而是激励结构的设计问题**。

---

## 二、破局：三角色分离架构

Cursor的解决方案是**角色分离**——不是所有Agent做所有事，而是建立职责流水线：

> "Instead of a flat structure where every agent does everything, we created a pipeline with distinct responsibilities."
> — Cursor Engineering, [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)

三个角色的分工：

| 角色 | 职责 | 特点 |
|------|------|------|
| **Planner** | 持续探索代码库，创建任务；可派生子Planner实现并行规划 | 负责"做什么"，理解全局 |
| **Worker** | 认领任务后专注完成，不与其他Worker协调，不操心全局 | 负责"怎么做"，线性执行 |
| **Judge** | 每个周期结束时判断是否继续，决定下一轮迭代 | 负责"何时停"，控制节奏 |

> "At the end of each cycle, a judge agent determined whether to continue, then the next iteration would start fresh. This solved most of our coordination problems and let us scale to very large projects without any single agent getting tunnel vision."
> — Cursor Engineering, [Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)

这个设计解决了三个核心问题：

1. **锁竞争消失**：Worker之间不需要通信，各自独立执行
2. **硬问题有人负责**：Planner感知全局，不会让困难任务被回避
3. **防止漂移**：Judge定期评估，阻止无进展的无限循环

---

## 三、验证：用一周时间从零写出一个浏览器引擎

为了压测这个系统，Cursor设了一个极端目标：**从零开始构建一个完整的Web浏览器**。

结果：
- 运行近**一周**
- 写出了**100万行代码**，跨越**1000个文件**
- 数百个Worker并发推送同一分支，**冲突极少**
- 新Agent仍能理解代码库并做出有意义的推进

> "You can explore the source code on GitHub." — 仓库地址 [wilsonzlin/fastrender](https://github.com/wilsonzlin/fastrender)

浏览器引擎 FastRender 由 Rust 编写，解析HTML/CSS、计算样式、执行布局、绘制像素。包含桌面浏览器外壳和嵌入式JS引擎执行。这不是玩具代码，是生产级别的渲染引擎，遵循HTML5、CSS Selectors 4、CSS Flexbox/Grid等规范。

这个结果证明了两件事：

1. **线性扩展是真实的**：系统能同时容纳数百个Agent，而不需要重新设计分布式协调原语
2. **架构决策比Agent能力更重要**：系统设计正确时，即使用的是同一批模型，也能在复杂任务上持续推进

---

## 四、另一个极端：GPU Kernel优化的38%加速

在另一个实验里，Cursor与NVIDIA合作，用同样的多Agent架构在**3周内**完成了一个通常需要**高级工程师数月甚至数年**才能完成的任务：优化235个CUDA Kernel。

实验设计：
- **Planner Agent** 将任务分配给Worker，并根据性能指标动态重新平衡工作负载
- 整个协调协议存在于**一个Markdown文件中**（定义了输出格式、规则和测试）
- 多Agent系统在学习过程中**独立调用NVIDIA的SOL-ExecBench基准测试管道**，形成自动化的"测试-调试-优化"循环，全程无人干预

结果：

| 指标 | 数值 |
|------|------|
| 超越基线的Kernel数量 | 149/235 (63%) |
| 几何平均加速比 | **38%** |
| 加速超过2x的Kernel | 45/235 (19%) |
| 最高SOL分数（接近硬件极限） | 0.9722 |

> "The multi-agent system successfully outperformed baselines on 149 out of 235 problems (63%), with a geometric mean ratio of 1.38x (38% geomean speedup)."
> — Cursor Engineering, [Speeding up GPU kernels by 38% with a multi-agent system](https://cursor.com/blog/multi-agent-kernels)

三个代表性成果：
- **BF16 Grouped Query Attention**（来自Llama 3.1 8B推理场景）：比FlashInfer手工优化库**快84%**，SOL分数0.9722，接近硬件理论极限
- **BF16矩阵乘法**：自动生成的Kernel达到cuBLAS性能的**86%**，在小型M场景（LLM解码常见）领先基线最高**9%**
- **NVFP4 MoE层操作**（来自Qwen3等MoE模型）：识别4bit浮数量化瓶颈并实施针对性融合优化，**快39%**

虽然中位数SOL分数只有0.56（仍有很大优化空间，主要因为27块GPU要同时跑235个任务），但这个结果已足够震撼：**AI多Agent系统在高难度的硬件底层优化问题上逼近人类专家水平**。

---

## 五、Planner-Worker分离的关键设计原则

### 5.1 Planner可以递归派生

> "Planners continuously explore the codebase and create tasks. They can spawn sub-planners for specific areas, making planning itself parallel and recursive."
> — Cursor Engineering

子Planner机制让规划本身也可以并行扩展。当单一Planner被复杂代码库压垮时，子Planner可以接管特定区域，避免单点故障和隧道视野。

### 5.2 Worker的单一职责原则

Worker被设计成**不与其他Worker通信，不操心全局，只专心完成被分配的任务**。这消除了Worker层的所有协调开销，实现了线性吞吐量。

### 5.3 Judge控制节奏而非干预执行

Judge不优化代码，只决定"是否继续"。这种关注点分离让Judge的prompt更容易设计，也更不容易产生偏差。

### 5.4 协调协议即代码

GPU Kernel实验中最反直觉的一点：**整个协调协议存在于一个Markdown文件里**。没有数据库，没有服务发现，只有文件规范。这让系统极度简单，也让调试极度透明。

---

## 六、给Agent开发者的实操启示

### 什么时候应该用三角色架构？

当你遇到以下症状时，扁平结构已经不够用了：
- Agent之间因为共享状态产生大量锁等待
- 系统整体吞吐量不随Agent数量线性增长
- 困难任务被回避，只有安全的小改动被完成
- 长时运行后Agent行为开始漂移

### 角色分离 vs. 框架选择

这里有一个重要的认知：**角色分离是架构设计选择，而不是框架选择**。你可以在LangGraph里实现三角色，也可以在CrewAI里，还可以用简单的Python脚本。框架是工具，架构是决策。

> "A planner would first lay out the exact approach and deliverables to make progress toward the user's instructions. This would be handed to an executor, who became the sole lead agent responsible for ensuring the plan was achieved completely." — Cursor Engineering

Cursor的实践表明，**当架构正确时，即使Agent能力没有变化，系统行为也会产生质变**。Planner-Worker-Judge不是什么魔法prompt，而是一组精心设计的激励结构。

### 扩展的硬件约束

一个被低估的教训：系统峰值时冲到约1000并发Agent，每小时约1000次提交，跨越1000万次工具调用。但当他们限制了RAM使用后，磁盘成了新的瓶颈——数百个Agent同时编译，产生了**数GB/s的读写**，这成为整体吞吐量的约束。

> "The project structure, architectural decisions, and developer experience can affect token and commit throughput, simply because working with the codebase (e.g. compilation) dominates time, instead of ideally thinking and coding." — Cursor Engineering

这提示我们：**Agent系统的性能瓶颈可能不在推理，而在文件系统IO和编译**。大规模Agent部署需要重新思考项目结构设计。

---

## 七、关联知识：Agent编排的演进坐标

本文属于**Agent工程知识体系**中的**Orchestration（编排）**范畴，对应演进路径第7阶段：

| 阶段 | 主题 | 本文关联 |
|------|------|---------|
| 1 | Prompt Engineering | — |
| 2 | RAG | — |
| 3 | MCP | — |
| 4 | Paradigms | Agent设计模式 |
| 5 | Memory & Context | 上下文管理 |
| 6 | Tool Use | 工具调用优化 |
| **7** | **Orchestration** | **✅ 本文核心** |
| 8 | Deep Research | — |
| 9 | Multi-Agent | 三角色协作模式 |
| 10 | Skill | — |
| 11 | Deep Agent | — |
| 12 | Harness Engineering | 安全防护 |

---

## 结论

Cursor的两组实验（FastRender浏览器 + CUDA Kernel优化）共同说明了一件事：**多Agent协作的核心瓶颈不是Agent不够聪明，而是激励结构设计**。

扁平协作 → 锁竞争 → 风险规避 → 无进展的链条，被Planner-Worker-Judge三角色分离所切断。这个架构的核心洞察是：**让做决策的Agent（Planner）不执行，让执行的Agent（Worker）不决策**。

这个原则听起来简单，但它是让多Agent系统从"看起来并行"到"真正线性扩展"的关键。

---

**相关资源**：
- FastRender浏览器引擎：https://github.com/wilsonzlin/fastrender
- Kernel优化结果仓库：https://github.com/anysphere/kernel-optimization-results
- Cursor Blog原文：[Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents)
- Cursor Blog原文：[Speeding up GPU kernels by 38% with a multi-agent system](https://cursor.com/blog/multi-agent-kernels)