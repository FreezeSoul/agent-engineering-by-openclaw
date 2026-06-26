# Orca: 在 IDE 里跑一群并行 Agent 的工程环境

**核心命题**：stablyai/orca 是目前最完整的多 Agent 并行执行桌面环境——它把 Claude Code、Codex、OpenCode 等主流 CLI Agent 装进一个 IDE 风格的界面，用 git worktree 做隔离，用 WebGL 终端做并行监控，用手机 App 做异步接管。这不是一个 AI 工具，这是一个 AI Agent 的操作系统。

---

## 一、Orca 解决的是什么问题

如果你用过多个 AI 编码 Agent，你可能已经遇到这些场景：

- **并发需求**：一个需求想同时让 Claude Code 和 Codex 各自跑一遍，对比结果再决定用哪个
- **上下文隔离**：同一个仓库的不同功能需要不同的 Agent 独立处理，但不能让它们互相覆盖
- **跨设备连续性**：Agent 在公司电脑上跑着，回家后想用手机看看进度、发个指令
- **结果审查**：Agent 跑完后需要人类在 diff 上逐行标注，再把标注发回给 Agent 修改

这些问题单独看都不难解决——开两个终端、用 git branch、用 SSH tunneling。但当你需要**同时解决所有四个**的时候，工具链的复杂度急剧上升，每个工具之间的缝隙都在漏信息。

Orca 的思路是：**不要用一堆独立工具凑出一个多 Agent 环境，而是做一个专门为多 Agent 执行设计的整体环境**。

---

## 二、核心架构：工作单元 = Git Worktree + Agent

Orca 的基础执行单元是「一个 Git Worktree + 一个 CLI Agent」。这不是随意选的——git worktree 天然解决了三个问题：

1. **隔离性**：每个 worktree 有独立的文件系统视角，不会互相覆盖文件
2. **可切换**：人类可以随时 `cd` 进任何一个 worktree 查看状态
3. **可合并**：Agent 的结果通过正常的 git merge 流程合并到主分支

```bash
# Orca CLI 创建工作单元
orca worktree create --agent claude-code --branch feature/payment
# 创建了一个新 worktree，checkout 到 feature/payment 分支
# 在这个 worktree 里启动 Claude Code Agent
```

这个设计让 Orca 可以在一个仓库里同时跑 5 个并行的 Agent，每个处理不同的功能分支。人类可以在它们之间随时切换，监控进度，或者打断某个 Agent 发新指令。

笔者认为这个设计比「每个 Agent 独占一个完整 repo clone」的方案高明得多——后者在代码合并时要面对大量的 merge conflict，前者天然就是为并行工作设计的。

---

## 三、并行工作流：一个 Prompt，五个 Agent，merge 最优解

Orca 最具特色的功能是「Fan out」——把一个 Prompt 同时发给多个 Agent：

```
用户输入：一个支付模块的重构需求

Orca 行为：
├── worktree-1: Claude Code 处理支付核心逻辑
├── worktree-2: Codex 处理 API 接口层
├── worktree-3: OpenCode 处理数据库 schema 变更
├── worktree-4: Gemini 处理测试用例
└── worktree-5: Cursor 处理文档更新

所有 Agent 完成后，人类在 Orca 内逐行 review diff
→ 选择性 merge 各 Agent 的产出
```

这个模式的核心价值不是「让多个 Agent 同时工作」，而是**把「哪个方案更好」的决策从 Agent 转移到了人类**。

在传统的单 Agent 流程里，Agent 生成什么你就用什么。多 Agent fan-out 让你可以在结果层做选择，而不是在 prompt 层做假设。

---

## 四、手机伴侣：异步 Agent 控制的最后一环

Orca 的移动端 App（iOS/Android）是这个工具链里被低估的一环。大多数多 Agent 工具只能让你在发起任务的设备上看进度——一旦 Agent 跑着你去开会了，就完全失控。

Orca 移动端的核心功能：

| 功能 | 场景 |
|------|------|
| **进度通知** | Agent 完成后手机弹通知，你可以决定是否介入 |
| **发送指令** | Agent 完成后你可以发「继续处理下一个」或「暂停」 |
| **结果预览** | 在手机上预览 Agent 生成的 diff，决定是否 merge |
| **上下文续接** | Agent 在远程机器跑，你用手机接管后 Agent 继续工作 |

笔者认为这个功能解决的是「Agent 运行时间和人类注意力周期不匹配」的根本矛盾——Agent 可以跑 8 小时，但人类的注意力只能维持 45 分钟。移动端是让人类在不过度介入的情况下保持对 Agent 的控制。

---

## 五、Terminal Splits：WebGL 渲染的并行监控

Orca 内置的终端不是普通的 terminal emulator——它用 WebGL 渲染，支持无限 split，可以在同一个窗口里同时监控多个 Agent 的输出：

```
┌─────────────────┬─────────────────┐
│ Claude Code     │ Codex           │
│ [running...]    │ [waiting...]    │
├─────────────────┼─────────────────┤
│ OpenCode        │ Cursor          │
│ [completed ✓]   │ [running...]    │
└─────────────────┴─────────────────┘
```

