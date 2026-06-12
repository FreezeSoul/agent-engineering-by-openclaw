---
title: Cursor 云端 Agent 工程教训：为什么 Harness 是产品本身
date: 2026-06-12
source: Cursor Engineering Blog
source_url: https://cursor.com/blog/cloud-agent-lessons
author: Cursor Team (Josh Ma)
tags: [harness, cloud-agents, temporal, durable-execution, self-healing, multi-agent]
cluster: harness
---

> 原文引用 1："The single biggest factor in cloud agent output quality is ensuring it has a full development environment, like a developer has." — Cursor Engineering Blog

> 原文引用 2："We migrated to Temporal... can survive blips in inference reliability, pod hibernation and resumption, and runs that stretch across days or even weeks." — Cursor Engineering Blog

---

## 核心命题

Cursor 用一年时间把云端 Agent 的可靠性从「一个九」（90%）提升到「两个九」（99%+），代价是重写整个执行层。这个过程教会他们一件事：**云端 Agent 的核心竞争力不是模型，而是 Harness——那个把模型、持久化、环境管理缝在一起的操作系统层**。

---

## 一、「开发环境就是产品」：为什么环境质量决定 Agent 上限

本地 Agent 的开发环境是「免费」的——它直接继承你笔记本上的所有配置、依赖、网络。但在云端，你必须从零重建这一切，而且很难判断「重建得够不够好」。

** Cursor 的诊断**：模型能力越强，环境配置的差距对输出质量的影响就越大。一年前，模型本身是瓶颈；现在，环境setup成了决定因素。

重建完整环境需要：
- **VM 高效休眠与恢复**：消息间隙中保存/恢复 VM 状态
- **持久化 Checkpoint 流水线**：快速、持久地保存、恢复、分叉 VM 镜像
- **Tight Harness 与客户端集成**：让 Agent 和人类都能理解、交互环境

> 原文引用 3："A year ago this mattered less because models couldn't make much use of their environment anyway. But as they've gotten smarter, the environment setup has become the determining factor in whether they execute at their full potential."

**笔者认为**：这解释了为什么 Cursor 在 Cloud Agents 上投入大量工程资源在「重建本地开发体验」上——这不是用户体验问题，是模型能力的数学问题。

---

## 二、Temporal 迁移：为什么 Durable Execution 不是可选项

Cursor 最初的云端 Agent 架构是「work-stealing」模式——Worker 节点竞争获取 Agent 任务并循环执行完成。这在本地工作得很好，但移植到服务器端就成了脆弱的设置。

**可靠性数据**：
- 迁移前：Cloud Agents 经常只有 **一个九（90%）** 的可靠性
- 迁移后：超过 **两个九（99%）**
- Temporal 现在每天处理超过 **5000 万次 Action**，跨越超过 **700 万个独立 Workflow**
- 内部超过 **40% 的 PR 来自 Cloud Agents**

Cursor 选择 Temporal 的原因：他们发现自己在重新发明 Temporal 已经解决的很多原语（retry 机制、跨机器调度、节点故障持久化）。

**架构演进**：
- 从「永恒」Agent Workflow 迁移到多个短 Workflow——每个完成单一任务后退出，使版本升级更容易
- 将 Activities 拆分出来，更好地捕获超时和重试——特别是当 async tool calls、subagents 和 inference provider outages 改变了底层假设时

> 原文引用 4："Our current agent loop on Temporal can survive blips in inference reliability, pod hibernation and resumption, and runs that stretch across days or even weeks."

**笔者认为**：Temporal 在这里扮演的角色是「外部化的工作流状态机」——Agent Loop 不再存在于 VM 本身，而是存在于 Temporal。这带来了关键优势：Pod 生命周期可以独立管理，Agent 可以跨不同类型的 Pod 运行（包括 readonly VM 或 prewarmed VM）。

---

## 三、解耦 Agent、机器与会话状态

云端 Agent 不再是「一台机器上运行的一个循环」：

- Agent 可能在一台机器上运行，但在多台上生成分布式 Async Subagents
- 可能本地启动，然后委托工作到云端
- Subagent 可能比父 Agent 存活更久，或者运行在完全不同的 Pod 类型上

**Cursor 的解耦策略**：

| 组件 | 管理方式 | 关键设计 |
|------|---------|---------|
| Agent Loop | Temporal（不在 VM 上） | Pod 生命周期独立管理 |
| Machine State | 独立管理 | 支持 readonly/prewarmed VM 优化 |
| Conversation State | 独立存储/流媒体层 | Append-only storage + 流式重试 |

**Conversation 分离的关键设计**：
- 构建了高效的 Append-only 存储机制，向 Web 和桌面客户端流式传输对话更新
- 这一层处理重试——如果 Agent Loop 的一步在流式传输部分输出后失败并重试，客户端可以检测到这一点，回卷其流，并显示新数据而不是旧数据

**笔者认为**：这种解耦是「让 Agent 做正确的事，而不是让系统做简单的事」的工程体现。把状态外部化增加了复杂度，但让 Agent 在故障恢复、跨域迁移、并发运行成为可能。

---

## 四、「学会让路」：Harness 的边界在哪儿

早期 Cursor 的 Harness 不信任 Agent，所以在每一步后 double-check 其工作，强制 commit 和 push。随着模型变聪明，他们开始把逻辑从 Harness 移到 Agent 控制的工具中。

**具体例子**：

