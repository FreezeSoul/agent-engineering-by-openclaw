---
title: Anthropic Skill-Creator：Eval 驱动的技能创作革命 2026
date: 2026-03-03
source: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills
author: Anthropic
tags: [harness, evaluation, agent-skills, skill-creator, eval-driven-development, multi-agent-eval]
topics: [Anthropic, Agent Skills, Eval-Driven Development, Skill Authoring, Multi-Agent Eval, Comparator Agents]
description: Anthropic 在 2026 年 3 月为 skill-creator 增加 eval 能力、benchmark mode、多 agent 并行执行和 comparator A/B，让非工程师也能为 SKILL.md 编写 evals，把 Skill 开发从「写完调调看」推进到「先定义成功，再动手写」。
length: 4200
cluster: harness
cluster_role: anchor
round: 489
---

# Anthropic Skill-Creator 进化：Eval-Driven Skill Authoring 让非工程师也能写测试

> 原文：[Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)（Anthropic Claude Blog，2026 年 3 月 3 日）

## 核心命题

Agent Skills 自 2025 年 10 月上线以来，作者画像高度集中——**大多数是领域专家，不是工程师**。他们能写出工作流的 SKILL.md，却没有任何工具来回答三个核心问题：

1. 这个 Skill 在新模型上还能正常工作吗？
2. 它在应该触发的时候真的被触发了吗？
3. 我刚才的修改是让它变好了还是变差了？

Anthropic 在 2026 年 3 月 3 日发布的 skill-creator 更新，把软件开发的「测试 / 基准 / 迭代改进」三项严谨实践引入 Skill 创作流程，**而且全程不要求写代码**。这是 harness engineering 的又一次范式转变——把 eval 从「工程师的可选工作」变成「领域专家的标准操作流程」。

## 一、为什么 Skill 急需系统化测试

传统软件开发有 CI/CD、单元测试、集成测试，任何代码变更都会被自动化测试捕获。但 Agent Skills 不同——它的输出是非确定性的，依赖模型能力，且技能之间可能存在隐含依赖。

更糟糕的是，**模型会演化**。一个 Skill 昨天工作正常，不代表今天还能工作。Anthropic 在文章里点出两个直接威胁：

> "As models and the infrastructure around them evolve, a skill that worked well last month might behave differently today. Running evals against a new model gives you an early signal when something shifts before it impacts your team's work."

第二个威胁更加隐蔽——**基础模型可能已经「学会」了 Skill 想教的能力**：

> "If the base model starts passing your evals without the skill loaded, that's a signal the skill's techniques may have been incorporated into the model's default behavior. The skill isn't broken; it's just no longer necessary."

这意味着 Skill 的生命周期管理是一个**持续监控问题**，不是一次性的发布问题。Eval 既是回归检测器，也是「Skill 是否还有存在价值」的判断器。

## 二、两类 Skill，两种测试理由

Anthropic 在文章里区分了两类 Skill，**这个分类本身就是 harness engineering 的重要概念**：

| Skill 类型 | 特征 | 测试关注点 |
|------------|------|-----------|
| **Capability uplift** | 让模型做本来做不到或做不好的事（如 PDF 文档创建） | 编码能力、坐标精度、格式正确性 |
| **Encoded preference** | 把已有的能力按团队流程串起来（NDA 审查、weekly update） | 流程遵循度、字段完整性 |

两类 Skill 的测试目标不同。Capability uplift 需要严格的输出质量检测（PDF 坐标对不对、表单填没填）。Encoded preference 需要流程完整性检查（NDA 关键字段是否都被识别、weekly update 是否覆盖所有数据源）。

无论哪种类型，Anthropic 给出的判断标准一致：

> "Testing turns a skill that seems to work into one you know works."

## 三、Skill-Creator 的新能力矩阵

### 3.1 Eval 编写器：零代码写测试

skill-creator 现在帮助作者**写出 evals**——这与传统软件测试的思路一致：定义一些测试 prompts（如果需要的话加上测试文件），描述「好的输出长什么样」，然后让 skill-creator 验证 Skill 是否达标。

文章给出一个真实案例：PDF Skill 之前在非可填表单上挣扎——Claude 必须在没有定义字段引导的情况下，把文本放到精确的坐标上。Eval 把失败隔离开来，团队随后上线了一个修复，把定位锚定到抽取出来的文本坐标上。

这是 eval-driven development 的精髓——**先定义成功，再动手写**。失败不再是一个模糊的「这个 Skill 好像不太行」，而是一个可复现、可定位、可修复的具体指标。

### 3.2 Benchmark Mode：标准化评估

新加的 benchmark mode 提供**标准化的评估流程**：用你的 evals 跑一次评估，记录 eval pass rate、elapsed time、token usage 三项核心指标。

这个能力看起来简单，但意义重大——它把 Skill 的质量**量化**了。模型升级前跑一次，模型升级后再跑一次，diff 直接告诉你这个升级对 Skill 的影响。这正是 R348 OpenAI Dreaming 提到的「stay current」目标在 Skill 维度的实现：不是被动等模型升级，而是主动测量变化。

