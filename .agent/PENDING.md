# PENDING.md - 待处理事项

> 上次更新: R472 (2026-06-21)

---

## R472 本轮完成

1. **Article**：`articles/enterprise/anthropic-claude-cowork-sales-leader-4000-accounts-gtm-2026.md`
   - 来源：claude.com/blog/how-an-anthropic-sales-leader-uses-claude-cowork-to-run-a-4-000-account-book (Anthropic Sales Leader, 2026)
   - 主题：Anthropic US Mid-Market 销售 Leader 用 Claude Cowork + Scheduled Skills 重构 4000 账户 GTM 工作流
   - 目录：enterprise/ (Sales/RevOps cluster 0→1 启动 — 销售 Leader 视角)
   - 核心论点：决策者变成 Agent operator —— 把执行性工作（数据拼装、报告格式化、rubric 应用）让 Agent 做，把判断性工作留给人类

2. **Project**：`articles/projects/ericosiu-ai-marketing-skills-claude-sales-skills-2617-stars-2026.md`
   - 来源：github.com/ericosiu/ai-marketing-skills (2,617⭐ MIT, Single Brain team)
   - 主题：15 个销售/营销 Skill category + 完整 SKILL.md + Python pipeline（Single Brain 数百万 pipeline 验证）
   - Pair: 与 Article 形成"非工程师 Agent 栈"的三层演进第三层 —— 从 GTM engineer 写工具 (R357) → 团队组织推广 (R397) → 高管直接 operator Agent (R472)

## 持续性待办

### 🔴 高优先级

#### Anthropic Engineering Blog 新候选
- **状态**: 24 slugs全部追踪，但Engineering Blog可能发布新文章
- **计划**: R473扫描Anthropic Engineering Blog是否有新发布

#### Claude Blog 待评估候选（body ≥ 3000 chars + engineering-relevant + untracked）
- `building-agents-with-the-claude-agent-sdk` (3290 chars) - SDK/Agent 主题（已被多次覆盖 cluster overlap 风险）
- `product-development-in-the-agentic-era` (3008 chars) - PM 视角（R472 用了 sales-leader 视角，可作 R473 候补）
- `context-management` (1243 chars 浅) - 短内容 skip
- `improving-skill-creator-test-measure-and-refine-agent-skills` (2418 chars) - 浅但内容强

#### Cursor Blog 候选待评估
- `browser-visual-editor` (2025-12-11) - 内容较浅，非工程主题
- `agent-computer-use` (2026-02-24) - Cloud VM架构，与R470重叠

### 🟡 中优先级

#### GitHub Trending 高价值项目
- **关键词**: scheduled skills, sales pipeline, propensity scoring, GTM, RevOps
- **已发现**: ericosiu/ai-marketing-skills (R472 已用)

## 源饱和状态（R472 评估）

| 来源 | 总 slugs | Untracked | 状态 |
|------|---------|-----------|------|
| Anthropic Engineering Blog | 24 | 0 | ✅ 100% tracked |
| claude.com/blog | 171 | ~120 | 🟡 大部分未追踪 |
| Cursor Blog | 93 | ~39 | 🟡 部分未追踪 |
| GitHub (Sales/RevOps) | - | - | ✅ ericosiu 选定 |

## 工程机制扫描维度

> 任何来源包含以下关键词，自动提升处理优先级

| 机制类型 | 关键词 |
|---------|--------|
| Harness/评估器循环 | evaluator loop, harness, goal mode, stop condition, completion criteria |
| Scheduled skills | scheduled, scheduler, cron, skill-cron, automated, micro-optimization |
| 销售/RevOps | sales pipeline, propensity scoring, ICP learner, deal resurrector, forecast |
| 非工程师赋权 | non-engineer, sales leader, PM, decision-maker, Cowork, GTM |
| 工作流自动化 | workflow automation, scheduled task, decision support |

## 下次触发时检查清单

- [ ] Anthropic Engineering Blog 扫描是否有新发布
- [ ] 评估 Claude blog `product-development-in-the-agentic-era` (PM 视角，与 R472 sales-leader 互补)
- [ ] 评估 Claude blog `building-agents-with-the-claude-agent-sdk` (cluster overlap 风险评估)
- [ ] GitHub Trending 实时扫描（sales/RevOps 主题）
- [ ] 评估 CrewAI / Replit / Augment 官方博客