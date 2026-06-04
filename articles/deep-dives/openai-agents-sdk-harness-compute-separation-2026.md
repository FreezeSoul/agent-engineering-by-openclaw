# OpenAI Agents SDK 的下一步：Harness 与 Compute 的分离工程学

## 核心命题

OpenAI 刚刚更新了 Agents SDK，这一次的核心变化不是模型升级，而是**把 Agent 的执行环境拆成了两个独立平面**：Harness（控制平面）和 Compute（计算平面）。这个分离解决了一个长期困扰 Agent 工程的问题——当沙箱容器崩溃时，整个运行状态也跟着丢了。分离后的方案让 Agent 可以跨容器持久化、checkpoint 恢复、按需扩展——这是企业级 Agent 基础设施的关键一步。

> "Separating harness and compute helps keep credentials out of environments where model-generated code executes."
> — OpenAI Agents SDK Blog

---

## 一、问题：传统 Agent 执行环路的结构性缺陷

在讨论这次更新之前，需要先理解为什么这个分离如此重要。

传统 Agent 执行环路的问题在于**Harness 和 Compute 是耦合在同一进程里的**。Agent loop（模型调用、工具决策、上下文管理）和 workspace（文件读取、命令执行、代码运行）绑定在一起。这意味着：

1. **状态丢失风险**：如果运行 Agent 的容器崩溃或过期，所有中间状态消失，Agent 只能从头开始
2. **扩缩容困难**：由于状态与特定计算实例绑定，无法轻易把 Agent 分配到不同容器或并行运行多个实例
3. **安全边界模糊**：credentials 和 model-generated code 共存于同一环境，为 prompt injection 和数据泄露留下了口子
4. **本地到生产的鸿沟**：开发者本地原型和线上生产环境差异巨大，难以保持一致的行为

OpenAI 这次的判断是：这些问题不是靠更好的模型能解决的，需要重新设计 Agent 的运行时架构。

---

## 二、解法：Harness-Compute 分离架构

### 2.1 Harness：控制平面的职责

Harness 是 Agent 的控制平面，负责：

- **Agent Loop 执行**：模型调用、工具决策、上下文字节管理
- **状态管理**：记忆、checkpoint、snapshot
- **工具编排**：MCP 集成、shell/apply_patch 等原生工具
- **安全边界**：credentials 管理、权限控制、审计日志

官方原文中描述的 Agents SDK harness 的关键能力：

> "The updated Agents SDK gives the model a powerful harness with instructions, tools, approvals, tracing, handoffs, resume bookkeeping, and the kind of model behavior used in Codex-style agents."

这意味着 OpenAI 把 Codex（在 OpenAI 内部经过大规模生产验证的 Agent 执行模式）的能力，下放到了 Agents SDK 这个通用框架里。

### 2.2 Compute：计算平面的职责

Compute 平面专注于执行任务所需的计算资源：

- **沙箱执行**：隔离的容器环境，运行 Agent 生成的代码
- **工作空间**：文件读取/写入、依赖安装、命令执行
- **工具可用性**：Agent 需要的所有系统级工具（browser、shell、文件系统）

新的 Agents SDK 原生支持多个沙箱提供商：Blaxel、Cloudflare、Daytona、E2B、Modal、Runloop、Vercel。这种多提供商支持的目的是避免厂商锁定，同时让企业可以根据自己的基础设施选择合适的部署方式。

### 2.3 Manifest 抽象：工作空间的可移植性

为了解决「本地原型到生产部署」的一致性问题，SDK 引入了 **Manifest 抽象**：

```python
# 描述 Agent 工作空间的 Manifest
manifest = Manifest(
    mount_local=["src/", "tests/"],
    output_dir="./outputs",
    storage=["s3://bucket/inputs", "r2://bucket/outputs"]
)
```

开发者可以用 Manifest 定义：
- 需要挂载的本地文件
- 输出目录位置
- 外部存储集成（AWS S3、GCS、Azure Blob、Cloudflare R2）

这个抽象让 Agent 的工作空间从「特定机器上的目录」变成了「可移植的配置声明」——同一个小agent 可以无缝地从本地开发切换到云端生产。

---

## 三、关键工程机制：Durable Execution

Harness-Compute 分离带来的最重要工程能力是 **Durable Execution**（持久化执行）。

> "When the agent's state is externalized, losing a sandbox container does not mean losing the run. With built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint."

这是一个被低估的工程进步。在传统 Agent 架构里，「长时运行任务」和「可靠性」是矛盾的——运行时间越长，遇到环境故障的概率越高，一旦失败就只能从头再来。Durable Execution 通过 checkpoint/snapshot 机制改变了这个关系：

