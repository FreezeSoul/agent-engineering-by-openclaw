# Atmosphere：JVM 平台的多协议实时传输 Agent 框架

> 当你的 AI Agent 需要同时面对浏览器（WebSocket）、移动端（SSE）和企业内部系统（gRPC）时，传输层的多协议适配是不可避免的工程难题。Atmosphere 提供的答案是：**一次声明，多协议暴露**——用 `@Agent` 注解定义行为，传输层自动匹配。

---

## 核心命题

JVM 平台上搭建生产级 AI Agent 的团队面临一个典型困境：传输层实现分散在各种客户端协议中（WebSocket、SSE、gRPC、MCP、A2A），每个协议都要单独维护。Atmosphere 的核心价值是**将传输层抽象为可插拔的基础设施**，让业务逻辑（`@Agent` 注解）和传输协议（WebSocket/SSE/gRPC/...）分离。

---

## 一、为什么需要多协议传输层

### 1.1 Agent 的多元消费方

现代 AI Agent 不再只是"对话窗口"，它的消费方包括：

| 消费方 | 典型协议 | 特点 |
|--------|----------|------|
| **Web 浏览器** | WebSocket / SSE | 双向流，低延迟 |
| **移动端 App** | SSE / Long Polling | 防火墙友好 |
| **企业内部服务** | gRPC | 高性能，低带宽 |
| **AI 工具生态** | MCP | 标准化工具发现 |
| **其他 Agent** | A2A | Agent 间协作 |
| **IM 平台** | Slack/Telegram/Discord | 消息渠道接入 |

每个协议都有其最佳适用场景，Agent 需要同时暴露多个协议端点。

### 1.2 传输层与业务逻辑耦合的问题

传统做法是为每个协议写独立的 endpoint：

```
AgentService
├── WebSocketEndpoint  ← 重复的认证、内存、政策逻辑
├── SSEEndpoint         ← 重复的认证、内存、政策逻辑
├── GrpcEndpoint       ← 重复的认证、内存、政策逻辑
└── MCPEndpoint        ← 重复的认证、内存、政策逻辑
```

维护成本高，协议之间行为不一致，治理逻辑难以集中。

---

## 二、Atmosphere 架构解析

### 2.1 核心设计：`@Agent` 注解 + 模块化传输

```
@Agent(name = "my-agent", description = "...")
public class MyAgent {
    @Prompt
    public void onMessage(String message, StreamingSession session) {
        session.stream(message);
    }

    @Command(value = "/status", description = "Show status")
    public String status() { ... }

    @AiTool(name = "lookup", description = "Look up data")
    public String lookup(@Param("query") String query) { ... }
}
```

**关键洞察**：只需要声明一次 `@Agent`，classpath 上的模块决定暴露哪些协议：

| 模块 | 暴露协议 |
|------|---------|
| `atmosphere-agent` | 浏览器端点 `/atmosphere/agent/my-agent` |
| `atmosphere-mcp` | MCP 端点 |
| `atmosphere-a2a` | A2A 端点 + Agent Card |
| `atmosphere-agui` | AG-UI 端点 |
| `atmosphere-channels` | Slack/Telegram/Discord/WhatsApp |

> "Modules on the classpath decide which endpoints and integrations are registered." — Atmosphere README

### 2.2 传输层架构

Atmosphere 的 broadcaster transport 是整个框架的基础设施：

```
┌─────────────────────────────────────────────────────────────┐
│                    Broadcaster Pipeline                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │WebSocket │  │   SSE    │  │gRPC/Binary│  │WebTransport│  │
│  │(always-on)│  │(always-on)│  │ (optional) │  │HTTP3 (opt) │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ↑
                    ┌─────────────────────┐
                    │  @Agent 业务逻辑     │
                    │  (传输协议无关)       │
                    └─────────────────────┘
```

**默认开启**：WebSocket、SSE、Long Polling（始终可用）
**可选启用**：gRPC（二进制高效）、WebTransport/HTTP3（需额外依赖）

### 2.3 治理架构（Governance）

Atmosphere 将治理（Governance）放在关键路径上，而非事后审计：

| 治理机制 | 说明 |
|----------|------|
| **Policy Admission** | 每次工具调用前通过策略准入 |
| **@AgentScope** | 作用域隔离，控制 Agent 权限边界 |
| **Plan-and-Verify** | 执行前计划，执行后验证 |
| **Cost Ceilings** | 设置成本上限，防止无限消耗 |
| **PII Rewriting** | 自动重写敏感信息 |
| **Admin Kill Switches** | 管理员可随时终止 Agent |
| **Durable HITL Approvals** | 人类批准流程可休眠，不占线程，持久化状态 |

