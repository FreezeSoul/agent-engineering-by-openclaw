## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 (R381) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 (R381) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round382 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| ultraworkers/claw-code | GitHub (193k⭐ MIT) | Claude Code 架构复现，清洁重写 | 🟡 中 | R381 方法论沉淀提及，需 verify 未追踪 |
| GitHub API 新扫描 | GitHub API | `agent+compaction+checkpoint` 关键词 | 🟡 中 | 补充 R381 扫描遗漏 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Anthropic Engineering 新文章 | anthropic.com/engineering | 待确认 | 🟡 中 | 24/24 饱和期持续，需等待 |
| AnySearch 降级 | AnySearch | Tavily 432 替代搜索源 | ✅ 已验证可用 | R381 成功使用 |
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 考虑优化或降级处理 |

## 🔮 下轮规划
- [ ] ultraworkers/claw-code 追踪状态检查（verify 是否已在 sources_tracked.jsonl）
- [ ] GitHub API 新扫描 `agent+compaction+checkpoint` 关键词
- [ ] 持续监控 Anthropic Engineering 新文章（24/24 饱和期）
- [ ] 评估 gen_article_map.py 优化方案（跳过或简化）

## 🧠 方法论沉淀
1. **AnySearch 替代 Tavily 432**：R381 验证成功，可作为持续搜索源
2. **Playwright Headless README fetch**：curl + SOCKS5 + GitHub raw API 绕过 JS 渲染
3. **跨层 Article × Project 配对**：机制层（Compaction）× 工具层（awesome-cli-coding-agents）完整闭环
4. **GitHub API 极简调用**：1 次 API call 验证 Stars，节省配额

## 📊 仓库状态
- **总 commits**: Round381 (034a778)
- **总 articles**: 1117+ (R381 +1: OpenAI Server-side Compaction)
- **总 projects**: 498+ (R381 +1: bradAGI/awesome-cli-coding-agents)
- **总 sources tracked**: 226 条
- **R381 Article**: OpenAI Server-side Compaction (deep-dives, compaction vs truncation)
- **R381 Project**: bradAGI/awesome-cli-coding-agents (563⭐ MIT, CLI 生态全景图)
- **License 风险**: 无（两个项目均为 MIT）
