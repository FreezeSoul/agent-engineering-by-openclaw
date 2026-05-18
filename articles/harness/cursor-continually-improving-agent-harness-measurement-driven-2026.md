# Cursor 是如何持续改进 Agent Harness 的：测量驱动工程实践

> 本文深度解读 Cursor 官方博客 [Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness)，聚焦 Cursor 的测量驱动 harness 工程方法论。

---

## 核心问题：harness 和模型共同决定 agent 质量，但"好"很难量化

Cursor agent 的能力由 harness 和模型共同决定，但"好"是一个难以定义的概念。Cursor 选择了**测量驱动**的方法：通过多层测量体系来定位和修复问题，让 harness 的改进不再是靠直觉，而是靠数据。

这与 Anthropic 在 Eval 上的投入方向一致——好的评测不只是打分，是研发流程的一部分。

---

## 一、测量体系的两个维度：离线基准 vs 在线实验

Cursor 维护了**两套互补的测量体系**：

### 1.1 离线评估：CursorBench 公开基准

```
CursorBench → 快速、标准化的质量读数，支持跨时间对比
```

CursorBench 是 Cursor 自己的评测套件，提供快速、标准化的质量读数。配合公开基准（如 SWE-bench），让团队能够跨时间对比进展。

但即使是最好的基准，也只是**近似**真实使用场景——这意味着如果完全依赖基准，会错过重要信号。

### 1.2 在线实验：A/B 测试真实用户行为

Cursor 同时进行在线实验，将多个 harness 变体并排部署：

**衡量的核心指标：**

| 指标类型 | 具体指标 | 说明 |
|---------|---------|------|
| 性能指标 | 延迟、Token 效率、工具调用次数、缓存命中率 | 方向性有用，但不直接反映 agent 是否做好了工作 |
| **行为指标** | **Keep Rate**：agent 生成的代码在用户代码库中保留的比例 | 直接反映用户是否需要手动调整 agent 输出 |
| **行为指标** | **LLM 语义满意度**：用 LLM 读取用户对 agent 初始输出的响应 | 用户直接进入下一个功能 = agent 做得好；用户粘贴堆栈跟踪 = agent 没做好 |

> 笔者注：Keep Rate 是一个聪明的设计——它把"好"从主观评价变成了可量化的代码留存率。用户自己用脚投票，比任何人工评分都可靠。

---

## 二、异常检测与自动化问题发现

### 2.1 工具调用错误分类体系

随着模型和能力的增加，harness 变得越来越复杂，工具调用错误是最大的表面区域之一。Cursor 将错误分为"预期的"和"未知的"：

**预期错误（Expected Errors）：**

| 分类 | 含义 | 处理方式 |
|------|------|---------|
| InvalidArguments | 模型工具调用参数错误 | 属于训练分布内，计入基线 |
| UnexpectedEnvironment | 上下文窗口内信息矛盾 | 计入基线 |
| ProviderError | 工具供应商宕机（如 GenerateImage、WebSearch）| 计入基线 |
| UserAborted / Timeout | 用户中止或超时 | 计入基线 |

**未知错误（Unknown Errors）：**
- 任何无法分类的错误 → **始终是 harness 的 bug**

### 2.2 分层告警机制

Cursor 定义了两层告警：

```
未知错误率告警（固定阈值）
  └─ 任何工具的未知错误率超过阈值 → 立即告警（因为未知错误 = bug）

异常检测告警（动态基线）
  └─ 预期错误显著超过基线 → 告警（区分：是 bug 还是预期行为？）
  
  基线按工具、按模型分别计算
  └─ 不同模型的工具调用错误率天然不同
```

### 2.3 自动化问题发现：Cloud Agent + Log Analysis Skill

Cursor 的做法特别有意思——他们用一个 Cloud Agent 专门跑日志分析：

> "We also run a weekly Automation equipped with a skill that teaches the model how to search through our logs, surface issues that are new or recently spiked, and create or update tickets in a backlog with an investigation."

这本质上是一个**用 agent 监控 agent 的系统**。而且他们能通过 Linear 直接触发修复：

> "We lean heavily on Cloud Agents to kick off fixes for many issues at once, and can even trigger them directly from Linear."

笔者注：这是"软件工厂"（software factory）理念的具体实现——自动化地发现、分类、跟踪和修复 harness 问题，而且通过 Linear 形成闭环。

---

## 三、模型定制化：每个模型有自己专属的 harness

### 3.1 工具格式定制

这是一个常被忽视但影响很大的细节：

- **OpenAI 模型**训练使用**基于 patch 的编辑格式**
- **Anthropic 的模型**训练使用**字符串替换格式**

> "Either model could use either tool, but giving it the unfamiliar one costs extra reasoning tokens and produces more mistakes."

所以在 Cursor 的 harness 中，每个模型都配了**它训练时使用的工具格式**——这不只是提示词调整，而是工具选择层面的优化。

