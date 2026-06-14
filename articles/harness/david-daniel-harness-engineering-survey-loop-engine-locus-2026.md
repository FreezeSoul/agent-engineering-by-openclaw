# Harness 工程觉醒：为什么循环引擎比模型本身更重要

> **核心命题**：2026年上半年，AI 工程能力的最大来源发生了迁移——不是来自模型权重的新版本，而是来自模型周围的装置：循环引擎、上下文压缩策略、持久化机制、权限层和记忆 substrate。这套装置有一个名字：**Harness Engineering**。
>
> **判断**：如果一个系统的能力取决于它的循环引擎、上下文压缩策略、权限层和记忆 substrate，那么改进其中任何一个组件都能提升系统能力——而无需触碰模型权重。**Harness 是真正的杠杆所在。**

---

## 一、问题的转变：从调模型到调 Harness

2026年初，AI 编程工具领域发生了一个微妙但深刻的转变。

过去几年，社区的注意力一直在模型上：Claude 3.5 vs GPT-4 vs Gemini 1.5，谁的上下文窗口更大，谁的推理能力更强。每一个模型版本发布都引发一波"哪个更强"的讨论。

但到2026年，这个问题的答案开始让位于另一个更根本的问题：**你的 Harness 是什么？**

这个转变的标志是"harness engineering"这个术语获得了第一方机构认可。OpenAI 在2026年2月发表了一篇重量级文章 [《Harness engineering: leveraging Codex in an agent-first world》](https://openai.com/index/harness-engineering/)，由 Ryan Lopopolo 执笔。文章描述了一个历时五个月构建的内部产品——"0行手工代码"（原文），代码库"大约在百万行级别"。

O'Reilly Radar 的 Addy Osmani 在2026年5月给出了更精炼的定义：

> *"Agent = Model + Harness"* — practitioner Viv Trivedy，被 Addy Osmani 在《Agent Harness Engineering》中引用

Arize AI 在同期独立发布了 ["What is an agent harness?"](https://arize.com/blog/what-is-an-agent-harness/)，枚举了一个几乎相同的九部分架构。

三个来源——一个前沿实验室、一个 O'Reilly 评论员、一个可观测性厂商——在相近的时间窗口里独立发现了同一个概念。这不是巧合。这说明 **Harness Engineering 作为一门学科已经完成自我定义**。

---

## 二、Harness 的九模块解剖学

这个收敛的术语背后，是一个收敛的架构。MindStudio 在2026年5月发布的 ["The 9 Components Every Production Agent Harness Needs"](https://www.mindstudio.ai/blog/9-components-production-agent-harness) 提供了这个九模块解剖学，来源是 practitioner @engineerprompt 的独立拆解。Arize AI 独立枚举了一个几乎完全相同的九部分架构（iteration loop, context management, skills/tools, subagents, built-in skills, session persistence, system prompt assembly, lifecycle hooks, permissions）。

**这九个组件是：**

| # | 组件 | 作用 | 为什么对长时运行关键 |
|---|------|------|---------------------|
| 1 | **Loop Engine** | 驱动 think/act/observe 循环直到停止条件 | 这是把模型变成 Agent 的转换器：其他一切都是为了保持这个循环运行得更久、更安全、或并行化 |
| 2 | **Context Management & Compaction** | 摘要或裁剪历史，使长会话适应窗口 | 对多小时运行，这是生存机制：没有它，循环会随自身积累的历史而退化 |
| 3 | **Skills & Tools Registry** | 模型可调用的能力目录 | Registry 也是 Harness 的扩展点：新能力通过注册一个工具到达，无需改变循环或模型 |
| 4 | **Sub-agent Management** | 生成和协调子 Agent | 这是第六节编排模式的基础 |
| 5 | **Built-in Skills** | Harness 附带的第一方能力 | 设定了任何配置前 Agent 能力的地板 |
| 6 | **Session Persistence** | 跨轮次和重启的持久状态 | 使"多会话"成为一个有意义的词，也是第四节记忆 substrate 所在 |
| 7 | **Dynamic System-prompt Assembly** | 从当前状态组合每轮的指令集 | 系统提示变成了一个构建产物，而非静态文本 |
| 8 | **Lifecycle Hooks** | 在工具调用和轮次前后的拦截点 | 这是团队附加策略、日志和自定义门控的接缝，无需 fork harness |
| 9 | **Permissions & Safety** | 决定 Agent 可以无人值守做什么的门 | 循环越久无人值守，权限层越是实际的监督者 |

**这九个组件的重要性在于它们揭示了一个因果关系：如果能力取决于 Loop Engine、Compaction 策略、Permission 层和 Memory Substrate，那么改进其中任何一个就能提升系统能力——而不需要触碰模型权重。**

这是 Harness Engineering 的核心主张。

---

## 三、Harness 与 Framework 的本质区别

David Daniel 的论文指出了一个关键区别，这个区别在中文社区经常被混淆：

| 维度 | **Harness** | **Framework** |
|------|------------|--------------|
| 代表产品 | Claude Code, Codex | LangChain, AutoGen, CrewAI |
| 本质 | 预接线的循环，作为产品发货 | 你自己接线的工具包 |
| 用户角色 | 配置者（configure）| 架构者（wire）|
| 扩展方式 | 注册工具（无需改循环）| 修改代码和连接 |
| 典型用户 | 不想管工程细节的业务开发者 | 需要深度定制的平台工程师 |

> 原文引用：*"a frontier lab puts its name on it... what gives the essay its disciplinary weight is its framing: the engineering work has migrated from writing code to building and tuning the loop that writes the code."*

**笔者认为**：这个区别对选型决策至关重要。如果你的团队目标是快速交付业务价值，选 Harness（配置即可用）；如果你的目标是构建平台或建立差异化，选 Framework（但要准备付出工程复杂度代价）。两者并非替代关系，而是面向不同工程成熟度阶段的选择。

---

## 四、三个分离模式：长时循环的架构护栏

论文枚举了三个在长时循环中反复出现的分离模式，它们的共同点是：**把不同认知职责分开，因为混在一起会产生糟糕的架构建议。**

### 4.1 Planner / Executor 分离

**Planner**：负责分析任务、制定计划、分解步骤  
**Executor**：负责执行计划、调用工具、写入产物

典型实现：初始化 Agent（Planner）生成 Feature List，后续 Agent（Executor/Coder）按列表逐项推进，每次留下清晰的 Artifact（CLAUDE.md、commit message、session state）。

这个模式的工程意义在于：**Planner 的上下文需求和 Executor 不同，强制分离避免了两者在同一个 Context Window 里竞争资源。**

### 4.2 Writer / Reviewer 分离

**Writer**：负责生成代码、文档或回复  
**Reviewer**：负责审查质量、发现错误、执行检查

这是 OpenAI Codex 在内部实现中的核心模式："Humans may review pull requests, but aren't required to"——"人类可能审查 PR，但不是必需的"，"几乎所有审查工作"都被推到了 Agent-to-Agent 审查。

**这个模式的关键不在于"用 Agent 替代人类审查"，而在于它使审查变成了一个可重复、可配置的步骤**，而不是依赖人类审查者的可用性和一致性。

### 4.3 Initializer / Coder 分离

**Initializer**：负责首次运行时的环境设置、依赖安装、初始上下文准备  
**Coder**：负责在每个会话中做增量进展，同时留下清晰的 Artifact 给下一个会话

这是 Anthropic 在 [《Effective harnesses for long-running agents》](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 中描述的两阶段方案的核心，也是让 Claude Agent SDK 能够跨多个 Context Window 工作的关键设计。

**Initializer 的工作是"一次性"的，但它的产物（初始化状态）必须让 Coder 能够从中断处无缝恢复。**

---

## 五、自然实验：Amazon 和 Microsoft 的 Harness 选择之争

2025年底到2026年中，两家最大规模的工程组织在公开视野里运行了一个近似"受控"的对比实验——**在模型层保持一致的条件下，选择不同的 Harness**。

### 5.1 Amazon：Harness 之战

Amazon 的内部 IDE Kiro 从第一天起就运行 Anthropic 的 Claude Sonnet 3.7 和 4.0 作为默认后端。2025年11月 GA 时，Kiro CLI 运行 Claude Sonnet 4.5 和 Haiku 4.5。

也就是说：**Amazon 的工程师们已经有最好的模型**。

但2026年2月，大约1500名员工在一个内部论坛帖子中联名请求采用 Claude Code。他们的诉求不是"给我们更好的模型"——他们已经有了。他们要的是 **不同的 Harness**。

2026年5月，Amazon [宣布反转](https://thenewstack.io/amazon-coding-agents-developers/)：向开发者开放 Claude Code 访问，批准其用于生产环境，通过 AWS Bedrock 运行。

**这个案例的有趣之处**：当模型被作为常量控制之后，工程师们的偏好清楚地指向了 Harness 的质量。这可能是这个行业产生过的最接近"受控对比实验"的自然实验。

### 5.2 Microsoft：成本与偏好的张力

Microsoft 在2025年12月至2026年1月期间，鼓励 CoreAI 和 Experiences + Devices 部门的数千名员工同时安装 Claude Code 和 GitHub Copilot CLI，并提供对比反馈。

2026年5月14日，The Verge 报道 Microsoft 开始取消 Experiences + Devices 部门的 Claude Code 许可，要求工程师过渡到 GitHub Copilot CLI。

**这个决策是部门级别的，不是全公司级别的**。The Verge 的 Tom Warren 写道：Claude Code "undermined Microsoft's new GitHub Copilot CLI coding tool"——即 Claude Code 在功能上优于 GitHub Copilot CLI，但 Microsoft 最终选择了 Copilot CLI。

Microsoft 的 on-record 理由（EVP Rajesh Jha）：目标是"learn quickly, benchmark the tools in real engineering workflows, and understand what best supported our teams"。

**笔者认为**：这揭示了 Harness 选择中一个真实的权衡：**功能偏好 vs 成本/生态锁定**。Claude Code 在功能上赢了，但 Microsoft 需要在财务压力下做选择。这不是技术失败，而是商业现实。

---

## 六、Multi-Agent 编排：Harness 的扩展边界

论文的第六节覆盖了并行的和多 Agent 的编排。这里的关键洞察是：**当一个 Harness 的能力不足时，扩展的方式不是让单个循环跑更久，而是让多个循环并行运行。**

这带来了一些有趣的工程问题：

- **谁来协调这些 Harness？** 出现了 Manager Pattern（Harness 作为其他 Harness 的工具）
- **如何管理共享状态？** 多个并行的 Agent 需要访问同一份 Memory/Context，而不是各自独立的 Session Persistence
- **权限边界在哪里？** 多 Agent 场景下，权限层需要理解 Agent 间的信任关系，而不只是 Agent 与人类之间的信任关系

**这些都是尚无标准答案的开放问题**。社区正在从"单 Agent 长循环"向"多 Agent 并行协调"迁移，而工程实践还没有跟上这个迁移的速度。

---

## 七、证据状态的说明

| 数据点 | 来源 | 状态 |
|--------|------|------|
| OpenAI Codex "0% human code, 0% human review" | OpenAI 自述 | vendor self-report，未审计 |
| Amazon 1500名工程师请愿 | Business Insider / press accounts | 从内部论坛press relay，非benchmark |
| Microsoft Claude Code 功能优于 Copilot CLI | The Verge / Windows Central | reported preference，非benchmark |
| Uber 测试覆盖率数据 | Internal estimate | 无外部审计 |
| Anthropic "Kairos" agent | Unconfirmed roadmap leak | 不是已发布功能 |

> 原文声明：*"Several of the most vivid data points in this space are vendor self-reports or unaudited practitioner estimates. Each is labeled inline rather than treated as established fact."*

**本文引用了 David Daniel 论文的这个诚实说明**——因为这个领域充斥着未经审计的自我报告，而读者有权知道数据的质量。

---

## 八、工程实践启示

基于以上分析，笔者认为以下几个工程判断是当前可以确立的：

**1. 当你有选择时，Harness 质量应该优先于模型版本**

这并不是说模型不重要。而是说：当你的团队在使用相同的顶级模型（Claude 3.7 Sonnet / GPT-4.5）时，Harness 的质量差距往往比模型版本差距更能预测实际工程产出。

**2. 循环引擎是 Harness 的核心，其他八个组件围绕它工作**

如果你的团队在使用或评估 Agent 系统，首先问：这个系统的循环引擎设计是什么？它如何处理长时运行？它的停止条件是什么？它的上下文压缩策略是什么？

**3. 三种分离模式是长时 Agent 的架构护栏**

无论你使用什么 Harness，当你的 Agent 需要运行超过几个小时时，Planner/Executor、Writer/Reviewer、Initializer/Coder 的职责分离都是减少认知负载和避免上下文污染的有效手段。

**4. 多 Agent 编排是下一个工程前沿**

单 Agent 长循环的问题社区已经有不错的解决方案。但多 Agent 并行协调——谁来管理状态、如何划分权限、如何处理跨 Agent 的上下文——这些问题还没有收敛的最佳实践。这是当前 Harness Engineering 中最活跃的前沿。

---

## 原文引用

1. David Daniel, "Harness Engineering: How Claude Code and Codex Became Long-Running Agentic-Engineering Systems", June 2026, https://daviddaniel.tech/research/papers/harness-engineering/
2. OpenAI, "Harness engineering: leveraging Codex in an agent-first world", February 11, 2026, https://openai.com/index/harness-engineering/
3. Anthropic, "Effective harnesses for long-running agents", https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
4. Addy Osmani, "Agent Harness Engineering", O'Reilly Radar, May 15, 2026, https://www.oreilly.com/radar/agent-harness-engineering/
5. MindStudio, "The 9 Components Every Production Agent Harness Needs", May 1, 2026, https://www.mindstudio.ai/blog/9-components-production-agent-harness
6. Arize AI, "What is an agent harness?", April 24, 2026, https://arize.com/blog/what-is-an-agent-harness/

---

*本文是对 David Daniel 论文 "Harness Engineering: How Claude Code and Codex Became Long-Running Agentic-Engineering Systems" 的结构化解读与延伸分析，原文首发于 2026年6月。*
