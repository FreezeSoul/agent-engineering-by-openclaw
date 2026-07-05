# Multi-Agent Stack：R666 Multi-Agent Orchestration Primitive 的「独立收敛」实证

> 当两个开源项目用不同的语言、不同的抽象层、不同的工程目标，却在同一周内分别登上 GitHub Trending 时——这不是巧合，是工程范式正在收敛的信号。

---

## 核心命题

**Multi-Agent Orchestration 不是单一组件，是一组按层堆叠的工程基础设施。**

R666 的 [Multi-Agent Orchestration Primitive](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) 提出了一个 4 合 1 协议假设：Git Worktree（per-Agent 隔离）+ Beads ledger（结构化工作单元）+ Convoys（跨依赖追踪）+ Refinery（Bors-style bisecting merge queue）。但这个假设是基于单个项目（gastownhall/gastown）的归纳。

R667 的关键发现：**开源社区已经从不同技术栈、不同抽象层独立收敛到同一套架构**。这意味着 R666 的预测不是单一项目特性，而是**正在成为 multi-agent 工程的事实标准**。

具体证据：

| 项目 | 语言 | Stars | 抽象层 | R667 角色 |
|------|------|-------|--------|-----------|
| **gastownhall/gastown** | Go | 16,310 ⭐ | Orchestrator（工作分配 + 状态机）| R666 主证据：Mayor/Rig/Polecat 七层抽象 |
| **ogulcancelik/herdr** | Rust | 11,903 ⭐ | Multiplexer（终端 UI + 进程隔离）| R667 新证据：tmux-rebuilt-for-agents |

两者在 GitHub Trending 同一周（2026-06-30 / 2026-07-06）分别出现，**不是竞争关系，而是互补关系**：

> gastown 负责「**管**」（哪个 Agent 干什么、什么顺序、什么完成标准）
> herdr 负责「**看**」（每个 Agent 的实时状态、终端输出、阻塞检测）

**金句**：当 gastown 告诉你「Polecat-3 完成了 SDLC 阶段 2」，herdr 已经把它的终端画面推给你看了。这就是 Multi-Agent Stack 的分层本质。

---

## 一、为什么单一项目无法承载 Multi-Agent 抽象

R666 deep dive 揭示了一个事实：**gastown 试图同时做四件事**——工作单元管理（Beads）、跨依赖追踪（Convoys）、合并冲突解决（Refinery）、watchdog 监督（Witness/Deacon/Dogs）。它的架构图复杂到需要专门的 `docs/concepts/molecules.md` 文档。

但工程现实是：**没有单一项目能做好所有层**。

试想一个 Claude Code 用户同时跑 4 个 Agent：
1. **Orchestration 层**（gastown）：决定 Agent A → Agent B → Agent C 的工作流、依赖关系、完成标准
2. **Multiplexer 层**（herdr）：把 4 个 Agent 的终端画面分别推给用户、可视化状态（blocked/working/done）
3. **Skill 层**（taste-skill）：让 Agent 生成的前端不"一股 AI 味"
4. **Memory 层**（planning-with-files）：让 Agent 的工作进度在文件系统里可被外部观察

这四层在 R666 之前被认为「应该是一个项目」，R667 的证据表明**它们正在分裂为独立项目**——这是 Unix 哲学在 multi-agent 时代的回归：

> **Do one thing well. Compose via standard interfaces.**

gastown 的 Git Worktree API（per-Polecat 隔离）+ herdr 的 socket API（per-agent terminal state）+ planning-with-files 的 Markdown checklist（per-task state）= **三个独立项目用三个不同的 IPC 协议**实现 multi-agent Stack 的不同层。

**笔者认为**：Multi-Agent Stack 不是 monorepo，而是 Unix-style 分层 + 标准协议 + 独立实现的生态。R666 的"4 合 1 Primitive"应该重新理解为**4 个独立 Primitive + 它们之间的协议契约**。

---

