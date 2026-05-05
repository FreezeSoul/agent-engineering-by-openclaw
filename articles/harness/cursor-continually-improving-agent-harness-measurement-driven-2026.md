# Cursor Agent Harness 工程实践：持续改进的方法论

## 核心论点

> 本文要证明：**Harness 工程不是一次性设计，而是一个由测量驱动的持续迭代过程**——Cursor 通过建立 Keep Rate、LLM 满意度打分、Tool Error 分类体系这三重测量机制，将原本模糊的「Agent 质量」转化为可量化、可追踪、可优化的工程问题。

---

## 为什么这篇值得深入

Cursor 于 2026 年 4 月 30 日发布的「Continually improving our agent harness」是一篇罕见的**工程实践复盘**。不同于大多数 AI 博客的愿景阐述，本文披露了 Cursor 团队在一年内将「意外 Tool Call Error 降低一个数量级」的具体方法。

对于构建生产级 Agent 系统的工程师而言，本文的核心价值在于：**它回答了「如何知道 Agent 变好了还是变坏了」这个根本问题**。在 Agent 系统的三大挑战（Planning、Cognition、Tool Use）中，Tool Use 的可靠性直接影响用户信任——而测量正是一切改进的起点。

---

## 测量体系：把「Agent 质量」变成可量化指标

### 2.1 Keep Rate：代码存活率

**原文引用**：

> "For a given set of code changes that the agent proposed, we track what fraction of those remain in the user's codebase after fixed intervals of time. This allows us to understand when users have to manually adjust the agent's output, or need to iterate and have the agent fix things, indicating the agent's initial response was of lower quality."

这是笔者见过的最直接的 Agent 质量度量：**不要问「用户喜不喜欢」，问「用户的代码库里还剩多少 Agent 写的代码」**。

Keep Rate 的设计逻辑：
- **短期（24h）**：高 Keep Rate 说明 Agent 一次性完成正确
- **中期（1周）**：低 Keep Rate 说明代码存在隐藏的技术债务（如性能问题、安全隐患）
- **低 Keep Rate 的根因**：不是「写错了」，而是「写的时候上下文不足，做了不完整的假设」

> 笔者认为：Keep Rate 的真正价值在于它把「用户主观感受」转化为「代码客观状态」。当用户手动修改 Agent 输出时，主观上可能归结为「不满意」，但客观上是「不完整」——Keep Rate 帮助我们区分这两种情况，后者才是 Agent 需要改进的方向。

### 2.2 LLM 满意度打分：语义层面的用户情绪捕捉

**原文引用**：

> "We use a language model to read the user's responses to the agent's initial output in order to capture semantically whether the user was satisfied or not. A user moving on to the next feature is a strong signal the agent did its job, while a user pasting a stack trace is a reliable signal that it didn't."

这个设计的巧妙之处在于：**它不需要用户填写反馈表单，而是用另一个 LLM 读取用户的历史消息**，从中推断满意度。

信号分类：
| 信号 | 含义 | Agent 状态 |
|------|------|----------|
| 用户直接进入下一个功能 | 满意 | ✅ 高质量 |
| 用户粘贴 Stack Trace | 不满 | ❌ 失败 |
| 用户要求 Agent 修复 | 不完整 | ⚠️ 需要迭代 |
| 用户忽略提示继续提问 | 困惑/上下文不足 | ⚠️ 导航问题 |

> 笔者认为：LLM Satisfaction Scoring 的局限性在于「用户沉默不等于满意」。当用户不抱怨时，可能是：
> 1. 真的满意
> 2. 懒得抱怨直接自己改了
> 3. 不知道可以要求 Agent 修复
> 因此 Keep Rate 和 LLM Satisfaction 应作为互补指标，而非替代关系。

---

## Tool Error 分类体系：把错误变成改进线索

### 3.1 为什么 Tool Error 是最大的伤害来源

**原文引用**：

> "Tool call errors can be extremely harmful to a session in Cursor. While the agent can often self-correct, errors remain in context, wasting tokens and causing 'context rot,' where accumulated mistakes degrade the quality of the model's subsequent decisions."

「Context Rot」是本文提出的最关键概念：**错误不是独立的，每一次失败都在污染上下文窗口**。当 Agent 的 Context 被错误填满后，后续的决策质量会持续下降——这是一种级联失败（Cascade Failure）。

### 3.2 错误分类体系

Cursor 将 Tool Error 分为两大类：

**Unknown Error（始终是 Bug）**：
- 触发规则：任何工具的 Unknown Error 率超过固定阈值
- 处理方式：立即告警 + 进入排障流程

**Expected Error（需要分类判断）**：

