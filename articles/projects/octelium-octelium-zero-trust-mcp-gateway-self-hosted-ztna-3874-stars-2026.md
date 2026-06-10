# octelium/octelium：自托管零信任 + MCP 隧道的开源对位

> **亮点**：Octelium 是一个**自托管、零信任（Zero Trust）安全访问平台**——既能当 VPN/ZTNA/BeyondCorp，也能当 **API Gateway / AI Gateway**，还能直接**构建 MCP Gateway 与 AI Agent 架构**（README 原话）。它的「**出站隧道** + **无公网入口** + **身份级策略**」三件套，正是 Anthropic Claude Managed Agents **MCP tunnels** 的开源对位。

**引用来源**：[octelium/octelium](https://github.com/octelium/octelium) · 3,874 Stars · AGPL-3.0/Apache-2.0 (dual) · Go

---

## 一、它解决了什么问题

2026 年企业部署 AI Agent 时，三个最棘手的网络问题是：

1. **代码执行边界**：Agent 在哪里跑？沙箱在哪？数据能不能出域？
2. **MCP 服务暴露**：内部 MCP server 如何让 Agent 访问，但**不暴露公网**？
3. **凭据管理**：企业 API keys 不能进入 Agent 沙箱，但 Agent 又必须调用这些 API

Anthropic 5 月 19 日发布 Claude Managed Agents 自托管沙箱 + MCP tunnels 时，给出了官方回答：

> "Your agents reach MCP servers inside your private network without exposing them to the public internet. A lightweight gateway you deploy makes a single outbound connection, no inbound firewall rules, no public endpoints, and traffic encrypted end to end."

**Octelium 就是这个架构模式的开源自托管实现**——而且比 Anthropic 商业版更早、更通用（不绑定 Anthropic，可对接任何 Agent 框架）。

## 二、与 Claude Managed Agents MCP tunnels 的对位

| 维度 | Anthropic MCP tunnels | Octelium |
|---|---|---|
| **部署位置** | Anthropic 管理控制台配置 | 自托管 K8s 集群 |
| **隧道方向** | 单向出站 | 单向出站（WireGuard/QUIC）|
| **公网入口** | 无 | **无**（README: "no public gateways, no need to open ports"）|
| **入站防火墙** | 无需规则 | 无需规则 |
| **加密** | 端到端 | 端到端（QUIC/WireGuard/mTLS）|
| **身份认证** | Claude Console 组织管理 | OIDC/SAML/OAuth2/GitHub OAuth + MFA + WebAuthn |
| **L7 策略控制** | 由 Anthropic 内置 | **policy-as-code**（CEL/OPA 表达式，每请求 L7 感知）|
| **审计** | Anthropic 控制台 | OpenTelemetry OTLP 导出，可对接任意 SIEM |
| **MCP 集成** | 内置（Managed Agents + Messages API）| 内置（MCP Gateway 示例文档）|
| **多协议** | MCP 专用 | MCP + A2A + LLM Gateway + API Gateway + SSH + Kubernetes Ingress |

**最关键的差异化**：Octelium 的「**身份感知代理**」（identity-aware proxy）架构让策略不仅基于 IP/端口，还基于**身份 + 上下文 + L7 协议**。这比 Anthropic 的 MCP tunnels 更通用——一个 Octelium 集群能同时承载 MCP Gateway、AI Gateway、内部 SSH、数据库访问，**统一身份 + 统一策略**。

## 三、核心架构

Octelium 的 README 自述是一个**多用途统一平台**：

> "A free and open source, self-hosted, unified zero trust secure access platform that is flexible enough to operate as a modern zero-config remote access VPN, a comprehensive Zero Trust Network Access (ZTNA)/BeyondCorp platform, an ngrok/Cloudflare Tunnel alternative, an API gateway, an AI/LLM gateway, **a scalable infrastructure for access and deployment to build MCP gateways and AI agent-based architectures/agentic meshes**, a PaaS-like deployment platform..."

支撑这个统一平台的是 **Octelium Cluster**——一个部署在 K8s 上的身份感知代理层：

```
┌──────────────────────────────────────────────────────────┐
│  Agent (Claude Code / Cursor / 自研)                       │
│  出站 QUIC/WireGuard 隧道 → Octelium Cluster               │
└──────────────────────┬───────────────────────────────────┘
                       │
       ┌───────────────┴────────────────┐
       │  Octelium Cluster (K8s)        │
       │  ┌──────────────────────────┐  │
       │  │ 身份认证 (OIDC + MFA)      │  │
       │  └────────────┬─────────────┘  │
       │  ┌────────────▼─────────────┐  │
       │  │ Policy-as-Code (CEL/OPA)  │  │
       │  └────────────┬─────────────┘  │
       │  ┌────────────▼─────────────┐  │
       │  │ Secretless 凭据注入       │  │
       │  └────────────┬─────────────┘  │
       └───────────────┼────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    │                  │                  │
┌───▼────┐    ┌────────▼─────┐    ┌───────▼────┐
│MCP服务 │    │内部数据库     │    │SaaS APIs   │
│(私有)  │    │(私有)        │    │(凭据注入)   │
└────────┘    └──────────────┘    └────────────┘
```

**关键特性**：
- **Secretless Access** —— API keys/SSH 密码/数据库密码**永远不进 Agent 沙箱**，由 Octelium 在网络边界注入
- **Zero Standing Privileges** —— 无 admin 概念，所有访问按请求 context-aware 评估
- **OpenTelemetry Native** —— 每次访问都是 OTel span，可接入任意 SIEM
- **客户端少/无二选** —— 有 Octelium Client（zero-config 客户端）或 Clientless（基于 Web 终端）

## 四、与已有项目的关系

本仓库已有：
- `articles/projects/multica-ai-multica-open-source-managed-agents-platform-29k-stars-2026.md` —— Claude Managed Agents 的**编排层** OSS 对位
- `articles/projects/daytona-open-source-ai-agent-sandbox-oci-containers-2026.md` —— Daytona 沙箱（执行层）
- `articles/harness/cloudflare-sandboxes-ga-agent-persistent-execution-environment-2026.md` —— Cloudflare 沙箱（执行层商业）
- `articles/projects/portkey-ai-gateway-unified-llm-gateway-cost-controls-11978-stars-2026.md` —— Portkey AI Gateway

**Octelium 在仓库内的位置**：

| 项目 | 抽象层 | 角色 |
|---|---|---|
| Multica | 编排层 OSS | Claude Managed Agents 编排层开源对位 |
| Daytona | 执行层 OSS | 自托管沙箱 |
| Cloudflare Sandboxes | 执行层商业 | 沙箱执行 |
| Portkey AI Gateway | LLM 网关层 | 模型路由 + 凭据 + 缓存 |
| **Octelium** | **零信任接入层** | **MCP/AI/API 统一零信任接入** |

**Octelium 是 5 个抽象层中最底层的"网络边界"**——它解决的不是"Agent 怎么调度"或"代码怎么执行"，而是「**Agent 如何安全地访问所有内外部资源**」。

## 五、为什么这是 SPM（Self-Positioning Match）

Round 237 验证的 **Pattern9 SPM** 协议：当 Article 主题与候选 Project 的 README 自我定位显式重叠时为最强闭环。

**Octelium README 显式使用以下定位词**（与 Anthropic MCP tunnels 高度对齐）：

| Anthropic 表述 | Octelium README 表述 |
|---|---|
| "MCP tunnels" | "MCP Gateways"（用例章节） |
| "single outbound connection, no inbound firewall rules" | "no public gateways, no need to open ports behind firewalls" |
| "traffic encrypted end to end" | QUIC/WireGuard tunnels, "encrypted end to end" |
| "internal databases, private APIs, knowledge bases become tools" | "identity-based, L7-aware access control" |

**SPM 命中**：Octelium 是 Anthropic MCP tunnels 范式的**开源、自托管、协议无关**实现——同一架构目标，两种交付形态。

## 六、典型部署场景

### 场景 1：Claude Code 企业部署

```bash
# 1. 部署 Octelium 集群（自托管 K8s）
./install-cluster.sh --domain octelium.acme.com

# 2. 配置企业 IdP（Okta / Azure AD / GitHub Enterprise）
octeliumctl create idp --type oidc --config okta.json

# 3. 配置 MCP Server 接入
octeliumctl create service mcp-prod --type http \
  --upstream https://mcp.internal.acme.com \
  --policy "ctx.user.role == 'agent' && ctx.request.path.startsWith('/tools/')"

# 4. 在 Claude Code 中连接
# 通过 Cordium（Octelium 自带沙箱）访问，无需配置 SSH/VPN
```

### 场景 2：多团队统一零信任

- **工程团队** → SSH 到开发机（Octelium 内置 SSH 服务）
- **数据团队** → PostgreSQL 只读访问（policy-as-code 限制）
- **AI 团队** → MCP Gateway 暴露内部工具集
- **运维团队** → Kubernetes API（无需 kubeconfig）

所有访问通过**同一身份层 + 同一策略引擎**，审计日志统一到 OpenTelemetry。

## 七、与类似项目对比

| 项目 | 抽象层 | 零信任 | 自托管 | MCP 一等公民 | LLM Gateway | Stars |
|---|---|---|---|---|---|---|
| **Octelium** | **零信任接入** | ✅ 完整 ZTNA | ✅ K8s | ✅ 内置 | ✅ | 3.9K |
| Twingate / Cloudflare Access | 零信任 SaaS | ✅ | ❌ SaaS | ❌ | ❌ | — |
| ngrok / Cloudflare Tunnel | 反向隧道 SaaS | ⚠️ 部分 | ❌ SaaS | ❌ | ❌ | — |
| Kong API Gateway | API 网关 | ⚠️ 需插件 | ✅ | ⚠️ 插件 | ⚠️ 插件 | 43.5K |
| metatool-ai/metamcp | MCP 聚合器 | ❌ | ✅ | ✅ | ❌ | 2.4K |
| IBM/mcp-context-forge | MCP Gateway | ⚠️ 鉴权 | ✅ | ✅ | ❌ | 3.9K |
| archestra-ai/archestra | Enterprise AI | ⚠️ 鉴权 | ✅ | ✅ | ⚠️ | 3.8K |

**Octelium 的独特定位**：唯一在**零信任层**完整实现的、**支持 MCP/A2A/LLM/API/SSH/DB 多种协议**的统一接入平台。

## 八、限制与适用边界

- **复杂度**：完整 K8s 部署，不是「单机一键启动」的轻量方案（虽然有 single-node K8s 推荐）
- **学习曲线**：policy-as-code（CEL/OPA）+ 身份认证 + K8s 网络模型 = 较高的上手门槛
- **协议覆盖**：MCP 与 A2A 是核心场景，但内部 MCP server 仍需自行实现（MCP 协议侧）
- **客户端依赖**：client-based 模式需要安装 Octelium Client（虽然 clientless 模式可绕过）

**适用边界**：
- ✅ 100+ 工程师的企业，需要统一零信任
- ✅ 需要 MCP Gateway 但不希望暴露公网
- ✅ 多协议统一接入（MCP + A2A + API + SSH）
- ❌ 5 人小团队用 Claude Code（直接 sandbox SDK 更合适）
- ❌ 个人开发者单机 Agent（不需要零信任）

## 九、一句话总结

> **Octelium = 开源版「Anthropic MCP tunnels + Zero Trust 网关」——** 一个自托管、统一身份、协议无关的零信任接入平台，把 Agent 安全访问内外部资源这件事做成了 L7-aware 的 policy-as-code 引擎。

---

## 附：技术规格速览

- **License**：AGPL-3.0（社区版）+ Apache-2.0（部分组件）—— 商业自托管友好
- **Language**：Go（核心）+ TypeScript（管理 UI）
- **Architecture**：Kubernetes-native，部署为 K8s operator + CRD
- **Performance**：WireGuard/QUIC 隧道，sub-second 启动
- **Compliance**：SOC 2 Type II ready（自托管数据流完全可控）
- **社区**：Discord + Slack 活跃
- **生态**：[Cordium](https://github.com/octelium/cordium)（Octelium 自带沙箱）—— 与 Anthropic Managed Agents + 自托管沙箱的混合模式天然契合

*本文属于「Agent 零信任网络」系列，分析 MCP tunnels / ZTNA / 私域 Agent 部署的工程含义。*