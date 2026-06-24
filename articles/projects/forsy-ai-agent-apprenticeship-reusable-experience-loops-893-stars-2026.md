---
title: Forsy-AI/agent-apprenticeship：执行迹回灌训练（893 Stars）
date: 2026-06-24
source: https://github.com/Forsy-AI/agent-apprenticeship
stars: 893
license: MIT
tags: [agent-apprenticeship, agent-economy, post-training, training-signals, experience-reuse, ecosystem-learning, mentor-apprentice, hermes-agent, openclaw, codex, claude-code, opencode, cursor, real-world-tasks, reinforcement-learning]
topics: [Agent Apprenticeship, Post-Training, Training Signals, Experience Reuse, Ecosystem Learning, Mentor-Apprentice Pattern, Agent Economy, Hermes Agent, OpenClaw, Codex, Claude Code, OpenCode, Cursor]
description: Forsy-AI 的 agent-apprenticeship（MIT，893 Stars，2026-06-23）把「真实世界任务的执行迹」抽象成可复用的 post-training 信号，500+ 任务种子 / 495 节课 / 1000+ 执行轨迹的开放生态，npx 一行接入 Hermes Agent / OpenClaw / Codex / Claude Code / Cursor / OpenCode，把 harness 工程的下一站从「Skill 创作」推到「执行迹回灌训练」。
length: 3800
cluster: harness
cluster_role: project
round: 521
pair_article: articles/harness/agent-apprenticeship-real-world-tasks-post-training-2026.md
pair_reason: "Agent Apprenticeship 文章把这个项目放进 2026 H1 harness 演化时间线（Skill → Eval-driven Skill → Loop → Apprenticeship），本文补上「项目工程结构 + 接入流程 + 与已有项目的位置关系」"
---

# Forsy-AI/agent-apprenticeship：执行迹回灌训练的开放生态

> 仓库：[github.com/Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) — MIT，893 Stars，2026-06-23

## 1. 项目定位

agent-apprenticeship 不是 framework、不是 harness、不是 eval 工具——**它是 post-training signal collector**：装在 agent runtime 上，采集真实任务的执行迹，抽象成 lesson，回流到生态。

| 维度 | 描述 |
|------|------|
| **类别** | Post-Training 工具链 / Agent 训练信号生产 |
| **License** | MIT |
| **Stars** | 893（2026-06-24 验证） |
| **首次发布** | 2026-06-23 |
| **安装方式** | `npx agent-apprenticeship init` |
| **支持 agent** | Hermes Agent / OpenClaw / Codex / Claude Code / Cursor / OpenCode |
| **种子数据规模** | 500+ 任务 / 495 节课 / 1000+ 执行迹 / 1000+ task rollouts |
| **核心循环** | 任务执行 → trace 采集 → mentor agent 抽象 lesson → 生态回流 |

## 2. 三层架构（工程视角）

### 2.1 第一层：Seed Dataset（种子数据集）

仓库内置 4 类基础数据，构成生态的「冷启动」：

- **500+ curated seed tasks**：从真实世界 sourcing、grounding 过
- **495 reusable agent lessons**：抽象可复用的经验单元
- **1000+ full agent execution traces**：完整执行轨迹
- **1000+ agent work episodes / task rollouts**：任务级 rollout 数据

关键不是数据量大，而是 **数据形态标准**：每个 trace 都是 `(task, plan, actions, outcome, lesson)` 五元组，让任何 post-training pipeline 都能消费。

### 2.2 第二层：Workflow Loop（工作流循环）

> "Iterative workflow loops across domains, from simple tasks to complex specialized work. Apprentice agents work with mentor agents or human experts to complete long-horizon, real-world tasks, while each workflow generates reusable learning signals for the ecosystem."

三类角色：

- **Apprentice agents**（学徒）：执行具体任务、产生 trace
- **Mentor agents**（导师）：审核 trace、抽象 lesson、过滤低质量信号
- **Human experts**（人类专家）：仲裁 mentor 决策

> **注意**：mentor agent **不是简单的 reward model**——它能产出 lesson（抽象经验），不是只有 scalar reward。这是它和 RLHF 的核心区别。

### 2.3 第三层：Ecosystem Exchange（生态交换）

> "Compounding exchange of agent work experience: economically valuable task execution generates training signals, those signals improve future work, and future work creates new reusable experience for the ecosystem."