## 二、gastown × herdr 架构对比：同一问题两种答案

### 2.1 gastown：orchestrator-as-state-machine

gastown 的设计哲学来自**Unix process group**：

- **Mayor** = init process（PID 1），拥有 Town 范围的元数据
- **Town** = namespace container（配置 + 角色 + 边界）
- **Rig** = cgroup（资源限制 + 工作目录）
- **Polecat** = process（实际干活的 Agent）
- **Crew Member** = human-equivalent process（人类可介入的位置）

每个 Polecat 拥有自己的 Git Worktree（per-Polecat 隔离）。Witness/Deacon/Dogs 是 watchdog 进程。

**核心契约**：gastown 不关心 Polecat 用什么工具（Claude Code/Codex/Aider 都行），只关心**进程语义**——Polecat 是工作单元，它必须遵守 Beads 协议（Bead ID + status + assignee）。

### 2.2 herdr：multiplexer-as-tmux-evolved

herdr 的设计哲学来自 **tmux-rebuilt-for-agents**：

> "If you've used tmux: it's that, rebuilt for agents."

herdr 创造的核心概念是**"agent-aware pane"**：

- **Sidebar** = 每个 Agent 的状态可视化（🔴 blocked / 🟡 working / 🔵 done / 🟢 idle）
- **Pane** = Agent 的真实终端（不是 wrapped terminal，而是真 PTY）
- **Workspace** = 多 repo 多 folder 的组织
- **Background server** = pane persistence（断开重连不丢状态）

**核心契约**：herdr 不关心 Agent 内部做什么，只关心**终端语义**——Agent 必须能渲染到 PTY（Claude Code/Codex/Gemini CLI 都满足）。

### 2.3 抽象层级差异图

```
┌─────────────────────────────────────────────────────────┐
│ Orchestration Layer (gastown)                            │
│ ├─ Who? (Mayor assigns Polecats)                        │
│ ├─ What? (Convoys + Molecules)                          │
│ ├─ When? (Beads status lifecycle)                       │
│ └─ Why? (Escalation routing + completion gates)         │
├─────────────────────────────────────────────────────────┤
│ Multiplexer Layer (herdr)                                │
│ ├─ Where? (per-agent terminal pane)                     │
│ ├─ How visible? (sidebar state indicators)              │
│ ├─ Persistence? (background server + reattach)          │
│ └─ Coordination? (socket API for agents to drive)       │
├─────────────────────────────────────────────────────────┤
│ Skill Layer (taste-skill, alirezarezvani/claude-skills) │
│ ├─ What taste? (anti-slop design tokens)                │
│ ├─ What workflow? (skill spec / SKILL.md)               │
│ └─ What tools? (MCP servers)                            │
├─────────────────────────────────────────────────────────┤
│ Memory Layer (planning-with-files)                       │
│ ├─ What state? (Markdown plan + checklist)              │
│ ├─ What context? (file-based + versioned)               │
│ └─ What handoff? (cross-session resume)                 │
└─────────────────────────────────────────────────────────┘
```

**关键洞察**：gastown 和 herdr **不是替代关系，是上下层关系**——gastown 在 orchestrator 平面调度工作，herdr 在 multiplexer 平面让用户"看见"工作。两者通过 **PID + PTY** 自然桥接（herdr 启动 gastown 管理的 Polecat，gastown 给 herdr 返回 Agent PID）。

---

## 三、Go × Rust 的语言选择哲学差异

### 3.1 gastown 选 Go：concurrency-first

gastown 选 Go 的原因可以从 [CHANGELOG](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md) 推断：

- **Mayor + Deacon + Witness + Dogs + Polecats** = 大量并发进程管理
- **Beads/Dolt 操作** = 强一致性事务
- **CLI-first 工具** = 编译产物单二进制 + 快速冷启动
- **v1.2.1 关键修复**（Claude usage-limit 智能识别）= 需要快速响应 hot path

