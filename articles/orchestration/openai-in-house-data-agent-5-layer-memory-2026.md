# OpenAI 内置数据 Agent：五层上下文记忆与自调试循环

> 原文：[Inside OpenAI's in-house data agent](https://openai.com/index/inside-our-in-house-data-agent/)  
> 作者：Bonney Xu, Aravind Suresh, Emma Tang  
> 发布：2026-01-29  
> 分类：orchestration / context-memory

---

## 核心命题

OpenAI 内部的数据 Agent（不面向外部）解决了企业级数据分析的一个核心矛盾：**规模越大，找表比写 SQL 更费时**。这个 Agent 通过五层上下文记忆和一个自调试循环，让「从问题到洞察」从几天缩短到几分钟——而且每次对话都在变聪明。

笔者认为，这篇文章的真正价值不在于「可以这样用 AI 做数据分析」，而在于它揭示了一个**可复制的工程模式**：当 Agent 需要在真实生产环境中处理高价值决策时，Context 的质量直接决定了输出质量，而 Memory 必须超越 RAG 成为**非显而易见知识（non-obvious knowledge）的结晶层**。

---

## 背景：规模杀死效率

OpenAI 的数据平台服务超过 **3,500 名内部用户**，横跨 Engineering、Product、Research，覆盖 **600 PB 数据、70,000 个数据集**。

在这种规模下：

> 「我们有很多相似的表，我花大量时间弄清楚它们之间的差异，以及该用哪个。有些包含注销用户，有些不包含。有些字段重叠，很难判断表的实际含义。」
> —— 内部用户原话

即使选对了表，正确的 SQL 也需要分析师理解表之间的关系和语义。常见失败模式包括：
- **多对多JOIN**导致结果膨胀
- **Filter pushdown 错误**导致数据丢失
- **未处理的 NULL**导致统计偏差

这些问题在数据规模下会静默失效——SQL 跑出来了，但结果错了。

---

## 架构：五层上下文记忆系统

这个 Agent 不靠单一记忆机制。它构建了 **五层上下文**，每层解决不同类型的信息缺失。

### Layer 1：Table Usage Metadata

- **Schema 元数据**：列名、数据类型
- **表血缘（Lineage）**：上游表 / 下游表关系
- **历史查询**：通过历史 SQL 理解哪些表通常被一起 JOIN

> 原文引用：「Ingesting historical queries helps the agent understand how to write its own queries and which tables are typically joined together.」

### Layer 2：Human Annotations

专家手动提供的描述，包含：
- 表和列的业务含义（intent、semantics）
- 已知限制和注意事项
- 无法从 schema 或历史查询中推断的隐性知识

### Layer 3：Codex Enrichment（代码级上下文）

这一层是整个设计的亮点——**通过代码定义来理解表**。

Agent 利用 Codex 对表的 Spark/Python 代码定义进行解读，从而知道：
- 数据唯一性特征
- 更新频率
- 数据范围（如「只包含第一方 ChatGPT 流量」）
- 在 SQL 之外的用法

> 原文引用：「Nuances on what is stored in the table and how it is derived from an analytics event provides extra information. For example, it can give context on the uniqueness of values, how often the table data is updated, the scope of the data, etc.」

这解决了「两个表 schema 完全相同，但业务含义完全不同」的经典问题。

### Layer 4：Institutional Knowledge

Agent 可以访问：
- Slack
- Google Docs
- Notion

这些系统记录了公司内部的关键信息：发布计划、可靠性事件、内部代号和工具名称、关键指标的规范定义和计算逻辑。

访问控制通过 metadata 和 permissions 实现，运行时由 retrieval service 处理缓存。

### Layer 5：Memory（自我改进）

这是最关键的一层，也是与其他四层本质不同的一层——**它存储的是「纠错」**。

当 Agent 遇到以下情况时，它会记住：
- 某个指标的计算需要特殊 filter（如实验 gate 的特定字符串匹配）
- 对特定数据问题的隐性约束
- 用户提供的纠正

> 原文引用：「The goal of memory is to retain and reuse non-obvious corrections, filters, and constraints that are critical for data correctness but difficult to infer from the other layers alone.」

### 上下文更新管道

每天的离线管道把前四层（Table Usage、Human Annotations、Codex Enrichment）聚合成一个标准化表示，然后通过 OpenAI Embeddings API 转换成 embedding 存储。

查询时，Agent 只检索最相关的嵌入上下文，而不是扫描原始元数据或日志。

---

## 核心机制：自调试循环

这个 Agent 的核心能力不是「一次性给出正确答案」，而是**在过程中识别错误并自我修正**。

工作流：

```
用户提问
  ↓
Agent 推理 → 写 SQL → 执行
  ↓
结果检查（零行？数据分布异常？）
  ↓
如果有问题 → 调查原因 → 调整 JOIN/filter/条件
  ↓
重试，直到结果合理
```

> 原文引用：「If an intermediate result looks wrong (e.g., if it has zero rows due to an incorrect join or filter), the agent investigates what went wrong, adjusts its approach, and tries again.」

这个机制的关键在于：**Agent 携带完整上下文**，每一次迭代都继承前一次的认知，而不是从零开始。

---

## 超越单点答案：像队友一样工作

OpenAI 明确把这个 Agent 设计成「可以与之推理的队友」，而不是「答案机器」。

关键设计点：

| 场景 | Agent 行为 |
|------|-----------|
| 问题模糊 | 主动提问澄清 |
| 无响应 | 应用合理默认值继续（如默认最近 7/30 天）|
| 跑偏 | 用户随时打断，重定向方向 |
| 重复分析 | 打包成可复用的 Workflow |

用户可以要求它做快速问答，也可以做探索性分析，Agent 在两种模式下表现一致。

---

## Eval 机制：持续质量保护

因为 Agent 是 always-on 且持续进化，**质量漂移的风险真实存在**。

OpenAI 使用 Evals API 保护响应质量：

- 精选问题-答案对（Question-Answer pairs）
- 每个问题配有手写的「黄金 SQL」，生成预期结果
- 发送自然语言问题 → 执行生成的 SQL → 对比结果

Eval grader 不做简单的字符串匹配，而是比较 SQL 和结果数据，接受语法不同但语义等价的结果。

> 原文引用：「These evals are like unit tests that run continuously during development to identify regressions as canaries in production.」

---

## 安全模型：纯接口层

这个 Agent 的安全设计非常清晰——**它只是接口层，不自己持有权限**。

- 所有访问都是 pass-through
- 用户只能查询他们已有权限的表
- 缺失权限时，Agent 会标记或回退到替代数据集

> 原文引用：「All of the agent's access is strictly pass-through, meaning users can only query tables they already have permission to access.」

---

## 给我们的教训

笔者认为，这个案例揭示了三个可迁移的工程原则：

### 1. Context 是基础设施，不是可选项

当 Agent 需要处理高价值决策时，Context 的质量直接决定了可靠性。五层设计中的 Codex Enrichment 和 Memory 层尤其值得借鉴——它们解决的问题是「schema 相同但含义不同」和「非显而易见约束」。

### 2. Memory 不是 RAG，是纠错结晶

大多数 Agent Memory 实现停留在「记住之前说过什么」。OpenAI 的 Layer 5 做得更深入——它记住的是**「这里的正确方式与直觉相反」**这类知识。这是让 Agent 真正变聪明的路径。

### 3. Self-debugging 是长程任务的标准配置

任何需要跨多个步骤、可能产生错误结果的 Agent，都需要内建自调试能力，而不是假设每一步都正确。重试 + 上下文继承是打破这个问题的关键。

---

**关联项目**：[strukto-ai/mirage](https://github.com/strukto-ai/mirage) — 统一虚拟文件系统，让 Agent 用同一套 bash 工具操作所有后端。与本文的 Layer 4（跨服务上下文整合）形成互补。