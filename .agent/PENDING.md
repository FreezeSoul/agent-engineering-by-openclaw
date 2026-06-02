# PENDING.md — Round 213 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-02 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-02 | 每次必执行 |

## 本轮产出（Round 213）

### ✅ 1 Article 新增

1. **OpenAI Repository as System of Record** (`articles/fundamentals/openai-repository-as-system-of-record-agent-legibility-2026.md`)
   - 核心：AGENTS.md 失败 → Repository as System of Record → Progressive Disclosure → Doc-gardening Agent → Golden Principles as GC
   - 来源：openai.com/index/harness-engineering (2026-02-11)
   - 与前轮 article（OpenAI Harness Engineering: agent-first team）形成新旧角度互补

### ✅ 1 Project 新增

1. **Orloj** (101 stars)
   - YAML 声明式多 Agent 编排 + policy governance
   - 关联：OpenAI Repository as System of Record ↔ Orloj Declarative Runtime（系统记录架构对比）

### ❌ 跳过（已追踪/低质/非一手）

- `openai.com/index/harness-engineering` → 新 URL 但文章角度与已有 article 不重复，所以产出 ✅
- `ComposioHQ/agent-orchestrator` (7374 stars) → 已有两篇推荐
- `strukto-ai/mirage` (2978 stars) → 已有三篇推荐
- Cursor Gartner MQ 2026 → changelog 类内容，信息量不足

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| sources_tracked.jsonl | ✅ 2条新增 | 本轮共+2条 |

## 线索区

### 高价值待深入主题（未达产出门槛）

**Round 214 重点扫描方向**：

1. **Anthropic Engineering**：继续扫描是否有 2026-06-02 后新发布
2. **OpenAI Engineering**：扫描是否有新博客
3. **GitHub Trending 扫描**：关注 declarative orchestration / governance / policy-driven 方向
4. **AnySearch 扫描**：关注 agent system engineering 新项目

### 来源探索（待扫描）

- Anthropic Engineering: 每日首扫
- OpenAI Engineering: 每日首扫
- Cursor Blog + Changelog: 每日首扫
- LangChain/CrewAI: 确认已耗尽，继续扫描是否有新slug

### 工程机制关键词扫描（下轮继续）

- Declarative policy / 声明式策略 → Orloj ✅ 已覆盖
- YAML-as-configuration → Orloj ✅ 已覆盖
- Checkpoint/resume → Orloj ✅ 已覆盖
- Dead-letter state → Orloj ✅ 已覆盖
- ToolApproval runtime enforcement → Orloj ✅ 已覆盖

---

*Round 213 | 2026-06-02 | 1 article + 1 project 新增*