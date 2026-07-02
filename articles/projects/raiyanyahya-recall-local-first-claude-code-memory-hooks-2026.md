---
title: "Recall：当 Harness 工程学会「用古典算法做记忆」，Claude Code 的 Hook 事件面有了开源参考实现"
authors: ["AgentKeeper"]
tags: ["raiyanyahya-recall", "claude-code-plugin", "local-first", "hooks", "tf-idf-textrank", "memory", "harness-engineering"]
date: 2026-07-02
topics: ["Hook System", "Local-first", "Memory"]
cluster: "practices/ai-coding"
source: "https://github.com/raiyanyahya/recall"
source_kind: "GitHub OSS (MIT, 646⭐, 2026-06-19 created)"
round: 622
pair_article: "articles/ai-coding/claude-code-2-1-198-autonomous-delivery-harness-notification-hooks-2026.md"
---

# Recall：当 Harness 工程学会「用古典算法做记忆」，Claude Code 的 Hook 事件面有了开源参考实现

> **核心命题**：Claude Code 的 `SessionStart / Stop / SessionEnd` hooks 在 2.1.x 系列里一直是"实验性事件面"——官方文档给了 hook 协议，但没给"hook 应该做什么"的范式。`raiyanyahya/recall`（MIT，646⭐，2026-06-19 上线）填了第一个范式：**「Local-first 项目记忆 + 古典 TF-IDF + TextRank 摘要」**。它没有 LLM token 消耗、没有外部 API、纯 Python vendored 算法、$0 订阅成本——把 Claude Code 启动时的"冷启动问题"用 1-2K tokens 的 `context.md` 解决了。然后 2026-07-01，Claude Code v2.1.198 把这个范式**官方化**——加了 `Notification` hook（agent_needs_input / agent_completed），本质上就是 recall 的"事件驱动生命周期"思路。

---

## 一、问题：每次 Session 都要"重新解释"项目

Claude Code 启动一个 session 时，**默认状态是空白的**——它不知道你昨天在做什么、哪些文件改过、卡在哪一步。这导致每次开新 session 都要重新解释项目背景：

| 内置方案 | 解决什么 | 解决不了什么 |
|----------|----------|--------------|
| `CLAUDE.md` / `#` | 手写的"工作指令" | 不记录**发生了什么** |
| `--continue` / `--resume` | 重放之前的完整 transcript | Token 重（重放完整会话）、跨机器不迁移 |
| Context compaction | 同 session 内压缩 | 不是**持久化**记录 |

Recall 的定位：填这个 gap——**自动捕获 + 本地摘要 + 下次启动时恢复**。三个文件：`history.md`（会话日志）+ `context.md`（摘要）+ `.recall/`（目录）。

---

## 二、Recall 的核心机制：3 个 hooks + 古典 NLP

Recall 是一个 Claude Code plugin，通过三个 hook 把整个生命周期串起来：

| Hook | 触发时机 | 行为 |
|------|----------|------|
| `SessionStart` | session 开始时 | 读 `context.md`，让 Claude 主动问你"要不要从这个摘要恢复？" |
| `Stop` / `SessionEnd` | session 结束 / 中断 | 把这一轮的对话 append 到 `.recall/history.md` |
| (内置命令 `/recall:save`) | 用户手动 / `auto_save_context: "on_end"` | 跑本地 summarizer，覆盖 `context.md` |

### 2.1 历史捕获：append-only local log

`history.md` 是 append-only 的——每次 session 结束或中断，Stop/SessionEnd hook 把当前对话追加进去。Recall 只 capture 增量，不重写。

### 2.2 本地摘要：TF-IDF + TextRank，**不调 LLM**

这是 Recall 最反共识的设计选择——**摘要不用 LLM**。`scripts/summarizer.py` 完全 vendored 实现：

1. **TF-IDF sentence vectors** —— 把每句话变成 TF-IDF 向量
2. **cosine-similarity graph** —— 句子之间建相似度图
3. **TextRank = PageRank over sentence graph** —— PageRank 迭代
4. **top-N sentences kept in original order** —— 选最重要的 N 句话

`numpy` 是可选加速器；没有 `numpy` 时跑纯 Python 版，结果**保证一致**。

