# OpenAI Harness Engineering：代码生成的代码生成

> **核心论点**：Harness engineering 不是安全防护，而是一套让 Agent 工作从「不可控」变成「可追踪」的控制层设计。OpenAI 用 Codex 五个月内生成百万行代码的实验揭示了一个反直觉的事实：当 Agent 成为主要生产力时，软件工程的纪律不是消失了，而是从「写代码」转移到了「搭环境、建反馈循环、编码知识」——这些工作本质上是在为 Agent 设计一个可推理的工作空间。

## 背景：一场五个月的极限实验

2025 年 8 月，OpenAI 一个三人工程师团队开始了一个实验：**从零行手写代码开始，用 Codex 构建一个内部产品**。没有祖传代码，没有 human-in-the-loop 的代码审查，只有 Codex 和一套精心设计的控制环境。

五个月后：
- 约 **100 万行代码**，涵盖产品逻辑、基础设施、工具、文档
- **1500 个 PR** 合并，人均日吞吐量 **3.5 PRs/工程师**
- 产品已有**数百名内部日常用户**
- 人类工程师的代码贡献：**0 行**

OpenAI 将这个约束称为 "no manually-written code"——这不是秀肌肉，而是一个刻意设计的边界条件，迫使团队把所有精力投入到一个过去从未被认真思考过的问题：**当人类不再写代码时，工程工作的本质是什么？**

## 核心洞察：Agent 需要的是「可推理性」，不是「更多信息」

### AGENTS.md 的失败

实验早期，团队首先尝试了当时最流行的做法：一个庞大的 AGENTS.md 文件，列出所有规则、约定、架构决策。

这个方案以可预测的方式失败了：

> "Context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant docs—so the agent either misses key constraints or starts optimizing for the wrong ones."

> "Too much guidance becomes non-guidance. When everything is 'important,' nothing is."

> "It rots instantly. A monolithic manual turns into a graveyard of stale rules."

这三个失败模式揭示了一个根本性的问题：**给 Agent 更多上下文 ≠ 让 Agent 更好地工作**。当信息密度超过 Agent 的处理能力时，重要信息反而被稀释了。

### 解决方案：AGENTS.md 作为目录，docs/ 作为系统

OpenAI 的核心转变是将知识管理从「指令型」改为「结构型」：

