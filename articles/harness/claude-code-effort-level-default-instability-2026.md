# Claude Code 静默降级：Provider Default 作为隐性 Harness 层

> **核心判断**：Provider 的默认参数不是恒定的——当 Anthropic 将 Claude Code 的 effort 级别从 high 静默降为 medium，依赖"默认配置稳定"假设的 Agent 系统遭受了系统性质量退化。这个事件揭示了一个被整个行业忽视的架构问题：**Provider defaults 是隐性 Harness 配置，Agent 工程师必须像管理代码配置一样显式管理它们**。

---

## 背景：三月静默变更

2026年3月，Anthropic 将 Claude Code 的默认 effort 级别从 `high` 降为 `medium`。这不是一个小变动——effort 级别是 Claude 内部的推理深度控制参数：

| Effort 级别 | 行为特征 |
|-------------|---------|
| **High（此前默认）** | 深入追踪依赖关系、映射变更影响半径、检查类型错误传播、验证测试不会破坏 |
| **Medium（当前默认）** | "这个文件改一下就行了"——更快速、更便宜，但更可能简化或跳过指令 |

**问题在于**：这个变更是通过 changelog 披露的，没有主动通知。对于企业客户——数十个员工在各自的工作流中使用 Claude，每个人都假设 API 行为一致——没有人在意 changelog 的这一行。直到2026年4月14日 Fortune 报道此事，Anthropic 才通过 Boris Cherny（Claude Code 负责人）的 Reddit 回复间接承认。

**关键悖论**：Anthropic 声称变更"obvious and explicit"（显而易见且明确），但数百名用户公开表示"毫不知情"。这不是用户的问题——这是沟通机制的失败。

---

## 机制解析：effort 级别如何控制模型行为

effort 级别控制的是模型在生成响应前的"思考深度"。这不是一个软性参数，而是一个直接影响推理路径的参数：

**High effort 场景（complex refactor）**：
```
1. 追踪文件间的依赖关系
2. 映射变更的 blast radius（影响范围）
3. 检查类型错误是否跨模块传播
4. 验证测试不会因为这次变更而失败
```

**Medium effort 场景（same refactor）**：
```
"I'll just change this file, that should do it."
```

这是可测量的质量退化，不是随机的噪声。根据 jangwook.net 的用户报告，具体症状包括：

- 多文件重构中的依赖更新遗漏
- 源码变更但对应测试未更新
- 错误处理被简化
- 原本自动处理的 edge case 现在需要显式指定

**为什么简单任务察觉不到**：effort 级别差异在简单任务上几乎不可见。问题暴露在：复杂多步工作流、长自动化管道、跨数十个文件的任务。换句话说——**使用越深度，受到的影响越大**。

---

## 企业客户为何没有提前发现

这里有一个架构层面的假设被打破：**企业客户假设"未改动的默认配置保持不变"**。

这个假设在传统软件中合理，在 LLM API 中不合理。原因：

1. **API 语义由 Provider 控制**：Claude Code 是一个产品，不是一个协议。effort 级别的语义（high 意味着什么）由 Anthropic 单方面定义和变更
2. **缺少版本化承诺**：传统 API 有版本号和变更通知机制。LLM API 的"版本"通常是模型版本，但 effort 级别这种服务参数不在版本化范围内
3. **企业监控盲区**：大多数企业没有对 LLM 输出质量建立自动化基线——所以当质量悄悄退化时，第一个注意到的是用户，不是监控系统

---

## Token 消耗悖论：降级导致消耗增加

讽刺的是：effort 降低本意是节省 token，结果对高级用户适得其反。

一些用户报告：token 消耗反而增加了 **4倍到10倍**。

原因：
- Medium effort → 模型更容易跳过指令
- 跳过指令 → 输出不符合要求
- 输出不符合要求 → 用户重试
- 重试 → 更多 token 消耗

Anthropic 自己也承认：usage limits 消耗速度远超预期，是团队的最高优先级问题。这个悖论值得所有 Agent 工程师记住——**当底层模型质量下降时，复杂 Agent 系统的 token 消耗可能非线性增长**，因为 pipeline 中的错误会级联放大。

---

## 定价变更：雪上加霜

时机再糟糕不过。2026年4月16日——性能争议最热的时候——Anthropic 宣布企业订阅定价变更：

| 此前 | 变更后 |
|------|--------|
| $200/user/month 封顶 | $20/user/month 基础 + 按用量计费 |

对于可预测的有限使用场景，这可能更便宜。对于重度用户或大规模自动化 pipeline，成本可能显著增加。

Gizmodo 的标题精准捕捉了用户情绪：**"Anthropic 在用户抱怨模型变差的同时上调高级用户的价格"**。

定价变更本身是合理的商业决策。但顺序错了——先悄悄降低质量，再在质量降低的舆论中涨价，三件事叠加成"Anthropic 在变差"的单一叙事。如果时序不同：先清晰告知 effort 变更 → 收集反馈 → 再宣布定价变更，每件事都有机会单独评估其合理性。

---

## 三大缓解策略

