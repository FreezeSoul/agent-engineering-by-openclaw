# Cursor 如何为 Codex 模型定制 Agent Harness：模型特定调优的工程实践

> 本文深度解析 Cursor 官方工程博客，探讨如何针对不同 frontier 模型定制 agent harness。

---

## 核心命题

**模型特定的 agent harness 调优不是「写好 prompt」那么简单——它是门级的系统工程，每个 frontier 模型都需要专属的工具定义、指令模式和基础设施适配。** Cursor 的实测数据证明：reasoning traces 被丢弃时，Codex 模型性能下降 **30%**，而同等条件下 GPT-5 在 SWE-bench 仅下降 3%。这个 30% 的 gap 就是 harness 工程的价值证明。

---

## 一、问题：Frontier 模型各有「脾性」

Cursor 集成了所有前沿 AI 编程模型，但每个模型在 Cursor 的 agent harness 中表现差异巨大。

官方原文：

> "AI labs train new models on a variety of different instructions and tools. In specific domains like coding, models may favor patterns that are more similar to what they've already seen in training."

**笔者认为**：这句话揭示了一个关键认知——模型训练时的工具偏好不是 bug，是特性。Harness 工程师的任务不是「纠正」这些偏好，而是为模型提供它熟悉的工具集和指令模式，让它在自己擅长的领域发挥到极致。

不同模型的脾性：

| 模型家族 | 天然工具偏好 | Harness 挑战 |
|---------|------------|-------------|
| GPT-5 主线 | 标准工具调用模式 | 相对容易适配 |
| Codex 系列 | Shell 导向，倾向用命令行工具 | 需要「伪装」工具定义 |
| Claude 系列 | Artifact / 结构化输出优先 | 需要不同的 action bias |

---

## 二、Codex 模型的五项 Harness 定制

### 2.1 Shell-Forward 工具适配

OpenAI 的 Codex CLI 原生面向 shell 工作流，模型在训练时大量接触 `rg`（ripgrep）、`cat`、`sed` 等命令行工具。因此 Codex 天然更信任 shell 命令，而非 Cursor 提供的专用工具。

Cursor 的解决方案是把工具名称和定义做得更像 shell 等价物：

> "We made the names and definitions of tools in Cursor closer to their shell equivalents like rg (ripgrep)."

同时增加了明确指令：

> "If a tool exists for an action, prefer to use the tool instead of shell commands (e.g. read_file over `cat`)."

**笔者认为**：这里的工程思路很巧妙——不是强迫模型改变偏好，而是让工具「伪装」成模型熟悉的形态。这比直接 prompt 说「不要用 shell」有效得多。类似地，如果你的 agent 总是绕过你的工具层，先检查工具定义是否「看起来像」模型训练时的工具。

### 2.2 Reasoning Summaries 的平衡术

Codex 模型家族使用 reasoning summaries（推理摘要）来与用户沟通工作进展。与 GPT-5 主线模型不同，这些摘要可能是单行标题，也可能是一段完整的消息。

Cursor 面临的工程挑战是：**让用户能跟得上 agent 的进度，但不至于被刷屏**。

官方策略：

- 限制 reasoning summaries 为 1-2 句
- 发现新信息或发起新策略时才输出
- 禁止在摘要中评论自己的沟通行为（如 "I'm explaining to the user..."）

**关键发现**：Codex 模型在 agent turn 结束前无法正常「说话」，所以 Cursor 移除了所有「mid-turn 与用户沟通」的 prompt 语言。移除后，模型最终代码输出质量反而提升了。

**笔者认为**：这是一个反直觉的优化——减少模型说话，代码质量反而更好。这说明在 agentic coding 场景中，模型的「沟通欲望」往往干扰它的「执行专注度」。如果你的 coding agent 经常产出半成品，先检查它是否在 mid-turn 阶段花了太多精力组织语言。

### 2.3 推理痕迹保留（Reasoning Traces Preservation）

这是整篇文章最关键的量化数据。

> "In our Cursor Bench experiments, removing reasoning traces from GPT-5-Codex caused a **30% performance drop**. In comparison, OpenAI observed a smaller **3% degradation** for GPT-5 on SWE-bench when reasoning traces were omitted."

Codex 模型尤其依赖 reasoning traces 的连续性。Reasoning traces 丢失时，模型需要「猜测」之前的 thought process，导致：

- 丢失 subgoals
- 规划退化
- 工具调用乱序
- 重复推导前面的步骤

Cursor 的工程响应是增加 alerting 机制，确保 reasoning traces 始终被正确保留和转发。

**笔者认为**：30% vs 3% 的差异值得深思——Codex 的 agentic 特性（更长的 reasoning chain、更复杂的多步规划）让它对 context 完整性更敏感。如果你的 agent 性能不稳定，先排查 reasoning traces 是否在某些边界情况下被丢弃了。这可能是隐藏的性能杀手。

