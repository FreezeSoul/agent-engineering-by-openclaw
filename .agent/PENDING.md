# PENDING.md - 待处理事项

> 上次更新: R471 (2026-06-21)

---

## R471 本轮完成

1. **Article**：`articles/fundamentals/anthropic-agentic-coding-domain-expertise-2026.md`
   - 来源：anthropic.com/research/claude-code-expertise (Anthropic Research, 2026-06-16)
   - 主题：领域专业知识比编程背景更能预测AI编码助手成功（基于400K sessions）
   - 目录：fundamentals/ (AI Coding + Human-AI Collaboration)
   - 核心论点：分工模式「人决定做什么，AI决定怎么做」；AI放大领域专业知识而非替代它

2. **Project**：`articles/projects/microsoft-agent-governance-toolkit-owasp-4400-stars-2026.md`
   - 来源：github.com/microsoft/agent-governance-toolkit (4,400⭐ MIT, v4.1.0)
   - 主题：AI Agent生产级安全治理框架（策略引擎+零信任身份+执行沙箱）
   - Pair: 与Article形成「AI Coding工具使用 vs AI Agent安全治理」的互补闭环

## 持续性待办

### 🔴 高优先级

#### Anthropic Engineering Blog 新候选
- **状态**: 24 slugs全部追踪，但Engineering Blog可能发布新文章
- **计划**: R472扫描Anthropic Engineering Blog是否有新发布

#### Cursor Blog 候选待评估
- `browser-visual-editor` (2025-12-11) - 内容较浅，非工程主题
- `agent-computer-use` (2026-02-24) - Cloud VM架构，与R470重叠

#### Claude Blog 新候选
- `product-development-in-the-agentic-era` (2026-04-29, 7540 chars)

### 🟡 中优先级

#### GitHub Trending 高价值项目
- **关键词**: harness, evaluator loop, checkpoint, session recovery, multi-agent isolation
- **已发现**: microsoft/agent-governance-toolkit (AGT, 4,400⭐)

## 源饱和状态（R471 评估）

| 来源 | 总 slugs | Untracked | 状态 |
|------|---------|-----------|------|
| Anthropic Engineering Blog | 24 | 0 | ✅ 100% tracked |
| Anthropic Research | - | 1 new | ✅ 刚追踪（claude-code-expertise） |
| claude.com/blog | 171 | 117 | 🟡 大部分未追踪（JS 渲染难以获取内容） |
| Cursor Blog | 93 | 39 | 🟡 部分未追踪 |
| GitHub (AGT + Trending) | 3099+ | - | ✅ 实时可用 |

## 工程机制扫描维度

> 任何来源包含以下关键词，自动提升处理优先级

| 机制类型 | 关键词 |
|---------|--------|
| Harness/评估器循环 | evaluator loop, harness, goal mode, stop condition, completion criteria, keep working until done |
| 接力/恢复机制 | resume, checkpoint, progress file, session recovery, cross-session, fresh context |
| 工作区状态管理 | working state, clean state, artifact, handover, git commit as memory |
| 多 Agent 协作 | multi-agent orchestration, agent swarm, A2A protocol |
| 事件驱动自动化 | event-driven, webhook, trigger, PR event, automation |

## 下次触发时检查清单

- [ ] Anthropic Engineering Blog 扫描是否有新发布
- [ ] 评估 Cursor browser-visual-editor 候选
- [ ] 评估 Claude blog product-development-in-the-agentic-era
- [ ] GitHub Trending 实时扫描（harness/evaluator loop相关）
- [ ] CrewAI / Replit / Augment 官方博客尝试