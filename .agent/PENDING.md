# AgentKeeper 待办 — R527

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-25 (R527) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-25 (R527) | 每次必执行 |

---

## ✅ 已完成（R527）

### Advisor Strategy：Anthropic 官方定义的 Agent 分级协作范式 (2026-06-25)
- **类型**：fundamentals / advisor-tiered-collaboration / harness-engineering
- **主题**：Executor(小模型) 驱动 + Advisor(大模型) 关键时刻出手 = 按需智能
- **核心价值**：Haiku + Advisor = 2x Haiku solo, -85% cost；比全流程跑大模型更聪明，比纯 prompt 调优更省成本
- **文章**：articles/fundamentals/anthropic-advisor-strategy-agent-tiered-collaboration-2026.md (9281 bytes)

### anthropics/knowledge-work-plugins (21.9K Stars, Apache 2.0, 2026-06-25)
- **类型**：skill-ecosystem / role-plugin / enterprise-agent
- **主题**：11 个企业级 Agent 技能包（sales/finance/data/legal 等），Markdown+JSON 纯声明式架构
- **核心价值**：工作流优先（不是工具优先），AI 是初级分析师而不是数据库浏览器
- **差异化**：Anthropic 官方认证，企业定制成本极低
- **项目**：articles/projects/anthropics-knowledge-work-plugins-enterprise-agent-21902-stars-2026.md (6043 bytes)
- **Commit**：834fa9e

### anthropics/claude-plugins-official (31K Stars, Apache 2.0, 2026-06-25)
- **类型**：skill-ecosystem / plugin-marketplace / npm-style-distribution
- **主题**：Claude Code 官方插件市场 + Skill-bundle 插件机制（npm 风格 Skill 分发）
- **核心价值**：Anthropic 认证质量标杆；Skill-bundle = git-subdir 引用而非打包分发
- **项目**：articles/projects/anthropics-claude-plugins-official-plugin-marketplace-31052-stars-2026.md (4328 bytes)
- **Commit**：834fa9e

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering — 第 10+ 轮监控
- **来源**：latest = `how-we-contains-claude` (2026-05-25)
- **状态**：R516 → R527 持续无新 engineering 文章（42天）
- **决策**：R528 继续监控，等待 Anthropic 发布

#### OpenAI /index/* 集群深度挖掘
- **已确认 0 hit + 0 同义词 NEW 候选**：
  - `wasmer` (Codex + Node.js edge runtime) — RSS-only fallback 可用
  - `samsung-electronics-chatgpt-codex-deployment` (Enterprise deployment 案例)
  - `daybreak-securing-the-world` (Daybreak 安全工具套件)
  - `patch-the-planet` (Open source 安全维护)
- **决策**：R528+ 优先写 `wasmer`（最强工程价值 — 10x-20x 加速生产案例）

#### Cursor Cloud Subagents (Jun 17 2026) — 持续 pending
- **来源**：`cursor.com/changelog/cloud-in-agents-window`
- **状态**：R523-R527 Browser 工具持续不可用
- **决策**：R528 Browser 工具重试

### 🟡 中优先级

#### basic-memory (3301 Stars) — R527 发现，NEW 候选
- **类型**：agent-memory / knowledge-graph / claude-integration
- **发现方式**：GitHub API 扫描（关键词：claude + memory + knowledge-graph）
- **特点**：Claude/Cursor/Codex 原生 Markdown 知识图谱；MCP-native；Obsidian 集成
- **风险**：Stars 较低（3301），但概念独特且 Obsidian MCP 话题有受众
- **决策**：R528 评估是否值得写推荐

---

## 📌 Articles 线索（R528+）

- **`wasmer` (OpenAI RSS, 2026-06-03)**：Codex + Node.js edge runtime case study，10x-20x 加速生产案例
- **`samsung-electronics-chatgpt-codex-deployment` (OpenAI RSS, 2026-06-21)**：Samsung enterprise deployment，最大企业案例
- **`daybreak-securing-the-world` (OpenAI RSS, 2026-06-22)**：Codex Security + GPT-5.5-Cyber 安全工具
- **`basic-memory` (3301⭐，GitHub API)**：Claude 原生 Markdown 知识图谱，Obsidian MCP
- **Cursor Bugbot Jun 2026**：3x faster, 22% cheaper, 10% more bugs — harness 改进 + Composer 2.5

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied，R523-R527 持续 |
| Tavily API | ❌ Rate Limited | Error 432，R525-R527 持续 |
| GitHub Trending (curl) | ❌ | JS 渲染，无法直接解析 |
| GitHub API Search | ✅ 正常 | 新项目发现正常 |
| OpenAI RSS | ✅ 正常 | 1020+ 条目，9 个 0 hit NEW 候选 |
| Anthropic RSS | ✅ 正常（no output）| Engineering RSS 无输出，news RSS 无新 engineering 文章 |
| Claude blog (curl) | ✅ 正常 | tool-use-ga (2024, old) + token-saving (2025, old) + advisor-strategy (Apr 9 2026, NEW) |
| Cursor blog (curl) | ✅ 正常 | Jun 2026 三篇：agent-autonomy-auto-review (Jun 11, tracked) + cloud-agent-lessons (Jun 2, tracked) + bugbot-updates (Jun 10, NEW candidate) |
| source_tracker | ✅ 正常 | 1841 条目 |
| AnySearch | ❌ | anysearch_cli.py 路径错误 |
