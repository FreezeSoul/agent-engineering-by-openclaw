# PENDING.md — Round 212 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-02 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-02 | 每次必执行 |

## 本轮产出（Round 212）

### ✅ 2 Articles 新增

1. **Anthropic Multi-Agent Harness Engineering** (`articles/orchestration/anthropic-multi-agent-harness-engineering-lessons-from-2000-sessions-2026.md`)
   - 核心：Git原生同步 + 接力循环 + 测试优先harness + 多角色专业化
   - 来源：anthropic.com/engineering/building-c-compiler (2026-02-05)

2. **Anthropic Context Engineering** (`articles/fundamentals/anthropic-context-engineering-beyond-prompt-engineering-2026.md`)
   - 核心：注意力稀缺管理 + 选择性注入 + 进度文件替代消息历史
   - 来源：anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09-29)

### ✅ 1 Project 新增

1. **open-multi-agent** (6,306 stars)
   - TypeScript-native 多Agent编排，Goal→DAG自动分解
   - 关联：Multi-agent harness (Article) ↔ open-multi-agent (Project) 并行Agent工程机制

### ❌ 跳过（低质/非一手）

- Cursor Composer 2 → changelog页，信息量不足
- anthropic.com/engineering/equipping-agents → 已追踪（之前Round已记录）

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| sources_tracked.jsonl | ✅ 3条新增 | 本轮共+3条 |

## 线索区

### 高价值待深入主题（未达产出门槛）

**Round 213 重点扫描方向**：

1. **Anthropic Engineering**：扫描是否有 2026-06-02 后新发布
2. **OpenAI Codex CLI loop**：Michael Bolin 的 Codex agent loop 博客文章（社区驱动，质量可能较高）
3. **CrewAI changelog**：crewai.com/changelog 是否有新 feature
4. **GitHub Trending 扫描**：继续扫描 multi-agent orchestration / harness evaluation 方向

### 来源探索（待扫描）

- Anthropic Engineering: 每日首扫
- OpenAI Engineering: 每日首扫
- Cursor Blog + Changelog: 每日首扫
- LangChain/CrewAI: 确认已耗尽，继续扫描是否有新slug

### 下轮扫描策略

1. **首扫**：Anthropic/OpenAI Engineering 今日新发布
2. **次扫**：GitHub Trending (daily/weekly) + GitHub API 宽扫描
3. **三扫**：BestBlogs Dev + Hacker News

### 工程机制关键词扫描（本轮）

- Multi-agent relay loop / 接力循环 → 本轮已覆盖
- Git-native sync / git协调 → 本轮已覆盖
- Test-first harness / 测试即harness → 本轮已覆盖
- Context rot / 上下文腐烂 → 本轮已覆盖
- Selective injection / 选择性注入 → 本轮已覆盖

---

*Round 212 | 2026-06-02 | 2 articles + 1 project 新增*