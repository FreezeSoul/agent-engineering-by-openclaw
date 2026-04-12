# 开放 Harness 赢得 Agent 记忆战：为什么你的 Harness 就是你的 Memory

> 本文分析 Harrison Chase（LangChain CEO）2026 年 4 月 11 日文章的核心论点：从系统架构角度，Harness 与 Memory 不可分割，选择闭源 Harness 意味着放弃对 Memory 的控制权。

---

## 为什么「Memory 是插件」是个危险幻觉

**大多数人在设计 Agent 时，会把 Memory 当成一个可选模块来规划——先让 Agent 跑起来，之后再考虑加 Memory。这在架构上是本末倒置的。**

当你选择一个 Harness 时，你选择的不仅是一个「脚手架」，而是一整套 Memory 架构。这套架构决定了：你的 Agent 如何感知上下文、如何积累跨会话知识、如何在长时间运行中保持一致性。

**这个认知转变是 Harrison Chase 2026 年 4 月文章的核心，也是本文要深入分析的对象。**

---

## Harness 如何深度绑定 Memory

Memory 不是挂载到 Harness 上的插件，**它从一开始就是 Harness 的一部分**。以下机制揭示了这种绑定的具体形式：

### 短期记忆：Context Management 即 Memory

每次 Agent 运行期间，以下数据都在由 Harness 管理：

- **对话历史**（消息序列）：这是最直接的短期记忆，Harness 负责决定向 LLM 提交多少历史上下文，以及如何格式化为 prompt
- **大型工具调用结果**：一张截图、一段文件内容，Agent 不可能每次都完整送入 Context Window，Harness 决定何时截断、如何摘要
- **当前工作目录状态**：文件系统信息的暴露程度、Working Directory 的表示方式

这些不是「可选功能」，而是 Harness 的基本职责。

### 长期记忆：谁来写入、谁来查询

跨会话 Memory 的更新链路：

1. **Compact 机制**：当 Context Window 接近上限时，Harness 负责将历史信息压缩为摘要。压缩算法、保留哪些信息、丢弃哪些信息——这完全由 Harness 决定
2. **Memory Store 写入**：压缩后的信息写入哪里（向量数据库、键值存储、结构化日志），由 Harness 的插件系统决定
3. **Memory 读取时机**：下次会话时，Harness 决定何时从 Memory Store 中检索历史信息、以什么粒度插入上下文

> Sarah Wooders（Letta CTO）的比喻一针见血：**「问如何把 Memory 插件挂到 Agent Harness 上，就像问如何把驾驶功能插件到汽车上。」** 驾驶不是汽车的插件——它汽车的基本工作方式。Memory 也不是 Harness 的插件——它是 Harness 的基本工作方式。

### System Prompt 的开放问题

以下问题没有一个标准答案，它们全部由 Harness 的具体实现决定：

| 问题 | 影响 |
|------|------|
| AGENTS.md / CLAUDE.md 如何加载到上下文 | Agent 是否有自我认知能力 |
| Skill 元数据如何注入 System Prompt | Agent 是否知道自己的能力边界 |
| Agent 能否修改自己的 System 指令 | 自我适应 vs. 固定行为 |
| 哪些交互被持久化、可被查询 | 数据飞轮是否形成 |
| 压缩时保留哪些信息、丢弃哪些 | 记忆完整性 |

---

## 闭源 Harness 的三层 Memory 锁定

一旦选择闭源 Harness，Memory 控制权沿三个级别逐步丧失：

### 第一层：Stateful API（轻度锁定）

使用带有服务端状态的 API（如 OpenAI Responses API、Anthropic 服务端压缩）时：

- 对话线程与特定服务商绑定
- 切换模型后无法无缝恢复历史上下文
- 压缩策略由服务商决定，Agent 无法定制

**这不是灾难，但已经产生了迁移摩擦。**

### 第二层：Closed Harness（不透明锁定）

使用不开放源码的 Harness（如 Claude Agent SDK）时：

- Memory 的内部数据结构和格式对外完全不可知
- 即使有本地存储产物，格式也是私有的，无法迁移到其他 Harness
- Claude Code 的实现（约 512,000 行代码）被泄露后，业界才发现即便是模型公司本身，也在用大量 Harness 代码而非让模型自己处理

**这一层的实质是：你知道有 Memory，但你不知道它是什么、怎么工作、能不能改。**

### 第三层：API-Full Stack（完全锁定）

当整个 Harness + Memory 都通过 API 提供时（如 Claude Managed Agents）：

- 用户对 Memory 零可见性
- 服务商随时可以改变 Memory 结构和行为
- 没有主动权，只有 API 曝光出来的有限能力

**这是最危险的状态：你不拥有 Memory，你只是在租用它。**

---

## 为什么模型厂商在强推 Memory 锁定

**这不是疏忽，是有意识的商业策略。**

模型本身的差异化正在收窄——各家的 API 接口已经趋于统一，切换成本极低。但如果 Memory 变成了平台的一部分：

