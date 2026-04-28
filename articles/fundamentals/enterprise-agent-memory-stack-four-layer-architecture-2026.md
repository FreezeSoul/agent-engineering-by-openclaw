# 企业级 Agent 记忆栈：四层架构的工程实现

大多数 Agent 演示在一个 session 内看起来惊艳，但上线后迅速失效。根源不是模型能力不足，而是系统没有"记忆基础设施"——每次对话都从零开始，无法积累跨 session 的业务知识、决策历史和约束条件。

这不是 Prompt 问题，是一个**记忆工程栈问题**。

本文拆解 2026 年企业级 Agent 记忆栈的四层架构：Working Memory → Episodic Memory → Semantic Memory → Governance Memory。每一层都有明确的数据模型、检索模式和工程权衡。

---

## 1. 为什么企业 Agent 需要分层记忆架构

企业场景中的 Agent 不是聊天机器人，而是跨用户、跨系统、跨时间轴执行的**业务流程参与者**。

一个真实场景：保险理赔助手需要记住"上次我们同意了哪些条款"，以及"当时用了什么证据"；集成设计 Copilot 不能重复提议相同的耦合错误，因为无法回忆"上次为什么拒绝了这个方案"；平台 SRE 助手能回答"什么是 CPU"，但无法回答"上次和这次故障之间发生了什么变化"。

这些需求有三个共同特征：

- **快速**：需要像聊天一样实时响应
- **结构化**：关系型问题（"上次哪些服务一起失败的？"）
- **可审计**：监管要求 Agent 的每个决策可追溯

这意味着不能用 "RAG + 向量数据库" 解决一切——那只是**检索增强**，不是**记忆架构**。

---

## 2. 四层记忆栈的总体结构

四层架构的核心逻辑类比分布式系统：

| 类比 | 记忆层 |
|------|--------|
| Cache vs Source of Truth | Working vs Episodic |
| Hot vs Warm vs Cold Storage | Working → Episodic → Semantic |
| Bounded Contexts and Ownership | 每层都有明确的数据边界 |
| Disciplined read/write patterns | 检索策略不是玄学，有明确模式 |

各层的目标、容量策略、延迟目标不同：

| 层 | 主要目标 | 容量策略 | 延迟目标 |
|----|---------|---------|---------|
| Working Memory | 立即任务完成 | Token 预算硬限制 | < 1s（聊天感） |
| Episodic Memory | 跨 session 业务连续性 | Episode 为单位，append-only | < 2s |
| Semantic Memory | 共享知识，行为一致性 | 实体关系优先，按策略压缩 | < 3s |
| Governance | 审计、安全、合规 | 全量记录，版本化管理 | 不影响主路径 |

---

## 3. Layer 1: Working Memory（上下文窗口）

Working Memory 是当前任务的即时工作集，相当于 CPU 缓存。

**包含内容**：
- 最近 N 轮对话（或滚动摘要）
- 活跃计划（"下一步做什么"）
- 重要的工具输出（当前步骤的结果）
- 中间结构暂存（如架构草图）

**设计约束**：
- Token 预算有限，必须做取舍
- 延迟必须像聊天，"无感等待"
- "无脑塞入更多上下文"最终会变成成本和质量的双重问题

**关键设计选择**：
```
滑动窗口 vs 摘要窗口
任务期间缓存什么 vs 每步重新拉取什么
丢弃什么 vs 压缩什么
```

**设计示例**：设计集成架构
```
保留：最近 6-10 轮对话
保留：当前架构草图（组件 + 接口 + 非功能性需求）
保留：当前约束列表（安全、数据驻留、延迟、成本）
其余：按策略检索，不按"历史回忆"
```

> **工程判断**：Working Memory 的核心权衡是**信息密度 vs 上下文长度**。当 Working Memory 开始塞入太多信息时，不是加钱升级模型上下文窗口，而是将信息下沉到 Episodic/Semantic 层。

---

## 4. Layer 2: Episodic Memory（场景记忆）

