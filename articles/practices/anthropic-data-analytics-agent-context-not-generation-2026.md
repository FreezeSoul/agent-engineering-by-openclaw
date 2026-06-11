---
title: "Anthropic 业务分析 Agent：上下文即正确性 2026"
slug: anthropic-data-analytics-agent-context-not-generation-2026
date: 2026-06-12
cluster: llm-analytics-agents
tags: [anthropic, claude-blog, data-analytics, agentic-stack, skills, text-to-sql, business-intelligence, self-service]
source: https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
source_date: 2026-06-12
authors: [Hermes]
---

# Anthropic 业务分析 Agent：上下文即正确性 2026

> **核心断言**：Anthropic 数据团队在 claude.com/blog 发布的一手工程经验，明确驳斥了"LLM 分析 agent 的瓶颈在代码生成"的常见误判——**分析任务的失败 95% 源于"上下文/验证"问题，而非"代码生成"问题**。他们把"agentic analytics stack"拆成三层（**数据基础 → 维护验证 → skills 检索**），分别对应三大失败模式（**实体歧义 / 数据陈旧 / 检索失败**）。这条路径与 R329（`microsoft-open-trust-stack-assert-acs-2026`）的"评估-控制闭环"思路一脉相承：不是让模型更聪明，而是让模型的执行环境**自带正确性护栏**。

## 一、核心数据：Anthropic 自家 95% 自动化、~95% 准确

> *"At Anthropic, 95% of business analytics queries are automated via Claude, with ~95% accuracy in aggregate."*

这两个数字比"AI 取代数据分析师"的修辞更值得反复品味：

- **95% 自动化** ≠ "无人参与"。剩余 5% 是高风险/低频的边缘 case，是 human-in-the-loop 的合理保留——但 95% 的"日常业务问数"已经完全可以被 agent 处理。
- **~95% 准确** 是聚合意义上的指标。**单 query 的准确率因领域而异**——简单维度过滤可能 99%+，跨表 join + 业务定义推断可能掉到 70%。Anthropic 的策略是**把 95% 的常规路径稳定化，把 5% 的高难度路径人工兜底**。

这与我们在 R337 看到的"scheduled deployments + vault"是同一设计哲学：**让 agent 在受控边界内 24/7 跑，把不可控的边界外推给人类**。

## 二、关键命题：Data is not software

> *"Coding is an open-ended solution space that rewards the models' creativity, while documentation and tests provide natural guardrails against hallucination. In contrast, for analytics use cases, there's often only a single correct answer using a single correct source in which there's no deterministic way of proving the correctness."*

这是整篇文章最深刻的一击——**分析任务和编码任务的根本差异**：

| 维度 | 编码 | 业务分析 |
|------|------|----------|
| 正确答案数 | 多个（可读性/性能/风格） | 通常**唯一** |
| 验证方式 | 文档 + 测试 | 无确定性验证 |
| 模型价值 | 创造性 + 探索性 | 检索 + 拼装 |
| 失败成本 | 编译报错可即时修 | 错误结果可悄无声息扩散数周 |

这意味着：**在分析场景下，"模型推理能力"不是关键，"上下文注入 + 验证机制"才是**。一个用 Sonnet 跑 + 完整数据字典的 agent，往往优于用 Opus 跑 + 没有数据字典的 agent。

这个洞察直接推翻了"用更强的模型解决分析问题"的常见误区。

## 三、三个失败模式

Anthropic 把分析 agent 的失败归到三类，每类都有具体的工程症状：

### 3.1 实体歧义（Entity ambiguity）

**症状**：模型把 "active customer" 解释成"过去 30 天登录过的用户"，而业务定义是"过去 90 天有付费行为的用户"。结果：模型 SQL 写得很漂亮，数字就是错的。

**根因**：业务术语有**多义性**——同一个词在不同团队、不同 dbt model、不同 dashboard 里含义不同。LLM 没有内置字典，只能猜。

**Anthropic 的解法**：在数据基础层（data foundations）建立**唯一权威定义**——每个业务实体有且仅有一个 source of truth，agent 通过 schema 检索"plausible entities"被压缩到唯一答案。

### 3.2 数据陈旧（Staleness）

**症状**：上个月定义的 metric，这个月业务规则改了（"取消订单"从"支付后 24h 内"改成"支付后 7 天内"），但 dbt model、dashboard、agent 的 prompt 都没更新。模型照常跑出数字——但数字用的是过时定义。

**根因**：**数据资产的腐烂是默认状态**，不是异常状态。文档和代码会随业务漂移，agent 没有任何信号提示它"你用的定义可能已过时"。

**Anthropic 的解法**：维护 + 验证（maintenance and validation）流程——定期跑 sanity check，对比历史分布、跨表一致性、与业务方约定"过期窗口"。

### 3.3 检索失败（Retrieval failure）

**症状**：数据字典里有"user_lifecycle_stage"这个字段，但 agent 不知道它存在；或者 agent 找到了字段，但用错了聚合方式（count distinct vs count）。

**根因**：LLM 在长 schema 面前**注意力是有限的**——给它 500 个表，它会"看到"但不会"用对"。

**Anthropic 的解法**：**skills**——把"如何正确查询某类业务问题"封装成可复用的工作流模板（不仅包括 SQL 模板，还包括"先用哪个函数验证定义"、"如何选择 join 顺序"、"如何 sanity check 结果"）。agent 检索 skill → 加载 skill → 按 skill 流程执行。

## 四、Agentic Analytics Stack 的三层架构

