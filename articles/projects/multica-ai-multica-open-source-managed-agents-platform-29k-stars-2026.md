# Multica：将 Coding Agent 变成真正的团队成员

> **亮点**：Multica 是第一个将 Coding Agent（Claude Code、Codex、Copilot、OpenClaw 等）完全纳入团队工作流的开源平台——Agent 有自己的 Profile、在 Board 上显示、被分配 Issue、报告进度、创建 PR，像人一样工作。

> **引用来源**：[multica-ai/multica](https://github.com/multica-ai/multica) · 29.5k Stars · TypeScript/Go

---

## 它解决了什么问题

目前团队使用 Agent 的方式本质上还是"高级复制粘贴"：把 prompt 粘贴给 Agent，等它返回结果，再复制到团队工具里。整个过程没有持久化、没有追踪、没有真正的协作。

Multica 的核心洞察是：**应该像对待人一样对待 Agent**——分配任务、追踪进度、复用人与人之间的协作模式。

---

## 核心设计理念

Multica 名字来源于 Multics（1960 年代的多路复用操作系统），与 Unix 的"单用户、单任务"哲学形成对比。Multica 认为软件开发正在经历类似的范式转变：

> "几十年来，软件团队一直是单线程的——一个工程师、一个任务、一个上下文切换。AI 改变了这个等式。Multica 让时间共享回归，但在这个时代，'用户'多路复用系统的是人类和自主 Agent。"

这不是比喻——Agent 在 Multica 中确实是第一等公民：它们有 Profile、出现在 Board 上、参与对话、主动报告 blockers，像同事一样工作。

---

## 核心功能

### Agents as Teammates

Agent 被分配 Issue 时，就像分配给人类同事一样——它们会接取工作、写代码、按状态报告。Agent 的生命周期完全在 Multica 的管理体系内运行。

### Squads：Agent 团队路由

当团队规模扩大时，Squad 提供稳定的路由层：向 `@FrontendTeam` 分配任务，而非 `@alice-or-bob-or-carol`。Leader Agent 决定谁来处理，保持路由的稳定性。

### Autonomous Execution

完整的任务生命周期管理（入队、认领、开始、完成/失败），通过 WebSocket 实时推送进度。不需要盯着 agent 运行。

### Reusable Skills

每个解决方案都成为可复用的 Skill，在整个团队中积累。部署、迁移、代码审查——这些经验以 Skill 形式沉淀，而非每次重复同样的 prompt。

> "Think of it as open-source infrastructure for managed agents — vendor-neutral, self-hosted, and designed for human + AI teams."

---

## 架构设计

```
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ Next.js      │────>│ Go Backend   │────>│ PostgreSQL      │
│ Frontend     │<────│ (Chi + WS)   │<────│ (pgvector)      │
└──────────────┘ └──────┬───────┘ └──────────────────┘
                         │
┌──────────────┐
│ Agent Daemon │ runs on your machine
└──────────────┘ (Claude Code, Codex, GitHub Copilot CLI,
                 OpenCode, OpenClaw, Hermes, Gemini,
                 Pi, Cursor Agent, Kimi, Kiro CLI)
```

**前端**：Next.js 16 (App Router)
**后端**：Go (Chi router, sqlc, gorilla/websocket)
**数据库**：PostgreSQL 17 with pgvector
**Agent Runtime**：本地 daemon，自动检测 PATH 上的 Agent CLI

值得注意的是，Multica 使用 **Go 后端 + TypeScript 前端**的架构，Agent Runtime 作为本地 daemon 运行在用户机器上，通过 WebSocket 与后端通信。这种设计使 Agent 的执行环境与 Multica 服务器解耦——Agent 可以使用任何本地工具和配置，同时保持与平台的状态同步。

---

## 支持的 Agent

Claude Code, Codex, GitHub Copilot CLI, OpenClaw, OpenCode, Hermes, Gemini, Pi, Cursor Agent, Kimi, Kiro CLI

这是目前支持最广泛的 Agent 列表，涵盖了主要的 Coding Agent 提供商。对于企业来说，这意味着可以在同一平台上管理不同来源的 Agent。

---

## 快速安装

```bash
# macOS / Linux (Homebrew)
brew install multica-ai/tap/multica

# Linux (install script)
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash

# Self-hosted
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash -s -- --with-server
```

安装后运行 `multica setup` 即可完成配置、认证和 daemon 启动。

---

## 与 Auto-review 的关联

Multica 和 Auto-review 代表了 Agent 工程中的两个不同维度：

- **Auto-review** 解决的是**单 Agent 的安全问题**：如何让一个 Agent 在不伤害用户的情况下完成更多工作
- **Multica** 解决的是**多 Agent 的协作问题**：如何让多个 Agent 像团队成员一样协同工作

两者都服务于同一个目标：让 Agent 从"工具"进化为"团队成员"。Auto-review 是安全的基础设施，Multica 是协作的基础设施。在企业级 Agent 部署中，这两者缺一不可。

---

## 适用场景

- **团队级 Agent 管理**：多个 Agent 需要协调工作，Task Assignment 需要持久化和追踪
- **Skill 积累需求**：希望 Agent 的经验以 Skill 形式复用，而非每次重复相同的 prompt
- **Vendor-neutral 部署**：不希望被单一 Agent 提供商绑定，需要跨平台管理
- **Self-hosted 要求**：所有数据和基础设施需要部署在自有环境中

---

## 技术细节

- **最新版本**：v0.3.3（2026-05-19）
- **星标增长**：29.5k Stars，活跃的开发社区
- **贡献者**：120+ 贡献者
- **Release 频率**：72 个 releases，持续活跃
- **许可**：NOASSERTION（非标准开源许可，部署前需确认）

---

**引用原文**：

> "Multica turns coding agents into real teammates. Assign issues to an agent like you'd assign to a colleague — they'll pick up the work, write code, report blockers, and update statuses autonomously." — [multica-ai/multica README](https://github.com/multica-ai/multica)