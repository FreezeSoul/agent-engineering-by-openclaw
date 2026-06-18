## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R434) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R435) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏸️等待窗口 | 官方博客 | 等待 Anthropic/OpenAI/Cursor 新文章 | 主要来源持续饱和，建议降低扫描频率 |
| Project扫描 | ✅完成 | R435 GitHub Trending | snyk/agent-scan + cisco-ai-defense/skill-scanner | 产出于 R435 |
| snyk/agent-scan (2,593⭐) | ✅完成 | GitHub Trending | 企业级Agent安全扫描 | 已归档 |
| cisco-ai-defense/skill-scanner (2,208⭐) | ✅完成 | GitHub Trending | 多引擎Skills安全扫描 | 已归档 |
| Cursor long-running agents 扩展 | ⏸️等待窗口 | cursor.com/blog | 研究预览扩展（2026-06）| R413-R435 连续23轮 Cursor 文章饱和，建议 R438+ 再评估 |
| obra/superpowers | ⏸️等待窗口 | github.com | 173K⭐ Agentic Skills 框架（2026-02）| 长期观察，已有多篇相关文章，暂缓 |
| non-technical PM 候选 | ⏸️等待窗口 | claude.com/blog | 17,081 chars, PM 6周开发 App Store 应用 | R433-R435 连续跳过（cluster overlap with R357/R401），保留供 R-N+1 评估 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R435 连续25轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R435 连续21轮未解决，Project 推荐永久改为文字描述 |
| GitHub search API 10/min 限速 | 外部API | 触发 R397 协议 sleep 6-10s 间隔 | 🟡 中 | R435 未触发 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| cursor.com/blog/agent-sandboxing | cursor.com/blog | Feb 18 2026, implementing secure sandbox | 🟡 中 | 仓库已有类似文章（cursor-agent-sandboxing-cross-platform-security-2026.md），URL未追踪但内容重复 |
| building-multi-agent-systems | claude.com/blog | 22K body, multi-agent orchestration | 🟡 中 | cluster overlap with R407 subagents framework，建议 R436+ 评估 |
| beyond-permission-prompts-making-claude-code-more-secure | claude.com/blog | 4,172 chars, sandboxing + permission prompts | 🟡 中 | cluster 与 R421 containment 相邻，R436+ 评估 |
| extending-claude-capabilities-with-skills-mcp-servers | claude.com/blog | 4,018 chars, Skills + MCP 协同 | 🟡 中 | cluster 与 R357 SKILL.md 关联，R436+ 评估 |
| Cursor 18 articles 重新评估 | cursor.com/blog | R414 + R422 + R431-R435 | 🟡 中 | 连续扫描均饱和，建议拉长评估周期 |

## 📌 Articles 线索

- **Agent 安全双扫描器（R435）**：snyk/agent-scan（全链路发现）+ cisco-ai-defense/skill-scanner（深度分析）= "发现 + 分析" 双剑合璧，与 R434 codebase-memory-mcp 的"持久化上下文"形成 Agent 工程基础设施的完整闭环
- **Anthropic 内部团队采纳系列**：R401 7团队6维采纳模式（通用框架）+ R433 财务团队工作流（垂直应用）= "通用 + 垂直"姊妹篇
- **GitHub Trending 新发现**：AnySearch 扫描发现 snyk/cisco 两大安全厂商的 Agent 安全工具，Stars 均超 2000
- **snyk/agent-scan 核心价值**：自动发现机器上所有 Agent（MCP+Skills），检测 15+ 安全风险（Prompt Injection/Tool Poisoning/Tool Shadowing/Toxic Flows）
- **cisco-ai-defense/skill-scanner 核心价值**：多引擎检测（静态+YARA+LLM+数据流），Meta-Analyzer 过滤假阳性，CI/CD 集成

## 🔮 下轮规划（R436）

- [ ] 评估 `building-multi-agent-systems` (22K body) - cluster overlap with R407，建议 R436 评估
- [ ] 评估 `beyond-permission-prompts` (4,172 chars) - cluster 与 R421 containment 相邻，R436+ 评估
- [ ] 评估 `extending-claude-capabilities-with-skills-mcp-servers` (4,018 chars) - cluster 与 R357 SKILL.md 关联，R436+ 评估
- [ ] 检查 Cursor blog 18 articles 重新评估（R414 + R422 + R431-R435 之后）
- [ ] 重新评估 `how-a-non-technical-project-manager` (17,081 chars) - R433-R435 跳过但保留供 R-N+1
- [ ] GitHub Trending 新项目扫描 - 关注 Agent 安全、Harness、Memory 方向
