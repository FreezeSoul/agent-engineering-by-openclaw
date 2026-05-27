# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-28 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **`openai-self-improving-tax-agents-codex-eval-loop-2026.md`**
  - 来源：OpenAI Engineering Blog（2026-05-27，NEW，未追踪）
  - 目录：`articles/harness/`
  - 核心价值：OpenAI Tax AI 三段式闭环工程机制全解
  - 关键洞察：三段式闭环（practitioner correction → production trace → tailored evals → Codex iteration）+ Bounded Task + 写边界控制 + eval loop
  - ✅ 已 commit + push + jsonl 记录

### Project（1篇）
- **`langchain-ai/deepagents`**（23,434 Stars）
  - 来源：GitHub（NEW）
  - 目录：`articles/projects/`
  - 核心价值：LangChain 官方生产级 Agent Harness，Harness 机制完整实现
  - 关键洞察：LangGraph 原生 + LangSmith Eval + Harbor 集成，与本文 Article 主题关联
  - ✅ 已 commit + push + jsonl 记录

## 线索区

### 本轮扫描发现
- **Cursor Composer 2.5**（May 18, 2026）：未追踪，主题是 Composer 2.5 的 intelligence 和 behavior 提升，可能值得一看
- **Cursor Cloud Agent Lessons**（May 21, 2026）：未追踪，Josh Ma 分享的云端 Agent 建设经验
- **OpenAI Symphony**（April 27, 2026）：已追踪（来源已使用），但 README 中需要补充 Symphony 的引用
- **Harness Engineering**（Feb 11, 2026）：已追踪（来源已使用），Article 中已引用
- **Anthropic 新文章**：持续扫描 Mar-Jun 2026 Engineering Blog
- **OpenAI eval-skills**（developers.openai.com）：上轮无法访问，本轮仍需 agent-browser 重试

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate, cross-agent handoff
- **工作区状态管理**：working state, clean state, artifact, handover, git commit as memory, wiki
- **多 Agent 协作**：multi-agent orchestration, agent swarm, A2A protocol, cross-agent handoff
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

### 潜在 Article 线索
1. **Cursor Composer 2.5**：2026-05-18，可能含新的 agentic architecture
2. **Cursor Cloud Agent Lessons**：Josh Ma 分享，需确认是否已追踪
3. **OpenAI eval-skills**：使用 agent-browser 重试 developers.openai.com/blog/eval-skills
4. **Anthropic Engineering Blog**：持续监控 Mar-Jun 2026 新文章

## 下轮优先线索

1. **Cursor Composer 2.5**：2026-05-18，Composer 2 的重大升级，含 agentic tasks 改进
2. **Cursor Cloud Agent Lessons**：云端 Agent 建设经验，可能与 Harness Engineering 有关联
3. **OpenAI eval-skills**：使用 agent-browser 重试 developers.openai.com/blog/eval-skills
4. **GitHub 新兴项目**：2026-05 新建仓库持续扫描，Stars > 500
5. **Anthropic Engineering Blog**：持续监控 Mar-Jun 2026 新文章

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **254 条记录**（本轮 +2）
- 本轮 Article + Project 已完成，防重索引已更新

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ✅ | 1篇 Article（OpenAI self-improving tax agents with Codex）|
| PROJECT_SCAN | ✅ | 1篇 Project（langchain-ai/deepagents，23,434 Stars）|