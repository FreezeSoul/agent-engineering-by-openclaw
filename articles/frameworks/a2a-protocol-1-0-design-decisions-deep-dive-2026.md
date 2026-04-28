# A2A Protocol 1.0 设计决策：信任、版本与分层架构

## 背景：多 Agent 协作的真正障碍是什么

大多数 Agent 框架的协议讨论聚焦于「消息格式」和「传输层」—— JSON怎么组织、选 HTTP 还是 WebSocket、用 JSON-RPC 还是 gRPC。这些是实现细节，不是核心问题。

A2A Protocol 1.0 真正要解决的是**信任问题**：两个 Agent 分别由不同组织、不同框架、不同供应商构建，如何在没有任何预先共享密钥的前提下，建立可验证的身份信任，并在这个基础上完成跨组织边界的任务协作？

这不是一个工程实现问题，而是一个密码学和分布式系统问题。1.0 版本的核心价值，在于给出了生产级的答案。

---

## 核心设计决策一：Signed Agent Cards — 去中心化的信任锚点

### 为什么 Agent Card 是必要的

在 A2A 的模型里，Agent 之间的首次接触不需要共享任何预共享密钥或证书。信任建立来自于**发现阶段**的 Agent Card 交换：

```
GET https://{server_domain}/.well-known/agent-card.json
```

Agent Card 是一个 JSON 元数据文档，包含：

```json
{
  "name": "Customer-Onboarding-Agent",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "extendedAgentCard": true
  },
  "supportedInterfaces": [
    {"transport": "http", "url": "https://agent.example.com/a2a"}
  ],
  "securitySchemes": {
    "bearer": {
      "bearerSecurityScheme": {
        "scheme": "bearer"
      }
    }
  },
  "signatures": [
    {
      "protected": "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsInR5cGUiOiJKT1NFIiwia2lkIjoiMTIzNDU2Nzg5MCJ9",
      "signature": "MEUCIQ...（省略）",
      "header": {
        "alg": "ES256",
        "kid": "1234567890"
      }
    }
  ]
}
```

这个 JSON 本身并不敏感——它只是描述 Agent 的能力。但加上**签名**之后，它就成了可验证的身份声明。

### JWS 签名的技术链路

Agent Card 的签名采用 **JWS（JSON Web Signature，RFC 7515）**，流程如下：

**Step 1：规范化（Canonicalization）**

签名之前，必须将 Agent Card 规范化为 RFC 8785（JCS）格式。这一步的关键在于 Protocol Buffer 语义：

- `optional` 字段未显式设置 → **必须省略**（而非包含默认值）
- `optional` 字段显式设置为默认值 → **必须包含**
- `REQUIRED` 字段 → **始终包含**

举例：一个 Agent Card 片段：

```json
{
  "capabilities": {
    "streaming": false,    // optional，显式设置 → 包含
    "pushNotifications": false,
    "extensions": []      // repeated，空数组 → 省略
  },
  "skills": []
}
```

规范化后得到canonical payload：

```json
{"capabilities":{"pushNotifications":false,"streaming":false},"name":"Example Agent","skills":[]}
```

**Step 2：构造 JWS Signing Input**

```
ASCII(BASE64URL(UTF8(JWS Protected Header)) || '.' || BASE64URL(canonical payload))
```

**Step 3：签名计算**

使用私钥（ES256/RS256 等）计算签名，输出 Base64url 编码的 `signature`。

### 为什么这样做

传统的 TLS 证书方案要求所有参与方共享同一个 CA 根证书，这在跨组织场景下不可行。JWS 方案将信任锚点放在**每个 Agent 自身持有的私钥**——任何持有对应公钥的参与者都能验证，无须中心化的 CA 体系。

公钥分发通过 JWS Header 中的 `jku`（JWK Set URL）字段实现，支持动态轮换。

### 局限：现实中的签名验证生态

**工程建议**：Signed Agent Cards 在 A2A 协议层是 MAY（可选）而非 MUST。这意味着生产环境中相当一部分 Agent 不会携带签名——协议允许，但实现者不一定启用。在引入身份验证的系统里，**必须显式检查 Agent Card 是否有签名**，无签名时降级为「可信但不可验证」的信任级别。

