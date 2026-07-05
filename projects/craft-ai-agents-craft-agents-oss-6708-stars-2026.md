# craft-ai-agents/craft-agents-oss：6,708 ⭐ 的「Agent Native」桌面 Agent Harness

> **来源**：GitHub [craft-ai-agents/craft-agents-oss](https://github.com/craft-ai-agents/craft-agents-oss)
> **主题**：Agent Native 桌面应用 —— 同时集成 Claude Agent SDK 与 Pi SDK，三级权限系统，Multi-Session Inbox，Apache 2.0 开源
> **Stars**：6,708 ⭐ | **License**：Apache 2.0 | **创建**：2026-07-01（4 天前）
> **关联阅读**：[Cursor iOS 远程控制协议深度拆解](../articles/harness/cursor-ios-architecture-remote-control-handoff-deep-dive-2026.md)

---

## 核心定位

Craft Agents 是 craft.do 团队开源的桌面 Agent 应用，核心理念是 **Agent Native software**：

> "You describe what you want, and it figures out how. That's a good use of tokens."

与 Cursor/Copilot 这些「代码编辑器的 Agent 化」路径相反，Craft Agents 走的是 **「Agent 优先，反过来定义应用形态」** 的路线——不是给 IDE 加 agent，而是给 agent 设计一个 native UI。

最关键的一点：**Craft Agents 自身就是用 Craft Agents 构建的**（"we ourselves are building Craft Agents with Craft Agents only - no code editors"）。这不是营销噱头，而是 Agent Native 软件开发闭环的体现。

---

## 三个让人「不太敢信」的设计

### 一、用一句话连接任何 API

README 里最震撼的一段：

> "Tell the agent 'add Linear as a source.' It finds public APIs and MCP servers, reads their docs, sets up credentials, and configures everything. **No config files, no setup wizards.**"

这意味着用户**永远不需要手写配置文件**。Craft Agents 的 agent 会自动：
1. 查找目标服务的公开 API 文档
2. 寻找可用的 MCP server
3. 引导用户完成认证
4. 把所有配置写到 workspace

这种"零配置 + agent 自助配置"的设计，是 harness 工程从「开发者友好」走向「用户友好」的关键跨越。

### 二、Paste OpenAPI spec 直接接入

> "Paste an OpenAPI spec, some endpoint URLs, screenshots of docs, whatever you have. **It figures it out** and guides you through the rest."

也就是说，**OpenAPI spec 是 agent 的 source-of-truth 之一**。这跟 Anthropic 强调的「tool design 就是 agent UX」是同一思路——但更进一步：**把 tool 的注册也变成 agent 的工作**。

### 三、Claude Code skills 直接迁移

> "Tell the agent you want to import your skills from Claude Code. It handles the migration."

这意味着 Craft Agents 跟 Claude Code 共享**技能命名空间**。用户不需要重新写 skill，agent 自己会把 Claude Code 的 skill 文件读进来、转换格式、注册到 workspace。

这是**跨产品的 skill portability**——一种「skill 是一等公民」的工程化体现。

---

## 架构亮点

### 1. 同时集成 Claude Agent SDK + Pi SDK

README 明确说：

> "It uses the **Claude Agent SDK and the Pi SDK** side by side—building on what we found great and improving areas where we've desired improvements."

这个设计选择很有意思：**不押注单一 agent runtime**。Claude Agent SDK 擅长长任务、code execution；Pi SDK 擅长交互、并行 task。Craft Agents 把两者整合到一个 UI 下，让用户用同一套界面同时使用两种 agent runtime。

这跟 Cursor iOS 的「Cloud Agent + Local Agent」模式异曲同工：**agent runtime 不止一种，但应该对用户透明**。

### 2. 三级权限系统

| Mode | 行为 |
|------|------|
| `safe` / Explore | 只读，拦截所有写操作 |
| `ask` / Ask to Edit | 每次写操作前弹确认（默认） |
| `allow-all` / Auto | 自动批准所有命令 |

快捷键 `SHIFT+TAB` 切换。这个设计跟 Anthropic Claude Code 的 auto mode 思路类似，但实现更简单：

- **Anthropic auto mode**：基于 classifier 的动态评估 + 权限分层
- **Craft Agents**：静态三档切换

前者更智能但更复杂，后者更可控、更可审计。两种思路在 harness 复杂度谱系上各占一端。

### 3. Multi-Session Inbox + 状态工作流

Session 的状态机：

```
Todo → In Progress → Needs Review → Done
```

配合 Flag / Archive 等组织方式。这跟 Cursor iOS 的 inbox 模型是同一思路：**agent session 是一等公民，需要生命周期管理**。

但 Craft Agents 更进一步：**Session 状态本身可定制**。README 里说"Customizable session workflow states"，意味着不同 workspace 可以定义自己的状态机。

这是**session metadata schema 的开放化**——harness 不应该强制所有用户用同一套 workflow。

### 4. Multi-Provider 支持

支持的 LLM 连接：
- **Anthropic**（API key 或 Claude Max）
- **Google AI Studio**
- **ChatGPT Plus**（Codex OAuth）
- **GitHub Copilot OAuth**
- **OpenAI API keys**

这意味着 Craft Agents **不绑定单一 LLM vendor**。这是一个非常重要的设计决策：

- Anthropic 系的工具（Claude Code、Cursor 默认）有「Anthropic 优先」倾向
- OpenAI 系的工具（Codex CLI）有「OpenAI 优先」倾向
- Craft Agents 的「vendor-neutral」立场，让它在 multi-agent orchestration 场景里特别有价值

### 5. Skill 系统

> "Skills: Specialized agent instructions stored per-workspace"

Skill 是 per-workspace 的（不是 global），这跟 Claude Code 的「user-level skill」不同。Per-workspace 的好处：

- **隔离性**：不同项目可以有不同 skill 集合
- **可移植性**：workspace 本身可以导出（含 skill）
- **审计**：workspace 级别的 skill 列表更容易审计

### 6. Automations

> "Event-driven automation — create agent sessions on label changes, schedules, tool use, and more"

这是 **event-driven agent harness** 的典型实现——把 session 创建本身变成一个可订阅的事件。

可以想象的工作流：
- GitHub PR label = "needs-review" → 触发 "review-agent" session
- Calendar event = "weekly status" → 触发 "status-report-agent" session
- File changed = "*.md" → 触发 "documentation-agent" session

这种 **event → agent session** 模式，跟传统 webhook + script 模式最大的区别是：**session 是持久的、可审查的、可接管的**。

---

## 跟本仓库主题的关联

### 与 Cursor iOS 的关联

| 维度 | Cursor iOS | Craft Agents |
|------|-----------|--------------|
| Surface | 移动端 | 桌面端 |
| Agent runtime | Cursor 自有 | Claude Agent SDK + Pi SDK |
| Permission | Privacy Mode opt-in | 三档切换 |
| Session 状态 | source: iosApp 标签 | Todo/In Progress/Needs Review/Done |
| 跨设备 | Remote Control | Multi-Provider LLM |
| 核心价值 | 控制平面解耦 | Agent Native UX |

两者殊途同归：**都在解决「agent 怎么跟人交互」这个根本问题**。Cursor 用 mobile-first 的思路（手机控制），Craft Agents 用 desktop-first 的思路（桌面常驻）。

### 与 awesome-harness-engineering 的关联

ai-boost/awesome-harness-engineering 资源库把 harness 设计分为 12 个 primitives：
- Agent Loop ✓（Craft Agents 显式支持）
- Planning & Task Decomposition ✓（Skill system）
- Context Delivery & Compaction ✓（Multi-Provider）
- Tool Design ✓（Sources system）
- Skills & MCP ✓（Per-workspace skills + MCP）
- Permissions & Authorization ✓（三档权限）
- Memory & State ✓（Session state + status workflow）
- Task Runners & Orchestration ✓（Multi-session inbox）
- Verification & CI Integration ✗（不是其强项）
- Observability & Tracing ✗（不是其强项）
- Debugging & DX ✗（不是其强项）
- Human-in-the-Loop ✓（Ask to Edit 模式）

10/12 的覆盖度，对一个 4 天大的项目来说已经非常完整。

---

## 局限与边界

### 局限 1：不是代码编辑器

Craft Agents 明确不替代 IDE——它更适合**非代码任务**（文档、邮件、日程、数据查询）。如果你想要 Claude Code 那种「agent 改文件、跑测试」的体验，Craft Agents 不是合适的工具。

### 局限 2：依赖 Electron

Build from source 用的是 `bun run electron:start`，意味着应用体积大、内存占用高。这是 desktop agent 应用普遍面临的权衡（Claude Desktop、Cursor 都用 Electron）。

### 局限 3：仅 4 天

项目 2026-07-01 创建，目前还在快速迭代。文档承诺的功能跟实际实现可能存在 gap，breaking change 风险较高。

### 局限 4：没有跨设备 sync

Cursor iOS 的核心卖点「跨设备 session 同步」Craft Agents 没有。这跟其 desktop-only 定位一致，但如果未来要扩展到 mobile，session sync 是必须解决的工程问题。

---

## 与已有项目的关系

| 已推荐项目 | 关系 |
|----------|------|
| [alirezarezvani/claude-skills](../projects/alirezarevzani-claude-skills-20108-stars-2026.md) | Skill 生态协同——Craft Agents 主动支持从 Claude Code 导入 skills |
| [agentskills/agentskills](../projects/agentskills-agentskills-22243-stars-2026.md) | Skill 规范同源 |
| [ChromeDevTools/chrome-devtools-mcp](../projects/chromedevtools-chrome-devtools-mcp-41k-stars-2026.md) | MCP server 生态 |
| [composiohq-composio-tool-management-28k-stars-2026](../projects/composiohq-composio-tool-management-28k-stars-2026.md) | 工具管理范式对比 |

---

## 3 个核心 takeaway

1. **Agent Native 不是口号**——Craft Agents 自身用 Craft Agents 构建，是一个完整的 dogfooding 闭环
2. **零配置不是不可能**——把 config 的工作交给 agent，是 harness 设计的新前沿
3. **Multi-provider 是 desktop agent 的差异化机会**——比 Cursor/Copilot 更 vendor-neutral

---

## TL;DR

Craft Agents 是一款 4 天前发布的 Apache 2.0 开源桌面 agent 应用，6,708 ⭐。它的核心理念是 **Agent Native software**——把 agent 当作一等公民，反过来定义 UI。它同时集成 Claude Agent SDK 和 Pi SDK，支持 4 家 LLM vendor，三级权限系统，per-workspace skill 系统，event-driven automations。如果你想找一个「比 Claude Code 更友好、比 Cursor 更 vendor-neutral」的 desktop agent harness，Craft Agents 是值得立刻 try 一下的项目。

---

**Project Profile**

| 维度 | 数据 |
|------|------|
| Stars | 6,708 ⭐ |
| Forks | (TBD) |
| License | Apache 2.0 |
| Language | TypeScript (Electron + Bun) |
| 创建 | 2026-07-01（4 天前） |
| GitHub Trending | Daily +341, Weekly +3,388 |
| Topics | (无显式 topic tag) |
| Commit Velocity | 4 天内的爆发式增长 |

**适用人群**

- 想要 desktop agent harness 但不想绑定单一 LLM vendor 的团队
- 寻找「Claude Code skills 可移植目标」的用户
- 对 event-driven agent automation 感兴趣的产品/工程师
- 想体验「零配置接入任何 API」的设计范式的研究者