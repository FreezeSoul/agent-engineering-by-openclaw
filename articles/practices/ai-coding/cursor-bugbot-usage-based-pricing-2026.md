# Cursor Bugbot 定价策略转型：从席位订阅到用多少付多少

> **核心观点**：Cursor 将 Bugbot 从 $40/月/席位的固定订阅转为纯使用量计费（$1.00-$1.50/PR），这不仅是定价策略的调整，而是 AI 编程工具市场走向成熟后、企业级采购逻辑从「人头预算」向「结果导向」转变的标志性事件。

---

## 背景：Seat-based 订阅的局限性

Seat-based 定价（按人头收费）是 SaaS 产品的经典模型，优势在于收入可预测、管理简单。但对 AI Coding Agent 这类产品，Seat-based 模型有几个结构性问题：

1. **使用分布不均**：一个团队里真正高频使用 Bugbot PR 审查的，可能只有 2-3 人，但需要为 10 人买席位
2. **价值难以归因**：企业很难向财务证明「买了 10 个席位，具体产出了多少 bug 修复」
3. **规模化悖论**：团队越大、自动化程度越高，单席位价值越被摊薄

对于 Cursor 来说，$40/席/月意味着年营收约为 $480/席，但实际使用数据显示「平均每次运行成本 $1.00-$1.50」——如果一个工程师每月审查 30 个 PR，实际成本只有 $30-$45，是席位费的 75%-100% 被浪费了。

---

## 新定价结构：Usage-based Billing

从 2026 年 6 月 8 日起（新客户立即生效），Bugbot 切换到纯使用量计费：

| 维度 | 旧模型 | 新模型 |
|------|--------|--------|
| **计费方式** | $40/月/席位 | $1.00-$1.50/PR（按大小和复杂度） |
| **Teams 账单来源** | 按席位数固定月费 | On-demand spend |
| **Individuals 账单** | 包月订阅 | Included usage + 超量按需 |
| **现有客户** | 年约到期后切换 | 可提前在 dashboard 切换 |

**关键数据**：Cursor 内部运行显示，Bugbot 高努力模式比默认模式多发现 35% 的 bug，但解决率保持在 80%——这意味着企业可以通过调整 effort level 来控制成本与质量的平衡。

---

## Effort Level：成本与质量的量化控制

这是新定价模型最有意思的部分。Cursor 引入了 Effort Level 概念，让企业可以动态调整 Bugbot 的「深度」：

- **Default Effort**：80% 的 bug 在 merge 前被解决（现有行为）
- **High Effort**：多花 35% 的成本，但能发现 35% 更多的 bug

```python
# 用户可以配置自定义逻辑动态决定 effort level
bugbot.configure({
    'effort': 'auto',  # 或 'default' / 'high' / custom function
    'dynamic_effort': lambda pr: 'high' if pr.size > 500 else 'default'
})
```

这是一个典型的**成本-质量权衡显式化**设计：原来这个权衡是隐式的（买更多席位 = 更多覆盖），现在变成了用户可以直接控制的参数。

---

## 这意味着什么

### 对 Cursor

从财务角度看，Usage-based 模型可能带来更高的 ARPU（每用户平均收入），因为高频用户会贡献更多收入，同时低频用户不会因为「感觉贵」而流失。但代价是收入波动性增加——这对上市公司很重要，对成长期公司则是融资时需要解释的变量。

### 对市场

这是 AI Coding 工具定价的一个转折点。GitHub Copilot 的seat-based 模型面临同样压力——当企业开始算「每个 PR 多少成本」时，席位订阅的溢价就显得不合理了。

> **笔者判断**：未来 12-18 个月内，AI Coding 工具的主流定价将从 seat-based 转向 outcome-based（按结果计费），Bugbot 的转型是这个趋势的早期信号。

---

## 关联项目

与本次主题相关的高价值项目：

| 项目 | Stars | 关联性 |
|------|-------|--------|
| [shannhk/hermes-agent-control-room](https://github.com/shannhk/hermes-agent-control-room) | 380 | 多 Agent 系统的控制平面，Pricing/Harness 设计参考 |
| [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) | 970 | Agent Harness 工程知识库，包含定价策略讨论 |

---

## 引用来源

1. [Updates to Bugbot for Teams and Individuals – Cursor](https://cursor.com/blog/may-2026-bugbot-changes)
   > "The average Bugbot run costs $1.00-$1.50, depending on PR size and complexity"
   > "Bugbot with high effort finds 35% more bugs while resolution rate stays constant at 80%"

2. [Cursor in Jira – Changelog](https://cursor.com/changelog/05-19-26)
   > "Cursor is now available in Jira... When the agent finishes, Jira shows completion updates and includes a link to the pull request."

---

*归档目录：`articles/practices/ai-coding/`*
*来源：cursor.com/blog/may-2026-bugbot-changes*
*写作时间：2026-05-20*