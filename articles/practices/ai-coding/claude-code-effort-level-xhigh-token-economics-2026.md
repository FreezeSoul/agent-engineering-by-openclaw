# Claude Code 2.1 的 Effort Level 系统：为什么 xhigh 是 AI Coding 成本控制的关键转折点

> **核心结论**：Claude Code 2.1 将 effort level 从 4 级扩展到 5 级（low/medium/high/**xhigh**/max），并将其中的 xhigh 设为所有计划的默认级别。这不只是一个参数调整——它重新定义了 AI Coding 工具中「推理深度」与「Token 消耗」之间的契约关系，配合 Task Budgets 和 Self-Verification，构成了一套完整的长程 Agent 成本控制机制。

---

## 一、背景：Claude Code 为何要在 effort level 上做文章

在 Claude Code 2.1 之前，Claude Code 的 effort level 只有 4 级：low、medium、high、max。开发者通常要么用 high（默认，适合大多数任务），要么用 max（复杂任务，但 Token 消耗大）。这两者之间的gap，在 2026 年的生产工作流中变得越发明显：

- **high 不够用**：复杂的多文件重构、系统设计任务，high effort 常常在关键路径上「偷懒」，产出质量不如预期
- **max 太贵**：对于大多数需要「比 high 更认真一点」的任务，max 的 Token 消耗是 high 的 3-4 倍，但质量提升并不成比例

Claude Opus 4.7 的发布（2026年4月14日）引入了 xhigh effort level，填补了这个空白。与此同时，Claude Code 2.1 随之发布，**将 xhigh 设为所有计划的新默认**，覆盖 Pro、Max、Teams 和 Enterprise。

---

## 二、核心机制：五级 Effort Level 的架构解析

### 2.1 五级量表的设计意图

Opus 4.7 的 effort 量表现在有 5 个级别：

| 级别 | 定位 | 适用场景 |
|------|------|---------|
| **low** | 最小推理 | 格式化、分类、简单提取 |
| **medium** | 标准推理 | 常规问答、短文档生成 |
| **high** | 增强推理（原来的默认） | 明确范围的标准编码任务 |
| **xhigh** | **深度推理（现为默认）** | 复杂重构、多文件设计、安全敏感代码 |
| **max** | 极限推理 | 已知的高难问题、批量容许延迟的场景 |

**关键理解**：这 5 个级别控制的不是「模型能力」，而是**推理深度策略**。在 Opus 4.7 中，Extended Thinking（扩展思考）模式已被 Adaptive Thinking（自适应思考）取代——模型自己决定推理多长时间，effort 参数的作用是「偏向」这个决策：低 effort 时模型倾向于少思考，高 effort 时倾向于多思考。

### 2.2 xhigh 在量表中的位置

xhigh 的设计目标是「接近 max 的质量，代价显著低于 max」。根据 Anthropic 官方数据：

> "xhigh approaches 75% of max on complex coding tasks; max pushes higher but burns significantly more tokens for marginal gains on most workloads."

这句话背后有一个重要的基准对比（同样来自 Anthropic 官方发布）：

> "low-effort Opus 4.7 is roughly equivalent to medium-effort Opus 4.6."

这意味着**整个 effort 量表上移了半级**：4.7 时代的 high，大致相当于 4.6 时代的 xhigh。因此将默认级别从 high 升级到 xhigh，实际上是让大多数用户在**不额外付费的情况下，获得略高一个档次的推理深度**。

### 2.3 xhigh 与 Token 消耗的经济学

这是最重要的工程现实：

> **xhigh 在长程 Agent 运行中大约使 Token 消耗翻倍（相对于 high）。**

这个「翻倍」有两个来源：

1. **推理 Token 增加**：更深的思考本身产生更多中间 Token
2. **Opus 4.7 的新 Tokenizer**：4.7 使用了更新后的 tokenizer，对相同输入产生的 Token 数量是 4.6 的 1.0–1.35 倍（因内容类型而异）

两者叠加，相同的代码工作量从 Opus 4.6/higherffort 迁移到 Opus 4.7/xhigh effort，Token 消耗增加约 **1.35–2.0 倍**。

