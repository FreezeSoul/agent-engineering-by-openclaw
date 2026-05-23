# Agency Swarm：用组织结构思维构建多 Agent 系统的编排框架

**目标用户画像**：用 Python 构建多 Agent 应用的工程师，想要用清晰的通信拓扑替代扁平的消息广播。

**核心结论**：Agency Swarm 的核心设计思想是把多 Agent 系统当作一个组织来设计——每个 Agent 有明确的 Role、Tools 和 Communication Flows，而不是让所有 Agent 都通过共享消息池通信。这个设计让 Agent 协作变得可预测、可调试、可版本化。

**一手来源**：[VRSEN/agency-swarm GitHub README](https://github.com/VRSEN/agency-swarm)（今日 GitHub Trending，4,400 Stars）

---

## 场景锚定

想象一个典型场景：你的应用需要一个 CEO Agent 协调任务，一个 Developer Agent 执行代码，一个 Virtual Assistant Agent 处理日常沟通。

没有 Agency Swarm 的世界：
- 所有 Agent 都通过同一个消息队列通信
- 你需要手动管理「谁在什么情况下该响应什么消息」
- 增加新 Agent 时需要修改所有现有 Agent 的消息路由逻辑

有 Agency Swarm 的世界：

```python
agency = Agency(
    ceo,  # 入口点，与用户对话
    communication_flows=[
        ceo > dev,   # CEO 可以主动联系 Developer
        ceo > va,    # CEO 可以主动联系 Virtual Assistant
        dev > va     # Developer 可以主动联系 Virtual Assistant
    ],
    shared_instructions='agency_manifesto.md',
)
```

通信方向用 `>` 操作符显式声明：**谁可以主动发起与谁的对话**。这个约束让整个系统的协作拓扑变得透明。

---

## 技术拆解

### 核心设计：组织结构即架构

> "This framework continues the original vision to simplify the creation of AI agencies by thinking about automation in terms of real-world organizational structures, making it intuitive for both agents and users."
> — [README](https://github.com/VRSEN/agency-swarm)

这个设计的底层逻辑是：**Agent 之间的通信应该像组织内部的信息流动一样，有明确的拓扑，而不是混沌的消息广播**。在真实组织中，信息流动是有方向的——CEO 可以给 Developer 发指令，但 Developer 通常不会主动给 CEO 发任务。这个约束在 Agency Swarm 中变成了通信流的配置。

### Type-Safe Tools：用 Pydantic 约束 Agent 行为

> "Type-Safe Tools: Develop tools using Pydantic models for automatic argument validation, compatible with the OpenAI Agents SDK's FunctionTool format."
> — [README](https://github.com/VRSEN/agency-swarm)

Agency Swarm 的工具系统基于 Pydantic，这让它有别于大多数用字典或字符串定义工具的框架。好处是工具参数在运行时被自动验证——如果调用方传入错误的参数类型，框架会在调用发生前拦截，而不是让 Agent 收到一个模糊的错误然后尝试修复。

```python
from agency_swarm import function_tool

@function_tool
def create_project(name: str, template: str = "default") -> str:
    """Create a new project from template."""
    return f"Project {name} created from {template}"
```

装饰器 `@function_tool` 包装的函数自动兼容 OpenAI Agents SDK 的 FunctionTool 格式。也可以从 OpenAPI Schema 生成工具：

```python
from agency_swarm.tools import ToolFactory

with open("schemas/api.json") as f:
    tools = ToolFactory.from_openapi_schema(f.read())
```

### 文件夹结构：每个 Agent 有自己的命名空间

> "This structure ensures that each agent has its dedicated space with all necessary files to start working on its specific tasks."
> — [README](https://github.com/VRSEN/agency-swarm)

Agency Swarm 推荐一个文件夹对应一个 Agent 的结构：

```
AgentName/
├── files/           # 上传到 OpenAI 的文件
├── schemas/         # 转为工具的 OpenAPI Schema
├── tools/           # 默认导入的工具
├── AgentName.py     # Agent 主类
├── __init__.py
├── instructions.md  # Agent 的指令文档
└── tools.py         # 角色专用工具
```

这个结构的价值在于：**每个 Agent 的上下文是自包含的**。添加新 Agent 不需要修改已有 Agent 的代码，只需要创建新文件夹并在 Agency 中声明通信流。

### 与 Cursor Autoinstall 的关联

有趣的是，Cursor Autoinstall 的两阶段设计（Goal Setting Agent → Attempt Agent）与 Agency Swarm 的通信流设计有相似的结构：

| Autoinstall | Agency Swarm | 共同点 |
|-------------|-------------|--------|
| Goal Setting Agent 定义成功标准 | CEO Agent 分配任务 | 都是「定义目标」的角色 |
| Attempt Agent 执行配置 | Developer Agent 执行任务 | 都是「执行目标」的角色 |
| 5次重试后丢弃环境 | 通信流约束防止无效消息 | 都有失败处理机制 |

本质上，两个系统都在用**明确的拓扑结构**替代**全连接的消息交换**。这是多 Agent 系统走向生产级的关键一步。

---

## 技术指标

| 指标 | 数值 | 说明 |
|------|------|------|
| GitHub Stars | 4,400+ | 今日 Python Trending，增长中 |
| 语言 | Python 3.12+ | 明确的环境要求 |
| 许可证 | MIT | 可商业使用 |
| 底层框架 | OpenAI Agents SDK + Responses API | 已有生态 |
| LiteLLM 支持 | 是 | 可桥接 Anthropic/Google/Grok |
| Cursor IDE 支持 | 是 | 专门的 workflow 文档 |
| Agent 文件夹结构 | 是 | 自包含的 Agent 命名空间 |
| Type-Safe Tools | 是 | Pydantic 模型验证 |
| 状态持久化 | 是 | load_threads/save_threads callbacks |

---

## 快速启动

```bash
pip install -U agency-swarm

# 定义 Agent
from agency_swarm import Agent, ModelSettings

ceo = Agent(
    name="CEO",
    description="Responsible for task planning and management.",
    instructions="You must converse with other agents to ensure complete task execution.",
    tools=[my_custom_tool],
    model="gpt-5.4-mini",
    model_settings=ModelSettings(max_tokens=25000),
)

# 定义通信流
from agency_swarm import Agency

agency = Agency(
    ceo,
    communication_flows=[ceo > dev, dev > va],
    shared_instructions='agency_manifesto.md',
)

# 运行
agency.copilot_demo()  # Web UI
# 或
agency.tui()           # Terminal
```

---

## 笔者的判断

Agency Swarm 代表了一个明确的方向：**多 Agent 系统的编排应该像组织设计一样，有明确的角色定义和通信拓扑**。这个方向比「把所有 Agent 扔进一个消息池让它们自己协调」要更接近真实世界的协作模式，也更容易调试和演进。

对于构建多 Agent 系统的团队，Agency Swarm 提供了两个实际价值：
1. **通信拓扑可视化**：方向性的通信流让系统行为更容易预测
2. **Agent 隔离**：文件夹结构让每个 Agent 的上下文自包含，添加新 Agent 不影响现有 Agent

如果你在用 OpenAI Agents SDK 构建多 Agent 应用，Agency Swarm 是一个值得考虑的编排层。