---
title: "Cursor 云 Agent 的工程转身：从 work-stealing 到 Temporal 与三层状态解耦"
date: 2026-06-30
tags: [Cursor, Cloud Agents, Durable Execution, Temporal, Harness Engineering, State Decoupling, Self-Healing, Autonomy Inversion]
source: https://cursor.com/blog/cloud-agent-lessons
source_kind: Cursor Blog (first-party)
author: Josh Ma
published: 2026-06-02
round: 595
cluster: deep-dives
---

# Cursor 云 Agent 的工程转身：从 work-stealing 到 Temporal 与三层状态解耦

> 这篇文章不是「Cursor 怎么跑云 Agent」的营销稿，而是 Cursor 团队自己复盘 **从 work-stealing 自研编排到全面迁移到 Temporal** 这一步具体走了多远、走得多痛。文章披露了一组结构性事实：(1) 早期 work-stealing 架构只有 1 个 9 的可靠性，迁移到 Temporal 后稳定过 2 个 9，今日承载 **每天 5000 万次 action、700 万条独立 workflow**；(2) 把 agent loop / machine state / conversation state 拆成三个独立层，让 pod 替换、subagent 跨机器、用户本地开始 + 云端接续都成为可重放的；(3) 把"harness 里做的工作"反向迁回成"工具"，完成 autonomy inversion；(4) 自愈环境（self-healing via autoinstall）让环境缺陷从「不可见的错误降级」变成「Agent 自己报告 + 自我修复」。这 4 个机制决策直接关系到「为什么我们 fork 的 Agent 框架总是跑长一点就崩」。

---

## 这篇文章要回答的核心问题

过去两年 Agent 工程的争论基本停在两个问题上：**Agent 怎么编排** 和 **Agent 怎么调 prompt**。而 Cursor 在 2026 年 6 月发布的 [What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons) 把问题推到了第三层：**当 Agent 跑在云端而不是本地时，哪些工程原则会被颠覆、哪些会被放大？**

笔者认为，这篇文章的真正价值不在 "Cursor 也用 Temporal" 本身，而在于它把云 Agent 从「把本地 Agent 搬到服务器」重新定义为「围绕 Agent 构建操作系统层」，并把这一年的具体痛苦决策（work-stealing → Temporal、loop/state/stream 三层分离、autonomy inversion、self-healing env）公开出来做正负反馈设计指引。

> "Cloud agents have improved immensely in just the last few months, and we expect the rate of change to only accelerate from here. Cursor cloud agents let teams take advantage of this expansive surface without having to build or maintain the infrastructure underneath it."

一句话总结 Cursor 的判断：**模型进步曲线已经把 Agent 框架的瓶颈从"调度"挪到"环境"，把"harness 行为"挪到"工具"**。

---

## 关键拐点数据：1 个 9 → 2 个 9

Cursor 公开了一组罕见的 SRE 数字：

| 阶段 | 架构 | 可靠性 | 代价 |
|------|------|--------|------|
| 上线早期 | work-stealing 自研 worker node | **1 个 9**（约 90%） | 用户经常丢失会话状态 |
| 迁移后 | Temporal durable execution | **> 2 个 9** | 每天 5000 万 action / 700 万 workflow |
| 业务占比 | "Internally, more than 40% of our PRs come from cloud agents, and growing." | — | — |

> "We started building cloud agents with a work-stealing architecture, where worker nodes could pick up agents and loop them to completion. It transplanted what works locally to a server and it was a fragile setup—our early beta of cloud agents often operated at one 9 of reliability. As cloud agents matured, we found ourselves on the verge of rebuilding a lot of the durable execution primitives that Temporal already solves (e.g., retry mechanisms, scheduling work across machines, durability across node failures), so instead we migrated there."

**反直觉点**：Cursor 一开始的选择是 **work-stealing**——这是分布式系统界非常主流的设计。但事实证明，当 Agent 工作流比 transaction 长得多、推理节点和执行节点都会失败时，**自己重做一套 durable execution** 是在重建 Temporal。

换句话说：**你不是 Google/Amazon，没有能力同时再造一个 S3 + DynamoDB + Step Functions**——云 Agent 工程里这事更明显，因为模型推理本身就比传统 API 更脆弱、更长程、更跨节点。

