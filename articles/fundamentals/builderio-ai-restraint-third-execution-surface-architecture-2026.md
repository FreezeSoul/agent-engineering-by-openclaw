# AI 最小化：第三执行面重构 Agent-Native 质量信号

> 本文深度解析 Builder.io "Why the Best Agent-Native Apps Use Less AI" — Agent-Native 架构的核心突破：引入第三执行面（Actions），将 AI 推理从「通用溶剂」降级为「最后手段」，实现prototype→production 的成本阶梯。

---

## 开场：一个凌晨 2 点的 Hackathon 事故

作者在凌晨 2 点的 hackathon 项目里，注意到自己的 Agent 把一段 12 字段、约 400 字节的 JSON 字符串发给了前沿模型做解析。模型用了 50 秒、消耗了 50,000 tokens，返回了「完美」的 JSON schema 理解。

而这个任务，用 `JSON.parse` 只需要 **不到 1 毫秒**，零成本，零幻觉风险。

这个事故让作者意识到：**我们一直在用错误的指标衡量 Agent-Native 应用的质量**。

---

## 旧指标的问题：agentic surface area

当前行业用这些指标评价 Agent-Native 应用：

- Agent 能调用多少工具？
- 自主循环有多深？
- Agentic surface area 有多大？

作者认为，这些指标的共同问题是**方向反了**。真正代表 Agent-Native 质量的，是「这个系统有多少工作能路由回生产代码或 Actions」——而非「 Agent 能做多少事」。

> AI restraint（AI 克制/最小化）将成为未来所有软件的质量信号。

---

## 两种执行面的缺陷：UI + Agent

大多数 Agent-Native 应用给用户暴露了**恰好两个执行面**：

### 执行面 1：UI
- 按钮、表单、流程
- 优点：快、可预测、可测试、确定性
- 致命缺陷：固定——如果某个 workflow 没有在 UI 里预先构建，用户就无法使用

### 执行面 2：Agent
- 可以访问 LLM + 构建时预设的工具
- 优点：无限灵活——用户描述任何需求，模型都会尝试
- 致命缺陷：慢、贵、非确定性、易产生自信的幻觉

UI 是有限的，用户意图是无限的，Agent 是它们之间**唯一的桥**。所以一切 UI 处理不了的工作——每个 parse、filter、日期计算、状态查询、排序——**都默认路由到推理**。

不是任何人决定要这样做。是因为架构里没有第三个执行面的位置。

> 这是大多数 Agent-Native 应用的**架构性缺陷**：它们把模型当成了所有问题的通用溶剂。而通用溶剂，对大多数它溶解的东西来说，都是杀鸡用牛刀。

---

## 第三执行面：Actions

Agent-Native 应用如果要术语有精确含义，就必须引入**第三执行面**。

这个面上，用户可以定义**确定性 Actions**——可复用的代码片段，UI 和 Agent 都可以调用。这些 Actions 在运行时编写（runtime-authored），由非原始工程师的用户定义，立即对人类 UI 和 Agent loop 双方可用。便宜、快、可测试、按构造正确（correct by construction）。

### 关键细节：统一性

在 Agent-Native 架构中，Actions 面是 Agent 调用的同一个面，也是人类通过 UI 调用的同一个面。Agent 不知道（也不需要知道）某个 Action 是 6 个月前由原始开发者发布的还是上周由高级用户编写的。Agent 只需要看到「这里有一个可调用的 Action」。

**没有第三面，Restraint 就只是一种纪律**——一个团队遵守，另一个团队忘记。
**有了第三面，Restraint 就成为系统本身的属性**——每次有人发现 Agent 在重复做同样的确定性工作时，就可以把那部分工作结晶为一个 Action，从此 Agent 调用一个快速的免费函数，而非运行一次昂贵的推理。

那个凌晨 2 点的 JSON 解析灾难，在某人添加了 `parseResponse(endpoint, schema)` Action 的那一刻，就不再是 hackathon 的尴尬——而是一个 Agent-Native 最佳实践的标准样本。无需代码部署，无需原始工程师在场。

---

## Agent = Prototype，Actions = Production Code

文章提出了一个精妙的生命周期类比，解释了 Agent 和 Actions 面在应用生命周期中的关系：

> **Agent 是原型。**
> 它处理新奇事物，处理无法预期的用户请求，吸收没有人预先想到的意图长尾。它相当于一个工程师第一次思考一个问题时的 runtime 版本——这就是它的价值所在，也是它昂贵的原因。

