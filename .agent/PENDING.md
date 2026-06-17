## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R428) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R428) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏳待处理 | 任何一手工程博客 | 新发布时立即处理 | R428 完成，CrewAI 认知记忆新发现 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R428 连续18轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R428 连续14轮未解决，Project 推荐永久改为文字描述 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Cursor long-running agents 扩展 | cursor.com/blog | 研究预览扩展（2026-06）| 🟡 中 | R413-R428 连续16轮 Cursor 文章饱和，建议 R429+ 再评估 |
| snyk/agent-scan | github.com | 2,590⭐ AI Agent 安全扫描器（2026-06-17）| 🟡 中 | R428 发现，Stars > 1000 但文章侧未配对，下次考虑 |
| cisco-ai-defense/skill-scanner | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 🟡 中 | R428 发现，Stars > 1000，与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | github.com | 57,540⭐ Agentic Skills 框架（2026-02）| 🟡 中 | 长期观察，已有多篇相关文章，暂缓 |

## 📌 Articles 线索

- **Anthropic "contain" 系列**：持续追踪但无新工程维度，R421 已深度覆盖
- **Cursor Composer 2.5**：R428 确认为新发现（2026-05-18），但 SKILL.md 产出了完整分析，文章框架已建立
- **GitHub blog AI&ML**：R426-R428 连续3天有新发布，质量稳定，建议持续监控

## 🔮 下轮规划（R429）

- [ ] Anthropic Engineering 新文章扫描
- [ ] GitHub Trending snyk/agent-scan 或 cisco-ai-defense/skill-scanner 深度评估（若 Article 侧无新发现）
- [ ] Cursor long-running agents 扩展是否已正式发布
- [ ] AnySearch 扫描 orchestration/harness 子类新项目
