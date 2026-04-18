# MCP 生产部署的三层架构挑战：传输、会话与可发现性

> 分类：tool-use
> 来源：MCP 2026 Roadmap + WaveSpeedAI 生产踩坑 + AWS ECS 部署实践
> 阶段：Stage 3-4（Framework → Production Engineering）
> 评估：传输层从无关细节变成一阶架构问题；服务发现是生产部署关键；企业级需求需要独立架构设计

---

## 背景：MCP 的协议层已经 Ready，基础设施还没有

MCP（Model Context Protocol）在 2024 年 11 月发布，到 2026 年 4 月已经达到了 97M 月度 SDK 下载量。OpenAI 和 Google DeepMind 都已官方支持 MCP。协议层的稳定性已经得到验证——官方明确表示这个 cycle 不会增加新的官方传输层，而是演进现有的 Streamable HTTP。

但协议 Ready 不等于生产 Ready。WaveSpeedAI 的工程师 Dora 在一次生产踩坑中描述了这个现实：

> "Last month I hit a wall that no blog post had warned me about when I was wiring an image generation pipeline into a multi-tool agent session: my MCP server kept dropping the session state behind a load balancer, and I'd been staring at the same cryptic timeout for two hours before I understood why."

这不是个例。这是每一个在生产环境部署 MCP 的人迟早会遇到的问题。

---

## 第一层挑战：传输层的状态问题

### Streamable HTTP 的两种模式

MCP 的 Streamable HTTP 传输支持两种模式：

**Stateless 模式**（默认）：
- 每个工具调用是一个自包含的 HTTP 请求
- 服务器端无会话状态
- 可以水平扩展，多个副本无需 session affinity
- 适合简单的单步工具调用

**Stateful 模式**（通过 `Mcp-Session-Id` header）：
- 跨请求维持服务器端会话状态
- 适合多步骤工作流和服务器端上下文
- 但会引入水平扩展问题——session 绑定到特定服务器实例

### 水平扩展的核心矛盾

状态与会话是分布式系统的基本矛盾，MCP 的 Stateful 模式将这个矛盾暴露在了 Agent 架构的核心位置：

```
客户端 → Load Balancer → MCP Server A（持有session）→ MCP Server B（没有session）
                              ↑
                        首次请求路由到这里
```

当 Load Balancer 将后续请求路由到不同服务器实例时，session 状态丢失。这个问题在toy demo中不存在，因为只有单机运行。在生产环境中，这是必须解决的第一道坎。

### AWS ECS 的工程解法

AWS 在 ECS 上部署 MCP 的实践提供了一个参考架构：

| 组件 | 技术 | 职责 |
|------|------|------|
| UI Service | Gradio + ECS | Web 聊天界面，公开访问 |
| Agent Service | Strands Agents SDK + Bedrock | AI 推理和 MCP 工具调用编排 |
| MCP Server | FastMCP + ECS | 产品目录等工具暴露 |
| Service Connect | AWS Cloud Map + Envoy | 服务到服务发现和路由 |
| Express Mode | Managed ALB + Auto-scaling | 自动负载均衡和 HTTPS 终端 |
| Product Catalog | Amazon S3 | JSON 格式产品数据存储 |

关键设计选择：
- **Stateless 默认**：MCP Server 运行在无状态模式，每个请求自包含
- **Service Connect**：解决服务发现问题，而不是依赖 IP/端口
- **Express Mode**：自动化负载均衡，无需手动配置 sticky session

这个架构的局限：适合相对简单的工具调用场景。如果需要复杂的多步骤会话状态，可能需要外部会话存储（Redis 或数据库）。

### MCP Roadmap 的规划

MCP 2026 Roadmap 将 **Transport Evolution and Scalability** 列为四大优先级之首。规划方向：

1. **演进传输和会话模型**：让服务器能够水平扩展而无需持有状态，同时提供清晰、明确的会话处理机制

2. **标准元数据格式**：通过 `.well-known` 端点暴露服务器能力，实现无需建立连接即可发现服务

Roadmap 明确指出：不会增加更多官方传输层，这是有意的设计决定，遵循 MCP 设计原则。演进而非扩展。

---

## 第二层挑战：服务发现

### 当前的问题

在没有标准发现机制的情况下，Agent 如何知道有哪些 MCP Server 可用、如何连接？

当前的实践是手动配置：

```bash
claude mcp add my-server \
  --transport http \
  --header "Authorization: Bearer ${MY_TOKEN}" \
  https://my-mcp-server.com/mcp
```

每个 Agent 需要知道所有 MCP Server 的地址、认证方式、传输类型。这在小规模内部工具场景可以工作，但在企业环境中——数十个团队、数百个 MCP Server——这就是噩梦。

### Roadmap 的方向

MCP Roadmap 明确将 **Server Discovery** 列为传输层演进的一部分：

> "standard metadata format, that can be served via .well-known, so that server capabilities are discoverable without a live connection"

这是一个关键的设计方向：协议层面的发现机制，让 Agent 可以动态感知环境中可用的工具，而不是靠手动配置。

### Claude Code 的懒加载实践

Claude Code 在工具发现上的设计值得参考：

> "In Claude Code, MCP tool search uses lazy loading: only tool names load at session start, so adding more MCP servers has minimal impact on the context window. Tools that Claude actually uses enter context on demand."

这个设计解决了两个问题：
1. **上下文窗口压力**：不需要在 session 启动时加载所有工具 schema
2. **按需激活**：只将实际使用的工具放入 context

这是处理大量 MCP Server 的有效工程策略，延迟发现而非预加载。

---

## 第三层挑战：企业级需求

### 当前差距

