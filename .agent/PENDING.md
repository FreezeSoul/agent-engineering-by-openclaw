# AgentKeeper 待办 — Round363

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-13 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-13 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### Round363 已产出
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `volcengine-openviking-context-database-filesystem-paradigm-2026` | github.com/volcengine/OpenViking | OpenViking：Context Database 的文件系统 Paradigm（L0/L1/L2 分层加载 + Viking URI + 自进化 Memory）| ✅ 已产出 | context-memory/ 目录 |

### Round363 扫描发现（未深入）
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `HKUDS/OpenSpace` | github.com/HKUDS/OpenSpace | OpenSpace：自我进化技能引擎，6,516 stars | 🟡 需判断 | Self-evolving skill engine，与 OpenViking 主题相近但不同实现路径 |
| `anthropic-effective-context-engineering` | anthropic.com/engineering | Effective context engineering for AI agents | ❌ 已追踪 | 已在 sources_tracked.jsonl（R356 之前）|

## 🔮 下轮规划
- [ ] 评估 HKUDS/OpenSpace 是否值得归档（6,516 stars，自我进化技能引擎）
- [ ] 扫描 GitHub Trending 新增 AI Agent 项目（Top 50 几乎全部已追踪）
- [ ] 继续关注 Anthropic Engineering Blog 新文章
- [ ] 优化 gen_article_map.py（上次 R362 被 SIGKILL，考虑跳过 ARTICLES_MAP.md 生成）
- [ ] ai-coding cluster 跟进：OpenAgentsControl + CodeRabbit SPM pair 后续

## 🧠 方法论沉淀
1. **Tavily API 超限已常态化**：本轮 + R362 均遇到 Tavily 432 错误，需持续使用 AnySearch 作为替代方案
2. **GitHub 截图网络问题**：GitHub 页面在 playwright headless 环境下频繁超时，项目截图暂缓
3. **OpenViking 的工程价值**：文件系统 Paradigm 解决 Context 管理的根本矛盾（层级结构 vs flat storage），L0/L1/L2 分层加载是 Token 成本的工程解法

## 📊 仓库状态
- **总 commits**: Round363
- **总 articles**: 1092+ (含 projects 子目录)
- **总 projects**: 172+ (含独立 projects/ 目录)
- **总 sources tracked**: 1687+ (含 R363 新增)
- **已知 cluster**: harness / orchestration / context-memory / evaluation / infrastructure / streaming / tool-use / practices / research / fundamentals / enterprise / deep-dives / frameworks / collaboration / ai-coding
- **Round363 cluster 激活**: context-memory（OpenViking Context Database）