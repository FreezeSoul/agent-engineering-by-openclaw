# fastapi_mcp：用 FastAPI 接口直接暴露 MCP 工具

> 本文推荐 [tadata-org/fastapi_mcp](https://github.com/tadata-org/fastapi_mcp)（11,880 Stars），一个将 FastAPI 端点自动转化为 MCP 工具的框架，让 AI Agent 通过标准 MCP 协议调用任意 FastAPI 功能。

---

## 核心命题

**MCP 的价值不是「多一个协议」，而是「工具发现的标准化」**——fastapi_mcp 解决的是企业「已有大量 FastAPI 服务，Agent 不知道该怎么调用」的问题：通过装饰器注解，把 FastAPI endpoint 自动暴露为 MCP 工具，让任何 MCP-compatible Agent（Claude Code、Cursor、OpenAI Agent）直接调用。

> "Expose your FastAPI endpoints as Model Context Protocol (MCP) tools, with Auth!"
> — [fastapi_mcp README](https://github.com/tadata-org/fastapi_mcp)

**笔者认为**：MCP 协议的核心价值在于**工具发现的互操作性**——同一套 MCP 工具可以被任何 MCP Client 消费。fastapi_mcp 把企业现有的 FastAPI 资产变成 MCP 工具，等于把「定制化 Agent 集成」变成了「标准化即插即用」，这是企业 AI 落地的关键路径。

---

## 为什么这个项目重要

### 1. 企业现有 FastAPI 资产的一步式 MCP 化

传统方式让 Agent 调用 FastAPI：
1. 写一个 Python 包装脚本
2. 让 Agent 通过 subprocess 调用
3. 自己处理参数序列化和返回解析

fastapi_mcp 方式：
```python
from fastapi_mcp import add_mcp_routes

app = FastAPI()
add_mcp_routes(app)  # 一行，把所有 endpoint 变成 MCP 工具
```

Agent 立刻知道有哪些工具可用、参数是什么、返回值是什么格式。

### 2. 内置 Auth 支持

企业级 API 几乎都有认证需求。fastapi_mcp 支持：
- API Key 认证
- OAuth2 / Bearer Token
- 自定义 Header 认证

这意味着把内部 API MCP 化时不需要自己处理认证层的桥接。

### 3. 11,880 Stars 的生态认可

项目 topics 包含 `mcp`、`mcp-server`、`fastapi`、`claude`、`cursor`、`llm` 等，说明它被 MCP 生态和 AI Coding 工具（Claude Code、Cursor、Windsurf）广泛采用。

### 4. 与 Claude Code / Cursor 的直接集成

README 明确标注了与 Claude Code 和 Cursor 的兼容性——意味着开发者可以在不写额外代码的情况下，让这些 AI Coding 工具直接调用内部 FastAPI 服务。

---

## MCP 工具化的技术细节

### 核心机制

`add_mcp_routes()` 做了什么：
1. 扫描 FastAPI app 的所有 Route
2. 为每个 Route 生成 MCP 工具定义（名称、参数 schema、返回类型）
3. 注册 MCP Server，提供 `tools/list` 和 `tools/call` 端点
4. Agent 通过标准 MCP 协议调用，底层自动转发到对应 FastAPI endpoint

### 支持的认证方式

| 认证类型 | 说明 |
|---------|------|
| API Key | `X-API-Key` Header |
| Bearer Token | Authorization Header |
| OAuth2 | 通过 FastAPI 依赖注入实现 |

### 自动序列化

FastAPI 的 Pydantic 模型自动映射为 MCP 的 JSON Schema，Agent 能精确知道参数结构。

---

## 应用场景

### 场景 1：内部工具 MCP 化

企业有 CRM、ERP、内部工具的 FastAPI 接口，通过 fastapi_mcp 一次性暴露为 MCP 工具，Claude Code 等 Agent 立刻可以调用：

```python
# 内部 HR API
@app.get("/employees/{id}/leave-balance")
async def get_leave_balance(employee_id: str):
    ...

# 一行 MCP 化
add_mcp_routes(app)
```

Claude Code 现在可以用自然语言查询员工假期余额，无需手写 API 调用代码。

### 场景 2：跨 Agent 工具共享

同一套 MCP Server 可以同时服务于：
- Claude Code（代码编写）
- Cursor（代码补全）
- 内部对话机器人（客服）

而不是每个 Agent 各自维护一套 API 包装。

---

## 与其他 MCP 项目的协同

| 项目 | Stars | 定位 | 协同关系 |
|------|-------|------|---------|
| [microsoft/mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners) | 16K | MCP 入门教程 | 基础层：学习 MCP 协议 |
| [tadata-org/fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) | 11,880 | FastAPI → MCP 工具暴露 | **执行层**：把现有 API 变成 MCP 工具 |
| [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry) | 6,854 | MCP 工具注册中心 | 分发层：发现和分发 MCP 工具 |

**闭环**：学会 MCP（microsoft/mcp-for-beginners）→ 把 FastAPI 暴露为 MCP（fastapi_mcp）→ 发布到 MCP 工具注册中心（modelcontextprotocol/registry）。

---

## 参考资源

- GitHub: [tadata-org/fastapi_mcp](https://github.com/tadata-org/fastapi_mcp)（MIT License）
- Topics: `mcp`, `mcp-server`, `fastapi`, `claude`, `cursor`, `llm`
- 关联 MCP 项目: [microsoft/mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners)（16K Stars，MCP 入门）
