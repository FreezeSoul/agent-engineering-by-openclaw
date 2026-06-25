# OpenAI 的 Harness Engineering 实验：零手动代码、百万行与 3.5 PRs/人/天

> **来源**：[Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/)，OpenAI，2026年2月

## 核心判断

过去五个月，OpenAI 团队用纯 Codex 写出了一个有真实用户的产品——百万行代码、零手动提交、日均 3.5 PRs/人。这个实验的结论不是「Codex 比人类强」，而是：**当 Agent 成为执行主体，工程师的核心工作从「写代码」变成「设计让 Agent 能可靠工作的环境」**。这不是一个关于 AI 的故事，这是一个关于工程角色的重定义。

---

## 实验背景

2025年8月末，一个空仓库迎来了第一次提交。

这个产品的开发规则只有一条：**不允许任何人手动写代码**。不是「鼓励用 AI」，是字面意义上的零手写——应用逻辑、测试、CI 配置、文档、可观测性、内部工具，全部由 Codex 生成。人类只做一件事：**描述任务，然后让 Agent 执行**。

五个月后，仓库包含约**百万行代码**，3人团队合并了约 **1500 个 PR**，人均日产出 3.5 PRs。随着团队扩到7人，这个数字没有下降，反而在上升。

> "We intentionally chose this constraint so that we would build what was necessary to increase engineering velocity by orders of magnitude."
> 
> 我们刻意选择这个约束，是为了构建那些能将工程效率提升一个数量级所需的东西。

这不是概念验证。这是**真实产品**——内部日活用户、外部 alpha 测试员都在用。唯一特殊的是：没有一行代码是工程师亲手敲的。

---

## 工程师的角色重定义

### 不是「AI 写代码」，是「环境设计」

实验最初的进展比预期慢。但原因不是 Codex 不够强，而是**环境配不上 Agent 的能力**。

OpenAI 团队的原话：

> "Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified. The agent lacked the tools, abstractions, and internal structure required to make progress toward high-level goals."

当一个问题卡住，人类的本能反应是「再试一次」。但在这个环境里，这个策略无效。正确的做法是：**「什么能力缺失了，如何让 Agent 能理解并遵守它？」**

这是两种完全不同的工程思维。传统工程师遇到 bug → 修复 bug；Harness 工程师遇到瓶颈 → 重新设计让 Agent 能工作的环境。

### Agent-to-Agent Review

人类最终几乎退出了代码 review 环节。Codex 被要求自行 review 本地变更，在云端发起其他 Agent review，响应人类或 Agent 的反馈，反复迭代直到所有 Agent reviewer 满意。这个过程被 OpenAI 称为 **Ralph Wiggum Loop**——直到所有相关方都点头，才算完成。

> "Humans may review pull requests, but aren't required to. Over time, we've pushed almost all review effort towards being handled agent-to-agent."

这揭示了一个关键转变：当 Agent 的输出质量足够高，人类不再是质量的守门人，而是**方向的定义者**。

---

## 仓库知识 = 系统事实

这是我认为这篇博文最值得记住的工程洞察。

### AGENTS.md 作为百科全书失效了

OpenAI 试过「一本大 AGENTS.md」的方式——把所有规则写进一个文件，塞进 Agent context。效果如预期般糟糕：

| 失败模式 | 描述 |
|---------|------|
| **上下文拥挤** | 巨型指令文件挤占了任务、代码和相关文档的空间，Agent 要么漏掉关键约束，要么开始优化错误的指标 |
| **过犹不及** | 当所有事情都标注为「重要」，就没有重点了。Agent 开始本地模式匹配，而非系统性导航 |
| **快速腐坏** | 单一本 monolithic 手册变成了一堆过时规则的坟墓。Agent 无法判断哪些仍然有效，人类停止维护，文件安静地变成了「有吸引力的麻烦」 |
| **难以验证** | 一个单一 blob 无法做机械检查（覆盖率、新鲜度、归属、交叉链接），漂移不可避免 |

这不是 AGENTS.md 本身的失败，是**信息组织方式**的失败。

### 解决方案：AGENTS.md = 目录，docs/ = 百科全书

改进后的方式：

- **AGENTS.md（约 100 行）**：作为 context 注入，只做**地图**——指向更深层事实的指针，而非事实本身
- **docs/ 目录**：知识的系统记录，按主题索引，包含验证状态和归属
- **Architecture 文档**：领域顶层地图和包分层
- **Plans 即第一等公民**：临时轻量计划用于小改动，复杂工作使用执行计划，记录进度和决策日志，check in 到仓库

> "This enables progressive disclosure: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front."

这个机制通过机械方式强制执行：定制的 linter 和 CI 任务验证知识库是最新的、交叉链接的、结构正确的。一个定期的「文档园丁」Agent 扫描过时文档并发起修复 PR。

**关键认知**：对于 Agent 来说，任何在运行期间无法在 context 中访问的东西，**等同于不存在**。存在 Google Docs、聊天记录、人类脑海中的知识对 Agent 不可见。**只有仓库本地的版本化产物**（代码、markdown、schema、可执行计划）才对 Agent 可及。

---

## 让应用对 Codex 可读

当代码吞吐量增加，人类 QA 能力成为瓶颈。为了最大化人类时间，OpenAI 做了两件事：

### 1. Chrome DevTools Protocol 接入 Agent Runtime

Agent 无法直接「看到」浏览器里的 UI 行为——除非你把 UI 变成可读的数据。他们做了：

