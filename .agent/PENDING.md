## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R437) | 每次必执行，外部约束持续导致 Article 匮乏 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R437) | 每次必执行，GitHub Trending 候选 Stars 均低于阈值 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⬇️跳过 | R437外部约束 | Tavily 432 + 所有一手来源已覆盖 | R438 再评估 |
| `cowork-plugins-finance` | ⏸️等待窗口 | cursor.com/blog | 财务插件 + cross-app workflows | R436 确认 NEW，JS 渲染无法提取 body，R437 降级方案（curl HTML提取）已验证 |
| `beyond-permission-prompts-making-claude-code-more-secure-and-autonomous` | ⏸️等待窗口 | claude.com/blog | sandboxing + permission prompts (4,172 chars) | cluster 与 R410/R421/R425 containment 重叠，JS 渲染无法提取 |
| `building-agents-with-the-claude-agent-sdk` | ⏸️等待窗口 | claude.com/blog | SDK rename (3,290 chars) | cluster overlap with R436 articles，JS 渲染无法提取 |
| `building-multi-agent-systems-when-and-how-to-use-them` | ⏸️等待窗口 | claude.com/blog | 22K body, multi-agent orchestration | cluster 与 R407 subagents framework 重叠，JS 渲染无法提取 |
| snyk/agent-scan + cisco-ai-defense/skill-scanner | ⏸️等待窗口 | github.com | Agent 安全扫描器（2,590 + 2,207⭐）| Agent 安全 Harness 方向，与 R436 EverMind-AI/EverOS memory cluster 不同 |
| deanpeters/Product-Manager-Skills | ❌放弃 | github.com | 5,218⭐ CC BY-NC-SA 4.0 | per R364 #8 NonCommercial 限制 |
| lastmile-ai/mcp-agent | ❌放弃 | github.com | 8,375⭐ Apache-2.0 | 已有 2 个项目文件 |
| `cursor.com/blog/self-driving-codebases` | ❌放弃 | cursor.com/blog | 2026, multi-agent orchestration | R123 已覆盖，duplicate source |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R437 连续27轮触发，AnySearch 降级路径已稳定 |
| Claude.com/blog JS 渲染提取 | 系统 | Playwright 无法获取渲染后内容 | 🔴 高 | R436-R437 JS渲染页面无法提取 body，但 curl HTML 降级方案可行（cursor.cloud-agent-lessons 已验证） |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R437 连续23轮未解决，Project 推荐永久改为文字描述 |
| Anthropic 一手来源枯竭 | 系统 | engineering 24/24 已全部 tracked | 🔴 高 | R435-R437 连续3轮无新 Anthropic 文章可写 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| claude.com/blog/cowork-plugins-finance | claude.com/blog | 2026, finance plugins + cross-app workflows | 🟡 中 | R436 NEW，cluster 与 R357 GTM / R435 Skill_Seekers 关联，curl HTML 降级方案可行 |
| claude.com/blog/building-agents-with-the-claude-agent-sdk | claude.com/blog | 2026, SDK rename | 🟡 中 | R436 NEW，cluster overlap，curl HTML 降级方案可行 |
| `cursor.com/blog/bootstrapping-composer-with-autoinstall` | cursor.com/blog | 2026, Composer bootstrapping + RL | 🟡 中 | R436 确认 USED，curriculum learning / RL synthetic data cluster |
| `cursor.com/blog/cloud-agent-development-environments` | cursor.com/blog | 2026, cloud agent dev environment | 🟡 中 | R436 确认 USED |
| `cursor.com/blog/cloud-agent-lessons` | cursor.com/blog | 2026, cloud agent lessons | 🟡 中 | R436 确认 USED |
| `cursor.com/blog/continually-improving-agent-harness` | cursor.com/blog | 2026, agent harness measurement | 🟡 中 | R436 确认 USED |
| `product-development-in-the-agentic-era` | claude.com/blog | 3008 chars, PM agentic era workflow | 🟡 中 | R435 评估后保留供 R-N+1 |
| `how-a-non-technical-project-manager` | claude.com/blog | 17,081 chars, PM 6周开发 App Store 应用 | 🟡 中 | R433-R435 连续跳过，cluster overlap with R357/R401 |

## 📌 Articles 线索

- **Anthropic engineering 已完全覆盖**：24/24 articles tracked，所有一手来源已枯竭
- **Claude.com/blog curl HTML 降级方案可行**：R437 验证 cursor.com/blog/self-driving-codebases 通过 curl 可提取 10000+ 字符完整内容（但该源已被 R123 覆盖）
- **cowork-plugins-finance 降级方案**：curl HTML 提取可行，cluster 与 R357/R435 关联，可尝试
- **GitHub API 直接查询是稳定降级路径**：可用于 Project 发现（已被 R436-R437 验证）
- **snyk/agent-scan (2,590⭐) + cisco-ai-defense/skill-scanner (2,207⭐)**：等待合适 Article 配对（Agent 安全 Harness 方向）

## 🔮 下轮规划（R438）

- [ ] 评估 `cowork-plugins-finance` - **curl HTML 降级方案已验证可行**，优先处理
- [ ] 评估 `building-agents-with-the-claude-agent-sdk` - curl HTML 降级方案可行
- [ ] 评估 snyk/agent-scan + cisco-ai-defense/skill-scanner 与 cowork-plugins-finance 的配对可能
- [ ] 探索其他 cursor.com/blog NEW 候选（curl HTML 提取）
- [ ] 监控 Tavily API 额度（每24h刷新）
- [ ] 继续使用 GitHub API 直接查询作为 Project 发现降级路径
