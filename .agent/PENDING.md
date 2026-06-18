## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-19 (R442) | 每轮必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-19 (R442) | 每轮必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| `claude.com/blog` 4个新slug | ⏸️JS渲染 | claude.com/blog | artifacts-in-claude-code, claude-for-foundation-models, connectors-for-everyday-life, steering-claude-code-skills-hooks-rules-subagents-and-more | R442发现，需agent-browser获取内容 |
| Loop Engineering Guide | ⏸️降级评估 | aibuilderclub.com | evaluator loop, open vs closed loop, stop condition, Claude Code /goal | R442发现，高质量但非第一梯队 |
| Tessl 880 evals | ⏸️降级评估 | tessl.io | 14模型×11技能×880次评估，skill adherence lift数据 | R442发现，高质量一手数据但非官方来源 |
| SkillsBench (arxiv) | ⏸️降级评估 | arxiv.org | 86任务×11领域，skill efficacy benchmark | R442发现，学术评估方法论文 |

## 🔴 高优先级问题

| 问题 | 来源 | 状态 | 备注 |
|------|------|------|------|
| Tavily API rate limit | 外部API | 🔴 持续 | 32/32 连续触发 432 错误，已无Tavily搜索能力 |
| 第一梯队内容枯竭 | 系统 | 🔴 持续 | Anthropic 24/24已track，Claude/OpenAI JS渲染无法访问 |
| Brave Search限流 | 外部API | 🔴 新增 | R442触发429限流 |
| GitHub Trending JS渲染 | 系统 | 🔴 持续 | curl/fetch/playwright均无法获取 |
| agent-browser 超时 | 系统 | 🟡 新增 | R442尝试claude.com/blog超时 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/artifacts-in-claude-code` | claude.com/blog | Claude Code artifacts功能 | 🟡 中 | R442发现，JS渲染需agent-browser |
| `claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more` | claude.com/blog | Skills/Hooks/Subagents | 🟡 高 | R442发现，harness相关，JS渲染需agent-browser |
| `claude.com/blog/claude-for-foundation-models` | claude.com/blog | Foundation models | 🟡 中 | R442发现，JS渲染需agent-browser |
| `claude.com/blog/connectors-for-everyday-life` | claude.com/blog | Connectors | 🟡 中 | R442发现，JS渲染需agent-browser |
| `cursor.com/blog/bugbot-updates-june-2026` | cursor.com/blog | Bugbot 3x faster | 🟢 低 | R442发现，产品更新，仅一句"harness improvements" |
| `anthropic.com/engineering/a-postmortem-of-three-recent-issues` | anthropic.com/engineering | Sep 2025基础设施bug postmortem | 🟢 低 | 9个月前旧文，时效性差 |
| `anthropic.com/engineering/desktop-extensions` | anthropic.com/engineering | MCP .mcpb打包格式 | 🟢 低 | Sep 2025旧文，产品公告性质 |

## 📌 Articles 线索

- **R442 饱和**：第一梯队实质枯竭，Anthropic 24/24 tracked全面饱和
- **claude.com/blog 4个新slug**：R442通过sitemap发现，但JS渲染无法获取内容，需agent-browser深度抓取
- **第二梯队高质量内容**：
  - Loop Engineering Guide：evaluator loop vs generator loop、open vs closed loop、stop condition、Claude Code /goal
  - Tessl 880 evals：880次评估数据，skill lift对各类模型的普遍性
- **工具链降级**：Tavily 32轮失败，Brave 429限流，GitHub Trending JS渲染，claude.com/blog JS渲染

## 🔮 下轮规划（R443）

- [ ] 用 agent-browser 深度抓取 claude.com/blog 的4个新slug（skills/hooks/subagents最重要）
- [ ] 重新评估 Loop Engineering Guide 是否降级收录
- [ ] 重新评估 Tessl 880 evals 是否降级收录
- [ ] 尝试 GitHub Trending API（如 github-trending-api npm包）
- [ ] 考虑 Tavily 付费方案或 JINA_API_KEY 配置
