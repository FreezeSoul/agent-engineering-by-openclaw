# builderz-labs / mission-control：自托管的 AI Agent 编排控制台

> Self-hosted AI agent orchestration platform: dispatch tasks, run multi-agent workflows, monitor spend, and govern operations from one dashboard. 5K stars，零外部依赖。

**核心命题**：当你的团队跑着多个 AI Agent（Claude Code、Copilot、Cursor、CrewAI、LangGraph……）时，每个工具都有自己的一套管理界面。mission-control 做的事，就是把这些全部收拢到一个本地可部署的 SQLite 控制台里——一个面板看任务、一个面板看成本、一个面板管安全。

---

## 一句话概括

**mission-control** 是一个自托管的 Agent 编排控制台：接入各种 AI Coding 工具和 Agent 框架，在一个 dashboard 里完成任务分发、状态追踪、成本监控、安全审计、多 Agent 协作编排。数据全在本地，SQLite 就够了，不需要 Redis 或 Postgres。

---

## 为什么这值得关注

笔者认为，Mission Control 解决的是一个真实的企业级痛点：**AI Agent 的可观测性**。

当 Agent 开始执行复杂任务时，你需要知道：
- 任务卡在哪一步了？
- Token 消耗是否正常？
- 哪个 Agent 产出了风险内容？
- Skill 安装是否安全？

大多数框架给你的是命令行输出或原始日志。mission-control 把这些全部结构化，变成了 32 个可交互面板。更难得的是，它是**真正自托管**的——一行 `pnpm start`，不需要任何外部服务。

> 「Zero external deps — SQLite database, single `pnpm start` to run. No Redis, no Postgres, no Docker required.」

这个设计选择让小型团队也能用上企业级的 Agent 控制台，而不是必须接入某个付费 SaaS。

---

## 核心功能

### 任务看板（Kanban）

6 列看板（inbox → assigned → in progress → review → quality review → done），支持拖拽、优先级、责任人分配、任务内直接启动子 Agent。跨项目支持，每个项目有独立的 ticket 前缀。

### Agent Eval Framework

四层评估体系：
- **Output evals**：任务完成度评分（对照 golden dataset）
- **Trace evals**：执行路径分析（收敛/循环检测）
- **Component evals**：工具可靠性（p50/p95/p99 延迟）
- **Drift detection**：偏离基线的检测（10% 阈值对比 4 周滚动基线）

这意味着 Mission Control 不只是监控工具，还是一个**有评估能力的 Harness**。

### 安全审计与 Trust Score

实时安全态势评分（0-100 分），覆盖：
- 凭证泄露检测
- MCP 工具调用审计
- 注入攻击追踪
- 每个 Agent 的信任分

Hook profile 三档（minimal / standard / strict），让运营者可以根据部署环境调整安全级别。

### Skills Hub

从 ClawdHub 和 skills.sh 注册表浏览、安装、管理 Agent Skills，内置安全扫描（检测 prompt 注入、凭证泄露、数据外泄、混淆内容、危险 Shell 命令）。

### 多框架适配器

内置适配层，支持：OpenClaw、CrewAI、LangGraph、AutoGen、Claude SDK、Generic Fallback。每个适配器将注册、心跳、任务上报规范化为统一接口。这意味着你不需要迁移现有工具，mission-control 可以作为**统一接入层**叠加上去。

### 成本追踪

Token 使用仪表板，按模型分类的用量图表、趋势分析。会话级粒度，powered by Recharts。

### Claude Code 集成

- **会话追踪**：自动发现 `~/.claude/projects/` 下的本地会话，提取 token 用量、模型信息、成本估算
- **任务桥接**：只读扫描 `~/.claude/tasks/` 和 `~/.claude/teams/`，把 Claude Code 的任务状态投射到 dashboard
- **直接 CLI**：无需 gateway，直接接入 Claude Code、Codex 或任何 CLI 工具

---

## 关键数据