- **AGENTS.md**：仅约 100 行，作为地图（table of contents），指向更深层的知识来源
- **docs/**：结构化的知识库，作为系统的事实来源（system of record）
  - 设计文档带索引和验证状态
  - 架构文档（ARCHITECTURE.md）提供顶层包结构和领域划分
  - **Plans 作为一等公民**：短期计划用轻量 ephemeral plans，长期工作用 execution plans（含进度和决策日志，checkin 到仓库）
  - 质量文档对每个产品域和架构层打分，持续追踪差距

这本质上是一种**渐进式披露（progressive disclosure）**策略：Agent 从一个小型、稳定、可信的入口开始，在需要时主动查询更深的上下文，而不是在启动时就被海量信息淹没。

**OpenAI 原文**：

> "Plans are treated as first-class artifacts... Active plans, completed plans, and known technical debt are all versioned and co-located, allowing agents to operate without relying on external context."

## 应用层可读性：让 Agent 能直接操作自己的工作对象

### 传统方案的盲区

大多数 Agent 开发框架关注的是「如何让 Agent 更好地理解代码」，而 OpenAI 关注的是「如何让代码本身对 Agent 可操作」——这两个问题的答案完全不同。

传统思路是扩大 Context Window，或者改进 RAG 检索。OpenAI 的思路是：**让应用程序本身对 Agent 可直接运行和观测**。

### 三个关键工程决策

**1. Git worktree 隔离**：每个变更对应一个独立的 git worktree，Codex 可以在完全隔离的环境中启动和驱动应用程序实例。这意味着 Agent 不是在静态代码上工作，而是在一个真实的、运行中的实例上工作。

**2. Chrome DevTools Protocol 集成**：Agent 可以直接操作 DOM snapshots、截图、页面导航来复现 bug、验证修复、推理 UI 行为。这意味着测试不再是「运行 pytest」，而是可以真实地观察用户面对的界面。

**3. Ephemeral observability stack**：日志、指标、traces 都对 Codex 可见，且每个 worktree 有独立的临时可观测性栈。这意味着 Agent 可以直接用 PromQL 查询「确保服务启动在 800ms 内完成」这样的具体目标。

**OpenAI 原文**：

> "We regularly see single Codex runs work on a single task for upwards of six hours (often while the humans are sleeping)."

这六个小时的连续工作能力，不是靠更大的 Context Window，而是靠让应用程序本身对 Agent 可操作、可观测。

## 架构即约束：让 Agent 在边界内自由

### 一个反直觉的发现

通常我们在代码量较小、团队较小时不会投入太多精力做架构设计——架构是「等你有足够多工程师时才值得做的事」。OpenAI 的发现是：**对于 Agent-first 开发，这恰恰相反**。

> "Agents are most effective in environments with strict boundaries and predictable structure"

Agent 不是在「聪明地处理混乱」，而是在「高效地执行约束内的任务」。没有边界的 Agent 会把精力浪费在处理不一致性上，而不是真正的工作上。

### 分层架构强制执行

OpenAI 设计了一个严格的分层架构模型：**每个业务域只允许单向依赖固定的层序列**（Types → Config → Repo → Service → Runtime → UI），跨领域关注点（认证、连接器、可观测性）通过单一明确的 Providers 接口注入。

关键在于：**这些约束是机械强制执行的，不是靠文档约定**。自定义 linter（由 Codex 生成）和结构性测试会在 PR 阶段就拦截违规的依赖关系，而不是等到代码腐烂后才处理。

**OpenAI 原文**：

> "Once encoded, they apply everywhere at once."

> "This is the kind of architecture you usually postpone until you have hundreds of engineers. With coding agents, it's an early prerequisite: the constraints are what allows speed without decay or architectural drift."

### Taste invariants：从「人工审查」到「代码强制」

除了架构边界，OpenAI 还定义了一套 "taste invariants"——通过静态检查强制执行：
- 结构化日志格式
- Schema 和类型的命名规范
- 文件大小限制
- 平台特定的可靠性要求

这些 taste invariants 的关键设计在于：**linter 的错误信息中直接注入修复指令**，让 Agent 在看到错误时就能获得修复指导，而不是需要额外的上下文。

## 架构漂移的垃圾回收：持续小步清理

### Agent 生成的熵增问题

当 Agent 可以自主生成代码时，一个新问题随之出现：**Codex 会复制仓库中已有的模式——包括不均匀的、有问题的模式**。随着时间推移，熵增是不可避免的。

传统方案是周期性大扫除。OpenAI 最初也是这样——每周五花 20% 的时间清理「AI slop」。但这不可扩展。

### Golden principles + 自动巡检

OpenAI 的解决方案是将 taste 编码为机械规则，建立定期的清理流程：

1. **Golden principles**：Opinionated、机械性的规则，例如：
   - 优先使用共享工具包而不是手写 helpers（保持 invariant 集中）
   - 不做 "YOLO-style" 数据探测——在边界验证或使用类型化 SDK（防止 Agent 建立在猜测的数据结构上）

2. **Recurring cleanup agent**：后台任务定期扫描偏离情况，更新质量评分，打开针对性的重构 PR。单个 PR 审查时间通常不到一分钟，大多数可以自动合并。

**OpenAI 原文**：

> "Technical debt is like a high-interest loan: it's almost always better to pay it down continuously in small increments than to let it compound and tackle it in painful bursts."

这本质上是一个**持续运行的垃圾回收机制**：技术债务不会累积到需要「停机大扫除」的程度，而是每天都被小步清理。

## Agent 自主能力的临界点

当足够多的开发循环（测试、验证、review、反馈处理、恢复）被编码到系统中时，Codex 跨越了一个有意义的临界点：**可以端到端驱动一个新功能**。

给定一个 prompt，Agent 现在可以：

1. 验证代码库当前状态
2. 复现报告的 bug
3. 录制演示失败过程的视频
4. 实现修复
5. 通过驱动应用程序验证修复
6. 录制演示修复成功的视频
7. 打开 PR
8. 响应 Agent 和人类反馈
9. 检测并修复构建失败
10. 仅在需要判断时才升级给人类
11. 合并变更

OpenAI 特别指出：**这个行为依赖于这个仓库特定的结构和工具配置**，不应该被假设为可以泛化。但这个临界点的存在本身已经说明了问题。

## 方法论沉淀：Harness 的本质

### Harness ≠ 安全防护

这篇博客最重要的贡献，可能不是任何一个具体工程决策，而是一个概念澄清：**harness engineering 不是安全防护（guardrails）的同义词**。

安全防护是 harness 的一部分，但不是全部。Harness engineering 是：

1. **环境设计**：让 Agent 有一个可操作、可观测的工作空间
2. **知识结构化**：让 Agent 有一个可信、可查询的知识来源（不是指令的堆砌）
3. **反馈循环编码**：让 Agent 的输出能被自动验证，错误能被自动捕获和修复
4. **约束系统**：通过架构边界和 taste invariants 让 Agent 的行为空间可预期
5. **持续清理机制**：让技术债务不会随时间累积到失控的程度

### 工程师角色的重新定义

当 Agent 执行，人类工程师做什么？

OpenAI 的答案是：

> "When something failed, the fix was almost never 'try harder.' Because the only way to make progress was to get Codex to do the work, human engineers always stepped into the task and asked: 'what capability is missing, and how do we make it both legible and enforceable for the agent?'"

这不是一个「减少工程师」的叙事，而是一个「工程师做什么」的重定义：**从写代码变成了搭环境、建反馈循环、编码知识**。这是软件工程中从未被正式命名过的一种工作，而 OpenAI 给了它一个名字：**harness engineering**。

## 适用边界

这个方法论有明确的适用边界：

- **Codex 级别的自主能力**：实验中的 Agent 可以 6 小时连续工作，端到端驱动功能。这需要相当强的模型能力和工具集成深度
- **结构化知识积累**：需要团队愿意投入时间建立 docs/ 知识库、execution plans 习惯、golden principles 编码。这不是一次性工作，而是持续投入
- **小团队约束**：OpenAI 用 3 人团队驱动整个仓库，是因为 Agent 吞吐量远超人类注意力。小团队不是先决条件，但「人类注意力是稀缺资源」是方法论的核心假设

对于小规模原型或实验性项目，这个框架的投入可能过重。但对于需要 Agent 处理复杂、长程任务的场景，这套 harness engineering 方法论提供了一套可操作的起点。

## 结语

**OpenAI 原文**：

> "Building software still demands discipline, but the discipline shows up more in the scaffolding rather than the code."

当代码生成不再是瓶颈时，**环境的可推理性**、**约束的清晰性**、**反馈的及时性**就成了决定性因素。Harness engineering 回答的正是在 Agent-first 世界中，软件工程纪律如何重新分配的问题。

---
**参考来源**：
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/) — OpenAI Engineering Blog, February 11, 2026
- [agents.md](https://agents.md/) — Agent development guidelines standard
- [Execution Plans](https://cookbook.openai.com/articles/codex_exec_plans) — OpenAI Cookbook
- [Architecture documentation philosophy](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) — by Alex Klokus
- [Parse, don't validate](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/) — by Alexis King