# Cursor 3：多 Agent 并行执行与跨仓库工作区架构

## 核心命题

Cursor 3 引入的多 Agent 并行执行（`/multitask`）、工作树隔离（Worktrees）和多根工作区（Multi-root Workspaces）构成了 AI Coding 领域首次规模化落地的**多 Agent 协作工程架构**——不是玩具式的单 Agent 问答，而是真正能让多个子 Agent 同时处理不同分支、不同仓库的并行工业级方案。

> 原文：「With /multitask, Cursor will run async subagents to parallelize your requests instead of adding them to the queue. It will also break down larger tasks into smaller chunks for a fleet of async subagents to tackle simultaneously.」
> — Cursor Changelog, 2026-04-24

## 一、为什么这不是普通的 UI 更新

Cursor 3 之前，所有 AI Coding 工具（包括 Claude Code）本质上都是**单一 Agent 执行模式**：用户发一条指令，Agent 串行处理，等完成再处理下一条。即便是所谓的 "subagent" 支持，也只是让一个主 Agent 调用另一个 Agent，本质上还是串行的。

Cursor 3 的 `/multitask` 则不同：

- **真正的并行**：多个 async subagent 同时运行，不是队列
- **任务分解**：一个大任务自动拆分成多个小块，分给并行的 subagent fleet
- **结果合并**：各自完成后再合并结果

这意味着 Cursor 3 从底层重新设计了 Agent 执行模型，从「单 Agent 串行」演进到「多 Agent 并行」。

## 二、三层架构拆解

### 2.1 `/multitask`：任务分解与并行执行层

`/multitask` 的核心能力不是「并发执行」那么简单，而是**任务自动分解**：

```
用户请求（复杂任务）
    ↓
任务分解引擎（/multitask）
    ↓
┌─────────┬─────────┬─────────┐
│Subagent │Subagent │Subagent │  ← 并行执行，独立线程
│  Task 1 │  Task 2 │  Task 3 │
└─────────┴─────────┴─────────┘
    ↓         ↓         ↓
结果队列 → 主 Agent 合并 → 用户
```

关键工程挑战：
- **任务粒度怎么定**：太大则并行度不够，太小则调度开销大
- **依赖关系怎么处理**：Task 2 依赖 Task 1 的输出怎么办
- **冲突检测**：多个 subagent 同时修改同一文件怎么办

Cursor 选择了「信任主 Agent」的方案：分解和合并都由主 Agent 负责，subagent 只负责执行独立任务。

### 2.2 Worktrees：分支隔离的工程基础

Git Worktree 允许同一个仓库的多个分支同时存在于文件系统的不同目录。Cursor 将这个能力引入 Agent 执行：

```
main repo:   /project
worktree 1:  /project-feature-a  (feature-branch)
worktree 2:  /project-feature-b  (refactor-branch)
```

每个 worktree 有独立的 Git 分支，意味着：
- **子 Agent 修改不会污染主分支**：在隔离环境中运行
- **上下文切换零成本**：不需要 `git stash` / `git checkout`
- **测试简单**：完成后一键将分支移回主目录

> 原文：「Run isolated tasks in the background across different branches. When you're ready to test changes, move any branch into your local foreground with one click.」

### 2.3 Multi-root Workspaces：真正的跨仓库协作

这是最关键的创新点。传统的多仓库支持需要为每个仓库单独启动一个 Agent session。Cursor 3 的 Multi-root Workspaces 允许：

- **一个 Agent session** 对接**多个文件夹**（跨 frontend/backend/shared libs）
- Agent 可以在仓库之间「穿越」，不需要每次换仓库时重新初始化上下文
- 文件系统的语义对 Agent 保持一致（跨仓库 import、跨仓库 refactor）

```
workspace = {
  "frontend": "./packages/frontend",
  "backend": "./packages/backend", 
  "shared": "./packages/shared"
}
一个 Agent session 同时理解三个仓库的代码
```

## 三、工程机制解析

### 3.1 通信协议：主 Agent ↔ Subagent

Cursor 没有公开这个协议细节，但从行为推断：

