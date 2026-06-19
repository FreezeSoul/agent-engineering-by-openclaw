# Anthropic 企业 MCP 授权 + IdP 治理 2026

> 分类：tool-use
> 来源：[claude.com/blog/enterprise-managed-auth](https://claude.com/blog/enterprise-managed-auth) | 2026-06-18 | Anthropic
> 阶段：Stage 4（Production Engineering — 身份治理层）
> 评估：MCP 第一次获得**原生企业授权层**——IdP 治理替代逐个 OAuth 同意，MCP 从"工具协议"升级为"受治理基础设施"

---

## 背景：MCP 连接器的"最后一公里"问题

截至 2026 年 6 月，MCP 已经走完三段旅程：

| 阶段 | 时间 | 焦点 | 关键里程碑 |
|------|------|------|------------|
| 协议诞生 | 2024-11 | 工具调用标准 | Anthropic 发布 MCP |
| 厂商采纳 | 2025-上半年 | OpenAI/Google 加入 | 双巨头支持 |
| 企业化 | 2026-Q2 | 治理 + 安全 + 部署 | AAIF 成立、SDK 月下载 1.1 亿 |

但**企业部署的最后一公里**一直是隐性痛点：**MCP 连接器的 OAuth 授权是逐用户、逐连接器的同意流程**。一个 2000 人的工程团队要接入 15 个 MCP 连接器（Asana/Atlassian/Linear/Slack 等），意味着：

- 每个新员工入职要做 15 次 OAuth 同意
- 每个离职员工留下 15 个孤儿授权
- IT 管理员无法集中撤销（必须分别到 15 个 SaaS 后台）
- 工作账号和个人账号混用风险高（员工可能误把个人 Slack 链接到公司 Claude）

Anthropic 在 2026-06-18 发布 **Enterprise-Managed Authorization** 扩展（基于 Cross-App-Access 协议），正是为最后一公里补上**身份治理层**。

---

## 第一原理：Enterprise-Managed Authorization 的核心机制

### 1. 三方角色重新划分

| 角色 | 传统 MCP | Enterprise-Managed Auth |
|------|----------|------------------------|
| 授权发起方 | 用户逐个点击 | IdP（Okta 等）单次配置 |
| 权限作用域 | 个人 OAuth scope | IdP 组 + 角色继承 |
| 撤销路径 | 各自 SaaS 后台 | IdP 单点撤销 |
| 工作/个人隔离 | 用户自行辨别 | 强制 IdP-only 模式 |

### 2. 关键设计原则

**原则 A：连接一次，所有人生效**

> "When an employee logs in, their connectors are already there."

管理员在 IdP 配置一次 IdP ↔ MCP 授权映射，所有该 IdP 组成员登录 Claude 时**自动获得对应连接器**。不再有 per-user OAuth 弹窗。

**原则 B：访问决策回到 IdP**

每次 MCP 工具调用，Claude 通过**带签名的 token** 向 MCP provider 验证权限。MCP provider 信任 IdP 签发的访问决策，**不再单独存用户授权状态**。

**原则 C：强制 IdP-only 防止账号混用**

管理员可启用"必须经过 IdP 连接"开关——员工无法把个人账号链接到公司 Claude。Okta 的 Cross-App-Access 协议在底层强制这一隔离。

### 3. 三大角色与首批支持矩阵

**Identity Providers（治理访问的身份源）**
- ✅ **Okta**（首发）
- 🔜 其他 IdP（公告"coming soon"）

**MCP Providers（支持新标准的连接器）**
- ✅ **Asana, Atlassian, Canva, Figma, Granola, Linear, Supabase**（7 家首发）
- 🔜 **Slack**（"coming soon"）

**首批客户企业**
- **Hubspot, Ramp, Webflow** 等

这一矩阵透露两个信号：(a) **新协议首发得到 Atlassian/Canva/Figma 等大厂同步支持**——不是孤立标准；(b) **首批企业都是 SaaS-native 公司**——他们早已用 IdP 治理员工 SaaS 访问，MCP 只是新接入的一个端点。

---

## 协议层：Cross-App-Access 与 MCP 的嵌入

### OpenIG / OpenID Foundation 背景

Enterprise-Managed Authorization 不是 Anthropic 私有的协议——它是 **Cross-App-Access (XAA)** 协议的 MCP 实现。XAA 由 OpenID Foundation 起草，是 OAuth 2.0 的演进，专门解决"工作流跨应用"场景：

```
传统 OAuth：    用户 → [同意页] → 应用 A 应用 B 应用 C (各做各的)
Cross-App-Access：用户 → IdP（Okta） → 应用 A 应用 B 应用 C (IdP 统一授权)
```

Anthropic 把 XAA 嵌入到 MCP 的授权扩展层，意味着 **MCP 第一次有了"应用身份"层**——传统 OAuth 是"用户身份"，XAA 让 MCP provider 能识别"调用来自哪个 IdP 治理下的用户"。

### 协议扩展点

MCP 规范新增 `Enterprise-Managed Authorization` 扩展类型。任何 MCP provider 实现该扩展后：
- 接受来自 Claude 的 `id_token` 而非 `access_token`
- 通过 IdP 的 JWKS 验证 token 签名
- 按 IdP 组/角色映射本地权限

**这对 MCP provider 的工程影响**：(a) 需要部署 IdP 公钥缓存（JWKS endpoint）；(b) 需要把"用户角色"逻辑从本地 DB 移到 IdP 同步；(c) 需要支持"只接受 IdP 调用"开关以隔离个人账号。

---

## 实战数据：客户案例与效率提升

### Slack 视角（即将上线）

> "Slack is the place where humans and agents are working side by side, in the same conversation, with the same context, toward the same goals."

Slack MCP 团队明确把"human-agent 协作"作为 Enterprise-Managed Auth 的核心场景——员工的 Slack 身份就是他们的 agent 身份，**不必每次重新授权**。

### Supabase 视角

> "The only way to use Supabase through Claude was to be an org owner or hand out Personal Access Tokens to everyone on your team. Enterprise-managed auth fixes that."

Supabase 揭示了 Enterprise-Managed Auth 解决的**历史困境**：要么 admin 自己用，要么每个工程师拿 Personal Access Token（安全风险）——Enterprise-Managed Auth 让 IdP 控制一切，**个人 PAT 不再必要**。

### Ramp 视角

> "Our team opens Claude and every tool they're cleared for is right there, scoped by the identity groups IT already runs. Enterprise-managed auth turned AI into something people use instead of request."

Ramp 给出最简洁的效果描述：**AI 从"要审批的工具"变成"自然会用的工具"**——这是 Enterprise-Managed Auth 的产品级目标，零摩擦接入。

### 量化数据点

- **Webflow**："2,000 employees, per-connector OAuth approvals 队列归零"
- **Atlassian Rovo MCP**：接入时间从按周降到"log in to Claude on day one"
- **Canva**："95% of Fortune 500 trust Canva" + MCP server + Enterprise-managed auth = 一致的品牌体验入口

---

## Cluster 0→1 启动：MCP 授权治理作为新子维度

### 既有 MCP 文章盘点（截至 R454）

| 文章 | 子维度 | 关键机制 |
|------|--------|----------|
| `mcp-production-transport-session-discovery-architecture-2026.md` | 传输层 | Streamable HTTP 状态管理 + 服务发现 |
| `mcp-production-engineering-five-lessons-2026.md` | 生产工程 | 5 个 lesson（鉴权/限流/可观测等） |
| `mcp-dns-rebinding-cve-2026-34742-attack-surface-2026.md` | 攻击面 | CVE 安全审计 |
| `mcp-security-cve-systemic-analysis-2026.md` | 系统性安全 | 协议层架构缺陷 |
| `mcp-enterprise-infrastructure-mcp-dev-summit-2026.md` | 基础设施层 | AAIF 治理 + 1200 人峰会 |
| `claude-blog-building-agents-that-reach-production-systems-with-mcp-2026.md` | 部署层 | 集成模式 |
| `anthropic-code-execution-with-mcp-98-percent-token-reduction-2026.md` | 执行层 | 98% token 优化 |

**所有 7 篇既有文章无一覆盖"授权 / IdP 治理"子维度**。本文是 `articles/tool-use/` cluster 内 **授权治理 0→1 启动**。

### 与既有 cluster 的维度差异

| 维度 | 既有文章焦点 | 本文焦点 |
|------|-------------|----------|
| 协议层 | Streamable HTTP 传输 | OAuth → IdP 治理迁移 |
| 工程层 | 服务发现 + 限流 | 跨应用身份联邦 |
| 安全层 | CVE 攻击面 | 治理层防滥用 |
| 部署层 | 集成模式 | IT 管理员单点配置 |

**协议层互补**而非重叠：既有文章谈"MCP 怎么把工具接好"，本文谈"MCP 怎么让 IT 把人管好"。

---

## Pattern 22 维度互补判定

### 文章与配套 Project 的对位矩阵

| 维度 | 文章（Anthropic 一手源）| Project（jarvis-registry）|
|------|------------------------|---------------------------|
| 角色 | 协议扩展起草者 | 网关开源实现 |
| 焦点 | 授权语义 + IdP 协议 | 流量代理 + 权限执行 |
| 范围 | 跨厂商标准 | 单部署统一接入 |
| 形式 | 闭源 spec + 闭源实现 | 开源 gateway |

**Pair 闭环强度 ⭐⭐⭐⭐⭐**：文章（标准制定）↔ Project（开源落地）形成完整 stack。

---

## 工程影响清单

### 对 MCP provider（Asana/Atlassian 等）

1. 实现 `Enterprise-Managed Authorization` 扩展（接受 IdP token）
2. 部署 JWKS endpoint 或使用托管 IdP SDK
3. 把"用户角色"逻辑从本地 DB 迁移到 IdP 同步
4. 提供"只接受 IdP 调用"开关

### 对企业 IT 管理员

1. 在 IdP（Okta 等）配置 Claude ↔ MCP provider 授权映射
2. 按 IdP 组/角色控制员工可用连接器
3. 离职流程：撤销 IdP 账号 → 所有 MCP 访问自动失效
4. 审计：所有 MCP 调用可追溯到 IdP 用户身份

### 对 MCP 生态

- **正向**：标准化授权让 MCP 进入大型企业的合规清单（SOX/HIPAA 等）
- **风险**：IdP 绑定——如果只用 Okta，其他 IdP 用户被排除（Anthropic 公告其他 IdP coming soon）
- **机会**：MCP provider 不必自己实现用户管理——专注工具能力

---

## 总结：MCP 的"身份治理层"补完

Enterprise-Managed Authorization 把 MCP 从"工具协议"推到"受治理基础设施"。Cross-App-Access 协议嵌入让 MCP 在 OAuth 之上获得**应用身份层**，这是企业 IT 能够接受 MCP 的**最后一个技术前提**。

**对 Agent Engineering 仓库的意义**：

- `articles/tool-use/` cluster 新增**授权治理**子维度（与传输层、攻击面、安全系统性分析、部署模式互补）
- 配套 Project `ascending-llc/jarvis-registry`（1,406⭐ Apache-2.0）提供开源 gateway 落地参考
- Pattern 22 五星配对：标准制定 ↔ 开源实现

下一步值得追踪的子主题：(a) Slack MCP 加入后的"human-agent 协作"治理；(b) Anthropic 公告的"additional identity providers"具体名单；(c) MCP 治理在 SOX/HIPAA 合规清单中的位置。