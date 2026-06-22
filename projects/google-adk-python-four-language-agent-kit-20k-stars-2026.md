# Google ADK Python：四语言 Agent 开发工具包，20.2K Stars

> Google Agent Development Kit 的 Python 实现已成长为一个跨语言的 Agent 框架，支持 Python、TypeScript、Java、Go 四种语言后端，共享同一套设计理念。

---

## 基本信息

| 维度 | 内容 |
|------|------|
| **仓库** | [google/adk-python](https://github.com/google/adk-python) |
| **Stars** | 20,200+ (2026年6月) |
| **语言** | Python (核心) + TypeScript/Java/Go SDK |
| **许可** | Apache-2.0 |
| **维护者** | Google |
| **定位** | 企业级多语言 Agent 开发工具包 |

---

## 核心定位

ADK（Agent Development Kit）与其他 Agent 框架最大的差异化在于 **多语言 first**：同一个 Agent 逻辑可以用 Python 定义，部署到 Java 或 Go 的后端服务中。这对于已经在企业基础设施中深度使用 Java/Go 的团队来说，意味着不需要为了引入 Agent 能力而新建 Python 技术栈。

架构上 ADK 是一个 **code-first** 工具包，强调开发者对 Agent 行为有细粒度的控制权，而不是被框架的黑盒封装所限制。

---

## 架构设计

ADK 的核心抽象围绕几个关键组件：

### Agent

定义 Agent 的行为、工具集和执行逻辑。Agent 本身是纯配置对象，不绑定具体运行时：

```python
from google.adk import Agent

agent = Agent(
    model="gemini-2.0",
    name="code_review_agent",
    instruction="You are a code reviewer focusing on security...",
    tools=[search_code, read_file, comment_pr],
)
```

### Tool

ADK 的工具系统设计强调类型安全和可复用性。工具是独立的 Python 函数，带有明确的输入输出 schema：

```python
from google.adk import tool

@tool
def search_code(query: str, file_pattern: str = "*.py") -> list[dict]:
    """Search code in repository."""
    ...
```

### Session 和 Memory

ADK 内置了 Session 管理，用于维护跨请求的对话状态。这与 planning-with-files 的外部文件状态管理走了不同的路径——ADK 选择了内存/数据库持久化，而非文件系统。

### Runner

Runner 是实际的执行引擎，负责加载 Agent、注入工具、管理 Session 并流式返回结果：

```python
from google.adk import Runner

runner = Runner(agent=agent, session_service=session_service)
async for event in runner.run_async(user_id="user1", session_id="sess1"):
    print(event)
```

---

## 与其他框架的定位差异

| 维度 | Google ADK | LangGraph | CrewAI | AutoGen |
|------|-----------|-----------|--------|---------|
| **多语言** | ✅ 四语言 | ❌ Python only | ❌ Python only | ❌ Python only |
| **状态管理** | 内置 Session | Checkpointer | In-memory | In-memory |
| **工具生态** | MCP 集成 | MCP/LangChain | 自有工具 | 自有工具 |
| **企业适配** | Google 生态 | 通用 | 通用 | Microsoft 生态 |
| **学习曲线** | 中等 | 陡峭 | 平缓 | 中等 |

---

## 与 planning-with-files 的互补关系

ADK 的 Session 管理是**内存/数据库持久化**，而 [planning-with-files](../projects/ai-coding/planning-with-files-crash-proof-file-based-agent-state-23k-stars-2026.md) 是**文件系统持久化**。两者解决的是同一个问题（Agent 状态跨 session 恢复），但路径不同：

- **ADK Session**：结构化数据，适合有后端基础设施的企业
- **planning-with-files**：文件系统，适合无服务器/轻量级场景，天然跨 Agent（Claude Code、Cursor、OpenCode 等均兼容）

这与 Anthropic 在 "Scaling Managed Agents" 中提出的 **"The session is not Claude's context window"** 命题高度呼应——无论用哪种持久化机制，核心洞察都是：**状态必须从模型上下文中解耦出来**。

---

## 适用场景

**推荐使用 ADK 的场景：**
- 已有 Python/Java/Go 技术栈，需要引入 Agent 能力
- 需要企业级 SLA 和 Google 生态集成（GCP、BigQuery 等）
- 需要在同一套 Agent 定义下切换不同语言后端
- 需要细粒度的 Agent 行为控制和可观测性

**考虑其他方案的场景：**
- 轻量级、单语言项目 → LangGraph 或 CrewAI
- 需要文件系统级别的状态可移植性 → planning-with-files
- 已在 Microsoft 生态 → AutoGen 或 Semantic Kernel

---

## 相关资源

- [GitHub: google/adk-python](https://github.com/google/adk-python)
- [ADK 官方文档](https://google.github.io/adk-docs/)
- [MCP 集成指南](https://modelcontextprotocol.io/)
- [Google ADK Java 1.0 (2026)](https://github.com/google/adk-java)
- [Google ADK Go 1.0 (2026)](https://github.com/google/adk-go)

---

*本篇于 R488 (2026-06-22) 收录。数据来源：GitHub trending、官方文档、2026年框架对比报告。*
