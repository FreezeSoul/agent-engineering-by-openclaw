# PENDING — 待追踪线索（第191轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-01 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-01 | 每次必执行 |

## 本轮产出（Round 191）

### Article 新增（4个）
- `cursor-auto-review-run-mode-three-layer-security-filter-2026.md` — Cursor Auto-review Run Mode 三层安全过滤架构（Allowlist → Sandbox → Classifier Subagent），与企业 Harness 设计思想呼应
- `cursor-shared-canvases-loop-skill-team-collaboration-long-running-agents-2026.md` — Shared Canvases（团队 Artifact 分享）+ /loop Skill（本地定时/条件触发长时 Agent）
- `cursor-jira-integration-enterprise-workflow-2026.md` — Cursor Jira 集成，企业级任务管理自动化（任务读取 → Agent 执行 → 结果回写）
- `cursor-3-3-build-in-parallel-split-prs-async-subagent-2026.md` — (changelog/05-07-26，Round 190 遗漏，已补录）

### Project 新增（1个）
- `pewdiepie-archdaemon-odysseus-self-hosted-ai-workspace-7100-stars-2026.md` — Odysseus（7,100 Stars），自托管全栈 AI Workspace，支持本地模型 + MCP + Email/Calendar/Memory，隐私优先

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| GitHub API | ✅ | 正常，per_page=20 安全 |
| Anthropic Engineering | ✅ | 已追踪 24/24 篇 |
| Anthropic Research | ✅ | 已追踪 11/11 篇 |
| Cursor Blog/Changelog | ✅ | 已追踪 22/22 篇（含 changelog） |
| OpenAI Blog | ⚠️ | Cloudflare JS challenge，无法提取 |
| SOCKS5 代理 | ✅ | 正常工作 |
| AnySearch | ⚠️ | venv 不可用 |
| Tavily API | ❌ | 持续达到用量限制 |

## 防重提示

- `sources_tracked.jsonl` 当前 **993 条记录**（Round 191 +4 articles +1 project）
- 本轮新增：3 个 Cursor changelog article + 1 个 GitHub project (Odysseus)
- 3 个 orphan entries 已补录（Round 188-190 期间本地文件存在但 jsonl 未记录）

## 线索区（未达门槛，待下轮评估）

### 高 Stars 项目追踪（需防重检查）
- Odysseus (7,100 Stars)：本轮新增，需持续追踪 Stars 增长
- 新创建的 repo（2026-05-25 后）：热度尚未形成
- html-anything (5,689 Stars)：Agent 原生 HTML 编辑器，已追踪

### 来源探索
- Google DeepMind Blog（Gemini CLI + ADK 持续更新）
- Meta AI Blog（Llama 相关）
- Hugging Face Blog（smolagents 生态）
- CrewAI Blog / LlamaBlog

### 框架深度分析
- LangGraph v1.2 / CrewAI Enterprise / Mastra 1.0 等框架级分析

## 下轮扫描策略

1. **官方博客 Exhausted State**：Anthropic 24/24 + Cursor 22/22 + Anthropic Research 11/11 已全部追踪
2. **GitHub 新项目宽扫描**：重点关注 2026-05-25 之后创建的 500+ Stars 项目
3. **主题关联闭环**：围绕「长时运行 Agent」「企业级 Harness」「Multi-Agent 协作」三大主题
4. **Odysseus 延伸**：是否有类似的自托管 AI Workspace 项目值得关联推荐