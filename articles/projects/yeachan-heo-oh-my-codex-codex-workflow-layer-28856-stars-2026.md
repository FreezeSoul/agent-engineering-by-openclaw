# OMX (Oh My codeX)：Codex 的 Workflow Layer 与生态扩展

> 关键词：Codex Plugins、Agent Teams、Hooks、Workflow Automation、OMX
>
> 项目：[Yechan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex) | Stars: 28,856 | MIT License
>
> 关联 Article：[Anthropic Auto Mode vs OpenAI Hooks：Agent 可编程性的两条路径](./anthropic-auto-mode-vs-openai-hooks-agent-extensibility-2026.md)
>
> 分类：Agent Extensibility / Workflow Layer

---

## 这个项目解决了一个什么问题

如果你用 Codex CLI，你会发现一个尴尬的事实：**Codex 本身只提供了执行引擎，没有任何 workflow 管理能力**。

当你开始一个中型任务——澄清需求、制定计划、分任务给多个 Agent、执行、审查——你只能自己手动管理这一切：开多个终端、记住每个 Agent 的状态、在它们之间传递上下文。

OMX 就是来解决这个问题的：**在 Codex 执行引擎之上，加一层完整的 workflow 管理**。

根据项目 README：

> OMX is a workflow layer for OpenAI Codex CLI. It keeps Codex as the execution engine and makes it easier to: start a stronger Codex session by default, run one consistent workflow from clarification to completion, invoke the canonical skills with `$deep-interview`, `$ralplan`, `$team`, and `$ralph`.

这是一个**设计选择**：OMX 不修改 Codex 本身，而是通过外部 wrapper 的方式给 Codex 加上 workflow 能力。这样做的好处是永远和上游 Codex 保持兼容，不被锁定。

---

## 核心功能

### 1. 标准 Workflow 模式

OMX 定义了一个标准的三阶段 workflow：

```
$deep-interview  →  $ralplan  →  $ralph/$team
```

| 阶段 | Skill | 功能 |
|------|-------|------|
| **澄清** | `$deep-interview` | 深入理解需求，消除模糊点 |
| **计划** | `$ralplan` | 制定方案，review tradeoffs，获得批准 |
| **执行** | `$ralph` / `$team` | 持续执行或在多 Agent 间并行分发 |

这个 workflow 的设计逻辑很清晰：**Agent 在行动之前必须先理解清楚（澄清）、计划清楚（计划），而不是一上来就开始做**。

这实际上是一种**强制性的 Agent 纪律**——用 prompt 和 skill 约束来弥补基础模型在长程任务中容易跑偏的问题。

### 2. 多 Agent 并行执行（`$team`）

```bash
$team 3:executor "execute the approved plan in parallel"
```

`$team` 让你在 tmux session 中启动多个并行的 Codex Agent，每个 Agent 承担一个子任务。根据 README：

> On macOS/Linux interactive terminals with `tmux` available, this starts the recommended durable team runtime.

**多 Agent 协作的关键设计**：每个 Agent 的状态、上下文、输出都持久化在 `.omx/` 目录中，下一个阶段可以无缝继承上一个阶段的输出。

### 3. 生态扩展能力

OMX 的野心不止于 workflow 管理——它试图成为 Codex 的"插件平台"：

| 扩展类型 | 说明 |
|---------|------|
| **Plugins** | 官方插件布局（`plugins/oh-my-codex`），支持 marketplace 元数据 |
| **Skills** | 官方 canonical skills：`$deep-interview`、`$ralplan`、`$ralph`、`$team` |
| **Hooks** | 原生运行时 hooks（在 setup 阶段管理，不走插件 manifest） |
| **Agents** | 专门的 Agent 角色定义（Leader/Executor 等） |

这种分层设计和 OpenAI 的 Hooks API 形成了一种有趣的呼应：**OpenAI 定义了 Hooks 的接口规范，OMX 给出了 Hooks 的一种具体实现**。

---

## 技术架构

### 分层设计

```
┌─────────────────────────────────┐
│         User Interface          │
│    ($deep-interview, $ralph...)  │
├─────────────────────────────────┤
│         OMX Workflow            │
│   (Clarify → Plan → Execute)    │
├─────────────────────────────────┤
│         Codex CLI               │
│      (Execution Engine)         │
└─────────────────────────────────┘
```

OMX 把自己放在用户和 Codex 之间，拦截用户命令并路由到对应的 workflow 阶段。每个阶段都调用 Codex 完成实际工作，但用 OMX 的 prompt 模板约束了 Codex 的行为方式。

### 状态持久化

OMX 用 `.omx/` 目录管理所有状态：

```
.omx/
├── plans/         # 计划阶段输出
├── logs/          # 执行日志
├── memory/        # Agent 间共享上下文
├── ultragoal/     # 跨 session 的长程目标
└── mode-tracking/ # 当前模式状态
```

这个设计很关键：**有了持久化状态，多个 Agent 之间才能真正共享上下文，而不是每次都从零开始**。

---

## 笔者的判断

OMX 值得关注，有两个原因：

**第一，它验证了一个判断**：Codex 的成功不是因为它自己有多强大，而是因为围绕它的生态足够丰富。28,856 stars 说明大量开发者愿意在 Codex 之上构建 workflow 层——而不是等待官方内置。

**第二，它的 `$team` 多 Agent 模式和 OpenAI 的 Remote SSH + Hooks 形成了互补**：OMX 通过 tmux 在本地管理多 Agent，OpenAI 通过远程 SSH 在云端管理多 Agent。两者解决的是同一个问题（如何让多个 Agent 协调工作），但技术路线不同。

对于想用 Codex 构建复杂 Agent 系统的开发者，OMX 是一个**低门槛的起点**——它不需要你理解 tmux 或复杂的 hook 配置，只需要记住几个 skill 名字就能启动一个完整的多 Agent workflow。

---

## 快速开始

```bash
npm install -g @openai/codex oh-my-codex

# 推荐的启动方式
omx --madmax --high

# 在 Codex 中使用标准 workflow
$deep-interview "clarify the authentication change"
$ralplan "approve the auth plan and review tradeoffs"
$ralph "carry the approved plan to completion"
$team 3:executor "execute the approved plan in parallel"
```

---

## 参考资料

- [GitHub: Yechan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)
- [OMX Docs: Getting Started](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/getting-started.html)
- [OMX Discord Community](https://discord.gg/PUwSMR9XNk)