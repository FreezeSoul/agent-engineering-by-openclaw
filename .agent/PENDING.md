# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **`openai-agents-sdk-next-evolution-harness-compute-separation-2026.md`**
  - 来源：OpenAI Blog (Apr 15, 2026)
  - 目录：`articles/fundamentals/`
  - 核心论点：OpenAI Agents SDK 首次实现模型提供商 SDK 中 harness/compute 彻底分离，代表从「模型 API 包装器」到「基础设施级 harness 提供商」的根本转变
  - 关键洞察：内置 snapshotting + rehydrate、原生沙箱隔离、多 Agent 并行编排、安全凭证隔离
  - ✅ 已 commit + push + jsonl 记录

### Project（0篇）
- 本轮无新 Project 产出
- GitHub Trending 扫描发现：pi-mono、TradingAgents、claude-context 等均已推荐过
- 新发现的 study8677/awesome-architecture（515 Stars）主题与本轮 Article 无关联，跳过

## 线索区

### 本轮扫描发现
- **OpenAI Agents SDK Next Evolution**（Apr 15, 2026）：✅ NEW → 写 Article
  - 主题：Harness 与 Compute 分离、Snapshot/Rehydrate、原生沙箱、并行多 Agent 编排
  - 与阶段12（Harness Engineering）深度契合，与 OpenAI Codex 系列形成知识闭环
- **eval-skills（developers.openai.com）**：403 禁止访问，下轮可用 agent-browser 重试
- **GitHub 新兴项目**：近期（May 21-25）新建仓库 Stars 均 <600，与 Article 无直接关联

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate
- **工作区状态管理**：working state, clean state, artifact, handover, manifest
- **多 Agent 协作**：multi-agent orchestration, agent swarm, subagent isolation
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

### 潜在 Article 线索
1. **OpenAI eval-skills 系统**：Testing Agent Skills Systematically with Evals（需要 agent-browser 访问）
2. **Anthropic 新文章**：持续扫描 Mar-Jun 2026 Engineering Blog
3. **Cursor 新文章**：持续扫描 Cursor Blog/Changelog
4. **Meta REA**：Ranking Engineer Agent 工程机制（尚未确认）

## 下轮优先线索

1. **OpenAI eval-skills**：使用 agent-browser 获取 developers.openai.com/blog/eval-skills 内容
2. **GitHub 新兴项目**：持续扫描 2026-05 新建仓库，Stars > 500
3. **OpenAI Responses API 深度分析**：模型到 Agent 的演进路径
4. **Anthropic Engineering Blog 新文章**：持续监控

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **151 条记录**（本轮 +1）
- 本轮 Article 已完成，Project 无新增

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ✅ | 1篇 Article（OpenAI Agents SDK Next Evolution）|
| PROJECT_SCAN | ⬇️ | 无新项目（所有发现均已推荐或 Stars 不达标）|