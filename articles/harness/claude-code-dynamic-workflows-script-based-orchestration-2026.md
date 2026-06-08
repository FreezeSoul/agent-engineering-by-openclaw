# Claude Code 动态工作流：把编排计划写入代码

>2026年6月2日，Anthropic 在 Claude Code 中推出了 Dynamic Workflows 功能。Claude 可以动态编写自己的多 Agent Harness，而且是针对每个任务定制化的。本文深入解析这一特性背后的工程机制。

---

## 核心命题

Claude Code 之前的版本，一个对话就是一个固定的 Harness：Claude 作为单一 Agent，在每次交互中决定下一步做什么。这在大多数场景下是高效的——但当任务需要协调数十个 Agent 时，单一 Agent 的上下文窗口就成了瓶颈。

**Dynamic Workflows 的本质转变**：将"编排计划"从 Claude 的上下文窗口移到 JavaScript 脚本中。脚本控制整个执行流程，Claude 的上下文只承载最终答案，中间结果存在脚本变量里。

>原文："A workflow moves the plan into code. With subagents, skills, and agent teams, Claude is the orchestrator: it decides turn by turn what to spawn or assign next, and every result lands in a context window. A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer."
> — [Claude Code Docs: Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)

---

## 为什么这个转变重要

### 传统多 Agent 编排的困境

在 subagents、skills、agent teams 三种模式下，Claude 都是"逐轮决定下一步"（turn by turn）的 orchestrator：

| 模式 | 谁持有计划 | 中间结果存在哪 | 可扩展性 |
|------|-----------|--------------|---------|
| **Subagents** | Claude（逐轮决定）| Claude 上下文窗口 | 几个任务/轮次 |
| **Skills** | Claude（按 prompt 执行）| Claude 上下文窗口 | 同上 |
| **Agent Teams** | Lead Agent（逐轮决定）| 共享任务列表 | 少数长时运行的 peers |
| **Dynamic Workflows** | **JavaScript 脚本（代码化）** | **脚本变量** | **数十到数百个 Agent/次运行** |

当任务规模扩大时，逐轮决策模式的两个问题暴露出来：

1. **上下文耗尽**：每个 Agent 的结果都塞进主 Agent 的上下文窗口，很快达到 token 上限
2. **不可中断恢复**：中断后只能重启，无法从上次位置继续

### 动态工作流的解决思路

Dynamic Workflows 的设计核心是**计划即代码**（Plan as Code）：

-脚本持有执行循环、分支逻辑、中间结果
- Claude 只负责"写脚本"和"在每个 phase 中充当 Agent"
- 每个 phase 可以并行运行多个 subagent
- phase 之间用脚本变量传递结果，不占用 Claude 上下文

