# Using Git with Coding Agents

> **来源**: [Simon Willison — Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/using-git-with-coding-agents/)
> **发布时间**: 2026-03-21
> **标签**: #coding-agents #git #agentic-engineering

---

## 核心洞察

Coding Agent 都深度理解 Git 概念。这使得我们可以更充分地利用 Git 的全部能力，而不必亲自记住每一个命令细节。

**关键前提**: 将代码置于版本控制之下，让 Agent 能够记录变更历史、追踪进度、调查和回滚错误。

---

## 核心操作与提示词模板

### 初始化仓库

```
Start a new Git repo here
```

→ 将当前目录转换为 Git 仓库（执行 `git init`）

---

### 提交变更

```
Commit these changes
```

→ 创建新提交记录变更（执行 `git commit -m "message"`）

---

### 添加远程仓库

```
Add username/repo as a github remote
```

→ 配置 GitHub 远程仓库（需先在 github.com/new 创建仓库）

---

### 审查当日变更

```
Review changes made today
```

或 "recent changes" / "last three commits"。这是开启新的 Coding Agent 对话时非常有价值的起点。

---

### 切换分支

```
Create a branch for this experiment
```

→ 创建实验分支，完成后可通过 PR 合并回主分支

---

### 增量工作的检查点模式

Git 的 commit 历史对于 Coding Agent 来说是**免费且无网络延迟**的。Agent 可以在工作过程中频繁创建检查点，无需担心网络流量：

```
Commit a checkpoint of my progress so far
```

这个模式使得长时间运行的复杂任务可以安全地分阶段进行，而不必担心灾难性回退。

---

## 工程模式：Ralph Loop 中的 Git

[Ralph Loop](https://ghuntley.com/loop/) 是一种在多轮对话中保持 Agent 上下文清洁的模式。通过结合 Git：

1. 每轮结束时 Agent 创建 commit
2. 下一轮以干净上下文启动，但通过 Git 历史恢复状态
3. 这使得 Agent 可以跨越多个上下文窗口完成长时任务

---

## 关键设计原则

| 原则 | 说明 |
|------|------|
| **Commit as Checkpoint** | 将 commit 视为工作检查点，而非仅是"完成"标记 |
| **Branch for Experiments** | 用分支隔离实验性工作，避免污染主分支 |
| **History is Free** | Git 历史查询对 Agent 没有额外网络成本 |
| **Review Before Restart** | 开始新会话时先看历史，快速恢复上下文 |

---

## 与 AGENTS.md 的协同

> 参见: [AGENTS.md 作为 Context Engineering 工具](https://simonwillison.net/guides/agentic-engineering-patterns/using-git-with-coding-agents/)

结合 `AGENTS.md` 文件，团队可以为 Coding Agent 定义：
- 代码风格规范
- Commit message 格式要求
- 分支命名约定
- 必须通过的检查步骤（linter、test）

---

## 相关阅读

- [What is agentic engineering?](https://simonwillison.net/guides/agentic-engineering-patterns/what-is-agentic-engineering/) — Simon Willison
- [How coding agents work](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/) — Simon Willison
- [Agent Patterns](../patterns/) — 仓库中的 Agent 设计模式集合
