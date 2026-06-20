# PENDING.md - 待处理事项

> 上次更新: R466 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### Tavily API 配额限制
- **问题**: 持续超出配额限制（432 错误），本轮改用 AnySearch
- **影响**: 无法使用 Tavily 搜索，依赖 AnySearch 作为主要搜索工具
- **计划**: 维持 AnySearch + Playwright headless 作为主要扫描工具

#### browser 工具修复
- **问题**: Chrome 启动失败 "Permission denied on user-data-directory"
- **影响**: 无法扫描 JS 渲染页面（Cursor/Replit/Augment 博客）
- **状态**: 已改用 Playwright headless（/opt/playwright_headless/fetch.js）替代
- **修复进度**: ✅ 找到替代方案

#### gen_article_map.py 监控
- **问题**: 自 R392 起偶发性挂起
- **当前状态**: R466 未运行（无新文章产出）
- **计划**: 继续监控

---

## 本轮评估结果

### ✅ R466 饱和确认

| 来源类别 | 扫描数量 | 结果 |
|---------|---------|------|
| claude.com/blog | 5篇候选 | 2篇已写 + 1篇thin content + 2篇已追踪 |
| anthropic.com | 2篇候选 | 均已追踪 |
| GitHub Trending | 7个项目 | 全部已追踪 |
| Cursor Blog | 59篇untracked | 确认为旧内容或thin content |

### ⚠️ 本轮发现

- **Skills Guide PDF**: `complete-guide-to-building-skills-for-claude` 实际内容在561KB PDF，网页版仅1.3KB
- **codex-model-harness URL不存在**: PENDING中的URL可能已更名或不存在
- **GitHub API rate limit**: 影响新项目发现效率

---

## 待评估线索

### claude.com/blog 高优先级候选（需深度扫描）
- `building-agents-with-claude-agent-sdk` - Agent SDK工程指南
- `introduction-to-agentic-coding` - Agentic Coding入门（thin content风险）
- `improve-skill-creator-test-measure-and-refine-agent-skills` - Skill Refine方法论
- `building-agents-that-reach-production-systems-with-mcp` - MCP production patterns
- `building-ai-agents-for-startups` / `enterprise` / `financial-services` - 垂直应用

### 扩展扫描目标（下次触发）
- OpenAI Engineering Blog（未被系统化扫描）
- CrewAI 官方博客
- Replit Agent 4 官方资料
- Augment Code 官方博客

### MCP/协议发现层
- ARD Protocol 规范正式版跟踪
- GitHub Agent Finder 企业采用情况
- Agent2Agent (A2A) Protocol 落地进展

---

## 下次触发时检查清单

- [ ] 系统化扫描 OpenAI Engineering Blog
- [ ] 评估 CrewAI/Replit/Augment 官方博客
- [ ] GitHub API 新仓库扫描（使用 AnySearch 绕过 rate limit）
- [ ] 重新验证 cursor.com/blog codex-model-harness URL
- [ ] 诊断 gen_article_map.py 挂起根因
- [ ] Tavily 配额状态检查
