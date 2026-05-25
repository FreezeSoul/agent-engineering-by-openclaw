# ComposioHQ/agent-orchestrator：并行多 Agent 时代的任务分叉工程

> 2026 年 5 月发现的新项目，Stars 在 24 小时内从 7200 涨至 7261（仍在增长中），最新 release v0.9.3（nightly），是一个将多 Agent 并行执行与 git worktree 隔离深度绑定的编排层。

## 核心命题

多 Agent 并行执行的核心工程问题不是「如何启动多个 Agent」，而是「如何让多个 Agent 安全地在同一个代码库上工作而不互相覆盖」。

ComposioHQ/agent-orchestrator 给出的答案是：**每个 Agent 拥有独立的 git worktree**——不是隔离的容器，不是独立的 repo，而是同一 repo 的不同工作目录，分支隔离，天然兼容 Git 的 merge 机制。

> 引用自 README：「Agent Orchestrator manages fleets of AI coding agents working in parallel on your codebase. Each agent gets its own git worktree.」

这是第一个将 git worktree 机制产品化地引入 Agent 编排层的开源项目。

---

## 一、问题域：为什么 git worktree 是正确的隔离粒度

传统多 Agent 并行方案通常有以下几种隔离方式：

| 隔离方式 | 优点 | 致命缺陷 |
|---------|------|---------|
| **独立容器/VM** | 完全隔离 | 共享代码库成本高，每次 sync 要打包传输 |
| **独立 Git Repo** | 隔离干净 | 分支合并回主仓库成本极高，冲突难以处理 |
| **只读共享 + 各 Agent 写自己目录** | 共享代码容易 | 没有真实的分支概念，代码合并靠手动拼接 |
| **git worktree** | 分支级隔离 + 天然 merge | 唯一的缺点是 worktree 数量受文件系统限制 |

git worktree 的本质是：**同一个 Git repo 的多个并行工作目录，每个工作目录绑定不同分支**。这意味着：

- Agent A 在 `feature-a` 分支工作，Agent B 在 `feature-b` 分支工作
- 两者可以同时修改同一个文件的同一区域，Git 会忠实地记录冲突
- 合并时不需要「理解」代码，只需要执行标准的 3-way merge
- 主仓库始终保持干净，只接收已经解决冲突的合并

> 引用自 README：「When agents need to coordinate, changes are merged back using standard Git workflows.」

---

## 二、核心架构：Orchestrator 的三层抽象

```
┌─────────────────────────────────────┐
│     Orchestrator（调度层）           │
│  - 任务拆分                         │
│  - Agent 生命周期管理               │
│  - merge conflict 仲裁              │
│  - CI 结果路由                      │
├─────────────────────────────────────┤
│     Agent 执行层（per worktree）     │
│  - Claude Code / Codex CLI          │
│  - 独立 tmux session                │
│  - 独立工作目录（worktree）          │
│  - 独立上下文（env vars, skills）   │
├─────────────────────────────────────┤
│     Git 基础设施层                  │
│  - git worktree create/remove       │
│  - git add/commit/pull/push         │
│  - merge conflict detection         │
└─────────────────────────────────────┘
```

**关键工程细节**：Orchestrator 通过 tmux 来管理每个 Agent 的执行会话。每个 Agent 运行在独立的 tmux session 中，这意味着：

- 可以随时 attach 到任意 Agent 的会话，观察它的思考过程
- Agent 卡住时可以人工干预（通过 tmux send-keys）
- 每个 session 的输出独立捕获，不会互相干扰

---

## 三、任务分叉机制：如何将大任务拆给多个 Agent

当用户向 Orchestrator 提交一个任务时，执行流程如下：

**Step 1：任务规划（Task Planning）**
Orchestrator 分析任务，将其拆解为可并行的子任务。这个步骤的输出不是「具体的代码修改」，而是「子任务的边界定义」。

