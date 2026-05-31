# Cursor 3.6 Auto-review：三层过滤的 Agent 权限架构

> Auto-review Run Mode 将 Shell/MCP/Fetch 工具调用路由经三层过滤（Allowlist → Sandbox → Classifier Subagent），实现更长的无人值守运行，同时保留安全边界。

**来源**：[Cursor Changelog - Auto-review Run Mode](https://cursor.com/changelog/auto-review)，2026年5月29日（3.6版本）

---

## 背景：权限模式的演进问题

Cursor 在3.6 之前提供两种权限模式：**Yolo**（直接运行）和 **Auto**（逐个确认）。两者都有明显缺陷：

- **Yolo**：安全事件已有公开记录，任何工具调用都不经审核，在团队环境中不可接受
- **Auto**：每个 Shell 命令都要点一次确认，多步骤任务变成了「批准马拉松」，开发者很快学会无视弹窗

这个两极之间的空白，就是 Auto-review 要填补的位置。

---

## 三层过滤架构

Auto-review 将工具调用路由分三个阶段处理：

### 第一层：Allowlist（立即执行）

预定义的白名单规则匹配后直接放行，无需任何模型调用。示例：
- `shell commands that only read files, run linters, or run the test suite`
- 文件读取、格式化命令、类型检查

这是**最便宜且最可预测**的信号——零模型调用延迟，行为完全确定。

### 第二层：Sandbox（沙箱执行）

无法直接 Allowlist 但可沙箱化的调用，在隔离环境里执行。Shell 类型的调用如果可以限制网络/文件系统权限，就走这层。

这是 Cursor 的架构优势：跨平台的 Agent 沙箱已经内置，Auto-review 把它变成了权限路由的一站。

### 第三层：Classifier Subagent（分类子 Agent）

Allowlist 和 Sandbox 都不适用时，调用进入一个专门的**分类子 Agent**——一个规模较小的模型实例，输入是：

1. 项目的 `.cursor/permissions.json`（`allow_instructions` + `block_instructions`）
2. 用户自定义的 `custom instructions`
3. 当前工具调用的上下文（工具名、参数、环境）

输出是三种决策之一：**Allow** / **Try different approach** / **Escalate to user approval**。

```
┌─────────────────────────────────────────────┐
│ Tool Call Incoming │
└──────────────────┬──────────────────────────┘
                   ▼
         ┌────────────────────┐
         │  1. Allowlist Check │ ← 静态规则，零延迟
         └────────┬───────────┘
                  ▼ (no match)
         ┌────────────────────┐
         │ 2. Sandbox Try │ ← 可沙箱化则执行
         └────────┬───────────┘
                  ▼ (cannot sandbox)
         ┌────────────────────┐
         │ 3. Classifier Agent│ ← 小模型判断
         │ (项目规则+上下文) │ Allow / Retry / Escalate
         └────────────────────┘
```

---

## 权限配置：`.cursor/permissions.json`

Auto-review 的核心配置是一个项目级权限文件：

```json
{
  "allow_instructions": "shell commands that only read files, run linters, or run the test suite are fine to run without asking",
  "block_instructions": "any shell call that mutates the database, sets environment variables, or writes to .env must ask for approval"
}
```

笔者认为这里有个设计上的微妙之处：**允许规则是自然语言描述，而不是正则表达式列表**。这意味着：
1. 规则更易读，团队成员都能维护
2. 分类器需要理解语义，不能靠字符串匹配
3. 误判率比静态列表高，但正确率对于「明显安全/明显危险」之外的调用已经足够好

---

## MCP 工具调用：被低估的覆盖范围

Auto-review 覆盖三类调用：**Shell、MCP、Fetch**。其中 MCP 工具调用最容易被忽略。

当前 Cursor 连接 MCP 服务器的数量持续增长，每个 MCP 服务器都可能对数据库、计费系统、或任何外部服务执行有状态操作。Auto-review 把 MCP 纳入三层过滤，意味着**数据库 mutation 调用也需要经过分类器判断**。

这是和 Claude Code 权限模型的一个显著差异：Claude Code 的 Allowlist 主要是静态的 `acceptEdits` / `auto` / `dontAsk` 模式配置，而 Cursor Auto-review 在静态规则之上叠加了一个动态分类层。

---

## 与其他 Agent 权限模式的对比

| Agent | 权限模式 | 关键差异 |
|-------|---------|---------|
| **Cursor3.6 Auto-review** | Allowlist + Sandbox + Classifier Subagent | 三层过滤，动态分类，适用 Shell/MCP/Fetch |
| **Cursor (older) Auto** | 逐个确认 | 每步都停，开发者疲劳 |
| **Claude Code** | allow/auto/edits/bypassPermissions 静态配置 | 规则是静态的，无动态分类层 |
| **OpenAI Codex CLI** | Named permission profiles | 命名配置，但仍是静态规则 |
| **Cline** | auto-approve list | 简单的静态 Allowlist |

---

## 局限与适用边界

Cursor 官方明确说明：

> *"The classifier is non-deterministic and can make mistakes in both directions, so treat Auto-review as best-effort convenience, not a security boundary."*

这个声明非常重要。Auto-review 的定位是**减少 approval fatigue**，而不是提供生产级安全边界。以下场景**不应该**使用 Auto-review：

- 生产凭证环境
- 有状态 mutation 的 MCP 服务器
- 不可逆操作可能造成不可接受损失的环境

适用场景：
- 个人开发分支或沙箱项目
- MCP 服务器限制为只读（文档、搜索、内部 Wiki）
- Fetch 工具限制为小范围已批准主机
- 代码可通过 code review 捕获错误（有 Diff 可审查）

---

## 工程意义

笔者认为 Auto-review 的工程意义在于它揭示了一个行业趋势：**Agent 权限控制正在从「配置驱动」向「模型驱动」演进**。

静态 Allowlist 的问题是列表要么太大（不安全）要么太小（太烦人）。而模型驱动的分类可以在语义层面做判断，理解「这个 git commit 只改了测试文件所以可以自动通过」和「这个 rm -rf 是在删除 node_modules 所以必须问」之间的差别。

当然，模型驱动的分类器目前还做不到完全可靠。但对于**受信任的开发环境**，Auto-review 提供了一个合理的中间地带——让规则覆盖80% 的明显安全调用，用沙箱覆盖 15% 的可隔离风险，剩下 5% 交给分类器和人工判断。

---

## 引用

> *"Auto-review is a new run mode that allows Cursor to work for longer with fewer approval prompts and safer execution. Auto-review applies to Shell, MCP, and Fetch tool calls. Allowlisted calls run immediately, and calls that can be sandboxed run in the sandbox. All other agent actions go to a classifier subagent that decides whether to allow the call, try a different approach, or ask for your approval."*

— [Cursor Changelog - Auto-review Run Mode](https://cursor.com/changelog/auto-review)，2026年5月29日

---

##关联阅读

- [Cursor Auto-review Run Mode in 2026: What It Does, How It Compares, and When to Trust It](https://www.totalum.app/blog/cursor-auto-review-totalum)（第三方分析，含与 Claude Code/Codex 权限模式对比）
- [Cursor 3.6 — Auto-review reduces 'y-spamming' but is not a security boundary](https://note.com/marusho_1266/n/nf4845bd739b3)（日文分析）
- [Anthropic Claude Code 权限架构](../harness/anthropic-claude-code-auto-mode-two-layer-security-architecture-2026.md)——三层分类 vs静态配置的对比分析