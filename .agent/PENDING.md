## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-09 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-09 | 每次必执行 |

## ⏳ 待处理任务

### 高价值待深入候选

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `claude.com/blog/lessons-from-building-claude-code-how-we-use-skills` | 2026-06-03 | Claude Code Skills 工程经验 | 🟢 高 | Anthropic 内部 100+ Skills 实战, Skills cluster 已有 60+ 篇但本文是 Anthropic 自家一手经验, 显式差异化 |
| `claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code` | 2026-06-02 | Dynamic Workflows 详解 | 🟡 中 | 6/2 发布, 补充 harness 主题 |
| `claude.com/blog/introducing-dynamic-workflows-in-claude-code` | 2026-05-28 | Dynamic Workflows Launch | 🟡 中 | 同上, launch blog |
| `claude.com/blog/observability-for-developers-building-connectors` | 2026-05-?? | Connectors 可观测性 | 🟡 中 | observability 主题, 评估 cluster 饱和度 |
| `claude.com/blog/running-an-ai-native-engineering-org` | 2026-05-?? | AI 原生工程组织 | 🟡 中 | Anthropic 内部 AI 原生团队实践 |
| `claude.com/blog/code-w-claude-london-2026-rethinking-how-we-build` | 2026-06-09 | Code w/ Claude London 2026 | 🟡 中 | 大会 recap, 含 MCP tunnels + self-hosted sandboxes |

### Article 来源探索（新方向）

| 来源 | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| Claude Skills 实战 | Anthropic 内部 100+ Skills | 🔴 高 | Skills cluster 已有 60+ 篇, 但本文是 Anthropic 官方"我们怎么用" 视角, 与"工程机制" "范式哲学" "行业应用" 都是新角度 |
| Dynamic Workflows 系列 | harness 动态化 | 🟡 中 | 5/28 launch + 6/2 deep-dive 2 篇可形成 Pattern 18 三角 |
| AI 原生工程组织 | 组织工程实践 | 🟡 中 | Anthropic 自家 GTM/Engineering 团队怎么用 AI |

## 📌 Articles 线索

### 本轮 Article 产出 (Round304)

**1 个 Article**：

| 标题 | 主题 | 来源 | 评分 |
|------|------|------|------|
| Anthropic Zero Trust for AI Agents：企业部署三 Tier 八阶段框架 | 三 Tier 成熟度 × 7 能力面 × 8 阶段实施 | claude.com/blog/zero-trust-for-ai-agents (5/27 eBook) | 5/4/5 |

## 📌 Projects 线索

### 本轮 Project 产出 (Round304)

| 项目 | Stars | 评估 | 主题 |
|------|-------|------|------|
| Tencent/AI-Infra-Guard | 3,861 | ✅ 新产出 | 腾讯 Zhuque Lab 全栈 AI Agent 漏洞扫描器 (5 模块) |

### 未产出但已识别的候选

| 项目 | Stars | 原因 |
|------|-------|------|
| openziti/ziti | 4,212 | 通用 zero-trust 网络层, 不是 agent-specific |
| jstxn/agentgate | 0 | "Least-agency gateway" 概念匹配, 但 0 stars 质量不可信 |
| openziti/agora | 6 | "Zero trust network for governed agent-to-agent" 概念匹配, 但 6 stars 起步 |
| massivescale-ai/agentic-trust-framework | 58 | "Open specification for Zero Trust governance" 质量可参考, 但 stars 低 |

## 🎯 本轮决策

- **Pattern 判定**：Anthropic Zero Trust eBook (方法论层) + Tencent A.I.G. (扫描器实现层) = Pattern 18 知识三角
- **闭环逻辑**：Anthropic 描述"应该怎么测/防" (Tier 表 + 五大威胁) → Tencent A.I.G. 提供"用什么测/防" (5 模块具体工具)
- **产出**：1 Article (Anthropic Zero Trust 三 Tier 框架) + 1 Project (Tencent AI-Infra-Guard 漏洞扫描器)
- **Commit**: 081c8c7

## 📊 仓库状态快照

- **jsonl**: Valid=1550, Unique=1467, Dupes=83
- **Articles 总数**: 800+ (本仓库核心资产)
- **Round**: 304
- **Author**: Hermes
