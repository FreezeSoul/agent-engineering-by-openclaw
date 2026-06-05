# Supermemory：AI 时代的记忆控制平面，用 6 行代码给 Agent 装上记忆

> GitHub: [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)
> 
> 本文是 [ChatGPT Dreaming 记忆系统解析](../context-memory/openai-chatgpt-dreaming-background-memory-synthesis-2026.md) 的实证案例——OpenAI 解决了"ChatGPT 怎么记住你"的问题，Supermemory 则把相同理念产品化为开发者可用的开源记忆层。

---

## 核心命题

**Supermemory 干了一件事：让任何 AI Agent 在对话之间保持记忆，且不需要你配置向量数据库、embedding管道或分块策略——6 行代码就够。**

---

## 为什么这个项目值得关注

AI Agent 的记忆问题是2026 年最被讨论的工程难题之一。

当你让 Claude Code 或 Cursor 去完成一个跨周的项目时，你会发现：第二周的 Agent 完全不记得第一周你们讨论过什么技术选型。当你让 ChatGPT 帮你规划旅行时，它不记得你三周前提过自己是素食者。

这不是模型的问题——是**记忆层缺失**的问题。

大多数现有方案的复杂度：

```
传统 RAG 记忆方案：
1. 配置向量数据库（Pincone / Qdrant / Weaviate）
2. 设计 embedding 管道
3. 选择 chunk策略（句子级？段落级？）
4. 写 retrieval 逻辑
5. 写 memory update 逻辑
6. 处理时效性和矛盾
```

Supermemory 的复杂度：

```javascript
import { createMemory } from 'supermemory'

const memory = createMemory()
await memory.add(conversation)
const context = await memory.get(userId)
```

**6 行代码获得生产级的记忆系统**——这不是噱头，是工程简化。

---

## 核心能力

### 🧠 Memory：自动事实提取

Supermemory 不只是存储对话——它从对话中**提取事实**，处理：

- **时序变化**：用户说"我下个月要去东京"，Supermemory 会自动在时间到达时更新为"用户去过东京"
- **矛盾处理**：用户前后说法矛盾？Supermemory 有内置的矛盾检测和解决机制
- **自动遗忘**：过期的、不再相关的信息会被自然遗忘，不需要手动维护

### 👤 User Profiles：50ms 获取用户上下文

> *"Auto-maintained user context — stable facts + recent activity. One call, ~50ms."*

每次用户查询只需要约 50ms 就能获取该用户的完整上下文。这对于需要实时响应用户请求的 Agent 场景至关重要。

### 🔍 Hybrid Search：RAG + Memory 一次搞定

> *"RAG + Memory in a single query. Knowledge base docs and personalized context together."*

大多数 RAG 系统的局限是：知识库检索和用户个人上下文是分离的。Supermemory 在一次查询中同时返回：
- 知识库中的相关文档
- 用户个人上下文中的相关记忆

### 🔌 Connectors：开箱即用的数据源

Supermemory 提供了开箱即用的连接器：
- Google Drive · Gmail · Notion · OneDrive · GitHub
- 支持实时 webhook 同步

这意味着**你的 Gmail 和 Notion 自动成为 Agent 的记忆来源**。

### 📄 Multi-modal Extractors

支持 PDF、图像（OCR）、视频（转录）、代码（AST-aware 分块）——不需要手动处理各种格式的文档。

---

## Benchmarks：#1 on 三大记忆评估

这是 Supermemory 最硬的部分——它在三个主要 AI 记忆评估基准上都排名第一：

| 基准 | 说明 | Supermemory 排名 |
|------|------|-----------------|
| [LongMemEval](https://github.com/xiaowu0162/LongMemEval) | 长程记忆评估 | **#1** |
| [LoCoMo](https://github.com/snap-research/locomo) | 本地对比记忆评估 | **#1** |
| [ConvoMem](https://github.com/Salesforce/ConvoMem) | 对话记忆评估 | **#1** |

三个基准同时第一，说明 Supermemory 的记忆系统不是偏科生——在长程记忆、本地上下文记忆、对话级记忆三个维度都是 S 级。

---

## 两种使用方式

### 方式一：开箱即用的 App

不想写代码？Supermemory 提供了消费者级应用：

- 浏览器扩展
- AI助手插件（MCP server）
- App（免费使用）

安装后，任何兼容的 AI 助手都能获得持久记忆。**一次安装，AI 永远记得你**。

### 方式二：开发者 API

```bash
# npm
npm install supermemory

# pip
pip install supermemory
```

不需要配置向量数据库，不需要设计 embedding 管道。Supermemory 的 API 设计理念是：**开发者只需要关心对话，不需要关心记忆工程**。

---

## 与 Dreaming 理念的关联

本文的 Article 描述了 OpenAI 的 Dreaming 记忆系统如何用**后台合成**解决记忆时效性问题。

Supermemory 在工程实现层面呼应了这个思路：

| Dreaming (OpenAI) | Supermemory (开源实现) |
|------------------|----------------------|
| 后台合成进程 | 自动事实提取 + 时序更新 |
| 记忆状态而非记忆列表 | 动态用户 profile 而非静态存储 |
| 时效性自动维护 | 矛盾检测 + 自动遗忘 |
| 评估驱动迭代 | 三项 benchmark 验证 |

Dreaming 是闭源产品在数亿用户规模下的实现。Supermemory 是相同工程理念在开源、开发者导向场景下的实现。

---

## 适用场景

**适合用 Supermemory**：
- 跨会话的 AI Coding Agent（Claude Code / Cursor 等）
- 需要个性化上下文的 Chatbot
- 长期项目助手（周级/月级任务）
- 多数据源集成的 AI 应用（Gmail + Notion + Drive → Agent 记忆）

**不太适合**：
- 单会话一次性任务（没有跨会话记忆需求）
- 对数据隐私有极端要求（目前是云端方案）
- 需要完全自定义的记忆策略（Supermemory 屏蔽了底层复杂度）

---

## 原文引用

> *"Your AI forgets everything between conversations. Supermemory fixes that."*

> *"It automatically learns from conversations, extracts facts, builds user profiles, handles knowledge updates and contradictions, forgets expired information, and delivers the right context at the right time."*

> *"No vector DB config. No embedding pipelines. No chunking strategies."*

---

## 结论

Supermemory 的核心价值主张是**记忆工程的民主化**——把原本只有大厂能做的后台记忆合成，做成开发者6 行代码就能用的 API。

对于正在用 Claude Code / Cursor 等工具做生产的开发者，Supermemory 提供了缺失的记忆层。对于正在构建 AI Agent 的团队，Supermemory 提供了经过三项 benchmark 验证的记忆引擎。

配合本文的 [Dreaming 架构解析](../context-memory/openai-chatgpt-dreaming-background-memory-synthesis-2026.md)，你可以完整理解：为什么记忆系统需要从"存储"演进到"合成"，以及如何在你的 Agent 中实现它。

---

*推荐关联：[ChatGPT Dreaming 背景记忆合成架构解析](../context-memory/openai-chatgpt-dreaming-background-memory-synthesis-2026.md)*