# GitHub Copilot CLI：同一个 Agent Harness，不同的终端形态

> 项目：[github/copilot-cli](https://github.com/github/copilot-cli)
> Stars：10,630（截至 2026-06-10）
> License：Other (NOASSERTION)
> 语言：Shell

---

## 核心命题

GitHub 在 2026 年 6 月的 Microsoft Build 大会上发布了 Copilot CLI 的重大更新——引入了 rubber duck、voice input、prompt scheduling 和全新的实验性终端界面。这个工具的核心定位是：**将 Copilot 的 coding agent 能力直接带到你的终端**。

笔者认为，Copilot CLI 的最大价值不在于功能本身，而在于它揭示了一个重要的工程信号：**GitHub 的 Agent Harness 正在从 IDE 扩展到 CLI 场景**。这意味着，同样的 harness 设计可以驱动不同的前端形态。

---

## 亮点描述

### 与 Claude Code 的差异化定位

GitHub Copilot CLI 和 Claude Code 面向同一个问题域（AI Coding Agent），但设计哲学不同：

| 维度 | Claude Code | GitHub Copilot CLI |
|------|-----------|-------------------|
| **交互形态** | 交互式 TUI，带 Pane/Sidebar | 终端对话 + 异步任务 |
| **上下文来源** | 本地文件系统 + Claude 生态 | 本地文件系统 + GitHub 生态 |
| **Harness 来源** | Anthropic 官方 | GitHub 官方 |
| **GitHub 集成** | 间接（需要手动 push）| **深度集成**（PR/issue 直接操作）|
| **适用场景** | 深度开发任务 | 快速查询 + GitHub 操作 |

### 2026 年 6 月更新亮点

根据 GitHub Changelog，Copilot CLI 在 2026 年 6 月新增：

- **Rubber Duck 模式**：用户可以对着 AI 解释问题，AI 通过复述和提问帮助用户理清思路
- **Voice Input**：支持语音输入，适合 hands-free 场景
- **Prompt Scheduling**：定时执行 prompt，适合 CI/CD 场景
- **实验性新终端界面**：重新设计的 TUI，改进任务可视化管理

> "GitHub Copilot CLI brings the power of GitHub Copilot coding agent directly to your terminal." — GitHub

### Harness 的产品化

笔者认为，GitHub 在 Copilot CLI 中做了一个重要的工程决策：**将 Copilot 内部的 Agent Harness 产品化**。

README 明确写道：

> "Powered by the same agentic harness as GitHub's Copilot coding agent"

这意味着：
1. CLI 版本和 IDE 版本共享同一个 harness 核心
2. CLI 可以作为 harness 的轻量级测试场
3. GitHub 在将 harness 工程从内部工具转化为外部产品的过程中，Copilot CLI 是一个里程碑

---

## 技术原理

### Architecture

Copilot CLI 的核心架构可以理解为：

```
┌─────────────────────────────────────────┐
│           GitHub Copilot Harness         │
│  (same as IDE Copilot's harness)        │
├─────────────────────────────────────────┤
│  Context Package │ Tool Descriptions │   │
│  Instructions    │ GitHub Integration │   │
└─────────────────────────────────────────┘
           ↓                    ↓
    ┌──────────┐        ┌──────────┐
    │ IDE UI    │        │ CLI UI   │
    │ (Copilot) │        │ (CLI)    │
    └──────────┘        └──────────┘
```

### 与 Claude Code 的技术对比

| 维度 | Claude Code | Copilot CLI |
|------|-------------|-------------|
| **Harness 所有权** | Anthropic | GitHub/Microsoft |
| **工具集** | bash, edit, glob, grep, view | Shell-native + GitHub API |
| **上下文管理** | 滚动 context + 自动 compaction | 终端 session 管理 |
| **权限模型** | Auto mode + approval fatigue 管理 | 依赖于 GitHub 权限体系 |
| **多 Agent 支持** | Desktop 支持多 Pane 并行 | CLI 主要单 session |

### 笔者认为的工程差异

Claude Code 的 harness 更倾向于"让 Agent 自己决定"（特别是 Opus 4.6 的 subagent 能力），而 Copilot CLI 的 harness 更倾向于"让用户通过 GitHub 权限体系控制"。这反映了两种不同的安全模型：

- **Claude Code**：信任模型内能力，通过 Auto Mode 和 approval fatigue 管理来控制
- **Copilot CLI**：信任 GitHub 权限体系，通过 GitHub 组织策略来控制

---

## 竞品对比

### 终端 AI Coding Agent 生态

| 项目 | Stars | 特点 | 与 Copilot CLI 的差异 |
|------|-------|------|----------------------|
| **Copilot CLI** | 10,630 | GitHub 官方 + 深度 GitHub 集成 | 官方 IDE/CLI 双形态 |
| **Claude Code** | 75K+ | Anthropic 官方 + 深度 Claude 集成 | 官方 IDE/CLI 双形态 |
| **Aider** | 12K+ | Git-aware CLI pair programmer | 开源 + 多模型支持 |
| **continue** | 18K+ | VSCode/JetBrains extension | IDE plugin 而非纯 CLI |

### 选型建议

笔者认为，选择哪个工具取决于你的生态锁定：

- **深度 GitHub 生态**（GitHub Actions、PR、Issues 是日常）→ Copilot CLI
- **深度 Claude 生态**（需要 Claude 的高级 reasoning 能力）→ Claude Code
- **跨模型灵活性**（不锁定特定模型）→ Aider 或 continue
- **需要 IDE 集成**（不想纯用终端）→ continue

---

## 落地指引

### 安装与快速开始

```bash
# macOS
brew install github/gh Copilot

# 或通过 npm
npm install -g @github/copilot

# 认证
gh copilot auth

# 启动 CLI
gh copilot
```

### 场景化使用

**场景 1：快速代码审查**
```bash
gh copilot "review the changes in this PR"
```

**场景 2：GitHub 操作**
```bash
gh copilot "create an issue for this bug"
gh copilot "explain why this test is failing"
```

**场景 3：Rubber Duck 调试**
```bash
gh copilot --mode rubber-duck
# 向 AI 解释你的问题，AI 会通过复述来帮助你理清思路
```

**场景 4：Voice Input（hands-free）**
```bash
gh copilot --voice
```

**场景 5：Prompt Scheduling（CI/CD）**
```bash
# 定时运行代码质量检查
gh copilot schedule "0 9 * * *" "run code quality check on ./src"
```

### 与 Claude Code 的互补使用

笔者认为，Copilot CLI 和 Claude Code 不是非此即彼的选择，而是可以互补：

```bash
# 1. 用 Copilot CLI 做快速 GitHub 操作
gh copilot "what are the open issues for this repo"

# 2. 用 Claude Code 做深度开发
claude code

# 3. 用 Copilot CLI 做 rubber duck 调试
gh copilot --mode rubber-duck
```

---

## 笔者判断

笔者认为，Copilot CLI 的价值被低估了。大多数开发者知道 GitHub Copilot（IDE 插件），但不了解 Copilot CLI 可以：

1. **作为 harness 的轻量测试场**：GitHub 的 CLI 版本通常先于 IDE 实现新功能
2. **深度 GitHub 集成**：PR/Issues/Actions 的直接操作是 Claude Code 不支持的
3. **CI/CD 集成**：prompt scheduling 适合自动化工作流

但也需要注意：
- **License 是 NOASSERTION**，生产使用前需确认合规
- **依赖 GitHub 权限体系**，组织管理员可以禁用
- **Harness 闭源**，无法自定义 harness 逻辑

对于深度 GitHub 生态的团队，Copilot CLI 是一个值得添加到工具链的补充。

---

## 引用

1. GitHub Copilot CLI README: "Powered by the same agentic harness as GitHub's Copilot coding agent"
2. GitHub Changelog (2026-06-02): Copilot CLI improvements
3. Microsoft Build 2026: Copilot CLI major refresh announcement