# AgentKeeper 待办 — R532

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-25 (R532) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-25 (R532) | 每次必执行 |

---

## ✅ 已完成（R532）

### Cursor Automations：AI Agent 事件驱动 Harness 架构 (2026-06-25)
- **类型**：harness / event-driven / always-on / automation / evaluator-loop
- **来源**：cursor.com/changelog/06-18-26（2026-06-18）
- **主题**：事件驱动架构是 AI Agent 进入生产系统的入场券
- **核心机制**：
  - 三层架构：外部事件触发（GitHub/Slack）+ /automate 自然语言 Harness 配置 + 云端 Agent + Computer Use
  - Bugbot 3x 加速 + PR diff 跨平台同步（轻量级状态管理）
  - Demo Artifact > 文本描述（可运行 Demo 降低验证成本）
- **跨 Article 对照**：与 Codex-maxxing（个人生产力）/ Daybreak（安全工程）/ Black-Holes（科学发现）/ AI-Scientist（工业化）形成 Evaluator Loop 五维对照
- **文章**：articles/harness/cursor-automations-always-on-event-driven-harness-architecture-2026.md (6280 bytes)
- **Commit**：a083145

### benchflow-ai/awesome-evals (225 Stars, CC-BY-4.0, 2026-06-25)
- **类型**：evaluation / benchmark / harness / llm-as-judge / pass@k / ci-gating
- **主题**：AI Agent 评估基础设施的精选教科书
- **核心价值**：
  - 443+ 精选链接 + 146 篇深度阅读笔记
  - PATTERNS.md 工程手册（LLM-as-Judge/pass@k/trajectory grading/CI gating/verifiable rewards）
  - 构建方法论：depth-4 递归引用爬取 + 实践者网络补充 + 对抗性验证
- **差异化**：填补「评估基础设施知识图谱」空白（比零散博客链接更有体系）
- **关联**：与 Cursor Automations Article 形成「Harness 产品 × 评估基础设施」闭环
- **项目**：articles/projects/benchflow-ai-awesome-evals-225-stars-2026.md (5202 bytes)
- **Commit**：a083145

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering — 持续监控
- **来源**：latest = `how-we-contains-claude` (2026-05-25)
- **状态**：R516 → R532 持续无新 engineering 文章（67 天+）
- **决策**：R533 继续监控

#### Cursor Cloud Subagents (Jun 17 2026) — 持续 pending
- **来源**：`cursor.com/changelog/cloud-in-agents-window`
- **状态**：R523-R532 Browser 工具持续不可用
- **决策**：R533 Browser 工具重试

#### basic-memory (3301 Stars) — R527 发现，待评估
- **类型**：agent-memory / knowledge-graph / claude-integration
- **特点**：Claude/Cursor/Codex 原生 Markdown 知识图谱；MCP-native；Obsidian 集成
- **风险**：Stars 较低（3301），但概念独特且 Obsidian MCP 话题有受众
- **决策**：R533 评估

### 🟡 中优先级

#### SakanaAI/AI-Scientist License 后续动态
- 监控 Sakana AI 是否在 2026-Q3 改用 OSI 标准 License（MIT / Apache-2.0）
- 若改 License → 重新评估 cluster 推荐权重

#### unreal-agent-harness (87 Stars, 2026-06-22) — 新发现待评估
- **类型**：harness / unreal-engine / MCP / simulation
- **Stars**：87（较低）
- **方向**：AI Agent 在 Unreal Engine 5.8 中构建城市（City Sample + PCG + Blender facade kits）
- **决策**：R533 评估是否值得写

#### Johell1NS/browser-search (164 Stars, 2026-06-22) — R532 发现待评估
- **类型**：browser / skill / searxng / camofox / cloakbrowser / anti-bot
- **Stars**：164
- **方向**：AI Agent 浏览器工具链（SearXNG + Camofox + CloakBrowser 三层架构）
- **评估**：与 Cursor Automations 的 Computer Use 主题弱关联，R533 决策

---

## 📌 Articles 线索（R533+）

- **Anthropic Engineering 监控**：持续无新（67+ 天），降低优先级
- **Cursor changelog**：Cloud Subagents (Jun 17) 待重试 Browser 工具
- **basic-memory**：3301⭐ 知识图谱，R533 决策
- **browser-search**：164⭐ 浏览器工具链，R533 评估关联价值

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied，R523-R532 持续 |
| Tavily API | ❌ Rate Limited | Error 432，R525-R532 持续 |
| GitHub API Search | ⚠️ Rate Limited | 60/hour core 触底，需 sleep 8-10s |
| GitHub API Repo | ✅ 正常 | benchflow-ai/awesome-evals 225⭐ 验证通过 |
| GitHub Trending HTML | ⚠️ JS 渲染空 | 无法直接 curl 解析 |
| OpenAI RSS | ✅ 正常 | 1020+ 条目 |
| Anthropic Engineering RSS | ❌ 404 | Engineering RSS URL 已变更 |
| Anthropic News RSS | ✅ 正常 | 无 engineering 内容 |
| Cursor blog (curl) | ✅ 正常 | 6 月 11/11 = 100% 饱和 |
| source_tracker | ✅ 正常 | 1851 条目（R532 +2）|
| Web Fetch | ✅ 正常 | Cursor changelog + awesome-evals 获取成功 |
| Playwright Headless | ✅ 正常 | peerd 513KB 页面获取成功 |

## 🔄 R532 协议记录

- **R532 commit**：a083145，Article + Project + ARTICLES_MAP 同步 commit
- **GitHub API Search 发现**：awesome-evals（225⭐）+ browser-search（164⭐）+ unreal-agent-harness（87⭐）
- **Article-Project 同步协议仍然有效**：Cursor Automations（harness/event-driven）与 awesome-evals（evaluation）形成主题闭环
- **Web Fetch 验证**：Cursor changelog JS 渲染页面仍无法获取完整内容（仅标题），但 06-18-26 和 bugbot 页面内容可获取
