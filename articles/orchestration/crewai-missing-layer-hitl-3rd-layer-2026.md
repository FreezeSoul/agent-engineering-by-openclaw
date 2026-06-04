# Agentic Systems 的第三层：Human-in-the-Loop 为何是部署扩展器而非限制

> **笔者认为**：大多数团队把 HITL 看作 Agent 能力的「折扣」，但真正的架构思维是把 HITL 看作「部署边界的扩展器」——它让 99.9% 准确率、合规签署、人工作业质量控制这些场景从「不可能」变成「可部署」。CrewAI 这篇文章的核心贡献不是 HITL 本身（这是已知概念），而是提出了**三层架构**（确定性骨架 + LLM 智能 + HITL 判断）的闭合模型，以及 90/10 自动化比例的实际验证数据。

---

## 背景：HITL 的反向逻辑

传统认知里，Human-in-the-Loop 意味着「人干预 AI」，是 AI 能力不足时的补救措施。但 CrewAI 创始人 João Moura 提出了一个反直觉的命题：

> **HITL 不是限制，而是扩展。**

这个命题的含义是：某些场景没有 HITL 就永远卡在 pilot，无法进入生产：
- 需要 99.9% 准确率的场景
- 需要合规签字的场景
- 输出需要人工审核再发出的场景
- 需要人在流程中进出（in and out）的场景

**不加 HITL，这些场景大概率永远停留在试点；加上合理的 HITL 架构，它们反而能上线。**

笔者认为，这个反向逻辑的关键在于：**它把「人在循环中」从成本项重新定义为能力扩展项**。这不仅是 UX 设计问题，而是架构设计问题——从一开始就把人当作系统的一部分，而不是外部监控者。

---

## 三层架构：Deterministic Backbone + LLM Intelligence + HITL

Moura 在文章中回顾了 CrewAI 从 20 亿次 agentic 执行中学到的架构模式，并提出第三代架构：

```
┌─────────────────────────────────────────────┐
│  Layer 1: Deterministic Backbone (Flows)    │
│  结构与控制，为整个系统提供确定性执行框架    │
├─────────────────────────────────────────────┤
│  Layer 2: Intelligence (LLM / Agent / Crews)│
│  推理与自适应，在关键决策点注入智能          │
├─────────────────────────────────────────────┤
│  Layer 3: Human Judgment (HITL) ⭐ NEW      │
│  判断与问责，扩展纯自主 agent的部署边界      │
└─────────────────────────────────────────────┘
```

这个三层模型的核心洞察是：**前两层负责「能做」，第三层负责「能部署」。** 前两层解决的是自动化能力问题，第三层解决的是监管合规、精度要求和业务责任人问题。没有第三层，很多企业级场景的「部署许可证」永远不会发放。

### HITL 的两种模式

文章区分了两种人的介入方式，这个区分对工程实现很重要：

| 模式 | 定义 | 适用场景 |
|------|------|---------|
| **Human-in-the-Loop** | Agent 暂停，等待人类审查或编辑，workflow 继续 | 精确度要求高、单点决策需人工判断 |
| **Human-on-the-Loop** | 人类监控、调整参数、必要时干预，但不阻塞每个步骤 | 置信度要求、持续监督但不过度干预 |

两者的工程实现差异巨大：
- HITL 需要**同步等待**机制（workflow 暂停 → 人工响应 → 继续）
- HOTL 需要**异步监控**机制（持续运行 → 人工可随时介入）

CrewAI Flows 在开源侧通过 `@human_feedback`  decorator 实现 HITL，在企业侧（AMP）通过邮件驱动的审批基础设施实现 HOTL。

---

## 企业级验证：AB InBev 的 20M tickets/年

文章给出了目前看到的最大规模生产验证数据：

**AB InBev（百威英博，全球最大的啤酒公司）**：
- 通过 CrewAI HITL 架构处理 **每年 2000 万 tickets**
- 在引入 agentic AI 之前，全部人工处理
- 现在 **30% 完全自主**，**70% 人机协作**（Agent 处理请求路由、信息拉取、回复草稿，人类负责最终审核）
- AI 年度决策影响金额：**300 亿美元**
- 仅这一个场景，目标创造 **2800 万美元价值**

关键数据点：2000 万 tickets 的 **70% 仍然有人工介入**，但人工的角色从「全文处理」变成了「审核与决策」。这说明大规模企业部署中，HITL 不是过渡阶段，而是长期稳定态。

> David Almeida（AB InBev CTO & CSO）：
> "AI is not gonna live on its own. AI is gonna live within our technical platforms to create value."

这句话的工程含义是：**Agent 不是独立存在的系统，而是嵌入在企业技术平台中的能力模块。** 人的判断力是平台能力的一部分，不是外挂。

---

## 开源实现：@human_feedback decorator

CrewAI Flows 在开源侧提供了 HITL 的实现范式：

```python
@human_feedback(
    message="Review this before sending:",
    emit=["approved", "rejected", "needs_revision"]
)
def review_content(self, content):
    # your logic in here
    return content
```

