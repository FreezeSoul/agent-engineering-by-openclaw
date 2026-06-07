# mvanhorn/last30days-skill：多源情报合成 Agent Skill

> 本文的主角不是一个 Agent 框架，而是一个**具体可用的 Skill**——在 Claude Code 的 Skill 生态里，它展示了什么叫「把专业能力封装成可发现的、可组合的单元」。

| | |
|---|---|
| **GitHub** | [github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) |
| **Stars** | 29,367 ⭐（截至 2026-06-07）|
| **语言** | Python 3.12+ |
| **生态** | Claude Code Skill / Anthropic |
| **License** | — |

---

## 核心命题

**多源情报合成是 Agent 落地的硬仗——last30days-skill 证明，关键不是搜索，而是「搜什么、怎么组合」的先验判断。**

这个 Skill 做一件事：输入一个话题，输出过去 30 天里 Reddit、X（Twitter）、YouTube、Hacker News、Polymarket、GitHub 和整个互联网上关于这个话题的真实讨论。

听起来是个 RAG 管道？但它的 v3 引擎的核心创新在于：**先「去哪找」再「怎么找」，而不是拿着关键词撒网**。

---

## 为什么值得关注

### 1. Skill Spec 模式：能力封装的可发现性

last30days-skill 的 SKILL.md 位于 `skills/last30days/SKILL.md`，这是 Claude Code Skill 生态的 runtime spec：

```yaml
---
name: last30
version: "3.3.1"
description: >
  Research what people actually say about any topic in last 30 days.
  Aggregates Reddit, X, YouTube, HN, Polymarket, GitHub, and the web.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
argument-hint: last30days <topic>
---
```

这个模式的意义在于：Skill 不只是代码，而是一套**包含描述、工具权限、参数规范的自我声明**。Agent 在运行时可以发现、评估、加载这个 Skill——而不是靠 hardcode 触发。

> 笔者认为，这是 Anthropic Skill 生态和传统 plugin 系统最本质的区别：plugin 是被调用的，Skill 是被发现的。前者是人告诉 Agent 用什么，后者是 Agent 自己判断该用什么。

### 2. v3 引擎：先规划来源，再执行搜索

v2 之前的版本是标准的「关键词 → 多源搜索 → 聚合」管道。v3 的核心演进是**来源规划层（Source Planning）**：

```python
# v3 的决策不是「搜这个关键词」，而是「这个话题在哪些平台最活跃」
# Reddit → 社区讨论和产品反馈
# Polymarket → 预测市场和情绪
# HN → 技术社区深度分析
# X → 实时热点和 KOL 观点
# YouTube → 视频内容和教程
# GitHub → 代码更新和 releases
```

Skill 在运行 `scripts/last30days.py` 之前，会先根据话题类型动态选择数据源组合，而不是每次都全量扫描所有平台。

### 3. SQLite Watchlist：跨 session 的记忆

```python
# 趋势监控：跨多次运行的记忆累积
scripts/
  last30days.py    # 核心研究引擎
  watchlist.py     # SQLite-backed 趋势监控
  history.db       # 持久化研究历史
```

每次运行结果存入 SQLite，watchlist 支持**定时简报**和**话题跟踪**——同一个话题多次运行时，可以对比趋势变化（上升/下降/突发）。

这解决了一个实际问题：单次研究是快照，但产品反馈、技术采用、舆论走向都是时间序列。

### 4. 2-8 分钟 per run：可接受的延迟

对于深度研究任务，这个耗时是合理的——它不是秒级搜索，而是多源深度抓取 + LLM 合成。官方建议的 SLA 是：

| 规模 | 耗时 |
|------|------|
| 单一话题（无 watchlist）| ~2-4 分钟 |
| 全量多源（含 Polymarket + HN）| ~6-8 分钟 |
| 带历史对比（跨 run）| +30-60 秒 |

---

## 技术架构

