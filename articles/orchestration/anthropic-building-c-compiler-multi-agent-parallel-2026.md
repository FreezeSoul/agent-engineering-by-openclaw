# 多 Agent 并行开发：Git Lock 同步的 C Compiler 实践

> **核心结论**：Anthropic 的 Nicholas Carlini 用 16 个 Claude Agent 并行开发了一个可编译 Linux 6.9 的 Rust C Compiler，耗时 $20,000、近 2,000 次 Claude Code 会话。这不是炫耀，而是对"多 Agent 如何同步、避免冲突、持续推进"工程难题的深度复盘。

---

## 背景：为什么需要 Agent Teams

现有 Agent 框架（如 Claude Code）需要操作员在线并持续参与。模型会解决部分问题，但最终会停下来等待输入——一个问题、一个状态更新，或一个澄清请求。

Carlini 构建了一个 Agent Team 系统，目标是：**让多个 Claude 实例在共享代码库上并行工作，无需主动人工干预**。这个系统大幅扩展了 LLM Agent 的能力边界。

压力测试任务：用 Agent 团队从零编写一个 Rust 实现的 C Compiler，能够编译 Linux 内核。

---

## 架构：最简单的多 Agent 同步方案

### 核心机制：Git Lock 文件同步

Carlini 的实现非常朴素：

1. 为每个 Agent 创建一个 Docker 容器，仓库挂载到 `/upstream`
2. 每个 Agent 把代码克隆到自己的 `/workspace`
3. **用 Git 作为分布式锁**：Agent 通过在 `current_tasks/` 目录下写文件来"锁定"任务（如 `parse_if_statement.txt`、`codegen_function_definition.txt`）
4. 如果两个 Agent 尝试认领同一个任务，Git 的同步机制会强制第二个 Agent 选择不同的任务

```bash
# Agent 工作流程
Agent 工作在任务上 → 提交到本地 → 从 upstream 拉取合并 → 推送 → 删除锁
```

冲突频繁，但 Claude 足够聪明能够解决。

### 循环驱动：Ralph Loop

为了持续运行，Carlini 构建了一个"永不停止"的循环：

```bash
#!/bin/bash
while true; do
    COMMIT=$(git rev-parse --short=6 HEAD)
    LOGFILE="agent_logs/agent_${COMMIT}.log"
    claude --dangerously-skip-permissions \
        -p "$(cat AGENT_PROMPT.md)" \
        --model claude-opus-X-Y &> "$LOGFILE"
done
```

Agent 完成一个任务后，立即挑选下一个。循环永远运行（虽然有一次 Claude 不小心 `pkill -9 bash` 自杀了循环——Whoops!）。

### Agent Prompt 的设计

在 Agent Prompt 中，Carlini 告诉 Claude：
- 要解决的问题
- 分解成小块来处理
- 跟踪正在做什么
- 弄清楚下一步要做什么
- 持续工作直到完美

---

## 并行 Agent 的两个核心优势

### 1. 调试并行化

单个 Claude Code 会话一次只能做一件事。当问题范围扩大，在并行中调试多个问题效率更高。

### 2. Agent 专业分工

- 部分 Agent 被分配解决实际问题
- 其他专业 Agent 可以：
  - 维护文档
  - 关注代码质量
  - 解决专门的子任务

> "在大多数情况下，Claude 会挑选'下一个最明显'的问题。当被 bug 卡住时，Claude 通常会维护一个正在运行的文档，记录失败的尝试和剩余的任务。"

---

## 关键教训：长时间运行的 Agent 编排

### 写让 Agent 保持正轨的测试

在没有人工监督的情况下，让 Agent 保持正轨是关键挑战。Carlini 发现测试驱动是关键：让 Agent 为自己生成测试，然后运行测试验证。

### 何时拆分工作，何时让单个 Agent 继续

不是所有问题都适合并行。拆分的成本是协调复杂度。当问题之间依赖关系强时，并行收益降低。

### 这种方法的局限性

Carlini 坦承这是"非常早期的研究原型"：
- 尚未实现 Agent 之间任何其他通信方法
- 没有执行管理高层目标的流程
- 不使用编排 Agent，而是让每个 Claude Agent 自己决定如何行动
- 没有强制任何任务优先级或依赖管理机制

---

## 关键引用

> "With agent teams, multiple Claude instances work in parallel on a shared codebase without active human intervention. This approach dramatically expands the scope of what's achievable with LLM agents."
> — Nicholas Carlini, Anthropic Safeguards Team

> "A new bare git repo is created, and for each agent, a Docker container is spun up with the repo mounted to /upstream. Each agent clones a local copy to /workspace, and when it's done, pushes from its own local container to upstream."
> — Nicholas Carlini

---

## 笔者观点

### 1. Git 作为分布式锁：简单到令人惊讶

用 Git 文件锁做协调听起来粗糙，但实际上极其优雅：
- **无额外基础设施**：不需要消息队列、etcd、Redis
- **天然幂等**：Git 操作本身可重试
- **代码即日志**：每次提交都是完整的任务历史

这种方法在工程上的可行性取决于代码库的结构——如果任务之间的依赖很弱，Git Lock 就足够。

### 2. "无编排 Agent"的哲学

Carlini 选择不给 Agent 配编排层，而是让它们自主协调。这与主流的多 Agent 框架（Orchestrator + Workers）截然不同。

优点：避免了单点失败和额外的协调开销
缺点：当任务有复杂依赖时，系统可能做出次优决策

### 3. $20,000 和 2,000 次会话的教训

这个数字本身就说明问题：即使是 16 个 Agent 并行，从零构建一个可编译 Linux 内核的 C Compiler 仍然需要巨大的资源和反复调试。这不是否定 Agent 的价值，而是说明**软件工程的复杂性有物理下界**。

### 4. 最重要的工程洞察

"让 Agent 保持正轨"的关键不是限制 Agent 的行为，而是让它**自己生成验证机制**。测试驱动不只是质量保证，也是让 Agent 保持目标感的手段。

---

## 相关信息

- **关联主题**：多 Agent 编排、Git-based 同步、并行开发
- **关联项目**：GreyhavenHQ/greywall（容器无关的 Agent 沙箱，Git Lock 与 Docker 容器结合可扩展）

---

**参考来源**：[Anthropic Engineering Blog — Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler)（Published Feb 05, 2026）