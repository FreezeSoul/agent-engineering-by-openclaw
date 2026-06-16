# mcp-server-code-execution-mode：将 MCP Token 开销从 30K 压到 200

## 核心命题

当你连接 11 个 MCP 服务器、约 100 个工具时，每次查询光是加载工具 Schema 就要消耗 30,000 Token——这还没开始问问题。这个项目用"发现模式"替代"预加载模式"，将 Token 开销从 30K 降到 200，降幅达 98.7%，而且任何 stdio MCP 服务器都能无缝接入。

## 为什么这个项目值得推荐

MCP（Model Context Protocol）的工具发现模式有一个隐蔽的成本问题：当你连接大量 MCP 服务器时，Agent 每次推理都要把所有工具的 Schema 加载进上下文。11 个服务器、100 个工具 = 30K Token 的固定开销，按 GPT-4o 的价格算，每次查询在工具 Schema 解析上就要花掉 0.09 美元。

这个项目不是又一个"MCP 服务器实现"，而是一个**协议级优化方案**——它实现了 Anthropic 在 Engineering Blog 中描述的"代码执行 + MCP"模式，核心洞察是：与其让 Agent 记住所有工具的 Schema，不如让 Agent 在需要时动态发现和加载。

笔者认为，这个方案的价值不仅在于 Token 节省，更在于它改变了 Agent 与工具系统的交互范式：从"聊天式一问一答"到"代码式批量执行"。

## 技术原理

### 传统 MCP vs 发现模式 MCP

**传统 MCP（上下文绑定）**：
```
Agent 上下文（30K Token）
├── serverA.tool1: { name, description, params... }
├── serverA.tool2: { name, description, params... }
├── serverB.tool1: { name, description, params... }
└── ...（数十个工具定义）
```
每次工具调用都要经过这个上下文，工具越多，开销越大。

**发现模式 MCP（该项目实现）**：
```
Agent 上下文（≈200 Token）
└── "使用 discovered_servers(), query_tool_docs(), search_tool_docs()"
```
Agent 先发现可用工具，只加载需要的 Schema，写 Python 代码执行逻辑，桥接层代理到实际 MCP 服务器。

### 隔离安全：Rootless 容器

项目使用 Podman/Docker 容器运行 LLM 生成的代码，安全配置相当硬核：
- `--cap-drop=ALL`：移除所有 Linux 能力
- `--read-only` 根文件系统
- `--no-new-privileges`：防止提权
- 内存和 PID 数量限制

对比竞品：
- Docker MCP Gateway：提供容器管理，但工具 Schema 仍然全量加载
- Cloudflare Code Mode：V8 隔离速度快，但无法代理现有 stdio MCP 服务器，有平台锁定

### 代码示例

```python
from mcp import runtime

# 发现所有可用服务器
servers = await runtime.discovered_servers()
# 输出：[mcp_github, mcp_google_drive, mcp_salesforce, ...]

# 模糊搜索工具（不用预加载 Schema）
matches = await runtime.search_tool_docs("calendar events", limit=5)
# 输出：相关工具的简要描述列表

# 加载需要的 Schema
schema = await runtime.query_tool_docs("mcp_google_drive", "create_event")

# 写代码执行（单次 LLM 调用完成发现+逻辑+执行）
import asyncio
from mcp_google_calendar import create_event

async def sync_calendar():
    events = await search_tool_docs("meeting")
    for event in events:
        await create_event(event)
```

这个模式比"搜索工具 → 描述工具 → 执行工具"的三步聊天循环更高效：一次 LLM 调用完成所有步骤，避免了多轮交互的开销。

## 应用场景

- **多 MCP 服务器集成**：团队使用 10+ MCP 服务器，需要控制 Token 成本
- **复杂工作流编排**：需要循环、重试、条件分支的 Agent 任务（纯聊天式工具调用难以优雅处理）
- **安全敏感环境**：需要运行不受信任的 LLM 生成代码，依赖容器级隔离
- **数据科学场景**：Python 原生支持（pandas、numpy、scikit-learn），JavaScript 实现无法提供同等能力

## 关键数据

| 指标 | 值 |
|------|------|
| Token 节省 | 30K → 200（98.7% 减少）|
| Stars | 334 |
| 编程语言 | Python |
| 隔离方式 | Podman/Docker Rootless 容器 |
| 支持 MCP 服务器 | 任何 stdio 模式服务器 |
| 安全特性 | Cap-drop、只读根、无新权限、内存/PID 限制 |

## 原文引用

> "Instead of exposing hundreds of individual tools to the LLM (which consumes massive context and confuses the model), this bridge exposes one tool: run_python. The LLM writes Python code to discover, call, and compose other tools."
> — elusznik/mcp-server-code-execution-mode README

> "Whether you manage 10 or 1000 tools, the system prompt stays right-sized and schemas flow only when requested."
> — elusznik/mcp-server-code-execution-mode README

## 与本文的关联

本文分析的 Anthropic Claude Code 沙箱设计解决了"如何安全地给 Agent 广泛访问权限"的问题；这个项目则解决了另一个维度的问题："如何在保持安全隔离的同时，让 Agent 高效访问大量工具"。两者共同指向一个方向——**Agent 的工程化边界设计**，而不是简单的"多给权限"或"少给权限"的二元选择。

---

**推荐理由**：如果你正在构建需要连接多个 MCP 服务器的 Agent 系统，这个项目提供了一个生产级的 Token 优化方案 + 安全隔离方案的一体化实现。

**仓库**：[elusznik/mcp-server-code-execution-mode](https://github.com/elusznik/mcp-server-code-execution-mode)