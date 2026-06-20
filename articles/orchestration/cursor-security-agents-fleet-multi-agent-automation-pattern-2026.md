# Cursor 安全 Agent Fleet 架构：多 Agent 自动化实战解析

> **核心观点**：Cursor 的安全 Agent Fleet 不是"多个 Agent 堆在一起"，而是一个精心设计的**事件驱动多 Agent 协作系统**——每个 Agent 有明确职责边界，通过共享 MCP backbone 实现状态共享和去重，以 Webhook 为触发引擎，最终实现 5x PR 吞吐量和 200+ 漏洞的自动化捕获。理解这个架构比看多少个"安全 Agent prompt 技巧"都有用。
>
> **来源**：https://cursor.com/blog/security-agents（2026-03，Cursor 官方工程博客）
> **关联 Project**：`mcpeak/cursor-security-automation`（官方开源 MCP 参考实现）

---

## 背景：为什么安全自动化需要 Agent Fleet

Cursor 的工程师在九个月内将 PR 吞吐量提升了 5 倍。传统的安全工具——静态分析、刚性的代码所有权规则——在这个规模下已经不够用了。静态分析能发现模式化的漏洞，但无法理解复杂的代码逻辑；代码所有权规则能控制访问，但无法判断一段代码是否真的引入了安全风险。

> "Security tooling based on static analysis or rigid code ownership remains helpful, but is not enough at this scale." — Cursor Engineering Blog

Cursor 的解法不是"给现有流程加一个 AI 层"，而是**重新设计安全自动化的工作模式**：用一群专业化的 Agent 替代单一检查工具，每个 Agent 专注于一个特定的安全场景，通过事件驱动的方式协作。

---

## 架构全貌：四层结构

```
┌─────────────────────────────────────────────────────────────┐
│                     Webhook / GitHub Events                  │
│                   (PR 创建 / 代码变更 / 定时)                  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              Automation Trigger Layer                        │
│         Cursor Automations (Cloud Agent Platform)            │
└────────────────────────────┬────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Agentic      │   │  Vuln Hunter  │   │  Anybump      │
│  Security     │   │               │   │               │
│  Review       │   │               │   │               │
│  (PR Gate)    │   │               │   │               │
└───────┬───────┘   └───────┬───────┘   └───────┬───────┘
        │                   │                    │
        └───────────────────┼────────────────────┘
                            │
              ┌─────────────▼──────────────┐
              │   Security MCP Server      │
              │   (Lambda, Just-in-Time)   │
              │                            │
              │  • Persistent Data         │
              │  • Deduplication (Gemini)  │
              │  • Consistent Output       │
              └────────────────────────────┘
                            │
              ┌─────────────▼──────────────┐
              │   Invariant Sentinel       │
              │   (Daily Drift Monitor)    │
              └────────────────────────────┘
```

---

## 第一层：事件触发引擎（Cursor Automations）

Cursor 安全 Agent Fleet 的触发层基于 Cursor Automations 平台，这是一个云端 Agent 运行时（cloud agent），提供开箱即用的：

- **Webhook 接收**：接收 GitHub PR 事件、代码变更通知
- **定时触发**：支持每日/定期扫描
- **上下文传递**：将事件信息注入 Agent 的执行上下文

这层的关键是**不需要轮询**。传统安全扫描需要定时跑全量扫描，消耗大量资源。Cursor 的方案是让 Agent 在正确的时机"出场"——PR 创建时、分支合并时、每日巡检时。

> "Automations are powered by cloud agents, which gives them all the tools, skills, and observability that cloud agents have access to."

---

## 第二层：专业化 Agent 分工

四个安全 Agent 各司其职，形成分工体系：

### 2.1 Agentic Security Review（PR 看门人）

**职责**：对每个 PR 进行安全审查，可以评论 PR、发送 Slack 通知，并在发现关键漏洞时**阻断 CI**。

**核心设计决策**：这是一个**只读 Agent**——它发现问题，但不主动修复。它有权限评论 PR 和触发 gate check，但没有权限直接推送代码。

这个设计选择非常重要。Cursor 安全团队在实践中发现，Agent 在安全上下文中的误报率足以让人类在环（human-in-the-loop）成为必要：

> "The review agent explicitly does not push fixes. It finds, it reports, it blocks, but a human still decides what to done." — Snyk 分析

**结果**：过去两个月运行在数千个 PR 上，阻止了数百个安全问题进入生产环境。

### 2.2 Vuln Hunter（存量代码猎手）

**职责**：对现有代码库进行周期性安全扫描，将代码库划分为逻辑段，逐段搜索漏洞。

**核心设计决策**：这是**存量发现 Agent**，与 Agentic Security Review 的增量检查形成互补。传统安全扫描往往只关注新代码，存量代码中的历史漏洞才是企业安全债的大头。

团队通过 Slack 的 `@Cursor` 命令直接生成修复 PR——这意味着 Agent 不仅发现问题，还能**根据 Slack 指令生成修复代码**，将"发现"到"修复"的链路压缩到单次对话。

### 2.3 Anybump（依赖补丁自动化）

**职责**：自动化处理依赖漏洞修复。这是安全工作中最容易被"放弃"的环节——reachability 分析 → 追踪相关代码路径 → 运行测试 → 检查兼容性 → 通过后自动开 PR。

