# OpenAI Agents SDK：Harness 与 Compute 分离的工程机制

> 本文解读 OpenAI 于 2026 年 4 月发布的 Agents SDK 更新，聚焦于其**将 Harness 从 Compute 中分离**的核心工程机制设计，以及这背后的安全、耐久性和规模化逻辑。
>
> **核心论点**：Agent 的可靠性不只取决于模型能力，更取决于 Harness 的工程质量——OpenAI 新版 SDK 通过 checkpoint/snapshot-rehydration + sandbox isolation + Manifest 抽象，给出了一种可复用的 Harness 工程框架。

---

## 一、问题：Harness 为什么需要与 Compute 分离

在深入 OpenAI 的方案之前，先理解为什么这个问题值得关注。

传统 Agent 架构中，Harness（工具、内存、文件系统、指令）和 Compute（模型执行环境）往往紧耦合：

- Agent 的凭证直接放在执行环境中
- Sandbox 容器崩溃 = Agent 状态丢失
- 扩展只能在同一个容器内进行，无法并行或隔离子任务

OpenAI 在博客中直指这个问题的本质：

> *"Agent systems should be designed assuming prompt-injection and exfiltration attempts. Separating harness and compute helps keep credentials out of environments where model-generated code executes."*

这层逻辑是：**当模型生成的代码可能在 sandbox 内执行时，任何在 sandbox 内的凭证都是潜在攻击面**。

---

## 二、OpenAI 的解法：三层工程机制

### 2.1 Checkpoint / Snapshot / Rehydration

新版 Agents SDK 的核心 durable execution 机制：

```python
result = await Runner.run(
    agent,
    "Compare FY2025 revenue with FY2024.",
    run_config=RunConfig(
        sandbox=SandboxRunConfig(client=UnixLocalSandboxClient()),
    ),
)
```

背后是**自动状态快照与恢复能力**：当 sandbox 容器失败或过期时，Agent 的状态（内存、文件系统、执行进度）可以从上一次 checkpoint 恢复，在新容器中继续执行，而不是从头开始。

官方原文描述：

> *"built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint"*

**工程意义**：这解决了"长任务不可中断"的工程难题——6 小时的任务中途失败，不再需要人类重试，Agent 自己能从断点恢复。

### 2.2 Sandbox-Aware Orchestration

新版 SDK 的 Orchestration 层是 **sandbox-aware** 的，即编排层理解 sandbox 的边界和状态，可以：

- 按需调用 sandbox（不是一直开着）
- 将子任务路由到隔离的 sandbox
- 并行跨容器执行以加速

```python
# 子任务路由到独立 sandbox
run_config=SandboxRunConfig(client=UnixLocalSandboxClient())
```

官方描述的 primitives 包括：
- **Tool use via MCP**（Model Context Protocol）
- **Progressive disclosure via Skills**（`agentskills.io`）
- **Custom instructions via AGENTS.md**（`agents.md`）
- **Code execution via shell tool**
- **File edits via apply-patch tool**

这些都是 **Harness Components**，在 OpenAI 的定义中，每个组件的存在都是因为"模型自己做不了这件事"——随着模型能力提升，这些假设会逐步失效，这是理解 Harness 设计原则的关键。

### 2.3 Manifest 抽象：可移植的工作区描述

OpenAI 引入了 `Manifest` 抽象来描述 Agent 的工作区：

```python
agent = SandboxAgent(
    name="Dataroom Analyst",
    model="gpt-5.4",
    instructions="Answer using only files in data/. Cite source filenames.",
    default_manifest=Manifest(entries={"data": LocalDir(src=dataroom)}),
)
```

支持的挂载类型包括：
- 本地文件目录（`LocalDir`）
- AWS S3 / Google Cloud Storage / Azure Blob / Cloudflare R2
- 定义输出目录
- 多 provider 的 sandbox 环境（Blaxel, Cloudflare, Daytona, E2B, Modal, Runloop, Vercel）

**工程意义**：`Manifest` 将"工作区长什么样"从代码中抽离成可移植的声明式配置，使得从本地原型到生产部署的环境迁移变得可复现，也使得模型有一个**可预期的工作区**：输入在哪里、输出写哪里、长任务如何保持组织。

---

## 三、为什么这是重要的工程框架

