# ChatGPT 是怎么做"梦"的：OpenAI 背景记忆合成架构解析

> 本文深度解析 OpenAI 2026年6月发布的 ChatGPT "Dreaming" 记忆系统，揭示如何在数亿用户、多年时间跨度下实现可扩展的个性化记忆。

---

## 核心命题

**Dreaming 不是"记住"，是"合成"——OpenAI 用后台进程持续重构用户记忆状态，解决了传统记忆系统的三个根本矛盾：时效性、正确性、可扩展性。**

---

## 背景：为什么记忆系统这么难

当我们讨论 AI Agent 的记忆时，大多数人想到的是"保存-读取"模式：用户说一句话，存到某个数据库，下次读取。

这个模型在原型阶段工作良好，但到了**生产规模**会立即崩溃：

- **时效性**：你说"我7月要去新加坡"，系统记住了。但7月过了，系统还认为你在新加坡
- **正确性**：记忆会过时、相互矛盾。手动维护的记忆清单很快变成误导性信息垃圾堆
- **可扩展性**：Saved Memories依赖强触发信号（"请记住我..."），大多数有价值的信息发生在自然对话中，从未被显式标记为"需要记忆"

ChatGPT 面对的是数百万人、多年的时间跨度——这个问题不在于"怎么存"，而在于**怎么让记忆保持鲜活**。

---

## Dreaming：三代记忆架构的演进

OpenAI 在博客中清晰描述了三年三代架构的演进：

### 2024：Saved Memories（手动记忆）

第一代记忆允许用户要求 ChatGPT 记住特定信息。这个系统的问题在实践中暴露无遗：

> *"Saved memories were only written during the conversation and relied on strong cues to decide when to trigger memory... interacting with this system could feel like talking to someone who took a few notes, but still forgot everything that wasn't written down."*

**核心缺陷**：必须显式触发 + 不会自动过期 + 不处理矛盾

### 2025：Dreaming V0（后台补充）

第二代引入了 Dreaming 的第一个版本——后台进程，从聊天历史中自动整理记忆：

> *"In contrast to saved memories, dreaming leverages a background process that allows ChatGPT to learn from many conversations and synthesize ChatGPT's memory state in order to always provide the freshest, most relevant context to your conversations."*

但 V0 从未打算作为独立记忆系统——它只是对 Saved Memories 的补充，解决过时问题。

### 2026：Dreaming V3（完整记忆系统）

第三代 Dreaming 是**完全可扩展的背景记忆合成系统**，解决了三个核心问题：

**1. 传送有用上下文**
你告诉 ChatGPT 一次的信息，在后续对话中自动可用。OpenAI 构建了专项 eval 来评估模型在需要回忆用户事实时是否正确利用了记忆。

**2. 遵循偏好和约束**
偏好有多种形式：
- 行为指令（"不要提起 Stan"）
- 个人偏好（"我是素食者"）
- 隐含偏好（"我住在旧金山附近" → 本地选项需要个性化）

**3. 随时间保持最新**

这是 Dreaming 最关键的工程贡献。传统记忆系统的问题：

> *"you tell ChatGPT 'I'm in Singapore and need a dinner recommendation for tonight.' Then, time passes, your trip ends, and you wonder why ChatGPT still thinks you're in Singapore."*

Dreaming V3 的解决方案：记忆随时间自动更新。当旅行结束后，"你即将去新加坡"自动演变为"你2026年7月去过新加坡"。用户回到家后，ChatGPT 重新提供基于家庭位置和时区的建议。

---

## 工程机制：Dreaming 的后台合成是怎么工作的

这是本文的核心价值——从原文碎片中还原 Dreaming 的工程实现。

### 不是"保存"，是"合成"

Dreaming 的关键洞察是：**记忆不是保存的，是合成的**。

传统的记忆思维：
```
用户输入 → 提取信息 → 存入记忆数据库 → 下次读取
```

Dreaming 的思维：
```
用户输入 → 后台进程持续扫描 → 跨对话综合记忆状态 → 实时提供最相关上下文
```

"合成"意味着：
- 不存在固定的"记忆列表"，只有**记忆状态**——一个持续重构的概率性知识表示
- 记忆内容来自**所有对话**的统计聚合，而非单次显式保存
- 时效性通过**时间感知的更新机制**自动维护，而非过期删除

