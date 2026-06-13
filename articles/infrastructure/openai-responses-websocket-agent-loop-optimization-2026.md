# OpenAI Responses API WebSocket Mode：消除 Agent Loop 瓶颈的工程突破

> 本文深入解析 OpenAI 如何通过 WebSocket Mode 将 Codex Agent Loop 提速 40%，揭示"持久连接 + 连接作用域缓存"这一解决长任务 Agent 性能问题的核心工程框架。

---

## 核心命题

当模型推理速度从 65 TPS 提升到 1000 TPS 时，API 层面的累积开销反而成为了瓶颈。OpenAI 的解决方案是：**放弃 HTTP 的无状态请求-响应模型，改用 WebSocket 持久连接 + 连接作用域缓存**，让 Agent Loop 只传输增量信息，而非每次都重建完整上下文。

---

## 一、问题：模型变快了，API 却变慢了

### 1.1 从 GPU 到 CPU 的瓶颈转移

在 GPT-5 时代，LLM 推理是 Agent Loop 中最慢的环节，API 服务端的处理开销可以"藏在" GPU 推理时间后面。但当 GPT-5.3-Codex-Spark 达到 ~1000 TPS 时，推理不再是大问题——问题转移到了 API 层。

OpenAI 测量了 Codex Agent Loop 各阶段耗时：

| 阶段 | 说明 |
|------|------|
| **API 服务端处理** | 验证请求、处理对话状态 |
| **模型推理** | GPU 生成 Token |
| **客户端时间** | 运行工具、构建模型上下文 |

当推理从 65 TPS 提升到 1000 TPS 后，API 服务端的 CPU 开销相对于 GPU 推理时间变得极其显眼。

### 1.2 HTTP 无状态模型的结构性缺陷

传统 HTTP 模式下，每个 Codex 请求都被当作独立请求处理：

```
请求1: full_history → API处理 → 推理 → 响应1
请求2: full_history → API处理 → 推理 → 响应2  ← 重复处理相同对话状态
请求3: full_history → API处理 → 推理 → 响应3  ← 对话越长，重复开销越大
```

**核心问题**：即使对话中 95% 的内容没变，每次请求都要重建完整的对话状态，包括：
- 重新解析完整的对话历史
- 重新执行安全分类器检查整个历史
- 重新渲染所有已生成的 Token

> "Even when most of the conversation hadn't changed, we still paid for work tied to the full history. As conversations got longer, that repeated processing became more expensive." — OpenAI Engineering Blog

---

## 二、方案：WebSocket 持久连接 + 连接作用域缓存

### 2.1 设计目标

两个相互制约的目标：
1. **最优性能**：像本地工具调用一样处理 Agent Loop（推理 → 阻塞等待工具执行 → 继续推理）
2. **API 兼容性**：保持开发者熟悉的 `response.create` + `previous_response_id` 接口不变

### 2.2 架构解析

```
┌─────────────────────────────────────────────────────────────┐
│                      WebSocket 连接                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │        连接作用域 In-Memory 缓存                      │   │
│  │  • previous_response 对象                           │   │
│  │  • 之前所有 Input/Output Items                     │   │
│  │  • Tool 定义和命名空间                               │   │
│  │  • 已渲染的 Token（追加写入，跳过重复 tokenization）│   │
│  └─────────────────────────────────────────────────────┘   │
│                              ↑                               │
│  response.create(prev_response_id) ──→ 只传增量输入         │
└─────────────────────────────────────────────────────────────┘
```

**关键机制**：

1. **持久连接**：WebSocket 建立后不关闭，整个 Agent Rollout 复用同一连接
2. **连接作用域缓存**：服务端在连接生命周期内维护 in-memory 缓存，存储可复用的状态
3. **增量传输**：客户端每次只需发送 `previous_response_id` + 新增的输入项，服务端从缓存恢复完整上下文

### 2.3 缓存带来的优化链

通过复用连接作用域缓存，实现了多项优化：

| 优化项 | 说明 |
|--------|------|
| **安全分类器增量处理** | 分类器只检查新输入，不扫描完整历史 |
| **Token 缓存追加写入** | 已渲染 Token 缓存，新 Token 直接追加，跳过 tokenization |
| **模型路由复用** | 成功解析的路由逻辑跨请求复用 |
| **后推理工作重叠** | 计费等后推理任务与后续请求重叠执行，不阻塞推理 |

### 2.4 为什么选 WebSocket 而非 gRPC

