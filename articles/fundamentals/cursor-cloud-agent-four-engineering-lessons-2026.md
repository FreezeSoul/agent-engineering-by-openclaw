# Cursor 云端 Agent 实战复盘：四个被忽视的工程教训

> **核心观点**：Cursor 的云端 Agent 建设揭示了一个被低估的事实——当 Agent 从个人工具升级为团队基础设施时，**开发环境、持久化执行、状态解耦、harness 哲学**这四个维度必须作为一等公民来设计，而不是作为本地 agent 的服务端移植。

**关联 Project**：`cursor.com/blog/cloud-agent-lessons`（本文）+ `obra/superpowers`（方法论闭环）

---

## 一、背景：云端 Agent 不是「本地 Agent 的服务器版」

Cursor 在 2025 年推出云端 Agent 时，最初的假设很简单：云端 Agent 就是把本地 Agent 跑在服务器上，加个并行能力和更长任务支持。

一年后的复盘说明，这个假设是错的。云端 Agent 带来了一系列本地不会遇到的问题：

- **环境重建**：本地 Agent 直接继承用户的开发环境（依赖、配置、工具链），云端 Agent 必须从零构建完整环境，且环境问题往往不会报错，只会导致输出质量悄悄下降
- **中断暴露**：本地 Agent 跑在用户电脑上，中断风险低；云端 Agent 跑在 VM/Pod/EC2 节点上，面临推理服务商故障、Pod 回收、节点宕机
- **状态复杂性**：本地 Agent 是单机器单循环，云端 Agent 可能是跨多机器、多租户、父 agent 死后子 agent 继续运行

Cursor 的结论是：**云端 Agent 的复杂度更接近构建操作系统层，而非移植一个本地工具**。

---

## 二、教训 1：开发环境是一等产品

### 问题本质

本地 Agent 不需要考虑环境问题——它直接运行在开发者的电脑上，继承了完整的工具链、依赖和配置。

云端 Agent 没有这个 inheritance，必须自己重建。问题在于：

> 很多情况下，环境不完整不会导致报错，只会导致输出质量**悄悄下降**。开发者可能以为是模型问题，实际上是环境问题。

Cursor 追踪了大量「模型问题」，最终发现最大因素是**云端 Agent 没有完整的环境来执行和验证工作**。

### Cursor 的重建内容

为了达到「完整开发环境」，Cursor 必须重建以下基础设施：

| 基础设施 | 作用 |
|---------|------|
| 用户工具（UI） | 让用户配置 Agent 环境 |
| VM 休眠/恢复机制 | 在消息之间高效保存/恢复状态 |
| 检查点/恢复/分叉 Pipeline | 快速持久化保存 VM 镜像 |
| Harness + 客户端集成 | 让 Agent 和人类都能理解和交互环境 |
| 网络访问控制 | 让 Agent 能创建 PR、拉取依赖、做 research |
| Secret 管理 + 凭证管理 | 企业级安全要求 |

Cursor 的总结：

> 今天，要达到「完整环境」需要重建大量基础设施——本质上是在为 Agent 构建企业级 IT 能力。

这和 Superpowers 的「设计优先」理念形成有趣对比：Superpowers 在流程层约束 Agent 行为，Cursor 在基础设施层给 Agent 配备完整执行能力。两者都是为了让 Agent 真正发挥潜力，而非只是看起来能动。

---

## 三、教训 2：持久化执行需要专门的执行层

### 问题本质

本地 Agent 的可靠性挑战主要是「资源竞争」——和本地其他进程抢 CPU/内存。云端 Agent 的可靠性挑战是「分布式中断」：

- 推理服务商故障
- Pod 需要回收和重启
- EC2 节点宕机
- 任务可能跨越几天甚至几周

Cursor 早期用「工作窃取架构」（worker nodes 拾取 agent 任务并循环完成），结果是**可靠性只有 1 个 9**（90% 可用）。

### 迁移到 Temporal

Cursor 评估后选择了 Temporal 作为执行层，而不是自己重建分布式执行能力：

> 我们在重建 Temporal 已经解决了的大量持久化执行原语（重试机制、跨机器调度、节点故障恢复），所以我们迁移到了 Temporal。

迁移后的效果：
- 可靠性从 ~90% 提升到 99%+
- Temporal 现在每天处理超过 **5000 万次 action**，跨越超过 **700 万个独立 workflow**
- Cursor 内部超过 **40% 的 PR 来自云端 Agent**，且比例还在增长

### 工程经验

Cursor 在 Temporal 架构上学到的经验：

1. **从「永恒」Agent workflow 转为多个短 workflow**：每个 workflow 完成一个任务后退出，这样版本升级更容易
2. **将 activity 拆分**：更好地捕获超时和重试——当底层假设变化（异步工具调用、子 agent、推理服务商故障）时，拆分能让重试更精准