### 评估框架：三个记忆目标的量化

OpenAI 建立了三个专项评估：

| 评估目标 | 描述 | 度量方式 |
|---------|------|--------|
| 上下文传送 | 是否正确回忆用户事实 | 事实回忆准确率 |
| 偏好遵循 | 是否正确应用素食等偏好 | 偏好敏感任务准确率 |
| 时效更新 | 是否随时间更新记忆 | 时间敏感场景正确率 |

对每一代架构（2024 Saved / 2025 V0 / 2026 V3）分别跑这三个 eval，Dreaming V3 在所有三个维度都显著优于前两代。

### 可扩展性：5x 计算效率提升是关键

Dreaming V3 最重要的工程突破不是算法改进，而是**计算效率**：

> *"Recent improvements reduced the compute required to serve dreaming to Free users by approximately 5x, making it possible to begin rolling out dreaming to Free users over the coming weeks."*

5x 的计算减少使得：
- 付费用户获得完整的高质量记忆合成
- 免费用户也能获得满足质量门槛的版本

这是典型的**成本控制驱动功能开放**——不是技术不能，是成本太高。现在成本下来了，免费用户也能用。

---

## 记忆状态可视化：Memory Summary Page

Dreaming 合成的记忆通过 Memory Summary Page 向用户展示：

- 用户可以看到 ChatGPT 对他们的认知摘要
- 可以添加或修改个人信息
- 可以指示 ChatGPT 应该在何时提起什么话题
- 也可以深入某个领域与模型对话

这是一个**双向记忆接口**——用户不只是记忆的被动接收者，也可以主动编辑记忆状态。

---

## 对 Agent 工程的意义

### 1. 记忆即合成，而非存储

Dreaming 颠覆了"记忆 = 数据库"的心智模型。对 Agent 工程而言，这意味着：

- **不要设计"记忆写入"逻辑**，而要设计"记忆合成"的后台进程
- **不要假设记忆是准确的**，而要假设记忆是概率性的，需要持续验证
- **时间维度必须内置于记忆系统**，而非事后处理过期

### 2. 评估驱动记忆迭代

OpenAI 的三代记忆演进是通过**明确的量化评估**推进的：

```
Eval: 上下文回忆 → 发现 V0 不够 → 改进 → V3 Eval: 偏好遵循 → 发现时效问题 → 改进时间感知 → V3
```

这不是一次设计定稿，而是评估驱动的迭代。这对 Agent 工程的方法论有直接指导意义：**你的记忆系统需要自己的 eval**。

### 3. 可扩展性是记忆系统的元问题

Dreaming 面临的核心挑战不是"怎么记住"，而是"怎么在数百万人、多年时间跨度下记住"。这意味着：

- 架构设计时需要问：**这个记忆方案在 1000 万用户下还能工作吗**
- 成本模型需要先行：**每用户记忆合成成本**需要持续优化
- 免费层和付费层可以有不同的记忆质量：**分层记忆质量**是商业可行策略

---

## 原文引用

> *"In contrast to saved memories, dreaming leverages a background process that allows ChatGPT to learn from many conversations and synthesize ChatGPT's memory state in order to always provide the freshest, most relevant context to your conversations."*

> *"Dreaming also makes it easier for memory to include context that occurs naturally in conversation, without relying on explicit requests to remember something."*

> *"Recent improvements reduced the compute required to serve dreaming to Free users by approximately 5x, making it possible to begin rolling out dreaming to Free users over the coming weeks."*

---

## 结论

Dreaming 的本质是**后台记忆合成引擎**——它不等待用户显式说"请记住"，而是在对话结束后持续分析、综合、更新用户记忆状态。

这对 Agent 工程的核心启示是：**记忆不是存储问题，是持续综合问题**。你的 Agent 需要一个 Dreaming 式的后台进程，而不是一个记忆数据库。

下一篇文章我们将介绍 Supermemory——一个将 Dreaming 理念产品化的开源记忆层项目。

---

*来源：[Dreaming: Better memory for a more helpful ChatGPT](https://openai.com/index/chatgpt-memory-dreaming)，OpenAI Research，2026年6月4日*