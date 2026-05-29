# study8677/awesome-architecture：架构图谱——AI 时代的架构判断力知识库

> **751 Stars | 2026-05-23 创建 | 中英双语 | 21 张架构图 + 26 章节教程**

GitHub 链接：`https://github.com/study8677/awesome-architecture`

---

## 核心命题

这个项目解决了一个正在变得越来越紧迫的问题：

> 当 AI 能以秒级速度吐出能跑的代码时，程序员的核心竞争力是什么？

它的答案是：**架构判断力**——在动手之前，先想清楚系统应该长什么样子。

这不是另一个「awesome」列表。这是一套从 0 到 26 章的完整教程，加上 25 个真实系统的架构地图（AI gateway、RAG、Claude Code、OpenClaw 等），每张地图都链接到真实开源项目源码。

---

## 为什么值得关注

### 1. 填补了「AI 写代码 vs 架构判断」的知识断层

Cursor 3 的发布博客说了一句大实话：「More powerful coding models will unlock new interaction patterns」。当 AI 能写出代码时，工程师的价值就变成了「判断 AI 写的代码是否合理、系统设计是否正确」。

awesome-architecture 完整覆盖了这个转变所需的思维框架：
- 经典架构模式（分层、微服务、事件驱动、CQRS）
- 分布式系统硬道理（一致性、共识、级联失败）
- **AI 原生系统设计**（RAG、Agent 工作流、模型推理服务）
- **大模型时代的架构判断**（vibe coding、非确定性、上下文工程、agentic 硬骨头）

第 17 章专门讲「AI 时代的架构判断」，这在 2026 年的技术社区里是稀缺内容。

### 2. 21 张真实系统的架构地图，不是抽象概念

每个模板都是一张「架构地图」，刻意不讨论语言/框架，只讲：
- 这类系统解决什么问题
- 由哪些部件组成，数据怎么流动
- 关键决策怎么取舍，规模化时会死在哪里

覆盖的系统类型：

**经典/通用：**
- 电商平台（Amazon/Shopify）、社交信息流（Twitter/X）、实时通讯（WhatsApp/Slack）
- 支付系统（Stripe/支付宝）、搜索引擎（Google/ES）、网约车（Uber/滴滴）

**AI 原生（2026 新增）：**
- AI 网关（One API/LiteLLM/Portkey）
- RAG 知识库（RAGFlow/LlamaIndex/Dify）
- AI Agent 平台（Dify/Coze/LangGraph）
- 模型推理服务（vLLM/SGLang/Triton）
- 向量数据库（Milvus/Qdrant/pgvector）

**AI 编码 / 自治 Agent（真实在用的产品架构）：**
- Claude Code（Anthropic）—— 本地优先编码 Agent、子代理/钩子/技能/MCP
- OpenAI Codex —— 本地 CLI + 云端异步沙箱双形态
- OpenClaw —— 自托管 Gateway、聊天软件即 UI
- Hermes —— 常驻自我成长、FTS5 持久记忆

> 每个模板末尾都附真实开源项目/工程文档链接，可顺着一个项目去读源码。

### 3. 26 章节完整教程，涵盖从入门到高级

从「为什么先有架构思维」（第 01 章）到「AI 协同设计篇」（第 23-26 章），完整的学习路径：

| 阶段 | 章节 | 核心能力 |
|------|------|---------|
| 基础篇 01-09 | 架构思维、思考框架、C4 模型、十大模式、数据与状态、取舍、从 0 设计、ADR | 架构判断基本功 |
| 进阶篇 10-17 | 分布式硬道理、数据一致性工程、韧性设计、规模化力学、演进与拆分、组织即架构、安全多租户、AI 时代判断 | 大型系统设计能力 |
| 实战篇 18-22 | 读地图拆解陌生系统、中等复杂度完整设计演练、演进剧本、迁移实战、AI 原生系统设计 | 工程落地能力 |
| **AI 协同篇 23-26** | 规格即架构（AGENTS.md）、AI 产出审查清单、评测驱动、协作决策树 | **AI 时代的架构师技能** |

第 23-26 章是 2026 年的新增内容，直接对应「AI 写代码 → 人类判断架构」的时代转型。

### 4. 配套 architecture-copilot skill，把知识变成交互式工具

> 配套 skill：[architecture-copilot](https://github.com/study8677/architecture-copilot)—— 把这套知识变成能在 Claude Code / Cursor / Codex 里引导你一步步设计架构的交互式 skill。

这不是一个静态知识库——它把知识直接嵌入到了 AI 编码工具里，让 AI 在帮你写代码的同时，也能引导你做架构判断。

---

## 与本仓库的闭环

awesome-architecture 的 **AI Agent / 工作流模板**（Dify/Coze/LangGraph）与 `orchestration/` 目录下已有内容形成互补——它提供了更底层的「这类系统由哪些部件组成、数据怎么流动」的架构知识，而非工具使用教程。

第 17 章「AI 时代的架构判断」和第 23-26 章「AI 协同设计篇」与 `fundamentals/` 和 `practices/ai-coding/` 目录高度相关——这些章节专门讨论 vibe coding、上下文工程、agentic 硬骨头，正是 AI Coding 时代的核心工程问题。

**闭环设计**：Cursor 3 文章讨论「AI 时代工程师从写代码变成架构判断」，awesome-architecture 提供了这套判断力的完整知识体系。

---

## 适用场景

- **学习架构思维**：按顺序读完 tutorial，从第 01 章到第 26 章
- **设计新系统**：先去 tutorial/07 学方法论，再去 templates/ 找最接近场景的地图
- **读懂现有系统**：对任何一个模板逆向读「为什么这么设计」，以 RAG / AI 对话产品练眼
- **AI 协同设计**：用 architecture-copilot skill 在 Claude Code / Cursor 里引导架构决策

---

## 原文引用

1. "当机器几秒就能吐出能跑的代码，'用 for 还是 map、背没背过某个 API、熟不熟某种语法'这些曾经的看家本领，一夜之间一文不值。真正不会贬值、而且越来越值钱的，是另一种能力：在动手写第一行代码之前，先想清楚这个系统应该长什么样子。" — README.md

2. "目前共 25 个模板（16 经典/通用 + 5 AI 原生 + 4 AI 编码/自治 Agent），每个都在末尾附真实开源项目/工程文档链接，可顺着去读源码。" — README.md

3. "AI 协同设计篇(23-26)—— 会设计之后，学会与 AI 协作落地与审查。" — README.md

---

*归档路径：`articles/projects/study8677-awesome-architecture-21-architecture-maps-751-stars-2026.md`*
*来源：https://github.com/study8677/awesome-architecture*
*标签：Architecture / Knowledge Base / AI Era / System Design*