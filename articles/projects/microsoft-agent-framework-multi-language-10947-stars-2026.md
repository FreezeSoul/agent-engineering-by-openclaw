# Microsoft Agent Framework：企业级多语言 Agent 编排框架

> 项目来源：https://github.com/microsoft/agent-framework
> Stars: 10,947 | 语言: Python (50.1%) + C# (46.6%) | 最新版本: python-1.7.0 (2026-05-28)
> 本文为 **Anthropic 长时运行 Agent Harness** 主题的实证案例

---

## 核心命题

Microsoft Agent Framework（MAF）解决的问题是：**从原型到生产级部署之间，Agent 系统缺失的工程基础设施**。Anthropic 的长时运行 Agent 研究指出了四种失败模式（One-Shot 冲动、过早宣布胜利、环境脏乱、测试不充分），MAF 的答案是一套完整的多 Agent 编排框架——图结构工作流、持久化 Checkpoint、OpenTelemetry 可观测性、YAML 声明式 Agent 定义——把「如何让 Agent 在真实生产环境中稳定工作」变成一个可复用的工程产品。

---

![GitHub](screenshots/microsoft-agent-framework-10947-stars-2026.png)

---

## 一、为什么 MAF 与 Anthropic Harness 研究形成闭环

Anthropic 那篇文章的深层主张是：**Harness 不是安全壳，而是 Agent 与工作状态交互的接口协议**。MAF 恰好是这一主张的企业级实现：

| Harness 要素 | Anthropic 描述 | MAF 对应实现 |
|-------------|----------------|-------------|
| **跨 Session 状态持久化** | Feature List + Progress File + Git History | Checkpointing + Durable Task Hosting |
| **增量式任务执行** | 每次只做一个功能 | Sequential Workflow + Handoff Pattern |
| **结构化环境管理** | Initializer Agent 设定初始状态 | Declarative Agents (YAML 定义) |
| **可验证的进度追踪** | passes 字段 + Puppeteer 截图验证 | OpenTelemetry + 内置 Tracer |
| **失败恢复** | Git revert + 从 clean state 重启 | Restartability + Time-Travel Debugging |

笔者认为，MAF 的价值不在于「又一个 Agent 框架」，而在于它把过去散落在各公司内部最佳实践里的 **Harness 工程机制**，变成了一套开源可用的产品级实现。

---

## 二、核心技术设计

### 2.1 图结构多 Agent 编排

MAF 不采用单一 Agent 循环，而是用**有向图**表达 Agent 之间的编排关系：

```python
# Sequential: 顺序执行，下一个 Agent 承接上一个 Agent 的输出
# Concurrent: 并行执行，多个 Agent 同时处理独立子任务
# Handoff: Agent 之间转移控制权，适合分工明确的场景
# Group Collaboration: 多 Agent 协作处理同一任务
```

这直接呼应了 Anthropic 文末提出的开放问题：「单一通用 Agent 是否是最优解」——MAF 选择了**不回答这个问题，而是让架构师自己决定**，通过图结构支持从单一 Agent 到多 Agent 分工的完整谱系。

### 2.2 Checkpointing + Restartability

Anthropic 的 Harness 设计中，Agent 每次 Session 结束必须留下 clean state。MAF 在框架层面实现了这一点：

> "includes checkpointing, streaming, human-in-the-loop, and time-travel"

MAF 的 Checkpoint 不只是保存进度，而是保存**完整的工作流状态**——包括每个 Agent 的中间输出、当前节点、等待条件等。系统崩溃后可以恢复到任意 Checkpoint，而不是从头开始。

### 2.3 OpenTelemetry 原生集成

```python
# Python observability samples
from agent_framework.observability import trace, span

@trace(agent_name="HaikuAgent", operation="write_haiku")
async def run_haiku_agent(prompt: str):
    ...
```

笔者认为这是 MAF 最被低估的能力。企业级 Agent 系统最大的工程挑战不是「让 Agent 跑起来」，而是**出了问题能追根溯源**。OpenTelemetry 原生集成意味着从第一天起就能接入 Datadog、Splunk、Azure Monitor 等企业级可观测性平台。

### 2.4 Declarative Agents via YAML

```yaml
# declarative-agents 示例
name: HaikuAgent
instructions: "You are an upbeat assistant that writes beautifully."
provider:
  type: foundry
  project_endpoint: ${FOUNDRY_PROJECT_ENDPOINT}
tools:
  - type: file_read
  - type: bash
```

