# Anthropic 实证研究：AI Agent 自主性的真实图谱

> 原文：[Measuring AI agent autonomy in practice](https://anthropic.com/research/measuring-agent-autonomy) — Anthropic Research, 2026-02-18

## 核心论点

模型的能力与它实际展现的自主性之间存在一道鸿沟。

Anthropic 在这篇 2026 年 2 月发布的实证研究中，利用 Clio（隐私保护基础设施）分析了 millions 级别的真实人机交互数据，得出一个反直觉的结论：**现有模型实际展现的自主性，远低于它们本可以做到的**。这个发现对整个 Agent 领域都有深远的工程意义。

---

## 一、研究方法：如何测量「自主性」

研究 Agent 的自主性面临三个根本挑战：

1. **没有统一口径的定义** — 什么算 Agent？单人对话线程？多 Agent 系统？
2. **系统快速演进** — 去年最复杂的 Agent 还是单对话线程，今天已有运行数小时的自治系统
3. **模型提供商视角有限** — 无法可靠地将 API 请求关联为「会话」级别的 Agent 活动

Anthropic 的解法是**以工具调用为分析单元**：只要 AI 系统配备了工具（执行代码、调用外部 API、发送消息），它就是一个 Agent。这个定义虽然宽泛，但具有可操作性。

数据来源分两类：

| 数据源 | 优势 | 局限 |
|--------|------|------|
| **公共 API** | 覆盖数千个不同客户的 Agent 部署 | 只能分析单个动作，无法重建完整行为序列 |
| **Claude Code** | 可以关联跨会话的完整工作流 | 单一产品，缺乏多样性 |

> "We analyze actions in isolation, and cannot reconstruct how individual actions compose into longer sequences of behavior over time."

---

## 二、核心发现一：Claude Code 正在变得更 autonomous

**数据**：Claude Code 单次运行时长在三个月内几乎翻倍——从不足 25 分钟增长到超过 45 分钟。

**关键洞察**：这个增长是**平滑的**，跨模型版本一致。这意味着增长并非单纯来自模型能力提升，而是来自用户行为变化——用户越来越信任 Claude，愿意让它 running autonomously 更久。

**工程意义**：这不是一个功能开关，而是信任的渐变。Harness 设计中一个常被忽视的维度是：**用户的信任曲线会随时间改变**，但大多数 Harness 设计是静态的。

---

## 三、核心发现二：经验用户的监督模式是「Inverse」的

直觉上，我们以为「更有经验的用户会更细致地监督 Agent」。数据告诉我们相反：

- **新用户**：约 20% 的会话使用完全自动批准（Full Auto-Approve）
- **经验用户**：超过 40% 的会话使用完全自动批准

但这不意味着经验用户「不管了」。相反，经验用户在 Agent 遇到复杂问题时**介入更频繁**，而不是每个动作都检查。他们学会了区分「哪些情况需要我」和「哪些情况让它自己来」。

> "Agents are used in risky domains, but not yet at scale."

**工程意义**：理想的 Harness 不是「批准一切」或「批准 nothing」，而是一个**动态的信任梯度**——基于任务类型、风险等级和上下文自适应调整。AUTO-APPROVE 应该是一个 spectrum，不是一个 binary 开关。

---

## 四、核心发现三：Agent 自己暂停的频率 > 人类中断的频率

在最复杂任务上，Claude Code **停下来请求澄清的频率**是人类主动中断频率的两倍以上。

这是 Agent 设计中常被忽视的 oversight 形式：**Agent-Initiated Stops**。不是人类踩刹车，而是 Agent 自己说「我需要确认」。

**工程意义**：当你设计的 Harness 只关注「人类如何干预 Agent」，你可能忽略了更大的一类 oversight 机制——**Agent 自身的不确定性检测和请求暂停能力**。一个好的 Harness 应该让 Agent 更容易说「我不确定」。

---

## 五、核心发现四：Agent 的应用域分布

| 领域 | 占比 | 风险等级 |
|------|------|---------|
| 软件工程（Claude Code）| **~50%** | 中低，可逆 |
| 医疗 | 新兴 | 高 |
| 金融 | 新兴 | 高 |
| 网络安全 | 新兴 | 高 |

**关键判断**：当前大多数 Agent 行为是**低风险且可逆的**。高风险领域（医疗、金融、网络安全）已有部署，但尚未形成规模。

> "Agents are used in risky domains, but not yet at scale."

---

## 六、核心判断：Harness 需要「Post-Deployment Monitoring Infrastructure」

这篇研究最重要的结论不是某个具体数据点，而是它揭示的**系统性问题**：

**现有模型的能力 > 它们实际被允许展现的自主性**

这意味着：

1. **模型的自主性上限远未触及** — 能力不是瓶颈，Harness 和人机交互范式才是
2. **监督机制必须进化** — 静态的「每次批准」或「全自批准」都不够；需要**自适应的信任梯度**
3. **Post-Deployment Monitoring 是基础设施** — 不是可选项，而是安全部署的前提条件

> "Effective oversight of agents will require new forms of post-deployment monitoring infrastructure and new human-AI interaction paradigms that help both the human and the AI manage autonomy and risk together."

---

## 七、行动启示

对于构建 Agent Harness 的团队：

**第一，测量你的用户信任曲线**。Claude Code 的数据表明，用户信任是随时间增长而非静态的。你的 Harness 有没有埋点记录「用户多久开始接受 AUTO-APPROVE」？

**第二，把 Agent-Initiated Stops 纳入设计**。不只是「人类何时干预」，还要问「Agent 何时会说我不确定」。一个好的不确定检测机制比 1000 行批准规则更有价值。

**第三，建立 Post-Deployment Monitoring 作为核心组件**。不是发版后才想起「要不要加个监控」，而是 Harness 的设计阶段就要回答「我如何知道这个 Agent 在做什么」。

---

## 引用

> "How much autonomy do people grant agents? How does that change as people gain experience? Which domains are agents operating in? And are the actions taken by agents risky?"

> "Our central conclusion is that effective oversight of agents will require new forms of post-deployment monitoring infrastructure and new human-AI interaction paradigms that help both the human and the AI manage autonomy and risk together."

---

*来源：Anthropic Research — 2026-02-18，基于 Claude Code 百万级会话和公共 API 工具调用级别的实证数据。*