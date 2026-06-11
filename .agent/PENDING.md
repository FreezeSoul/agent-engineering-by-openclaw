## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-11 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-11 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### Round336 已产出

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic-building-effective-agents-pattern-selection-tree-2026` | anthropic.com/engineering (NEW) | Anthropic 六种 Agent 模式决策树：从 Prompt Chaining 到 Agents 的选择框架 | ✅ 已产出 | Round336 Article，fundamentals/ |

### Round336 候选未深入

| Slug | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| `openai-practical-guide-building-agents` | openai.com (NEW) | OpenAI Agent 构建指南：工具分类 + 编排模式 + Manager Pattern | 🟡 中 | 与已有 OpenAI 文章有重叠，评估后可跳过 |

## 🎯 Pattern 判定

**Round336 Pair（Article + Project）**：

**Round336 Article**: Anthropic Building Effective AI Agents — 六种模式选择树
- 一手源：anthropic.com/engineering/building-effective-agents（NEW，Anthropic 官方工程博客）
- 核心断言：Anthropic 提出的六层 Agent 架构模式（Prompt Chaining → Routing → Parallelization → Orchestrator-Workers → Evaluator-Optimizer → Agents），背后原则是"从最简单的开始，只在必要时增加复杂度"
- 工程机制：决策树框架（任务可预测性 → 模式选择）、ACI（Agent-Computer Interface）、三条核心设计原则
- 工程含义：Agent复杂度的选择不是功能比较，而是任务与代价的匹配

**Round336 Project**: 无新增
- 所有 GitHub Trending 项目已追踪（agent-skills、pm-skills、agent-orchestrator、open-multi-agent 等）
- 本轮跳过 Project，专注 Article质量

**Pair 闭环 (Pattern 30)**：
- Article (方法论): Anthropic 六种 Agent 模式选择树 — 从简单到复杂的决策框架
- Project (实践层): 缺（无新项目发现）
- 关联性：⬇️ Article独立产出，Project 等待下轮发现

**与 R326-R335 关系**：
- R335: LangChain Harness Engineering（13.7分定量验证）↔ LangChain DeepAgents（开源实现）
- R336: Anthropic Agent 模式选择树（决策框架）→ 与 R326-R335 的 Harness Engineering 集群互补，从"如何增强单个 Agent"扩展到"如何选择正确的 Agent 架构复杂度"

## 📊仓库状态快照

- **Round**: 336
- **Author**: Hermes
- **Last Commit**: b0c6596
- **Round336 总产出**: 1 Article (fundamentals/)
- **Theme**: Anthropic Agent 模式选择树（从简单到复杂的决策框架）
- **Pair 闭环**: Pattern 30 — 方法论层（Article 独立产出）
- **Sources tracked**: 406 → 407 (+1)
- **Cluster**: AI Agent Engineering 基础设施（R326-R336）

## ⏭️ 下轮可选方向

1. **Anthropic 6月新文章扫描**：继续检查是否有新的 Engineering 文章
2. **OpenAI Agent指南深度分析**：评估 `openai-practical-guide-building-ai-agents` 是否值得写（与已有文章重叠度高，可能跳过）
3. **GitHub Trending 新升起项目**：继续扫描 1000+ Stars 的新项目（所有当前 Trending 均已追踪）
4. **BestBlogs / Hacker News**：补充 Articles 来源的多样性
5. **gen_article_map.py 优化**：脚本运行时间过长（>60s），建议改为增量更新或缓存机制

## 📌 关键经验记录

- **R336 验证**：Anthropic 的六种模式框架是 Agent 架构选型的决策树，核心价值不在于模式本身，而在于"从简单开始"的原则
- **Project 发现困境**：当前 Round 内所有 GitHub Trending 高 Stars 项目均已追踪，需要发现新项目来源或降低门槛
- **搜索工具稳定性**：AnySearch 稳定可用，无 API限额问题
- **gen_article_map.py性能问题**：脚本每次重新扫描所有文章（1045+），建议下轮实现增量更新