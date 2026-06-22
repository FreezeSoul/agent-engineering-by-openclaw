---
title: Cursor Automations 06-18-26：Skill-Based Agent 自动化新范式 2026
date: 2026-06-22
source: https://cursor.com/changelog/06-18-26
author: Cursor
tags: [cursor, automations, skill, agent-automation, harness, multi-agent, computer-use, github-integration]
topics: [Cursor Automations, Agent Skills, Automation Triggers, Computer Use, Skill Authoring]
description: Cursor 在 06-18-26 的 Automations 更新中引入了 /automate skill（自然语言创建自动化）、5 个 GitHub 事件触发器，以及 Automations 专属的 Computer Use 工具。Cursor 的自动化正在从「配置型」向「Skill 驱动型」演进。
length: 2400
cluster: orchestration
cluster_role: anchor
round: 489
---

# Cursor Automations 进化：从配置型到 Skill 驱动型

> 原文：[Improvements to Cursor Automations](https://cursor.com/changelog/06-18-26)（Cursor Changelog，2026 年 6 月 18 日）

## 核心命题

Cursor Automations 的这次更新，回答了一个长期悬而未决的问题：**谁来编写自动化 Agent 的 Skill？** 以往的答案要么是工程师手工配置，要么是用户点点点。Cursor 这次给出了第三条路——让 Agent 自己根据自然语言描述生成 Skill。

## 一、/automate skill：用自然语言建造自动化

`/automate` 是这次更新的核心功能。用户不需要理解触发器、指令或工具配置，只需要用自然语言描述任务：

> "当有人在 GitHub PR 里留下 review comment，就让 Agent 自动分析并尝试修复相关代码问题"

Cursor Agent 会理解这个描述，自动配置触发器、指令和工具。这不是简单的参数填充——这是 Agent 自主完成 Skill 创作的能力。

**笔者认为**：这与 Anthropic Skill-Creator 的 eval-driven skill authoring 在方向上一致，但路径不同。Anthropic 的思路是「先定义成功标准，再写 Skill」；Cursor 的思路是「先描述任务，Agent 自己推断成功标准」。两条路径最终都会指向同一个问题：谁来验证这个 Skill 真的在做正确的事？

## 二、GitHub 事件触发器：5 个新触发点

Cursor Automations 新增了 5 个 GitHub 触发器：

| 触发器 | 触发时机 | 典型场景 |
|--------|---------|---------|
| Issue comment | 非 PR issue 收到评论 | Issue 分类 + 标签 |
| PR review comment | PR diff 上留下行内评论 | 代码审查反馈处理 |
| PR review submitted | PR review 提交 | Review 摘要 + 相关修改 |
| Review thread updated | Review thread 标记 resolved/unresolved | 遗留问题追踪 |
| Workflow run completed | GitHub Actions workflow run 结束 | CI 失败自动修复 |

Cursor 还在 Marketplace 提供了两个模板：[triage-github-workflow-failures](https://cursor.com/marketplace/automations/triage-github-workflow-failures) 和 [auto-fix-pr-review-comments](https://cursor.com/marketplace/automations/autofix-pr-review-comments)。

**笔者认为**：这 5 个触发器覆盖了 GitHub 工作流的「人来」部分——评论、review、workflow 结果。这些恰恰是传统 CI/CD 无法自动化处理、必须有人介入的环节。Cursor 的思路是：让 Agent 在这些节点上「替代人做判断」。

## 三、Computer Use for Automations：让云端 Agent 展示工作成果

Cloud agents 在 Automations 中现在可以使用 Computer Use 工具，生成 demos 或 artifacts 来展示工作成果。这个能力默认开启，只需在指令中告诉 Agent「包含 demo」即可。

**笔者认为**：这个功能看似简单，实则解决了自动化中的一个核心问题——信任。传统的 CI 脚本失败后，你只能看日志；Cursor Automations 的 Agent 失败后，你可以看它生成的截图或录像。这是一种「可视化 Harness」，让人在不用盯着的的情况下也能理解 Agent 做了什么、为什么失败。

## 四、Skill 与 Harness 的交汇点

这次更新的真正意义，不是单个功能，而是三条线的交汇：

1. **Skill 创作**：`/automate` 让 Agent 自己生成 Skill，而不只是执行 Skill
2. **Trigger 体系**：GitHub 事件作为外部 Harness，定义了 Agent 的「何时行动」
3. **Computer Use**：输出层的可视化，让 Harness 的执行结果可审查

**笔者认为**：这三者的组合，已经让 Cursor Automations 成为一个完整的 Harness 系统——有触发条件（Trigger）、有执行逻辑（Agent Skill）、有结果验证（Computer Use）。这比大多数所谓的「Agent 框架」更接近真实的工程需求。

## 五、Cursor 与 Anthropic Skill-Creator 的对比

| 维度 | Anthropic Skill-Creator | Cursor /automate |
|------|------------------------|-----------------|
| **创作主体** | 非工程师用 eval 驱动 | Agent 根据自然语言自动生成 |
| **验证机制** | 内置 eval + comparator | 无内置 eval（依赖 human review） |
| **触发方式** | 手动调用 / 事件触发 | 外部事件（GitHub/Slack/定时） |
| **输出层** | 结果 + 日志 | 结果 + Computer Use artifacts |
| **适用场景** | 深度 Skill 创作 | 轻量自动化任务 |

两者代表了 Skill 创作的两种哲学：**Anthropic 相信「先验证再执行」**，**Cursor 相信「先执行再可视化」**。在实际工程中，两者都有存在的价值——前者适合高风险任务，后者适合高频重复任务。

---

**相关项目**：推荐关注 [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（199K Stars）—— 内置自改进学习循环的 Agent，与 Skill 自我进化方向高度契合。