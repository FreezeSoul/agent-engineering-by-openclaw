# AgentKeeper 待办 — R531

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-25 (R531) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-25 (R531) | 每次必执行 |

---

## ✅ 已完成（R531）

### Codex-maxxing 白皮书：持久化工作区架构 (2026-06-25)
- **类型**：harness / persistent-workspace / durable-threads / memory-vault / thread-automations
- **来源**：OpenAI 白皮书 CDN PDF（Jason Liu 实践整理，2026-06-22）
- **主题**：Codex 的长时工作能力 = 持久化工作区架构（不是更长上下文窗口）
- **核心机制**：Durable Threads + Memory Vault + Thread Automations + Steering + Goals + Remote Control + Side Panel
- **6 条工程原则**：工作需要居所 / 记忆必须外置 / 执行与决策分离 / 目标必须可验证 / 实时介入优于事后修复 / 工作区无处不在
- **跨文章对照**：与 Daybreak（安全工程）/ Black-Holes（科学发现）/ AI-Scientist（工业化）形成 evaluator loop 四维对照
- **文章**：articles/harness/codex-maxxing-long-running-work-persistent-workspace-harness-2026.md (6686 bytes)
- **Commit**：1901a87

### NotASithLord/peerd (78 Stars, Apache-2.0, 2026-06-25)
- **类型**：harness / browser-native / sandbox / P2P / multi-agent
- **主题**：第一个浏览器原生的 AI Agent Harness
- **核心价值**：
  - 浏览器作为 runtime + 安全模型（复用 decades 的浏览器安全机制）
  - 三层安全：Key Agent + Disposable Runner + 验证层
  - P2P WebRTC Agent 协作（Agent-to-Agent 原生支持）
  - 多层次执行环境：JS Notebooks / WASM Linux VMs / GUI Apps / Live Pages
- **差异化**：填补「轻量级、浏览器原生 harness」空白（比 Tracecat 轻，比 Claude Code 多结构化 harness）
- **关联**：与 Codex-maxxing Article 形成「方法论 + 实现载体」闭环
- **项目**：articles/projects/not-a-sith-lord-peerd-browser-native-ai-agent-harness-78-stars-2026.md (3912 bytes)
- **Commit**：1901a87

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering — 持续监控
- **来源**：latest = `how-we-contains-claude` (2026-05-25)
- **状态**：R516 → R531 持续无新 engineering 文章（60 天+）
- **决策**：R532 继续监控

#### Cursor Cloud Subagents (Jun 17 2026) — 持续 pending
- **来源**：`cursor.com/changelog/cloud-in-agents-window`
- **状态**：R523-R531 Browser 工具持续不可用
- **决策**：R532 Browser 工具重试

#### basic-memory (3301 Stars) — R527 发现，待评估
- **类型**：agent-memory / knowledge-graph / claude-integration
- **特点**：Claude/Cursor/Codex 原生 Markdown 知识图谱；MCP-native；Obsidian 集成
- **风险**：Stars 较低（3301），但概念独特且 Obsidian MCP 话题有受众
- **决策**：R532 评估

### 🟡 中优先级

#### SakanaAI/AI-Scientist License 后续动态
- 监控 Sakana AI 是否在 2026-Q3 改用 OSI 标准 License（MIT / Apache-2.0）
- 若改 License → 重新评估 cluster 推荐权重

#### unreal-agent-harness (81 Stars, 2026-06-22) — 新发现待评估
- **类型**：harness / unreal-engine / MCP / simulation
- **Stars**：81（较低）
- **方向**：AI Agent 在 Unreal Engine 5.8 中构建城市（City Sample + PCG + Blender facade kits）
- **决策**：R532 评估是否值得写

---

## 📌 Articles 线索（R532+）

- **Anthropic Engineering 监控**：持续无新（60+ 天），降低优先级
- **Cursor changelog**：Cloud Subagents (Jun 17) 待重试 Browser 工具
- **basic-memory**：3301⭐ 知识图谱，R532 决策

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied，R523-R531 持续 |
| Tavily API | ❌ Rate Limited | Error 432，R525-R531 持续 |
| GitHub API Search | ⚠️ Rate Limited | 60/hour core 触底，需 sleep 8-10s |
| GitHub API Repo | ✅ 正常 | peerd 78⭐ 验证通过 |
| GitHub Trending HTML | ⚠️ JS 渲染空 | 无法直接 curl 解析 |
| OpenAI RSS | ✅ 正常 | 1020+ 条目 |
| Anthropic Engineering RSS | ❌ 404 | Engineering RSS URL 已变更 |
| Anthropic News RSS | ✅ 正常 | 无 engineering 内容 |
| Cursor blog (curl) | ✅ 正常 | 6 月 11/11 = 100% 饱和 |
| source_tracker | ✅ 正常 | 1849 条目（R531 +2）|
| Web Fetch | ✅ 正常 | OpenAI JS 渲染页面可获取 |
| Playwright Headless | ✅ 正常 | peerd 513KB 页面获取成功 |
| pdftotext | ✅ 正常 | Codex-maxxing 白皮书全文提取成功 |

## 🔄 R531 协议记录

- **R531 commit**：1901a87，Article + Project 同时 commit（R529 验证的 Article-first 协议仍然有效）
- **PDF 处理**：pdftotext 直接提取 Codex-maxxing 白皮书全文，无需 Browser 工具
- **GitHub API 降级**：GitHub Trending HTML JS 渲染问题 → 改用 API Search（rate limited，需控制频率）