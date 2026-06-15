# AgentOS：用认知记忆重新定义多 Agent 协作

> AgentOS 是一个 TypeScript AI Agent 框架，通过认知记忆系统、运行时工具锻造和六种编排策略，解决了多 Agent 协作中的记忆衰减和信息孤岛问题。

## 核心命题

多 Agent 协作最大的工程难题，不是让 Agent 完成任务，而是让 Agent **记住上下文**、**形成协作人格**、**在长程任务中保持一致性**。

当前的 Agent 框架（LangChain、CrewAI 等）在记忆层面做的是简单的 buffer 或向量检索。AgentOS 的做法完全不同：它用神经科学-backed 的认知记忆机制替代简单 RAG，让 Agent 真正模拟人类的长时记忆特性。

笔者认为，比起主流框架的「记忆即向量数据库」范式，AgentOS 的方向更接近我们对人类记忆的工程理解——记忆不是检索，而是重建。

## 关键特性解析

### 认知记忆：8 种神经科学机制

AgentOS 的记忆系统不是简单的 embedding search，它模拟了 8 种已知的认知记忆现象：

- **Ebbinghaus 遗忘曲线**：记忆强度随时间衰减
- **检索诱导遗忘**：提取一段记忆会弱化相关记忆
- **再巩固**：激活的记忆会进入不稳定状态后重建
- **来源置信度衰减**：对记忆来源的信心随时间下降

这套机制解决了一个实际问题：当 Agent 在长程任务中处理数百轮交互时，简单的 RAG 检索会引入太多「噪音」上下文，而 AgentOS 通过认知优先队列确保每次只激活最相关的记忆片段。

benchmark 数据验证了方向：在 LongMemEval-S 上达到 **85.6% 准确率**（$0.0090/correct），是唯一在 LongMemEval-M 上超过 65% 的开源框架，可重现的 gpt-4o 方案中最高分。

### 运行时工具锻造（Tool Forging）

当没有现成工具覆盖子任务时，Agent 不是调用 API，而是**自己写一个 TypeScript 函数**，附上 Zod schema，然后：

1. LLM Judge 审核代码安全性
2. 在 hardened node:vm sandbox 执行（5 秒 wall clock，禁止 eval/require/process）
3. 通过审核后加入工具目录，供 session 复用

笔者认为，这个设计把「工具安全」从静态配置变成了动态评估：工具不是预设的，而是 Agent 根据任务需要实时锻造并经过安全审核的。这比预设 allowlist 更灵活，同时比直接允许 Agent 执行任意代码更安全。

锻造出的工具可以导出为 SKILL.md 格式的技能，实现跨 session 复用。

### HEXACO 个性系统

AgentOS 引入了 HEXACO 人格模型（开放性、尽责性、外向性、宜人性、情绪稳定性、诚实-谦逊），Agent 的检索、路由和决策会被人格向量加权。

这对多 Agent 协作非常重要：不同人格的 Agent 在同一上下文下会做出不同的决策序列。这不是 prompt 注入，而是**持久的人格偏见**——即使在上下文压力下也能保持行为一致性。

### Soul Files：身份、记忆与边界

Soul File 是 Agent 的「灵魂容器」，包含：
- 身份定义（voice/hard limits/HEXACO scores）
- 记忆目录（markdown wiki 作为长期记忆源）
- 向量/图索引从 markdown 重建

这个设计的关键洞察：**markdown 是记忆的事实来源，向量索引只是加速结构**。如果向量索引损坏，从 markdown 重建即可。这比向量数据库的持久化更可靠，也更可审计。

## 多 Agent 编排：6 种策略

AgentOS 支持 6 种编排策略，覆盖不同的协作模式：

- Sequential（顺序执行）
- Parallel（并行执行）
- Hierarchical（层级）
- Hub-and-spoke（中心辐射）
- Random
- Custom（自定义）

值得注意的是，Anthropic 的论文发现组织结构对伦理结果的影响有限——真正重要的是模型选择和 Agent 类型配置。AgentOS 的 6 种编排策略 + 可配置的 red-teamed agent ratio，让工程师可以在框架层面系统地测试不同配置下的行为。

## 技术规格

| 维度 | 值 |
|------|---|
| Stars | 574（2026-06-05 新发布）|
| 语言 | TypeScript |
| 供应商 | 11 个 LLM 提供商 |
| Extensions | 100+ |
| Skills | 88 个，开机自加载 |
| 记忆 benchmark | LongMemEval-S 85.6% / LongMemEval-M 70.2% |
| 许可证 | 需查看 README |

## 快速开始

```bash
npm install @framers/agentos
```

```typescript
import { agent } from '@framers/agentos';

const tutor = agent({
  provider: 'anthropic',
  instructions: 'You are a patient CS tutor.',
  personality: { openness: 0.9, conscientiousness: 0.95 },
  memory: { types: ['episodic', 'semantic'], working: { enabled: true } },
});

const session = tutor.session('student-1');
await session.send('Explain recursion with an analogy.');
await session.send('Can you expand on that?'); // remembers context
```

## 竞品对比

对比主流框架的核心差异：

| 框架 | 记忆系统 | 工具安全 | 个性系统 | 语言 |
|------|---------|---------|---------|------|
| LangChain | Vector store | Allowlist | 无 | Python |
| CrewAI | 简单 buffer | 预设工具 | 无 | Python |
| Mastra | 增强 RAG | 预设工具 | 无 | TypeScript |
| **AgentOS** | **认知机制（8种）** | **运行时锻造+Judge** | **HEXACO** | **TypeScript** |

## 笔者的判断

AgentOS 的记忆系统是笔者见过的最认真的 Agent 记忆工程化尝试。85.6% 的 LongMemEval-S 准确率在开源方案中确实领先，但更重要的是背后的认知科学框架——记忆不是存储，而是动态的、可衰减的、需要重建的。

运行时工具锻造是另一个被低估的设计。行业主流做法是预设工具 + allowlist，但这限制了 Agent 的适应能力。AgentOS 的做法把工具安全变成动态审核，更灵活但也更复杂。

对于需要长程任务、高精度记忆和个性化 Agent 行为的场景，AgentOS 值得关注。对于追求快速原型和主流生态集成的场景，LangChain/CrewAI 仍然是更稳妥的选择。

---

## 链接

- GitHub: https://github.com/framerslab/agentos
- 文档: https://docs.agentos.sh
- npm: `@framers/agentos`

---

## 原文引用

> "AgentOS is an open-source TypeScript framework for AI agents that remember, adapt, and write their own tools."

来源：[GitHub README](https://github.com/framerslab/agentos)

> "When no tool covers a sub-task, the agent writes a TypeScript function with a Zod schema; a separate LLM judge approves it; it runs in a hardened node:vm sandbox (5s wall clock, no eval/require/process), then joins a discoverable index for the rest of the session."

来源：[GitHub README](https://github.com/framerslab/agentos)

> "Top open-source memory benchmarks: 85.6% on LongMemEval-S at $0.0090/correct (gpt-4o), and 70.2% on LongMemEval-M, the only open-source library above 65% on M with reproducible methodology."

来源：[GitHub README](https://github.com/framerslab/agentos)