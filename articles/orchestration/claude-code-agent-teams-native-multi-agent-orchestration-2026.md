# Claude Code Agent Teams：原生多 Agent 协作的架构与工程实践

**发布于**：2026-04-24 | **演进阶段**：Stage 7 · Orchestration | **分类**：orchestration/

## 开篇

多 Agent 系统的协作模式，长期存在一个被忽视的结构性问题：**信息必须经过主节点中转**。无论子 Agent 如何并行工作，最终都要把结果汇报给主 Agent，再由主 Agent 分发下一个任务。这不是真正的协作——这是带有一层中介的批处理。

Claude Code Agent Teams（后文简称 Agent Teams）试图解决的是这个问题。它让多个 Claude Code 实例以点对点方式通信、共享任务队列、互相发送消息——而不是一切经过主会话。

这不是一个简单的功能叠加。它重新定义了 Claude Code 作为协作平台的能力边界。

本文拆解 Agent Teams 的架构设计、通信协议、工程实践中的权衡，以及它与现有多 Agent 方案的的本质区别。

---

## 1. 为什么需要 Agent Teams：Hub-and-Spoke 的瓶颈

在 Agent Teams 之前，Claude Code 的并行执行依赖两种机制：

**单会话 + 串行执行**：一个 Claude Code 实例按顺序处理任务。上下文窗口是唯一的信息载体。
**Subagents（Task 工具）**：主会话派生出独立工作单元，但它们只能向主会话报告结果，不能互相通信。

Subagents 的通信拓扑是严格的 Hub-and-Spoke：

```
[Main Agent] ←—— report —— [Subagent A]
     ↑                           ↓
     ←—— report —— [Subagent B]
     ↑                           ↓
     ←—— report —— [Subagent C]
```

这意味着：当 Subagent B 发现 Subagent A 的方案有问题时，它无法直接告诉 A。只能报告主 Agent，再由主 Agent 转述。在需要实时协作的场景——比如多个 Agent 共同调试一个竞态条件，或者并行研究不同方案再互相 review——这种拓扑是根本性的障碍。

Agent Teams 改变了这一点。

---

## 2. 架构：四个核心组件

Agent Teams 的架构由四个组件构成，它们共同支撑了一个真正点对点的多 Agent 协作系统。

### 2.1 Team Lead

Team Lead 是用户的主要 Claude Code 会话。它的工作是：

1. 初始化团队，定义角色和职责边界
2. 生成共享任务列表（Shared Task List）
3. 向队友分配任务
4. 汇总各队友的发现，输出最终结果

Team Lead 不再是信息中转站，而是一个协调器——它定义结构，但不再垄断信息流。

### 2.2 Teammates

每个 Teammate 是一个完全独立的 Claude Code 实例，有自己的：

- 独立上下文窗口（独立的 CLAUDE.md、MCP 服务器配置、Skills）
- 独立的文件系统和项目状态视图
- 独立的工具调用权限（继承自 Team Lead 的权限配置）

> 关键设计决策：Teammate 启动时**不继承** Team Lead 的对话历史。它拿到的是 CLAUDE.md + 项目上下文 + spawn prompt。这意味着 Team Lead 的对话历史不会污染 Teammate 的推理空间。

每个 Teammate 有自己的 Mailbox，可以接收来自 Team Lead 或其他 Teammate 的消息。

### 2.3 Shared Task List

Shared Task List 是 Agent Teams 的核心协调机制。它是一个中心化的任务队列，所有 Agent 都能读写。

任务有三种状态：`pending`（等待中）、`in_progress`（进行中）、`completed`（已完成）。任务之间可以声明依赖关系，这使得 Team Lead 能够合理地安排执行顺序，而 Teammates 能够自主判断"我已经可以开始了"。

```
Task-1: 分析 API 层设计 (pending, deps: none)
Task-2: 实现数据库迁移 (pending, deps: Task-1)
Task-3: 编写测试套件 (pending, deps: Task-2)
```

每个任务包含：标题、详细描述、状态、依赖列表、指派的 Teammate（可选）。

### 2.4 Mailbox（消息系统）

每个 Teammate 有自己的 Mailbox，实现任意 Agent 之间的直接消息传递。Mailbox 的物理存储位置：

```
~/.claude/teams/{team-name}/config.json  # 团队配置
~/.claude/tasks/{team-name}/            # 任务列表
~/.claude/inboxes/{team-name}/{teammate-name}.jsonl  # 每个 Teammate 的收件箱
```

Mailbox 支持：

- **Direct message**：点对点消息给特定 Teammate
- **Broadcast**：向所有 Teammate 广播（谨慎使用，成本随团队规模线性增长）
- **Idle notification**：Teammate 空闲时通知其他 Agent

消息格式是 JSONL（JSON Lines），每条消息是一个 JSON 对象，包含发送者、接收者、时间戳和内容。

