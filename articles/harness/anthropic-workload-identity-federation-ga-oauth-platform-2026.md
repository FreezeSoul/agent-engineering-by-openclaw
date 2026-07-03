---
title: Anthropic Workload Identity Federation GA：把"Claude API Key"从静态密码升级为 OIDC 联邦
date: 2026-07-03
source: https://claude.com/blog/workload-identity-federation
source_docs:
  - https://platform.claude.com/docs/en/manage-claude/workload-identity-federation
  - https://platform.claude.com/docs/en/manage-claude/authentication
  - https://platform.claude.com/docs/en/api/admin/service_accounts/create
  - https://platform.claude.com/docs/en/manage-claude/wif-providers/aws
cluster: harness
subcluster: identity-federation
tags: [workload-identity, oidc, federation, security, authentication, platform]
round: R634
authors: Anthropic Platform team
---

# Anthropic Workload Identity Federation GA：把"Claude API Key"从静态密码升级为 OIDC 联邦

## 一、为什么这件事值得单独写一篇

2026 年 7 月 2 日，Anthropic 把 **Workload Identity Federation（WIF）** 升级到了 **GA（Generally Available）** 状态。这意味着：**从今往后，你的 CI/CD 流水线、Lambda 函数、Kubernetes Pod、GitHub Actions job 不再需要持有 `sk-ant-...` 这种长生命周期 API key**——它们可以直接拿 AWS IAM、Google Cloud、GitHub Actions、Kubernetes、SPIFFE、Microsoft Entra ID、Okta 颁发的 **OIDC 短令牌**，向 Claude Platform 换一张有时长、有归属、有审计的 access token。

听起来像是把"换一种 token"包装了一下。但它实际上是一次**身份模型的范式迁移**：

- **过去**：API key = 静态密码。所有 workload 共享同一个密钥；谁能拿走这个 key，谁就能在 30 天里调用 Claude API；审计只能追溯到"key ID"，追溯不到"哪个 workload 在哪个时刻调用了什么"。
- **现在**：WIF = OIDC 联邦。每次调用都基于 IdP 颁发的短期 JWT，Anthropic 验证后换发绑定到 service account 的 token，**审计粒度到 service account → federation rule → IdP issuer 的完整链路**。

更重要的是，WIF 不只是一个"换 token"的协议，它把 Anthropic 的安全边界从"我信任持 key 的人"升级成了"我信任持 OIDC token 的、且其声明满足我联邦规则的 workload"。这条规则——`fdrl_...`——是 WIF 的灵魂。

## 二、WIF 的三个核心概念

WIF 协议建立在三个相互配合的实体上。把这三个搞清楚，整个机制就清楚了。

### 2.1 Service Account：WIF 的"主体"

Service account（服务账号）是 Claude Platform 内部的一个**命名身份**，它是 workload 在 Claude 这一侧的代表。每个 service account 有：

- **name**：组织内唯一的人类可读名
- **organization_role**：developer（默认）或 admin
- **workspace memberships**：决定这个 service account 归属哪个 workspace（影响 rate limit 与 usage attribution）

关键的设计取舍：**Service account 不是 secret**。它的 ID（`acct_...`）可以在配置里明文写出来，因为它自己不能用来调用 API——必须经过 federation rule 验证 OIDC token 后才会被换发 access token。

### 2.2 Federation Issuer：信任的源头

Federation issuer（联邦签发者）是 Claude Platform 信任的 OIDC token 来源。在 GA 阶段，Anthropic 官方支持的 IdP 包括：

| IdP | 适配场景 |
|------|---------|
| **AWS IAM** | Lambda、EC2、ECS、EKS 上跑的 workload（via STS `GetWebIdentityToken`） |
| **Google Cloud** | GCP 上的 workload（via service account JWT） |
| **GitHub Actions** | CI/CD 流水线（via GitHub OIDC token） |
| **Kubernetes** | K8s 集群内 pod（via projected service account token） |
| **SPIFFE** | 跨云、跨平台的工作负载身份（via SPIRE 颁发的 SVID） |
| **Microsoft Entra ID** | Azure 生态 |
| **Okta** | 通用企业 IdP |

