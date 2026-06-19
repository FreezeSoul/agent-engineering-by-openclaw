# Agent-Native：重新定义 Agent 与应用的关系

> 本文首次提出 **Agent-Native** 范式：Agent 与 UI 是同一系统的平等公民，而非 Agent 孤零零地挂在应用旁边。

---

## 核心观点

**大多数人在构建 AI 应用时犯了一个根本性错误：把 Agent 和 UI 当成两个独立系统，然后用 API 把它们粘在一起。**

真正的范式转变是：**让 Agent 和 UI 共享同一个应用模型——Actions、状态、权限全部对等**。如果 UI 能做到，Agent 也能做到；如果 Agent 能做到，UI 也能做到。

---

## 背景：三个阶段的演化

回顾 AI 应用构建的历史，我们经历了三个阶段：

### 第一阶段：LLM 调用

```javascript
// 这是起点，但远远不够
const output = await llm(prompt)
```

没有工具，没有循环，没有反馈机制。LLM 只是一个更聪明的函数。

### 第二阶段：工具 + 循环

```javascript
// 给 LLM 工具，让它循环执行
const tools = [draftEmail, searchEmails, sendEmail]
// LLM → 工具调用 → 结果 → LLM → ... 直到完成
```

这是当前主流范式。Agent 有工具了，但仍然是一个黑盒，应用不知道 Agent 在做什么。

### 第三阶段：UI 集成 + 反馈

在工具循环的基础上加入 UI：流式输出、用户可以打断、可以给反馈。这是 Claude Code、Cursor 等产品的形态。

但这里仍然有一个根本问题：**Agent 和 UI 是两套独立的系统，用 API 连接在一起**。按钮触发的是 Agent，不是同一个动作。

---

## Agent-Native 的核心设计

Agent-Native 的出现，源于一个观察：

> 如果你的应用本质上是一组操作的集合，那么**定义一次 Action，就同时定义了 Agent 能做什么和 UI 能做什么**。

### 核心原则：Actions 是原语

```javascript
// 一个 Action，两种使用方式
export default defineAction({
  schema: z.object({
    emailId: z.string(),
    body: z.string(),
  }),
  run: async ({ emailId, body }) => {
    await db.insert(replies).values({ emailId, body });
  },
});
```

这个 Action：
- **UI 层**：用户点击"回复"按钮时触发
- **Agent 层**：Agent 在对话中决定"需要回复这封邮件"时触发
- **API 层**：外部系统通过 HTTP 调用
- **MCP/A2A 层**：其他 Agent 通过协议调用

同一个 Action，四种入口，结果一致。

### Agent 和 UI 是平等公民

在 Agent-Native 架构中，Agent 和 UI 共享：

| 要素 | 说明 |
|------|------|
| **同一个数据库** | SQL-backed state，Agent 的修改直接反映在 UI |
| **同一个 Auth** | 权限分层对两者一致 |
| **同一个上下文** | Agent 知道用户在看什么，用户知道 Agent 在做什么 |
| **同一个 Workspace** | Skills、Memory、Instructions、Sub-agents，可定制 |

### Workspace：让 Agent 像 Claude Code 一样工作

Workspace 是 Agent-Native 引入的一个关键概念。它让你可以为每个用户配置：

- **Instructions**：Agent 的行为指南
- **Skills**：可复用的 Agent 技能包
- **Memory**：跨会话的持久记忆
- **Sub-agents**：拆分的子 Agent
- **MCP Servers**：工具扩展

这正是 Claude Code/Codex 让开发者着迷的原因——**深度定制化**。Agent-Native 把这套能力带到了应用层。

---

## 为什么 Agent-Native 比现有方案更好

### 传统方案的问题

| 方案 | 问题 |
|------|------|
| **纯 Chat UI** | Agent 是个黑盒，无法和应用状态同步 |
| **API 嵌入** | Agent 和 UI 是两个世界，数据不一致 |
| **Buttons → LLM Call** | 按钮触发的不是同一个 Action，无法追踪 |

### Agent-Native 的优势

1. **状态同步是内置的**：Agent 修改了数据，UI 自动更新，无需手动同步
2. **权限控制是统一的**：不需要为 Agent 和 UI 分别实现权限层
3. **上下文感知**：Agent 知道用户当前在看什么，可以给出更精准的响应
4. **渐进式复杂度**：可以从 Headless API 开始，逐步添加 Rich Chat，最后到 Whole App

---

## 适用场景

Agent-Native 特别适合以下场景：

### 需要深度 Agent 定制的 SaaS

如果你的应用需要用户能像配置 Claude Code 一样配置 Agent 行为——不同的 Instructions、不同的 Skills、不同的 Memory——Agent-Native 提供了开箱即用的 Workspace 抽象。

### Agent 和 UI 需要深度协作

比如一个邮件应用：
- **场景 A**：用户在邮件列表中选中一封邮件，点击"AI 总结"
- **场景 B**：用户在聊天中说"帮我总结收件箱里所有未读邮件"

在 Agent-Native 中，这两个场景调用的是同一个 Action，数据一致性天然保证。

### 多 Agent 协作

Agent-Native 原生支持 A2A 协议。一个 Agent 可以"召唤"另一个 Agent 来处理特定任务，两个 Agent 共享同一个应用上下文。

---

## 不适合的场景

Agent-Native 不是银弹，在以下场景可能过度设计：

1. **简单的 Q&A Bot**：不需要复杂的状态同步
2. **纯后台任务**：没有 UI 的 Agent 工作
3. **高度封闭的系统**：Agent 不需要访问应用状态

---

## 笔者的判断

Agent-Native 范式最有价值的地方在于它**重新定义了 Agent 和应用的关系**。

过去十年，我们习惯了"MVC"架构：Model 是数据，View 是界面，Controller 是逻辑。AI 时代，这个范式需要升级：

> **MVA: Model-View-Action，其中 Action 是 Agent 和 UI 共享的业务逻辑原语。**

但这里有一个值得警惕的问题：**Agent-Native 假设你的应用是完全重新设计的**。如果你有一个存量应用，要迁移到 Agent-Native 的成本不低。

笔者认为，这个范式更适合**新构建的应用**，尤其是需要深度 Agent 集成的 B2B SaaS 产品。

---

## 引用

> "Don't choose between rich user interfaces and autonomous agents. Every Agent-Native app is both."

来源：[BuilderIO - How to build agent-native applications (and what not to do)](https://www.builder.io/blog/agent-native-apps)

---

## 关联项目

本文配套项目推荐：[BuilderIO/agent-native](/articles/projects/builderio-agent-native-framework-agent-native-apps-969-stars-2026.md) — Agent-Native 范式的开源框架实现