**核心设计决策**：这是一个**全自动修复 Agent**。与 Agentic Security Review 不同，它在测试通过后直接开 PR，不需要人类在环。但这不意味着它完全自主——它仍然依赖人类的 PR review 和合并动作。

> "After the PR is merged, Cursor's canary deployment pipeline provides a final safety gate before anything reaches production." — Cursor Engineering Blog

### 2.4 Invariant Sentinel（合规监控）

**职责**：每日监控代码库是否偏离一组安全和合规不变量。将代码库分段，启动子 Agent 验证每个分段是否满足不变量列表。

**核心设计决策**：这是**状态比对 Agent**，利用 Cursor Automations 的 memory 功能存储历史运行状态。每次运行后与前次结果比对，如果检测到漂移（drift），重新验证后再更新 memory。

这个 Agent 特别值得注意，因为它展示了一种**跨 Agent 状态共享**的模式：Agent 之间通过共享 memory 进行状态比较，而不是各自独立。

---

## 第三层：Security MCP Server（共享 backbone）

四个 Agent 共享一个定制 MCP server，以 **serverless Lambda** 方式部署，按需启动，不占用常驻资源：

```
                    ┌──────────────────┐
                    │  Security MCP    │
                    │  Server          │
                    │  (Lambda)        │
                    └───────┬──────────┘
                            │
        ┌───────────────────┼────────────────────┐
        │                   │                    │
        ▼                   ▼                    ▼
  ┌──────────┐       ┌──────────┐         ┌──────────┐
  │Persistent│       │Dedup     │         │Consistent│
  │Data      │       │(Gemini   │         │Output    │
  │Store     │       │Flash 2.5)│         │(Slack)   │
  └──────────┘       └──────────┘         └──────────┘
```

**三个核心功能**：

1. **Persistent Data（持久化数据）**：跟踪和测量安全影响的时序数据，用于持续优化触发策略
2. **Deduplication（去重）**：多个 Review Agent 同时运行可能用不同措辞描述同一个漏洞，通过 Gemini Flash 2.5 驱动的分类器判断语义等价性
3. **Consistent Output（一致输出）**：所有 Agent 的发现通过 MCP 发送格式统一的 Slack 消息，支持 dismiss/snooze 操作

这个 MCP server 是理解整个系统的关键：它不是简单地把 Agent 输出转发到 Slack，而是**承担了状态管理、去重和路由的职责**，让每个 Agent 可以是无状态的执行单元。

---

## 第四层：Terraform 管理的部署基础设施

所有安全工具变更通过 Terraform 管理，确保：

> "all changes to security tooling go through a standard review and deployment process."

这意味着安全 Agent 本身的变更也需要 code review——不是人类手动审批，而是通过 Terraform 的 standard review 流程。这是一个重要的**元安全（meta-security）考量**：你怎么保证你的安全 Agent 本身是安全的？

---

## 核心工程机制提炼

Cursor 安全 Agent Fleet 展示了几个重要的 Agent 工程机制：

### 1. 事件驱动触发（Event-Driven Invocation）

不是轮询，不是定时全量扫描，而是**在正确的时机让正确的 Agent 出场**。Webhook 驱动 PR 审查，定时驱动存量扫描，状态漂移驱动 invariant 告警。

### 2. 专业化分工 + 共享状态 backbone

每个 Agent 有明确职责边界（Review / Hunt / Patch / Monitor），但通过共享 MCP server 实现：
- 状态共享（时序数据）
- 发现去重（跨 Agent）
- 输出一致（Slack 格式）

### 3. 人类在环的精确控制

不同 Agent 对人类在环的需求不同：
- **Review**：Gate check 模式，Agent 发现，人类决定是否阻断
- **Anybump**：全自动修复，人类只做 PR review
- **Sentinel**：全自动比对，drift 触发后才告警

这不是"让人类批准每一步"，而是**在正确的决策点保留人类判断**。

### 4. MCP 作为 Agent 间通信协议

MCP 在这里不只是"工具调用协议"，而是**状态共享和协调协议**。去重、持久化、一致输出——这些都是多 Agent 协作中的核心挑战，MCP 作为 backbone 提供了解法。

---

## 这个案例教会我们什么

**安全 Agent 的设计不是写一个超级 prompt，而是设计一个 Agent 系统。** Cursor 安全团队花了大量工程工作在 MCP server、Terraform 部署、去重分类器上，prompt 本身反而非常简洁。

> "The prompt is simple because the surrounding infrastructure is not." — Snyk

这对所有想做"AI 安全自动化"的团队是一个重要的提醒：如果你的 Agent 系统只有 prompt 没有 infrastructure，你的 Agent 系统就是残缺的。

**具体来说**：
- 你需要状态管理（跨 Agent 的发现追踪）
- 你需要去重机制（LLM 输出天然的多样性）
- 你需要一致的输出路由（Slack / 告警 / ticket）
- 你需要部署治理（Terraform 管理安全工具本身）

---

## 标题备选

1. **Cursor 安全 Agent Fleet：事件驱动的多 Agent 协作实战** — 策略：好奇心缺口
2. **为什么 Cursor 的安全 Agent prompt 只有 15 行** — 策略：反直觉揭示
3. **从 5x PR 吞吐量看 Agent Fleet 的工程设计** — 策略：数据冲击

---

*本文属于 `orchestration/` cluster，记录多 Agent 协作模式与安全自动化工程实践。*