这些 IdP 的共同特征：**它们都遵循 OIDC（OpenID Connect）协议**，能颁发标准 JWT。Anthropic 不需要为每个 IdP 写适配代码，只需要验证 JWT 签名 + 校验声明即可。

### 2.3 Federation Rule：把三者串起来的桥梁

**Federation rule（联邦规则）才是 WIF 真正有"魔法"的地方**。它的格式是 `fdrl_...`，是一段声明式配置：

> "当来自 issuer X 的 JWT，声明（claims）匹配 Y，就为 service account Z 换发 scope 为 S 的 access token。"

官方文档原话：

> A **federation rule** (`fdrl_...`) is the bridge between an issuer and a service account: "when a JWT from issuer X has claims that look like Y, mint a token for service account Z with scope S."

举一个 AWS 场景的具体例子。假设你在 Lambda 里跑 inference worker，IAM role ARN 是 `arn:aws:iam::123456789012:role/inference-worker`，那对应的 federation rule 配置大致长这样：

```json
{
  "issuer": "aws-iam",
  "subject_prefix": "arn:aws:iam::123456789012:role/inference-worker",
  "audience": "https://api.anthropic.com",
  "service_account": "inference-worker-prod",
  "scopes": ["messages.write", "models.read"]
}
```

`subject_prefix` 用了**前缀匹配**，意味着如果你把前缀放宽到 `arn:aws:iam::123456789012:role/*`，那么所有匹配这个前缀的 IAM role 都会映射到同一个 Anthropic service account。**这是"最小权限"与"运维便利"之间的可调节旋钮**——匹配越窄越安全，匹配越宽越省事。

## 三、协议层细节：换 token 的真实流程

WIF 的换 token 流程可以简化为 4 步：

```
┌──────────┐  ① 拿 OIDC token    ┌────────────┐
│ Workload ├─────────────────────▶│  IdP       │
│(Lambda等)│                      │(AWS/GCP/  │
└──────────┘  ◀──────────────────┤ GitHub等)  │
   │        ② 短期 JWT           └────────────┘
   │  ③ 拿 JWT 换 access token
   ▼
┌──────────────────────────────────────┐
│ Claude Platform                       │
│ 1) 验 JWT 签名 → 检查 issuer 是否在信任列表
│ 2) 检查声明 → 找匹配的 federation rule
│ 3) 检查 federation rule 的 workspace 是否匹配 service account 的 memberships
│ 4) 换发 access token（短生命周期，绑定到 service account）
│ 5) 写入 audit log：service_account_id + federation_rule_id + IdP claims 摘要
└──────────────────────────────────────┘
   │
   ▼
④ 用 access token 调 Claude API
```

几个微妙但重要的设计点：

### 3.1 Workspace 双重检查

Anthropic 不只检查 federation rule 里的 service account，还会**再次确认**这个 service account 是否真的有那个 workspace 的 membership。这条"双重检查"避免了"我用 prod rule 调 dev workspace 的 API"这种越权——service account 的 workspace membership 是独立的元数据，跟 federation rule 没有强制绑定。

### 3.2 Token 的"短"到底有多短

WIF 换发的 Anthropic access token 是**短生命周期**的（具体时长由 IdP 颁发的 JWT 有效期决定，通常是 15 分钟到 1 小时）。这意味着：

- 即使 token 泄露，攻击窗口被压到了分钟级
- 不需要像传统 API key 那样做 90 天轮换的运维噩梦
- 任何一个 workload 想持续调用 API，就必须每次重新走 federation 流程——**每一次调用都在审计**

### 3.3 Service Account 的"替代静态 key"语义

官方文档明确说：

> API keys work alongside WIF, so you can migrate one workload at a time.

也就是说 WIF **不是**强制替换 API key，而是**并存**——你可以一个 workload 一个 workload 地迁移。这是降低迁移成本的渐进式设计。但一旦所有 workload 都迁完，**静态 `sk-ant-...` 在你的环境里就应该彻底消失**。

## 四、与 R454 enterprise-managed-auth 的边界

