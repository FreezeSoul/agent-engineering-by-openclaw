# Anthropic 官方详解：Claude Code 的五大工程机制

> 本文解读 Anthropic 2026年3月24日发布的 *Claude Code Advanced Patterns: Subagents, MCP, and Scaling to Real Codebases* 官方技术文档。
>
> **核心命题**：这份 PDF 揭示了 Anthropic 官方认可的五种 Claude Code 规模化工程机制——从单点工具到多 Agent 编排平台的架构演进路线图。

---

## 一、CLAUDE.md：项目级上下文注入

CLAUDE.md 是 Anthropic 给 Claude Code 配置项目上下文的官方方案，定位类似 README 但专为 AI 设计。

### 层级化指令管理

Claude Code 在执行时会**向上遍历目录树**，自动发现并加载沿途的 CLAUDE.md 文件。这意味着你可以在 monorepo 根目录放一个全局策略文件，在每个子包放置局部规则：

```
/                        ← 系统级 overview
  /packages/CLAUDE.md    ← 包级架构说明
    /packages/ui        ← UI 组件专项
    /packages/api       ← API 设计规范
    /packages/test       ← 测试策略
```

### 最佳实践（官方建议）

| 原则 | 说明 |
|------|------|
| **保持 < 200 行** | 更长的文件消耗更多上下文，影响指令遵循度 |
| **使用 .claude/rules/** | 将大量规则拆分为多个文件，通过目录组织 |
| **scoped paths** | 规则文件 frontmatter 中通过 `paths` 字段限定作用域 |
| **claudeMdExcludes** | 通过设置排除与项目无关的 CLAUDE.md 文件 |

> "Longer files consume more context and can negatively affect instruction adherence." — *Anthropic, CLAUDE.md Best Practices*

### 与 AUDE.md 的区别

Anthropic 在 PDF 中首次正式提到 **AUDE.md**（Assistant User Description Editor），这是一个"强制 README"机制——让团队管理员为 Claude 预设结构化指令，确保每个成员获得一致的项目理解。

---

## 二、Hooks：生命周期自动化的官方入口

Hooks 是 Claude Code 生命周期事件的自动化钩子，通过 `/hooks` 目录注册 shell 命令，在特定时机自动触发。

### 官方示例场景

```
● Notifications: 自定义通知方式
● Automatic formatting: 保存时自动格式化
● Logging: 记录执行轨迹
● Correcting Claude behavior: 纠正 Claude 行为偏差
```

### Hooks vs CLAUDE.md vs MCP

这是 Anthropic 给出的官方决策矩阵：

| 维度 | CLAUDE.md | Hooks | MCP |
|------|-----------|-------|-----|
| **触发方式** | 项目上下文注入 | 确定性生命周期事件 | 按需调用外部工具 |
| **典型场景** | "用 pnpm不用 npm，用 pytest 而非 unittest" | 保存时自动格式化、编辑后运行测试、完成时发通知 | 查询数据库、访问 GitHub、发 Slack 消息 |
| **本质** | 静态指令 | 确定性自动化 | 通过标准化协议的外部 API 访问 |

> "Deterministic automation that must always run at specific lifecycle events." — *官方定位*

---

## 三、MCP：外部系统接入的标准协议

MCP（Model Context Protocol）在 PDF 中被定义为"让 Claude 访问外部系统的标准协议"，适用于需要**推理外部状态**的场景——如拉取 Figma 设计稿、创建工单、查询数据库等。

### 官方接入方式

```bash
mcp add <server-name>
```

### MCP 的适用边界

MCP 不是万能的。官方明确指出：当 Claude 只需要"复制粘贴"信息时，不需要 MCP；但当需要**实时推理外部状态**时，MCP 是正确答案。

**典型 MCP 场景**：
- "Check Sentry and Statsig to understand the usage of the feature described in ENG-4521."
- 查询数据库、访问 Google Drive、GitHub API 等

---

## 四、Parallel Claude：多实例并行

Parallel Claude 让团队可以在**同一代码库的不同工作区**并行运行多个 Claude Code 实例，每个实例拥有独立上下文。

### 两种并行模式

#### 1. Git Worktrees

```bash
claude --worktree <name>
```

Anthropic 的官方描述：
> "Create isolated working directories from the same repo. Each Claude instance operates on a different worktree, avoiding file conflict."

#### 2. 多终端并行

在各自终端中运行多个 Claude Code 实例，每个实例处理独立任务。

### Parallel vs Subagents vs Agent Teams

| 场景 | 工具选择 |
|------|---------|
| 同时处理多个**无关任务**（每个在独立终端/worktree）| **Parallel Claude** |
| 从主会话委托**聚焦子任务**（隔离上下文）| **Subagents** |
| 将大任务拆分为**独立工作流**（各 Agent 协调同步）| **Agent Teams** |

> "Agent teams shine when a task can be broken into independent workstreams, so each agent can own a slice without blocking others."

---

## 五、Subagents：隔离上下文的高效委托

Subagents 是 Claude Code 的**上下文隔离机制**，而非简单的并发执行。当主 Agent 需要处理复杂任务但不想让子任务的上下文污染主会话时，Subagents 是官方解法。

### 三个官方定义的理想场景

**1. Well-defined roles（角色明确）**
当能给出子 Agent 清晰的职责、工具权限和完成标准时：

```
my-project/
├── CLAUDE.md
├── agents/
│   ├── code-reviewer.md   ← 角色定义 + 工具限制 + 成功标准
│   ├── researcher.md
│   └── writer.md
```

**2. Hands-off delegation（放手委托）**
当你不需要跟踪子 Agent 工作过程，只关心最终结论时：

> "When inspecting or interacting with the subagent's work is not a priority for you and only need a task to complete and return a few conclusions."

**3. Enhance context management（上下文管理）**
当主会话上下文即将耗尽时，子 Agent 的**隔离上下文窗口**可以将信息过滤后再汇报给主 Agent，避免上下文污染。

---

## 六、Agent Teams：研究预览中的多 Agent 协调

PDF 最后提到了 **Agent Teams**（研究预览阶段）：多个 Claude Code 实例通过消息通信协调工作，共同完成一个任务。

### Agent Teams 的适用场景

- 任务可被拆分为独立工作流
- 每个工作流 Agent 可以"拥有自己的切片"而不会阻塞其他 Agent
- 需要协调多个专业角色（如 code-reviewer + researcher + writer）

### Agent Teams vs Parallel Claude

| 维度 | Agent Teams | Parallel Claude |
|------|-------------|----------------|
| **协调方式** | Agent 间消息通信 | 独立并行无协调 |
| **上下文** | 共享协调层 | 完全独立 |
| **依赖关系** | 任务间有依赖，需要协调 | 任务间无依赖 |
| **适用场景** | 多服务重构（每个 Agent 负责一个服务）| 单任务多实例并行 |

---

## 七、GitHub Actions 集成：Claude Agent SDK 的生产落地

PDF 还展示了如何通过 **Claude Agent SDK** 将 Claude Code 嵌入 GitHub Actions：

```yaml
# Run Claude Code in GitHub Actions
- name: Claude Code Review
  uses: anthropic/claude-code-action
```

### 官方 Code Review 功能

Anthropic 在 PDF 中预告了 Claude Code 的 **Code Review 功能**（基于 Agent Teams）：
-  Specialized agents with context on your full codebase
-  Capable of finding easy-to-miss edge cases and regressions
-  Post inline comments on bugs, security gaps, rated by severity

---

## 八、五种机制的演进关系

Anthropic 的五层 Claude Code 规模化工程机制，形成了一个完整的能力演进路径：

```
Level 1: CLAUDE.md (静态上下文注入)
    ↓ 增强了项目理解
Level 2: Hooks (确定性自动化)
    ↓ 自动化生命周期
Level 3: MCP (外部工具接入)
    ↓ 扩展执行能力边界
Level 4: Parallel Claude (多实例并行)
    ↓ 突破单会话吞吐量
Level 5: Subagents + Agent Teams (多 Agent 协调)
    ↓ 实现任务级编排
    ↓
终极形态: 自主运行的多 Agent 团队
```

### 核心设计思想

Anthropic 在 PDF 中反复强调一个观点：

> "In 2026, the value of an engineer's contributions shifts to system architecture design, agent coordination, quality evaluation, and strategic problem decomposition."

这五种工程机制，不是五个独立功能点——它们共同构成了 Anthropic 设想的 **Agent 时代的软件工程范式**：人类工程师从"写代码"转向"编排 Agent 写代码"，核心职责变成架构设计、Agent 协调、质量评估和战略问题分解。

---

## 笔者判断

这份 PDF 的价值不在于任何一个单点功能——而在于它揭示了 **Anthropic 对 Claude Code 的终极定位**：从"单点 AI 辅助编程工具"演进为"支持多 Agent 协调的生产级平台"。

五种机制面向不同层次的工程问题：

- **CLAUDE.md** → 项目级知识共享（静态）
- **Hooks** → 开发流程自动化（确定性）
- **MCP** → 外部能力扩展（按需）
- **Parallel** → 吞吐量扩展（并行）
- **Subagents/Teams** → 任务编排（协同）

对于已经在使用 Claude Code 的团队，这份 PDF 是理解"Anthropic 认为你应该怎么用"的直接窗口；对于计划规模化 Agent 落地的架构师，它是官方推荐的演进路线图。

---

## 附录：PDF 核心引用

> "Control Claude's behavior with CLAUDE.md and Hooks." — Learning Outcomes #1

> "Parallelize Claude for major productivity gains." — Learning Outcomes #2

> "Agents that can check and improve their own output are fundamentally more reliable." — *Anthropic, Claude Agent SDK Documentation*

> "Subagents use their own isolated context windows, and only send relevant information back to the orchestrator, rather than their full context." — *Anthropic, Claude Agent SDK*

---

*来源：[Claude Code Advanced Patterns: Subagents, MCP, and Scaling to Real Codebases](https://resources.anthropic.com/hubfs/Claude%20Code%20Advanced%20Patterns_%20Subagents%2C%20MCP%2C%20and%20Scaling%20to%20Real%20Codebases.pdf)，Anthropic，2026年3月24日*