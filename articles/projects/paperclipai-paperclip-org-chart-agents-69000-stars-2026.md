# Paperclip AI：当你的 AI Agent 们有了组织架构

> 这个项目解决了一个长期以来让人头疼的问题——当你同时运行 20 个 AI Agent 时，如何让它们像一个团队的员工一样协作，而不是一群各干各的独立进程？

## 核心命题

Paperclip 的 tagline 一句话就说清楚了本质：**If OpenClaw is an employee, Paperclip is the company.**

它不是一个 AI Agent 框架，而是一个** Agent 编排控制平面**——用组织架构（Org Chart）、预算（Budget）、工作流（Task System）和治理（Governance）来协调多个 AI Agent。

<!-- Screenshot pending: browser unavailable, to be added manually -->

## 一、为什么这个方向值得关注

笔者认为，Agent 框架经历了三个阶段：

- **第一阶段：单 Agent 框架**（LangChain / CrewAI）——如何让一个 Agent 完成任务
- **第二阶段：多 Agent 协作**（AutoGPT / OpenHands）——多个 Agent 如何配合
- **第三阶段：Agent 组织化管理**（Paperclip）——如何像管员工一样管一群 Agent

Paperclip 处于第三阶段的起点。它的核心问题是：**当你的公司有 10 个 AI Agent，分别负责编码、审核、运维、客服时，谁来决定它们的优先级？谁来控制预算？谁来审批它们的敏感操作？**

不是所有团队都需要这一步。但当你的 Agent 数量超过 5 个、成本超过每月 $1000、团队成员超过 3 人时，你就会开始需要 Paperclip 回答的那些问题。

## 二、核心机制拆解

### Org Chart：给 Agent 分配职位

Paperclip 的 Org Chart 不是装饰，而是真正的权限体系：

```
CEO Agent
├── CTO Agent
│   ├── Engineering Team
│   │   ├── Frontend Agent
│   │   └── Backend Agent
│   └── DevOps Agent
├── CFO Agent
└── Marketing Agent
```

每个 Agent 有：
- **Role（角色）**：CEO、CTO、Engineer
- **Title（职称）**：给人类看的描述
- **Reporting Line（汇报线）**：向上汇报给谁
- **Budget（预算）**：每月最多花多少 Token
- **Permissions（权限）**：可以执行哪些操作

这听起来像组织架构图，但它解决的是实际问题：当 Frontend Agent 需要调用生产环境 API 时，它需要向 CTO Agent 发起申请，而不是直接动手。

### Heartbeat：让 Agent 持续运行而不需要人盯着

传统 Agent 的问题是：终端关闭，Agent 就停止。

Paperclip 的 Heartbeat 机制解决了这个问题：

```python
# 每 5 分钟唤醒一次，检查是否有新任务
Agent.wake_on_schedule("0 */5 * * *")
Agent.wake_on_event("pull_request.opened")
Agent.wake_on_goal_achieved()  # 持续工作直到任务完成
```

Agent 醒来后，从上次中断的地方继续工作——不丢失上下文，不重新开始。Paperclip 官方把这个叫做**Persistent Agent State**：

> "Agents resume the same task context across heartbeats instead of restarting from scratch."

这对长任务至关重要。一个需要 2 小时完成的代码重构，不应该因为开发者下班而中断。

### 预算强制执行：Agent 超支自动停止

这是笔者认为 Paperclip 最有企业价值的机制。

当一个 Agent 的月预算用完时，它会自动停止——不会继续消耗 Token，不会产生意外账单。这对财务管理至关重要：

> "Monthly budgets per agent. When they hit the limit, they stop. No runaway costs."

原子执行（Atomic Execution）保证了不会有双重工作：Agent 完成任务时，任务会被锁定（checkout + execution lock），防止两个 Agent 同时做同一件事而浪费预算。

### 治理与审批：谁批准 Agent 的敏感操作

Paperclip 实现了多级审批机制：

- **Board Approval**：重大决策需要人类审批（如访问生产环境）
- **Rollback**：配置变更会被版本化，错误的变更可以回滚
- **Immutable Audit Log**：所有操作都有完整日志，不可篡改

这与企业级的安全合规需求完全对齐。

## 三、技术架构一览

Paperclip 的架构分为两层：

```
┌─────────────────────────────────────────────┐
│           PAPERCLIP SERVER                   │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │Identity │ │ Work &  │ │Heartbeat│        │
│  │& Access │ │ Tasks   │ │Execution│        │
│  └─────────┘ └─────────┘ └─────────┘        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │Org Chart│ │Budget & │ │Activity │        │
│  │& Agents │ │ Costs   │ │& Events │        │
│  └─────────┘ └─────────┘ └─────────┘        │
└─────────────────────────────────────────────┘
            ▲          ▲          ▲
     ┌──────┴──┐  ┌────┴────┐ ┌──┴──────┐
     │ Claude  │  │ OpenClaw │ │  HTTP   │
     │  Code   │  │          │ │web bots │
     └─────────┘ └──────────┘ └─────────┘
```

支持适配的 Agent 类型：
- Claude Code
- OpenClaw
- Codex / CLI agents
- HTTP/Webhook bots
- 自定义 Adapter

**一个公司可以用 Claude Code 写代码，用 OpenClaw 做运维，用自建 bot 处理客服**——Paperclip 提供统一的任务协调层。

## 四、竞品对比

| 维度 | Paperclip | 传统 Agent 框架 | 企业 SaaS 工具 |
|------|-----------|----------------|--------------|
| 核心抽象 | 组织架构 | 工作流/Chain | 任务管理 |
| 权限控制 | Agent 级别 RBAC | 无或极简 | 人类员工级别 |
| 预算管理 | 每 Agent 月度预算 | 无 | 无 |
| 多 Agent 支持 | 原生（跨框架）| 通常只支持同框架 | N/A |
| 自我托管 | ✅（MIT License）| ✅ 通常开源 | ❌ 通常 SaaS only |
| 适用规模 | 5+ Agents | 1-3 Agents | 单人 |

笔者认为，Paperclip 的真正竞争对手不是其他 Agent 框架，而是**企业自己搭建的 Agent 管理脚本**。当团队开始用 Notion + Cron + 各种脚本拼凑 Agent 管理方案时，Paperclip 提供了开箱即用的正式替代。

## 五、什么时候不该用 Paperclip

笔者认为，在以下情况下，Paperclip 是过度设计：

- **团队只有 1-2 个 Agent**：直接用 Claude Code / Cursor 就够了
- **Agent 任务是独立且临时的**：不需要组织架构和审批流
- **预算充足、不需要严格控制成本**：用多少算多少
- **全云托管，不接受自我托管**：Paperclip 是自托管方案，需要运维能力

Paperclip 解决的是**规模化**和**治理**的问题。如果你的 Agent 还没到这个规模，它的复杂度会变成负担。

## 六、如何开始

Paperclip 是开源项目，MIT License，可以直接 GitHub 部署：

```bash
# Clone 并运行
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
npm install
npm start

# 访问 http://localhost:3000
```

官方文档地址：https://paperclip.ing/docs

> 引用来源：
> - [GitHub README：paperclipai/paperclip](https://github.com/paperclipai/paperclip)
> - 官方 tagline："If OpenClaw is an employee, Paperclip is the company"