---

## 3. 与 Subagents 的本质区别

这是理解 Agent Teams 最关键的部分。

| 维度 | Subagents | Agent Teams |
|------|-----------|-------------|
| **通信拓扑** | Hub-and-Spoke（所有经过主 Agent） | Mesh（任意 Agent 间直接通信）|
| **上下文关系** | 子上下文，汇总回主会话 | 完全独立上下文窗口 |
| **任务协调** | 主 Agent 手动分配 | Shared Task List + 自主 Claim |
| **启动延迟** | 即时 | ~20-30 秒（spawn）|
| **Token 成本** | 约 1.2-1.5x 单会话 | 约 3-4x 单会话（3 个 Teammate）|
| **适用场景** | 独立、聚焦、只关心结果 | 复杂、需要讨论、需要协调 |

Agent Teams 不是 Subagents 的"增强版"。它们解决的是不同问题。

Subagents 是承包商：你派出去，办完事回来，结果汇总给你。
Agent Teams 是项目组：大家坐在同一间屋子里，各自负责一块，实时同步，发现问题直接讨论。

当你只需要"帮我并行分析这 5 个文件"时，Subagents 更划算。当你需要"帮我重设计这个架构，三个 Agent 要互相 challenge 对方的方案"时，Agent Teams 是唯一可行的选择。

---

## 4. 工程流程：一个完整示例

假设任务：重构一个包含 API 层、数据库层、前端组件和测试的大型代码库。

### Step 1：启用 Agent Teams

```bash
export CLAUDE_AGENT_TEAMS_ENABLED=true
```

或写入 `~/.claude/settings.json`：

```json
{
  "agentTeams": {
    "enabled": true
  }
}
```

### Step 2：描述任务和团队结构

向 Claude 说：

```
我需要重构 /src 目录下的整个 API 层。当前设计耦合严重，
需要拆分为独立模块。请组建一个 Agent Team 来完成这件事：
- 1 个 Agent 分析当前 API 依赖图，输出重构方案
- 2 个 Agent 并行实现不同的模块（auth 和 payments）
- 1 个 Agent 负责编写测试并验证重构后没有回归

每个 Agent 要能互相通信。如果某个 Agent 发现另一个 Agent
的方案有问题，直接告诉对方，不用通过我转达。
```

### Step 3：Team Lead 的工作

Team Lead 分析任务后，创建 Shared Task List：

```
Task-1: 分析 API 依赖图（Agent: architect）
Task-2: 实现 auth 模块（Agent: auth-dev, deps: Task-1）
Task-3: 实现 payments 模块（Agent: payments-dev, deps: Task-1）
Task-4: 编写测试验证（Agent: tester, deps: Task-2, Task-3）
```

architect 完成 Task-1 后，auth-dev 和 payments-dev 同时Claim Task-2 和 Task-3（不需要等待 Team Lead 分配）。

### Step 4：Teammates 之间直接通信

假设 architect 发现 payments 模块依赖 auth 模块，它会直接给 payments-dev 发消息：

```json
{
  "from": "architect",
  "to": "payments-dev",
  "type": "direct",
  "content": "Task-2 (auth) 是 Task-3 (payments) 的前置依赖。
  建议等 Task-2 完成后你再开始，或者我们开个会同步一下接口设计。"
}
```

payments-dev 可以：
1. 接受建议，等 Task-2 完成
2. 先开始不需要 auth 的部分
3. 向 architect 回复，反馈自己的理解

这种实时协调在 Hub-and-Spoke 拓扑下需要 Team Lead 多次转述。

### Step 5：清理

```bash
/team-cleanup
```

**注意**：必须由 Team Lead 执行清理，且要先关闭所有 Teammate，再关闭 Team Lead。

---

## 5. 任务分配策略：何时用 Agent Teams

### 适合 Agent Teams 的场景

| 场景 | 为什么 Agent Teams 更适合 |
|------|--------------------------|
| 多模块重构（API、DB、前端、测试各自独立）| 每个 Teammate 有明确边界，可以并行且实时协调 |
| 调试时多个 Agent 测试不同假设 | Teammates 可以互相 challenge，直接反驳对方的推理 |
| 架构评审需要多方观点收敛 | 不同 Agent 代表不同的设计理念，辩论后收敛到最强方案 |
| 大规模数据分类/处理 | 任务天然可分割，且 Teammates 不需要互相通信（可用 Batch 替代）|
| 研究型任务（需要探索、分享发现）| Teammates 可以实时分享发现，不需要等主 Agent 汇总 |

### 不适合 Agent Teams 的场景

