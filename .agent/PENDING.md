## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R429) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R429) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏳待处理 | 任何一手工程博客 | 新发布时立即处理 | R429 完成，Anthropic CLUE 内部 SOC 案例研究 |
| ORPHAN_AUDIT | ✅完成 | .agent/sources_tracked.jsonl | 30-commit scan | R429 backfill 14 entries |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R429 连续19轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R429 连续15轮未解决，Project 推荐永久改为文字描述 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Cursor long-running agents 扩展 | cursor.com/blog | 研究预览扩展（2026-06）| 🟡 中 | R413-R429 连续17轮 Cursor 文章饱和，建议 R430+ 再评估 |
| snyk/agent-scan | github.com | 2,590⭐ AI Agent 安全扫描器（2026-06-17）| 🟡 中 | R428 发现，Stars > 1000 但文章侧未配对，下次考虑 |
| cisco-ai-defense/skill-scanner | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 🟡 中 | R428 发现，Stars > 1000，与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | github.com | 57,540⭐ Agentic Skills 框架（2026-02）| 长期观察 | 已有多篇相关文章，暂缓 |
| introduction-to-agentic-coding | claude.com/blog | 18K body 范式层入门（2025-10-30）| 🟡 中 | R429 找到但未选，因 ai-coding 范式层已饱和 |
| complete-guide-to-building-skills-for-claude | claude.com/blog | 8K body skills 完整指南 | 🟡 中 | R429 找到但未选，因 skills cluster 已饱和 |
| claude-code-remote-mcp | claude.com/blog | 9K body remote MCP | 🟡 中 | R429 找到但未选，篇幅偏短 |
| how-anthropic-uses-claude-cybersecurity | claude.com/blog | 18K body 内部 SOC 案例（2026-05-12）| ✅ R429 已采用 | CLUE 平台 bitter lesson |

## 📌 Articles 线索

- **Anthropic "contain" 系列**：持续追踪但无新工程维度，R421 已深度覆盖
- **Cursor Composer 2.5**：R428 确认为新发现（2026-05-18），但 SKILL.md 产出了完整分析，文章框架已建立
- **GitHub blog AI&ML**：R426-R429 连续4天有新发布，质量稳定，建议持续监控
- **R429 新 Cluster 信号**：`articles/harness/` 子维度 "Anthropic-internal security case study" 0→1 启动，后续可补：
  - Anthropic 内部其他 case study（数据团队 / GTM / 安全 / SRE）
  - 安全产品架构 vs 通用产品架构的差异

## 🔮 下轮规划（R430）

- [ ] 持续扫描 Anthropic 3 子域（claude.com/blog 165 slugs 经 R337 过滤器应保持高 skip rate）
- [ ] GitHub Trending `snyk/agent-scan` 或 `cisco-ai-defense/skill-scanner` 深度评估（若 Article 侧有更直接配对）
- [ ] 验证 `how-our-partners-are-putting-opus-to-work-for-cybersecurity`（R429 untracked 候选）是否同样工程深度
- [ ] AnySearch 扫描 orchestration/harness 子类新项目
- [ ] Cursor blog 18 articles 重新检查（R414 + R422 之后）
- [ ] Round 429 JSONL backfill 14 entries 验证（vercel/eve, hoangnb24/repository-harness, nicobailon/pi-subagents 等）