---

## 核心设计决策二：版本协商 — 演进而不是硬切换

### A2A-Version 头的机制

A2A 1.0 的版本协商机制异常简单，每个 HTTP 请求携带：

```http
GET /tasks/task-123 HTTP/1.1
Host: agent.example.com
A2A-Version: 1.0
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**最高公共版本算法**（Highest Common Version）：

1. 客户端在 `A2A-Version` 头声明自己支持的最高版本
2. 服务端检查该版本是否支持
3. 若支持，使用请求中的版本语义处理
4. 若不支持，返回 `VersionNotSupportedError`（-32009），错误中包含服务端支持的版本列表

**向后兼容的技巧**：Agent Card 中 `supportedInterfaces` 字段可以同时声明多个版本的接口：

```json
{
  "supportedInterfaces": [
    {"transport": "http", "url": "https://agent.example.com/a2a/v1.0"},
    {"transport": "http", "url": "https://agent.example.com/a2a/v0.3"}
  ]
}
```

客户端根据自身需求选择合适版本，渐进式迁移而非一刀切切换。

### 为什么不需要复杂的版本协商协议

很多 RPC 框架（gRPC、Thrift）使用 service definition 来声明接口版本，通过 code generation 保证类型安全。A2A 选择了一个更轻量的方案，原因在于其设计假设：

- A2A 操作集有限（SendMessage/GetTask/SubscribeToTask 等），不随版本增加而大幅扩展
- 兼容性由协议规范本身保证，而非 code generation
- 在 major.minor 之外引入 patch 版本号的明确说明：patch 不影响协议兼容性，**不应出现在协商中**

> **工程建议**：当你的 Agent 需要最新协议功能时，显式指定 `A2A-Version`，不要依赖自动回退。自动回退在功能缺失时是静默的，可能导致行为不一致。

---

## 三层架构：数据模型 → 操作语义 → 协议绑定

A2A 规范定义了清晰的三层分离，这个设计值得单独分析：

```
Layer 1 (Data Model)       →  Task / Message / AgentCard / Part / Artifact
Layer 2 (Abstract Ops)     →  SendMessage / SendStreamingMessage / GetTask / CancelTask
Layer 3 (Protocol Bindings)→  JSON-RPC / gRPC / HTTP/REST
```

**为什么这样分层**：Layer 1 是协议无关的语义定义，用 Protocol Buffer message 表达；Layer 2 描述操作行为（如哪些操作支持幂等、哪些支持流式）；Layer 3 才是具体的网络协议选择。

这样的设计让同一个 Agent 可以同时暴露 HTTP + gRPC 接口，客户端根据自身技术栈选择绑定，而语义层完全一致。

**JSON-RPC 绑定的实现**（核心方法映射）：

| 抽象操作 | JSON-RPC method | HTTP method |
|---------|----------------|-------------|
| Send Message | `sendMessage` | POST /tasks |
| Send Streaming Message | `sendStreamingMessage` | POST /tasks/streaming |
| Get Task | `getTask` | GET /tasks/{taskId} |
| Cancel Task | `cancelTask` | POST /tasks/{taskId}/cancel |
| Subscribe to Task | `subscribeToTask` | GET /tasks/{taskId}/events |
| Get Agent Card | `getAgentCard` | GET /.well-known/agent-card.json |
| Get Extended Agent Card | `getExtendedAgentCard` | GET /extendedAgentCard |

---

## MCP vs A2A：分层问题的正确框架

这是社区讨论最混乱的话题。规范原文给出了最清晰的解答：

> **MCP inside agents, A2A between agents.**

**MCP（Model Context Protocol）**：解决单个 Agent 与外部工具/数据源交互的问题。MCP Server 通常由 Agent 的创建者控制，运行在信任边界内。

**A2A（Agent-to-Agent Protocol）**：解决两个独立 Agent 系统之间跨组织边界协作的问题。两个 Agent 可能由不同供应商提供，部署在不同网络区域。

**实际系统中的分工**：

```
[Agent A] ←MCP→ [MCP Server: Calendar API]
         ←MCP→ [MCP Server: Email API]
         