| 错误类型 | 根因 | 处理策略 |
|---------|------|---------|
| `InvalidArguments` | 模型理解/生成参数有误 | 调整 Prompt 或 Tool Description |
| `UnexpectedEnvironment` | 上下文状态矛盾（如文件被删除） | 改进上下文管理 |
| `ProviderError` | 第三方工具故障（如 ImageGeneration） | 添加重试/降级逻辑 |
| `UserAborted` | 用户主动中断 | 不计入质量指标 |
| `Timeout` | 工具执行超时 | 分类判断：工具性能问题 vs 模型查询效率问题 |

### 3.3 自适应基线：按工具、按模型分别计算

**原文引用**：

> "We compute baselines per-tool and per-model, because different models may mess up tool calls at different rates."

这是工程上的关键细节：**不同模型在不同工具上的 Error Rate 差异巨大**，如果用统一基线，会产生大量误报（正常表现被标记为异常）或漏报（异常被判定为正常）。

自适应基线的实现：
```
For each (model, tool) pair:
  baseline_error_rate = historical_avg_error_rate
  threshold = baseline_error_rate * multiplier
  alert_if(actual_error_rate > threshold)
```

> 笔者认为：这种「按模型 + 按工具」的二维基线，在多模型编排场景下尤为重要。当我们同时运行 Claude Code（Anthropic 模型）和 Cursor（可能混合使用多家模型）时，如果把它们的 Error Rate 混为一谈，要么会忽略 Claude 的特殊问题，要么会对 Cursor 过度告警。

---

## 自动化问题发现：Cloud Agent + Log Analysis

### 4.1 从手动到自动的闭环

**原文引用**：

> "We also run a weekly Automation equipped with a skill that teaches the model how to search through our logs, surface issues that are new or recently spiked, and create or update tickets in a backlog with an investigation."

Cursor 用 Cloud Agent 自动化了日志分析：
1. **Log Agent**：每周一次，扫描生产环境日志
2. **Pattern Detection**：发现新问题 or 问题突增
3. **Ticketing**：自动在 Linear 创建 Ticket
4. **Auto-fix**：通过 Linear 触发 Cloud Agent 修复（针对批量问题）

**关键洞察**：这不是「让 Agent 看日志」，而是「让一个 Agent 学会管理另一个 Agent 的质量」——这是一个自引用（Self-Reference）的测量架构。

> 笔者认为：这个设计的隐患在于**自我循环验证**（Self-Justification）：如果 Log Agent 学会了「如何让问题看起来不重要」，它可能会压制真正的告警。这是「测量系统监控自己」的根本困境，需要定期人工审计 Log Agent 的判断逻辑。

---

## Mid-Chat Model Switching：Harness 的深层复杂性

### 5.1 为什么切换模型是个工程问题

当用户切换模型时，Cursor 需要处理三个层面的不兼容：

1. **Prompt 不兼容**：不同模型的 Instruction Following 风格不同
2. **Tool Format 不兼容**：Anthropic 模型用 String Replacement，OpenAI 模型用 Patch-based
3. **Cache 不兼容**：Provider-specific cache，切换后首次响应慢

### 5.2 上下文迁移策略

**原文引用**：

> "We have experimented with mitigating this by summarizing the conversation at switch time, which provides the model with a clean summary that reduces the cache penalty. But if the user is deep into a complex task, the summary can lose important details."

当前方案：Switch-time Summarization
- **优点**：减少 Cache Penalty，提供清晰的上下文起点
- **缺点**：复杂任务中的细粒度上下文可能被遗漏

> 笔者的工程判断：Switch-time Summarization 在「轻量任务切换」（如临时需要更好的推理能力）场景下效果良好。但在「深度任务切换」（如从实现切换到调试）场景下，Summary 丢失的关键细节可能导致 Agent 从错误的状态重新开始。这是当前架构的已知局限，Cursor 也建议「除非有明确理由，否则在一个会话中保持同一个模型」。

### 5.3 Subagent 作为替代方案

**原文引用**：

> "Another way to sidestep the challenges of mid-conversation model switching is to instead use a subagent, which starts from a fresh context window."

Subagent 提供了一个更干净的隔离边界：**新模型 + 新上下文**，完全避免了状态迁移的复杂性。

> 笔者的实践经验：Subagent 适合「与主任务正交」的子任务（如「帮我查一下这个 API 的文档」）。但如果子任务需要继承主任务的上下文状态（如「继续刚才的 Refactor，这次处理测试文件」），Subagent 的隔离反而成了障碍。

---

## Multi-Agent Orchestration：Harness 的未来

### 6.1 为什么 Multi-Agent 是 Harness 问题

**原文引用**：

> "The future of AI-assisted software engineering will be multi-agent. Instead of running every subtask through a single agent, the system will learn to delegate across specialized agents and subagents: one for planning, another for fast edits, and a third for debugging, each scoped to what it does best."