对于一个每月在 Claude Code 上花费 $1,000 的团队，这意味着月度账单可能变为 $1,350–$2,000。

---

## 三、自适应思考模式：Effort Level 的底层逻辑变了

在 Opus 4.6 时代，Effort Level 与「是否启用扩展思考」有一定对应关系：high 通常不启用，max 启用 Extended Thinking（固定的长推理链）。

**在 Opus 4.7 中，这个对应关系被打破。** Extended Thinking 模式已被移除，取而代之的是 Adaptive Thinking——模型根据当前上下文动态决定推理长度，effort 参数只是一个偏向信号。

这带来一个关键变化：

- **旧模式（max + Extended Thinking）**：强制模型走完整的推理链，不管问题是否真的需要
- **新模式（xhigh/max + Adaptive Thinking）**：模型自己判断需要多少推理，effort level 调整的是「判断阈值」

这对开发者的意义是：**不要把 xhigh 理解为「更长的固定思考」，而应理解为「更倾向于深度思考的策略」**。对于明确、范围清晰的问题，xhigh 的自适应思考不会无谓拉长；但对于模糊、涉及多文件、存在隐藏复杂性的问题，xhigh 的深度策略会显著提升输出质量。

---

## 四、Claude Code 2.1 的配套机制：Task Budgets 与 Self-Verification

effort level 的提升解决的是「推理深度」问题，但无助于解决「Token 总量失控」问题。Claude Code 2.1 同时引入了两个配套机制：

### 4.1 Task Budgets（公共 Beta）：为 Agent 循环设置软上限

**问题背景**：在 Claude Code 2.1 之前，Agent 运行没有机制告知模型「你还有 N 个 Token 可用，请相应规划」。模型会一直调用工具直到达到 max_tokens 上限或遇到硬错误。这意味着两种常见失败模式：

- 预算耗尽但任务未完成（没有 graceful handoff）
- 达到 max_tokens 时任务被截断，中途放弃

**Task Budgets 的设计**：设置一个软 Token 上限，模型在接近这个上限时会主动调整行为——优先完成核心路径、提前总结结论、为未完成部分提供交接说明，而不是直接截断。

```python
# Task Budget 用法示意（Claude Code 内）
/task-budget 50000  # 设置 50k token 的软上限
```

这是一个「让模型知道边界」的机制，区别于硬截断的 max_tokens 参数——模型可以提前规划，而不是被动中断。

### 4.2 Self-Verification：改变「完成」的契约

Self-Verification 在 Claude Code 2.1 中默认启用。它的核心改变是：**模型不再只根据「是否执行了工具调用」来判断任务完成，而是主动验证输出的正确性**。

具体表现：

- 在声称完成之前，模型会重新审视关键实现
- 对于单元测试，会实际运行验证
- 如果验证失败，会主动重试或报告问题

这改变了用户与 Claude Code 之间的隐式契约：**从「工具调用停止 = 任务完成」变为「输出经过验证 = 任务完成」**。在 xhigh effort 下，Self-Verification 通常会消耗额外 Token，但它也减少了「看起来完成但实际有问题」的情况——从整个工作流看，可能是净节省。

---

## 五、/ultrareview： Effort 系统之外的质量门

### 5.1 定位

/ultrareview 是 Claude Code 2.1 引入的专属代码审查命令，设计意图是为合并门（merge gate）提供一个高质量的最终审查。它的核心特点：

- **多轮次（Multi-pass）**：不是单次 Review Pass，而是多角度、多轮次的审查
- **主动寻找的东西**：测试未覆盖的边界情况、安全漏洞（通常来自组件交互而非单行代码）、异步/并发代码的状态管理 Bug、Refactor 后行为不一致的问题

```bash
# 在 Claude Code 会话中调用
/ultrareview
# 或针对特定文件
/ultrareview src/auth/login.ts
```

### 5.2 与 Effort Level 的关系

这里有一个设计上的微妙对应关系：

- **xhigh effort** 控制的是「生成代码时的推理深度」
- **/ultrareview** 提供的是「生成代码后的审查深度」

两者组合，形成了 **「深生成 + 深验证」** 的双重质量保障。在 Claude Code 的典型工作流中，这意味着：xhigh 生成代码 → Self-Verification 初次验证 → /ultrareview 最终审查。三者分别在不同的阶段发挥作用。

