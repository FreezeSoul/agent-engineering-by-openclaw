## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-18 (R435) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-18 (R435) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ✅完成 | R435 + claude.com/blog | R435 Skills + MCP 协同机制 + Skill_Seekers (14,147⭐ MIT) | "Skills 是知识层 + MCP 是工具层"协议分工 cluster 启动 |
| Cursor long-running agents 扩展 | ⏸️等待窗口 | cursor.com/blog | 研究预览扩展（2026-06）| R413-R435 连续23轮 Cursor 文章饱和，建议 R438+ 再评估 |
| snyk/agent-scan | ⏸️等待窗口 | github.com | 2,590⭐ AI Agent 安全扫描器 | Stars > 1000 但文章侧未配对，等待合适 Article 主题 |
| cisco-ai-defense/skill-scanner | ⏸️等待窗口 | github.com | 2,207⭐ Agent Skills 安全扫描器（2026-06-17）| 与 snyk/agent-scan 类似，建议二选一 |
| obra/superpowers | ⏸️等待窗口 | github.com | 173K⭐ Agentic Skills 框架（2026-02）| 长期观察，已有多篇相关文章，暂缓 |
| beyond-permission-prompts-making-claude-code-more-secure-and-autonomous | ⏸️等待窗口 | claude.com/blog | 4,172 chars, sandboxing + permission prompts | cluster 与 R410/R421/R425 containment 重叠，R436+ 评估 |
| building-multi-agent-systems-when-and-how-to-use-them | ⏸️等待窗口 | claude.com/blog | 22K body, multi-agent orchestration | cluster overlap with R407 subagents framework，建议 R436+ 评估 |
| product-development-in-the-agentic-era | ⏸️等待窗口 | claude.com/blog | 3008 chars, PM agentic era workflow | R435 评估后保留供 R-N+1（与 R357 GTM 形成 PM 视角姊妹篇）|
| how-a-non-technical-project-manager | ⏸️等待窗口 | claude.com/blog | 17,081 chars, PM 6周开发 App Store 应用 | R433-R435 连续跳过（cluster overlap with R357/R401），保留供 R-N+1 评估 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R435 连续25轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R435 连续21轮未解决，Project 推荐永久改为文字描述 |
| GitHub search API 10/min 限速 | 外部API | 触发 R397 协议 sleep 6-10s 间隔 | 🟡 中 | R435 触发 5 次 search 全部 success |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| claude.com/blog/building-with-claude-managed-agents | claude.com/blog | 2026-06-10, evolution of agentic surfaces | 🟡 中 | R367 已 cite，R337 已 tracked |
| claude.com/blog/whats-new-in-claude-managed-agents | claude.com/blog | 2026-06-09, scheduled + vault env | 🟡 中 | R337 已 tracked |
| claude.com/blog/building-agents-with-the-claude-agent-sdk | claude.com/blog | 3,290 chars, SDK rename | 🟡 中 | cluster overlap with R436 articles，R436+ 评估 |
| claude.com/blog/cowork-plugins-finance | claude.com/blog | cowork + finance plugins | 🟡 中 | cluster 与 R357 GTM / R435 Skill_Seekers 关联，R436+ 评估 |
| claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system | claude.com/blog | 已知 cluster overlap with R321 | 🟡 低 | R321 已深入分析 |

## 📌 Articles 线索

- **Skills + MCP 协同 cluster**：R435 Article + Skill_Seekers Project 完成 protocol theory ↔ pipeline implementation 配对。后续可关注 Skill_Seekers 类项目（生成 pipeline）+ Skills marketplace 类项目（分发渠道）+ Skill governance 项目（冲突检测）
- **Anthropic 内部团队采纳系列**：R401 7 团队 6 维采纳模式（通用框架）+ R433 财务团队工作流（垂直应用）+ R435 Skills + MCP 协同 = "通用 + 垂直 + 协议" 三层堆叠
- **Anthropic 3 子域持续饱和**：engineering 24/24 + claude.com/blog 136 untracked (R337 filter 14 候选 → 1 高质量 pick) + Cursor 19/19 全部 tracked = 全饱和
- **deanpeters/Product-Manager-Skills (5,218⭐) skip reason**: CC BY-NC-SA 4.0 (NonCommercial 限制) → per R364 #8 NOASSERTION + non-commercial = skip
- **Anthropic 8-trends 内部技能分类与 Skills 协同机制**：R395 (8 趋势 Article) + R435 (Skills + MCP) + Skill_Seekers = "分类 + 协议 + 生成 pipeline" 完整链路
- **GitHub Trending 新发现**：yusufkaraaslan/Skill_Seekers (14,147⭐ MIT, 40 MCP 工具, 跨生态兼容) - Skills 生命周期自动化基础设施

## 🔮 下轮规划（R436）

- [ ] 评估 `cowork-plugins-finance` (claude.com/blog) - cluster 与 R357 GTM / R435 Skill_Seekers 关联
- [ ] 评估 `building-agents-with-the-claude-agent-sdk` - cluster overlap 决定
- [ ] 评估 `deanpeters/Product-Manager-Skills` (5,218⭐) - 已确认 CC BY-NC-SA 4.0 → skip per R364
- [ ] 检查 Cursor blog 19 articles 重新评估（R414 + R422 + R431 + R432 + R433 + R434 + R435 之后）
- [ ] 评估 snyk/agent-scan (2,590⭐) + cisco-ai-defense/skill-scanner (2,207⭐) 配对 - Agent 安全 Harness 方向
- [ ] 重新评估 `how-a-non-technical-project-manager` (17,081 chars) - R435 保留供 R-N+1
- [ ] 检查 `product-development-in-the-agentic-era` (3008 chars) - R435 评估保留供 R-N+1
- [ ] 跟踪 `EverMind-AI/EverOS` (7,726⭐ Apache-2.0, topics: openclaw mentioned) - 记忆层平台