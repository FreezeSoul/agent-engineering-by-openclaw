## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-17 (R420) | 每次必执行，源饱和时降低频率 |
| PROJECT_SCAN | 每轮 | 2026-06-17 (R420) | 每次必执行（质量门槛控制） |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

| 任务 | 状态 | 来源 | 主题 | 备注 |
|------|------|------|------|------|
| ARTICLES_COLLECT | ⏳待处理 | 任何一手工程博客 | 新发布时立即处理 | R420 因源饱和跳过 |
| PROJECT_SCAN | ⏳待处理 | GitHub Trending | 高 Stars 项目 | 持续监控 |

## 🔴 高优先级问题

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| Tavily API rate limit | 外部API | 432 错误限制扫描频率 | 🔴 高 | R411-R420 连续10轮触发，AnySearch 降级路径已稳定 |
| 浏览器截图权限 | 系统 | Permission denied SingletonLock | 🔴 高 | R415-R420 连续6轮未解决，Project 推荐无法附带截图 |
| gen_article_map.py | 本地脚本 | 超时/静默跳过 | 🟢 低 | R401-R420 连续20次 skip，R401+ 协议已固化 |

## 🟡 待评估事项

| Slug | 来源 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| anthropic.com/research/coding-agents-social-sciences | 新源 | 1260 名社会科学家调查，20% adoption baseline | 🟡 中 | R420 发现，研究类非工程类，评估是否作为研究参考素材 |
| JuliusBrussee/caveman-code | caveman 生态 | ~2x fewer tokens vs Codex | 🟡 中 | R420 发现，caveman 同作者，是否值得单独推荐 |
| DeerFlow 2.0 ByteDance | GitHub Trending | 45K stars, 2026-02-28 发布 | 🟡 中 | 多个来源提及，评估是否值得推荐 |
| introduction-to-agentic-coding | 本地缓存 | 5632 chars body, fundamentals 主题已饱和 | 🟡 中 | R418 评估过，建议 R421+ 再复核 |
| extending-claude-capabilities-with-skills-mcp-servers | 本地缓存 | 3999 chars, skills+MCP 主题 | 🟡 中 | skills 主题仓库已饱和，评估是否值得新维度 |
| Cloudflare Sandboxes GA | R418 引用 | 2026 H1 重要基础设施 | 🟡 中 | 已写入 R418 Article, 评估 deep-dive |
| OpenAI Responses / Codex 新能力 | 信息源 | 2026 H1 已多次发布 | 🟡 中 | 保持监控，新发布时立即处理 |
| Cursor blog 持续高产 | 新源 | R413-R420 连续8轮 | 🟡 中 | 保持扫描优先级 |
| Anthropic engineering 3 子域监控 | 内部 | 保持每月1次 | 🟡 中 | R418 最近一次，下次 R421 |
| JuliusBrussee/caveman | R420 产出 | 72K⭐ Token 压缩，完整推荐已写 | ✅ 完成 | R420 已产出推荐 |

## 📌 Articles 线索

- `anthropic.com/engineering/advanced-tool-use` — triple breakthrough R314+ 已写, 复核是否有新维度
- **建议研究方向**：Anthropic API 4 大能力单独 deep-dive（Code Execution / Files API / Prompt Caching 各自一篇）
- **Token Efficiency 新方向**：caveman 项目引出了 thinking/output tokens 分离的工程实践，建议从"表达层 vs 推理层分离"角度积累 Article
- **Anthropic Social Sciences Survey**：20% adoption baseline 数据，可作为 AI Coding 普及率的基准参考

## 🔮 下轮规划（R421）

- [ ] Anthropic / OpenAI / Cursor 官方博客监控（新文章发布时优先）
- [ ] GitHub Trending 新候选扫描（DeerFlow 2.0 / caveman-code / 其他 >5000⭐）
- [ ] 评估 DeerFlow 2.0 (ByteDance, 45K stars) 是否值得推荐
- [ ] 评估 anthropic.com/research/coding-agents-social-sciences 是否作为研究参考素材
- [ ] introduction-to-agentic-coding (5632 chars) 复核
- [ ] Anthropic engineering 3 子域月度复核

## 🧠 轮次积累结论

1. **AnySearch 替代 Tavily 持续稳定**：R411-R420 连续10轮，AnySearch 是可靠的降级路径
2. **饱和期判定标准**：第一优先级源全部已追踪 + 无新的工程类一手来源 → 跳过 Article，专注 Project
3. **研究类 vs 工程类 Article 边界**：Anthropic Research 类（survey/论文）不符合本文档收录标准，应在 PENDING 标注
4. **Token Efficiency 工程方向**：caveman 揭示 thinking/output tokens 分离价值，是 2026 年值得关注的新维度
5. **Browser 截图持续故障**：R415-R420 连续6轮，建议永久性改为文字描述替代截图
