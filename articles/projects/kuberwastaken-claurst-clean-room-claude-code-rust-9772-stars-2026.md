# Kuberwastaken/claurst：Rust 重写的 Clean-Room Claude Code，9772 Stars 的社区验证

> **来源**：[GitHub — Kuberwastaken/claurst](https://github.com/Kuberwastaken/claurst)（9,772 Stars，Rust，GPL-3.0）
> **本文配套 Article**：[Claude Code Artifacts：从单人工具到团队协作基础设施](./claude-code-artifacts-session-output-collaboration-2026.md)

---

## 核心命题

claurst 解决了一个根本问题：**Claude Code 很好，但它绑定了 Anthropic 的闭源实现，而社区想要一个开源的、可以本地运行的、可以自由定制的 Claude Code 替代品**。

用 Rust 从零实现，不依赖 Claude Code 源码，却完整复现了它的行为——这本身就是一次对"AI Coding Agent 究竟是什么"的工程拆解。

> "Claurst is an open-source, multi-provider terminal coding agent built from the ground up in Rust. It started as a clean-room reimplementation of Claude Code's behavior."
> — [GitHub README](https://github.com/Kuberwastaken/claurst)

---

## 为什么值得关注

### 1. Clean-Room 策略：不用源码，却能完整复刻

claurst 的起点是 Zed 的 Agent Client Protocol（ACP）规范加上对 Claude Code 行为的观察——不是逆向，而是**从产品需求出发重新实现**。

> "It started as a clean-room reimplementation of Claude Code's behavior (from [spec](https://github.com/kuberwastaken/claurst/tree/main/spec))"

这种思路的工程价值在于：它逼迫工程师去回答"Claude Code 的能力里，哪些是本质的、哪些是偶然的"——这是比直接抄代码更深的理解。

### 2. Rust 优先：性能与安全的双重收益

选择 Rust 不是炫技。对于一个需要长时间运行的本地 Agent：

- **内存效率**：不会像 Electron-based 工具那样吃掉 1GB+ 内存
- **启动速度**：毫秒级冷启动
- **类型安全**：复杂的 Agent 状态机需要 Rust 的类型系统来保证正确性

```bash
# 一键安装
curl -fsSL https://github.com/Kuberwastaken/claurst/releases/latest/download/install.sh | bash

# 或通过 npm/bun 安装
npm install -g claurst

# 设置 API Key
export ANTHROPIC_API_KEY=sk-ant-...

# 启动
claurst
```

### 3. Multi-Provider 支持：打破单一模型绑定

Claude Code 绑定了 Anthropic 的模型。claurst 从设计上是多 Provider 的——不只是 Claude，任何实现了对应 API 的模型都可以接入。

这对企业用户尤其重要：**可以在自托管模型和商业模型之间切换**，不需要换一个工具。

### 4. ACP 协议：编辑器集成的事实标准

claurst 使用 Agent Client Protocol（ACP）——这是 Zed 主导的编辑器到 Agent 通信协议。任何兼容 ACP 的编辑器（Zed、Neovim、JetBrains 插件）都可以把 claurst 作为后端驱动。

> "Claurst speaks the Agent Client Protocol (ACP) — the open protocol pioneered by Zed for editor-to-agent communication."

这意味着 claurst 不是一个孤立的 CLI，而是一个**可以被任何编辑器无缝集成的基础设施**。

---

## 关键特性一览

| 特性 | 说明 | 状态 |
|------|------|------|
| **Rust 实现** | 内存高效，启动快速 | ✅ Stable |
| **Multi-Provider** | 支持多种 LLM Provider | ✅ Stable |
| **TUI 界面** | 丰富的终端用户界面 | ✅ Stable |
| **ACP 协议** | 编辑器集成（Zed/Neovim/JetBrains）| ✅ Stable |
| **/goal 模式** | 多轮目标追踪（跨多轮而非单轮）| ⚡ Experimental |
| **/share 分享** | 通过 GitHub Gist 分享 Session | ⚡ Experimental |
| **Rustle 助手** | 内置 Rust 伴侣助手 | ⚡ Experimental |
| **Memory Consolidation** | 记忆整合 | ⚡ Experimental |
| **Plugin 系统** | 插件支持 | ⚡ Experimental |
| **无追踪/遥测** | 不收集任何使用数据 | ✅ |

---

## 笔者认为最值得关注的三个功能

### /goal：多轮目标驱动

这是 claurst 最有意思的实验性功能之一。普通的 CLI Agent 是**单轮模式**：你给一个指令，它完成就停止。/goal 模式让 claurst 持续追踪一个目标，跨越多个对话轮次。

> "Use `/goal <objective>` to see claurst keep working an objective, spanning multiple turns instead of stopping after one normal turn."

这解决了长时任务里"Agent 跑偏了不知道"的问题——目标始终在，上下文中 Agent 知道自己在为什么工作。

### /share：通过 Gist 分享 Session

> "Use `/share` to share chat sessions with others via unlisted GitHub Gists."

这和 Claude Code Artifacts 有异曲同工之妙——都是解决"Session 输出如何分享"的问题。只不过 claurst 用的是 GitHub Gist，Claude Code Artifacts 用的是 claude.ai 的私有 URL。

笔者认为这两条路径各有优势：Gist 更开放（任何人都可以查看），Artifact URL 更私密（需要组织认证）。

### Memory Consolidation

对于需要 Agent 记住上下文的长时开发，Memory Consolidation 是一个值得关注的方向。虽然文档还没有详细说明，但其设计方向是让 claurst 能够在多次 Session 之间保持记忆连续性。

---

## 竞品对比

| 项目 | 语言 | Stars | 多模型 | ACP 协议 | 隐私 |
|------|------|-------|--------|----------|------|
| **claurst** | Rust | 9,772 | ✅ | ✅ | 无遥测 |
| Claude Code | 闭源 | N/A | ❌ | ❌ | 受限 |
| Cursor | TypeScript | N/A | 部分 | ❌ | 受限 |
| Codex CLI | Python | N/A | 部分 | ❌ | 受限 |
| aider | Python | 9K+ | ✅ | ❌ | 无遥测 |
| swe-agent | Python | 5K+ | ✅ | ❌ | 无遥测 |

---

## 笔者的判断

claurst 的价值不只是"Claude Code 的开源替代"。

笔者认为它更重要的地方在于：**它证明了一个观点——Claude Code 的核心能力是可以被完整抽象和重新实现的**。不是复刻界面，是理解它解决了什么问题，然后用 Rust 的方式重新做一遍。

这对整个 AI Coding 工具链的演进有重要意义：

1. **基础设施层**：ACP 这样的开放协议让 Editor 集成 Agent 能力变成标准动作，不再是每个编辑器各自实现
2. **多模型路由**：Claude Code 的护城河是模型绑定的体验，claurst 把这个拆开了——用户可以自由选择模型
3. **本地化优先**：没有遥测，没有账号体系，直接跑在本地——这是企业采纳的重要条件

如果你在评估 AI Coding 工具的工程架构，claurst 的 SPEC 文档（`/spec` 目录）是一份非常好的参考——它把 Claude Code 的能力拆解成了可执行的规范。

---

## 快速体验

```bash
# Linux/macOS 一键安装
curl -fsSL https://github.com/Kuberwastaken/claurst/releases/latest/download/install.sh | bash

# Windows PowerShell
irm https://github.com/Kuberwastaken/claurst/releases/latest/download/install.ps1 | iex

# 设置 API Key
export ANTHROPIC_API_KEY=sk-ant-...

# 启动
claurst

# 设置免费模式（Experimental）
/connect

# 使用 /goal 追踪多轮目标
/goal 实现用户认证模块，包括注册、登录和 JWT 刷新
```

**GitHub**：[https://github.com/Kuberwastaken/claurst](https://github.com/Kuberwastaken/claurst)
**SPEC**：[https://github.com/kuberwastaken/claurst/tree/main/spec](https://github.com/kuberwastaken/claurst/tree/main/spec)
