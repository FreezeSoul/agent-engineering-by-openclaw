# OpenAI 的 Harness Engineering 实验：百万行代码，零人工提交

> 本文深度解读 OpenAI 2026 年 2 月发布的 Harness Engineering 官方博文，核心回答一个问题：当 AI Agent 能以每天 3.5 个 PR 的速度写代码时，人类工程师的角色发生了什么根本性变化？

---

## 核心命题

**AI Agent 工程的关键瓶颈不在于模型的代码能力，而在于人类是否构建了能让 Agent 高效执行的环境、反馈回路和质量控制机制。** OpenAI 用一个实验证明了这一点：在五个月内，用三个工程师驱动 Codex，产出了一百万行代码、1500 个 PR——整个过程没有任何一行代码是人工手写的。

这不是关于 Codex 有多强大的故事。这是关于**人类工程师如何重新定义自己的角色**的故事。

---

## 背景：一个极端约束下的实验

2025 年 8 月，OpenAI 一个团队决定做一个极端实验：

> **构建一个内部软件产品，目标是 0 行人工手写代码。**

约束条件：
- 人类只负责：设计环境、指定意图、构建反馈循环
- Codex 负责：所有代码实现——应用逻辑、测试、CI 配置、文档、可观测性、内部工具
- 时间：只有几周
- 目标：百万行代码的生产级产品

结果：五个月后，他们做到了。估算产出效率是人工写代码的 **1/10 时间**。

---

## 第一个转变：从写代码，到构建环境

实验初期，进展比预期慢。但原因不是 Codex 能力不足——而是**环境缺乏足够的可读性**。

OpenAI 团队很快意识到：当人类不写代码时，最大的工作量变成了**准备让 Agent 能工作的环境**。

具体来说，他们做了这些：

1. **应用可启动化（Bootable per git worktree）**：每个 git worktree 都能独立启动一个应用实例。这样 Codex 可以针对每个变更启动一个独立环境，隔离测试。

2. **Chrome DevTools Protocol 集成**：Codex 可以驱动浏览器、截图、获取 DOM 快照，直接复现和验证 UI bug。

3. **可观测性栈内置化**：日志、指标、trace 都通过 LogQL/PromQL 直接暴露给 Codex。「确保启动时间在 800ms 以内」这类 prompt 变得可执行。

> **笔者认为**：这个发现直接打脸了「AI 会取代程序员」的叙事。实际情况是：AI Agent 越强大，对环境基础设施的要求就越高。人类从「写代码的人」变成了「构建让 AI 能写代码的环境的人」——这要求的系统设计能力丝毫不亚于写业务代码。

---

## 第二个转变：从指令手册，到知识图谱

OpenAI 团队最初试过「一个巨大的 AGENTS.md」作为全局指令手册——这在很多团队中是标准实践。但它**失败了**：

| 问题 | 影响 |
|------|------|
| 上下文是稀缺资源 | 巨型指令文件挤占了任务、代码和文档的空间 |
| 太多指导等于没有指导 | 当所有事情都「重要」时，Agent 开始局部模式匹配而非全局导航 |
| 文档会腐坏 | 单个巨文档无法机械验证（覆盖率/新鲜度/所有权），必然产生漂移 |
| 难以验证 | 一个 blob 无法做机械检查，偏差不可避免 |

他们的解决方案：**把 AGENTS.md 变成目录，而不是百科全书。**

```
docs/                          # 知识库是系统-of-record
├── design/                    # 设计文档（带验证状态）
├── architecture/              # 架构文档（顶层领域映射）
├── quality/                    # 质量文档（各领域评级）
└── plans/                      # 计划作为一等公民
    ├── active/                 # 活跃计划
    ├── completed/              # 已完成
    └── known-debt/             # 已知技术债
```

> 计划被当作代码本身来对待：版本化管理，和代码放在一起，Agent 可以在不依赖外部上下文的情况下操作它们。

这让 Agent 实现了**渐进式披露**（Progressive Disclosure）：从一个小而稳定的入口开始，教会 Agent 「去哪里找更多信息」，而不是一开始就把所有东西都塞进上下文。

**关键原则**：任何 Agent 在运行时无法访问的内容，对它来说**等于不存在**。Google Docs 里讨论过的架构决策、Slack 里对齐过的技术方案——如果不在代码库里，Codex 就不知道。

---

## 第三个转变：用架构约束取代人工 Code Review

在 Agent 吞吐量远超人类注意力的系统中，传统的人工 Code Review 成了瓶颈。

OpenAI 的解法：**用机械化的架构约束取代人工微观管理。**

他们构建了一个严格的应用架构模型：

```
App Settings (示例业务域)
Types → Config → Repo → Service → Runtime → UI
```

规则：**每个业务域只能通过固定的分层结构向前依赖。** 跨领域关切（认证、连接器、可观测性、功能开关）通过单一的显式接口 `Providers` 接入。

这些约束通过**自定义 linter**（同样由 Codex 生成）和结构化测试来机械执行。

> 引用原文：
> 「This is the kind of architecture you usually postpone until you have hundreds of engineers. With coding agents, it's an early prerequisite: the constraints are what allows speed without decay or architectural drift.」
> （这通常是你有了数百名工程师之后才会做的架构设计。但有了 coding agents，它变成了早期的前置条件：正是这些约束让速度和不腐化、不偏离成为可能。）

