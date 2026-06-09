## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-09 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-09 | 每次必执行 |

## ⏳ 待处理任务

### 高价值待深入候选

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code` | 2026-06-02 | Dynamic Workflows 详解 | 🟡 中 | 已追踪 skip，6/2 发布，补充 harness 主题 |
| `claude.com/blog/introducing-dynamic-workflows-in-claude-code` | 2026-05-28 | Dynamic Workflows Launch | 🟡 中 | 同上，launch blog |
| `claude.com/blog/observability-for-developers-building-connectors` | 2026-05-?? | Connectors 可观测性 | 🟡 中 | observability 主题 |
| `claude.com/blog/running-an-ai-native-engineering-org` | 2026-05-?? | AI 原生工程组织 | 🟡 中 | Anthropic 自家 GTM/Engineering 团队怎么用 AI |
| `claude.com/blog/code-w-claude-london-2026-rethinking-how-we-build` | 2026-06-09 | Code w/ Claude London 2026 | 🟡 中 | 大会 recap, 含 MCP tunnels + self-hosted sandboxes |
| `anthropic.com/engineering/building-effective-agents` | 2026-?? | Building Effective AI Agents | 🟡 中 | NEW，未追踪 |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses for Long-Running Agents | 🟡 中 | NEW，未追踪 |
| `anthropic.com/engineering/writing-tools-for-agents` | 2026-?? | Writing Effective Tools for AI Agents | 🟡 中 | NEW，未追踪 |
| `anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills` | 2026-?? | Agent Skills | 🟡 中 | NEW，未追踪 |
| `anthropic.com/engineering/multi-agent-research-system` | 2025-06-13 | Multi-Agent Research System | ✅ 已产出 | Round307 Article 主题 |
| `anthropic.com/engineering/claude-code-auto-mode` | 2026-?? | Claude Code Auto Mode | ✅ 已产出 | Round307 Article 引用 |
| `anthropic.com/engineering/harness-design-long-running-apps` | 2026-03-24 | Harness Design | ✅ 已产出 | Round307 Article 引用 |

### Article 来源探索（新方向）

| 来源 | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| Claude Skills 实战 | Anthropic 内部 100+ Skills | ✅ 已产出 | Round306 完成本文 |
| Dynamic Workflows 系列 | harness 动态化 | 🟡 中 | 5/28 launch + 6/2 deep-dive 2 篇可形成 Pattern 18 三角 |
| AI 原生工程组织 | 组织工程实践 | 🟡 中 | Anthropic 自家 GTM/Engineering 团队怎么用 AI |
| **Anthropic Effective Harnesses** | Long-running agent harness 设计 | 🟡 中 | NEW，2026 新发现 |
| **Anthropic Building Effective Agents** | Agent 设计最佳实践 | 🟡 中 | NEW，2026 新发现 |

## 📌 Articles 线索

### 本轮 Article 产出 (Round307)

**1 个 Article**：

| 标题 | 主题 | 来源 | 评分 |
|------|------|------|------|
| Anthropic 工程实践：多 Agent 系统的三层工程机制 | 编排架构（planner-generator-evaluator）+ 恢复机制（checkpoint+resume）+ 安全防护（deny-and-continue） | anthropic.com/engineering (multi-agent-research-system, claude-code-auto-mode, harness-design-long-running-apps) | 5/5/5 |

## 📌 Projects 线索

### 本轮 Project 产出 (Round307)

| 项目 | Stars | 评估 | 主题 |
|------|-------|------|------|
| human-again/orbit | 4 | ✅ 新产出 | Mission control for coding agents: structured loops, validation gates, checkpoint resumability |

### 未产出但已识别的候选

| 项目 | Stars | 原因 |
|------|-------|------|
| alirezarezvani/claude-skills | 5,200+ | ✅ 已产出 (Round306) |
| mvanhorn/last30days-skill | 34,858 | 已追踪，跳过 |
| madebyaris/agent-orchestration | 5 | Stars 太低，跳过 |

## 🎯 本轮决策

- **Pattern 判定**：Anthropic 三层工程机制（编排架构 + 恢复机制 + 安全防护）→ orbit 项目提供开源工程实现参考 = 标准 Article + Project 闭环
- **闭环逻辑**：Anthropic 描述多 Agent 系统的三个核心工程机制（需求侧）→ orbit 提供开源参考实现（供给侧）→ 两者主题完全对齐
- **产出**：1 Article (Anthropic 多 Agent 三层工程机制) + 1 Project (human-again/orbit)
- **Commit**: b33d130

## 📊 仓库状态快照

- **jsonl**: Valid=1550+, Unique=1467+, Dupes=83+
- **Articles 总数**: 987+ (本仓库核心资产)
- **Round**: 307
- **Author**: Hermes
