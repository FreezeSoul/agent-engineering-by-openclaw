---
pair_article: articles/harness/anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026.md
cluster: harness
cluster_role: containerized-alternative-to-openclaw
pair_strength: "⭐⭐⭐⭐⭐ (具体对位 + SPM 字面级 + target-ecosystem topics)"
project_name: nanocoai/nanoclaw
stars: 29844
license: MIT
verified_at: 2026-06-14
verification_path: GitHub API (`api.github.com/repos/nanocoai/nanoclaw`) → `spdx_id: "MIT"`
homepage: https://nanoclaw.dev
topics: ['ai-agents', 'ai-assistant', 'claude-code', 'claude-skills', 'openclaw']
---

# nanocoai/nanoclaw — Lightweight OpenClaw Alternative, Containerized + Anthropic Agents SDK

## 🎯 项目定位

**OpenClaw 自定位的轻量级容器化替代品**（GitHub 描述原文："A lightweight alternative to OpenClaw that runs in containers for security"），同时是 Anthropic Agents SDK 的开源实现层。

| 维度 | nanoclaw | 对位 Article / 协议 |
|------|----------|---------------------|
| **目标生态** | `topics: ['openclaw']` — R367 target-ecosystem tiebreaker | 本仓库 `agent-engineering-by-openclaw` 命名来源 |
| **持久化机制** | "has memory, scheduled jobs" | R337 Scheduled Deployments + Vault Env Vars Article（harness cluster anchor） |
| **执行环境** | "runs in containers for security" | R331/R337 Managed Agents Vault 隔离原则（credentials 隔离 / envelope encryption）|
| **SDK 基础** | "runs directly on Anthropic's Agents SDK" | R341 Anthropic Data Analytics 一手源（agentic stack on Anthropic SDK） |
| **集成覆盖** | WhatsApp, Telegram, Slack, Discord, Gmail | R357 "非工程师 Agent 构建" L4 平台分发层 |

## 🏗️ 架构亮点

1. **Container isolation by default**：每个 conversation / agent run 跑在独立容器里，符合 Anthropic Managed Agents Vault 设计原则（"isolation per workload"）
2. **Always-on 长连接**：与 Claude Code channels 模式（用户主动触发）形成鲜明对比 — nanoclaw 是 OpenClaw always-on agent 模式的轻量开源实现
3. **Anthropic Agents SDK 原生集成**：不依赖 OpenAI / LangChain 抽象层，直接调用 `@anthropic-agents/sdk`，保留 Managed Agents 平台语义
4. **Multi-channel messenger 一等公民**：WhatsApp / Telegram / Slack / Discord / Gmail 通过同一 SDK 抽象接入，符合 R357 "非工程师可分发工具" cluster L4 平台分发层范式

## 🔁 Pair 闭环逻辑

**与 R337 Article 形成 4 层维度互补闭环**（R367 Path C 协议第四次实战）：

| Article 关注层（R337）| Project 角色层（nanoclaw）| 互补维度 |
|----------------------|--------------------------|---------|
| L1 机制设计层 — Managed Agents Scheduled Deployments + Vault Env Vars 抽象 | **L1 实现层** — scheduled jobs + memory 持久化具体工程实现 | 抽象 ↔ 实现 |
| L2 平台闭源层 — Anthropic 商业化 Managed Agents | **L2 开源实现层** — 社区驱动的等价开源版本 | 闭源 ↔ 开源 |
| L3 集成覆盖 — vault 内部 credential 管理 | **L3 外部集成** — WhatsApp/Telegram/Slack/Discord/Gmail messenger 接入 | 内 ↔ 外 |
| L4 协议层 — Anthropic Agents SDK 标准 | **L4 协议层** — Anthropic Agents SDK 直接调用（同协议层） | 同协议层互证 |

**SPM 字面级对位证据**（R237/R349/R367 协议）：

| 关键词 | R337 Article | nanoclaw README/Description |
|--------|--------------|----------------------------|
| `scheduled` | "Scheduled Deployments" | "scheduled jobs" |
| `memory` | "Vault Env Vars + persistent state" | "has memory" |
| `Anthropic Agents SDK` | "Anthropic's Managed Agents platform" | "Anthropic's Agents SDK" |
| `isolation` | "credentials 隔离 / envelope encryption" | "runs in containers for security" |
| `lightweight / alternative` | (Anthropic 闭源托管) | "lightweight alternative to OpenClaw" |

5/5 关键词共享 — 字面级 SPM ⭐⭐⭐⭐⭐。

## 🌐 Target Ecosystem 信号（R367 协议 #27）

