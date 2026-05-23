# open-multi-agent：用 Goal 取代 Graph 的 TypeScript 多智能体编排框架

> **核心命题**：大多数多智能体框架要求开发者先画好任务图再执行——这在理论上优雅，在实践中却限制了智能体的自主决策能力。open-multi-agent 的答案是：告诉它目标，它自己生成 DAG，然后执行。

## 一、解决了什么问题

多智能体编排有一个根本矛盾：**你需要提前知道任务如何分解，才能画好图；但如果你已经知道如何分解任务，为什么要委托给智能体？**

传统框架（LangGraph、CrewAI 等）采用的是"图优先"（Graph-First）设计：

```python
# 你需要先定义好任务依赖关系
graph = Graph()
graph.add_node("architect", architect_agent)
graph.add_node("developer", developer_agent)
graph.add_edge("architect", "developer")  # 你来决定执行顺序
```

open-multi-agent 反其道而行之，采用**目标优先**（Goal-First）设计：

```typescript
const team = orchestrator.createTeam('api-team', {
  name: 'api-team',
  agents: [
    { name: 'architect', model: 'claude-sonnet-4-6', systemPrompt: 'Design clean API contracts.', tools: ['file_write'] },
    { name: 'developer', model: 'claude-sonnet-4-6', systemPrompt: 'Implement runnable TypeScript.', tools: ['bash', 'file_read', 'file_write', 'file_edit'] },
    { name: 'reviewer', model: 'claude-sonnet-4-6', systemPrompt: 'Review correctness and security.', tools: ['file_read', 'grep'] },
  ],
  sharedMemory: true
})

// 你只需要描述目标，框架自己生成 DAG
const result = await orchestrator.runTeam(team, 'Create a REST API for a todo list in /tmp/todo-api/')
```

**这个转变的意义**：在真实的工程场景中，任务分解方式往往取决于执行过程中的中间状态。提前画好的图是静态的，而 coordinator agent 生成的 DAG 是动态的——它可以根据当前执行结果调整后续任务的优先级和依赖关系。