> 原文："Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive."
> — [Claude Code Docs](https://code.claude.com/docs/en/workflows)

---

## 核心技术机制

### 1. 脚本作为 Harness

动态工作流本质上是一个**自定义 Harness 生成器**。用户描述任务，Claude 为该任务动态编写一个 JavaScript Harness脚本。这个脚本包含：

- **Phase 定义**：每个阶段的目标、Agent数量、token 预算
- **Subagent 模板**：Claude 为每个 subagent 生成专门的 system prompt
- **执行控制**：循环、分支、暂停、恢复的逻辑全部在脚本中
- **结果聚合**：各 phase 的结果通过脚本变量汇总

```javascript
// Claude动态生成的 workflow 脚本示例结构
const workflow = {
  phases: [
    { name: 'research', agents: 5, task: 'explore multiple angles' },
    { name: 'cross-check', agents: 3, task: 'verify findings adversarially' },
    { name: 'synthesize', agents: 1, task: 'produce final report' }
  ],
  intermediateResults: new Map(),
  resumeFrom: null // 支持断点恢复
};
```

### 2. 可恢复的执行（Resumable）

这是 Dynamic Workflows 相比传统 Agent 编排的关键工程优势：

| 能力 | Subagents | Agent Teams | Dynamic Workflows |
|------|-----------|-------------|------------------|
| **中断后恢复** | ❌ 重启本轮 | ⚠️ teammates保持运行 | ✅ **同 session 内可恢复** |
| **进度持久化** | ❌ |⚠️ 任务列表 | ✅ **脚本变量 + resume token** |
| **结果复用** | ❌ |⚠️ 共享列表 | ✅ **脚本变量跨 phase 可用** |

> 原文："Reach for a workflow when a task needs more agents than one conversation can coordinate, or when you want the orchestration codified as a script you can read and rerun."
> — [Claude Code Docs](https://code.claude.com/docs/en/workflows)

### 3. 内置质量模式：对抗性审查

Dynamic Workflows 不仅仅是"运行更多 Agent"，还能应用**可复用的质量模式**。典型例子是 `/deep-research` 的工作流：

1. **Fan-out**：从多个角度并行搜索
2. **Cross-check**：独立 Agent 互相审查对方的发现
3. **Vote**：对每个 claim 投票，淘汰未通过交叉验证的
4. **Synthesize**：生成带引用的最终报告

> 原文："it can have independent agents adversarially review each other's findings before they're reported, or draft a plan from several angles and weigh them against each other, so you get a more trustworthy result than a single pass."
> — [Claude Code Docs](https://code.claude.com/docs/en/workflows)

这意味着 Harness 不只是"让 Agent 跑起来"，而是**将工程最佳实践编码为可复用脚本**。

---

## 与现有 Harness 体系的关系

### Anthropic Harness 演进路径

Anthropic 的 Harness 工程经历了三个阶段：

| 阶段 | 特征 | 代表 |
|------|------|------|
| **固定 Harness** | 单一 Agent + 固定工具集 | Claude Code初始版本 |
| **可配置 Harness** | 通过配置调整 Agent 行为 | Auto Mode 的双层安全架构 |
| **动态 Harness（Dynamic Workflows）** | **按任务需求动态生成 Harness** | Claude Code v2.1.154+ |

Dynamic Workflows 是前两个阶段的超集：它保留了固定 Harness 的确定性，同时引入了动态生成能力。

### 与传统 Harness 的关键区别

| 维度 | 固定 Harness | Dynamic Workflows |
|------|-------------|------------------|
| **Harness 生成时机** | 设计时（开发者编写）| **运行时（Claude 动态生成）** |
| **Agent 数量** | 1-N 个固定 | **按需扩展（数十到数百）** |
| **执行控制** | Claude 逐轮决定 | **脚本控制（代码化）** |
| **上下文管理** | 全塞进主 Agent | **脚本变量隔离，按 phase聚合** |
| **恢复能力** | 无 | **session 内可恢复** |

---

## 适用场景与不适用场景

###适合 Dynamic Workflows 的场景

- **代码库范围的 Bug 排查**：需要数十个 Agent 并行扫描不同模块
- **大型代码迁移**（500+ 文件）：需要分阶段、可验证的迁移
- **交叉验证的研究问题**：需要多个独立源互相审查
- **多角度计划制定**：从多个独立角度起草计划，再权衡选择

### 不适合的场景

- **简单的一次性任务**：直接用 Claude 对话更高效
- **需要深度上下文连贯性的任务**：脚本变量无法替代 Agent 的上下文窗口
- **非结构化的探索性任务**：过于僵硬的 phase 结构可能限制探索

---

## 工程意义

### Harness 从"配置"到"代码"的转变

传统的 Agent Harness 本质上是**配置文件**——告诉 Agent 可以做什么、不能做什么、用什么工具。但配置无法表达"流程控制"和"多 Agent 协调"。

Dynamic Workflows 将 Harness 的表达能力从"配置"提升到"代码"：

- **配置 Harness**：声明式，告诉你 Agent 能做什么
- **代码 Harness**：命令式，告诉 Agent **按什么顺序、什么条件、什么分支**做什么

> 笔者认为，这个转变是 Agent 工程化的关键一步：Harness 不再只是"边界防护"，而是**完整的任务执行引擎**。

### 对 Agent 工程的启示

1. **Evaluator Loop 的脚本化**：传统的 evaluator loop 需要 Claude 在每轮判断"任务是否完成"。Dynamic Workflows 将这个判断外化到脚本变量和 phase边界中
2. **工作区状态管理的进化**：中间结果不再依赖"git commit as memory"，而是存在结构化的脚本变量中
3. **多 Agent 协作的规模化**：从"几个 Agent 协作"扩展到"数十个 Agent 并行"

---

## 结论

Claude Code Dynamic Workflows 代表了 Anthropic 在 Harness 工程上的最新演进：**从固定 Harness → 可配置 Harness → 动态生成 Harness**。

其核心工程机制：
- **计划即代码**：将编排计划从上下文窗口移到 JavaScript 脚本
- **可恢复执行**：session内的断点恢复能力
- **质量模式编码**：将工程最佳实践（对抗性审查、多角度验证）固化为可复用脚本
- **规模化多 Agent**：支持数十到数百个 Agent 的并行协调

**金句**：当你的 Harness 需要协调超过 10 个 Agent 时，也许该问的不是"如何优化我的 Agent"，而是"我的计划是不是该写成代码了"。

---

## 引用来源

- [A harness for every task: dynamic workflows in Claude Code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) (2026-06-02)
- [Orchestrate subagents at scale with dynamic workflows - Claude Code Docs](https://code.claude.com/docs/en/workflows)
- [YouTube: Claude Can Now Build Its Own Harness... For Every Task](https://www.youtube.com/watch?v=l5rae4LMKBc)

---

*归档目录：`articles/harness/` | 相关主题：Harness 工程、Multi-Agent 编排、工作区状态管理*