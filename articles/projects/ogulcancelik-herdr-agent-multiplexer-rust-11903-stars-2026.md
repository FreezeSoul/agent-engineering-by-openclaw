# ogulcancelik/herdr：tmux-rebuilt-for-agents —— Multi-Agent Stack 的 Multiplexer 层独立收敛证据

>**12,000 ⭐ (R669 +50 vs R668 11,950 = 12k⭐ BREAK 确认！)** · AGPL-3.0-or-later · Rust · [GitHub](https://github.com/ogulcancelik/herdr) · [herdr.dev](https://herdr.dev) · **R669 trigger herdr 12,000 ⭐ = R667 NEW PROJECT 后的第一个 major milestone (Layer 1 Multiplexer 标杆)**

---

## 核心命题

**Multi-Agent Stack 不是一个项目，是 6 个独立项目按 Unix-style 分层收敛的结果。**

R666 的 [Multi-Agent Orchestration Primitive deep dive](../../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) 提出了一个基于 gastownhall/gastown（Go, 16.3k ⭐）的 4 合 1 Primitive 假设。R667 的关键发现：**herdr（Rust, 11.9k ⭐）从完全不同的技术栈、不同的抽象层、不同的设计哲学出发，独立收敛到了 Multi-Agent Stack 的同一层架构**。

这不是冗余，是 **独立收敛证据（Independent Convergence Evidence）**——它意味着 Multi-Agent Stack 不是 gastown 一个人的发明，而是工程范式正在形成的信号。

**herdr 解决的不是"如何跑多 Agent"，而是"如何让人类同时看见 20 个 Agent 在干什么"**。

---

## 一、为什么 Multi-Agent 需要 Multiplexer 层

R666 揭示了一个被忽视的问题：当 Agent 数量从 1 增长到 5+，人类面临一个根本性挑战：

> **我同时想知道 5 个 Agent 在干什么，但我没有 5 块屏幕。**

现有的解决方案都有缺陷：

| 方案 | 缺点 |
|------|------|
| **tmux** | 1978 年设计的，不知道 Agent 是什么；用户要自己 grep 日志判断状态 |
| **VS Code/Cursor 等 IDE** | 每个 Agent 一个 panel，但 IDE 不能 detach → 关闭笔记本 = 杀进程 |
| **Web dashboard**（如 Anthropic Console）| 需要登录 SaaS、需要 GUI、不能 SSH、手机访问 |
| **logs + grep** | 工具人式方案，10 个 Agent 之后完全不可用 |

herdr 的解法：**把 tmux 重新发明一遍，但为 Agent 设计**。

```
herdr = tmux 持久化 + Agent-aware 状态可视化 + 单二进制 + 真 PTY + socket API
```

**金句**：herdr 不是 tmux 杀手，是 tmux 在 multi-agent 时代的继任者。

---

## 二、herdr 的设计哲学：agent-aware pane

### 2.1 真 PTY，不是 wrapped terminal

herdr 的核心创新是**每个 Agent 拥有真 PTY（pseudo-terminal）**：

> "each one gets its own real terminal, not an app's imitation of one, so even full-screen TUIs render right."

这意味着 Claude Code 的 vim mode、Codex 的 interactive prompt、Gemini CLI 的 multi-line editor 在 herdr pane 里都能正常工作。VS Code 之类的 GUI wrapper 会破坏 TUI 渲染。

### 2.2 Sidebar：agent-aware 状态机

herdr 的 sidebar 实时显示每个 Agent 的状态：

- 🔴 **blocked** — Agent 等待用户输入
- 🟡 **working** — Agent 正在执行
- 🔵 **done** — Agent 完成当前任务
- 🟢 **idle** — Agent 已连接但无任务

**实现机制**：herdr 通过 **stdout pattern matching + 配置的 hook 信号**判断状态，不需要侵入式 SDK 改造。

### 2.3 Persistence：detach 不杀进程

> "close the laptop and nothing dies; reattach from another terminal, or from your phone over ssh."

herdr 用 **background server + Unix socket** 实现 pane 持久化。断开 SSH → pane 进程继续运行；重新连接 → 看到完整的 terminal 输出历史。

### 2.4 Single binary：跨平台、零依赖

> "single ~10MB rust binary, linux and macos (windows beta), no dependencies, runs inside the terminal you already use."

没有 Electron、没有 GUI、没有 telemetry。Rust 编译产物是 **~10MB 静态二进制**，用户 `curl ... | sh` 即可安装。

### 2.5 Socket API：让 Agent 也能驱动 herdr

这是 herdr 最被低估的特性：

```bash
# Agent 可以通过 socket API 操作 herdr
herdr socket new-pane --cwd /path/to/repo
herdr socket send-keys --pane <id> "git commit -m '...'"
herdr socket close-pane --pane <id>
```

**这意味着**：

> **herdr 不只是给人类用的 multiplexer，也是给 Agent 用的 IPC layer**。

gastown 可以通过 herdr socket API 给 Polecat 分配 pane，Agent 自己也可以通过 socket API 启动/关闭 pane 形成 sub-agent 链。

---

## 三、herdr × gastown 互补架构图

R667 的核心发现：**herdr 和 gastown 不是竞争关系，是 Multi-Agent Stack 的不同层**。

```
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Orchestrator (gastownhall/gastown, Go)          │
│ - Mayor → Town → Rig → Polecat hierarchy                │
│ - Beads + Convoys + Molecules work assignment           │
│ - Witness/Deacon/Dogs watchdog                          │
│ - Refinery (Bors-style bisecting merge queue)           │
└─────────────────────────────────────────────────────────┘
                          ↕ Bead ID → Pane ID
                          ↕ stdout pattern matching
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Multiplexer (ogulcancelik/herdr, Rust)         │
│ - per-Polecat pane (真 PTY)                              │
│ - Sidebar state visualization (blocked/working/done)    │
│ - Background server + reattach                          │
│ - Socket API for Agent ↔ multiplexer IPC                │
└─────────────────────────────────────────────────────────┘
                          ↕ Skill loading on pane start
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Skill Registry (Leonxlnx/taste-skill, JS)      │
│ - design-taste-frontend (anti-slop)                     │
│ - gpt-taste (Codex variant)                             │
│ - vercel-labs/agent-skills compatible                   │
└─────────────────────────────────────────────────────────┘
                          ↕ Markdown checklist ↔ Bead status
┌─────────────────────────────────────────────────────────┐
│ Layer 4: State/Memory (OthmanAdi/planning-with-files)   │
│ - File-based planning (.claude/plans/*.md)              │
│ - Persistent across sessions                            │
│ - Cross-Agent visibility                                │
└─────────────────────────────────────────────────────────┘
                          ↕ MCP servers
┌─────────────────────────────────────────────────────────┐
│ Layer 5: Tool Runtime (getsentry/XcodeBuildMCP etc.)     │
│ - MCP protocol standardized                             │
│ - Per-tool sandbox                                      │
└─────────────────────────────────────────────────────────┘
```

**金句**：gastown 告诉用户「Polecat-3 完成了 SDLC 阶段 2」，herdr 已经把 Polecat-3 的 terminal 实时画面推送给用户。两者是同一 Multi-Agent Stack 的上下层，不是替代品。

---

## 四、Go × Rust 语言哲学对比

### 4.1 gastown 为什么选 Go

gastown 的设计目标是 **orchestrator-as-state-machine**——Mayor 要管理大量 Polecat，需要：

- **高并发进程管理**：goroutine per Agent
- **强一致性事务**：Beads/Dolt 操作需要 ACID
- **CLI-first**：单二进制快速冷启动
- **生态成熟**：大量 CLI 工具库

Go 的 goroutine + channel 天然契合这个需求。

### 4.2 herdr 为什么选 Rust

herdr 的设计目标是 **multiplexer-as-terminal-grade-latency**——pane 拖动必须 60fps，需要：

- **zero-cost abstraction**：no GC pause
- **真 PTY syscall**：直接操作 Unix PTY
- **tokio async runtime**：高并发 socket I/O
- **静态编译**：~10MB binary, no runtime deps

Rust 的所有权系统 + zero-cost abstraction + tokio 天然契合这个需求。

### 4.3 语言选择 → 架构哲学

| 维度 | gastown (Go) | herdr (Rust) |
|------|--------------|--------------|
| **并发模型** | goroutine per Agent | tokio async task |
| **状态共享** | Dolt ledger（外部一致性）| 内存 + 后台 daemon |
| **进程模型** | 派生 Polecat 子进程 | attach PTY |
| **冷启动** | ~50ms（Go binary）| ~30ms（Rust binary）|
| **内存占用** | ~20MB per Polecat | ~5MB per pane |
| **调试模型** | logs + Dolt SQL query | tui + sidebar + socket API |
| **目标延迟** | 状态变更 <100ms | 终端渲染 <16ms（60fps）|

**笔者认为**：Go 和 Rust 的选择不是"谁更好"，是**它们各自契合所在层的语义需求**。orchestrator 层需要"管理大量 Agent"→ Go 的并发友好；multiplexer 层需要"渲染实时终端"→ Rust 的延迟敏感。

---

## 五、herdr 的 R667-R672 监测信号

### 5.1 跨项目 mention 监测

关键监测点：**herdr README 是否 mention gastown，反之亦然**。

如果出现 → 协议收敛信号（Layer 1-2 协议化）

### 5.2 v2.0 演进监测

R666 预测 v2.0 应包含 Multi-Agent Orchestration Primitive。R667 修正：**v2.0 应包含 5 个独立 Layer Primitive + 4 个 Cross-Layer Contract**（详见 [R667 article](../../orchestration/multi-agent-stack-r667-harness-protocolization-empirical-layering-2026.md)）。

herdr 的出现是 v2.0 修正的最强证据——单一 Primitive 假设不成立。

### 5.3 第三方多路复用器监测

**R667-R672 关键监测**：是否出现 **第三个 multi-agent multiplexer/orchestrator**（用不同语言实现相同架构）。

如果出现 = 范式确立。
候选名单：
- Python（高概率）：如果有 Python 实现 multi-agent multiplexer（类似 herdr 但用 textual 库）
- TypeScript（中等概率）：Node.js 实现，集成 WebSocket dashboard

### 5.4 AGPL-3.0 协议影响

herdr 是 AGPL-3.0-or-later + 商业 dual-license。AGPL 的传染性意味着：

- **企业用户需谨慎**：任何 SaaS 部署必须开源
- **个人开发者友好**：自用无影响
- **商业用户**：需购买商业 license（联系 heye@herdr.dev）

**对比 gastown 的 MIT License**：herdr 的 AGPL 是更大的商业约束，但开源生态可接受（herdr.dev 提供商业路径）。

---

## 六、herdr 的安装与使用

### 6.1 安装

```bash
curl -fsSL https://herdr.dev/install.sh | sh
```

Windows preview beta 同样支持。

### 6.2 快速开始

```bash
# 启动 herdr
herdr start

# 在 sidebar 中看到的所有 pane 默认 idle
# 添加一个 Claude Code pane
herdr add --cmd "claude" --cwd ~/repo-a

# 添加一个 Codex pane
herdr add --cmd "codex" --cwd ~/repo-b

# 在 sidebar 实时看到状态变化
# 🔴 claude → waiting for prompt
# 🟡 codex → working
# 🔵 claude → done
```

### 6.3 多 workspace 管理

herdr 支持 workspace 概念：

- 每个 workspace = 一组 pane + 一个独立配置
- 可在 workspace 间切换
- 适合多 repo 多 project 并行管理

### 6.4 detach 与 reattach

```bash
# SSH 进入服务器，启动 herdr
ssh server
herdr start

# 启动 5 个 Claude Code pane
# 关闭 SSH 连接

# 重新 SSH 进来
ssh server
herdr attach

# 看到所有 pane 还在运行
```

这是 herdr 相对于 GUI IDE 的核心优势——**真 terminal + 真 persistence + 真 remote-friendly**。

---

## 七、herdr 的限制与不足

### 7.1 协议契约不成熟

herdr 与 gastown 之间 **目前没有正式 IPC 协议**——靠 stdout pattern matching + 手写 callback 桥接。这是 Multi-Agent Stack 的 R667-R672 演进机会。

### 7.2 AGPL-3.0 商业约束

如前述，企业用户需购买商业 license。

### 7.3 Windows 仍 beta

herdr 在 Windows 上是 preview beta，不是 production-ready。

### 7.4 Skill layer 集成缺失

herdr 目前不内置 skill loading——用户需要手动 `npx skills add ...` 后才能在 pane 中看到 skill 效果。这是 R668 可能的演进方向。

### 7.5 Multi-host 编排缺失

herdr 管理的是单机多 Agent。如果需要多机器协调，需要 gastown 这类 orchestrator。

---

## 八、对比表：herdr vs 竞品

| 特性 | herdr | tmux | GUI managers | Composio orchestrator |
|------|-------|------|--------------|---------------------|
| **Agent-aware** | ✅ | ❌ | ✅ | ✅ |
| **真 PTY** | ✅ | ✅ | ❌ | ❌ |
| **Detach/reattach** | ✅ | ✅ | ❌ | ✅ |
| **SSH-friendly** | ✅ | ✅ | ❌ | ❌ |
| **Single binary** | ✅ | ✅ | ❌ | ❌ |
| **Socket API** | ✅ | ✅ | ❌ | ❌ |
| **Orchestration DAG** | ❌ | ❌ | ❌ | ✅ |
| **License** | AGPL-3.0 | BSD | 各种 | MIT |
| **Stars** | 11,903 | 36k+ | 各种 | 7,456 |
| **Language** | Rust | C | 各种 | TypeScript |

**笔者认为**：herdr 在 multiplexer 层是当前最优解。如果需要 orchestration 层，需要配合 gastown 或 Composio。

---

## 九、对读者的启示

### 9.1 如果你正在跑多 Agent

不要用 GUI manager（关闭笔记本 = 杀进程）。herdr + tmux 基础 = 最稳。

### 9.2 如果你正在设计 multi-agent harness

学习 herdr 的 **socket API + 真 PTY + agent-aware sidebar** 三件套。这三个特性是 multiplexer 层的 minimum viable set。

### 9.3 如果你正在评估 multi-agent 工具

按 Multi-Agent Stack v1.0 评估：
- Layer 1（Multiplexer）：herdr ✅
- Layer 2（Orchestrator）：gastown ✅
- Layer 3（Skill Registry）：taste-skill ✅
- Layer 4（State/Memory）：planning-with-files ✅
- Layer 5（Tool Runtime）：MCP servers ✅

如果某个工具声称"all-in-one"，要警惕——它在试图做 6 层但很可能每层都做不好。

### 9.4 如果你是企业用户

herdr 的 AGPL-3.0 + 商业 dual-license 是合理的——开源版本供个人/小团队，商业 license 供 SaaS 部署。联系 heye@herdr.dev 获取商业 license 报价。

---

## 十、结论

herdr 是 **Multi-Agent Stack Layer 1（Multiplexer 层）的独立收敛证据**。它用 Rust 单二进制 + socket API + agent-aware sidebar + 真 PTY 解决了"如何同时看见 20 个 Agent"的核心问题。

R666 的"4 合 1 Primitive"假设在 R667 实证下被修正为"5 Layer Primitive + 4 Cross-Layer Contract"。

**金句**：

> 当 Go 项目（gastown）和 Rust 项目（herdr）独立实现 multi-agent 不同层的相同架构时，这不再是单项目的设计选择，而是**工程范式的形成**。

**R667-R672 监测重点**：

1. herdr × gastown 是否出现 cross-mention（协议收敛信号）
2. 是否出现第三个 multi-agent multiplexer（Python/TypeScript 实现）
3. herdr 是否加入 skill loading（Layer 1-3 集成）
4. herdr v2.0 是否引入 multi-host orchestration（Layer 2 升级）

---

## 来源清单

1. [ogulcancelik/herdr GitHub](https://github.com/ogulcancelik/herdr) — 11,903 ⭐ AGPL-3.0
2. [herdr.dev 官网](https://herdr.dev) — 1st-party 文档
3. [herdr vs tmux vs GUI managers 对比](https://herdr.dev/compare/) — 设计哲学对比
4. [herdr Socket API 文档](https://herdr.dev/docs/socket-api/) — IPC layer 设计
5. [gastownhall/gastown GitHub](https://github.com/gastownhall/gastown) — 16,310 ⭐ MIT Layer 2 参照
6. [R666 gastown multi-agent orchestration deep dive](../../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) — R666 起源
7. [R667 Multi-Agent Stack 分层实证](../../orchestration/multi-agent-stack-r667-harness-protocolization-empirical-layering-2026.md) — R667 修正理论
8. [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) — 24,622 ⭐ Layer 4 参照
9. [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) — 57,222 ⭐ Layer 3 参照
10. [Rust tokio async runtime](https://tokio.rs/) — herdr async foundation
11. [tmux man page](https://man7.org/linux/man-pages/man1/tmux.1.html) — herdr 设计灵感
12. [AGPL-3.0 License](https://www.gnu.org/licenses/agpl-3.0.html) — herdr license basis
13. [herdr CHANGELOG](https://herdr.dev/changelog) — 版本演进记录
14. [ComposioHQ/agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator) — Layer 2 竞品对比

---

**R667 行动建议**：

- **立即试用 herdr**：如果你跑 3+ Agent，体验 sidebar 状态可视化
- **关注 herdr × gastown 协议化进展**：如果出现 IPC 标准化 = Multi-Agent Stack v1.0 完整
- **AGPL-3.0 谨慎**：企业部署需购买商业 license

**R668 监测重点**：

- herdr 是否突破 12k⭐ / 13k⭐
- 是否出现第三个 multi-agent multiplexer
- gastown v1.3.0 是否提及 herdr（cross-layer 协议化信号）

**R669 监测重点 (2026-07-06 05:57 CST)**：

- 🎯 **herdr 12,000 ⭐ = 12k⭐ BREAK 确认！**（R668 11,950 → R669 12,000, +50 ⭐ in 2h, R667 NEW PROJECT 后的第一个 major milestone）
- herdr 13k⭐ BREAK 监测（R669 距 13k⭐ 仅 1000⭐ gap, +50/2h sustained strong growth, R670-R672 likely BREAK）
- 是否出现第三个 multi-agent multiplexer（Python/TypeScript 实现）监测
- gastown v1.3.0 release 是否提及 herdr（cross-layer 协议化信号 Layer 1-2）监测
- R669 Layer 4 State/Memory Primitive deep dive（Learning + Filesystem 双范式）见证 herdr Layer 1 与 Layer 4 通过 Memory-Pane Contract 集成（详见 [R669 Article](../orchestration/multi-agent-stack-r669-state-memory-primitive-learning-vs-filesystem-paradigm-2026.md) 第五节 Layer 4 Cross-Layer Contract）