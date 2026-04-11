# 持续学习的三层架构：Model、Harness 与 Context

> **核心问题**：大多数关于 Agent 持续学习的讨论只聚焦于模型权重更新，但这个视角忽略了 Agent 系统中另外两个同样重要的学习层。本文拆解 Model、Harness、Context 三层各自的学习机制、工具链和适用场景，帮助架构师在系统设计阶段就确定正确的优化方向。

---

## 为什么要区分三层

当团队发现 Agent 表现不及预期时，常见的反应是"换模型"——假设问题出在模型能力上。但对于已部署的 Agent 系统，真正影响用户体验的往往不是模型太弱，而是：

- Harness 层的指令逻辑写死了，无法适应新场景
- Context 层（Skill、文档、记忆）没有随时间更新
- 模型层确实有短板，但没有训练数据来微调

换模型解决不了 Harness 层的问题。引入 RAG 解决不了模型层的缺陷。如果不在设计阶段明确三层各自的职责，团队会陷入反复换模型、反复调 Prompt、反复加 Skill 的低效循环。

三层各自的更新频率和成本差异巨大：模型层一次更新需要数天和大量算力；Harness 层一次代码提交可以立即生效；Context 层可以通过上下文注入实时改变。三者的容错性也不同——模型层更新一旦引入灾难性遗忘，影响不可逆；Harness 和 Context 层的改动可以快速回滚。

---

## Model 层：权重更新与灾难性遗忘

Model 层的持续学习指的是通过更新模型权重来改变 Agent 的行为。这是大多数人听到"持续学习"时最先想到的层面。

### 技术路径

主流的模型权重更新技术有三种：

- **SFT（Supervised Fine-Tuning）**：在标注数据上做监督微调。适用于有明确正确答案的任务，但需要大量人工标注，扩展成本高。
- **GRPO（GRPO 算法）**：DeepSeek 推广的一种强化学习方法，通过_reward signal_让模型自己判断输出质量，无需人工标注偏好数据。
- **DPO（Direct Preference Optimization）**：通过偏好对（preferred/dispreferred）直接优化模型，比 PPO 类方法更简单高效。

### 灾难性遗忘：核心挑战

Model 层持续学习的最大障碍是**灾难性遗忘（Catastrophic Forgetting）**：当模型在新任务上微调时，它倾向于丢失之前学到的能力。这在 Agent 场景中尤为棘手——一个专门针对工具调用优化的模型可能会失去对话连贯性。

灾难性遗忘使得 Model 层更新必须伴随完整的回归测试。在 Agent 评测中，这通常意味着需要在每次模型更新后重新运行完整的 Benchmark 套件（SWE-bench、Terminal Bench 等），成本极高。

### 实际应用

在实际 Agent 部署中，Model 层的更新通常以"Agent 版本"为单位进行。OpenAI 的 Codex 模型族可以视为针对编程 Agent 任务定制的模型；Anthropic 的 Claude Opus/Sonnet 系列则是针对不同成本-能力平衡点设计的通用 Agent 底座。

**笔者观察到的一个趋势**：越来越多的团队选择不在 Model 层做持续学习，而是通过 Harness 和 Context 层来适应特定场景。只有当模型能力本身成为瓶颈（如某类推理任务持续失败）时，才考虑定制化的模型训练。

---

## Harness 层：代码、指令与工具的协同进化

Harness 层指驱动 Agent 运行的核心代码和始终内置的指令与工具。这一层的学习不同于模型更新——它不改变模型权重，而是改变 Agent 运行时所依赖的**执行框架**。

### 什么属于 Harness 层

Harness 层的组成包括：

- Agent 的主循环逻辑（如何决定下一步行动）
- 内置的工具集（即便不是 Agent 自己配置的）
- 系统级指令（安全策略、边界约束）
- 与外部系统的集成代码（MCP 协议实现、记忆存储客户端）

在 Claude Code 中，Harness 就是 Claude Code 本身——即 Pi Agent 的脚手架代码加上 Claude 的模型共同构成完整的 Agent。

在 OpenClaw 中，Harness 是 Pi 运行时加上所有内置的 Skills（包括文件系统、搜索、记忆等核心 Skill）。

### Meta-Harness：从日志到优化

最近一篇重要论文 **Meta-Harness: End-to-End Optimization of Model Harnesses** 提出了一个关键思路：将 Agent 的执行轨迹（traces）作为 Harness 优化的输入。

具体做法是：

1. 让 Agent 在一组任务上运行，收集所有执行轨迹
2. 将轨迹日志写入文件系统
3. 启动一个"优化 Agent"（coding agent）分析这些轨迹
4. 优化 Agent uggest 修改 Harness 代码
5. 用修改后的 Harness 重新运行，验证改进效果

这个循环实际上将 ML 中的"观察-分析-调整"机制引入了 Harness 工程，只是学习对象从模型权重变成了代码。

### Harness 层的更新节奏

Harness 层的更新粒度通常由代码变更驱动。一个 Feature Flag 可以立即改变 Harness 的行为；一次依赖升级可能影响整个 Agent 的稳定性。因此 Harness 层的持续学习需要配套的 CI/CD 流程和灰度发布机制。

---

## Context 层：外部知识与配置的动态演进

Context 层是 Agent 的"外部大脑"——它位于 Harness 之外，可以通过配置来调整 Agent 的行为，而无需修改代码或重新训练模型。

### Context 的组成

Context 包括：