### 2.4 Action Bias：推动模型主动执行

Cursor 的默认 agent 模式希望 agent 自主读写文件，但实际使用中用户经常 tab 过去发现 agent 在「等待许可」。

对 Codex 的特殊处理：

> "Unless the user explicitly asks for a plan or some other intent that makes it clear that code should not be written, assume the user wants you to make code changes or run tools to solve the user's problem."

在 Cloud Agents（异步远程工作流）中，这个指令甚至更强硬。

**笔者认为**：Action bias 的设计反映了一个重要的 UX 哲学——**在 agentic coding 场景中，「过度谨慎」比「适度鲁莽」更伤害用户体验**。用户delegation 的心智模型是「去做」，而不是「来问我」。如果你的 agent 经常停下来问「你要我这样做吗」，检查你的 harness 是否在无意中注入了过多 conservative bias。

### 2.5 Message Ordering 的微调

OpenAI 模型训练时严格遵循消息优先级：system prompt > user messages > tool results。

这个特性本来是好事，但当 Cursor 的 harness prompt 与用户消息冲突时，Codex 可能会拒绝执行用户请求。

具体案例：

> "At one point we told Codex that it should take care to preserve tokens and not be wasteful. But we noticed that this message was impacting the model's willingness to perform more ambitious tasks... Sometimes it would stop and stubbornly say, I'm not supposed to waste tokens!"

**笔者认为**：这个案例揭示了 harness 调优中的「副作用盲区」——一个看似无害的指令（如「不要浪费 token」）可能在特定模型上产生与预期相反的行为。解决办法是建立 harness 变更的 eval 矩阵，确保每个新指令不会在多个模型上产生意外行为。

---

## 三、Harness 工程的方法论沉淀

从 Cursor 的实践中，我们可以提炼出模型特定 harness 调优的方法论：

```
评估流程：
1. 基础集成 → 2. 模型特定工具适配 → 3. Prompt 平衡调优 → 4. Eval 验证 → 5. 部署监控
```

**关键工程检查点**：

| 阶段 | 检查项 | 指标 |
|------|--------|------|
| 工具适配 | 工具名称/定义是否接近模型训练模式 | Tool call 成功率 |
| Reasoning summaries | 刷屏率 vs 跟进率 | 用户主动关闭率 |
| Reasoning traces | Trace 完整性 | 端到端任务完成率 |
| Action bias | 等待许可频率 | 自主完成任务率 |
| Message ordering | 指令冲突检测 | 用户请求拒绝率 |

---

## 四、给 Harness 工程师的启示

1. **模型不是通用的**：同一套 harness 不可能最优地服务所有模型。每个新模型都需要专属的适配工作。

2. **量化是硬道理**：Cursor 能够发现 30% 的性能差异，是因为他们有 Cursor Bench 这套 internal eval。没有 eval 的 harness 调优是盲人摸象。

3. **副作用在 prod 之前发现**：Message ordering 案例说明，harness 变更需要在多模型上做矩阵式测试，否则一个看似无害的改动可能在某个模型上引发严重问题。

4. **工具定义即 API**：工具的名称、参数定义、返回值格式都会影响模型的工具调用决策。这是 harness 工程中最细粒度的调优点。

---

## 五、结语

Cursor 的 Codex harness 调优实践揭示了一个核心事实：**agent harness 是连接模型能力与产品体验的桥梁，而不是简单的 prompt 包装**。

随着模型家族的扩大（GPT-5、Codex、Claude Sonnet、Haiku……），harness 工程的复杂度会指数增长。每个模型都有独特的工具偏好、reasoning 模式、通信风格和 conservative bias。构建一个能够动态适配多模型的 harness 基础设施，将是 2026 年 AI coding 平台的核心竞争力。

**下一步行动**：如果你在构建自己的 coding agent harness，先为当前使用的模型建立 baseline eval。然后每次修改 harness 时，运行完整的 eval 矩阵。你可能会发现，一些看似微小的改动（如工具重命名、指令措辞调整）能够带来显著的性能提升——就像 Cursor 发现 30% 的 reasoning traces 问题一样。

---

## 参考文献

1. [Improving Cursor's agent for OpenAI Codex models](https://cursor.com/blog/codex-model-harness) - Cursor Engineering Blog
2. [Responses API - OpenAI](https://platform.openai.com/docs/guides/migrate-to-responses) - Reasoning traces 保留机制
3. [Cursor Cloud Agents](https://cursor.com/docs/cloud-agent) - Action bias 应用的完整语境

---

*本文属于 `harness/` 目录，聚焦 agent 工程机制设计。相关主题：multi-agent orchestration、evaluator loop、working state management。*
