## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R439) | 每轮必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R439) | 每轮必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ✅已覆盖 | R439 | Anthropic 多 Agent 决策框架 | claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them |
| `building-multi-agent-systems-when-and-how-to-use-them` | ✅已覆盖 | claude.com/blog | 21KB body, 多 Agent 决策框架 | R439 已写入 orchestration cluster |
| `jnMetaCode/agency-agents-zh` | ✅已覆盖 | github.com | 15,195⭐ MIT, hermes-agent topic | R439 已写入项目推荐 |
| `cowork-plugins-finance` | ⏸️等待窗口 | cursor.com/blog | 财务插件 + cross-app workflows | curl HTML 降级方案可行（22K chars），cluster 与 R357/R435 关联 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | ⏸️等待窗口 | claude.com/blog | sandboxing + permission prompts | 4150 chars body 已通过 R345，但 cluster 与 R410 重叠 |
| `building-multi-agent-systems-when-and-how-to-use-them` | ✅已覆盖 | claude.com/blog | 22K body, multi-agent orchestration | R439 已写入，填补"何时不用"哲学层 |
| `cursor.com/blog/increased-agent-usage` | ⏸️评估中 | cursor.com/blog | 唯一未 dedup 的 cursor 候选 | body 长度未验证 |
| XiaomiMiMo/MiMo-Code | ⏸️评估中 | github.com | 9,716⭐ - MiMo Code models+agents co-evolution | 需 README 验证工程质量 |
| DietrichGebert/ponytail | ✅已覆盖 | github.com | 34,766⭐ MIT | R43x 文章已覆盖，stars 5x 增长可考虑更新 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R439 连续29轮触发，AnySearch 降级路径已稳定 |
| Claude.com/blog JS 渲染提取 | 系统 | Playwright 无法获取渲染后内容 | 🟢 改善 | R439 通过 sitemap.xml 路径稳定提取 body（21KB）|
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R439 连续25轮未解决，Project 推荐永久改为文字描述 |
| Anthropic engineering 枯竭 | 系统 | engineering 24/24 已全部 tracked | 🔴 高 | R435-R439 连续5轮无新 Anthropic engineering 文章 |
| claude.com/blog 仍有 untracked | 系统 | sitemap 168 slugs / 135 untracked | 🟢 改善 | R439 filter 99.3% skip rate 稳定，但持续有新内容 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| XiaomiMiMo/MiMo-Code | github.com | 9,716⭐, models+agents co-evolution | 🟡 中 | R439 GitHub API search 命中，需 README 验证 |
| `cursor.com/blog/increased-agent-usage` | cursor.com/blog | 唯一未 dedup 的 cursor 候选 | 🟡 中 | 需验证 body 长度 + cluster 关联 |
| `cursor.com/blog/cowork-plugins-finance` | cursor.com/blog | finance plugins + cross-app workflows | 🟡 中 | R438/R439 评估中，cluster 与历史 Article 关联 |

## 📌 Articles 线索

- **claude.com/blog sitemap 持续高 ROI**：135 untracked → R337 filter → 1 候选 → 99.3% skip rate 但每轮都有 1 个高质量 Article 命中
- **Anthropic engineering 已完全覆盖**：24/24 articles tracked
- **GitHub API direct search `topics` 字段是关键信号**：`hermes-agent` topic 直接命中本仓库目标生态（R367 #27）
- **Anthropic news 8 untracked 全是 partnerships/announcements**：R439 确认非工程相关
- **cursor.com/blog dedup 命中率高**：93 slugs → 60 untracked → 58 dedup hit 既有文章 → 仅 1-2 novel

## 🔮 下轮规划（R440）

- [ ] 评估 XiaomiMiMo/MiMo-Code (9,716⭐) — GitHub API search 命中
- [ ] 评估 `cursor.com/blog/increased-agent-usage` — 唯一未 dedup 的 cursor 候选
- [ ] 监控 Tavily API 额度恢复
- [ ] 探索 anthropic.com/research (R422 P2 监控)
- [ ] 考虑更新 ponytail 文章（stars 5x 增长）
- [ ] 继续走 R337+R345+R393 三层 filter pipeline 跑 claude.com/blog
- [ ] GitHub API search 持续用 `hermes-agent` topic 作为 R367 #27 tiebreaker