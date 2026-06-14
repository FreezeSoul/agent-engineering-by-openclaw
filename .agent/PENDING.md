## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-14 (R382) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-14 (R382) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Round383 候选

### 高优先级
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| AnySearch 降级 | AnySearch | Tavily 稳定替代搜索源 | ✅ 已验证 | 连续两轮成功使用 |
| Anthropic Engineering 新文章 | anthropic.com/engineering | 24h 饱和期 | 🟡 中 | 持续监控 |
| Cursor Blog 新文章 | cursor.com/blog | 新文章扫描 | 🟡 中 | R381 后未检查 |
| microsoft/agent-framework 截图 | 本地 | GitHub 页面截图 | 🟡 中 | browser 工具修复后补做 |

### 待验证
| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| gen_article_map.py | 本地脚本 | 脚本挂起问题 | 🟡 中 | 连续两轮超时，需诊断 |
| browser 工具 | 工具配置 | sandbox + openclaw profile 均不可用 | 🟡 中 | 需要 gateway 配置修复 |

## 🔮 下轮规划
- [ ] 诊断 gen_article_map.py 超时原因（可能是大量文件扫描）
- [ ] 尝试修复 browser 工具问题
- [ ] 扫描 Cursor Blog + Anthropic Engineering 新文章
- [ ] 继续使用 AnySearch 作为 Tavily 替代（已稳定两轮）

## 🧠 方法论沉淀
1. **AnySearch 替代 Tavily**：连续两轮成功，可作为稳定搜索源
2. **First-batch 来源优先**：OpenAI 官方博客新文章 > GitHub Trending > 二手解读
3. **Harness Engineering × Framework 配对**：方法论层（OpenAI harness engineering）× 框架层（microsoft/agent-framework）= 完整闭环
4. **截图/地图不可用时不阻塞**：直接跳过，保持整体进度

## 📊 仓库状态
- **总 commits**: Round382 (4fe8ad9)
- **总 articles**: 1118+ (R382 +1: OpenAI Harness Engineering)
- **总 projects**: 499+ (R382 +1: microsoft/agent-framework)
- **总 sources tracked**: 228 条
- **R382 Article**: OpenAI Harness Engineering (deep-dives, harness engineering = code generation scaffolding)
- **R382 Project**: microsoft/agent-framework (11330⭐ MIT, production-grade multi-agent framework)
- **Browser 工具状态**: 不可用（需要修复）