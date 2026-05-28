# Cursor TypeScript SDK：编程式 Agent 如何成为组织的基础设施

> **核心论点**：当一个 AI Coding 平台的 SDK 开始强调"CI/CD 触发"、"产品嵌入"、"dedicated VM"这些词汇时，它已经不只是"编程工具"了——它是企业 AI 基础设施的一部分。

---

## 从交互工具到编程基础设施

Cursor 博客最近发布了一篇关于 TypeScript SDK 的文章，标题是《Build programmatic agents with the Cursor SDK》。这句话里值得注意的词不是"agents"，而是"programmatic"和"production"。

> "Coding agents are evolving from interactive tools for individual developers to programmatic infrastructure for organizations."
> — Cursor SDK 官方文档

这意味着什么？

在过去一年多，Cursor 的叙事一直是"让 IDE 更智能"——帮助个体开发者写代码、Review PR、解释报错。但这篇博客的核心受众不是个人开发者，而是**工程团队负责人**和**平台工程师**。

关键词变了：
- "CI/CD pipelines"（不是"写代码更快"）
- "automations for end-to-end workflows"（不是"修复 Bug"）
- "embedding agents into their core products"（不是"在编辑器里用"）
- "dedicated VM"（不是"本地运行"）

这是一次定位的跃迁：从工具到基础设施。

---

## SDK 核心设计：解决什么问题

构建可靠 coding agent 的工程挑战，被 Cursor 总结为四个维度：

1. **安全沙箱**：代码执行环境必须隔离
2. **持久状态与会话管理**：Agent 必须能跨网络中断存活
3. **环境配置**：每次任务需要正确的代码库上下文
4. **模型适配**：当新模型发布时，Agent loop 需要相应调整

原文引用：
> "Building fast, reliable, and capable coding agents that run safely against your data requires meaningful engineering effort: secure sandboxing, durable state and session management, environment setup, and context management."

Cursor SDK 的核心价值主张，就是**把这四件事封装好**，让开发者专注业务逻辑。

---

## 三大核心能力

### 1. 云端 Dedicated VM

```typescript
const agent = await Agent.create({
  apiKey: process.env.CURSOR_API_KEY!,
  model: { id: "composer-2" },
  cloud: {
    repos: [{ url: "https://github.com/cursor/cookbook", startingRef: "main" }],
    autoCreatePR: true,
  },
});
```

Cloud session 不是共享的容器，而是**每个 Agent 独立的专用 VM**，包含：
- 代码库的干净 clone
- 完全配置好的开发环境
- 强隔离的沙箱

这意味着你的 Agent 可以跑很长时间（"keeps going when your laptop sleeps or network drops"），跑完后可以**自动开 PR**、push 分支、上传截图和 demo。

### 2. 三种运行时灵活切换

同一个 SDK，可以跑在：
- **Cloud**：Cursor 基础架构（Dedicated VM）
- **Self-hosted**：自己的网络内（数据不出域）
- **Local**：自己机器上（快速迭代）

```typescript
// 切云端
const agent = await Agent.create({ cloud: { repos: [...] } });

// 切本地
const agent = await Agent.create({ local: { cwd: process.cwd() } });
```

这对企业来说非常重要：**数据治理要求不同，运行时选择就不同**。

### 3. 完整 Harness 能力

通过 SDK 调用的 Agent，拥有与 Cursor IDE 内相同的 harness：

| Harness 组件 | 说明 |
|-------------|------|
| **MCP servers** | 通过 `.cursor/mcp.json` 或 inline 配置连接外部工具和数据源 |
| **Skills** | 自动从仓库的 `.cursor/skills/` 目录加载 |
| **Hooks** | 通过 `.cursor/hooks.json` 观察、控制、扩展 Agent loop |
| **Subagents** | 主 Agent 通过 Agent tool 派生命名子 Agent（各自有独立 prompt 和模型） |
| **Context management** | 代码库索引 + 语义搜索 + 即时 grep |

这意味着你在 SDK 里创建的 Agent，和 Cursor 工程师自己用的 Agent，**用的是同一个基础设施**。

---

## 实际应用场景

