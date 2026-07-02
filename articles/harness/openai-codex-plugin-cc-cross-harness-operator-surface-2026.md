---
title: OpenAI Codex Plugin for Claude Code：当竞品 1st-party 走进对手 Harness
date: 2026-07-02
source: openai/codex-plugin-cc GitHub README + TLDR AI 2026-03-31 + FountainCity Codex/Claude Driver-Worker 报道
source_url: https://github.com/openai/codex-plugin-cc
author: OpenAI Codex Plugin for Claude Code (1st-party) + TLDR + FountainCity
tags: [codex, claude-code, cross-harness, layer-6, operator-surface, subagent, plugin-marketplace, openai-official, driver-worker]
cluster: cross-harness-operator-surface
related_articles:
  - articles/harness/github-issue-fields-mcp-ga-platform-operation-canonical-interface-2026.md
  - articles/ai-coding/claude-code-2-1-198-autonomous-delivery-harness-notification-hooks-2026.md
  - articles/practices/ai-coding/ai-coding-three-layer-convergence.md
pair_project: openai-codex-plugin-cc-cross-harness-operator-22k-stars-2026
---

> **核心论点**：R622 命名的 Layer 6: Autonomous Delivery Harness 需要跨平台执行能力；R623 命名的 Cluster `platform-operation-canonical-interface` 把 GitHub Issue Fields / Repository / Browser 三 surface 收束到「MCP + Hooks + Browser Surface」三套接口。但 R622/R623 都默认 Agent 在自家 Harness 里操作——把 Anthropic Claude Code 当成唯一宿主。今天发现 **OpenAI 1st-party 维护的 `openai/codex-plugin-cc` 仓库（22k Stars、Apache-2.0、3 月 30 日首次 push、6 月 23 日仍活跃）以 Claude Code 插件的形式把 Codex 包装成 Claude Code 内部可调用的 subagent**，提供 7 个命令（`/codex:review` / `:adversarial-review` / `:rescue` / `:transfer` / `:status` / `:result` / `:cancel`）。这意味着 **Anthropic 和 OpenAI 共同把「跨 Harness Operator Surface」认定为 2026 H2 AI Coding 工具竞争的新一层**——竞品不只是抢用户，还主动把对手的 Harness 当成自己的运行时，通过 plugin marketplace 在对方 Harness 里注册可编程 Operator。这条 transition 的范式分量等于「Harness 之间从零和博弈切换到正交化协作」：写作（Claude Code）和评审（Codex）成了两个可独立调度的 Agent Operator。

---

## 一、为什么这件事比它看上去重要

先看一组对比：

| 维度 | LangChain、AutoGen、CrewAI 等多 Agent 框架 | openai/codex-plugin-cc |
|------|---------------------------------------|------------------------|
| **跨 Harness 性质** | 同一个 Python 进程内部的多 Agent 协作 | 跨**厂商 / 跨 CLI / 跨 Anthropic+OpenAI** 的协作 |
| **1st-party 背书** | 第三方框架 | OpenAI 官方仓库（`openai/` org）|
| **集成方式** | SDK import | Claude Code plugin marketplace（`/plugin marketplace add openai/codex-plugin-cc`）|
| **运行时** | 同一 Python runtime | Claude Code 调度 Codex CLI + Codex App Server |
| **认证** | 框架自己处理 | 直接复用本地 Codex CLI 认证 |

关键不是 Codex 能做什么（Codex CLI 本来就能 review），而是 **OpenAI 主动把 Codex 包装成 Claude Code 的内部 subagent（`codex:codex-rescue`），并把它发布到 Claude Code 自己的 plugin marketplace 上**。这条 1st-party 决策，等同于 Anthropic 和 OpenAI 共同承认：**AI Coding 工具的下一阶段不在「谁更强」，而在「谁能在对手 Harness 里成为一等 Operator」**。

笔者认为这是 2026 H2 Agent 生态最重要的范式 transition 之一。Harness 不再是封闭的工作流容器，而是「其他 Agent Operator 入驻的执行平面」。这跟传统 SaaS 的「API 集成」不是一回事——plugin 不只是数据接口，而是 subagent 形式的执行接口。

---

## 二、7 个命令揭示的工程机制

`openai/codex-plugin-cc` 暴露的 7 个 slash command 看似简单，但每一个背后都是一种具体的 Operator 语义：

```bash
/codex:review                  # 静态 Codex 评审（read-only，最常用）
/codex:adversarial-review      # 可指挥的对抗性评审（质疑选择、压力测试）
/codex:rescue                  # 把任务交给 Codex subagent 处理
/codex:transfer                # 把会话从 Claude Code 移交到 Codex
/codex:status                  # 查询后台任务进度
/codex:result                  # 取回 Codex 任务结果
/codex:cancel                  # 取消运行中的 Codex 任务
```

