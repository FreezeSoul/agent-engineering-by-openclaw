# revfactory/harness：L3 Meta-Factory 的 Team-Architecture Factory

> 当其他 Harness 在解决「如何让单个 Agent 更好地工作」时，Harness 在解决一个更上层的问题：如何让整个 Agent Team 的架构本身就对。

**核心命题**

revfactory/harness 是 Claude Code 生态里少数几个把自己定位在 **L3 Meta-Factory 层** 的工具——它不是一个具体的 Harness，而是一个**生成 Harness 的工厂**。用户说「Build a harness for this project」，它就把领域描述转成 Agent Team + Skills，从 6 种预定义架构模式里选一个匹配的执行。

---

## 一、问题：大多数 Harness 解决的是执行层，不是架构层

在 Claude Code 生态里，Harness 是个被用烂的词。从 L1 的基础执行层到 L4 的自适应层，每个层级都叫 Harness。但真正的问题是：**当你需要构建一个复杂任务的多 Agent 协作时，最大的困难不是「怎么让每个 Agent 更好地工作」，而是「整个 Agent Team 的架构应该怎么设计」**。

Harness 解决了前者。Harness（revfactory）解决了后者。

它的核心思路是：把「Team Architecture Design」本身变成一个可复用的工作流。你不需要从零设计每个 Agent 的职责、他们之间的通信协议、以及任务如何分解——Harness 把这个过程自动化了。

---

## 二、核心技术：6 种团队架构模式

Harness 预置了 6 种经过验证的多 Agent 协作模式，这是它最有价值的资产：

| 模式 | 适用场景 | 核心机制 |
|------|---------|---------|
| **Pipeline** | 顺序依赖的任务链 | 前一个 Agent 的输出是下一个的输入 |
| **Fan-out/Fan-in** | 并行独立任务 + 结果聚合 | 多个 Agent 同时处理子任务，最后汇总 |
| **Expert Pool** | 上下文相关的选择性调用 | 根据任务类型动态选择最合适的 Agent |
| **Producer-Reviewer** | 生成 + 质量审查循环 | 生成 Agent 产出 → 审查 Agent 评分 → 不合格打回重做 |
| **Supervisor** | 中央调度 + 动态任务分发 | 中央 Agent 负责任务分配和结果协调 |
| **Hierarchical Delegation** | 递归委托的层级结构 | 顶层 Agent 分解任务，委托给子 Agent，子 Agent 继续分解 |

这 6 个模式不是随意拼凑的。每一个都对应实际工程中的高频场景。比如 Producer-Reviewer 模式和 Anthropic 那篇 GAN-inspired three-agent architecture（planner/generator/evaluator）高度一致——都是「生成」和「评价」分离，避免 Agent 自评失真。

---

## 三、工作流：6 个阶段的自动生成

Harness 的执行流程是一个 6 阶段的流水线：

```
Phase 1: Domain Analysis（领域分析）
Phase 2: Team Architecture Design（选哪种模式）
Phase 3: Agent Definition Generation（生成 .claude/agents/*.md）
Phase 4: Skill Generation（生成 .claude/skills/）
Phase 5: Integration & Orchestration（Agent 间如何通信）
Phase 6: Validation & Testing（触发验证 + 干跑测试）
```

输出物是 Claude Code 原生的 `.claude/agents/` 和 `.claude/skills/` 文件——不是专有格式，而是 Claude Code 自身的设计。这保证了生成的架构可以直接在 Claude Code 里运行，不需要额外的运行时。

---

## 四、生态定位：L3 Meta-Factory 里的 Team-Architecture Factory

Harness 的 README 给自己的定位非常清晰，在生态里划了一条很准的线：

