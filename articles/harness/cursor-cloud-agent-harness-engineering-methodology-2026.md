# Cursor 云端 Agent 的 Harness 工程方法论：两篇博客的底层逻辑

> **核心判断**：Cursor 的两篇 Harness 博文揭示了一个重要趋势——Harness 不是「安全护栏」，而是 **Agent 的操作系统层**：负责环境构建、状态管理、任务调度、故障恢复、质量评估。这与 Anthropic 的 GAN Architecture 框架一脉相承，但 Cursor 从产品工程角度给出了更具体的实现路径。

---

## 一、背景：为什么云端 Agent 需要不一样的 Harness

Cursor 博客的开篇就点明了核心张力：

> 「一年前，我们觉得云端 Agent 只是本地 Agent 的简单延伸。现在我们发现，这越来越不像是在移植一个本地 Agent 到服务器上，而更像是在围绕它构建一个操作系统层。」

这个判断来自实践教训。云端 Agent 面临四个本地不会遇到的问题：

| 问题维度 | 本地 Agent | 云端 Agent |
|---------|----------|-----------|
| **执行时长** | 分钟级，会话级 | 小时级/天级，甚至周级 |
| **环境可控性** | 直接继承开发者机器 | 需要从零重建完整开发环境 |
| **故障模式** | 无（本地稳定）| 推理 provider outage、Pod 休眠/重启、EC2 节点宕机 |
| **并行规模** | 单用户单 agent | 多 agent 并行、跨机器协作 |

这些问题不是「大号本地 Agent」能解决的。

---

## 二、开发环境就是产品

Cursor 第一篇博客（cloud-agent-lessons）最反直觉的结论是：**云端 Agent 输出质量的决定性因素，是它是否拥有完整的开发环境**。

本地 Agent 天然继承开发者的环境——编辑器配置、本地依赖、Git 状态、网络权限，全部免费获得。云端 Agent 需要从零重建这一切，而且没有错误信息提醒你重建得不完整：

> 「通常唯一的迹象是输出质量的细微下降。你可能一开始不会注意到，或者即使注意到了，你也会把它归咎于模型。」

Cursor 的解决方案是构建一整套企业级 IT 基础设施：

- **环境构建工具**：让用户能高效配置 agent 的运行环境
- **Hibernate/Resume**：消息间隔之间休眠和恢复 VM
- **Checkpoint/Restore/Fork**：快速可靠地 checkpoint、恢复和 fork VM 镜像
- **Tight harness integration**：让 agent 和人类都能解释和交互环境
- **企业级网络管控**：Secret redaction、网络策略、凭证管理

---

## 三、持久化执行：从 Work-Stealing 到 Temporal

Cursor 早期的云端 Agent 架构是 work-stealing——worker 节点抢任务，loop 到完成。这个架构从本地移植而来，脆弱得可笑：早期 beta 经常只有 **one 9 of reliability**（90%）。

他们的解决方案是迁移到 **Temporal**——一个成熟的工作流引擎。Cursor 官方数据：

> 「迁移到 Temporal 后，我们跨越了两个 9 的可靠性门槛。今天，Temporal 每天处理超过 **5000 万次 action**，横跨超过 **700 万个独立工作流**。内部超过 **40% 的 PR 来自云端 Agent**，而且还在增长。」

这个数字的震撼在于：Cursor 的核心代码产出已经高度依赖云端 Agent，而这种依赖建立在 Temporal 提供的持久化执行之上。Temporal 解决了三个问题：

1. **Retry 机制**：推理 provider 抖动时的自动重试
2. **跨机器调度**：Pod 休眠/恢复后的任务迁移
3. **节点故障容忍**：数天甚至数周的长任务不因节点宕机而中断

Cursor 还分享了一个工程细节：**从「永恒」agent 工作流拆成多个短工作流**，每个工作流只完成一个任务就退出。这样做的好处是版本升级更容易，因为每次只影响一个原子任务的生命周期。

---

## 四、三层状态分离架构

Cursor 提出的第三个关键设计是：**将 agent loop、机器状态、对话状态解耦为三个独立组件**。

传统架构：agent loop 绑定在 VM 上，状态耦合。

Cursor 架构：

- **Agent Loop 在 Temporal**（不在 VM 上）→ Pod 生命周期独立管理，agent 可以跨不同类型 Pod 运行
- **机器状态** → 可以做 readonly VM、prewarmed VM 等优化
- **对话状态分离** → 构建了高效的 append-only 存储机制，流式输出到 Web 和桌面客户端，同时处理 retry 和 rewind