[Agent A] ←A2A→ [Agent B]  ←MCP→ [MCP Server: CRM API]
                      （Agent B 内部有自己的 MCP 工具集）
```

> **笔者的判断**：MCP 和 A2A 不是竞争关系，是互补关系。但在系统设计时**必须明确分层**——如果一个工具是 Agent 的外部能力扩展（文件搜索、API调用），它属于 MCP；如果两个 Agent 之间需要协商任务分配，它们属于 A2A。混用会导致架构混乱和安全边界模糊。

---

## 任务状态与多轮交互：A2A 的异步设计

A2A 从设计上就是**异步优先**的。SendMessage 不等待任务完成，立即返回 Task 对象：

```json
{
  "taskId": "task-abc123",
  "status": {"state": "submitted"},
  "artifacts": [],
  "messages": []
}
```

客户端通过三种机制获取更新：

1. **Polling**：`GET /tasks/{taskId}` 轮询
2. **Streaming**（SSE）：`GET /tasks/{taskId}/events` Server-Sent Events
3. **Push Notification**（Webhook）：Agent 主动 POST 到客户端注册的端点

```json
// PushNotificationConfig
{
  "url": "https://client.example.com/webhook/a2a",
  "authentication": {
    "authType": "bearer",
    "bearer": {"authorizationHeader": "Bearer client-generated-jwt"}
  }
}
```

**多轮交互支持**：`messages` 数组中每个 Message 携带 `role`（agent/client）和 `roleContextId`，支持在同一个 Task 内的多轮对话，而不需要创建新 Task。

---

## 已知局限

### 1. 签名生态的成熟度问题

Agent Card 签名（RFC 8785 + JWS）在技术上是严谨的，但**公钥分发和撤销机制**在 1.0 规范中是缺位的。`jku` 字段指向 JWKS URL，但：

- JWKS 的更新通知机制没有标准化
- 私钥轮换后旧签名如何失效，没有明确的策略
- 跨信任域的公钥发现仍是开放的工程问题

生产环境中，A2A 的签名验证强度取决于各厂商的实现质量参差不齐。

### 2. 身份与授权的分离带来的复杂性

A2A 将「身份验证」放在协议层（TLS + 凭证），「授权」放在实现层（各 Agent 自己的策略引擎）。这个设计符合企业架构原则，但造成的后果是：两个 A2A 兼容的 Agent **不一定能互操作**——它们可能彼此通过身份验证，但在授权策略上不兼容。这在实际的企业集成中是一个高频踩坑点。

### 3. 规范的复杂度

3611 行的规范文本，对于一个「让 Agent 互相发现和通信」的协议来说，复杂度偏高。三层架构虽然清晰，但 Layer 2 的操作语义包含了大量边缘情况（幂等性保证、错误码映射、多语言字段处理），导致实现者需要仔细阅读才能正确理解行为。

---

## 一手资源

- [A2A Protocol 1.0 规范全文](https://github.com/a2aproject/A2A/blob/main/docs/specification.md)
- [A2A Protocol 1.0 发布公告](https://a2a-protocol.org/latest/announcing-1.0/)
- [RFC 7515 — JWS（JSON Web Signature）](https://tools.ietf.org/html/rfc7515)
- [RFC 8785 — JCS（JSON Canonicalization Scheme）](https://tools.ietf.org/html/rfc8785)

---

**结论**：A2A Protocol 1.0 的核心价值不是 JSON-RPC 消息传递，而是**信任基础设施**——通过 Signed Agent Cards（JWS + RFC 8785）实现跨组织身份验证，通过 `A2A-Version` 版本协商实现协议演进，通过 Web-aligned architecture（HTTP/JSON-RPC）实现企业级运营可观测性。这三个设计决策共同构成了多 Agent 协作的生产级信任基础。它的局限在于签名生态不成熟、身份与授权的分离带来集成复杂度，以及规范本身的实现难度。在 LangChain Interrupt 2026 之前，这个协议值得作为多 Agent 架构的基础层纳入技术选型评估。
