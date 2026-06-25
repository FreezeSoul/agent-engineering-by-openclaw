# Cursor Cloud Subagents：云端 VM 隔离的 Agent Harness 新范式

> **核心论点**：Cursor 的 Cloud Subagents 不是「把本地 Agent 搬到云上」这么简单——它实现了一种全新的 Harness 架构：**环境快照化 + VM 级隔离 + 跨 session 状态持久化**，让 Agent 可以在长周期任务中真正脱离本地资源约束，同时保持工作区状态的干净交接。这解决了 AI Coding 领域长期存在的一个核心工程矛盾：本地算力不足 vs 云端状态丢失。

---

## 背景：本地 Agent 的「算力困境」

2026 年的 AI Coding Agent 已经能够处理超长周期的复杂任务——从零搭建微服务架构、迭代式重构遗留代码库、持续优化性能瓶颈。然而，这些任务的执行时间和资源需求与本地开发环境形成了根本性冲突：

- **长任务打断工作流**：一个需要 2 小时代码生成的 Agent 任务，会让开发者的 IDE 完全冻结
- **本地资源竞争**：Agent 大量消耗 CPU/内存，导致开发者无法同时做其他工作
- **状态丢失风险**：本地 session 崩溃、机器重启 → 所有中间进度归零
- **并行能力受限**：一个本地 Agent 实例 = 一份本地资源，无法真正并行

Cursor Cloud Subagents 的回答是：**把 Agent 的执行环境和你的本地环境完全解耦**。

---

## 核心机制拆解

### 1. `/in-cloud`：独立 VM 上的云端 Agent

```bash
/in-cloud
```

这条命令在云端的新 VM 上启动一个独立的 Cursor Agent 实例：

- **隔离的 VM**：Agent 运行在完全独立的虚拟机上，不占用本地 CPU/内存
- **独立的 Branch**：所有代码变更在独立 Git branch 上工作，不污染主分支
- **本地工作区干净**：开发者本地 IDE 保持实时响应，可以继续工作

这解决了长任务与本地工作流的根本矛盾。**本地只是「驾驶舱」，真正的 Agent 工作在云端**。

### 2. 环境快照：跨 Session 的状态持久化

> "Your environment is captured in a reusable snapshot, so future cloud agents start up faster with the ability to test changes by running your software."

这是整个设计中最关键的一句话。Cursor 的 Cloud Agent 不是每次从头初始化，而是：

**快照 → 恢复 → 迭代 → 再快照**

```
Cloud Agent Session 1
  → 安装依赖（耗时 8 分钟）
  → 快照保存环境状态（.cursor/environment.json）
  → 完成部分任务
  
Cloud Agent Session 2（同一任务或新任务）
  → 从快照恢复（无需重新安装依赖）
  → 继续工作
```

这解决了 Agent 长任务的核心工程问题：**如何让第二个 Agent 承接第一个 Agent 的工作区状态，而不是从头开始**？快照化是最直接的答案——把工作区当「游戏存档」。

团队级别的 `.cursor/environment.json` 则是快照的共享版本：团队成员可以复用同一套云端环境配置，让整个团队的 Agent 行为更加一致。

### 3. `/babysit PR`：后台迭代式任务执行

```
/babysit
```

这是另一个关键创新。`/babysit` 让云端 Agent 在后台持续迭代一个 PR，直到满足合并条件：

- Agent 在云端后台运行，不占用本地任何资源
- 定期在 PR 下评论汇报进度
- 开发者随时可以 `pull` 下来本地测试
- 不满意可以直接打断，本地继续修改

这相当于给每个 PR 配备了一个**不知疲倦的 24/7 审查者和优化者**。

### 4. Handoff：本地与云端的双向迁移

Cursor 还支持**在任务中途**把 Agent session 从本地迁移到云端（`/in-cloud`），或从云端拉回本地：

