---
owner: BuilderIO
repo: agent-native
stars: 1003
license: ISC
verified_at: 2026-06-20
verified_via: GitHub API + package.json
---

# BuilderIO/agent-native — 五大架构原则的工程化身

> **1,003⭐ | ISC 协议 | MIT 风格开放许可**
> Agent 与 UI 是同一系统的平等公民。一次定义 Action，五端共享（UI/Agent/HTTP/MCP/A2A/CLI）。

---

## 项目定位

**BuilderIO/agent-native** 是 [Agent-Native Architecture](https://www.builder.io/blog/agent-native-architecture) 文章的官方开源实现，把五大架构原则从理论落地为可运行的 TypeScript 框架。

核心承诺：

> **Don't choose between rich user interfaces and autonomous agents. Every Agent-Native app is both.**

---

## 核心特性

### 1. Actions 一次定义，多端共享

```typescript
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

同一个 action 自动暴露为：
- UI mutation（前端直接调用）
- Agent tool（LLM function calling）
- HTTP endpoint（REST API）
- MCP tool（Model Context Protocol）
- A2A tool（Agent-to-Agent）
- CLI command（命令行）

### 2. SQL 状态协调层

- Agent 和 UI 读写同一份数据
- Actions 写入 SQL → version 变化 → UI 轮询更新
- 无需长连接、事件总线、共享内存
- 支持任何 Drizzle 兼容的 SQL 数据库（PostgreSQL/MySQL/SQLite）

### 3. Per-user Workspace

- Skills、memory、instructions、sub-agents、MCP servers
- SQL-backed，按用户隔离
- 达到 Claude Code 级别的灵活性 + SaaS 级别的经济性

### 4. Agent Runtime 完整组件

内置：
- Chat（聊天界面）
- Tools（工具调用）
- Skills（技能管理）
- Memory（记忆系统）
- Jobs（后台任务）
- Observability（可观测性）
- Handoffs（Agent 间交接）

### 5. 实时协作与多 Agent

- CRDT merging（文档协作）
- Live presence（光标、选择、谁在哪一页）
- Agent 作为 first-class peer editor
- A2A 协议：跨应用 Agent 协作
- 任何 SQL 数据库 + 任何 Nitro 兼容 host

### 6. 三种产品形态可切换

| 形态 | 描述 |
|------|------|
| **Headless** | 通过 code/CLI/HTTP/MCP/A2A 调用 agent 和 actions |
| **Rich chat** | 独立或嵌入的聊天界面（带表格、图表、审批、setup 流、tool 结果） |
| **Whole app** | 完整 SaaS/产品 UI，聊天可在中央、侧栏、并与应用状态保持同步 |

---

## 与文章 5 大原则的对应

| 文章原则 | 项目实现 |
|---------|---------|
| Agent UI Parity | 同一 action 同时驱动 UI 和 Agent |
| Define Actions Once | `defineAction()` schema 一次定义，五端暴露 |
| Context Awareness | `view-screen`/`navigate` actions + per-user workspace |
| Live Sync via Database | SQL 写入 → version 变化 → UI 轮询 |
| Observability and Audit | 内置 jobs + observability + audit log |

---

## 协议兼容性

内置支持：
- **A2A**（Agent-to-Agent）
- **MCP**（Model Context Protocol）
- **MCP Apps**
- **Standard remote MCP OAuth**
- **MCP clients**
- **HTTP/CLI action calls**
- **Native chat widgets**
- **`AgentChatRuntime` adapters**
- **Standard OpenAI** chat protocol
- **AG-UI**
- **Claude Agent SDK**
- **Vercel AI SDK** chat runtime connectors

---

## 技术栈

- **语言**: TypeScript
- **数据库 ORM**: Drizzle（任何兼容 SQL 数据库）
- **部署**: Nitro（任何兼容 host）
- **Schema 验证**: Zod
- **更新频率**: 活跃（最近更新 2026-06-19）
- **首次发布**: 2026-03-12

---

## 适合谁用

### 适合

- **构建协作型产品**（文档、项目管理、设计工具）—— 人机需要共享状态
- **复杂工作流产品**（CRM、ERP、邮件）—— 多步骤、多角色
- **数据驱动应用**（BI、analytics）—— UI 探索 + Agent 自动化

### 不适合

- 简单聊天机器人（LangChain/OpenAI Agents SDK 更轻量）
- 纯 coding agent（Claude Agent SDK 专项优化）
- 无状态 API 服务（增加不必要的复杂度）

---

## 与同类框架的对比

| 框架 | Agent-Native 程度 | 关键差异 |
|------|-------------------|---------|
| LangChain | 部分 | 偏 LLM 编排，UI 集成弱 |
| Claude Agent SDK | 中 | Coding agent 强，应用集成需自建 |
| OpenAI Agents SDK | 中 | 工具调用标准化，但状态管理分散 |
| Mastra | 中 | TypeScript-first，但 action 协议化弱 |
| **Agent-Native (BuilderIO)** | **高** | **Action 同时驱动 UI/Agent/协议** |

---

## Pair 闭环

**Article** (`articles/fundamentals/builderio-agent-native-architecture-five-principles-2026.md`) ↔ **Project** (BuilderIO/agent-native):

| Article 描述 | Project 实现 |
|-------------|------------|
| 五大架构原则（理论）| `defineAction()` + SQL state + per-user workspace（工程）|
| Agent-UI 对等 | 同一 action schema 同时驱动两端 |
| Action 一次定义 | TypeScript decorator-style action 定义 |
| 数据库协调层 | Drizzle + SQL（任何兼容 DB）|
| 协议分发 | MCP / A2A / HTTP / CLI 原生支持 |

闭环强度：⭐⭐⭐⭐⭐ SPM 字面级对位 + 同源（理论 ↔ 工程实现同团队）

---

## 引用与参考

- **项目仓库**: https://github.com/BuilderIO/agent-native
- **理论原文**: https://www.builder.io/blog/agent-native-architecture
- **姊妹文章**: https://www.builder.io/blog/agent-native-apps
- **延伸思考**: https://www.builder.io/blog/why-the-best-agent-native-apps-use-less-ai
- **姊妹项目** (R456): [BuilderIO/skills](https://github.com/BuilderIO/skills) — 1,133⭐ composable multi-agent coding skills
- **官方文档**: https://agent-native.com

---

> **核心价值**: Agent-Native 框架把「UI 与 Agent 平等公民」从博客愿景落地为可运行的 TypeScript 代码。当其他 Agent 框架还在解决「如何让 Agent 调用工具」时，BuilderIO 已经在解决「如何让 Agent 和 UI 共享同一个应用模型」——这是 AI 应用从 demo 走向 production 的关键跨越。