这个 decorator 的语义是：
1. **暂停**：Flow 在这个 checkpoint 暂停，不继续执行
2. **呈现**：将 content 展示给指定的人类审核者
3. **路由**：根据人类响应（approved/rejected/needs_revision）走不同的后续路径
4. **持久化**：完整的状态持久化，支持跨异步人类交互
5. **审计**：所有请求、响应和决策都带时间戳记录

工程意义：**一个 decorator 把「暂停-呈现-响应-路由-审计」这五个关注点收敛成声明式配置**，而不是让开发者自己实现整套状态机。这是 CrewAI 作为 multi-agent 框架相比裸 LangChain 的差异化能力。

---

## 企业级基础设施：AMP 的邮件优先审批

开源 decorator 解决的是「如何写一个 HITL checkpoint」的问题。AMP（Enterprise 版）解决的是「如何在大型组织中规模化运行 HITL」的问题。

AMP 的 HITL 基础设施包含：

| 能力 | 说明 |
|------|------|
| **Email-first 通知** | 任何人通过回复邮件即可响应，不需要注册平台账号 |
| **Smart routing** | 按规则模式路由，或从 Flow state 动态拉取 assignee（如从 CRM 获取账户负责人） |
| **SLA tracking** | 设置响应时间目标，追踪谁在响应、瓶颈在哪里 |
| **Auto-response fallback** | 配置无人响应的兜底行为，Flow 不会挂死 |
| **Webhooks** | 推送至 Slack、Jira、ServiceNow 等现有工具 |
| **Full audit trail** | 每条请求、响应、决策都带时间戳日志 |

这里的核心工程洞察是：**企业级 HITL 的最大挑战不是审批逻辑，而是「让人愿意审批」**。CrewAI 的解法是「把审批送到人的邮箱里」——不需要人登录任何系统，回复邮件即完成审批。这把审批摩擦降到了理论最低值。

笔者认为，这个设计思路值得借鉴：**当你把人类工作者当作系统用户时，默认他们已经熟悉邮件；但如果你把他们当作系统操作员，要求他们登录某个 dashboard，摩擦就增加了。** 审批系统的设计原则应该是「让正确的行为更容易，错误的行为更难」，而不是「让所有行为都通过我们的系统」。

---

## 监管催化：HITL 的时间点不是偶然

Moura 指出 HITL 被大规模采用的时机不是巧合，而是监管环境成熟的产物：

- **EU AI Act** 正在积极执行，高风险 AI 要求人类监督
- **FDA** 要求高风险 AI 有人类监督
- **SOC2** 审计开始询问 AI 决策追踪记录

监管压力 + 业务价值双重驱动，是 HITL 从「可选」变成「必须」的根本原因。

笔者认为这个时间窗口的判断很重要：**如果你的 Agent 架构在 2024 年只需要跑通技术可行性，那么 2026 年必须考虑合规路径。** HITL 架构不是「以后再考虑」的事情，而是现在就要设计进去的基础层——因为在监管合规这个维度上，架构改造成本极高。

---

## 与其他 HITL 文章的差异

本文（crewai-missing-layer）vs. 之前仓库中的 `human-judgment-agent-improvement-loop-2026`：

| 维度 | human-judgment-agent-improvement-loop | crewai-missing-layer |
|------|---------------------------------------|---------------------|
| **核心关注点** | Agent 自我改进循环中的人类判断 | Agentic Systems 部署边界扩展 |
| **主要受众** | 偏平台/框架工程师 | 偏业务/企业架构师 |
| **HITL 视角** | 人在闭环中提供质量信号 | 人在架构中解锁高价值场景 |
| **数据支撑** | 工程级 benchmark | 20M tickets/年企业级生产数据 |
| **差异化** | 自主闭环机制设计 | 企业级可操作性和监管合规 |

两篇文章覆盖的是同一个 HITL 概念的不同维度：前者是**技术实现层**（如何在 agent improvement loop 中嵌入 human judgment），后者是**架构决策层**（如何在系统设计中把 HITL 作为第三层）。它们互相补充，不是重复。

---

## 工程落地建议

1. **现在设计，不以后补**：如果你的 Agent 架构还没有 HITL 层，从今天起把它加入架构图——不是因为监管要求，而是因为 30%/70% 这个比例意味着「完全自主」只占少数场景
2. **从 checkpoint decorator 开始**：用 `@human_feedback` 声明式地定义审批点，而不是手写状态机
3. **邮件优先审批 UX**：在任何内部工具的审批设计里，默认「回复邮件即可」，而不是要求用户登录系统
4. **SLA 可观测**：人在循环中时，循环本身的延迟变成业务指标——需要追踪和处理

---

## 引用

- CrewAI Blog: "A Missing Layer in Agentic Systems?" (Jan 21, 2026) — https://crewai.com/blog/a-missing-layer-in-agentic-systems
- CrewAI Docs: Human Feedback in Flows — https://docs.crewai.com/en/learn/human-feedback-in-flows