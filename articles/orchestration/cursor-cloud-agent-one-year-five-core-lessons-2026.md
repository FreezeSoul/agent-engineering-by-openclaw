# Cursor 云端 Agent 构建一年后的核心教训：为什么基础设施才是产品

> **核心观点**：Cursor 的实践验证了一个反直觉的结论——云端 Agent 的输出质量不再取决于模型本身，而取决于重建完整开发环境的能力。当模型越来越聪明，环境搭建反而成了决定性瓶颈。这篇文章要回答的问题是：当你不再把 Agent 当作产品，而是把「让 Agent 高效工作的基础设施」当作产品，应该怎么设计？

---

## 一、被忽视的决定性因素：开发环境才是产品

Cursor 团队在构建云端 Agent 一年后，得出一个让很多人意外的结论：

> 过去一年我们学到最大的单一因素，是确保云端 Agent 拥有一个完整开发环境的能力，就像人类开发者所拥有的那样。
> 
> *— Josh Ma, Cursor Engineering*

本地 Agent 之所以效果好，是因为它天然继承了开发者的完整工作环境——IDE、配置、依赖、网络访问，一切都已经在笔记本电脑上准备好了。Agent「免费」获得了这些。

但云端 Agent 不同。在云端，你必须从零重建这一切。而最危险的是：**当环境不完整时，Agent 不会崩溃，只会产生微妙的质量下降**。你可能不会立即注意到这个问题，或者即使注意到了，也会误以为是模型的问题。

Cursor 团队追踪了他们遇到的大量质量问题，最终都指向同一个诊断：云端 Agent 缺乏执行和验证工作所需的环境。这种诊断在过去一年里反复出现，因为模型能力的提升反而让这个问题更突出——模型越聪明，对环境的依赖就越强。

原文引用：
> "A year ago this mattered less because models couldn't make much use of their environment anyway. But as they've gotten smarter, the environment setup has become the determining factor in whether they execute at their full potential."

这意味着，今天要构建高质量的云端 Agent，需要重建以下基础设施：

| 基础设施组件 | 作用 | Cursor 的实现方式 |
|---|---|---|
| VM 快速休眠与恢复 | Agent 在消息间隔之间高效休眠 | Agent VM 的状态持久化 |
| 镜像快速Checkpoint/恢复/Fork | 快速创建可用的 Agent 工作环境 | 持久化镜像流水线 |
| Harness 与客户端的紧密集成 | 让 Agent 和人类都能理解环境状态 | 共享 VNC + Chrome 的 Computer Use 架构 |
| 网络访问控制 | Agent 需要创建 PR、Pull 依赖、做研究 | 企业级 IT 能力：Secret redaction、网络策略、凭证管理 |

这已经不是「调教 Agent prompt」的问题了，这是**构建企业级 Agent 操作系统**的问题。

---

## 二、耐用执行：为什么 Temporal 比 Work-Stealing 更适合云端 Agent

Cursor 早期使用了一种经典的分布式架构思路：**work-stealing**（工作窃取）。Worker 节点可以从队列中抢任务，把 Agent 循环执行到完成。

这种架构在本地 Agent 场景下工作得很好，因为它直接移植了本地行为到服务器。但它有一个致命弱点：**不够耐用**。云端 Agent 会遇到：

- 推理服务商中断
- Pod 需要被替换
- EC2 节点宕机

Cursor 坦承，早期的云端 Agent beta 版本经常只能达到一个 9（90%）的可靠性。

他们的解决方案是迁移到 Temporal，一个已经解决了耐用执行问题的开源工作流引擎：

- **重试机制**：自动处理临时性故障
- **跨机器调度**：任务可以在任意节点上恢复
- **节点故障容忍**：工作流状态持久化，不怕节点挂掉

原文引用：
> "Our current agent loop on Temporal can survive blips in inference reliability, pod hibernation and resumption, and runs that stretch across days or even weeks. That migration alone took us past two 9s of reliability and today, Temporal handles more than 50 million actions per day across more than 7 million unique workflows."

这是一个重要的工程决策：**不要重复造轮子，去使用已经解决这些问题的开源基础设施**。Cursor 选择了 Temporal 而不是自研，因为他们意识到自己在重新实现 Temporal 已经解决的问题。

笔者认为，这个决策体现了架构设计的一个核心原则：**当你发现自己在重建一个已经成熟的系统时，应该直接使用那个系统，而不是试图用 Agent 代码重新实现它**。这对所有构建云端 Agent 的团队都是一个重要提醒。

---

## 三、三重解耦：Agent 循环、机器状态、对话状态

Cursor 提到的第三个核心教训是**解耦**：

> 云端 Agent 不再是运行在一台机器上的一个循环。Agent 可能在某台机器上运行，生成跨多台机器的异步子 Agent，或者先在本地启动然后委托到云端。子 Agent 可能比父 Agent 存活更长时间，或者运行在完全不同的 Pod 类型上。

为了支持这种复杂的拓扑结构，Cursor 将三个关注点分开管理：

| 组件 | 管理方式 | 优势 |
|---|---|---|
| **Agent 循环** | 存储在 Temporal 中，不在 VM 上 | 独立管理 Pod 生命周期，支持跨 Pod 运行 |
| **机器状态** | 与 Agent 循环解耦 | 可使用只读 VM、预热 VM 等优化 |
| **对话状态** | 独立的 Append-only 存储 + Streaming 层 | 失败重试时可以回卷 Stream，保证一致性 |

