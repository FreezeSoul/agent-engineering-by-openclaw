# Anthropic Claude Agent SDK Python：官方 Python 实现，6939 Stars

> 项目：anthropics/claude-agent-sdk-python | Stars: 6939 | 语言: Python | 官方 SDK

---

## 一句话评价

**Anthropic 官方的 Python Agent SDK，是 Claude Agent SDK 的 Python 原生实现，让 Python 开发者无需切换到 Claude Code CLI 就能构建 Agent 应用。**

---

## 核心能力

### 1. ClaudeSDKClient：双向交互

ClaudeSDKClient 支持与 Claude Code 的双向交互，相比 `query()` 方法增加了两个关键能力：

**自定义工具（Custom Tools）**

```python
# 定义一个 Python 函数作为工具
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city} 的天气是晴天，25°C"

# 注册到客户端
client = ClaudeSDKClient()
client.register_tool(get_weather)
```

自定义工具以 Python 函数的形式直接运行在进程内，不需要启动外部 MCP 服务器：

| 对比维度 | 外部 MCP 服务器 | 自定义工具（进程内） |
|---------|----------------|---------------------|
| 进程管理 | 需要独立管理 | 无额外进程 |
| 通信开销 | IPC 调用 | 函数直接调用 |
| 部署复杂度 | 需要多个进程 | 单进程 |
| 调试难度 | 跨进程调试 | 同进程调试 |

**钩子（Hooks）**

钩子是 Claude Code 应用在特定时机调用的 Python 函数，用于：

> "Hooks can provide deterministic processing and automated feedback for Claude."

典型场景：
- 在每次工具调用前记录日志
- 对 Agent 输出做自动格式化
- 实现自定义的预算控制逻辑
- 在关键节点插入人工审核

### 2. 混合服务器支持

Claude Agent SDK Python 支持同时使用进程内自定义工具和外部 MCP 服务器：

```python
client = ClaudeSDKClient(
    tools=[local_tool1, local_tool2],  # 进程内自定义工具
    mcp_servers=["external-server-1", "external-server-2"]  # 外部 MCP
)
```

这意味着可以保留已有的 MCP 生态，同时享受进程内工具的性能优势。

### 3. 进程内 MCP 服务器

自定义工具实际上是以**进程内 MCP 服务器**的形式运行：

```
┌─────────────────────────────────┐
│      ClaudeSDKClient            │
│  ┌───────────────────────────┐  │
│  │  进程内 MCP 服务器         │  │
│  │  - get_weather            │  │
│  │  - search_database        │  │
│  │  - format_output          │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
          ↓ 无需 IPC
┌─────────────────────────────────┐
│       Claude Code 进程          │
└─────────────────────────────────┘
```

优势：
- **无子进程管理**：不需要启动/维护独立的 MCP 服务进程
- **同进程执行**：工具调用没有进程间通信开销
- **类型安全**：Python 函数直接带类型提示，IDE 支持完整
- **简化部署**：打包成单个 Python 应用即可

### 4. Session Forking

从 v0.1.0 开始支持 Session Forking，允许从当前会话分叉出一个独立的子会话：

```python
# 从当前会话分叉一个新会话
forked_session = client.fork_session()

# 子会话独立运行，不影响父会话
result = forked_session.query("在子会话中执行独立任务")
```

这与 Claude Agent SDK 的 Subagent 设计完全对应——每个 Subagent 都有自己的独立 Session。

---

## 版本与发布

项目保持高频发布：

- **最新版本**：v0.2.82（2026-05-15）
- **发布频率**：111 个 releases，平均约每 4 天一个
- **追踪版本**：捆绑 Claude Code CLI 版本，支持 `2.0.0` 或 `latest`
- **发布流程**：GitHub Actions 自动发布到 PyPI

---

## 与 Claude Agent SDK TypeScript 的关系

Anthropic 同时维护 Python 和 TypeScript 两个版本：

| 维度 | Python 版本 | TypeScript 版本 |
|------|-----------|----------------|
| Stars | 6939 | 1427 |
| 主要语言 | Python (99.3%) | Shell（分发用） |
| 定位 | Python 生态 | TypeScript/JavaScript 生态 |
| 发布频率 | v0.2.82（111 releases） | v0.3.143（111 releases） |
| 维护团队 | Anthropic + 贡献者 | Anthropic + 贡献者 |

两者共享相同的设计理念，但在 API 层面针对各自语言生态做了适配。

---

## 典型应用场景

### 场景 1：Python 应用中的内置 Agent

不需要 Claude Code CLI，直接在 Python 应用中嵌入 Agent 能力：

```python
from claude_agent_sdk import ClaudeAgentClient

client = ClaudeAgentClient()

# 注册自定义工具
client.register_tool(process_data)
client.register_tool(query_database)

# 在 Python 应用中调用 Agent
result = client.query("分析销售数据，找出增长趋势")
```

### 场景 2：并行 Subagent 执行

```python
# 启动多个并行的子 Agent
with client.fork_session() as s1, client.fork_session() as s2:
    r1 = s1.query("分析代码库，找出性能瓶颈")
    r2 = s2.query("审查安全漏洞")
    
# 聚合结果
final_report = aggregate(r1, r2)
```

### 场景 3：自定义评估循环

```python
def evaluate_and_retry(client, task, max_retries=3):
    for attempt in range(max_retries):
        result = client.query(task)
        if evaluate(result):
            return result
        client.fork_session()  # 重置上下文
    return result
```

---

## 工程价值

**为什么关注这个项目？**

1. **官方实现**：Anthropic 官方维护，不是第三方封装，可信度高
2. **Python 生态优先**：Python 是 AI 工程的事实标准语言，官方 SDK 的 Python 支持意味着更好的集成体验
3. **进程内工具**：解决 MCP 部署复杂性问题，让工具集成更轻量
4. **高频迭代**：111 个 releases，持续优化，活跃度高
5. **Session Forking**：支持真正的 Subagent 隔离，与 SDK 设计理念完全对齐

---

## 快速上手

```bash
pip install claude-agent-sdk
```

```python
from claude_agent_sdk import ClaudeSDKClient

client = ClaudeSDKClient()

# 注册自定义工具
@client.tool()
def get_weather(city: str) -> str:
    return f"{city} 晴天，25°C"

# 启动 Agent
result = client.query("北京天气怎么样？")
print(result)
```

---

## 引用

> "ClaudeSDKClient supports bidirectional, interactive conversations with Claude Code. Unlike query(), ClaudeSDKClient additionally enables custom tools and hooks, both of which can be defined as Python functions."
> — GitHub README

> "A custom tool is a Python function that you can offer to to invoke as needed. Custom tools are implemented as in-process MCP servers that run directly within your Python application, eliminating the need for separate processes that regular MCP servers require."
> — GitHub README

> "You can use both [process-internal] and external MCP servers together."
> — GitHub README
