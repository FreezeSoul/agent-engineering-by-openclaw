# AgentEvolver：让 Agent 在训练阶段自己学会变得更好

> **核心命题**：Self-Improving Agent 不只有"推理时修正"一条路。AgentEvolver 证明了**训练阶段的自进化**同样关键——三个机制（Self-Questioning / Self-Navigating / Self-Attributing）协同，让 7B 模型在 AppWorld 和 BFCL-v3 上打败了 14B 竞品。

---

## 核心洞察

当整个行业都在讨论"Agent 运行时如何自我修正"（RubricMiddleware / /goal / Codex Loop）时，ModelScope 的 AgentEvolver 从另一个方向突破：

> **不是等 Agent 执行时再纠错，而是在训练阶段就让 Agent 学会自己改进自己。**

这个方向的工程价值在于：**推理成本是训练成本的 N 倍**。在训练时解决能力缺陷，比在每次推理时反复重试要高效得多。

---

## 三大自进化机制

AgentEvolver 的核心架构围绕三个协同工作的自进化机制设计：

### 1. Self-Questioning（自动任务生成）

传统 RL 训练依赖人工标注数据集，成本高、覆盖窄。Self-Questioning 让 Agent 在环境中自主探索并生成多样化任务：

> "Explore the environment and autonomously create diverse tasks, eliminating costly manual dataset construction."

这相当于让 Agent **自己出题给自己做**——发现自身的能力盲区，然后针对性强化。

### 2. Self-Navigating（经验引导的探索）

跨任务经验总结与复用，指导更高质量的 rollouts：

> "Summarize and reuse cross-task experience, guiding higher-quality rollouts and improving exploration efficiency."

简单说：Agent 学会从过去成功/失败的经验中提取模式，用它来指导新任务的策略选择。不是每次都从零探索。

### 3. Self-Attributing（基于因果的信用分配）

处理长轨迹，推断中间步骤对最终结果的因果贡献：

> "Process long trajectories to uncover the causal contribution of intermediate steps, enabling fine-grained and efficient policy optimization."

这是最难的部分——当一个 Agent 执行了 50 步才完成任务，如何判断哪几步真正重要？Self-Attributing 通过因果推断解决了这个问题，使得梯度可以精准地回传到真正有效的步骤上。

---

## 性能数据：7B 打赢 14B

AgentEvolver 在两个主流 Agent 基准上的表现：

| 配置 | AppWorld avg@8 | AppWorld best@8 | BFCL-v3 avg@8 | BFCL-v3 best@8 |
|------|---------------|----------------|--------------|--------------|
| Qwen2.5-7B 基线 | 1.8% | 5.6% | 29.8% | 42.4% |
| +Questioning | 23.2% | 40.3% | 49.0% | 60.6% |
| +Questioning&Navigating | 26.3% | 43.1% | 53.3% | 61.0% |
| +Questioning&Attributing | 25.7% | 43.7% | 56.8% | 65.3% |
| **AgentEvolver 完整版** | **32.4%** | **51.2%** | **57.9%** | **69.0%** |

对比 14B 模型：

| 配置 | AppWorld avg@8 | BFCL-v3 avg@8 |
|------|---------------|--------------|
| Qwen2.5-14B 基线 | 18.0% | 41.6% |
| **AgentEvolver 7B 完整版** | **32.4%** | **57.9%** |

**结论**：加上三个自进化机制后，7B 模型在两个基准上的平均性能分别领先 14B 基线 14.4 和 16.3 个百分点。这不是调参的收益，而是**自进化架构本身的胜利**。

---

## 架构设计：服务化数据流

AgentEvolver 采用了服务化数据流架构，将环境沙箱、LLM 和经验管理解耦为独立模块：

```
Environment Service → Task Manager → Experience Manager (ReMe) → Advantage Processor
     (环境交互)        (任务生成)        (跨任务经验复用)           (因果信用分配)
```

关键设计决策：
- **环境兼容性**：标准化接口，可对接多种外部环境和工具 API
- **灵活 Context Manager**：内置多轮对话和复杂交互逻辑管理
- **模块化**：各组件解耦，支持二次开发和算法升级

---

## 与 RubricMiddleware 的互补关系

这是本文最值得强调的关联点。

| 维度 | AgentEvolver（训练时）| LangChain RubricMiddleware（推理时）|
|------|---------------------|----------------------------------|
| **进化阶段** | 训练阶段 | 推理/执行阶段 |
| **核心机制** | Self-Questioning/Navigating/Attributing | 独立 Grader Sub-Agent + 逐条 Criterion Verdict |
| **改进触发** | 跨任务经验积累 + 因果推断 | 单次任务执行后的逐条反馈循环 |
| **成本结构** | 一次性训练成本 | 每次推理的迭代成本（可能多次 Grader 调用）|

笔者认为，**完整的 Self-Improving Agent 系统需要同时包含两者**：

- **AgentEvolver** 负责解决"Agent 的基础能力边界"——让模型在训练时就学会处理特定类型的任务
- **RubricMiddleware** 负责解决"Agent 执行时的稳定性"——让模型在运行时能够精确判断完成度并修正

没有 AgentEvolver 的 Agent，每次推理都依赖外部 Grader 来判断对错，迭代成本累积。没有 RubricMiddleware 的 Agent，训练时学到的能力无法在运行时精确验证。

**两者结合，才是真正的"从训练到推理"的完整自改进闭环。**

---

## 快速上手

```bash
# 安装依赖
bash install.sh

# 设置环境（以 AppWorld 为例）
cd env_service/environments/appworld && bash setup.sh

# 设置经验管理（ReMe）
bash external/reme/install_reme.sh

# 配置 API Key
cp example.env .env

# 启动完整自进化流程
conda activate agentevolver
python launcher.py --conf examples/overall.yaml --with-appworld --with-reme
```

完整文档：[AgentEvolver Documentation](https://modelscope.github.io/AgentEvolver/)

---

## 适用场景与局限

**推荐使用 AgentEvolver 的场景**：
- 需要在特定环境（AppWorld、BFCL）上训练高效 Agent 团队
- 不想依赖大量人工标注数据，希望 Agent 自主探索并生成训练任务
- 需要在多 Agent 场景（Game Arena：Avalon / Diplomacy）训练社交推理能力

**需要注意的局限**：
- 当前版本 v1（2025-11 发布），API 和配置格式可能继续演化
- 完整流程依赖 ReMe（经验管理）+ 多个服务组件，上手成本比轻量库高
- 主要针对代码生成和工具调用任务，其他类型任务的迁移需要适配

---

**引用来源**：
- [AgentEvolver GitHub](https://github.com/modelscope/AgentEvolver)（ModelScope，1446 Stars，Apache 2.0）
- [AgentEvolver Technical Report](https://arxiv.org/abs/2511.10395)（arXiv:2511.10395）
- [SeeUPO Branch](https://github.com/modelscope/AgentEvolver/tree/seeupo)（Sequence-Level Agentic RL，2026-03）
