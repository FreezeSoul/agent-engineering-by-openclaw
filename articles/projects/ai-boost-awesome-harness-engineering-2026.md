# awesome-harness-engineering：第一个专门为 Agent Harness 整理的知识库

> **推荐理由**：不是又一个 awesome list，这是一个专门回答「如何设计让 Agent 可靠工作的环境」的专家级知识聚合。

---

## 这个项目解决了什么问题

Harness Engineering（harness 工程）是一个正在快速成形的新学科——它回答的问题不是「模型有多强」，而是「如何设计让模型能稳定、可靠工作的 scaffold」。

这个领域有个特点：知识碎片化分布在论文、博客、GitHub 仓库里，没人把它们整合成一个结构化的地图。

awesome-harness-engineering 做了这件事：**把 harness 工程的核心能力域（context delivery、tool interface、verification loop、memory system、sandbox 等）整理成树状知识结构，并附上每个领域的代表性工具和参考资源**。

---

## 核心结构

项目的知识组织遵循 Agent harness 的能力架构：

```
📐 Foundations          ← 基础概念：什么是 harness，为什么需要它
🔄 Agent Loop           ← Agent 循环的设计模式
🗺️ Planning & Decomposition ← 任务分解与规划
📦 Context Delivery     ← 上下文传递与压缩
🔧 Tool Design          ← 工具接口设计
🔌 Skills & MCP         ← 技能封装与 MCP 协议
🛡️ Permissions          ← 权限与授权
🧠 Memory & State       ← 记忆与状态管理
⚙️ Orchestration        ← 任务编排与多 Agent 协作
✔️ Verification        ← 验证与 CI 集成
👁️ Observability        ← 可观测性与 tracing
🐛 Debugging            ← 开发者工具链
🔒 Security & Sandbox   ← 安全与沙箱
✅ Evals                ← 评测与基准测试
📋 Templates            ← 可用模板
```

每一条目都直接对应了 Agent 工程师在实际项目中需要解决的真实问题。

---

## 为什么值得关注

### 1. 第一个专注「harness」而非「model」的 curated list

目前 GitHub 上有 LangChain 生态的 awesome-list，有 AI Agent 框架的 awesome-list，但没有一个专门从 **scaffold design** 角度整合资源的。这个项目填补了这个空白。

### 2. 知识结构直接映射工程问题

当你遇到「如何设计工具的边界」「如何做长程任务的 context 压缩」「verification loop 的标准设计」这些问题时，这个 list 的分类本身就是导航图。

### 3. 紧跟 OpenAI Harness Engineering 潮流

这个项目在 2026 年 3 月创建，正好对应 OpenAI 发布 Harness Engineering 博客的时间点。它的分类体系和术语与 OpenAI/Anthropic 的官方文档高度一致，意味着它的维护者在跟踪这个领域的核心进展。

---

## 关键引用

项目 README 中对 Harness Engineering 的定义：

> "Harness engineering is the discipline of designing the scaffolding — context delivery, tool interfaces, planning artifacts, verification loops, memory systems, and sandboxes — that surrounds an AI agent and determines whether it succeeds or fails on real tasks."

以及一条重要的设计哲学：

> "Every component here exists because the model can't do it alone — and the best harnesses are designed knowing those components will become unnecessary as models improve."

这条注释揭示了一个本质洞察：**最好的 harness 设计，不是让模型做更多，而是在模型能力边界扩张时，让新增的能力被可靠地使用**。这不是在给模型补短板，而是在为模型的进化准备容器。

---

## 与本轮 Article 的关联

本轮的 Article（[Agent Harness Engineering：为什么模型不是决定性因素](openai-harness-engineering-philosophy-2026.md)）分析了 OpenAI Harness Engineering 的核心哲学：**环境比模型更重要，harness 的质量是 2026 年 Agent 工程的核心竞争力**。

awesome-harness-engineering 是这个论点的「知识基础设施」——它把 harness 工程的核心能力域整理成结构化地图，为 Agent 工程师提供了一站式的参考资源。两者共同构成「理念 → 工具地图」的完整闭环。

---

## 数据快照

| 指标 | 值 |
|------|---|
| Stars | 970+ |
| 创建时间 | 2026-03-29 |
| 最近更新 | 2026-05-18 |
| 语言 | Python（主要是知识整理，非代码项目）|
| 主要贡献者 | ai-boost, noahbenjamin1994, claude |

---

*归档目录：`articles/projects/` — 关联 Article：[Agent Harness Engineering：为什么模型不是决定性因素](../fundamentals/openai-harness-engineering-philosophy-2026.md)*