# Cursor Cloud Agents 一年复盘：五大约束条件下的工程演化路径

> **来源**: [Cursor Blog - What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)（2026年5月21日）
> **作者**: Josh Ma, 9 min read

---

## 核心命题

Cloud Agent 不是「把本地 Agent 搬到服务器上」——这是一个根本性的认知偏差。Cursor 在过去一年里发现，构建 Cloud Agent 的真实工作更接近于**为 Agent 构建一套操作系统层**，而不是简单的环境迁移。这个过程中暴露的问题，与为人类开发者构建基础设施时的问题高度对称。

---

## 一、环境即产品（The Development Environment is the Product）

这是 Cursor 在一年实践中总结出的最重要发现：**Cloud Agent 输出质量的决定性因素，是确保它拥有完整开发环境的能力**。

本地 Agent 免费继承了你笔记本上的工作环境。Cloud Agent 需要从零重建这一切，而判断「环境是否已经完美重建」这件事，意外地困难。

> "Instead of a crash or an error message, often the only indication is a subtle degradation in output quality. You might not notice it at first, or if you do, you might chalk it up to the model."
> — [Cursor: What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)

关键洞察：**环境不完整时，Agent 不会报错，只会在输出质量上出现难以追踪的退化**。这个问题一年前影响较小，因为当时模型本身对环境的利用能力有限。但随着模型变聪明，环境配置的质量变成了决定 Agent 能否发挥全部潜力的决定性因素。

Cursor 估算，今天要实现「完整环境」，需要重建的基础设施包括：

- **用户工具**：用于构建 Agent 环境的更好工具
- **休眠/恢复机制**：在消息之间高效地休眠和恢复 Agent VM
- **Checkpoint 管道**：快速且持久地 checkpoint、restore 和 fork VM 镜像
- **Harness-客户端集成**：让 Agent 和人类都能解释和交互环境
- **网络访问控制**：为 Agent 创建 PR、pull 依赖、做研究的受控网络访问
- **企业级 IT for Agents**：包括 secret redaction、网络策略和凭证管理

这最后一项尤其值得注意——Cursor 发现自己在构建的实质上是**Agent 的企业 IT 系统**，这与人类开发者所使用的基础设施在概念上高度对称。

---

## 二、长时运行 Agent 需要持久执行（Durable Execution）

Cloud Agent 带来了本地 Agent 并不突出的可靠性挑战。Cloud Agent 运行在独立 VM 中，更容易并行运行多个 Agent、委托长时任务（通常是小时级别而非分钟级别）。

但 VM 带来了新的暴露：推理供应商中断、Pod 需要被替换、EC2 节点宕机。

Cursor 最初构建 Cloud Agent 时使用了 work-stealing 架构——worker 节点可以拾取 Agent 并循环完成。这移植了本地工作的方案，但这是个脆弱的设置，其早期 beta 的可靠性只有「一个 9」（90%）。

> "As cloud agents matured, we found ourselves on the verge of rebuilding a lot of the durable execution primitives that Temporal already solves (e.g., retry mechanisms, scheduling work across machines, durability across node failures), so instead we migrated there."
> — [Cursor: What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)

这是关键决策点：**Cursor 没有自己重建 Temporal 已经解决的那些原语，而是直接迁移到了 Temporal**。迁移后，可靠性超过了「两个 9」，今天 Temporal 每天处理超过 **5000 万次操作**，跨越超过 **700 万个独立 workflow**。

内部数据：超过 **40% 的 Cursor PR 来自 Cloud Agent**，并且这个比例还在增长。

### Cursor 从 Temporal 迁移中学到的架构经验

1. **从「永恒」Agent workflow 转向多个短 workflow**：每个 workflow 完成单一任务后退出，这让版本升级更容易
2. **将 activity 分离出来**：以更好地捕获超时和重试，因为异步工具调用、子 Agent 和推理供应商中断改变了底层假设

这意味着 Cloud Agent 的架构已经演化为：**Agent Loop 存在于 Temporal 中，而不是在 VM 本身上**。因此可以独立管理 Pod 生命周期，跨不同类型 Pod 运行 Agent（包括 readonly VM 或 prewarmed VM 等优化）。

---

## 三、解耦 Agent、机器与会话状态（Decoupling Agents and Machines from Conversation State）

Cloud Agent 不再只是「在一台机器上运行的一个循环」。

> "Instead, an agent might run on one machine, spawn async subagents across several, or start locally then delegate work to the cloud. A subagent might even outlive its parent, or run on a completely different kind of pod."
> — [Cursor: What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)

为了让这个模型工作，Cursor 发现将三个组件保持解耦很有价值：
- **Agent Loop**
- **机器状态**
- **会话状态**

