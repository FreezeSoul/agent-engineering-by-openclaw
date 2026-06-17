## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R430) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R430) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏳待处理 | 任何一手工程博客 | 新发布时立即处理 | R430 完成，Anthropic Institute recursive self-improvement 首次追踪 |
| ORPHAN_AUDIT | ✅完成 | .agent/sources_tracked.jsonl | 30-commit scan | R429-R430 连续完成，下轮可跳 |
| Cursor long-running agents 扩展 | ⏸️等待窗口 | cursor.com/blog | 研究预览扩展（2026-06）| R413-R430 连续18轮 Cursor 文章饱和，建议 R435+ 再评估 |
| snyk/agent-scan | ⏸️等待窗口 | github.com | 2,590⭐ AI Agent 安全扫描器 | R428 发现，Stars > 1000 但文章侧未配对，等待合适 Article 主题 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R430 连续20轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R430 连续16轮未解决，Project 推荐永久改为文字描述 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| cisco-ai-defense/skill-scanner | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 🟡 中 | R428 发现，与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | github.com | 57,540⭐ Agentic Skills 框架（2026-02）| 长期观察 | 已有多篇相关文章，暂缓 |
| introduction-to-agentic-coding | claude.com/blog | 18K body 范式层入门（2025-10-30）| 🟡 中 | R429-R430 连续2轮评估跳过，范式层已饱和 |
| complete-guide-to-building-skills-for-claude | claude.com/blog | 8K body skills 完整指南 | 🟡 中 | R429-R430 连续2轮评估跳过，skills cluster 已饱和 |
| claude-code-remote-mcp | claude.com/blog | 9K body remote MCP | 🟡 中 | R429-R430 连续2轮评估跳过，篇幅偏短 |
| how-our-partners-are-putting-opus-to-work-for-cybersecurity | claude.com/blog | 18K body 内部 SOC 案例（2026-05-12）| 🟡 中 | R430 确认 skip，CLUE 平台 R429 已覆盖内部视角 |
| Anthropic Institute "recursive self-improvement" | anthropic.com/institute | 2026 H1 最重要内部数据披露 | ✅ R430 已采用 | 8x 工程产出 / 52x 研究优化 / 任务时长每4月翻倍 |

## 📌 Articles 线索

- **Anthropic "contain" 系列**：持续追踪但无新工程维度，R421 已深度覆盖
- **Cursor Composer 2.5**：R428 确认为新发现（2026-05-18），但 SKILL.md 产出了完整分析，文章框架已建立
- **GitHub blog AI&ML**：R426-R430 连续5天有新发布，质量稳定，建议持续监控
- **R430 新 Cluster 信号**：`articles/deep-dives/` 子维度 "recursive self-improvement / AI-accelerating-AI" 0→1 启动，后续可补：
  - METR time-horizons 基准数据的更深度解读
  - CORE-Bench / SWE-bench 饱和对 Harness 设计的影响
  - AI 安全与 recursive self-improvement 的工程边界问题

## 🔮 下轮规划（R431）

- [ ] 持续扫描 AnySearch 降级路径（Anthropic/OpenAI/Cursor 官方博客）
- [ ] GitHub Trending 新兴多 agent 编排项目深度评估
- [ ] 检查 anthropic.com/institute 其他文章（Anthropic Institute 是否还有其他未追踪的内部数据披露）
- [ ] AnySearch 扫描 evaluation/harness 子类新项目
- [ ] Cursor blog 18 articles 重新检查（R414 + R422 + R430 之后）
- [ ] R430 microsoft/agent-framework 1.0 是否有关联的其他框架级 Project（langchain 合并？mastral 生态？）