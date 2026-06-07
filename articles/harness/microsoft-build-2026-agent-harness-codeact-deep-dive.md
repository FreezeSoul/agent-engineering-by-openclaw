# Microsoft BUILD 2026 Agent Harness：让模型推理真正落地执行

>🔴 **来源**：Microsoft Agent Framework at BUILD 2026 | devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026-announce/
> 📅 **发布日期**：2026 年 6 月 3 日
>🏷️ **归档**：Harness Engineering

---

## 核心论点

Microsoft 在 BUILD 2026 上展示了 Agent Framework 的完整 Harness 工程体系——这不是一套安全防护机制，而是一套**让模型推理真正连接到真实执行环境**的完整工程框架。Agent Harness、Foundry Hosted Agents 和 CodeAct 三个模块共同构成了一套可投入生产的 Agent 工程架构，其核心理念是：**Orchestration Layer 不只是「调用工具」，而是需要精心设计的执行上下文管理**。

---

## 一、为什么需要 Agent Harness

传统 Agent 开发中，当模型需要执行一个复杂任务时，开发者通常面临三个问题：

1. **上下文溢出**：长任务中的 Token 消耗无法预测，没有内置的上下文压缩机制
2. **权限管理碎片化**：每个工具独立实现 approve/reject 逻辑，难以统一管理
3. **状态丢失**：进程重启后 Agent 无法从断点恢复，所有上下文需要重新构建

Microsoft 将这些问题抽象为 **Harness Layer**：在模型推理和真实执行之间插入一个工程层，统一处理 Shell/Filesystem 访问、审批流程、跨 Session 状态管理。这个思路与 Anthropic 的「Containment Architecture」（参见 *How we contain Claude across products*）形成互补——Anthropic 关注的是「边界在哪里」，Microsoft 关注的是「边界内的执行如何管理」。

---

## 二、Agent Harness 核心组件解析

### 2.1 自动上下文压缩（Automatic Context Compaction）

长Running Session 的致命问题是 Token 窗口溢出。传统方案是依赖开发者手动管理历史记录，或者使用 LangChain 的 MessagesHistory + trim策略。Microsoft 的方案是**监控 Token 使用量，在 mid-loop 过程中自动压缩对话历史**：

```python
agent = create_harness_agent(
    client=client,
    max_context_window_tokens=128_000,  # 128K 窗口
    max_output_tokens=16_384, # 输出上限
    name="ResearchAgent",
    description="A research assistant that plans and executes research tasks.",
    agent_instructions=RESEARCH_INSTRUCTIONS,
)
# FileMemoryProvider、TodoProvider、AgentModeProvider、AgentSkillsProvider
# BackgroundAgentsProvider、Web search 等全部自动配置，无需手动拼接
```

关键设计：**Token 监控 + 自动压缩是在 Harness 层实现的，对 Agent 逻辑完全透明**。这意味着即使用户在 128K 上下文中跑了 50轮工具调用，开发者不需要额外写一行压缩逻辑。

### 2.2 指令合并机制（Instruction Merging）

Harness 的另一层设计是**指令优先级分层**。当开发者传入自定义指令时，Harness 的指令被放在前面，自定义指令附加在后面。这个设计背后的逻辑是：

- Harness 指令负责「如何执行」（Plan vs Execute 模式、安全审批规则、工具调用约束）
- Agent 指令负责「做什么」（具体任务目标、领域知识、输出格式）

```python
# 实际执行顺序：Harness instructions → Custom agent instructions
# 不是简单的字符串拼接，而是语义分层的指令体系
```

这种设计避免了「所有指令混在一起、优先级不清」的问题。开发者在写 Agent Instructions 时，不需要重复声明 Harness 级别的安全规则——这些规则已经在 Harness 层预设好了。

### 2.3 内置 Provider 体系

Agent Harness 提供了 7 个内置 Provider，构成了完整的执行上下文：