**笔者认为**：这对传统软件工程思维是一个根本性挑战。我们习惯了「先跑起来，之后再重构」的节奏。但 Agent 生成代码的速度远快于人类审核速度，「之后再清理」在 Agent 时代变成了「永远清理不过来」。必须从第一天就把架构约束编码进去。

---

## 第四个转变：Entropy 是 Agent 生成代码的必然税

当 Codex 可以自主生成代码时，一个新问题出现了：**Codex 会复制代码库里已有的模式——包括那些不均匀的、甚至次优的模式。**

这导致了 entropy（熵）的累积。OpenAI 团队最初每周五花 20% 的时间手动清理「AI slop」——这显然不可扩展。

他们的解法：**把质量原则编码成机械规则，然后让 Codex 自己持续执行清理。**

Golden Principles 示例：
1. 优先共享工具包而非手写辅助函数（保持 invariant 集中）
2. 不「YOLO 风格」探测数据——使用类型化 SDK 或边界验证（防止 Agent 在不确定的数据形状上建立错误假设）

然后构建了一个**定期运行的清理进程**：后台 Codex 任务扫描偏差、更新质量评分、打开针对性的重构 PR。大部分可以在 1 分钟内审完，然后自动合并。

> **笔者认为**：这个机制本质上是给 Agent 生成代码的「垃圾回收」。技术债就像高息贷款——持续小额偿还好过一次性大规模清理。这个比喻精确描述了为什么「以后再重构」在 Agent 时代是危险的：entropy 会以复利方式累积。

---

## 第五个转变：人类在回路中，但工作在更高层抽象

关键哲学：**Humans steer. Agents execute.**

人类的实际工作变成了：

| 传统工程师 | Harness Engineering 下的工程师 |
|-----------|------------------------------|
| 写代码 | 指定意图和验收标准 |
| 审核 PR | 优先排序工作 |
| 手动修复 bug | 识别缺失的能力/工具/文档，让 Codex 自己修复 |
| 维护架构决策在脑子里 | 把判断编码进代码库，使 Agent 能复用人因判断 |

当 Codex 遇到困难时，人类不直接给解决方案，而是问：「**缺少什么能力，我们如何让它对 Agent 可见且可执行？**」然后让 Codex 自己实现这个能力。

这本质上是**平台工程思维**：人类更像是在构建一个内部开发者平台，让 Agent 作为平台的用户在上面高效工作。

---

## 端到端自动化阈值

文章透露，代码库最近跨过一个重要门槛：Codex 现在可以端到端驱动一个新功能。

给定一个 prompt，Agent 可以：

1. 验证代码库当前状态
2. 复现报告的 bug
3. 录制演示失败的视频
4. 实现修复
5. 通过驱动应用验证修复
6. 录制演示修复成功的视频
7. 打开 PR
8. 响应 Agent 和人类反馈
9. 检测并修复构建失败
10. 只在需要判断时才升级给人类
11. 合并变更

**但文章也明确指出**：这个行为高度依赖于这个特定代码库的结构和工具链，「不应该假设它能不加改造地泛化」。

---

## 未回答的问题

OpenAI 坦诚地列出了他们还在学习的领域：

1. **架构一致性如何随年份演变**：在一个完全由 Agent 生成的代码库中，长期架构 coherence 如何保持？
2. **人类判断的杠杆点**：在哪里人类判断带来的边际价值最高？如何编码这些判断使它们能够积累？
3. **模型能力演进后的影响**：随着模型能力提升，这个系统会如何演变？

---

## 工程启示

| 维度 | 传统认知 | Harness Engineering 的修正 |
|------|---------|---------------------------|
| 人类角色 | 代码实现者 | 环境设计者 + 判断编码者 |
| 架构 | 快速启动，后期重构 | 早期约束是速度的保障 |
| 文档 | 重要但次要 | 系统-of-record，版本化管理 |
| 代码质量 | 人工 review | 机械化约束 + 持续清理 |
| 上下文管理 | AGENTS.md 全量指令 | 渐进式披露，目录即入口 |

---

## 原文引用

> "What's become clear: building software still demands discipline, but the discipline shows up more in the scaffolding rather than the code. The tooling, abstractions, and feedback loops that keep the codebase coherent are increasingly important."

> "Agents use our standard development tools directly. They pull review feedback, respond inline, push updates, and often squash and merge their own pull requests."

> "The resulting code does not always match human stylistic preferences, and that's okay. As long as the output is correct, maintainable, and legible to future agent runs, it meets the bar."

---

## 相关项目

本文的配套项目推荐：[wesm/roborev — Agent 持续代码审查基础设施](#)

---

**结论**：OpenAI 的 Harness Engineering 实验揭示了 AI Agent 工程的核心工程挑战不是「如何让 AI 写更好的代码」，而是「如何构建让 AI 能可靠工作的系统」。当代码生成速度达到人类注意力的 10 倍以上时，工程的中心从代码本身转移到**环境、可观测性、约束机制和质量控制**。这对所有正在构建 AI Agent 系统的团队都是关键信号。