> "The differentiator is the streaming + JVM + governance combination: long-lived stateful agent sessions over real-time transports, with policy admission on the critical path." — Atmosphere README

### 2.4 持久化与恢复机制

| 能力 | 说明 |
|------|------|
| **Durable Sessions** | Session 持久化，跨 JVM 重启 |
| **CheckpointStore** | 每步重试，恢复点继续 |
| **Replay Buffer** | 断点重连后恢复上下文 |
| **CoordinationJournal** | 事件溯源，AST from log |
| **Workflow\<S\>** | 可休眠的工作流，不占线程 |

---

## 三、与 OpenAI WebSocket Mode 的互补关系

### 3.1 主题关联

| 维度 | OpenAI Responses API WebSocket Mode | Atmosphere |
|------|------------------------------------|-----------|
| **层次** | API 协议层（OpenAI 官方实现）| 框架传输层（多协议抽象）|
| **协议** | WebSocket（单一协议）| WebSocket / SSE / gRPC / MCP / A2A / AG-UI（全系列）|
| **目标** | 减少 OpenAI API 开销 | 统一多端点传输体验 |
| **上下文** | OpenAI 服务端缓存 | JVM 端 Session + 持久化 |
| **治理** | 内置于 API 服务端 | 框架级别治理（Policy/HITL）|

两者解决的是不同层面的问题，但共同主题是**传输层优化对 Agent 性能的重要性**。

### 3.2 互补场景

**场景**：在 JVM 平台上使用 OpenAI Responses API 构建 Agent，同时需要支持多种客户端协议

```
浏览器 ←→ WebSocket ←→ Atmosphere ←→ OpenAI Responses API (WebSocket Mode)
手机   ←→ SSE      ←→ Atmosphere ←→ (同样的 Agent 逻辑)
内部系统 ←→ gRPC   ←→ Atmosphere ←→ (同样的 Agent 逻辑)
AI 工具 ←→ MCP     ←→ Atmosphere ←→ (同样的 Agent 逻辑)
```

OpenAI 提供高效的 API 层传输（WebSocket Mode），Atmosphere 提供多协议暴露层——两者是正交的。

---

## 四、快速开始

### 4.1 安装

```bash
# macOS/Linux
brew install Atmosphere/tap/atmosphere

# 或
curl -fsSL https://raw.githubusercontent.com/Atmosphere/atmosphere/main/cli/install.sh | sh
```

### 4.2 创建 Agent 应用

```bash
atmosphere new my-agent --template ai-chat
cd my-agent
LLM_API_KEY=your-key ./mvnw spring-boot:run
```

### 4.3 切换 Runtime Adapter

```bash
# 使用 Spring AI adapter
atmosphere new my-agent --template ai-chat --runtime spring-ai --force

# 使用 LangChain4j adapter
atmosphere new my-agent --template ai-tools --runtime langchain4j --force
```

### 4.4 导入 Skill

```bash
atmosphere import https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
cd frontend-design
LLM_API_KEY=your-key ./mvnw spring-boot:run
```

---

## 五、技术规格

| 规格 | 值 |
|------|-----|
| **Stars** | 10,528 |
| **语言** | Java (88%), TypeScript (9.6%) |
| **许可** | Apache 2.0 |
| **运行时** | JVM (Tomcat/Jetty/Netty/Undertow/Quarkus/Spring Boot) |
| **默认协议** | WebSocket, SSE, Long Polling |
| **可选协议** | gRPC, WebTransport/HTTP3, MCP, A2A, AG-UI |
| **Runtime Adapters** | 12 个（含 Built-in, Spring AI, LangChain4j, Google ADK, AgentScope 等）|

---

## 结论

Atmosphere 代表了一个重要的方向：**传输层抽象 + 治理内嵌**。当 Agent 系统需要同时服务多种客户端协议时，手写多协议 endpoint 的成本极高且难以维护。Atmosphere 通过`@Agent` 注解和模块化 classpath 机制，让同一套业务逻辑自然暴露为多个协议端点。

**关键判断**：对于 JVM 技术栈的团队，Atmosphere 提供了一条不依赖特定云平台的 Transport 层选择——这在"Agent 框架都在追求自有云基础设施"的趋势下，是一个值得关注的技术差异化方向。