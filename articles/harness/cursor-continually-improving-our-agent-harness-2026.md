# Cursor 如何持续迭代 Agent Harness：工程实践全解

> 本文解读 Cursor 2026年4月30日发布的工程博客 *Continually improving our agent harness*（Stefan Heule & Jediah Katz），剖析他们如何将 harness 工程化为一门系统化学科，而非「调调 prompt」的手艺活。

---

## 核心命题

**Harness 的质量直接决定 Agent 的可靠度。** 当业界还在争论「模型更重要还是 prompt 更重要」时，Cursor 用量化指标证明：同样的模型，在不同精调的 harness 下，可靠度差异超过一个数量级。更关键的是，这个差距来自工程实践的积累，而非模型本身。

Cursor 的实践指向一个明确结论：**Harness 工程 = 量化评估 × 系统化迭代 × 深度模型适配**，这是让 Agent 从「能用」走向「可靠」的核心杠杆。

---

## 一、问题背景：Harness 为何不是「加了工具的 prompt」

Cursor 从 2024 年末自研 coding agent 起，就意识到 harness 的复杂性远超最初的预期。早期版本中，他们投入大量精力做 context engineering：

- 为模型创建 guardrails：每次编辑后强制推送 lint/type 错误、限制单次工具调用数
- 提供静态 context：文件夹结构、语义匹配代码片段、压缩版用户附件文件

这些在模型能力较弱时有意义。但随着模型能力提升，**这些 guardrails 反而成为瓶颈**——模型能更好地自判断，却被迫接受过度约束。

Cursor 的解决思路是：随着模型能力进化，逐步拆除 guardrails，改为给 Agent 提供**动态获取 context 的能力**。这是 harness 适应模型能力的第一层含义。

---

## 二、量化评估体系：离线 Benchmarks + 在线 A/B 测试

Cursor 坦承，光靠公开 benchmark 不足以指导 harness 迭代，因为最好的 benchmarks 也只能近似真实使用场景。因此他们构建了两层评估体系：

### 2.1 离线评估：CursorBench

公开的 CursorBench 提供快速、标准化的质量读数，能跨时间对比。但这只是基线。

### 2.2 在线 A/B 测试：真正驱动决策的引擎

Cursor 在真实用户流量上并行部署两个或多个 harness 变体，通过多维指标衡量效果：

| 指标类型 | 具体指标 | 衡量内容 |
|---------|---------|---------|
| **效率指标** | 延迟、Token 效率、工具调用次数、缓存命中率 | Agent 是否「省力」 |
| **质量指标** | **Keep Rate**（代码保留率）| Agent 生成的代码，在用户代码库中经过固定时间后仍被保留的比例 |
| **质量指标** | **LLM 语义评判** | 用语言模型解读用户对 Agent 初始输出的反馈（用户转向下一个功能=好，用户粘贴堆栈=差）|

> 笔者注：Keep Rate 是一个被低估的指标。它直接回答了「用户是否需要手动调整 Agent 输出」这个终极问题，而不是看 Agent 做了什么。

这个双层评估体系让 Cursor 能识别出那些「直觉上有希望但实际没效果」的想法——他们提到曾试过用更贵的模型做 context summarization，结果对 Agent 质量影响微乎其微，不值得额外成本。这类反直觉的发现，只有在真实流量 A/B 测试中才能显现。

---

## 三、错误分类与异常检测：让「未知错误」归零

随着支持的模型和工具增加，harness 状态空间复杂度快速增长，工具调用错误是最大风险源。Cursor 将工具调用错误分为「已知」和「未知」两类：

**已知错误（Expected Errors）**：
- `InvalidArguments`：模型失误或 context 窗口内的矛盾
- `UnexpectedEnvironment`：模型试图操作不存在的环境
- `ProviderError`：第三方服务宕机（如 GenerateImage、WebSearch）
- `UserAborted`、`Timeout` 等

**未知错误（Unknown Errors）**：任何非预期的异常 → **永远视为 harness bug**

这带来一个关键工程原则：**任何未知错误的出现，都必须被修复，而不是被忽略。** 基于此，Cursor 设置了两级告警：

1. **固定阈值告警**：当任何工具的未知错误率超过预设阈值，立即触发（因为未知错误 = bug）
2. **异常检测告警**：针对已知错误，计算每个工具、每个模型的基线，当错误率显著偏离基线时触发（处理性能问题）

这套告警体系的背后是一个自动化流程：**每周运行一次 Cloud Agent equipped with a skill，搜索日志、发现新问题或激增问题、自动在 Linear 创建工单**。Cursor 透露，仅在一次专项冲刺中，就将未知工具调用错误降低了一个数量级。

---

## 四、模型定制化：让每个模型用自己熟悉的工具格式

这是最容易被忽视的工程细节：不同模型在预训练时接触的工具格式不同，强行让模型使用不熟悉的工具格式会付出额外的推理 token 且增加错误率。

