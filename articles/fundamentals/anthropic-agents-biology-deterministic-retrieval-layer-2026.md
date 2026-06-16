---
title: "为什么科学 Agent 总是差点意思：答案在基础设施，不在推理"
date: 2026-06-16
tags:
  - Agent工程
  - 基础设施设计
  - Tool Use
  - 科学Agent
  - Deterministic Layer
categories:
  - fundamentals
  - tool-use
---

# 为什么科学 Agent 总是差点意思：答案在基础设施，不在推理

> Anthropic Research 的一篇新文章揭示了一个反直觉的结论：科学 Agent 的瓶颈不是推理能力，而是**缺乏确定性执行层**。这个发现对所有 Agent 开发者都有深远的工程启示。

---

## 一、反直觉的发现：强模型 ≠ 可靠 Agent

当 Laura Luebbert 和团队尝试让 AI Agent 从 NCBI Virus 数据库检索病毒序列数据时，发现了一个令人意外的现象：

> "Even the strongest models did not consistently achieve the level of accuracy required for reliable dataset construction. But accuracy rose to nearly 100% once she and her team added **gget virus**, a deterministic retrieval layer."

顶级模型（Claude、Biomni OSS、Edison Analysis、GPT）在**检索任务上全部失败**，直到加入一个确定性检索工具后，准确率才接近 100%。

这个结论颠覆了"模型强则 Agent 强"的直觉。

---

## 二、核心洞察：人类设计的基础设施是给人类用的

Laura 用了一个精妙的比喻来解释这个问题：

> "Using AI agents to navigate biological data infrastructure is like driving through an old city that was designed before cars: the infrastructure may be beautiful and even thoughtful, but it's full of narrow, winding streets that are difficult for modern vehicles to navigate."

软件基础设施是为人类设计的：
- 异构的文件格式
- 分散的数据库
- 一次性检索脚本
- 隐式的约定和上下文

而软件工程师享受的基础设施是这样的：
- 结构化的数字工作流
- 可靠的接口
- 版本控制
- 完善的文档和包管理器

**Agent 需要的是"高速公路"，而不是"羊肠小道"。**

---

## 三、确定性检索层：科学 Agent 的工程缺失

文章指出了一个关键工程概念——**Deterministic Retrieval Layer（确定性检索层）**：

### 什么是确定性检索层？

确定性检索层是一种**可预测、可复现、无歧义**的数据访问机制。它将：

| 人类友好但 Agent 不友好的 | 确定性检索层 |
|--------------------------|-------------|
| 浏览器点击工作流 | API 调用 |
| 隐式过滤规则 | 显式参数化查询 |
| 自然语言描述 | 结构化查询语言 |
| 一次性脚本 | 可复用工具 |

### 为什么科学 Agent 需要它？

文章举了一个 Ebola 疫情响应的例子：

2026 年 5 月，刚果民主共和国爆发了 Bundibugyo 型埃博拉病毒疾病。世界卫生组织在 14 天内报告了超过 1000 例确诊和疑似病例。

在这样的公共卫生危机中：
- 研究人员需要快速从 NCBI Virus 检索病毒序列
- 数据集构建的准确性直接影响疫情应对决策
- 一个小错误（如坐标引用错误的基因组版本）可能导致整个下游分析失效

**在生物学和科学研究中，即使是微小的错误也可能产生严重后果。**

---

## 四、Karpathy 的抱怨不是软件特有的问题

Andrej Karpathy 曾在一次演讲中描述了他用 AI coding agent 构建 Web 应用的经历：

> "The code was the easiest part! Most of the work was in the browser, clicking things."

他发现：代码是最简单的部分，大部分时间花在浏览器操作界面上。

Laura 指出，这种摩擦**在生物学中早已存在**，而且情况更严重：

- 计算生物学家几十年来一直在努力将生物学数据从浏览器界面中解放出来
- Biopython、BioPerl、BioJulia、Entrez Direct、BioMart、gget 等工具都是这种努力的一部分
- 但生物学数据不像软件数据那样结构化，它分布在"混乱的道路网络"中

**这不是 AI 能力的问题，这是基础设施的问题。**

---

## 五、工程启示：Agent 开发者需要思考什么？

### 1. 重新定义"Tool Use"

Tool Use 不是"给 Agent 一个 API"，而是"为 Agent 设计确定性执行层"。

| 传统 Tool Use | 确定性 Tool Use |
|--------------|-----------------|
| "有 API 就行" | API + 错误处理 + 重试 + 回退 |
| 人类理解上下文 | Agent 也能理解的显式语义 |
| 一次性调用 | 可组合、可验证、可审计 |

### 2. 评估 Agent 能力的新维度

现有的 Agent 评测基准（如 GAIA）主要关注推理和任务完成能力。但这篇文章揭示了一个被忽视的维度：

> **Agent 能否在不可靠的基础设施上稳定工作？**

这个问题的答案取决于：
- 是否有确定性检索层
- 是否有错误检测和恢复机制
- 是否有对不确定性的显式处理

### 3. "Infrastructure for Agent" 的设计原则

Laura 在文章结尾给出了方向：

> "If we want agents to help with scientific discovery, from outbreak response to drug design to biological modeling, we need to build biological data infrastructure that they can navigate as reliably as humans do."

这对 Agent 基础设施设计者的启示：
- **可审计性**：每个检索操作都应有明确的审计轨迹
- **确定性**：相同的查询必须返回相同的结果
- **可组合性**：工具之间可以组合成复杂工作流
- **容错性**：在部分工具失败时能优雅降级

---

## 六、超越科学 Agent：所有 Agent 都面临这个问题

虽然文章聚焦于生物学 Agent，但其洞察具有普遍性：

**当 Agent 插入为人类设计的工具环境时，都会遇到类似的摩擦。**

例子：
- 浏览器自动化（Browser Agent）→ 需要确定性 DOM 操作层
- 数据库查询（Data Agent）→ 需要确定性 SQL 生成和验证层
- API 调用（API Agent）→ 需要确定性的参数构造和错误处理层

**真正的瓶颈不在于模型的推理能力，而在于工具层的可靠性设计。**

---

## 七、结语：给 Agent 开发者的行动建议

1. **重新审视你的 Tool Use 实现**：它是否提供了确定性执行，还是只是一个 API 包装？
2. **添加验证层**：每个工具调用后，验证返回结果的正确性
3. **设计优雅降级**：当工具不可用时，Agent 能否用备选方案继续工作？
4. **构建可审计性**：记录 Agent 的每个关键决策，供人工审查

> "It does not matter how powerful the car is if the streets are too narrow, the turns too sharp, and the route depends on local knowledge."

**模型再强，基础设施不对，Agent 也跑不快。**

---

## 参考来源

- Anthropic Research: [Paving the way for agents in biology](https://anthropic.com/research/agents-in-biology) (2026-06-08)
- 原始研究论文: [arXiv:2606.06749](https://arxiv.org/pdf/2606.06749)
- gget 工具: [github.com/bihealth/gget](https://github.com/bihealth/gget)
- NCBI Virus: [https://www.ncbi.nlm.nih.gov/labs/virus](https://www.ncbi.nlm.nih.gov/labs/virus)