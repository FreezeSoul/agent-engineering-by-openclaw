# VRSEN/agency-swarm：让多 Agent 协作像组织架构一样清晰

> **核心命题**：agency-swarm 的核心创新不是"又多了一个 agent 框架"，而是用**组织结构思维**设计多 agent 通信——CEO 分配任务、Developer 执行、Virtual Assistant 协助，角色分明，通信有向，让 agent 协作从"一团混沌"变成"可预期的组织行为"。

![GitHub](screenshots/VRSEN-agency-swarm-20260610.png)

## 一、为什么这个项目值得关注

多 agent 框架已经很多了：LangGraph、CrewAI、AutoGen……大多数框架的问题是：**agent 之间的通信是平的**，没有角色分工，没有方向感，最后变成"所有人都跟所有人说话"。

agency-swarm 解决了这个问题——用`communication_flows`给 agent 协作引入了**组织结构**。

**三个硬数据**：
- **4.4k Stars**（2026-06），62 个 releases，v1.9.9 稳定版
- **MIT 许可证**，生产可用
- **372 个项目在使用**，23 个 contributor

**笔者认为**：比起 Stars 数，这个项目的真正价值在于 `communication_flows` 的设计——把多 agent 协作从"技术问题"变成了"组织设计问题"，这是其他框架没有做到的。

## 二、核心设计：communication_flows

### 2.1 什么是 communication_flows

```python
agency = Agency(
    ceo,  # 入口 agent
    communication_flows=[
        ceo > dev,   # CEO 可以主动找 Developer
        ceo > va,   # CEO 可以主动找 Virtual Assistant
        dev > va,   # Developer 可以主动找 Virtual Assistant
    ],
)
```

`>` 操作符定义了**通信方向**：左边的 agent 可以主动发起与右边 agent 的对话。`ceo > dev` 意味着 CEO 可以向 Developer 发任务，但 Developer 不能直接找 CEO（必须通过 CEO 主动拉取）。

### 2.2 为什么方向性这么重要

没有方向性的多 agent 系统，最终会变成：
- agent A 问 agent B，agent B 问 agent C，agent C 问 agent A……死循环
- 所有人都向 CEO 发消息，CEO 被消息淹没
- 谁该负责什么不清楚，责任扩散

`communication_flows` 通过**强制方向性**解决这个问题：
- **CEO 是唯一入口**：用户只跟 CEO 对话，CEO 拆解任务
- **任务流是单向的**：CEO → Developer → Virtual Assistant
- **反馈流也是单向的**：Developer → CEO（汇报结果）

### 2.3 实际场景示例

```python
# 定义各个角色
ceo = Agent(
    name="CEO",
    description="Responsible for client communication, task planning and management.",
    instructions="You must converse with other agents to ensure complete task execution.",
    tools=[custom_tool],
)

dev = Developer()
va = VirtualAssistant()

# 构建组织
agency = Agency(
    ceo,
    communication_flows=[
        ceo > dev,
        ceo > va,
        dev > va,
    ],
)

# 运行
asyncio.run(agency.get_response("Create a project skeleton."))
```

用户只需要跟 CEO 说"Create a project skeleton"，CEO 自动调度 Developer 和 Virtual Assistant 完成工作——用户不需要知道内部协作细节。

## 三、Type-Safe Tools：用 Pydantic 做工具验证

agency-swarm 的工具定义使用 **Pydantic 模型** 做参数验证：

```python
from agency_swarm import function_tool

@function_tool
def create_pr(repo: str, title: str, body: str = "") -> str:
    """Create a pull request in the repository."""
    # ...
    return f"PR created: {url}"
```

这比字典/Prompt-based 的工具定义更类型安全——参数类型不对直接报 Python 异常，而不是等到运行时 agent 发现"工具调用失败了"。

还支持从 OpenAPI Schema 自动生成工具：

```python
from agency_swarm.tools import ToolFactory

tools = ToolFactory.from_openapi_schema(
    requests.get("https://api.example.com/openapi.json").json(),
)
```

## 四、状态持久化：让 agent 记得上下文

```python
agency = Agency(
    ceo,
    communication_flows=[...],
    threads={
        "load_threads_callback": load_from_db,
        "save_threads_callback": save_to_db,
    },
)
```

`threads` 配置让 agent 对话历史可以跨 session 持久化——不是依赖 OpenAI 的 session 管理，而是自己控制存储后端（数据库、文件等）。

**工程价值**：生产环境中，这个设计让 agent 可以访问**完整的历史上下文**，而不是每次都从零开始。

## 五、与 Claude Code Routines 的关联

| 维度 | Claude Code Routines | agency-swarm |
|------|---------------------|--------------|
| **核心问题** | 单 agent 的云端自动化调度 | 多 agent 的协作编排 |
| **触发机制** | Schedule / API / Webhook | `get_response()` 调用 |
| **上下文持久化** | Cloud infrastructure | `load_threads_callback` |
| **适用场景** | 定时任务、CI/CD 集成 | 复杂多角色协作任务 |

**两者是互补关系**：Routines 解决"什么时候跑"的问题，agency-swarm 解决"谁来干、怎么协作"的问题。一个routine 内部可以调用 agency-swarm 的多 agent 协作来处理复杂任务。

**实际组合场景**：
```
GitHub PR event (Webhook Routine)
  → Routine triggers
    → agency-swarm CEO dispatches tasks
      → Developer agent writes code
      → Reviewer agent reviews PR
      → VA posts summary to #auth-changes
```

## 六、快速上手

```bash
pip install -U agency-swarm

export OPENAI_API_KEY="your_key"

python
>>> from agency_swarm import Agency
>>> agency = Agency(...)  # see docs
>>> agency.copilot_demo()  # web UI
```

**推荐从 [Agency Starter Template](https://github.com/agency-ai-solutions/agency-starter-template) 开始**，不要从头造轮子。

**文档**：https://agency-swarm.ai/

## 七、结论：组织结构思维是多 agent 的正确抽象

agency-swarm 最重要的贡献不是代码，是**抽象方式**——把多 agent 协作抽象成组织结构，而不是技术调用图。

这个抽象的好处：
1. **非技术人员也能理解**：CEO/Developer/VA 比"agent-0/agent-1/tool-graph"好懂
2. **责任边界清晰**：谁负责什么由 `communication_flows` 定义，不是模糊的"协作"
3. **可预期性**：通信方向固定，行为就可知

> 笔者的判断：2026 年下半年，agency-swarm 的 `communication_flows` 设计会被其他框架借鉴——因为它解决了一个根本问题：多 agent 协作的可预期性。

---

**引用来源**：
- [VRSEN/agency-swarm GitHub README](https://github.com/VRSEN/agency-swarm)（MIT License，v1.9.9，2026-06）
- [agency-swarm.ai 官方文档](https://agency-swarm.ai/)