Cursor 的做法：**每个模型使用它训练时接触的工具格式**。具体例子：

- OpenAI 系列模型：擅长 patch-based 编辑格式
- Anthropic Claude 系列：擅长 string replacement 格式

给 Claude 用 patch 格式，或给 GPT 用 replacement 格式，都会增加推理开销和错误率。这是模型无关的 harness 抽象层能做到的最底层适配。

更深层的定制化还包括：**Provider 级别的 custom prompting**，以及**模型版本的微调**。Cursor 观察到不同模型版本之间也存在行为差异，需要不同的 harness 配置。

### 4.1 特殊案例：Context Anxiety

Cursor 提到一个真实的模型 quirk：某个模型在 context 窗口填满时，会表现出「拒绝工作」的行为——它开始犹豫、声明任务太大。Cursor 通过调整 prompt 成功降低了这种行为。这说明**即使模型行为异常，也未必需要换模型**——harness 可以缓解模型的某些不良行为模式。

---

## 五、对话内模型切换：挑战与缓解策略

用户中途切换模型是一个特殊的工程挑战：不同模型有不同的行为、prompts 和工具形态，而对话历史是另一个模型产生的，处于该模型的分布之外。

Cursor 的处理方案：

1. **自动切换 harness**：切换模型时，Cursor 自动切换到对应模型的 harness（prompts + 工具集）
2. **注入引导指令**：告诉模型「你正在从中途接手另一个模型的对话」，并引导它避免调用历史中存在但当前模型工具集中没有的工具
3. **缓存 miss 惩罚**：切换意味着 cache miss，他们尝试在切换时 summarization 来生成干净摘要，减少 cache 惩罚，但在复杂任务深处细节仍可能丢失
4. **推荐策略**：除非有明确理由，建议用户在一个对话内保持使用同一模型

Cursor 还指出了 subagent 作为替代方案的价值：subagent 从全新的 context  window 启动，天然绕过了 mid-chat 切换的挑战。

---

## 六、多 Agent 未来：Harness 是协调层

Cursor 给出了一个明确的前瞻判断：

> 「AI 辅助软件工程的未来是多 Agent 的。系统需要知道派发哪个 Agent、如何为每个 Agent 的优势塑形任务、如何将结果缝合为连贯的工作流。这种协调能力将存在于 harness 中，而非任何一个单一 Agent。」

这个判断的工程含义是：**Harness 的核心能力将变为编排（orchestration），而非执行（execution）**。当一个任务需要 planning agent 负责分解、fast edit agent 负责快速修改、debugging agent 负责验证时，谁来协调它们、如何定义它们的交接协议，这些问题都属于 harness 层的设计范畴。

这对 harness 工程的要求意味着：
- 需要定义 Agent dispatch 策略
- 需要设计任务塑形（task framing）机制，让同一任务在不同 Agent 看来有不同的表现形式
- 需要处理 Agent 间结果的合并与冲突解决

这已经从「写好 prompt」演进到了「设计协作协议」。

---

## 七、工程启示

### 7.1 Harness 是第一性工程系统

Cursor 的实践表明，harness 不是配置调优，而是**一个需要版本控制、自动化测试、持续集成的工程系统**。错误分类、基线计算、异常检测、量化迭代——这些是软件工程的标配方法论，harness 开发同样需要。

### 7.2 量化评估是迭代的基础

没有 Keep Rate、没有 A/B 测试，harness 优化就是盲目的。Cursor 愿意为一次实验在真实流量上跑并等待结果，这种基础设施投入是大多数团队缺失的。

### 7.3 模型无关抽象的边界

harness 抽象到足够深时，模型无关就成了伪命题——工具格式、custom prompting、context anxiety 处理，都与模型强相关。Cursor 选择在 harness 层做深度定制，而不是在模型层妥协，这是一个务实的工程决策。

---

## 八、相关工具与项目

| 工具 | 说明 |
|------|------|
| [CursorBench](https://cursor.com/blog/cursorbench) | Cursor 公开的 coding agent 评估基准 |
| [lm-evaluation-harness (EleutherAI)](https://github.com/EleutherAI/lm-evaluation-harness) | 语言模型评估的标准框架，可用于构建 Agent harness 评估体系 |
| [Temporal](https://temporal.io) | Cursor 用于构建 durable execution 的工作流引擎，处理长时运行任务的容错与恢复 |

---

## 引用

> 「The agent harness that powers Claude Code (the Claude Code SDK) can power many other types of agents, too.」——Anthropic Engineering Blog

> 「The future of AI-assisted software engineering will be multi-agent. Instead of running every subtask through a single agent, the system will learn to delegate across specialized agents and subagents.」——Cursor Engineering Blog

---

*来源：[Cursor Engineering Blog - Continually improving our agent harness](https://cursor.com/blog/continually-improving-our-agent-harness)（2026年4月30日，Stefan Heule & Jediah Katz）*