---
title: 0xNyk/lacp — Control-Plane-Grade Agent Harness
description: Control-plane-grade agent harness for Claude, Codex & Hermes: policy gates, verification/evidence loops, 5-layer memory, and auditable execution.
slug: 0xNyk-lacp-control-plane-grade-agent-harness-268-stars-2026
stars: 268
license: MIT
topics:
  - agent-harness
  - control-plane
  - claude-code
  - verification-loops
  - policy-gates
  - hermes
source: GitHub API (R380)
date: 2026-06-14
commit: Round380
license_risk: MIT — clean, no restrictions
---

# 0xNyk/lacp — Control-Plane-Grade Agent Harness

## 1. 项目概述

**LACP** (Local Agent Control Plane) 是一个以 **control-plane 为核心** 的 agent harness 框架，为 Claude、Codex 和 Hermes 提供本地优先的、受策略管控的 agent 执行环境。

核心定位：**不是生成输出，而是产出可审计的、符合策略的结果**。

> Alpha v0.9.0，处于活跃开发中。

## 2. 核心架构

### 2.1 双层结构：Harness Layer + Control Plane Layer

| 层级 | 职责 | 关键组件 |
|------|------|---------|
| **Harness Layer** | 任务执行循环 | Tasks、Verification Contracts、Evidence Manifests、Replayable Run Loops |
| **Control Plane Layer** | 策略治理 | Risk Tiers（safe/review/critical）、Budget Ceilings、Context Contracts、Session Fingerprints、Approvals、Provenance |

### 2.2 Policy Gates（策略门控）

- **Risk Tiers**：safe / review / critical 三级风险分层
- **Budget Ceilings**：token 用量上限
- **Context Contracts**：上下文合约
- **Session Fingerprints**：会话指纹
- 每次 agent 调用都经过门控和审计

### 2.3 5-Layer Memory

| 层 | 功能 |
|----|------|
| Session Memory | 单次会话内的上下文保持 |
| Obsidian Knowledge Graph | 结构化知识图谱持久化 |
| Ingestion Pipeline | 知识摄取流水线 |
| Code Intelligence (GitNexus) | 代码语义索引 |
| Agent Identity | Agent 身份 + 哈希链溯源 |

### 2.4 Hook Pipeline（Claude Code 集成）

可插拔 Python Hooks：
- **Session Context Injection**：会话上下文注入
- **Pre-tool Guards**：工具调用前置守卫
- **Write Validation**：写入校验
- **Stop Quality Gates**：停止质量门控（本地 LLM 评估）

### 2.5 Multi-Agent Orchestration

- **dmux/tmux**：会话隔离管理
- **Git Worktree Isolation**：代码仓库多分支隔离
- **Swarm Workflows**：多智能体协同
- **Claude Native Worktree Backend**：Claude 原生 worktree 支持

### 2.6 Evidence Pipeline

支持三类端到端测试：
- Browser e2e
- API e2e
- Smart Contract e2e

产出 **Evidence Manifests**（证据清单），用于 PR 前置门控。

## 3. 技术特性

### 安装方式

```bash
# Homebrew
brew tap 0xNyk/lacp && brew install lacp

# 或 cURL bootstrap
curl -fsSL https://raw.githubusercontent.com/0xNyk/lacp/main/install.sh | bash
```

### 快速验证

```bash
lacp bootstrap-system --profile starter --with-verify
lacp doctor --json | jq '.ok,.summary'
```

### 执行层级（Execution Tiers）

| 层级 | 场景 |
|------|------|
| `trusted_local` | 完全信任的本地执行 |
| `local_sandbox` | 本地沙箱隔离 |
| `remote_sandbox` | 远程沙箱（Daytona/E2B） |

策略驱动路由 + 提供商覆盖。

## 4. 与本仓库的关联

### 4.1 SPM 关键字级配对

| LACP 关键词 | 对应 Article | 命中 |
|------------|-------------|------|
| Control Plane（控制平面） | R337 `anthropic-managed-agents-scheduled-deployments-vault-env-vars-2026.md` — "Anthropic 把 control plane 做成了平台原语" | ✅ |
| Policy Gates（策略门控） | R375 `nvidia-nemoclaw-open-shell-runtime-20791-stars-2026.md` — nanoclaw 策略层 | ✅ |
| Verification/Evidence（验证/证据） | R337 — evidence manifest / verification | ✅ |
| Session Memory（会话记忆） | R354 `axdsan-mnemosyne-zero-dependency-memory-865-stars-2026.md` — 零依赖内存 | ✅ |
| Multi-Agent Orchestration | R337/R354 — 多智能体协同 | ✅ |
| Hook Pipeline | R337 — pre-tool guards / context injection | ✅ |

**6 个核心命题词同时命中 → R375 协议 #34 Layer 2 SPM 命中**

### 4.2 与既有项目的三角对位

```
理论框架层: wquguru/harness-books (R379, 2465⭐)
    ↓ 全景理论（Control Plane Ch.2 / Query Loop Ch.3 / Permissions Ch.4）
SDK 实现层:   0xNyk/lacp (R380, 268⭐) ← 本篇
    ↓ policy gates / 5-layer memory / evidence pipelines
一手源:      Anthropic R337/R354 Articles
```

LACP 是 harness-books 理论框架在工程实践层的具体实现验证。

### 4.3 与同类项目的差异化

| 项目 | 特点 | lacp 的差异化 |
|------|------|--------------|
| nanoclaw (NVIDIA) | 30K⭐, Shell Runtime, 云原生 | lacp 本地优先、轻量、Python Hooks 可扩展 |
| loop-engineering | Anthropic 开源, 框架层 | lacp 聚焦 control-plane 治理 + evidence pipeline |
| harness-books | 2465⭐, 双书理论 | lacp 是书籍理论的具体代码实现 |

## 5. 重要文件

- `docs/assets/readme-banner.png` — 项目 banner
- `install.sh` — 安装脚本
- `LICENSE` — MIT License

## 6. License

**MIT** — 无限制使用，商业友好。

## 7. 参考链接

- GitHub: https://github.com/0xNyk/lacp
- Alpha Release v0.9.0: https://github.com/0xNyk/lacp/releases