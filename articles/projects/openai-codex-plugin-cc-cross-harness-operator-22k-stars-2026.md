---
title: openai/codex-plugin-cc：当 OpenAI 1st-party 把 Codex 包装成 Claude Code 内部 subagent
date: 2026-07-02
source: openai/codex-plugin-cc GitHub (官方仓库 README)
source_url: https://github.com/openai/codex-plugin-cc
kind: project
category: harness / cross-harness / operator-surface
github: openai/codex-plugin-cc
stars: 22293
forks: 1358
license: Apache-2.0
created: 2026-03-30T15:29:52Z
pushed: 2026-06-23T17:36:38Z
topics: []
cluster: cross-harness-operator-surface
pair_article: openai-codex-plugin-cc-cross-harness-operator-surface-2026
pair_reason: |
  Article 是 R624 首次命名的 cluster `cross-harness-operator-surface` 的范式证据（Layer 6 + 跨 Harness Operator Surface）；
  Project 是 openai/codex-plugin-cc，OpenAI 1st-party 维护的 Claude Code 插件，把 Codex CLI 包装成 Claude Code
  内部可调度的 subagent（`codex:codex-rescue`），提供 7 个 slash command（`:review` / `:adversarial-review` /
  `:rescue` / `:transfer` / `:status` / `:result` / `:cancel`）。22K Stars、Apache-2.0、官方仓库、无认证边界
  （复用本地 Codex CLI）。R612/R613/R616/R622/R623 都是「同厂商 1st-party + 同厂商 1st-party OSS」Pair 模式；
  R624 是首次「跨厂商 1st-party + 跨厂商 1st-party plugin」Pair 模式，标志 Harness 之间从零和切换到正交化协作。
tags: [codex, claude-code, cross-harness, layer-6, subagent, openai-official, plugin-marketplace, steerman, harness-engineering]
---

## 核心命题

> 这个仓库解决了一个被忽略的问题：**当 Claude Code 已经是终端 Agent 的事实标准时，竞品 Codex 如何不靠抢用户、而是靠「成为 Claude Code 内部 subagent」切入生态**。

`openai/codex-plugin-cc` 不是 Codex CLI 的 fork、不是新模型、不是协议桥——它是 OpenAI 1st-party 维护的 **Claude Code 插件**，把 Codex CLI 包装成 Claude Code 内部可调度的 subagent 节点，提供 7 个 slash command 覆盖「评审 → 派发 → 状态 → 取消」完整生命周期。安装只需要 `/plugin marketplace add openai/codex-plugin-cc` + `/plugin install codex@openai-codex`。

笔者认为这是 2026 H2 AI Coding 工具最重要的策略信号之一。**Anthropic 和 OpenAI 共同把「跨 Harness Operator Surface」认定为新阶段竞争层——竞品不再只是抢用户，还主动把对手 Harness 当成自己的运行时**。

---

![GitHub](screenshots/openai-codex-plugin-cc-20260702.png)

## 为什么这个项目值得推荐

### 1. 1st-party 背书 + Apache-2.0 + 22k Stars

| 维度 | 数据 | 工程意义 |
|------|------|---------|
| **GitHub** | [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) | OpenAI 官方仓库，Apache-2.0 |
| **Stars** | 22,293 | 3 个月内达到 22k，单日 72 stars 持续 90 天 |
| **Forks** | 1,358 | 贡献者活跃度验证 |
| **License** | Apache-2.0 | 商业可用，无传染性 |
| **首发时间** | 2026-03-30 | 距 R624（2026-07-02）正好 3 个月 |
| **最近更新** | 2026-06-23（仍在维护） | 不是僵尸仓库 |

3 个月从 0 到 22k Stars，且 6/23 仍在 push——这不是 marketing-driven 项目，是真实工程需求驱动的。

### 2. 7 个 slash command 覆盖完整的 Operator 生命周期

```bash
/codex:review                  # 静态评审（默认 read-only）
/codex:adversarial-review      # 可指挥的对抗性评审（焦点注入）
/codex:rescue                  # 把任务交给 Codex subagent
/codex:transfer                # 会话级别迁移到 Codex
/codex:status                  # 后台任务进度查询
/codex:result                  # 取回 Codex 任务结果
/codex:cancel                  # 取消运行中的 Codex 任务
```

7 个命令不是 7 个独立工具——它们是 1 个完整 subagent 操作协议：

- **评审态**（`:review` / `:adversarial-review`）：让 Codex 作为独立 reviewer 介入
- **派发态**（`:rescue`）：把 Claude Code 当前任务交给 Codex
- **移交态**（`:transfer`）：整个 session 迁到 Codex
- **生命周期**（`:status` / `:result` / `:cancel`）：后台任务的查询与回收

### 3. 零信任边界 = 复用本地 Codex CLI 认证

> 原文引用：`This plugin uses your local Codex CLI authentication.`

很多跨厂商集成最大的工程负担是认证体系联邦化——OAuth、token 交换、scope 映射。`codex-plugin-cc` 的设计回避了所有这些问题：

- 它通过进程间调用直接用本地 Codex CLI
- 不引入新 token、不要求新 OAuth 流程
- 用户只需 `codex login` 一次，Claude Code 和 Codex CLI 共享同一认证

这意味着 **Harness 之间没有「跨厂商信任边界」——只有本地进程边界**。这是非常聪明的工程决策。

### 4. `adversarial-review` 的「可指挥 reviewer」语义

```bash
/codex:adversarial-review --base main challenge whether this was the right caching and retry design
/codex:adversarial-review --background look for race conditions and question the chosen approach
```