- 本地任务跑了一半 → 迁移到云端继续 → 本地解放出来做其他事
- 云端任务遇到需要本地调试的问题 → 拉回本地处理 → 再推回云端

这打破了「本地 vs 云端」的非此即彼，是一个**持续性混合执行模型**。

---

## 工程意义：从 Ephemeral 到 Stateful 的范式转变

Cursor Cloud Subagents 的架构意义需要放在更大的背景下理解。

2025-2026 年的主流 Agent 框架（LangGraph、CrewAI、AutoGen）大多数采用 **Ephemeral Session 模型**：每次 Agent 运行是一个新 context，session 结束状态丢失。这种设计对短任务友好，但无法处理真正的长周期工程任务。

Cursor 的 Cloud Subagents 代表了一种新的方向：**Stateful Harness**：

| 维度 | Ephemeral Agent（传统） | Stateful Harness（Cursor） |
|------|------------------------|--------------------------|
| **Session 持久化** | ❌ 每次新建 | ✅ 快照恢复 |
| **执行环境** | 本地进程 | 云端 VM 隔离 |
| **资源竞争** | 与开发者争夺 | 完全独立 |
| **任务中断** | 丢失所有进度 | 可继续、可交接 |
| **并行能力** | 受本地资源限制 | 云端无限水平扩展 |

笔者认为，这种 Stateful Harness 是 2026 年 AI Coding 从「辅助工具」走向「自主工程师」的关键工程支撑。如果 Agent 无法保持长周期的工作区状态，就永远只能做「一次性任务」；只有状态可以持久化，Agent 才能真正像一个工程师一样——持续迭代、接手他人工作、在长周期项目中保持上下文。

---

## 与现有 Harness 方案的对比

这不是 Cursor 独有的方向，但 Cursor 的实现有独特的工程选择：

| 方案 | 状态持久化方式 | 隔离级别 | 适用场景 |
|------|--------------|---------|---------|
| **Cursor Cloud Subagents** | 环境快照 + VM 隔离 | VM 级 | 长周期 Coding 任务 |
| **Claude Code Remote** | 远程 SSH Session | 进程级 | 已有服务器环境 |
| **GitHub Copilot Workspace** | 云端 Session 保持 | Session 级 | 快速原型 |
| **OpenAI Codex (Long Running)** | Workspace Artifact | Artifact 级 | 代码生成任务 |

Cursor 的差异化在于：**快照化 + VM 隔离 + babysit 迭代** 三者的组合，是目前最完整的云端 Agent Harness 工程方案。

---

## 适用场景与局限性

**适用**：
- 超长周期的代码重构或架构迁移任务
- 需要并行执行多个 Agent 任务的复杂项目
- CI/CD 流程优化、Bug 修复等多分支并行工作
- 团队需要统一 Agent 执行环境的企业场景

**局限性**：
- 需要 Cursor 3.7+ 订阅（Cloud Agent 为付费功能）
- 依赖 Cursor 的云端基础设施，无法自托管
- 环境快照的版本管理和生命周期管理尚未成熟

---

## 一句话结论

Cursor Cloud Subagents 解决的不是「把 Agent 放云端」这个表象问题，而是**如何在云端实现一个有状态的、可持续迭代的、能够跨 session 保持上下文的长周期 Agent 执行引擎**——这是 AI Coding Agent 从「辅助工具」进化为「自主工程师」的必经工程路径。

> 📌 **引用来源**：本文技术细节来自 [Cursor 官方 Changelog - Cloud Environment Setup and Cloud Subagents in Agents Window](https://cursor.com/changelog/cloud-in-agents-window)（2026-06-22），以及 [Cursor 官方 Changelog - Customize Page](https://cursor.com/changelog/customize)（2026-06-26）。

---

**Cluster**: `harness`  
**Tags**: `cursor`, `cloud-agent`, `harness`, `vm-isolation`, `environment-snapshot`, `stateful-agent`, `2026`  
**首次产出**: R538  
