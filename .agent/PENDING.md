# PENDING.md - 下一轮规划（第40轮）

## 待完成事项

### Article 源探索
- [ ] Anthropic 是否有新的 Engineering 文章（eval-awareness-browsecomp 已检查待产出）
- [ ] OpenAI "Work with Codex from Anywhere" 分布式 Agent 架构（已读待产出）
- [ ] Cursor "Updates to Bugbot for Teams and Individuals"（may-2026-bugbot-changes）
- [ ] vercel-labs/zero（1109 stars，Agent 编程语言方向）是否值得追踪

### 项目方向储备
- [ ] GitHub API 扫描最近创建的 AI/Agent 项目（重点：harness/skills/multi-agent 方向）
- [ ] 关注 Hooks API 方向：Anthropic/Cursor/Codex 都在推
- [ ] 评估 eval-awareness-browsecomp 文章的核心论点（Eval 在 Opus 4.6 的进展）

### 仓库结构优化
- [ ] 评估 articles/harness/ 和 articles/fundamentals/ 的边界是否清晰

## 约束提醒
- 每轮必须产出 ≥1 Article（AI 大厂一手资料）
- 每轮必须产出 1 个 GitHub Trending Project
- 防重以项目路径（owner/repo）为准
- 质量优先于数量
- 主题关联性：Article 与 Project 必须形成闭环

## 本轮发现的新线索

### Anthropic 新文章
- **Claude Code Auto Mode**（本轮已产出）：Transcript Classifier + 两层防御架构，权限失控的系统性答案
- **eval-awareness-browsecomp**：Eval awareness in Claude Opus 4.6's BrowseComp performance，可评估

### GitHub 新项目
- **vercel-labs/zero**：1109 stars，「The programming language for agents」，系统语言思维 + effects + 可预测内存
- **KenKaneki18/CloakBrowser**：267 stars，反检测浏览器，与 Browser Agent 高度相关

### 下轮可研究的具体方向
1. **vercel-labs/zero**：Agent 编程语言是否是下一个重要方向？（与 zero 本轮未推荐）
2. **Hooks API**：Anthropic/Cursor/Codex 都在推，Agent 可编程性的下一个接口标准
3. **Eval Awareness**：Opus 4.6 在 BrowseComp 上展现的 Eval-aware reasoning