Cursor 在博客里列出了几个典型场景：

### 场景 1：CI/CD 驱动的自动化 Agent

```
代码提交 → CI 触发 Agent → Agent 分析变更 → Root Cause 分析 → 自动修复 → PR 更新
```

这是程序员最熟悉的工作流，现在**每个环节之间可以插入 Agent**。

### 场景 2：嵌入客户产品

一些客户把 Cursor SDK 嵌入到**面向客户的 SaaS 产品**里，最终用户不需要懂代码，就能获得 Agent 体验。

这说明 SDK 的使用者不只是"内部工具"，也可能是**toB 或 toC 产品的后端**。

### 场景 3：Programmatic Agent 平台

Faire 和 Rippling 这样的公司，正在用 SDK 构建**自己的 Agent 平台**——不是用 Cursor 的 UI，而是用 SDK 的 API。

原文引用（Faire 工程经理 George Jacob）：
> "Cursor offers a great cloud experience for running many agents in parallel from the editor and CLI. We're excited about the SDK as a path to running our own programmatic agents on that same cloud runtime, without managing VMs or working around memory limits."

这段话的核心是：**他们要的不是 Cursor 这个产品，而是 Cursor 的 runtime**。

---

## 与 Claude Code 的对比

Cursor SDK 和 Claude Code 的 Plugin 系统，走的是两条不同的路：

| 维度 | Cursor SDK | Claude Code Plugins |
|------|-----------|---------------------|
| **交互方式** | 纯 API（Programmatic） | 交互式（Slash Commands + /plugin） |
| **运行时** | Cloud / Self-hosted / Local | 本地为主 |
| **定位** | 企业基础设施 | 个人开发者工具 |
| **API 形态** | REST + streaming | Plugin marketplace |
| **适用场景** | CI/CD、产品嵌入、平台构建 | 日常开发任务 |

**笔者认为**：Claude Code 的 Plugin 系统更注重"人在回路"的交互体验，而 Cursor SDK 更注重视"机器对机器"的编排能力。两者都有价值，取决于你的使用场景。

---

## 工程启示

### 1. AI Coding 平台正在"云化"

两年前，AI Coding 的叙事是"在你本地 IDE 里装一个 AI 助手"。现在，以 Cursor Cloud Agents + SDK 为代表的新范式，是**云端跑 Agent，专门 VM，数据隔离**。

这对企业来说意味着：
- 不需要在本地配环境
- 不需要自己的 GPU 集群
- 只需 API 调用

### 2. "Programmatic"是新的分水岭

不是所有 Agent 都是 Programmatic 的。区别在于：
- **Interactive Agent**：人实时参与，Agent 靠 human-in-the-loop 纠错
- **Programmatic Agent**：人定义目标和边界，Agent 自主完成，可用 CI/CD 触发

Programmatic Agent 的关键特征：可编排、可观测、可重复、可审计。

### 3. SDK 是平台化的关键步骤

一个 AI Coding 平台出 SDK，意味着它已经认可了"用户会用它来构建自己的产品"这一前提。这不是"帮你写代码更好"，而是"我们的 Agent runtime 可以成为你产品的基础设施"。

---

## 总结

Cursor TypeScript SDK 的发布，标志着 AI Coding 平台正在经历一次重要的范式转移：

**从"工具"到"基础设施"**——不是帮你写代码更快，而是帮组织把 AI Agent 集成到自己的工作流和产品里。

这个转变的核心，是把"交互式 Agent"（人在回路）和"编程式 Agent"（机器对机器）分开：前者继续在 IDE 里优化体验，后者通过 SDK 向企业级场景延伸。

> **笔者认为**：2026 年的 AI Coding 平台竞争，已经不只是"谁更能帮你写代码"了，而是"谁更能成为企业 AI 基础设施的一部分"。Cursor SDK 是这个判断的一个有力证据。

---

*来源：[Build programmatic agents with the Cursor SDK](https://cursor.com/blog/typescript-sdk) (Apr 29, 2026) | [Cursor Docs - SDK](https://cursor.com/docs/sdk/typescript) | [Cloud Agents API](https://cursor.com/docs/cloud-agent/api/endpoints)*