读到这里，你可能会问：这跟之前 R454 覆盖的 enterprise-managed-auth（MCP 连接器授权）有什么区别？

| 维度 | R454 enterprise-managed-auth | R634 WIF |
|------|----------------------------|----------|
| **身份主体** | MCP connector（连接器） | Workload（计算单元） |
| **认证方式** | IdP 集中授权 | OIDC token 联邦 |
| **解决什么** | 用户/组能接入哪些 MCP connector | Workload 怎么证明自己是合法的 |
| **粒度** | 连接器级别 | Service account 级别 |
| **静态 vs 短期** | 通常配合短期凭据 | 强制短期 OIDC token |

简单说：
- **enterprise-managed-auth 解决的是"我能用什么连接器"**——是 user-side 的访问控制
- **WIF 解决的是"我的 workload 怎么证明自己是我的"**——是 workload-side 的身份认证

两者**互补不重叠**：enterprise-managed-auth 管理用户授权、MCP 连接器权限；WIF 管理 workload 身份、API 调用认证。一个组织要真正落地 enterprise Claude adoption，**两个机制都要用**。

## 五、多云适配矩阵：WIF 在 7 种 IdP 下的具体落地

WIF 的协议设计是"OIDC 抽象层"，但落地到每个 IdP 都有微妙差异。下面这张表是基于 platform.claude.com/docs/en/manage-claude/wif-providers 系列文档的官方推荐路径：

| IdP | 推荐认证方式 | 配置复杂度 | 适合场景 |
|------|--------------|------------|----------|
| **AWS IAM** | STS `GetWebIdentityToken` | 中（需要 IAM role + trust policy） | Lambda/EC2/ECS/EKS 全覆盖 |
| **Google Cloud** | GCP service account JWT | 低（GCP 原生） | Cloud Run/Cloud Functions/GKE |
| **GitHub Actions** | `permissions: id-token: write` | 极低（YAML 一行） | CI/CD 流水线 |
| **Kubernetes** | projected service account token | 中（需要 OIDC issuer 配置） | 集群内 pod |
| **SPIFFE/SPIRE** | SVID JWT | 高（需要 SPIRE 部署） | 跨云、零信任网络 |
| **Microsoft Entra ID** | federated identity credential | 中（Azure Portal 配置） | Azure 生态 |
| **Okta** | OIDC app + custom claim | 中（需要 Okta admin） | 企业通用 IdP |

**官方推荐路径的细节值得注意**：AWS 上有两种选择——STS `GetWebIdentityToken`（任何有 AWS credentials 的地方都能用）或 Kubernetes projected-token（只在 pod 内可用）。**官方明确推荐前者**，因为它适用范围更广。

## 六、WIF 与 Zero Trust 框架的关系

R314/R320 我们覆盖过 Anthropic 的 **Zero Trust for AI Agents 三 Tier 框架**：

- Tier 1：人 + Agent 的身份（identity）
- Tier 2：访问控制（authorization）
- Tier 3：审计与可观测性（audit）

WIF 在这个框架里**同时承担 Tier 1 和 Tier 3**：

- **Tier 1（身份）**：WIF 用 OIDC token 替代静态 API key，本质是把"信任密码"升级为"信任 IdP 的 token 验证结果"
- **Tier 3（审计）**：WIF 的 audit log 包含 service_account_id + federation_rule_id + IdP issuer + claims 摘要——审计粒度比 API key 细一个数量级

但 WIF **没有直接解决 Tier 2（访问控制）**——那是 enterprise-managed-auth（R454）或更上层的 IAM 策略要做的事。

## 七、5 条给工程团队的行动建议

基于 WIF 的协议设计和落地路径，我给到 5 条可执行建议：

### 建议 1：把"消灭静态 API key"写进 OKR

如果你的团队还在用 `sk-ant-...` 长生命周期 key 做 CI/CD、K8s pod、Lambda 调用，**这就是技术债**。把"所有 production workload 都用 WIF"作为本季度 OKR，目标值是 `sk-ant-...` 出现在生产环境配置里的次数 = 0。

### 建议 2：从 GitHub Actions 开始迁移

