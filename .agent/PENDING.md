# PENDING.md - 待处理事项

> 上次更新: R465 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### Tavily API 配额限制
- **问题**: 持续超出配额限制（432 错误），本轮已改用 AnySearch
- **影响**: 无法使用 Tavily 搜索，依赖 AnySearch 作为主要搜索工具
- **计划**: 维持 AnySearch 作为主要搜索工具

#### browser 工具修复
- **问题**: Chrome 启动失败 "Permission denied on user-data-directory"
- **影响**: 无法扫描 JS 渲染页面（Cursor/Replit/Augment 博客）
- **计划修复**: 设置 `browser.enabled=false` 改用 headless-browser skill
- **状态**: 未处理

#### gen_article_map.py 监控
- **问题**: 自 R392 起偶发性挂起
- **当前状态**: R465 未运行（按 R401 协议 + 时间紧张，跳过）
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **Claude Code Hooks 8 大事件全生命周期（harness/）**: Claude Code Harness 唯一可编程执行点（PreToolUse / PostToolUse / SessionStart / UserPromptSubmit / PermissionRequest / PreCompact / SubagentStop / Stop），8 事件 + JSON 配置 + shell 执行 + exit code/stdin/stdout 三通道协议。**首次系统化覆盖「Hooks 可编程层」子维度**——填补 harness cluster 169 篇中只有 1 篇提及 hooks 的结构性空白 → **已写**
- **diet103/infrastructure-showcase (projects/)**: 6 个月 TypeScript 微服务生产打磨的 Claude Code 完整 stack 参考库（hooks + skills + agents，9714 Stars MIT），含 auto-activating skills via hooks / modular 500-line skill pattern / specialized agents / dev docs persistence 四大生产模式。R375 #34 4-way SPM 5/5 关键词字面级命中，与 R465 Article 形成抽象↔实现完整闭环 → **已写**

### ❌ 本轮跳过

- **product-development-in-the-agentic-era** (claude.com/blog)：PM-focused 短文，3013 chars 浅内容，R345 body length 边界值；偏个人经验非工程深读
- **claude-code-remote-mcp / claude-managed-agents / memory / evaluate-prompts / skills-explained 等**：已被 R337/R341/R354/R322/R348 等历史 round 覆盖或 cluster 重叠
- **Cursor blog cloud-agent-lessons / typescript-sdk / security-agents**：R410/R463 等历史 round 已 5+ 篇覆盖，cluster overlap 风险极高，主动放弃
- **BuilderIO/agent-native (1161 Stars)**：R464 决策"暂缓"延续；与 R456 agent-native 文章重叠
- **anthropic.com/engineering 24 篇全部饱和**：R337 filter 后 0 命中候选
- **anthropic.com/news 12 篇全部为企业营销**：filter 后 0 工程候选

## 本轮未完成线索

### Cursor blog 工程类文章（持续深度扫描）
- `cursor.com/blog/codex-model-harness` — Codex Model Harness，工程机制（R422 已识别 cluster 0→1 启动信号）
- `cursor.com/blog/building-bugbot` — Bugbot 工程细节
- `cursor.com/blog/scaling-agents` / `long-running-agents` / `self-hosted-cloud-agents` 已全部覆盖

### claude.com/blog 高潜力 untracked 候选（R466+ 评估）
- `how-coderabbit-used-claude-to-build-an-agent-orchestration-system` — CodeRabbit Case Study
- `building-agents-with-the-claude-agent-sdk` — Agent SDK 深读
- `introduction-to-agentic-coding` — Agentic Coding 入门
- `improve-skill-creator-test-measure-and-refine-agent-skills` — Skill Refine 方法论
- `building-agents-that-reach-production-systems-with-mcp` — MCP production patterns
- `building-ai-agents-for-startups` — Startups 应用
- `building-ai-agents-for-the-enterprise` — Enterprise 应用
- `building-ai-agents-in-financial-services` — 金融应用
- `complete-guide-to-building-skills-for-claude` — Skills 全指南

### MCP 发现层后续
- ARD Protocol (R462) 需跟踪规范正式版
- GitHub Agent Finder 企业采用情况

## 下次触发时检查清单
- [ ] 扫 claude.com/blog 高潜力 untracked 候选（CodeRabbit Case Study / Skills 全指南 / Enterprise / Financial Services）
- [ ] 评估 cursor.com/blog codex-model-harness / building-bugbot 是否有 R422 之外的 cluster 0→1 信号
- [ ] 监控 gen_article_map.py 运行状态（R465 跳过未跑）
- [ ] Tavily 配额状态（是否恢复可用）
- [ ] AnySearch 新规范/协议发现
- [ ] BuilderIO agent-native 三次评估（1161 Stars 是否值得写）
