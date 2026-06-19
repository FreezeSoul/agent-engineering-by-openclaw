# BuilderIO/agent-native：让 Agent 与 UI 成为应用的平等公民

> 969 Stars | TypeScript | MIT License | 210 stars today
> GitHub: [BuilderIO/agent-native](https://github.com/BuilderIO/agent-native)

---

## 核心命题

大多数 AI 应用把 Agent 和 UI 当成两个独立系统——Agent 在聊天框里干活，UI 在界面上展示结果，然后用 API 硬粘在一起。这导致状态不同步、权限不一致、上下文丢失。

**agent-native 的解法是：重新设计应用的原子单位——Actions，让 Agent 和 UI 天然共享同一个执行模型。**

---

![GitHub](screenshots/builderio-agent-native-20260620.png)

---

## 为什么这个项目值得关注

### 1. 同一个 Action，四种触发方式

```typescript
// 定义一次，到处可用
export default defineAction({
  schema: z.object({ emailId: z.string(), body: z.string() }),
  run: async ({ emailId, body }) => {
    await db.insert(replies).values({ emailId, body });
  },
});
```

这个 Action 同时是：
- **UI 按钮的点击处理器**
- **Agent 对话中的工具调用**
- **HTTP API 的端点**
- **MCP/A2A 协议的调用**

不需要为每种入口单独写代码。

### 2. Workspace：把 Claude Code 的能力带到应用层

这是我认为这个项目最有价值的设计。它把 Claude Code 的定制化能力（Skills、Memory、Instructions、Sub-agents）抽象成了一套可复用的 Workspace 系统：

```typescript
// 每个用户有自己的 Workspace 配置
const workspace = {
  instructions: '你是邮件助手，用中文回复',
  skills: ['visual-plan', 'visual-recap'],
  memory: '记住用户的偏好设置',
  subagents: [draftAgent, summaryAgent]
}
```

**关键洞察**：如果一个 SaaS 产品想让用户深度定制 Agent 行为，这套 Workspace 抽象是开箱即用的。

### 3. 多 Agent 协作：Agent 召唤 Agent

在 Agent-Native 中，一个 Agent 可以通过 A2A 协议召唤另一个 Agent：

```
用户 → 邮件 Agent → 召唤日历 Agent → 协作完成任务
```

所有 Agent 共享同一个应用上下文，不需要额外的数据同步。

### 4. 三种形态，按需渐进

| 形态 | 说明 |
|------|------|
| **Headless** | 纯 API/CLI 调用，适合后台任务 |
| **Rich Chat** | 带聊天界面的 Agent，支持流式输出 |
| **Whole App** | Agent 和 UI 完全融合，支持实时协作 |

---

## 技术细节

### 架构

- **Runtime**：TypeScript/Node.js
- **数据库**：任何 Drizzle 支持的 SQL 数据库
- **部署**：任何 Nitro 支持的目标（Vercel、Cloudflare Workers、Docker）
- **协议**：MCP、A2A、HTTP/CLI、OpenAI Agents SDK、Vercel AI SDK

### 与竞品对比

| 特性 | agent-native | 传统方案 |
|------|-------------|---------|
| Agent-UI 状态同步 | 内置，自动 | 手动同步，容易出错 |
| 权限控制 | 统一 | 分开实现 |
| 上下文感知 | Agent 知道用户在看什么 | Agent 不知道 |
| MCP/A2A 支持 | 原生 | 需要额外集成 |
| 学习曲线 | 中等 | 低（但后续维护成本高）|

---

## 笔者的判断

**agent-native 最有价值的地方不是某个具体功能，而是它提出的问题框架：你的应用到底是为 Agent 设计的，还是为人类设计的？**

在 agent-native 之前，我们倾向于"先有人类应用，再把 Agent 粘上去"。这个范式颠倒了顺序：**先定义 Actions（Agent 和 UI 共享的业务逻辑），再决定如何暴露这个 Action**。

笔者认为这个方向是对的，尤其适合需要深度 Agent 定制的 B2B SaaS 产品。但需要注意：

1. **存量应用迁移成本高**：如果已有应用，要迁移到 agent-native 需要较大改动
2. **复杂度增加**：统一 Action 模型意味着更强的耦合，需要更好的测试覆盖
3. **成熟度**：目前 969 Stars，v0.x 版本，生产使用需评估风险

---

## 如何上手

```bash
# 创建完整 SaaS 模板
npx @agent-native/core@latest create my-platform

# 添加单个 App
npx @agent-native/core@latest add-app mail --template mail

# 部署
npx @agent-native/core@latest deploy
```

或者只是想给现有 Claude Code 添加能力：

```bash
# 单独安装 visual-plan skill
npx @agent-native/core@latest skills add visual-plan
```

---

## 引用

> "Every Agent-Native app is both. The agent and the UI are equal citizens of the same system."

来源：[GitHub README - BuilderIO/agent-native](https://github.com/BuilderIO/agent-native)

---

## 关联文章

本文配套文章：[Agent-Native：重新定义 Agent 与应用的关系](/articles/fundamentals/builderio-agent-native-paradigm-equal-citizens-2026.md) — 深度解析 Agent-Native 范式