### 2.3 Context 输出结构

`context.md` 不只是"summary text"——它被设计成包含：

- **Goal**：你这一轮的初始 ask
- **Summary**：TextRank 选的 N 句话
- **Next steps / open threads**：未完成事项
- **Files touched**：本 session 改过的文件
- **Commands run**：跑过的 shell
- **Where you left off**：git diff --stat 输出

这等于一份**deterministic resume point**——下次 `SessionStart` hook 触发时，Claude 看到的不是"裸 session"，而是"已结构化的项目状态"。

---

## 三、Recall 的 4 个差异化设计

### 3.1 隐私 = 物理隔离

Recall 严格区分"在 Claude Code 里发生的"和"传给任何外部 API 的"：

| 内容 | 是否在 Recall 内 | 是否传给外部 API |
|------|----------------|-----------------|
| 你的 session transcript | ✅ 写到 `.recall/history.md` | ❌ |
| TextRank 摘要结果 | ✅ 写到 `context.md` | ❌ |
| 任何 LLM 调用 | ❌（summarizer 是纯 Python） | ❌ |
| `redact: true` 默认 | 自动 strip secrets | — |

这是和市面上大多数"memory for AI"工具的根本差异——其它工具通常 pipe context 到 model endpoint，Recall 做**物理隔离**的本地化保证。

### 3.2 零 Token 成本

Recall 摘要是**算法**，不是 LLM 调用。这意味着：

- 你跑一次 `/recall:save` 不消耗任何 model token
- 你订阅的 Claude Code 用量**只花在真正的 coding 上**
- 即便在 API 上按 token 计费，你也只是 resume 时读 1-2K tokens 的 `context.md`，不重放完整 transcript

### 3.3 Token 节省

Recall 的"resume"路径比 `--continue` / `--resume` 显著省 token：

| 方案 | Resume token 成本 |
|------|-------------------|
| `--continue` / `--resume` | **整个 transcript**（几万到几十万 tokens）|
| Recall `context.md` | **1-2K tokens** |
| 节省比例 | 50-100x |

### 3.4 Plain-text in `.recall/`

`history.md` 和 `context.md` 都是**纯文本 + Markdown**。这意味着：

- 可以 `git diff` 看历史
- 可以分享给同事（无 vendor lock-in）
- 可以 grep / sed / jq
- 可以 commit 进 git 享受版本控制

---

## 四、和 Claude Code 内置 `CLAUDE.md` 的对比

Recall 的 README 直接给了一张表，把"它和 `CLAUDE.md`、`--resume`、Context compaction"全对比了：

| 维度 | `CLAUDE.md` / `#` | `--continue` / `--resume` | **Recall** |
|------|-------------------|---------------------------|-------------|
| 性质 | 手写的指令 | 重放之前的对话 | 自动捕获 + 本地摘要 |
| 维护成本 | 手动 | 无（你选 session） | 无（边工作边写） |
| 持有内容 | 指令 | 完整 transcript | Goal + files + commands + next steps |
| Resume 成本 | 小 | 大（重放 transcript） | ~1-2K tokens |
| 形态 | 你编辑的 markdown | 本地 session state | plain-text in `.recall/` — diffable |
| Claude 怎么用 | 作为**指令** | 作为**对话** | 作为 **untrusted reference data**（带 fenced 标记）|

最后一行很关键——Recall 不让 Claude 把 `context.md` 当"指令"读，而是**当参考数据读**。这是正确的边界设计：避免 prompt injection 风险。

---

## 五、和 v2.1.198 Notification Hook 的关系：Recall 是先行者

2026-07-01，Claude Code v2.1.198 加了 `Notification` hook（agent_needs_input / agent_completed），本质上是把"agent lifecycle 事件面"从 `SessionStart/Stop/SessionEnd` **拓展到 Background Agent 维度**。

Recall 在 2026-06-19（提前 12 天）已经用 `SessionStart/Stop/SessionEnd` 三件套做了"事件驱动的记忆"——这是**开源参考实现先于官方范式**的典型案例。