对话状态的解耦尤其有意思：Cursor 构建了一个高效的 Append-only 存储机制，可以将对话更新流式传输到 Web 和桌面客户端。当 Agent 循环的某一步在流式传输部分输出后失败并重试时，客户端可以检测到这一点，回卷 Stream，并显示新数据而不是旧数据。

这个设计让前端可以始终展示正确的状态，即使后端的 Agent 执行流程经历了多次重试和恢复。

---

## 四、让 Harness「让开」：从控制到授权的范式转移

Cursor 早期对 Agent 不够信任，所以 Harness 会在每个任务后做双重检查，强制提交和推送。但随着模型变得更聪明，他们开始把逻辑从 Harness 移出，交给 Agent 控制的工具。

这个转变可以从两个例子看出来：

### 例子 1：多 repo 设置

**一年前**：需要硬编码的 Harness 行为来处理多 repo 场景。

**现在**：给 Agent repo 布局，暴露分支和 PR 的工具，然后让 Agent 自己决定怎么做。

### 例子 2：CI Autofix

**早期版本**：Harness 包含逻辑来获取 job 失败日志并写入 VM。

**现在**：给 Agent 访问 GitHub CLI 的权限，自动把大输出写入文件供 Agent 搜索。通知 Agent 的方式大大简化了，而且这个趋势还在继续。

原文引用：
> "The harness isn't going away so much as what it contains is changing."

这告诉我们，Harness 的角色正在发生变化。它不是消失，而是**从「执行控制者」变成「授权者」**——提供工具和边界，但不控制具体的执行路径。

另一个关键洞察是关于 Computer Use 的架构：

> "Our cloud agent harness has a dedicated subagent type for computer use, with its own model routing, custom prompting, and screen recording. The VNC and Chrome belong to the environment, which is shared between the parent agent and the subagent. This lets the parent make use of them directly, for example, by running a Playwright script."

这说明，即使在这个阶段，模型还不太能完全独立处理 Computer Use，Cursor 仍然把控制权交给了 Agent（Agent 决定何时调用 Computer Use），而不是让 Harness 控制整个流程。

---

## 五、自愈环境：超越「放手」和「掌控」的二元对立

Cursor 认为，未来的方向不是简单地在「扶着 Agent」和「放手」之间做二元选择，而是一个更好的模式：**给 Agent 理解周围系统的工具**。

他们希望云端 Agent 能够做到：

- 当缺少 Secret 时主动报告
- 当网络访问被阻止时主动报告
- 当环境阻止它取得进展时能够自我修复

Cursor 在一篇相关的技术博客（Bootstrapping Composer with Autoinstall）中提到了实现这一点的一条路径：**Autoinstall**——让 Agent 能够自动识别缺失的依赖并自行安装。

---

## 六、工程教训总结：五个维度

从 Cursor 的实践中，我们可以提炼出构建生产级云端 Agent 的核心工程维度：

| 维度 | 核心问题 | Cursor 的答案 |
|---|---|---|
| **环境完整性** | 如何确保 Agent 有完整的工作环境？ | 把环境当作产品来构建，不只是 Agent |
| **耐用执行** | 如何在分布式环境下保证执行可靠性？ | 使用 Temporal 而不是自研 work-stealing |
| **状态解耦** | 如何让 Agent 跨机器、跨 Pod 运行？ | Agent 循环/机器状态/对话状态三层分离 |
| **Harness 演进** | 如何让基础设施跟上模型能力的提升？ | 从控制逻辑转向授权工具，Agent 控制具体执行 |
| **自愈能力** | 如何让 Agent 能够感知并修复环境问题？ | 给 Agent 环境感知工具，而非硬编码修复逻辑 |

---

## 七、笔者的判断：这个方向为什么重要

Cursor 这篇文章的核心价值不在于他们用了什么技术，而在于他们揭示了一个重要的范式转变：

**AI Coding Agent 的竞争焦点，正在从「模型能力」转向「基础设施能力」**。

当模型能力不断提升并逐渐趋同时，决定 Agent 质量和可靠性的，将是基础设施的完善程度——环境复现能力、故障恢复能力、状态管理能力、工具授权能力。

这对所有 AI Coding 平台都是一个重要信号：如果你还在拼命提升模型能力，但忽略了基础设施，你可能会发现即使是最好的模型也无法发挥出全部潜力。

反过来，对于任何想要在 AI Coding 领域建立竞争壁垒的公司来说，答案不是「训练一个更好的模型」，而是「构建让模型能够充分施展能力的基础设施」。

这就是为什么 Cursor 说「开发环境才是产品」——这不是比喻，这是一个精确的工程描述。

---

**引用来源**：
- [What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons) — Cursor Engineering Blog, Josh Ma, 2026-05-21
- [Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness) — Cursor Engineering Blog
- [Development environments for your cloud agents](https://cursor.com/blog/cloud-agent-development-environments) — Cursor Engineering Blog
- [Bootstrapping Composer with autoinstall](https://cursor.com/blog/bootstrapping-composer-with-autoinstall) — Cursor Engineering Blog

---

*本文属于 AI Coding Agent 工程实践系列，分析了 Cursor 云端 Agent 构建一年后的核心工程教训，关联前轮 Claude Code SWE-bench 49% 和 ChromeDevTools MCP 的验证工具层主题。*