MCP 2026 Roadmap 将 **Enterprise Readiness** 列为四大优先级之一，但明确表示这是"定义最不清晰"的领域。现有差距：

| 需求 | 当前状态 | 挑战 |
|------|---------|------|
| 审计日志 | 无标准 | 哪些工具被调用、何时、由哪个 Agent |
| SSO 集成 | 无标准 | 企业身份层到 MCP 凭证的映射 |
| Gateway 行为 | 无标准 | 流量管控、速率限制、访问控制 |
| 配置可移植性 | 无标准 | 跨环境的 MCP Server 配置迁移 |

### Cross-App Access 的愿景

Roadmap 提出了 **Cross-App Access** 的目标：

> "instead of each client managing credentials, access would be brokered through the organization's identity layer — SSO in, scoped tokens out"

这是企业安全的正确方向：集中式身份代理，而不是分散的凭证管理。但目前大多数 MCP Server 还达不到这个标准。

### 重要约束：Enterprise features as extensions

MCP 团队明确表示：

> "We expect most of the enterprise readiness work to land as extensions rather than core spec changes. Enterprise needs are real, but they shouldn't make the base protocol heavier for everyone else."

这个设计决策非常重要：企业级功能不会进入 core protocol，而是作为 extensions 实现。这意味着：
- Core protocol 保持简洁和通用
- 企业级需求由 gateway/proxy 层解决
- 不同企业可以有不同的 enterprise extensions 实现

---

## Agent Communication：Tasks 的下一步

MCP 的 Tasks primitive（SEP-1686）已经作为实验特性发布，用于 Agent 之间的通信。早期生产使用暴露了两个需要关闭的 lifecycle gaps：

1. **重试语义**：任务临时失败时的重试策略
2. **过期策略**：完成后结果保留多长时间

这是正确的迭代路径：先发布实验版本 → 收集生产反馈 → 迭代改进。MCP 不打算在一年内大幅改变 Tasks 的设计，而是填补这些具体的 gaps。

---

## Auth 的现实：最不一致的领域

WaveSpeedAI 的分析将 Auth 列为"MCP 生态中实现最不一致的部分"：

- 协议支持 OAuth 2.1 + PKCE 和静态 API Key
- 实践中很多早期 MCP Server 根本没有 Auth

### 常见失败模式

**失败模式 1：过度广泛的 Personal Access Token**

```bash
# 错误：使用长期 PAT，拥有所有权限
claude mcp add my-server \
  --header "Authorization: Bearer ${LONG_LIVED_PAT}"
```

当 Agent 调用工具时，继承了 Token 的全部权限。配置错误或 prompt injection 的影响范围是灾难性的。

**失败模式 2：没有结构化错误返回**

```python
# 错误：让异常传播
def handle_tool_call(name: str, arguments: dict):
    result = execute_tool(name, arguments)  # 异常直接传播

# 正确：返回结构化错误，让 Agent 可以推理
def handle_tool_call(name: str, arguments: dict):
    try:
        result = execute_tool(name, arguments)
        return {"content": [{"type": "text", "text": str(result)}]}
    except RateLimitError as e:
        return {
            "content": [{"type": "text", "text": f"Rate limit hit. Retry after {e.retry_after}s."}],
            "isError": True
        }
```

---

## 架构判断：传输层是一阶问题

### 从"无关细节"到"核心架构"

在传统的微服务架构中，传输层（HTTP、WebSocket 等）通常是无关细节——选一个，固定就好。但在 MCP 生产部署中，传输层的选择直接影响：

1. **水平扩展能力**：stateless vs stateful 决定了你能否简单地增加副本
2. **服务发现方式**：是否需要外部服务注册中心
3. **认证模型**：token 如何传递和验证
4. **调试复杂度**：session 相关的 bug 难以复现

### 三种生产部署形态

基于当前生态，MCP 生产部署可以分为三种形态：

**形态 1：轻量工具网关**
- Stateless Streamable HTTP
- 无持久会话状态
- 适合简单工具调用、API 聚合
- 扩展方式：水平扩展 + Load Balancer

**形态 2：会话式工具服务**
- Stateful Streamable HTTP（带 session）
- 需要 session affinity 或外部会话存储
- 适合多步骤工作流
- 扩展方式：Redis 外部会话 + sticky session 或单实例

**形态 3：企业级 Agent 平台**
- 完整的 gateway 层（审计、SSO、流量管控）
- MCP 作为内部协议
- 适合大型组织
- 扩展方式：取决于 gateway 实现

---

## 结论

MCP 在协议层面已经成熟，但在生产部署层面仍有三个核心挑战需要跨越：

1. **传输层的状态管理**：stateless vs stateful 的选择需要根据具体场景做出，没有银弹
2. **服务发现机制**：当前靠手动配置，大规模部署需要协议层面的发现标准
3. **企业级架构**：审计、SSO、gateway 等需求将由 extensions 解决，而非 core protocol

MCP 2026 Roadmap 的方向是正确的——演进而非扩展，保持 core 简洁。但对于已经在生产中部署 MCP 的团队来说，这些挑战是当下的现实，不是路线图上的未来。

---

## 相关资源

- [MCP 2026 Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [WaveSpeedAI: MCP in Production](https://wavespeed.ai/blog/posts/mcp-model-context-protocol-production/)
- [AWS: Deploying MCP Servers on Amazon ECS](https://aws.amazon.com/blogs/containers/deploying-model-context-protocol-mcp-servers-on-amazon-ecs/)
- [MCP Specification - Streamable HTTP](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)
- [MCP Tasks Primitive (SEP-1686)](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1686)

---

## 变更记录

- 2026-04-19: 初始化，基于 MCP 2026 Roadmap + WaveSpeedAI + AWS ECS 部署实践