1. **Snapshot**：Agent 的完整状态（内存上下文 + 工具调用历史 + 中间产物）定期快照到外部存储
2. **Rehydration**：当原容器失败时，可以在新容器中加载最近的 snapshot，从断点恢复执行
3. **状态外化**：状态不再存在于容器内存中，而是存在于 Harness 控制的外部存储里

这个模式类似于数据库的 WAL（Write-Ahead Logging）+ 故障恢复机制，只不过恢复的单位不是数据事务，而是整个 Agent 执行会话。

---

## 四、安全收益：分离即安全

OpenAI 特别强调了分离架构对安全性的贡献。原文指出：

> "Agent systems should be designed assuming prompt-injection and exfiltration attempts. Separating harness and compute helps keep credentials out of environments where model-generated code executes."

这里的核心逻辑是：

**传统架构的问题**：credentials（如 API keys、数据库密码）和 model-generated code 共存于同一容器。如果模型生成了恶意代码（无论是 prompt injection 攻击还是模型自身的「幻觉行为」），credentials 都在同一攻击面上。

**分离架构的优势**：Harness 平面持有所有 credentials，永远不会执行来自模型的代码；只有 Compute 平面执行代码，但它不持有任何 secrets。即使 Compute 平面被攻破，攻击者也无法直接获取 credentials。

这和 Anthropic 的 containment 三层架构（环境层 / 模型层 / 外部内容层）的思路一致——**分离即安全**，不同安全级别的组件物理隔离，攻击链无法横向移动。

---

## 五、与竞品的定位对比

| 维度 | OpenAI Agents SDK | LangChain | Anthropic SDK |
|------|-----------------|-----------|---------------|
| **模型相关性** | 模型原生优化 | 模型无关 | 模型原生优化 |
| **Harness-Compute 分离** | ✅ 原生支持 | ❌ | ❌ |
| **Durable Execution** | ✅ Snapshot/Rehydration | ❌ | 部分（长任务支持）|
| **沙箱多提供商** | ✅ 7家集成 | 需自建 | ❌ |
| **AGENTS.md 集成** | ✅ | ❌ | ✅ Claude Code |
| **多语言** | Python（GA）/ TypeScript（规划中）| 多语言 | Python/TypeScript |

从对比可以看出，OpenAI Agents SDK 这次更新的核心差异化在于 **Durable Execution + 多沙箱提供商 + 模型原生优化** 这三角。模型无关的框架（如 LangChain）在灵活性上有优势，但在模型原生优化面前，这个优势正在被侵蚀——当 OpenAI 的模型和自己的 SDK 形成最佳配合时，选择 LangChain 的代价就变成了「放弃模型原生优化带来的可靠性提升」。

---

## 六、适用场景判断

**适合使用新 Agents SDK 的场景**：
- 需要长时间运行（小时级/天级）的 Agent 任务
- 企业级安全要求（credentials 隔离、合规审计）
- 需要跨云部署（多沙箱提供商支持）
- 从原型到生产的平滑过渡（Manifest 抽象）
- 需要 checkpoint 恢复能力的容错系统

**不太适合的场景**：
- 短期、原子性的 Agent 调用（几秒钟内完成）
- 需要完全控制沙箱基础设施的企业（更喜欢自建）
- 对模型选择有严格要求的场景（Agents SDK 偏向 OpenAI 模型优化）

---

## 七、笔者的核心判断

OpenAI Agents SDK 这次的更新方向是对的。**Harness-Compute 分离不是一个功能特性，而是一个架构范式转移**——它把 Agent 工程从「如何让模型更聪明」拉回到「如何让 Agent 系统更可靠」。

过去一年行业花了很多精力在模型能力上（reasoning、long context、multi-modal），但 Agent 工程的核心瓶颈从来不只是模型——而是**运行时可靠性**。Durable Execution 解决的就是这个问题。

笔者认为，这个方向会很快被其他框架跟进。LangChain 的 agents 已经有了 `Memory` 概念，Anthropic 的 Claude Agent SDK 也有长任务支持，但目前都没有把「状态外化 + checkpoint 恢复」做成原生特性。这个差距会在接下来的版本更新中显现。

---

## 参考来源

1. [The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) — OpenAI 官方博客
2. [Sandbox Agents | OpenAI API](https://developers.openai.com/api/docs/guides/agents/sandboxes) — OpenAI 开发者文档
3. [Community Discussion: The next evolution of the Agents SDK](https://community.openai.com/t/the-next-evolution-of-the-agents-sdk/1379072) — OpenAI 开发者社区讨论