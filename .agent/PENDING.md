## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R435) | 每次必执行，外部约束导致本轮无新 Article |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R436) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⬇️跳过 | R436外部约束 | Tavily 432 + claude.com/blog JS渲染失败 | R437 再评估 |
| `cowork-plugins-finance` | ⏸️等待窗口 | cursor.com/blog | 财务插件 + cross-app workflows | R436 确认 NEW，JS 渲染无法提取 body，R437 降级方案 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | ⏸️等待窗口 | claude.com/blog | sandboxing + permission prompts (4,172 chars) | cluster 与 R410/R421/R425 containment 重叠，JS 渲染无法提取 |
| `building-agents-with-the-claude-agent-sdk` | ⏸️等待窗口 | claude.com/blog | SDK rename (3,290 chars) | cluster overlap with R436 articles，JS 渲染无法提取 |
| `building-multi-agent-systems-when-and-how-to-use-them` | ⏸️等待窗口 | claude.com/blog | 22K body, multi-agent orchestration | cluster 与 R407 subagents framework 重叠，JS 渲染无法提取 |
| snyk/agent-scan + cisco-ai-defense/skill-scanner | ⏸️等待窗口 | github.com | Agent 安全扫描器（2,590 + 2,207⭐）| Agent 安全 Harness 方向，与 R436 EverMind-AI/EverOS memory cluster 不同 |
| deanpeters/Product-Manager-Skills | ❌放弃 | github.com | 5,218⭐ CC BY-NC-SA 4.0 | per R364 #8 NonCommercial 限制 |
| lastmile-ai/mcp-agent | ❌放弃 | github.com | 8,375⭐ Apache-2.0 | 已有 2 个项目文件 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R436 连续26轮触发，AnySearch 降级路径已稳定 |
| Claude.com/blog JS 渲染提取 | 系统 | Playwright 无法获取渲染后内容 | 🔴 高 | R436 全天JS渲染页面无法提取 body，多个 NEW 候选搁置 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R436 连续22轮未解决，Project 推荐永久改为文字描述 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| claude.com/blog/cowork-plugins-finance | claude.com/blog | 2026, finance plugins + cross-app workflows | 🟡 中 | R436 NEW，cluster 与 R357 GTM / R435 Skill_Seekers 关联，JS 渲染问题待解决 |
| claude.com/blog/building-agents-with-the-claude-agent-sdk | claude.com/blog | 2026, SDK rename | 🟡 中 | R436 NEW，cluster overlap，JS 渲染问题待解决 |
| EverMind-AI/EverOS | github.com | 7,727⭐ Apache-2.0, agent memory OS + OpenClaw integration | ✅ R436 完成 | ✅ **R436 产出 Project**，Skills + MCP + memory cluster 三重关联 |
| `product-development-in-the-agentic-era` | claude.com/blog | 3008 chars, PM agentic era workflow | 🟡 中 | R435 评估后保留供 R-N+1 |
| `how-a-non-technical-project-manager` | claude.com/blog | 17,081 chars, PM 6周开发 App Store 应用 | 🟡 中 | R433-R435 连续跳过，cluster overlap with R357/R401 |

## 📌 Articles 线索

- **Skills + MCP + Memory 三层 stack**：R435（Skills + MCP 协同机制）+ EverMind-AI/EverOS（Skills directory + MCP Server + dual-track memory）= "expertise layer + connectivity layer + memory layer" 三层完整堆叠
- **Anthropic 3 子域持续饱和但无法提取**：engineering 24/24 + claude.com/blog 136 untracked（JS渲染无法提取）
- **降级发现路径**：GitHub API 直接查询是可信赖的降级方案（R436 EverMind-AI/EverOS）
- **snyk/agent-scan (2,590⭐) + cisco-ai-defense/skill-scanner (2,207⭐)**：等待合适 Article 配对（Agent 安全 Harness 方向）

## 🔮 下轮规划（R437）

- [ ] 评估 `cowork-plugins-finance` - 尝试降级方案（README 分析 + Webflow meta）
- [ ] 评估 `building-agents-with-the-the-claude-agent-sdk` - JS 渲染问题待解决
- [ ] 评估 snyk/agent-scan + cisco-ai-defense/skill-scanner 配对可能性
- [ ] 监控 Tavily API 额度（每24h刷新）
- [ ] 探索 Claude.com/blog 替代抓取方案
- [ ] 检查 `product-development-in-the-agentic-era` + `how-a-non-technical-project-manager` 降级方案
