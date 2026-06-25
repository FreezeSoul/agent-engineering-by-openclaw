---
title: "Claude Tag Agent Identity：多玩家 Agent 的访问控制新范式"
date: 2026-06-26
tags: [Anthropic, Claude, Claude Tag, Agent, Identity, Access-Control, Multi-Agent, Zero-Trust, Security]
description: Claude Tag 的 Agent Identity 访问模型把权限问题从「这个用户能做什么」换成「这个 Agent 在这个 channel 能做什么」——admin 定义 agent 自己的 identity，channel 继承并覆盖，跨系统凭证隔离、audit 集中、just-in-time 凭证是 next。
---

# Claude Tag Agent Identity：多玩家 Agent 的访问控制新范式

> **官方博客**：[Agent identity in Claude Tag: a new access model for autonomous, team-wide AI](https://claude.com/blog/agent-identity-access-model)
> 发布时间：2026 年 6 月 24 日 | 类型：Claude Code / Access Model Architecture
> 作者：Noah Zweben（Claude Code team technical staff）

## 核心命题

**Anthropic 把 Agent 访问控制的语义从「这个用户能做什么」彻底替换为「这个 Agent 在这个 channel 里能做什么」。Claude Tag 的 Agent Identity 模型让 Agent 拥有自己的服务账号（不是借用人类凭证），admin 在 workspace 级别定义 baseline identity，每个 channel 在此基础上 override。Channel 是访问控制的最小单元，不是用户。**

这是 2026 年最深刻的安全范式转移之一：multiplayer AI 让「权限归属于人」的传统 ACL 失效，「权限归属于 Agent + 上下文边界」成为新基线。

---

## 一、为什么 multiplayer Agent 必须重新设计访问控制

### 1.1 Single-player 的 ACL 假设失效

过去所有访问控制（OAuth scopes、RBAC、ACL）都假设**操作者是某个具体的人**：

- 一个 session 对应一个人
- 凭证归属于这个人的身份
- 审计日志能追溯到这个人

但在 Claude Tag 的 multiplayer 场景里，**一个 channel 里同时有 5 个工程师 + 1 个 PM 在 @Claude**：

> *"In a channel where three engineers and a PM are debugging together. But when more than one person is steering, whose permissions apply? There's no single choice of person that'd be right all of the time."*

「用谁的权限」没有唯一答案——Alice 发起、Bob 接管、Carol 接力、PM 提需求，**任何时刻的「当前用户」都是不确定的**。

### 1.2 共享 channel 不能成为私人凭证的侧门

如果让 Agent 借用某个人的 OAuth token，会有两类灾难：

1. **凭证泄漏面扩大**：Alice 把 channel 加给外部承包商，承包商 @Claude 时 Claude 用的还是 Alice 的全权限 token，承包商实际拿到 Alice 的访问权限
2. **审计归属错乱**：Claude 写的 PR / 跑的 query / 发的消息到底算谁的？Alice 离职后她的 token 撤销，但 Claude 在 channel 里残留的所有 action 全失效

Claude Tag 的解决方案是 **Claude 永远以「自己」的身份行动，不借任何人的凭证**。

---

## 二、Agent Identity 的 4 大设计原语

### 2.1 Claude Acts as Itself（Claude 拥有自己的账号）

> *"In a channel where Claude Tag is active, Claude isn't acting on behalf of a single user. It has its own account in each system it touches: it posts in Slack as the Claude app, opens pull requests as the Claude GitHub App, and queries your warehouse under a service account provisioned by an admin."*

每个系统，Claude 都有**专属账号**：

| 系统 | Claude 的身份 |
|---|---|
| Slack | Claude app（不是某个人发的消息） |
| GitHub | Claude GitHub App（不是某人的 PAT） |
| 数据仓库 | admin 预置的 service account |
| Google Drive | Claude workspace service account |
| 内部工具 | admin 预置的 service principal |

**没有「Alice 的 OAuth token」在流通**。所有操作归属都是「Claude + 它的 channel identity」。

### 2.2 Workspace → Channel 两级继承（Inheriting Permissions）

> *"Admins define an identity—the baseline set of connections and skills Claude holds everywhere—at the workspace level, and every channel inherits it by default. Then, where it makes sense, they can override it at the channel level."*

**两级配置结构**：

```
workspace
  └─ baseline identity (admin 定义)
      ├─ engineering channel → + GitHub + warehouse (override)
      ├─ legal channel → + Westlaw + Contracts repo (override)
      ├─ data-team channel → + write access to warehouse (override)
      └─ general channel → 只读 baseline
```

每个 channel 的 profile 包含 4 类配置：

1. **Repository access**：可读/写哪些 repo
2. **Connectors + API keys**：不同 service 在不同 channel 可用不同权限级别（如 general channel 只读 / data-team channel 读写）
3. **Skills + plugins**：动态加载的指令/脚本/资源
4. **Standing instructions**：每个 channel 的定制上下文

**撤销一个 identity = 撤销所有 channel 里 Claude 的访问**。比逐个 user 撤销简单一个数量级。

### 2.3 Identity Boundaries（边界隔离）

> *"Claude Tag creates a distinct identity for each private channel; public channels in a workspace share a workspace-level identity. Claude's identity in a legal channel can't reach code that wasn't granted there."*

**隔离规则**：

- 私有 channel = 独立 identity
- 公开 channel = 共享 workspace identity
- legal channel 的 Claude **不能读** engineering channel 的 code
- engineering channel 的 Claude **不能读** legal channel 的 docs
- memory 也遵守同样隔离：private channel 学到的内容不会泄漏到 workspace

**关键设计**：identity 归属于 channel，**任何 channel 成员都能 @Claude**（不需要各自授权），但 admin 可以用 RBAC 进一步限制谁能 invoke Claude。

### 2.4 跨系统组合价值（Cross-System Composition）

> *"Each connected system makes every other one more useful, because Claude can combine context across them—pulling a thread from Slack, a doc from Drive, a ticket from a tracker, and a query from a warehouse into one answer that no single tool could provide."*

**核心洞察**：Claude 的价值随连接的系统数**复合增长**——能从 Slack 拉 thread + Drive 拉 doc + tracker 拉 ticket + warehouse 拉 query 组合成一个答案。

但**前提是 admin 给了 broad 初始访问**。Anthropic 的实操建议：

> *"Our advice is to start with a baseline profile in a few channels, read the audit trail, and then extend access where the work justifies it, one deliberate grant at a time."*

---

## 三、DMs vs Channels：两种访问模型并存

### 3.1 DMs 走用户账号（个人场景）

> *"Direct messages work differently than in shared channels. DMs run on users' individual claude.ai accounts—their connectors, credentials, and name on the result."*

DMs 保留 single-player 模型：

- 用用户自己的 claude.ai 账号
- 用用户自己的 connectors + credentials
- 结果归属用户名字
- **适合**：邮件草稿、独占授权的软件、个人 license 才能用的工具

### 3.2 Channels 走 Agent identity（团队场景）

Channels 走 Agent identity：

- 用 Claude 自己的服务账号
- 用 admin 预置的 connectors
- 结果归属 Claude app
- **适合**：跨人协作、跨系统集成、长期 thread

**两种模式并存**让用户能在「个人私事」和「团队协作」之间无缝切换，而不用关心权限细节。

---

## 四、安全与审计

### 4.1 凭证隔离存储 + 网络边界注入

> *"When an admin adds a connection to a channel's profile, the credential is stored independently and mapped to that channel's identity, then injected at the network boundary at request time."*

**关键技术点**：

1. 凭证**独立存储**，按 channel identity 索引
2. **请求时**才注入到网络层（不存内存）
3. **未授权的 host 一律 outbound block**

### 4.2 全链路审计

> *"Every routine, memory write, and network call made with agent credentials is recorded, and because Claude acts under its own service accounts, those actions also land in each connected system's own logs."*

**审计双写**：

- Pomerium-style 集中日志（所有 routine/memory/network call）
- 每个连接系统**自身**的 log（因为 Claude 用的是该系统的 service account）

合规 + 调试 = 一次审计完成两个验证。

---

## 五、What's Next：JIT 凭证 + 用户级检查

> *"In the future, we plan to strengthen our Claude Tag's security offerings to include just-in-time credential grants—so that a user can approve a single sensitive action in the moment without permanently widening the agent's scope—and an identity-aware overlay for organizations with more complex clearance structures."*

两个未来方向：

1. **JIT credentials**：用户临时授权一次敏感 action（如「这次 PR 允许 merge 到 main」），不需要永久扩大 scope
2. **Identity-aware overlay**：在 agent scope 之上加用户级权限检查（**只有当 channel profile + 当前用户权限都允许时** Claude 才行动）

这是 **defense-in-depth** 的标准实践：channel 是粗粒度，用户级检查是细粒度。

---

## 六、对其他 Agent 平台的启示

### 6.1 Anthropic 在做「Agent 时代的 RBAC」

传统 RBAC = `User → Role → Permission`
Agent Identity = `Agent Identity → Channel Scope → Skill/Plugin/Connector`

把 Agent 当**一等公民**而非「借用人类身份的工具」，是企业级 AI Agent 部署的硬需求。

### 6.2 与 Octelium / Pomerium 的开源对位

- **[octelium/octelium](https://github.com/octelium/octelium)（3.9K⭐）**：自托管零信任 + MCP 隧道（已有项目收录），解决「MCP server 不暴露公网 + 凭据隔离」的网络层
- **[pomerium/pomerium](https://github.com/pomerium/pomerium)（4.9K⭐）**：身份感知代理，正在做 Agentic Access Gateway，让 AI Agent 也走 zero trust 鉴权（详见本日新增项目）

Claude Tag Agent Identity 补的是**应用层**：channel 是什么、谁能在 channel 里 invoke Claude、Claude 用哪个 service account。

### 6.3 MCP / A2A 协议需要补齐 per-request AuthZ

正如 Pomerium 团队指出的：

> *"The current MCP spec focuses on tool interaction and discovery but leaves per-request authorization largely undefined. Relying solely on initial OAuth scopes ... falls short for dynamic agent workflows."*

MCP 协议需要从「连接期 OAuth scopes」升级到「per-request AuthZ + context-aware policy」。Anthropic 这次的 Agent Identity 模型是这个方向的具体实践。

---

## 七、值得收藏的 4 个 takeaway

1. **Agent 必须有自己的一等身份**，不能借用人类凭证
2. **Channel 是访问控制的最小单元**，不是 user、不是 session、不是 request
3. **Workspace baseline + channel override** 两级配置是企业级复杂度下的唯一可行解
4. **审计双写**（集中 log + 各系统自有 log）是合规 + 调试的最短路径

---

**引用来源**：
- [Agent identity in Claude Tag: a new access model for autonomous, team-wide AI](https://claude.com/blog/agent-identity-access-model)
- [Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag)

**关联阅读**：
- [Anthropic Claude Tag：Slack 原生 Agent 协作者](../fundamentals/anthropic-claude-tag-slack-native-multiplayer-agent-2026.md) — Channel 协作的 harness 层
- [Anthropic zero-trust AI agents three-tier framework](../harness/anthropic-zero-trust-ai-agents-three-tier-framework-2026.md) — 传统 zero trust 框架
- [octelium/octelium：自托管零信任 + MCP 隧道的开源对位](../projects/octelium-octelium-zero-trust-mcp-gateway-self-hosted-ztna-3874-stars-2026.md) — 网络层 zero trust
- [pomerium/pomerium：身份感知 Agent 访问网关（4.9K Stars）](../projects/pomerium-pomerium-identity-aware-agent-access-gateway-4863-stars-2026.md) — 鉴权层 zero trust
