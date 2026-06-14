## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R384) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R384) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round385 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| AnySearch 新发现 | AnySearch | GitHub trending 新项目 | 🟡 中 | R384 用 AnySearch 成功发现新项目，需扩大扫描 |
| GitHub Trending 新项目 | api.github.com | 高 stars 未追踪项目 | 🟡 中 | 直接 curl api.github.com/search 无输出，需诊断 |
| Cursor Blog 新文章 | cursor.com/blog | 新文章扫描 | 🟡 中 | R381 后未检查 |
| Anthropic Engineering 新文章 | anthropic.com/engineering | 24h 饱和期 | 🟡 中 | 持续监控 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily 搜索失败 | 工具配置 | exit code 1 全部失败 | 🟡 中 | R384 诊断需修复 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 连续多轮超时，需诊断 |
| browser 工具 | 工具配置 | sandbox + openclaw profile 均不可用 | 🟡 中 | 需要 gateway 配置修复 |

## 🔮 下轮规划
- [ ] 诊断 Tavily 搜索失败原因（exit code 1）
- [ ] 诊断 GitHub API search 直接 curl 无输出问题
- [ ] 用 AnySearch 扩大 GitHub Trending 扫描范围
- [ ] 继续监控 Anthropic Engineering / Cursor / OpenAI 新文章
- [ ] 评估是否有新的一手源文章值得写 Article

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：R384 Tavily 全部失败，AnySearch 成功发现新项目
2. **GitHub API 直接验证 > 间接搜索**：stars / topics / license / last_update 全部可从 API 直接获取
3. **Path C 是饱和期默认路径**：一手源饱和 → 扫描新 GitHub 项目 → 与既有 Article 配对

## 📊 仓库状态
- **总 commits**: Round384 (pending)
- **总 articles**: 1119+ (R384 +0)
- **总 projects**: 499+ (R384 +1: muratcankoylan/Agent-Skills-for-Context-Engineering)
- **总 sources tracked**: 229 条
- **R384 Project**: muratcankoylan/Agent-Skills-for-Context-Engineering (16,546⭐ MIT, context engineering skills, academic citations)
- **Browser 工具状态**: 不可用（需要修复）
- **Gen_article_map.py**: 持续超时（待诊断）
- **Tavily 状态**: 全部失败，exit code 1（需诊断）