### 3.2 Prompt 定制

不同模型有不同的行为特征：

| 特征 | OpenAI 模型 | Claude 模型 |
|------|------------|------------|
| 指令遵循 | 更 literal、更精确 | 更 Intuitive、更容忍不精确指令 |
| Prompt 风格 | 需要更结构化的指令 | 可以更自然随意 |

### 3.3 观察到的模型 quirk："Context Anxiety"

Cursor 团队观察到某个模型有一种行为特征，他们称之为 **context anxiety**：

> "As its context window filled up, it would start refusing work, hedging that the task seemed too big."

他们通过**Prompt 调整**减少了这种行为。

> 笔者注："Context Anxiety"是一个很有洞察力的命名。这种行为可能源于 RL 训练中对"超出上下文"信号的过度泛化。好的 harness 不只是提供工具，还要引导模型在边界情况下做出正确选择。

---

## 四、Mid-Chat 模型切换：跨模型对话的挑战

### 4.1 问题所在

当用户中途切换模型时，有两个挑战：

1. **上下文错位**：对话历史由另一个模型产生，对当前模型来说是 out-of-distribution
2. **缓存失效**：缓存按 provider 和 model 分别计算，切换 = 缓存未命中 = 更慢的第一轮

### 4.2 Cursor 的解决方案

**针对上下文错位：**
- 添加自定义指令，告诉模型它正在"mid-chat takeover"
- 引导模型不要调用当前工具集中没有的工具

**针对缓存失效：**
- 尝试在切换时**总结对话**，提供简洁摘要减少缓存惩罚
- 但如果用户深入复杂任务，摘要可能丢失重要细节
- **建议**：除非有明确理由，否则建议在一个会话中保持使用同一模型

**更好的替代方案——Subagent：**
- Subagent 从全新的上下文窗口开始，不存在切换问题
- Cursor 最近增加了直接用特定模型运行 subagent 的能力

---

## 五、未来展望：Harness 是多 Agent 协调的核心

Cursor 明确表达了他们的方向：

> "The future of AI-assisted software engineering will be multi-agent. Instead of running every subtask through a single agent, the system will learn to delegate across specialized agents and subagents: one for planning, another for fast edits, and a third for debugging, each scoped to what it does best."

关键洞察：

> "Making that work well is fundamentally a harness challenge. The system needs to know which agent to dispatch, how to frame the task for that agent's strengths, and how to stitch the results into a coherent workflow. The ability to orchestrate that kind of coordination will live in the harness rather than any single agent."

> 笔者注：这是对 harness 角色的根本性重新定义。在单 agent 场景下，harness 主要是"环境包装"；在多 agent 场景下，harness 变成了"编排层"。这种演进意味着 harness engineer 的核心技能要从"如何让单个 agent 少犯错"转向"如何让多个 agent 协作好"。

---

## 六、工程实践总结

### 6.1 测量驱动 vs 直觉驱动

| 方法 | 说明 | 适用场景 |
|------|------|---------|
| **离线基准** | CursorBench + 公开基准 | 快速标准化评估、新模型验证 |
| **在线 A/B 测试** | Keep Rate + LLM 满意度 | 真实用户场景、深层质量信号 |
| **异常检测** | 预期错误 vs 未知错误分类 + 动态基线 | 生产环境监控 |
| **自动化问题发现** | Cloud Agent + Log Analysis Skill | 可扩展的质量维护 |

### 6.2 关键设计原则

1. **Unknown Error = Bug**：无法分类的错误永远算 harness bug，强制触发告警
2. **基线按工具×模型计算**：不同组合的错误率天然不同
3. **Keep Rate > 人工评分**：用代码留存率代替主观评价
4. **工具格式匹配模型训练方式**：避免额外的 reasoning token 消耗
5. **Harness 是多 agent 编排的核心**：而非单 agent 的附属

### 6.3 适用边界

- 这个框架适合**已有一定规模的 agent 系统**（Cursor 的 harness 有大量模型、大量工具、大量用户）
- 早期项目可能没有足够的流量支撑 A/B 测试和 Keep Rate 统计
- 但异常检测告警和错误分类体系可以在早期就建立

---

**引用来源（原文）：**

> "We approach building the Cursor agent harness the way we'd approach any ambitious software product. Much of the work is vision-driven, where we start with an opinion about what the ideal agent experience should look like."

> "The first is the 'Keep Rate' of agent-generated code. For a given set of code changes that the agent proposed, we track what fraction of those remain in the user's codebase after fixed intervals of time."

> "Any unknown error represents a bug in the harness, and we treat it accordingly."

> "The future of AI-assisted software engineering will be multi-agent."

> "Making that work well is fundamentally a harness challenge. The system needs to know which agent to dispatch, how to frame the task for that agent's strengths, and how to stitch the results into a coherent workflow."

---

*本文是对 [Cursor 官方博客 Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness) 的深度解读与结构化分析，原文版权归属 Cursor AI。*