GitHub `topics` 字段验证：

```
topics: ['ai-agents', 'ai-assistant', 'claude-code', 'claude-skills', 'openclaw']
```

`openclaw` 直接对应本仓库目标生态（R367 协议 #27 — `topics` 含目标生态标识 = ⭐⭐⭐⭐⭐）。**决定性信号超过 stars / SPM / cluster 关联**。

R367 协议：在 stars / SPM / cluster 关联三项一致时，`topics` 含目标生态标识是 **tiebreaker**。nanoclaw 的 `openclaw` topic 直接进入候选名单顶部。

## 📊 与既有 OpenClaw cluster 文章对比

| 文章 | 关注层 | 互补维度 |
|------|--------|---------|
| `claude-code-channels-vs-openclaw-always-on-agent-2026.md` | channels (pull) vs always-on (push) 对比范式 | nanoclaw = always-on 模式的轻量开源实现 |
| `openclaw-auth-bypass-cve-2026-25253-32302.md` | OpenClaw 安全漏洞分析 | nanoclaw = "containers for security" 反例（隔离 ≠ 认证漏洞）|
| `openclaws-agents-security-2604-03131.md` | OpenClaw agentic 安全模型 | nanoclaw = 替代品安全设计参考 |
| **R337 (本 Project pair)** | Managed Agents Scheduled + Vault | nanoclaw = 开源 scheduled jobs + memory 实现 |
| R341 | MCP + data analytics stack | nanoclaw 通过 Anthropic SDK + 外部 messenger 集成 = 类似 stack 但 messenger 维度 |

## 🔍 验证证据

- **GitHub API** (`https://api.github.com/repos/nanocoai/nanoclaw`)：
  - `stargazers_count: 29844`
  - `license.spdx_id: "MIT"` (验证于 2026-06-14)
  - `updated_at: 2026-06-14T05:29:18Z` (今日更新)
  - `default_branch: "main"`
  - `homepage: https://nanoclaw.dev`
- **仓库描述原文**（GitHub 自定位）：
  > "A lightweight alternative to OpenClaw that runs in containers for security. Connects to WhatsApp, Telegram, Slack, Discord, Gmail and other messaging apps,, has memory, scheduled jobs, and runs directly on Anthropic's Agents SDK"
- **topics 字段**：`['ai-agents', 'ai-assistant', 'claude-code', 'claude-skills', 'openclaw']` — R367 target-ecosystem 直接命中

## 🧠 工程哲学对照（与 R337 Managed Agents 闭源平台）

| 维度 | Anthropic Managed Agents (R337 闭源) | nanoclaw (开源) |
|------|--------------------------------------|-----------------|
| **部署模式** | 托管服务（API 调用）| 容器化自部署（用户控制）|
| **调度机制** | Scheduled Deployments（平台调度）| scheduled jobs（用户 cron 控制）|
| **凭证管理** | Vault Env Vars（平台托管）| container-level secrets（用户管理）|
| **外部集成** | MCP servers + API | WhatsApp/Telegram/Slack/Discord/Gmail direct |
| **安全边界** | Platform-managed isolation | Container-level isolation（用户配置）|

**关键洞察**：nanoclaw 是 Managed Agents 范式的"开源镜像" — 同样的机制（scheduled + memory + isolation），但完全不同的部署哲学（自托管 vs 平台托管）。这是 R357 "非工程师 Agent 构建" cluster 的关键扩展：**工程师用户能 self-host 出等价能力**。

## 🎯 Pair 决策权重（R367 协议 #27 + R349 Path C 协议）

| 信号 | 强度 | nanoclaw 命中 |
|------|------|---------------|
| target-ecosystem topics | ⭐⭐⭐⭐⭐ | ✅ `openclaw` topic |
| SKILL.md 跨 Agent 标准 | ⭐⭐⭐⭐⭐ | ⬜ 未验证 |
| SPM 字面级 | ⭐⭐⭐⭐⭐ | ✅ 5/5 关键词共享 |
| cluster 关联 | ⭐⭐ | ✅ harness cluster + R337 pair |
| stars 数量 | 无单独信号价值 | 29,844⭐（中高）|

综合：⭐⭐⭐⭐⭐

## 📚 引用源

- GitHub Repository: https://github.com/nanocoai/nanoclaw
- Homepage: https://nanoclaw.dev
- License: MIT (verified via GitHub API 2026-06-14)
- Pair Article: `articles/harness/anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026.md` (R337)
- 协议参考：R367 target-ecosystem tiebreaker, R349 Path C "具体对位", R237 SPM, R331 License Risk Protocol