由于 Agent Loop 存在于 Temporal 中而不是 VM 本身上，可以独立管理 Pod 生命周期。

在会话方面，Cursor 将**存储和流式层与核心 Agent workflow 分离**。他们构建了一个高效的 append-only 存储机制，向 Web 和桌面客户端流式传输会话更新。这一层处理重试——如果 Agent Loop 的一步在流式传输部分输出后失败，然后重试，客户端可以检测到这一点，回滚其流并显示新数据而不是旧数据。

---

## 四、知道何时让路（Knowing How to Get Out of the Way）

构建 Cloud Agent harness 意味着不断重新评估多少行为是确定性的、多少是交给 Agent 的。

早期 Cursor 对 Agent 的信任度不高，所以 harness 会在每个任务后双重检查其工作，强制 commit 和 push。随着模型变得更聪明，他们开始将逻辑从 harness 移出，移交给 Agent 控制的工具。

> "A year ago, multi-repo setups required hardcoded harness behavior. Now, we can give the agent the repo layout, expose tools for branches and PRs, and let it decide how to do the work."
> — [Cursor: What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)

同样的转变发生在 CI Autofix 上——早期版本的 harness 包含抓取 job 失败日志并写入 VM 的逻辑。现在，Cursor 只需给 Agent 访问 GitHub CLI 并自动将大输出写入文件。

**Harness 不会消失，但它包含的内容正在改变**。Computer Use 是一个很好的例子——Cursor 的 Cloud Agent harness 有一个专门的 subagent 类型用于 computer use，有自己的模型路由、自定义提示和屏幕录制。VNC 和 Chrome 属于环境，由父 Agent 和 subagent 共享。这让父 Agent 可以直接使用它们（例如运行 Playwright 脚本）。Cursor 使用这个脚手架是因为模型还没有完全准备好自己处理 computer use，但 Agent 仍然控制何时调用它。

另一个关键区别：**Cloud Agent 需要不同于本地 Agent 的 harness 提示**。Cursor 鼓励 Cloud Agent 更自主，因为阻塞的代价要高得多。本地情况下，你知道 Agent 何时停止并等待许可，但在云端，它可能会闲置数小时然后你才回去检查。

---

## 五、自愈 Agent 环境（Self-Healing Agent Environments）

Cursor 的前瞻性方向：**超越「牵手」和「放手」之间的二元选择**。

> "A better pattern is to give the agent tools for understanding the system around it."
> — [Cursor: What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)

Cursor 希望 Cloud Agent 能够：
- 在 secret 缺失、网络访问被阻止或其环境阻止其取得进展时进行报告
- 然后以自愈方式采取行动

Cursor 在最近的研究博客中提到的路径之一称为「autoinstall」——Agent 可以检测缺失的依赖并自动安装它们。

Cloud Agent 在过去几个月已经有了巨大改进，Cursor 预计变化速度只会加快。

---

## 工程方法论：从这个案例学到什么

### 1. 持久执行原语不应该自己重建

Cursor 发现自己在重建 Temporal 已解决的原语时，选择直接迁移而非自己重建。这是正确的工程判断——当一个开源基础设施已经解决了你的核心问题时，选择它而不是重新发明轮子。

### 2. 环境配置是质量的决定性因素

一年前的观点可能是「模型是瓶颈」。今天的观点是：**环境配置的质量是决定性因素**，而这个问题比最初看起来要复杂得多。环境不完整不会导致错误，而是导致难以追踪的质量退化。

### 3. 解耦是架构复用的前提

将 Agent Loop、机器状态和会话状态解耦，使 Cursor 能够跨不同类型 Pod 运行 Agent、优化成本并支持更复杂的编排模式。这是 Cloud Agent 架构从「单 Agent 单机」演进到「多 Agent 分布式协作」的基础。

### 4. Harness 是一个演进目标而非固定设计

Cursor 的经验表明，Harness 的内容会随着模型能力变化。早期需要大量 guardrail，随着模型变强可以移除。更重要的是，**Harness 工程师应该持续关注模型能力的变化**，并相应地调整 harness 的干预程度。

---

## 关联主题

本文与以下主题形成关联：
- **Harness 工程**：Cursor 的五点经验是 Harness 设计的重要实践案例
- **持久执行**：Temporal 迁移经验对构建生产级 Agent 有直接参考价值
- **自愈环境**：与环境配置质量主题强相关

---

**引用来源**：
- [Cursor Blog: What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)
- [Cursor Blog: Continually improving our agent harness](https://cursor.com/blog/continually-improving-agent-harness)
- [Anthropic Engineering: Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)