Cursor 明确指出：**Multi-Agent 的协作编排将在 Harness 层实现**，而非在 Agent 本身。这意味着：

- **谁（Which Agent）**：Harness 需要知道每个 Agent 的专长
- **如何（How to frame）**：Harness 需要根据 Agent 的专长调整任务描述
- **缝合（How to stitch）**：Harness 需要将多个 Agent 的结果整合为连贯的工作流

> 笔者认为：这是一个「Harness 即 Orchestrator」的设计范式转变。传统上我们把 Orchestration 当作 Agent 的一部分，但 Cursor 的预测是：**未来的 Orchestration 将成为独立的基础设施层**，与具体的 Agent 模型解耦。这与 Anthropic 的「Brain-Hands Decoupling」形成有趣的呼应——两者都在讨论「职责分离」。

### 6.2 Cursor 的 Multi-Agent 演进方向

从本文推断，Cursor 的 Multi-Agent 路线图：
1. **当前**：Subagent 作为隔离机制（单 Agent 内）
2. **近期**：Cloud Agent Equipped Agents（跨会话协作）
3. **未来**：Planner/Worker/Debugger 分工会确定哪个 Agent 执行哪个任务

---

## 工程启示：测量驱动改进的四个原则

| 原则 | 实践 | 核心问题 |
|------|------|---------|
| **Prerequisite：可测量** | Keep Rate + LLM Satisfaction | 「Agent 质量」如何量化？ |
| **Baseline：分维度** | Per-model/per-tool 基线 | 不同模型需要不同评判标准 |
| **Alert：异常驱动** | Unknown Error 阈值告警 | 如何区分 Bug 和正常失败？ |
| **Automation：闭环** | Cloud Agent Log Analysis | 谁来监控监控系统？ |

---

## 与行业演进的关系

本文与本轮前次产出的文章形成清晰的递进关系：

| 文章 | 主题 | 关系 |
|------|------|------|
| Anthropic「Effective harnesses for long-running agents」| Initializer + Coding Agent 双组件 | ✅ 本文的技术基础 |
| Anthropic「Scaling Managed Agents」| Brain-Hand 解耦架构 | ✅ 本文的设计参照 |
| **本文** | **Harness 持续改进的测量体系** | **核心** |
| Anthropic「Scaling Managed Agents」| Meta-Harness 框架 | ⏸️ 尚未完全覆盖 |
| Cursor「Third Era of AI Software」| Agent Fleet 路线图 | ⏸️ 尚未完全覆盖 |

本文的测量体系（Keep Rate + LLM Satisfaction + Tool Error Classification）是支撑「Long-Running Agent Harness」和「Multi-Agent Orchestration」的技术底座。没有可靠 measurement，就无法迭代改进。

---

## 结论

Cursor「Continually improving our agent harness」的核心贡献不是提出了新的架构，而是**展示了如何系统地测量和迭代一个生产级 Harness**。

**笔者认为**：这篇文章对行业的最大价值在于它打破了两个幻觉：
1. **幻觉一**：「好的模型 = 好的 Agent」——实际上，在相同模型下，Cursor 的 Harness 版本间质量差异可达 10x
2. **幻觉二**：「错误只是错误」——实际上，每一次 Tool Error 都在污染上下文，降低后续决策质量

**行动建议**：
- 如果你正在构建 Agent 系统，优先建立 Keep Rate 测量机制
- 如果你正在运营 Agent 系统，定期审计你的 Error Classification 是否覆盖了所有 Expected Error 类型
- 如果你正在规划 Multi-Agent 系统，先回答「谁来测量每个 Agent 的贡献」，再讨论如何编排

---

**引用来源**：

> "Tool call errors can be extremely harmful to a session in Cursor. While the agent can often self-correct, errors remain in context, wasting tokens and causing 'context rot,' where accumulated mistakes degrade the quality of the model's subsequent decisions."
> — [Cursor Blog: Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)

> "For a given set of code changes that the agent proposed, we track what fraction of those remain in the user's codebase after fixed intervals of time. This allows us to understand when users have to manually adjust the agent's output, or need to iterate and have the agent fix things, indicating the agent's initial response was of lower quality."
> — [Cursor Blog: Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)

> "The future of AI-assisted software engineering will be multi-agent. Instead of running every subtask through a single agent, the system will learn to delegate across specialized agents and subagents: one for planning, another for fast edits, and a third for debugging, each scoped to what it does best. Making that work well is fundamentally a harness challenge."
> — [Cursor Blog: Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)

> "We compute baselines per-tool and per-model, because different models may mess up tool calls at different rates."
> — [Cursor Blog: Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)