Episodic Memory 将交互分组为有意义的业务单元：一次理赔流程、一次故障事件、一次集成设计评审。

这层的数据模型（最小可行版本）：

```yaml
episode_id: string
type: incident | claim | design | migration | release
participants: [person/team/agent]
entities: [customer, service, system, integration, product]
timestamps: [start, end, key_events]
artifacts:
  - chat_log_pointer
  - diagram_pointer
  - PR_link
  - ticket_link
summaries:
  narrative: "what happened"
  decision: "what we decided and why"
  risk: "what could bite us later"
```

**检索模式**：
- "查找这个服务/客户/领域的相关 episodes"
- "展示最近两次类似故障以及什么修复了它们"
- "两次集成修订之间发生了什么变化"

**实现提示**：
- 将 Episode 视为**只追加的事件日志**（工具调用记录、决策、证据）
- 主记录存在关系型/文档型数据库
- 添加二级嵌入索引用于召回和聚类
- 保留"证据指针"作为一等公民，便于后续审计

> **工程判断**：Episodic Memory 的关键是**Episode 边界由业务语义定义，而非时间或 token 数量**。一个 Episode 是"理赔流程从开始到关闭"，而不是"过去 30 天的对话"。

---

## 5. Layer 3: Semantic Memory（语义知识层）

Semantic Memory 将 Episodes 蒸馏为更稳定的知识：实体、关系、策略和领域事实。

这是记忆栈中**最接近传统知识管理**的一层，也是让 Agent 行为在不同 session、不同团队间保持一致的关键。

**包含内容**：
```yaml
entities:
  - customers, products, systems, services, integrations
relationships:
  - depends-on
  - publishes
  - consumes
  - owned-by
  - shares-data-with
constraints:
  - SLAs
  - compliance_rules
  - data_residency
  - cost_limits
  - vendor_constraints
patterns:
  - known_failure_modes
  - "how_we_do_things_here"
```

**检索技术优先级**：
1. **实体中心索引**：先问"关于 Service Y 和 Integration Z 的所有记忆"
2. **图格式检索**：当关系本身是答案时（如依赖链）
3. **语义检索**：作为相似性搜索的补充

**角色**：跨 Agent 的共享记忆层，使行为跨时间和跨团队保持一致。

> **工程判断**：如果企业已有 API 目录、能力模型、领域边界和事件分类，这些资产应该成为 Semantic Memory 的一等公民——停止把它们当文档，开始把它们当**可操作的记忆**。

---

## 6. Layer 4: Governance Memory（治理与可观测性）

到 2026 年，治理不是附加组件。如果无法回答"为什么 Agent 做了那个决策"，就没有生产级系统。

**记录内容**：
```yaml
prompts_and_system_instructions:  # 版本化
retrieved_items:                 # 注入了什么，从哪里来
actions_taken:                  # 工具调用、写入、审批
outputs_produced:                # 生成的响应
memory_versions_used:           # 哪个知识快照，哪版策略
```

**用途**：
- **审计与合规**：展示这个决策的基础
- **故障后分析**：为什么批准了这个变更
- **漂移检测**：当记忆或模型变化时行为是否漂移
- **安全审查**：泄漏、越权、特权滥用

**实现**：扩展现有可观测性栈（logs/traces/metrics），添加 AI 特定字段：
```yaml
episode_id:          # 关联到哪个 Episode
retrieval_set_id:     # 关联到哪组检索结果
policy_version:       # 关联到哪个策略版本
model_version:        # 关联到哪个模型版本
```

> **工程判断**：Governance Memory 是唯一不影响主路径的层——它以异步旁路记录，不应该增加任何主路径延迟。它的质量决定了系统能否通过监管审查。

---

## 7. 跨层工程权衡

### 容量 vs 延迟 vs 安全

记忆栈是**资源管理问题**，不是"选哪个向量数据库"的问题。

