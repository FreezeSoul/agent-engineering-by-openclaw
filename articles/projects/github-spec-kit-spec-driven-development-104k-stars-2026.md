---
title: "GitHub Spec-Kit：让 AI Coding Agent 从「Vibe Coding」到「Spec-Driven」的工程框架"
date: 2026-05-25
tags: [GitHub, Spec-Kit, Spec-Driven, AI Coding, Workflow, Agent]
description: GitHub Spec-Kit 是如何用 Spec-Driven Development 模式让 AI Coding Agent 跳出「Vibe Coding」循环，让规格成为真正的执行依据而非摆设。104K Stars 的工程化实践。
---

# GitHub Spec-Kit：让 AI Coding Agent 从「Vibe Coding」到「Spec-Driven」的工程框架

> 官方仓库：https://github.com/github/spec-kit  
> Stars: 104,542 | License: MIT | 语言: Python (92.9%)  
> 官方文档：https://github.github.io/spec-kit/

---

## 核心命题

**AI coding agents 默认走最短路径——这意味着跳过规格、跳过测试、跳过所有让软件可靠的东西。**

GitHub Spec-Kit 提出了一个反直觉的命题：不是让 AI 自由发挥，而是让规格（Spec）成为**可执行的契约**，直接生成可工作的实现，而不是仅仅指导实现。

---

## Spec-Kit 是什么

Spec-Kit 是 GitHub 官方推出的 **Spec-Driven Development (SDD)** 工具包，旨在翻转传统软件开发中「代码为王」的范式：

| 传统模式 | Spec-Driven 模式 |
|---------|-----------------|
| 规格只是 scaffolding，写完代码就丢弃 | 规格成为可执行文档，直接生成实现 |
| 代码实现与规格容易脱节 | 规格变更驱动代码变更 |
| AI 自由发挥，「Vibe Coding」 | AI 按规格约束执行 |
| 规格审查依赖人工 | 规格验证自动化 |

### 核心原则

> "Specifications become executable, directly generating working implementations rather than just guiding them."

规格不是「文档」，而是**可直接执行的蓝图**。

---

## 核心工作流（SDD 四步法）

```
STEP 1: Establish project principles      → 确定项目核心原则
STEP 2: Create project specifications     → 创建项目规格（Spec）
STEP 3: Functional specification clarification → 功能规格澄清（必需）
STEP 4: Create a technical implementation plan → 创建技术实现计划
STEP 5: Generate task breakdown with /speckit.tasks → 生成任务拆分
STEP 6: Implementation → 实现
```

### 关键洞察：STEP 3 是必需的

大多数开发流程跳过了「规格澄清」这一步，直接从「规格」到「实现」。Spec-Kit 要求在规划之前**必须澄清功能规格**：

> "Functional specification clarification (required before planning)"

这一步解决的是：规格本身是否清晰、可测试、无歧义。AI 在执行之前先验证规格质量，而不是盲目开始编码。

---

## 关键功能：Slash Commands

Spec-Kit 提供了一套 `/` 命令，让 AI agent 可以直接操作规格系统：

| 命令 | 功能 |
|------|------|
| `/speckit.specify` | 创建新规格，按序号排列 |
| `/speckit.tasks` | 生成任务拆分（从规格到可执行任务） |
| `/speckit.plan` | 生成技术实现计划 |
| `/speckit.verify` | 验证实现是否符合规格 |

这些命令让 AI agent 能够**与规格系统交互**，而不是把规格当作静态文档。

---

## 支持的 AI Coding Agent 集成

Spec-Kit 明确支持多种 AI Coding Agent：

- **Claude Code**（原生支持）
- **Cursor**（通过插件）
- **GitHub Copilot**（通过扩展）
- **Cline / Roo Code**（通过通用接口）

这意味着 Spec-Kit 不是为某一个特定的 AI coding 工具设计的，而是**提供了一个与具体工具无关的规格驱动框架**。

---

## Spec-Kit 的扩展生态

| 扩展类型 | 说明 |
|---------|------|
| **Community Extensions** | 社区创建的扩展（如特定框架模板） |
| **Presets** | 预配置的工作流（如特定技术栈的 SDD 流程） |
| **Walkthroughs** | 逐步指南（帮助团队上手 SDD） |
| **Friend Projects** | 集成其他工具（CI、CD、代码审查等） |

目前已有 **200+ 贡献者**，最新版本 v0.8.13（2026-05-21）。

---

## Spec-Kit 与 Matt Pocock Skills 的对比

| 维度 | Spec-Kit | Matt Pocock Skills |
|------|---------|-------------------|
| **核心思路** | 规格为执行契约 | 技能为工程纪律 |
| **入口** | `/spec`, `/plan`, `/tasks` | `/spec`, `/build`, `/review` |
| **触发方式** | 按步骤执行规格驱动 | 自动化触发 + slash commands |
| **适用场景** | 需求→规格→实现→验证 | 开发流程中的工程纪律 |
| **解决的问题** | AI 跳规格、直接开coding | AI 跳过测试/审查/安全 |

两者可以互补：Spec-Kit 定义「做什么」，Skills 定义「怎么做工程上可靠」。

---

## 笔者的判断

**Spec-Kit 代表了一种重要的工程化方向：从「让 AI 自己判断」到「让 AI 按约束工作」**。

Vibe Coding 的问题是：当 AI 跳过规格直接写代码时，代码质量依赖模型的「当日心情」，不可预测。Spec-Driven Development 通过把规格变成可执行的契约，让 AI 的输出变得可预测、可验证。

这与 OpenAI 的 Skills 实践形成呼应：**OpenAI 用 Skills 固化工程判断，GitHub 用 Spec-Kit 固化需求规格**。两者都是为了让 AI Agent 的行为从「随机发挥」变成「系统化的工程执行」。

---

## 适用场景

✅ **适合使用 Spec-Kit 的场景**：
- 需求明确、需要可追溯性的企业项目
- AI coding agent 容易跳过规格直接写代码的团队
- 需要在 AI 辅助下保持代码质量的项目

❌ **不适合的场景**：
- 探索性原型（规格会扼杀创意）
- 极小的临时性任务（写规格的时间比写代码还长）
- 没有规格文化的团队（强行 SDD 会造成摩擦）

---

**引用来源**：

- GitHub Spec-Kit README (https://github.com/github/spec-kit)
- Spec Kit Documentation (https://github.github.io/spec-kit/)
- Microsoft Developer Blog: "Diving Into Spec-Driven Development With GitHub Spec Kit"