- App 支持 per-git-worktree 启动，所以 Codex 可以为每个变更启动一个独立实例
- Chrome DevTools Protocol 接入 Agent runtime，支持 DOM snapshot、截图、导航
- Codex 可以复现 bug、验证修复、直接推理 UI 行为

### 2. 可观测性栈暴露给 Codex

Logs、metrics、traces 通过本地可观测性栈暴露给 Codex，且是**ephemeral 的**——每个 worktree 独立，Agent 工作完毕后销毁。Codex 可以用 **LogQL 查日志**、**PromQL 查指标**。

这让之前不可能的 prompt 变得可操作：

- "确保服务启动在 800ms 内完成"
- "这四个关键用户路径没有 span 超过两秒"

> "We regularly see single Codex runs work on a single task for upwards of six hours (often while the humans are sleeping)."

这是 Harness Engineering 的另一个核心洞察：**当你把应用的内部状态变成 Agent 可读的数据，你就把「人工审批」变成了「结构化验证」**。

---

## 机械执行架构约束

OpenAI 团队的结论反直觉但正确：

> "This is the kind of architecture you usually postpone until you have hundreds of engineers. With coding agents, it's an early prerequisite."

为什么？因为**Agent 在严格边界和可预测结构的环境中效率最高**。这不是软道理，是硬约束。

### 具体做法

他们的应用围绕严格的架构模型构建：

- **每业务域固定分层**：Types → Config → Repo → Service → Runtime → UI，依赖方向严格验证
- **跨领域关注点（auth、connector、telemetry）** 通过单一显式接口（Providers）进入
- 自定义 linter（由 Codex 生成）强制执行这些规则
- 还有 taste invariants：静态强制的结构化日志、schema 命名规范、文件大小限制

> "Because the lints are custom, we write the error messages to inject remediation instructions into agent context."

这不是微管理，是**在边界处强制正确性，在边界内给予自由**。这与大型工程平台组织的运作方式相同：集中强制边界，本地允许自主。

最终产出不总是匹配人类审美偏好，但这没关系。**只要输出是正确的、可维护的、对未来 Agent 运行可读的，它就达到标准了。**

---

## 吞吐量改变 Merge 哲学

当 Codex 的吞吐量远超人类注意力，许多传统工程规范变得适得其反。

他们的仓库操作**最小化阻塞性 merge gate**：
- PR 生命周期短
- 测试 flakiness 通常通过后续运行解决，而非无限期阻塞进度
- 在 Agent 吞吐量远超人类注意力的系统里，修正成本低廉，**等待才是昂贵的**

这和传统软件工程的「质量第一」哲学背道而驰。OpenAI 的判断是：**当修正成本足够低，阻塞性 gate 的代价超过了它的价值**。

> "In a system where agent throughput far exceeds human attention, corrections are cheap, and waiting is expensive."

当然，这需要一个前提：**你的 Agent 输出质量已经足够高**。如果 Agent 的第一次正确率还在 60%，这个哲学会让你淹没在无效 PR 里。

---

## 工程机制对照：五维度 Harness 架构

结合 OpenAI Codex 的实验与之前积累的案例，可以梳理出一个五维度 Harness 架构全景：

| 维度 | 案例 | 核心机制 | 验证标准 | 时间尺度 |
|------|------|---------|---------|---------|
| **Evaluator Loop** | Sakana AI-Scientist | LLM Reviewer 评分自动循环 | 论文质量评分 | 天-周 |
| **接力/恢复** | peerd (78⭐) | git commit + 进度文件 + cross-session | 会话可恢复性 | 分钟-天 |
| **工作区状态管理** | Codex-maxxing | Git worktree + artifact + clean handover | PR 可合并率 | 小时-天 |
| **事件驱动** | Cursor Automations | 外部事件触发 + Computer Use | 业务价值交付 | 秒-天 |
| **人类监督** | Anthropic Auto Mode | 双层 Permission Classifier | 零越权操作 | 秒-分钟 |

OpenAI 的实验最清晰地揭示了**工作区状态管理**的必要性：当你的 Agent 运行 6 小时处理单一任务，**没有一个可靠的状态管理机制，一切都会在某个地方崩溃**。

---

## 笔者的判断

OpenAI 的实验给行业最重要的一个认知，不是「AI 可以写代码」，而是：

> **当 Agent 成为执行主体，工程师的核心竞争力从「自己能写好代码」变成「能设计出让 Agent 可靠工作的环境」**。

这意味着：模型能力每年翻倍，但环境设计能力取决于人类工程师的系统思维水平——这个能力不会自动增长。

对于正在构建 AI Coding 能力的团队，OpenAI 的实验指向了几个具体的工程杠杆：
1. **不要过度投资 prompt 优化，要投资环境可读性**（让 Agent 能直接查询应用状态）
2. **不要用文档约束 Agent，用机械 linter 强制边界**
3. **小步快跑，快速修正，比等待完美更好**——但这要求你的 Agent 输出正确率足够高

---

**引用来源**：
1. "We intentionally chose this constraint so that we would build what was necessary to increase engineering velocity by orders of magnitude." — [OpenAI](https://openai.com/index/harness-engineering/)
2. "Agents are most effective in environments with strict boundaries and predictable structure." — [OpenAI](https://openai.com/index/harness-engineering/)
3. "This enables progressive disclosure: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front." — [OpenAI](https://openai.com/index/harness-engineering/)
4. "Humans steer. Agents execute." — [OpenAI](https://openai.com/index/harness-engineering/)
5. "What capability is missing, and how do we make it both legible and enforceable for the agent?" — [OpenAI](https://openai.com/index/harness-engineering/)