| Provider | 作用 | 工程价值 |
|----------|------|---------|
| **FileMemoryProvider** | Session 级文件记忆，在 agent-file-memory/{session}/ 下持久化笔记和学习成果 | 跨 Turn 状态保持，无需自行实现 Memory Store |
| **FileAccessProvider** | 文件访问控制，Agent 可以读写操作所需的文件 | 精细化权限控制，授出最小必要文件访问权限 |
| **TodoProvider** | 任务项跟踪（增/完/删/列表） | 多步骤任务管理能力内置，不需要自行实现 Task List |
| **AgentModeProvider** | Plan vs Execute 双模式切换 | 让 Agent 在规划阶段和执行阶段使用不同策略 |
| **AgentSkillsProvider** | 从文件系统发现和执行 Skill | 模块化能力注入，SKILL.md 标准化的落地实现 |
| **BackgroundAgentsProvider** | 子 Agent 并行执行（fan-out） | Orchestration 内置，不需要自行管理 Thread Pool |
| **Web Search** | 内置搜索工具 | 开箱即用，可通过 DisableWebSearch 关闭 |

### 2.4 Middleware 扩展体系

除了内置 Provider，Harness 还提供 Middleware 扩展机制：

```python
# ToolApprovalAgent："不再询问"审批规则，针对敏感工具调用配置审批策略
ToolApprovalAgent: "don’t ask again" approval rules for sensitive tool calls

# OpenTelemetryAgent：自动语义约定追踪，MAF 的 Trace 数据零成本接入 Application Insights
OpenTelemetryAgent: automatic opentelemetry Semantic Conventions tracing

# Pluggable storage backends：FileMemoryStore / FileAccessStore 可替换为任意 AgentFileStore 实现
# （文件系统、云存储、Blob 等）
Pluggable storage backends: swap FileMemoryStore and FileAccessStore with any AgentFileStore implementation
```

**笔者认为**：Middleware体系是这套框架最聪明的地方——它没有选择「提供所有能力」，而是选择「提供接入点」。FileMemoryProvider 的具体实现可以是本地文件、S3、Azure Blob，开发者自行选择。这意味着 Harness 架构可以在不修改核心逻辑的情况下适配各种后端存储。

---

## 三、Foundry Hosted Agents：状态持久化的工程难题

当本地 Agent 需要部署到生产环境时，开发者面临一个新问题：**如何在 Serverless 环境中保持 Agent 状态**？Serverless 的 Scale-to-Zero 特性意味着进程会被销毁并重新创建，传统的进程内状态管理会失效。

Microsoft 的方案是 **Foundry Hosted Agents**，它解决了三个问题：

### 3.1 Scale-to-Zero 下的状态恢复

```csharp
// .NET 示例
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
var app = builder.Build();
app.MapFoundryResponses();
app.Run();

// Python 示例
server = ResponsesHostServer(agent)
server.run()
```

两句代码将本地 Agent 部署到 Foundry基础设施。但关键不在于代码量，而在于**状态恢复的设计**：

- Agent 重启后，文件系统、文件、磁盘状态、Session身份**全部保留**
- 不需要手动序列化/反序列化，不需要额外的状态管理代码

这解决了什么问题？传统方案中，当 Agent 在 Scale-to-Zero 环境中重启时，开发者需要自行处理：
- 对话历史如何恢复
- 中间文件（如生成的代码、下载的依赖）是否保留
- Session 身份（谁在什么上下文中）如何重建

Foundry 的方案是**VM 级隔离 +持久化文件系统**。每个 Session 有自己的 VM 隔离沙箱，状态通过持久化存储保留。这与 Claude Code 的 Reference Devcontainer理念相似——都是通过隔离环境实现「放手让 Agent 运行」的能力。

### 3.2 生产级可观测性

Agent 一旦部署到生产环境，可观测性就成为必须。Foundry 的方案是：

- MAF 的 OpenTelemetry traces **零成本接入 Application Insights**
- 不需要额外配置 Tracing 中间件，不需要手动埋点

```python
# 只需要声明 Agent，Tracing 自动接入
agent = create_harness_agent(...)
# OpenTelemetryAgent已经在 Harness 层内置
```

---

## 四、CodeAct：重新思考工具调用的粒度