**给团队的启示**：当你的 Agent 框架还在自研 "scheduled executor / retry middleware / state checkpoint"，你大概率该停下来接 Temporal，而不是继续往上堆功能。

---

## 机制 1：三层状态解耦（agent loop / machine state / conversation state）

Cursor 把云 Agent 的状态切成 3 个独立层，每层有自己的生命周期：

| 层 | 职责 | 替换/迁移影响 |
|---|------|------|
| **Agent loop** | 跑在 Temporal 上的核心循环 | 业务逻辑层，独立于 VM |
| **Machine state** | Pod/VM 节点本身的状态 | 可被替换、调整大小、做只读化/预热化 |
| **Conversation state** | 用户可见的对话历史 | append-only 持久化 + 流式分发 |

> "To make that work, we've found it valuable to keep the agent loop, the machine state, and the conversation state as decoupled components. Because the agent loop lives in Temporal rather than on the VM itself, we can manage pod lifecycles independently and run agents across different kinds of pods — including optimizations like readonly VMs or prewarmed VMs."

**关键技术决策**：

1. **Agent loop 进 Temporal 而不进 VM** —— 这是与"work-stealing"最大的差别。loop 不再和机器绑定，所以 VM 可以：
   - 进入 readonly 状态（节能）
   - 预热好（低延迟）
   - 跨多种 pod 类型路由

2. **Conversation state 用 append-only + retry-aware stream** —— 输出层与执行层分离。

> "On the conversation side, we separated the storage and streaming layer from the core agent workflow. We built an efficient append-only storage mechanism that streams conversation updates out to web and desktop clients. This layer accounts for retries, so that if a step of the agent loop fails after streaming partial output and then gets retried, the client can detect this, rewind its stream, and show the new data instead of the old."

这一段是云 Agent 用户体验的 **最强差异化点**：当一段输出已经推送给用户、然后失败被重试时，客户端要能 **rewind stream**，显示新的输出而不是叠加在旧的输出之上。这是设计上看上去很小，但工程上要协调 storage 层、stream 层、UI 层才能不露痕迹完成的事。

**笔者认为**，这一段是 2026 年 Agent 框架的隐藏门槛——**多数开源 Agent 框架（包括 LangGraph、CrewAI 等）都没解决"已发送给用户的部分输出如何 revert"的问题**。Cursor 这条经验值得被反复引用。

---

## 机制 2：Autonomy Inversion（"知道什么时候让开"）

Cursor 命名了一个很有意思的概念：**autonomy inversion**——把 harness 里曾经做的事反向迁回工具里，给 Agent 控制权。

早期 Cursor 的 harness 是"双重检查 + 强制 commit + 强制 push"——这是因为模型不靠谱，所以用 harness 兜底：

> "Early on, we didn't trust the agent very much, so the harness would double-check its work after every task, force a commit, and push. As models got smarter, we started moving logic out of the harness and into tools the agent controls."

具体迁移包括：

- **多仓库 setup**：以前是 hardcoded harness 行为，现在把 repo layout 给 Agent，让 Agent 用 branches 和 PRs 工具自己决定
- **CI Autofix**：以前 harness 抓 CI failure logs 写到 VM，现在给 Agent GitHub CLI + 让它把大输出写文件供 grep

> "The harness isn't going away so much as what it contains is changing. Computer use is a good example right now. Our cloud agent harness has a dedicated subagent type for computer use, with its own model routing, custom prompting, and screen recording. The VNC and Chrome belong to the environment, which is shared between the parent agent and the subagent."

**关键的边界判断**：computer use 子 agent 的 VNC 和 Chrome 是 **environment 一部分**，但 Agent 仍然 control 调用时机——所以环境是分层的，**每一层都在自己的 granularity 上做 autonomy**。

> "Cloud agents also need different kinds of prompts in the harness than local agents do. We encourage them to be more autonomous, because the cost of blocking is much higher. Locally, you know when an agent has stopped and is waiting for permission, but in the cloud, it could sit there for hours before you go back and check on it."

