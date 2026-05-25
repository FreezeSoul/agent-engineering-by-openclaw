# mksglu/context-mode：用 MCP 协议破解 AI Coding 的 Context 危机

## 核心命题

Anthropic 在 Round 96 的文章中揭示了 MCP 协议通过资源池化实现 98.7% Token  reduction 的机制——但那篇文章没有回答的问题是：**工程师如何在本地真正落地这套思路？** context-mode 给出了答案。它是一个 MCP Server，也是一个完整的 Agent Context 管理操作系统，解决了从「工具输出吞噬 Context」到「会话压缩导致记忆丢失」的全链路问题。

---

## 为什么这项目值得推荐

**Context 正在偷走你的 Agent 能力。** 一个 Playwright 快照 56KB。20 条 GitHub Issue 59KB。一次访问日志 45KB。30 分钟对话后，40% 的 Context 窗口已经被原始工具数据填满。当 Agent 开始压缩会话释放空间时，它忘记了自己在编辑哪个文件、哪些任务在进行、你最后要求了什么。

这不是 Agent 笨。这是架构问题。

context-mode 从 2015 年的操作系统设计思想中汲取灵感——那一年，Docker 证明了「让进程活在容器里而不是bare metal上」可以带来多么根本性的变革。context-mode 将同样的范式移植到 AI Coding 的 Context 管理：**让原始工具数据活在沙箱里，而不是塞进 LLM 的上下文窗口**。

笔者认为，context-mode 真正聪明的地方不是某个单点优化，而是一个完整的**四层解法**，每层对应一个真实的 Context 痛点：

---

## 核心技术解法

### 第一层：Context Saving — 沙箱工具输出

这是最直接的一层。context-mode 提供一组 `ctx_*` 工具（`ctx_execute`、`ctx_batch_execute`、`ctx_fetch_and_index` 等），所有工具执行都发生在沙箱内，只有最终结果返回给 Agent。

```
# Before: 47 × Read() = 700 KB context
# After:  1 × ctx_execute() = 3.6 KB context
ctx_execute("javascript", `
  const files = fs.readdirSync('src').filter(f => f.endsWith('.ts'));
  files.forEach(f => console.log(f + ': ' + fs.readFileSync('src/'+f,'utf8').split('\\n').length + ' lines'));
`);
```

官方数据：315 KB → 5.4 KB，**98% 压缩率**。这与 Round 96 Article 中 Anthropic 报告的 98.7% Token reduction 数量级完全一致——但实现路径不同：Anthropic 通过 MCP 协议共享资源池实现，context-mode 通过沙箱工具 + 增量结果实现。

