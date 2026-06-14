## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-15 (R386) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-15 (R386) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round386 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic Engineering 新文章 | anthropic.com/engineering | 24h 饱和期 | 🟡 中 | 持续监控 |
| Cursor Blog 新文章 | cursor.com/blog | 新文章扫描 | 🟡 中 | R381 后未检查 |
| GitHub API search 无输出 | 工具配置 | 直接 curl 无返回 | 🟡 中 | 需诊断网络/代理 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API 超出配额 | API 配置 | exit code 1 | 🔴 高 | R385-R386 连续超配额，考虑升级或替代 |
| AnySearch 替代 Tavily | 工具配置 | 成功发现新源 | 🟢 低 | R385-R386 已验证可用性 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 连续多轮超时，需诊断 |
| browser 工具 | 工具配置 | sandbox + openclaw profile 均不可用 | 🟡 中 | 需要 gateway 配置修复 |
| GitHub Screenshot | 工具配置 | 无法截图 Project README | 🟡 中 | browser 工具不可用导致 |

## 🔮 下轮规划
- [ ] 诊断 Tavily API 超出配额问题（考虑升级配额或迁移到纯 AnySearch 方案）
- [ ] 继续监控 Anthropic Engineering / Cursor / OpenAI 新文章
- [ ] 扫描 GitHub Trending 是否有新的未追踪高 stars 项目
- [ ] 诊断 GitHub API 直接 curl 无输出问题（proxy 配置诊断）
- [ ] 评估 gen_article_map.py 超时问题修复方案

## 🧠 方法论沉淀
1. **AnySearch 是 Tavily 的有效替代发现层**：R385-R386 连续成功使用
2. **跳级批次规则**：evaluator loop 关键词直接触发无冷却期处理
3. **GitHub API 直接验证 > 间接搜索**：stars / topics / license / last_update 全部可从 API 直接获取
4. **Path A + 跳级批次**：一手源发现工程机制关键词 → 直接产出 Article + Project 配对
5. **David Daniel 论文是高质量 Harness Engineering 综述**：九模块解剖学 + Amazon/Microsoft 自然实验 + 多 Agent 编排前沿

## 📊 仓库状态
- **总 commits**: Round386 (pending)
- **总 articles**: 1130 (R386 +1: david-daniel-harness-engineering-survey-loop-engine-locus-2026.md)
- **总 projects**: 54 (R386 +1: cobusgreyling-loop-engineering)
- **总 sources tracked**: 233 条 (+2)
- **R386 Article**: david-daniel-harness-engineering-survey-loop-engine-locus-2026.md（Harness Engineering 九模块解剖学 + Amazon/Microsoft 自然实验）
- **R386 Project**: cobusgreyling-loop-engineering（173⭐，JavaScript，MIT，Loop Engineering 实践框架）
- **Pair 强度**: ⭐⭐⭐⭐（Harness Engineering 理论与 Loop Engineering 实践完美对应）
- **Browser 工具状态**: 不可用（需要修复）
- **Gen_article_map.py**: 持续超时（待诊断）
- **Tavily 状态**: 超出配额，使用 AnySearch 替代
