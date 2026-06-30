# 测量 Agent 自主性：Anthropic 揭示「部署滞后」现象与 Harness 设计的真实约束

**源**: [Anthropic Research - Measuring AI agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy)

**核心论点**：Anthropic 用 235,000 人、400,000 个会话的真实数据回答了一个长期悬而未决的问题——Agent 在生产环境中的自主性到底由什么决定？答案是：**模型能力、用户信任、产品设计三者共同构造**，且三者中任意一个的滞后都会形成「部署滞后（deployment overhang）」。这意味着 Harness 设计的核心不是「让 Agent 更自主」，而是「让三者的协同效率更高」。

---

## 问题：能力评估为何不足以描述真实部署

传统上我们用「能力评估（capability evaluation）」来衡量 Agent——给它一组测试任务，看能完成多少。但 Anthropic 这篇研究指出：

> "Neither capability evaluations nor our measurements alone give a complete picture of agent autonomy, but together they suggest that the latitude granted to models in practice lags behind what they can handle."

能力评估只回答「Agent 能做什么」，但生产环境关心的是「Agent 在被实际使用时的自主性边界」。这两个数字之间的差距，就是「deployment overhang」——模型能处理的复杂度，超出了用户在产品里实际授权给它的范围。

这意味着：**把模型变强不一定能提升部署自主性**。如果产品默认要求逐条审批、用户没有建立信任，再强的模型也只能在 L4 自动驾驶的车上以 L2 的速度跑。

---

## 数据规模与方法

| 维度 | 数值 |
|------|------|
| 时间窗口 | 2025 年 10 月 – 2026 年 4 月 |
| 会话数 | ~400,000 个交互会话 |
| 用户数 | ~235,000 人 |
| 隐私保护 | 仅分析聚合的聚类，不读取个体内容 |
| 排除规则 | 自动剔除未达最小聚合阈值的小众用例 |

这个规模本身就是信号——Anthropic 第一次有数据基础去研究「真实部署」而不是「能力评估」。这件事的工程意义在于：**Agent 工程的下一阶段不是继续刷 capability benchmark，而是去量化 deployment**。

---

## 关键发现一：Turn Duration 的尾部才是真相

> "The more revealing signal is in the tail. The longest turns tell us the most about the most ambitious uses of Claude Code, and point to where autonomy is heading."

平均 Turn Duration 是一个糟糕的指标——绝大多数交互很短，长尾才反映「最复杂的真实使用」。Anthropic 发现：

- **2025 年 10 月**：99.9 分位的 Turn Duration < 25 分钟
- **2026 年 1 月**：99.9 分位的 Turn Duration > 45 分钟
- **变化幅度**：不到一个季度，几乎翻倍

这意味着：用户在慢慢学会「把更复杂的任务一次性交给 Agent」，而 Harness 必须支持这种趋势——checkpoint、状态恢复、长任务可见性，这些都是为了支撑这个 45+ 分钟的 Turn 而存在的工程机制。

**笔者认为**：如果你的 Agent Harness 不能支持 45 分钟的单 Turn，要么你的用户群还没到这个复杂度，要么你的 Harness 已经把人推回到短任务了。这是一个 Harness 设计是否「够现代」的硬指标。

---

## 关键发现二：Auto-Approve 率随经验增长

> "Newer users (<50 sessions) employ full auto-approve roughly 20% of the time; by 750 sessions, this increases to over 40% of sessions."

具体含义：

| 用户经验 | Auto-Approve 占比 |
|---------|-----------------|
| 新用户（<50 sessions）| ~20% |
| 老用户（~750 sessions）| ~40% |
| 增长曲线 | 渐进的，无明显跃迁 |

**值得注意**：Claude Code 的默认设置是「手动审批每一个操作」，所以这个增长完全是用户主动配置的结果——他们配置 auto-approve 不是因为产品默认开了，是因为他们建立了信任，主动放权。

**Harness 启示**：

1. **信任是渐进资产**——产品设计不能用「一次性配置」的假设，要支持逐步放权的曲线
2. **Auto Mode 的真正用户是熟练用户**——把 Classifier 设计给 40% auto-approve 的人群看，而不是给 20% 的人群看
3. **Trust Ledger 的隐性积累**——产品需要让用户能「感知到自己的经验在积累」，否则信任建立是无意识的

---

## 关键发现三：Interrupt 率与 Clarification 率的对比

Interrupt 率（人类打断 Agent 的频率）随经验变化：

| 用户经验 | Interrupt 占比 |
|---------|--------------|
| 新用户（~10 sessions）| 5% per turn |
| 老用户 | 9% per turn |

但 Claude 自身的 Clarification 率（主动问澄清问题的频率）随任务复杂度上升，且**比人类 Interrupt 更频繁**。

**核心洞察**：人类的监督策略从「事后纠正」转向「事前介入」——新用户倾向于看到结果不对再打断，老用户倾向于在 Claude 进入危险区前就拦下。这意味着：

> **Claude 不是被动执行者，它是自主性系统的主动参与者**——它通过「停下来问问题」主动减少自己承担的责任。

Anthropic 把这种现象总结为：

> "The autonomy agents exercise in practice is co-constructed by the model, the user, and the product."

这个三方共建模型是文章最重要的概念贡献。

---

## 关键发现四：软件工程仍占 50%，其他领域是前沿

> "Today, agents are concentrated in a single industry: software engineering accounts for nearly 50% of tool calls on our public API (Figure 6)."

分布：

