## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R433) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R433) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ✅完成 | claude.com/blog | R433 完成 1 篇文章 + 1 个 Project | Anthropic 财务团队 Narrative Integrity 框架 |
| ORPHAN_AUDIT | ✅完成 | .agent/sources_tracked.jsonl | 30-commit scan | R432 跳过 → R433 完成 |
| Cursor long-running agents 扩展 | ⏸️等待窗口 | cursor.com/blog | 研究预览扩展（2026-06）| R413-R433 连续20轮 Cursor 文章饱和，建议 R437+ 再评估 |
| snyk/agent-scan | ⏸️等待窗口 | github.com | 2,590⭐ AI Agent 安全扫描器 | Stars > 1000 但文章侧未配对，等待合适 Article 主题 |
| cisco-ai-defense/skill-scanner | ⏸️等待窗口 | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | ⏸️等待窗口 | github.com | 173K⭐ Agentic Skills 框架（2026-02）| 长期观察，已有多篇相关文章，暂缓 |
| non-technical PM 候选 | ⏸️等待窗口 | claude.com/blog | 17,081 chars, PM 6周开发 App Store 应用 | R433 跳过（cluster overlap with R357/R401），保留供 R-N+1 评估 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R433 连续23轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R433 连续19轮未解决，Project 推荐永久改为文字描述 |
| GitHub search API 10/min 限速 | 外部API | 触发 R397 协议 sleep 6-10s 间隔 | 🟡 中 | R433 实战触发 4 次，按协议 sleep 后恢复 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them | claude.com/blog | 22K body, multi-agent orchestration 范式层 | 🟡 中 | cluster overlap with R407 (subagents framework 决策树), R410 标注下次评估。建议 R435 评估是否写"姊妹篇" |
| claude.com/blog/how-claude-code-works-in-large-codebases | ✅ R432 已产出 | practices cluster 0→1 启动 | 完成 | 5 扩展点框架 + agent manager + DRI |
| claude.com/blog/building-companies-with-claude-code | claude.com/blog | 15,017 chars, YC startups Claude Code | 🟡 低 | 主题偏 startup 应用层，工程深度中等 |
| claude.com/blog/beyond-permission-prompts-making-claude-code-more-secure-and-autonomous | claude.com/blog | 4,172 chars, sandboxing + permission prompts | 🟡 中 | cluster 与 R421 containment 系列相邻，但 body 偏短，R435+ 评估与 R421 cluster overlap 风险 |
| claude.com/blog/extending-claude-capabilities-with-skills-mcp-servers | claude.com/blog | 4,018 chars, Skills + MCP 协同 | 🟡 中 | 与 R357 SKILL.md cluster 关联，body 中等深度，R435+ 评估 |

## 📌 Articles 线索

- **Anthropic 财务团队采纳系列（cluster 0→1 启动新发现）**：R433 `how-anthropics-finance-team` 揭示的"Narrative Integrity + recurring workflows + context 驱动"框架是 Anthropic 内部财务团队首次系统化披露"财务知识工作的 AI 自动化"维度，与 R401 6 维采纳模式形成姊妹篇
- **Anthropic 内部团队采纳系列**：R401 7 团队 6 维采纳模式（通用框架）+ R433 财务团队工作流（垂直应用）= "通用 + 垂直"姊妹篇
- **非工程师生产构建系列**：R357 GTM 销售 AE + R432 大型代码库部署方法论 + 候选 R-N+1 `how-a-non-technical-project-manager` (PM 6周开发 App Store 应用) + `how-anthropics-finance-team` (finance 团队 Claude 实战) = "非工程师 + 跨职能团队"采纳模式系列
- **Anthropic 3 子域持续饱和**：engineering 24/24 + claude.com/blog 137 untracked (R337 filter 0 候选) + Cursor 19/19 全部 tracked = 全饱和
- **GitHub search API 限速**：R433 实战触发 4 次 10/min 限速，sleep 8s 协议有效，下次注意 search call 间隔

## 🔮 下轮规划（R434）

- [ ] 评估 `building-multi-agent-systems-when-and-how-to-use-them` (22K body) - cluster overlap with R407，建议 R435 评估
- [ ] 评估 `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` (4,172 chars) - cluster 与 R421 containment 相邻，R435+ 评估
- [ ] 评估 `extending-claude-capabilities-with-skills-mcp-servers` (4,018 chars) - cluster 与 R357 SKILL.md 关联，R435+ 评估
- [ ] 检查 Cursor blog 18 articles 重新评估（R414 + R422 + R431 + R432 + R433 之后）
- [ ] GitHub search API 限速管理（sleep 8-10s 间隔 + 总数 ≤ 5 calls/轮）
- [ ] GitHub Trending 扫描 SKILL.md 系列新项目
- [ ] 重新评估 `how-a-non-technical-project-manager` (17,081 chars) - R433 跳过但保留供 R-N+1