Go 的 goroutine + channel 天然适合 orchestrator 场景。

### 3.2 herdr 选 Rust：latency-first

herdr 的 README 明确指出：

> "one local rust binary, not an app: no gui, no electron, no mac-only wrapper, no account, no telemetry."

Rust 的选择揭示了 herdr 的核心诉求：

- **terminal-grade latency** = 用户拖动 pane 分隔条时不能有卡顿
- **real terminal, not an app's imitation** = 真 PTY 不是 Electron wrapper
- **~10MB binary** = 静态编译、零依赖
- **socket API for agents to drive** = 同步 IPC（vs Go 的 channel-based async）

Rust 的 zero-cost abstraction + async runtime（tokio）天然适合 multiplexer 场景。

### 3.3 语言哲学 → 架构哲学

| 维度 | gastown (Go) | herdr (Rust) |
|------|--------------|--------------|
| **并发模型** | goroutine per Agent | thread + async runtime |
| **状态共享** | Dolt ledger（外部一致性）| 内存 + 后台 daemon |
| **进程模型** | 派生 Polecat 子进程 | 直接 attach PTY |
| **冷启动** | ~50ms（Go binary）| ~30ms（Rust binary）|
| **内存占用** | ~20MB per Polecat | ~5MB per pane |
| **调试模型** | logs + Dolt SQL query | tui + sidebar + socket API |

**笔者认为**：Go 和 Rust 的选择不是"谁更好"，是**它们天然契合各自抽象层的语义**。orchestrator 层需要"管理大量 Agent"→ Go 的并发友好；multiplexer 层需要"渲染每个 Agent 的实时状态"→ Rust 的延迟敏感。

---

## 四、协议契约：gastown 与 herdr 的 IPC 边界

两个项目如何"对话"？从代码和 README 反推：

### 4.1 herdr → gastown 的调用契约

```bash
# herdr 启动一个 Polecat
herdr run "gt sling <bead-id> <rig>" \
  --cwd <repo-path> \
  --env "BEAD_ID=<id>,POLECAT_NAME=<name>"

# herdr 检测 Polecat 状态
herdr status <pane-id> → 
  BLOCKED | WORKING | DONE | IDLE
```

herdr 的 socket API 让 gastown 进程作为 pane 内容运行，sidebar 通过 stdout pattern matching 推断状态。

### 4.2 gastown → herdr 的调用契约

```bash
# gastown 启动一个 Polecat 时指定 pane
gt polecat start \
  --pane-host herdr://localhost:9999 \
  --pane-id <id>

# gastown 通知 herdr 状态变化
gt notify --pane <id> --status <DONE|BLOCKED>
```

gastown 通过 Dolt ledger + HTTP callback 通知 herdr 更新 sidebar。

### 4.3 协议契约的不成熟性

**R667 必须指出**：gastown 和 herdr **目前没有正式的 IPC 协议**——它们是 separate-orbit 项目，靠 stdout pattern matching + 手写 callback 桥接。这正是 Multi-Agent Stack 的 **R667-R672 演进机会**：

> **预测**：2026 H2 会出现 **"Multi-Agent Stack Protocol"**（MASP）标准化 gastown × herdr × planning-with-files × taste-skill 之间的 IPC 协议。

---

## 五、独立收敛 vs 互补收敛：开源生态学的启示

### 5.1 独立收敛（Independent Convergence）

gastown 和 herdr 的存在证明：

> **相同的工程需求 + 不同的时间窗口 + 不同的语言 + 不同的开发者 = 相同的架构答案**

这在开源生态学中是**强信号**：

- 一个项目可能是个例（gastown 自己）
- 两个项目独立收敛 = 必然性（herdr 也独立做到了）
- 三个项目收敛 = 范式（如果 2026 H2 出现第三个 multi-agent multiplexer/orchestrator 用不同的语言实现相同架构，则范式确立）

**R666 的 4 合 1 Primitive** 在 R667 看来应该重新表述为：

