# LangChain Deep Agents Deploy：开源部署方案与 Claude Managed Agents 的架构分叉

> **核心问题**：当 Anthropic 用 Claude Managed Agents 巩固其专有云托管生态时，LangChain 在次日发布 Deep Agents Deploy，以开源、自托管、模型无关的姿态直接叫板。两者的竞争本质不是功能之争，而是**Agent 基础设施控制权**的路线之争。
>
> **读完能得到什么**：理解 Deep Agents Deploy 的核心架构决策、与 Claude Managed Agents 的根本差异、以及"模型无关 + 数据自主"这条开源路径的工程可行性。

---

## 一、背景：Claude Managed Agents 确立了什么

2026 年 4 月 8 日，Anthropic 向公众开放 Claude Managed Agents beta。这是 Agent 基础设施领域的一个里程碑，因为它在生产级别验证了 Brain/Hands/Session 三组件架构的工程可行性——但这一切建立在 Anthropic 自有基础设施之上。

Anthropic 的核心主张：
- **安全隔离**：Hands（代码执行）在独立沙盒中运行，凭据不与 LLM 同进程
- **Session 持久化**：外部化上下文存储，支持中断恢复和长时间任务
- **全托管**：开发者无需关心底层基础设施

这是工程上的正确答案之一，但它是**有代价的**——Agent 的记忆（Memory）、Agent 的执行上下文、Agent 的工具生态，全部绑定在 Anthropic 的专有系统中。

---

## 二、Deep Agents Deploy 的架构响应

2026 年 4 月 9 日，LangChain 发布 Deep Agents Deploy beta。距离 Claude Managed Agents 向公众开放不足 24 小时，时机本身就是宣战。

Deep Agents Deploy 的核心定位：**把 Claude Managed Agents 的架构思路搬进开源、自托管、模型无关的世界里。**

### 2.1 核心架构组件

Deep Agents Deploy 构建在 Deep Agents 之上——一个开源的、模型无关的 Agent Harness 框架。它的部署架构包含以下核心组件：

```
Deep Agents Deploy = Deep Agents（Harness）+ LangSmith Deployment Server + Sandbox + Memory Endpoints
```

**Harness 层（Deep Agents）**
Deep Agents 是 LangChain 的开源 Agent Harness，提取自 Claude Code 的核心设计思路，但使其模型无关。支持任何支持 Tool Calling 的 LLM：Anthropic、OpenAI、Google Gemini、Llama、Mistral，以及 LangChain Model Providers 生态中的数百个模型。

核心设计：
- **长期规划**：Agent 在更长的时间跨度上做规划，而非短程反应
- **上下文管理**：自动上下文摘要，维持长程任务的上下文连贯性
- **文件系统共享工作区**：用虚拟文件系统作为子 Agent 之间的共享存储，避免上下文膨胀
- **子 Agent 委托**：复杂任务分解给专门的子 Agent 处理

**Sandbox 层**
代码执行可以在指定的 Sandbox 提供商中运行。Deep Agents Deploy 的设计允许任何 Sandbox 实现接入——不锁定在某一家的隔离方案中。这与 Claude Managed Agents 的专有沙盒形成对比。

**Memory Endpoints**
这是最关键的架构差异之一。Deep Agents Deploy 提供：
- 短时记忆端点（Short-term Memory）
- 长时记忆端点（Long-term Memory）

Agent 的记忆以标准格式存储（AGENTS.md、Skills 文件等），可以通过 API 直接查询。如果团队自托管，记忆数据**始终保存在自己的数据库中**，而不是第三方平台。

**LangSmith Deployment Server**
每个 Deep Agents Deploy 实例捆绑一个 LangSmith Deployment 服务器，负责追踪（Tracing）和可观测性。

### 2.2 开放标准策略：AGENTS.md + Agent Skills

Deep Agents Deploy 押注的两个开放标准：

| 标准 | 定位 | 作用 |
|------|------|------|
| **AGENTS.md** | Agent 指令规范 | 用 Markdown 定义 Agent 的角色、能力边界、行为规范——让 Agent 的"脑子"变成可移植的文件 |
| **Agent Skills** | 能力抽象单元 | 通过 Skill Registry 体系（agentskills.io）管理专业化知识，支持动态注入和版本控制 |

这是架构上的一着好棋：如果 Agent 的记忆和指令都是标准化的开放格式，那么"换供应商"的成本就从"重写整个 Agent 系统"降到"迁移一堆 Markdown 文件"。这直接挑战了 Claude Managed Agents 的锁定效应。

---

## 三、两条路线的核心分歧

把 Claude Managed Agents 和 Deep Agents Deploy 放在一起对比，能看出基础设施控制权的两条截然不同的路线：