这个设计的精妙之处在于：解耦后，每一层都可以独立演进和优化，而不需要改动其他层。

---

## 五、评估 Harness 变化的两个维度

Cursor 第二篇博客（continually-improving-agent-harness）给出了他们如何量化评估 harness 改进的方法，这是目前业界最透明的实践分享之一。

### 维度一：离线 Benchmark

维护公开 benchmark + 内部 CursorBench，提供快速、标准化的质量读数，能跨时间对比。但 Cursor 明确指出：**即使最好的 benchmark 也只能近似真实使用场景**，所以不能完全依赖它们。

### 维度二：在线 A/B 实验

将两个或多个 harness 变体并行部署，A/B 测试真实使用。关键指标包括：

- **Keep Rate**：agent 生成的代码在用户代码库中留存的比例——这个指标直接衡量「用户是否需要手动调整 agent 输出」
- **用户满意度信号**：用语言模型分析用户对 agent 初始输出的反馈——用户直接转向下一个功能说明 agent 做得好，用户粘贴 stack trace 说明 agent 没搞定

> 「有时在线测试告诉我们一个看似有前途的想法应该被搁置。曾经试过一个更贵的模型做上下文摘要，观察到它对 agent 质量的影响可以忽略不计，不值得更高的成本。」

---

## 六、Harness 的演进方向：从护栏到脚手架

Cursor 两篇博客最核心的观点是：**Harness 正在经历从「管控」到「赋能」的范式转移**。

早期 Cursor 不太信任 agent，所以 harness 在每个任务后 double-check，强制 commit 和 push。随着模型能力提升，他们开始把逻辑从 harness 移到 agent 控制的工具中：

| 旧 harness 逻辑 | 现状 |
|--------------|------|
| harness 抓取 CI 失败日志写入 VM | 给 agent 访问 GitHub CLI + 自动写大输出到文件 |
| 多 repo 设置需要硬编码 harness 行为 | 给 agent repo layout + 分支/PR 工具，让它自己决定 |
| 每次编辑后强制 check | 移除护栏，信任模型 |

但这不意味着 harness 在消失，而是**它管理的内容在变化**：

> 「Harness 不是在消失，而是它包含的东西在变化。Computer use 是一个好例子。我们的 cloud agent harness 有专门的 subagent 类型做 computer use，有自己的模型路由、自定义提示和屏幕录制。VNC 和 Chrome 属于环境，被 parent agent 和 subagent 共享。」

---

## 七、自我修复的环境：下一代 Agent 环境

Cursor 最后的展望是**让 Agent 能报告和自愈环境问题**：

- 当 secrets 缺失时报告
- 当网络访问被阻止时报告
- 当环境阻止它取得进展时能够自我修复

他们把这个能力叫做 **"autoinstall"**——让 agent 能够自动识别缺失的依赖并自我安装，这是摆脱「二进制选择」（要么 hold its hand，要么 get out of its way）的路径。

---

## 八、工程启示录

Cursor 的两篇博文构成了一个完整的 Harness 工程方法论：

### 核心原则

1. **环境即产品**：云端 Agent 的质量上限由环境决定，而不是模型本身
2. **持久化执行是基础设施**：Temporal 不是可选项，而是云端 Agent 可靠性的基座
3. **三层分离**：agent loop、机器状态、对话状态独立演进
4. **评估驱动演进**：离线 benchmark + 在线 A/B 双轨评估
5. **赋能而非管控**：Harness 的职责从管控转向提供能力和工具

### 关键架构决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 执行引擎 | Temporal | 成熟的持久化执行、retry、跨机器调度能力 |
| 工作流设计 | 短任务工作流 | 版本升级更容易，故障边界更清晰 |
| 环境管理 | VM checkpoint + fork | 快速创建干净环境，支持并行 |
| 网络管控 | 企业级 IT 基础设施 | Secret redaction、网络策略、凭证管理 |
| 评估体系 | CursorBench + Keep Rate + LLM 满意度分析 | 快速迭代 + 真实质量信号 |

### 未来方向

> 「AI 辅助软件开发的未来是多 agent 的。与其让每个子任务都经过单个 agent，系统将学会在专业化的 agent 和 subagent 之间委托：一个负责规划，一个负责快速编辑，一个负责调试，每个都在自己最擅长的领域发力。将这些协调能力做好本质上是一个 harness 挑战。」

这意味着 **Harness Engineering 的重要性只会增加**，而不会减少。

---

**引用来源**：

- Cursor Blog: [What we've learned building cloud agents](https://www.cursor.com/blog/cloud-agent-lessons)（2026-05-21）
- Cursor Blog: [Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)（2026-04-30）