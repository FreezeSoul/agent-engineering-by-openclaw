# Cursor SDK 的工程三剑客：自定义工具 + Auto-review 分类器 + 嵌套 Subagent

> 本文深入分析 Cursor SDK 2026年6月更新的三个核心工程特性，揭示生产级 Agent 系统的关键架构设计。

## 核心命题

Cursor 在 2026年6月的 SDK 更新中，同时交付了三个工程突破：自定义工具的零配置 MCP 化、基于自然语言描述的权限分类器、以及 Subagent 的任意深度嵌套。这三个特性并非独立功能，而是共同构成了一套完整的生产级 Agent 工程框架——分别解决的是**工具集成**、**权限控制**和**任务分解**三个核心问题。

---

## 一、自定义工具：从 MCP 服务器到函数定义的降维

### 旧方案的痛苦

在 Cursor SDK 这次更新之前，如果你想把一个自定义能力暴露给 Agent，需要经历完整的 MCP 服务器搭建流程：定义 stdio 或 HTTP 传输协议、实现 JSON-RPC 接口、处理错误返回。这是合理的抽象，但也意味着"我想让 Agent 调用我的一个函数"这件简单的事，需要写一个独立的服务进程。

Cursor 团队显然注意到了这个杠杆点。

### 新方案：一行函数定义就够了

现在你只需要传入函数定义：

```typescript
const agent = new Agent({
  name: 'MyAgent',
  instructions: '...',
});

// 通过 local.customTools 注入自定义工具
const result = await agent.send(prompt, {
  local: {
    customTools: [
      {
        name: 'queryDatabase',
        description: 'Query the production database for metrics',
        parameters: {
          type: 'object',
          properties: {
            sql: { type: 'string', description: 'SQL query to execute' }
          },
          required: ['sql']
        }
      }
    ]
  }
});
```

这个函数定义被 Cursor SDK 暴露给 Agent 的方式，是一个内置的 MCP 服务器，名字叫 **`custom-user-tools`**。模型通过标准的 MCP 调用路径访问你的函数——这意味着你的自定义工具和任何一个外部 MCP 工具，走的是完全相同的权限 gate。

笔者认为，这是一个极其聪明的设计决策：**不是简化工具接入的协议，而是让最简单的接入方式走标准协议**。你不需要为"简单场景"发明一个新的轻量协议，因为 MCP 协议本身已经被广泛采用。

### 工具的级联可见性

还有一个细节值得注意：自定义工具对整个 Subagent 调用树可见。一个工具定义一次，在父 Agent 和所有子 Subagent 中都可以被调用。这解决了 Agent 系统中一个常见的工程问题——工具共享。

---

## 二、Auto-review 分类器：超越二元的权限决策

### 为什么二元权限不够用

传统的 Agent 权限模型是二元的：`allow` 或 `deny`。但现实远比这复杂。一个"删除操作"可能是：
- 删除 `./dist` 目录下的构建产物（完全无害）
- 删除 `./node_modules`（浪费资源但可恢复）
- 删除 `.env` 文件（灾难性）

如果你用简单的 allow/deny 来控制，第一种和最后一种被你迫不得已都标记为 allow，或者都 block。

### 分类器：自然语言描述的权限策略

Cursor 的解法是引入一个**分类器**，而不是一个规则引擎：

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

这个分类器读取 `allow_instructions` 和 `block_instructions` 中的自然语言描述，决定哪些工具调用自动执行、哪些需要人工确认。

这意味着你不需要精确描述规则，只需要描述意图。分类器理解"build artifacts under ./dist"是构建产物，理解"delete operations"需要暂停。

> "A classifier decides which calls run automatically and which to hold back, rather than bypassing review entirely."

笔者认为，这个设计最妙的地方在于它把权限控制的粒度，从"操作类型"提升到了"操作意图"。这与 Anthropic 在 Claude Code auto mode 中描述的"Harness 设计原则"一脉相承——**权限不是关于"能做什么"，而是关于"在什么上下文中做是合理的"**。

### 实际工作流

当你在本地运行 SDK Agent 时，默认行为是所有调用直接执行（因为没有人工在循环中）。启用 `autoReview` 后：

```
Tool Call → Classifier检查 → 自动执行 or 暂停等待确认
```

这个流程对开发者是完全透明的——你不需要写任何 if-else 逻辑，只需要配置 permissions.json。

---

## 三、嵌套 Subagent：自动级联的任务分解

### 从一层代理到任意深度

在之前的 SDK 版本中，你可以定义 Subagent，但 Subagent 不能再定义自己的 Subagent。这次更新解除了这个限制：

> "Subagents can now spawn their own subagents, and so on. A reviewer subagent can delegate to a test-writer, which can delegate further, with each level keeping its own prompt and model."

这意味着你可以构建这样的调用树：

```
Root Agent (Code Review)
  └── Subagent: Test Writer
        └── Subagent: Unit Test Generator
              └── Subagent: Assertion Helper
```

