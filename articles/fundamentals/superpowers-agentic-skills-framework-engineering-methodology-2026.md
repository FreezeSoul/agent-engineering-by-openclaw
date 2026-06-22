# Superpowers：让 Coding Agent 遵循工程方法论的技能框架

**发布于**：2026-06-22 | **演进阶段**：Stage 10 · Skill | **分类**：fundamentals/

## 开篇

一个 coding agent 拿到需求后立即开始写代码，和一个先问"你要解决什么问题"再制定计划最后才动手的 agent，你更愿意把代码审查权交给哪个？

答案不言而喻。但问题是：**大多数 agent 默认的行为模式是前者**。

Superpowers 试图解决这个问题。它不是一个"更智能的 agent"——而是一套**让 agent 遵循软件工程方法论的技能系统**。它的核心理念是：与其教 agent 更多技能，不如让 agent 在动笔之前先搞清楚要写什么、为什么要这样写、如何验证写得对不对。

这不是一个工具，而是一种**工程文化的强制执行机制**。

---

## 一、问题：Agent 为何总是跳过思考直接动手？

笔者见过太多这样的情况：给 agent 一个"帮我写一个用户登录模块"的需求，它立刻开始写 User 模型、LoginController、AuthService——然后花两倍的时间修 bug、删掉重写、或者发现自己理解错了需求。

这不是 agent 笨。这是**激励机制的问题**。

Agent 的默认目标是"产生代码"——它被优化为尽快产出可工作的代码，而不是先产出正确的理解。两者在prompt层面没有明确的区分，agent 自然选择更容易的路径。

传统解决方案是写更长的 system prompt，反复强调"先理解需求再动手"。但这种方法有几个根本缺陷：

1. **Prompt 不具备强制力**：Agent 可以跳过，可以忽略，可以在压力下放弃
2. **难以维护**：随着规则增加，prompt 变得越来越长，最终没人看得懂
3. **不同 agent 行为不一致**：同一个 prompt 在 Claude Code 和 Cursor 里的行为可能不同

Superpowers 选择了不同的路径：**把工程规则编码为技能（Skills），让 agent 在正确的时机自动触发正确的技能**。

---

## 二、Superpowers 的核心架构：技能系统

Superpowers 的核心是一套**可组合的技能系统**。每个技能（Skill）是一个包含触发条件、工作流程和验收标准的 markdown 文件，它告诉 agent：**在这个阶段，你应该做什么、怎么做、如何验证做对了**。

根据官方文档，Superpowers 目前包含 14 个核心技能，涵盖了软件开发的完整生命周期：

```
Spec → Plan → TDD → Implementation → Review → Deploy
```

这不是一个线性的流水线，而是一套**可组合的技能模块**。Agent 可以根据任务性质选择启用哪些技能、以什么顺序组合它们。

### 2.1 技能触发机制

Superpowers 的技能是**自动触发**的。当 agent 检测到特定的上下文信号时，对应的技能自动激活，不需要人工干预。

官方文档这样描述：

> "As soon as it sees that you're building something, it *doesn't* just jump into trying to write code. Instead, it steps back and asks you what you're really trying to do."

这个"step back"的行为不是靠一次性的 prompt 实现的，而是靠**技能系统在每个关键时刻的持续引导**。

### 2.2 Subagent 驱动开发

Superpowers 引入了一个有趣的概念：**subagent-driven development**。当 agent 需要处理复杂任务时，它会：

1. 将任务分解为多个子任务
2. 为每个子任务启动一个 subagent
3. 监督 subagent 的工作质量和进度
4. 在必要时进行 review 和调整

官方文档这样描述：

> "It's not uncommon for your agent to work autonomously for a couple hours at a time without deviating from the plan you put together."

这是 Superpowers 与普通 agent 最大的区别：**它不是在帮你写代码，它是在帮你管理一个开发团队**。

---

## 三、多 Agent 框架兼容性：不是独占，是泛化

Superpowers 最令人印象深刻的设计决策是**跨框架兼容性**。

它不是一个只服务于 Claude Code 的插件。官方数据显示，Superpowers 可以在以下环境中工作：

| 框架 | 安装方式 |
|------|---------|
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| OpenAI Codex App | 官方插件市场 |
| OpenAI Codex CLI | `/plugins` → 搜索安装 |
| Cursor | `/add-plugin superpowers` |
| GitHub Copilot CLI | `copilot plugin install superpowers@superpowers-marketplace` |
| Gemini CLI | `gemini extensions install` |
| Factory Droid | `droid plugin install` |
| Antigravity | `agy plugin install` |
| Kimi Code | 官方插件市场 |
| OpenCode | 自定义安装脚本 |
| Pi | `pi install git:github.com/obra/superpowers` |

这是 11 个不同的 coding agent 框架，Superpowers 为每一个都提供了兼容方案。

**这意味着什么？**

笔者认为，这意味着 Superpowers 团队从一开始就没有把自己定位为"Claude Code 的插件"。他们定义的是**一套技能规范**，任何愿意遵循这套规范的 agent 框架都可以接入。

