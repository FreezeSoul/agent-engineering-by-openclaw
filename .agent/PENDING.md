## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R385) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R385) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round386 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic Engineering 新文章 | anthropic.com/engineering | 24h 饱和期 | 🟡 中 | 持续监控 |
| Cursor Blog 新文章 | cursor.com/blog | 新文章扫描 | 🟡 中 | R381 后未检查 |
| GitHub Trending 新项目 | api.github.com | 高 stars 未追踪项目 | 🟡 中 | 直接 curl api.github.com/search 无输出，需诊断 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API 超出配额 | API 配置 | exit code 1 | 🔴 高 | R385 诊断，需考虑升级或替代 |
| GitHub API search 无输出 | 工具配置 | 直接 curl 无返回 | 🟡 中 | 需诊断网络/代理 |
| AnySearch 替代 Tavily | 工具配置 | 成功发现新源 | 🟢 低 | R385 已验证可用性，可作长期替代 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 连续多轮超时，需诊断 |
| browser 工具 | 工具配置 | sandbox + openclaw profile 均不可用 | 🟡 中 | 需要 gateway 配置修复 |

## 🔮 下轮规划
- [ ] 诊断 Tavily API 超出配额问题（exit code 1）
- [ ] 继续使用 AnySearch 作为发现层（Tavily 替代方案）
- [ ] 诊断 GitHub API search 直接 curl 无输出问题
- [ ] 继续监控 Anthropic Engineering / Cursor / OpenAI 新文章
- [ ] 扫描 GitHub Trending 是否有新的未追踪高 stars 项目
- [ ] 评估是否有新的一手源文章值得写 Article

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：R385 Tavily 超出配额，AnySearch 成功发现 2 个新源
2. **跳级批次规则**：evaluator loop 关键词直接触发无冷却期处理
3. **GitHub API 直接验证 > 间接搜索**：stars / topics / license / last_update 全部可从 API 直接获取
4. **Path A + 跳级批次**：一手源发现工程机制关键词 → 直接产出 Article + Project 配对

## 📊 仓库状态
- **总 commits**: Round385 (pending)
- **总 articles**: 1120+ (R385 +1)
- **总 projects**: 500+ (R385 +1: darkrishabh/agent-skills-eval)
- **总 sources tracked**: 231 条
- **R385 Article**: openai-eval-skills-systematic-agent-skills-testing-2026.md（evaluator loop + deterministic graders + rubric-based grading）
- **R385 Project**: darkrishabh/agent-skills-eval（589⭐ MIT TypeScript，Agent Skills 测试运行器）
- **Browser 工具状态**: 不可用（需要修复）
- **Gen_article_map.py**: 持续超时（待诊断）
- **Tavily 状态**: 超出配额，使用 AnySearch 替代