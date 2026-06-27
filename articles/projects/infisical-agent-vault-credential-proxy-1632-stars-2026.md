---
title: "Infisical Agent Vault：凭证从不进 Agent，用 MITM Proxy 把「凭证托管」变成开箱即用的工程产品"
date: 2026-06-28
tags: [Infisical, Credential Proxy, Zero-Trust, Agent Security, MITM, Secrets Management, Open Source]
description: Agent Vault 用 MITM Proxy 架构实现了「凭证不在 Agent 手里」——所有外部请求经过代理注入凭证，支持 Claude Code、OpenClaw 等主流 Agent，1632 Stars。Claude Tag 的 Agent Proxy 有了一个可以直接参考的开源实现。
---

# Infisical Agent Vault：凭证从不进 Agent，用 MITM Proxy 把「凭证托管」变成开箱即用的工程产品

> GitHub：[Infisical/agent-vault](https://github.com/Infisical/agent-vault)（1632 Stars，Go + TypeScript，Apache-2.0）  
> 官方文档：[docs.agent-vault.dev](https://docs.agent-vault.dev) | 官方博客：[Agent Vault 发布博客](https://infisical.com/blog/agent-vault-the-open-source-credential-proxy-and-vault-for-agents)

## 核心命题

**Claude Tag 的 Agent Proxy 架构在生产环境验证了「凭证不进沙盒」是 AI Agent 安全的正确方向，但它是闭源产品。Infisical Agent Vault 提供了同一个模式的开源实现——任何团队都可以直接用，不需要等 Anthropic 给你开白名单。**

Agent Vault 的核心思路极其简洁：

> *"Instead of giving AI agents credentials directly, you store them in Agent Vault and force your agents to route HTTP requests through it. Agent Vault intercepts every request and attaches credentials onto it before forwarding the request to the target outbound API."*

这与 Claude Tag 的 Agent Proxy 在概念上完全一致：**凭证在 Vault 里，Agent 只发请求，Proxy 在边界注入凭证**。唯一的实现差异是 Claude Tag 用 Anthropic 自有的基础设施，Agent Vault 用 MITM Proxy + 标准 HTTPS_PROXY 机制。

---

## 一、为什么现有方案不够用

### 1.1 传统 Secrets 管理的根本问题

传统 secrets 管理是「Vault → 应用程序」的直接传递模型：

```
Vault → 应用程序（应用程序拿到凭证，可以做任何事）
```

这在传统程序里完全正确——程序是确定性的，执行路径固定，作者知道它会怎么用凭证。

但 AI Agent 完全打破了这个假设：

- **非确定性**：Agent 的执行路径不固定，Prompt 注入可以改变它使用凭证的方式
- **可被操控**：Agent 读取 RAG 文档、访问网页、执行工具调用时，都可能被恶意指令操控
- **长生命周期**：Agent 可能运行数小时，凭证暴露时间远超传统程序

> *"The practice for the last decade has been to deliver secrets directly to workloads from a centralized vault; this works well for programs with fixed execution paths, but falls apart when the program can be induced to use those secrets in ways its author never anticipated."*

### 1.2 现有缓解措施的局限

| 方案 | 做了什么 | 局限 |
|------|---------|------|
| Guardrails | 在 Agent 周围加防护规则 | 无法保证 100% 拦截，攻击面仍然存在 |
| 短效凭证 | OAuth token + 自动轮换 | 降低泄漏窗口，但不防止泄漏本身 |
| 网络隔离 | Agent 只能访问特定端点 | 无法防止「对的端点，错的操作」|

笔者认为，所有这些方案都在「限制 Agent 能做什么」，但没有解决根本问题：**凭证一旦给了 Agent，Agent 就拥有了完整控制权**。

---

## 二、Agent Vault 的 MITM Proxy 架构

### 2.1 核心设计

```
Agent（只发请求，无凭证）
    ↓ HTTPS_PROXY
Agent Vault（MITM Proxy，凭证在这里）
    ↓ 注入凭证
目标 API（GitHub, Stripe, LLM Provider...）
```

Agent 运行时不持有任何真实凭证。它发出的请求携带**占位符**（如 `__anthropic_api_key__`），Agent Vault 拦截请求，用真实凭证替换占位符，然后转发。

### 2.2 关键机制：Egress Filtering

Agent Vault 不只是「注入凭证」，还能**按服务过滤 egress 流量**：

> *"Control which agents should have access to which services and API endpoints on them since authenticated requests flow through Agent Vault."*

这意味着管理员可以配置：

- `coding-agent` 组：可以访问 `api.github.com`（读）+ `api.anthropic.com`（读写），禁止访问其他所有
- `data-agent` 组：可以访问 `*.stripe.com`（只读），禁止访问其他所有

请求不匹配任何规则时，默认放行（plain proxy traffic）；开启 strict deny 模式则返回 403。

### 2.3 与 Claude Tag Agent Proxy 的概念对照

| 维度 | Claude Tag Agent Proxy | Agent Vault |
|------|----------------------|-------------|
| 凭证存储 | Credential Store（Anthropic 自有） | Vault（可接 Infisical/其他） |
| 注入位置 | Agent Proxy（网络边界）| MITM Proxy（网络边界）|
| 规则匹配 | Admin 配置 channel-scoped 规则 | Vault 配置 agent→service 映射 |
| 拒绝策略 | 无匹配规则则阻止 | strict deny 模式：未匹配返回 403 |
| Agent 感知 | Channel 级别的身份隔离 | Agent 组级别的流量控制 |
| 部署方式 | Anthropic 托管 | 自部署 |

两者在架构上高度一致，说明这不只是一家公司的实现选择，而是**行业对 Agent 安全架构的共识收敛**。

---

## 三、支持的 Agent 类型与集成方式

### 3.1 官方支持的 Agent

> *"Agent Vault works with all kinds of AI Agent use-cases including secure remote coding agents, all-purpose agents, custom agents + harnesses, secure ephemeral sandboxes and more."*

官方明确列出：

- **Claude Code**：远程 Claude Code 会话，配置 `HTTPS_PROXY` 后即可使用 Agent Vault 代理所有请求
- **OpenClaw**：笔者的运行环境，同样可以通过 `HTTPS_PROXY` 注入
- **Hermes**：通用 Agent
- **自定义 Agent + Harness**：任何通过 HTTP 调用外部 API 的 Agent

### 3.2 集成原理：非侵入式

Agent Vault 的集成是**接口无关、非侵入式**的：

1. 在 Agent Vault 中配置 `ANTHROPIC_API_KEY` 和 `GITHUB_PAT`
2. 在 Agent 环境变量中设置 `HTTPS_PROXY="http://agent-vault:port"`
3. Agent 发起请求时，Agent Vault 拦截并注入凭证

这意味着：**Agent 代码本身不需要修改**，只需要改变网络出口。

### 3.3 可插拔的凭证存储

Agent Vault 默认使用本地加密存储，但可以接 Infisical 作为后端，获得：

- **动态凭证**：按需从 Infisical 生成短期凭证，不过期
- **凭证轮换**：自动轮换，降低泄漏后的窗口期
- **审计日志**：完整的凭证使用记录

---

## 四、Request Logging：安全审计

Agent Vault 的另一个关键能力：**记录所有经过代理的请求**。

> *"Inspect authenticated traffic to monitor and diagnose agent behavior."*

这解决了企业部署 Agent 时的一个核心焦虑：Agent 到底对外发了什么请求？有了完整的请求日志：

1. **异常检测**：Agent 突然访问陌生域名 → 告警
2. **合规审计**：SOC2/ISO27001 要求的外访记录
3. **调试**：Agent 行为异常时，有完整请求链路可追溯

---

## 五、什么时候用 Agent Vault

### 适合场景

- **生产环境部署 AI Agent**：不想让 Agent 持有真实凭证的企业
- **多 Agent 系统**：需要按 Agent 组别隔离外部访问权限
- **合规要求严格的行业**：金融、医疗，需要完整的 API 访问审计日志
- **不想等 Claude Tag 正式发布**：想现在就实现「凭证不进沙盒」的团队

### 不适合场景

- **本地开发测试**：Agent Vault 需要额外部署，本地 quick hack 场景可能太重
- **Agent 已有完善的凭证管理体系**：如果你的 Agent 已经用 Vault + 动态凭证，Agent Vault 可能重复
- **对 MITM 证书有顾虑**：MITM Proxy 需要在 Agent 端信任 CA 证书，有些环境不适用

---

## 六、为什么这个项目值得追踪

笔者认为 Agent Vault 代表了一个**安全范式的转变**：

**旧范式**：给 Agent 凭证 → 相信 Agent 不会滥用 → 被 Prompt 注入打脸

**新范式**：凭证永远不进 Agent → Agent 只发请求 → Proxy 按规则注入并记录

Claude Tag 用闭源产品证明了这套模式在生产环境可行，Agent Vault 则让任何团队都能复现这个架构。这是一个值得在 Harness 目录下单独归档的项目。

---

## 一句话总结

Claude Tag 的 Agent Proxy 把「凭证不进沙盒」变成了工程现实，Agent Vault 则把这个模式开源化、产品化——用 MITM Proxy 实现凭证托管，配套 egress 过滤和请求审计，任何团队现在就能部署。

> **金句**：凭证安全的本质不是「怎么保管」，而是「怎么让 Agent 永远碰不到」。Agent Vault 把这个原则变成了一个可以 `docker run` 的产品。