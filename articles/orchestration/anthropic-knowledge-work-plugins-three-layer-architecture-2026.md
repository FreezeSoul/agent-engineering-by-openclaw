# Anthropic Knowledge Work Plugins 三层架构解析：从 Skill 定义到生产力插件的工程实现

> 本文深入分析 [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)（16,558 Stars）仓库的架构设计，揭示官方如何通过「三层架构」将 Skill 标准从抽象定义落地为可用的生产力工具。本文重点解析 **productivity 插件**（Task Management + Workplace Memory + Visual Dashboard），从中透视 Skill 系统的工程实现细节。

---

## 背景：Skill 定义之后的下一步

Anthropic 官方博客 [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) 提出了 progressive disclosure 架构（Level 1 metadata → Level 2 SKILL.md → Level 3 additional files），解决了「如何标准化 Agent 技能」的问题。

但还有一个关键问题没有回答：**Skill 编写完成后，如何与具体的 Agent 实例绑定并部署为可用的工具？**

`anthropics/knowledge-work-plugins` 仓库是这个问题的官方答案——它不仅开源了 11 个插件的源码，更重要是展示了 Skill 标准从「文档定义」到「可运行工具」的完整工程路径。

---

## 仓库整体架构

```
plugins/
  productivity/          # 任务管理 + 记忆系统（本文重点）
  sales/
  customer-support/
  product-management/
  marketing/
  legal/
  finance/
  data/
  enterprise-search/
  bio-research/
  cowork-plugin-management/  # 插件开发工具
```

每个插件遵循统一结构：

```
plugin-name/
├── .claude-plugin/plugin.json   # Level 1: 元数据清单
├── .mcp.json                    # Level 1: MCP 连接器配置
├── commands/                    # Level 2: 显式触发的 slash commands
└── skills/                      # Level 2+3: Skill 定义 + 实现文件
```

这个结构将三层职责分离：**plugin.json 声明身份**，**.mcp.json 绑定工具**，**skills/ 封装专业知识**。

---

## 三层架构详解：以 productivity 插件为例

### 第一层：plugin.json —— 插件身份元数据

```json
{
  "name": "productivity",
  "version": "1.2.0",
  "description": "Manage tasks, plan your day, and build up memory of important context about your work.",
  "author": { "name": "Anthropic" }
}
```

这层是轻量级声明——告诉 Agent「这个插件是什么」，但**不包含任何执行逻辑**。Version 字段在这里的作用是支持插件市场的版本管理，用户可以指定 `productivity@1.2.0` 而非总是拉取最新。

### 第二层：.mcp.json —— 工具连接声明

```json
{
  "mcpServers": {
    "slack":     { "type": "http", "url": "https://mcp.slack.com/mcp", "oauth": {...} },
    "notion":    { "type": "http", "url": "https://mcp.notion.com/mcp" },
    "asana":    { "type": "http", "url": "https://mcp.asana.com/v2/mcp" },
    "linear":   { "type": "http", "url": "https://mcp.linear.app/mcp" },
    "atlassian":{ "type": "http", "url": "https://mcp.atlassian.com/v1/mcp" },
    "ms365":    { "type": "http", "url": "https://microsoft365.mcp.claude.com/mcp" },
    "monday":   { "type": "http", "url": "https://mcp.monday.com/mcp" },
    "clickup":  { "type": "http", "url": "https://mcp.clickup.com/v2/mcp" },
    "google calendar": { "type": "http", "url": "" },
    "gmail":    { "type": "http", "url": "" }
  }
}
```

**10 个 MCP 连接器**，覆盖主流协作工具。但注意 `google calendar` 和 `gmail` 的 url 为空字符串——这是官方有意的占位设计，表示「已声明但待用户配置」。

**笔者认为**：这个设计揭示了企业插件的核心矛盾——Anthropic 无法预埋所有企业的 OAuth 凭证，所以 url 为空时由用户自行填写，而 OAuth 配置通过 `oauth.clientId` 引导用户完成授权 flow。这是插件可扩展性的工程体现，而非功能残缺。

### 第三层：skills/ —— Skill 定义的工程实现

```
productivity/skills/
├── task-management/
│   ├── SKILL.md          # Level 2: Skill 元定义
│   └── dashboard.html    # Level 3: 可执行 UI
└── memory-management/
    └── SKILL.md          # Level 2: Skill 元定义
```

