# 从 2 Billion 执行中发现的 Agent 生产真相：为什么智能不是瓶颈

> 本文源自 CrewAI 工程团队基于 2B+ agentic workflow executions 的一手经验总结，2026年6月发布。

---

## 核心命题

**做 AI Agent 的团队，大多不缺智能，缺的是把智能可靠跑起来的工程体系。**

GPT-4o-mini 依然在跑着 CrewAI 自家的很多生产负载。最新的大模型很强，但不是解锁生产部署的关键。真正的解锁点是 Agent Operations——一套能把「notebook 里能跑」变成「生产环境可靠跑」的基础设施。

这是 2 billion executions 教给整个行业的一课。

---

## 2 Billion 的规模意味着什么

CrewAI 过去 12 个月处理了约 **20 亿次 agentic system 执行**。覆盖的企业包括 PepsiCo、Johnson & Johnson、PwC、美国国防部、DocuSign、AB InBev、BDO、NTT Data、Experian。

一些具体的数字：

- 某客户目标：未来 5 年通过 CrewAI 节省 **10 亿美元**，同时创造 10 亿美元营收
- 另一家：几个月内实现 **30% 的工单完全自治**
- 还有一个：评估了市面所有方案后选了 CrewAI，上线时间几周，代码量比之前另一个框架少 **14 倍**

这些不是概念验证，是已经跑在生产里的数字。

---

## 为什么很多 Agent 从未上线

行业数据确认了大多数团队进场前就已知的事实：**质量（即信任）是生产部署的头号障碍**。这种信任缺失来自幻觉，也来自输出的一致性问题。

但更根本的问题是：

> 很多团队聊起 agentic 系统有多复杂，早期的抽象选择堆得有多快、能怎么帮倒忙。大量工程师后悔选了图架构——看起来很漂亮，生产环境里却成了调试噩梦。
>
> Graph、sub-graph、state object，一层叠一层，真正的 agent 逻辑藏在多层间接访问后面。出了问题，工程师要在多层跳转里挖才能找到是哪个 prompt 或哪个 tool 导致。更别说版本更新带来的 breaking changes，现在花在维护框架上的时间比构建系统的时间还多。

需求侧的结构性问题在于：**原型的需求仍然是生产需求的 10 倍**。结果是市面大多数产品专注在「构建」那部分，而帮助企业真正解决「把 agentic 系统跑起来、跑可靠、产生真实业务价值」这部分严重不足。

这不是智能的问题。大多数模型够用了。GPT-4o-mini 跑着 CrewAI 自家的很多生产负载至今。真正的问题在 Agent Operations 侧。

---

## 从万亿次执行中浮现的三个核心模式

### 模式一：信任是在生产中挣来的

拿到最大结果的团队不是从全自主 agent 开始的，而是从 **100% 人工审核**开始，然后逐步降低比例。

一个 HR 服务公司案例：3000+ 员工工单/月，合规团队人手不够。他们用 CrewAI 构建了 agent 系统处理工单，但没有一步到位——每个输出都经过人工审核后再到达员工。

Agent（代号 Andy）负责起草回复、关联政策、标记边缘案例。每个工单都过人工。

然后有趣的事发生了：几千次执行后，合规团队注意到了质量，SVP 问：「我们能不能用这些输出训练我们的人类 agent？」

这时候团队知道可以开始降低监督比例了。现在 Andy 处理 **50%+ 的触达无需人工审核**，因为 agent 通过几千次一致的、可审计的决策挣得了信任。

改进速度比他们预期的快，用了几周而不是几个月。

> **关键洞察**：信任梯度（Trust Gradient）——看似简单的 human-in-the-loop，当部署正确时，可以成为系统的信任累积机制。系统证明自己 → 人工审核比例下调 → 更多自主权 → 更快迭代。

---

### 模式二：架构选择会快速复合

DocuSign 是最早采用 CrewAI Flows 的客户之一，看他们如何架构系统让我们学到了很多。

用例是销售线索加速：获取线索 → 研究 → 撰写个性化外联 → 验证质量 → 发送。他们称之为「3 Ps」：Productivity、Personalization、Pipeline。

