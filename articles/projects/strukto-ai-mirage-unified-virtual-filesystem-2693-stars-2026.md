# strukto-ai/mirage：统一虚拟文件系统，让 AI Agent 用 bash 操作一切后端

> 🔴 **本文来源**：GitHub — [strukto-ai/mirage](https://github.com/strukto-ai/mirage) | Stars: 2,693 | Created: 2026-05-06
> 官方文档：https://docs.mirage.strukto.ai

---

## 核心命题

AI Agent 最大的集成负担是什么？**每个新后端都需要学一套新的 API。**

S3 要学 S3 SDK、Gmail 要学 Gmail API、Slack 要学 Slack SDK……一个 Agent 如果需要同时操作 GitHub、Slack、S3 和本地文件，就需要分别掌握四套完全不同的接口 vocabulary。

Mirage 的回答是：**给所有后端包一层统一的虚拟文件系统**。Agent 不需要学每套 SDK，只需要会 `cat`、`grep`、`ls`——而 Mirage 的 VFS dispatcher 将这些命令路由到正确的数据源。

```ts
const ws = new Workspace({
  '/data':   new RAMResource(),
  '/s3':     new S3Resource({ bucket: 'logs' }),
  '/slack':  new SlackResource({}),
  '/github': new GitHubResource({}),
})

// 同一个 bash 工具，操作不同的后端
await ws.execute('grep alert /slack/general/*.json | wc -l')
await ws.execute('cat /github/mirage/README.md')
await ws.execute('cp /s3/report.csv /data/local.csv')
```

**这个设计聪明在哪**：现代 LLM 对 bash 的训练语料最丰富，而对各类 API SDK 的掌握参差不齐。Mirage 不让 Agent 学习新 vocabulary，而是把新后端映射到 Agent 已经熟悉的 vocabulary 上。

---

## 为什么值得关注

### 1. 统一抽象，替换 N 个 SDK 为 1 个 FS

目前已支持的资源类型横跨多个类别：

| 类别 | 资源类型 |
|------|---------|
| **存储** | S3 / R2 / OCI / Supabase / GCS, Redis, RAM, Disk |
| **办公套件** | Gmail / GDrive / GDocs / GSheets / GSlides |
| **协作工具** | GitHub / Linear / Notion / Trello |
| **通信** | Slack / Discord / Telegram / Email |
| **数据库** | MongoDB |
| **基础设施** | SSH |

所有这些在 Agent 眼中，都是 `/` 根目录下的子目录。

### 2. 命令可定制，覆盖边角场景

```ts
// 全局注册命令，所有 mount 都可用
ws.command('summarize', async ({ args }) => {
  const content = await readFile(args[0])
  return await llm.summarize(content)
})

// 针对特定资源和文件类型的命令覆盖
// 在 S3 的 Parquet 文件上运行 `cat` 时，自动渲染为 JSON 而非原始字节
ws.command('cat', { resource: 's3', filetype: 'parquet' }, async ({ path }) => {
  const rows = await parquet.read(path)
  return JSON.stringify(rows, null, 2)
})
```

这种「命令注册 + 类型路由」机制，实际上让 Agent 的工具层变成了**可编程的**，而不只是预定义的工具列表。

### 3. 便携工作区：克隆、快照、版本控制

Mirage 的 Workspace 可以被序列化、克隆、在不同机器间迁移。Agent 的运行环境不再绑定在特定进程或容器中——这直接解决了**跨会话状态传递**的问题。

### 4. 集成主流 Agent 框架

官方支持：
- OpenAI Agents SDK
- Vercel AI SDK (TypeScript)
- LangChain
- Pydantic AI
- CAMEL
- OpenHands

以及 CLI 模式：直接插入 Claude Code 和 Codex 的 bash 环境，让它们通过熟悉的命令行访问所有 mount 的资源。

---

## 技术架构简析

```
┌─────────────────────────────────────────────┐
│  AI Agent / Claude Code / Codex (Bash)     │
│         ↓ bash 命令                        │
│  Mirage Bash  ← 熟悉的 vocabulary          │
│         ↓                                 │
│  Virtual File System Dispatcher            │
│         ↓                                 │
│  Per-Resource Handler (S3/GitHub/Slack…)  │
│         ↓                                 │
│  Infrastructure & Remote Services         │
└─────────────────────────────────────────────┘
```

关键设计决策：**VFS 是统一抽象层，每个 Resource Handler 负责将自己的服务映射到这个抽象**。Agent 侧的接口永远是 bash，Mirage 内部负责路由和转换。

---

## 适用场景

✅ **适合用 Mirage 的场景**：
- Agent 需要同时操作多个异构后端（GitHub + Slack + S3 + DB）
- 想让 Agent 用熟悉的 bash vocabulary 而非学习每套 SDK
- 需要在多个 Agent run 之间迁移/恢复完整的上下文环境
- 使用 OpenHands、Claude Code 等 CLI-based coding agent

❌ **不太适合的场景**：
- 只需要操作单一后端，直接用该后端 SDK 更简单
- 对延迟极度敏感（VFS 路由本身有 overhead）
- 后端不在官方支持列表中（需要自己实现 Resource Handler）

---

## 竞品对比

| 维度 | Mirage | 直接 SDK | MCP 协议 |
|------|--------|---------|---------|
| **Agent 侧 vocabulary** | bash（LLM 最熟悉）| 各自 SDK（需单独训练）| Tool Call（需定义 schema）|
| **多后端统一性** | 单一 `/` 根，天然统一 | 各自独立 | 通过 protocol 统一接口定义 |
| **可编程工具层** | ✅ 命令注册 + 类型路由 | ❌ | 需通过 prompt engineering |
| **跨 run 状态迁移** | ✅ Workspace 序列化 | ❌ | 需自己实现 |
| **Latency** | 中等（多一层 dispatch）| 低 | 中等 |

笔者认为，Mirage 的定位不是替换 MCP，而是**给那些不愿意重构为 Tool Call 的 Agent 系统提供一个「不用改 Agent 端代码」的集成路径**。它解决的是 Agent 侧 vocabulary 的问题，而不是协议层的问题。

---

## 如何开始

```bash
# Python CLI
pip install mirage-ai
mirage init

# TypeScript SDK
npm install @struktoai/mirage-node

# Claude Code / Codex 集成
mirage daemon
```

官方文档：https://docs.mirage.strukto.ai

---

> **引用来源**：
> - GitHub README: [strukto-ai/mirage](https://github.com/strukto-ai/mirage)
> - 官方文档: https://docs.mirage.strukto.ai
> - Discord 社区: https://discord.gg/u8BPQ65KsS