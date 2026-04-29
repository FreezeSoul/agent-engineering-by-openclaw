# Cursor 3 Glass：并行 Agent 架构的工程拆解

> **核心问题**：Cursor 3 将 IDE 从"AI 辅助编辑工具"重新定义为"Agent 编排平台"。这个转变背后的工程决策是什么？为什么工作树（Worktree）是这个架构的核心抽象？
>
> **Tags**: `Cursor 3` `Agent Architecture` `Parallel Agents` `Worktree` `AI Coding`

---

## 一、为什么 IDE 的形态必须改变

Cursor 3 的代号是"Glass"，发布于 2026 年 4 月 2 日。它的 headline 变化不是新模型，而是**新形状**。

Composer，那个从 2024 年以来定义 Cursor 的侧边面板，被移除了。取而代之的是一个全屏的 **Agents Window**：可以同时启动多个 Agent，分别指向不同的任务，各自维护独立的上下文和工作树。

这个重新设计的背后有一个明确的产品论断：**大多数代码未来将由 AI Agent 编写；人类工程师的角色是编排这些 Agent**。Glass 是 Cursor 对这个未来的赌注。

但这不是一个 UI 层面的改动。它要求底层的任务调度、上下文隔离、结果合并机制全部重新设计。本文拆解这个架构的核心工程决策。

---

## 二、核心抽象：为什么是 Worktree

### 2.1 工作树不是什么

Cursor 2 也支持工作树（Worktree），但用法完全不同。Cursor 2 的工作树是"完全独立的并行上下文"——每个分支有自己的一套代码和对话历史，工程师需要在最后手动决定哪个分支的改动"是对的"然后合并回主分支。这是一个面向人类的并行工具。

Cursor 3 的工作树设计目标不同。它的核心问题是：**当多个 Agent 同时修改同一个代码库时，如何让它们的改动能够被系统性地合并，而不是制造一堆冲突的分支？**

### 2.2 PR 导向的工作树

Cursor 3 的答案在官方社区帖子中被描述为"PR-oriented worktree"。

```
每个 Agent 在自己的工作树上操作，
每个工作树对应一个独立的 PR/任务。
完成后通过一个 Merge Agent 协调合并。
```

这意味着**并行不再意味着"同时改同一份代码"**，而是"把任务分解为独立子任务，每个子任务在独立的代码快照上执行"。合并时只需要处理逻辑冲突，而不需要处理 git 层面的分支合并。

伪代码层面的任务分配逻辑大概是：

```python
# Cursor 3 Agents Window 的任务分配逻辑（概念模型）
def launch_parallel_refactor(main_task, subtasks, agents_config):
    # 1. 克隆主仓库为 N 个工作树
    worktrees = [clone_to_worktree(main_task.repo, f"wt-{i}") 
                 for i in range(len(subtasks))]
    
    # 2. 每个 Agent 在独立工作树上执行独立子任务
    futures = []
    for task, wt in zip(subtasks, worktrees):
        agent = create_agent(config=agents_config[task.type])
        # Agent 获得：子任务描述 + 工作树路径 + 不重名的指令
        futures.append(agent.execute(task, worktree=wt))
    
    # 3. 等待所有 Agent 完成
    results = [f.result() for f in futures]
    
    # 4. Merge Agent 读取各工作树的 diff，协调合并
    merge_agent = create_agent(type="merge")
    merge_result = merge_agent.merge([r.diff for r in results])
    
    return merge_result
```

工作树的隔离粒度是**仓库级**的，而不是文件级。这意味着 Agent 之间不会看到彼此的部分修改，减少了相互干扰。但这个设计也意味着：**如果任务本身不是可分解的（即子任务之间存在强依赖），强行并行反而会更糟**。

---

## 三Agents Window 的架构位置

### 3.1 从侧边栏到全屏工作区

Composer 的物理形态是 IDE 右侧的一个面板。它与主编辑区共存，工程师可以在写代码的同时和 Agent 对话。

