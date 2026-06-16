---
title: "Claude Code Subagents 实战决策框架：什么时候用、什么时候别用"
date: 2026-06-16
cluster: orchestration
source: https://claude.com/blog/subagents-in-claude-code
source_type: claude_blog
tags: [subagent, claude-code, multi-agent, context-isolation, decision-framework]
pair_project: VoltAgent/awesome-claude-code-subagents
pair_stars: 21876
pair_license: MIT
---

# Claude Code Subagents 实战决策框架：什么时候用、什么时候别用

> 原文：[Subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code) | Anthropic 官方博客 | 2026-06 发布

## 一、问题：从主会话里"偷"清静

Claude Code 擅长处理复杂、多步的项目工程，但长会话会积累负担。每一次文件读取、每一次岔路探索、每一次未完成的思路都会留在上下文窗口里，拖慢响应、推高 token 成本。

试想在大型 TypeScript monorepo 里构建新功能。主体工作是实现，但侧任务接连出现：跟踪一个已存在服务如何处理认证、寻找日期格式的公共工具、检查设计系统是否已有相近组件。这些任务**不需要**完整项目上下文，在主会话里跑只会制造噪音。

**能不能并行跑？** 这就是 subagent 的存在意义。一个 subagent 是一个隔离的 Claude 实例，拥有自己的上下文窗口。它接收任务、执行工作、只返回结果。subagent 就像 Claude Code 会话的"浏览器标签页"——一个可以追支线、不丢主线的位置。

## 二、什么是 subagent

Subagent 是拥有各自上下文窗口的自包含 agent。当 Claude 派生 subagent 时，那个 assistant 独立地读文件、探索代码、做修改。完成任务后，subagent 只把相关结果返回给主会话。每个 subagent 都是从零开始，不被会话历史或已调用 skills 的负担拖累。

多个 subagent 可并行运行，每个可拥有不同权限：研究型 subagent 可能只有只读访问权限，而实现型 subagent 拥有完整编辑能力。

Claude Code 内置几种 subagent 类型：

- **General-purpose agents**：处理复杂多步任务
- **Plan agents**：在呈现实现策略前研究代码库
- **Explore agents**：为快速、只读代码搜索而优化

Claude Code 经常自己派生 subagent 来处理分配的任务。也可以**显式引导**这种行为，并定义 Claude 自动委派的可复用专家。**知道何时拿出 subagent**，才让这个特性真正有用。

## 三、什么时候该用 subagent

某些工作类别明显受益于 subagent 委派。学会识别它们，让这个特性高效得多。

### 3.1 研究密集型任务

当理解某物如何运作是改变它的前提时，subagent 可以探索代码库并返回总结，而不是把几十个文件倒进会话。

- **信号**：收集上下文需要读取几十个文件
- **收益**：主会话保持干净，合成后的发现到达，而不是原始内容

### 3.2 多个独立任务

当跨多个文件修复错误、更新多个组件的模式、做互不依赖的修改时，并行 subagent 更快完成任务。

- **信号**：子任务之间没有依赖
- **收益**：三个 subagent 同时工作通常更快完成

### 3.3 需要新视角时

当目标是对实现做无偏见的审查时，subagent 提供干净起点——它不继承主会话的假设、上下文或盲点。

- **信号**：验证需要不被会话历史影响
- **收益**：更干净、更客观的反馈

> Pro-tip：`/clear` 命令也会重置上下文与会话历史，提供类似的 unbiased slate，但代价是**完全丢失历史**。subagent 达到同样的新鲜视角，同时主会话保持完整。

### 3.4 提交前验证

在最终化修改前，独立的 subagent 可验证实现没有对测试过拟合、没有遗漏边界情况。

- **信号**：提交代码前需要第二意见
- **收益**：抓住熟悉代码可能掩盖的问题

### 3.5 流水线工作流

当任务有清晰阶段（设计 → 实现 → 测试），每个阶段都受益于专注处理。

- **信号**：清晰交接的顺序阶段
- **收益**：每个 subagent 集中于自己的阶段，不被其他阶段的上下文制造噪音

> Pro-tip：当任务需要探索 10 个或以上文件，或涉及 3 个或以上独立工作块，这就是**引导 Claude 使用 subagent** 的强信号。

## 四、如何引导 subagent 使用