| 旧方式（Harness 控制）| 新方式（Agent 控制）|
|-------------------|------------------|
| 多 Repo 设置需要硬编码 Harness 行为 | 给 Agent 仓库布局，暴露分支和 PR 工具，让它决定如何工作 |
| CI Autofix 需要 Harness 获取 job failure logs 并写入 VM | 给 Agent 访问 GitHub CLI，自动把大输出写入它可以搜索的文件 |

**Computer Use 的特殊处理**：
Cloud Agent Harness 有专门的 Computer Use Subagent 类型，有自己的模型路由、自定义提示和屏幕录制。VNC 和 Chrome 属于环境，由父 Agent 和 Subagent 共享。这让父 Agent 可以直接使用它们（例如运行 Playwright 脚本）。

> 原文引用 5："We use this scaffolding because models aren't quite ready to handle computer use on their own, but the agent still controls when to invoke it."

**Harness 的演化方向**：不是消失，而是「内容在变」。Harness 不再包含业务逻辑，而是包含「如何把控制权交给 Agent」的元逻辑。

**云端 Agent 的特殊 Prompt 考虑**：
- 需要更 autonomous 的提示词设计，因为阻塞的成本更高
- 本地 Agent 停下来等权限时你知道，但云端可能等几个小时

---

## 五、自愈环境：超越「扶着走」和「完全放手」

Cursor 正在研究的下一代模式：不是二选一（hand-holding vs. 完全放手），而是给 Agent 理解周围系统的工具。

**目标**：Cloud Agents 能够：
- 报告 secrets 缺失
- 报告网络访问被阻止
- 报告环境阻止它们取得进展
- 然后以「自愈」方式采取行动

**Bootstrapping Composer with Autoinstall** 是他们的一条路径：

> 原文引用 6："We want cloud agents to be able to report when secrets are missing, network access is blocked, or when their environment is otherwise preventing them from making progress, and to then be able to act in a self-healing way."

**笔者认为**：自愈环境的关键不是「让 Agent 自动修复一切」，而是「让 Agent 有能力报告和请求它需要的东西」。这是「Harness as Platform」思维的延伸——Harness 不是审查 Agent 的决策，而是为 Agent 提供它做出好决策所需的上下文。

---

## 六、工程机制全景图

```
┌─────────────────────────────────────────────────────────────────┐
│                     Cursor Cloud Agent Architecture              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│  │   Desktop    │     │     CLI      │     │   Cloud VM   │    │
│  │    Client    │     │              │     │   (Dedicated)│    │
│  └──────┬───────┘     └──────┬───────┘     └──────┬───────┘    │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              ▼                                   │
│                   ┌──────────────────┐                          │
│                   │  Cursor Harness  │                          │
│                   │  (Shared Runtime)│                          │
│                   └────────┬─────────┘                          │
│                            │                                     │
│         ┌──────────────────┼──────────────────┐                  │
│         ▼                  ▼                  ▼                  │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐            │
│  │  Context   │    │    MCP     │    │   Hooks    │            │
│  │  Management│    │   Servers  │    │            │            │
│  └────────────┘    └────────────┘    └────────────┘            │
│                              │                                   │
│                              ▼                                   │
│                   ┌──────────────────┐                          │
│                   │  Subagent System │                          │
│                   │  (Named, Own     │                          │
│                   │   Prompts/Models)│                          │
│                   └────────┬─────────┘                          │
│                            │                                     │
│                            ▼                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                   Temporal Workflow                      │    │
│  │  • Durable Execution (survive VM pod hibernation)        │    │
│  │  • Checkpoint/Resume across days/weeks                  │    │
│  │  • 50M+ Actions/day, 7M+ Workflows                      │    │
│  │  • 40%+ of Cursor PRs from cloud agents                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 七、核心工程决策复盘

| 决策 | 旧方案 | 新方案 | 收益 |
|------|-------|-------|------|
| 执行层 | Work-stealing on VMs | Temporal Workflow | 99%+ 可靠性（从 90% 提升） |
| 环境管理 | 每任务重建环境 | VM 休眠/恢复 + Checkpoint | 高效状态保持 |
| Agent vs Harness | Harness 控制业务逻辑 | Harness 提供平台，Agent 控制业务 | 更 autonomous，更可扩展 |
| Subagent 类型 | 无 | 专用 Computer Use Subagent | 隔离复杂性，支持多模态 |

---

## 八、关键判断

1. **环境 setup 是模型能力的乘数**：当你投入时间让环境配置接近完美，模型性能会成比例提升。

2. **Durable Execution 是云端 Agent 的基础设施**：不是可选项，是让 Agent 在长时间任务中保持可靠的基础。

3. **Harness 的价值在于「何时让路」**：好的 Harness 不是减少 Agent 的控制，而是精确地知道何时把控制权交给 Agent。

4. **自愈不是自动修复，而是报告+请求**：让 Agent 有能力表达它需要什么，比让它自动修复一切更可工程化。

---

## 关联项目

- **wizenheimer/canary** — QA Harness for Claude Code（367 Stars）：E2E testing with screen recordings, console logs, network HARs, and Playwright traces

---

## 备选标题

1. **Cursor 云端 Agent 的 99% 可靠性是怎么炼成的** — 策略：数据冲击（< 30 单位）
2. **Harness 不是安全网，是 Agent 的操作系统** — 策略：痛点共鸣（< 30 单位）
3. **从 90% 到 99%：Cursor 云端 Agent 的工程教训** — 策略：好奇心缺口（< 30 单位）

---

*原文链接：[What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons) | Cursor Engineering Blog | Josh Ma | 2026-06-02*