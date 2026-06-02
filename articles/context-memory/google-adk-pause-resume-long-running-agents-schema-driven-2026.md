# Google ADK 如何实现长时运行 Agent 的暂停与恢复：跨越容器重启的上下文不丢失

> **本文来源**：https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/
> 
> **核心论点**：Google Agent Development Kit (ADK) 通过三层架构设计 — 结构化 Memory Schema、事件驱动休眠门（dormancy gate）、多 Agent 委托 — 让 Agent 能够在数天的企业工作流中跨越容器重启而保持上下文不丢失。

---

## 一、为什么长时运行 Agent 的上下文丢失是一个工程难题

企业工作流的本质是**长时间 idle**：新员工入职审批可能跨两周，发票争议处理可能拖数天，销售线索培育以月计。传统的无状态 Chatbot 在容器重启后立即丢失所有上下文 — 这不是 Bug，是设计取舍。

Google ADK 团队在博客中指出了这个问题的核心矛盾：

> "Real enterprise workflows are mostly idle time, and a stateless chatbot forgets everything the moment a container restarts."

当一个客服 Agent 处理一个跨度两周的纠纷时，容器重启意味着它需要重新开始 — 对话历史虽然还在向量数据库里，但**实时的会话状态**（当前处理到哪一步、哪些信息已确认、哪些还在等待）全部丢失。这是不可接受的工程现实。

---

## 二、ADK 的三层架构解法

ADK 团队展示了一个完整的 New Hire Onboarding Coordinator 实现方案，包含三个架构层面的设计决策。

### 2.1 第一层：结构化 Memory Schema（替代原始 JSON 向量存储）

传统的 Agent Memory 实现通常是把 JSON 状态直接塞进向量数据库，然后靠相似性检索来"回忆"。ADK 团队认为这是错误的做法：

> "structured memory schemas instead of raw JSON in a vector DB"

ADK 提倡的是**结构化 Schema**：每个 Agent 的状态被定义为强类型的数据模型，包含明确的字段和语义，而非裸的 JSON 字符串。这意味着：

- **类型安全**：状态的序列化和反序列化是可验证的
- **可组合**：Schema 之间可以引用、继承、组合
- **可查询**：字段级别的精确查询替代模糊的向量相似性搜索
- **增量更新**：部分字段更新不影响整体结构

这与传统的 RAG Memory 有本质区别：RAG Memory 是"搜索过去的记忆"，而 ADK 的结构化 Memory 是"记录当前的状态"。对于跨越多天的长时任务，后者远比前者可靠。

### 2.2 第二层：事件驱动休眠门（Event-driven Dormancy Gate）

传统的 Stateful Agent 在任务 idle 时会持续占用内存和计算资源。ADK 引入了**休眠门机制**：

当 Agent 进入等待状态（如等待用户回复、等待外部系统回调、等待定时触发），它不会保持一个运行的容器，而是触发**休眠事件**，将状态序列化到外部存储，然后释放所有运行时资源。

休眠门的工作流程：
1. **检测 idle**：Agent 识别任务进入等待状态
2. **状态快照**：将当前完整的执行上下文序列化到结构化 Memory
3. **释放资源**：终止容器，释放内存和 CPU
4. **注册唤醒事件**：在外部系统（队列、调度器、webhook）中注册回调
5. **恢复触发**：外部事件到达时，重新启动 Agent 并从 Memory 恢复

这与传统的"保持容器运行"的方案相比，资源效率是数量级的差异。一个两周的入职流程，如果全程保持容器运行，费用可能高得离谱；但如果只在需要处理事件时唤醒，成本可以压缩到原来的几十分之一。

### 2.3 第三层：多 Agent 委托（替代单体大 Prompt）

ADK 团队展示的 New Hire Onboarding Coordinator 不是一个大 Prompt 的单体 Agent，而是一组专门 Agent 的协作：

- **主 Agent**（Onboarding Coordinator）：负责任务路由和状态管理
- **子 Agent**（IT Setup Agent）：负责笔记本配置、账号开通
- **子 Agent**（HR Paperwork Agent）：负责合同、证件录入
- **子 Agent**（Benefits Enrollment Agent）：负责福利选择

这种设计的核心理念是：每个子 Agent 都有自己独立的 Memory Schema 和生命周期，主 Agent 只负责协调和决策。这与 LangChain/CrewAI 的多 Agent 框架不同之处在于，ADK 的多 Agent 是**状态可持久化**的 — 每个 Agent 都可以独立地进入休眠和恢复，而不影响其他 Agent。

---

## 三、与传统方案的对比

| 维度 | 传统 Stateless Chatbot | 传统 Stateful Agent | ADK 三层架构 |
|------|----------------------|--------------------|-------------|
| 容器重启后 | ❌ 完全丢失上下文 | ⚠️ 依赖历史消息，状态不完整 | ✅ 结构化 Memory 完整恢复 |
| 资源效率 | ✅ 无状态，无额外开销 | ❌ 持续占用容器 | ✅ 休眠时不占用资源 |
| 多 Agent 状态 | ❌ 无 | ⚠️ 粗粒度共享 | ✅ 独立 Memory Schema |
| 状态查询 | 向量相似性搜索 | 消息历史回溯 | 字段级精确查询 |

---

## 四、"跨越容器重启"的技术本质

Google ADK 博客中的这张图值得深入理解：

```
[触发休眠事件] → [状态序列化到 Memory] → [容器释放] → [等待唤醒事件] → [恢复并继续执行]
```

这个流程的技术本质是**状态与执行分离**（State/Execution Separation）：

- **State**：包含完整的执行上下文 — 当前任务进度、已收集的信息、下一步决策点
- **Execution**：只在需要推进任务时才运行

传统的 Stateful Agent 把 State 和 Execution 耦合在同一进程中，所以进程死亡 = 状态丢失。ADK 将状态持久化到外部存储，让状态不依赖任何特定进程的存活。

这与 OpenAI Agents SDK 的 `harness/compute separation` 理念是一致的 — harness（持久化的状态层）和 compute（按需运行的执行层）分离。但 ADK 更进一步：它的 Memory Schema 是结构化的、可组合的、可精确查询的，而不是简单的键值存储。

---

## 五、这对 Agent 工程意味着什么

ADK 的三层架构揭示了一个重要的工程趋势：**长时运行 Agent 的上下文管理正在从"消息历史"转向"结构化状态"**。

传统的 RAG + Memory 方案本质上是把 Agent 当作一个"知道很多事情的聊天机器人"。而 ADK 的方案是把 Agent 当作一个"有持久化状态的工作流参与者"。

这两种范式的区别在于：

- **聊天机器人范式**：每次交互都是独立的，上下文靠历史消息维系
- **工作流参与者范式**：每个任务都是跨时间的连续过程，上下文靠持久化状态维系

对于企业场景（HR 入职、采购审批、客户服务），第二种范式是必须的。而 ADK 提供了这个范式的第一个完整的、开源可用的工程实现。

> **引用来源**：
> - Google Developers Blog: "Build Long-running AI agents that pause, resume, and never lose context with ADK" (https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/)
> - 原文：*"structured memory schemas instead of raw JSON in a vector DB"* — Google ADK Team

---

*标签：#context-memory #orchestration #harness #Google-ADK #long-running-agents #state-management*