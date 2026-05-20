# open-multi-agent：让开发者描述目标，而非设计图

> "Your engineers describe the goal, not the graph."

## 一句话评价

**open-multi-agent** 是一个 TypeScript 原生的多 Agent 编排框架，它最核心的设计哲学是：**开发者只需要描述最终目标，框架自动将目标分解为任务 DAG 并行执行**。3 个运行时依赖，直接嵌入 Node.js 后端，MIT 协议开源。

---

## 为什么这个项目值得关注

### 痛点：多 Agent 编排的认知负担

当前的 Agent 编排框架（LangGraph、Mastra、CrewAI）要求开发者在开始前就设计好完整的任务图：
- 定义节点（哪些 Agent）
- 定义边（Agent 之间的依赖关系）
- 定义条件路由（何时走哪个分支）

这意味着**在写第一行代码之前**，开发者必须对整个工作流有完整的mental model。但在真实场景中，很多工作流的细节是在执行过程中才逐渐清晰的。

### open-multi-agent 的答案：Goal-First

```
// 你只需要描述目标
const result = await orchestrator.runTeam(team, 
  'Create a REST API for a todo list in /tmp/todo-api/'
)

// Coordinator 自动完成：
// 1. 分解目标为任务 DAG
// 2. 识别可并行的独立任务
// 3. 按依赖顺序执行
// 4. 汇总结果
```

这与 OpenAI Workspace Agents 的思路不谋而合——**描述期望的结果，而不是规定执行路径**。

---

## 核心特性解析

### 1. 三种运行模式

| 模式 | 方法 | 适用场景 |
|------|------|---------|
| **Single Agent** | `runAgent()` | 单一 Agent 处理单一任务 |
| **Auto Team** | `runTeam()` | 描述目标，Coordinator 自动规划 |
| **Explicit Pipeline** | `runTasks()` | 你定义任务图，框架负责执行 |

```typescript
// 模式 1：单 Agent
const result = await orchestrator.runAgent(agent, 'Summarize this report')

// 模式 2：自动团队协作
const team = orchestrator.createTeam('api-team', { agents, sharedMemory: true })
const result = await orchestrator.runTeam(team, 'Create a REST API for a todo list')

// 模式 3：显式任务管道
const plan = await orchestrator.runTasks(team, taskGraph, { planOnly: true })
```

### 2. Goal-First 的 Coordinator

Coordinator 是 open-multi-agent 的核心创新。它不是执行预定义的工作流，而是：

1. **理解目标**：分析用户的自然语言描述
2. **任务分解**：将目标拆解为可执行的子任务
3. **依赖分析**：构建任务 DAG
4. **并行优化**：识别可同时执行的任务
5. **结果汇总**：合并各 Agent 的输出

```typescript
// Coordinator 的输出示例
agent_start coordinator
task_start design-api          // 1. 协调者规划
task_complete design-api
task_start implement-handlers  // 2. 并行执行独立任务
task_start scaffold-tests
task_complete scaffold-tests
task_complete implement-handlers
task_start review-code         // 3. 依赖任务完成后执行
task_complete review-code
agent_complete coordinator     // 4. 汇总结果
```

**与 OpenAI Workspace Agents 的对比**：

| 维度 | OpenAI Workspace Agents | open-multi-agent |
|------|------------------------|------------------|
| 目标分解 | 预设模板 + 自然语言 | 动态 Coordinator |
| 适用场景 | 企业级标准化工作流 | 开发者自定义工作流 |
| 平台 | OpenAI 托管 | 自托管 |
| 治理 | 企业级 RBAC | 开发者可扩展 |

### 3. 生产级工具链

| 能力 | 实现 |
|------|------|
| **Token 预算控制** | `maxTokenBudget` 硬上限 |
| **上下文管理** | 滑动窗口 / 摘要 / 压缩 / 自定义 |
| **工具输出裁剪** | `maxToolOutputChars` 按工具配置 |
| **失败重试** | `maxRetries` + `retryDelayMs` + 指数退避 |
| **循环检测** | `loopDetection` with 自定义处理器 |
| **可观测性** | `onProgress` / `onTrace` / DAG 渲染 |

### 4. 10+ Provider 支持

| 类别 | 支持 Provider |
|------|--------------|
| **官方支持** | Anthropic, OpenAI, Azure OpenAI, GitHub Copilot, xAI Grok, DeepSeek, MiniMax, Qiniu, AWS Bedrock |
| **OpenAI 兼容** | Ollama, vLLM, LM Studio, OpenRouter, Groq |
| **Vercel AI SDK** | 60+ 模型和部署目标 |

### 5. MCP 集成

```typescript
import { connectMCPTools } from '@open-multi-agent/core'

// 连接 MCP 服务器到 Agent
const agent = {
  name: 'github-agent',
  model: 'claude-sonnet-4-6',
  tools: await connectMCPTools('./mcp-servers/github')
}
```

---

## 与主流框架的对比