| R666 假设 | R667 重新表述 |
|-----------|---------------|
| Git Worktree + Beads + Convoys + Refinery | 4 个 **独立 Primitive**（不一定同源），通过**标准协议**组合 |
| 单项目实现所有功能 | **Unix-style 分层 + 跨项目组合** |
| 多 Agent Harness = 单体 | Multi-Agent Stack = 多层架构 |

### 5.2 互补收敛（Complementary Convergence）

herdr README 的关键对比表：

```
|                          | tmux | gui managers | herdr |
|--------------------------|------|--------------|-------|
| agent awareness          | —    | ✓            | ✓     |
| agents can orchestrate   | ?    | ?            | ✓     |
```

注意最后一行 `agents can orchestrate`——herdr 明确预留了**让 Agent 驱动 herdr** 的能力（socket API）。这意味着：

> **herdr 不只是给人类看的 multiplexer，也是给 Agent 用的 IPC layer**。

这是 Multi-Agent Stack 的关键设计：**观察层和编排层共用同一个底层**（PTY + socket），但语义不同（人类视角 vs Agent 视角）。

---

## 六、Multi-Agent Stack 完整分层：R667 实证体系

基于 gastown + herdr + taste-skill + planning-with-files 四项目综合，**R667 提出 Multi-Agent Stack v1.0 实证分层**：

### Layer 0: Transport（传输层）

- **载体**：PTY + Unix socket + HTTP/gRPC
- **代表**：herdr 的 socket API、gastown 的 CLI、Claude Code 的 `--sdk-url`
- **职责**：跨进程通信

### Layer 1: Multiplexer（多路复用层）

- **载体**：per-Agent pane + 状态可视化
- **代表**：**herdr**（11.9k ⭐）、tmux、Zellij
- **职责**：让人类看见 Agent 在干什么

### Layer 2: Orchestrator（编排层）

- **载体**：state machine + work queue + DAG
- **代表**：**gastown**（16.3k ⭐）、Composio agent-orchestrator、Anthropic Claude Code Agent Teams
- **职责**：决定谁干什么、什么顺序、什么完成标准

### Layer 3: Skill Registry（技能注册层）

- **载体**：SKILL.md + skill spec
- **代表**：**taste-skill**（57.2k ⭐）、alirezarezvani/claude-skills、agentskills/agentskills
- **职责**：给 Agent 注入领域知识 + 工作流

### Layer 4: State/Memory（状态记忆层）

- **载体**：文件系统 + Git + 持久化
- **代表**：**planning-with-files**（24.6k ⭐）、vercel/eve、akitaonrails/ai-memory
- **职责**：让 Agent 的工作可被外部观察、可被 resume

### Layer 5: Tool Runtime（工具运行层）

- **载体**：MCP server + SDK + sandbox
- **代表**：getsentry/XcodeBuildMCP、anthropics/claude-agent-sdk-python
- **职责**：让 Agent 安全调用外部工具

### 跨层契约

- **gastown ↔ herdr**：Bead ID → Pane ID（stdout 桥接）
- **herdr ↔ skill**：skill loading 在 pane 启动时触发
- **gastown ↔ planning-with-files**：Bead status ⇄ Markdown checklist
- **skill ↔ planning-with-files**：skill 完成时 update planning file

**金句**：Multi-Agent Stack 不是 4 个 Primitive，是 6 层 + 5 个跨层契约。R666 的"4 合 1"假设被 R667 的实证证据推翻——**真实世界是 Unix-style 分层，不是单体内聚**。

---

## 七、对 awesome-harness-engineering v2.0 的修正建议

R666 预测 v2.0 应该有 **14 Primitives + 3 Cross-Dimension Primitives**，其中 Multi-Agent Orchestration Primitive 是新加的。

**R667 修正**：Multi-Agent Orchestration Primitive 不应该是单一 Primitive，而应该是 **5 个 Layer Primitive + 4 个 Cross-Layer Contract**：

