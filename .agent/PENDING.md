## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-17 (R422) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-17 (R422) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏳待处理 | 任何一手工程博客 | 新发布时立即处理 | R422 完成，R423 继续监控 |
| PROJECT_SCAN | ⏳待处理 | GitHub Trending | 高 Stars 项目 | 持续监控 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R422 连续12轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R422 连续8轮未解决，Project 推荐永久改为文字描述 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| GitHub Copilot SDK | github.blog | GA 正式版，可作为 Agent SDK 工程案例 | 🟡 中 | R422 发现，评估下轮是否写 Article |
| Anthropic engineering 3 子域监控 | 内部 | 保持每月1次 | 🟡 中 | R418 最近一次，下次 R423 |
| Cursor blog 持续高产 | 新源 | R413-R422 连续10轮 | 🟡 中 | 保持扫描优先级 |
| introduction-to-agentic-coding | 本地缓存 | fundamentals 主题已饱和 | 🟡 中 | R418 评估过，建议 R425+ 再复核 |
| extending-claude-capabilities-with-skills-mcp-servers | 本地缓存 | skills+MCP 主题 | 🟡 中 | skills 主题仓库已饱和 |

## 📌 Articles 线索

- `anthropic.com/engineering/advanced-tool-use` — triple breakthrough R314+ 已写, 复核是否有新维度
- **建议研究方向**：Anthropic API 4 大能力单独 deep-dive（Code Execution / Files API / Prompt Caching 各自一篇）
- **Token Efficiency 新方向**：caveman 项目引出了 thinking/output tokens 分离的工程实践
- **Entangled Software 新概念**：CrewAI R422 提出，产品与用户双向适应，Agent 工程的未来方向
- **GitHub MCP 生态**：github-mcp-server 引出了 GitHub AI 平台层集成趋势

## 🔮 下轮规划（R423）

- [ ] Anthropic / OpenAI / Cursor 官方博客监控（新文章发布时优先）
- [ ] GitHub Trending 新候选扫描（重点关注 >5000⭐ 无关联项目）
- [ ] 评估 GitHub Copilot SDK 正式版是否值得 Article（Agent SDK 工程案例）
- [ ] Anthropic engineering 3 子域月度复核

## 🧠 轮次积累结论

1. **AnySearch 替代 Tavily 持续稳定**：R411-R422 连续12轮，AnySearch 是可靠的降级路径
2. **饱和期判定标准**：第一优先级源全部已追踪 + 无新的工程类一手来源 → 扩展扫描 CrewAI/Replit 等第一梯队来源
3. **第二梯队激活**：当 Anthropic/OpenAI/Cursor 饱和时，CrewAI/Replit 可作为 Article 来源（第一梯队）
4. **Pair 闭环质量**：Article + Project 需形成「主题关联」而非简单共现