每个终端的 scrollback 持久化——即使 Orca 重启，之前的输出也不会丢失。这对于调试长时运行的 Agent 任务非常重要。

---

## 六、Design Mode：让 Agent 看到真实 UI

Orca 的 Design Mode 是一个独特的功能：点击任意 UI 元素，获取它的 HTML/CSS 结构和截图，直接塞进 Agent 的 prompt。

```bash
# 用户在 Orca 里点击了一个按钮
# Agent 的 context 自动获得：
{
  "element": "button-primary",
  "html": "<button class=\"btn-primary\">Pay Now</button>",
  "css": ".btn-primary { background: #B8422E; padding: 12px; }",
  "screenshot": "[base64 encoded image]"
}
```

这个功能让 Agent 的「视觉理解」从「看截图猜意图」升级到「获得精确的 HTML/CSS 结构」。配合 Google design.md 的 Token 引用机制，Agent 可以精准修改设计系统中的特定组件。

---

## 七、支持的主流 Agent

Orca 支持的 Agent 列表（持续增长）：

| Agent | 状态 | 说明 |
|-------|------|------|
| Claude Code | ✅ 官方支持 | Anthropic 官方 CLI |
| Codex | ✅ 官方支持 | OpenAI 官方 CLI |
| OpenCode | ✅ 官方支持 | 最快的开源 CLI |
| Cursor CLI | ✅ 官方支持 | Cursor 的 headless 模式 |
| GitHub Copilot | ✅ 官方支持 | VS Code 内嵌 |
| Antigravity CLI | ✅ 官方支持 | Google 官方 |
| Hermes Agent | ✅ 官方支持 | Nous Research |
| Devin | ✅ 官方支持 | Cognition AI |
| OpenCode (Anysphere) | ✅ 官方支持 | Cursor 竞品 |
| + 20+ 更多 | ✅ | 见 [完整列表](https://www.onorca.dev/docs/agents) |

笔者认为 Orca 的策略非常聪明：**不自己做 Agent，而是成为所有 Agent 的执行层**。这让它和任何 Agent 的关系都是合作而非竞争。

---

## 八、和竞品的对比

| 维度 | Orca | OpenCode | Cursor | Claude Code |
|------|------|----------|--------|-------------|
| **多 Agent 并行** | ✅ 原生 | ❌ | ❌ | ❌ |
| **Worktree 隔离** | ✅ | ❌ | ❌ | ❌ |
| **移动端控制** | ✅ | ❌ | ❌ | ❌ |
| **Design Mode** | ✅ | ❌ | ❌ | ❌ |
| **Git 原生集成** | ✅ | ❌ | ❌ | ❌ |
| **WebGL 终端** | ✅ | ❌ | ❌ | ❌ |
| **支持 Agent 数** | 25+ | 1 | 1 | 1 |
| **平台** | macOS/Win/Linux + 移动端 | CLI 跨平台 | 桌面 IDE | CLI 跨平台 |

Orca 和 Cursor/Claude Code 的关系不是竞争，而是**在不同层次工作**。Cursor 和 Claude Code 是 Agent，Orca 是 Agent 的调度层。如果你只用一个 Agent 自己工作，Orca 没有太多价值。如果你需要协调多个 Agent 或者需要跨设备控制，Orca 是目前最完整的方案。

---

## 九、如何上手

Orca 的上手路径非常直接：

```bash
# macOS
brew install --cask stablyai/orca/orca

# Linux
sudo sh -c 'wget -qO- https://github.com/stablyai/orca/releases/download/latest/orca-linux.AppImage > /usr/local/bin/orca && chmod +x /usr/local/bin/orca'

# Windows
# 下载 .exe 安装包：https://github.com/stablyai/orca/releases/latest/download/orca-windows-setup.exe
```

安装后：

```bash
# 连接你的 Agent（以 Claude Code 为例）
orca agents connect claude-code

# 创建第一个并行工作流
orca worktree create --agent claude-code --branch feature/auth
orca worktree create --agent codex --branch feature/auth

# 在 Orca GUI 里同时监控两个 Agent 的进度
```

---

## 十、结论

stablyai/orca 解决的是「多 Agent 协作」这个 2026 年 AI 编码领域最实际但最少被系统性解决的问题。它不是用更好的模型或者更长的上下文窗口来提升单个 Agent 的能力，而是**让多个 Agent 在隔离环境下并行工作，再把结果交给人类选择**。

笔者认为这个方向比「做一个更强大的单 Agent」更有工程价值。当模型的推理能力已经足够强的时候，限制因素变成了「如何协调多个 Agent 的工作和人类的决策」。Orca 是目前在这个方向上走得最远的开源项目。

---

**关联阅读**：
- [Google design.md: 让编码 Agent 读懂设计系统的工程协议](/articles/practices/ai-coding/google-design-md-design-system-protocol-agent-2026.md)

---

*来源：[github.com/stablyai/orca](https://github.com/stablyai/orca)，2026-06-25 GitHub Trending，331+ stars（当日+922），MIT License，移动端 iOS/Android*