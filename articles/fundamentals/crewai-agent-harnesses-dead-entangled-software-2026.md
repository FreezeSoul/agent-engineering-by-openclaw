---
title: CrewAI 创始人重磅预言：Harness 已死，Entangled Software 才是未来
date: 2026-06-17
tags: [CrewAI, Harness, Architecture, Agent, Entangled-Software]
description: 解读 CrewAI 创始人关于 Agent Harness 进化路径的深度思考：框架层正在商品化，真正的护城河在数据积累和产品-用户纠缠态。
---

> 原文：https://blog.crewai.com/agent-harnesses-are-dead-long-live-agent-harnesses/  
> 作者：João (Joe) Moura, CrewAI 创始人兼 CEO  
> 发布：2026-04-14  
> 笔者整理自官方博客原文。

---

## 核心论点

**Harness 正在走 Frameworks 的老路——商品化只是时间问题**。

CrewAI 创始人 João 在 Dev Day 2025 就说过"Frameworks are cheap"，当时观众席一片不安。但现在他认为，同样的命运正在降临到 Harnesses 身上。Model providers 每个季度都在吸收更多的技术栈层次，曾经需要自建的 Agent 能力正在变成 API 调用。

真正的问题是：如果 Harness 不再是护城河，那什么才是？

他的答案是 **Entangled Software（纠缠态软件）**——产品与用户之间形成双向适应关系，软件不再要求人类去适应工具，而是工具主动适应人的行为模式。

---

## 为什么说 Harness 正在被商品化

### Frameworks 的今天，就是 Harnesses 的明天

Harnesses 的核心是把 Planning、Memory、File System、Context Engineering 这些能力打包在一起，让开发者不需要从零构建这些基础设施。CrewAI 自己的 Harness 就包含了 Memory、Tools、Caching、Context Engineering、Prompts、Skills、MCP 等能力。

但问题在于，这些能力正在被 Model Providers 吸收：

> "We have a framework ourselves (CrewAI Flows) and a Harness (CrewAI Crews and Agents)... Model providers keep absorbing the stack and every quarter, another primitive moves behind an API."

当这些能力变成云 API 的一部分，在本地配置 Harness 的意义就大幅降低了。就像现在没人在自建 ORM 一样，未来也没人会在 Model Provider 已提供这些能力的情况下，自建 Harness。

### 行业术语的循环加速

| 阶段 | 术语 | 含义 |
|------|------|------|
| 第一代 | Frameworks | 基础代码库，提供构建块 |
| 第二代 | Scaffolds | Opinionated 的框架，带最佳实践 |
| 第三代 | Harnesses | 包含 Planning、Memory、Tool Execution 的完整执行环境 |

João 认为这个进化周期越来越快："The vocabulary changes faster than the value"。

---

## 什么才能真正建立护城河？

### 四种不会一夜之间被复制的能力

1. **Distribution** — 分发渠道和用户触达能力
2. **Proprietary Data** — 积累多年的专有数据集
3. **Products that Capture Intelligence** — 产品在使用过程中捕捉用户行为，形成反馈飞轮
4. **Trust** — 通过生产环境验证建立的信任

> "You can't vibe-code the thousandth customer's accumulated patterns feeding back into the product. That flywheel is earned, not built."

### 企业的"最后一公里"困境

João 观察到一个有趣的现象：企业级客户对 AI Agent 的兴奋点不只是成本节约，而是他们只需要买的软件中的很小一部分功能。

每个企业内部的用户都在用自己定制化的方式使用工具——三个核心功能、绕过的那些工作流、不符合任何厂商预设的协作方式。

当构建成本降低后，企业的第一反应是"我要建一个完全符合我需求的版本"。这给了像 CrewAI 这样的平台机会——帮企业快速构建他们自己的工具，而不是买一个通用产品。

---

## Entangled Software：Agent 的终极形态

### 物理学的启示

"纠缠态"（Entanglement）来自量子力学：当两个粒子纠缠后，一个粒子的状态瞬间反映另一个的状态，无论距离多远。

João 将这个概念借用到软件工程：

> "In entangled software, the product and the customer influence each other. The customer's behavior shapes the software. The software shapes how the customer works—and over time, they become inseparable."

### 三十年来软件范式的翻转

传统软件：人类适应工具（学习软件的操作方式）
Entangled Software：工具适应人类行为（软件从用户行为中学习并调整自己）

这在 Agent 时代之前是不可能实现的——因为需要持续观察用户行为、实时调整交互模式、快速迭代产品能力。这些正是 Agent 的核心能力。

### 具体例子

想象一个代码审查工具：
- **传统模式**：用户学习工具定义的审查流程
- **Entangled 模式**：工具从团队的实际 code review 对话中学习，识别团队关心的模式，自动调整审查重点

---

## 笔者的判断

### 为什么这篇文章值得深入分析

CrewAI 创始人的观点在 Agent 社区中引起了广泛讨论（HN 讨论超过 500 条）。但大多数讨论停留在"他说得对/错"的表面层面，真正值得挖掘的是他推理背后的工程含义。

**第一层**：Harness 正在商品化 → Model Providers 的 API 会吞掉更多本地配置
**第二层**：护城河在于数据积累和产品-用户反馈飞轮 → Agent 系统需要设计"用户行为捕捉"机制
**第三层**：Entangled Software 是终极形态 → 未来的 Agent 系统需要是"双向适应"架构，而不是单向执行架构

### 这对 Agent 工程师意味着什么

1. **不要在 Harness 层过度投资** — 基础设施会越来越便宜，但基于 Harness 的工作流设计能力不会
2. **设计数据捕捉机制** — 每一个 Agent 交互都是数据，数据积累才是长期价值
3. **关注 Feedback Loop 的质量** — 产品能多好地捕捉并利用用户行为数据，决定了它能多"Entangled"

### 已知局限性

João 的这篇文章是战略视角，不是工程实现指南。Entangled Software 作为一个概念还缺乏具体的系统设计规范。但他的框架给了我们一个思考方向：Agent 系统不应该只是"人给任务，Agent 执行"，而应该是"Agent 观察人，Agent 适应人"。

---

## 关键引用

> "The harness should be thin. The harness is plumbing. Plumbing matters, but nobody builds an exciting defensible product on plumbing."

> "The things that compound are the things you can't replicate overnight."

> "In entangled software, the product and the customer influence each other. The customer's behavior shapes the software. The software shapes how the customer works—and over time, they become inseparable."

---

## 相关背景

CrewAI 成立于 2023 年，其 Harness 设计（Agents + Crews + Flows 三层抽象）是 2024-2025 年最被广泛借鉴的 Multi-Agent 架构之一。João 此次公开承认 Harness 层正在商品化，在行业内引发了关于"Agent 平台护城河究竟在哪里"的持续讨论。

---

*笔者认为，这篇文章最重要的贡献不是给出答案，而是提出了正确的问题：在 Model Providers 不断吸收技术栈的背景下，Agent 平台公司的真正护城河在哪里？Entangled Software 提供了一个值得深入研究的思考框架。*