| 层级 | 定位 | 代表项目 |
|------|------|---------|
| L3 — Meta-Factory / **Team-Architecture Factory** | **Harness（我们）** | revfactory/harness |
| L3 — Meta-Factory / Runtime-Configuration Factory | 确定性运行时配置 | coleam00/Archon |
| L3 — Meta-Factory / Codex Runtime Port | 同一概念，Codex 版本 | SaehwanPark/meta-harness |
| L2 — Cross-Harness Workflow | 跨 Harness 的标准化 | affaan-m/ECC |
| L4 — Adaptive | 自适应/自优化 | — |

ECC（Everything Claude Code）是 L2 层的 Cross-Harness Workflow，代表跨多个 Harness 的标准化技能和规则共享。Harness 是 L3 的 Team-Architecture Factory，代表从领域描述自动生成 Agent Team 结构。两者是互补的：ECC 解决「多个 Harness 怎么统一」，Harness 解决「一个 Harness 的 Team 架构怎么生成」。

---

## 五、和同类项目的区别

**vs. 固定 Agent Team 方案**：大多数 Agent Team 方案要求你预先定义好每个 Agent 的职责和通信方式。Harness 让这个过程变成了一个可配置的生成流程。

**vs. 单一 Agent 框架（LangChain/CrewAI）**：那些框架关注的是「如何让单个 Agent 能力更强」，Harness 关注的是「如何让 Agent Team 的结构本身更合理」。

**vs. 其他 Claude Code Harness 项目**：大多数 Claude Code 插件是 L1-L2 层的实现（特定场景的 Harness），Harness 是 L3 层的生成器（生成其他 Harness 所用的架构）。

---

## 六、实战：触发方式

安装后，在 Claude Code 里直接说：

```
Build a harness for this project
Design an agent team for this domain
```

支持三种语言的触发指令（英文、韩文、日文），以及两种执行模式：**Agent Teams**（使用 Claude Code 原生 TeamCreate + SendMessage + TaskCreate）和 **Subagents**（直接 Agent 工具调用）。

---

## 七、笔者的判断

Harness 的价值不在于它生成的东西有多完美——生成的 Agent 定义和 Skills 肯定需要人工调优。它的价值在于**把「Team Architecture Design」从专家级手工活变成了可配置的自动化流程**。

对于一个需要构建复杂 Agent 协作系统的团队来说，最大的成本往往不是「如何让每个 Agent 更好地工作」，而是「我们到底应该用哪种架构，Pipeline 还是 Producer-Reviewer，每个 Agent 的职责怎么划定」。Harness 把这个问题变成一个结构化的决策流程，加上 6 个经过验证的预置模式作为选项。

**适用场景**：需要构建多 Agent 协作系统，且希望用 Claude Code 原生格式管理 Agent 定义和 Skills 的团队。

**不适用场景**：只需要单个 Agent 完成简单任务；或者已经有一套成熟的自定义多 Agent 框架。

> 真正的问题是：当你需要在同一个项目里协调 3 个以上的 Agent 时，最大的瓶颈不是「每个 Agent 的能力」，而是「整个 Team 的架构设计」。Harness 解决的是瓶颈，不是细节。

---

## 附录：项目信息

| 项目 | 信息 |
|------|------|
| **Stars** | 4,202 |
| **语言** | Claude Code Plugin + Markdown |
| **定位** | L3 Meta-Factory / Team-Architecture Factory |
| **安装方式** | `/plugin marketplace add revfactory/harness` + `/plugin install harness@harness-marketplace` |
| **输出格式** | Claude Code 原生 `.claude/agents/` 和 `.claude/skills/` |
| **License** | Apache 2.0 |
| **官方文档** | [GitHub](https://github.com/revfactory/harness) · [Star History](https://star-history.com/#revfactory/harness) |

---

*推荐关联阅读*：
- [Anthropic GAN-inspired three-agent architecture](https://www.anthropic.com/engineering/harness-design-long-running-apps)（Producer-Generator-Evaluator 三角色与 Harness 的 Producer-Reviewer 模式同构）
- [Anthropic Claude Code Agent Teams](https://docs.claude.com/claude-code/agent-teams)（Claude Code 原生 Agent Teams 机制，Harness 的执行目标）