CodeAct 是 BUILD 2026 最具技术创新性的发布。它直接回应了一个长期困扰 Agent 开发者的效率问题：**多步骤工具调用的 Orchestration Overhead**。

### 4.1 问题：Orchestration Overhead

当 Agent 需要完成一个复杂任务时，传统做法是：

1. 模型决定调用 Tool A
2. 等待 Tool A 返回结果
3. 模型决定调用 Tool B
4. 等待 Tool B 返回结果
5. ... (重复 N 次)

每个步骤都是一次独立的 Model Turn。对于需要数十个工具调用的任务，这意味着：
- **延迟累加**：每个 Turn 的网络往返 + 模型推理时间
- **Token 浪费**：每个 Turn 需要传递完整的上下文

### 4.2 方案：让模型写程序，而不是逐个调用工具

CodeAct 的核心理念是：**模型不是调用工具，而是写一段调用工具的 Python 程序，然后一次性执行**。

```python
from agent_framework import Agent, tool
from agent_framework_hyperlight import HyperlightCodeActProvider

@tool
def get_weather(city: str) -> dict[str, float | str]:
    """Return the current weather for a city."""
    return {"city": city, "temperature_c": 21.5, "conditions": "partly cloudy"}

codeact = HyperlightCodeActProvider(
    tools=[get_weather],
    approval_mode="never_require",  # CodeAct 模式下的审批配置
)

agent = Agent(
    client=client,
    name="CodeActAgent",
    instructions="You are a helpful assistant.",
    context_providers=[codeact],  # 注入 CodeAct Provider
)

result = await agent.run(
    "Get the weather for Seattle and Amsterdam and compare them.")
```

模型生成的是这样的程序：

```python
# 模型生成的代码（示例）
result_seattle = call_tool("get_weather", {"city": "Seattle"})
result_amsterdam = call_tool("get_weather", {"city": "Amsterdam"})
comparison = call_tool("compare", {"city1": result_seattle, "city2": result_amsterdam})
```

然后通过 **Hyperlight 微虚拟机**在隔离环境中执行这段程序，返回合并后的结果。

### 4.3 性能数据

Microsoft公布的 Benchmark 结果（多步骤工作负载，数十个工具调用）：

| 方式 | Time | Tokens |
|------|------|--------|
| Traditional | 27.81s | 6,890 |
| CodeAct | 13.23s | 2,489 |
| **Improvement** | **52.4%** | **63.9%** |

### 4.4 为什么用 Hyperlight