这与 MCP 协议的设计思路有异曲同工之妙——都是在建立开放的标准，让用户不被单一平台绑定。

---

## 四、TDD 作为默认开发模式

Superpowers 强制要求采用 **TDD（测试驱动开发）** 作为默认开发模式。这在当前的 AI coding 工具中是极为罕见的设计决策。

大多数 coding agent 的默认行为是：
1. 理解需求
2. 写代码
3. （可能）运行测试验证

Superpowers 的行为模式是：
1. 理解需求
2. **写测试用例**（Red）
3. **写最小代码让测试通过**（Green）
4. **重构**（Refactor）
5. 重复

官方文档明确强调：

> "It emphasizes true red/green TDD, YAGNI (You Aren't Gonna Need It), and DRY."

这三个原则——TDD、YAGNI、DRY——是软件工程中最基础但也最难坚持的原则。Superpowers 试图通过**技能系统的强制执行**让 agent 也遵循它们。

### 4.1 为什么 TDD 对 Agent 特别重要

笔者认为，TDD 对 coding agent 的价值比对人更大，原因有以下几点：

1. **Agent 的输出更容易验证**：测试用例是明确的成功/失败标准，不像代码审查依赖主观判断
2. **防止"看起来对了但实际错了"**：Agent 经常生成看起来正确但实际有边界 bug 的代码，TDD 可以早发现
3. **提供安全边际**：当 agent 重构或添加新功能时，测试是回归测试的唯一可靠保障

---

## 五、与 Cursor 的方法论对比

笔者之前写过 [Cursor 的四个工程教训](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/fundamentals/cursor-cloud-agent-four-engineering-lessons-2026.md)，其中提到了 Cursor 通过基础设施层面的能力增强（云端执行环境、PR 测试、自动修复）来解决 agent 的工程可信度问题。

Superpowers 走了另一条路：**它不增强 agent 的执行能力，而是约束 agent 的行为模式**。

| 维度 | Cursor | Superpowers |
|------|--------|-------------|
| **解决问题的思路** | 给 agent 更好的工具 | 强制 agent 遵循流程 |
| **核心机制** | 云端执行 + 自动测试 | 技能系统 + 流程约束 |
| **用户干预点** | 结果审查（PR 测试后） | 过程审查（每个阶段前）|
| **对 agent 的假设** | agent 能正确执行，但需要验证 | agent 容易被误导，需要引导 |
| **典型场景** | 大型代码库的专业开发 | 需要工程纪律的规范化开发 |

两者并不矛盾。实际上，**Superpowers 的流程约束 + Cursor 的执行验证**是一个理想的组合：Superpowers 负责让 agent 先想清楚，Cursor 负责验证 agent 想的和做的是否一致。

---

## 六、安装与配置

Superpowers 的安装非常简洁。以 Claude Code 为例：

```bash
# 从官方插件市场安装
/plugin install superpowers@claude-plugins-official
```

安装完成后，Superpowers 会自动激活。当 agent 检测到你正在构建新项目时，它会自动进入技能引导流程。

如果使用其他框架，安装命令各有不同，但核心理念一致：**加载 Superpowers 的 markdown 技能文件，agent 在关键时刻读取它们**。

---

## 七、Superpowers 的局限性

笔者认为，评价一个工具必须同时看它的局限性。Superpowers 也不例外：

### 7.1 学习曲线

Superpowers 假设使用者理解软件工程方法论（TDD、YAGNI、DRY）。如果团队本身对这些概念不熟悉，Superpowers 可能会让 agent 遵循一套没人理解的规则，反而降低效率。

### 7.2 对简单任务的过度工程

对于一个简单的"在文件末尾加一行日志"这样的任务，Superpowers 的完整流程可能是杀鸡用牛刀。Superpowers 官方也承认这一点——它的技能系统设计是**可组合的**，用户可以选择性启用。

### 7.3 跨 agent 一致性

虽然 Superpowers 支持 11 个框架，但每个框架的技能触发机制略有不同。同一套技能在不同 agent 中的行为可能不完全一致，这需要用户有一定的调试经验。

---

## 总结

Superpowers 解决的不是"agent 能不能写代码"的问题，而是**"agent 写代码之前有没有想清楚"**的问题。

在 coding agent 如雨后春笋般涌现的今天，大多数工具都在追求"更强的执行能力"——更多的上下文、更长的输出、更多的工具调用。Superpowers 选择了另一条路：**更强的工程纪律**。

这不是一个性感的选择。但对于需要把代码审查权交给 agent 的团队来说，这可能是一个更负责任的选择。

**笔者认为**：如果你在使用 coding agent 时经常遇到"agent 写了一堆代码但不是我要的"的问题，Superpowers 值得一试。它不会让 agent 变得更快，但它会让 agent 变得**更值得信任**。

---

## 关联项目

- **Headroom**（44K stars）：压缩 Agent 工具输出，减少 LLM token 消耗。官网：[github.com/chopratejas/headroom](https://github.com/chopratejas/headroom)
