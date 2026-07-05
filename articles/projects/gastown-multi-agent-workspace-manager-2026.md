# Gas Town：多 Agent 工作空间编排的工业级实现（R668 UPDATE 持续 monitoring 17k⭐ BREAK 临界）

**核心主张**：Gas Town 不是又一个「用 Agent 写代码」的工具，它是**多 Agent 协作的操作系统**——通过 Git Worktree 做状态持久化、Beads 做工作追踪、Witness/Deacon/Dogs 做健康监控，实现了 20-30 个 Agent 并行工作而不失控。这与 Cursor 第三时代的「多 Agent Fleet」理念形成呼应，但 Gas Town 更接近底层框架，而 Cursor 更接近终端用户产品。

**R668 UPDATE 状态**: **16,330 ⭐ (R668 monitoring 2026-07-06 03:57 CST, +20 in 2h from R667 16,310 ⭐, +38 in 8h from R666 16,292 ⭐)** MIT license, **v1.2.1 (2026-06-06)** — R668 持续 monitoring，距 17k⭐ BREAK 670⭐ gap，R668-R672 likely BREAK。详细分析见 [R666 deep dive article](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md).

**R667 UPDATE 状态**: 16,310 ⭐ + R667 Multi-Agent Stack 分层 deep dive 主证据，Layer 2 Orchestrator 标杆。

**R666 UPDATE 状态**: **16,292 ⭐ (R666 monitoring 2026-07-05 23:57 CST, +1,378 in ~30 days from 14,914 ⭐ 2026-06-04, +9.2% sustained strong growth)** MIT license, **v1.2.1 (2026-06-06)** — 最新版本加入了 Convoys `mountain` label、Molecules（TOML Formula 工作流模板）、Refinery（Bors-style bisecting merge queue）、Escalation（severity-routed）等工业级 multi-agent 编排抽象。

**读者画像**：已经有单 Agent 使用经验，正在探索「如何同时跑多个 Agent」或「如何让 Agent 持续运行」的工程师。

**核心障碍**：当你想同时跑多个 Agent（每个处理不同任务）时，很快会遇到：上下文丢失、会话状态无法持久、Agent 之间无法协调、出了问题无法追踪。

---

## T - Target：谁该关注 Gas Town

**目标用户画像**：
- 正在从「单 Agent 串行」迁移到「多 Agent 并行」的团队
- 有大规模代码库维护需求（多模块、多仓库同时迭代）
- 希望 Agent 能在后台持续运行，而不是每次重启都「失忆」
- 需要对多个 Agent 的工作进度有集中可视化的团队负责人

**技术水平要求**：
- 熟悉命令行操作，有 tmux 使用经验更佳
- 理解 Git Worktree 机制（Gas Town 用它做隔离工作区）
- 有多 Agent 协作需求，而非单 Agent 增强场景

---

## R - Result：能带来什么具体改变

| 对比维度 | 无 Gas Town | 有 Gas Town |
|---------|------------|-------------|
| 多 Agent 并行规模 | 3-5 个本地会话（资源争抢） | 20-30 个 Agent 并行（独立 VM/容器） |
| Agent 重启后状态 | 完全丢失，需要重建上下文 | 通过 Git Hooks 自动恢复 |
| 工作追踪方式 | 人工记录或脑子记 | Beads 分类账本，结构化可查 |
| Agent 协调方式 | 人类在多个窗口切换监督 | Mayor 统一协调，Agent 间通过 Mailbox Handoff |
| 问题发现方式 | 等 Agent 跑完了才知道 | Witness/Deacon 实时监控，发现卡顿立即报警 |
| 工作复用 | 换一个会话完全重来 | Seance 查询上一个 Session 的决策和发现 |

