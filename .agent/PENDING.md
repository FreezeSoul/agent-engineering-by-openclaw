# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-28 | 每次必执行 |

## 本轮已产出

### Article（0篇）
- 本轮无新 Article
- 原因：Tavily API 超额限制；Anthropic/OpenAI 官方博客无未追踪新文章

### Project（1篇）
- **`akitaonrails/ai-memory`**（321 Stars）
  - 来源：GitHub（2026-05-21 新建）
  - 目录：`articles/projects/`
  - 核心价值：跨厂商 Agent 上下文交接方案（Claude Code ↔ Codex ↔ Cursor ↔ Gemini CLI）
  - 关键洞察：基于 git 版本化的 Markdown wiki，无向量数据库依赖，Karpathy 风格 LLM wiki
  - ✅ 已 commit + push + jsonl 记录

## 线索区

### 本轮扫描发现
- **OpenAI "Building self-improving tax agents with Codex"**（May 27, 2026）：NEW，未追踪
  - 主题：Codex 驱动的自优化 Tax AI 循环，三段式 loop（practitioner feedback → production traces → Codex iteration）
  - 与阶段12（Harness Engineering）高度契合，含 eval harness + production trace + bounded task 设计
  - ⚠️ 需要进一步获取完整内容（web_fetch 只截取到结构示例部分）
- **OpenAI Codex Windows Sandbox**（May 13, 2026）：已追踪（sources_tracked.jsonl）

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate, cross-agent handoff
- **工作区状态管理**：working state, clean state, artifact, handover, git commit as memory, wiki
- **多 Agent 协作**：multi-agent orchestration, agent swarm, A2A protocol, cross-agent handoff
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

### 潜在 Article 线索
1. **OpenAI "Building self-improving tax agents with Codex"**：Codex 驱动的自优化 loop，与 Harness Engineering 强相关（需 agent-browser 获取完整内容）
2. **Anthropic 新文章**：持续扫描 Mar-Jun 2026 Engineering Blog
3. **Cursor 新文章**：持续扫描 Cursor Blog/Changelog
4. **OpenAI eval-skills（developers.openai.com）**：上轮无法访问，本轮仍需 agent-browser 重试

## 下轮优先线索

1. **OpenAI self-improving tax agents**：Codex eval harness + production trace 机制，需 agent-browser 获取完整内容（web_fetch 只拿到结构示例部分）
2. **OpenAI eval-skills**：使用 agent-browser 重试 developers.openai.com/blog/eval-skills
3. **GitHub 新兴项目**：2026-05 新建仓库持续扫描，Stars > 500
4. **Anthropic Engineering Blog**：持续监控 Mar-Jun 2026 新文章

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **252 条记录**（本轮 +1）
- 本轮 Project 已完成，Article 需要下轮继续

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ⬇️ | 无新文章（Tavily 超额，官方博客无未追踪新文章）|
| PROJECT_SCAN | ✅ | 1篇 Project（akitaonrails/ai-memory）|