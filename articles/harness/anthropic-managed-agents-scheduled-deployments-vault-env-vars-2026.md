---
title: "Anthropic Managed Agents 调度部署 + Vault 环境变量 2026"
slug: anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026
date: 2026-06-11
cluster: ai-agent-credential-brokering
tags: [anthropic, claude-managed-agents, scheduled-deployments, vault, environment-variables, credentials, mcp, cron]
source: https://claude.com/blog/whats-new-in-claude-managed-agents
source_date: 2026-06-09
authors: [Hermes]
---

# Anthropic Managed Agents 调度部署 + Vault 环境变量 2026

> **核心断言**：Anthropic 在 2026-06-09 的 Claude Managed Agents 更新中，将 agent 平台从"按需运行"扩展为"调度运行 + 凭据边界即服务"。两个新机制——**Scheduled Deployments** 和 **Environment Variables in Vaults**——补齐了 Anthropic 在 R322 / R331 已经讨论过的"凭据 vault + Brain/Hands 解耦"图景，把 agent 从"长会话 + 手动触发"演进到"定时执行 + 凭据永远不外泄给模型"。

## 一、为什么这两个机制重要

Anthropic 在 R322（`anthropic-managed-agents-security-boundary-credential-vault-2026`）中已经确立了"凭据 vault 隔离 + 网络边界注入"的核心原则；在 R331（`claude-managed-agents-vault-cluster-discovery`）中我们识别出"AI Agent Credential Brokering"这一 cluster 0→1 启动信号。

2026-06-09 的更新把这一图景向前推了两步：

1. **时间维度**：从"用户主动触发 → 一次性 session"扩展到"cron 调度 → 多 session 自动执行"
2. **凭据维度**：从"完整 secret 注入到 sandbox"演进到"占位符 + 网络边界处真实 secret 注入 + 域名白名单"

这两步看似独立，但本质是同一命题：**agent 越自动化，凭据越需要"被代理"而非"被交接"**。当 session 24/7 自动启动时，模型在任何时刻都不应能看到 key；当 CLIs 集成时，key 不应在 sandbox 文件系统里落地。

## 二、Scheduled Deployments：让 agent 像 cron job 一样被调度

### 2.1 机制定义

Anthropic 的 Scheduled Deployments 给一个 agent deployment 绑定一个 cron schedule。每次 schedule 触发时，agent 启动**全新的 session**完成任务，用户无需自建 scheduler：

> *"A scheduled deployment gives an agent a cron schedule. Each time the schedule fires, the agent starts a new session and completes its task, with no scheduler for you to build or host."*

### 2.2 设计意图：解耦"任务定义"与"执行时机"

传统 serverless 平台（AWS Lambda、Vercel Cron）的痛点是"agent 有状态、cron 无状态"——agent 需要长期记忆、工具栈、sandbox，但 cron 只是触发器。Anthropic 的设计把两者解耦：

- **Deployment** 持有 agent 配置（prompt、工具、sandbox 模板、vault 引用）
- **Schedule** 只是一个"启动信号"——它告诉平台"现在开始一次新的 session"
- **Session** 是一次完整的 agent run，结束时销毁，但 deployment 持久存在

这与我们在 R326（`anthropic-harness-engineering-lifecycle-sessions-2026`）讨论的"session as unit of execution"一脉相承——现在 session 不仅可以手动触发，还能被 cron 调度。

### 2.3 三个工程含义

**(a) 平台承担了原本的"自己跑 cron + 唤醒 service"基础设施负担**

Rakuten 的 PM 团队用 scheduled deployments 把 production logs 转化成"无需建 dashboard 的健康摘要"——他们不再需要"自己写的 scheduler + 单独跑的脚本 + 通知链路"。Anthropic 把这条链路做成了平台原语。

**(b) "Fewer agents" 设计哲学得到强化**

Anthropic 在客户引言中明确：*"Most of our users prefer to work with fewer agents rather than many. With scheduled deployments, they can bundle more capabilities into one autonomous agent."* 这与 R334（Harness 全框架整合）、R335（LangChain Harness 13.7 分跃升）的"少而精"方向一致——调度能力让单 agent 承担更多工作。

**(c) "Pause / Resume / Archive / On-demand trigger" 控制面**

部署上线后，用户可以随时暂停、恢复、归档，或在 schedule 之外触发额外 run。这把 cron 从"fire-and-forget"升级为"可控的工作项"，对周期性合规扫描、夜间数据同步等场景尤其重要。

## 三、Environment Variables in Vaults：凭据永远不外泄给模型

### 3.1 机制定义

Anthropic 扩展了原本只支持"完整 secret 注入到 sandbox"的 vault，新增 environment variables 类型：

> *"Now we're extending vaults to support environment variables, so CLIs and other tools can make authenticated requests. Register an API key with an environment variable name and the domains it can reach, and the CLIs installed in an agent's sandbox can use it to make authenticated API calls."*

### 3.2 关键差异：从"secret 注入 sandbox"到"placeholder + 边界注入"

这是凭据管理范式的转移：

| 旧模式（R322） | 新模式（R337，本轮） |
|---------------|---------------------|
| 真实 key 注入 sandbox，模型可见 | Sandbox 只有**占位符**（placeholder） |
| Agent 可读取并使用 key 做事 | 真实 key 在**网络边界**处附加，sandbox 内不可见 |
| 一旦 key 泄露，需要轮换 sandbox | 任何时刻 agent 看到的都是 placeholder |

引用原文：

> *"The agent never sees your key because the sandbox only holds a placeholder. The real key is attached at the network boundary, and only on requests to domains you allow, so it only goes where you've approved."*

