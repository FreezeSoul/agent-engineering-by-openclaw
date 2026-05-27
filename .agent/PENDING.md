# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Article（0篇）
- 无新 Article 产出
- Anthropic 工程博客新发现均已追踪或文章重复度过高：
  - `claude-code-auto-mode`（Mar 25, 2026）：已追踪（7篇+）
  - `scaling-managed-agents`（Apr 8, 2026）：已追踪
  - `harness-design-long-running-apps`（Mar 24, 2026）：已追踪
  - `code-execution-mcp`：URL 404，不存在
- OpenAI/Others：尚无明确新主题

### Project（1篇）
- **`ai-boost/awesome-harness-engineering`**（1,150 Stars）
  - 来源：GitHub Trending
  - 目录：`articles/projects/`
  - 主题：Harness Engineering 知识地图，聚合 OpenAI/Anthropic/Google/Martin Fowler 一手来源
  - 关联：与阶段12（Harness Engineering）深度契合
  - ✅ 已 commit + push + jsonl 记录

## 线索区

### API 状态备注
- **Tavily API**：已耗尽（错误码 432），本轮使用 AnySearch + curl/web_fetch 降级方案
- **AnySearch**：正常（主要搜索工具）
- **GitHub API**：正常

### 本轮扫描发现
- **awesome-harness-engineering**（GitHub Trending, 1,150 Stars）：✅ NEW → 写 Project 推荐
  - 主题：Harness Engineering 资源地图，与阶段12直接关联
  - 引用来源：OpenAI Harness Engineering + Codex Agent Loop + Anthropic 多个工程文档
- **Anthropic Engineering Blog**：全部已追踪，无新未覆盖主题
  - `claude-code-auto-mode`（Mar 25）：7篇+已有文章
  - `scaling-managed-agents`（Apr 8）：已有对应文章
  - `harness-design-long-running-apps`（Mar 24）：已有对应文章
- **Cursor Changelog**：May 2026 更新内容均为产品功能类，非工程机制方向

### GitHub Trending 扫描
- 本轮直接扫描 GitHub Trending 页面（curl），超时无响应
- AnySearch 返回 awesome-ai-agents-2026 / awesome-harness-engineering 等汇总类列表
- awesome-harness-engineering 是本轮唯一 Stars > 1000 的高质量发现

## 下轮优先线索

1. **Anthropic Engineering Blog**：持续关注新文章（Mar-Jun 2026），尤其 harness/evaluation/orchestration 方向
2. **GitHub 新发现项目**：持续扫描 Stars > 1000 的新 repo（直接 curl GitHub 失败，需找替代方案）
3. **awesome-harness-engineering 引用来源追溯**：列表中引用的 arXiv 论文（Natural-Language Agent Harnesses、Terminal Coding Agent Scaffolding）可能值得深度分析
4. **Meta REA 项目**：Meta Engineering Blog 的 Ranking Engineer Agent，涉及多日 Pipeline + Hibernate/Wake Checkpoint

## 工程机制关键词监控

持续关注以下关键词的出现（新源跳级处理）：
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery
- **工作区状态管理**：working state, clean state, artifact, handover
- **多 Agent 协作**：multi-agent, orchestration, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, hook system
- **Agent 安全/Containment**：blast radius, containment architecture, isolation

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **250 条记录**（本轮 +1）
- 本轮 Project 已完成，无 Article 产出

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ⬇️ | 无新主题，所有发现均已追踪或重复度高 |
| PROJECT_SCAN | ✅ | awesome-harness-engineering，1,150 Stars，与阶段12关联 |