- **主 Agent 负责任务分解**：分析用户请求 → 生成子任务 → 分配给 subagent
- **Subagent 独立执行**：每个 subagent 有独立的 context window
- **异步通信**：主 Agent 不阻塞等待 subagent，通过事件队列收集结果
- **结果合并**：主 Agent 等待所有 subagent 完成 → 合并 diff → 呈现给用户

### 3.2 冲突处理

当两个 subagent 同时修改同一文件时，Cursor 的策略是：
- **文件级别锁**：同一文件同一时刻只能有一个 subagent 修改
- **合并冲突提示**：如果确实冲突，主 Agent 会提示用户手动解决

### 3.3 工作区状态管理

每个 worktree 的状态（未提交的修改、branch、HEAD）都是独立的。Agent 在 worktree 中工作产生的状态变更不会影响其他 worktree，也不影响主仓库。

```
# 主仓库状态保持干净
main: feature-x ✅ clean (等待 worktree 结果合并)

# Worktree 独立运行
feature-a: refactor-backend 💥 in-progress
feature-b: add-tests 🟡 in-progress
```

## 四、与 Claude Code Auto Mode 的架构对比

| 维度 | Cursor 3 Multitask | Claude Code Auto Mode |
|------|-------------------|---------------------|
| **并行模式** | 多 subagent 真正并行执行 | 单一 Agent，自动批准 |
| **任务分解** | 主 Agent 自动分解 | 用户定义任务边界 |
| **工作区隔离** | Git worktree 隔离 | 单一工作区 + 沙箱 |
| **跨仓库** | Multi-root 原生支持 | 单仓库模式 |
| **冲突处理** | 文件锁 + 合并提示 | 沙箱边界限制 |
| **适用场景** | 多任务并行、跨仓库协作 | 长周期单任务、自主执行 |

两者代表了两种不同的工程路线：
- **Cursor 路线**：多 Agent 并行 + 任务自动分解 → 适合「有很多事同时要做」
- **Claude Code 路线**：单 Agent 自主执行 + 自动批准 → 适合「一件事做很久不需要人介入」

## 五、为什么这对 Harness 工程重要

多 Agent 并行执行引入了新的 Harness 问题：

### 5.1 评估器循环的粒度变化

传统 Harness 的评估器循环是**单 Agent 级别**的：
```
Agent 执行 → 评估结果 → 决定是否继续 → 循环
```

多 Agent 架构下，评估器需要处理**任务级别**和**子 Agent 级别**两层：
- **任务级别**：整个 `/multitask` 任务的目标达成率
- **子 Agent 级别**：每个 subagent 的执行质量

### 5.2 权限边界的复杂化

当多个 subagent 同时运行时：
- 每个 subagent 的权限需要独立控制
- 权限提升（sudo）需要级联确认
- 跨 subagent 的文件访问需要协调

### 5.3 工作区状态的并发管理

Git worktree 解决了文件系统的隔离问题，但：
- **共享状态**（环境变量、凭证）怎么管理
- **子 Agent 之间的中间结果**怎么传递
- **失败的子 Agent** 怎么回滚不影响其他

## 六、笔者的判断

Cursor 3 的 Multi-root Workspaces 是本轮 AI Coding 战争中最重要的工程突破。它解决了一个根本问题： реальном мире，软件开发不是单仓库的，Agent 需要能够在多个仓库之间协作而不丢失上下文。

但笔者认为这个能力目前还是**工程预览版**：
- 任务分解的质量完全依赖主 Agent 的能力
- 跨仓库的语义理解（比如跨仓库的 TypeScript import）还不够稳定
- 多 subagent 并行时的资源消耗没有明确上限

真正的成熟形态应该是：当用户说「帮我把这些 Bug 都修一下」，Agent 自动理解哪些在哪些仓库、哪些有依赖关系、哪些可以并行，然后自动执行、自动合并。

这不是 Cursor 一家能解决的问题，需要整个行业一起定义「多 Agent 协作的接口协议」。

---

**引用来源**：
- [Cursor Changelog 04-24-26](https://cursor.com/changelog/04-24-26)
- [Cursor 3 Worktrees & Best-of-N](https://cursor.com/blog/cursor-3)（Blog 原文）
- [Git Worktrees 文档](https://git-scm.com/docs/git-worktree)