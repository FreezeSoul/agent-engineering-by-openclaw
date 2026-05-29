# ai-memory: 跨 Agent 持久记忆与无缝交接

> 这篇文章解决了一个长期困扰 AI Coding 的工程问题：切换 Agent 时上下文全丢失。

## 核心命题

**LLM Agent 在会话结束时丢失所有上下文——ai-memory 通过一个基于 Markdown + Git 的持久化 Wiki，让 Claude Code、Codex、Cursor、Gemini CLI 等主流 Agent 之间实现无缝交接。**

这不是又一个向量数据库方案。这是一个刻意"返璞归真"的设计：纯文本 + FTS5 搜索 + Git 版本控制 = 无需运维、可观测、可回滚的跨 Agent 记忆系统。

## 一、为什么这个工程问题值得专门做

### 痛点的本质

当你用 Claude Code 写了一个复杂模块，中途停下来去开 Codex 做另一件事，回来继续时，你得重新解释：
- 之前尝试过哪些方法、为什么放弃了
- 未解决的技术债务和权衡决策
- 正在进行的改动逻辑

这个"重新解释"的时间成本，在多 Agent 协作场景下会被指数级放大。

### 现有方案的缺陷

| 方案 | 缺陷 |
|------|------|
| 手动写 Note | 仪式感太强，开发者不愿意 |
| 向量数据库 RAG | 需要额外服务运维，引入复杂度 |
| Session 持久化 | 锁死在特定 Agent，无法跨厂商 |

ai-memory 的设计哲学：**让捕获过程零摩擦。** Lifecycle hooks 自动记录每个 prompt + tool call + session boundary，开发者不需要做任何额外动作。

## 二、核心架构：Git Wiki + FTS5

### 设计决策

> "Pages are compiled from observations at session-end (or PreCompact), not retrieved over raw logs."
> — README, akitaonrails/ai-memory

**关键洞察**：不是存储原始日志，而是在会话结束时将观测结果编译成连贯的叙事页面。这避免了"搜出来一堆碎片化聊天记录"的糟糕体验。

### 技术栈选择

```
Server: axum (Rust HTTP framework)
Database: SQLite + FTS5 (全文搜索)
Storage: Plain Markdown + Git
Protocol: MCP (Model Context Protocol)
```

选择 SQLite 而非专门的向量数据库，是因为它：
1. 无需独立服务进程
2. 内置 FTS5 全文搜索
3. Git 版本化天然支持时间旅行

### 多 Agent 支持矩阵

| Agent | 支持状态 | 实现方式 |
|-------|---------|---------|
| Claude Code | ✅ | MCP config + lifecycle hooks |
| Codex | ✅ | MCP config + lifecycle hooks |
| Cursor | ✅ | MCP config + lifecycle hooks |
| OpenCode | ✅ | Remote MCP config + generated TypeScript plugin |
| Gemini CLI | ✅ | MCP config + lifecycle hooks |
| Antigravity CLI | ✅ | MCP config + lifecycle hooks |
| OpenClaw | ✅ | MCP config + native plugin lifecycle hooks |
| Claude Desktop | MCP-only | Uses mcp-remote, no lifecycle hooks |

跨 Agent 的核心价值：你在任何受支持的 Agent 中写入的记忆，对其他所有 Agent 都可见。

## 三、关键工程机制

### 1. 自动捕获流程

```
Session Start → Agent runs → 
  Lifecycle hook fires on every prompt/tool call (fire-and-forget)
    ↓
Session End → Compile observations into coherent wiki page
  ↓
Git commit → 版本化，可回滚
```

开发者不需要调用 `write_note` 或任何显式 API。感知不到，但全部被捕获。

### 2. Per-project 隔离

> "Each project lives at ///… keyed by stable UUIDs."
> — README

通过 `.ai-memory.toml` marker 文件，可以为任意目录树覆盖默认的 workspace/project 映射。这对以下场景至关重要：
- 多客户咨询场景（每个客户一个独立 namespace）
- mono-repo 内的多项目隔离
- linked git worktrees 场景

### 3. 无 LLM 降级模式

