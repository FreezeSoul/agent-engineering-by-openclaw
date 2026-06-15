---
title: Claude Code Auto Mode：双层权限判断的 Harness 工程实践
date: 2026-06-16
source: Anthropic Engineering Blog
author: Anthropic
tags: [harness, claude-code, permission, classifier, security, agentic-coding]
topics: [Claude Code, Agent Security, Permission System, Auto Mode]
description: Anthropic 如何在 Claude Code 中构建双层权限判断系统，用 Sonnet 4.6 分类器替代 93% 的人工审批，同时保持安全边界。
length: 2600
cluster: harness
cluster_role: anchor
round: 398
---

# Claude Code Auto Mode：双层权限判断的 Harness 工程实践

> 原文：[How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode)（Anthropic Engineering Blog）

## 核心命题

Claude Code 的 auto mode 本质上是一套**双层权限判断 Harness**：输入层扫描工具输出中的提示注入，输出层用 Sonnet 4.6 分类器评估每个操作的安全性，用机器替代 93% 的人工审批，同时保持安全边界不崩塌。这不是简单的「自动化」，而是一种**精确的权限委托机制**——把「信任决策」从运行时移到配置时，从人类点击移到分类器规则。

## 背景：为什么需要 Auto Mode

Claude Code 默认在执行命令或修改文件前请求用户审批。这个设计很安全，但也很烦人：用户最终会习惯性点击「同意」，审批变成了仪式，安全价值归零。Anthropic 的数据印证了这一点——**Claude Code 用户批准了 93% 的权限提示**。这个数字说明的不是用户信任 Agent，而是用户陷入了审批疲劳。

> "Over time that leads to approval fatigue — and approval fatigue is not the same as trust."

审批疲劳不是信任，是麻木。而麻木的审批比没有审批更危险：它让恶意提示注入有机会在「反正你会同意」的惯性里溜进去。

Auto mode 要解决的不是「要不要安全」，而是「如何在保证安全的前提下，让安全检查本身不成为负担」。

## 双层防御架构

Auto mode 由两层独立的防御组成，各自解决不同类别的威胁：

### 第一层：输入层——提示注入检测

当 Agent 调用工具（读文件、Web Fetch、Shell 输出、外部工具响应）时，工具的输出先经过**服务器端提示注入探针**扫描，再进入 Agent 的上下文。

```
工具输出 → 注入探针扫描 → 上下文（如果干净）→ Agent 推理
```

这个设计的精妙之处在于：它在 Agent 看到内容之前就拦截了问题。提示注入的核心手法是将恶意指令藏在看起来无害的输出里（文件内容、Web 页面、命令结果），期待 Agent 在后续推理中「无意」执行这些指令。注入探针在数据进入上下文之前就切断这条链路。

注入探针不是大模型判断，而是一个规则/模式匹配系统，原因很简单：延迟和成本。用轻量级规则快速过滤「明显异常」的模式，把真正模糊的判断留给输出层。

### 第二层：输出层——操作分类器

通过注入层检测后，Agent 的每个操作在执行前还要经过**Transcript Classifier**的评估。这是个运行在 Sonnet 4.6 上的分类器，输入是完整的对话上下文，输出是四类决策：

| 决策 | 含义 | 例子 |
|------|------|------|
| **自动批准** | 安全，直接执行 | `git status`、读文件 |
| **确认** | 需要用户看一眼 | 删除多个文件、重写核心模块 |
| **阻止** | 危险操作 | 尝试删除系统目录、执行可疑脚本 |
| **跳过** | 无法判断 | 不确定上下文是否干净 |

关键设计点：**决策不是二元的，是四类的**。很多 Agent 系统把权限判断做成二元（允许/阻止），这其实是在强制 Agent 做不可能的判断——现实中大量操作处于「基本安全但需要确认」的灰色地带。四类决策让系统的表达力大幅提升。

### 两层的协作逻辑

```
输入层（注入检测）
    ↓ 干净通过
Agent 推理
    ↓ 输出操作
输出层（分类器判断）
    ↓ 决策分类
自动批准 / 确认 / 阻止 / 跳过
```

两层各有分工：**输入层解决外部威胁**（提示注入），**输出层解决内部推理风险**（诚实错误 + 过度行为）。

## 威胁模型：两类需要区分的风险

Auto mode 的设计哲学建立在对两类风险的清晰区分上：

**第一类：提示注入攻击**。恶意文本通过工具输出注入到 Agent 上下文，诱导 Agent 执行非预期操作。输入层负责切断这条链路。

**第二类：诚实错误**。Agent 本身的推理没有问题，但因为对项目结构、用户意图或系统状态理解不足，执行了一个破坏性操作——比如删错了文件、改错了配置。这类错误输入层检测不出来（内容本身没有恶意），只有输出层能通过「操作上下文」判断。

