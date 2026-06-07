---
title: Anthropic「Writing Tools for Agents」：用 Agent 思维重新定义工具设计
date: 2026-06-07
description: 深度解读 Anthropic 工程博客关于 AI Agent 工具设计的方法论，核心洞见：工具是「确定性系统」与「非确定性 Agent」之间的新契约，设计重心应从「功能覆盖」转向「Agent 可用性」。
tags: [tool-use, agent-engineering, MCP, evaluation, anthropic]
---

# Anthropic「Writing Tools for Agents」：用 Agent 思维重新定义工具设计

> 本文深度解读 Anthropic Engineering 博客「Writing effective tools for AI agents—using AI agents」，原文发表于 2026 年，核心贡献是提出一套系统化的 Agent 工具设计方法论，核心观点是：**工具不是 API，而是 Agent 与世界之间的接口，设计的重心是让 Agent 能成功，而不是让功能覆盖完整。**

---

## 一、核心命题：工具是 Agent 的「接口」，不是 API

传统软件开发中，API 是确定性系统之间的契约：`getWeather("NYC")` 无论调用多少次，结果的获取方式都是一样的。

但 Agent 不同。同样的工具，Agent 可能在不同上下文下做出截然不同的反应——可能调用工具，可能直接回答，可能反问clarifying question。**这是因为 Agent 是非确定性系统：相同输入不保证相同输出。**

Anthropic 提出的核心洞见是：

> 工具是一种**新类型的软件**——它是「确定性系统」与「非确定性 Agent」之间的契约。

这意味着设计工具时，不能用写 API 的思路（定义好输入输出，让调用方自己处理）。工具设计必须考虑 Agent 的**affordances**——Agent 能「感知」到的潜在行动方式。

**一个典型的错误**：把现有软件的功能包装成工具，不考虑这个工具对 Agent 是否友好。

---

## 二、方法论：Agent 驱动的工具迭代循环

Anthropic 提供了完整的工具开发流程，核心是**让 Agent 参与工具的构建和改进**，形成评估→分析→优化的闭环。

### 2.1 构建原型（Build a prototype）

第一步不是设计完整的工具集，而是快速搭建原型。

关键做法：
1. 用 MCP server 或 Desktop Extension (DXT) 包装工具，快速接入 Claude Code
2. 用 `claude mcp add <name> <command>` 连接本地 MCP server 到 Claude Code
3. 手动测试工具，找出粗糙边缘
4. 收集用户反馈，建立对 Agent 使用模式的直觉

Anthropic 的经验是：**LLM-friendly 的文档格式（如 llms.txt）能显著提升 Claude 对工具的理解质量**。如果工具依赖复杂库，给 Claude 提供文档比让 Agent 自己探索要高效得多。

### 2.2 运行评估（Run an evaluation）

评估是整个方法论的核心。Anthropic 推荐的评估流程：

**生成评估任务**：
- 好的任务：需要多工具调用，可能涉及几十步操作
  - "Schedule a meeting with Jane next week to discuss our latest Acme Corp project. Attach the notes from our last project planning meeting and reserve a conference room."
  - "Customer ID 9182 reported that they were charged three times for a single purchase attempt. Find all relevant log entries and determine if any other customers were affected."
- 坏的任务：过于简单，不 stress-test 工具
  - "Search the payment logs for purchase_complete and customer_id=9182."

**运行评估**：用简单的 while-loop 包装 LLM API + 工具调用，每个任务一个评估 Agent。Anthropic 建议在 system prompt 中要求 Agent 输出 reasoning 和 feedback blocks（触发 CoT），这能帮助分析工具问题。

**收集指标**：
- Top-level accuracy
- 工具调用总数
- 单个工具调用 runtime
- Token 消耗
- 工具错误率

### 2.3 Agent 协作优化（Collaborate with agents）

这是 Anthropic 方法论最有趣的部分：**让 Agent 分析评估结果并改进工具本身**。

