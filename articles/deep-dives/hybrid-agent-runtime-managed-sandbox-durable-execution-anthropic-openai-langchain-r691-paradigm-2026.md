# Hybrid Agent Runtime:Managed Sandbox + Durable Execution 三家 1st-party 范式收敛

> **R691 核心论点**:**Anthropic claude-agent-sdk-typescript + OpenAI "The next evolution of the Agents SDK" + LangChain Deep Agents v0.5** 三家 1st-party 厂商在 24-48h 窗口内同步 ship "Managed Agent Runtime" 形态 —— **Managed Sandbox + Durable Execution + Async Subagents** 是 R690 论证的「Hybrid 三层架构」在 Layer 2 (Harness) 和 Layer 3 (State) 上的 1st-party 显式兑现,**"vendor SDK 越做越薄,managed runtime 越做越厚" 是 R691 的核心 insight**。

**关键词**:Managed Agent Runtime / Durable Execution / Snapshotting & Rehydration / Async Subagents / Agent Protocol / MCP Tasks / Sandbox Abstraction
**类型**:deep-dive(Hybrid Architecture meta-synthesis 第 5 段 arc,承接 R687 / R688 / R689 / R690)
**核心命题**:**Hybrid 范式在 Layer 2/3 上 1st-party 收敛为 "Managed Agent Runtime"** —— 这是 Agent 工程从 SDK 走向 Runtime 的范式跃迁。

---

## 一、R691 触发条件:三层 1st-party evidence 同框

R691 触发本轮的不是新 1 个 SDK release,而是**三家 1st-party 厂商在 24-48h 窗口内同步 ship 「Managed Agent Runtime」形态** —— 三个 release 各自独立,但都指向同一个 mental model:

| 维度 | Anthropic (claude-agent-sdk-typescript) | OpenAI (The next evolution of the Agents SDK) | LangChain (Deep Agents v0.5) |
|------|----------------------------------------|----------------------------------------------|------------------------------|
| **核心命题** | "Fixed background agent, remote agent, and MCP task state not being restored when resuming a session via the SDK" | "Separating harness from compute for security, durability, and scale" | "Async (non-blocking) subagents via Agent Protocol" |
| **Layer 2 (Harness)** | `canUseTool` callback + `requestId` correlation + `blocked` field on `workflow_agent` events | "model-native harness" + Codex-like filesystem tools + AGENTS.md / skills / shell / apply patch | Deep Agents harness + 5 tools (start/check/update/cancel/list_async_tasks) |
| **Layer 3 (State)** | **MCP task state restored on resume** | **snapshotting and rehydration** in fresh container | **AsyncSubAgent threads + runs** (Agent Protocol native stateful) |
| **执行环境** | bundled CLI 2.1.202+ | Native sandbox:Blaxel / Cloudflare / Daytona / E2B / Modal / Runloop / Vercel | ASGI transport + LangSmith deployment |
| **协议** | MCP (bundled) | MCP + skills + AGENTS.md + shell + apply_patch | Agent Protocol (LangChain 1st-party open spec) |
| **1st-party URL** | github.com/anthropics/claude-agent-sdk-typescript CHANGELOG | openai.com/index/the-next-evolution-of-the-agents-sdk | langchain.com/blog/deep-agents-v0-5 |

> **R691 笔者认为**:**这不是三个独立的产品演进,这是 Hybrid Architecture meta-synthesis 在 Layer 2 + Layer 3 的 1st-party 同步兑现** —— Managed Agent Runtime 已经成为 OpenAI / Anthropic / LangChain 共识性的 1st-party 形态。R691 论证的不是 SDK 选型问题,而是 **Agent 工程正在从 "SDK + 业务代码" 走向 "Managed Runtime + 业务代码"** 的范式跃迁。

---

## 二、OpenAI "The next evolution of the Agents SDK" 1st-party 原型解读

### 2.1 核心论点:Separating harness from compute for security, durability, and scale

OpenAI 2026 年 7 月 7 日发布的 [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk) 文章,核心命题有三条:

> **(1) A more capable harness for the agent loop**:With today's release, the Agents SDK harness becomes more capable for agents that work with documents, files, and systems. It now has configurable memory, sandbox-aware orchestration, Codex-like filesystem tools, and standardized integrations with primitives that are becoming common in frontier agent systems.

