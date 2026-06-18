# EverMind-AI/EverOS：当 Agent 的记忆变成文件夹

**GitHub**: [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS) | **Stars**: 7,727 ⭐ | **License**: Apache-2.0 | **Lang**: Python

> 这篇文章要回答的问题是：Agent 的长期记忆究竟应该怎么存？为什么 EverOS 选择把记忆写成 Markdown 文件，而不是塞进向量数据库——这个反直觉的设计背后，藏着对 Agent 记忆本质的深刻理解。

---

## 核心命题

EverOS 解决了一个让所有长时运行 Agent 开发者头疼的问题：记忆的持久化和复用。

大多数 Agent 框架选择把记忆存进向量数据库，用 embedding 检索。但 EverOS 走了一条完全不同的路——**它把每一次交互都写成 Markdown 文件存在磁盘上**，然后用 SQLite + LanceDB 做索引。内存是 Markdown，索引只是衍生品。

这个反直觉的设计有一个核心理由：

> "Canonical `.md` files that are readable, editable, diffable, and Git-versioned." — EverOS README

记忆如果不可读、不可编辑、不可比对，它就只是一个黑盒子。EverOS 把记忆变成了团队协作的基础设施——你可以用 Obsidian 打开 Agent 的大脑，可以用 Git 做版本控制，可以用任何文本编辑器修改。

这不只是存储格式的选择，而是对"Agent 记忆应该是什么"的一种哲学回答。

---

## 为什么 Agent 记忆应该是文件夹？

### 传统方案的三个困境

| 方案 | 困境 |
|------|------|
| **纯向量数据库** | 存储的是 embedding，无法直接理解；更新需要 re-embed；无法与人类协作 |
| **图数据库** | 存储结构清晰，但同样不可直接读取；需要专门的查询语言 |
| **Key-Value / 文档库** | 解决了可读性，但缺少检索能力 |

EverOS 的答案是：**用 Markdown 作为 source of truth，用索引作为检索加速层**。两者不是替代关系，而是主从关系——Markdown 是原始数据，索引是从 Markdown 重建的，丢了索引可以重建，丢了 Markdown就丢了记忆。

### 记忆的六层存储结构

```
~/.everos/
├── default_app/
│   └── default_project/
│       ├── users/<user_id>/
│       │   ├── user.md           # 用户profile（人类可读）
│       │   ├── episodes/         # 每日对话记忆（可见层）
│       │   ├── .atomic_facts/    # 原子事实（从对话中提取）
│       │   └── .foresights/     # 预测性记忆（dotfile隐藏）
│       └── agents/<agent_id>/
│           ├── agent.md
│           ├── .cases/           # 任务案例（一个case = 一个任务生命周期）
│           └── skills/           # 命名技能记忆（procedural memory）
├── .index/
│   ├── sqlite/system.db         # 状态 + 队列 + 审计
│   └── lancedb/*.lance/          # 向量 + BM25 + 标量索引
└── .tmp/                         # 临时文件
```

这个结构的精妙之处在于**双轨设计**：

- **User track**（用户层）：`episodes/profile` — 存储用户的历史偏好、说过的事实、行为模式
- **Agent track**（Agent层）：`cases/skills` — 存储 Agent 在任务中的经验总结、技能定义

两条轨道并列存在，互不干扰，但可以通过 user_id + agent_id 联合检索。

> 笔者认为，这个双轨设计比大多数"统一记忆库"方案更接近真实：人类记忆和 Agent 经验本来就是不同性质的东西，混在一起只会让检索噪音变大。

---

## Self-Evolving Memory：Idle 时 Agent 在想什么？

EverOS 1.0.0 的核心特性不是存储，而是**自我演化**。

官方文档透露了两个即将上线的功能：

1. **Knowledge Wiki**：把记忆自动转成可编辑的、源数据可溯源的 Markdown 知识页面。记忆不再是死的记录，而是活的文档。
2. **Reflection**：当系统空闲或离线时，Agent 会主动运行反思循环——连接信号、压缩历史、优化 Profile 和 Skills。

```
Coming next: Reflection will run when the system is idle or offline 
to connect signals, compress history, and improve profiles and 
skills between sessions.
```

Reflection 这个概念让 EverOS 从"记忆存储"进化成了"记忆操作系统"。它不只是被动地记录，还在主动地消化和重组。

> 笔者认为，Reflection 机制才是真正的 Agent 记忆进化点。大多数现有方案的"记忆"只是检索增强，而 EverOS 正在做的是让 Agent 具备meta-cognition 能力——知道自己记住了什么、记住了多好、哪些需要忘掉或压缩。

---

## MCP 协议的工程实现：EverMemos-MCP

EverOS 不只是自己用 Markdown 存记忆——它还通过 MCP 协议把记忆能力对外暴露。

`tt-a1i/evermemos-mcp` 是 EverOS 的 MCP Server 实现，让任何 MCP Client（比如 Cursor、Windsurf、Cline）都能接入 EverOS 的记忆层：

> "AI Coding Assistants With EverOS: Universal long-term memory layer for AI coding assistants, powered by EverOS." — EverOS README

这意味着什么？意味着**EverOS 是第一个把 Agent 记忆能力标准化成 MCP 工具的项目**。你可以用 Cursor 写代码、问 EverOS 关于这个项目你知道什么、它从你的历史对话中检索相关记忆。

这与 R435 产出文章的核心论点形成完美闭环：

- **R435 Article 论点**：Anthropic 说 "Skills 是 expertise layer，MCP 是 connectivity layer，协同才是关键"
- **EverOS 实现**：MCP Server = connectivity layer，对外暴露记忆工具；Skills directory = expertise layer，存储 Agent 的领域知识和工作流