这是 Apprentice 与其他类似项目最不一样的地方——**信号不只服务于一个组织，而是「经济价值驱动的双向流动」**：

- 跑任务的人（贡献者）通过共享 trace 获得生态反馈
- 跑任务的人（受益者）通过消费生态信号提升 agent 质量
- 经济价值高的任务（金融分析 / 临床诊断 / 工业设计）自然形成「高质量信号供给」

## 3. 接入流程

```bash
# 在任意 agent runtime 项目里
npx agent-apprenticeship init
```

这一行命令会：

1. 检测当前 agent runtime（Codex / Claude Code / Hermes Agent / OpenClaw / Cursor / OpenCode）
2. 注入 trace 采集 hook（监听 agent 的 tool call / file edit / shell exec / LLM call）
3. 把 trace 上传到 agent-apprenticeship 生态
4. 配置本地 mentor agent 抽象规则
5. 返回一个 dashboard URL 让你看自己贡献了多少 trace / 抽象了多少 lesson

零配置文件、零环境依赖、零网络代理配置——这种「**像装 eslint 一样装一个训练信号采集器**」的部署模型，是它能在 6 个异构 agent runtime 里都跑起来的关键。

## 4. Topics 解析

仓库 GitHub Topics 一共 20 个，对应 6 大主题：

```
['agent-apprenticeship', 'agent-economy', 'agent-experience', 'agent-learning',
 'agent-traces', 'agentic-ai', 'ai-agents', 'autonomous-agents',
 'claude-code', 'codex', 'cursor', 'ecosystem-learning',
 'hermes-agent', 'loop-engineering', 'openclaw', 'opencode',
 'post-training', 'real-world-tasks', 'reinforcement-learning', 'training-signals']
```

- **范式层**（5 个）：agent-apprenticeship / agent-economy / agent-experience / agent-learning / ecosystem-learning
- **数据形态**（3 个）：agent-traces / real-world-tasks / training-signals
- **训练方法**（1 个）：post-training / reinforcement-learning / loop-engineering
- **能力定位**（3 个）：agentic-ai / ai-agents / autonomous-agents
- **Runtime 支持**（6 个）：claude-code / codex / cursor / hermes-agent / openclaw / opencode
- **应用层**（2 个）：agent-experience / agent-economy

> 一个 893 Stars 的早期项目能同时支持 6 个 agent runtime（Hermes Agent / OpenClaw / Codex / Claude Code / Cursor / OpenCode），**说明它的抽象层做得足够低**——不是「OpenAI 协议 vs Anthropic 协议 vs 开源 CLI」分类，而是「任何能跑 npx 命令的 agent runtime」都能挂上去。

## 5. 与已有项目的位置关系

| 项目 | Stars | 类别 | 与 agent-apprenticeship 的关系 |
|------|-------|------|-------------------------------|
| **Forsy-AI/agent-apprenticeship** | 893 | Post-Training Signal Collector | 自身 |
| [Cursor Composer 2.5](../ai-coding/cursor-composer-2-5-targeted-rl-synthetic-data-2026.md) | n/a | Targeted RL + 合成数据 | **互补**：可控合成 vs 真实迹 |
| [OpenAI AI Chemist](../harness/openai-ai-chemist-harness-loop-experimental-validation-2026.md) | n/a | 实验验证 loop | 上下游：跑任务 → 生成 trace |
| [Anthropic Skill-Creator](../harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md) | n/a | Eval-Driven Skill Authoring | 互补：Skill 创作 vs 执行迹回灌 |
| [Cursor Continually Improving Agent Harness](../ai-coding/cursor-continually-improving-agent-harness-2026.md) | n/a | Self-Improving Harness | 上下游：continual loop → trace 采集 |
| [Vercel Eve](../projects/vercel-eve-filesystem-first-durable-agent-framework-1651-stars-2026.md) | 1651 | Durable Agent Framework | 互补：状态持久化 vs 训练信号 |

两个特别值得关注的对照：

### 5.1 vs Cursor Composer 2.5（Targeted RL + 合成数据）

agent-apprenticeship 走的是「**真实世界任务的执行迹**」路线，Composer 2.5 走的是「**受控合成 + RL**」路线。两个项目分别押注 post-training 范式光谱的两端。

