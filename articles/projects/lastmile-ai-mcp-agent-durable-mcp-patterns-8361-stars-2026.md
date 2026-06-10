# lastmile-ai/mcp-agent：用 MCP 协议把"临时 Agent"变成"持久 Agent"

## 核心命题

MCP 协议（Model Context Protocol）已经成了 AI Agent 工具调用的事实标准，但大多数 MCP 实现只解决了"连接"问题，没有解决"持久"问题——一旦进程重启，Agent 的状态全部丢失。`mcp-agent` 解决的是这个问题：**用 MCP 的生态 + Temporal 的耐久性，构建真正可以长时间运行的生产级 Agent**。

---

## 一、为什么"临时 Agent"是个工程问题

### 临时 Agent 的痛点

大多数 Agent 框架的默认模式：

1. **启动**：加载工具列表、初始化上下文
2. **运行**：处理任务 → 返回结果
3. **结束**：状态丢失，一切归零

如果任务需要 2 小时，中间 Agent 崩溃了，或者你想让它"明天继续"，怎么办？

传统答案：自己写 checkpoint + resume逻辑。这本身是个合理的工程问题，但每个框架都自己实现一遍，造成大量重复劳动。

### mcp-agent 的核心主张

> mcp-agent's vision is that MCP is all you need to build agents, and that simple patterns are more robust than complex architectures for shipping high-quality agents.

翻译：**用 MCP 解决连接问题，用 Temporal 解决耐久性问题，剩下的交给简单模式**。

---

## 二、架构拆解

### 核心组件

```
┌─────────────────────────────────────────────┐
│              mcp-agent                      │
├─────────────────────────────────────────────┤
│  MCP Client Layer                           │
│  ├─ Full MCP support (tools/resources/ │
│  │ prompts/notifications) │
│  ├─ Advanced: OAuth/Sampling/Elicitation  │
│  └─ Lifecycle management (自动重连/清理)  │
├─────────────────────────────────────────────┤
│  Agent Pattern Layer                        │
│  ├─ Orchestrator-Workers │
│  ├─ Map-Reduce                             │
│  ├─ Evaluator-Optimizer │
│  └─ Router                                 │
├─────────────────────────────────────────────┤
│  Durable Runtime (Temporal)                │
│  ├─ Pause / Resume / Recover │
│  └─ No API changes needed │
└─────────────────────────────────────────────┘
```

### 与 Anthropic "Building Effective Agents" 的对应关系

mcp-agent 的文档明确说明：

> It implements every pattern described in Anthropic's "Building Effective Agents" in a composable way

这意味着文档中列出的模式（orchestrator-workers, map-reduce, evaluator-optimizer, router）直接对应 Anthropic 官方工程博客中定义的 Agent 设计模式。这是 MCP生态中少有的**直接把官方方法论实现出来的框架**。

---

## 三、Minimal Example 的工程启示

官方示例代码：

```python
import asyncio
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

app = MCPApp(name="hello_world")

async def main():
    async with app.run():
        agent = Agent(
            name="finder",
            instruction="Use filesystem and fetch to answer questions.",
            server_names=["filesystem", "fetch"],
        )
        async with agent:
            llm = await agent.attach_llm(OpenAIAugmentedLLM)
            answer = await llm.generate_str("Summarize README.md in two sentences.")
            print(answer)

asyncio.run(main())
```

**笔者认为**：这段代码的简洁度说明了什么？**当协议层（MCP）和耐久层（Temporal）被框架吸收后，Agent 开发者的认知负担只剩业务逻辑本身**。

对比用 LangGraph写同样功能的代码量——mcp-agent 的复杂度明显更低，因为大量的工程复杂度被框架内部消化了。

---

## 四、Temporal 耐久层的工程价值

### 为什么是 Temporal

mcp-agent 选择 Temporal 作为耐久层，不是技术偏好，而是工程权衡：

1. **已有生态**：Temporal 已经有成熟的工作流耐久性实践
2. **模式兼容**：Temporal 的 Activity/Workflow 模型天然适配 Agent 的 task/result模式
3. **无 API 变更**：Agent 代码不需要因为加入耐久层而修改接口

### Durable Agent 的实际意义

官方文档提到的场景：

- **长时间运行**：Agent 可以跨天、跨周持续运行
- **故障恢复**：进程崩溃后从上次 checkpoint 恢复
- **人工审批**：在关键节点暂停，等待人工确认后继续

**这对企业场景至关重要**：当 Agent 要处理财务报表生成、合同审核这类任务时，不能"跑完就结束"，必须支持中断→审批→继续的流程。

---

## 五、竞品对比

| 维度 | mcp-agent | LangChain AgentExecutor | CrewAI |
|------|-----------|------------------------|--------|
| **协议层** | 原生 MCP | LangChain 原生 | LangChain/Custom |
| **耐久层** | Temporal（可选） | 无 | 无 |
| **模式实现** | 直接对应 Anthropic 官方博客 | 部分实现 | 自己的模式 |
| **上手成本** | 低（MCP 生态熟悉度） | 中 | 中 |
| **生产成熟度** | 8k stars，Apache 2.0 | 高（LangChain 生态） | 高（CrewAI 生态） |
| **笔者判断** | **MCP 场景首选** | LangChain 生态深度用户 | 多 Agent 协作场景 |

**核心差异**：mcp-agent 是目前唯一把 MCP 协议层和 Durable Agent 模式绑在一起的开源框架。LangChain 有更强的生态深度，但缺少原生 MCP + Temporal 的组合；CrewAI 的多 Agent 协作更强，但缺少耐久层。

---

## 六、适用场景

**适合用 mcp-agent**：
- 已有 MCP 工具集，想要快速构建 Agent 而不想自己管理生命周期
- 需要 Agent 支持长时间运行（跨 session持续）
- 企业场景需要故障恢复 +人工审批节点
- 想用 Anthropic 官方 Agent 模式，但不想自己实现一遍

**不适合**：
- 只需要临时任务执行（普通的 function calling 就够了）
- 深度定制 LangChain 生态（用 LangGraph）
- 需要复杂的多 Agent 协作编排（用 CrewAI）

---

## 结语

mcp-agent 的核心价值是**做 MCP 协议的集大成者，同时补上耐久性这个缺失环节**。它不是最强大的框架，但是把"连接"和"耐久"这两个工程问题解决得最干净的。

如果你在构建需要长期运行的 MCP Agent，这个项目值得优先考虑。

---

**引用来源**：
- [lastmile-ai/mcp-agent GitHub](https://github.com/lastmile-ai/mcp-agent)（Stars: 8,361）
- [Building Effective Agents - Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Model Context Protocol](https://modelcontextprotocol.io/introduction)