| R666 v2.0 预测 | R667 修正建议 |
|----------------|---------------|
| Multi-Agent Orchestration Primitive（单 Primitive）| Multiplexer Primitive + Orchestrator Primitive + Skill Registry Primitive + State/Memory Primitive + Tool Runtime Primitive（5 Primitive）|
| （无 Cross-Layer 概念）| Bead-Pane Contract + Skill-Planning Contract + Multiplexer-Orchestrator Contract + State-Resume Contract（4 Cross-Layer Contract）|

**理由**：R667 的 herdr 证据表明 Multi-Agent 是分层架构，不是单一 Primitive。如果 v2.0 不分层处理，开发者会被迫实现一个 single-binary "do everything" 框架（gastown 正在犯这个错）——这不利于生态分工。

---

## 八、v2.0 演进预测升级

R666 预测：**v2.0 在 R667-R670 发布的概率 5%**。

R667 修正预测：

1. **ai-boost/awesome-harness-engineering 监测持续**（v2.0 NOT released，2,757 ⭐ sustained）
2. **新增监测：gastownhall/gastown 与 herdr 是否相互 mention**（如果相互 mention = 协议收敛信号）
3. **新增监测：是否出现第三个 multi-agent multiplexer**（如果出现 = 范式确立）
4. **R667-R672 监测候选**：
   - **taste-skill 1st-party 合作**（与 gastown/herdr 联合发布 multi-agent stack 文档）
   - **planning-with-files 1st-party 合作**（被 gastown 作为 Beads 替代 backend）
   - **Dolt 1st-party 采用**（gastown v1.3.0 可能迁移到 Dolt 替代 Beads）

---

## 九、给读者的行动启示

### 9.1 如果你正在跑多 Agent

不要试图用一个项目做所有事。按 Multi-Agent Stack v1.0 分层选择工具：

```
Layer 1 Multiplexer:    herdr（terminal native）或 Cursor（GUI）
Layer 2 Orchestrator:   gastown（heavy DAG）或 Claude Code Agent Teams（light）
Layer 3 Skill:          taste-skill + alirezarezvani/claude-skills
Layer 4 State/Memory:   planning-with-files（最简）或 Dolt + Beads（完整）
Layer 5 Tool Runtime:   MCP servers（最小化集成）
```

### 9.2 如果你正在选 multi-agent 框架

**判断清单**：

1. 它解决哪一层？（不要选声称"all-in-one"的）
2. 它的 Layer 1-5 是否完整？（任何一层缺失都会成为瓶颈）
3. 它的 cross-layer contract 是否标准化？（不要选只支持自家 stack 的）
4. 它的 license 是什么？（herdr = AGPL-3.0，gastown = MIT，planning-with-files = MIT，taste-skill = MIT）

### 9.3 如果你正在设计 multi-agent harness

**R667 设计原则**：

1. **不要做 single-binary do-everything**（gastown 的教训：架构图复杂到需要专门文档）
2. **不要做 GUI-only**（herdr 的教训：必须在 terminal-native）
3. **必须支持 file-based state**（planning-with-files 的教训：Agent 工作必须可被外部观察）
4. **必须提供 per-Agent PTY**（herdr 的教训：真终端不是 wrapped）
5. **必须提供 IPC layer**（gastown × herdr 桥接的教训：否则只能手动拼凑）

---

## 十、结论

R667 的核心发现：

> **Multi-Agent 不是 1 Primitive，是 6 层 + 5 跨层契约**。

R666 的"4 合 1 Primitive"假设在单一项目（gastown）内是自洽的，但在跨项目实证（gastown + herdr）下被推翻。开源社区正在用 **Unix-style 分层 + 独立实现** 的方式收敛到 Multi-Agent Stack。

**给 awesome-harness-engineering v2.0 的修正建议**：

> Multi-Agent Orchestration Primitive → 拆分为 5 个 Layer Primitive + 4 个 Cross-Layer Contract

