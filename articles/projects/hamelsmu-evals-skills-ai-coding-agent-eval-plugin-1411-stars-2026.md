---
title: hamelsmu/evals-skills — AI 编程 Agent 的评估技能插件 2026
date: 2026-06-22
source: https://github.com/hamelsmu/evals-skills
author: Hamel Husain (Hamel & Shreya)
tags: [agent-skills, evaluation, evals, skill-plugin, ai-evals, harness, openai]
topics: [Eval Skills, AI Coding Agent, Skill Plugin, LLM Evaluation, Eval-Driven Development]
description: Hamel Husain & Shreya 的 evals-skills 把 AI Evals 课程中的最佳实践沉淀为 SKILL.md 插件，AI 编程 Agent（Claude Code/Codex 等）安装后能自动审计、修复和改进 LLM 评测管道。1,411⭐ MIT 许可证，2026 年 3 月 1 日发布。
stars: 1411
license: MIT
license_verified: 2026-06-22 via GitHub API
created: 2026-03-01
last_pushed: 2026-06-10
cluster: harness
cluster_role: project
pair_article: articles/harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md
pair_theme: Eval-Driven Skill Development
round: 489
---

# hamelsmu/evals-skills — AI 编程 Agent 的评估技能插件

> **核心命题**：LLM evaluation 是 AI 产品里最难也最容易出错的一环。Hamel Husain（AI Evals 课程的讲师）把自己在 50+ 公司咨询中见过的最常见陷阱沉淀成一组 SKILL.md，AI 编程 Agent 装上之后，**就能像资深 eval 工程师一样审计和改进评测管道**。

## 一、定位破题

**一句话定义**：一组用来引导 AI 编程 Agent 构建 LLM 评估的 SKILL.md 插件。

**问题锚定**：你（或你的团队）正在搭一套 LLM 评测——LLM-as-judge、prompt A/B、模型对比。但你不确定：评测对象真的对吗？Judge 模型有偏吗？数据有 contamination 吗？Prompt 里的指令会让 LLM 输出"讨好"judge 吗？

**价值主张**：不用自己踩坑，AI 编程 Agent 装上这个 plugin 后，按 `/evals-skills:eval-audit` 就能并行跑诊断、合成报告、推荐改进方向。

**生态对位**：这是 Anthropic SKILL.md 标准的最佳实践示范——一个第三方开发者用 SKILL.md 格式封装了一整套"eval 知识"，让任何 Claude Code / Codex 用户都受益。

## 二、和 Anthropic skill-creator 的双层闭环

Anthropic 2026 年 3 月发布的 skill-creator（参考 R489 Article）解决了**「Skill 作者怎么写 evals」**——领域专家不写代码也能为 SKILL.md 写测试。

hamelsmu/evals-skills 解决了**「AI 编程 Agent 怎么帮我做 evals」**——AI Agent 装上 plugin 后，遵循 Hamel 的最佳实践帮你审计、修复、改进 LLM 评测管道。

两个项目构成完整的 eval-driven development 闭环：

| 维度 | Anthropic skill-creator | hamelsmu/evals-skills |
|------|------------------------|----------------------|
| 面向谁 | 写 SKILL.md 的领域专家 | 搭评测管道的 AI/ML 工程师 |
| 触发方式 | `Ask Claude to use the skill-creator` | `/plugin marketplace add hamelsmu/evals-skills` |
| 核心能力 | 给 Skill 加 evals + benchmark mode + A/B + 触发调优 | 给 Agent 加 evals 工程能力：审计、修复、改进 |
| 评估对象 | 单一 SKILL.md 的质量 | 完整的 LLM 评测管道 |
| 状态 | Anthropic 官方 (Mar 3, 2026) | 社区开源 (Mar 1, 2026) |

## 三、核心 SKILL.md 拆解

从 README 看，evals-skills 至少包含以下几类 skill：

### 3.1 eval-audit（入口 skill）

让 AI 编程 Agent **用独立的 subagent 并行**审计评测管道的多个诊断维度，然后综合成单份报告：

```bash
Install the eval skills plugin from https://github.com/hamelsmu/evals-skills,
then run /evals-skills:eval-audit on my eval pipeline.
Investigate each diagnostic area using a separate subagent in parallel,
then synthesize the findings into a single report.
Use other skills in the plugin as recommended by the audit.
```

这个用法和 Anthropic 2026 年 3 月在 skill-creator 中推出的"multi-agent parallel eval execution"在结构上完全一致——**两者都是 harness engineering 的"用多 agent 换速度"范式的不同应用**。

### 3.2 其他 skill（推断）

README 提到 "Use other skills in the plugin as recommended by the audit"，意味着 eval-audit 会推荐其他 skill 来修复具体问题。常见类别可能包括：