> **(2) Native sandbox execution**:The updated Agents SDK supports sandbox execution natively, so agents can run in controlled computer environments with the files, tools, and dependencies they need for a task.

> **(3) Separating harness from compute for security, durability, and scale**:Agent systems should be designed assuming prompt-injection and exfiltration attempts. Separating harness and compute helps keep credentials out of environments where model-generated code executes. **It also enables durable execution. When the agent's state is externalized, losing a sandbox container does not mean losing the run. With built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint if the original environment fails or expires.**

**R691 笔者认为这三点恰好对应 R690 三层架构的 Layer 2 + Layer 3**:

| OpenAI 命名 | R690 三层架构对应 | 工程含义 |
|------|------------|----------|
| model-native harness | Layer 2 (Harness / Middleware) | vendor SDK 不再 "全栈",而是提供 programmable rules engine + native tools |
| Codex-like filesystem tools | Layer 2 (Harness / Middleware) | filesystem operations 作为 first-class harness primitive |
| Native sandbox execution | Layer 2 (Harness / Middleware) | sandbox 成为 harness 的 execution substrate,而非业务代码自建 |
| **snapshotting and rehydration** | **Layer 3 (Protocol / State)** | **state 显式化为 durable execution primitive,这是 R690 "State 显式化" 工程拐点的 1st-party 兑现** |
| **Manifest abstraction** | **Layer 3 (Protocol / State)** | **workspace 描述显式化(Manifest),允许跨 sandbox provider 移植** |

> **R691 笔者认为**:**OpenAI 的 "Manifest abstraction for workspace" 是 R689 MCP Tasks extension + checkpoint/resume pattern 在 SDK 层的 1st-party 显式兑现** —— 业务侧不再需要写自己的 workspace serialization,而是用 Manifest descriptor 描述,Runtime 负责 snapshot + rehydrate。

### 2.2 OpenAI 的 "vendor-agnostic sandbox" 战略

OpenAI 列出 Native sandbox 支持 7 家 sandbox provider:

> Developers can bring their own sandbox or use built-in support for **Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, and Vercel**.

**R691 笔者认为这是 vendor-agnostic 战略的明确信号**:

- OpenAI 没有 lock-in 到自己的 sandbox(虽然云厂商有 Cloudflare / Vercel 关系)
- 主动拥抱开源 sandbox 生态(E2B / Daytona)
- 主动拥抱"developer bring your own" 模型

> **R691 笔者认为**:**OpenAI 的策略是把 Agents SDK 做成"harness-as-a-service",把 sandbox 作为 portable execution substrate** —— 这是 R688 Hybrid Architecture "Rules engine + LLM" meta-synthesis 中"rules engine 是 vendor-agnostic 通用层"的 1st-party 兑现。

### 2.3 OpenAI 的 "primitive 标准化" 战略

OpenAI 列出的 harness primitive:

> These primitives include tool use via **MCP**, progressive disclosure via **skills**, custom instructions via **AGENTS.md**, code execution using the **shell** tool, file edits using the **apply patch** tool, and more.

**R691 笔者认为这是 Hybrid 范式 "跨 vendor 协议层" 的 1st-party 显式兑现**:

| Primitive | 来源 | Hybrid Layer |
|-----------|------|--------------|
| **MCP** | modelcontextprotocol.io | Layer 3 (Protocol) - 跨 vendor 工具协议 |
| **skills** | agentskills.io | Layer 2 (Harness) - progressive disclosure 跨 vendor skill 描述 |
| **AGENTS.md** | agents.md | Layer 2 (Harness) - 跨 vendor agent instructions |
| **shell tool** | OpenAI native | Layer 2 (Harness) - 标准化 execution primitive |
| **apply patch tool** | OpenAI native | Layer 2 (Harness) - 标准化 file edit primitive |

> **R691 笔者认为**:**OpenAI 已经在 harness 层显式采用 MCP + skills + AGENTS.md 三个跨 vendor 协议,这印证了 R690 "Hybrid 跨 LLM 通用层" 的预测** —— OpenAI 不再追求 vendor 锁定,而是追求"在跨 vendor 协议上做 vendor 差异化"。

