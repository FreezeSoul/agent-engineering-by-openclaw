# GitHub Security Lab Taskflow Agent：MCP 原生多智能体安全研究框架

> 原文：https://github.blog/security/ai-supported-vulnerability-triage-with-the-github-security-lab-taskflow-agent/

## 核心问题：为什么传统静态分析在漏洞 triage 上总是输给人工审计？

CodeQL 扫描会产生大量警报，但其中的误报率让安全团队头疼。经验丰富的审计员能在几秒内判断「这个警报是误报」——比如一个 GitHub Actions 触发事件是 `pull_request` 而非 `pull_request_target`，意味着它运行在非特权上下文。但这种判断依赖的是**语义理解**，而非代码模式匹配。传统静态分析工具无法编码这种模糊逻辑。

GitHub Security Lab 的答案是：**不要试图让 LLM 做端到端漏洞发现，而是用 Taskflow 将 LLM 嵌入人工审计工作流，让它做最擅长的部分**。

## 什么是 Taskflow？

Taskflow 是 YAML 配置文件，描述了一系列由多个 Agent 协作完成的审计任务。它的设计哲学是：

> **用 Prompt 级别的问题定义来捕获漏洞模式，随着前沿模型能力演进，安全研究结果将大规模改善。**

框架构建于 OpenAI Agents SDK 之上，同时支持 MCP（Model Context Protocol）工具集成。

### 核心架构：三阶段工作流

```
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Information Collection（信息收集）                  │
│  ├─ 获取权限配置、触发事件、工作流禁用状态                   │
│  ├─ 通过 MCP server 调用 GitHub API                        │
│  └─ 将结果序列化为「audit notes」供下一阶段使用             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Audit Issue（审计判断）                           │
│  ├─ 检查触发事件是否能被攻击者触发                           │
│  ├─ 检查工作流是否运行于特权上下文                           │
│  ├─ 检查是否有 sanitizer 存在                               │
│  └─ 大量误报在这个阶段被过滤                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: Report Generation + Validation（报告生成与验证）    │
│  ├─ 生成漏洞报告，包含精确代码引用和行号                     │
│  ├─ 验证报告格式和内容完整性                                 │
│  └─ 不满足条件则标记为误报并丢弃                            │
└─────────────────────────────────────────────────────────────┘
```

### Taskflow 的关键工程决策：分而治之

Taskflow 将复杂任务拆解为独立步骤，每个步骤有清晰的目标和验证条件。这种设计解决了 LLM 在长程任务中的常见失败模式：

> **如果给 LLM 一个包含 15 个子步骤的长 Prompt，至少有 3 个会被遗漏或敷衍完成。Taskflow 强制每个步骤独立执行并验证，降低复合误差。**

GitHub Security Lab 使用的另一个关键机制是**批量「for loop」风格任务**。审计 CodeQL 警报时，需要对每个警报应用相同的 prompt，但用不同的警报详情替换。Taskflow Agent 支持模板化 prompt 迭代，这是人工审计中最大的重复性工作量来源。

## 实战成果：2 个月，40 个仓库，91 个真实漏洞

从 2025 年 8 月开始的两个月里，GitHub Security Lab 使用 Taskflow Agent 审计了约 40 个开源仓库的 CodeQL 警报。模型仅被赋予获取文件和搜索的基础工具，没有使用任何静态或动态分析工具（仅用于生成 CodeQL 警报）。

结果：
- LLM 最初建议了 **1,003 个问题**
- 审计后标记为漏洞 **139 个**
- 去重后人工验证，最终报告 **91 个漏洞**
- 其中 **30+ 个已修复并公开披露**

使用的模型主要是 **Claude Sonnet 3.5**，大部分通过 OpenAI Agents SDK 的 handoff 机制实现 Agent 间的任务交接。

## 为什么 LLM 在漏洞 triage 上比传统工具更有效？

传统 SAST 工具依赖规则匹配，无法理解上下文语义。例如，判断一个 GitHub Actions 工作流是否「运行在特权上下文」需要知道：

1. 触发事件是 `pull_request`（非特权）还是 `pull_request_target`（特权）
2. 工作流是否有 `permissions: write-all` 声明
3. 调用方工作流是否设置了 `pull_request_target` 触发且有特权

这些检查需要理解代码语义，而非简单的正则匹配。人类审计员靠的是「我知道这种情况通常意味着什么」，这正是 LLM 从训练数据中学会的模式。

### 关键：减少幻觉的工程实践

GitHub Security Lab 发现，严格的任务定义可以大幅降低幻觉率：

> *"你应该在 notes 中包含精确的文件和行号引用，以及被调用的非信任代码或包管理器的名称。"*

这种精确性要求强制 LLM 做出可验证的声明，而非模糊的推测。验证失败时，Taskflow 会标记该报告为无效。

## MCP 集成的价值

Taskflow Agent 内置了多个 MCP server，最关键的是 **CodeQL MCP Server**。这个 server 不让 Agent 自己生成 CodeQL 查询，而是提供基于模板的 CodeQL 查询工具，让 Agent 用查询结果作为上下文来导航代码库。

这是一个重要的设计选择：**不要让 Agent 生成 CodeQL，而是给它工具去使用 CodeQL**。前者容易产生语法错误和幻觉查询，后者利用 CodeQL 本身的能力，只让 Agent 负责理解结果。

## 局限性与边界

GitHub Security Lab 明确指出 Taskflow Agent 不是端到端漏洞发现工具。它的能力边界是：

- **擅长**：分类 triage、识别误报原因、基于规则的语义判断
- **不擅长**：发现全新的漏洞模式、生成可执行的漏洞利用代码

这与他们的使用场景一致：用 LLM 做 triage 过滤，而不是做原始漏洞发现。原始发现仍然需要安全研究员的领域知识和创造力。

## 笔者的判断

GitHub Security Lab Taskflow Agent 的价值在于它**正确地框定了 LLM 在安全审计中的角色**：不是取代人工审计，而是将人工审计中最重复的部分自动化。它找到了一个真正的 sweet spot：

> **「很多重复步骤，每个步骤有清晰定义的目标，但步骤之间的判断依赖语义而非代码模式。」**

这是 LLM 自动化的完美场景。而那些试图用 LLM 直接做端到端漏洞发现的方案，往往会在幻觉和误报上挣扎。

框架本身已开源（MIT License），任何安全团队都可以基于此开发自己的 triage taskflow。关键学习是：**Taskflow 设计决定了上限，而不是模型能力**。

---

**引用来源**：
- GitHub Security Lab 官方博客：https://github.blog/security/ai-supported-vulnerability-triage-with-the-github-security-lab-taskflow-agent/
- GitHub Security Lab Taskflow Agent 仓库：https://github.com/GitHubSecurityLab/seclab-taskflow-agent
- seclab-taskflows 仓库：https://github.com/GitHubSecurityLab/seclab-taskflows