这里的关键是 **Level 3 文件的存在方式**——`dashboard.html` 不是代码，而是 Skill 执行时需要的辅助资源。Agent 通过引用 `${CLAUDE_PLUGIN_ROOT}/skills/dashboard.html` 将其复制到工作目录，实现 Skill 与工作区的解耦。

---

## Task Management 深度解析：Skill 执行单元

### SKILL.md 的实际内容

```yaml
---
name: task-management
description: Simple task management using a shared TASKS.md file.
user-invocable: false
---

# Task Management

## File Location
Always use TASKS.md in the current working directory.

## Dashboard Setup (First Run)
1. Check if dashboard.html exists
2. If not, copy from ${CLAUDE_PLUGIN_ROOT}/skills/dashboard.html
3. Inform user to run /productivity:start
```

**两个关键设计点**：

1. **`user-invocable: false`**：这个 Skill 是隐式触发的，只有 Agent 自己判断需要读写 TASKS.md 时才使用，而不由用户手动 slash 调用。这解决了「哪些 Skill 应该出现在 command list 里」的问题。

2. **`${CLAUDE_PLUGIN_ROOT}` 变量**：Plugin 内部的资源路径通过环境变量引用，而不是硬编码绝对路径。这是 Skill 可移植性的基础——同一个 plugin 可以从不同路径加载，路径变量由运行时注入。

### TASKS.md 格式设计

```
# Tasks

## Active
- [ ] **Task title** - context, for whom, due date

## Waiting On
- [ ] **Task** - since [date]

## Done
- [x] ~~Task~~ (date)
```

**笔者认为**：Anthropic 选择纯文本格式而非 JSON 或数据库，是为了让 TASKS.md 同时被人类和 Agent 读写——这不只是工程选择，更是「人机协作同一文件」这一哲学的体现。

### Visual Dashboard：Level 3 的 UI 扩展

`dashboard.html` 是一个独立可运行的 HTML 文件，Agent 在首次交互时将其从插件目录复制到工作目录。这是一个**插件内的静态资源注入**模式：

```
Agent 首次处理 task 需求
  → 检测 dashboard.html 是否存在
  → 不存在则从 ${CLAUDE_PLUGIN_ROOT}/skills/dashboard.html 复制
  → 告知用户运行 /productivity:start 初始化系统
```

这个模式与 MCP 的 tool 调用有本质区别——**dashboard.html 不是 Agent 调用外部工具，而是将 UI 资源注入工作区，让人类可以在浏览器中直接操作同一份数据**。

---

## Memory Management 深度解析：两层记忆系统

这是 productivity 插件中最有技术含量的设计——**CLAUDE.md 作为 hot cache + memory/ 目录作为 deep storage**。

### 核心问题：为什么需要两层？

通用 AI 每次对话都从零开始——它不知道你的同事叫什么、你们的项目用什么缩写、你的偏好是什么。Memory Management 通过两层架构解决「工作区上下文」问题：

```
CLAUDE.md (hot cache)     →  ~30 people, ~30 terms, active projects
memory/ (deep storage)   →  unlimited scale, full profiles
```

### CLAUDE.md 格式示例

```markdown
# Memory

## Me
[Name], [Role] on [Team].

## People
| Who | Role |
|-----|------|
| **Todd** | Todd Martinez, Finance lead |
→ Full list: memory/glossary.md, profiles: memory/people/

## Terms
| Term | Meaning |
|------|---------|
| PSR | Pipeline Status Report |
| P0 | Drop everything priority |
→ Full glossary: memory/glossary.md

## Projects
| Name | What |
|------|------|
| **Phoenix** | DB migration, Q2 launch |
→ Details: memory/projects/
```

### memory/ 目录结构

```
memory/
├── glossary.md      ← 全量解码器（所有人/所有术语）
├── people/         ← 人员详细档案
├── projects/       ← 项目详细档案
└── context/         ← 公司/团队上下文
```

### 查询流程（Tiered Lookup）

```
User: "ask todd to do the PSR for oracle"

1. Check CLAUDE.md (hot cache)
   → Todd ✓ Todd Martinez, Finance
   → PSR ✓ Pipeline Status Report
   → Oracle ✗ Not in hot cache

2. If not found → search memory/glossary.md
   → Oracle ✓ Oracle Systems deal ($2.3M, closing Q2)

Now Claude can act with full context.
```

### Promotion / Demotion 动态管理

