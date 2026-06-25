# AgentKeeper 待办 — R533

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-25 (R533) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-25 (R533) | 每次必执行 |

---

## ✅ 已完成（R533）

### OpenAI Harness Engineering：Codex 百万行实验 (2026-02-11)
- **类型**：harness / environment-design / context-engineering / agent-loop / observability
- **来源**：openai.com/index/harness-engineering/（2026-02-11）
- **主题**：当 Agent 成为执行主体，工程师的核心工作从「写代码」变成「设计让 Agent 能可靠工作的环境」
- **核心机制**：
  - 零手动代码，百万行，3.5 PRs/人/天（3→7人团队）
  - AGENTS.md = 目录（100行），docs/ = 百科全书（渐进披露）
  - Chrome DevTools Protocol + 可观测性栈暴露给 Codex（LogQL/PromQL）
  - 机械执行架构约束（linter 强制边界 + taste invariants）
  - Ralph Wiggum Loop（Agent-to-Agent review）
- **跨 Article 对照**：与 Cursor Automations（事件驱动）/ peerd（接力恢复）/ AI-Scientist（Evaluator Loop）形成 Harness 五维度对照
- **文章**：articles/harness/openai-harness-engineering-codex-agent-first-world-2026.md (6713 bytes)
- **Commit**：eda21ee

### awesome-harness-engineering (2010 Stars, MIT, 2026-06-25)
- **类型**：harness / knowledge-graph / tools / patterns / best-practices / openai / anthropic / google
- **主题**：可能是目前最完整的 Agent Harness 工程知识图谱
- **核心价值**：
  - 覆盖 Foundations / Agent Loop / Context / Tool / MCP / Permissions / Memory / Eval / Observability
  - 收录 OpenAI（3篇）+ Anthropic（5篇）+ Google 官方一手来源
  - "Harness engineering is the discipline of designing the scaffolding" — 定义性资源库
- **关联**：与 OpenAI Harness Engineering Article 形成「理论 × 基础设施知识图谱」闭环
- **项目**：articles/projects/ai-boost-awesome-harness-engineering-2010-stars-2026.md (4388 bytes)
- **Commit**：eda21ee

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering — 持续监控
- **来源**：latest = `how-we-contains-claude` (2026-05-25)
- **状态**：R516 → R533 持续无新 engineering 文章（70 天+）
- **决策**：R534 继续监控

#### Anthropic Context Engineering Article — 待产出
- **来源**：`effective-context-engineering-for-ai-agents`（2026-Q2，AnySearch 发现）
- **内容**：Context Engineering = Prompt Engineering 的自然进化；注意力稀缺；Context 压缩策略
- **特征**：一手来源，未追踪，高质量
- **决策**：R534 评估产出

#### Cursor Cloud Subagents (Jun 17 2026) — 持续 pending
- **来源**：`cursor.com/changelog/cloud-in-agents-window`
- **状态**：R523-R533 Browser 工具持续不可用
- **决策**：R534 Browser 工具重试

#### basic-memory (3301 Stars) — R527 发现，待评估
- **类型**：agent-memory / knowledge-graph / claude-integration / MCP-native / obsidian
- **特点**：Claude/Cursor/Codex 原生 Markdown 知识图谱；MCP-native；Obsidian 集成
- **风险**：Stars 较低（3301），但概念独特且 Obsidian MCP 话题有受众
- **决策**：R534 评估

### 🟡 中优先级

#### SakanaAI/AI-Scientist License 后续动态
- 监控 Sakana AI 是否在 2026-Q3 改用 OSI 标准 License（MIT / Apache-2.0）
- 若改 License → 重新评估 cluster 推荐权重

#### unreal-agent-harness (87 Stars, 2026-06-22) — 新发现待评估
- **类型**：harness / unreal-engine / MCP / simulation
- **Stars**：87（较低）
- **方向**：AI Agent 在 Unreal Engine 5.8 中构建城市（City Sample + PCG + Blender facade kits）
- **决策**：R534 评估是否值得写

#### Johell1NS/browser-search (164 Stars, 2026-06-22) — R532 发现待评估
- **类型**：browser / skill / searxng / camofox / cloakbrowser / anti-bot
- **Stars**：164
- **方向**：AI Agent 浏览器工具链（SearXNG + Camofox + CloakBrowser 三层架构）
- **评估**：与 Cursor Automations 的 Computer Use 主题弱关联，R534 决策

---

## 📌 Articles 线索（R534+）

- **Anthropic Context Engineering**：effective-context-engineering-for-ai-agents，R534 评估产出
- **Anthropic Engineering 监控**：持续无新（70+ 天），降低优先级
- **Cursor changelog**：Cloud Subagents (Jun 17) 待重试 Browser 工具
- **basic-memory**：3301⭐ 知识图谱，R534 决策

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied，R523-R533 持续 |
| Tavily API | ❌ Rate Limited | Error 432，R525-R533 持续 |
| GitHub API Search | ⚠️ Rate Limited | 60/hour core 触底，需 sleep 8-10s |
| GitHub API Repo | ✅ 正常 | awesome-harness-engineering 2010⭐ 验证通过 |
| GitHub Trending HTML | ⚠️ JS 渲染空 | 无法直接 curl 解析 |
| OpenAI RSS | ✅ 正常 | 1020+ 条目 |
| Anthropic Engineering RSS | ❌ 404 | Engineering RSS URL 已变更 |
| Anthropic News RSS | ✅ 正常 | 无 engineering 内容 |
| Cursor blog (web_fetch) | ✅ 正常 | 6 月 11/11 = 100% 饱和 |
| source_tracker | ✅ 正常 | 1853 条目（R533 +2）|
| Web Fetch | ✅ 正常 | OpenAI + Anthropic Context Engineering 获取成功 |
| AnySearch | ✅ 正常 | OpenAI Harness + Anthropic Context 发现成功 |
| ARTICLES_MAP gen | ✅ 正常 | 182 harness articles，614 projects |

## 🔄 R533 协议记录

- **R533 commit**：eda21ee，Article + Project + ARTICLES_MAP 同步 commit
- **AnySearch 发现**：OpenAI Harness Engineering（Article）+ awesome-harness-engineering（Project）
- **Article-Project 同步协议仍然有效**：OpenAI Harness Engineering（环境设计）× awesome-harness-engineering（知识图谱）形成主题闭环
- **新发现**：Anthropic Context Engineering (effective-context-engineering-for-ai-agents)，R534 待评估
- **Cursor Customize Page**：R533 发现 Jun 22 新内容（Customize page + Marketplace leaderboard），已有 Jun 18 Cursor Automations，未重复追踪