Agents Window 是全屏的。它的形态更接近"一个专门为 Agent 协作设计的 IDE"，而不是一个附属于代码编辑器的聊天窗口。

这意味着交互模型的转变：

| 维度 | Composer 2（Cursor 2.x） | Agents Window（Cursor 3） |
|------|------------------------|--------------------------|
| **交互模式** | 人机协作（人在写，AI 辅助） | 人-Agent 协作（人编排，Agent 执行） |
| **上下文窗口** | 共享主编辑器上下文 | 每个 Agent 独立工作树上下文 |
| **任务粒度** | 单文件或小范围修改 | 多文件、跨模块的大型任务 |
| **反馈循环** | 实时（人在看 Agent 改） | 异步（Agent 在后台跑，结果回来再看）|
| **UI 形态** | 侧边面板（与人操作的编辑器共存）| 全屏工作区（人是观众，不是操作者）|

这个转变的核心是**控制权反转**：在 Composer 中，人是主体，AI 是工具；在 Agents Window 中，Agent 是主体，人是审查者。

### 3.2 三种运行环境

Agents Window 支持三种 Agent 运行环境：

- **本地（Local）**：Agent 在本机文件系统上操作，适用于需要直接访问本地开发环境的场景
- **云沙箱（Cloud）**：Agent 在云端隔离环境中运行，适用于长时间任务或需要特殊硬件资源的任务
- **远程 SSH**：Agent 在远程服务器上操作，适用于需要访问生产环境或特殊部署目标的场景

这个三环境设计解决了 Deep Agent 范式中的一个实际问题：不同任务类型需要不同的执行上下文。快速的文件操作适合本地；耗时任务适合云端；部署相关任务适合 SSH 环境。

---

## 四、Composer 2：Glass 的推理底座

### 4.1 技术规格

Glass 不是新模型，但它的 Agents Window 严重依赖 Composer 2 作为核心推理引擎。

