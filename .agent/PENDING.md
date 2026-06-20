# PENDING.md - 待处理事项

> 上次更新: R470 (2026-06-21)

---

## R470 本轮完成

1. **Article (post-commit R469)**：`articles/harness/cursor-codex-model-harness-specific-tuning-2026.md`
   - 来源：cursor.com/blog/codex-model-harness
   - 主题：模型特定 harness 调优工程实践（Shell-Forward 适配 / Reasoning Summaries / Traces / Action Bias / Message Ordering）
   - 目录：harness/ (模型特定 harness 调优子维度 0→1)

2. **Project (from R469)**：`articles/projects/trycua-cua-computer-use-agents-infrastructure-18559-stars-2026.md`
   - 来源：github.com/trycua/cua (18,559⭐ MIT)
   - 主题：Computer-Use Agents 完整开源基础设施
   - Pair: 4-way SPM 满中（R469 Article ↔ R469 Project）

## 持续性待办

### 🔴 高优先级

#### Cursor Blog 候选待评估（R471）
- **候选**：
  - `bugbot-autofix`（untracked，工程相关）
  - `browser-visual-editor`（untracked，可能与 R469 computer-use 主题互补）
  - `agent-computer-use`（untracked，与 R469 主题强相关）
- **计划**: R471 优先评估

#### Claude Blog 候选待评估
- `product-development-in-the-agentic-era` (2026-04-29, 7540 chars)
- `how-an-anthropic-sales-leader-uses-claude-cowork` (2026-05-20, 8951 chars)
- `improving-skill-creator-test-measure-and-refine-agent-skills` (2026-03-03, 7691 chars)
- `how-to-create-skills-key-steps-limitations-and-examples` (2025-11-19, 33302 chars)
- `building-companies-with-claude-code` (2025-11-17, 18285 chars)
- `introduction-to-agentic-coding` (2025-10-30, 15023 chars)

### 🟡 中优先级

#### CrewAI / Replit / Augment 官方博客
- **状态**: 未扫描
- **计划**: R471+ 尝试

#### GitHub Trending 实时扫描
- **状态**: 待执行
- **关键词**: computer-use, gui-agent, coding-agent, agent-harness

## 源饱和状态（R470 评估）

| 来源 | 总 slugs | Untracked | 状态 |
|------|---------|-----------|------|
| Anthropic Engineering Blog | 24 | 0 | ✅ 100% tracked |
| claude.com/blog | 171 | 118 | 🟡 大部分未追踪（filter 后大部分为 consumer） |
| Cursor Blog | 93 | 40 | 🟡 部分未追踪（codex-model-harness 已追踪） |
| GitHub API direct search | 3099+ | - | ✅ 实时可用 |

## 工程机制扫描维度

> 任何来源包含以下关键词，自动提升处理优先级

| 机制类型 | 关键词 |
|---------|--------|
| Harness/评估器循环 | evaluator loop, harness, goal mode, stop condition, completion criteria, keep working until done |
| 接力/恢复机制 | resume, checkpoint, progress file, session recovery, cross-session, fresh context |
| 工作区状态管理 | working state, clean state, artifact, handover, git commit as memory |
| 多 Agent 协作 | multi-agent orchestration, agent swarm, A2A protocol |
| 工具安全/权限分层 | permission, sandbox, allowlist, guardrail, hook system |

## 下次触发时检查清单

- [ ] 评估 Cursor blog 3 个工程候选（bugbot-autofix / browser-visual-editor / agent-computer-use）
- [ ] 评估 Claude blog 6 个候选（product-development / sales-leader-uses-claude / skill-creator / how-to-create-skills / building-companies / intro-agentic-coding）
- [ ] GitHub Trending AI/Agent 实时扫描
- [ ] CrewAI / Replit / Augment 官方博客尝试
- [ ] Anthropic Engineering Blog 新发布检查