| 场景 | 替代方案 |
|------|---------|
| 顺序执行的单文件编辑 | 单会话 + Subagents |
| 任务之间无通信需求 | `/batch` 命令（更简单）|
| 简单并行任务（只关心结果）| Async Workflows |
| 紧耦合的单体任务 | 单会话（Agent Teams 的协调开销不划算）|

---

## 6. 资源消耗与工程权衡

### Token 成本

3 个 Teammate 的 Agent Team 约消耗 3-4x 单会话的 token。

为什么这么高？每个 Teammate 都要加载完整的项目上下文（CLAUDE.md、MCP 配置等），且每个 Teammate 的完整推理链都独立存在于自己的上下文窗口中。没有结果压缩、没有信息摘要——这是 Mesh 拓扑的代价。

### 时间 vs 成本

对于一个需要 60 分钟串行执行的任务，Agent Team 可以在约 20 分钟完成（3 个 Agent 并行），但 token 成本是 3-4x。

计算：如果单会话执行成本是 $0.10，3 个 Teammate 1 小时的成本约 $0.30-0.40。但如果节省了 40 分钟，这是否值得取决于你的场景。

对于大型重构（数小时的工作），这个交换通常合理。对于快速 small task，这种开销不划算。

### Spawn 开销

Agent Teams 的另一个隐性成本是 spawn 时间。每个 Teammate 需要约 20-30 秒才能启动并开始工作。这意味着它的价值在"任务时长 >> spawn 开销"的场景中才能体现。

---

## 7. 局限性：诚实的评估

Agent Teams 目前还有一些重要的局限：

**1. 没有跨 Teammate 的共享状态**
每个 Teammate 的上下文窗口是独立的，没有类似于"共享内存"的机制。信息传递只能通过 Mailbox 消息，这意味着如果你需要 Teammate B 读取 Teammate A 的完整输出，B 需要自己请求 A 直接发送。

**2. 任务依赖声明是声明式的**
Shared Task List 支持声明依赖，但没有强制的执行顺序检查。Team Lead 需要自己管理依赖的正确性。

**3. 权限继承但不可定制**
Teammate 启动时继承 Team Lead 的权限设置，但无法在 spawn 时为不同 Teammate 配置不同权限层级（这个功能在路线图上）。

**4. Linux 不支持**
目前 Agent Teams 只支持 macOS 和 Windows。对于在 Linux 上运行的 CI/CD 场景，无法使用。

**5. 协作质量依赖 CLAUDE.md 的清晰度**
如果 CLAUDE.md 写得模糊，每个 Teammate 需要花大量时间探索项目结构。这会显著推高 token 成本。

---

## 8. Agent Teams 在多 Agent 协作光谱中的位置

Claude Code 提供了一套从简单到复杂的多 Agent 工具，Agent Teams 位于光谱的一端：

| 方案 | 通信 | 最适合 |
|------|------|--------|
| 单会话 | 无 | 顺序的、聚焦的任务 |
| Subagents | Hub-and-Spoke（通过主 Agent）| 并行聚焦任务，只关心结果 |
| Builder-Validator 配对 | 结构化任务传递 | 需要质量门的实现任务 |
| **Agent Teams** | **Mesh（任意 Agent 直接通信）** | **需要讨论、协作、实时协调的复杂任务** |

这是一个渐进式的工具链。你可以根据任务复杂度选择合适的工具——而不是用 Agent Teams 解决所有问题。

---

## 结论

Claude Code Agent Teams 解决了多 Agent 协作中一个根本性的拓扑问题：从 Hub-and-Spoke 到 Mesh。

它的核心价值不是"并行"（这可以用 Subagents 做到），而是"实时协作"——Teammates 能够直接通信、互相 challenge、协调行动，而不需要经过主 Agent 转述。

对于需要多个 Agent 共同探索、辩论和协调的复杂任务，这是一个值得深入掌握的工程能力。但它的 token 成本、spawn 开销和协调复杂度意味着——你需要清楚自己在做什么，才不会为简单的任务付出不必要的代价。

---

## 参考文献

- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) — Claude 官方文档，Agent Teams 权威说明
- [Claude Code Agent Teams: Setup & Usage Guide 2026](https://claudefa.st/blog/guide/agents/agent-teams) — 完整的设置与使用指南，包含高级控制和实战模板
- [What Is Claude Code Agent Teams? How Parallel Agents Share a Task List](https://www.mindstudio.ai/blog/claude-code-agent-teams-parallel-shared-task-list/) — 任务列表机制的技术解析
- [Collaborating with agents teams in Claude Code](https://heeki.medium.com/collaborating-with-agents-teams-in-claude-code-f64a465f3c11) — 实际工作流中的团队协作模式
- [Architecture of Multi-Agent Coordination — opencode](https://dev.to/uenyioha/porting-claude-codes-agent-teams-to-opencode-4hol) — Agent Teams 架构向 OpenCode 的移植分析（Mailbox 实现细节）