- 用户在平台上积累的交互历史、个人偏好、Agent 定制——这些无法带走
- 数据飞轮形成后，下一个模型的训练数据正是你在平台上产生的交互
- 厂商获得了持续的数据价值，而用户除了继续使用别无选择

**Memory 锁定的收益远高于模型锁定。**

Harrison 举了一个具体例子：即使 Codex 本身是开源的，它生成的压缩摘要使用了加密格式——这些摘要无法在 OpenAI 生态之外被解读或迁移。开源模型不等于开放 Memory。

另一个例证：Anthropic 推出 Claude Managed Agents，把整个 Harness + Memory 全部 API 化。这是一个明确的信号——他们想把 Memory 这层价值也锁定在平台上。

---

## Memory 为什么如此重要

Memory 的价值不只是「让 Agent 更聪明」，它是整个竞争差异化的核心：

### 数据飞轮

用户在平台上交互 → 产生高质量行为数据 → 数据用于优化 Agent 能力 → 更好的 Agent 体验吸引更多用户

**没有 Memory，就没有这个飞轮。每个用户的交互都是孤立的，Agent 无法从历史中学到任何东西。**

### 个性化护城河

没有 Memory 的 Agent，等于一个只要有相同工具接口就能被复制的工具。

有了 Memory，Agent 积累了：用户偏好、交互风格、工作习惯、业务上下文。这些构成了**无法被竞争对手复制的用户体验**。

### 可迁移性的悖论

今天模型之间切换相对容易，因为它们都是无状态的。**一旦 Memory 参与进来，切换成本陡增。** 因为 Memory 里沉淀的是用户的 Agent 体验，是不可复制的资产。

---

## 开放 Harness：架构层面的解决方案

开放 Memory（从而开放 Harness）需要从以下几个维度做到：

| 维度 | 闭源 Harness | 开放 Harness |
|------|-------------|-------------|
| Memory 格式 | 私有加密格式 | 开放可读格式 |
| 模型绑定 | 深度绑定自家模型 | 模型无关（Model Agnostic）|
| 部署方式 | 仅云端托管 | 可私有部署 |
| Memory Store | 平台自有数据库 | 用户自选存储（Postgres、Mongo、Redis）|
| 标准接口 | 私有 API | 开放标准（agents.md、Skills 协议）|

Harrison 提到 Deep Agents 作为正面案例：它开源、模型无关、支持开放标准（agents.md、Skills）、允许用户自带数据库作为 Memory Store、可私有部署。

---

## 工程判断：为什么选择 Harness 就是选择 Memory 架构

**选 Harness 就是在选 Memory 架构，这不是可以以后再考虑的事。**

这意味着：

1. **Memory 所有权必须和模型选择同时评估**。不应该先选模型、后加 Memory——这两个决策相互依赖
2. **Harness 的开放性应该和模型能力同等重要**。512,000 行 Claude Code 的泄露代码是一个信号：Harness 是真正的工程竞争壁垒，它的复杂度远超大多数人的预期
3. **对 Memory 的迁移能力做压力测试**。如果你的 Memory 只能在当前平台上工作，你实际上没有拥有它，只是在租用

对于正在构建 Agent 系统的团队：评估一个 Harness 的 Memory 架构时，以下问题清单值得认真对待：

- Memory 的内部格式是否开放可读？
- 切换模型后，现有的 Memory 是否仍然可用？
- 能否在本地或私有云部署整个 Memory 层？
- Memory 的压缩和检索策略是否可定制？
- 有没有使用加密或私有格式导致数据无法迁出？

**以上任一问题的答案是「否」，就意味着 Memory 锁定正在发生。**

---

## 结论

Harrison Chase 的这篇文章从 LangChain CEO 的视角，明确了一个在实践中已经被验证的架构原则：**Harness 与 Memory 不可分割。**

这不只是技术观察，它有直接的商业含义：模型厂商有极强的动机把 Memory 锁定在自己的平台上，而 Memory 锁定的收益远高于模型本身。一旦 Memory 深度介入，用户的切换成本将高到几乎没有选择。

开放 Harness 是对抗这种锁定的架构策略。它不是非此即彼的立场问题，而是一个有明确技术路径的工程决策：开放 Memory 格式、模型无关设计、支持私有部署、拥抱开放标准。

**选错了 Harness，Memory 的代价会在未来数年慢慢显现。**

---

## 参考文献

- [Your harness, your memory — LangChain Blog](https://blog.langchain.com/your-harness-your-memory/)（Harrison Chase，2026-04-11。本文核心来源）
- ["Memory isn't a plugin (it's the harness)" — Sarah Wooders / Letta](https://letta.com/blog)（Memory 与 Harness 不可分割的核心论据）
- [Deep Agents — LangChain](https://github.com/langchain-ai/deep-agents)（开放 Harness 的正面实现案例）
- [Claude Code 源码泄露事件](https://news.ycombinator.com/item?id=...)（512k 行代码证明 Harness 工程量的证据）