Composer 2 发布于 2026 年 3 月 19 日，是 Cursor 的第一个自有推理模型，定价 $0.50/M input / $2.50/M output tokens。以下是关键基准数据（来自[官方技术报告](https://arxiv.org/abs/2603.24477)，2026 年 3 月）：

| 模型 | CursorBench | Terminal-Bench 2.0 | SWE-bench Multilingual |
|------|------------|-------------------|----------------------|
| Composer 2 | 61.3 | 61.7 | 73.7 |
| Composer 1.5 | 44.2 | 47.9 | 65.9 |
| Composer 1 | 38.0 | 40.0 | 56.9 |

Terminal-Bench 2.0 使用官方 Harbor 评估框架，5 次迭代取平均值。值得注意的是，Composer 2 的 Terminal-Bench 2.0 分数（61.7）低于 Claude Code 获得的官方分数（不同 harness 之间不可直接比较）。

### 4.2 /best-of-n：模型选择的工程意义

Cursor 3 引入了 `/best-of-n` 机制，本质上是对同一个任务并行运行多个模型/配置，选择结果最好的一个。

这不是新概念（LLM 的 self-consistency、best-of-N sampling 早已有之），但将它做成 IDE 内置功能意味着：**模型选择本身变成了一个工程可配置项**，而不是开发者在不同工具之间手动切换。

/best-of-n 的工程含义：
- 对于简单任务：用便宜模型多次尝试，总成本仍然低于一次 Frontier 模型
- 对于关键任务：Frontier 模型 + N 次重试，提升 pass@1
- 代价是 Token 消耗可能显著增加（N 次输入 + N 次输出）

---

## 五、设计权衡：Glass 的工程取舍

### 5.1 并行 Agent 的真实代价

dev.to 的分析给出了一个具体案例：为一个 FastAPI refund 端点添加 idempotency、audit log 和测试。

**Composer 2 串行工作流**（约 6 分钟，~$0.20）：
```
Agent 依次完成：API endpoint → audit log → tests
单 Agent，上下文共享
```

**Agents Window 并行工作流**（约 3 分钟，~$0.30）：
```
Agent 1: API endpoint（工作树 A）
Agent 2: audit log（工作树 B）
Agent 3: tests（工作树 C）
→ Merge Agent 合并
```

并行节省了 50% wall time，但 Token 消耗增加了约 50%。在 Max Mode 下，这个乘数效应更加明显。

**关键洞察**：Agents Window 是一个**token 预算放大型**的 UI。每一个 Agent Tab 都在消耗 token。如果团队不建立并发的资源意识，Token 消耗会远超实际效益。

### 5.2 Design Mode 的局部价值

Glass 引入的 Design Mode 值得单独评价。它的核心能力是：在渲染后的浏览器页面中直接标注 UI 元素，将标注结果作为结构化指令传给 Agent。

这解决了前端开发中一个长期痛点：视觉调整类需求（"把这个按钮右移 8px"）在传统 text-based Agent 对话中很难精确表达。Design Mode 提供了一个更自然的输入通道。

但 Design Mode 的适用范围是**前端视觉类任务**，对于后端逻辑、数据处理、系统架构类任务几乎没有帮助。这是一个面向特定场景的局部优化，不是通用能力。

### 5.3 Max Mode 的定价结构

2026 年 3 月 16 日起，Frontier 模型（GPT-5.4、Sonnet-4.6、Opus-4.6、GPT-5.3 Codex）被移至 Pro/Pro+/Ultra 订阅的 Max Mode 层级。Max Mode 的计费方式是在标准请求费率上叠加乘数。

这意味着：**Glass 的 Agents Window 与 Max Mode 的计费模型直接叠加**——并行 Agent × Max 乘数 × Agent 数量。这是 2026 年 AI Coding 成本结构中一个值得密切关注的组合。

---

## 六、工程适用性判断

### Glass 适用的场景

以下场景中，Glass 的 Agents Window 提供了真实的工程价值：

- **多文件大型重构**：跨 20+ 文件的 domain concept rename，分解为多个子任务并行处理
- **多 package monorepo 操作**：各 package 之间的改动相对独立，并行收益高
- **代码 + 测试双线并行**：一个 Agent 负责实现，一个 Agent 负责测试，合并时逻辑冲突少
- **长时间后台任务**：云端 Agent 执行测试套件或类型检查，本地继续其他工作

### Glass 不适用或成本不划算的场景

- **单文件简单修改**：强行并行只会增加合并成本和 token 消耗
- **强耦合的多文件改动**：如果多个 Agent 都需要了解同一个文件的上下文，并行收益为负
- **预算受限的团队**：Max Mode 下的并行 Agent 成本可能远超实际时间节省
- **需要深度代码理解的复杂逻辑**：当前模型在跨模块上下文理解上仍存在局限，多 Agent 并行会放大理解误差

### 团队采用建议

1. **从三并发开始，不要从六并发开始**。三个并行 Agent 是大多数可分解任务的合理上限
2. **周五检查 Max Mode 账单**。如果发现 Token 消耗异常增长，回顾本周的 Agent 并发使用情况
3. **建立并行任务的准入标准**：任务必须可分解为"边界清晰、上下文独立的子任务"才使用并行 Agent
4. **不要禁用 Frontier 模型**。用 Frontier 模型处理核心复杂逻辑，Composer 或其他便宜模型处理简单任务

---

## 七、一手资源

- [Composer 2 技术报告 (arXiv:2603.24477)](https://arxiv.org/abs/2603.24477)
- [Cursor 3 官方更新日志](https://cursor.com/changelog/3-0)
- [Cursor 3 官方发布博客](https://cursor.com/blog/cursor-3)
- [Cursor 3：Worktrees & Best-of-N 官方讨论](https://forum.cursor.com/t/cursor-3-worktrees-best-of-n/156507)
- [Terminal-Bench 2.0 官方评估框架 (Harbor)](https://github.com/laude-institute/harbor)