把这 7 个命令按 Operator Surface 维度展开，会看到一个完整的「评审 → 派发 → 状态 → 取消」生命周期：

| 阶段 | 命令 | 角色定位 | 关键设计决策 |
|------|------|---------|-------------|
| **评审态** | `/codex:review` | 默认 read-only reviewer | 不动代码，只看 diff——零写权限 |
| **质疑态** | `/codex:adversarial-review` | 可 steerable challenger | 接受焦点文本（如 "challenge whether this was the right caching and retry design"），可以问「如果选 Redis 不用 Memcached 会怎样」 |
| **派发态** | `/codex:rescue` | 任务移交 agent | 把当前任务交给 `codex:codex-rescue` subagent，Claude Code 不再继续 |
| **移交态** | `/codex:transfer` | 会话级移交 | 把当前 Claude Code session 的上下文整段搬到 Codex |
| **状态态** | `/codex:status` / `:result` / `:cancel` | 后台任务生命周期 | `--background` 模式下的进度查询、结果回收、取消 |

这 7 个命令不是 7 个独立工具，而是一个**完整的 subagent 操作协议**。特别值得注意的是：

### 2.1 `adversarial-review` 的「可指挥」语义

`/codex:review` 是只读静态评审，但 `/codex:adversarial-review` 接受可指挥的焦点：

> 原文引用：`/codex:adversarial-review --base main challenge whether this was the right caching and retry design`
> 原文引用：`/codex:adversarial-review --background look for race conditions and question the chosen approach`

这意味着 Codex 不只是被动 reviewer，而是**可被注入具体焦虑点的对抗性思考者**——你能告诉它「请用 race condition 的视角审」或者「请质疑我选的 caching 方案」。这种「焦点指挥 + 对抗性立场」的组合，等同于让一个 Operator 同时具备「独立视角」和「任务适配」两个属性。

### 2.2 `:rescue` subagent 集成

`:rescue` 不是简单调用 Codex CLI，而是把 Codex 包装成 Claude Code 内部可调度的 subagent：

> 原文引用：`Hands a task to Codex through the codex:codex-rescue subagent.`

这条机制意味着 Claude Code 的 task graph 里多了一个可被调度的 Operator 节点。Claude Code 不再只是「自己干」，而是「可以把任务交给 Codex 干」。这等于把 Layer 6 (R622) 的「Autonomous Delivery Harness」从「单 Harness 内部派发」扩展到「跨 Harness 派发」。

### 2.3 复用本地 Codex CLI 的认证与配置

`/codex:setup` 的设计非常聪明：它不引入新认证，而是要求用户本地已经 `codex login` 完毕，然后插件直接复用本地 Codex CLI 的认证、配置、模型选择：

> 原文引用：`This plugin uses your local Codex CLI authentication.`
> 原文引用：`If you already use Codex, the plugin picks up the same configuration.`
> 原文引用：`Your existing sign-in method and config still apply.`

这意味着 Anthropic Claude Code + OpenAI Codex CLI 的「联邦执行」是**零信任边界**的——没有代理层、没有中间凭证、没有跨厂商 OAuth。Claude Code 通过进程间调用直接用本地 Codex 的能力。

---

## 三、为什么这个 cluster 该命名 `cross-harness-operator-surface`

R622 命名的 `autonomous-delivery-harness` 关注 Harness **自身**的能力（Background Agent auto-PR + Notification hook + Team failure recovery）。
R623 命名的 `platform-operation-canonical-interface` 关注 Harness 操作**外部平台**的接口（MCP + Hooks + Browser Surface）。

R624 的发现暴露了第三个维度：**跨 Harness 的 Operator Surface**——一个 Harness 可以作为另一个 Harness 的执行后端，且这种「跨」是 1st-party 维护的、有版本演进的、有完整子命令协议的。

| Cluster | 关注对象 | 代表事件 | 范式分量 |
|---------|---------|---------|---------|
| **autonomous-delivery-harness** (R622) | Harness 自身能力 | Claude Code v2.1.198 Background Agent auto-PR | Agent 不再需要用户在场就能交付 |
| **platform-operation-canonical-interface** (R623) | Harness ↔ 外部平台 | Issue Fields MCP GA + Claude in Chrome GA | Agent 拥有对外部平台的结构化写权限 |
| **cross-harness-operator-surface** (R624) | Harness ↔ 竞品 Harness | openai/codex-plugin-cc | 跨厂商 Harness 互为 Operator，1st-party 互嵌 |

三条 cluster 合起来，构成 Layer 6 Harness 工程的完整拼图：

1. **Harness 自给自足**（R622）
2. **Harness 操作世界**（R623）
3. **Harness 互相调用**（R624）

