# OpenClaw Gateway 架构：用一个进程连接所有消息表层的工程哲学

> **来源**：[OpenClaw Architecture Docs](https://github.com/openclaw/openclaw/blob/main/docs/concepts/architecture.md)（官方架构文档）
> **主题**：OpenClaw 如何用「单一长驻 Gateway」架构同时接管所有即时通讯渠道的消息总线——以及这种设计背后的工程权衡
> **适用场景**：理解 Agent 系统的消息路由架构、多渠道 Agent 部署、企业级 Agent 基础设施设计

---

## 核心命题：一个进程，所有消息渠道

当大多数 AI Agent 框架还在讨论「如何让 Agent 更好地调用工具」时，OpenClaw 在解决一个更基础的问题：**如何让一个 Agent 同时「活」在 WhatsApp、Telegram、Slack、Discord、iMessage、WebChat 这么多地方，而不需要为每个渠道单独运维一套基础设施。**

OpenClaw 给出的答案是：**一个 Gateway 进程掌控所有消息表层的接入点**。

这不是微服务拆分式的「每个渠道一个服务」，而是更激进的主张——所有渠道的消息路由、安全认证、设备配对、WebSocket 协议解析，都集中在同一个守护进程里（默认绑定 `127.0.0.1:18789`）。

---

## 为什么这值得写

大多数 Agent 框架在「如何让模型更聪明」上卷，但 OpenClaw 在解决一个被低估的基础设施问题：**跨渠道一致性**。

如果你同时在 Slack 和 WhatsApp 上和一个 Agent 对话，你期望它记住上下文。但如果每个渠道各自维护一套会话状态，这个期望就无法自然满足。

OpenClaw 的架构选择让这个期望天然成立——因为 Gateway 是唯一的真相之源，所有渠道的消息都汇入同一个 WS 协议栈。

> **笔者认为**：OpenClaw 的 Gateway 架构本质上是**消息总线的去中心化等价物**——它没有用一个中央服务器把所有渠道聚拢，而是让 Gateway 进程本身成为消息总线，每个渠道只是它的一个接入协议。这种思路在消费级 Agent 场景（个人助手、家庭自动化）非常有价值，但在企业多租户场景可能会遇到运维瓶颈。

---

## 核心架构组件

### Gateway（守护进程）

Gateway 是整个系统的唯一有状态中枢：

- **持有所有渠道连接**：Baileys（WhatsApp）、grammY（Telegram）、Slack、Discord、Signal、iMessage，全部由 Gateway 管理
- **暴露typed WS API**：请求/响应/服务端推送事件（agent、chat、presence、health、heartbeat、cron）
- **协议验证**：所有入站帧都用 JSON Schema 验证
- **单一职责**：是唯一一个打开 Baileys WhatsApp session 的进程

官方原文：

> A single long-lived Gateway owns all messaging surfaces (WhatsApp via Baileys, Telegram via grammY, Slack, Discord, Signal, iMessage, WebChat).

### 控制面客户端（macOS App / CLI / Web UI / Automations）

所有控制面客户端通过 WebSocket 连接到 Gateway：

```
Client → WebSocket → Gateway (127.0.0.1:18789)
```

- 每客户端一个 WS 连接
- 发送请求（health、status、send、agent、system-presence）
- 订阅事件（tick、agent、presence、shutdown）

### 节点（macOS / iOS / Android / Headless）

节点也连接同一个 WS 服务器，但携带 `role: node` 声明：

```json
{
  "type": "req",
  "method": "connect",
  "params": {
    "role": "node",
    "caps": ["canvas.", "camera.", "screen.record", "location.get"],
    "permissions": [...]
  }
}
```

配对基于设备身份（device-based pairing），需要 Gateway 显式审批。

### Canvas Host（Agent 可编辑的 Web 内容）

Gateway 的 HTTP 服务器同时承载两个特殊路径：

- `/__openclaw__/canvas/` — Agent 可编辑的 HTML/CSS/JS 画布
- `/__openclaw__/a2ui/` — A2UI 主机

两者共用 Gateway 的同一个端口，Agent 可以在运行时直接生成并交付 Web 内容给用户。

---

## 连接生命周期：WebSocket 协议的核心流程

```
Client           Gateway
  │                │
  │──req:connect──▶│
  │◀─res: hello-ok─┤  ← 包含 snapshot: presence + health
  │                │
  │◀─event:presence┤
  │◀─event:tick────┤  ← 周期性心跳
  │                │
  │──req:agent────▶│  ← 触发 Agent 执行
  │◀─res: ack ─────┤  ← 立即返回 {runId, status:"accepted"}
  │◀─event:agent───┤  ← 流式输出
  │◀─res: final ───┤  ← 最终结果 {runId, status, summary}
```

**关键设计点**：

1. **Handshake 强制**：第一个帧必须是 `connect`，任何非 JSON 或非 connect 帧都会导致硬关闭
2. **幂等性 Key**：所有有副作用的方法（send、agent）必须带幂等性 key，Gateway 维护短期去重缓存
3. **事件不重放**：客户端必须在断开时刷新状态，不依赖事件重放

---

## 配对与信任模型

OpenClaw 的安全模型围绕设备身份构建：

| 连接类型 | 信任级别 | 配对要求 |
|---------|---------|---------|
| 本地回环（127.0.0.1）| 最高 | 自动审批 |
| Tailscale Serve / trusted-proxy | 高 | 信任请求头，跳过共享密钥 |
| Tailnet / LAN | 中 | 显式配对审批 |
| 公共入口 | 最低 | 禁用 `gateway.auth.mode: "none"` |

配对时，Gateway 为设备颁发一个设备令牌（device token），后续重连用令牌认证。签名 payload v3 还绑定了平台和 deviceFamily，换设备需要重新配对。

---

## Agent 循环：详细执行周期

OpenClaw 的 Agent 循环是独立文档描述的，详细见 [Agent Loop 文档](https://github.com/openclaw/openclaw/blob/main/concepts/agent-loop)。从架构图可以看到它与 Gateway Protocol、Queue、Security 三个模块并列。

这说明 Agent 循环本身是**与消息路由解耦的**——Gateway 负责「收到消息 → 路由到 Agent 循环 → 返回结果」，而 Agent 循环内部怎么处理 Tool Call、Memory、Compact，是另一层抽象。

这种分层带来的实际好处：你可以让同一个 Agent 循环跑在本地 CLI 上，也可以通过 WebSocket 触发它，而不需要改 Agent 本身的代码。

---

## 远程访问方案

| 方案 | 适用场景 | 配置难度 |
|------|---------|---------|
| Tailscale / VPN | 跨网络设备连接 | 简单 |
| SSH Tunnel | `ssh -N -L 18789:127.0.0.1:18789 user@host` | 中等 |
| TLS + WS Pinning | 远程且需加密 | 复杂 |

官方推荐 **Tailscale 或 VPN**，SSH tunnel 作为备选。

---

## 与 Claude Code 的架构对比

| 维度 | OpenClaw | Claude Code |
|------|---------|------------|
| **架构模式** | 单一 Gateway 守护进程 | Claude Agent SDK 循环 |
| **多渠道支持** | 内置（6+ 消息渠道）| 不适用（CLI 工具）|
| **协议层** | WebSocket + JSON Schema | Claude API + Tool Call |
| **Canvas 支持** | 内置（Agent 可编辑 Web）| 无 |
| **节点类型** | macOS/iOS/Android/Headless | 纯 CLI |
| **安全模型** | 设备配对 + 幂等 Key | API Key + OAuth |
| **Stars** | 374K | 闭源 |

**笔者认为**：OpenClaw 的多渠道架构和 Claude Code 的深度编码能力代表了两个不同的 Agent 进化方向：前者解决「Agent 如何无处不在」，后者解决「Agent 如何真正完成任务」。两者并不竞争，而是互补——在企业场景，结合 OpenClaw 的消息接入能力和 Claude Code 的编码能力，可能是下一代 Agent 系统的一种可行组合。

---

## 工程权衡分析

### 做得好的

1. **关注点分离**：Gateway 专注消息路由，Agent 循环专注任务执行，两者通过 WS API 解耦
2. **幂等性设计**：所有副作用操作都要求 idempotency key，防止网络重试导致的重复执行
3. **设备身份安全**：配对和签名机制确保只有授权设备能连接 Gateway
4. **Canvas 内置**：Agent 运行时生成 Web 内容的能力，是大多数框架没有的原语

### 待观察的

1. **单点风险**：一个 Gateway 进程管理所有渠道，如果 Gateway 崩溃，所有渠道同时断连
2. **水平扩展限制**：每个 host 一个 Gateway，在多租户场景需要额外部署机制
3. **协议复杂度**：typed WS API + JSON Schema 验证 + 设备配对，维护成本不低
4. **规模验证**：374K Stars 背后，真正在生产环境运行 OpenClaw Gateway 的企业案例披露有限

---

## 结论

OpenClaw 的 Gateway 架构回答了一个具体问题：**如何让一个 Agent 天然存在于所有主要的消息渠道里**。它用单一进程 + WebSocket 协议 + 设备配对模型实现了这个目标，并在 Agent Loop、Canvas Host、A2UI 等方向上展示了除消息路由之外的更大野心。

对于需要构建「无处不在的个人 Agent」系统的开发者，OpenClaw 的架构提供了有价值的参考。而对于追求「深度任务完成能力」的团队，OpenClaw 的消息层和 Claude Code 的执行层可能是最值得组合的两种能力。

---

## 参考链接

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)（374K Stars）
- [Gateway Architecture 原文](https://github.com/openclaw/openclaw/blob/main/docs/concepts/architecture.md)
- [Agent Loop 文档](https://github.com/openclaw/openclaw/blob/main/concepts/agent-loop)
- [Gateway Protocol](https://github.com/openclaw/openclaw/blob/main/gateway/protocol)
- [Security 文档](https://github.com/openclaw/openclaw/blob/main/gateway/security)