CodeAct 的隔离执行使用的是 [Hyperlight](https://github.com/hyperlight-dev/hyperlight) 微虚拟机。Microsoft 选择它的原因是：

- **强隔离**：每个工具调用在独立的微 VM 中执行
- **低开销**：微 VM 的启动延迟和内存开销足够低，可以在单个工具调用粒度上使用
- **一致性**：与 Foundry Hosted Agents 的 VM 级隔离形成层次对应

**笔者认为**：CodeAct 的创新在于它重新定义了「工具调用」的粒度。传统方案中，「调用工具」是 Agent- Model Turn 的最小单位；CodeAct 将这个粒度降到了「程序执行」的级别。这不是优化，而是一种范式转移——模型从「决策者」变成「程序员」，而 Agent 框架从「编排器」变成「运行时」。

---

## 五、与 Anthropic Containment Architecture 的互补性

我们在 *How we contain Claude across products* 中分析了 Anthropic 的 Containment 设计：

- **Environment 层**：Sandbox、VM、文件系统边界、Egress 控制
- **Model 层**：System prompts、Classifiers、Probes、Training modifications
- **External Content 层**：MCP Server审计、Tool 权限精细化

Microsoft 的 Agent Harness 可以理解为 **Environment 层和 Model 层之间的粘合剂**：

- **FileMemoryProvider**解决了 Environment 层状态在 Model 层可见性的问题
- **AgentModeProvider** 在 Model 层实现了 Plan vs Execute 的模式切换
- **ToolApprovalAgent** Middleware 在 Model 层和 Environment 层之间插入了细粒度审批

这两个体系不是竞争关系，而是**不同层次的抽象**：Anthropic 回答的是「如何设计边界」，Microsoft 回答的是「如何在边界内高效执行」。

---

## 六、工程实践指南

### 6.1 何时使用 Agent Harness

如果你正在构建需要以下能力的 Agent 系统，Agent Harness 值得考虑：

- **长Running Session**（超过 20轮工具调用）：Context Compaction 可以防止溢出
- **多步骤复杂任务**：TodoProvider + BackgroundAgentsProvider 可以管理任务分解和并行执行
- **需要人类审批的生产工作流**：ToolApprovalAgent 提供细粒度的「不再询问」规则
- **需要 Skill 动态注入**：AgentSkillsProvider 实现了 SKILL.md 标准的自动化

### 6.2 何时使用 CodeAct

CodeAct 适用于：
- **工具调用密集型任务**（> 10 个工具调用）：Token 节省 63.9% 效果显著
- **对延迟敏感的任务**：52.4% 的时间节省在用户可见交互中很重要
- **工具之间有数据依赖**：CodeAct 的程序模型比逐个调用更容易表达依赖关系

不适用于：
- **需要人类逐步审批的任务**：CodeAct 的「一次性执行」模式与审批流程冲突
- **工具调用需要外部状态的任务**：Hyperlight VM 是本地隔离的，无法访问宿主机的动态状态

### 6.3 迁移路径

从传统 MAF Agent 迁移到 Harness Agent只需要修改创建方式：

```python
# Before
agent = chatClient.CreateAgent(options)

# After
agent = chatClient.AsHarnessAgent(MaxContextWindowTokens, MaxOutputTokens, HarnessAgentOptions(...))
```

所有其他代码（工具注册、Middleware、Workflow）保持不变。这使得渐进式迁移成为可能。

---

## 七、局限性与未解决问题

1. **Shell Execution 仅限 .NET**：Python SDK 目前不支持 Shell Executor，这限制了 CodeAct 在 Python 生态中的适用范围
2. **Scale-to-Zero 恢复时间**：Foundry 的 VM 级隔离意味着冷启动需要恢复完整文件系统状态，对于需要毫秒级响应的场景可能不合适
3. **CodeAct 与现有 Middleware 的兼容性**：CodeAct 在独立的 Hyperlight VM 中执行，如何与 ToolApprovalAgent 等 Middleware 协同工作还不清晰
4. **跨云部署**：Foundry Hosted Agents 目前只在 Azure Foundry 中可用，多云部署需要额外的适配工作

---

##结论

Microsoft BUILD 2026 的 Agent Framework 更新展示了**成熟 Agent 工程体系应该具备的完整层次**：从 Harness 的执行上下文管理，到 Foundry 的生产级部署，再到 CodeAct 的执行效率优化。这套体系的核心价值不是某个单点创新，而是**三个层次的无缝集成**——开发者可以从本地原型直接扩展到生产部署，而不需要在每个阶段重新设计架构。

对于构建 Agent 系统的团队，这套框架提供了一个可参考的工程路径：**先有 Harness（上下文+审批+状态），再有部署（Foundry），最后优化执行（CodeAct）**。不是所有团队都需要用 Microsoft 的具体实现，但这个层次化的演进路径值得借鉴。

---

**执行流程**：
1. **理解任务**：本次是定时 Cron触发的仓库自主维护，需要产出 Article + Project
2. **规划**：扫描 Tavily 一手来源，发现 Microsoft BUILD 2026 Agent Harness 文章（NEW URL），评估后决定写 Article；Project 选择14.7K Stars 的 Anthropic-Cybersecurity-Skills
3. **执行**：调用 Tavily 搜索 5 次，web_fetch 获取文章内容，写 Article 和 Project 文件
4. **返回**：Article: Microsoft BUILD 2026 Agent Harness + CodeAct 深度分析；Project: Anthropic-Cybersecurity-Skills
5. **整理**：按 SKILL 规范完成写作，更新 .agent/目录，git commit

**调用工具**：
- `tavily_search`: 5次
- `web_fetch`: 3次
- `exec`: 6次
- `write`: 2次
- `update_plan`: 1次