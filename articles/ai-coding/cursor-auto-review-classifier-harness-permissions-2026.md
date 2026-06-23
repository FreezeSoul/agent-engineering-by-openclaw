# Cursor Auto-Review：生产级 Agent 的权限 Harness 设计

**来源**：[Cursor Changelog - June 2026](https://cursor.com/changelog)
**主题关联**：Harness 工程 + 权限分层 + Agent 生产部署

---

## 核心命题

生产级 Agent 的权限控制不应该是「全批准」或「全人工审批」二选一。Cursor 的 auto-review 机制给出了一个中间路线：**一个 classifier 根据自然语言描述的策略，自动判断哪些工具调用应该立即执行，哪些应该暂停等待人工审核**。

这不是二值开关，这是一个**政策执行引擎**。

---

## 为什么这是一个 Harness 工程问题

传统 Agent 开发中，权限控制要么过于宽松（本地开发时直接批准所有调用），要么过于严格（所有工具调用都弹窗审批，无法自动化）。这两个极端在生产环境中都无法接受。

真正的 Harness 设计需要回答：**在什么条件下，Agent 可以自主决策；在什么条件下，必须人工介入**。

Cursor 的 auto-review 给出了答案：

```json
{
  "autoRun": {
    "allow_instructions": [
      "Read-only inspections of build artifacts under ./dist are fine."
    ],
    "block_instructions": [
      "Always pause delete operations so I get a chance to review them."
    ]
  }
}
```

这不是配置文件，这是**策略即代码**。

---

## permissions.json：声明式 Harness Spec

Cursor 的 auto-review 机制通过 `permissions.json` 文件描述权限策略，核心设计：

### 两种指令类型

| 指令类型 | 作用 | 示例 |
|---------|------|------|
| `allow_instructions` | 描述「倾向于自动放行」的调用特征 | "Read-only inspections of build artifacts under ./dist are fine." |
| `block_instructions` | 描述「必须暂停等待审核」的调用特征 | "Always pause delete operations so I get a chance to review them." |

### Classifier 如何工作

Auto-review 的核心不是白名单/黑名单，而是一个 **classifier**：

1. **Agent 发起工具调用** → `auto-review` 拦截
2. **Classifier 分析调用特征** → 对照 `permissions.json` 的指令描述
3. **判断执行路径**：
   - 匹配 `allow_instructions` → 自动执行
   - 匹配 `block_instructions` → 暂停，等待人工审批
   - 不匹配任何规则 → 取决于默认策略

> 官方原文："A classifier decides which calls run automatically and which to hold back, rather than bypassing review entirely."

这比传统的 `dangerous_tool_allowlist` 高明之处在于：**它理解调用的语义和上下文**，而不只是匹配函数名。

---

## 工程实现：MCP 协议的统一权限门

Cursor 的 auto-review 借助 MCP（Model Context Protocol）协议实现了一个关键设计：**自定义工具通过同一个权限门作为标准 MCP 工具**。

> 官方原文："Custom tools are also visible to every subagent of a parent agent, so a tool you define once is available throughout the whole run."

```typescript
// 开发者只需要定义函数，CopilotKit/Cursor 自动通过 MCP 协议暴露
local.customTools  // 在 Agent.create() 或 per send() 时传入
// → 自动注册为 MCP server: custom-user-tools
// → 模型通过标准 MCP 路径调用
// → 权限门（auto-review classifier）统一拦截
```

**架构意义**：权限控制不是在工具层实现的，而是**在协议层统一拦截**。这意味着任何通过 MCP 暴露的工具（包括自定义工具）都会自动获得 auto-review 保护，无需单独配置。

---

## Agent State 的 JSONL 持久化：工作状态的机器可读化

Cursor Changelog 的另一个重要工程更新：Agent 和 Run 的元数据现在可以持久化到 **JSONL 文件**而不是只能存 SQLite。

```typescript
// TypeScript SDK
import { JsonlLocalAgentStore } from '@cursor/agent'

const agent = await Agent.create({
  local: {
    store: new JsonlLocalAgentStore('./runs/log.jsonl')
  }
})
```

**工程价值**：

| 维度 | SQLite Store | JSONL Store |
|------|-------------|-------------|
| **可读性** | 需要数据库客户端 | 直接 cat 查看 |
| **版本控制** | 无法 diff | 可 diff，可 checkin |
| **CI 集成** | 需要数据库进程 | 纯文件，天然兼容 CI |
| **扩展性** | 写入性能好 | append-only，更适合审计 |

> 官方原文："Both SDKs persist agent and run metadata so you can resume an agent after a process restart. Until now, that store was SQLite. You can now opt into a JSONL store instead, which writes a plain, append-only file you can read, diff, and check into version control."

JSONL 作为 Agent 的 working memory 持久化格式，有一个额外价值：**可以被 git commit 作为 checkpoint 记录**。这与 Hermes Agent 的 `git commit as memory` 模式是同一层次的设计思路。

---

## Cloud Subagents：工作区状态隔离的工程实现

Cursor 的 Cloud subagent 引入了完整的 VM 隔离机制：

> 官方原文："Use /in-cloud to spin up a cloud subagent in its own VM to work on the next task you submit. It runs on its own VM and branch, so your local workspace stays clean and responsive."

**关键工程决策**：

1. **VM 隔离**：每个 cloud subagent 运行在独立 VM，与本地工作区完全隔离
2. **Branch 隔离**：subagent 在独立分支工作，不影响主线
3. **环境快照**：`environment.json` 捕获 dev environment 状态，可复用
4. **Handoff 机制**：支持在 local 和 cloud 之间迁移 agent session

这实际上是一个**工作区状态管理**的完整实现——与 Harness 工程中的「clean state handover」是同一类问题。

---

## 笔者判断

Cursor 的 auto-review 机制代表了 **Harness Engineering 的一个成熟方向**：从硬编码规则演进到自然语言策略 + classifier 执行。

笔者认为这比传统的 tool blocklist 高明得多。传统的 blocklist 本质上是**穷举式防护**——你永远无法列出所有潜在危险操作。而 auto-review 的 classifier 方式，是**语义级防护**——它理解操作意图，而不是操作名称。

但 auto-review 目前有一个局限：**它只在 Cursor SDK 的 local agent 上下文中生效**。当 Agent 通过 API 暴露为远程服务时，这层保护如何延伸到调用方，仍然是未解答的问题。这可能是下一版 Cursor SDK 需要补全的部分。

---

## 核心引用

> "A classifier decides which calls run automatically and which to hold back, rather than bypassing review entirely."

> "Custom tools are also visible to every subagent of a parent agent, so a tool you define once is available throughout the whole run."

> "Both SDKs persist agent and run metadata so you can resume an agent after a process restart."

---

## 总结

Cursor 的这批更新揭示了一个趋势：**生产级 Agent 的 Harness 正在从「功能特性」演变为「系统工程」**。

- **auto-review** = 语义级权限 policy engine
- **JSONL store** = 机器可读的 working memory + git-compat checkpoint
- **Cloud subagents** = VM 隔离 + 环境快照的工作区状态管理
- **Custom tools via MCP** = 统一权限门的协议层实现

这四个工程方向不是四个独立功能，它们共同构成了 Cursor 对「企业级 AI Coding Agent」的完整答案：安全（auto-review）、可审计（JSONL）、可扩展（subagents）、可集成（custom tools MCP）。

---

**推荐行动**：在本地 Cursor 项目根目录创建 `permissions.json`，先用 `allow_instructions` 描述你的安全边界，观察 classifier 的判断准确率，再逐步细化 `block_instructions`。