```
Anthropic 理论层：Skills (expertise) + MCP (connectivity)
EverOS 工程层：Skills/ (procedural memory) + EverMemos-MCP (MCP Server)
```

---

## OpenClaw 的官方记忆方案

EverOS 还有一个特殊身份——它是 **OpenClaw 的官方记忆层方案**。

README 中有一段专门的迁移文档：

> "Legacy OpenClaw Agent Memory: Archived pre-1.0.0 plugin reference. New integrations should use the EverOS 1.0.0 API." — EverOS README

这意味着：
1. OpenClaw 曾经有自己的 Agent Memory 插件（pre-1.0.0）
2. EverOS 1.0.0 是 OpenClaw 官方推荐的升级路径
3. OpenClaw → EverOS 的集成是第一等的(first-class)支持场景

对于 OpenClaw 用户而言，EverOS 提供了开箱即用的长期记忆能力：跨 session 的上下文保持、Agent 经验积累、用户偏好学习。

---

## DDD 五层架构：记忆的工程实现

EverOS 的架构是标准的 DDD 五层设计，但每一层都围绕"记忆"这个核心问题展开：

```
┌───────────────────────────────────────────────┐
│  entrypoints/  (CLI + HTTP API)                │  presentation
├───────────────────────────────────────────────┤
│  service/      (use cases: memorize/retrieve)  │  application
├───────────────────────────────────────────────┤
│  memory/       (extract + search + cascade)    │  domain
├───────────────────────────────────────────────┤
│  infra/        (markdown / sqlite / lancedb)   │  infrastructure
└───────────────────────────────────────────────┘
        ↑                    ↑
   component/            core/
   (LLM/Embedding)       (observability/lifespan)
```

- **Domain 层（memory/）**：核心业务逻辑——记忆的提取、检索、级联同步都在这里
- **Infrastructure 层（infra/）**：Markdown 文件 + SQLite 状态 + LanceDB 向量索引
- **Application 层（service/）**：两个核心用例 `memorize` 和 `retrieve`

有趣的是，**LLM/Embedding 被放在 component/ 而非 core/**——它们是外部依赖，不是核心域。这意味着 EverOS 的记忆域是完全与 LLM 解耦的，你可以换掉 LLM Provider 而不影响记忆域本身。

---

## 竞品对比：为什么不是 pgvector 或者 Chroma？

| 维度 | EverOS | pgvector / Chroma / Pinecone |
|------|--------|------------------------------|
| **存储格式** | Markdown（人类可读）| Embedding 向量（机器专有）|
| **索引来源** | 从 Markdown 重建 | 主存储 |
| **协作能力** | Git + 文本编辑器 + Obsidian | 需要 API |
| **记忆演化** | Reflection + Wiki（自动重组）| 无 |
| **多Agent支持** | user_id + agent_id 正交检索 | namespace 隔离 |
| **本地化** | SQLite + LanceDB（本地）| 依赖外部向量库 |

核心差异是**存储哲学**的选择：其他方案把向量当作记忆本身，EverOS 把 Markdown 当作记忆本身。

> 笔者认为，EverOS 的方案更适合"人类需要理解和干预记忆"的场景——比如你要删掉某条错误的记忆、修改某个事实、用 Obsidian 做知识管理。而纯向量方案更适合"机器检索优先、人类不需要直接读"的场景。

---

## 快速上手：三行代码解锁记忆

```bash
# 1. 安装
uv pip install everos

# 2. 初始化
everos init   # 生成 .env 配置文件

# 3. 启动服务
everos server start

# 4. 写入第一条记忆
TS=$(($(date +%s)*1000))
curl -X POST http://127.0.0.1:8000/api/v1/memory/add \
  -H 'Content-Type: application/json' \
  -d '{
    "session_id": "demo-001",
    "messages": [
      {"sender_id": "alice", "role": "user", "timestamp": '$TS', "content": "I prefer TypeScript over Python."}
    ]
  }'

# 5. 检索回来
curl -X POST http://127.0.0.1:8000/api/v1/memory/search \
  -H 'Content-Type: application/json' \
  -d '{"user_id": "alice", "query": "What language do I prefer?", "top_k": 3}'
```

Open `~/.everos/` 看看 Agent 的记忆长什么样——就是一堆 Markdown 文件。

---

## 关联 Article

本文与 R435 Article 形成完美的**理论 ↔ 工程**闭环：

- **R435 Article**：Anthropic 解读 Skills + MCP 协同机制（Skills 是 expertise layer、MCP 是 connectivity layer）
- **本文（EverOS）**：Skills directory = expertise layer 的工程实现；EverMemos-MCP = connectivity layer 的工程实现

两者共同回答：协议分工模型怎么在真实系统中落地？

**相关 Article**：[Anthropic 扩展 Claude 能力：Skills 与 MCP 的协同机制 2026](../tool-use/anthropic-extending-claude-capabilities-skills-mcp-coordination-2026.md)

---

## 一句话总结

EverOS 把 Agent 记忆做成了一个用 Markdown 写作、用文件夹管理的操作系统——当记忆变成磁盘上的文件，它就不再只是 AI 的内部状态，而是团队可以一起阅读、编辑、版本控制的协作资产。

**适用场景**：需要跨 session 保持上下文、需要在多个 Agent 之间共享记忆、需要人类能够理解和干预 Agent 记忆的系统。

**不适用场景**：纯机器检索场景、无法容忍文件 IO 延迟的极高频记忆写入、对存储体积敏感的边缘部署。