笔者认为 R624 这条 cluster 是 Layer 6 范式真正的「社会化」拐点——之前的 Harness 是「能力封闭的 worker」，从今天开始 Harness 是「能力开放的 operator mesh」。后续 6-12 个月，这条范式会继续展开：

- Anthropic 是否会出 1st-party 插件把 Claude 嵌入 Codex / Cursor？
- GitHub Copilot 是否会出 1st-party 插件让 Claude Code / Codex 调用 Copilot？
- 「可指挥的 reviewer」(steerable reviewer) 是否会成为所有跨 Harness 插件的标配？

R625 重点监控：**Anthropic 是否对等回应——出 1st-party Claude 插件嵌入 Codex / Cursor**。如果回应，是 cluster 加速；如果沉默，是单边开放。

---

## 四、对开发者的实际意义

不要把这篇文章读成「OpenAI 帮 Claude Code 做事」的宣传。它更实际的意义是：

### 4.1 写和审是正交 Concern

Claude Code 写、Codex 审，两个 Operator 各司其职。这跟 pair programming 里「作者不能审自己的代码」是同构的——`/codex:review` 把这条工程常识转成了工程机制：

> 原文引用：`Code review especially for multi-file changes might take a while. It's generally recommended to run it in the background.`

后台化 review（`--background`）是默认推荐——意味着 Claude Code 写完代码不必等 Codex 审完，可以并行继续下一步。

### 4.2 失败有 rescue 通道

`/codex:rescue` 的存在意味着「Claude Code 解决不了的问题」不再是死胡同——可以把任务交给 Codex subagent 试一次。这等于在 Harness 内部建了一个「跨厂商 fallback」。

### 4.3 思考可被对抗性挑战

`/codex:adversarial-review` 不是「请赞美我的代码」，而是「请质疑我的选择」。这条机制让 Agent Operator 从「执行者」变成「批判者」——这是 Harness 工程里少见的「内置反对派」设计。

---

## 五、未解决的问题

| 开放问题 | 重要程度 | 影响 |
|---------|---------|------|
| Anthropic 是否会出对等 1st-party 插件（让 Claude 嵌入 Codex）？ | 高 | 如果回应，是 cross-harness-operator-surface 加速；如果沉默，OpenAI 单边开放，Anthropic 默认接受「Claude Code 是被集成的对象」|
| `/codex:transfer` 是否会成为「会话级别 migration」的事实标准？ | 中 | 如果是，「Harness 边界」的定义会发生根本改变——session 不再属于某个 Harness，而是属于「Operator mesh」|
| `:rescue` 是否会被滥用为「跨厂商 token 套利」？ | 中 | 如果是，需要 plugin marketplace 加 rate limit + usage audit |
| Steerable reviewer 是否会扩展到 steerable executor？ | 高 | 如果是，跨 Harness 不仅可评审，还可可执行——风险和价值同步放大 |

---

## 六、给读者的下一步建议

| 你是... | 你应该... |
|--------|----------|
| **Claude Code 重度用户** | 装一次 `/codex:review --background`，体验「Claude 写、Codex 审」的工作流 |
| **Harness 维护者** | 思考自己的 Harness 是否提供了「被嵌入」接口——`/plugin marketplace` 是否对外暴露 + subagent 是否可被注册 |
| **架构师** | 把 Layer 6 拼图从 2 块（R622 + R623）扩到 3 块（+ R624）——你的 Agent 系统是否同时具备「自给自足」「操作世界」「跨 Harness 调用」三层能力？|
| **AI Coding 工具决策者** | 重估「工具碎片化」的风险模型——不再是「用户选哪个 Harness」，而是「用户怎么编排多个 Harness」 |

---

**References**:

1. openai/codex-plugin-cc GitHub: <https://github.com/openai/codex-plugin-cc>
2. TLDR AI 2026-03-31 "Codex Plugin for Claude Code": <https://tldr.tech/ai/2026-03-31>
3. FountainCity "Codex (GPT-5.5) vs Claude Code (Opus 4.7): Driver/Worker Guide": <https://fountaincity.tech/resources/blog/codex-claude-code-harness-together>
4. Firecrawl "Claude Code vs Codex: Which AI Coding Agent Should You Use in 2026": <https://www.firecrawl.dev/blog/claude-code-vs-codex>
5. Layer 6 (R622): articles/ai-coding/claude-code-2-1-198-autonomous-delivery-harness-notification-hooks-2026.md
6. platform-operation-canonical-interface (R623): articles/harness/github-issue-fields-mcp-ga-platform-operation-canonical-interface-2026.md

---

**Tags**: codex, claude-code, cross-harness, layer-6, operator-surface, subagent, plugin-marketplace, openai-official, driver-worker

**Cluster**: `cross-harness-operator-surface`（R624 首次命名）

**Word count**: ~2,400 字