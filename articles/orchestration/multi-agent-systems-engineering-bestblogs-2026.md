# 从单 Agent Shell 到多 Agent 编排：Multi-Agent Systems Engineering 生产级框架

> 本文来源：[Multi-Agent Systems Engineering: From Theory to Production](https://www.bestblogs.dev/en/explore/topics/multi-agent-systems)（BestBlogs.dev，2026-06）

## 核心命题

Harness engineering 的下一个台阶，不是更强的单 Agent，而是**多 Agent 系统的编排工程**。

业界长期将"多 Agent"视为单 Agent 的简单复制——多个 Agent 并行跑，取最强输出。但这个思路忽略了关键问题：**多 Agent 系统是一类全新的工程挑战**，它需要独立的架构设计：编排层、运行时隔离、共享状态、结果评估。这四个平面缺一不可，否则多 Agent 系统只是"一群各行其是的 Agent"，而非真正的协同系统。

BestBlogs 这篇合成文章的核心判断值得重视：

> "A harness is the engineering shell around a single agent; a multi-agent system is the dispatch, communication, and shared logistics around a fleet of agents. Same engineering culture, one level up."

这句话点出了多 Agent 系统的本质：**不是造更强的 Agent，而是建立 Agent 之间的调度、通信与共享机制**。

---

## 一、为什么现在必须关注多 Agent 系统工程

多 Agent 系统从学术好奇走向生产现实，背后有三个驱动因素：

**1. 任务复杂性超过单 Agent 能力边界**

当任务需要同时处理多个领域上下文（数据库 schema变更 + 前端 UI 重构 + 安全审计），没有任何单 Agent 能稳定完成。拆解给多个专业 Agent 是自然思路，但前提是编排层可靠。

**2. MCP 生态催生跨 Agent 互操作性需求**

Model Context Protocol 的普及使得不同 Agent 调用不同工具成为标准实践。但协议层只解决了"如何通信"，解决不了"谁来调度谁"和"结果如何汇总"。

**3. 生产环境对可观测性和容错的要求**

单 Agent 出错影响单一任务；多 Agent 出错可能产生级联副作用。生产级多 Agent 系统必须能回答："谁在哪一步失败了"、"剩余任务如何处理"、"结果是否可信"。

---

## 二、多 Agent 系统的四个核心平面

BestBlogs 提出的四平面模型是本文最有价值的框架贡献：

### 平面一：编排（Orchestration）

**回答问题**：哪个 Agent 在什么时候做什么？

三种常见编排模式：

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **Manager-Worker** | 一个 Manager Agent 分发任务给多个执行 Agent | 任务可分解、结果需汇总 |
| **Pipeline** | Agent A 输出作为 Agent B 输入 | 有严格依赖顺序的处理链 |
| **Parallel** | 多个 Agent 同时处理同一任务的不同切片 | 独立子任务、需并行加速 |

Anthropic Managed Agents 官方支持全部三种模式。

### 平面二：运行时（Runtime）

**回答问题**：Agent 如何隔离、如何恢复？

单 Agent 运行时需要沙箱和检查点；多 Agent 运行时还需要**跨 Agent 的状态协调**。这包括：

- **Session隔离**：不同 Agent 运行在独立沙箱中，防止相互干扰
- **检查点（Checkpoint）**：任务中断后能从断点恢复，而非从头开始
- **追踪（Tracing）**：记录每个 Agent 的决策路径，供事后审计

### 平面三：状态（State）

**回答问题**：Agent 之间如何共享信息？

多 Agent 状态管理比单 Agent 复杂得多：

**Memory vs. Dreaming**：
- **Memory**：Agent 在单个 session 内学习，存储于文件系统
- **Dreaming**：跨 session 的带外过程，回顾历史 session，提取模式，更新共享 Memory，使 Agent 车队不再重复同一错误

Anthropic 的实现中，Memory 是常规文件系统，Agent 通过 `bash` 管理笔记，内容哈希用于乐观并发控制。

**共享状态的挑战**：谁来写、谁只读、冲突时如何解决？这些问题在单 Agent 架构中不存在，在多 Agent 架构中必须显式处理。

### 平面四：评估（Evaluation）

**回答问题**：多 Agent 协作的结果是否正确？

单 Agent 评估看输出质量；多 Agent 评估还需要看**协作质量**：

- 结果是否来自正确的 Agent 协作？
- 是否有 Agent 偷懒（跳过本应执行的步骤）？
- 是否有 Agent 重复做另一 Agent 已完成的工作？
- 整体 token 成本是否在预算内？

Grader（评分器）需要能评估过程，而非仅评估最终结果。

---

## 三、MCP 在多 Agent 系统中的角色

MCP（Model Context Protocol）在多 Agent 系统中的角色不是"粘合剂"，而是**标准接口层**。

当每个 Agent 通过 MCP 与工具交互时：
- **工具调用可跨 Agent 复用**：无需为每个 Agent 单独实现工具封装
- **工具行为可统一审计**：所有 Agent 的工具调用通过同一协议层，可集中监控
- **新工具可热插拔**：在不停机的情况下为 Agent车队添加新能力

笔者认为，MCP 在多 Agent 系统中的价值类似于 REST API 在微服务中的价值——它不是最优雅的解决方案，但是一个足够好用的标准化接口，使得跨 Agent 互操作成为可能。

---

## 四、为什么说这是"Harness Engineering 的下一步"

过去一年的 harness engineering 讨论集中在单 Agent 场景：如何设计 permission layer、如何做 eval harness、如何做 checkpoint/resume。这些经验在单 Agent 层面已经相对成熟。

但多 Agent 系统不是"单 Agent 乘以 N"。当 Agent 之间需要协调时：

- **Permission 问题升级**：不再是"Agent 能做什么"，而是"Agent A 能否授权 Agent B 代表它行动"
- **Eval 问题升级**：不再是"单 Agent 输出是否正确"，而是"多 Agent 协作流程是否高效"
- **状态管理问题升级**：不再是"单 Agent Memory"，而是"共享 Memory 的所有权和一致性"

这种"升维"要求工程团队重新思考 harness 的边界。多 Agent 系统需要一个**显式的编排层**，这个编排层本身也是一个需要工程化的组件，而非自然涌现。

---

## 五、工程实践要点

基于四平面模型，以下是构建生产级多 Agent 系统的最低要求清单：

**编排层最低要求**：
- [ ] 显式定义编排模式（Manager-Worker / Pipeline / Parallel）
- [ ] 任务分发可追踪（谁分发了什么、何时分发）
- [ ] 支持任务中止和重新调度

**运行时最低要求**：
- [ ] Session 级别隔离（防止 Agent 间状态泄露）
- [ ] 检查点机制（支持从非末尾步骤恢复）
- [ ] 全局追踪（跨 Agent 的决策路径记录）

**状态层最低要求**：
- [ ] 共享 Memory 的所有权策略（读/写权限）
- [ ] Dreaming 机制或等效的跨 session 学习能力
- [ ] 冲突检测和解决策略

**评估层最低要求**：
- [ ] 结果正确性评估（与传统测试等价）
- [ ] 过程评估（Agent 是否遵循了正确的协作流程）
- [ ] 成本评估（Token 消耗是否在预算内）

---

## 结语

多 Agent 系统工程不是学术命题，而是生产需求。当你的任务复杂度超过单 Agent 能力边界时，你需要的不只是更多 Agent，而是一套**显式的编排、运行时、状态和评估机制**。

BestBlogs提出的四平面模型提供了一个清晰的思考框架：先把问题分解到四个平面，再为每个平面设计工程方案。这比"一堆 Agent 加一个聊天界面"要可靠得多。

**真正的多 Agent 系统，是先有编排工程，后有多 Agent 实例**。