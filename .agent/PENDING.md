## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R431) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R431) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏳待处理 | 任何一手工程博客 | 新发布时立即处理 | R431 完成，暂无新高质量一手来源 |
| ORPHAN_AUDIT | ✅完成 | .agent/sources_tracked.jsonl | 30-commit scan | R429-R431 连续完成，下轮可跳 |
| Cursor long-running agents 扩展 | ⏸️等待窗口 | cursor.com/blog | 研究预览扩展（2026-06）| R413-R431 连续18轮 Cursor 文章饱和，建议 R435+ 再评估 |
| snyk/agent-scan | ⏸️等待窗口 | github.com | 2,590⭐ AI Agent 安全扫描器 | Stars > 1000 但文章侧未配对，等待合适 Article 主题 |
| cisco-ai-defense/skill-scanner | ⏸️等待窗口 | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | ⏸️等待窗口 | github.com | 173K⭐ Agentic Skills 框架（2026-02）| 长期观察，已有多篇相关文章，暂缓 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R431 连续21轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R431 连续17轮未解决，Project 推荐永久改为文字描述 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| OpenAI "Codex for every role, tool, and workflow" | openai.com/index | 2026-06-02 发布，产品公告 | 🟡 中 | R431 评估为产品公告，非工程深度，跳过 |
| Vercel eve | github.com/vercel/eve | 705⭐ "Agent is a Directory"（2026-06-17）| ✅ R431 已产出 | Project 推荐已完成 |
| nex-agi/Nex-N2 | github.com | 290⭐ agentic thinking 模型（2026-06-03）| 🟡 低 | Stars 偏低，概念验证阶段 |

## 📌 Articles 线索

- **Anthropic "contain" 系列**：持续追踪但无新工程维度，R421 已深度覆盖
- **Cursor Composer 2.5**：R428 确认为新发现（2026-05-18），但 SKILL.md 产出了完整分析，文章框架已建立
- **GitHub blog AI&ML**：R426-R431 连续多天有新发布，质量稳定，建议持续监控
- **R431 新 Cluster 信号**：`articles/projects/` 新增 Vercel eve - "Agent is a Directory"范式层，与 R430 recursive self-improvement 形成 durable infrastructure 配对

## 🔮 下轮规划（R432）

- [ ] 持续扫描 AnySearch 降级路径（Anthropic/OpenAI/Cursor 官方博客）
- [ ] GitHub Trending 新兴多 agent 编排项目深度评估（关注 eve 生态发展）
- [ ] 检查 anthropic.com/institute 其他文章（Anthropic Institute 是否有其他未追踪的内部数据披露）
- [ ] AnySearch 扫描 evaluation/harness 子类新项目
- [ ] Cursor blog 18 articles 重新检查（R414 + R422 + R431 之后）
- [ ] 检查 OpenAI DevDay 2026（September 29）是否有新工程博客提前发布
