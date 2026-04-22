# LangChain Blog: Your Harness, Your Memory

> **来源**：[LangChain Blog - Your Harness, Your Memory](https://www.langchain.com/blog/your-harness-your-memory)（Harrison Chase，2026-04-11）
> **主题**：Agent Harness 与 Memory 的共生关系；封闭 Harness 如何造成 Memory 锁定；为什么开放 Harness 是 Agent 系统的基础设施选择
> **适用场景**：Harness 选型决策；Agent 架构设计；Memory 系统建设策略

---

## 核心论点：Harness 与 Memory 不可分割

LangChain CEO Harrison Chase 在这篇博客中提出了一个在 Agent 工程界被长期忽视的结构性问题：

**Memory 不是 Agent 的插件，而是 Harness 的核心职责。如果你不拥有 Harness，你就不拥有 Memory。**

这是一个架构层面的判断，而非供应商偏好。它来自于对当前 Agent 系统实际运作方式的严格分析。

---

## 为什么说 Memory 不是插件

行业里有一种错误的思维模型：把 Memory 当作一个可以「插入」任意 Agent 的独立服务，就像给 API 添加缓存层一样。这种思维在 2026 年的 Agent 系统中是错误的。

Sarah Wooders 提出的类比足够精准：**「问如何给 Agent Harness 插入 Memory，就像问如何给汽车插入驾驶一样。」**

Memory 不是一个功能模块，而是一种**系统级的横切关注点**，弥散在 Harness 的每一个设计决策中：

| Memory 相关设计决策 | 实现方式 |
|---------------------|---------|
| AGENTS.md / CLAUDE.md 如何加载到上下文 | Harness 读取文件 → 注入 System Prompt |
| Skill 元数据如何展示给 Agent | System Message 中的结构化描述 |
| Agent 能否修改自己的 System Prompt | Harness 的指令更新机制 |
| 哪些信息在压缩（Compaction）后存活 | Harness 的上下文压缩策略 |
| 对话历史是否可查询 | Harness 的状态管理后端 |
| Memory 元数据如何呈现给 Agent | Harness 的 Memory 界面设计 |
| 当前工作目录如何表征 | Harness 的文件系统抽象层 |

这些决策每一个都深深地嵌入在 Harness 的实现中。如果你的 Harness 是封闭的，这些设计决策就对你是黑箱，Memory 的行为方式也随之成为黑箱。

---

## 三种封闭程度与 Memory 锁定的关系

Harrison Chase 将封闭 Harness 按严重程度分成了三个层级：

### 层级一：状态存储在服务商服务器（Mild）

典型案例：OpenAI Responses API、Anthropic 服务端压缩（Server-side Compaction）。

特征：你的对话状态存在第三方服务器上。如果你想切换模型或换供应商，之前的线程无法迁移，你的 Memory 实际上被绑定在这个供应商的服务上。

影响：中等。至少 Memory 的结构和行为对你仍然是可见的（通过 API 响应）。

### 层级二：封闭 Harness 但本地有产物（Bad）

典型案例：Claude Agent SDK（底层使用 Claude Code，代码非开源）。

特征：Harness 在客户端与 Memory 交互，生成某种产物（文件、结构化数据）。但这些产物的格式、结构和用法对外部是完全不透明的。你无法将这些产物迁移到另一个 Harness，无法跨平台复用你的 Memory 积累。

影响：严重。你不知道 Memory 是如何被管理、压缩、检索的，你对 Memory 的演进没有任何控制力。

### 层级三：整个 Harness + Memory 都在 API 背后（Worst）

典型案例：Anthropic Claude Managed Agents——整个 Harness 和 Long-term Memory 全部封装在 API 之后。

特征：
- 你不知道 Harness 的实现（因此不知道怎么用 Memory）
- 你不拥有 Memory 的任何部分
- 供应商控制 Memory 的公开程度和访问方式
- Memory 成为平台锁定的核心手段

影响是系统性的：当整个 Memory 都在 API 后面，供应商就有了单一模型无法提供的锁定效应。用户切换成本不只是「重新调优 Prompt」，而是丢失所有积累的交互偏好、历史学习、个性化数据。

---

## 模型厂商为何积极推动封闭化

Harrison Chase 指出了这背后的经济逻辑：**Memory 创造了模型厂商无法通过模型本身获得的差异化。**

当前模型 API 的同质化程度很高——切换成本低，各家性能接近。模型厂商从模型本身获得的竞争优势是有限的。

但 Memory 不一样。Memory 积累的是**专有数据集**——用户交互数据、偏好模式、使用习惯。这些数据可以训练出更好的个性化体验，形成数据飞轮，并创造真正的切换成本。

Harrison Chase 举了一个自己的例子：他有一个基于 Fleet 平台模板构建的邮件助手，运行了几个月积累了大量 Memory（偏好、语气、工作习惯）。某天 Agent 被意外删除，他试图从同一个模板重建——结果体验断崖式下降，需要重新教会它所有偏好。

这个故事说明：**Memory 是 Agent 价值的核心载体，是让 Agent 从「通用工具」变成「个性化助手」的关键资产。**

模型厂商深知这一点。即使 Codex 是开源的，它生成的压缩摘要（Compaction Summary）是加密的且只能在 OpenAI 生态内使用——即使你用了开源工具，你的 Memory 积累仍然被锁在生态内。

---

## 开放 Harness 的战略必要性

Harrison Chase 提出了一个原则性的主张：**Memory（以及生产它的 Harness）必须与模型提供商分离。**

这个主张的核心理由是**保持可选性**（Preserving Optionality）：

```
当前模型能力快速迭代，各家都有自己的强项。
如果你的 Memory 被锁定在某个封闭 Harness，
你就失去了在模型能力竞争中灵活切换的能力。
```

开放 Harness 意味着：
1. **Memory 数据自己控制**：存储格式、访问接口、压缩策略都是你自己定义的
2. **跨模型迁移能力**：可以用同一个 Memory 基础在不同模型之间切换
3. **Memory 积累的真正价值**：你建立的是一个独立于模型供应商的专有数据集

Harrison Chase 特别指出 LangChain 正在建设 Deep Agents，一个开放 Memory + 开放 Harness 的 Agent 系统。这既是商业判断，也是技术判断——在他们看来，不开放的 Memory 在长期会给整个 Agent 生态带来系统性的锁定风险。

---

## 对 Agent 工程实践的含义

### 对 Harness 选型的影响

评估一个 Agent 框架/Harness 时，Memory 的可控制性应该是核心评估维度之一：

| 维度 | 开放 Harness | 封闭 Harness |
|------|--------------|--------------|
| Memory 存储格式 | 可知、可迁移 | 黑箱 |
| 压缩策略 | 可配置 | 供应商决定 |
| 跨平台迁移 | 支持 | 不支持 |
| 切换模型成本 | 低 | 高（含 Memory 损失）|
| Memory 积累价值 | 保留在自己系统 | 积累在供应商系统 |

### 对 Memory 架构设计的影响

在 Memory 系统的设计中，需要明确地将「Memory」作为 Harness 设计的一部分来考虑，而不是作为一个独立层：

1. **Compaction 策略即 Memory 策略**：上下文压缩时保留什么、丢弃什么，直接决定 Memory 的质量
2. **Memory 检索接口即 Harness 接口**：Memory 如何暴露给 Agent，决定了 Agent 能如何利用历史
3. **跨会话状态即 Memory 边界**：是否跨会话、跨任务保留状态，是 Memory 设计的核心决策

### 对 Agent 提供商的影响

如果你在构建给客户使用的 Agent 服务，Harrison Chase 的建议是：**给你的客户所有权，而不是给自己锁定。**

客户数据（Memory）应该是客户的资产。平台通过模型能力、服务质量和使用体验来维持客户，而不是通过 Memory 锁定。这既是更健康的商业模式，也是更符合用户利益的设计。

---

## 笔者评注：锁定是真实存在的，但开放也有代价

Harrison Chase 的论点从商业逻辑和技术架构两个层面都是成立的。Memory 与 Harness 的深度耦合是一个当前的技术现实，而不是理论假设。

但也必须指出：**开放 Harness 同样有代价**。维护一套可迁移的 Memory 系统需要额外的工程投入；开放存储格式意味着你要承担 Schema 演进的兼容性负担；跨模型 Memory 复用本身在技术上也存在挑战（不同模型的 Context 压缩方式不同，Memory 表示不一定完全通用）。

现实中的选型往往是：**对于个人或小团队开发者，封闭 Harness 的易用性可能超过 Memory 可控性的价值；对于企业级应用，Memory 锁定是一个需要认真对待的战略风险。**

关键的是把这个权衡纳入决策框架，而不是在无意识中被锁定。

---

## 参考文献

- [Your Harness, Your Memory](https://www.langchain.com/blog/your-harness-your-memory)（LangChain Blog，Harrison Chase，2026-04-11）— 本文核心论点来源
- [The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/)（LangChain Blog）— Agent Harness 结构解析
- Sarah Wooders["Memory isn't a plugin, it's the harness"](https://x.com/sarahwooders/status/2040121230473457921)（X/Twitter，2026）— Memory 与 Harness 不可分割的核心论据
- [Anthropic Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)（Anthropic 官方文档）— 封闭 Harness 案例