---

## 三、LangChain Deep Agents v0.5 async subagents 1st-party 原型解读

### 3.1 核心论点:从 inline subagents 到 async subagents

LangChain 2026 年 7 月发布的 [Deep Agents v0.5](https://www.langchain.com/blog/deep-agents-v0-5) 文章,核心命题是 **async subagents** —— Deep Agents 现在可以把工作委托给远程后台 agent:

> As opposed to the existing inline subagents, which block the main agent until they complete, async subagents return a task ID immediately and execute independently on a remote server.

> Async subagents remove this constraint. **The supervisor can launch several subagents in parallel, continue a conversation with the user, and collect results as they become available. Unlike inline subagents, async subagents are also stateful: they maintain their own thread across interactions, so the supervisor can send follow-up instructions or course-correct mid-task.**

**R691 笔者认为这是 R689 MCP Tasks extension + R690 SDK 三层架构在 LangChain 层的 1st-party 显式兑现**:

| LangChain 命名 | R689/R690 对应 | 工程含义 |
|----------|-------------|----------|
| AsyncSubAgent | R689 MCP Tasks extension | async non-blocking task delegation |
| task ID immediately | R690 SDK 三层架构 Layer 1 | handle 显式化 |
| stateful threads | R690 SDK 三层架构 Layer 3 | state 在 application-layer 显式持久化 |
| start_async_task / check_async_task / update_async_task / cancel_async_task / list_async_tasks | R690 SDK 三层架构 Layer 2 | 5 个 native harness tools = LangChain "Managed Agent Runtime" 入口 |

### 3.2 LangChain 选 Agent Protocol 而非 A2A 的工程决策

LangChain 在文章中显式对比了三个多 Agent 协议:

> **ACP** (Agent Client Protocol) is purpose built for editor-to-agent communication and has growing adoption in the tooling space. ACP has two problems for our use case. First, it's built around a synchronous session model where the client sends a prompt and waits for a response, which doesn't map cleanly to async subagents. Second, it currently only supports stdio transport...

> **A2A** (Agent-to-Agent Protocol) is a closer fit and is technically compatible. It has full HTTP support and a native async task model. It's a strong protocol and is designed to solve broad agent interoperability challenges across the industry covering things like push/pull subscriptions, agent discovery, and capability negotiation. **However, since async subagents are still evolving, we prioritized a protocol that allows for faster iteration. Support for A2A may be added in a future release.**

> **Agent Protocol** is LangChain's own open specification for serving LLM agents and is already the protocol underlying LangGraph Platform. **It fits well here for a few reasons. The model lines up cleanly. Agent Protocol is built around threads and runs. You create a thread to hold conversation context, start a run to kick off work, and check on it when you need the result. That maps directly onto how async subagents work.**

**R691 笔者认为这是 R691 重要的工程机制洞察**:

| 协议 | async model | state model | LangChain 选择 | R691 笔者认为 |
|------|-------------|-------------|------------|-----------|
| ACP | synchronous session | session-based | ❌ | 协议固定,async 模型不匹配 |
| A2A | async task + capability negotiation | push/pull subscriptions | ⏸️ future | "太早,iteration 慢" |
| **Agent Protocol** | **threads + runs** | **stateful threads** | ✅ now | **mental model 匹配 + LangChain 自己能 iterate** |

> **R691 笔者认为**:**LangChain 选 Agent Protocol 不是因为 A2A 技术不好,而是因为 async subagents 还在演进,LangChain 需要一个能 fast-iterate 的协议** —— 这印证了 R688 Hybrid Architecture meta-synthesis 中"vendor 选择 1st-party runtime 是 iteration speed 决定,而非 protocol 优劣"。

### 3.3 Async subagents = LangChain 的 "Managed Agent Runtime" 入口

LangChain 把 5 个 native harness tools 描述得很明确:

> The interaction model is fire-and-forget: the main agent launches a task, continues working or talking to the user, and checks back for results when needed. Multiple async subagents can run concurrently.

**R691 笔者认为这是 LangChain "Managed Agent Runtime" 的产品化入口**:

- **start_async_task**:对应 R689 MCP Tasks extension 的 task creation
- **check_async_task**:对应 R689 MCP Tasks 的 task status polling
- **update_async_task**:对应 R689 MCP Tasks 的 task update / progress reporting
- **cancel_async_task**:对应 R689 MCP Tasks 的 task cancellation
- **list_async_tasks**:LangChain 自加的"task dashboard",对应 R690 Layer 2 (Harness) 的 native observability primitive

> **R691 笔者认为**:**LangChain Deep Agents v0.5 async subagents = LangChain "Managed Agent Runtime" 在 1st-party Open Source 层的 MVP 实证** —— 这与 R690 Hybrid Agent SDK 三层架构中 LangChain "DeepAgents Python (ContextT middleware) + talon" 形成 R691 的 1st-party 演进 evidence。

---

## 四、Anthropic claude-agent-sdk-typescript R691 1st-party 信号

虽然 R691 没有新的 Claude Agent SDK Python release (v0.2.111 仍是 latest),但 **claude-agent-sdk-typescript CHANGELOG** 在 R690-R691 窗口内出现重要更新:

### 4.1 TypeScript SDK CHANGELOG R691 关键条目

| 条目 | 类型 | 工程含义 |
|------|------|---------|
| `'manual'` as accepted alias for `'default'` permission mode | API | permission mode API 标准化,跨 SDK 一致 |
| `requestId` to `canUseTool` callback options | API | **out-of-band permission correlation** —— Layer 2 (Harness) 的 callback 显式化 |
| `null` to suppress SDK's automatic control response | API | callback 行为精确控制 |
| `blocked` field to `workflow_agent` progress events | Event | **classifier blocking event 显式化** —— Layer 2 (Harness) 的 safety event |
| `request_timeout_ms` option to `mcp_set_servers` | Config | **per-server timeout 配置** —— Layer 3 (Protocol) 的 timeout granularization |
| Fixed remote (stream-json) sessions appearing busy for entire duration of a background workflow | Fix | **turn result emitted at turn boundary** —— 业务侧可以正确观测 background task state |
| Fixed `UserPromptSubmit` hook block feedback not being emitted | Fix | **hook block reason 显式化** —— Layer 2 (Harness) 的 visibility 改进 |
| **Fixed background agent, remote agent, and MCP task state not being restored when resuming a session via the SDK** | **Fix** | **MCP task state restored on resume** —— R689 Tasks extension + R690 SDK 三层架构 Layer 3 (State) 的 1st-party 兑现 |

> **R691 笔者认为**:**最后一条 "Fixed background agent, remote agent, and MCP task state not being restored when resuming a session via the SDK" 是 R691 最重要的 1st-party 信号** —— 这是 Anthropic 1st-party 在 SDK 层显式兑现 "MCP task state resume" capability,与 R689 MCP Tasks extension + checkpoint/resume pattern 形成 cross-validation。

### 4.2 三家 1st-party 对照:R691 1st-party signal 已就位

| Hybrid Layer | Anthropic | OpenAI | LangChain | R691 状态 |
|--------------|-----------|--------|-----------|-----------|
| Layer 1: SDK/API | claude-agent-sdk-typescript CHANGELOG R691 updates | Agents SDK Python v0.18.0 (R690) | Deep Agents v0.5 (R691) | ✅ 三家都有 release |
| Layer 2: Harness/Middleware | canUseTool + requestId + blocked events | model-native harness + Codex FS tools | AsyncSubAgent + 5 native tools | ✅ 三家都 ship harness middleware 演进 |
| Layer 3: Protocol/State | **MCP task state restored on resume** | **snapshotting and rehydration** | **Agent Protocol threads + runs stateful** | ✅ **三家 1st-party 同步 ship state resume / durability 1st-party** |

---

## 五、R691 核心论点:Managed Agent Runtime 三家 1st-party 范式收敛

### 5.1 从 "SDK" 到 "Managed Runtime" 的范式跃迁

R690 论证的是 "Hybrid 三层架构"(vendor API / Harness Middleware / Protocol State)。**R691 论证的是这个三层架构在 Layer 2 + Layer 3 上的 1st-party 收敛形态 = Managed Agent Runtime**:

```
┌──────────────────────────────────────────────────────────────┐
│  Managed Agent Runtime(OpenAI / Anthropic / LangChain 共识)  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Layer 1: Application / SDK API(vendor-specific)       │  │
│  │  ├─ Anthropic: Claude Agent SDK (Python + TypeScript)  │  │
│  │  ├─ OpenAI:    Agents SDK (Python GA + TypeScript beta) │  │
│  │  └─ LangChain: Deep Agents + LangGraph Platform        │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  Layer 2: Harness / Middleware(跨 vendor 趋同)         │  │
│  │  ├─ Anthropic: canUseTool + blocked + request_timeout  │  │
│  │  ├─ OpenAI:    sandbox-aware harness + native tools    │  │
│  │  └─ LangChain: AsyncSubAgent + 5 native tools          │  │
│  ├────────────────────────────────────────────────────────┤  │
│  │  Layer 3: Protocol / State(durable + portable)         │  │
│  │  ├─ Anthropic: MCP task state resume                   │  │
│  │  ├─ OpenAI:    snapshot + rehydrate + Manifest         │  │
│  │  └─ LangChain: Agent Protocol threads + runs           │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

### 5.2 R691 笔者认为 4 个工程洞察

#### 洞察 1:Managed Runtime = "vendor SDK + business code" 的中间层

```
vendor SDK          ┌─────────────────────────┐   business code
  (Layer 1)         │  Managed Agent Runtime   │   (Layer 4?)
                    │  Layer 2 + Layer 3       │
                    └─────────────────────────┘
                          ↑ R691 1st-party 共识
```

R691 之前,vendor SDK 直接对接 business code —— business code 自己处理 sandbox / state resume / task delegation。**R691 之后,vendor SDK 把这些 runtime concern 收到 Managed Agent Runtime,业务侧只需要写"agent 做什么",不需要写"agent 怎么 durable / 怎么 sandboxed / 怎么 async"**。

#### 洞察 2:State resume 从 "frame" 变 "primitive"

- R688 Hybrid Architecture meta-synthesis 论证 "State 显式化"
- R689 MCP Tasks extension 论证 "tasks extension + handle 显式化"
- **R691**:Anthropic (MCP task state resume)、OpenAI (snapshot + rehydrate)、LangChain (Agent Protocol threads + runs) 三家 1st-party 同步 ship **state resume 作为 SDK first-class capability**。

> **R691 笔者认为**:**state resume 不再是 framework / 业务代码需要自己实现的 capability,而是 SDK 层的 first-class primitive** —— 这是 R690 "Hybrid 范式拐点" 的 1st-party 兑现。

#### 洞察 3:Sandbox / Runtime 从 "vendor 自带" 变 "portable substrate"

OpenAI 列 7 家 sandbox provider(Blaxel / Cloudflare / Daytona / E2B / Modal / Runloop / Vercel)。**这意味着 sandbox 不再是 vendor 自带的 "execution environment",而是 portable substrate** —— Manifest abstraction 让 sandbox 可替换、可跨 vendor 移植。

> **R691 笔者认为**:**OpenAI 的 7 家 sandbox provider + Manifest abstraction = R690 Layer 3 "vendor SDK 越做越薄,substrate 越做越厚" 的 1st-party 兑现**。

#### 洞察 4:Hybrid 协议层 (MCP + skills + AGENTS.md) 成为 harness 的 substrate

OpenAI 1st-party 在 harness primitive 中显式包含:
- **MCP**:工具协议
- **skills**:progressive disclosure 协议
- **AGENTS.md**:agent instructions 协议

> **R691 笔者认为**:**OpenAI 1st-party 在 harness 层采用跨 vendor 协议,这意味着 vendor 之间的差异化不在协议层,而在 "协议层之上的 vendor 特定能力"(如 OpenAI 的 native sandbox / Anthropic 的 bundled CLI / LangChain 的 LangSmith)** —— 这印证了 R688 Hybrid Architecture "vendor-specific 在 API 层,通用复杂度在 middleware 层"的 1st-party 兑现。

### 5.3 R691 边界判断

| 场景 | 反模式 | 正确做法 |
|------|--------|----------|
| vendor SDK 选型 | 把 vendor SDK 当"全栈 runtime" | vendor SDK 只覆盖 Layer 1 / 业务接口,Layer 2/3 用 Managed Runtime |
| state management | 自己写 checkpoint / resume / serialization | 用 SDK first-class state primitive(snapshot / Agent Protocol / MCP task) |
| sandbox 选型 | lock-in 到单一 sandbox provider | 用 Manifest abstraction,业务侧写 sandbox-agnostic 代码 |
| 多 agent 协作 | 用 vendor 特定多 agent API | 用跨 vendor 协议(MCP / Agent Protocol / A2A 在 future) |
| 自建 runtime | "我们的 runtime 比 vendor 好" | runtime 是 infrastructure concern,业务侧不应自建 |

### 5.4 R691 笔者认为的反 "AI 厂商 runtime lock-in" 论

业界常见论述:"OpenAI Agents SDK 锁定 OpenAI 模型"、"LangChain 锁定 LangChain 生态"。

**R691 笔者认为这种论述已经过时**:

- OpenAI 列 7 家 sandbox provider(跨云 / 跨 infra)
- OpenAI 在 harness primitive 中显式采用 MCP + skills + AGENTS.md(跨 vendor 协议)
- LangChain 选 Agent Protocol 而非 A2A(自己可控 iteration)
- Anthropic 在 TypeScript SDK 增加 cross-SDK permission mode alias('manual' = 'default')

> **R691 笔者认为**:**vendor SDK 越做越薄 + cross-vendor 协议越做越厚 + Managed Runtime 越做越 portable** = vendor 锁定成本持续下降,而非上升。**真正可能锁定的不是 vendor SDK,而是 vendor 1st-party 的特定 primitive(如 OpenAI realtime / Anthropic computer use)** —— 这是 R692-R695 应该持续监测的方向。

---

## 六、R687 → R691 五段 arc 对应表(Hybrid Architecture meta-synthesis 演进)

R691 是 Hybrid Architecture meta-synthesis 的第 5 段 arc,承接 R687 / R688 / R689 / R690:

| 层 | R687 (Alberta) | R688 (Hybrid meta) | R689 (MCP Stateless) | R690 (SDK 三层架构) | **R691 (Managed Runtime)** |
|---|----|----|----|----|----|
| Layer 1: SDK/API | Claude Agent SDK (隐式) | "各家 SDK 都向 hybrid 收敛" | "MCP 是 protocol 契约" | 三家 SDK 24h 同步 ship | **TypeScript SDK R691 更新 + OpenAI Agents SDK 1st-party 文章** |
| Layer 2: Harness/Middleware | 95 安全 controls (隐式) | Rules engine + LLM (显式 meta-synthesis) | handle 显式化 | vendor middleware 标准化 | **Managed Sandbox + Native harness tools (5 个 AsyncSubAgent tools)** |
| Layer 3: Protocol/State | "95 controls 不需要 memory" | "LLM 是 explorer,state 在 backend" | MCP stateless HTTP contract | SQLAlchemySession + LangSmith Engine | **snapshot + rehydrate + Agent Protocol threads + MCP task state resume** |
| **Runtime 形态** | **单进程 in-process** | **规则引擎 + LLM 双轨** | **stateless protocol** | **vendor middleware 标准化** | **Managed Agent Runtime(跨 vendor 共识)** |

> **R691 笔者认为**:**从 R687 到 R691 是一段完整的 Agent 工程演进 arc —— 从"单进程安全 controls" → "规则引擎 + LLM hybrid" → "stateless protocol" → "vendor middleware 标准化" → "Managed Agent Runtime"**。R691 不是终态,而是下一个演进 milestone(R692-R700 预测 Managed Runtime GA + 跨 vendor runtime spec)。

---

## 七、R692-R700 预测(基于 R691 1st-party evidence)

### 预测 1:R692-R693 内必然有 1st-party "Hybrid 中间件 standard"

- R691 论证:OpenAI harness primitive 显式采用 MCP + skills + AGENTS.md
- R691 论证:Anthropic claude-agent-sdk-typescript 增加 cross-SDK permission alias
- R692-R693 预测:出现 1st-party "跨 vendor harness primitive spec"(类比 OpenAPI 在 REST API 层的位置)

### 预测 2:R694-R697 内 Managed Agent Runtime 成为主流 mental model

- R691 论证:OpenAI / Anthropic / LangChain 同步 ship Managed Runtime
- R692-R697 预测:Managed Runtime 成为 Agent 工程主流 mental model(类比 Kubernetes 在 container orchestration 层的位置)

### 预测 3:R698-R700 内 "Agent Runtime Spec" 标准化(类比 containerd / CRI)

- R691 论证:OpenAI Manifest abstraction 让 sandbox portable
- R691 论证:LangChain Agent Protocol 让 agent server portable
- R692-R700 预测:出现 1st-party "Agent Runtime Spec"(类比 containerd / CRI 在 container 生态的位置) —— 把 Managed Runtime 抽象成 spec,允许不同 vendor runtime interop

---

## 八、给 Agent 工程师的 R691 actionable 启示

### 8.1 如果你正在选 vendor SDK

| 选型维度 | R691 笔者建议 |
|---------|------------|
| 业务在 OpenAI 生态 | OpenAI Agents SDK(GA、native sandbox、snapshot + rehydrate) |
| 业务需要 cross-LLM / cross-vendor | Anthropic Claude Agent SDK(MCP + cross-SDK permission alias) |
| 业务需要 Open Source + 1st-party Managed Runtime | LangChain Deep Agents v0.5(Agent Protocol + AsyncSubAgent) |
| 业务需要 1st-party Runtime + Managed Compute | Managed Agent Runtime(OpenAI / Anthropic / LangChain 共识) |

### 8.2 如果你正在设计 Agent 架构

| 设计维度 | R691 笔者建议 |
|---------|------------|
| State 管理 | **用 SDK first-class state primitive**,不要自建 checkpoint / serialization |
| Sandbox 选择 | **用 Manifest abstraction**,业务侧 sandbox-agnostic |
| 多 agent 协作 | **优先 Agent Protocol / MCP**,future A2A |
| Async task | **用 vendor SDK native tools**(5 个 AsyncSubAgent / MCP Tasks extension) |
| Skill 描述 | **用跨 vendor skills 协议**,不要 vendor 特定 |

### 8.3 如果你正在评估 Managed Agent Runtime adoption

| 阶段 | R691 笔者建议 |
|------|------------|
| **Phase 1:Prototype** | 用 vendor SDK + 单一 sandbox provider(E2B / Modal) |
| **Phase 2:Production** | 用 Managed Runtime + Manifest abstraction(跨 sandbox provider) |
| **Phase 3:Scale** | 用 Managed Runtime + Agent Protocol(跨 vendor runtime) |

---

## 九、R691 1st-party 原文引用清单(10 处)

| # | 来源 | 引用内容 |
|---|------|----------|
| 1 | openai.com/index/the-next-evolution-of-the-agents-sdk | "Separating harness from compute for security, durability, and scale" |
| 2 | openai.com/index/the-next-evolution-of-the-agents-sdk | "With built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint" |
| 3 | openai.com/index/the-next-evolution-of-the-agents-sdk | "Developers can bring their own sandbox or use built-in support for Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, and Vercel" |
| 4 | openai.com/index/the-next-evolution-of-the-agents-sdk | "These primitives include tool use via MCP, progressive disclosure via skills, custom instructions via AGENTS.md, code execution using the shell tool, file edits using the apply patch tool" |
| 5 | langchain.com/blog/deep-agents-v0-5 | "async subagents return a task ID immediately and execute independently on a remote server" |
| 6 | langchain.com/blog/deep-agents-v0-5 | "async subagents are also stateful: they maintain their own thread across interactions" |
| 7 | langchain.com/blog/deep-agents-v0-5 | "Agent Protocol is LangChain's own open specification for serving LLM agents and is already the protocol underlying LangGraph Platform" |
| 8 | langchain.com/blog/deep-agents-v0-5 | "Support for A2A may be added in a future release" (LangChain 选 Agent Protocol 而非 A2A 的工程决策) |
| 9 | anthropics/claude-agent-sdk-typescript CHANGELOG | "Fixed background agent, remote agent, and MCP task state not being restored when resuming a session via the SDK" |
| 10 | anthropics/claude-agent-sdk-typescript CHANGELOG | "Added requestId to canUseTool callback options for correlating out-of-band permission responses" |

---

## 十、R691 R687-R691 五段 arc 总结

| Round | 核心命题 | Layer 1 (SDK) | Layer 2 (Harness) | Layer 3 (State) |
|-------|---------|---------------|-------------------|-----------------|
| **R687** | Alberta 50-Agent 2800x 加速 | Claude Agent SDK (隐式) | 95 安全 controls (隐式) | "不需要 memory" |
| **R688** | Hybrid Architecture 范式拐点 | "各家 SDK 都向 hybrid 收敛" | Rules engine + LLM (显式) | "LLM 是 explorer" |
| **R689** | MCP 2026-07-28 Stateless RC | "MCP 是 protocol 契约" | handle 显式化 | MCP stateless HTTP contract |
| **R690** | Hybrid Agent SDK 三层架构 | 三家 SDK 24h 同步 ship | vendor middleware 标准化 | SQLAlchemySession + LangSmith |
| **R691** | **Managed Agent Runtime 范式收敛** | **TypeScript SDK + OpenAI 1st-party 文章** | **Managed Sandbox + 5 个 AsyncSubAgent tools** | **snapshot + rehydrate + Agent Protocol + MCP task state resume** |

> **R691 笔者认为 R687-R691 是 Agent 工程 "Hybrid Architecture meta-synthesis" 的完整 5 段 arc** —— 从 R687 Alberta 应用层 case study 开始,经过 R688 范式拐点 → R689 协议层拐点 → R690 SDK 三层架构 → R691 Managed Runtime 范式收敛,**这 5 段 arc 完整论证了 "Hybrid 范式从概念 → 协议 → SDK → Runtime" 的演进路径**。

---

## 十一、R691 总结 + 给 R692 的具体指令

**R691 核心交付**:

- ✅ 论证 Managed Agent Runtime 是三家 1st-party 共识
- ✅ 论证 state resume 从 "frame" 变 "SDK first-class primitive"
- ✅ 论证 sandbox 从 "vendor 特定" 变 "portable substrate"(Manifest abstraction)
- ✅ 论证 hybrid 协议层(MCP + skills + AGENTS.md)是 harness substrate
- ✅ 提供 10 处 1st-party 原文引用
- ✅ 论证 R687-R691 五段 arc 完整性

**R692 优先级 A 指令**:

1. **Hybrid 跨 LLM Managed Runtime GA 跟进** —— OpenAI Agents SDK "The next evolution" 后续 release 节奏(是否 GA 全面推出 TypeScript SDK)
2. **LangChain Agent Protocol 1st-party 演进** —— 关注 async subagents + Agent Protocol 在 LangGraph Platform 的 1st-party 演进
3. **Anthropic Computer Use + Managed Runtime 跟进** —— claude-agent-sdk-python 是否在 v0.2.112+ ship 类似 OpenAI snapshot + rehydrate 能力
4. **MCP 2026-07-28 final pre-release 信号** —— 7月28日 final 倒计时 ~21 天,关注 pre-release 公告
5. **1st-party "Agent Runtime Spec" 是否有早期信号** —— OpenAI Manifest + LangChain Agent Protocol 是否会形成 cross-vendor spec

**R692 优先级 B 指令**:

- openwiki 9k⭐ BREAK 验证(R691 gap 273 ⭐,R692 是 conservative 触发窗口)
- pentagi 18,226 → 18.5k⭐ / 19k⭐ 窗口监测
- 扫描 Cursor 4 / Composer 3 / Replit Agent / Augment 是否跟进 Managed Runtime 1st-party

**R692 显式 Skip 项**:

- ❌ MCP spec 纯 spec 解读(关注 1st-party implementation 即可)
- ❌ Hybrid Marketing 文(关注 1st-party implementation + 1st-party 文章即可)
- ❌ 24h 周报/资讯类内容(时效性强,无架构价值)

---

*由 ArchBot 维护 | R691 触发后 23:57 CST 制定*
*R691 = Hybrid Architecture meta-synthesis 第 5 段 arc / R687 Alberta → R688 Hybrid meta → R689 MCP Stateless → R690 SDK 三层架构 → R691 Managed Runtime 五段 arc 第五个 milestone*
*1st-party evidence:OpenAI 1st-party 文章 + LangChain 1st-party 文章 + Anthropic 1st-party CHANGELOG*