**笔者认为**，这条洞察直接挑战了"云 Agent = 更严格的权限校验"这个常见误区。Cursor 的反思路是：**云 Agent 的成本结构让"阻塞等权限"变得极贵**，所以 harness 的 prompt 要比本地 Agent 提示它"更主动"，而不是相反。

---

## 机制 3：Self-Healing via Autoinstall

这是 5 节里最短的一节，但工程上意义重大——Cursor 直接承认"环境 bug 是云 Agent 输出质量的最大杀手"：

> "Instead of a crash or an error message, often the only indication is a subtle degradation in output quality. You might not notice it at first, or if you do, you might chalk it up to the model."

——这是非常罕见的、诚实的工程复盘：**云 Agent 的失败模式不是崩溃，是"无声降级"**——你看起来 Agent 没在工作，其实是环境缺一个 tool/bin/library。这件事 90% 的团队连监控都不会做。

Cursor 解决方案：让 Agent 自己 report + 自我修复：

> "We want cloud agents to be able to report when secrets are missing, network access is blocked, or when their environment is otherwise preventing them from making progress, and to then be able to act in a self-healing way. In a recent research blog we talked about one path for achieving this which we call 'autoinstall.'"

**工程含义**：云 Agent 的 self-healing 必须满足 4 个最小条件——
1. 能感知环境缺陷（missing tools / blocked network）
2. 能把这个状态报告给上游（不是 silently degraded）
3. 能自己尝试修复（autoinstall）
4. 修复成功要进入 audit log（不能再 silent）

| Self-Healing 失败模式 | 触发场景 | 修复路径 |
|--------------------|---------|---------|
| Tool 缺失 | `pg_config` / `cmake` 不在 PATH | autoinstall + retry |
| 网络阻塞 | outbound port blocked | 上报 + 等网络策略调整 |
| Secret 缺失 | API key 不在 secret manager | **不能 autoinstall**（必须人工配）—— 这是边界条件 |
| 环境降级 | OS 镜像损坏 | fork VM image from 已校验快照 |

**笔者认为**，Cursor 给出的是一份非常宝贵的 **"哪些事不能自愈"清单**：secrets 必须人工，错误是 critical 的 inference broker outage 必须回退——这些边界条件如果 Agent 自动修了，反而引入不可审计的风险。

---

## 4 个机制决策的关系

这 4 个机制不是并列的。它们构成一个 **递进的工程依赖链**：

```
[1 个 9 → 2 个 9]
   ↓  需要 durable execution
[Temporal 迁移]
   ↓  需要 loop/state/stream 三层解耦
[三层状态解耦]
   ↓  允许 autonomy inversion
[harness → tools]
   ↓  释放 Agent 自我感知能力
[self-healing env]
```

也就是说，**没有 (1) Temporal，就没有 (2) 三层解耦；没有 (2)，就没有 (3) autonomy inversion；没有 (3)，就没有 (4) self-healing**。这是云 Agent 工程里少见的、被完整披露出来的演进路径。

---

## 对照本仓库已有文章

| 已有文章 | 关注点 | 本文补充 |
|---------|------|---------|
| [Codex Remote Queue/Steer + Plan/Goal](../practices/ai-coding/openai-codex-remote-engineering-control-plane-queue-vs-steer-plan-vs-goal-2026.md) | **控制侧 UX 远程化**（prompt 介入模式 + 意图分层）| **执行侧基础设施**（durable execution + 状态解耦）|
| [Anthropic Effective Harnesses for Long-Running Agents](../harness/anthropic-effective-harnesses-long-running-agents-2026.md) | 长程 Agent 的系统层 harness 设计原则 | Cursor 给出了"实际部署后哪条原则会被放大、哪条会被颠覆"|
| [VulnClaw](../projects/unclecheng-li-vulnclaw-ai-pentest-agent-1166-stars-2026.md) | 目标驱动的 Agent 终止条件 | Cursor 给出云 Agent "环境故障" 这种被多数框架忽略的终止条件 |

**本文补的最关键一点**：**云 Agent 不是"把本地 Agent 移植到服务器"，而是"围绕 Agent 重新构建操作系统层"**。这条认知差决定了 90% 自研云 Agent 框架会在一年内重写一遍。