每个层级都有自己的 prompt 和模型配置。父 Agent 的 Test Writer 不需要知道 Unit Test Generator 是怎么工作的，它只需要把自己的输出传下去。

### 自动注册机制

实现的技术细节也很有意思——"There's nothing to turn on; a subagent session registers the executor it needs to call Task, so nesting works automatically for any agent that defines subagents."

每个 Subagent 会话在创建时，自动注册它需要的 executor。当你定义 Subagent 时，SDK 自动处理了嵌套的连接问题，开发者不需要手动管理调用树的深度。

笔者认为，这个设计体现了**自然延迟绑定**的工程原则：父 Agent 说"我需要有人帮我写测试"，它不需要指定是谁来写、那个人又需要谁帮忙——这些决策在子层级自行解决。

---

## 四、JSONL Store：状态持久化的范式转换

虽然这个特性在 Changefeed 中被放在最后，但它对生产环境有深远影响。

### SQLite → JSONL

之前的 SDK 用 SQLite 存储 Agent 和 Run 的元数据。这次你可以选择 JSONL Store：

```typescript
import { JsonlLocalAgentStore } from '@openai/agents';

// 使用 JSONL 而不是 SQLite
const store = new JsonlLocalAgentStore('./agent-runs.jsonl');
```

JSONL 是 append-only 的，每一行是一个完整的 JSON 对象。你可以：
- 直接 `cat` 查看运行记录
- 用 `diff` 比较两次运行的差异
- 把运行记录 `git commit` 进版本控制

这解决了一个实际问题：当 Agent 的决策过程需要被审计时，SQLite 的二进制格式是一个黑盒，而 JSONL 是完全透明的。

### 自定义 Store 接口

更进一步的，你可以实现 `LocalAgentStore` 接口来使用任何后端：

> "Build an in-memory store for ephemeral CI runs, or back persistence with Postgres when you want agent state to live next to the rest of your application data."

CI 环境用内存存储（不需要持久化），生产环境用 Postgres（需要和其他应用状态一起管理）。同一个接口，两种部署场景。

---

## 五、工程关联：从工具到系统

### 与 Round352 的 Eval Awareness 形成呼应

在 Round352 中，我们分析了 Anthropic 的"评测感知"现象——模型能够识别自己正在被评测，从而可能调整行为。Cursor 的 Auto-review 分类器提供了一种工程对冲：不是试图阻止模型识别评测环境，而是让权限策略足够细粒度，使得即使模型"知道了"，也无法绕过核心安全边界。

### Custom Tools 与 MCP 的演进

笔者认为，Cursor 的 custom-user-tools MCP 服务器，代表了一种 MCP 的**内部化**趋势：协议还是那个协议，但服务器不再需要是独立进程。当工具数量少、信任边界清晰时，把 MCP 服务器嵌入 SDK 运行时，是合理的工程取舍。

### 嵌套 Subagent 与任务分解范式

多层嵌套的 Subagent，本质上是一种**树状任务分解**。与单层 Agent 相比，它支持更复杂的工作流程，但也带来了新的问题：调用深度的可视化、错误传播的路径、超时和取消的级联。这些是下轮可以继续追踪的工程问题。

---

## 总结：三个特性，一个框架

Cursor SDK 这次更新的三个特性，回答了三个不同的工程问题：

| 特性 | 解决的工程问题 | 核心设计决策 |
|------|--------------|------------|
| Custom Tools | 工具集成的复杂度 | 内置 MCP 服务器，函数定义即接入 |
| Auto-review Classifier | 权限控制的粒度 | 自然语言描述的分类器，而非规则引擎 |
| Nested Subagents | 任务的层次化分解 | 自动级联注册，每个层级独立配置 |
| JSONL Store | 状态持久化的灵活性 | Append-only 文件，支持版本控制 |

这四个特性组合在一起，构成了一套适合生产环境的 Agent 工程框架。不需要 2024 年的 LangChain heavy-weight，也不需要复杂的外部编排——SDK 内置了工具接入、安全分类、任务分解和状态管理的完整能力。

---

## 备选标题

1. **Cursor SDK 三特性：重新定义生产级 Agent 工程框架** — 策略：价值概括（28单位）
2. **Custom Tools + Auto-review + 嵌套 Subagent：Cursor SDK 的工程突破** — 策略：特性清单（32单位，超限需优化）
3. **一个函数定义就够了：Cursor SDK 的零配置 MCP 化设计** — 策略：痛点共鸣（28单位）

---

**引用来源**：
- Cursor Changelog: "Custom stores, custom tools, and auto-review for the Cursor SDK" (2026-06) — https://cursor.com/changelog/sdk-updates-jun-2026
- Cursor Documentation: Auto-review — https://cursor.com/docs/agent/tools/terminal#run-mode
- Cursor Documentation: permissions.json — https://cursor.com/docs/reference/permissions
- Anthropic Engineering: "How we built Claude Code auto mode" (2026-03) — https://anthropic.com/engineering/claude-code-auto-mode