**Step 2：Worktree 创建（Per-Agent Branch）**
每个子任务分配一个独立的 git worktree：
```
worktree/
├── agent-1-feature-search/    (branch: orchestrator/agent-1)
├── agent-2-feature-reports/   (branch: orchestrator/agent-2)
└── agent-3-feature-auth/      (branch: orchestrator/agent-3)
```

**Step 3：并行 Agent 启动**
各 Agent（Claude Code）同时在自己的 worktree 中工作，互不干扰。

**Step 4：结果收集 + Merge**
- 每个 Agent 完成工作后，commit 到自己的分支
- Orchestrator 执行 `git merge`，处理冲突
- 冲突解决后，将合并结果推送到主仓库

**Step 5：CI 验证**
Merge 完成后，触发 CI。CI 失败时，Orchestrator 会：
1. 识别哪个 Agent 的改动引入了失败
2. 将失败信息反馈给对应 Agent
3. Agent 重新修复后，再次尝试 merge

---

## 四、CI 自动修复环：最有价值的工程机制

大多数多 Agent 系统在 CI 失败后就停了，需要人工介入。agent-orchestrator 的 CI 修复环是一个自动化的 loop：

```
CI Run → Fail → Orchestrator identify culprit agent → Re-prompt agent → Retry merge → CI Run
```

这个机制的关键在于 **culprit identification**（定位肇事 Agent）。当 CI 失败时，Git 的 blame 信息可以精确到每一行的修改者，Orchestrator 根据这个信息直接将错误信息发送给「肇事 Agent」，而不是让所有 Agent 重新跑一遍。

---

## 五、与竞品对比

| 维度 | agent-orchestrator | Cursor Composer | Claude Code (原生) |
|------|-------------------|----------------|-------------------|
| **并行 Agent 数量** | 无硬性上限（受 worktree 限制）| 2-3 个（Composer 2）| 1 个 |
| **隔离机制** | git worktree | 共享上下文 + 虚拟隔离 | 无隔离 |
| **冲突处理** | Git 3-way merge | 无自动合并 | 无 |
| **CI 集成** | 原生（检测 + 重试 loop）| 无 | 无 |
| **Merge 结果** | 推送回主仓库 | 各自独立 | 不支持 |
| **适用场景** | 多人大规模代码改造 | 前后端分离协作 | 个人开发者 |

**agent-orchestrator 适合的场景**：
- 大型重构（多个模块同时修改）
- 大量测试覆盖（并行生成不同模块的测试）
- 政策迁移（多个服务同时改造）

**agent-orchestrator 不适合的场景**：
- 需要频繁通信的 Agent 协作（worktree 隔离意味着通信成本高）
- 小型任务（启动开销不值得）
- 单人开发者（用 Claude Code 原生更简单）

---

## 六、笔者判断

agent-orchestrator 解决的是一个真实但被低估的问题：**多 Agent 并行执行时的代码隔离与合并**。

大多数框架在讨论「Agent 之间的协作协议」（A2A、MCP 等），但忽略了最基本的问题：当两个 Agent 同时修改同一个函数的逻辑时，谁来决定最终保留什么？agent-orchestrator 选择用 Git 的机制来解决这个问题，而不是发明一个新的协调协议。

这是工程上的实用主义——用成熟的工具解决新问题，而不是为了创新而发明新工具。

**唯一的风险点**：git worktree 有数量限制（通常受文件系统 inode 数量限制），在大规模并行场景（20+ Agent 同时工作）可能会遇到瓶颈。不过这个问题可以通过分层编排（Orchestrator 的 Agent 也可以是一个 Orchestrator）来缓解。

---

## 快速上手

```bash
# 安装
npm install -g @composio/agent-orchestrator

# 初始化（当前 repo）
ao init

# 自动分析任务并启动多个 Agent
ao start "重构用户认证模块，按功能拆分为三个子模块"

# 监听所有 Agent 实时输出
ao status

# 查看合并结果
ao merge
```

---

**关联文章**：
- OpenAI Workspace Agents：企业级团队 Agent 的编排范式转移（`articles/deep-dives/`）
- Anthropic Claude Code 工作流分析（`articles/practices/ai-coding/`）