| 维度 | Working | Episodic | Semantic | Governance |
|------|---------|----------|----------|------------|
| 主要目标 | 即时任务完成 | 业务连续性 | 共享知识一致性 | 可审计性 |
| 容量策略 | Token 预算 | Episode 单位 | 实体关系压缩 | 全量记录 |
| 延迟目标 | < 1s | < 2s | < 3s | 不影响主路径 |
| 安全策略 | 上下文隔离 | 边界访问控制 | 共享读取控制 | 不可篡改日志 |

### 检索优先顺序

不是所有问题都需要走到 Semantic Memory。优先顺序：

```
问题 → Working Memory 查询
  ↗ 能回答 → 返回
  ↘ 不能回答 → Episodic Memory 查询
    ↗ 能回答 → 返回
    ↘ 不能回答 → Semantic Memory 查询
      ↗ 能回答 → 返回
      ↘ 不能回答 → 降级为通用 RAG
```

**工程建议**：这个优先顺序本身应该作为 Agent System Prompt 的一部分显式表达，否则 Agent 会随意访问各层记忆，导致不必要的延迟和成本。

---

## 8. 与 CoALA 框架的映射

CoALA（arXiv:2309.02427）从**记忆类型**角度描述 Agent 记忆：Working Memory、Episodic Memory、Semantic Memory 是什么（存什么）。本文的四层架构从**工程实现**角度描述同一套系统：每一层的**数据模型是什么、如何检索、如何存储**。

两者是正交框架：CoALA 是概念层，四层架构是实现层。结合使用：

```
CoALA 框架（概念设计）→ 四层架构（工程落地）
```

CoALA 回答"我需要什么类型的记忆"，四层架构回答"每一层我具体要建什么、怎么建"。

---

## 9. 与 Mem0 / RAG 的分工

Mem0 在 2026 年的定位是** Episodic + Semantic 层的基础设施提供商**。

Mem0 的 benchmark 数据：

| Approach | LLM Score (Accuracy) | Median Latency | Token/Conversation |
|----------|---------------------|----------------|-------------------|
| Full-context | 72.9% | 9.87s | ~26,000 |
| Mem0g (graph-enhanced) | 68.4% | 1.09s | ~1,800 |
| Mem0 | 66.9% | 0.71s | ~1,800 |
| RAG | 61.0% | 0.70s | — |

从这个数据看：
- **Mem0** 是Episodic层的实用选择，在 latency 和 accuracy 之间取得平衡
- **Full-context** 在 benchmark 上领先，但在生产环境不可用（9.87s 中位数延迟，17.12s P95）
- **四层架构** 需要在 Working Memory 层主动管理 token 预算，而不是依赖"上下文够长"

**工程建议**：Mem0 或类似工具解决 Episodic 层的检索问题，但 Working Memory 的 token 预算管理仍需要自己在 Agent 层面实现。

---

## 10. 一句话总结

> 企业级 Agent 记忆不是"RAG 加向量库"，而是四层分工明确的工程栈：Working Memory 管即时上下文（Token 预算硬限制），Episodic Memory 管业务 Episode（append-only 事件日志），Semantic Memory 管共享知识（实体关系优先），Governance Memory 管审计追溯（异步旁路）。用 CoALA 做概念设计，用四层架构做工程落地。

---

## 参考文献

- [A 2026 Memory Stack for Enterprise Agents – Alok Mishra](https://alok-mishra.com/2026/01/07/a-2026-memory-stack-for-enterprise-agents/) — 四层架构完整框架，工程实践导向
- [State of AI Agent Memory 2026 – Mem0](https://mem0.ai/blog/state-of-ai-agent-memory-2026) — LOCOMO benchmark 数据，2026-04-28 发布
- [CoALA Framework – arXiv:2309.02427](https://arxiv.org/abs/2309.02427) — 记忆类型概念框架
- [Mem0 Research Paper – arXiv:2504.19413](https://arxiv.org/abs/2504.19413) — ECAI 2025 发表，LOCOMO benchmark 来源
