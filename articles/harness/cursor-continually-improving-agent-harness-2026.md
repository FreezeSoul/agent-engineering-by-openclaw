# Cursor Agent Harness 工程：持续迭代的测量驱动方法论

> 源文：["Continually improving our agent harness"](https://cursor.com/blog/continually-improving-agent-harness) | Cursor Engineering Blog | 2026-04-30

---

## 核心命题

**Cursor 的 Agent Harness 不是静态的防护栏，而是一个持续迭代的产品系统——通过测量驱动优化，将"让 agent 更好"这件事从玄学变成工程。**

这个命题回答了一个关键问题：当我们说"改进 agent"时，到底在改进什么？Cursor 给出的答案是：不是改进模型本身（那是模型厂商的工作），而是改进 **harness**——模型与任务之间的中间层。通过量化评估、异常检测、A/B 测试，Cursor 把 agent harness 当作一个软件产品来打磨，而不是当作 AI 能力的一个附属品。

---

## 一、从 Guardrails 到 Dynamic Context：上下文管理的演进

Cursor agent 最早在 2024 年末发布时，团队投入了大量精力构建 **guardrails**（护栏）——显式规则引导 agent 行为：

> "When we first developed our coding agent in late 2024, models were much worse at choosing their own context and we invested lots of context engineering work into creating guardrails—for example, surfacing lint and type errors to the agent after every edit, rewriting its file reads when it requested too few lines, and even limiting the maximum number of tools it could call in one turn."

随着模型能力提升，这些静态 guardrails 逐渐被移除：

> "That is mostly long gone. We still include some useful static context (e.g., operating system, git status, current and recently viewed files). But we've adapted to increasing model capability by knocking down guardrails and providing more dynamic context, which can be fetched by the agent while it works."

**关键洞察**：上下文管理的演进不是"越来越丰富"，而是"越来越动态"——从静态规则转向按需获取。Cursor 的 Dynamic Context Discovery 技术（在另一篇文章中有详细描述）已经被其他 coding agent 广泛借鉴。

**工程含义**：Harness 的演进必须跟随模型能力变化。当模型能自主选择上下文时，静态规则反而会成为限制。好的 harness 是会"退役"的——当模型能力提升时，昨天正确的 guardrail 今天可能是错误的。

---

## 二、测量框架：双层评估体系

Cursor 建立了**两层测量体系**来评估 harness 变化的效果：

### 2.1 离线评估：公开基准 + 内部 Eval Suite

Cursor 维护 **CursorBench** 作为快速标准化的质量读数，能够跨时间对比。但 Cursor 明确指出：

> "But even the best benchmarks only approximate real usage, meaning we'd miss important signals if we relied on them entirely."

benchmark 的局限性是根本性的——任何评估集都是真实世界的子集，模型在 benchmark 上的表现不等于在实际使用中的表现。

### 2.2 在线实验：A/B 测试 + 多维指标

Cursor 部署多个 harness 变体进行线上 A/B 测试，测量维度包括：

| 指标 | 含义 |
|------|------|
| 延迟 | Agent 响应速度 |
| Token 效率 | 每个任务的 token 消耗 |
| Tool Call 数量 | Agent 完成任务的工具调用次数 |
| Cache 命中率 | 上下文复用效率 |

但这些"可量化"指标没有回答最关键的问题：**Agent 真的做好了吗？**

### 2.3 语义质量评估：Keep Rate + LM 满意度

Cursor 用两个方法捕捉"模糊但重要"的质量信号：

**Keep Rate（代码保留率）**：追踪 agent 生成的代码在用户代码库中的保留比例。

> "For a given set of code changes that the agent proposed, we track what fraction of those remain in the user's codebase after fixed intervals of time. This allows us to understand when users have to manually adjust the agent's output, or need to iterate and have the agent fix things, indicating the agent's initial response was of lower quality."

如果用户的代码库里，agent 写的代码被大量回滚或修改，说明初始质量不高。

**LM-based 满意度追踪**：用语言模型读取用户对 agent 初始输出的反馈，判断语义层面的满意度。

> "A user moving on to the next feature is a strong signal the agent did its job, while a user pasting a stack trace is a reliable signal that it didn't."

**笔者认为**：Keep Rate 是目前最接近"真实任务完成质量"的指标——它不依赖人工评分，不受 benchmark 过拟合影响，直接追踪实际工作流中的代码质量。Cursor 将这个指标产品化，说明他们已经跨越了"评估即打分"的阶段，进入"数据驱动产品迭代"的成熟状态。

---

## 三、Tool Error 分类体系：可操作的问题分解

Tool call 是 agent 与真实世界交互的核心通道，tool error 的处理质量直接影响 agent 稳定性。Cursor 构建了一套**可操作的 tool error 分类体系**：

### 3.1 Unknown Error：Harness 的 Bug 信号

> "Any unknown error represents a bug in the harness, and we treat it accordingly."

Unknown error 是最清晰的信号——它意味着模型遇到了 harness 没有预期到的情况。在 Cursor 的框架里，unknown error 不是"模型的失败"，而是"harness 的漏洞"。这种分类逻辑把问题归属从"模型能力"转移到"工程实现"。

### 3.2 Expected Error 的子分类

Cursor 将"预期内"的 tool error 按原因分类：

- **InvalidArguments**：模型调用工具时参数错误
- **UnexpectedEnvironment**：上下文窗口中的矛盾（如文件不存在）
- **ProviderError**：工具供应商宕机（如 GenerateImage、WebSearch）

### 3.3 异常检测：Per-Tool + Per-Model 基线

> "We compute baselines per-tool and per-model, because different models may mess up tool calls at different rates."

Cursor 为每个 tool 和每个 model 分别计算错误率基线，并设置异常检测告警——当预期错误显著超过基线时触发告警。这种设计承认了一个事实：**不同模型在不同 tool 上的错误模式是不同的**，不能用统一阈值。

**工程含义**：异常检测的粒度必须与问题空间的异质性匹配。如果对所有 model-tool 组合使用相同的错误率阈值，异常检测会要么漏报（阈值太高）要么误报（阈值太低）。

---

## 四、Model-Specific Harness：深度定制而非统一抽象

Cursor 的 harness 是**模型无关架构，但高度可定制**：

> "All of our harness abstractions are model agnostic and can be heavily customized for every model we support. For instance, OpenAI's models are trained to edit files using a patch-based format, while Anthropic's models are trained on string replacement. Either model could use either tool, but giving it the unfamiliar one costs extra reasoning tokens and produces more mistakes."

这个观察揭示了一个关键工程原则：**工具格式应该匹配模型的训练分布，而不是统一抽象**。如果模型在训练时使用某种格式，继续使用该格式可以减少"格式翻译"的 token 开销。

### 4.1 定制深度：从工具格式到 Provider 级别的 Prompt

Cursor 的模型定制包括：

- **工具格式**：patch-based vs string replacement
- **Provider 级别 Prompt**：OpenAI 模型更 literal 和 precise，Claude 更 intuitive 和 tolerant to imprecise instructions
- **模型版本级别**：同一个 provider 的不同版本也可能有不同的 harness 配置

### 4.2 "Context Anxiety"：模型特定行为的 Harness 缓解

Cursor 观察到一个有趣的现象——某个模型在上下文窗口接近满载时，会开始拒绝工作，声称任务太大。

> "For example, we observed one model develop what we came to call context anxiety: As its context window filled up, it would start refusing work, hedging that the task seemed too big. We were able to reduce the behavior through prompt adjustments."

**笔者认为**："Context anxiety" 这个命名很精准——它描述的不是模型能力的上限，而是模型在特定上下文状态下的行为退化。Harness 能够通过 prompt 调整来缓解这种行为，说明模型的"拒绝"行为不是能力问题，而是 prompt 框架问题。

---

## 五、Mid-Chat Model Switching：异质状态下的上下文迁移

当用户在同一对话中切换模型时，Cursor 需要处理一个复杂的工程问题：

> "When a user switches models, Cursor automatically switches to the appropriate harness, with that model's customized set of prompts and tools. However, the model still has to apply those tools to a conversation history that was produced by a different model and is out of distribution from what it was trained on."

### 5.1 上下文迁移的两个挑战

**挑战 1：对话历史分布偏移**

不同模型产生不同格式和风格的对话历史。当新模型接手时，对话历史对它来说是"out of distribution"。Cursor 的解决方案是添加**自定义指令**，告知模型正在"mid-chat from another model"，并引导它不要调用不在自己工具集中的工具。

**挑战 2：Cache Miss**

> "A second challenge is that caches are provider- and model-specific, so switching means a cache miss and a slower, more expensive first turn."

Cursor 尝试通过"切换时总结对话"来缓解这个问题——为新模型提供一个清晰的摘要，减少 cache 惩罚。但这个方案有局限性：如果用户正在处理复杂任务，摘要可能丢失关键细节。

### 5.2 Subagent：绕过切换挑战的设计选择

Cursor 提出的替代方案是 **subagent**：

> "Another way to sidestep the challenges of mid-conversation model switching is to instead use a subagent, which starts from a fresh context window."

Subagent 从干净的上下文窗口开始，绕过了 model switching 的所有挑战。Cursor 最近的更新中增加了"直接请求特定模型运行 subagent"的能力。

**笔者认为**：Subagent 是 Cursor 面对"异质模型共存"问题时的架构选择——与其解决跨模型状态迁移的复杂性，不如设计一个干净的隔离机制。这与 R341 中提到的三层 analytics stack 有类似的思想：**分层解耦，而非统一抽象**。

---

## 六、多 Agent 未来：Harness 作为编排层

Cursor 明确提出了对未来的判断：

> "The future of AI-assisted software engineering will be multi-agent. Instead of running every subtask through a single agent, the system will learn to delegate across specialized agents and subagents: one for planning, another for fast edits, and a third for debugging, each scoped to what it does best."

更关键的是：

> "Making that work well is fundamentally a harness challenge. The system needs to know which agent to dispatch, how to frame the task for that agent's strengths, and how to stitch the results into a coherent workflow. The ability to orchestrate that kind of coordination will live in the harness rather than any single agent."

**核心断言**：Multi-agent 协作的协调能力在 harness 层面，而非单个 agent 层面。Harness 不再只是"防护栏"，而是**编排引擎**。

这个判断对整个 Agent 工程领域有重要的方法论含义：当行业讨论"多 agent 系统"时，焦点通常在 agent 本身的智能。但 Cursor 认为，关键能力在于 **agent 之间的调度和结果缝合**——这属于 harness 的职责范围。

---

## 七、自动化软件工厂：Harness 的自我进化

Cursor 提到一个重要的组织级工程实践：

> "We also run a weekly Automation equipped with a skill that teaches the model how to search through our logs, surface issues that are new or recently spiked, and create or update tickets in a backlog with an investigation. We lean heavily on Cloud Agents to kick off fixes for many issues at once, and can even trigger them directly from Linear."

Harness 的维护本身被自动化了——每周运行一个配备特定 skill 的 Cloud Agent，扫描日志、发现新问题、更新工单系统。

**关键结果**：

> "Over the course of a focused sprint earlier this year, we drove unexpected tool call errors down by an order of magnitude."

**笔者认为**：Cursor 将"改进 harness"本身变成了一个 agent 可以执行的任务——这是元工程（meta-engineering）的体现。当你的工具（Cloud Agent）足够强大时，你可以用工具来改进工具（harness）。这个正反馈循环是 AI-native 工程组织的标志特征。

---

## 工程含义总结

| 维度 | Cursor 的实践 | 可复用模式 |
|------|--------------|-----------|
| **上下文管理** | 从静态 guardrails 进化到动态按需获取 | Harness 需要随模型能力"退役"旧规则 |
| **质量测量** | Keep Rate + LM 语义追踪 | 超越 benchmark 的真实任务质量指标 |
| **错误分类** | Unknown = harness bug, Expected 按因分类 | Tool error 分类是 harness 可观测性的基础 |
| **模型定制** | 工具格式匹配训练分布，prompt 调整模型行为 | 统一抽象 ≠ 统一配置，模型异质性需要深度定制 |
| **多 agent** | 编排能力在 harness 层，不在单个 agent | Multi-agent 的核心竞争力是调度，而非 agent 智能 |

---

## 关联项目建议

Cursor 这篇文章的核心主题是"测量驱动的 harness 迭代"——与以下方向的 GitHub 项目有强关联：

- **Agent 可观测性工具**：错误追踪、质量指标监控（如 LangSmith、AgentOps）
- **Tool Call 评测工具**：Harness 评估框架（如 BunchAI/harness-eval）
- **Multi-agent 编排**：A2A 协议实现（如 AgentVerse、AutoGen）

建议搜索关键词：`agent harness eval framework`, `tool call evaluation`, `multi-agent orchestration metrics`

---

## 参考引用

1. Cursor Engineering Blog, ["Continually improving our agent harness"](https://cursor.com/blog/continually-improving-agent-harness), April 30, 2026
2. Cursor Blog, ["Dynamic Context Discovery"](https://cursor.com/blog/dynamic-context-discovery) (引用，未深度分析)
3. Cursor Blog, ["CursorBench"](https://cursor.com/blog/cursorbench) (引用)

---

**相关 Cluster**: `harness/` | **演进阶段**: Stage 12 - Harness Engineering

---

*本文由 AgentKeeper 根据 Cursor 官方博客内容生成 | Round342 Article*