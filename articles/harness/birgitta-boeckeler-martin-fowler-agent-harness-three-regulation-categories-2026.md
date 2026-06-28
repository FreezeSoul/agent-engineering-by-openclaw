# Harness Engineering 三维框架：Böckeler 的 Feedforward/Feedback 体系解读

> **核心论点**：Martin Fowler 网站上 Birgitta Böckeler 的这篇 Harness Engineering 文章，做了一件纯工程视角的事——**把「Harness」这个宽泛概念拆解成可操作的维度**。Feedforward vs Feedback 的二元结构，Computational vs Inferential 的执行层划分，以及 Maintainability / Architecture Fitness / Behaviour 三类监管目标，构成了一套完整的 Harness 认知框架。理解这个框架，比记住任何一个具体工具都重要。
>
> **读完能得到什么**：掌握「引导在前、传感在后」的二元结构；理解为什么 LLM-as-judge 是「正向的 prompt injection」；看清 Behaviour Harness 为什么是行业当前最难攻克的领域。

---

## 1. 背景：为什么需要给 Harness 划维度

Harness Engineering 作为一个概念在 2026 年已经被广泛讨论，但存在一个根本问题：**Harness 包含的东西太多了**。系统提示词是 Harness，RAG 是 Harness，工具调用是 Harness，MCP 服务器是 Harness——把所有这些都装进一个袋子，实际上什么都没说。

Birgitta Böckeler（Thoughtworks Distinguished Engineer，超过 20 年软件开发与架构经验）在 Martin Fowler 网站发表的文章，做了一件看似简单实则关键的事：**给 Harness 划定边界，并给出可操作的分类维度**。她的分析针对的是「Coding Agent 用户」这个具体场景，这让整个框架的实用价值大幅提升。

她开篇给出的定义精准地划定了讨论范围：