具体做法：
1. 把评估 Agent 的完整 transcript（包括 reasoning、feedback、tool calls、tool responses）拼接起来
2. 把这些 transcript 丢给 Claude Code
3. Claude 是「分析 transcript 和大规模重构工具的专家」——可以同时确保工具实现和描述的一致性

Anthropic 坦诚地说：**这篇文章的大部分建议就是这样来的**——反复用 Claude Code 优化内部工具实现，基于评估结果迭代。

---

## 三、工具设计四原则

### 原则一：选择正确的工具（Choosing the right tools）

**More tools don't always lead to better outcomes.**

常见的错误：为 Agent 提供太多工具，或者提供重叠的工具。Agent 会面临选择困难，不知道该用哪个工具。

关键洞察：LLM agents 有有限的「context」（能同时处理的信息量有限），而计算机内存是便宜且充裕的。

**一个具体的反模式**：

> 想象在通讯录里搜索联系人——传统程序可以高效地逐一检查每个联系人。但 LLM agent 如果使用一个返回所有联系人的工具，就必须 token-by-token 读完所有不相关的信息才能找到目标。

正确的做法：提供 `search_contacts(name)` 或 `message_contact(name)` 工具，而不是 `list_contacts`。

**工具可以合并功能**：把多个操作封装在一个工具内，让工具自己处理复杂的内部逻辑。

### 原则二：Namespacing 工具（Namespacing your tools）

当 Agent 潜在访问数十个 MCP server 和数百个工具时，工具名称的重叠会导致选择错误。

**Namespacing 的两种方式**：

| 方式 | 示例 | 效果 |
|------|------|------|
| Prefix-based | `asana_search`, `jira_search` | 按服务划分边界 |
| Suffix-based | `projects_search`, `users_search` | 按资源类型划分边界 |

Anthropic 发现命名方式对评估结果有显著影响，效果因 LLM 而异，建议根据自己团队的评估结果选择。

Namespacing 的核心价值：**把 Agent 的认知负担从 Agent 的 context 转移回工具本身**。清晰的工具边界让 Agent 不需要记住每个工具的具体能力，只需要记住工具的命名模式。

### 原则三：返回有意义上下文（Returning meaningful context）

工具响应应该只返回高信号信息，优先考虑上下文相关性而非灵活性。

**避免返回**：
- 低级技术标识符（uuid, 256px_image_url, mime_type）
- Agent 无法直接用于下游行动的原始数据

**应该返回**：
- name, image_url, file_type——这些能直接 inform Agent 的下游行动和响应

另一个关键建议：**把 UUID 解析为语义化的自然语言标识符**。Anthropic 发现把任意字母数字 UUID 转换为语义化的语言（或 0-indexed ID）能显著减少幻觉，提高检索精度。

**ResponseFormat enum 示例**：

```python
enum ResponseFormat {
    DETAILED = "detailed",  # 返回完整信息，包括 ID 等用于后续工具调用
    CONCISE = "concise"     # 只返回主要内容，省略技术标识符
}
```

以 Slack threads 为例：
- **Detailed 响应**（206 tokens）：包含 thread_ts, channel_id, user_id → 可触发后续 tool calls
- **Concise 响应**（72 tokens）：只返回 thread 内容 → 节省 2/3 tokens

### 原则四：优化 Token 效率（Optimizing tool responses for token efficiency）

**工具响应的大小对 Agent 性能有直接影响。**

Anthropic 建议对任何可能大量返回内容的工具实现：
- 分页（Pagination）
- 范围选择（Range selection）
- 过滤（Filtering）
- 截断（Truncation）——Claude Code 默认限制工具响应在 25,000 tokens

**截断时的关键做法**：在截断响应中添加引导性指令，告诉 Agent 正确的搜索策略。例如：「If you need to find specific information, try making targeted searches rather than broad ones.」

**错误响应设计**：

