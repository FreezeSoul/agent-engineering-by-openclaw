---
title: "Claude Tag 的 Agent Proxy 架构：凭证从不进沙盒，零信任在 AI Agent 生产环境的首次落地"
date: 2026-06-28
tags: [Anthropic, Claude, Claude Tag, Zero-Trust, Agent Proxy, Credential Injection, Security, Harness]
description: Anthropic 在 Claude Tag 中实现了一个具体的 Agent 零信任架构：凭证存在沙盒外部的 Credential Store，Agent Proxy 按规则注入，请求无匹配规则则被拒绝——这是 AI Agent 安全模型第一次有生产级参考实现。
---

# Claude Tag 的 Agent Proxy 架构：凭证从不进沙盒，零信任在 AI Agent 生产环境的首次落地

> 官方文档：[How agent identity works](https://claude.com/docs/claude-tag/concepts/agent-identity)  
> 发布时间：2026 年 6 月 23 日（与 Claude Tag 同步）| 类型：工程机制 / 零信任架构

## 核心命题

**Claude Tag 的安全架构回答了一个长期悬而未决的问题：AI Agent 在生产环境中应该如何获得外部系统（GitHub、数据库、监控）的访问凭证？**

Anthropic 给出的答案是：**凭证永远不进入 Agent 的执行沙盒**。所有外部请求必须经过 Agent Proxy，由 Proxy 按管理员配置的规则注入凭证，无匹配规则的请求直接被拒绝。

这个设计不是概念，而是 Claude Tag 生产环境的一部分。这是 AI Agent 领域第一次有科技大厂把云原生时代的零信任安全模型（永不信任，始终验证）完整落地到 Agent 运行时。

---

## 一、问题：传统 Agent 的凭证困境

### 1.1 当前主流做法及其风险

今天大多数 AI Agent 访问外部系统时，凭证的处置方式本质上是这样的：

1. **硬编码**：API key 直接写在 Agent 配置或 Prompt 里
2. **环境变量渗透**：Agent 运行时能看到完整的环境变量列表，里面可能包含所有凭证
3. **服务账号继承**：Agent 以「部署它的用户」的权限访问一切，不做最小权限隔离
4. **无审计路径**：Agent 对外部系统的调用无法追溯是哪个 Agent 实例发出的

这意味着：当 Agent 被攻破或 Prompt 泄漏时，攻击者拿到的是整个系统的钥匙。

### 1.2 为什么 Channel 场景更危险

Claude Tag 的核心创新是「一个 Channel 一个 Claude 实例」，这让问题变得更尖锐。

传统 ChatGPT 单用户场景：Agent 的上下文是私有的，凭证可以用用户个人的 OAuth token。

Claude Tag 的 multiplayer 场景：一个 Channel 里有 5 个工程师 + 1 个 PM，所有人共用一个 Claude。这个 Claude 的外部访问权限应该多大？

- 5 个工程师都在 #eng channel，Claude 应该能访问 GitHub 和 CI
- #sales channel 的 Claude 不能看到任何 engineering 数据
- 财务 channel 的 Claude 只能访问 CRM

如果凭证跟着 Claude 实例走，那就需要一个**能区分「哪个 Channel 的 Claude」**的动态凭证注入机制。

---

## 二、Claude Tag 的三区架构

Claude Tag 的技术文档里有一张请求路径图，描述了一次 Channel 任务触发的完整请求生命周期：

```
Slack Workspace (Task in channel)
        ↓
Session Sandbox (Anthropic infrastructure)
        ↓  (outbound request)
Agent Proxy (network boundary)
        ↓  (credential injection)
Credential Store (admin-provisioned service accounts)
        ↓
External Systems (GitHub, Data Warehouse, Monitoring, HTTP APIs)
```

### 2.1 Zone 1: Slack Workspace（触发区）

用户或定时任务在 Slack Channel 里 `@Claude` 一个请求。这个请求启动了 Channel 对应的一个新 Session Sandbox。

**关键约束**：一个 Channel 同一时间可以有一个或多个 Session 在运行，但每个 Session 都是独立的隔离环境。

### 2.2 Zone 2: Session Sandbox（执行区）

这是 Claude 的「工作间」——运行在 Anthropic 基础设施上的隔离环境，Claude 在这里读取文件、写代码、运行命令。

**最关键的设计决策**：

> *"The credentials you provision are not placed in the sandbox; they stay in the credential store and are injected at the proxy."*

**凭证不在沙盒里**。这与传统架构完全不同——传统架构下 Agent 进程拥有所有凭证，而 Claude Tag 的沙盒里只有代码执行能力，没有凭证。

### 2.3 Zone 3: Agent Proxy + Credential Store（安全边界）

当沙盒需要访问外部系统（GitHub API、数据库等）时，请求先到 **Agent Proxy**。Agent Proxy 做三件事：

1. **规则匹配**：检查请求是否匹配管理员配置的访问规则
2. **凭证注入**：如果匹配，从 Credential Store 获取对应的服务账号凭证，注入请求
3. **阻止未授权请求**：没有匹配规则的请求直接拒绝，不传递任何凭证

> *"A request matching no rule is blocked."*

---

## 三、Credential Store：服务账号而非用户凭证

### 3.1 凭证按工具组织

管理员在配置 Claude Tag 时，需要为每个外部系统创建一个独立的服务账号：

- **GitHub**：Claude GitHub App（不是任何个人的 GitHub 账号）
- **数据仓库**：独立的服务账号，有最小必要的数据库权限
- **监控**：只读 API token，无法写操作

> *"An organization Owner provisions this identity during setup, so it arrives with its own account in each system it works in: the Claude app in Slack, the Claude GitHub App on GitHub, and a service account in every other connected tool."*

### 3.2 为什么不用用户 OAuth Token

传统 SaaS 集成用 OAuth 让用户登录，拿用户的 Token。这意味着 Token 继承了用户的全部权限——而用户通常有远超最小必要的权限。

Claude Tag 的服务账号方案：Claude 访问 GitHub 时，用的是「Claude GitHub App」，这个 App 的权限由管理员精确控制，可能是「只能读 `org/repo` 下的代码，无法写其他仓库」。

笔者认为，这个分离是 Claude Tag 安全架构里最重要的一刀：**「Agent 的身份」和「任何人类的身份」完全解耦**。这是企业级 Agent 访问控制的正确起点。

### 3.3 DM 场景的特殊处理

文档里有一个值得注意的例外：

> *"In direct messages (DMs) between a user and @Claude, the provisioned identity does not apply. DMs run on the individual's own account instead."*

DM 场景下 Claude 以用户身份行动（OAuth token 继承用户权限）。这是合理的——DM 本质上是「用户让 Claude 替自己办事」，不是 Channel 场景下的团队协作。

但这也意味着：**DM 是 Claude Tag 安全模型的盲区**。企业如果想确保完整的 Agent 访问控制，应该限制 DM 或对 DM 做额外审计。

---

## 四、Channel-scoped Identity：身份与 Channel 绑定

### 4.1 每个 Channel 都是独立的权限边界

Claude Tag 的 Channel-scoped identity 是这个安全模型的第二层：

- `#eng` channel 的 Claude 拥有 Engineering 工具集的凭证
- `#sales` channel 的 Claude 拥有 CRM 和数据分析工具的凭证
- 两个 Claude 实例在外部系统看来是不同的服务账号，**彼此之间无法跨 Channel 访问**

> *"A model set up for sales work won't pass on memories to one set up for engineering; nor will it give engineers access to any sales data or tools."*

### 4.2 为什么 Channel 而不是 User 是权限边界

这个设计选择反映了一个根本性的认知转变：

| 维度 | 传统（User 为边界） | Claude Tag（Channel 为边界） |
|------|-------------------|--------------------------|
| 上下文共享 | 不可共享，每个用户独立 | Channel 内完全共享 |
| 权限控制 | 用户拥有什么权限，Agent 就有 | Channel 允许什么工具，Claude 才能用 |
| 凭证归属 | 借用人的 OAuth token | Agent 自有服务账号 |
| 审计追溯 | 「User X 做了某操作」| 「Channel Y 的 Claude 实例做了某操作」|
| 数据泄漏风险 | 用户有意或无意分享给其他人 | Channel 是天然的访问控制边界 |

Channel 作为边界的本质是：**团队是 Agent 访问控制的正确粒度**。Claude Tag 押注的是 2026 年的企业 AI 落地，核心场景是多团队协作，而不仅仅是个人效率工具。

---

## 五、工程意义：为什么这不只是 Claude Tag 的事

### 5.1 AI Gateway 的参考实现

今天任何企业在部署多 Agent 系统时，都会遇到一个共性挑战：**AI Gateway（AI 网关）如何路由不同 Agent 的外部访问请求？**

Claude Tag 的 Agent Proxy 模式给出了一个具体的参考：

```
Agent → [规则匹配] → [凭证注入] → 外部系统
         ↑
    管理员配置规则
```

这个模式可以抽象为一个 AI Gateway 的标准架构：所有 Agent 的外部调用都经过同一个 Proxy，Proxy 维护「Agent Identity → 允许的外部系统 → 所需凭证」的三元映射。

笔者认为，未来会有越来越多的企业从「每个 Agent 自己管凭证」迁移到「统一的 Agent Proxy 网关」，Claude Tag 是这个趋势的第一个生产级参考。

### 5.2 与 Claude Code 2.1.187 的协同

同一天（2026 年 6 月 23 日）Anthropic 还发布了 Claude Code 2.1.187，其中包含了一个类似的安全特性：

> *"The sandbox.credentials setting in Claude Code 2.1.187 applies a similar pattern at the file-system level: the agent sees only the credentials it needs for its current task scope."*

两个产品同一天发布，说明这是 Anthropic 的统一安全策略：**在 Code 级别和 Tag 级别同时推进最小权限凭证模型**，而不是在某个单一产品里做实验。

### 5.3 8 月 3 日迁移窗口

Anthropic 宣布现有的「Claude in Slack」集成将在 **2026 年 8 月 3 日** 迁移到 Claude Tag。这意味着：

1. 正在使用旧集成的企业需要重新配置工具访问策略
2. 如果旧集成用了个人 OAuth Token，迁移后需要改用服务账号
3. 这是企业审视「Agent 访问控制现状」的一个硬截止日期

---

## 六、架构亮点与已知局限

### 亮点

1. **凭证从不进沙盒**：这是零信任架构的核心——永不信任执行环境，始终在边界验证
2. **服务账号而非用户凭证**：Agent Identity 与 Human Identity 完全解耦
3. **Channel 作为权限边界**：团队粒度的访问控制，天然符合企业协作结构
4. **生产级参考实现**：不是白皮书，是真实产品的真实架构，有具体参数和行为

### 局限

1. **DM 盲区**：DM 场景下回归传统用户凭证模型，审计能力弱化
2. **迁移成本**：8 月 3 日前需要企业重新配置所有 Slack 集成的访问策略
3. **目前仅限 Slack**：其他协作工具（Teams、飞书、Discord）的扩展需要等
4. **Proxy 单点**：Agent Proxy 是所有外部请求的必经节点，如果 Proxy 本身被攻破，攻击者可以控制所有凭证注入

---

## 七、一句话总结

Claude Tag 的 Agent Proxy 架构把「零信任」从云安全概念变成了 AI Agent 运行时的事实标准：**凭证存在沙盒外面，外部请求必须经过 Proxy 按规则注入，无匹配则拒绝**。这对所有正在构建企业级 Agent 系统的团队，是一个可以直接参考的生产级架构。

> **金句**：凭证是 Agent 安全的最短木板。Claude Tag 的答案是——让最短的木板根本不进 Agent 的屋子。