### 3.3 三个工程含义

**(a) 域名白名单从"网络层"下沉到"凭据层"**

传统 vault 的 ACL 是"这个 secret 可以被哪些 service 调用"。Anthropic 的设计把 ACL 细化到"这个 secret 可以被哪些 domain 的 HTTP 请求使用"——更细粒度，更难滥用。即使 agent 误调用了一个未授权域名，key 也不会被附加。

**(b) CLI 集成路径变得安全**

CLI 是 agent 集成外部系统的"轻量捷径"，但传统 CLI 需要从环境变量或配置文件读 key——一旦 agent 拥有 shell 访问权，理论上 `echo $API_KEY` 就能泄露。Anthropic 的"网络边界处附加"模式让 CLI 在 sandbox 内执行，但 key 在请求离开 sandbox 时才被注入；sandbox 内永远只有占位符。

Browserbase、KERNEL、Notion、Ramp、Sentry 等 CLI 都被点名支持。

**(c) 凭据轮换从"sandbox 重启"降级为"vault 同步"**

> *"To change a key, update it in the vault, and running sessions will pick up the new value on their next call."*

这意味着轮换 key **不需要重启 agent 或 sandbox**——vault 是唯一真相源，所有运行中的 session 在下次调用时自动获取新值。这对长跑 agent（scheduled deployments 场景下特别重要）是一个关键运维改进。

## 四、两个机制合起来："24/7 自主 agent"的真正安全姿态

Scheduled Deployments + Env Vars in Vaults 不是两个独立功能，而是同一个产品愿景的两面：

```
┌──────────────────────────────────────────────────────────┐
│                Scheduled Deployment (cron)                │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Agent Session (24/7 auto-started)               │    │
│  │                                                   │    │
│  │  ┌──────────────┐         ┌──────────────────┐  │    │
│  │  │  Sandbox     │ ──HTTP──│ Network Boundary │  │    │
│  │  │  + CLI       │         │ (key injection)  │  │    │
│  │  │  placeholder │         │                  │  │    │
│  │  │  only        │         │ → allowed domains│  │    │
│  │  └──────────────┘         └──────────────────┘  │    │
│  │       ▲                          │               │    │
│  │       │                          ▼               │    │
│  │       │                   ┌──────────────┐       │    │
│  │       │                   │ Vault        │       │    │
│  │       └─────── next call ─│ env var      │       │    │
│  │                           │ + real key   │       │    │
│  │                           └──────────────┘       │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

**当这两个机制同时启用**：
- 调度让 agent 24/7 自动执行（不再需要人工触发）
- 凭据边界让 agent 永远不接触真实 key（即使 24/7 也在跑）
- 域名白名单让 agent 只能访问被授权的 API（即使 key 暴露给攻击面）
- vault 同步让运维不必为每次轮换重启（即使出问题也能热修）

这是 Anthropic 在 2026 年中给出的"长跑 agent 安全姿态"完整答案——比 R322 的"凭据 vault 隔离"更进一层，比 R331 的"vault gateway 模式"更可操作。

## 五、与既有 R322 / R331 的关系：演进图景

| 轮次 | 主题 | 视角 |
|------|------|------|
| R322 | 凭据 vault + Brain/Hands 解耦 | 机制设计层（防御侧） |
| R331 | Vault 集群 0→1 启动信号 | 实践层（开源实现涌现） |
| **R337（本轮）** | **调度部署 + Vault 环境变量扩展** | **平台产品层（自动化场景落地）** |

R337 不重复 R322 的"vault 解耦架构"叙事，也不重复 R331 的"开源 vault 涌现"叙事，而是聚焦"**当 agent 必须 24/7 跑 + 必须用 CLI 集成时，凭据如何永远不外泄**"——这是产品演进视角的差异化。

## 六、对工程团队的启示

1. **评估"少而精 + 调度"是否替代"多而专 + 手动"**：如果你的工作流是"每晚同步数据"或"每周合规扫描"，单 agent + scheduled deployment 可能比 N 个专用 agent 更省运维成本。
2. **CLI 集成优先于直接 API**：当外部系统提供 CLI 时，优先用 CLI 路径——env var in vault 让 CLI 在 sandbox 内安全运行，绕开"agent 必须持有 key"的传统模式。
3. **凭据轮换策略升级**：因为 vault 同步不需要重启，团队可以实施更激进的轮换策略（比如每周轮换）而不增加运维负担。
4. **域名白名单视为代码**：env var 的 allowed_domains 字段应纳入 IaC，避免"运行时随便加"导致安全态势漂移。

## 七、源与引用

- 一手源：[New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults](https://claude.com/blog/whats-new-in-claude-managed-agents)（Anthropic Claude Blog，2026-06-09）
- 关联 R322：`anthropic-managed-agents-security-boundary-credential-vault-2026`
- 关联 R331：`claude-managed-agents-vault-cluster-discovery`
- 关联 R335：`langchain-harness-engineering-13-7-score-jump`（少而精方向）
- 客户引用：Rakuten（scheduled deployments 替代自建 scheduler）、Browserbase（CLI 集成 + scheduled 验证 catalog）、KERNEL（数据库连接 + 用量激增实时检测）

## 八、本文限制

- 文章基于 Anthropic 官方博客的对外公告，未深入 Claude Console 内部部署细节
- "域名白名单"的具体实现（DNS 层 vs HTTP 拦截层）未在公开文档中披露
- Scheduled deployments 的 SLA / 失败重试策略 / 跨 region 行为未在博客中详述，需进一步文档验证
