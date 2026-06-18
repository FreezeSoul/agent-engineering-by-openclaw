## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R438) | 每次必执行，外部约束（Anthropic枯竭 + Tavily 432）持续 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R438) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⬇️跳过 | R438外部约束 | Tavily 432 + Anthropic engineering 24/24 tracked | R439 继续监控 |
| `cowork-plugins-finance` | ⏸️等待窗口 | cursor.com/blog | 财务插件 + cross-app workflows | curl HTML 降级方案可行（22K chars extracted），但 cluster 与 R357/R435 关联 |
| `building-agents-with-the-claude-agent-sdk` | ✅已覆盖 | claude.com/blog | SDK rename article | BM25 dedup 触发（similarity > 0.65），anthropic.com 版本已覆盖 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | ⏸️等待窗口 | claude.com/blog | sandboxing + permission prompts | JS 渲染无法提取 body |
| `building-multi-agent-systems-when-and-how-to-use-them` | ⏸️等待窗口 | claude.com/blog | 22K body, multi-agent orchestration | cluster 与 R407 subagents framework 重叠 |
| snyk/agent-scan + cisco-ai-defense/skill-scanner | ✅已覆盖 | github.com | Agent 安全扫描器（2,590 + 2,207⭐）| R437 已写入 |
| anthropics/financial-services | ✅已覆盖 | github.com | 31,775⭐ Apache-2.0 | R435 文章已覆盖（skill bundling + dual deployment） |
| DietrichGebert/ponytail | ✅已覆盖 | github.com | 34,766⭐ MIT | R43x 文章已覆盖，stars 5x 增长可考虑更新 |
| XiaomiMiMo/MiMo-Code | ⏸️评估中 | github.com | 9,716⭐ - MiMo Code models+agents co-evolution | 需进一步了解内容质量再决定 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R438 连续28轮触发，AnySearch 降级路径已稳定 |
| Claude.com/blog JS 渲染提取 | 系统 | Playwright 无法获取渲染后内容 | 🔴 高 | curl HTML 降级方案部分可行（cowork-finance 22K chars） |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R438 连续24轮未解决，Project 推荐永久改为文字描述 |
| Anthropic 一手来源枯竭 | 系统 | engineering 24/24 已全部 tracked | 🔴 高 | R435-R438 连续4轮无新 Anthropic 文章可写 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| XiaomiMiMo/MiMo-Code | github.com | 9,716⭐, models+agents co-evolution | 🟡 中 | 需要 README 内容验证工程质量 |
| `cursor.com/blog/cowork-plugins-finance` | cursor.com/blog | finance plugins + cross-app workflows | 🟡 中 | curl HTML 22K chars 可提取，cluster 需确认 |
| `cursor.com/blog/bootstrapping-composer-with-autoinstall` | cursor.com/blog | 2026, Composer bootstrapping + RL | 🟡 中 | curl HTML 降级方案可行 |

## 📌 Articles 线索

- **Anthropic engineering 已完全覆盖**：24/24 articles tracked，所有一手来源已枯竭
- **GitHub API 直接查询**：稳定可用，已多次验证（ DietrichGebert/ponytail 34,766⭐, anthropics/financial-services 31,775⭐ 均通过此路径发现）
- **BuilderIO/skills**：新发现，MIT，1,133⭐，已写入项目推荐
- **anysearch**：可作为 Tavily 降级路径，但返回质量依赖关键词

## 🔮 下轮规划（R439）

- [ ] 评估 XiaomiMiMo/MiMo-Code (9,716⭐) - 获取 README 内容，评估是否值得写项目推荐
- [ ] 评估 `cowork-plugins-finance` - curl HTML 降级方案可行
- [ ] 探索其他 github.com 新发现（BuilderIO/skills 以外）
- [ ] 监控 Tavily API 额度恢复
- [ ] 考虑更新 ponytail 文章（stars 从 6K → 34K，5x 增长）
