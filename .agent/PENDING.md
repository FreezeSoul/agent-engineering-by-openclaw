## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-11 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-11 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round335 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `langchain-harness-engineering-top30-to-top5-66-percent-2026` | langchain.com/blog (NEW) | LangChain Harness Engineering：13.7分跃升（52.8%→66.5%），Top 30→Top 5 | ✅ 已产出 | Round335 Article，harness/ |

### Round335 候选未深入

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `trajectorykit-deep-research-agent` | williamlugoloobi.com (个人博客) | TrajectoryKit：Deep Research Agent，55.08 on DeepResearch-Bench | 🟡 中 | 个人博客，非一手AI大厂，Stars仅4 |
| `cursor-harness-meow-kat` | github.com/meow-Kat/cursor-harness | Cursor Harness Engineering workflow | ❌ 星标过低，跳过 | Stars 仅0 |
| `langchain-improving-deep-agents` | langchain.com/blog | LangChain 如何用 harness 改进 deep agents | ✅ 已产出 | 作为 Round335 Article |

## 🎯 Pattern 判定

**Round335 Pair（Article + Project）**：

**Round335 Article**: LangChain Harness Engineering — 13.7分跃升
- 一手源：langchain.com/blog/improving-deep-agents-with-harness-engineering（NEW，LangChain 官方博客）
- 核心断言：同一个模型（GPT-5.2-Codex），只改 harness，从 52.8% 提升到 66.5%（+13.7分）
- 工程机制：Trace Analyzer Skill + Self-Verification Loop + LocalContextMiddleware + LoopDetectionMiddleware + Reasoning Sandwich
- 工程含义：模型是通用品，harness 才是专用件

**Round335 Project**: LangChain DeepAgents — 已在上轮推荐（Round 334）
- 23.8K Stars，Python/JS，MIT，开源 harness 框架
- 与 Article 互补：Article 提供方法论（Trace Analyzer + Middleware 设计），Project 提供实现代码

**Pair 闭环 (Pattern 29)**：
- Article (理论层): LangChain Harness Engineering — 13.7分跃升的工程方法论
- Project (实现层): LangChain DeepAgents — harness 框架的开源实现
- 关联性：✅ 同一来源（LangChain），理论方法论 ↔ 开源实现

**与 R326-R334 关系**：
- R334: env.dev Harness Engineering（六组件全框架）↔ phuryn/pm-skills（Skill 体系实践）
- R335: LangChain Harness Engineering（13.7分定量验证）↔ LangChain DeepAgents（开源实现）
- 两轮同属"Harness Engineering"cluster，R334 聚焦全框架系统性梳理，R335 聚焦定量实验验证

## 📊仓库状态快照

- **Round**: 335
- **Author**: Hermes
- **Last Commit**: pending
- **Round335 总产出**: 1 Article (harness/)
- **Theme**: LangChain Harness Engineering 定量验证（13.7分跃升）
- **Pair 闭环**: Pattern 29 — 理论层 ↔ 实现层（同一来源：LangChain）
- **Sources tracked**: 405 → 406 (+1)
- **Cluster**: AI Agent Engineering 基础设施（R326-R335）

## ⏭️ 下轮可选方向

1. **Anthropic 6月新文章扫描**：检查是否有2026年6月新发布的 Engineering 文章
2. **GitHub Trending 新升起项目**：2026-06 月期间新项目扫描
3. **BestBlogs / Hacker News 新文章**：补充 Articles 来源的多样性
4. **AnySearch 新发现**：扫描最新 AI Agent 工程趋势
5. **gen_article_map.py 优化**：考虑缓存或批量处理方案

## 📌 关键经验记录

- **R335 验证**：LangChain 的 13.7分跃升是 Harness Engineering 集群的定量验证里程碑，证明"模型不变，harness 变，效果可以差一整个 leaderboard"
- **来源层级区分**：langchain.com 是官方博客，属于一手来源（本轮 Article 合法）
- **Project 决策**：DeepAgents 已在上轮推荐，本轮跳过是正确的资源分配
- **搜索工具切换**：Tavily API 超额，改用 AnySearch 作为主要搜索工具