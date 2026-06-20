# ARD 协议：让 Agent 自己找到该用哪个工具

> 原文：[ARD Specification](https://agenticresourcediscovery.org/spec/)（AgenticResourceDiscovery.org，v0.9 Draft，2026-05-28）| [GitHub Copilot Agent Finder 发布](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/)（2026-06-17）
> 2026 年 6 月 17 日，GitHub 正式上线 Agent Finder，背后的规范是 ARD（Agentic Resource Discovery）。这是由 Microsoft、Google、Hugging Face、GoDaddy 联合推出的开放规范，目标是解决 AI Agent 的工具发现问题。

---

## 核心命题

AI Agent 现在面临一个结构性问题：工具太多了。

MCP 服务、Skills、Canvas、第三方 Agent、API——一个配置完整的开发环境可能有几十个可用工具。但 Agent 的上下文窗口是有限的，它不可能把所有工具的描述都塞进去，等任务来了再挑。

**ARD 的解决思路**：不要让 Agent 带着所有工具的描述跑任务，而是让 Agent **在任务需要时去查注册表**。

这就是"按需发现"（on-demand discovery）——Agent 不是"装配好所有工具的瑞士军刀"，而是"知道怎么找到正确工具的问询处"。

---

## ARD 的工作方式

### 三层架构

ARD 规范定义了三个核心角色：

1. **AI Client（AI 客户端）**：Claude Code、GitHub Copilot、Cursor 等
2. **Registry（注册表）**：存放 AI 资源的目录（工具、Skill、Agent 等）
3. **Resource（资源）**：具体的 MCP 服务器、Skill 包、Agent 实现

当 AI Client 需要完成一个任务时，它向 Registry 发起查询，用自然语言描述任务，Registry 返回匹配的资源列表，Client 选择性加载。

### 关键设计：按需加载，不是全部加载

传统模式下，Agent 的工具列表是静态配置的——工程师预先写好所有可能用到的工具，Agent 启动时全部加载。

ARD 模式下，工具列表是动态查询的——Agent 只需要描述它当前要做什么，注册表返回相关工具，Agent 按需接入。

>原文："Agents load what the work calls for instead of carrying every tool just in case."
>— [GitHub Changelog: Agent Finder](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available/)

### 企业场景的关键设计：私有注册表

ARD 支持私有注册表，企业可以架设自己的内部资源目录：

>原文："Discover from a registry you choose: Point agent finder at GitHub's curated public catalog, or at your own private registry of internal resources, and the answers an agent gets are scoped to that source."

这意味着：
- 企业可以把内部的 MCP 服务、专有 Skill 放入私有注册表
- Agent 查询时只返回企业内部允许使用的资源
- 不存在"Agent 意外接入了未经审批的外部工具"的问题

---

## GitHub Agent Finder：ARD 的首个企业级实现

2026 年 6 月 17 日，GitHub 正式上线了基于 ARD 的 Agent Finder 功能。

### 功能描述

>原文："GitHub agent finder is now available. Instead of hand-wiring which MCP servers, skills, canvases, agents, and tools each agent should use—and filling your context window in the process—GitHub Copilot can now discover the right capability for a task on its own."

用户用自然语言描述任务，Agent Finder 在注册表中搜索匹配的资源，返回排名结果，用户决定加载哪个。

### 不自动安装原则

Agent Finder 有一个重要的设计原则：**不自动安装**。

>原文："Agent finder finds the right tool at the right time. It doesn't silently connect anything. You stay in control of what actually gets wired in."

这意味着发现和接入是分开的——Agent 可以告诉你"这个任务适合用这个 MCP 服务"，但实际连接需要用户授权。这对安全敏感的企业环境很重要。

### ARD 生态联盟

ARD 规范的参与方：

| 公司 | 角色 |
|------|------|
| **Microsoft** | ARD 规范主要推动者，GitHub Agent Finder 实现 |
| **Google** | 规范共同开发，Jubberbu（Google）担任主要作者 |
| **Hugging Face** | 规范共同开发，提供模型和工具生态 |
| **GoDaddy** | 规范共同开发，企业实际需求输入 |
| **GitHub** | Agent Finder 实现，公有注册表运营 |

这个联盟阵容覆盖了 AI 编码工具的主要玩家——Copilot、Claude Code 生态（通过 Hugging Face 的工具生态）、Cursor（间接）。

---

## 工程意义：工具装配模式的范式转变

笔者认为 ARD 最重要的工程意义不是"少配置几个参数"，而是改变了 Agent 开发的一个基本假设。

**旧范式**：开发者知道 Agent 需要什么工具 → 预先配置 → Agent 启动时全部加载

**新范式**：Agent 知道任务需要什么工具 → 运行时查询注册表 → 按需加载

这个转变的影响：

### 1. Agent 开发从"配置驱动"变成"发现驱动"

旧模式下，Agent 的能力边界是由开发者预先定义的——你知道这个 Agent 会处理哪些任务，所以你知道该配置哪些工具。

新模式下，Agent 的能力边界是动态扩展的——Agent 通过查询发现它需要的工具，而不需要开发者预先知道所有任务类型。

### 2. MCP 生态的发现层问题被解决

MCP 协议解决了"工具怎么调用"的问题，但没有解决"工具怎么被发现"的问题。

ARD 恰好填补了这个空白——它是 MCP 的发现层，让 Agent 可以动态找到正确的 MCP 服务，而不需要预先配置完整的 MCP 服务器列表。

### 3. 企业 AI 安全的新基线

>原文："Enforce with managed settings: The same place you govern Copilot is where you define which resources agents are allowed to discover and use. Agent finder only ever surfaces what your enterprise permits."

企业可以在一个地方管理哪些 AI 资源允许被使用——这是"AI 权限管理"的基础设施层面的支撑。

---

## 局限性

ARD 规范目前是 v0.9 Draft（2026-05-28），还不是正式版：

- **规范稳定性**：v0.9 意味着还在快速迭代，企业大规模采用需等待正式版
- **注册表覆盖率**：公有注册表需要工具作者主动提交，目前覆盖范围有限
- **查询质量**：自然语言查询的匹配准确性取决于注册表的索引质量

---

## 结论

ARD 规范和 GitHub Agent Finder 的上线，代表了 AI Agent 工具装配模式的一个转折点：从"预先配置所有可能用到的工具"到"任务驱动、按需发现"。

对于 Harness 工程师来说，这意味着未来设计 Agent 系统时，需要考虑的不仅是"这个 Agent 应该有哪些工具"，还要考虑"这个 Agent 怎么知道它需要什么工具"——这是两个不同层次的问题，ARD 解决了后者。

---

## 关联项目

[VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)（1,643 ⭐）— 学术界的 Claude Code 系统性分析。ARD 规范解决的"工具发现问题"，在 Claude Code 的架构中是通过静态配置解决的——理解 Claude Code 原有的工具装配模式，有助于理解 ARD 为什么会带来范式转变。