- **judge-quality**：评估 judge model 的偏差（position bias / length bias / self-preference）
- **data-quality**：检查 eval set 的污染和分布漂移
- **prompt-clarity**：检查 eval prompt 的歧义和"讨好"诱导
- **metric-design**：评估 metric 设计的合理性（precision/recall/F1 选错）
- **eval-iteration**：基于结果迭代改进

## 四、安装与生态集成

evals-skills 在 README 中明确支持两种安装路径：

### 4.1 Claude Code 原生 plugin

```bash
# Step 1: 注册 plugin 仓库
/plugin marketplace add hamelsmu/evals-skills
# Step 2: 安装
/plugin install evals-skills@hamelsmu-evals-skills
```

### 4.2 开放 Skills CLI

README 提到 "If you use the open Skills CLI, install from this repo"——这是对**跨 Agent 兼容**标准的支持（参考 R375 nanoclaw 的 SKILL.md 跨 Agent 路径）。

这种双路径设计意味着 evals-skills 不绑定 Claude Code——OpenAI Codex、Cursor、Aider 等 AI 编程 Agent 都能消费。

## 五、生态对位（Pair 强度分析）

### 5.1 与 Anthropic skill-creator 的 SPM 对位

**共享关键词（5+）**：
- "skill" / "skills" / "SKILL.md"
- "eval" / "evaluation" / "evaluate"
- "agent" / "AI coding agent"
- "test" / "testing"
- "plugin"
- "Hamel"（在 AI Evals 圈子是知名讲师）

**维度互补**：
- 抽象 ↔ 实现：skill-creator 是**给 Skill 加 eval**的工具层抽象，evals-skills 是**用 Skill 做 eval**的工程实践
- 官方 ↔ 社区：skill-creator 是 Anthropic 官方产品，evals-skills 是 Hamel 个人+社区
- Skill 作者 ↔ Skill 消费者：skill-creator 服务 Skill 作者，evals-skills 服务 Skill 消费者

### 5.2 与 R487 superpowers 的对比

superpowers（obra/superpowers，198K⭐ MIT）也是 SKILL.md 格式的"软件工程方法论技能库"——但 superpowers 覆盖范围广（从 TDD 到 code review 全套），evals-skills 专注在 **AI/LLM evals** 这一个垂直领域。

**深度对比**：
- superpowers：横向广度，工程师日常用
- evals-skills：纵向深度，AI/ML 工程师专项

## 六、为什么 R489 选这个项目

1. **Pair 强度满中**：与 R489 Article 共享 5+ 关键词，维度互补（抽象 ↔ 实现，官方 ↔ 社区，作者 ↔ 消费者）
2. **License 清洁**：MIT，商用友好
3. **Stars 中等但权威**：1,411⭐ 不算顶流，但作者 Hamel Husain 是 AI Evals 圈最有影响力的讲师之一，**作者权威性补偿 stars 数字**
4. **生态契合**：SKILL.md 跨 Agent 标准，与仓库 target ecosystem（openclaw / claude-code / codex）直接对齐
5. **填补空白**：darkrishabh/agent-skills-eval 已经覆盖了"测试 Skill 本身"的工具，evals-skills 覆盖"用 Skill 测 LLM 评估管道"的工具——**两个不同垂直**

## 七、对其他 Agent 项目的启示

evals-skills 的设计给其他想用 SKILL.md 标准做工具分发的项目一个**清晰的样板**：

1. **垂直深度优先**：不要做大而全的 skill 库，做深一个垂直（evals、PDF、code review 等）
2. **入口 skill + 推荐其他 skill 的 audit 模式**：eval-audit 是入口，audit 结果推荐其他 skill——**这是 skill 组合编排的样板**
3. **跨 Agent 安装路径**：同时支持 Claude Code plugin + 开放 Skills CLI，不要锁定单一平台
4. **作者权威性是 SKILL.md 生态的核心资产**：Hamel 的 50+ 公司经验 + 课程 = 这个 plugin 的护城河。SKILL.md 标准是载体，**人+经验是内容**

## 引用源

> GitHub: [hamelsmu/evals-skills](https://github.com/hamelsmu/evals-skills)
> Stars: 1,411（2026-06-22 验证）
> License: MIT（GitHub API 验证）
> 发布日期: 2026 年 3 月 1 日
> 最近更新: 2026 年 6 月 10 日
> 作者背景: Hamel Husain & Shreya，AI Evals For Engineers & PMs 课程讲师
> Pair Article: [Anthropic Skill-Creator: Eval-Driven Skill Authoring](articles/harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md)
> Cluster: harness（eval-driven agentic development 子维度）
