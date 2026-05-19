# Agent Harness Engineering：为什么模型不是决定性因素

> **核心论点**：真正决定 Agent 成败的，不是模型有多强，而是围绕它的「harness」（挽具/支架）设计得有多精妙。当模型能力边界逐渐模糊，harness 的质量就成了区分工业级 Agent 和玩具原型的分水岭。

---

## 01 为什么我们谈错了重点

过去三年，Agent 社区的讨论几乎被一个问题主导：**什么模型最好？**

这个问题本身就错了。

OpenAI 的一个团队做过一次极限实验：五个月内，用 Codex 驱动一个完全由 Agent 构建的产品——零行人工代码。应用逻辑、测试、CI 配置、文档、可观测性，全部由 Codex 生成。最终产出了约百万行代码，1500 个 PR 合并，平均每人每天 3.5 个 PR。

关键不是模型多强。关键是他们花了五个月时间设计**让模型能可靠工作的环境**。

这就是 Harness Engineering 想要回答的问题：当模型不是瓶颈时，什么才是？

---

## 02 Harness 的定义：一个被低估的学科

Harness Engineering 是**围绕 Agent 设计的 scaffold（脚手架）**——它决定了 Agent 是成功还是失败。

具体包括：

- **Context Delivery**：上下文如何传递，消息如何组织
- **Tool Interface**：工具边界如何设计，参数如何定义
- **Planning Artifact**：执行计划如何表达和维护
- **Verification Loop**：结果如何验证，质量如何把关
- **Memory System**：历史状态如何保持，长程任务如何不遗忘
- **Sandbox**：危险操作如何隔离，副作用如何控制

OpenAI 在其Responses API 的设计文档中说得直白：

> "The model only proposes a tool call. It can't execute the call on its own."

模型只负责「想」，执行靠 harness。这不是实现细节，这是架构原则。

---

## 03 第一个工程教训：环境比模型更重要

OpenAI 的实验揭示了一个反直觉的事实：**早期进展慢，不是因为 Codex 不够强，而是环境描述不足**。

当工程师给 Codex 的初始 prompt 是「构建一个有搜索、推荐、支付功能的应用」，Agent 的进展远低于预期。不是模型理解不了这个任务，而是它没有足够的**建筑材料**来分解这个任务。

人类的解决方案是：退后一步，问自己——「什么能力缺失了？」然后系统性地构建那个能力。

OpenAI 工程师 Brian 总结过一句话，后来被反复引用：

> "Fixes were almost never 'try harder.' Because the only way to make progress was to get Codex to do the work, human engineers always stepped into the task and asked: 'what capability is missing, and how do we make it both legible and enforceable for the agent?'"

这揭示了 harness 设计的核心心法：**不要试图让模型克服环境的不足，要让环境适配模型的工作方式**。

---

## 04 第二个工程教训：代码不好看，但必须可读

OpenAI 团队遇到了一个有趣的问题：当 codebase 完全由 Agent 生成时，代码风格出现了「对人类不友好」的趋势。函数过长、命名随意、抽象层级混乱。

他们的解法不是让 Agent 写出「更好看」的代码，而是**让代码对 Agent 更好读**。

具体来说：

1. **强制结构边界**：每个业务域被划分为固定层级（Types → Config → Repo → Service → Runtime → UI），层级间依赖方向被机械验证。
2. **自定义 linter 注入修复指令**：当 lint 报错时，错误信息本身就是对 Agent 的修复指令——不是「这段代码有风格问题」，而是「这个函数的圈复杂度超过了 15，请重构」。
3. **可读性优先于最优解**：宁可让 Agent 用「无聊」的技术（因为 GPT-5 的训练数据更丰富，模型对「无聊」技术的理解更准确），也不要用新奇的库增加 Agent 的认知负担。

这是 Agent 时代工程思维的范式转变：**代码不是写给人看的，是写给 Agent 和人共同维护的**。而 Agent 的可读性 ≠ 人类的可读性，有时甚至相反。

---

## 05 第三个工程教训：文档是系统，不是装饰

传统的工程团队把文档当作「完成开发后的整理工作」。在 Agent 时代，这个逻辑完全失效了。

OpenAI 团队最初试过用一个巨大的 AGENTS.md 文件（类似本仓库的 SOUL.md）来指导 Agent。效果很快崩溃，原因很直接：

1. **上下文是稀缺资源**：巨大的指导文件挤占了任务本身、代码和相关文档的空间
2. **重要的事情变得不重要**：当所有规则都标记为「重要」，Agent 开始本地模式匹配而不是全局导航
3. **文档腐烂**：单一的巨型手册无法跟进代码变化，Agent 会根据过时信息做决策

他们的解法是把文档当作**系统**来设计：