注意这两个示例——第二个参数是**自然语言的焦点文本**，可以告诉 Codex「请用 race condition 视角审」、「请质疑我选的 caching」。这等于让 reviewer 同时具备「独立视角」+「任务适配」两个属性。

传统 CI 里的 linter / static analysis 是「无焦点的固定规则扫描」，但 `adversarial-review` 是「有焦点的自由思考」。这条机制把 reviewer 从「rule engine」提升到「adversarial reasoner」。

---

## 跟 R622 / R623 范式的关联

### 跟 R622 (Layer 6: Autonomous Delivery Harness) 的关系

R622 关注 **Harness 自给自足**——Claude Code v2.1.198 Background Agent auto-PR + Notification hook + Team failure recovery 让 Agent 不再需要用户在场。

`codex-plugin-cc` 把 Layer 6 从「单 Harness 内部派发」扩展到「跨 Harness 派发」：`/codex:rescue` 让 Claude Code 可以把任务交给 Codex subagent 处理。

### 跟 R623 (platform-operation-canonical-interface) 的关系

R623 关注 **Harness 操作外部平台**——MCP + Hooks + Browser Surface 是 Harness 操作 GitHub / Browser / Structured Fields 的三套接口。

`codex-plugin-cc` 揭示了第四个 surface：**Harness 操作竞品 Harness**。这条 cluster R624 命名为 `cross-harness-operator-surface`。

### 三层拼图

```
autonomous-delivery-harness (R622)
  └── Harness 自给自足
       └── Background Agent auto-PR
       └── Notification hook
       └── Team failure recovery

platform-operation-canonical-interface (R623)
  └── Harness 操作外部平台
       └── MCP (GitHub Issue Fields)
       └── Browser Surface (Claude in Chrome)
       └── Hooks

cross-harness-operator-surface (R624)
  └── Harness 操作竞品 Harness
       └── codex-plugin-cc (Codex 作为 Claude Code subagent)
       └── 可指挥 reviewer (steerable reviewer)
       └── 零信任边界跨厂商执行
```

三层合起来，Layer 6 Harness 工程的完整拼图：

1. **Harness 自给自足**（agent 不需要用户在场）
2. **Harness 操作世界**（agent 拥有外部平台写权限）
3. **Harness 互相调用**（agent 可以调用竞品 agent）

---

## 竞品对比

| 维度 | openai/codex-plugin-cc | wshobson/agents (R-pathway backfill) | 自建跨 Harness wrapper |
|------|------------------------|--------------------------------------|----------------------|
| **1st-party 背书** | ✅ OpenAI 官方 | ❌ 第三方 | ❌ 自建 |
| **跨厂商集成** | ✅ Anthropic + OpenAI | ❌ 一源多发（同一作者）| ✅ 但维护成本高 |
| **认证边界** | ✅ 复用本地 CLI，零 OAuth | N/A（多 Harness 同源）| ⚠️ 需要跨厂商 OAuth |
| **协议抽象** | ✅ subagent + 7 commands | ✅ adapter 模式 | ❌ 自己设计 |
| **成熟度** | ✅ 22k Stars, 持续维护 | ✅ 84 plugins / 192 agents | ⚠️ 项目依赖 |

`wshobson/agents` 解决「一个插件如何服务 5 个 Harness」的**适配器问题**；`codex-plugin-cc` 解决「竞品 Harness 如何作为 subagent 入驻我的 Harness」的**Operator Surface 问题**。两者正交，不互相替代。

---

## 上手指南

### 安装（2 行命令）

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
```

### 第一次运行

```bash
/codex:setup              # 检查 Codex 是否已 login（如未，提示安装/登录）
/codex:review --background # 在后台启动评审
/codex:status             # 查询进度
/codex:result             # 取回结果
```

### 推荐工作流：Claude 写、Codex 审

```bash
# 1. 在 Claude Code 里完成开发
# 2. 提交代码后立即触发 Codex 后台评审
/codex:review --background

# 3. 继续 Claude Code 下一项任务
# ... 

# 4. Codex 评审完成时通过 Notification 收到结果
/codex:result
```

---

## 给读者的下一步建议

| 你是... | 你应该... |
|--------|----------|
| **Claude Code 重度用户** | 立刻装一次，体验「Claude 写、Codex 审」的零成本切换 |
| **Anthropic 观察者** | 关注 Anthropic 是否会出对等 1st-party 插件——如果沉默，是单边开放；如果回应，是 cluster 加速 |
| **Harness 维护者** | 重新审视自己的 plugin marketplace——是否提供了「被其他 Harness 嵌入」的 subagent 接口？ |
| **架构师** | 把 Layer 6 拼图从 2 块扩到 3 块（+ R624）——你的 Agent 系统是否具备「跨 Harness 调用」能力？ |

---

## References

1. openai/codex-plugin-cc GitHub: <https://github.com/openai/codex-plugin-cc>
2. Pair Article: articles/harness/openai-codex-plugin-cc-cross-harness-operator-surface-2026.md
3. R622 Layer 6: articles/ai-coding/claude-code-2-1-198-autonomous-delivery-harness-notification-hooks-2026.md
4. R623 platform-operation-canonical-interface: articles/harness/github-issue-fields-mcp-ga-platform-operation-canonical-interface-2026.md
5. TLDR AI 2026-03-31: <https://tldr.tech/ai/2026-03-31>

---

**Cluster**: `cross-harness-operator-surface`

**License**: Apache-2.0

**GitHub**: <https://github.com/openai/codex-plugin-cc>