这种设计的意义在于：**把 Agent 定义与代码解耦**。Anthropic 的 Feature List 用 JSON 管理功能状态，MAF 的 Declarative Agents 用 YAML 管理 Agent 定义——都是把「配置」提升为「第一等公民」，让非工程师也能理解和修改 Agent 行为。

### 2.5 双语言支持：Python + C#/.NET

MAF 是目前唯一同时支持 Python 和 C# 的主流 Agent 框架（10,947 Stars，140 Contributors）。这个设计选择笔者认为是务实的企业策略：

- Python 覆盖 Data Science / ML 团队
- C# 覆盖 Enterprise / Windows 团队
- 两者共用同一套 API 语义，迁移成本低

---

## 三、生产级能力

### 3.1 多种 Hosting 模式

| Hosting 模式 | 适用场景 |
|-------------|---------|
| **Azure Foundry Hosted Agents** | 企业级托管，2行代码接入 |
| **Azure Functions** | Serverless 事件驱动场景 |
| **Durable Task** | 长时任务，进程重启不丢状态 |
| **A2A (Agent-to-Agent) Protocol** | 跨框架 Agent 通信 |

### 3.2 Middleware Pipeline

```python
# 灵活的中间件系统
agent.use(middleware.exception_handler())
agent.use(middleware.retry_policy(max_attempts=3))
agent.use(middleware.context_injection(user_context))
```

这与 Anthropic 的「Harness 是架构层」观点高度一致——Middleware 正是**框架层面定义 Agent 行为约束**的标准模式。

### 3.3 Agent Skills

> "Build domain-specific knowledge bases from multiple sources—files, inline code, class libraries—for agents to discover and use"

这直接对应 Anthropic 的 **Agent Skills** 发布（2026-06-02）。两者虽然命名相同，但 MAF 的 Skills 侧重于**知识库构建 + 动态发现**，与 Anthropic 的「技能包可复用」概念在工程层面形成呼应。

---

## 四、与竞品对比

| 维度 | MAF | LangGraph | CrewAI | AutoGen |
|------|-----|-----------|--------|---------|
| **多语言支持** | Python + C# | Python only | Python only | Python only |
| **Checkpoint** | 原生 | 可用 | 无 | 部分 |
| **Declarative Agent** | YAML | 无 | 无 | 无 |
| **OpenTelemetry** | 原生 | 第三方 | 无 | 第三方 |
| **A2A Protocol** | 支持 | 无 | 无 | 无 |
| **Foundry 集成** | 原生 | 无 | 无 | 无 |
| **Stars** | 10,947 | ~25,000 | ~44,600 | ~35,000 |

笔者认为，MAF 的差异化不是某个单点技术突破，而是**唯一同时具备多语言支持 + Checkpointing + OpenTelemetry + A2A + Declarative Agents + Foundry 集成的企业级框架**。对于 already Microsoft/Azure 的企业来说，MAF 是从原型到生产路径最短的选择。

---

## 五、适用场景判断

**适合使用 MAF 的场景**：
- 企业内部已有 Microsoft 生态（Azure, Teams, Foundry）
- 需要 Python + C# 混合团队
- 有合规 / 审计要求，需要 OpenTelemetry 可观测性
- 长时任务占比高，需要 Checkpoint + Restartability
- 需要 Declarative Agent 定义以便非工程师维护

**不太适合的场景**：
- 纯研究 / 原型验证（LangGraph / CrewAI 上手更快）
- Non-Microsoft 技术栈为主（接入成本高于收益）
- 需要最快迭代的独立开发者场景

---

## 六、实战资源

```bash
# Python 安装
pip install agent-framework

# .NET 安装
dotnet add package Microsoft.Agents.AI
dotnet add package Microsoft.Agents.AI.Foundry

# 快速开始文档
https://learn.microsoft.com/agent-framework/overview/agent-framework-overview
```

社区支持：Discord (https://discord.gg/b5zjErwbQM) + Weekly Office Hours

---

> **引用来源**：
> - Microsoft Agent Framework README, GitHub. https://github.com/microsoft/agent-framework
> - "Effective harnesses for long-running agents", Anthropic Engineering Blog, November 2025. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
> - Microsoft Agent Framework Blog, Devblogs. https://devblogs.microsoft.com/agent-framework/