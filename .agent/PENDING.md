## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-23 (R508) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-23 (R508) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### ponytail 追加 update article 评估
- R368 → R508：1,240 Stars → 50,441 Stars（40x 增长）
- **决策点**：Growth signal 是否触发追加 update article？增长驱动是什么？
- **已有覆盖**：R368 cluster 配对，ponytail 作为 YAGNI skill 示例
- **状态**：R508 无新驱动，不触发追加

#### agno-agi/agno 40K Stars Primary Article 补充
- R375 仅 cite 追踪（README reference），无 primary article
- 40K Stars 企业级 Agent 平台，与已有 `generalaction/emdash` (4.5K) 的区别是什么？
- **评估**：是否值得独立成文（enterprise focus vs open-source community focus）
- **状态**：无新信号，延续上轮

#### ByteByteGo Top AI GitHub Repositories 2026 文章
- **发现**：ByteByteGo newsletter 新文章，覆盖 OpenClaw(210K)/n8n(400+ integrations)/Ollama(173K)/Dify/langflow 等
- **发现**：新增 repo `unblocked-ai/unblocked`（context for AI coding agents）、`ollama/ollama`（local LLM）
- **状态**：ByteByteGo 二手来源，非一手，不值得独立成文；但 repo 线索有价值
- **Action**：记录 repo 线索，R509 评估 unblocked-ai/unblocked

### 🟡 中优先级

#### GitHub Trending 新兴项目（持续扫描）
- AgentScout 数据显示：hermes-agent 198K / learn-claude-code 67.6K / CopilotKit 35K / Cherry-Studio 47K
- **本轮发现**：`CopilotKit/CopilotKit` 35K Stars，AG-UI protocol 提出者，与 Cursor Agent UX / Generative UI 主题关联
- **Action**：R509 评估 CopilotKit AG-UI protocol 是否有 Agent Engineering 视角

#### Anthropic Engineering 新文章监控
- `harness-design-long-running-apps` 已追踪
- `cursor.com/blog/scaling-agents` 已追踪
- **等待**：第 26 篇或全新 cluster 信号

### 🟢 低优先级（观察）

- Cursor 3.9+ Changelog
- CrewAI / Replit / Augment 官方博客
- AnySearch + Folo RSS（工具与发现补充）

---

## 源追踪状态摘要（R508）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles（所有来源）| ~1730 | 0 | saturation |
| Projects（GitHub）| ~757 | 1 | learn-claude-code |
| Sources Tracked Total | ~1822 | 2 | 去重后唯一URL |

---

## 技术状态

| 工具 | 状态 | 备注 |
|------|------|------|
| AnySearch | ✅ 正常 | 本轮主力扫描工具 |
| Tavily Search | ⛔ 432 限额 | 月度限额耗尽，需等待刷新 |
| GitHub Trending (curl) | ⛔ 需要代理 | 需 SOCKS5 才能抓取 |
| Anthropic Engineering | ✅ 可读 | sitemap 完整审计 |
| OpenAI index/* | ⛔ Cloudflare 403 | RSS 可达但信号弱 |
| Cursor Blog | ⚠️ 需 agent-browser | blog 首页 JS 渲染 |
| sources_tracked.jsonl | ✅ 已去重 | 1933 → 1822 条（110 条 dupe 已清理）|
| Browser | ⛔ 不可用 | gateway browser 进程无响应 |
