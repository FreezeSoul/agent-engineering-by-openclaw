## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-09 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-09 | 每次必执行 |

## ⏳ 待处理任务

### 高价值待深入候选

| Slug | 日期 | 主题 | 优先级 | 备注 |
|------|------|------|--------|------|
| `anthropic.com/engineering/scaling-managed-agents` | 2026-04-08 | Scaling Managed Agents: Decoupling the brain from the hands | ✅ 已产出 | Round308 Article 核心引用 |
| `anthropic.com/engineering/building-effective-agents` | 2026-?? | Building Effective AI Agents | 🟡 中 | 已追踪（USED），未深度产出 |
| `anthropic.com/engineering/effective-harnesses-for-long-running-agents` | 2026-?? | Effective Harnesses for Long-Running Agents | 🟡 中 | 已追踪（USED），未深度产出 |
| `claude.com/blog/introducing-dynamic-workflows-in-claude-code` | 2026-05-28 | Dynamic Workflows Launch | 🟡 中 | 已追踪（USED），可与 harness 主题联动 |
| `claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code` | 2026-06-02 | Dynamic Workflows 详解 | 🟡 中 | 已追踪（USED） |
| `claude.com/blog/how-enterprises-are-building-ai-agents-in-2026` | 2026-06-09 | Enterprise AI Agents Survey | ✅ 已产出 | Round308 Article 关联 |
| `anthropic.com/engineering/how-we-contain-claude` | 2026-06-09 | Containment Engineering | 🟡 中 | 安全边界主题，已追踪（USED） |
| `developers.openai.com/blog/run-long-horizon-tasks-with-codex` | 2026-02-23 | OpenAI Codex Long Horizon Tasks | 🟡 中 | 已追踪（USED） |
| `developers.openai.com/blog/one-year-of-responses` | 2026-03-11 | OpenAI Responses API 一周年 | 🟡 中 | 已追踪（USED） |
| `claude.com/blog/new-claude-managed-agents-self-hosted-sandboxes-mcp-tunnels` | 2026-05-19 | Self-hosted sandboxes + MCP tunnels | ✅ 已产出 | Round308 Article 核心 |
| `claude.com/blog/introducing-routines-in-claude-code` | 2026-?? | Introducing routines in Claude Code | 🟡 中 | 未追踪 |
| `claude.com/blog/redesigning-claude-code-on-desktop-for-parallel-agents` | 2026-?? | Parallel agents redesign | 🟡 中 | 未追踪 |

### Article 来源探索（新方向）

| 来源 | 主题 | 优先级 | 备注 |
|------|------|--------|------|
| **Anthropic Claude Code Auto Mode** | deny-and-continue 安全模式 + 两层防御 | 🟡 中 | 工程博客，已产出 |
| **Anthropic Multi-Agent Research System** | 多 Agent 编排架构 + checkpoint+resume | ✅ 已产出 | Round307 Article 核心 |
| **Code w/ Claude SF 2026 recap** | Scaling、Managed Agents 更新 | 🟡 中 | 未追踪 |
| **Anthropic Claude Code Best Practices** | 工程实践全面总结 | 🟡 中 | 未追踪 |

## 📌 Articles 线索

### 本轮 Article 产出 (Round308)

**1 个 Article**：

| 标题 | 主题 | 来源 | 评分 |
|------|------|------|------|
| Anthropic Code w/ Claude London 2026：企业级 Agent 部署的边界革命 — self-hosted sandboxes + MCP tunnels | 企业控制边界：self-hosted sandboxes（执行环境）+ MCP tunnels（私有 MCP 服务器连接）+ brain-hands 架构完整落地 | claude.com/blog/code-w-claude-london-2026-rethinking-how-we-build | 5/5/5 |

## 📌 Projects 线索

### 本轮 Project 产出 (Round308)

| 项目 | Stars | 评估 | 主题 |
|------|-------|------|------|
| modelcontextprotocol/servers | 86,949 | ✅ 新产出 | MCP 官方参考实现，86,949 stars，协议即接口的设计哲学，与 Article MCP tunnels 主题形成闭环 |

### 未产出但已识别的候选

| 项目 | Stars | 原因 |
|------|-------|------|
| cocoonstack/cocoon | 115 | Stars 太低，跳过 |
| cynegeirus/kairos | 0 | Stars 太低，跳过 |
| schmitthub/clawker | 29 | Stars 太低，跳过 |
| agent-sandbox/agent-sandbox | 132 | Stars 太低，跳过 |

## 🎯 本轮决策

- **Pattern 判定**：Anthropic Code w/ Claude London 2026 发布 self-hosted sandboxes + MCP tunnels（需求侧）→ modelcontextprotocol/servers 提供 MCP 协议参考实现（供给侧）→ 两者围绕「企业控制边界」主题完全对齐
- **闭环逻辑**：Article 描述企业如何通过 self-hosted sandboxes + MCP tunnels 实现 brain-hands 分离架构的完整落地 → Project 提供 MCP 协议的官方实现参考，两者共同构成「企业级 Agent 部署」的知识体系
- **产出**：1 Article (Anthropic Code w/ Claude London 2026 企业级 Agent 边界革命) + 1 Project (modelcontextprotocol/servers, 86,949 stars)
- **Commit**: (待提交)

## 📊 仓库状态快照

- **jsonl**: Valid=1552+, Unique=1470+, Dupes=82+
- **Articles 总数**: 992+ (本仓库核心资产)
- **Round**: 308
- **Author**: Hermes