> "Instead of losing context when agents restart, Gas Town persists work state in git-backed hooks, enabling reliable multi-agent workflows."
> — [Gas Town GitHub README](https://github.com/gastownhall/gastown)

---

## I - Insight：它凭什么做到这些

### 核心架构设计

Gas Town 的架构设计围绕**状态持久化**展开，这是它与其他多 Agent 方案的根本差异。

**1. Git Worktree 隔离（Hook）**

每个 Rig（即项目）使用独立的 Git Worktree，Agent 的工作直接写入 Worktree 而不影响主分支。这解决了：
- 多 Agent 同时操作同一仓库时的分支冲突
- Agent 工作可审核、可回滚、可追溯
- Agent 崩溃后，工作状态不丢失

**2. Beads 分类账本**

Beads 是 Gas Town 的工作单元抽象，格式为 `gt-abc12` 这样的 ID 前缀 + Git-backed 存储。Beads 的本质是**结构化的工作描述 + 状态追踪**，类似于轻量级的 Issue Tracker 内嵌在 Git 里。

**3. 三层看门狗（Witness / Deacon / Dogs）**

```
┌──────────────────────────────────────────┐
│  Deacon（全局巡逻监督者）                    │
│  ┌────────────────────────────────────┐  │
│  │  Witness（单 Rig 生命周期管理）       │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │  Polecat（实际工作的 Agent）   │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
        ↓ 触发
      Dogs（基础设施工人，执行清理/修复任务）
```

- **Witness**：监控单个 Rig 内的 Polecat，发现卡顿触发恢复
- **Deacon**：全局后台巡逻，协调跨 Rig 的资源分配
- **Dogs**：被 Deacon 派去执行具体任务的 Workers（如 Boot 做初始分类）

**4. Mayor 作为统一协调入口**

用户不需要记住各种 Agent 命令，只需要跟 Mayor（一个 Claude Code 实例）说话，告诉它你想完成什么。Mayor 理解工作空间的结构和 Agent 的能力，负责拆解任务并分配给相应的 Polecat。

> "Start here - just tell the Mayor what you want to accomplish."
> — [Gas Town GitHub README](https://github.com/gastownhall/gastown)

**5. Seance：跨 Session 的上下文继承**

`gt seance` 命令可以发现之前的 Agent Session，让当前 Agent 能查询上一个 Session 发现的上下文和决策。这解决了「上一个 Agent 发现了什么重要信息，换一个 Session 后完全丢失」的问题。

---

## P - Proof：谁在用、效果如何

| 指标 | 数据 |
|------|------|
| GitHub Stars | **16,292 ⭐**（R666 monitoring 2026-07-05，+1,378 in 30 days from 14,914 ⭐ 2026-06-04，+9.2% sustained strong growth） |
| Forks | 1,612 |
| 编程语言 | Go（高性能，原生并发） |
| 最新更新 | 2026-05-03（活跃维护） |
| 依赖生态 | Git + Dolt + tmux + Claude Code/Codex/Copilot |
| 主要用户场景 | 多 Agent 并行的代码库维护、长时后台任务 |

**支持多种 Agent 运行时**：
- Claude Code（默认）
- OpenAI Codex
- GitHub Copilot CLI
- Gemini CLI（可扩展）

这意味着 Gas Town 不是一个 Claude 绑定的方案，团队可以根据需求选择或混用不同的 Agent 后端。

---

## 适用边界与竞品对比

### 何时用 Gas Town

- 需要同时处理 **5+ 个并行任务**的大型代码库维护
- 希望 Agent **持续在后台运行**而不占用本地资源
- 需要**结构化追踪多 Agent 工作进度**（不只是看 diff）
- 团队有 **tmux 使用经验**，习惯命令行工作流

### 何时不用 Gas Town

- 小型项目，单 Agent 串行就能完成
- 习惯 GUI 优先，不喜欢命令行操作
- 只需要「偶尔让 Agent 帮个忙」而非持续 Agent 工作流

### 与竞品的定位差异

| 方案 | 定位 | 核心优势 | 劣势 |
|------|------|---------|------|
| **Gas Town** | 多 Agent 工作空间 OS | 工业级规模（20-30 Agent）、Git-backed 状态持久化 | 需要 CLI 熟练，有一定学习曲线 |
| **Cursor 3** | 终端用户产品 | UI 友好、Cloud Agent 即开即用 | 对底层控制有限，不适合自托管 |
| **OpenAI Symphony** | Issue Tracker 编排协议 | 与 Linear 深度集成、任务驱动 | 依赖外部 Issue Tracker，需要一定工程集成能力 |
| **Claude Code（原生）** | 单 Agent 增强 | 无需额外工具、上手简单 | 多 Agent 并行需要手动管理 |

---

## 快速上手

### Step 1：安装 Gas Town

```bash
# macOS/Linux（Homebrew）
brew install gastown

# 或者 npm
npm install -g @gastown/gt

# 或者 Go 从源码编译
go install github.com/steveyegge/gastown/cmd/gt@latest
```

### Step 2：初始化工作空间

```bash
gt install ~/gt --git
cd ~/gt
```

### Step 3：添加项目 Rig

```bash
gt rig add myproject https://github.com/you/repo.git
```

### Step 4：启动 Mayor（统一协调入口）

```bash
gt mayor attach
```

然后直接告诉 Mayor 你想做什么，剩下的由 Mayor 协调 Agent 完成。

---

## 局限性与已知问题

1. **依赖复杂**：需要 Go 1.25+、Git 2.25+、Dolt、tmux，新用户环境配置成本高
2. **CLI-first 设计**：没有 GUI，对非 CLI 用户不友好
3. **概念密度高**：Mayor/Rig/Polecat/Hook/Bead/Convoy/Molecule 一整套术语体系，学习曲线陡
4. **macOS 限制**：Go 编译的二进制会被 macOS SIGKILL，需要通过 Homebrew 安装
5. **Dolt 依赖**：工作追踪依赖 Dolt（一个 Git-like 的 SQL 数据库），增加了运维复杂度

---

## 结论

Gas Town 代表了多 Agent 协作领域的**工业级框架**方向——不追求「一个命令让 AI 写代码」的酷炫，而是解决**「如何让 20-30 个 Agent 同时稳定运行」**这个真实的工程问题。

它的核心价值在于：
1. **Git Worktree 隔离**解决了多 Agent 并行时的状态冲突
2. **Beads 账本**解决了工作追踪的结构化问题
3. **三层看门狗**解决了大规模 Agent 集群的健康监控

如果你正在探索「多 Agent 并行工作」且有一定工程能力，Gas Town 是目前最完整的开源解决方案之一。但它的复杂性也说明：**多 Agent 协作的工程挑战还没有被「一键解决」，每个方案都在复杂度和能力之间做权衡**。

> 笔者认为：Gas Town 的架构设计值得多 Agent 框架开发者研究——它的分层（Hook/Bead/Convoy/Molecule）和健康监控体系是目前见过的最完整的工程实现。但对于大多数团队，Cursor 3 这样的产品方案可能是更好的起点，等需求复杂到 Cursor 3 满足不了时再考虑 Gas Town 或自建类似系统。

---

*来源：[Gas Town GitHub README](https://github.com/gastownhall/gastown)*

---

## 第八节：R666 update — v1.2.0/v1.2.1 工业级稳定化 + Convoys/Molecules/Refinery 多 Agent 工作流引擎

**R666 monitoring 状态**: **16,292 ⭐ (+1,378 in 30 days, +9.2% sustained strong growth)**, **v1.2.1 (2026-06-06)**, MIT License

R665 决策仅写作 deep dive article，本节（第八节）为 R666 UPDATE 持续 monitoring 增量——聚焦 **v1.2.0/v1.2.1 的工业级稳定性修复 + 新增工业级 multi-agent 工作流抽象**。

### 8.1 v1.2.1 (2026-06-06) 关键修复：Shell 集成不再侵入任意 shell

> "**Shell integration no longer nags in arbitrary shells** — the `gt install --shell` hook prompted `Add '<repo>' to Gas Town? [y/N/never]` in any git repo that wasn't a known rig, and on bash it re-prompted before *every* command (not just on `cd`). An interrupted prompt (Ctrl-C) never recorded the answer and could loop indefinitely across restored terminal sessions. The add-offer is now **opt-in** (set `GASTOWN_OFFER_ADD=1`); by default the hook stays silent and only exports `GT_TOWN_ROOT`/`GT_RIG` inside known rigs."
> — [Gas Town v1.2.1 CHANGELOG](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md)

**判断**：v1.2.1 之前，每次进入任意 git 仓库都触发 `Add to Gas Town?` 提示 + bash 下每个命令前都提示 → 开发者**对 Gas Town 产生厌恶感**。v1.2.1 改为 **opt-in（`GASTOWN_OFFER_ADD=1`）+ 仅在 `cd` 时提示**，是**「vibes-based 开发体验」的关键 UX 修复**。

### 8.2 v1.2.0 (2026-05-27) 关键修复：Daemon crash-loop vs Claude usage limits

> "**Daemon crash-loop vs Claude usage limits** — Stuck-agent-dog now inspects the agent's tmux pane for Claude usage-limit / rate-limit signatures before killing and restarting. Detected pauses apply a fixed retry delay (`PauseBackoff`, default 60s) and don't count toward the crash-loop fault budget, letting `quota_dog` rotate accounts instead of burning the budget on transient API limits (gh#3398, hq-j6hur.4.1)."
> — [Gas Town v1.2.0 CHANGELOG](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md)

**工程意义**：multi-agent 系统的「Agent 卡住」有 5+ 种原因（Claude rate limit / 死循环 / 网络超时 / 工具异常 / 资源耗尽），每种需要不同恢复策略。v1.2.0 让 watchdog **先识别症状再决策**，是 multi-agent 系统从「**粗暴脚本**」升级为「**智能 watchdog**」的关键拐点。

### 8.3 v1.2.0 关键修复：Dolt 数据库分裂 + Stale hooked mail beads 累积

> "**Rig init no longer creates duplicate Dolt databases** — Beads written from the rig could land in the orphan while the mayor read from the canonical DB — a silent data split. Cleanup now removes both naming forms and `AddRig` fails loudly if an orphan persists (gh#3562, hq-j6hur.4.2)."
> — [Gas Town v1.2.0 CHANGELOG](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md)

> "**Stale hooked mail beads** — `sendHandoffMail()` now closes any `gt:message` beads left in `status=hooked` from previous sessions before creating a new handoff bead, preventing indefinite accumulation across sessions (#3859)."
> — [Gas Town v1.2.0 CHANGELOG](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md)

**判断**：Dolt 数据库分裂是 **silent data split**——Agent 写入 orphan DB，Mayor 从 canonical DB 读取，**没有任何告警**。v1.2.0 改为 **fail loudly if orphan persists** = **fail-fast 哲学**。Stale hooked mail beads 累积是 multi-agent 系统的 **长尾资源泄漏**，v1.2.0 的「house-keeping as code」是**自动化资源回收机制**——避免系统无限膨胀。

### 8.4 新增工业级 multi-agent 工作流抽象（v1.2.x 系列）

v1.2.x 系列在原有 Mayor/Rig/Polecat/Hook/Beads 基础上，新增了三个工业级 multi-agent 编排抽象：

#### 8.4.1 Convoys + Mountain label

> "**Convoy completion + cross-rig dep notifications** — Convoy completion and cross-rig dependency resolution now fire notifications, surfacing milestone events without polling (#3838)."
> — [Gas Town v1.1.0 CHANGELOG](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md)

> "**Convoys** — Work tracking units. Bundle multiple beads that get assigned to agents. Convoys labeled `mountain` get autonomous stall detection and smart skip logic for epic-scale execution."
> — [Gas Town README](https://github.com/gastownhall/gastown)

**工程意义**：
1. **Convoy = 多 Bead 聚合**：把关联 Beads 打包成「一起追踪、一起完成」的工作单元（类比 JIRA Epic + Sprint，但 Git-backed）
2. **`mountain` label = epic-scale execution**：超大规模 Convoy 启用**自主 stall 检测 + 智能 skip 逻辑**
3. **跨 rig dep notifications**：v1.1.0 之前需要 polling，v1.1.0 改为**主动 push 通知**——分布式系统的成熟模式（pub/sub > polling）

#### 8.4.2 Molecules（TOML Formula 工作流模板）

> "**Molecules** are workflow templates that coordinate multi-step work. Formulas (TOML definitions) are instantiated as molecules with tracked steps. Two modes: **root-only wisps** (steps materialized at runtime, lightweight) and **poured wisps** (steps materialized as sub-wisps with checkpoint recovery)."
> — [Gas Town README](https://github.com/gastownhall/gastown)

**两种 Molecule 模式对比**：

| 模式 | 步骤物化时机 | checkpoint 恢复 | 适用场景 |
|------|------------|----------------|---------|
| **Root-only wisps** | 运行时物化 | 无 | 轻量级工作流 |
| **Poured wisps** | 步骤物化为 sub-wisps | 有 | 长任务 + 中断恢复 |

**判断**：Molecule 是 Gas Town 对**「工作流即代码」**的工程实现——把工作流从「人类脑中的隐性知识」升级为「TOML 文件中的显性合约」。这与 R665 提出的 **Planning Primitive（vendor-neutral plan + completion gate + file-based working state）** 一脉相承。

#### 8.4.3 Refinery（Bors-style bisecting merge queue）

> "**Refinery** — Per-rig merge queue processor. When polecats complete work via `gt done`, the Refinery batches merge requests, runs verification gates, and merges to main using a **Bors-style bisecting queue**. Failed MRs are isolated and either fixed inline or re-dispatched."
> — [Gas Town README](https://github.com/gastownhall/gastown)

**关键工程机制**：
1. **批量合并**：不是「每个 MR 单独合并」，而是**先把一批 MR 排队，统一测试，二分定位**
2. **Verification gates**：合并前自动跑测试，失败 = 不合并
3. **Bors-style bisecting**：当一批 MR 中某个导致测试失败，**二分定位是哪个 MR 导致**——而不是「重新跑所有 MR 直到找到罪魁祸首」
4. **Failed MR 隔离**：失败的 MR 不污染主分支，要么 inline 修复，要么重新派发

**笔者认为**：Refinery 是 Gas Town 工程价值的**真正护城河**——Git Worktree + Beads + Convoy 任何人都能模仿，但 **Bors-style bisecting merge queue** 需要**对分布式 CI 的深刻理解**。这是为什么 Gas Town 能「**让 20-30 个 Agent 并行而不失控**」的根本原因。

### 8.5 v1.2.x 重大修复 vs v1.0/v1.1 修复对比

| 版本 | 修复类型 | 关键修复 | 工程意义 |
|------|---------|---------|---------|
| **v1.1.0 (2026-05-06)** | 功能增强 | Convoy completion notifications + cross-rig dep notifications | 从 polling 转向 pub/sub |
| **v1.2.0 (2026-05-27)** | 关键稳定性 | Claude usage-limit 识别 + Dolt 数据库分裂修复 + Stale hooked mail beads 清理 | multi-agent 系统的「production-readiness」跃迁 |
| **v1.2.1 (2026-06-06)** | UX 修复 | Shell 集成不再侵入任意 shell + mail reply-to 推断 + Dolt prefix 数据库 | 从「侵入式 hook」升级为「友好 hook」 |

### 8.6 R666 决策：作为 Multi-Agent Orchestration Primitive 的工业级实证

R666 deep dive 文章（[../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md)）论证了 **Gas Town v1.2.1 是 R661-R665 三维度体系的「multi-agent 场景最强实证」**：

- **horizontal 解耦**：Git Worktree per-Polecat 隔离 = horizontal 维度的物理实现
- **cross-device 协同**：Beads + Convoys = R664 cross-device 维度的工业级工作单元
- **vertical 解耦的延伸**：Refinery verification gates + Bors-style bisecting = R663 vertical 解耦在 multi-agent 场景的具体实现
- **Planning Primitive 工业级扩展**：vendor-neutral plan (Beads) + completion gate (Refinery) + file-based working state (Git Worktree) = R665 Planning Primitive 的 multi-agent 扩展

**R666 关键定位**：multi-agent orchestration 不是 harness 协议化的「第四维度」，而是 **horizontal + cross-device 维度在极端并发场景下的复合压力测试**。

### 8.7 R666+ monitoring 计划

| 监测项 | 当前状态 | 下一阶段监测点 |
|--------|---------|---------------|
| **16,292 ⭐ → 17k⭐ 临界** | 距 17k 仅 708⭐ gap | R667-R668 likely 17k⭐ BREAK |
| **v1.3.0 release** | v1.2.1 仍是 latest | R667-R668 监测：Dolt SPoF 解决方案 + Mayor 高可用机制 + Windows 完整兼容 |
| **awesome-harness-engineering 收录** | 监测 ai-boost 是否在 Multi-Agent Orchestration 章节引用 | R666-R668 监测 R666 Multi-Agent Orchestration Primitive 提案是否被采纳 |
| **Anthropic 1st-party 官方推荐** | 监测 Anthropic / OpenAI 是否在 1st-party 文档中引用 | R666-R668 持续监测 |
| **20k⭐ 临界** | 距 20k 3,708⭐ gap | R670-R672 监测 |

### 8.8 来源追加（R666 monitoring）

- [Gas Town GitHub README](https://github.com/gastownhall/gastown) — **16,292 ⭐** v1.2.1 (R666 monitoring 2026-07-05 via GitHub API, +1,378 in 30 days from 14,914 ⭐ 2026-06-04, +9.2%)
- [Gas Town CHANGELOG v1.2.0/v1.2.1](https://github.com/gastownhall/gastown/blob/main/CHANGELOG.md) — 关键 stability 修复 + new abstractions
- [Gas Town docs/concepts/molecules.md](https://github.com/gastownhall/gastown/blob/main/docs/concepts/molecules.md) — Molecule 概念详解
- [Gas Town docs/design/escalation.md](https://github.com/gastownhall/gastown/blob/main/docs/design/escalation.md) — Escalation 严重性路由
- [Anthropic Claude Code Agent Teams (Native)](https://code.claude.com/docs/en/agent-teams) — 官方 Agent Teams 文档
- [Anthropic: Multi-Agent Harness Engineering: Lessons from 2000+ Sessions](https://www.anthropic.com/engineering/multi-agent-harness-engineering-lessons-from-2000-sessions) — 多 Agent Harness 工程实践
- [Bors: Merge Queue for Rust](https://github.com/rust-lang/bors) — Bors-style bisecting 合并队列
- [R666 deep dive article](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) — 姊妹篇 deep dive
- [R661 overview meta article](../deep-dives/awesome-harness-engineering-three-dimensions-protocolization-2026.md) — harness 协议化三维度体系起源
- [R662 horizontal 解耦 deep dive](../deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md)
- [R663 vertical 解耦 deep dive](../deep-dives/harness-vertical-decoupling-control-plane-execution-plane-protocol-2026.md)
- [R664 cross-device 协同 deep dive](../deep-dives/harness-cross-device-coordination-mobile-cloud-session-state-protocol-2026.md)
- [R665 meta synthesis + Planning Primitive](../deep-dives/harness-protocolization-r661-r664-meta-synthesis-planning-primitive-v2-prediction-2026.md) — R661-R664 meta 综述 + Planning Primitive 关键发现