| 类型 | 示例 | 效果 |
|------|------|------|
| 无用的错误 | `Error: 500, Stack trace: ...` | Agent 无法从中学习 |
| 有用的错误 | `That didn't work. Try narrowing your search to a specific date range or customer ID.` | 引导 Agent 修正行为 |

---

## 四、元循环：工具改进的工具体系

Anthropic 方法论最深刻的地方在于它的**自反性**：用 Agent 来构建和改进 Agent 的工具。

```
┌─────────────────────────────────────────────────────┐
│                   工具迭代循环                       │
│                                                     │
│  构建原型 → 运行评估 → 分析结果 → 优化工具           │
│       ↑                                              │
│       └──────── Agent 分析 transcript ─────────────┘│
└─────────────────────────────────────────────────────┘
```

这个循环的关键是：
1. **评估任务**必须 grounded in real-world uses，不能过于简化
2. **Agent 的 reasoning 和 feedback**（而非只看 accuracy）才是真正的改进线索
3. **工具的「不说」比「说」更重要**——Agent 省略的信息往往比包含的更重要

---

## 五、工程实践要点

### 5.1 工具响应格式的选择

没有「一刀切」的最佳格式。JSON、XML、Markdown 各有优劣，取决于：
- Agent 训练的格式倾向
- 具体任务类型
- 工具复杂程度

Anthropic 的建议：**根据你自己的评估结果选择**，不要假设某种格式「总是最好」。

### 5.2 评估的 held-out test set

Anthropic 强调用 held-out test set 避免 overfit 到训练评估集。结果显示，即使「专家」手工写的工具实现，也能被 Agent 通过评估和迭代进一步优化。

### 5.3 工具描述的 Prompt Engineering

工具描述和规格是 Agent 理解工具的主要来源。Anthropic 建议：
- 提供具体的示例（examples）
- 明确工具的目的和使用场景
- 说明参数格式要求

---

## 六、核心判断：笔者认为

**1. 工具设计是 2026 年 Agent 工程的关键瓶颈。**

基础模型能力已不是主要限制，如何设计让 Agent 能成功使用的工具，才是决定 Agent 实际可用性的核心。这与「MCP 协议」的热潮不同——协议解决的是互联互通问题，工具设计解决的是「Agent 能否真正完成任务」的问题。

**2. 工具评估是整个方法论的核心，也是最容易忽略的环节。**

大多数团队会花时间构建工具，但不会花时间系统性地评估工具对 Agent 的有效性。Anthropic 的方法论证明：**没有评估的迭代是盲目的，评估驱动的发展才是可持续的**。

**3. 工具的「少而精」优于「多而全」。**

给 Agent 提供 10 个精心设计、目标明确的工具，优于提供 50 个功能重叠、设计粗糙的工具。Namespacing 和工具合并是控制工具数量的两个主要手段。

**4. Agent 驱动的工具改进不是噱头，是实际的工程实践。**

Anthropic 坦诚地说这篇文章的大部分建议就是这样来的。这证明了 Agent 不仅能完成任务，还能参与工程过程本身——这是 2026 年 Agent 工程的重要里程碑。

---

## 七、关联项目

| 项目 | Stars | 说明 |
|------|-------|------|
| [anthropic-experimental/sandbox-runtime](https://github.com/anthropic-experimental/sandbox-runtime) | — | Anthropic 开源的沙箱运行时，与工具安全的工程实践直接相关 |
| [modelcontextprotocol/sdk](https://github.com/modelcontextprotocol/sdk) | — | MCP 协议的官方 SDK，工具开发的协议层基础 |

---

## 参考来源

- [Writing effective tools for AI agents—using AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)（Anthropic Engineering）
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/docs/getting-started/intro)
- [Claude Code Sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing)

---

*本文是「Agent 工程方法论」系列的第 N 篇，探讨工具设计原则与评估驱动开发在 AI Agent 领域的实践。*