- **自然语言指令**：系统提示词（System Prompt）的动态部分
- **Skills**：可复用的能力包，如 Claude Code 的 `/skills`、OpenClaw 的 Skill 体系
- **工具定义**：MCP 协议的工具描述、参数 schema
- **记忆**：持久化的会话历史、用户偏好、领域知识

在 Claude Code 的架构中，`CLAUDE.md`、`/skills`、`mcp.json` 属于 Context 层。在 OpenClaw 的架构中，`SOUL.md` 和所有 Skill 的 Markdown 描述属于 Context 层。

### Context 学习的两个维度

Context 层学习可以从两个维度分类：

**按范围**：
- Agent 级：所有实例共享的上下文，如 OpenClaw 的 `SOUL.md` 记录了自己的身份和协作原则
- 用户/租户级：每个用户或组织有独立的上下文配置，如 Hex 的 Context Studio 为每个数据笔记本维护独立的上下文

**按时间**：
- 离线更新：定期从执行轨迹中提取知识，更新 Context（如 OpenClaw 的"dreaming"机制）
- 热路径更新：Agent 在执行过程中主动将关键信息写入上下文

### OpenClaw 的 Context 学习案例

OpenClaw 的"dreaming"机制是一个典型的 Context 层离线学习实现：Agent 在空闲周期中回顾近期执行轨迹，将有价值的洞察追加到 `SOUL.md`，使自身的协作能力随时间累积。

这与 Model 层的学习有本质区别：Context 层更新不改变模型权重，因此没有灾难性遗忘风险；更新结果对人类可读（就是 Markdown 文件），可审计、可回滚；更新频率可以很高（小时级甚至分钟级）。

---

## 三层对比：何时该优化哪一层

三层各有其适用场景，混淆各层的职责是 Agent 系统设计的常见错误。

| 维度 | Model 层 | Harness 层 | Context 层 |
|------|---------|-----------|-----------|
| **更新内容** | 模型权重 | 代码+内置指令+工具 | 外部知识+Skill+记忆 |
| **更新频率** | 数天~数周 | 随时（代码提交）| 分钟~小时 |
| **更新成本** | 高（GPU+数据）| 中（工程时间）| 低（文本编辑）|
| **回滚难度** | 困难 | 容易 | 极容易 |
| **灾难性遗忘风险** | 高 | 无 | 无 |
| **典型使用** | 模型能力成为瓶颈 | 需要新工具/安全策略 | 领域知识快速适应 |

**一个判断原则**：当 Agent 在某类任务上**稳定失败**（不是因为缺少领域知识，而是推理能力不足），应考虑优化 Model 层。当失败模式不固定，时而成功时而失败，优先检查 Harness 层。当 Agent **行为正确但缺乏领域特异性**，优先丰富 Context 层。

---

## Traces：贯穿三层的核心资产

无论优化哪一层，都依赖同一个输入：**执行轨迹（Traces）**。Traces 是 Agent 从启动到结束的完整执行路径记录，包含 LLM 的每次调用、工具执行的输入输出、中间状态。

LangChain 的观点是：Traces 是驱动三层持续学习的统一燃料。

- 要优化 Model 层？收集高质量的 Traces，送去 SFT/GRPO 训练
- 要优化 Harness 层？用 Traces 运行 Meta-Harness 循环，让优化 Agent 分析并改进代码
- 要优化 Context 层？从 Traces 中提取领域知识，更新 Skill 文档或记忆

这意味着**可观测性基础设施（tracing）不是事后诸葛亮，而是持续学习的前提条件**。在 Agent 系统设计阶段就需要考虑如何收集、存储和分析 Traces。

---

## 实践建议

### 1. 先定位瓶颈层，再投入资源

在加训模型之前，用 Traces 分析失败模式的稳定性。如果同一类任务反复失败，Model 层是瓶颈；如果失败模式分散且与领域相关，Context 层是瓶颈；如果 Agent 行为不稳定（有时候对有时候错），Harness 层是瓶颈。

### 2. 优先建设 Context 层的学习机制

Context 层是成本最低、风险最小的优化路径。在 Agent 上线初期，优先建设 Skill 体系和记忆机制，使 Agent 能够通过更新配置（而非重新训练）来适应新场景。OpenClaw 的 Skill 体系和"dreaming"机制是 Context 层持续学习的优秀参考实现。

### 3. 用 Golden Traces 做 Harness 回归测试

当更新 Harness 时，用一组 Golden Traces（有明确答案的高质量执行轨迹）作为回归测试集。这能有效防止 Harness 的新改动破坏已有的正确行为。

### 4. 谨慎对待 Model 层更新

Model 层更新是高风险操作。引入 Model 层更新前，必须完成完整的 Benchmark 回归。如果团队没有足够的评测基础设施（如 LangSmith 或自建的 eval pipeline），不要贸然做模型微调。

---

## 参考文献

- [Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/) — 将 ML 优化循环引入 Harness工程的论文
- [LangChain Blog: Continual learning for AI agents](https://blog.langchain.com/continual-learning-for-ai-agents/) — 本文主要参考来源，三层架构的原始提出
- [Deep Agents Documentation](https://deepagents.dev/) — Harness 层 Context 学习机制的生产级实现参考
- [LangSmith](https://docs.smith.langchain.com/) — Traces 收集与 eval 分析的平台

---

*本文属于 Stage 5（Memory & Context）体系，核心贡献是将持续学习问题从单一的"模型更新"扩展为三层架构，为 Agent 系统设计提供决策框架。*