```
AGENTS.md           ← 目录，不是百科全书
ARCHITECTURE.md     ← 顶层领域映射
docs/
  ├── design-docs/  ← 设计决策，含验证状态
  ├── exec-plans/   ← 执行计划（短生命周期）
  ├── product-specs/← 产品规格
  └── references/   ← 供 Agent 查询的参考信息
PLANS.md            ← 主动计划
QUALITY_SCORE.md    ← 质量追踪
```

核心设计原则：**渐进式披露**（Progressive Disclosure）——Agent 从小而稳定的入口开始，被告知「在哪里找更多信息」，而不是被淹没在所有信息中。

---

## 06 第四个工程教训：验证不是 QA，是架构

在传统软件开发中，验证（Verification）是发布前的检查点。在 Agent 时代，验证是让 Agent 能可靠工作的基础设施。

OpenAI 团队构建了一个自动验证循环：

- Agent 完成 PR → 自动运行 test suite → 结果注入回 Agent 上下文 → Agent 根据失败信息修复 → 循环直到通过

这个机制的关键不是「有测试」，而是**测试结果如何转化为 Agent 的可操作反馈**。

他们设计的测试框架输出格式是：

```
FAILED: test_payment_refund_edge_case
CONTEXT: Stripe API 返回 500 错误时，refund 函数未正确处理异常
SUGGESTION: 添加 try-catch 并在 except 分支中记录完整调用栈，供调试使用
```

不是测试报告，是**修复指令**。Agent 拿到这份输出，不需要人类介入就能继续工作。

---

## 07 第五个工程教训：长程任务需要显式记忆

当一个 Agent 需要运行数小时处理复杂任务时，context window 必然会被填满。传统的做法是手动总结历史上下文，但这个工作交给人类做就失去了自动化的意义。

OpenAI 在 Responses API 中引入了 **native compaction** 机制——模型自行分析对话历史，生成一个加密的、token 高效的「压缩项」，保留关键状态，清除冗余信息。

关键设计决策是：** compaction 不是人类的工具，是 Agent 的工具**。模型自己判断什么该保留，什么该压缩，不需要人类介入。

这带来了一个架构层面的变化：Agent 的记忆不再是「把所有东西都放在 context 里等人类提取」，而是「 Agent 自己维护一个它认为重要的状态子集」。

---

## 08 为什么 Harness Engineering 是 2026 年的核心技能

当模型能力逐渐趋同（GPT-5、Claude 4、Gemini 2 的能力边界差距越来越小），**harness 的质量开始成为决定性差异因素**。

这类似于云计算时代：基础设施的成熟让「用谁的虚拟机」不再是竞争力，竞争力变成了「如何设计你的基础设施」。AI Agent 正在进入类似的阶段：

| 阶段 | 核心竞争力 | 代表性问题 |
|------|----------|-----------|
| 模型驱动 | 模型能力 | 「GPT-5 还是 Claude 4 更好？」 |
| 应用驱动 | Prompt 工程 | 「如何写出更好的 instruction？」 |
| **Harness 驱动** | **架构与工程** | **「如何设计让 Agent 可靠工作的环境？」** |

Harness Engineering 涵盖了：上下文传递、工具设计、验证循环、记忆系统、沙箱隔离、可观测性、编排策略。这些都是工程问题，不是模型问题。

---

## 09 一个实践原则：先把环境做简单，再让模型做复杂

Anthropic 在「Building Effective Agents」中总结过一条原则：

> "You should consider adding complexity only when it demonstrably improves outcomes."

OpenAI 的实验验证了这句话的深层含义：当他们试图在 harness 中添加复杂的多Agent 协作逻辑时，系统可靠性下降。当他们回归「简单的 harness + 简单的 Agent 交互」时，吞吐量反而上升。

这不是说多 Agent 协作没有价值，而是说**复杂协作只有在简单的底层 harness 之上才能稳定运行**。就像微服务架构的前提是有可靠的进程间通信机制，而不是有了一堆微服务自然就可靠了。

---

## 结语：Harness 是 Agent 的操作系统

如果要用一个类比来理解 Harness Engineering：

> **模型是 CPU，Harness 是操作系统。CPU 决定计算能力上限，OS 决定这个能力能否被可靠地用起来。**

没有操作系统，CPU 只是一块硅片。没有精心设计的 harness，模型只是一个能说会道的统计模型。

2026 年，能区分 Agent 工程能力强弱的关键，不在于选择了哪个模型，而在于——

**你的 harness 是否足够精确，让模型能稳定地做好它应该做的事？**

---

## 引用来源

1. [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI Engineering Blog, February 11, 2026
2. [From model to agent: Equipping the Responses API with a computer environment](https://openai.com/index/equip-responses-api-computer-environment/) — OpenAI Engineering Blog, March 11, 2026
3. [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic Engineering, 2025

---

*归档目录：`fundamentals/` — 代表性文章：Harness Engineering 方法论*