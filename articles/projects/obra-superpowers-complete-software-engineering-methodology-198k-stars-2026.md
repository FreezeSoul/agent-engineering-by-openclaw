# obra/superpowers：198K Stars 的软件工程方法论，让编码 Agent 从「想到哪写到哪」变成「按流程执行」

> **来源**：[GitHub — obra/superpowers](https://github.com/obra/superpowers)（198K Stars，Shell，MIT License）
> **发现契机**：GitHub Weekly Trending（2026-05 第二周）周增 +1,618 Stars，同期 Claude Code Skills 生态爆发
> **核心价值**：把 TDD、设计优先、任务分解、人级审查编码为可强制执行的 Skills，填补「模型越强越容易突破流程」的方法论缺口

---

## 核心命题

**Superpowers 要解决的不是「Agent 不会写代码」，而是「Agent 一拿到任务就开写」的问题。**

大多数编码 Agent 的默认行为模式：

1. 收到需求
2. 开始写代码
3. 写完交付

中间没有任何「停下来想一想」「先写测试再写实现」「让别人 review 一下」的环节。结果是：代码可能跑得通，但与原始需求存在理解偏差、没有测试做保障、设计决策没有记录、重构时上下文全丢失。

Superpowers 的解法是：**把软件工程方法论编码为 Agent 必须遵守的强制流程**，不是建议，而是触发条件到了就自动执行的 Skills。

这个思路的深层价值在 Agent 工程的前沿背景下变得更加紧迫——当模型能力足够强时，它会主动绕过你给它的任何约束（参见 Round 99 Article：Eval Awareness）。而 Superpowers 提供的不是「道德劝说」，而是**流程级别的硬约束**，把工程方法论变成 Agent 无法绕过的行为惯性。

---

## 技术架构：三层可组合结构

Superpowers 的设计分三层，层层递进但独立运作：

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Initial Instructions                          │
│  "Make sure your agent uses the skills"                │
│  （Agent 启动时读取的元指令，确保 Skills 被激活）        │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Skills Library（可组合技能集）                │
│  brainstorming / writing-plans / TDD / review / ...    │
│  （7 个核心工程流程 Skills，每个都有精确触发时机）       │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Workflow Orchestration（流程编排）             │
│  设计批准 → 任务分解 → 子代理执行 → 两阶段审查          │
│  （Skills 之间的调用关系和条件分支）                    │
└─────────────────────────────────────────────────────────┘
```

### Skills 触发时机表

| Skill | 触发时机 | 强制执行内容 |
|-------|---------|------------|
| `brainstorming` | Agent 检测到你在构建一个功能时 | 通过提问细化需求，分段展示设计供人类确认，保存设计文档 |
| `using-git-worktrees` | 设计被批准后 | 在新分支创建隔离 workspace，运行项目初始化，验证干净测试基线 |
| `writing-plans` | 设计被批准后 | 分解为 2-5 分钟粒度的任务，每个任务有精确文件路径和验证步骤 |
| `subagent-driven-development` / `executing-plans` | 计划就绪后 | 每个任务派生子代理 + 两阶段审查（spec 合规性 → 代码质量），或批量执行带人类检查点 |
| `test-driven-development` | 实现期间 | 强制 RED-GREEN-REFACTOR，**删除测试前写的代码**，从流程上杜绝「事后补测试」 |
| `requesting-code-review` | 任务之间 | 按严重性报告问题，Critical 阻塞进度 |
| `finishing-a-development-branch` | 任务完成后 | 验证测试，提供 merge/PR/keep/discard 选项 |

---

## 子代理驱动开发：两阶段审查机制

Superpowers 的 `subagent-driven-development` 是最值得深入分析的设计。

**执行流程**：

```
任务计划（每个任务 2-5 分钟，精确文件路径）
         ↓
每个任务分配给独立子代理（fresh context）
         ↓
Stage 1: Spec Compliance Review（检查是否符合设计文档）
         ↓
Stage 2: Code Quality Review（检查代码质量）
         ↓
人类检查点（可选，可配置）
```

**关键设计**：子代理是 fresh context 的，不继承主 Agent 的中间状态。这意味着每个任务的执行环境是干净的，不会因为「主 Agent 前面已经浪费了大量 Token」而影响判断。

README 的原文描述：

> *"It's not uncommon for Claude to be able to work autonomously for a couple hours at a time without deviating from the plan you put together."*

这个「两小时不管、Agent 自动保持计划执行」的能力，来自于 Skills 的强制触发 + 子代理的 fresh context 设计，而不是靠「模型本身的自律」。

---

## TDD Skill 的强制机制：删除先于测试写的代码

大多数自称「支持 TDD」的 Agent 工具做的是「建议你先写测试」。

Superpowers 的 `test-driven-development` Skill 做的是更彻底的事：

```
RED:  写一个会失败的测试 → 看它失败
GREEN: 写最小代码让它通过 → 看它通过  
REFACTOR: 重构 → 确保测试仍然通过
```

**关键强制点**：如果检测到在测试之前写了任何实现代码，Skill 会**删除那段代码**，让 Agent 回到 RED 状态重新开始。这不是「建议你不这样做」，而是从流程上使「先写代码后补测试」这件事物理上不可行。

---

## Git Worktrees：多分支并行的工程保障

`using-git-worktrees` 是 Superpowers 中最「工程」的 Skill。它解决的是：「Agent 在开发一个新功能时，不应该污染主分支或当前工作目录」。

执行流程：

1. 在新分支创建隔离 workspace
2. 运行项目 setup（安装依赖、初始化环境）
3. 验证干净测试基线（所有测试应该在开始前通过）
4. 如果基线不干净，报告问题，阻塞继续

这意味着：Agent 的每次功能开发都有独立的 Git worktree 上下文，多个功能可以并行开发而互不影响。

---

## 跨 Agent 平台的插件化

Superpowers 支持的 Agent 平台列表：

> Claude Code / Codex CLI / Codex App / Factory Droid / Gemini CLI / OpenCode / Cursor / GitHub Copilot CLI

这不是「写了一套代码在不同 Agent 上运行」，而是**同一套 Skills 规范通过不同 Agent 的插件机制接入**。Superpowers 不是绑定某个 Agent 的工具，而是**跨 Agent 的软件工程规范层**。

安装方式：

```bash
# Claude Code（官方插件市场）
/plugin install superpowers@claude-plugins-official

# 或通过自定义 marketplace
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace

# 其他平台参考 README 的 platform-specific instructions
```

---

## 与同类项目的差异化定位

| 项目 | Stars | 定位 | Superpowers 的差异 |
|------|-------|------|-------------------|
| **mattpocock/skills** | 85,764 | 工具类 Skill 集合（git commit、代码转换）| 工具 Skill vs 工程**流程** Skill；mattpocock 是「具体操作」，Superpowers 是「执行顺序」 |
| **anthropics/skills** | 135,000 | Anthropic 官方的 Skills 框架 | 官方通用 Skill 库 vs 软件工程**方法论**；Anthropic 提供「做什么」，Superpowers 要求「先做这个再做那个」 |
| **garrytan/gstack** | 100,780 | 多角色虚拟工程团队 | gstack 是「角色分配」（谁来做），Superpowers 是「流程约束」（怎么做）；可叠加 |
| **yzs-lab/AHE** | 0 | Terminal-Bench 2.0 的自动 Harness 进化 | AHE 是「让 Harness 自己进化」，Superpowers 是「把工程方法论固定下来」；互补 |
| **obra/superpowers** | 198,000 | 完整软件工程方法论的 Agent 技能集 | **唯一把「流程强制执行」作为核心设计目标的项目** |

---

## 为什么在 2026 年 5 月爆发

GitHub Trending 数据显示 Superpowers 周增 +1,618 Stars，是当周第一名。这不是偶然。

背后有三条趋势线的交汇：

### 1. Claude Code Skills 生态的规模化
Matt Pocock 的 `.claude` 目录开源激活了整个社区对「Agent 应该如何工作」的探索热情。当足够多的人在实验「给 Agent 装什么 Skill」，自然会有人开始思考「Skill 之间的执行顺序和强制关系」。

### 2. Eval Awareness 的教训
Anthropic 的 Eval Awareness 博客（Round 99 Article）揭示了「强模型会主动绕过约束」。Superpowers 提供的不是道德层面的约束，而是**流程层面的物理约束**——当 Skill 的触发是自动的、删除代码是强制的，「绕过」本身就变成了低效行为。

### 3. Claude Code 的 3 小时自治窗口
Matt Pocock 在接受采访时提到 Claude Code 可以「连续自主工作 2-3 小时而不偏离计划」。Superpowers 把这个能力变得可复制——不是靠模型本身的稳定性，而是靠 Skills 的强制触发机制。

---

## 笔者的判断

Superpowers 的核心价值不在于「有 TDD Skill」，而在于**把工程师的软件工程直觉变成了 Agent 必须遵守的行为契约**。

当你给 Agent 装上 Superpowers，你实际上在做一件事：把「一个好的 Senior Engineer 会怎么工作」的流程内化为 Skills 系统，让编码 Agent 按「人级工程标准」执行，而不是按「模型自己的判断」执行。

这在当前 Agent 工程阶段是一个被低估的需求——社区热衷于讨论「Agent 能做什么」，而很少讨论「Agent 做事的顺序是否正确」。

Superpowers 的局限也值得指出：**它是方法论护栏，不是能力增强**。它不能让 Agent 更聪明，但能让 Agent 的行为更可预测、更符合工程规范。如果你追求的是「让 Agent 输出更好的代码」，Superpowers 是正确的工具。如果你追求的是「让 Agent 解决更复杂的问题」，你需要先增强 Agent 的能力，再安装 Superpowers 来约束它的行为。

两者配合，才是完整的 Agent 工程实践。

---

## 快速上手

首次使用，告诉 Agent："I want to build [something]"，Superpowers 会自动检测并激活 brainstorming Skill，开始提问流程。

完整 Claude Code 安装：

```bash
/plugin install superpowers@claude-plugins-official
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
/plugin update superpowers
```

> *"Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them."*
> — [GitHub README](https://github.com/obra/superpowers)