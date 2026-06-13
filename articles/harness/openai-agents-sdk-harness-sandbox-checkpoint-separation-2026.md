# OpenAI Agents SDK：用 Harness 思维重新定义 Agent 执行边界

> 原文：[The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)（2026-04-15）
> 标签：`harness` `orchestration` `sandbox` `checkpoint`

---

## 核心命题

OpenAI 最新的 Agents SDK 没有在模型层做文章，而是在**执行基础设施层**做了一次正本清源：把 Harness（控制层）、Compute（计算层）和 Agent State（持久化层）彻底解耦，让 Agent 从「在进程中跑一段代码」变成「在独立沙箱中跑一个可恢复的工作单元」。

这不是功能升级，这是**架构范式转移**。

---

## 一、为什么现有框架都在妥协

OpenAI 在官方文章里说了一句大实话：现有 Agent 系统存在三个层次的 trade-off：

| 框架类型 | 优势 | 问题 |
|---------|------|------|
| **Model-agnostic 框架**（LangChain 等）| 灵活，不绑定模型 | 无法充分利用前沿模型能力 |
| **Model-provider SDK**（官方 SDK）| 模型感知强 | 对 Harness 缺乏可见性，难以调试 |
| **Managed Agent API**（云服务）| 部署简单 | 约束 Agent 运行位置和数据访问方式 |

这三个角的困境，本质上是**把 Harness、Compute、State 混在一起**导致的。Harness 负责控制流，Compute 负责执行，State 负责记忆——当它们纠缠在一个进程里，扩展性、安全性和可靠性都会碰壁。

---

## 二、新 Harness 的三个核心能力

### 2.1 可配置内存（Configurable Memory）

传统 Agent 的内存是「上下文窗口」，是一个被动容器。新 SDK 的内存是**可配置的 Harness 组件**——你可以决定 Agent 在什么粒度上保留记忆、以什么形式持久化、在什么时机清理。

> "The Agents SDK harness becomes more capable for agents that work with documents, files, and systems. It now has configurable memory." — OpenAI

这意味着 Agent 的「记忆」不再是黑盒，而是一个**可编程的 Harness 层**。

### 2.2 Sandbox-aware Orchestration

Agent 不再直接操作主机文件系统，而是通过 Harness 层与沙箱交互。Harness 负责：
- 挂载本地文件到沙箱
- 定义输出目录
- 从 S3/GCS/Azure Blob/R2 拉取数据
- 给 Agent 一个**可预期的 workspace**：输入在哪里、输出写哪里、如何在长时任务中保持工作组织

### 2.3 Codex-like 文件系统工具

新 SDK 引入了一组与 Codex（OpenAI 内部使用的编码 Agent）同级的工具：
- `shell`：代码执行
- `apply patch`：文件编辑
- 工具使用通过 MCP 协议
- Skill 通过 [agentskills.io](https://agentskills.io) 的 progressive disclosure

---

## 三、Sandbox 执行：让 Agent 在隔离环境中工作

这是最关键的工程突破。

**核心设计原则**：Agent 系统应该假设存在 prompt injection 和数据泄露风险。分离 Harness 和 Compute：

1. **安全隔离**：凭据不进入模型生成代码执行的环境
2. **持久化执行**：Agent 状态外部化后，即使沙箱容器丢失也不丢失运行记录
3. **快照与恢复**（Snapshotting & Rehydration）：内置 checkpoint，原始环境失败或过期时可在新容器恢复

> "Separating harness and compute helps keep credentials out of environments where model-generated code executes. When the agent's state is externalized, losing a sandbox container does not mean losing the run." — OpenAI

### 沙箱提供商支持

内置支持：Blaxel、Cloudflare、Daytona、E2B、Modal、Runloop、Vercel

同时引入了 **Manifest abstraction**——用声明式方式描述 Agent workspace，让环境在提供商之间可移植。

---

## 四、架构解耦的工程含义

Harness 和 Compute 的分离，对 Agent 工程实践意味着：

| 能力 | 传统架构 | 新架构 |
|------|---------|--------|
| **故障恢复** | 进程崩溃 = 任务失败 | Checkpoint 恢复，继续从断点执行 |
| **水平扩展** | 单进程单 Agent | 按需创建多个沙箱，并行跑 subagent |
| **安全边界** | 凭据和代码混在同环境 | 凭据在 Harness 侧，代码在 Compute 侧 |
| **多租户** | 共享环境隔离困难 | 每个 Agent 跑独立沙箱，天然租户隔离 |

---

## 五、笔者的判断

**OpenAI 这次做对了一件核心的事**：把 Agent 当作一个**工作单元**而不是一段**代码**。

工作单元的特点：
- 有明确的输入输出
- 有可预期的生命周期
- 可以被暂停、恢复、并行
- 在隔离环境中执行

当 Agent 从代码变成工作单元，围绕它的工程实践（监控、恢复、安全、扩展）才能真正落地。这才是 Agents SDK 最值得关注的演进方向——不是又多了几个工具，而是**把 Agent 的工程模型重新定义了一遍**。

当然，Python 先发、TypeScript 稍后、多提供商支持还在扩展中——这些是早期状态，不影响方向的正确性。

---

## 关联项目

- [omnigent-ai/omnigent：跨平台 Meta-Harness，让 Claude Code / Codex / Pi 共享防护层](/articles/projects/omnigent-ai-omnigent-meta-harness-cross-platform-2026.md)

---

*来源：[OpenAI Agents SDK 官方更新](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)*