GitHub Actions 的 WIF 集成**最简单**——只需要在 workflow 里加一行 `permissions: id-token: write`，再配一条 federation rule 就行。这是迁移的"低垂果实"，先做这个能积累 federation rule 配置经验。

### 建议 3：Federation Rule 的 `subject_prefix` 不要过宽

官方文档明确警告：`subject_prefix` 越宽，blast radius 越大。最佳实践是**精确匹配单个 IAM role ARN** 或**只覆盖必要的 service account 子集**。`arn:aws:iam::*:*` 这种通配是反模式。

### 建议 4：Service Account 与 workload 一一对应

不要让一个 service account 被 50 个 Lambda 共享——这等于把静态 key 的问题换了个形式。**Service account 应该是"workload 的身份"，不是"项目的身份"**。每个生产 workload 一个 service account，审计才有意义。

### 建议 5：把 WIF 当作"零信任工作负载"的基础设施

WIF 不只是 Claude 平台的特性，它是**零信任架构在 AI 工作负载上的具体落地**。如果你的组织已经在用 SPIFFE 做内部 workload 身份，WIF 是天然的延伸——你的 SPIRE 颁发的 SVID 可以直接被 Claude Platform 验证，不需要额外的中间层。

## 八、金句

> **"API key 不是密钥，是组织级的技术债。"** — 在静态 `sk-ant-...` 还在生产配置里出现的每一天，你的 blast radius 都是"持 key 的所有人"。WIF 把这件事从"密码学问题"变成了"身份联邦问题"。

> **"Federation rule 才是 WIF 的灵魂。"** — Service account 是身份，issuer 是信任源，但只有 federation rule 把"哪个 issuer 的哪个声明 → 哪个 service account → 哪个 scope"这条链子完整定义下来。**配置错一条规则，等于开了一扇后门**。

> **"WIF 解决了'workload 怎么证明自己是我的'，没解决'workload 能做什么'。"** — 这是和 enterprise-managed-auth（R454）的清晰边界。前者是身份认证，后者是访问控制。一个组织要落地企业级 Claude，必须两个都做。

## 九、引用与一手源

### 主源
- **Anthropic Claude Blog - WIF GA Announcement**: https://claude.com/blog/workload-identity-federation
- **Author**: Anthropic Claude Platform team

### 协议层文档
- **Workload Identity Federation（核心协议）**: https://platform.claude.com/docs/en/manage-claude/workload-identity-federation
- **Authentication Overview**: https://platform.claude.com/docs/en/manage-claude/authentication
- **Create Service Account API**: https://platform.claude.com/docs/en/api/admin/service_accounts/create
- **WIF with AWS**: https://platform.claude.com/docs/en/manage-claude/wif-providers/aws

### 关联覆盖文章
- R454 enterprise-managed-auth (MCP 连接器授权): `articles/tool-use/anthropic-enterprise-mcp-authorization-idp-governance-2026.md`
- R314/R320 Zero Trust for AI Agents 三 Tier: `articles/harness/anthropic-zero-trust-ai-agents-three-tier-framework-2026.md` + `articles/harness/claude-zero-trust-ai-agents-three-tier-maturity-2026.md`
- R327 Security Program for AI-Accelerated Offense: `articles/ai-coding/anthropic-security-program-ai-accelerated-offense-engineering-2026.md`
- R315 Self-hosted Sandboxes & MCP Tunnels: `articles/harness/anthropic-claude-managed-agents-self-hosted-sandboxes-mcp-tunnels-2026.md`

## 十、开放问题

WIF 解决了 workload-side 的身份认证，但有一个**没明确回答**的问题：**当一个 workload 通过 WIF 拿到 access token 后，这个 token 能不能传给另一个 workload？** 换句话说，token 转发（token relay / delegation）是否被允许？

如果不允许，那么一个需要多个内部服务协作的 agent pipeline 怎么跨服务传递身份？如果允许，那是不是又引入了类似"token 泄露"的攻击面？

这个问题的答案，藏在 federation rule 的 `scopes` 字段里——但 Anthropic 目前没有在公开文档里给出明确的"是否允许 delegation"的设计原则。**这是我留给读者思考的问题**。