| 维度 | Cursor Composer 2.5 | Forsy-AI agent-apprenticeship |
|------|---------------------|-------------------------------|
| **数据来源** | 合成 + 受控 | 真实任务执行 |
| **数据流向** | 单向（公司内） | 双向（生态交换） |
| **使用门槛** | 用户不用管 | 用户主动贡献才能受益 |
| **可控性** | 高 | 中（取决于 mentor agent 质量） |
| **多样性** | 中（限于 Cursor 用例） | 高（多 agent + 多领域） |

### 5.2 vs Anthropic Skill-Creator（R489）

Skill-Creator 让「Skill 的质量可量化」——它是**知识编码**的工具；agent-apprenticeship 让「agent 跑过的任务能回流到训练」——它是**知识发现**的工具。两者叠加才完整：

```
Skill-Creator (领域专家沉淀) ⊕ agent-apprenticeship (执行回流) = 完整 harness
```

## 6. 关键技术挑战

仓库 README 没有回避它的核心风险：

1. **Signal 质量控制**：mentor agent 抽象出来的 lesson 是否真的能复用？需要对抗「低质量 trace 污染生态」的问题
2. **经济价值量化**：「task-level economic value」如何定义？不同领域不可比
3. **隐私 / 数据合规**：真实任务执行可能涉及企业敏感数据
4. **冷启动**：500+ 任务种子的「生态」距离真正的「compounding exchange」还差几个数量级

这 4 个挑战都不是纯工程问题，需要生态运营 + 经济模型设计。

## 7. 对 harness cluster 的位置

把它放进已有的 178 篇 harness 文章矩阵，agent-apprenticeship 的独特性在于：

- ❌ 不是 framework（不是 LangChain、AutoGen）
- ❌ 不是 harness 本身（不是 Claude Code、Codex）
- ❌ 不是 eval 工具（不是 SpecBench、Patronus TRACE）
- ✅ **是 post-training signal collection**（装在 agent runtime 上、采集执行迹、抽象 lesson、回流生态）

这是 harness cluster 里**第一个把「训练数据生产」当成产品来做的项目**——它的目标用户是「跑 agent 的人」，不是「写 agent 的人」，也不是「评测 agent 的人」。

## 8. 为什么选它（收录理由）

1. **主题新颖**：harness cluster 里「post-training signal collection」方向的首个项目，178 篇里没有同主题
2. **Stars 接近 1000**：893⭐，MIT 协议
3. **明确点名 OpenClaw/Hermes Agent**：仓库 topics 包含 `openclaw` 和 `hermes-agent`——这个项目把 OpenClaw 当作「值得支持的 agent runtime」之一收录，对我们维护的仓库来说是直接相关的「合作生态」
4. **多 runtime 支持**：跨 6 个 agent runtime 的抽象能力证明工程深度
5. **明确的范式突破**：把「agent 跑过的任务」从「单点 trace」变成「可交换生态资产」，这是 2026 H1 harness 演化的关键节点

## 9. 风险与边界

- **冷启动期**：500+ 任务的「生态」还很早期，compounding 效应未验证
- **Mentor agent 质量**：抽象 lesson 的质量直接决定生态价值，目前没有第三方 benchmark
- **跨域经济价值量化**：「task-level economic value」如何定义仍然是开放问题
- **数据合规**：真实任务 trace 可能含企业敏感数据，需要后续的隐私层

这些风险都不影响 R521 收录——但下轮（R522+）需要持续观察 mentor agent 抽象质量、生态 trace 增长速度、是否有第三方 benchmark 出现。

---

## 参考链接

- 仓库：[github.com/Forsy-AI/agent-apprenticeship](https://github.com/Forsy-AI/agent-apprenticeship) — MIT，893 Stars，2026-06-23
- npm：`npx agent-apprenticeship init`
- 配对文章：[Agent Apprenticeship: 执行迹 → Post-Training 开放生态](../harness/agent-apprenticeship-real-world-tasks-post-training-2026.md)
- 关联项目：
  - [Cursor Composer 2.5](../ai-coding/cursor-composer-2-5-targeted-rl-synthetic-data-2026.md) — Targeted RL + 合成数据
  - [Anthropic Skill-Creator](../harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md) — Eval-Driven Skill Authoring
  - [Cursor Continually Improving Agent Harness](../ai-coding/cursor-continually-improving-agent-harness-2026.md) — Self-Improving Harness
