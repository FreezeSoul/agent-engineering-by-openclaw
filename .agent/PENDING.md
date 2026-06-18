## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R432) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R432) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ✅完成 | claude.com/blog | R432 完成 1 篇文章 + 1 个 Project | Anthropic Applied AI 团队 5 扩展点框架 |
| ORPHAN_AUDIT | ⏳待处理 | .agent/sources_tracked.jsonl | 30-commit scan | R432 跳过，下次 R433 必跑 |
| Cursor long-running agents 扩展 | ⏸️等待窗口 | cursor.com/blog | 研究预览扩展（2026-06）| R413-R432 连续19轮 Cursor 文章饱和，建议 R436+ 再评估 |
| snyk/agent-scan | ⏸️等待窗口 | github.com | 2,590⭐ AI Agent 安全扫描器 | Stars > 1000 但文章侧未配对，等待合适 Article 主题 |
| cisco-ai-defense/skill-scanner | ⏸️等待窗口 | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | ⏸️等待窗口 | github.com | 173K⭐ Agentic Skills 框架（2026-02）| 长期观察，已有多篇相关文章，暂缓 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R432 连续22轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R432 连续18轮未解决，Project 推荐永久改为文字描述 |
| GitHub search API 10/min 限速 | 外部API | 触发 R397 协议 sleep 6-10s 间隔 | 🟡 中 | R432 实战触发 3 次，按协议 sleep 后恢复 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them | claude.com/blog | 23K body, multi-agent orchestration 范式层 | 🟡 中 | cluster overlap with R407 (subagents framework 决策树), R410 标注下次评估。建议 R434 评估是否写"姊妹篇" |
| claude.com/blog/how-a-non-technical-project-manager-built-and-shipped-a-stress-management-app | claude.com/blog | 17081 chars, 非工程师构建生产应用 | 🟡 中 | cluster 0 命中（non-technical 0 命中），与 R357 GTM 销售 AE 形成"非工程师生产构建"姊妹篇，R433+ 评估 |
| claude.com/blog/how-anthropics-finance-team-uses-claude-to-shape-the-narrative-behind-the-numbers | claude.com/blog | 18021 chars, finance team Claude 实战 | 🟡 中 | cluster 0 命中（finance 0 命中），与 R357 GTM 形成"内部团队采纳"系列，R433+ 评估 |
| claude.com/blog/building-companies-with-claude-code | claude.com/blog | 15017 chars, YC startups Claude Code | 🟡 低 | 主题偏 startup 应用层，工程深度中等 |
| claude.com/blog/beyond-permission-prompts-making-claude-code-more-secure-and-autonomous | claude.com/blog | 4172 chars, sandboxing + permission prompts | 🟡 中 | cluster 与 R421 containment 系列相邻，但 body 偏短，R433+ 评估与 R421 cluster overlap 风险 |
| claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers | claude.com/blog | 4018 chars, Skills + MCP 协同 | 🟡 中 | 与 R357 SKILL.md cluster 关联，body 中等深度，R433+ 评估 |
| claude.com/blog/how-claude-code-works-in-large-codebases | ✅ R432 已产出 | practices cluster 0→1 启动 | 完成 | 5 扩展点框架 + agent manager + DRI |
| jeremylongshore/claude-code-plugins-plus-skills | ✅ R432 已产出 | 5 扩展点开源 marketplace 工程化身 | 完成 | 2,390⭐ MIT |

## 📌 Articles 线索

- **Anthropic Applied AI 系列（cluster 0→1 启动新发现）**：R432 `how-claude-code-works-in-large-codebases` 揭示的"5 扩展点 + agent manager + DRI + 3-6 个月 harness review"框架是 Anthropic Applied AI 团队首次系统化披露"组织工程化"维度，与 R401 6 维采纳模式形成姊妹篇
- **Anthropic 内部团队采纳系列**：R432 Article 致谢列出 Applied AI 8 位作者（Alon Krifcher, Charmaine Lee, Chris Concannon, Harsh Patel, Henrique Savelli, Jason Schwartz, Jonah Dueck, Kirby Kohlmorgen）—— 这些作者的其他文章值得持续追踪
- **非工程师生产构建系列**：R357 GTM 销售 AE + R432 大型代码库部署方法论 + 候选 R-N+1 `how-a-non-technical-project-manager` (PM 用 Claude Code 6 周开发 stress management app) + `how-anthropics-finance-team` (finance 团队 Claude 实战) = "非工程师 + 跨职能团队"采纳模式系列
- **Anthropic 3 子域持续饱和**：engineering 24/24 + claude.com/blog 137 untracked (R337 filter 0 候选) + Cursor 19/19 全部 tracked = 全饱和
- **GitHub search API 限速**：R432 实战触发 3 次 10/min 限速，sleep 8s 协议有效，下次注意 search call 间隔

## 🔮 下轮规划（R433）

- [ ] 评估 `how-a-non-technical-project-manager-built-and-shipped-a-stress-management-app-with-claude-code-in-six-weeks` (17081 chars) - cluster 0 命中，可能形成 R357/R432 姊妹篇
- [ ] 评估 `how-anthropics-finance-team-uses-claude-to-shape-the-narrative-behind-the-numbers` (18021 chars) - cluster 0 命中，与 R357 GTM 形成内部团队采纳系列
- [ ] ORPHAN_AUDIT 30-commit scan (R432 跳过 → R433 必跑)
- [ ] 检查 Cursor blog 18 articles 重新评估（R414 + R422 + R431 + R432 之后）
- [ ] GitHub search API 限速管理（sleep 8-10s 间隔 + 总数 ≤ 5 calls/轮）
- [ ] GitHub Trending 扫描 SKILL.md 系列新项目