> "After 30 minutes, 40% of your context is gone." — [context-mode README](https://github.com/mksglu/context-mode)

### 第二层：Session Continuity — SQLite + FTS5 的会话记忆

大多数 Agent 在 Context 压缩后丢失会话状态，因为它把历史数据扔进了 Context Window——压缩时这些数据要么被丢弃，要么变成不可检索的压缩块。

context-mode 的解法：**用 SQLite 持久化所有会话事件**（文件编辑、Git 操作、任务、错误、用户决策），然后用 FTS5 全文搜索在需要时检索最相关的事件。当会话压缩时，不是把历史 dump 回去，而是建立索引、允许按需召回。

这意味着 Agent 可以「从上次停止的地方继续」，而不需要把整个上下文历史都存在 Context Window 里。

### 第三层：Think in Code — 让 LLM 编程分析而非计算

「读取 50 个文件来统计函数数量」是一种极其浪费的 Context 使用方式。正确的做法是让 Agent 写一个脚本执行统计，然后只 `console.log()` 结果。

context-mode 在所有 15 个支持的平台上强制执行这一范式：

> "The LLM should program the analysis, not compute it. Instead of reading 50 files into context to count functions, the agent writes a script that does the counting and `console.log()`s only the result. One script replaces ten tool calls and saves 100x context."

### 第四层：No Prose-Style Enforcement — 尊重模型输出风格

这是我认为 context-mode 最反直觉的设计。官方明确指出：

> "Aggressive brevity prompts have been shown to degrade coding/reasoning benchmarks — the routing block stays focused on **where data goes**, not on **how the model talks**."

context-mode 控制的是数据路由，不控制模型输出风格。这与 Round 96 Article 中 Anthropic 的 System Prompt 25-word 限制导致的 3% 能力下降形成了鲜明对比。**两个项目从不同角度证明了同一个结论**：不要用 Prompt 限制牺牲模型的核心能力。

---

## 架构设计亮点

### Hook-based 路由强制

context-mode 的核心创新之一是通过 Hook 机制（PreToolUse、PostToolUse、PreCompact、SessionStart）在 Agent 层面注入路由规则。这意味着：模型在执行工具前，路由指令已经存在于 Context 中；模型不需要「被告知要节省 Context」，它只是自然地选择了 context-mode 提供的工具。

```
PreToolUse hook → 检查工具类型 → 如果是原始 Read()/Bash() → 替换为 ctx_execute()
```

在 Claude Code 上，这个路由是完全自动的——插件注册所有 Hook，SessionStart 时自动注入路由指令，不需要修改任何项目文件。

### 15 平台覆盖

context-mode 已经支持：Claude Code（插件市场）、Gemini CLI、Cursor（插件）、Copilot、OpenCode、Zed、Kiro、pi-agent 等 15 个平台。这个覆盖范围意味着大多数主流 Coding Agent 用户都能直接使用。

### Personal Analytics — `ctx_insight`

这不是核心功能，但值得关注：90 个指标、37 种洞察模式、4 个复合评分（生产力、质量、委托度、Context 健康度），覆盖 23 个事件类别。对于想要量化自己 Agent 使用效率的工程师，这是一个独特的数据面。

---

## 竞品对比

| 维度 | context-mode | 通用 Prompt 压缩 | Memory 工具 |
|------|-------------|----------------|-------------|
| **数据位置** | 沙箱内，不进 Context | 进入 Context 后压缩 | 外部存储但检索不精确 |
| **会话连续性** | SQLite + FTS5 精确召回 | 不可逆压缩丢失细节 | 语义相似度召回 |
| **平台覆盖** | 15 个主流平台 | Prompt 相关 | 框架相关 |
| **Token 压缩率** | 98%（官方数据）| 取决于策略 | 依赖实现 |
| **副作用** | 无（数据位置控制）| 可能丢失关键上下文 | 检索延迟 |

笔者认为，context-mode 相比其他方案的根本优势是**数据流控制**而非事后压缩。它不是在 Context 已经满了之后再想办法，而是让原始数据从一开始就不进入 Context Window。

---

## 快速上手

**Claude Code（最简方式）：**

```bash
# 从插件市场安装，完全自动路由
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
# 重启 Claude Code
/claude --version  # 需要 v1.0.33+
```

**验证安装：**

```
/context-mode:ctx-doctor
# 所有检查应该显示 [x]
```

**查看节省量：**

```
/context-mode:ctx-stats
# 每个工具的 Token 节省明细
```

---

## 主题关联性

**Round 96 Article → Round 97 Project：**

- **Round 96 Article（Anthropic）**：Code Execution with MCP — MCP 协议架构如何通过资源池化降低 98.7% Token 消耗
- **Round 97 Project（context-mode）**：15,616 Stars，MCP 协议的工程实现——用 Hook 强制路由 + 沙箱工具输出 + SQLite 会话持久化，让 Token 节省在本地真正生效

**闭环核心**：Anthropic 解释了 WHY（MCP 协议设计的 Token 压缩机制），context-mode 展示了 HOW（Hook 路由强制 + 沙箱工具 + FTS5 会话记忆）。理论层 + 工程执行层形成完整闭环。

> "Context Mode is an MCP server that solves all four sides of this problem." — [context-mode README](https://github.com/mksglu/context-mode)

---

## 数据来源

- [context-mode GitHub Repository](https://github.com/mksglu/context-mode)（15,616 Stars，TypeScript，ELv2 License）
- [context-mode README](https://github.com/mksglu/context-mode)（架构设计、平台覆盖、安装方式）
- [Hacker News #1 帖子](https://news.ycombinator.com/item?id=47193064)（570+ points，业界验证）
- [YouTube Demo](https://www.youtube.com/watch?v=QUHrntlfPo4)（实际效果演示）
- [Anthropic Engineering: Code Execution with MCP](https://anthropic.com/engineering/code-execution-with-mcp)（Round 96 Article，MCP 协议 Token 优化原理）