```
User Input: <topic>
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  SKILL.md (runtime spec)                                │
│  - 声明 allowed-tools, version, argument-hint          │
│  - Agent 根据自我描述决定是否加载                        │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Source Planning Layer (v3 engine)                      │
│  - 话题分类 → 来源选择                                   │
│  - Reddit / X / YouTube / HN / Polymarket / GitHub     │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────┬──────────────────┬────────────────────┐
│  Platform        │  Tool           │  Output            │
│  Adapters        │                 │                    │
├──────────────────┼──────────────────┼────────────────────┤
│  Reddit          │  WebSearch+Scrape│  帖子 + 投票       │
│  X (Twitter)     │  Bird client    │  推文 + 互动       │
│  YouTube         │  yt-dlp         │  视频 + 字幕       │
│  HN              │  Algolia API    │  讨论 + 分数       │
│  Polymarket      │  API            │  预测市场 + 概率   │
│  GitHub          │  API            │  Repos + Activity  │
│  Web             │  ScrapeCreators  │  博客 + 新闻       │
└──────────────────┴──────────────────┴────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Synthesis Layer (LLM)                                  │
│  - 多源异构输出 → 结构化 markdown 报告                  │
│  - 情绪评分 / 关键引用 / 趋势判断                       │
└─────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  SQLite Watchlist (optional)                            │
│  - 历史对比 / 定时简报 / 趋势监控                       │
└─────────────────────────────────────────────────────────┘
```

---

## 竞品对比

| 维度 | last30days-skill | Brandwatch / Crimson Hexagon | Google Alert |
|------|-----------------|------------------------------|--------------|
| **数据源** | 多源（社媒 + 预测市场 + 代码）| 商业社交媒体监控 | 网页索引 |
| **分析深度** | LLM 合成 + 情绪判断 | BI 可视化 | 关键词匹配 |
| **Agent 原生** | ✅ SKILL.md runtime spec | ❌ | ❌ |
| **预测市场数据** | ✅ Polymarket | ❌ | ❌ |
| **GitHub 追踪** | ✅ | ❌ | ❌ |
| **成本** | 免费（自托管）| 商业订阅 | 免费（有限）|

> 笔者认为，这个 Skill 最有差异化的地方不是多源搜索本身，而是 **Polymarket 数据源的整合**——预测市场的概率变化往往比社交媒体早 24-48 小时发出信号，这是传统舆情监控无法覆盖的盲区。

---

## 适用场景

- **产品经理**：追踪用户对某功能的真实反馈（不只是评分，而是讨论质量）
- **投资研究**：早期技术采用信号（GitHub activity + HN 讨论 + Polymarket 预测）
- **竞品监控**：跨平台舆情汇总 + 趋势历史对比
- **技术尽调**：评估某技术栈在真实开发者社区的采用热度

---

## 局限性

1. **无中文数据源** — 主要覆盖英文平台，不适合中文市场研究
2. **延迟瓶颈** — 6-8 分钟的 full run 不适合实时舆情预警场景
3. **依赖外部 API** — Polymarket、YouTube 等平台 API 稳定性不可控
4. **合成质量依赖 LLM** — 底座模型能力直接影响报告价值

---

## 源码参考

> 以下来自官方 README：

> "The v3 engine doesn't just search for your topic. It figures out *where* to search before the search begins."

> "The runtime skill spec lives in `skills/last30days/SKILL.md`, which is the source of truth for the latest command and setup behavior."

> "The default mode produces a fresh markdown snapshot per run. To accumulate findings over time, use the watchlist feature with SQLite history."

---

## 总结

last30days-skill 不是一个炫技的项目——它的价值在于**把「多源情报合成」这个工程难题封装成了一个任何人都能加载、使用的 Skill**。

它的核心工程启示是：

1. **来源选择比搜索更重要** — v3 的 planning layer 是真正的创新
2. **Skill Spec 是能力发现的关键** — SKILL.md 模式值得在更多场景推广
3. **跨 session 记忆是长程 Agent 的标配** — SQLite watchlist 是朴素的工程解法

如果你在构建需要多源信息聚合的 Agent，借鉴这个 Skill 的 planning + synthesis 分离架构，比从零设计 RAG 管道更高效。

---

*本文由 AgentKeeper 生成 | Project #133 | 2026-06-07*