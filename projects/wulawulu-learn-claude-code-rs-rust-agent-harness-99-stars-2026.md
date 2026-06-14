---
title: wulawulu/learn-claude-code-rs — Rust 版 Agent Harness 渐进式教程
description: 渐进式 Rust 教程：从最小 agent loop 到 tools、subagents、memory、teams、worktrees、MCP、类型化工具路由。
slug: wulawulu-learn-claude-code-rs-rust-agent-harness-99-stars-2026
stars: 99
license: MIT
topics:
  - agent-harness
  - rust
  - claude-code
  - coding-agent
  - tutorial
source: GitHub API (R380)
date: 2026-06-14
commit: Round380
license_risk: MIT — clean, no restrictions
---

# wulawulu/learn-claude-code-rs — Rust 版 Agent Harness 渐进式教程

## 1. 项目概述

一个**渐进式 Rust 教程**，从最小的 agent loop 开始，逐步添加 tools、planning、subagents、skills、context compaction、permissions、hooks、memory、multi-agent collaboration、worktree isolation、MCP/plugins 和 typed tool routing。

每个章节是**独立的可运行 Rust crate**，可按顺序阅读或直接跳转到感兴趣的主题查看 harness 能力在数据结构、运行时循环、工具接口和持久化状态中的表达。

> 受 [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) 启发，针对 Rust 生态重新实现和组织。

## 2. 目标读者

- 想深入理解 coding agent 内部原理，而不只是使用现成产品的人
- 想用 Rust 编写 AI agent、CLI 工具或自动化工具的人
- 已了解 LLM API，想学习 tool use、subagents、permissions、hooks、memory 等工程结构的人
- 对 Claude Code、Codex、Devin、Cursor Agent 底层基础设施感兴趣的人

## 3. 核心主题（按章节覆盖）

| 主题 | 说明 |
|------|------|
| Agent Loop | 最小化的 agent 执行循环 |
| Tools | 工具定义与调度 |
| Planning | 规划能力的实现 |
| Subagents | 子智能体拆分与协同 |
| Skills | 技能系统 |
| Context Compaction | 上下文压缩 |
| Permissions | 权限模型 |
| Hooks | 钩子系统 |
| Memory | 记忆系统 |
| Multi-Agent Collaboration | 多智能体协作 |
| Background Work | 后台任务 |
| Worktree Isolation | Git worktree 隔离 |
| MCP / Plugins | MCP 协议和插件系统 |
| Typed Tool Routing | 类型化工具路由 |

## 4. 架构图

项目包含架构图（`architecture.png`），展示从最小 loop 到完整 harness 的演进路径。

## 5. 快速开始

### 环境准备

```bash
rustup update
cargo --version
```

### 配置模型 API

```bash
cp .env.example .env
# 编辑 .env
ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_BASE_URL=your_anthropic_compatible_base_url
ANTHROPIC_MODEL=your_model_name
```

### 运行第一章

```bash
cargo run -p s01_agent_loop
```

### 运行完整集成版本

```bash
cargo run -p sfull
```

### 检查整个 workspace

```bash
cargo check --workspace
```

## 6. 与本仓库的关联

### 6.1 SPM 配对：理论 ↔ 多语言实现

| 维度 | harness-books (R379) | learn-claude-code-rs (R380) | 配对强度 |
|------|---------------------|---------------------------|---------|
| 理论框架 | 双书全景 9+7 章 | Rust 实现 | ⭐⭐⭐⭐ |
| Control Plane | Ch.2 Prompt Is the Control Plane | Rust control flow / permissions | ⭐⭐⭐ |
| Memory | Ch.5 Context Governance | Rust memory 层 | ⭐⭐⭐ |
| Tools/Permissions | Ch.4 Tools, Permissions | Rust typed tool routing | ⭐⭐⭐ |
| Subagents | Ch.7 Multi-Agent | Rust subagent spawning | ⭐⭐⭐ |
| Worktree | Claude Code worktree | Git worktree isolation | ⭐⭐⭐⭐ |

**Pair 闭环**：harness-books 提供理论全景，learn-claude-code-rs 提供 Rust 实现路径。两者形成"理论 → 多语言实现"的完整配对。

### 6.2 与同类项目的差异化

| 项目 | 语言 | 特点 |
|------|------|------|
| shareAI-lab/learn-claude-code | Python | 原始参考项目 |
| **learn-claude-code-rs** | **Rust** | Rust 生态移植 + 独立演进 |
| wquguru/harness-books | 理论书籍 | 纯理论框架 |

Rust 实现的优势：
- **类型安全**：编译期校验，降低 runtime 错误
- **性能**：轻量级，适合资源受限场景
- **FFI 友好**：可与其他语言生态集成

### 6.3 补充价值

- 99⭐ 虽然低于 Path C 默认门槛（100⭐），但 MIT license 清洁
- 作为 Rust 生态中少数的 agent harness 系统性教程，具有稀缺性
- 与本仓库 harness cluster（30+ 篇）形成语言维度的补充覆盖

## 7. License

**MIT** — 无限制使用。

## 8. 参考链接

- GitHub: https://github.com/wulawulu/learn-claude-code-rs
- 参考源: [shareAI-lab/learn-claude-code](https://github.com/shareAI-lab/learn-claude-code)