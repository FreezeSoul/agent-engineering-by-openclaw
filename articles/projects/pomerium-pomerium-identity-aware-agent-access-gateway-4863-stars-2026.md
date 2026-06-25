---
title: "pomerium/pomerium：身份感知 Agent 访问网关（4.9K Stars）"
date: 2026-06-26
tags: [Pomerium, Agent, Identity, Access-Control, Zero-Trust, MCP, Gateway, OpenSource]
description: Pomerium 是开源身份感知代理（identity-aware proxy），正在新增 Agentic Access Gateway ——把 AI Agent 当一等公民身份做 per-request 鉴权、context-aware 策略、JIT 凭证、跨 MCP tool 集中 audit，4.9K Stars / Apache-2.0。
---

# pomerium/pomerium：身份感知 Agent 访问网关（4.9K Stars）

> **亮点**：Pomerium 是**生产级身份感知代理**（identity-aware proxy），正在构建 **Agentic Access Gateway** ——把 AI Agent 当作一等公民身份（first-class identity），per-request 鉴权、context-aware 策略、just-in-time 凭证、跨 MCP tool 集中 audit。**4,863 Stars · Apache-2.0 · Go**。

**引用来源**：[pomerium/pomerium](https://github.com/pomerium/pomerium) · [HN: Show HN – Pomerium Agentic Access Gateway](https://news.ycombinator.com/item?id=43887439)

---

## 一、它解决了什么问题

### 1.1 MCP 协议的授权空白

2026 年 MCP（Model Context Protocol）成为 Agent 调用工具的事实标准，但 MCP spec 只关注「工具如何被发现和调用」，**per-request 授权完全空白**：

> *"The current MCP spec focuses on tool interaction and discovery but leaves per-request authorization largely undefined. Relying solely on initial OAuth scopes, as suggested, falls short for dynamic agent workflows where context can change mid-task."*  
> —— Pomerium Agentic Access Gateway 公告

**三个核心缺口**：

1. **OAuth scopes 是粗粒度、静态的**——授权一次后不能随任务上下文动态收紧
2. **AuthZ 逻辑推到每个 tool**——每个 MCP server 各自实现策略，造成安全 sprawl
3. **无集中审计**——AI Agent 调过哪些 tool、传了什么数据，没有统一 log

### 1.2 AI Agent 时代的 Zero Trust

传统 zero trust 假设「调用方是人」。AI Agent 时代：

- 调用方是**非人类身份**（non-human identity）
- 调用频次是人的 1000×
- 调用上下文（context）每次都不同
- 凭证一旦泄漏比人类 OAuth token 危险 10×（Agent 可自主行动）

Pomerium Agentic Access Gateway **把 zero trust 范式扩展到 AI Agent**：

> *"It treats AI agents as first-class identities that carry context and require policy checks at each step."*

---

## 二、6 大核心能力

### 2.1 集中策略执行（Centralized Policy Enforcement）

Pomerium 充当所有 MCP tool（及其他 agent API）的网关：

- **一个地方**定义和执行访问策略
- 替代「每个 MCP server 各自实现 authz」的 sprawl 模式
- 减少 N 个 tool 的 N 次安全审计为 1 个 gateway 的 1 次审计

### 2.2 Context-aware 策略

每个 Agent 请求都过 policy check：

- **Who**：agent 代理谁（哪个 user / service account）
- **What**：尝试访问什么数据
- **Anomaly**：行为是否异常（相对历史 baseline）
- 任一不通过 → **当场拒绝**

**对比传统 OAuth**：OAuth 在 connection 时检查 scope；Pomerium 在每个 request 时检查 policy。粒度细 100×。

### 2.3 复用现有身份系统

Agent 通过标准 OAuth2.1 / OIDC 流程鉴权：

- Agent 行为可追溯到真实 user 或 service account
- 例：Alice 的 agent 继承 Alice 的权限（**只继承你允许的部分**）
- 不需要发明新的身份协议，复用企业已有 IdP

### 2.4 Just-in-Time 凭证（JIT）

替代静态 API keys：

- Agent 通过 Pomerium 请求访问 → 拿到 **短时 token**（scoped to specific task/tool）
- 没有「one token to rule them all」长期泄漏风险
- Token 自动过期，scope 自动收紧

**对比传统 API key**：key 一旦签发就长期有效；JIT token 仅当次任务有效。

### 2.5 集中审计

所有 Agent 行动都过一个 gateway：

- 单一审计日志
- 易合规、易调试
- 「哪个 AI 何时做了什么」一目了然

### 2.6 与现有工具栈兼容

由于构建在 Pomerium 之上：

- **不用改 MCP server 代码**
- 不用重写现有 agent
- 直接把 Pomerium 放在 agent 和 tool 之间

---

## 三、对比 Octelium（已收录项目）

| 维度 | Pomerium | Octelium |
|---|---|---|
| **核心定位** | 身份感知代理（鉴权 + authz） | 零信任 + MCP 隧道（网络层） |
| **Stars** | 4.9K | 3.9K |
| **License** | Apache-2.0 | AGPL-3.0 / Apache-2.0 dual |
| **协议层** | HTTP/gRPC 应用层 | WireGuard / QUIC 网络层 |
| **核心问题** | 谁能调用这个 tool | tool server 如何不暴露公网 |
| **Agent 角度** | per-request AuthZ | outbound 隧道隔离 |
| **互补关系** | 鉴权层 | 网络层 |

两者**不竞争而是互补**：

- Octelium 解决「internal MCP server 不暴露公网」
- Pomerium 解决「Agent 调用每个 tool 时谁能鉴权」

部署上可同时使用：Octelium 做网络层隔离，Pomerium 做应用层鉴权。

---

## 四、与 Claude Tag Agent Identity 的呼应

**[Claude Tag Agent Identity（6/24 发布）](../security/anthropic-claude-tag-agent-identity-multiplayer-access-model-2026.md)** 与 Pomerium Agentic Access Gateway 在哲学上完全同构：

| Claude Tag 概念 | Pomerium 对应 |
|---|---|
| Agent 有自己的 service account | Agent 是一等公民身份 |
| Channel-scoped identity | Per-request AuthZ context |
| Workspace baseline + channel override | Workspace policy + per-tool override |
| Audit 双写（集中 + 系统自有 log） | 集中 audit log + 系统自有 log |
| Just-in-time credentials（next） | Just-in-time tokens（已实现） |

**区别**：

- Claude Tag 是**商业产品**（绑定 Claude）
- Pomerium 是**开源基础设施**（不绑定任何 LLM）

**对于自建 Agent 平台的企业**：Pomerium 是当下能用的 open source 答案。

---

## 五、典型使用场景

### 5.1 企业内部 Agent 平台

- 自研 agent 调用内部 CRM / ERP / 数据仓库
- 每个 tool 都需要不同 user 权限级别
- 集中审计（SOX / GDPR 合规）

### 5.2 多租户 SaaS 的 Agent 功能

- SaaS 提供商让自己的 agent 调用客户的 API
- 客户 OAuth 授权 agent 短时访问
- provider 不能 long-lived 持有客户凭证

### 5.3 Agent-to-Agent（A2A）协作

- 多个 agent 互相调用
- 每个 agent 都需要明确身份 + 策略
- 避免「agent A 借 agent B 的 token 横向移动」

---

## 六、值得收藏的 5 个 takeaway

1. **MCP 协议需要从 connection-time scopes 升级到 per-request AuthZ**
2. **AI Agent 是一等公民身份**（first-class identity），不是借用人类 OAuth token 的工具
3. **Zero Trust 范式要扩展到 non-human identity**——Agent 频次 1000× 人，泄漏面 10× 大
4. **JIT 凭证替代静态 API keys**——token scoped 到任务、自动过期
5. **集中 audit 是合规的最短路径**——所有 agent 行动过一个 gateway

---

## 七、生产部署建议

### 7.1 与 IdP 集成

Pomerium 原生支持：

- Okta
- Google Workspace
- Azure AD
- Auth0
- Keycloak（开源）

接入后 agent 的 identity 直接对应企业 IdP 中的 user / group。

### 7.2 与 MCP server 集成

无需改 MCP server 代码：

- MCP server 监听 internal port（127.0.0.1）
- Pomerium reverse proxy 该 port
- Agent 通过 Pomerium 调用 MCP server
- 所有 request 走 Pomerium policy

### 7.3 与现有 audit 栈集成

Pomerium 支持把 log 推到：

- Splunk
- Datadog
- ELK
- S3 + Athena

---

**引用来源**：
- [pomerium/pomerium GitHub](https://github.com/pomerium/pomerium)
- [Show HN: Pomerium Agentic Access Gateway – dynamic auth for AI agents](https://news.ycombinator.com/item?id=43887439)
- [Pomerium Agentic Access Gateway documentation](https://www.pomerium.com/docs)

**关联阅读**：
- [Anthropic Claude Tag Agent Identity：多玩家 Agent 的访问控制新范式](../security/anthropic-claude-tag-agent-identity-multiplayer-access-model-2026.md) — 商业对位
- [octelium/octelium：自托管零信任 + MCP 隧道的开源对位](../projects/octelium-octelium-zero-trust-mcp-gateway-self-hosted-ztna-3874-stars-2026.md) — 网络层 zero trust
- [Anthropic zero-trust AI agents three-tier framework](../harness/anthropic-zero-trust-ai-agents-three-tier-framework-2026.md) — 传统 zero trust 框架
- [Claude Code sandboxing: OS-level isolation](../harness/anthropic-claude-code-sandboxing-os-level-isolation-2026.md) — 另一类 Agent 安全边界