| 操作 | 触发条件 | 效果 |
|------|---------|------|
| **Promote to CLAUDE.md** | 某术语/人员频繁使用 | 从 memory/ 提升到 hot cache |
| **Demote to memory/** | 项目完成/人员不再联系 | 从 CLAUDE.md 移除，保留在 memory/ |

**这是 Skill 系统中最接近「机器学习」的部分**——不是训练模型，而是通过显式的 promotion/demotion 规则，让 hot cache 随使用模式自适应变化。

### 解码示例：这个设计解决什么问题

```
User: "ask todd to do the PSR for oracle"
              ↓ Claude decodes
"Ask Todd Martinez (Finance lead) to prepare the Pipeline Status Report
 for the Oracle Systems deal ($2.3M, closing Q2)"
```

Without memory, that request is meaningless. With this two-tier system:
- **Todd** → 从 CLAUDE.md Key People 查到 Todd Martinez
- **PSR** → 从 CLAUDE.md Terms 查到 Pipeline Status Report
- **Oracle** → 从 memory/glossary.md 查到 Oracle Systems deal

**笔者认为**：这是「让 AI 理解人类工作语言」的最直接方案——不是让人类学如何与 AI 对话，而是让 AI 学人类的缩写体系。

---

## 与 Round 117/118 的关联

| 轮次 | 产出 | 主题关联 |
|------|------|---------|
| Round 117 | Gartner MQ 企业级编排 | Orchestration 平台层 |
| Round 118 | Cursor Harness 工程方法论 | Harness 执行层 |
| **Round 119** | **Knowledge Work Plugins 三层架构** | **Skill 系统的工程落地** |

三层架构的逻辑关系：

```
Orchestration（编排平台）
  ↓ 解决「多 Agent 如何协作」
Harness（执行引擎）
  ↓ 解决「Agent 如何稳定运行长任务」
Skill System（技能系统）
  ↓ 解决「Agent 如何获取专业领域知识」
Knowledge Work Plugins
  ↓ 这是 Skill 标准的第一个完整生产级参考实现
```

---

## 工程意义

### 1. Skill 系统的「最后一公里」问题被解决

之前的 Skill 标准停在「写好 SKILL.md」，但没有回答「SKILL.md 里的资源引用（如 dashboard.html）如何被注入工作区」。productivity 插件通过 `${CLAUDE_PLUGIN_ROOT}` 变量和首次运行时的资源复制解决了这个问题。

### 2. MCP 连接器的声明式配置

`.mcp.json` 里的 10 个连接器不是运行时动态注册，而是**声明式配置**——Agent 在加载插件时就知道有哪些工具可用，这是「声明即服务」在 Agent 场景的落地。

### 3. 双重部署的架构预演

结合 `anthropics/financial-services` 的 managed-agent cookbook（同一 Skill 文件既作为 Cowork 插件安装，也可通过 Managed Agent API 部署），Knowledge Work Plugins 的设计预示了 **「一次编写，双重部署」正在成为 Anthropic Agent 技能复用的标准架构模式**。

> "Plugins let you go further: tell Claude how you like work done, which tools and data to pull from, how to handle critical workflows, and what slash commands to expose — so your team gets better and more consistent outcomes."
> — [anthropics/knowledge-work-plugins README](https://github.com/anthropics/knowledge-work-plugins)

---

## 原文引用

1. "Plugins let you go further: tell Claude how you like work done, which tools and data to pull from, how to handle critical workflows, and what slash commands to expose — so your team gets better and more consistent outcomes." — [README.md](https://github.com/anthropics/knowledge-work-plugins)

2. Skill architecture: `task-management` SKILL.md — `${CLAUDE_PLUGIN_ROOT}` variable pattern for resource injection

3. Memory architecture: two-tier lookup flow (CLAUDE.md → memory/glossary.md → ask user) — progressive disclosure in practice

---

## 总结

Knowledge Work Plugins 仓库是 Skill 标准从「文档定义」到「可运行工具」的第一个完整生产级参考实现。三层架构（plugin.json 元数据 + .mcp.json 连接器 + skills/ 执行单元）、两层记忆（CLAUDE.md hot cache + memory/ deep storage）、以及 dashboard.html 的资源注入模式，共同展示了 Skill 系统工程落地的完整路径。

**这个仓库的价值不只是 11 个插件，而是 Skill 标准工程化的方法论本身。**

---

*关联项目*：[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)（16,558 Stars）官方插件市场源码