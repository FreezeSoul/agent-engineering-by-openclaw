# stablyai/orca：并行 Agent 桌面编排的跨厂商中立解

> **GitHub**：https://github.com/stablyai/orca
> **Stars**：4,519 · **License**：MIT · **Created**：2026-03-17
> **主页**：https://onOrca.dev

> **核心主张**：Orca 把"并行运行多个 AI 编码 Agent"做成了**桌面 ADE**（Agent Development Environment），支持 Claude Code / Codex / Grok / Gemini / Hermes / OpenCode 等 20+ CLI Agent，并通过 worktree-native 隔离让多 Agent 协作可在单一窗口内编排而不互相阻塞。它与 Claude Code Desktop 形成 Pattern 10 同构跨域互补——同一个范式（parallel-agent-first）在官方 vs 跨厂商两个生态位上的并行实现。

---

## 一、解决了什么问题

当你想让 Claude Code、Codex、Gemini CLI 同时在不同 repo 上跑任务时，问题立即暴露：

1. **每个 Agent 需要自己的 git worktree**（避免 stash/branch 冲突）
2. **每个 Agent 的输出需要独立窗口可读**（避免终端输出混在一起）
3. **需要快速在 Agent 之间切换**（按状态、按 project、按 task）
4. **PR 状态、CI 状态、Review 评论需要可视**（避免不停 tab 到 GitHub）

Claude Code Desktop 解决的是「单厂商（Claude）内的同一问题」。Orca 解决的是「**跨厂商** Agent 编排」这个更难的问题。

---

## 二、核心架构

### 2.1 Worktree-native Task

Orca 的核心抽象不是"session"，而是 **task + worktree**：

- 每个 task 自动创建一个 git worktree
- task 之间通过 worktree 隔离，互不污染 stash / branch
- PR 状态、CI 状态自动与 task 绑定，GitHub Actions 检查结果实时回显到 task 视图

这与 Claude Code Desktop 的「sidebar 多 session」是同一思想的不同实现——前者强调**文件级隔离**，后者强调**会话级列表**。

### 2.2 多 Agent 异构兼容

Orca 支持的 Agent 列表（README 显式列出）：

- Claude Code / OpenClaude
- OpenAI Codex / GitHub Copilot CLI
- xAI Grok CLI / Gemini CLI / Antigravity
- Moonshot Kimi Code / Qwen Code / Mistral Vibe
- OpenCode / Hermes Agent / Goose / Auggie / Kilo / Kiro
- 任何 CLI Agent（"not just this list"）

这是 Orca 与 Claude Code Desktop 最关键的差异：**不被锁死在单一厂商**。

### 2.3 三层运行视图

Orca 把所有 task 的状态可视化为三种：

- **Active**：正在跑（绿）
- **Waiting**：等待人类介入（黄）
- **Finished**：已完成（灰）

这一分类与 Claude Code Desktop 的 "Waiting for your input / Still working / Already shipped PRs" **字面对位**——说明并行 Agent 协调的 UI 词汇正在**收敛到一个共识**。

### 2.4 Bring Your Own Subscription (BYOS)

Orca 不强制 Orca 账号登录。你用什么 Agent CLI，就用那个 CLI 的订阅。Orca 本身是**纯编排层**：

- 它不重写 Agent prompt
- 它不转发模型调用
- 它不存储 prompt 或 response
- 它只是把多个 CLI Agent 的"输出窗口"统一在一个桌面 App 里

这是与 "AI 编码 IDE"（如 Cursor）最根本的差异：**Orca 不是 IDE，是元 IDE（meta-IDE）**。

---

## 三、关键差异化能力

### 3.1 Design Mode

Orca 内嵌浏览器 + Design Mode，让 Agent 修改前端时**视觉化**：

- 在浏览器里看 AI 的改动效果
- 直接在 UI 上批注
- 把精确的浏览器 context 回传给 Agent

这一能力与 Cursor 的 Design Mode 是**平行实现**（Pattern 10 验证）——两者都把"视觉反馈"做成了 Agent context 的一等公民。

### 3.2 Mobile Companion

Orca 有 iOS App + Android APK：

- 手机上监控 Agent 状态
- 接收通知（agent 完成 / 需要介入）
- 远程推送指令

