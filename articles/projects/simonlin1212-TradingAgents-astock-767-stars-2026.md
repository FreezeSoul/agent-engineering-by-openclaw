# simonlin1212/TradingAgents-astock：A股多 Agent 投研框架

**stars**: 767 | **language**: Python | **created**: 2026-05-13 | **homepage**: https://arxiv.org/pdf/2412.20138

## 概述

[TradingAgents-astock](https://github.com/simonlin1212/TradingAgents-astock) 是一个 **A股多 Agent 投研框架**，基于 TradingAgents 深度改造，适配 A 股数据源（龙虎榜、游资、解禁等）。核心机制：7 位 AI 分析师基于 A 股规则的辩论决策，支持多空讨论、风险评估。

## 核心机制

**7 位分析师辩论决策**：
- 每位分析师扮演不同角色（基本面分析师、技术分析师、情绪分析师等）
- 基于 A 股特有规则（涨停板、T+1、游资手法等）进行辩论
- 最终输出多空决策 + 风险评分

**A股特色数据源**：
- **龙虎榜**：营业部席位、机构席位异动
- **游资追踪**：著名营业部操盘手法
- **解禁数据**：限售股解禁压力
- **涨停板分析**：连板股、炸板股情绪

## Multi-Agent 协作架构

TradingAgents-astock 展示了 Multi-Agent 在垂直领域（金融投研）的应用：

```python
# 7 Agent 协作伪代码
analysts = [
    FundamentalAnalyst(),      # 基本面
    TechnicalAnalyst(),        # 技术面
    SentimentAnalyst(),        # 情绪面
    LimitUpAnalyst(),          # 涨停板
    JYCapitalAnalyst(),        # 游资
    UnlockDataAnalyst(),       # 解禁
    RiskAssesssor()            # 风险评估
]

debate_result = multi_agent_debate(analysts, stock_query)
```

## 与 OpenAI Codex / Claude Code 的差异

| 维度 | TradingAgents-astock | OpenAI Codex / Claude Code |
|------|---------------------|--------------------------|
| **任务类型** | 金融投研分析 | 通用软件工程 |
| **多 Agent 模式** | 辩论式协作 | 任务分解执行 |
| **数据源** | A 股特色数据 | 代码仓、互联网 |
| **输出** | 投资建议 | 代码、文档 |

## 主题关联

- **Multi-Agent 协作**：与 `multi-agent-orchestration-four-paradigms/` 文章形成「辩论式 vs 分层式」编排对照
- **金融 AI Agent**：与 `tradingagents-multi-agent-trading-framework/` 项目（79K Stars）形成专业 vs 通用的层级对照
- **垂直领域 Agent**：展示了 AI Agent 在金融、医疗、法律等垂直领域的定制化路径

## 延伸阅读

- [multi-agent-orchestration-four-paradigms](/articles/orchestration/multi-agent-orchestration-four-paradigms-anthropic-swarms-2026.md) — Multi-Agent 编排四大范式
- [daao-difficulty-aware-orchestration](/articles/orchestration/daao-difficulty-aware-agentic-orchestration-2509-11079.md) — 难度感知的 Agent 编排
- [anthropic-claude-code-auto-mode](/articles/harness/anthropic-claude-code-auto-mode-classifier-based-permission-2026.md) — Claude Code Auto Mode 权限架构
