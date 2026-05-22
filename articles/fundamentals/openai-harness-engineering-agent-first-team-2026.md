# OpenAI Harness Engineering：把 Codex 变成「自动驾驶」开发团队

> **核心命题**：OpenAI 用五个月证明，当代码全部由 Agent 生成时，工程团队的核心工作不再是写代码，而是**设计环境、定义意图、构建反馈循环**。

---

## 一、背景：零行手写代码的产品

2025 年 8 月底，OpenAI 一个团队在空 git 仓库种下了第一个 commit。五个月后，这个仓库包含了约 **100 万行代码**，横跨应用逻辑、基础设施、工具链、文档和内部开发工具。期间约 **1500 个 PR** 被合并，而整个团队只有 **3 名工程师** 驱动 Codex 工作——人均 3.5 个 PR/天，且随团队规模增长（现 7 人）吞吐量还在上升。

这不是概念验证。这个产品有**数百名内部用户**，包括每日使用的高频用户，并在持续部署、故障和修复的循环中运行着。

关键是：人类从未直接贡献过任何一行代码。他们只负责**设计系统而非实现它**。

---

## 二、重新定义工程师的角色

最初进展比预期慢，不是因为 Codex 能力不足，而是因为**环境定义不足**。Agent 缺乏实现高级目标所需的工具、抽象和内部结构。

于是工程师做了一件反直觉的事：他们不再写代码，而是帮 Codex 构建工作条件。

**深度优先的工作方式**：
- 将大目标分解为更小的构建块（设计、代码、审查、测试等）
- 引导 Agent 构建这些构建块，然后用它们解锁更复杂的任务
- 当某事失败时，修复方案几乎永远不是「再试一次」，而是「缺少什么能力？如何让它既清晰又可执行？」

> 原文："The primary job of our engineering team became enabling the agents to do useful work."

---

## 三、提升应用可读性：让 Codex 能「看到」系统

随着代码吞吐量增加，人工 QA 成为瓶颈。为最大化人类时间和注意力的利用效率，OpenAI 选择让**更多能力直接赋予 Codex**。

### 3.1 让 UI、日志和指标对 Codex 可直接访问

**关键工程决策**：

- **per-git-worktree 应用启动**：每个变更对应一个独立可启动的实例，Codex 可以针对每个变更启动一个实例进行测试
- **Chrome DevTools Protocol 集成**：Agent 运行时通过 CDP 直接操作浏览器，能**复现 bug、验证修复、推理 UI 行为**
- **可观测性栈暴露给 Codex**：日志、指标、trace 通过本地可观测性栈暴露，Codex 可用 **LogQL 查日志**、**PromQL 查指标**

这使得「确保服务启动在 800ms 内完成」或「这四个关键用户路径中没有任何 span 超过 2 秒」这类 prompt 变得可执行。

> 原文："Agents work on a fully isolated version of that app—including its logs and metrics, which get torn down once that task is complete."

---

## 四、知识管理：给 Codex 一张地图，而非 1000 页手册

Context 管理是让 Agent 有效处理大型复杂任务的最大挑战之一。OpenAI 的早期教训很简单：**给 Codex 一张地图，而非一份使用手册**。

### 4.1 「AGENTS.md 作为目录」的方法

他们尝试过「一大份 AGENTS.md」的方法，失败在意料之中：

| 问题 | 影响 |
|------|------|
| Context 是稀缺资源 | 巨大指令文件挤占了任务、代码和相关文档 |
| 过度指导等于无指导 | 当一切都是「重要」时，什么都不重要了 |
| 知识立刻过时 | 单一手册变成过时规则的坟墓，Agent 无法判断哪些仍有效 |
| 难以验证 | 单个 blob 不利于机械检查（覆盖度/新鲜度/所有权） |

**解决方案**：将 AGENTS.md 作为**目录**，而非百科全书。仓库的知识库存在于结构化的 `docs/` 目录：

```
1AGENTS.md
2ARCHITECTURE.md
3docs/
4├── design-docs/
5│ ├── index.md
6│ ├── core-beliefs.md
7│ └── ...
8├── exec-plans/
9│ ├── active/
10│ ├── completed/
11│ └── tech-debt-tracker.md
12├── generated/
13│ └── db-schema.md
14├── product-specs/
15│ ├── index.md
16│ ├── new-user-onboarding.md
17│ └── ...
18├── references/
19│ ├── design-system-reference-llms.txt
20│ ├── nixpacks-llms.txt
21│ ├── uv-llms.txt
22│ └── ...
23├── DESIGN.md
24├── FRONTEND.md
25├── PLANS.md
26├── PRODUCT_SENSE.md
27├── QUALITY_SCORE.md
28├── RELIABILITY.md
29└── SECURITY.md
```

### 4.2 机械执行的规则

- **专用 linter**：验证知识库处于最新状态、正确交叉链接、结构正确
- **CI 任务**：持续验证文档覆盖度和新鲜度
- **doc-gardening agent**：扫描过时或不再反映真实代码行为的文档，并主动开 PR 修复

---

## 五、强化架构与品味：约束即加速

仅靠文档无法保持全 Agent 生成代码库的协调。OpenAI 的做法是**强制执行不变量，而非微观管理实现**。

### 5.1 严格的架构边界

每个业务域被划分为固定层级集合，依赖方向被严格验证，允许的边有限。这些约束通过**自定义 linter 和结构测试**机械执行。

**分层架构规则**（每个业务域内）：
```
Types → Config → Repo → Service → Runtime → UI
```
跨领域关注点（认证、连接器、遥测、功能开关）通过单一明确接口 **Providers** 引入。

### 5.2 Agent 最有效的环境

> 原文："Agents are most effective in environments with strict boundaries and predictable structure."

在人类优先的工作流中，这些规则可能显得迂腐或限制性。但在 Agent 场景中，它们成为**乘数**：一旦编码，就在各处同时生效。

这本质上是在模拟大型工程平台组织的运作方式：**集中执行边界，本地允许自主**。

---

## 六、本轮关联：与 OpenAI Codex 文章的互补闭环

本文（OpenAI Harness Engineering）与上一轮产出的「OpenAI Codex：25小时自主运行，代码Agent进入「自动驾驶」时代」形成**执行可靠性闭环**：

- **上轮 Article**：Codex 25小时无中断运行的核心——Plan→Validate→Repair 循环、Git Worktrees、Runbook
- **本轮 Article**：当代码全部由 Agent 生成时，人类工程团队如何转型为「环境设计师」——知识管理、架构强化、反馈循环构建

两者共同揭示了一个核心命题：**Agent 时代的工程团队价值，不在于写出多少代码，而在于构建了多少让 Agent 高效工作的结构和系统**。

---

## 七、工程启示录

1. **人类时间是最稀缺的资源**：所有工程决策都应围绕最大化人类注意力的杠杆展开
2. **环境即产品**：对 Agent 可读性的投资，直接转化为吞吐量的提升
3. **约束是乘数**：早期架构投资对 Agent 生成代码库的重要性远超传统开发
4. **知识即系统**：文档的价值不在于记录，而在于能被 Agent 有效利用

> 原文："Humans steer. Agents execute."

---

**引用来源**：
- [Harness engineering: leveraging Codex in an agent-first world | OpenAI Engineering Blog](https://openai.com/index/harness-engineering/)（2026 年 2 月 11 日）