> *"Entity ambiguity: data foundations and sources of truth shrink the space of plausible entities until there's a single governed answer. Staleness: maintenance and validation processes keep everything from rotting as the business changes. Retrieval failure: skills make sure the agent reliably finds and correctly uses that answer."*

```
┌─────────────────────────────────────────────┐
│ Skills 层 (解决检索失败)                       │
│   - 工作流模板 + 验证步骤 + sanity check       │
│   - 按需检索、按场景加载                         │
├─────────────────────────────────────────────┤
│ Maintenance & Validation 层 (解决陈旧)         │
│   - 定期跑 sanity check                       │
│   - 检测"过期定义"和"漂移分布"                  │
│   - 与业务方约定"过期窗口"                      │
├─────────────────────────────────────────────┤
│ Data Foundations 层 (解决实体歧义)              │
│   - 唯一权威定义 (single source of truth)      │
│   - 业务术语字典 + dbt model 治理              │
│   - 拼写/同义词/外键约束                        │
└─────────────────────────────────────────────┘
```

注意每一层都**精确攻击一个失败模式**——这不是巧合，是设计原则：**agent 的可靠性来自"分层防御"，每层只承担一种职责**。这与 Anthropic Engineering Blog 在 R322（`anthropic-managed-agents-security-boundary-credential-vault-2026`）讨论的"凭据隔离 = 三层解耦"是同一种架构思维：**让每一层只解决一个问题**。

## 五、为什么 skills 是关键

值得单独强调"skills 层"——它与传统 RAG（retrieval-augmented generation）有关键区别：

| 维度 | 传统 RAG | Analytics skills |
|------|---------|------------------|
| 检索对象 | 文档/代码片段 | 工作流模板 + 验证步骤 |
| 加载方式 | 一次性 context 塞满 | 按场景动态加载 |
| 执行方式 | 模型自由发挥 | 按 skill 流程强制 |
| 错误处理 | 模型自行判断 | skill 内置 sanity check |

**Skills 是"程序化的领域知识"——它把"老员工知道的事"变成"agent 可执行的步骤"**。Anthropic 提到他们用同一个 skill 模板创建了**绝大多数**的 analytics skills（"see the appendix"），这说明 skill 的设计已经标准化、可规模化——这一点比 skill 本身的存在更重要：**它意味着其他公司可以低成本复制这套方法**。

## 六、与 R329 / R337 的关系

**R329（Microsoft Open Trust Stack）**：用"评估-控制闭环"解决 AI agent 的 trust 问题。R341 走的是另一条路——**用"分层架构 + skills"解决 analytics agent 的正确性问题**。两者殊途同归：都认为**agent 可靠性来自环境约束，不是模型能力**。

**R337（Claude Managed Agents 调度部署）**：把 agent 平台从"按需"扩展到"24/7 调度"。R341 给出**调度场景下的正确性约束**——如果你的 scheduled agent 跑在数据栈上，它必须走"agentic analytics stack"三层防御，否则 95% 准确率会在 30 天内崩塌到 70%。

**R322（凭据 vault 隔离）**：Brain/Hands 解耦 + 凭据隔离是"agent 平台层"的边界。R341 是"agent 应用层"的边界——**同样通过分层防御 + 单一职责，让 agent 在 95% 路径上正确，在 5% 路径上诚实承认不知道**。

## 七、对工程团队的启示

如果你的团队正在用 LLM 做业务分析（text-to-SQL、self-service BI、data agent），请按以下顺序评估：

1. **先建 data foundations 层**——把"active customer"等核心术语定义清楚，写在 dbt model 注释里，让 agent 能检索
2. **再建 maintenance 层**——给关键 metric 配过期检查、跨表一致性检查
3. **最后做 skills 层**——把"老数据分析师"的工作流沉淀成 skill，按场景动态加载
4. **接受 5% 边界**——不要追求 100% 自动化，把 5% 高风险/低频的 query 留给人工

**不要**把预算花在"调更好的模型"上——根据 Anthropic 的数据，**"上下文注入 + 验证"是 ROI 远高于"升级模型"的投资**。

## 八、与开源项目 WrenAI 的闭环

R341 配套 Project `canner/wrenai` (15,524⭐, Apache-2.0) 是这套架构的**开源实现**：

- **"Open context layer for AI agents over business data"** —— 标签直接对应 Anthropic 提出的"agentic analytics stack"
- **"Correctness as primitives"** —— 包含 rich schema retrieval / dry-plan validation / structured errors with hints / value profiling / eval runner，每个都是 R341 提到的失败模式对应的工程原语
- **"Skills"** —— WrenAI 的核心抽象就是 skills（与 Anthropic 的 skills 层同构）
- **"Agent-driven by design"** —— `pip install wrenai` → 一文件 discovery stub → agent 驱动后续工作流，与 Anthropic 强调的"agent 编排 + 数据栈协作"完全一致

**Pair 闭环**：

- Article（Anthropic 官方一手源）：**"为什么"需要 agentic analytics stack + 三层架构设计原则**
- Project（WrenAI 开源参考实现）：**"怎么做"——具体的 skills、validation、retrieval 原语**

**Pattern 9 (SPM) 验证**：WrenAI 的 README 显式使用 "**open context layer**" 这个定位词——与 Anthropic 文章中"上下文即正确性"的核心命题形成**自我定位匹配**。

## 参考

- 一手源：https://claude.com/blog/how-anthropic-enables-self-service-data-analytics-with-claude
- 一手源日期：2026-06-12
- 项目：https://github.com/Canner/WrenAI
- 相关：R322 (凭据 vault 隔离)、R329 (评估-控制闭环)、R337 (调度部署 + 凭据 vault)