| 维度 | Claude Managed Agents | Deep Agents Deploy |
|------|----------------------|-------------------|
| **基础设施** | Anthropic 自有云 | 自托管（任意云或本地） |
| **模型选择** | 绑定 Anthropic 模型 | 任意支持 Tool Calling 的模型 |
| **记忆存储** | Anthropic 平台管理 | 自有数据库，完全自主 |
| **沙盒方案** | 专有安全隔离 | 开放接口，任何实现可接入 |
| **工具生态** | 平台绑定 | 开放生态 |
| **锁定程度** | 高（端到端自有） | 低（开放标准，可迁移） |
| **运维负担** | 低（托管服务） | 高（自建基础设施） |

这不是"谁更好"的问题，而是"你在为什么买单"的问题：

- **Claude Managed Agents** 卖的是：**免运维 + 安全性已验证**。你把控制权交给 Anthropic，换来的是不需要自己搭沙盒、不需要自己管 Session 持久化、不需要自己处理多区域部署。
- **Deep Agents Deploy** 卖的是：**控制权 + 可移植性**。你有全部数据，有全部配置权，但代价是基础设施需要自己维护。

---

## 四、工程可行性分析

### 4.1 谁应该用 Deep Agents Deploy

**适合的场景**：
- 数据主权要求严格（如金融、医疗、政府）——数据不能出境的场景，自托管是硬性要求
- 需要在私有模型或微调模型上跑 Agent——Claude 和 GPT 未必是每个场景的最优解
- 已有基础设施团队——能够维护自己的沙盒、网络配置和监控体系
- 需要深度定制 Harness——Deep Agents 提供了完整的底层接口，可以改到骨子里

**不适合的场景**：
- 追求快速上线、不想运维基础设施的团队——这部分 Claude Managed Agents 更省心
- 安全团队资源不足、无法自己验证沙盒隔离有效性的组织——自托管沙盒的安全性需要自己保证

### 4.2 Sandbox 的安全性挑战

这是 Deep Agents Deploy 路线最大的工程风险。Claude Managed Agents 的专有沙盒经过了生产验证，有专门的团队处理隔离、漏洞和边界情况。自托管的 Sandbox 实现需要：

- 持续的隔离层维护（容器级别、网络级别）
- 对抗 Prompt Injection 的额外防护层
- 自己处理 Agent 逃逸风险

这对于没有专业安全团队的团队来说是高成本。LangChain 提供了 Sandbox 实现指南，但最终的安全责任落在使用者身上。

### 4.3 模型无关的代价

Deep Agents Deploy 宣称支持"数百个模型"，但模型无关不是没有代价的：

- **Harness 与模型的适配**：不同模型的 Tool Calling 格式、Token 预算、能力边界差异巨大。同一套 Harness 在 Claude Opus 4 上跑得好，在 Llama-3 上可能完全不行。LangChain 自己的 Better Harness 文章就提到了这种差异（GLM-5 和 Claude Sonnet 4.6 在同样 Harness 上的表现存在差异）。
- **开放生态的质量参差**：接入数量多不代表质量高。大量第三方模型提供商的 Tool Calling 实现存在各种边界情况。

---

## 五、竞争格局的工程含义

Claude Managed Agents vs Deep Agents Deploy 的竞争，本质上在回答一个问题：**Agent 基础设施应该走 iOS 路线（封闭但高体验）还是 Android 路线（开放但碎片化）？**

Claude Managed Agents 代表了前者：端到端自有，用户体验一致，安全性可验证，但代价是锁定。

Deep Agents Deploy 代表了后者：标准开放，数据自主，但要求使用者有足够的工程能力来保证安全和质量。

两种路线都有市场。决定因素是：
- **团队的安全合规要求**：数据是否能出境
- **团队的技术深度**：有没有能力维护自己的基础设施
- **供应商风险偏好**：是否愿意依赖单一供应商

---

## 六、核心 insight

1. **基础设施控制权成为新的竞争维度**：当模型能力趋于同质化，Agent 基础设施的归属和控制权开始成为核心差异化点。Anthropic 和 LangChain 的这次同周发布不是巧合，是两边都在抢占这个位置。

2. **开放标准是降低迁移成本的唯一路径**：AGENTS.md 和 Agent Skills 的价值不在于它们本身有多好，而在于它们让"换 Agent 平台"的成本从重写系统变成迁移文件。如果这两个标准被广泛采纳，平台锁定效应将被显著削弱。

3. **自托管的工程成本不可忽视**：Deep Agents Deploy 给了团队自由，但也给了团队责任。沙盒安全、基础设施可用性、运维成本——这些都是真实的工程投入。选这条路需要清醒的成本核算。

4. **两个路线并行存在是健康的**：市场不需要只有一个答案。iOS 和 Android 共存了十几年，Claude Managed Agents 和 Deep Agents Deploy 的竞争最终会让整个 Agent 基础设施生态更成熟。

---

> **相关阅读**：
> - [Anthropic Managed Agents：Brain/Hands/Session 架构解析](../deep-dives/anthropic-managed-agents-brain-hands-session-2026.md) — Claude Managed Agents 的内部架构
> - [Better Harness：Eval-Driven Agent 迭代优化](../frameworks/better-harness-eval-driven-agent-iterative-optimization-2026.md) — LangChain 的 Harness 迭代方法论
