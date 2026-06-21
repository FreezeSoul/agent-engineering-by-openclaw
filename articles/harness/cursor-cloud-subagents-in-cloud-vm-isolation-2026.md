# Cursor Cloud Subagents：云端 VM 级隔离的 Agent Handoff 新范式

> 本文源自 Cursor Changelog（2026-06-17）：Cloud Environment Setup and Cloud Subagents in Agents Window
>
> 原文摘要：
> - Cursor 可以帮你在云端设置开发环境，耗时不到 10 分钟
> - `/in-cloud` 启动独立 VM + 分支的云端子 Agent
> - 环境快照可复用，未来云端 Agent 启动更快
> - 支持 `/babysit` PR：远程迭代直到 PR 准备好合并
> - 本地与云端之间可双向 Handoff

---

## 一、核心命题

Cursor 的 Cloud Subagents 解决了一个根本问题：**本地 Agent 会阻塞主工作流**。

当你在本地运行一个长时 Agent 任务时，它会占用你的编辑器、终端和注意力。即使是后台运行，本地资源竞争也会影响响应速度。Cursor 的答案是把子任务彻底移出本地——不是"后台运行"，而是**独立的云端 VM + 独立分支**，完全隔离，不占用本地任何资源。

这不只是"云端执行"那么简单。它代表了一种新的 **Agent Handoff 模式**：工作单元不是在进程间传递，而是**在隔离的计算环境间转移**。

---

## 二、技术机制拆解

### 2.1 VM 级隔离：不是容器，是独立机器

Cloud Subagents 的核心是"在独立 VM 中运行"。这比 Docker 容器更进一步——每个子 Agent 有：
- **独立的文件系统视图**（代码分支隔离）
- **独立的网络空间**（不影响本地开发服务器端口）
- **独立的资源配额**（不抢本地 CPU/内存）

这解决了传统 Agent 架构中的一个痛点：多个 Agent 同时运行时的资源竞争和状态污染。当一个 Agent 在跑测试占用端口 3000，另一个 Agent 也在跑测试时，端口冲突几乎是必然的。VM 级隔离从根本上消除了这个问题。

### 2.2 分支级隔离：Git 分支作为工作区边界

每个 Cloud Subagent 运行在**独立的 Git 分支**上。这是一个聪明的设计选择：

```
本地 main 分支
  ├── cloud-subagent-1 → feature/fix-ci → 独立分支
  ├── cloud-subagent-2 → explore/refactor → 独立分支  
  └── cloud-subagent-3 → babysit/pr-123 → 独立分支
```

**为什么用分支而不是目录？** 因为分支有清晰的语义边界：这条分支上所有的变更都服务于这个特定任务。合并时只需要 PR，不需要手动清理文件。而且分支天然支持"放弃这个方向"而不影响主分支。

笔者认为，这是把 **Git 工作流作为 Agent 隔离机制**的最自然实现——不需要额外的状态管理，Git 本身就是分布式协作的事实标准。

### 2.3 环境快照：Checkpoint + Resume 的工程实现

文章中提到：

> "Your environment is captured in a reusable snapshot, so future cloud agents start up faster with the ability to test changes by running your software."

这句话背后是一个完整的 **Checkpoint/Resume 模式**：

1. **Checkpoint**：环境状态（依赖安装、配置、上下文）被序列化为 `.cursor/environment.json`
2. **Resume**：新 Agent 读取快照，无需重新执行初始化步骤，直接从上次状态继续

这与 Anthropic 在 "Harness design for long-running apps" 中描述的 initializer pattern 本质相同：把长时任务拆分为可恢复的工作单元。但 Cursor 的实现更务实——用 Git 分支作为工作区快照，用 `environment.json` 作为运行时状态快照。

**关键细节**：快照被 commit 到 `.cursor/environment.json`，意味着它是**版本化的**。团队成员可以复用同一个环境快照，这解决了"新 Agent冷启动"的问题。

### 2.4 `/babysit` PR：Pull-Request 级别的 Agent 任务封装

`/babysit` 是我认为最有意思的功能设计：

> "The cloud agent will iterate remotely to prepare your PR for merge without tying up the local session."

这不是一个通用 Agent，而是一个**专门化的工作流封装**。它明确地把"让 PR 达到可合并状态"作为任务目标，这意味着：