> "We have specific examples of this behavior from internal model testing."

Anthropic 明确指出，诚实错误是第二层的主要目标，而分类器对「过度行为」（over-eager behavior）做了特殊调优——因为这类行为在内部测试中有大量样本。

**为什么分类器用 Sonnet 4.6 而不是更小的模型？**

因为判断的输入是**完整对话上下文**。Agent 需要理解「这个删除操作在项目生命周期中的位置」，而不是「这条命令本身危险不危险」。这是一个需要全局推理的任务，不是简单的规则匹配。

## 工程实现细节

### 分类器决策标准

Transcript Classifier 的判断基于以下维度（原文描述）：

1. **操作的破坏性范围**：单文件修改 vs 多文件批量修改 vs 系统目录删除
2. **上下文的清晰度**：Agent 是否明确知道自己在做什么
3. **历史行为一致性**：Agent 的行为模式是否符合用户的历史偏好
4. **操作可逆性**：如果出了问题，回滚有多难

这四个维度组合在一起，形成了比「命令类型」更丰富的判断基础。比如同样是删除操作，在 Git 管理下的单文件删除 vs 根目录删除，在分类器眼里是完全不同的风险级别。

### 调优策略：宁可误拦，不可漏放

> "Our classifier is tuned to overeager behavior and honest mistakes."

分类器被调优到**宁愿多阻止、少放过**。这与安全系统的经典原则一致：false negative（漏过危险操作）的代价远高于 false positive（误拦安全操作）。但调优方向本身是有代价的——如果 false positive 率太高，用户会感到沮丧，重新回到手动审批的老路。

93% 的人工审批率意味着什么？意味着在 auto mode 上线之前，用户平均批准了 93% 的操作。那么 auto mode 的目标是：把这 93% 中**真正安全的操作**自动化，把剩下 7% 中**真正需要人工判断的**保留人工审批，同时在 93% 中**不引入额外的危险**。

### 与传统白名单的区别

传统的 Agent 权限系统通常用**白名单**或**规则列表**来控制权限：允许执行哪些命令、禁止执行哪些命令。白名单的问题在于它是静态的——无法根据上下文判断「在当前项目里删除 node_modules 是否安全」。

Auto mode 的输出层分类器是**上下文感知的动态判断**，不是静态规则。这是它与传统安全系统的本质区别。

## 与 Harness Engineering 的关联

R396 分析了 Harness Engineering 的配置优先原则，而 auto mode 是该原则的**具体工程实现**：

| Harness 维度 | Auto Mode 实现 |
|-------------|---------------|
| **Stop Hook** | 输出层分类器的「阻止」决策 |
| **条件判断** | 四类决策分类（自动批准/确认/阻止/跳过）|
| **权限分层** | 输入层（注入检测）vs 输出层（操作分类）|
| **渐进式授权** | 93% 自动化 + 7% 保留人工审批 |

更重要的是，auto mode 的设计者意识到：**审批疲劳是安全的天敌**。一个因为太麻烦而被绕过的安全系统，比没有安全系统更危险。这直接呼应了 Harness Engineering 的核心洞察——安全机制必须与开发者体验协同设计，否则会被人类绕过。

## 局限性

Auto mode 不是银弹。Anthropic 明确指出了它的局限：

1. **注入检测仍有盲区**：复杂的多步注入可能绕过探针
2. **诚实错误的判断不完美**：分类器对项目上下文的理解仍有局限
3. **「跳过」决策的处理**：当分类器无法判断时，系统必须退回到人工审批，这是正确的 fallback，但会打断流程

## 对 Agent 工程实践的启示

Auto mode 提供了一个重要的工程范式：**把「信任决策」从运行时移到配置时**。

传统做法：Agent 运行时问用户「我这样做可以吗？」
Auto mode 做法：配置时定义规则，运行时由分类器按规则执行，人只处理规则外的例外。

这与安全领域的「纵深防御」理念一致：每一层只解决自己能解决的问题，把无法确定的判断交给下一层，而不是全部推给用户。

> "The best security is security that doesn't get in your way — until it needs to."

## 引用

> "By default, Claude Code asks users for approval before running commands or modifying files. This keeps users safe, but it also means a lot of clicking 'approve.' Over time that leads to approval fatigue — and approval fatigue is not the same as trust."
> — Anthropic Engineering, "How we built Claude Code auto mode"

> "At the output layer, the transcript classifier evaluates each action against a set of decision criteria before it executes, acting as a substitute for a human approver."
> — Anthropic Engineering, "How we built Claude Code auto mode"

> "Our classifier is tuned to overeager behavior and honest mistakes, as we have specific examples of this behavior from internal model testing."
> — Anthropic Engineering, "How we built Claude Code auto mode"

---

*Anthropic Engineering Blog | 2026-06-16 | [原文](https://www.anthropic.com/engineering/claude-code-auto-mode)*