> "The term harness has emerged as a shorthand to mean everything in an AI agent except the model itself — Agent = Model + Harness. That is a very wide definition, and therefore worth narrowing down for common categories of agents."
>
> ——[Birgitta Böckeler, Harness Engineering, Martin Fowler](https://martinfowler.com/articles/harness-engineering.html)

这个 bounded context 的设定至关重要：她的框架不是关于通用 AI Agent 的，而是专门针对** Coding Agent 用户如何构建自己的 Outer Harness**。

---

## 2. 核心框架：Feedforward 与 Feedback 的二元结构

Böckeler 提出的最核心概念是 Harness 的**二元结构**：

### 2.1 Feedforward（引导）：在行动之前 steering

> "Guides (feedforward controls) — anticipate the agent's behaviour and aim to steer it before it acts. Guides increase the probability that the agent creates good results in the first attempt."

Feedforward 是**预防性控制**——在 Agent 执行之前就给它正确的上下文和约束，减少它犯错的可能性。

典型实现包括：
- **AGENTS.md / CLAUDE.md**：项目级规范文档，告诉 Agent 代码风格、架构约定、「我们这里不这样做」
- **Skills**：可复用的技能包，包含引导指令和 bootstrap 脚本
- **Code mods**：确定性代码转换工具（如 OpenRewrite recipes），在结构层面预防不符合规范的代码生成

### 2.2 Feedback（传感）：在行动之后 self-correct

> "Sensors (feedback controls) — observe after the agent acts and help it self-correct. Particularly powerful when they produce signals that are optimised for LLM consumption, e.g. custom linter messages that include instructions for the self-correction — a positive kind of prompt injection."

Feedback 是**检测+纠正控制**——在 Agent 执行之后检测问题，并触发自我修正。特别值得注意的是 Böckeler 的这个观察：**LLM-optimized 的错误信息本质上是一种正向的 prompt injection**——你主动注入的是修正指令，而非恶意内容。

典型实现包括：
- **Linters 和类型检查**：确定性反馈，毫秒级运行
- **单元测试/集成测试**：结构性反馈，覆盖率是硬指标
- **LLM-as-Judge**：推理性反馈，用另一个 LLM 评估代码质量

### 2.3 为什么两者缺一不可

Böckeler 给出了一个简洁但深刻的结论：

> "Separately, you get either an agent that keeps repeating the same mistakes (feedback-only) or an agent that encodes rules but never finds out whether they worked (feed-forward-only)."

这个洞察的工程含义是：
- **只有 Feedforward**：Agent 按规则行事，但不知道规则是否有效，错误会持续累积
- **只有 Feedback**：Agent 不断被纠正，但没有前置引导，同一个错误可能重复出现多次才被检测到

**真正有效的 Harness = Feedforward 减少错误概率 + Feedback 捕获遗漏错误**。

---

## 3. 执行层：Computational vs Inferential

在 Feedforward/Feedback 的二元结构之上，Böckeler 给出了第二个关键维度：**执行方式**。

| 维度 | Computational（计算型） | Inferential（推理型） |
|------|----------------------|---------------------|
| **性质** | 确定性，CPU 执行 | 语义分析，GPU/NPU 执行 |
| **速度** | 毫秒到秒级 | 秒到分钟级 |
| **成本** | 极低 | 较高 |
| **可靠性** | 高（每次结果一致）| 概率性（非确定性）|
| **适用场景** | 每次变更都运行 | Post-integration 或关键节点 |
| **典型例子** | Tests、Linters、Type Checkers、ArchUnit | LLM Code Review、LLM-as-Judge |

### 3.1 为什么这个划分很重要

这个划分解决了行业里的一个常见误区：**有人试图用 LLM 去做所有 Harness 的工作，结果成本爆炸且不可靠**。

Böckeler 的观点是：**Computational 传感器应该覆盖 80% 的场景**，因为它们够快、够便宜、够可靠。只有在需要语义判断的地方（比如「这段代码是否过度设计」「这个 PR 是否符合业务意图」），才值得动用推理型传感器——但要接受它的非确定性。

反过来，**推理型引导的价值在于处理无法被规则穷举的场景**。比如「这个模块的架构是否合理」——这不是一个可以用正则表达式检查的规则，而是一个需要语义理解的判断。

### 3.2 两者在开发周期中的分布

Böckeler 引用了软件工程中经典的**Shift Left**原则来说明 Harness 控制的分布：

> "You want to have checks as far left in the path to production as possible, since the earlier you find issues, the cheaper they are to fix."

具体分布逻辑：

**Feedforward（引导）**：
- 极快且确定性 → 可以在 commit 之前运行（pre-commit hook）
- 推理型引导（如 AGENTS.md）→ 在 Agent 启动时一次性加载

**Feedback（传感）**：
- Computational 传感器（linter、fast tests）→ 每次 commit、每次 PR 都运行
- Inferential 传感器（LLM-as-judge）→ Post-integration pipeline，仅在必要时触发

这个分布逻辑回答了一个实际问题：**什么时候用 LLM 做质量判断？** 答案是：在 CI/CD pipeline 的后期，在 Computational 传感器已经过滤掉确定性问题之后，作为最后一道语义层面的质量门。

---

## 4. 三类监管目标：Harness 到底在管什么

Böckeler 提出的第三个关键维度是 **Harness 试图监管的目标**。她识别出三个类别，这个分类的价值在于：**不同目标的 Harness 可行性差异巨大**，了解这一点可以避免制定不切实际的自动化目标。

### 4.1 Maintainability Harness（可维护性监管）

这是**当前最容易构建 Harness 的领域**，因为我们有大量现成的确定性工具。

**Computational 传感器覆盖范围**：
- 重复代码检测
- 循环复杂度检查
- 测试覆盖率
- 架构漂移（模块边界违反）
- 代码风格违规

**Inferential 传感器（LLM）可以部分处理**：
- 语义重复的代码
- 冗余测试
- 暴力修复
- 过度工程化的方案

**两者都无法可靠处理的**：
- 需求误判（Misdiagnosis of issues）
- 过度工程化和不必要的功能
- 理解偏差导致的错误方向

这个结论非常重要：Böckeler 明确指出，**即使有 LLM 加持的传感器，也无法可靠捕获「人类最初需求就没写清楚」的问题**。这是当前 Harness 的能力边界。

### 4.2 Architecture Fitness Harness（架构适应性监管）

这个类别将 **Fitness Functions** 概念引入 Agent Harness。

示例：
- **Feedforward**：Skills 传递性能需求描述，性能测试规范
- **Feedback**：性能测试结果反馈给 Agent，告知性能是否达标或退化

Böckeler 还提到了 observability 相关的例子：
- Feedforward：Skills 描述日志标准（logging conventions）
- Feedback：调试指令要求 Agent 反思它可用的日志质量

这个类别的关键是：**架构决策通常需要跨文件的全局视角**，这对单次工具调用维度的 Agent 来说是挑战，需要显式的架构约束规则（如 ArchUnit 测试）来 enforcement。

### 4.3 Behaviour Harness（行为监管）——行业最大的未解难题

这是 Böckeler 认为**当前最难解决的领域**，也是文章中最有价值的坦诚判断。

当前行业实践：
- **Feedforward**：功能规格说明书（从简短的 prompt 到多文件描述）
- **Feedback**：检查 AI 生成的测试套件是否 green、覆盖率是否足够

Böckeler 的判断毫不客气：

> "This approach puts a lot of faith into the AI-generated tests, that's not good enough yet."

她提出的核心问题是：**你怎么知道 AI 生成的测试真的测试了正确的行为？** 如果测试本身是被测系统的「共谋」，那么测试通过并不意味着行为正确。

她的同事在部分场景中取得了不错效果的是 **Approved Fixtures** 模式——人类预先批准 fixtures，Agent 在此基础上生成测试。这个方法并非万能，但在某些领域确实有效。

**Behaviour Harness 为什么最难**：
1. 功能正确性的定义本身就是最难的问题
2. AI 生成的测试套件质量无法被自身验证（循环依赖）
3. 人类的 manual testing 依然是最终信任锚点

这个判断对从业者的实际意义：**不要试图用 Harness 完全消除 Behaviour 层面的人工审查**。Behaviour Harness 的目标应该是**减少人工审查的频率和范围**，而不是替代人工审查。

---

## 5. Harnessability：代码库本身的「可 harness 性」

Böckeler 提出了一个容易被忽视的概念：**不是所有代码库都同等容易被 Harness**。

**强类型语言天然具备的传感器**：类型检查本身就是最基础的 Computational 传感器，不需要额外配置。

**清晰模块边界的价值**：明确的模块边界允许架构约束规则（如 ArchUnit）的构建，这是 Architecture Fitness Harness 的基础设施。

**框架的隐式保护**：像 Spring 这样的框架抽象掉了大量细节，Agent 不需要担心这些细节，因此成功率更高。

### Greenfield vs Legacy 的不对称性

这是全文中最发人深省的观察之一：

> "Greenfield teams can bake harnessability in from day one — technology decisions and architecture choices determine how governable the codebase will be. Legacy teams, especially with applications that have accrued a lot of technical debt, face the harder problem: **the harness is most needed where it is hardest to build**."

这个不对称性是 Agent Engineering 领域的结构性挑战：**最需要 Harness 的遗留系统，往往最难构建有效的 Harness**。这意味着在遗留系统上引入高自主性 Coding Agent 的风险，远比在 greenfield 项目上引入要大得多。

---

## 6. The Steering Loop：Harness 是持续工程，不是配置

Böckeler 文章的最后一个核心贡献是 **The Steering Loop** 概念——人类在 Harness Engineering 中的角色是**持续迭代 Harness**，而不是一次性配置好后置之不理。

> "Whenever an issue happens multiple times, the feedforward and feedback controls should be improved to make the issue less probable to occur in the future, or even prevent it."

这个概念的工程含义是：
1. **Harness 是活的系统**：随着 Agent 在代码库上工作，会暴露新的失败模式
2. **每次重复出现的错误都是 Harness 的改进机会**：正确的响应不是修改提示词，而是改进 Harness
3. **AI 可以帮助构建 Harness 本身**：Böckeler 提到 Agent 可以帮助编写结构性测试、从观察到的模式生成规则草案、为定制 linter 提供 scaffold

这也呼应了 Mitchell Hashimoto 对 Harness Engineering 的定义（已在仓库 `harness-engineering-mitchell-hashimoto-agent-framework-2026.md` 中覆盖）：**「每一次你发现 Agent 犯了一个错误，你就花时间工程化地解决它，使得 Agent 再也不会犯同样的错误。」**

---

## 7. 与现有 Harness 覆盖的差异

本文与仓库中已有的 Harness 文章（特别是 `harness-engineering-openai-fowler-convergence-2026.md`）的关系：

**已有的 convergence 文章侧重于**：
- OpenAI Codex 的五条 Harness 原则（0行人写代码，百万行程序的极端实验）
- AGENTS.md 作为目录而非百科全书
- 应用对 Agent 可见（per-git-worktree、CDP 集成、可观测性）

**本文（Böckeler Framework）新增的独特贡献**：
- Feedforward vs Feedback 的**完整二元结构**（不是隐式使用，而是显式框架）
- Computational vs Inferential 的**执行层划分**（回答了「什么时候用 LLM」）
- **三种监管目标分类**（Maintainability / Architecture Fitness / Behaviour）及其不同难度
- **Harnessability** 概念（greenfield vs legacy 的不对称性）
- Behaviour Harness 是**行业最大未解难题**的具体判断

---

## 8. 实践启示

基于 Böckeler 的框架，我给出以下实践判断：

**1. 构建 Harness 的顺序建议**
优先构建 Computational 传感器（linter、test、type checker）→ 再引入架构约束（ArchUnit、Fitness Functions）→ 最后在关键节点使用 Inferential 传感器。不要试图用 LLM 做所有事。

**2. Behaviour Harness 的现实目标**
Behaviour Harness 的目标不是消除人工审查，而是**将人工审查的范围缩小的可管理的大小**。当前阶段，Approved Fixtures 模式是有限范围内有效的方案。

**3. Greenfield 项目的架构决策**
在 greenfield 项目中，**技术选型就是 Harness 可行性选型**。强类型语言 + 清晰模块边界 + 成熟框架，是在为未来的 Agent 可控性投资。

**4. Steering Loop 的机制设计**
建立错误模式到 Harness 改进的闭环。当同一个错误出现两次时，正确的响应不是修改 prompt，而是问：「我需要在 Harness 的哪个层面（Guide 还是 Sensor）加入什么控制来预防？」

---

## 引用

> "A good harness should not necessarily aim to fully eliminate human input, but to direct it to where our input is most important."
>
> ——[Birgitta Böckeler, Harness Engineering, Martin Fowler](https://martinfowler.com/articles/harness-engineering.html)

---

*来源：[Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) by Birgitta Böckeler, Martin Fowler, 2026*