- Agent 知道何时停止（CI 绿灯 + Review 通过）
- Agent 知道如何验证（运行测试、检查 lint）
- Agent 不会在 PR 已经准备好之后继续"多此一举"

把 Agent 任务封装为**明确的完成标准**，而不是"一直运行直到用户中断"——这是 Harness 设计中的关键原则。Cursor 用 `/babysit` 这个 slash command 把它变成了一个可复用的模式。

---

## 三、Handoff 协议：双向状态迁移

文章中提到了三种 Handoff 场景：

| 场景 | 方向 | 触发条件 |
|------|------|---------|
| Offload | 本地 → 云端 | 本地资源紧张 / 需要并行 / 任务耗时 |
| Pull down | 云端 → 本地 | 云端完成验证 / 需要人工 review |
| Babysit | 云端独立运行 | PR 需要持续迭代直到可合并 |

这三种场景覆盖了 Agent 工作流中最常见的状态迁移需求。关键是**双向性**——Agent 不是单向地"跑在云端"，而是可以在任意时刻在本地和云端之间迁移。

笔者认为，这里的工程难点不在于"如何把 Agent 放到云端"，而在于**如何保证 Handoff 后 Agent 的上下文一致性**。当你把一个 Agent 从本地 pull 到云端时，它的 memory、tool state、pending file changes 如何保持一致？Cursor 选择了用 Git 分支作为事实边界——Handoff 时，变更已经 commit 到分支，云端和本地看到的是同一个 commit 历史。

这个设计把状态一致性问题的复杂度降到了最低：**Git 是天然的分布式状态同步机制**。

---

## 四、与现有架构的关联

### 4.1 与 Anthropic "Managed Agents" 的关联

Anthropic 在 Scaling Managed Agents 中描述了"brain-hands decoupling"模式：把规划/决策（brain）和执行（hands）分离到不同 Agent。Cursor 的 Cloud Subagents 在某种程度上是**同一思想的不同实现路径**：

- Anthropic：通过 IPC 在进程间传递任务
- Cursor：通过 Git 分支在 VM 间传递工作区状态

两者都在解决"如何让多个 Agent 协同而不互相干扰"的问题。Cursor 的方案更依赖基础设施（VM + Git），Anthropic 的方案更依赖 Agent 内部协议。

### 4.2 与 OpenAI "Harness Engineering" 的关联

OpenAI 在 Harness Engineering 中强调了 **sandbox 作为安全边界**的重要性。Cursor 的 VM 级隔离是这个原则的扩展——不只是安全隔离，还包括资源隔离和状态隔离。

---

## 五、工程实践视角

### 适合的场景

- **CI 修复**：在独立分支上跑 CI 调试，不阻塞本地开发
- **代码探索**：探索性重构时不影响本地工作区
- **PR babysitting**：需要多轮 CI + Review 迭代的长任务
- **并行任务**：需要同时处理多个独立任务

### 不适合的场景

- **需要频繁人机交互的任务**：云端 Agent 的反馈循环比本地慢
- **需要访问本地特有资源的任务**：硬件调试、本地数据库等
- **对延迟敏感的任务**：网络延迟会影响 Agent 响应速度

---

## 六、结论

Cursor Cloud Subagents 的核心创新不是"云端运行 Agent"，而是**把 Git 分支作为 Agent 工作区的隔离边界**，配合 VM 级资源隔离和环境快照机制，实现了真正意义上的**无损 Handoff**。

这解决了一个长期困扰 Agent 开发者的难题：如何在不阻塞本地工作流的情况下，让 Agent 完成需要长时间运行的任务。

笔者认为，这个方向的进一步发展可能是：把 Handoff 的粒度从"整个 Agent session"细化到"单个 tool call 的远程执行"——也就是说，不是在本地还是在云端运行 Agent，而是**单个工具调用可以在任意计算环境中执行**。这需要更细粒度的状态序列化和更强的安全边界，但能实现更灵活的资源调度。

---

## 参考来源

- [Cursor Changelog: Cloud Environment Setup and Cloud Subagents in Agents Window](https://cursor.com/changelog/cloud-in-agents-window)（2026-06-17）
- [Anthropic Engineering: Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)
- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)