在构建前他们评估了市场。LangChain、AutoGen、还有其他。选了 CrewAI，最终落地的模式说明了原因：

他们的初始用例包含 **5 个 agent**：Identifier、Researcher、Composer、Validator、Orchestrator。但这些 agent 不是随意跑，它们嵌入在一个**确定性 Flow** 里——Flow 控制顺序、处理错误、管理状态，然后持续调整多少交给模型、多少交给 agent 的判断力。

验证层就有**三层**：
1. LLM-as-judge 做质量判断
2. 对源材料做幻觉检查
3. API-based 质量评分

任何一步失败，他们能精确定位到哪层捕获了问题、怎么修。

结果：非常显著的周转时间缩短，更高的邮件打开率、回复率、转化率。而且代码库是团队真正能维护的——另一个客户的类似迁移评估显示，代码量比之前的图架构实现**少 14 倍**。

> **关键洞察**：这不是 merely agents that can reason，而是 production architectures——确定性部分和概率性部分被刻意分离的架构。

---

### 模式三：速度来自全栈，不只是 harness

几乎每个成功部署都有的模式不是「快速试错、快速失败」，恰恰相反——他们花时间评估真正重要的决策。

AB InBev 每年通过 AI 处理 **300 亿美元决策**。当他们的领导说「我希望公司在 agentic 方向领先」，这是一个战略指令。他们现在有几十个用例跑在 CrewAI AMP 上，对底线的影响是百万美元级别的。

让这种速度成为可能的不仅是更好的模型或更聪明的 agent。是**从第一天就有全栈**：
- 基础设施层（K8s）
- 可观测性（能追溯每个决策回溯到导致它的输入）
- 内嵌在架构里的 human-in-the-loop（不是后期加的）
- 通过安全审查的部署选项
- 正确的 PII 保护

这个组合被证明是真正的 super power。

---

## 如果你在构建 Agent 系统，这对你意味着什么

2 billion executions 教我们的是：「working demo」到「production system」的 gap 是大多数团队卡住的地方，而且主要是因为关注点放错了地方。

把 agentic 系统真正跑出来的公司明白：** intelligence 是 table stakes（智能是入场券），真正的解锁点是智能周围的一切——通过透明化挣来的信任，和把可预测的与不可预测的分开的架构。**

具体来说：

**1. 从 100% 人工审核开始，不要从全自主开始。**
信任是通过执行历史挣来的，不是设计出来的。设计好你的 trust gradient 机制，让系统证明自己。

**2. 把确定性逻辑和 agentic 逻辑分开。**
Flow 负责结构，Agent 负责需要判断的部分。不要让图架构把两者混在一起变成调试噩梦。

**3. 构建全栈，从第一天。**
Human-in-the-loop、traceability、可观测性、PII 保护、deployment flexibility——这些不是「以后再加」的东西。它们的组合才是让 agent 系统真正可用的原因。

**4. 模型不是瓶颈，Agent Operations 才是。**
GPT-4o-mini 跑生产负载没问题。最新模型很强，但不是解锁点。花时间在你周围的工程体系上，比追逐 SOTA 模型更有杠杆。

---

## 原文引用

> "The problem isn't intelligence though, most models out there are good enough. GPT-4o-mini runs many of our own production workloads up to this day still. Yes, the latest models are incredible and super powerful for certain use cases, but aren't the unlock. The problem is the Agent Operations side, getting from 'this works in a notebook' to 'this runs reliably at scale with audit trails, human oversight, and outcomes and we can trust it'."
>
> — CrewAI 工程团队，*Lessons From 2 Billion Agentic Workflows*，2026年6月

---

## 关联阅读

- [CrewAI OSS 1.0 GA — Deterministic Runs 解决 Agent 生产级部署的可复现性危机](./crewai-oss-1-0-ga-deterministic-runs-2026.md)
- [Letta — 23K Stars 的 Stateful Agents 平台](./letta-ai-letta-stateful-agents-23140-stars-2026.md)

---

*来源：[Lessons From 2 Billion Agentic Workflows](https://blog.crewai.com/lessons-from-2-billion-agentic-workflows)，CrewAI Blog，2026年6月4日*