存在多种调用 subagent 的方法，从简单对话到自动化工作流。正确的起点取决于工作流，复杂度可随模式涌现叠加。

### 4.1 对话式调用

最灵活的方式是直接在对话中让 Claude 使用 subagent。这适用于所有 Claude Code 界面：终端、VS Code、JetBrains、Web、桌面应用。可靠触发 subagent 的自然语言模式包括："use subagents to research X"、"parallelize this across three agents" 等。

### 4.2 通过 skills 自动委派

Skills 是结构化指令集，Claude 在相关任务出现时自动加载。可以创建**触发型 skill**，在特定任务类型出现时**自动派生** subagent 处理——把 subagent 选择从事后决策转为上下文驱动决策。

### 4.3 可复用 specialists

可以在 `~/.claude/agents/` 中定义可复用的子代理描述。Claude 在上下文匹配时自动委派给这些 specialists。这让团队可积累**领域专长库**——研究型 subagent、测试型 subagent、安全审查型 subagent——并在整个组织复用。

## 五、何时**不**该用 subagent

subagent 不是免费的。每个派生都消耗 token、设置时间、产生协调开销。**反模式**：

- **任务过小**：单文件修改、单查询、几行代码不值得 subagent 的开销
- **任务相互依赖**：subagent 之间的依赖需要串行化，并行收益消失
- **需要主会话上下文**：当任务依赖主会话的累积状态（如已读文件、已做决策），subagent 的隔离变成阻碍
- **过度拆分**：把连贯任务拆成太多 subagent 会增加协调复杂度，超过并行收益

## 六、配套开源项目：154+ 专业 subagent 集合

`VoltAgent/awesome-claude-code-subagents`（21,876⭐ MIT）是与本文主题直接 SPM 字面级对位的开源项目——**"the awesome collection of 154+ Claude Code subagents across 10 categories"**。它把 subagent 决策框架的"可复用 specialists"维度落到了工业级：

- **10 大类别覆盖**：语言专长（voltagent-lang）、基础设施（voltagent-infra）、元编排（voltagent-meta）等
- **官方插件安装路径**：`claude plugin marketplace add VoltAgent/awesome-claude-code-subagents` + `claude plugin install <plugin-name>` 是 Claude Code 一等公民集成方式
- **交互式安装器**：`./install-agents.sh` 支持浏览、选择、安装/卸载的单命令工作流
- **元编排 agent**：`voltagent-meta` 编排 agent 在其他类别安装时**效果最佳**——这是该项目的**关键工程洞察**：subagent 不是孤立的，而是分层编制的

该项目对**何时用 subagent** 决策框架的关键贡献是：它把"可复用 specialists"层从"自定义 .md 文件"升级为"10 大类工业级目录 + 元编排"。当团队面临"用 subagent 解决什么问题"的选择时，这个仓库提供**现成的领域答案**而非从零设计。

## 七、决策树总结

```
任务需要 subagent 吗？
├─ 是 → 派生
│   ├─ 研究/探索 → Explore agent
│   ├─ 多步实现 → General-purpose agent
│   ├─ 需要计划 → Plan agent
│   └─ 复用领域专长 → 自定义 specialist
└─ 否 → 在主会话中执行
    ├─ 单文件 / 几行修改
    ├─ 任务相互依赖
    └─ 需要累积上下文
```

## 八、与"多 Agent 决策框架"（R406 同源姊妹篇）的关系

本文是 `claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them`（多 Agent 决策框架）的**姊妹篇**。两文构成 Anthropic 完整的 subagent/multi-agent 决策方法论：

- **多 Agent 决策框架**（when-and-how-to-use-them）：**架构级**问题——何时该上多 agent、何时该坚持单 agent
- **本文（subagents-in-claude-code）**：**战术级**问题——在 Claude Code 里具体怎么用 subagent、什么模式、什么反模式

两文**互不重复**——前者是"该不该用"的二元判断，后者是"用起来怎么做"的实施手册。

## 参考

- 原文：<https://claude.com/blog/subagents-in-claude-code>
- 配套开源：`https://github.com/VoltAgent/awesome-claude-code-subagents`（21,876⭐ MIT, 2026-06-16 验证）
- 姊妹篇：`claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them`（多 Agent 决策框架）
- Claude Code 文档：<https://docs.claude.com/en/docs/claude-code>