---

## 直接引用：4 处原文精选

**① 1 个 9 → 2 个 9 的真话**：
> "We started building cloud agents with a work-stealing architecture... It transplanted what works locally to a server and it was a fragile setup—our early beta of cloud agents often operated at one 9 of reliability... Our current agent loop on Temporal can survive blips in inference reliability, pod hibernation and resumption, and runs that stretch across days or even weeks."

**② 三层状态解耦的边界判断**：
> "To make that work, we've found it valuable to keep the agent loop, the machine state, and the conversation state as decoupled components."

**③ Autonomy inversion 的反面（早期）vs 现状（autonomy 流动）**：
> "The harness isn't going away so much as what it contains is changing."

**④ 云 Agent 失败的真凶是环境，不是模型**：
> "Instead of a crash or an error message, often the only indication is a subtle degradation in output quality."

---

## 给团队的 4 条可落地建议

1. **别自己造 Temporal**：如果你的 Agent 框架还在自研 "scheduled executor / retry middleware / state checkpoint"，停下来接现成的 durable execution 库（Temporal / Restate / DBOS 任选）。自研路径的成本曲线在 6 个月内就会指数级升高。

2. **状态分层先于 prompt 调优**：把 agent loop / machine / conversation 三层在架构图上画出来。如果你的代码三层耦合在同一个进程里，云 Agent 路径上会撞到的"pod 替换"、"retry-aware stream"、"cross-pod subagent" 问题一个都解决不了。

3. **prompt 改动跟着 autonomy inversion 走**：每 3 个月回看一次 harness 里那些"曾经为了 safe 而做的兜底逻辑"——现在还能不能迁到 tools 里？computer-use / repo-layout 之类的边界条件提示，要把"harness 强校验"的 prompt 改成"工具 + Agent 控制调用时机"。

4. **环境监控先于模型监控**：你要监控的不是"模型答了没有"，而是"Agent 有没有 bin"——tool 缺失、network 阻塞、secret missing 这些 silent degradation 才是云 Agent 的真正 SLO。

---

## 启示

Cursor 这篇文章最值得被记录的不是 "Temporal 怎么用"，而是 **云 Agent 工程必须按"操作系统的复杂度"重新组织，而不是按"应用的复杂度"**。当一组数字：1 个 9 → 2 个 9、5000 万 action/day、40%+ PR 来自 Cloud Agents，被公开摆出来时，所有还在用 "本地 Agent + SSH 服务器 + 启动 Docker" 这套做法的团队，都会撞上 Cursor 已经撞过的那面墙。

> **所以你应该立刻做的事**：
> 1. 把你 Agent 的状态三层（loop / machine / conversation）在架构图上画清，画不清就先停下来
> 2. 列出你 harness 里目前还存在的"为安全而强行 commit / push / 校验"的逻辑，看看哪几条可以反转回 tools
> 3. 给你云端跑 1 个小时以上的 Agent 加环境监控（tool 缺失 / 网络阻塞 / secret missing），不监控这些相当于在 silent degradation 上裸奔
> 4. 评估是否迁移到 Temporal 或类似库

写完这 4 步，再讨论"我们该不该把 Agent 跑云端"才有意义。

---

## 来源

- **Article**: [What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons) — Cursor Blog (Josh Ma, 2026-06-02)
- **Cursor 早期 cloud agents**：参考 [Cloud Agent documentation](https://cursor.com/cloud)
- **关联工程文章**：[Anthropic Effective Harnesses for Long-Running Agents](../harness/anthropic-effective-harnesses-long-running-agents-2026.md)（系统层 harness）
- **关联 R594 文章**：[Codex Remote 控制平面](../practices/ai-coding/openai-codex-remote-engineering-control-plane-queue-vs-steer-plan-vs-goal-2026.md)（决策侧 UX 远程化）
- **关联 R595 项目**：[HKUDS/Vibe-Trading](../projects/hkuds-vibe-trading-mandate-gated-trading-agent-15213-stars-2026.md)（deploy-side harness，mandate-gated live trading + provider reliability layer）
- **底层引用工程**：[Temporal](https://temporal.io)（durable execution primitive）