这是一个典型的「不要重复造轮子」决策，但前提是要先识别出你要解决的是哪类问题（持久化执行 vs 应用逻辑）。

---

## 四、教训 3：三层状态需要解耦

### 问题本质

本地 Agent 的状态模型很简单：一个循环在一台机器上运行。

云端 Agent 的状态模型复杂得多：

- Agent loop 可能在机器 A 上运行，spawn 异步子 agent 跨多台机器
- 子 agent 可能比父 agent 活得久
- 子 agent 可能运行在完全不同的 Pod 类型上
- 对话状态需要在 Web/Desktop 客户端之间同步，且要处理重试导致的截断/回滚

### Cursor 的解耦方案

Cursor 将状态分为三层，每层独立管理：

| 状态层 | 管理方式 | 关键设计 |
|-------|---------|---------|
| **Agent Loop** | Temporal（不在 VM 上） | Pod 生命周期独立管理，支持 readonly/prewarmed VM 优化 |
| **Machine State** | VM 生命周期管理 | Pod 生命周期与 Agent loop 分离 |
| **Conversation State** | 独立存储/流式层 | 分离自核心 Agent workflow，支持 append-only 写入、客户端重试回滚 |

关于对话状态的流式层设计：

> 我们构建了一个高效的 append-only 存储机制，将对话更新流式输出到 Web 和 Desktop 客户端。这个层处理重试——如果 Agent loop 的一步在流式输出后失败并重试，客户端能检测到，回滚流并展示新数据，而不是显示旧数据。

这解决了一个微妙的 UX 问题：当 Agent 工作时，用户看到的是实时流式输出，但如果某步失败重试，用户不应该看到冲突的旧数据+新数据，而是应该看到干净的最终状态。

---

## 四（续）、教训 4：知道什么时候「让开」

### 问题本质

构建云端 Agent harness 的核心挑战是：**判断多少行为应该是确定性的，多少应该交给 Agent**。

早期 Cursor 的 harness 非常「家长式」：
- 每完成一个任务就 double-check
- 强制要求 commit 和 push
- 多仓库场景用硬编码 harness 行为

模型变强后，这种方式成了瓶颈——**harness 在帮倒忙**。

### 演进方向

一年后的转变：

> 一年前，多仓库设置需要硬编码 harness 行为。现在，我们可以给 Agent 更高级的目标，让它自己决定如何处理多仓库场景。

Cursor 的演进方向是：**把逻辑从 harness 移到 Agent 可控的工具中**。当 Agent 能控制自己的工具时，它可以根据上下文灵活调整行为，而不是被 harness 强制执行固定流程。

这与 Anthropic 的 harness 哲学形成对比——Anthropic 的 harness 强调「人类保留最终决策权」，Cursor 的方向是「Agent 有更多自主权，人类在关键节点干预」。两种哲学各有适用场景。

---

## 五、与 Superpowers 的方法论呼应

Cursor 的四个教训与 Superpowers 的软件工程方法论形成了有趣的对照：

| Cursor 教训 | Superpowers 对应 |
|-----------|-----------------|
| 开发环境是一等产品 | 提供完整开发环境（Superpowers 也依赖环境完整性） |
| 持久化执行需要专门执行层 | Superpowers 的长时间自主运行（2+ 小时不离计划）依赖可靠的执行基础 |
| 三层状态解耦 | Superpowers 的 human checkpoint 设计——状态解耦让人能在正确时机介入 |
| 知道什么时候「让开」| Superpowers 的设计优先——先设计后实现，Agent 在批准的设计内自主执行 |

两者都在解决同一个根本问题：**如何让 Agent 的能力真正释放，而不是被自己或 harness 的短视决策限制**。

---

## 引用

> "The single biggest factor in cloud agent output quality is ensuring it has a full development environment, like a developer has."
> — [Cursor Engineering Blog](https://cursor.com/blog/cloud-agent-lessons)

> "Today, getting to 'full environment' requires rebuilding a surprising amount of infrastructure."
> — [Cursor Engineering Blog](https://cursor.com/blog/cloud-agent-lessons)

> "We started building cloud agents with a work-stealing architecture... it was a fragile setup—our early beta of cloud agents often operated at one 9 of reliability."
> — [Cursor Engineering Blog](https://cursor.com/blog/cloud-agent-lessons)

> "We migrated to Temporal... that migration alone took us past two 9s of reliability and today, Temporal handles more than 50 million actions per day."
> — [Cursor Engineering Blog](https://cursor.com/blog/cloud-agent-lessons)

> "Over time, we've learned how to better architect our Temporal workflows. We've moved from 'eternal' agent workflows to multiple shorter ones that exit after completing a single task, which makes version upgrades easier."
> — [Cursor Engineering Blog](https://cursor.com/blog/cloud-agent-lessons)

---

*关联项目*：[obra/superpowers：让编码 Agent 真正学会软件工程方法论](./obra-superpowers-agentic-skills-software-development-methodology-2026.md)