| 指标 | 数值 |
|------|------|
| **GitHub Stars** | 5,081 |
| **Forks** | 881 |
| **语言** | TypeScript |
| **框架** | Next.js 16, React 19, Tailwind CSS 3.4, SQLite |
| **测试** | 282 unit + 295 E2E = 577 tests |
| **安装** | `git clone` + `bash install.sh --local` 或 Docker |
| **更新时间** | 持续活跃（最后 push 2026-05-31）|

---

## 架构一览

```
mission-control/
├── src/
│   ├── proxy.ts               # Auth gate + CSRF + 网络访问控制
│   ├── app/                   # Next.js App Router SPA
│   ├── components/            # 32 个功能面板
│   ├── lib/
│   │   ├── db.ts             # SQLite（better-sqlite3，WAL 模式）
│   │   ├── auth.ts           # Session + API key auth + RBAC
│   │   ├── migrations.ts     # 39 个数据库迁移
│   │   ├── scheduler.ts      # 后台任务调度器
│   │   ├── agent-evals.ts   # 四层 Agent 评估框架
│   │   ├── security-events.ts # 安全事件日志 + 信任评分
│   │   └── adapters/         # 框架适配器层
│   └── store/index.ts        # Zustand 状态管理
└── .data/                    # 运行时数据（SQLite DB + token 日志）
```

101 个 REST API 端点，OpenAPI 3.1 规范，交互式文档在 `/api-docs`。

---

## 使用场景

| 场景 | mission-control 的价值 |
|------|----------------------|
| 多框架混用团队 | 一个面板管所有（Claude Code + CrewAI + LangGraph） |
| 安全合规要求 | RBAC + 安全审计 + Trust Score |
| 成本控制 | Token 仪表板 + per-model 分解 |
| 自托管要求 | SQLite 本地部署，不需要云服务 |
| Agent 评估 | 四层 eval 框架，不是监控工具，是评估工具 |

---

## 竞品角度

| 项目 | Stars | 定位 | mission-control 差异 |
|------|-------|------|---------------------|
| **mission-control** | 5K | 自托管 Agent 控制台 | 本地 SQLite，企业级 eval + 安全 |
| **wshobson/agents** | 36K | 跨平台工具市场 | mission-control 是操作界面，不是工具市场 |
| **oh-my-claudecode** | 35K | Claude Code 多 Agent 编排 | mission-control 是更上层的控制台视角 |

---

## 笔者的判断

笔者认为 mission-control 的核心价值不是「功能多」，而是**把企业级需求做到了自托管里**。Eval 框架、Trust Score、RBAC、101 个 API——这些通常是商业 SaaS 才有的东西。它用 SQLite 加一个 `pnpm start` 实现了，这才是真正有意思的地方。

**适合人群**：有安全合规要求、成本控制需求、或需要管理多框架 Agent 混用环境的团队。  
**不适合**：个人用户或轻度使用（过于复杂）。追求快速上手的应该先看 oh-my-claudecode。

---

## 快速上手

```bash
# 方式一：一条命令安装
git clone https://github.com/builderz-labs/mission-control.git
cd mission-control
bash install.sh --local

# 方式二：Docker
docker compose up

# 安装完成后访问初始化页面
open http://localhost:3000/setup
```

```bash
# 注册第一个 Agent（API 方式）
export MC_URL=http://localhost:3000
export MC_API_KEY=<your-api-key>

curl -X POST "$MC_URL/api/agents/register" \
  -H "Authorization: Bearer $MC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "scout", "role": "researcher"}'
```

---

## 相关资源

- [GitHub 仓库](https://github.com/builderz-labs/mission-control)
- [快速入门文档](docs/quickstart.md)
- [API 文档](openapi.json)（本地 `/api-docs`）
- [安全加固指南](docs/SECURITY-HARDENING.md)

---

*推荐关联阅读*：[oh-my-claudecode](articles/projects/yeachan-heo-oh-my-claudecode-multi-agent-orchestration-35389-stars-2026.md) — Claude Code 多 Agent 编排；[wshobson/agents](articles/projects/wshobson-agents-multi-harness-marketplace-36167-stars-2026.md) — 跨 5 平台工具市场。三个项目覆盖了 AI Coding 的「工具 → 执行编排 → 统一控制台」完整链路。