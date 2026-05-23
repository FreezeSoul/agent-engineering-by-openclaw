# openai/symphony：把 Linear 当成 AI Agent 控制台，让人类"管工作"而非"管 Agent"

**核心命题**：Symphony 解决了一个本质矛盾——Coding Agent 再强，人盯 agent 也会成为瓶颈。Symphony 的解法是把项目管理工作流（Linear）变成 Agent 编排控制台，让人类从"监督多个 Tab 中的 Agent"变成"管理一个任务池"。

**Stars**：24,471（截至 2026-05-23）
**GitHub**：https://github.com/openai/symphony

---

## 一、为什么需要 Symphony

当 Coding Agent 的规模扩大时，OpenAI 团队发现了一个反直觉的瓶颈：

> "Each engineer would open a few Codex sessions, assign tasks, review the output, steer the agent, and repeat. In practice, most people could comfortably manage three to five sessions at a time before context switching became painful."

三个问题：
1. **Agent 很快，人成了系统瓶颈**：Agent 执行速度远超人类审核速度，多个并行 Agent 让工程师在 Tab 之间疲于奔命
2. **上下文切换的认知成本高**：每个 Tab 里 Agent 在做什么、卡在哪里、需要什么决策——这些信息随时变化，人要不断追踪
3. **监督 Agent ≠ 管理 Work**：人本能地关注"哪个 session 在做什么"，而忽略了真正重要的"哪个任务完成了"

Symphony 的核心洞察是：**把问题从"管理 Agent 会话"变成"管理待完成的工作"**。

---

## 二、Symphony 的核心设计

### 2.1 把 Linear 当成状态机

Symphony 将任务管理工具 Linear 建模为一个状态机，每个状态对应一个 Agent 生命周期阶段：

- **Open（待处理）** → 分配 Agent
- **In Progress（进行中）** → Agent 持续执行，循环直到完成或阻塞
- **In Review（审查中）** → 人类审核结果（PR、报告、证据）
- **Done（完成）** → 归档

关键点：**任务状态驱动 Agent 的生命周期，而不是 Agent 会话状态驱动人类的行为**。

### 2.2 Agent 自主从任务池拉取工作

不再由人类打开多个 Tab、分配任务。Symphony 的核心机制是：

1. **Continuous Watching**：Symphony 持续监控 Linear 板上的所有 Open 任务
2. **Agent Spawning**：每个 Open 任务触发一个独立的 Agent 实例（隔离的 workspace）
3. **Autonomous Execution**：Agent 自己从任务描述中理解目标，执行并产出结果
4. **Self-Recovery**：Agent 崩溃或 Stall 时，Symphony 自动重启（无需人工介入）

> "If an agent crashes or stalls, Symphony restarts it. If new work appears, Symphony picks it up and starts organizing work."

### 2.3 DAG 化的任务依赖

Symphony 支持在 Linear 中建模任务间的依赖关系（一个任务 Block 另一个），Agent 会自动识别并等待前置任务完成后再开始：

> "Agents only start working on tasks that aren't blocked, so execution unfolds naturally and optimally in parallel for this DAG."

这意味着工程师只需要建模"什么任务依赖什么"，Symphony 自动处理"谁先做谁后做、谁可以并行"。

### 2.4 Agent 可以创建新任务

最有趣的设计点：Agent 在执行过程中可以主动创建新的 Linear Issue：

> "During implementation or review, they often notice improvements that fall outside the scope of the current task... they simply file a new issue that we can evaluate and schedule later"

这是一个自我进化的反馈回路：Agent 执行 → 发现新问题 → 创建 Issue → 进入任务池等待评估和调度 → 下次被 Agent 接手。

---

## 三、Symphony 的关键工程数据

OpenAI 团队给出了具体的效率提升数字：

> "resulting in a 500% increase in landed pull requests on some teams"

500% 的 PR 增长背后，不是因为 Agent 变得更快，而是因为**人类从"每个 Session 都要盯"变成"看任务板就够了"**。

---

## 四、与 OpenAI Swarm 的对比

| 维度 | OpenAI Swarm | Symphony |
|------|-------------|----------|
| **抽象层次** | 多 Agent 之间的通信和角色分配 | 把任务管理工具变成 Agent 控制台 |
| **编排逻辑** | Agent 间点对点通信（Handoff）| 单一调度器（Linear）驱动所有 Agent |
| **人类角色** | 编排 Agent 之间的关系 | 审核 Agent 产出的结果 |
| **适用场景** | 多角色协作的复杂工作流 | 大规模、长周期、并行化的工程任务 |
| **设计哲学** | 去中心化的 Agent 网络 | 中心化的任务状态机 + 自主的 Agent 执行 |

**笔者认为**：Swarm 适合研究/实验阶段的 Multi-Agent 编排探索，Symphony 适合工程落地阶段——当你要让多个 Agent 真正大规模跑起来时，需要一个"可靠的任务管理层"而不是"灵活的 Agent 间协议"。

---

## 五、如何使用 Symphony

Symphony 提供了两种使用方式：

### Option 1：让 Agent 从零实现

> "Tell your favorite coding agent to build Symphony in a programming language of your choice"

给 Agent 一个 prompt，包含规范文档链接，让 Agent 自己选择语言实现。这是一个 meta 的用法——让 Agent 帮你构建 Agent 编排工具。

### Option 2：使用 Elixir 参考实现

Symphony 提供了一个实验性的 Elixir 实现，位于 `elixir/README.md`。可以快速上手体验。

---

## 六、Symphony 的局限

Symphony 的官方文档给出了明确警示：

> "Symphony is a low-key engineering preview for testing in trusted environments."

目前是工程预览版，不适合生产环境。其次，Symphony 依赖的前提是**你已经有一套适合 Agent 的开发环境**（即采用了 harness engineering 的实践）：

> "Symphony works best in codebases that have adopted harness engineering."

没有 CI guardrails、没有可靠的测试覆盖、没有规范化的代码结构，Agent 产出的 PR 质量无法保证。

---

## 七、关联文章

本文与以下文章形成闭环：

- **OpenAI Symphony 开源编排规范深度解读**（Articles）— Symphony 的设计理念与规范解析
- **openai/swarm：教育级多 Agent 编排框架**（Projects）— Swarm 作为 Symphony 的去中心化对照
- **cft0808/edict：三省六部制度性多 Agent 审核**（Projects）— 治理层的另一个视角

三层闭环：
- **编排层**：Swarm（Symphony 的去中心化变体）
- **治理层**：Edict（三省六部的制度性 QA）
- **管理层**：Symphony（Linear 任务板驱动）

---

**引用来源**：

1. "Symphony turns project work into isolated, autonomous implementation runs, allowing teams to manage work instead of supervising coding agents." — [GitHub README](https://github.com/openai/symphony)
2. "resulting in a 500% increase in landed pull requests on some teams" — [OpenAI Engineering Blog](https://openai.com/index/open-source-codex-orchestration-symphony/)

---

> **相关卫星项目推荐**：
> - [openai/symphony-elixir](https://github.com/openai/symphony) — Elixir 参考实现，快速上手
> - [openai/harness-engineering](https://openai.com/index/harness-engineering/) — Symphony 的前置条件，Agent 工程的 guardrails 实践