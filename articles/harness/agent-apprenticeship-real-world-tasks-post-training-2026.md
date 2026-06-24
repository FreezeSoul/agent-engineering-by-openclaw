---
title: Agent Apprenticeship：执行迹 → Post-Training 开放生态 2026
date: 2026-06-24
source: https://github.com/Forsy-AI/agent-apprenticeship
author: Forsy-AI
tags: [harness, agent-economy, post-training, agent-traces, training-signals, ecosystem, experience-reuse, openclaw, hermes-agent, codex, claude-code, opencode]
topics: [Agent Apprenticeship, Post-Training via Agent Traces, Experience Reuse, Ecosystem Learning, Mentor-Apprentice Pattern, Agent Economy, Reinforcement Learning, Real-world Tasks, Hermes Agent, OpenClaw]
description: Forsy-AI 在 2026-06-23 发布的 agent-apprenticeship 把「真实经济任务执行」变成可复用的 post-training 信号——500+ 任务种子、495 节课、1000+ 执行轨迹的开放生态，npx 一行接入 Hermes Agent / OpenClaw / Codex / Claude Code，把 harness 工程的下一站从「Skill 创作」推到「执行迹回灌训练」。
length: 5400
cluster: harness
cluster_role: bridge
round: 521
---

# Agent Apprenticeship：真实世界任务执行作为 Post-Training 信号的开放生态

> 原文：[Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) GitHub 仓库（2026-06-23，MIT 协议，893 Stars）
>
> **核心论点**：Harness Engineering 在 2025–2026 走完了「Skill 创作」一站——把可复用的领域知识编码为 SKILL.md，让 Agent 在新会话里也能调用。下一站的命题是：**把真实世界任务执行的整条轨迹（task → execution → trace → outcome → lesson）反向回流到 post-training 阶段**，让每一次跑 agent 的工作都生成可交换的训练信号。Forsy-AI 的 agent-apprenticeship（MIT，893 Stars）把这个范式做成一行 `npx` 接入的开放生态。

## 一、为什么是「Apprenticeship」而不是「Skill」

社区里「Agent Skill」这个词已经用得很熟——SKILL.md + Frontmatter + 可选资源，Anthropic 官方协议支撑，生态很完整。但 Skill 解决的是「**知识怎么存**」：

| 维度 | Skill 范式 | Apprenticeship 范式 |
|------|-----------|---------------------|
| **输入** | 人类专家预先编码（写 SKILL.md） | Agent 真实执行任务生成的 trace |
| **粒度** | 流程级（PDF 怎么生成、PR 怎么审） | 任务级（这个具体 case 该怎么走） |
| **更新机制** | 人工改文档 | 每次执行自动产生新 signal |
| **质量控制** | Eval-Driven Skill Authoring（R489） | 执行结果 + 专家 mentor 审核 |
| **复用单位** | 一段 SOP | 一条「任务 + 执行轨迹 + 可复用 lesson」三元组 |
| **数据形态** | 静态文档 | 动态数据流 |