| 需求 | 推荐框架 | 原因 |
|------|---------|------|
| 固定生产拓扑 +成熟的 checkpoint | LangGraph JS | 声明式图结构更适合稳定的工作流 |
| 显式 Supervisor + 手绘工作流 | Mastra | 高度可控，适合复杂条件分支 |
| Python 技术栈 + 成熟生态 | CrewAI | Python 首选，多 Agent 经验丰富 |
| AI 应用工具链 + 广泛模型支持 | Vercel AI SDK | 应用层 + 单 Agent 调用 |
| **TypeScript + 目标驱动自动规划** | **open-multi-agent** | **3 个依赖，直接嵌入后端** |

---

## 典型应用场景

### 场景 1：代码审查 DAG

```
        ┌─────────────────────────────────┐
        │      Contract Review DAG        │
        └─────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌────────┐   ┌─────────┐   ┌──────────┐
   │ Legal  │   │ Security│   │ Business │
   │ Review │   │  Scan   │   │  Impact  │
   └────────┘   └─────────┘   └──────────┘
        │             │             │
        └─────────────┼─────────────┘
                      ▼
              ┌─────────────┐
              │  Aggregator │
              │  + Report   │
              └─────────────┘
```

### 场景 2：会议摘要 MapReduce

```typescript
// 三个 Agent 并行处理不同部分
const pool = new AgentPool(agents)
const results = await pool.runParallel(transcript, {
  extractActionItems: 'Extract action items',
  analyzeSentiment: 'Analyze sentiment',
  identifyDecisions: 'Identify key decisions'
})

// Aggregator 合并结果
const summary = await aggregator.run(
  'Merge into report with action items and sentiment',
  results
)
```

### 场景 3：竞品监控

```typescript
// 三个 Agent 从不同来源并行抓取
const monitoring = orchestrator.createTeam('competitive', {
  agents: [agentTechCrunch, agentHackerNews, agentTwitter],
  sharedMemory: true
})

const report = await orchestrator.runTeam(monitoring, 
  'Monitor AI agent trends and flag contradictions'
)
```

---

## 快速上手

```bash
npm install @open-multi-agent/core
```

```typescript
import { OpenMultiAgent, type AgentConfig } from '@open-multi-agent/core'

const agents: AgentConfig[] = [
  { name: 'architect', model: 'claude-sonnet-4-6', 
    systemPrompt: 'Design clean API contracts.', 
    tools: ['file_write'] },
  { name: 'developer', model: 'claude-sonnet-4-6', 
    systemPrompt: 'Implement runnable TypeScript.', 
    tools: ['bash', 'file_read', 'file_write', 'file_edit'] },
  { name: 'reviewer', model: 'claude-sonnet-4-6', 
    systemPrompt: 'Review correctness and security.', 
    tools: ['file_read', 'grep'] },
]

const orchestrator = new OpenMultiAgent({
  defaultModel: 'claude-sonnet-4-6',
  onProgress: (event) => console.log(event.type, event.task ?? event.agent ?? ''),
})

const team = orchestrator.createTeam('api-team', { 
  name: 'api-team', 
  agents, 
  sharedMemory: true 
})

const result = await orchestrator.runTeam(team, 
  'Create a REST API for a todo list in /tmp/todo-api/'
)

console.log(result.success, result.totalTokenUsage.output_tokens)
```

---

## 局限性

1. **非 Python 优先**：TypeScript 生态在某些领域（数据科学）不如 Python 成熟
2. **相对年轻**：v1.4.1 于 2026-05-18 发布，社区积累不如 LangChain 深厚
3. **Coordinator 的不确定性**：自动分解目标的能力依赖模型，理解可能有偏差
4. **checkpoint 机制缺失**：与 LangGraph 相比，没有内置的持久化执行状态

---

## 与 Workspace Agents 的互补关系

| 维度 | OpenAI Workspace Agents | open-multi-agent |
|------|------------------------|------------------|
| **定位** | 企业级多租户 Agent 平台 | 开发者友好的编排框架 |
| **目标用户** | 企业 IT / 业务团队 | 开发者 / 工程团队 |
| **架构** | OpenAI 托管服务 | 自托管 / 开源 |
| **核心价值** | 治理、合规、多租户 | 灵活性、嵌入式、目标驱动 |
| **典型场景** | 销售线索管理、财务报告 | 代码开发、数据管道 |

**笔者的判断**：两者代表多 Agent 编排的两个极端——Workspace Agents 是「企业-ready 的完整解决方案」，open-multi-agent 是「开发者手里的灵活工具」。对于需要快速验证多 Agent 概念的团队，open-multi-agent 是一个值得关注的起点。

---

## 数据概览

| 指标 | 数值 |
|------|------|
| GitHub Stars | 6.2k |
| Forks | 2.4k |
| 最新版本 | v1.4.1 (2026-05-18) |
| 协议 | MIT |
| 主要语言 | TypeScript (98.4%) |
| 运行时依赖 | 3 个 |

---

## 原文引用

1. "From a goal to a task DAG, automatically." - GitHub README  
   https://github.com/open-multi-agent/open-multi-agent

2. "Your engineers describe the goal, not the graph." - GitHub README

3. "Three runtime dependencies, drops into any Node.js backend." - GitHub README

4. "Built-in safeguards help agents stay aligned with your instructions when they encounter misleading external content, including prompt injection attacks." - OpenAI Workspace Agents  
   https://openai.com/index/introducing-workspace-agents-in-chatgpt/