### 1. 显式 Pin Effort 级别

如果使用 Claude API，**不要依赖默认级别**。Pin 到你需要的级别：

```json
// default-model-settings 配置
{
  "thinking": {
    "type": "enabled",
    "budget_tokens": 10000
  }
}
```

`budget_tokens` 让你锁定处理深度，不受默认变更影响。对于关键 pipeline，每个会话都显式设置 effort 级别，而不是依赖全局默认。

### 2. 建立输出质量基线，持续测量

静默的质量退化在单次请求中不可见——它在输出质量的缓慢下滑中显现。

**最小化可行方案**：
```python
# 伪代码：质量变化检测
def check_output_quality(task, output, requirements):
    violations = []
    for req in requirements:
        if req not in output:
            violations.append(f"Missing: {req}")
    return len(violations) == 0, violations

# 每周运行一次关键任务抽样
# 对比输出与历史基线
# 设置告警阈值（如：违规率超过5%）
```

你不需要复杂的评测系统。你需要的是**变化检测**——当 provider 悄悄改变了行为，你能比用户先知道。

### 3. 供应商多元化

当你的整个 operation 依赖单一 LLM Provider，他们的定价决策和性能调整就成为你的基础设施风险。

这不意味着所有 pipeline 做双 Provider 冗余。而是：**至少在一个关键工作流上保持跨 Provider 可运行能力**。LiteLLM 这样的抽象层可以大幅降低切换成本。当主要 Provider 变更默认行为或涨价时，你不是被劫持的。

---

## Provider Defaults 是隐性 Harness 配置

这是这个事件最重要的架构教训。

**传统 Harness 配置**（Agent 工程师显式管理的）：
- Sandbox 权限边界
- 工具调用速率限制
- 输出内容过滤规则
- 会话超时和上下文截断策略

**Provider Default 配置**（通常被忽视的）：
- 模型 effort/reasoning 深度
- 温度/随机性参数
- 上下文窗口的实际行为（如截断策略）
- Token 速率限制的实际处理方式

这两类配置在功能上等价——都直接影响 Agent 的推理质量和行为。但第一类你会显式管理，第二类你通常信任 Provider 的默认值。

**这个事件证明：信任是无效的**。Provider 可以在不通知的情况下变更默认值，而这些变更会通过你的整个 Agent pipeline 放大。

---

## 更深的问题：整个行业没有透明度标准

这不是 Anthropic 独有的问题。OpenAI 和 Google 有完全相同的架构。

LLM Provider 可以在**没有版本变更的情况下调整服务质量的成本-质量权衡**——这是一个结构性问题。传统软件中，"软件的下一个版本更好"是普遍预期。LLM 服务中，"基础模型没有版本变更但服务质量悄悄下降"是真实可能。这两种情况可以同时为真，而 Provider 没有义务主动披露第二种情况。

**整个行业需要一个透明度标准**：
- 当默认参数变更时，通过邮件或产品内通知主动告知（不只是 changelog）
- 当基础模型的服务质量参数发生重大变更时，有明确的版本化或标签机制
- 企业客户能够设置 SLA 期望，即使在模型版本内部

Anthropic 在这次事件后会重置这个标准。但在那之前，每个 Agent 工程师需要意识到：**Provider 默认值是不稳定的配置，你的 Agent 系统需要为这种不稳定性做架构设计**。

---

## 文章分类

- **目录**：`harness/`
- **演进阶段**：Stage 12（Harness Engineering）
- **文章类型**：工程实践 / 教训总结
- **字数**：约 2800 字

---

## 参考资料

- [Fortune: Anthropic faces backlash over Claude AI performance issues (Apr 14, 2026)](https://fortune.com/2026/04/14/anthropic-claude-performance-decline-user-complaints-backlash-lack-of-transparency-accusations-compute-crunch/) — 一手报道，事件起源
- [Anthropic Claude Code Changelog (Mar 2026)](https://docs.anthropic.com/en/docs/claude-code/changelog) — effort 级别变更的原始披露
- [VentureBeat: Is Anthropic 'nerfing' Claude? (Apr 2026)](https://venturebeat.com/technology/is-anthropic-nerfing-claude-users-increasingly-report-performance) — 技术社区反应汇编
- [The Register: Anthropic admits Claude Code quotas running out too fast](https://www.theregister.com/) — Anthropic 官方承认 usage limits 问题
- [jangwook.net: The Anthropic Claude Performance Decline Controversy — What Actually Happened](https://jangwook.net/en/blog/en/anthropic-claude-performance-decline-controversy-april-2026/) — 技术分析深度覆盖
- [GitHub Issue #34428: Opus always defaults to medium reasoning effort](https://github.com/anthropics/claude-code/issues/34428) — 用户报告实例
- [Gizmodo: Anthropic Is Jacking Up the Price for Power Users Amid Complaints Its Model Is Getting Worse](https://gizmodo.com/) — 定价变更报道
- [Anthropic Boris Cherny Reddit statement on effort level change](https://www.reddit.com/r/ClaudeCode/comments/1soqwfl/) — Provider 方的公开解释