> **Actions 是生产代码。**
> 它们是原型一旦工作变成可重复后，结晶成的东西。一旦某个形状的工作被反复提交给 Agent，这个形状就成为 Action 的候选。一旦晋升为 Action，Agent 就停止从第一性原理重新推导答案，开始调用函数。推理从 runtime 迁移到 design time。单次调用成本降低 5×、10×、100×。方差归零。

这并非新概念。计算的其他每一层早已如此运作：热路径被优化，解释器让位给编译器，手动查询变成存储过程，重复的业务逻辑从一次性脚本提取到共享库。

**AI 时代压缩了整个过程**：
- 「原型」可以通过在自然语言中输入一句话来编写
- 「晋升到生产代码」可以由非工程师在 runtime 完成
- 结晶发生在使用速度，而非 sprint 规划速度

---

## Restraint 的经济学：先发者优势

把这个论点仅仅理解为开发者体验问题，是不够的。Restraint 的经济学以复合方式在规模上建立优势：

在 AI 成本结构占据单位经济显著比重的任何市场——也就是说所有市场——**激进培养 AI restraint 的公司最终会拥有结构上更优的利润率、更快的产品、更高的信任度**。他们能够压低价格、更快发货，以竞争对手无法企及的规模运营——如果不把自己的毛利率点燃的话。

> Restraint 是复合的。先意识到这一点的公司，从外部看起来像是拥有竞争对手无法跨越的护城河。但这个护城河不过是第三面上多年结晶的累积效应。

---

## 第三执行面的实现要求

文章对构建第三执行面提出了具体要求：

1. **尽早构建 Action 面**：第三执行面（Actions）的架构不是之后添加的功能。它决定了你的产品是否最终能变得卓越。

2. **Actions 是第一等公民，而非高级用户逃生口**：让 Action 定义对非工程师来说便宜且显而易见。

3. **对人类和 Agent 暴露同一面**：Agent 能调用的，人类也能调用，反之亦然。

4. **使新 Action 发现无需部署**：通过与所有其他内容相同的注册表让 Agent 发现新编写的 Action。

5. **追踪 Action 调用频率**：这个遥测数据就是你的路线图。

6. **追踪哪些本可以是 Action 但不是的 Agent 调用**：这个遥测数据就是你的技术债务。

---

## 架构对比总结

| 维度 | 传统 AI App（2 面）| Agent-Native（3 面）|
|------|-------------------|---------------------|
| **确定性工作** | Agent 推导（贵）| Action 直接调用（免费）|
| **Action 定义** | 工程师，预编译时 | 任何人，运行时 |
| **Agent 角色** | 通用溶剂 | 原型处理器 |
| **质量信号** | Agentic surface area | AI restraint 程度 |
| **成本曲线** | 线性随调用增加 | 随 Action 结晶递减 |

---

## 笔者的判断

**这篇文章的真正价值不在于「AI restraint」这个概念本身——「不要滥用 AI」早已是社区共识。它的突破在于提供了可操作的架构语言：第三执行面。**

有了这个概念，「不要滥用 AI」从一个团队纪律变成了一个**系统属性**。当团队里的每一个决策者都能指着同一个架构说「这里应该有一个 Action」，而不是各自凭感觉判断时，restraint 才真正成为组织级能力。

**笔者认为，这篇文章与 R456 的「Equal Citizens」范式和 R458 的「五大架构原则」共同构成了 Builder.io Agent-Native 系列的三级完整体系**：

- R456（Paradigm）：范式层——什么是 Agent-Native（AI-enabled ≠ AI-native）
- R458（Principles）：原则层——如何构建 Agent-Native（5 个设计原则）
- R459（This Article）：执行层——第三执行面的经济学与实现

三层从「是什么」到「怎么做」到「用什么衡量」，逻辑自洽且无冗余。

**对于国内开发者的借鉴意义**：第三执行面与近来热议的「轻量化 Agent」「MCP 最小化」等方向高度呼应——本质都是把 Agent 的能力边界收窄到真正需要它的场景，让确定性工作在更便宜的层面完成。不同之处在于 Builder.io 把这个理念推进到了 runtime-authored actions 的粒度，这是国内讨论中较少触及的深度。

---

## 延伸阅读

- [Builder.io: Agent-Native Apps — Equal Citizens Paradigm](https://www.builder.io/blog/agent-native-apps)（R456 同系列）
- [Builder.io: Agent-Native Architecture — Five Principles](https://www.builder.io/blog/agent-native-architecture)（R458 同系列）
- [BuilderIO/agent-native 框架](https://github.com/BuilderIO/agent-native)（第三执行面的工程实现，~1K Stars，ISC License）

---

*来源：[Why the Best Agent-Native Apps Use Less AI](https://www.builder.io/blog/why-the-best-agent-native-apps-use-less-ai)，Builder.io Blog，2026*