### 3.1 安全性：凭证不在执行域

传统的 Agent 构建模式中，很多开发者会把 API Key、云服务凭证放在 Agent 的执行环境里。如果模型生成的代码被攻击者控制（比如通过 prompt injection），这些凭证就成了攻击面。

分离后：
- **Harness**（工具定义、指令、凭证配置）在控制平面
- **Compute**（模型执行、Sandbox 代码运行）在隔离环境
- 即使 Sandbox 被攻破，攻击者拿不到 Harness 层的凭证

### 3.2 耐久性：checkpoint 不是重试，是连续

Checkpoint/Recovery 机制的本质不是"失败了重来"，而是"让 Agent 的工作流在时间上连续"。这对于需要数小时甚至数天的任务至关重要。

这一点与 Anthropic 的 building-c-compiler 实验形成有趣的对比：Anthropic 用 Git-based 去中心化同步（锁文件 + merge）来协调多 Agent 之间的状态，而 OpenAI 用 checkpoint/snapshot 来处理单个 Agent 在时间维度上的状态连续性。**两者解决的是同一个底层问题（状态一致性）的不同侧面**。

### 3.3 规模化：按需调用 + 隔离并行

Sandbox-aware orchestration 意味着 Agent 可以：

- 激活时调用 sandbox（而不是常驻）
- 不同子任务路由到不同容器（隔离性）
- 多个容器并行执行（吞吐率提升）

这对企业级 Agent 应用至关重要。

---

## 四、与其他 Harness 方案的对比

| 维度 | OpenAI Agents SDK | Anthropic Claude Agent SDK | Google ADK |
|------|------------------|--------------------------|------------|
| **Checkpoint 机制** | Snapshot + Rehydration | Initializer Agent 初始化 | 子 Agent 独立状态 |
| **Sandbox 支持** | 多 provider 原生集成 | 代码执行环境 | 各自集成 |
| **Manifest 抽象** | ✅（跨 provider 可移植）| ❌ | ❌ |
| **凭证分离** | ✅（Harness/Compute 分离）| 依赖平台层 | 依赖云平台 |
| **并行 Orchestration** | ✅（sandbox-aware）| ❌ | ✅ |
| **MCP 支持** | ✅ | ✅ | ✅ |
| **语言** | Python（TypeScript 规划中）| TypeScript + Python | Python |

---

## 五、这对 Agent 开发者意味着什么

**第一层**：理解"每个 Harness 组件都是因为模型做不了某件事"这个设计哲学。当你设计一个工具或 Memory 系统时，问自己：这个组件的假设会在模型能力提升后失效吗？如果会，它就是临时的 Harness 组件。

**第二层**：生产级 Agent 需要安全、耐久、可扩展的 Harness，而不是单次运行的概念验证。OpenAI 给出的方案（checkpoint + sandbox isolation + Manifest）是当前最完整的参考实现。

**第三层**：Harness Engineering 是一个独立的工程学科，不是模型能力的附庸。Martin Fowler 将其定义为三种交互系统的交集：Context Engineering（给 Agent 提供什么上下文）、Architectural Constraints（确定性测试和结构化约束）、Entropy Management（定期修复文档漂移的 Agent）。OpenAI 的这次更新是这个学科成形过程中的一个重要里程碑。

---

## 六、引用来源

> "Separating harness and compute helps keep credentials out of environments where model-generated code executes."
> — [The next evolution of the Agents SDK | OpenAI](https://openai.com/index/the-next-evolution-of-the-agents-sdk), April 15, 2026

> "built-in snapshotting and rehydration, the Agents SDK can restore the agent's state in a fresh container and continue from the last checkpoint"
> — [The next evolution of the Agents SDK | OpenAI](https://openai.com/index/the-next-evolution-of-the-agents-sdk), April 15, 2026

> "Developers need more than the best models to build useful agents—they need systems that support how agents inspect files, run commands, write code, and keep working across many steps."
> — [The next evolution of the Agents SDK | OpenAI](https://openai.com/index/the-next-evolution-of-the-agents-sdk), April 15, 2026

---

## 相关阅读

- [Anthropic: Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Building a C Compiler with Parallel Agents](https://www.anthropic.com/engineering/building-c-compiler)（Git-based 去中心化同步机制，对比见本文第四节）
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)