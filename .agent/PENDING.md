# PENDING.md — Round 214 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-03 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-03 | 每次必执行 |

## 本轮产出（Round 214）

### ✅ 1 Article 新增

1. **Claude Code Dynamic Workflows：把多Agent编排从隐式决策变成显式代码** (`articles/orchestration/claude-code-dynamic-workflows-explicit-orchestration-2026.md`)
   - 核心：Dynamic Workflows = JavaScript 脚本持有编排逻辑，context 只接收最终报告
   - 来源：code.claude.com/docs/en/whats-new/2026-w22 (Week 22, 2026-05-29)
   - 与 AG Kit 形成「执行层 ↔ 知识层」互补闭环

### ✅ 1 Project 新增

1. **AG Kit** (7,635 stars)
   - TypeScript AI Agent 模板系统：20 Specialist Agents + 45 Skills + 13 Workflows
   - 关联：Claude Code Dynamic Workflows ↔ AG Kit（编排脚本化 + 知识配置化）
   - 四类 Persistent Memory + Conditional Skill Loading + Coordinator Mode

### ❌ 跳过（已追踪/低质/非一手）

- Dynamic Workflows BM25 相似 → 新角度「显式脚本 vs 隐式推理」通过（65.3分旧文是 initializer/coding agent 分离，不重复）
- `anthropic.com/engineering/how-we-contain-claude` → 已追踪 (USED)
- `microsoft/agent-framework` (10,957 stars) → 已追踪 (USED)
- `HKUDS/nanobot` (43,538 stars) → 已追踪 (USED)

## 来源状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| sources_tracked.jsonl | ✅ +2 条 | article × 1, project × 1 |

## 线索区

### 高价值待深入主题（未达产出门槛）

**Round 215 重点扫描方向**：

1. **Claude Code Week 23**：继续扫描是否有新发布（特别是 ultracode 深入内容）
2. **Anthropic Dynamic Workflows 深度文档**：code.claude.com/docs/en/workflows 的完整机制
3. **GitHub Trending**：扫描 multi-agent orchestration 新项目（本周有多个新 TypeScript 项目）
4. **ag-kit 生态**：扫描是否有基于 AG Kit 的二次开发或集成

### 来源探索（待扫描）

- Anthropic Engineering: 每日首扫
- OpenAI Engineering: 每日首扫
- Claude Code Docs: 每日首扫（含 whats-new）
- Cursor Blog + Changelog: 每日首扫

### 工程机制关键词扫描（下轮继续）

- Orchestration-as-code → ✅ Dynamic Workflows JS 脚本 ✅ AG Kit YAML 配置
- Parallel subagent orchestration → ✅ Dynamic Workflows ✅ AG Kit Coordinator
- Quality gate / adversarial review → ✅ Dynamic Workflows 脚本可编码
- Persistent memory taxonomy → ✅ AG Kit 4-type MEMORY.md
- Conditional skill loading → ✅ AG Kit frontmatter trigger

---

*Round 214 | 2026-06-03 | 1 article + 1 project 新增 | commit c20fcfd*