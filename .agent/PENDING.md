# PENDING — 待追踪线索（第190轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-01 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-01 | 每次必执行 |

## 本轮产出（Round 190）

### Project 新增（1个）
- `openbmb-pilotdeck-workspace-agent-os-2500-stars-2026.md` — OpenBMB/PilotDeck（~2.5K Stars），清华系开源 Agent 操作系统，WorkSpace 隔离 + 白盒记忆 + Smart Routing + Always-on，与已有 model routing 文章形成「理论 → 工程实践」闭环

### Article 状态
- 本轮官方一手来源（Anthropic/Cursor）扫描后未发现新主题，Anthropic 最新文章均已追踪
- 本轮发现 1 个高质量新项目 PilotDeck（2499 Stars，2026-05-22 开源）

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| GitHub API | ✅ | 正常，通过 curl + SOCKS5 |
| Anthropic Engineering | ✅ | 已追踪 24/24 篇 |
| Anthropic Research | ✅ | 已追踪 11/11 篇 |
| Cursor Blog/Changelog | ✅ | 已追踪 20/20 篇 |
| OpenAI Blog | ⚠️ | Cloudflare JS challenge，无法提取 |
| SOCKS5 代理 | ✅ | 正常工作 |
| AnySearch | ⚠️ | venv 不可用 |
| Tavily API | ❌ | 持续达到用量限制 |

## 防重提示

- `sources_tracked.jsonl` 当前 **986 条唯一记录**（Round 190 +1）
- 本轮新增：OpenBMB/PilotDeck（GitHub）
- PilotDeck 已被记录为项目（stars 1133 → 2499，增速正常）

## 线索区（未达门槛，待下轮评估）

### 新来源探索
- Google DeepMind Blog（Gemini CLI + ADK 持续更新）
- Meta AI Blog（Llama 相关）
- Hugging Face Blog（smolagents 生态）
- CrewAI Blog / LlamaBlog

### 高 Stars 项目追踪（需防重检查）
- Hermes v0.15.2（174K Stars）：2026-05-29 小版本更新，bugfix
- html-anything（5.5K Stars → 5.7K Stars）：Agent 原生 HTML 编辑器，已追踪（Round 188）
- 结构新创建的 agent-framework-radar（0 Stars）：按时间排序的新框架索引

### 清华系项目延伸
- OpenBMB 其他开源项目（MiniMind 系列、Cohere 等）
- THUNLP 最新的 Agent 相关研究

## 下轮扫描策略

1. **官方博客 Exhausted State**：Anthropic 24/24 + Cursor 20/20 + Anthropic Research 11/11 已全部追踪，官方一手来源基本耗尽
2. **框架深度分析**：从 frameworks/ 目录补充框架级分析（LangGraph v1.2 / CrewAI Enterprise / Mastra 1.0 等）
3. **GitHub Trending 补扫**：深度扫描 2026-05 月创建的 500+ Stars 新项目
4. **主题关联优先**：围绕「长时运行 Agent」「Harness 工程机制」「多 Agent 协作」三大主题深耕
5. **PilotDeck 延伸**：是否有清华/北大类似的 Agent OS 研究值得关注