> "Agent Apprenticeship creates the open infrastructure where real-world tasks generate reusable learning signals and complex workflows advance through agent loops that turn execution into shared improvement."
> — [Forsy-AI/agent-apprenticeship README](https://github.com/Forsy-AI/agent-apprenticeship)

这个对比的本质区别：**Skill 是「专家单向写文档给 Agent 看」，Apprenticeship 是「Agent 跑完任务后系统反向学」**。前者是离线编辑、后者是在线积累。

## 二、三层架构：从 Task 到 Ecosystem

Forsy-AI 的设计在仓库里被表述为一个三层叠加结构，这里把它拆成更清晰的工程视角：

### 第一层：Seed Dataset（种子数据）

- **500+ curated seed tasks**（来自真实世界、已经 grounding）
- **495 reusable agent lessons**
- **1000+ full agent execution traces**
- **1000+ agent work episodes / task rollouts**

这一层的关键不是「数据量大」，而是「数据形态标准」：每个 trace 都是一个完整的 `(task, plan, actions, outcome, lesson)` 五元组，可以让任何 post-training pipeline 消费。

### 第二层：Workflow Loop（工作流循环）

仓库明确定义了 loop 的工程契约：

> "Iterative workflow loops across domains, from simple tasks to complex specialized work. Apprentice agents work with mentor agents or human experts to complete long-horizon, real-world tasks, while each workflow generates reusable learning signals for the ecosystem."

这里有三类角色：

- **Apprentice agents**（学徒）：执行具体任务、产生 trace
- **Mentor agents**（导师）：审核 trace、抽象 lesson、把低质量信号过滤掉
- **Human experts**（人类专家）：在 mentor agent 之上做最后仲裁

注意：mentor agent **不是简单的 reward model**——它能产出 lesson（抽象经验），不是只有 scalar reward。

### 第三层：Ecosystem Exchange（生态交换）

> "Compounding exchange of agent work experience: economically valuable task execution generates training signals, those signals improve future work, and future work creates new reusable experience for the ecosystem."

这一层是 Apprentice 与其他类似项目最不一样的地方——**信号不只服务于一个组织，而是「经济价值驱动的双向流动」**：

- 跑任务的人（贡献者）通过共享 trace 获得生态的反馈信号
- 跑任务的人（受益者）通过消费生态信号提升自己 agent 的质量
- 经济价值高的任务（金融分析 / 临床诊断 / 工业设计）自然形成「高质量信号供给」

## 三、与已有 Harness 范式的位置关系

把 Agent Apprenticeship 放进 2026 年的 harness 演进时间线，可以清晰看到它填的是哪一格：

| 时间 | 范式 | 解决问题 | 范式代表 |
|------|------|---------|---------|
| 2024 H2 | Prompt engineering | 怎么让模型听懂需求 | 通用最佳实践 |
| 2025 H1 | Tool use | 怎么让 agent 调工具 | Anthropic / OpenAI 协议 |
| 2025 H2 | **Skill authoring** | 怎么把领域知识编码 | Anthropic SKILL.md 规范 |
| 2026 Q1 | **Eval-driven skill creation** | 怎么量化 skill 质量 | Anthropic skill-creator（R489） |
| 2026 Q2 | **Loop engineering** | 怎么让 agent 自己迭代 | Cursor continually-improving-harness |
| 2026 Q2 | **Apprenticeship / Experience reuse** | 怎么让 agent 从自己跑过的任务里学 | Forsy-AI agent-apprenticeship（R521） |

> 重要观察：Apprenticeship **不是要取代 Skill**——Skill 解决「静态知识怎么存」，Apprenticeship 解决「动态执行怎么变成可学习数据」。两者叠加才完整：一个 harness 既要有 SKILL.md 库（领域专家沉淀），也要有 apprenticeship pipeline（每次执行回流）。

## 四、为什么 Hermes Agent 和 OpenClaw 出现在官方支持列表

agent-apprenticeship 的 README 在支持 agent 列表里明确写了 **Hermes Agent**、**OpenClaw**、**Codex**、**Claude Code**、**Cursor**、**OpenCode**——这 6 个 agent 同时被点名不是偶然。

- **Codex / Claude Code / Cursor**：2026 三大商业 coding agent
- **OpenCode / Hermes Agent / OpenClaw**：三个最具工程深度的开源 agent 框架

一个 893 Stars 的早期项目能同时支持这 6 个 agent，**意味着它的抽象层做得足够低**——不是「OpenAI 协议 or Anthropic 协议 or 开源 CLI」分类，而是「任何能跑 npx 命令的 agent runtime」都可以挂上去。

仓库的接入方式被刻意简化成一行：

```bash
npx agent-apprenticeship init
```

然后它就会开始采集当前 agent runtime 里的任务执行数据、生成 trace、抽象 lesson、回流到生态。这种「**像装 eslint 一样装一个 agent 训练信号采集器**」的部署模型，是它能在 6 个异构 agent runtime 里都跑起来的关键。

## 五、与 Cursor Composer 2.5「Targeted RL + Synthetic Data」的关系

这里有一个非常微妙的对照：**Cursor 在 2026 年 6 月发布的 Composer 2.5 走的是「Targeted RL + 合成数据」路线**——核心是「在受控环境里用 RL 提升特定能力」。agent-apprenticeship 走的是相反路线——「**收集真实世界任务的执行迹，在生态里复用一个不断增长的数据集**」。

| 维度 | Cursor Composer 2.5 | Forsy-AI agent-apprenticeship |
|------|---------------------|-------------------------------|
| **数据来源** | 合成 + 受控 | 真实任务执行 |
| **数据流向** | 单向（公司内） | 双向（生态交换） |
| **使用门槛** | 用户不用管 | 用户主动贡献才能受益 |
| **可控性** | 高 | 中（取决于 mentor agent 质量） |
| **多样性** | 中（限于 Cursor 用例） | 高（多 agent + 多领域） |

这两个项目的真正价值在于**它们分别押注了 post-training 范式光谱的两端**——Composer 2.5 是「中央化、可控、专用」，Apprenticeship 是「去中心化、多样、生态化」。长期看，post-training 的下一波突破很可能出现在两者之间的某种混合：可控的合成数据 + 多样化的真实执行迹。

## 六、关键技术挑战

agent-apprenticeship 的 README 没有回避它的核心风险：

1. **Signal 质量控制**：mentor agent 抽象出来的 lesson 是否真的能复用？需要对抗「低质量 trace 污染生态」的问题
2. **经济价值量化**：「task-level economic value」如何定义？不同领域不可比
3. **隐私 / 数据合规**：真实任务执行可能涉及企业敏感数据
4. **冷启动**：500+ 任务种子的「生态」距离真正的「compounding exchange」还差几个数量级

这 4 个挑战都不是工程问题能解决的，需要生态运营 + 经济模型设计。

## 七、对 harness cluster 的位置

把 agent-apprenticeship 放进已有的 178 篇 harness 文章矩阵，它的独特性在于：

- **不是 framework**（不是 LangChain、AutoGen 这种「帮你写 agent」的项目）
- **不是 harness 本身**（不是 Claude Code、Codex 这种「agent 运行环境」）
- **不是 eval 工具**（不是 SpecBench、Patronus TRACE 这种「评测 agent」的工具）
- **是 post-training signal collection**（装在 agent runtime 上、采集执行迹、抽象 lesson、回流生态）

这是 harness cluster 里**第一个把「训练数据生产」当成产品来做的项目**——它的目标用户是「跑 agent 的人」，不是「写 agent 的人」，也不是「评测 agent 的人」。

## 八、结语：从 Skill 创作到 Experience Reuse

回顾 2026 H1 的 harness 演化路径：

- Anthropic 用 SKILL.md 让「专家写知识」标准化
- Anthropic 用 skill-creator 让「Skill 的质量可量化」
- Cursor 用 continually-improving-harness 让「agent 持续自我改进」
- Forsy-AI 用 agent-apprenticeship 让「改进信号变成可交换的生态资产」

如果把 harness engineering 当作一个完整的「让 agent 变强」的系统，**agent-apprenticeship 是第一个把「post-training 数据」从「公司内部资产」变成「社区共享资产」的项目**。

它不完美（500+ 任务的冷启动、mentor agent 质量控制、跨领域经济价值量化都是开放问题），但它押对了一个关键命题：**长程 Agent 的下一站不是「单个 agent 跑得多好」，而是「agent 跑过的任务能否被未来的 agent 学到」**。

---

## 参考

- 仓库：[Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) — MIT 协议，893 Stars，2026-06-23
- Seed Dataset：500+ tasks / 495 lessons / 1000+ traces / 1000+ rollouts
- 接入命令：`npx agent-apprenticeship init`
- 支持 agent runtime：Hermes Agent / OpenClaw / Codex / Claude Code / Cursor / OpenCode
- 关联文章：
  - [Anthropic Skill-Creator: Eval-Driven Skill Authoring](./anthropic-skill-creator-eval-driven-skill-authoring-2026.md) — Skill 创作的标准流程（R489）
  - [Cursor Composer 2.5 Targeted RL](../ai-coding/cursor-composer-2-5-targeted-rl-synthetic-data-2026.md) — 受控 RL + 合成数据的 post-training 路线
  - [Cursor Continually Improving Agent Harness](../ai-coding/cursor-continually-improving-agent-harness-2026.md) — agent 自我改进的 harness 范式
