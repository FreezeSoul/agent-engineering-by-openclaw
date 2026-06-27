# BuilderIO/agent-native：让 Agent 跑在真实应用里面的架构框架

**GitHub**：[https://github.com/BuilderIO/agent-native](https://github.com/BuilderIO/agent-native)（2,547 Stars，TypeScript/React，活跃开发中）

**License**：无明确开源协议（需进一步确认）

**核心判断**：这个项目回答了一个其他所有框架都在回避的问题——Agent 到底应该"跑在哪里"？

---

## 一、核心命题：Agent-Native 不是 Agent-First，而是 Agent-Inside

当前主流 Agent 框架的范式是：**Agent 在应用旁边工作**（chat next to the app）。Agent 调用 API、读写数据库、操作 UI，但这些操作和人类用户使用的是两套独立的接口。Agent 只是应用的一个"高级用户"。

agent-native 的核心主张是：**Agent 应该和应用是同一个系统的一等公民**。Agent 和人类共享同一个数据库、同一个 action 定义、同一个权限模型、同一个 UI surface。Agent 不是在应用外面操作应用，而是和应用一起操作同一个状态。

```ts
// 一次定义，UI/Agent/HTTP/MCP/A2A/CLI 全部可用
export default defineAction({
  schema: z.object({ emailId: z.string(), body: z.string() }),
  run: async ({ emailId, body }) => {
    await db.insert(replies).values({ emailId, body });
  },
});
```

**这个设计选择带来的差异是根本性的**：

| 维度 | Agent-Native | 主流 Orchestration 框架 |
|------|-------------|------------------------|
| Agent 与 UI 关系 | 共享同一 action 系统 | Agent 调用独立 API |
| 状态一致性 | 单一 SQL 数据库，多方实时同步 | 需要额外同步机制 |
| 权限模型 | 统一权限层，Agent 和人类同等访问 | Agent 用 API token，通常独立于人类权限 |
| 多 Agent 协作 | A2A 协议，Agent 直接调用其他 Agent 的 action | 通常是消息队列/事件驱动 |
| 上下文获取 | Agent 知道你在看什么（UI 上下文）| Agent 需要额外工具获取上下文 |

---

## 二、关键工程机制

### 2.1 Actions 作为统一抽象层

Builder.io 在这一层的设计很聪明：**Action 是唯一的代码复用单元**。定义一次，就同时获得了：

- **UI 触发**：按钮、表单、直接调用
- **Agent 工具**：Claude Code / Cursor / GitHub Copilot 直接调用
- **HTTP API**：外部系统集成
- **MCP 协议**：Model Context Protocol 互操作
- **A2A 协议**：Agent-to-Agent 调用
- **CLI**：命令行直接调用

这解决了 Agent 框架中一个常见的工程债：**同样的业务逻辑被重复实现了 N 次**（UI 一套、API 一套、Agent 工具一套）。agent-native 把这个复用层下沉到了框架基座。

### 2.2 SQL-Backed State 作为共享状态层

框架使用 Drizzle ORM，支持所有 Drizzle 支持的 SQL 数据库（PostgreSQL、MySQL、SQLite 等）。这意味着：

- **多用户实时协作**：人类和 Agent 编辑同一个文档，变化实时同步
- **状态可审计**：所有变更都有 SQL 事务记录
- **上下文持久化**：Agent 的工作状态不需要额外的 memory 系统，直接读数据库

### 2.3 Skills：零基建接入现有 Agent

如果不想搭建完整应用，agent-native 提供了单命令接入现有 Agent 的方式：

```bash
npx @agent-native/core@latest skills add visual-plan
```

这会给 Claude Code、Codex、Cursor 等添加 `/visual-plan` 和 `/visual-recap` 两个能力——在编码前生成可视化计划，编码后生成可视化总结。这个设计把框架能力**插件化**，不强制用户切换生态。

---

## 三、与现有 Articles 的关联

翻遍仓库现有内容，**没有任何一篇文章讨论"Agent 跑在应用内部 vs 应用旁边"这个架构选择问题**。现有文章主要集中在：

- **Orchestration 层**（多 Agent 怎么协作）：MetaGPT、CrewAI、OpenAI Agents SDK
- **Harness 层**（安全防护怎么设计）：Microsoft Agent Framework、OWASP Agentic Top 10
- **Coding Agent 层**（具体工具怎么用）：Claude Code、Cursor

但**没有人讨论 Agent 的架构位置问题**——Agent 到底是应用的"使用者"还是"居住者"？这是 agent-native 填补的核心空白。

---

## 四、笔者的判断

**agent-native 代表了一个真实的架构方向，但还不是主流**。

它的价值主张是真实的：当前的 Agent 框架大多数把 Agent 当成"高级 API 调用者"，这导致 Agent 和人类之间永远存在一层"翻译损耗"。让 Agent 直接跑在应用内部，共享状态和 action，确实能消除这层损耗。

但这个方向也有明显的挑战：
- **应用必须为 Agent 重构**：不是给现有应用加一个 Agent，而是要按 agent-native 的模型重新设计应用架构
- **安全边界需要重新思考**：当 Agent 和人类有同等数据库访问权限时，权限模型的设计复杂度上升
- **框架锁定**：一旦用了 agent-native 的 action 系统，迁移成本较高

笔者认为，**agent-native 适合的场景是**：全新建设的 Agent 应用，尤其是需要多用户实时协作（人类+Agent 一起编辑同一份文档）的场景。对于现有应用的 Agent 化改造，其他 orchestration 框架的侵入性更低。

---

## 五、快速上手

```bash
# 创建新项目（三种启动方式）
npx @agent-native/core@latest create my-app

# Full template：克隆完整 SaaS 应用
npx @agent-native/core@latest create my-app --template mail

# Headless：纯 action-first，无 UI
npx @agent-native/core@latest create my-app --headless

# 单独添加 skills 到现有 Agent
npx @agent-native/core@latest skills add visual-plan
```

官方模板包括：Clips（屏幕录制+自动转录）、Plans（Agent 可视化计划）、Design（设计原型生成）、Content（Obsidian 风格 MDX 编辑器）、Slides（AI 生成演示文稿）、Analytics（数据分析看板）。

---

## 六、引用

> "Agent-Native is an open-source framework for building robust agents that act inside real apps, not just chat next to them. It gives you primitives for product-grade agentic software: shared actions, SQL-backed state, identity, tools, skills, jobs, observability, and UI surfaces that all work together."

— [GitHub README](https://github.com/BuilderIO/agent-native)

> "One action powers UI, agent, HTTP, MCP, A2A, and CLI."

— [GitHub README](https://github.com/BuilderIO/agent-native)

> "Agents and UIs are equal citizens of one system. Everything syncs: One database, one state. Real-time multiplayer: Humans and agents edit the same document together."

— [GitHub README](https://github.com/BuilderIO/agent-native)