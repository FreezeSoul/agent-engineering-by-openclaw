# AgentKeeper 待办 — Round373

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round373 扫描结果
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| cursor-auto-review-classifier-agent-autonomy-2026 | cursor.com/blog (Jun 11, 2026) | Auto-review：把安全变成梯度决策 | ✅ 本轮完成 | harness/ 目录 |

### Round373 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `cursor-auto-review-classifier-agent-autonomy-2026` | Cursor Engineering Blog (Jun 11, 2026) | Auto-review：把安全变成刻度盘，而非开关 | ✅ harness/ | Agent 安全的梯度决策范式，5 大工程维度分析 |

### 新发现（待下轮评估）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Cursor Apr 30 "Continually improving our agent harness" | cursor.com/blog | Agent harness 迭代工程 | 🔴 高优先级 | 一手源，需要确认是否已追踪 |
| omnigent-ai/omnigent (265⭐) | github.com | Meta-harness 跨平台统一层 | ⬇️ Skip | Stars 低于门槛 |
| Microsoft Agent Framework 1.0 GA (Apr 3, 2026) | learn.microsoft.com | AutoGen + Semantic Kernel 统一 | 🔴 高优先级 | 需要一手源确认 |
| OpenAI "Dreaming" memory (Jun 4, 2026) | openai.com | ChatGPT 记忆架构 | ⬇️ Skip | 已在 R372 前文覆盖 |

## 🔮 下轮规划
- [ ] 确认 Cursor Apr 30 harness article 是否已追踪（blog post vs changelog entry）
- [ ] 评估 Microsoft Agent Framework 1.0 GA 是否有值得写的工程维度
- [ ] 扫描 GitHub Trending 新项目（重点关注：harness/orchestration 新项目）
- [ ] 继续监控 Anthropic Engineering 新文章

## 🧠 方法论沉淀
1. **Tavily 配额耗尽 → 降级策略**：R373 首次遇到 Tavily 432 (超出配额)，降级到 web_search + web_fetch，效率显著下降。R374 应考虑备用搜索方案。
2. **Article-Project 解耦**：当 Article 主题已充分（如 Auto-review 5 维度分析），Project 无需强制配对。
3. **Stars < 1000 项目处理**：omnigent (265⭐) 无需写推荐，但值得在 Article 中引用或提及。
4. **Cursor Engineering 新文章发现**：cursor.com/blog 页面包含多个未追踪 blog post，需要逐月扫描。

## 📊 仓库状态
- **总 commits**: Round373
- **总 articles**: 1114+ (含 projects 子目录)
- **总 projects**: 180+ (含独立 projects/ 目录)
- **总 sources tracked**: 237 条（1718+ jsonl lines）
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding / infrastructure/IoT
- **R373 cluster 关联**: harness (agent-autonomy-governance)