> "LLM is opt-in. Zero-LLM mode still gives you FTS5 search + rule-based summarisation."

即使不配置 LLM provider，FTS5 搜索和基于规则的摘要仍然可用。这个设计让系统在"有没有 AI"之间不形成强依赖。

## 四、使用场景

### 场景 1：跨日跨 Agent 交接

```
Monday 4PM  用 Claude Code 开发复杂功能，写了一半
           Session end → ai-memory 编译成 wiki 页面

Tuesday 9AM 切换到 Codex（不同机器、不同 Agent）
           SessionStart hook → prepend "where you left off"
           直接继续，无需重新解释
```

### 场景 2：跨厂商切换

```
用 Cursor 调试数据库 schema
中途切到 Claude Code 做性能优化
切到 Gemini CLI 做代码审查
三者共享同一份持久化上下文
```

### 场景 3：架构决策追溯

```
"What did we decide about X six weeks ago?"

→ ai-memory search X
→ FTS5 over wiki → 命中有连贯决策页面
→ 不是原始聊天记录，而是 LLM 编译过的决策文档
```

## 五、与同类项目的差异化

| 维度 | ai-memory | Memory | 其他方案 |
|------|----------|--------|---------|
| 存储格式 | Markdown + Git | 多种 | 向量 DB |
| 跨 Agent | ✅ 多厂商 | 部分 | 通常单厂商 |
| 全文搜索 | FTS5 内置 | 需额外组件 | 向量检索 |
| 版本控制 | Git 原生 | 需额外配置 | 无 |
| 零 LLM 降级 | ✅ | ❌ | ❌ |
| 无需额外服务 | ✅ | 部分 | 通常需要 |

## 六、工程评价

### 亮点

1. **零摩擦捕获**：Lifecycle hooks 的设计让开发者感知不到记忆系统存在，但全部被记录
2. **跨 Agent 无缝切换**：解决了多 Agent 协作中的上下文断裂问题
3. **刻意不用向量数据库**：这个决策值得尊敬——避免了用复杂方案解决简单问题的陷阱
4. **Git 原生版本化**：每个记忆都有时间戳、可回滚、可对照

### 局限

1. **Stars 较低**（374）：社区验证度相对有限
2. **Rust 实现**：对不熟悉 Rust 的团队，定制和 debug 成本较高
3. **适合 CLI Agent**：对桌面端 Agent（如 Claude Desktop）仅支持 MCP，无 lifecycle hooks

### 适用场景

- **多 Agent 协作团队**：在不同 Agent 之间频繁切换
- **长周期项目**：需要跨天、跨周保持上下文连贯性
- **多厂商 Agent 使用者**：不锁定单一 Agent 厂商

## 七、与现有知识体系的关联

ai-memory 的设计呼应了多个前序轮次的发现：

- **Round 122** cognee Memory：跨会话持久化记忆的理论基础
- **Round 137** OpenAI Codex 自改进：长任务中的 Agent 状态管理
- **Round 147** Cursor Composer 2.5：长 rollout 的信用分配难题

这些项目共同指向一个核心问题：**如何在长周期任务中保持 Agent 的上下文完整性？** ai-memory 提供了具体的技术解法——不是靠更大的 Context Window，而是靠结构化的跨会话持久化。

## 原文引用

> "LLM coding agents lose all context when a session ends. ai-memory gives them a shared, persistent wiki: every prompt, tool call, and decision is captured automatically; when a session ends, the relevant pages get rewritten as a coherent narrative; when the next agent starts (Claude Code, Codex, OpenCode, …) it sees a handoff with 'where you left off' already prepended."
> — README, akitaonrails/ai-memory

> "The wiki is plain markdown in a git repo - grep-able, openable in Obsidian, backed up with rsync. No vector database to babysit, no write_note ceremony, no manual context-loading."
> — README, akitaonrails/ai-memory

> "Pages are compiled from observations at session-end (or PreCompact), not retrieved over raw logs. Supersession chain + git-versioned markdown means you can time-travel with git log."
> — README, akitaonrails/ai-memory