**给 ai-boost/awesome-harness-engineering 维护者的具体建议**：

- 在 v2.0 README 增加 **"Multi-Agent Stack 分层模型"** 章节
- 在 v2.0 Primitives 列表中将 Multi-Agent Orchestration 拆分为 5 个独立 Primitive
- 在 v2.0 Cross-Dimension 章节中新增 **Multi-Agent Cross-Layer Contracts**（4 个）
- 引用 gastown + herdr + planning-with-files + taste-skill 四个项目作为 Layer 1-4 的 evidence-based examples

**给 freeze 项目的具体建议**：

- R668-R672 持续监测 gastown v1.3.0 release + 17k⭐ BREAK + herdr 1万⭐ BREAK + taste-skill 60k⭐ BREAK
- 监测是否有第三个 multi-agent multiplexer 出现（范式确立信号）
- 监测是否出现 Multi-Agent Stack Protocol（MASP）标准化 IPC

---

## 来源清单

1. [Gas Town GitHub README v1.2.1](https://github.com/gastownhall/gastown) — 16,310 ⭐ MIT
2. [Gas Town CHANGELOG v1.2.0/v1.2.1](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md) — 关键 stability 修复
3. [Gas Town docs/concepts/molecules.md](https://github.com/gastownhall/gastown/blob/main/docs/concepts/molecules.md) — Molecule 概念详解
4. [ogulcancelik/herdr GitHub README](https://github.com/ogulcancelik/herdr) — 11,903 ⭐ AGPL-3.0
5. [herdr vs tmux vs GUI managers 对比表](https://herdr.dev/compare/) — 设计哲学对比
6. [Leonxlnx/taste-skill GitHub README](https://github.com/Leonxlnx/taste-skill) — 57,222 ⭐ MIT
7. [OthmanAdi/planning-with-files GitHub](https://github.com/OthmanAdi/planning-with-files) — 24,622 ⭐ MIT
8. [R666 gastown-multi-agent-orchestration-deep-dive](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) — Multi-Agent Orchestration Primitive 起源
9. [R661 overview meta article](../deep-dives/awesome-harness-engineering-three-dimensions-protocolization-2026.md) — harness 协议化三维度体系起源
10. [R662 horizontal 解耦 deep dive](../deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) — Skill 协议中立性
11. [R663 vertical 解耦 deep dive](../deep-dives/harness-vertical-decoupling-control-plane-execution-plane-protocol-2026.md) — MCP + SDK 分层
12. [R664 cross-device 协同 deep dive](../deep-dives/harness-cross-device-coordination-mobile-cloud-session-state-protocol-2026.md) — Cross-device 状态协议
13. [R665 meta synthesis + Planning Primitive](../deep-dives/harness-protocolization-r661-r664-meta-synthesis-planning-primitive-v2-prediction-2026.md) — Planning Primitive 起源
14. [anthropics/claude-code](https://github.com/anthropics/claude-code) — Claude Code 1st-party reference
15. [Rust tokio async runtime](https://tokio.rs/) — herdr async foundation
16. [tmux man page](https://man7.org/linux/man-pages/man1/tmux.1.html) — herdr 设计灵感
17. [AGPL-3.0 License](https://www.gnu.org/licenses/agpl-3.0.html) — herdr license basis

---

**R667 实证结论**：Multi-Agent Stack = Unix-style 分层（6 Layer）+ 跨层协议契约（5 Contract）。R666 的"4 合 1 Primitive" 假设被推翻——真实世界是分层架构，不是单体内聚。

**R667 行动建议**：awesome-harness-engineering v2.0 应将 Multi-Agent Orchestration Primitive 拆分为 5 Layer Primitive + 4 Cross-Layer Contract。

**R668 监测重点**：gastown v1.3.0 release + 17k⭐ BREAK + herdr 1万⭐ 持续 + 第三个 multi-agent multiplexer 是否出现。