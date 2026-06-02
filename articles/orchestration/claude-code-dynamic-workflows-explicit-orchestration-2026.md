# Claude Code Dynamic Workflows：把多 Agent 编排从「隐式决策」变成「显式代码」

> **核心观点**：Dynamic Workflows 的本质不是"更多 Agent"，而是把 Orchestration 的控制流从「模型 turn-by-turn 的隐式判断」迁移到「可执行、可保存、可复用的 JavaScript 脚本」。这是一个工程成熟度的跃迁，而非功能增量。

---

## 一、问题的本质：谁在控制编排？

在 Dynamic Workflows 出现之前，Claude Code 的多 Agent 协作模式有三种：

| 模式 | 控制者 | 结果存储 | 可复用性 | 规模上限 |
|------|--------|---------|---------|---------|
| **Subagent** | Claude（turn-by-turn） | Context Window | Worker 定义 | 每轮几个任务 |
| **Skills** | Claude（遵循指令） | Context Window | 指令模板 | 同 Subagent |
| **Agent Teams** | Lead Agent（turn-by-turn） | 共享任务列表 | Team 定义 | 少数长时运行的对等体 |

三种模式的共同问题：**编排逻辑内嵌在模型的每次推理决策中**。Claude 决定下一步派发给哪个 Subagent、下一个任务是什么——这个决策过程是隐式的，保存在 context window 的注意力权重里，外部无法检查、无法版本化、无法在会话结束后复现。

笔者认为，这种模式的根本局限不在于"模型决策质量"，而在于**决策本身没有脱离模型的推理过程而独立存在**。当任务规模扩大，隐式编排会面临两个问题：

1. **上下文耗尽**：每个中间结果都挤在 context window 里，长任务会触发 compaction
2. **不可复现**：同一个 prompt 两次运行，编排路径可能不同（模型的非确定性）

---

## 二、Dynamic Workflows 的工程机制

### 2.1 脚本作为 Orchestration 载体

Dynamic Workflow 的核心是一个**由 Claude 编写、由 Runtime 执行的 JavaScript 脚本**。用户描述任务时包含 "workflow" 关键词，Claude 就会生成对应的脚本：

```javascript
// Claude 生成的 workflow 脚本（示例，来自文档结构）
const workflow = {
  phases: [
    { name: 'plan', agents: 1, task: 'understand codebase structure' },
    { name: 'audit', agents: 12, task: 'check each API endpoint for auth' },
    { name: 'synthesize', agents: 1, task: 'compile findings into report' }
  ]
};

// Runtime 在后台执行脚本，会话保持响应
// 脚本变量存储中间结果，不占用 context window
```

这里的关键设计是：**脚本持有编排逻辑和中间结果，context window 只接收最终报告**。

### 2.2 与 Subagent 的根本区别

| 维度 | Subagent | Dynamic Workflow |
|------|----------|-----------------|
| 编排决策点 | 每次 LLM 推理轮次 | 脚本加载时（编译期） |
| 中间结果位置 | Context Window | 脚本变量 |
| 可中断/恢复 | restart 从头 | 可在同会话恢复 |
| 可复用单元 | Worker 定义 | 整个编排脚本 |
| 规模 | 几个并行 | 数十到数百个 Agent |

引用官方文档：

> *"A workflow moves the plan into code. With subagents, skills, and agent teams, Claude is the orchestrator: it decides turn by turn what to spawn or assign next, and every result lands in a context window. A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer."*

### 2.3 Quality Pattern 的可编程性

真正有意思的不只是规模扩展，而是**可以在脚本里编码质量门控模式**。文档提到：

> *"it can have independent agents adversarially review each other's findings before they're reported, or draft a plan from several angles and weigh them against each other, so you get a more trustworthy result than a single pass."*

这意味着可以在 workflow 里实现：
- **对抗性评审**：Agent A 的输出交给 Agent B 审查，两者结果不一致时触发仲裁
- **多角度起草**：同一任务从 3 个独立角度并行处理，最终投票合并
- **条件分支**：基于中间结果决定是否进入下一阶段

这些在 turn-by-turn 模式里也可以做，但需要模型自己记得去做——在 workflow 里是显式编码的，不依赖模型的注意力。

### 2.4 Ultracode：从请求到工作流的自动升级

`/effort ultracode` 是一个有意思的设计：设置后，Claude Code 会自动为每个实质性任务规划工作流，而不是等待用户说 "workflow"。

```text
/effort ultracode
// 之后每个实质性任务，Claude 都会自动规划 workflow
// 单次请求可能触发多个工作流：一个理解代码，一个执行变更，一个验证
```