- **软件工程**：~50% of tool calls
- **商业智能**：几个百分点
- **客户服务、销售、金融、电商**：各几个百分点
- **其他**：剩余

**风险与自主性联合分布**（Figure 5）：每个聚类按平均风险和平均自主性绘制。

> "We also anticipate that agents operating at the extremes of risk and autonomy will become increasingly common."

**Anthropic 的预测**：随着 Agent 进入软件工程以外的领域（金融、医疗、运营），「高风险 + 高自主性」的边界会扩张。这意味着 Harness 必须从「代码相关风险」扩展到「跨领域风险」——这是一次工程范式的扩张，不只是功能扩展。

---

## 核心洞察：Autonomy 是三方共建，不是模型单方面决定

文章最后给出总结：

> "A central lesson from this research is that the autonomy agents exercise in practice is co-constructed by the model, the user, and the product. Claude limits its own independence by pausing to ask questions when it's uncertain. Users develop trust as they work with the model, and shift their oversight strategy accordingly. What we observe in any deployment emerges from all three of these forces, which is why it cannot be fully characterized by pre-deployment evaluations alone."

把三方共建拆开看：

| 参与者 | 对自主性的贡献 | 工程机制 |
|--------|--------------|---------|
| **Model** | 通过「主动问澄清」自我限制 | Training on clarification triggers |
| **User** | 通过 auto-approve 比例动态放权 | Trust gradient + Override history |
| **Product** | 通过审批/沙箱/Classifier 设计约束 | Permission policy + Classifier + Checkpoint |

**Harness 设计的真正杠杆**：不是「让 Model 更聪明」（训练成本高、周期长），也不是「让 User 更信任」（不可控），而是**让 Product 这层的工程机制能匹配 Model 与 User 的真实协同模式**。

---

## 对 Harness 工程师的具体启示

### 1. 不要假设 Long-Turn 是异常情况

99.9 分位 Turn Duration 已经突破 45 分钟，并且仍在上升。Harness 必须支持：

- **Checkpoint 机制**（如 Claude Code 的 Esc+Esc+Rewind）——让长任务可恢复
- **状态可见性**——45 分钟内发生了什么，用户要能随时回看
- **异步唤醒**——长任务可以挂起，恢复后状态衔接

### 2. 默认设置不要假设用户是新手

20% 的新手 auto-approve 率是「保守默认值」的选择。但如果你的产品全部按新手设计，会让 40% 的熟练用户体验下降。

**建议设计模式**：
- 默认值偏保守
- 提供「经验解锁」机制——根据 session count 或 trust score 渐进放宽
- 让用户能看到自己的 trust 进度

### 3. 把「Clarification」当成一等公民

Claude 主动问澄清的频率比人类 Interrupt 更高。这意味着：

- Agent 的「我不知道」是个能力，不是个缺陷
- Harness 要把 Clarification 设计成 UX 流畅的环节，不是「失败回退」
- 把 Clarification 数据收集起来，反哺训练——这本身就是产品反馈

### 4. 监控 Deployment Overhang

> "Both measurements point to a significant deployment overhang, where the autonomy models are capable of handling exceeds what they exercise in practice."

这是一个可监控的指标：
- 能力评估 → 理论上限
- 真实部署测量 → 实际使用
- 两者差距 → deployment overhang
- 长期目标：缩小 overhang（让产品/用户跟得上模型能力）

### 5. 跨领域扩张是 Harness 的下一个战场

软件工程以外的领域（金融、医疗、运营）将出现「高风险 + 高自主性」组合：

- 当前 Harness 主要为「代码相关风险」设计
- 未来需要扩展到「跨领域风险」——financial、privacy、regulatory
- 权限模型要从「Operation-level」（read/write/bash）升级到「Domain-level」（trading/clinical/...）

---

## 与现有研究的关系

这篇文章的核心价值在于把三个已有的讨论线串起来：

1. **Effective harnesses for long-running agents**（Anthropic, R336）——讲 Harness 设计原则
2. **How we contain Claude**（Anthropic, R518+）——讲安全防护机制
3. **Cursor Cloud Agent - Temporal + 三层状态解耦**（R595）——讲部署层基础设施

新增的视角是**「真实部署的自主性曲线」**——用数据回答「这些机制在生产中到底被怎么用」。这是 Harness 工程的「实证基础」，是其他文章都缺少的维度。

---

## 引用来源

> "The autonomy agents exercise in practice is co-constructed by the model, the user, and the product."

> "Both measurements point to a significant deployment overhang, where the autonomy models are capable of handling exceeds what they exercise in practice."

> "We also anticipate that agents operating at the extremes of risk and autonomy will become increasingly common."

来源：
- [Measuring AI agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) — Anthropic Research, 2026-06-05
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — Anthropic Engineering
- [Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously) — Anthropic News, 2026-03-02
- 研究团队：Miles McCain, Thomas Millar, Saffron Huang, Jake Eaton, Kunal Handa, Michael Stern, Alex Tamkin, Matt Kearney, Esin Durmus, Judy Shen, Jerry Hong, Brian Calvert, Jun Shern Chan, Francesco Mosconi, David Saunders, Tyler Neylon, Gabriel Nicholas, Sarah Pollack, Jack Clark, Deep Ganguli

---

## 三个备选标题（单位长度 ≤ 30）

1. **测量 Agent 自主性** — 策略：直击核心（单位 13.5）
2. **部署滞后：模型强不等于敢用** — 策略：痛点反差（单位 15.5）
3. **三方共建：自主性不是模型的独角戏** — 策略：观点鲜明（单位 17.5）