这是「并行 Agent 时代」**人类注意力必然外延到移动端**的工程确认。Claude Code Desktop 暂无移动端，Orca 在此占得先机。

### 3.3 SSH Worktrees

远程开发机的 task 与本地 task 同等对待：

- 在远程 machine 上跑 Agent
- 桌面端监控状态
- worktree 在远程 / 本地之间无缝流动

这意味着 **Orca 不绑定本地开发机**——远程 vs 本地只是 task 的 location 属性。

### 3.4 Computer Use / Agent-Ready Browser

Orca 提供 **Computer Use** 与 **Agent-Ready Browser**：

- Computer Use：让 Agent 操作本地应用（GUI automation）
- Agent-Ready Browser：让 Agent 操作浏览器（网页自动化）

这两项把 Orca 从"代码 Agent 编排器"扩展为"**通用 GUI Agent 编排器**"。

---

## 四、为什么这是 Pattern 10 同构跨域信号

笔者把 Orca 与 Claude Code Desktop 并列分析时，发现一个有趣的并行结构：

| 维度 | Claude Code Desktop | Orca |
|------|---------------------|------|
| **厂商定位** | Anthropic 官方（first-party） | 第三方（ecosystem-wide） |
| **Agent 范围** | Claude Code 单一 | 20+ CLI Agent |
| **核心抽象** | Sidebar / Pane | Worktree / Tab / Split |
| **UI 词汇收敛** | Active/Waiting/Finished（同一三元组） | Active/Waiting/Finished |
| **设计哲学** | 在 Claude 内做深 | 在跨厂商做中立 |
| **移动端** | 无 | iOS + Android |

这不是"竞品对比"，而是**同一个工程范式在两个不同生态位的并行实现**：

> **范式**：并行 Agent 时代的桌面工作环境，必须提供「多会话可视 + 状态透明 + 编排可干预」三大能力。
>
> **Anthropic 的实现**：在 Claude Code 生态内做最深集成（与 CLI 插件 / 云会话 / SSH 完整对齐）。
>
> **Orca 的实现**：在跨厂商中立层做最广覆盖（20+ CLI Agent + BYOS + Mobile + Design Mode）。

读者根据**自己被锁定的程度**选边：

- **完全在 Claude 生态** → Claude Code Desktop 更顺滑
- **需要跨厂商（同时用 Codex / Gemini / Kimi 等）** → Orca 是几乎唯一的选择

---

## 五、安装与平台支持

| 平台 | 安装方式 |
|------|---------|
| macOS | `brew install --cask stablyai/orca/orca` 或下载 DMG |
| Windows | GitHub Releases 下载 |
| Linux | Arch AUR (yay) 或 GitHub Releases |
| iOS | App Store |
| Android | GitHub Releases APK |

> 注：mobile-v0.0.12 当前为早期版本。

---

## 六、可借鉴的工程决策

对于正在设计自己 Agent 工具的工程师，Orca 给出了三个值得借鉴的决策：

1. **把"跨厂商中立"作为产品定位**——不抢 Agent 厂商的活，只做编排层
2. **把"worktree"作为任务隔离的核心抽象**——比 session 更接近文件系统语义，开发者天然理解
3. **把"移动端"作为并行 Agent 体验的标准件**——人类注意力必须可外延

---

## 七、限制与适用场景

| 适用 | 不太适用 |
|------|---------|
| 同时跑 ≥ 2 个 CLI Agent | 只跑 1 个 Agent 的简单场景（CLI 已够用） |
| 跨厂商实验（Claude + Codex + Gemini 混合） | 深度锁定在单一厂商（用厂商原生工具更顺） |
| 移动端监控需求强 | 纯服务端场景（不需要移动端） |
| 需要 Computer Use / Browser Automation | 纯文本代码任务（这些能力用不到） |

---

## 来源

- 仓库：https://github.com/stablyai/orca
- 主页：https://onOrca.dev
- Stars：4,519（截至 2026-06-10）
- License：MIT
- 配套 Article：`anthropic-claude-code-desktop-redesign-parallel-agents-2026.md`

*本文属于「AI Coding 工具」系列，分析并行 Agent 时代桌面工作环境的工程演进。*