笔者认为，ultracode 是对「用户不需要知道编排细节」的工程承诺——模型判断任务复杂度，自动选择合适的执行模式。

---

## 三、工程意义：为什么这重要？

### 3.1 编排逻辑的可观测性

当编排是隐式的，调试 Agent 行为只能靠猜测："为什么这个任务没有派发给那个 Subagent？"当编排是脚本化的，workflow 的执行过程可以逐步检查，每个阶段的 agent 数量、token 消耗、运行时间都有记录。

Claude Code 提供了 `/workflows` 命令，可以查看运行中的工作流进度，钻进任何 phase 查看每个 agent 的 prompt 和 tool calls。

### 3.2 编排逻辑的可复用性

保存后的 workflow 就是一条可复用的命令。文档提到：

> *"If the run does what you wanted, you can save it as a command afterward."*

这意味着：**一个经过验证的编排模式可以固化为团队资产**。代码审查工作流、安全审计工作流、大规模迁移工作流——都可以作为命令分享给团队成员，输入任务描述即可重现完整编排。

### 3.3 「脚本即规范」的范式转移

在传统 Agent 使用模式里，"Prompts 就是规范"——Agent 行为由 prompt 描述，受限于 prompt 的表达能力和模型的注意力分配。

Dynamic Workflows 出现后，规范可以表达为：
- **控制流**（循环、条件分支、并行）
- **数据流**（中间结果存储、跨阶段传递）
- **质量门控**（对抗评审、多角度投票）

这些不是自然语言的模糊描述，而是**可执行、可静态分析、可以 CI 化的代码**。

---

## 四、与行业其他方案的横向对比

| 方案 | 编排载体 | 可视化 | 规模 | 质量门控 | 代表项目 |
|------|---------|--------|------|---------|---------|
| **Claude Code Workflows** | JS 脚本（Claude 编写）| `/workflows` TUI | 数十到数百 | 脚本编码 | Anthropic Claude Code |
| **LangGraph** | Python DAG 定义 | 多种可视化工具 | 任意规模 | 条件边 | LangChain |
| **CrewAI** | YAML 角色定义 | 无原生 | 少数角色 | 固定顺序 | CrewAI |
| **Microsoft Agent Framework** | .NET/Python 图 | Azure Workbench | 生产级 | checkpointing | Microsoft |
| **AutoGen** | Python 对话 | 无原生 | 任意规模 | 协商机制 | Microsoft |

笔者的判断是：Claude Code Workflows 在「用户意图到可执行编排」的路径上是最短的——**用户描述任务，模型生成编排脚本**。其他框架要求开发者自己编写编排逻辑，而 Workflows 把生成这一步也自动化了。

---

## 五、适用场景与边界

### 5.1 适合的场景

- **代码库级别的审计/迁移**：数百个文件的任务，超出单个 context window 容量
- **需要交叉验证的研究**：多个来源的结论需要相互核对
- **可重复的企业工作流**：安全审查、代码规范检查、依赖升级
- **长时运行的复杂任务**：需要暂停、恢复、检查进度的任务

### 5.2 不适合的场景

- **快速探索性任务**：工作流启动有 overhead，简单的一次性任务不值得
- **高度交互性的任务**：需要人在回路频繁干预的场景
- **非常简单的任务**：几个子任务就能搞定的不需要 workflow

### 5.3 当前限制

- 研究预览阶段（research preview），API 和稳定性可能有变化
- 需要 v2.1.154 或更高版本
- Pro 计划需要手动开启（`/config` → Dynamic workflows）

---

## 六、一句话总结

**Dynamic Workflows 不是让 Claude 做更多事情，而是把「谁做什么」的决策从模型的隐式推理中抽离出来，变成一行行的 JavaScript 代码。** 这让 Agent 编排从艺术变成工程——可检查、可复用、可版本化。

> *"A workflow moves the plan into code."* — Claude Code 文档

当编排可以保存为命令，可以代码审查，可以 CI 验证，Agent 工程才真正进入了软件工程的工业时代。

---

## 来源

- [Week 22 · May 25–29, 2026 - Claude Code Docs](https://code.claude.com/docs/en/whats-new/2026-w22)
- [Orchestrate subagents at scale with dynamic workflows - Claude Code](https://code.claude.com/docs/en/workflows)
- [Introducing Claude Opus 4.8 - Anthropic](https://www.anthropic.com/news/claude-opus-4-8)

---

*标签：multi-agent, orchestration, workflow-engineering, claude-code, anthropic*