> 引用原文："open-multi-agent is a multi-agent orchestration framework for TypeScript backends. Give it a goal; a coordinator agent decomposes it into a task DAG, parallelizes independents, and synthesizes the result." — [GitHub README](https://github.com/open-multi-agent/open-multi-agent)

## 二、核心设计决策

### 2.1 三运行时依赖：Node.js + 任一模型 API + TypeScript

相比之下，LangGraph 需要 Python 环境 + LangChain + 各种适配器；CrewAI 需要 Python + 多个依赖。open-multi-agent 明确标榜"three runtime dependencies"，这是有意为之的工程决策——对于需要在 Node.js 生态中集成 AI 能力的团队（特别是使用 TypeScript 的全栈团队），这是最低门槛。

### 2.2 自动 DAG 生成 = coordinator agent 模式

框架内置一个 **coordinator agent**，负责：

1. **分解目标**：将用户提供的 Goal 拆解为具体任务
2. **识别依赖**：判断哪些任务可以并行，哪些必须等待前置任务完成
3. **并行调度**：独立任务自动并行执行
4. **结果合成**：协调者汇总所有子任务输出，产生最终结果

```
agent_start coordinator
task_start design-api        → architect agent
task_complete design-api
task_start implement-handlers → developer agent（并行）
task_start scaffold-tests   → developer agent（并行）
task_complete implement-handlers
task_complete scaffold-tests
task_start review-code      → reviewer agent（等待实现完成后执行）
task_complete review-code
agent_complete coordinator   → 合成最终结果
```

这个模式与 Claude Code 的 internal multi-agent research system 有相似的设计哲学（Anthropic 在2025年6月披露过他们的多智能体研究系统），但 open-multi-agent 将其产品化为通用的开源框架。

### 2.3 10个内置 Provider + MCP 支持

框架内置支持：

| 类别 | Provider |
|------|---------|
| 主流闭源 | Anthropic, OpenAI, Azure, Bedrock, Gemini, Grok |
| 中国市场 | DeepSeek, MiniMax, Qiniu |
| 开发工具 | Copilot |
| 自托管 | Ollama / vLLM / LM Studio / OpenRouter / Groq（OpenAI兼容接口）|

> 引用原文："10 built-in: Anthropic, OpenAI, Azure, Bedrock, Gemini, Grok, DeepSeek, MiniMax, Qiniu, Copilot. Ollama / vLLM / LM Studio / OpenRouter / Groq via OpenAI-compatible." — [GitHub README](https://github.com/open-multi-agent/open-multi-agent)

MCP 支持通过 `connectMCPTools()` 实现，支持 stdio MCP 服务器接入。

### 2.4 流式 + 可观测性

`onProgress` 回调提供实时事件流——每次 task start/complete、agent start/complete 都会触发事件。这个设计让开发者可以在 CLI/UI 上渲染实时的 DAG 执行状态，而不是等到全部完成后才能看到结果。

```typescript
const orchestrator = new OpenMultiAgent({
  defaultModel: 'claude-sonnet-4-6',
  onProgress: (event) => console.log(event.type, event.task ?? event.agent ?? ''),
})
```

## 三、与同类项目的对比

| 维度 | open-multi-agent | LangGraph | CrewAI | Symphony |
|------|-----------------|-----------|--------|----------|
| 语言 | TypeScript | Python | Python | Rust |
| 设计模式 | Goal-First（自动DAG）| Graph-First（手动定义）| Flow-First（Role-Based）| Task-First（手动任务）|
| 依赖数 | 3 | 多个 | 多个 | 多个 |
| Provider 数 | 10+ | 多个 | 中等 | 较少 |
| MCP 支持 | ✅ | ✅ | ✅ | ✅ |
| Stars | 6,156 | 30K+ | 30K+ | 24K+ |
| 上线时间 | 2026-03（较新）| 成熟 | 成熟 | 较新 |

**核心差异**：LangGraph 和 CrewAI 的用户需要自己设计任务图，open-multi-agent 把这个职责交给了 coordinator agent。对于快速原型和动态任务场景，这是一个显著的时间节省；对于需要精确控制任务拓扑的场景，可能需要额外的 override 机制（框架也提供了 `runTasks()` 和 `planOnly` 选项来处理这种情况）。

## 四、适合谁用

**适合**：
- TypeScript 生态的团队（Node.js 后端、前端、全栈）
- 需要快速将多智能体能力集成到现有 TypeScript 应用的开发者
- 希望智能体自动处理任务分解，而不是手动设计 DAG 的场景
- 需要同时调用多个不同模型提供商的项目

**不适合**：
- Python 生态优先的团队（LangGraph/CrewAI 更成熟）
- 需要精细控制任务执行拓扑的复杂场景
- 需要在生产环境中深度定制协调策略的企业级应用

## 五、关键数据

| 指标 | 数值 |
|------|------|
| GitHub Stars | 6,156 |
| 语言 | TypeScript（98.3%），JavaScript（1.7%）|
| License | MIT |
| 上线时间 | 2026-03-31 |
| 最新版本 | v1.4.0（2026-05-09）|
| 贡献者数 | 40 |
| 运行时依赖 | 3 |
| 内置 Provider | 10+ |

## 六、快速上手

```bash
npm install @open-multi-agent/core

# 或 clone 并运行示例
git clone https://github.com/open-multi-agent/open-multi-agent && cd open-multi-agent
npm install
export ANTHROPIC_API_KEY=sk-...
npx tsx examples/basics/team-collaboration.ts
```

**如果你只想看 coordinator 生成的 DAG（不执行）**：

```typescript
const plan = await orchestrator.runTeam(team, goal, { planOnly: true })
// 查看 plan 了解框架如何分解你的任务
```

---

**引用来源**：
- [open-multi-agent GitHub README](https://github.com/open-multi-agent/open-multi-agent)
- [open-multi-agent NPM Package](https://www.npmjs.com/package/@open-multi-agent/core)
- [Multi-Agent Orchestration Patterns - Anthropic Engineering](https://www.anthropic.com/engineering/how-we-built-our-multi-agent-research-system)

**关联文章**：[从 Claude Code 质量事件看 Agent 工程的核心教训：问题不在模型，在 Harness](./harness/anthropic-claude-code-quality-regression-harness-lessons-2026.md)

**标签**：`multi-agent` `orchestration` `typescript` `open-multi-agent` `goal-driven`
**分类**：`projects/`
**推荐关联**：AI Coding + Orchestration 方向，与 Claude Code Harness 文章形成"框架 vs 控制层"的互补