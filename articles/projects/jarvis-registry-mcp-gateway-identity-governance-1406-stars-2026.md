# jarvis-registry：企业 MCP 网关身份治理实现

> **核心定位**：开源 MCP / Agent gateway，为任意 AI 助手或自主 agent 提供**单一、安全的接入点**，内置 identity（身份认证）、access control（访问控制）、full observability（完整可观测性）。
>
> **Stars**：1,406 ⭐ | **License**：Apache-2.0 | **首发**：2025-10 | **最近更新**：2026-06-19

---

## 项目快照

| 字段 | 值 |
|------|----|
| 仓库 | [ascending-llc/jarvis-registry](https://github.com/ascending-llc/jarvis-registry) |
| 描述 | "Connect any AI copilot or autonomous agent to your enterprise tools — through a single, secure MCP/Agent gateway with built-in identity, access control, and full observability." |
| Topics | `agent` / `agent-gateway` / `agent-orchestration` / `mcp` / `mcp-gateway` / `orchestration` |
| 协议实现 | MCP gateway + Agent orchestration |
| 部署形态 | 自托管（self-hosted）|

---

## 与 Pair Article 的维度对位

| 维度 | 文章（Anthropic Enterprise-Managed Auth）| jarvis-registry |
|------|----------------------------------------|------------------|
| **机制定位** | 协议扩展起草者（标准制定）| 开源 gateway 实现（落地参考）|
| **核心机制** | Cross-App-Access (XAA) 嵌入 MCP 授权扩展 | 单一入口 + 身份/访问控制/可观测 |
| **覆盖范围** | 跨厂商标准（Okta + 7 家 MCP provider 同步）| 单部署统一接入（任意 agent）|
| **形式** | 闭源 spec + 闭源实现 | Apache-2.0 开源 gateway |
| **Pair 强度** | — | ⭐⭐⭐⭐⭐（标准 ↔ 实现 强对位）|

**Pattern 22 (R349)**：标准制定 ↔ 开源实现 = 五星配对闭环。

---

## 为什么这个 Project 是文章的最佳 Pair

### 1. 关键词字面级对位（SPM Layer 2）

文章（Anthropic）使用的核心命题词与 jarvis-registry README 字面级共享：

| 关键词 | 文章出现 | Project 出现 |
|--------|---------|--------------|
| `identity` | ✅ IdP 身份治理 | ✅ "built-in identity" |
| `access control` | ✅ "IdP controls access" | ✅ "built-in access control" |
| `MCP gateway` | ✅ Cross-App-Access 在 MCP 层 | ✅ "MCP gateway" topic |
| `enterprise tools` | ✅ IT 治理企业 SaaS | ✅ "your enterprise tools" |
| `observability` | ✅ 审计可追溯 | ✅ "full observability" |
| `single secure entry` | ✅ "when employee logs in" | ✅ "single, secure ... gateway" |

**6 个核心命题词字面级同时命中** — 远超 R361 Path C 协议 "≥2 个同构关键词" 的最低要求。

### 2. 协议层互补（Pattern 21b 反向）

| 维度 | 文章 | Project |
|------|------|---------|
| 角色 | 协议扩展定义者（Cross-App-Access 嵌入）| 网关流量代理实现 |
| 抽象层 | 协议层 | 部署层 |
| 厂商定位 | 跨厂商标准 | 单部署统一接入 |
| 形式 | 闭源 spec | Apache-2.0 开源 |

**抽象 ↔ 实现** + **跨厂商 ↔ 单部署** + **闭源 ↔ 开源** = 三层维度互补，形成完整 stack 闭环。

### 3. 解决路径完全对应

文章描述的问题："MCP 连接器的 OAuth 授权是逐用户、逐连接器的同意流程" → 解决路径 = IdP 治理 + 单一授权入口。

jarvis-registry 的实现：**"single, secure MCP/Agent gateway with built-in identity"** = 同样以"单一安全入口 + 内置身份"为解决路径。

---

## jarvis-registry 自身的工程亮点

### 1. 不绑定具体 agent 框架

项目自定位 "Connect **any** AI copilot or autonomous agent" — 不绑定 Claude Code、Codex CLI 或 Cursor。**这与 Enterprise-Managed Auth 不绑定具体 IdP 是同一思路**（Okta 首发 + 其他 IdP coming soon）。

### 2. 内置三件套而不仅是 proxy

- **Identity**：内置身份验证（不依赖外部服务拼装）
- **Access control**：内置授权控制（registry-level policy）
- **Observability**：内置可观测性（流量 + 决策日志）

**不是 "yet another MCP proxy"** — 是 registry + gateway + observability 三合一。这种"网关集成身份/可观测"的模式与 `archestra-ai/archestra` (3,864⭐ AGPL-3.0) 方向相似，但 jarvis-registry 用 Apache-2.0 + 更轻定位。

### 3. Topics 命中 mcp-gateway + agent-gateway 双标签

Topics = `['agent', 'agent-gateway', 'agent-orchestration', 'mcp', 'mcp-gateway', 'orchestration']` —
- `mcp-gateway` 直接命中 MCP 协议治理维度
- `agent-gateway` + `agent-orchestration` 命中更上层的 agent 集群管理

**R397 协议 #36 目标生态 topics 三级信号判定**：`mcp` / `mcp-gateway` / `agent-gateway` 属于间接命中 ⭐⭐⭐（"claude-code" / "anthropic" / "agent" 级别），综合 ⭐⭐⭐⭐。

---

## Cluster 子维度定位

`articles/tool-use/` cluster 既有 MCP 文章盘点（截至 R454）：

| 文章 | 子维度 |
|------|--------|
| `mcp-production-transport-session-discovery-architecture-2026.md` | 传输层 |
| `mcp-production-engineering-five-lessons-2026.md` | 生产工程 lesson |
| `mcp-dns-rebinding-cve-2026-34742-attack-surface-2026.md` | 攻击面 |
| `mcp-security-cve-systemic-analysis-2026.md` | 系统性安全 |
| `mcp-enterprise-infrastructure-mcp-dev-summit-2026.md` | 基础设施层 |
| `claude-blog-building-agents-that-reach-production-systems-with-mcp-2026.md` | 部署层 |
| `anthropic-code-execution-with-mcp-98-percent-token-reduction-2026.md` | 执行层 |

**新维度 = "授权治理层"**（IdP 集成 + 跨应用身份联邦）— 7 篇既有文章 0 命中，是 cluster 内 0→1 启动。

jarvis-registry 的角色 = 该新维度的开源工程化身。

---

## License 验证

```bash
$ curl -s https://api.github.com/repos/ascending-llc/jarvis-registry | grep spdx_id
"spdx_id": "Apache-2.0"
```

**清洁度判定**：✅ Apache-2.0 — Production-friendly，无需二次验证（对比 R331 协议 NOASSERTION 风险路径）。

---

## 配套 / 替代候选对照

| 候选 | Stars | License | 关系 |
|------|-------|---------|------|
| **ascending-llc/jarvis-registry**（本文选）| 1,406 | Apache-2.0 | 单一网关 + 内置三件套 |
| archestra-ai/archestra | 3,864 | AGPL-3.0 | 更重（含 guardrails + registry + orchestrator），但 AGPL 网络 copyleft 风险 |
| agentic-community/mcp-gateway-registry | 716 | Apache-2.0 | 社区版本，stars 不足 1000（按 R337 协议未达标）|
| lasso-security/mcp-gateway | 376 | MIT | Stars 不足 1000 |

**选择 jarvis-registry 的核心理由**：
1. Apache-2.0 清洁（对比 archestra AGPL-3.0）
2. Topics 包含 `mcp-gateway` 直接命中目标
3. 描述字面级包含 6 个对位关键词
4. 活跃维护（2026-06-19 最近更新）

---

## 引用源

- 仓库主页：https://github.com/ascending-llc/jarvis-registry
- 配套 Article：`articles/tool-use/anthropic-enterprise-mcp-authorization-idp-governance-2026.md`
- License 验证：GitHub API（验证于 2026-06-19 via `api.github.com/repos/ascending-llc/jarvis-registry`）
- 协议参考：Cross-App-Access (XAA) by OpenID Foundation