### 3.3 多 Agent 并行执行：解决串行污染

传统串行 eval 跑得很慢，且**累积的上下文会污染后续测试**。skill-creator 现在能 spin up 独立 agents **并行**跑 evals——每个 agent 在干净上下文中执行，自带 token 和 timing metrics。

结果：**更快的结果，没有交叉污染**。这是 harness 设计的经典难题——如何在不牺牲隔离性的前提下提高 throughput。Anthropic 的解法和 OpenAI Codex 的 subagent 调度一致：**用并行 agent 换速度，用干净上下文换正确性**。

### 3.4 Comparator Agents：A/B 盲评

新加的 comparator agents 跑 A/B 对比——两个版本的 Skill，或者「有 Skill vs 无 Skill」。**关键设计：评判时不知道哪个是哪个**（blind comparison）。这消除了评判者的确认偏误——只有真正更好的版本才能持续胜出。

> "Two skill versions, or skill vs. no skill. They judge outputs without knowing which is which, so you can tell whether a change actually helped."

A/B 盲评在传统软件测试里没有直接对应物，但在 AI 产品迭代中已经是事实标准。Anthropic 把这个能力下放到 Skill 作者层，意义深远——领域专家不再需要求工程师帮忙做 A/B 框架，可以自己跑评测。

### 3.5 Trigger 描述调优：触发精度工程

Evals 测量输出质量，但**质量再好，Skill 不该触发的时候触发了，或者该触发的时候没触发，都是问题**。

随着 Skill 数量增长，description 的精度变得关键：太宽泛会有 false trigger（被错误激活），太窄又从不触发。skill-creator 现在能**自动分析你的当前 description 对照样本 prompts，建议修改，削减 false positive 和 false negative 两类错误**。

实战数据：Anthropic 在自己的 document-creation skills 套件上跑了这个工具，6 个公开 Skill 里有 5 个获得了触发改进。这是自动化 description 工程——领域专家不再需要靠直觉调参。

## 四、Skill 的未来：从 Implementation Plan 到 Specification

文章最后给出一个有哲学意味的观察：

> "As models improve, the line between 'skill' and 'specification' may blur. Today, a SKILL.md file is essentially an implementation plan, providing detailed instructions telling Claude how to do something. Over time, a natural-language description of what the skill should do may be enough, with the model figuring out the rest."

> "The eval framework we're releasing today is a step in that direction. Evals already describe the 'what.' Eventually, that description may be the skill itself."

这个判断和 OpenAI 的 Codex / Agent SDK 演进方向高度一致——**specification is the new code**。当模型能力足够强，**「成功标准」（eval 描述）可能就直接是 Skill 本身**，不需要中间的实现层。

但现在不是未来。SKILL.md 仍然是「如何做」的指令集，eval 是「什么是好」的检查器。两者的解耦让 Skill 作者可以分两层工作：先把成功标准写清楚（eval），再写实现（SKILL.md 指令）。

## 五、对 Harness Engineering 的三件事

1. **Eval-driven development 不是工程师的专利**。skill-creator 把 eval 写法的门槛从「会写 Python」降到「能描述预期行为」。这对**非工程师 Agent 构建**范式（R357）有直接增益——领域专家不只是写 SKILL.md，还能持续验证自己的 Skill。

2. **Skill 生命周期是「持续监控」问题，不是「一次性发布」问题**。模型升级会让 Skill 失效或冗余。skill-creator 的 benchmark mode + 定期重跑 = Skill 的可观测性基础设施。

3. **多 agent 并行 + 盲评 = Skill 迭代的正确姿势**。这与传统 A/B 测试的统计严谨性一致，但载体是 LLM agent。

## 六、和仓库已有内容的对位

- **vs R348 OpenAI Dreaming**：skill-creator 的 benchmark mode 是「stay current」目标在 Skill 维度的实现——主动测量模型变化对 Skill 的影响。
- **vs R406 Subagents in Claude Code**：skill-creator 的多 agent 并行执行是 Claude Code subagent 能力的应用层兑现——同一底层能力（独立 agent 隔离上下文）支持不同产品功能。
- **vs R475 OpenAI AI Chemist multi-agent harness loop**：两篇文章都把「多 agent + 评判回路」作为核心模式，但 OpenAI 强调是科研 Agent 内部，Anthropic 强调是 Skill 开发工具。
- **vs R379 Eval-Driven Development（OpenAI）**：R379 讲 TDD-style eval workflow，R489 讲「不需要写代码就能用 eval」——同一趋势的两个不同主体边界（工程师 vs 领域专家）。

## 引用源

> 原文：[Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
> 发布日期：2026 年 3 月 3 日
> 来源类别：🔴 Anthropic Claude Blog（一手源）
> 文章字数：约 5 分钟阅读（原始 1100 字 + Anthropic 内部数据）
