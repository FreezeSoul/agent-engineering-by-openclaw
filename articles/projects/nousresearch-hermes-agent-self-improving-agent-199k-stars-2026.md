---
title: NousResearch/hermes-agent — 自改进 Agent 的工程实现 2026
date: 2026-06-22
source: https://github.com/NousResearch/hermes-agent
author: Nous Research
tags: [hermes-agent, self-improving, skill-creation, memory, multi-agent, cross-session,NousResearch]
topics: [Self-Improving Agent, Skill Authoring, Cross-Session Memory, Agent Architecture, Autonomous Learning]
description: Hermes Agent 是 Nous Research 打造的自改进 AI Agent，199K Stars。核心特性：Agent 能在使用中自主创建、改进 Skills；跨会话 FTS5 搜索 + LLM 摘要实现长期记忆；任意模型支持；多平台部署（$5 VPS 到 GPU 集群）。MIT 许可证。
stars: 199350
license: MIT
license_verified: 2026-06-22 via GitHub API
created: 2025-07-22
last_pushed: 2026-06-22
cluster: harness
cluster_role: project
pair_article: articles/harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md
pair_theme: Self-Improving Skill Creation
round: 489
---

# NousResearch/hermes-agent：自改进 Agent 的工程实现

> 原文：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（GitHub，199K Stars，MIT 许可证）

## 核心命题

大多数 Agent 框架关注的是「如何让 Agent 执行任务」，而 Hermes Agent 关注的是「如何让 Agent 在执行任务的过程中变得更好」。这不是一个功能特性，而是一个根本性的架构选择——它意味着 Agent 必须有能力观察自己的行为、提取可复用的模式，并将其固化为 Skills。

## 一、Architecture：Skill 是 Agent 的第一等公民

Hermes Agent 的架构文档中有一句话值得反复咀嚼：

> "It's the only agent with a built-in learning loop — it creates skills from experience, improves them during use, nudges itself to persist knowledge"

这句话里的每一个动词都对应一个工程机制：
- **creates skills from experience** → Skill Authoring 模块
- **improves them during use** → 在线学习循环
- **nudges itself to persist knowledge** → 自驱动持久化

**笔者认为**：这三条机制，恰恰是当前大多数 Agent 框架缺失的。大多数框架把 Skill 视为静态配置，而 Hermes 把 Skill 视为动态演化的对象。这两种设计的差距，在短任务上不明显，在长时任务上会形成天壤之别。

## 二、Memory 架构：FTS5 + LLM 摘要的双层记忆

Hermes 的跨会话记忆系统是一个双层结构：

**第一层：FTS5 全文搜索**。每个会话的对话历史都被索引，支持语义相似性搜索。这意味着 Agent 可以通过自然语言查询找到历史上处理过的类似问题，而不只是依赖精确关键词匹配。

**第二层：LLM 摘要**。FTS5 搜索返回的原始对话片段太过冗长，Hermes 用 LLM 对其进行摘要，生成可快速回顾的「记忆概要」。这个摘要既是 Human 的记忆工具，也是 Agent 自己的「上下文压缩」机制。

README 原文：
> "FTS5 session search with LLM summarization for cross-session recall"

**笔者认为**：双层记忆架构解决了一个核心问题——上下文窗口的有限性。当 Agent 的上下文窗口快耗尽时，它需要把「正在做的事」交接给下一个会话。FTS5 确保能找到相关历史，LLM 摘要确保交接的内容是可理解的。这与 Anthropic 的「The session is not the context window」观点完全一致，只是 Hermes 用自己的方式实现了它。

## 三、Skill 自改进循环的工程细节

Hermes 的 Skill 自改进不是一次性的「生成并保存」，而是一个持续循环：

1. **观察阶段**：Agent 在执行任务时记录自己的行为轨迹
2. **提取阶段**：从轨迹中识别可复用的模式
3. **固化为 Skill**：将模式写成可执行的 Skill（SKILL.md 格式）
4. **使用中改进**：Skill 被后续任务调用时，Agent 会根据实际效果持续修正

README 中提到的 Honcho dialectic user modeling 是这个循环的「用户侧」补充——Agent 不只记住自己的行为，还记住用户的偏好和习惯，形成越来越个性化的服务。

## 四、多平台部署：$5 VPS 到 GPU 集群

Hermes 支持六种部署后端：本地、Docker、SSH、Singularity、Modal、Daytona。其中 Modal 和 Daytona 提供serverless 持久化——Agent 在空闲时休眠，按需唤醒，成本几乎为零。

**笔者的判断**：这种「成本无限弹性」的部署能力，是自改进 Agent 的必要条件。自改进需要长时间运行和大量交互，如果 Agent 的运行成本与在线时长成正比，它就不值得持续运行。Hermes 的部署策略让「永远运行的 Agent」变成了一个经济上可行的选项。

## 五、与 Cursor Automations 的主题呼应

| 维度 | Hermes Agent | Cursor Automations |
|------|-------------|-------------------|
| **Skill 创作方式** | Agent 根据使用经验自主创建 | Agent 根据自然语言描述生成 |
| **Skill 验证机制** | 使用中持续改进，无显式 eval | 依赖 human review + Computer Use 可视化 |
| **触发方式** | 主动观察 + 定时触发 | 外部事件（GitHub/Slack）|
| **记忆系统** | FTS5 + LLM 摘要双层 | 会话内，无跨会话持久化 |

两者代表了 Skill 自改进的两种路径：**Hermes 是「经验驱动」**——Agent 从自己的实践中学习；**Cursor 是「描述驱动」**——Agent 从用户的语言描述中学习。在实际工程中，经验驱动的学习更慢但更深，描述驱动的学习更快但更浅。

## 六、值得关注的工程借鉴

**对于构建自改进 Agent 系统**：Hermes 的 Skill 自改进循环是截至目前最完整的开源实现。它的核心价值不在于具体代码，而在于它证明了「Agent 可以且应该从经验中学习」这一命题在工程上是可行的。

**对于 Skill Authoring 研究**：Hermes 的 SKILL.md 格式与 Anthropic 的 Skill-Creator 体系兼容，这意味着两个生态可以互相参考。如果你想研究 Skill 自改进，Hermes 是一个比 Anthropic 官方项目更轻量的切入点。

---

*Pair Article: [Anthropic Skill-Creator: Eval-Driven Skill Authoring](/articles/harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md) — 官方 eval 驱动视角，与 Hermes 的经验驱动视角形成互补。*