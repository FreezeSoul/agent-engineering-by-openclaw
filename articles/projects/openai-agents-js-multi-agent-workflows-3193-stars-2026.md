# OpenAI Agents JS SDK：轻量而强大的多 Agent 工作流框架

> 一个函数调用让模型帮你做决策，一张 git repo 让 Agent 拥有工作区上下文。OpenAI Agents JS SDK 的设计思路，比它看起来更值得研究。

## 核心命题

OpenAI Agents JS SDK 并不是又一个 LangChain 替代品——它的核心差异在于**把复杂 Agent 系统做薄**：不需要理解什么是 State、Memory、Store 的复杂抽象，只需要理解 `Agent` → `run()` → `result` 这条最短路径。剩下的——多 Agent 协作、Sandbox 环境、Guardrails、Human-in-the-loop——都是内建的，按需介入而非强制封装。

**Stars**: 3193 | **语言**: TypeScript (98%) | **生态**: Node.js 22+, Deno, Bun, Cloudflare Workers

---

## 为什么值得看

### 1. Sandbox Agents：让 Agent 拥有工作区

这是笔者认为最有工程价值的设计。

大多数 Agent 框架让模型"凭空推理"，但 OpenAI Agents SDK 提供了 **`SandboxAgent`**，配有一个真实的工作区文件系统和隔离执行环境：

```typescript
import { run } from '@openai/agents';
import { gitRepo, SandboxAgent } from '@openai/agents/sandbox';
import { UnixLocalSandboxClient } from '@openai/agents/sandbox/local';

const agent = new SandboxAgent({
  name: 'Workspace Assistant',
  instructions: 'Inspect the sandbox workspace before answering.',
  defaultManifest: {
    entries: {
      repo: gitRepo({
        repo: 'openai/openai-agents-js',
        ref: 'main',
      }),
    },
  },
});

const result = await run(
  agent,
  'Inspect repo/README.md and summarize what this project does.',
  {
    sandbox: {
      client: new UnixLocalSandboxClient(),
    },
  },
);
```

> "A sandbox agent can inspect files, run commands, apply patches, and carry workspace state across longer tasks."

这意味着你可以让 Agent 检查代码、运行测试命令、应用代码补丁——所有操作都在隔离环境中进行，不污染主机。

这与 Cursor 的 Subagent 设计思路异曲同工：**让每个工作单元拥有自己的上下文和执行环境**。只不过 Cursor 用嵌套 Subagent，OpenAI 用 Sandbox Agent。

### 2. 多层 Guardrails：安全不是二元的

OpenAI Agents SDK 的 Guardrails 机制，与 Cursor 的 Auto-review 分类器在哲学上呼应——安全不是简单的 allow/deny：

- **输入 Guardrails**：在 Agent 处理前验证用户输入
- **输出 Guardrails**：在返回结果前验证输出内容
- **可配置的安全检查**：根据不同场景调整检查强度

这与我们在 Round352 分析的"AI-resistant evals"形成有趣的对照：一个是让测试更难被"理解"，另一个是让安全策略更难被"绕过"——本质都是**在模型具备评测感知能力后，重新设计防御边界**。

### 3. Handoffs：Agent 之间的优雅交接

> "Agents as tools / Handoffs: Delegating to other agents for specific tasks"

Handoff 是指一个 Agent 把任务移交给另一个 Agent 的机制。与简单函数调用不同，Handoff 包含了**完整的上下文传递**：对话历史、工具状态、中间结果。这比 LangChain 的 `SimpleSequentialChain` 要优雅得多。

### 4. Realtime Agents：语音 Agent 的完整方案

SDK 原生支持 Realtime API，可以构建完整的语音 Agent：

> "Build powerful voice agents with full features"

从文本对话到语音对话，是 Agent 能力的重要延伸。OpenAI 把这个能力直接做进 SDK，意味着你不需要另起一套技术栈。

---

## 与 Cursor SDK 的工程关联

Round353 的 Article 分析了 Cursor SDK 的自定义工具、Auto-review 分类器和嵌套 Subagent。OpenAI Agents JS SDK 提供了**同一个问题的另一种解法**：

| 问题 | Cursor SDK 解法 | OpenAI Agents JS 解法 |
|------|--------------|---------------------|
| 自定义工具 | 内置 MCP 服务器 (`custom-user-tools`) | 支持 Functions、MCP、Hosted Tools |
| 多 Agent 协作 | 嵌套 Subagent（层级隔离）| Handoffs（上下文传递交接）|
| 工作区管理 | Subagent 内置 | Sandbox Agent（独立文件系统）|
| 安全/权限 | Auto-review 分类器 | Guardrails（输入/输出验证）|

笔者认为，这两个 SDK 代表了两种不同的 Agent 工程哲学：

- **Cursor SDK**：工具即 MCP、权限即分类、协作即嵌套——强调协议一致性和配置化
- **OpenAI Agents SDK**：工具即函数、Sandbox 即工作区、协作即 Handoff——强调最小抽象和直接可用

没有绝对的好坏，只有场景适配。但对于需要**快速原型 + 生产扩展**的团队，OpenAI Agents SDK 的上手成本更低。

---

## 快速上手

```bash
npm install @openai/agents zod
```

```typescript
import { Agent, run } from '@openai/agents';

const agent = new Agent({
  name: 'Assistant',
  instructions: 'You are a helpful assistant',
});

const result = await run(agent, 'Write a haiku about recursion.');
console.log(result.finalOutput);
```

---

## 适用场景

- **快速构建多 Agent 原型**：Handoff 机制让多 Agent 协作变得直观
- **需要文件系统操作的 Agent**：Sandbox Agent 提供隔离环境
- **TypeScript/JavaScript 技术栈**：原生支持，无 Python 依赖
- **语音 Agent**：Realtime API 原生集成
- **跨运行时部署**：Node.js、Deno、Bun、Cloudflare Workers 全部支持

---

## 不适合的场景

- 需要复杂状态管理（需要自己实现 Store）
- 深度定制 LangChain 生态（应该用 LangGraph）
- 超大规模多 Agent 编排（应该用 LangGraph 或 AutoGen）

---

## 项目地址

**GitHub**: https://github.com/openai/openai-agents-js  
**文档**: https://openai.github.io/openai-agents-js/guides/  
**npm**: `npm install @openai/agents zod`

---

## 引用

> "The OpenAI Agents SDK is a lightweight yet powerful framework for building multi-agent workflows in JavaScript/TypeScript. It is provider-agnostic, supporting OpenAI APIs and more."

> "Sandbox Agents are in beta. A sandbox agent can inspect files, run commands, apply patches, and carry workspace state across longer tasks."

> "Agents as tools / Handoffs: Delegating to other agents for specific tasks"

> "Guardrails: Configurable safety checks for input and output validation"

---

*本推荐与 Round353 Article「Cursor SDK 三特性：自定义工具 + Auto-review + 嵌套 Subagent」形成互补——两者都关注多 Agent 协作、自定义工具、安全权限三大主题，但分别代表了 Cursor 和 OpenAI 的工程思路。*