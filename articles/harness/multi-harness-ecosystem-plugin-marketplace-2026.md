# 多 Harness 生态：一场插件市场革命正在重塑 AI Coding 版图

> **来源**: wshobson/agents GitHub README + 技术分析，MIT License，2026
> **分类**: harness / orchestration
> **关联 Project**: waltstephen/ArgusBot（Supervisor Agent 三角色架构）
> **核心判断**: AI Coding 的下一阶段竞争不在于谁能做出更强的模型，而在于谁能构建最丰富的插件生态——而这个生态的基础设施，是让同一个插件包能同时服务于 Claude Code、Codex CLI、Cursor、OpenCode、Gemini CLI、Copilot 的多 Harness 适配层。

---

## TL;DR

当大多数开发者还在讨论「哪个 AI Coding 工具最强」的时候，真正的趋势正在插件市场层面展开：**谁能用一套代码同时服务 5 个 Agent Harness，谁就能成为事实上的插件标准**。

wshobson/agents 正在做这件事：一份插件源码（`plugins/`），生成 5 个 Harness 的原生格式，84 个插件、192 个 Agent、156 个 Skills、102 个命令，从一个源头发往所有主流 Agent 平台。

---

## 核心问题

AI Coding 工具碎片化是 2026 年的现实：

| Harness | 代表工具 | 插件格式 |
|---------|---------|---------|
| Claude Code | Anthropic Claude Code | `marketplace.json` + `.claude-plugin/` |
| Codex CLI | OpenAI Codex CLI | `.codex-plugin/` + `.codex/skills/` |
| Cursor | Cursor Composer | `.cursor-plugin/` + `.cursor/rules/` |
| OpenCode | OpenCode CLI | `.opencode/` |
| Gemini CLI | Google Gemini CLI | `skills/` + `agents/` (TOML) |
| Copilot | GitHub Copilot | `.copilot/` |

每个平台都有自己的插件格式。如果插件开发者要为每个平台单独开发适配，工作量是 O(N×M)（N 个插件，M 个平台）。这就是为什么大多数插件只针对一个平台开发，跨平台插件几乎没有。

wshobson/agents 的答案是：**一个源头发，往所有平台发**。

---

## 多 Harness 适配的技术原理

### 架构：一源多发

```
plugins/python-development/          ← 单一真相来源
├── .claude-plugin/plugin.json       → Claude Code 原生格式
├── agents/                          → 共享定义
│   ├── python-pro/
│   ├── django-pro/
│   └── fastapi-pro/
├── commands/                        → 共享命令
└── skills/                          → 共享 Skills

↓ make generate HARNESS=<target>

.codex/plugins/                      → Codex CLI 格式
.cursor-plugin/                      → Cursor 格式
.opencode/                           → OpenCode 格式
.gemini/                             → Gemini CLI 格式
.copilot/                            → Copilot 格式
```

每个 harness adapter 把 `plugins/` 中的通用定义转换为该平台原生的插件格式。转换不是简单的翻译，而是**保留每个平台的 idiom**——例如 Claude Code 用 `marketplace.json`，Codex CLI 用 `.codex-plugin/plugin.json`，Gemini CLI 用 TOML 格式的 skills。

### 层级化模型策略

除了插件格式的适配，wshobson/agents 还实现了跨平台的**层级化模型策略**：

| Tier | 模型 | 用途 |
|------|------|------|
| 0 | Fable 5 | 超长时域自主工作——大规模迁移、数小时运行（需付费）|
| 1 | Opus | 架构、安全、代码审查、生产关键任务 |
| 2 | inherit | 用户自选——后端/前端/AI-ML/专业领域 |
| 3 | Sonnet | 文档、测试、调试、API 参考 |
| 4 | Haiku | 快速操作任务、SEO、部署、内容生成 |

这个层级设计反映了不同任务对模型能力的真实需求差异：写文档不需要 Opus 的能力，花费 Sonnet 的成本就足够了。

---

## 插件生态的结构设计

### 隔离与组合原则

每个插件是**孤立且可组合的**：

> *"Installing a plugin loads only its components into context — not the whole marketplace."*

这解决了插件市场的核心工程问题：插件数量增长时，全量加载会导致上下文溢出。ArgusBot 的设计保证了只把自己需要的组件装入上下文，而不是把 84 个插件全部塞进去。

### 插件类型体系

| 类型 | 数量 | 说明 |
|------|------|------|
| **Plugins** | 84 | 细粒度单用途安装单元 |
| **Agents** | 192 | 领域专家（架构、语言、基础设施、安全、数据、ML、文档、业务、SEO）|
| **Skills** | 156 | 模块化知识包，带渐进式披露（激活时才加载）|
| **Commands** | 102 | 斜杠命令：脚手架、安全扫描、测试生成、基础设施设置 |
| **Orchestrators** | 16 | 多 Agent 协调工作流（全栈、安全、ML、事件响应）|

192 个 Agents 按领域分离，每个 Agent 是该领域的专家。这意味着给一个 Python 后端任务注入的 Agent 上下文，和给同一个 workspace 的安全扫描任务注入的 Agent 是完全不同的——不是在同一个大上下文中塞入所有知识，而是按需加载专门的 Agent。

---

## 笔者判断

**多 Harness 插件市场是 AI Coding 的平台战争下一阶段**。

表面上看，Claude Code vs Cursor vs Copilot 的竞争是功能层面的：谁的反应更快、谁的上下文窗口更大、谁的模型更强。但真正的竞争正在向插件生态层面转移——因为当工具足够好后，用户迁移成本就变成了「我积累的插件和配置能带走多少」。

wshobson/agents 揭示的更深层趋势是：**插件市场的竞争不在于插件数量，而在于谁能用更低成本覆盖更多平台**。如果一个插件开发者可以用一套代码同时服务 6 个平台，这个开发者就会成为所有平台都依赖的标准。

从工程角度看，这个模式解决了一个真正的痛点：多平台适配的维护成本。对于拥有成熟插件体系的团队来说，wshobson/agents 的「一源多发」架构值得认真研究——不是从头做一个新平台，而是用适配层把现有插件资产最大化。

---

## 生态视角：ArgusBot 的位置

本文的关联 Project ArgusBot 解决的是**单个 Agent 的长任务 Supervisor 问题**。wshobson/agents 解决的是**多 Agent 平台插件的复用问题**。两者分别代表了 Harness Engineering 的两个维度：

- **ArgusBot**：单个 Agent 内部的多角色协作（Harness 内）
- **wshobson/agents**：跨平台的插件生态统一（Harness 间）

这两者不是竞争关系，而是互补关系——当你在一个多 Harness 生态中运行长任务 Agent 时，两者都需要。

---

## 结论

多 Harness 插件生态正在重新定义 AI Coding 的竞争规则。这不再只是"哪个模型最强"的模型战争，而是"谁能用更低成本服务更多平台"的生态战争。

对于插件开发者，wshobson/agents 提供了第一个可行的「一源多发」工程方案；对于 Agent 框架设计者，它验证了层级化模型策略在多平台场景下的必要性；对于 Harness Engineering 的从业者，它展示了一个关键原理：**平台碎片化不是借口，而是适配层的机会**。

---

**引用来源**：
- wshobson/agents GitHub README: https://github.com/wshobson/agents
- Topics: `agent-skills`, `multi-agent`, `claude-code-plugins`, `mcp`
- Stars: 36,782（截至 2026-06）
- License: MIT
- Created: 2025-07-24