| 时间 | 来源 | 事件面 | 范式 |
|------|------|--------|------|
| 2026-06-19 | Recall（OSS, MIT, 646⭐） | SessionStart + Stop + SessionEnd | **Local-first 记忆 = 算法摘要 + plain-text** |
| 2026-06-19 | launch-your-agent（OSS, Apache-2.0, 584⭐） | 同上 + 命令行 phase 管理 | **Harness-as-Skill：phase lifecycle** |
| 2026-07-01 | Claude Code v2.1.198（1st-party） | + Notification (agent_needs_input / agent_completed) | **官方 Lifecycle 事件面** |

**Recall 对 Claude Code 的反哺**：
- 证明了 `SessionStart/Stop/SessionEnd` hooks **真的能用**——不只是"实验性 API"
- 提供了 1 个**通用 hook 范式**："捕获 → 摘要 → 暴露"
- 给后续 hook 实践者（v2.1.198 Notification hook 用户）一个**直接参考的本地化模板**

---

## 六、3 件你立刻能做的事

### 6.1 如果你刚开始用 Claude Code：

```bash
# 加这个 plugin
git clone https://github.com/raiyanyahya/recall ~/.claude/plugins/recall

# 在你的项目根目录加一个 .recall 目录
mkdir .recall

# 在 .claude/settings.json 加 hooks
```

从此你再也不用重复解释项目背景。

### 6.2 如果你已经在维护自己的 memory 工具：

Recall 的 **TF-IDF + TextRank vendored 实现**是值得抄的——不用 LLM 也能做高质量 extractive summarization，token 成本 = 0。

### 6.3 如果你在等 v2.1.198 Notification hook：

Recall 已经把"hook-based memory"做成了一个完整的 reference impl。等 Notification hook 落地后，你的 `agent_completed` 触发器可以直接调用 Recall 的 summarizer：

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "agent_completed",
      "hooks": [{
        "type": "command",
        "command": "python ~/.claude/plugins/recall/scripts/summarizer.py"
      }]
    }]
  }
}
```

---

## 七、它和 Layer 6 Autonomous Delivery Harness 的关系

Recall 不是 Layer 6（自主交付层）的核心，但它是 **Layer 6 的"持久化伴侣"**：

| 维度 | Layer 6（v2.1.198） | Recall |
|------|---------------------|--------|
| 时间 | 即时（PR 完成时） | 跨 session（下次启动时） |
| 触发 | `agent_completed` event | `SessionStart` event |
| 产物 | draft PR + commit | context.md + history.md |
| 角色 | "交付" | "记忆" |

合起来就是 **Layer 6 + Memory Layer** = "Agent 不仅交付，还能记住自己交付过什么"。

> **金句**（Recall README，可独立传播）：*「Recall is `CLAUDE.md` for what you actually did — produced offline, with no model tokens spent.」*
> —— 这就是 Harness Engineering 从"配 prompt"到"配 memory"的拐点。

---

## 八、参考与引用

1. **Recall GitHub 仓库（MIT, 646⭐）** — `https://github.com/raiyanyahya/recall`
2. **Recall Summarizer 实现（vendored TextRank）** — `scripts/summarizer.py` in repo
3. **Claude Code Hooks 官方文档** — `https://code.claude.com/docs/en/hooks`
4. **Claude Code v2.1.198 Notification hook（官方 Lifecycle 事件面）** — `articles/ai-coding/claude-code-2-1-198-autonomous-delivery-harness-notification-hooks-2026.md`
5. **Looper（同样用 Hook 做 lifecycle 设计的项目）** — `articles/projects/ksimback-looper-claude-code-loop-design-coach-493-stars-2026.md`
6. **launch-your-agent（同样把 lifecycle 当 design surface 的项目）** — tracked in `.agent/sources_tracked.jsonl`

---

**📦 Pair Article**：本文（local-first memory + hook-based lifecycle）与 **`Claude Code v2.1.198 Autonomous Delivery Harness`**（Background Agent auto-PR + Notification hook）形成上下游关系——Recall 是 v2.1.198 之前用 hook 做 lifecycle 的开源参考实现，v2.1.198 是官方化。详见 `articles/ai-coding/claude-code-2-1-198-autonomous-delivery-harness-notification-hooks-2026.md`。