### 5.3 限制与已知问题

- Pro 和 Max 用户每个账单周期有 3 次免费 ultrareview，之后按标准 Opus 4.7 Token 费率收费（Launch 期政策，可能调整）
- Claude Code 文档建议：对于机械性改动（重命名、格式化）和迭代中的 Work-in-Progress，不值得用 /ultrareview

---

## 六、工程实践建议：如何在团队中落地 xhigh

### 6.1 立即行动：检查你的 Token 消耗

如果你的团队从 4 月 14 日之后没有调整过 Claude Code 配置，**你已经在使用 xhigh 默认级别**。第一步是确认这个变化对你的 Token 消耗的影响：

1. 查看 Claude Code 的 `/usage` 命令（新增）：`/usage breakdown` 可以显示什么在驱动你的 Token 消耗
2. 对比上周与本周的 Token 消耗趋势
3. 如果增幅超过预期，调整策略（见 6.2）

### 6.2 分级路由策略

不是所有任务都需要 xhigh。用分级路由可以让成本可控：

| 任务类型 | 推荐 Effort | 理由 |
|---------|-----------|------|
| 单文件 Bug 修复 | high | 范围明确，高 effort 浪费 |
| 多文件重构 | xhigh | 跨文件一致性需要更深度推理 |
| 全新模块设计 | xhigh 或 max | 设计阶段的深度推理价值高 |
| 简单格式化、重命名 | medium 或 low | 无需深度推理 |
| 生产安全关键代码审查 | max + /ultrareview | 质量优先 |

### 6.3 Task Budgets 的配置建议

对于长程 Agent 任务（如夜间批量代码生成），建议设置 Task Budget：

```
# 预算估算逻辑：
# - 估算任务的 Token 上限（基于历史经验）
# - 预留 15-20% 作为缓冲（模型需要空间做 Self-Verification）
# - 实际设置 = 估算上限 × 0.80
/task-budget <calculated_value>
```

### 6.4 监控与迭代

Claude Code 2.1 的 `/usage breakdown` 是新的观测工具。定期查看这个输出，识别 Token 消耗异常高的会话，并分析原因——是高 effort 任务本身 Token 密集，还是模型在某些任务上过度推理。

---

## 七、为什么说 xhigh 是「成本控制的关键转折点」

**因为它改变了默认行为**。

在 Claude Code 2.1 之前，工具的默认行为是「适中推理」。现在，默认行为变成了「深度推理」。这个变化发生得悄无声息——没有显式通知，没有费用警告，现有用户自动升级。

这与 Web 2.0 时代 CDN 费用暴涨的情况有相似之处：功能看起来是「免费升级」，但账单会在几个月后告诉你真相。

对于 AI Coding 的工程负责人来说，这意味着：

1. **必须主动管理 Effort Level 配置**：将 effort level 视为一种资源预算，而不是固定默认值
2. **Task Budgets 是必需的**：在 xhigh 成为默认的时代，没有 Token 上限机制的团队将面临不可预测的费用波动
3. **Self-Verification 的「完成」契约变化需要重新校准 CI/CD 预期**：模型声称完成后，可能还有额外验证在进行

> **笔者认为**：xhigh 的出现，本质上是 AI Coding 工具从「快速原型工具」向「可信赖的开发助手」演进的标志。代价是成本结构的根本性改变——2025 年的 Claude Code $500/月，在 2026 年的 xhigh + Opus 4.7 tokenizer 下，可能只够一半的工作量。团队需要重新建模 AI Coding 的 ROI。

---

## 一手资源

- [Introducing Claude Opus 4.7 (Anthropic)](https://www.anthropic.com/news/claude-opus-4-7)
- [Claude Code Week 16 · April 13–17, 2026 (Claude Code Docs)](https://code.claude.com/docs/en/whats-new/2026-w16)
- [Claude Code Week 17 · April 20–24, 2026 (Claude Code Docs)](https://code.claude.com/docs/en/whats-new/2026-w17)
- [Claude API Effort Parameter (Claude Platform Docs)](https://platform.claude.com/docs/en/build-with-claude/effort)