OpenAI 考虑了 WebSocket 和 gRPC 双向流两种方案，最终选择 WebSocket 的原因：

> "WebSocket because as a simple message transport protocol, users wouldn't have to change their Responses API input and output shapes." — OpenAI Engineering Blog

gRPC 虽然性能相近，但需要开发者学习新的 API shape。WebSocket 对现有 HTTP 开发者更友好，可以复用已有的 `response.create` 经验。

---

## 三、结果：40% 提速，1,000 TPS 变成现实

### 3.1 性能提升

| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|---------|
| **End-to-End Agent Loop** | 基线 | 提升 40% | — |
| **Token 生成速度** | 65 TPS | ~1000 TPS | 15x |
| **Time to First Token (TTFT)** | 改进 45% | — | — |

### 3.2 开发者体验

**最优化原型方案**（追求极致性能）：
- Agent Rollout 作为单个长 Running Response
- 使用 asyncio 异步阻塞采样循环
- 工具执行期间保持连接，发送 `response.done` 事件
- 客户端执行工具后发送 `response.append` 事件恢复采样

**最终发布方案**（追求 API 兼容性）：
- 保持 `response.create` + `previous_response_id` 的标准接口
- WebSocket 连接作用域内自动维护缓存
- 开发者无需修改 API 调用方式

> "The goal was to get as close as possible to the minimal-overhead prototype but with an API shape developers already understood and built around." — OpenAI Engineering Blog

---

## 四、工程启示：Agent Loop 的传输层优化范式

### 4.1 从"请求-响应"到"会话-增量"

传统 HTTP API 是无状态的，每个请求独立处理。Agent Loop 的长任务特性（可能需要几十到数百轮工具调用）使得无状态模型的成本累积变得无法忽视。

**核心转变**：

| 维度 | HTTP 无状态模型 | WebSocket 持久连接 |
|------|-----------------|-------------------|
| **上下文传输** | 每次传完整历史 | 只传增量 + 服务端缓存 |
| **状态管理** | 客户端维护 | 服务端连接作用域管理 |
| **连接方式** | 每次新建 HTTP | 单一 WebSocket 连接 |
| **适用场景** | 短请求/独立请求 | 长任务/多轮交互 |

### 4.2 连接作用域缓存的设计原则

OpenAI 的连接作用域缓存遵循以下原则：

1. **生命周期绑定**：缓存在 WebSocket 连接生命周期内有效，连接关闭即清理
2. **增量失效**：只有新增输入项需要处理，缓存状态只增不减
3. **分层缓存**：Token 缓存、工具定义缓存、对话状态缓存分层管理

### 4.3 对 Agent 框架的启示

这一设计对 Agent 框架有重要参考价值：

- **传输层抽象**：框架应支持可插拔的传输层（HTTP/WebSocket/gRPC），让开发者根据任务特性选择
- **上下文管理**：从"传输完整上下文"转向"传输增量 + 服务端缓存"的模式
- **性能可观测性**：Agent Loop 的性能瓶颈可能不在模型推理，而在传输层

---

## 五、相关实现

### 5.1 官方文档

- [OpenAI WebSocket Mode | OpenAI API](https://developers.openai.com/api/docs/guides/websocket-mode)
- [Speeding up agentic workflows with WebSockets in the Responses API](https://openai.com/index/speeding-up-agentic-workflows-with-websockets/)

### 5.2 社区实现

| 项目 | 说明 |
|------|------|
| [earendil-works/pi](https://github.com/earendil-works/pi) | TypeScript AI agent toolkit，支持 WebSocket Mode（62K stars）|
| [livekit/agents](https://github.com/livekit/agents) | Real-time voice AI framework，Roadmap 中包含 WebSocket Mode |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 统一 LLM API 兼容层，Issue #22051 讨论 WebSocket Mode 支持 |

---

## 结论

OpenAI Responses API WebSocket Mode 的核心贡献在于：**证明了 Agent Loop 的性能瓶颈可以通过传输层优化解决，而非只能依赖模型变快**。

当推理速度不再是瓶颈时，API 层的累积开销（重复上下文处理、多次 HTTP 握手、安全分类器全量扫描）会成为新的短板。WebSocket Mode 提供的"持久连接 + 连接作用域缓存"方案，为所有需要长任务运行的 Agent 框架提供了可复用的工程范本。

**关键判断**：未来 Agent 框架的竞争将不仅在于模型能力，更在于基础设施层的传输效率。传输层优化和模型优化同样重要。