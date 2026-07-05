# Harness 协议化三维度体系 — cross-device 协同 deep dive：会话状态协议如何让 harness 跨设备流动

> 来源：[Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile) + [Cursor for iOS blog](https://cursor.com/blog/ios-mobile-app) + [OpenAI: Codex 跨设备协作](https://openai.com/index/agents-of-change-mobile-collaboration/) + [SeemSeam/claude_codex_bridge 3,190 ⭐](https://github.com/SeemSeam/claude_codex_bridge) (CCB v8.0.15 Flutter Mobile) + [Anthropic: Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) + [Apple Newsroom: Xcode 26.3 unlocks agentic coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/)
>
> **核心论点**：cross-device 协同已经从「远程桌面」（屏幕镜像 + 输入转发）演化到「会话状态协议」（只同步「当前 step / 当前 tool / 当前 status」这种结构化状态）——Cursor iOS 的 Remote Control、OpenAI Codex 的 Secure Relay、CCB v8.0.15 的 Tailscale Serve + Flutter Mobile gateway，三家 1st-party / 准 1st-party 实现都收敛到同一个模式：**agent loop 与 tool execution 解耦 + append-only telemetry + cache-first 架构 + source 标签 session 模型**，让 harness 不再绑定在某一台设备上，而是按「会话状态协议」在 mobile / desktop / cloud 之间流动。

---

## 一、为什么 cross-device 协同单独成文

R661《[awesome-harness-engineering 三维度体系](awesome-harness-engineering-three-dimensions-protocolization-2026.md)》已经把 harness 协议化拆成三个正交维度：

1. **vertical 解耦**（control plane ↔ execution plane）—— R663 deep dive 已完成
2. **horizontal 解耦**（多 control plane ↔ 同一个 Skill + execution plane）—— R662 deep dive 已完成
3. **cross-device 协同**（多端 harness 通过会话状态协议交接）—— 本文

但为什么 cross-device 协同值得单独成文，而不是塞进 vertical 解耦的延伸？三个理由：

**理由 1：cross-device 协同是 harness 从「工具」走向「工作流」的范式跳跃**。Local-only harness（Claude Code CLI、Aider）和 cloud-only harness（Cloud Agent）本质都是「单一执行环境 + 单一用户设备」。cross-device 协同后，用户是移动的，agent 不需要跟着移动 ——「用户离开桌面」不再是 harness 的中断信号，而是「harness 在另一个 surface 继续执行」。这是工具向工作流演化的关键标志。

**理由 2：cross-device 协同的协议栈与 vertical/horizontal 解耦正交，但更深**。vertical 解耦关注「control plane 和 execution plane 之间的协议」（MCP），horizontal 解耦关注「Skill 跨 control plane 的协议」（agentskills/agentskills），cross-device 协同关注的是「整个 agent harness 跨设备的会话状态协议」——它要把 agent loop 的内部状态、tool call 的执行轨迹、permission 的决策记录、用户的中断指令**全部序列化**为可传输、可重放、可合并的事件流。这种「会话状态可序列化」的要求，比 MCP / agentskills 都更底层。

**理由 3：1st-party 实证已足够成熟**。Cursor iOS（R657 / R658）+ OpenAI Codex cross-device collaboration（2026-06）+ Apple Xcode 26.3 + Claude Agent SDK（R659）三家都给出了完整的「跨设备 agent harness」实现路径。社区层面，SeemSeam/CCB 3,190 ⭐ 已经把「multi-agent CLI + Flutter Mobile + Tailscale Serve」打成 8.0.15 版本，验证了「跨设备 + 多 vendor + 多 agent」的复合场景。证据齐备，时机成熟。

---

## 二、cross-device 协同的本质：会话状态协议 ≠ 远程桌面

### 2.1 远程桌面范式（已被淘汰）

在 cross-device 协同之前，让用户在多台设备上使用同一个 AI coding agent 的标准方案是「远程桌面」：

```
┌──────────────────────────────────────────────────────────────┐
│                  Remote Desktop (RDP / VNC / SSH)            │
│                                                               │
│   Phone/Desktop ── screen mirror + input ─→  Agent Machine    │
│                                                               │
│   - 全量屏幕像素传输（30+ fps）                                │
│   - 输入事件转发（鼠标、键盘、触控）                            │
│   - 状态在 agent 机器内存                                      │
│   - 网络断线 = 会话断线                                       │
└──────────────────────────────────────────────────────────────┘
```

远程桌面的本质问题是「**它是一个图像流协议，不是会话状态协议**」。如果网络抖动，屏幕撕裂；如果 agent 机器死机，会话丢失；如果用户切换设备，需要重新建立整个会话。

### 2.2 会话状态协议范式（2026 年的事实标准）

cross-device 协同的真正范式是「**会话状态协议（Session State Protocol）**」——只同步「当前 step / 当前 tool / 当前 status」这种结构化状态，不同步屏幕像素：

```
┌──────────────────────────────────────────────────────────────┐
│              Session State Protocol (SSP)                    │
│                                                               │
│   Mobile ── struct events ─→  Backend (event store)          │
│       ↑                       │                               │
│       └─ struct events ──────┘                               │
│                                                               │
│   - 事件流传输（不是屏幕镜像）                                  │
│   - append-only event log（事件溯源）                         │
│   - 状态可重放（断线重连后从 log 重放）                        │
│   - 状态可在多个 surface 共享                                  │
└──────────────────────────────────────────────────────────────┘
```

**核心转变**：从「全量状态」替换为「增量事件流」。这与分布式系统从 RPC 走向 Event Sourcing / CQRS 是同一类范式跃迁。

### 2.3 会话状态协议的四个核心 primitives

无论是 Cursor iOS、OpenAI Codex，还是 CCB v8.0.15，实现 cross-device 协同都收敛到以下四个 primitives：

| Primitive | 职责 | Cursor iOS 实现 | OpenAI Codex 实现 | CCB v8.0.15 实现 |
|-----------|------|----------------|-------------------|------------------|
| **append-only telemetry** | 所有状态变更记录为只追加事件流 | Cloud backend event store | Codex Relay event log | CCB gateway event log |
| **cache-first client** | 客户端先读本地缓存，再后台 sync | SQLite/CoreData on iOS | Local session cache on mobile | Flutter app local state |
| **source tag** | session 来源标签（desktop / iosApp / slack / cli） | `source: iosApp` 标签 | Code Source API tagging | pairing profile scope |
| **rewind-safe replay** | 断线重连后从 append-only log 重放状态 | `rewind` 协议（保留失败步骤） | Continue session 协议 | Mobile reconnect 后从断点继续 |

这四个 primitives 不是独立发明的，而是**对 Event Sourcing + CQRS + Offline-First 三个已有架构模式的重新组合**。

---

## 三、1st-party 范本：Cursor iOS 的 cross-device 协同深度拆解

### 3.1 三端混合拓扑

[Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile) 把 Cursor 的跨设备架构描述为「**移动控制 + 本地执行 + 云端执行**」的三端混合：

```
┌──────────────────────────────────────────────────────────────┐
│              Cursor Mobile-Cloud Hybrid Harness              │
│                                                               │
│   ┌──────────────┐                                            │
│   │   iOS App    │  Control Surface                           │
│   │  (Mobile)    │  - Launch/track agents                     │
│   │              │  - Remote Control                          │
│   │              │  - Voice input                             │
│   │              │  - Visual context (screenshot)             │
│   │              │  - Live Activities + Push notifications    │
│   └──────┬───────┘                                            │
│          │ struct events / status updates                    │
│          ▼                                                    │
│   ┌─────────────────────────────────────────────┐             │
│   │         Harness Orchestrator                │             │
│   │  (Cursor cloud, event-sourced)              │             │
│   └──────┬────────────────────┬─────────────────┘             │
│          │                    │                               │
│          ▼                    ▼                               │
│   ┌──────────────┐     ┌──────────────┐                      │
│   │ Local Agent  │     │ Cloud Agent  │                      │
│   │ (laptop)     │     │ (isolated VM)│                      │
│   │ - filesystem │     │ - full dev   │                      │
│   │ - shell      │     │   env        │                      │
│   │ - network    │     │ - persistent │                      │
│   │   (egress    │     │ - 长时间运行 │                      │
│   │   limited)   │     │              │                      │
│   └──────────────┘     └──────────────┘                      │
│                                                               │
│   Handoff protocol: local plan ↔ cloud execution              │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Remote Control 协议的精确语义（关键工程区别）

[Cursor docs](https://cursor.com/docs/cloud-agent/mobile) 有一句非常关键的话：

> "**The agent loop moves to the cloud while its tools keep running on your machine**, so it reads your files, runs your tests, and uses your local setup the same way it did on your desktop."

这是 cross-device 协同的**关键工程区别**：

| 组件 | 运行时位置 | 数据流 |
|------|-----------|--------|
| **Agent loop**（推理、规划、决策） | Cursor cloud | 从本地拉模型需要的 context |
| **Tool calls**（terminal、file edit、test、git） | 用户本地机器 | 在本地执行，结果回到 cloud loop |

你的电脑不再跑 Claude 的推理循环了——它退化成「**纯执行器**」。真正的「思考」在 Cursor 的 cloud 里完成，但所有「动手」（改文件、跑测试、读 git）都在你的本地机器发生。

这与「远程桌面」的「屏幕镜像 + 输入转发」有本质区别——**Remote Control 不是屏幕镜像，而是把 agent loop 和 tool execution 拆到两个不同机器上**。

### 3.3 append-only telemetry + rewind-safe replay

Cursor iOS 的 docs 明确提到：

> "The app is cache-first. It reads from local data so the inbox and conversations open fast, then syncs once your connection returns."

表面看是普通的客户端缓存优化。但与 source 标签、跨设备 sync 放在一起，会发现它实际上是 **offline-first 架构的标准模式**：

```
iOS Client                          Cursor Cloud Backend
┌──────────────────┐                ┌──────────────────┐
│ Local Cache      │  ── events ──→ │ append-only log  │
│ (SQLite)         │                │ (event store)    │
│                  │  ←── events ── │                  │
└──────────────────┘                └──────────────────┘
        ↑                                   │
        └──── rewind after reconnect ───────┘
```

**append-only log 的设计哲学**：所有状态变更都是「追加」而不是「覆盖」。这意味着：
- **rewind 安全**：任何状态可以回滚到任意历史点
- **断线安全**：断线时不会丢失状态，重连后从 append-only log 重放
- **多 surface 一致**：所有设备从同一个 event store 同步，最终一致

这种设计与 [Meta REA 的 hibernate-and-wake checkpointing](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) 一脉相承——都把「状态可重放」当作 cross-device 协同的第一公理。

### 3.4 source 标签：session-level source tagging

[Cursor docs](https://cursor.com/docs/cloud-agent/mobile) 有一句容易被忽视但极其重要的话：

> "Agents started on mobile are tagged with `source: iosApp` so you can tell where they came from."

同一个用户的同一个 repo，可能存在多个并发 session：
- 桌面上一个 agent 在重构代码（`source: desktop`）
- 手机上同一个 agent 继续 steer（`source: iosApp`）
- Slack 里又触发了一个 cloud agent（`source: slack`）

source 标签让你在 inbox 里**一眼区分** session 的来源 surface。

**source 标签隐含的工程约束**：如果 Cursor 用简单的「当前最新状态」模型（CRDT 之类），根本不需要 source 标签——因为状态最终一致即可。**只有当 session 历史、回放、审计成为一等公民时，source 才有意义**。这是 Event Sourcing 模型的标准用法。

---

## 四、1st-party 范本：OpenAI Codex 跨设备协作的安全 Relay 层

### 4.1 Codex Mobile + Remote SSH 的双重拓扑

OpenAI 在 2026-06 发布的 Codex 跨设备协作覆盖了**两个层次**：

1. **Codex Mobile + Desktop**：用户在移动端审批 / 引导 Codex 在桌面执行
2. **Codex Remote SSH**：Codex 直接接入企业远程开发环境

[原文](https://openai.com/index/agents-of-change-mobile-collaboration/)：

> "Your files, credentials, permissions, and local setup stay on the machine where Codex is operating, while updates flow back to your phone in real time."

### 4.2 安全 Relay 层：cross-device 协同的网络安全边界

OpenAI 没有详细说明技术实现，但关键描述揭示了核心架构：

> "Under the hood, Codex uses a secure relay layer that keeps trusted machines reachable across devices without exposing them directly to the public internet. That relay also keeps active session state and context synced anywhere you're signed in with ChatGPT."

```
用户 Desktop → Codex (Remote SSH) → 企业远程开发环境
      ↓
手机 ChatGPT App → Codex Relay Layer → 实时状态推送
```

**关键工程问题**：企业远程开发环境不能暴露在公网上。Codex 的解决方案是**安全 Relay 层**：

- 机器不直接暴露在公网，而是通过 Relay 可达
- Relay 维护活跃 session 状态和上下文同步
- Relay 只传递状态更新和指令，不传递敏感凭证

这意味着企业可以保持现有的网络安全策略（不能从外部访问的开发环境），同时让员工从任何设备接入。

### 4.3 与 Cursor iOS 的对比

| 维度 | Cursor iOS | OpenAI Codex |
|------|-----------|---------------|
| **网络层** | Cursor cloud (自家 backend) | Codex Relay (ChatGPT 账号体系) |
| **协议层** | source 标签 + append-only log | Code Source API + active session state |
| **控制平面** | iOS App (UI) | ChatGPT App (跨平台) |
| **执行平面** | Local machine 或 cloud VM | Local machine 或 Remote SSH 远程机器 |
| **安全模型** | Data locality（文件不离开本机）| Secure relay（机器不暴露公网）|
| **跨设备同步** | Cursor backend 统一 | ChatGPT 账号统一 |

两家收敛到**同一个模式**：cross-device 协同的本质是「**会话状态协议 + 安全 relay 层 + 凭证本地化**」，而不是「远程桌面」。

---

## 五、社区实证：SeemSeam/CCB v8.0.15 的 multi-agent + cross-device 复合架构

### 5.1 CCB 是什么

[SeemSeam/claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge)（CCB）3,190 ⭐，v8.0.15（2026-07-05 pushed），是 cross-device 协同 + horizontal 解耦**复合场景**的最完整社区实现。

CCB 的设计目标是「**去中心化多 agent + 跨设备移动控制**」：

```
┌─────────────────────────────────────────────────────────────┐
│              CCB v8.0.15 Architecture                       │
│                                                              │
│   ┌──────────────┐                                           │
│   │ Mobile App   │  Flutter (Android/iOS)                    │
│   │ (Flutter)    │  - Voice input                            │
│   │              │  - File transfer                          │
│   └──────┬───────┘  - Remote terminal                        │
│          │ struct events via Tailscale Serve                 │
│          ▼                                                   │
│   ┌─────────────────────────────────────┐                    │
│   │   CCB Mobile Gateway                │                    │
│   │   (loopback 127.0.0.1:8787)         │                    │
│   │   - pairing profile scope           │                    │
│   │   - view / content / terminal /     │                    │
│   │     file upload / file download     │                    │
│   └──────┬──────────────────────────────┘                    │
│          │                                                   │
│          ▼                                                   │
│   ┌─────────────────────────────────────┐                    │
│   │   CCB Backend (server)              │                    │
│   │   - Daemon 持续运行                  │                    │
│   │   - 项目状态脱离前台保持              │                    │
│   └──────┬──────────────────────────────┘                    │
│          │ multi-agent orchestration                         │
│          ▼                                                   │
│   ┌──────────────────────────────────────────────────────┐   │
│   │ Multi-Agent Window (TUI)                            │   │
│   │   main: codex                                       │   │
│   │   worker1: codex(worktree), worker2: claude(worktree)│  │
│   │   reviewer: claude, qa: gemini                       │   │
│   │   + kimi / qwen / cursor / copilot / opencode / ...  │   │
│   └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 CCB 的 cross-device 协同四要素

CCB 的 cross-device 实现完整覆盖了 Cursor iOS 的四个 primitives，并加入了第五个关键能力——**multi-agent orchestration**：

| Primitive | CCB v8.0.15 实现 |
|-----------|------------------|
| **append-only telemetry** | Daemon 持续运行，project state 脱离前台 |
| **cache-first client** | Flutter app local state 缓存 |
| **source tag** | pairing profile scope（view / content / terminal / file upload / file download）|
| **rewind-safe replay** | Mobile reconnect 后从断点继续 |
| **multi-agent orchestration**（额外）| A→B→C / A,B→C / A→B,C 协作模式 |

### 5.3 安全边界：Tailscale Serve + pairing profile

CCB 的安全设计是**三层防护**：

```
┌─────────────────────────────────────────────────────────┐
│   Security Boundary (CCB v8.0.15)                       │
│                                                          │
│   Layer 1: Network                                       │
│     - Gateway 只绑定 loopback (127.0.0.1:8787)           │
│     - 远程访问必须通过 Tailscale Serve                    │
│     - 不启用 Tailscale Funnel (避免公网暴露)              │
│                                                          │
│   Layer 2: Authentication                                │
│     - Pairing profile 配对码                            │
│     - 一次性 token, 自动过期                              │
│                                                          │
│   Layer 3: Authorization                                 │
│     - Mobile 端只获得 pairing profile 授权的 scope       │
│     - view / content / terminal / file upload /          │
│       file download 五个 scope 可选                       │
│     - 默认只读 (view)，写操作需明确授权                  │
└─────────────────────────────────────────────────────────┘
```

**关键工程决定**：CCB **不保存** Tailscale 密码 / OAuth token / admin API token，**不自动修改** tailnet ACL/grants。这意味着即使 mobile gateway 被攻破，攻击者也无法获得 Tailscale 网络的横向移动能力。

### 5.4 为什么 CCB 是 cross-device 协同的实证标杆

CCB 之所以是「**cross-device + horizontal 解耦 + multi-agent orchestration**」三重组合的最佳实证，是因为它同时解决了三个独立问题：

1. **cross-device 协同**：Mobile App ↔ Server backend via Tailscale Serve
2. **horizontal 解耦**：一个 backend 同时运行 15 家 CLI providers（Codex / Claude / Gemini / Kimi / Qwen / Cursor / Copilot / Pi / OpenCode / Kiro / Droid / Crush / Antigravity / Z.ai / MiMo）
3. **multi-agent orchestration**：A→B→C 协作 / A,B→C 协商 / A→B,C 委派等复杂协作关系

这三个问题在 1st-party 实现里只覆盖了**其中一个或两个**：
- Cursor iOS：覆盖 1（cross-device），部分覆盖 2（多 agent 不明显）
- OpenAI Codex cross-device：覆盖 1（cross-device），单 agent / 远程 SSH
- Apple Xcode + Claude Agent SDK：覆盖 vertical 解耦，不覆盖 cross-device

CCB 是**第一个把三个维度同时落地的开源项目**，这让它成为 R664 cross-device 协同 deep dive 的最佳实证标杆。

---

## 六、horizontal × vertical × cross-device 三维度协同

### 6.1 三维度的正交性

R661 overview 已经论证过：horizontal / vertical / cross-device 三维度正交。但 R664 补充一个更精确的论证：**cross-device 协同的会话状态协议是 horizontal + vertical 解耦的载体**。

| 维度 | 抽象对象 | 协议层 |
|------|---------|--------|
| **horizontal 解耦** | Skill | agentskills/agentskills vendor-neutral 规范 |
| **vertical 解耦** | execution plane | MCP（Model Context Protocol）|
| **cross-device 协同** | 会话状态 | append-only event log + source 标签 + cache-first |

**cross-device 协同依赖于 horizontal + vertical 解耦**：如果 Skill 不能跨 control plane 复用（horizontal 解耦失败），那么用户在 mobile 上触发的 agent 和在 desktop 上触发的 agent 不能共享 Skill；如果 execution plane 不能通过 MCP 协议中立访问（vertical 解耦失败），那么 mobile 上的 agent 不能驱动 desktop 上的工具。

反之，horizontal + vertical 解耦也**受益于** cross-device 协同：当用户在多设备之间无缝切换时，horizontal / vertical 解耦的价值才真正体现——一个 vendor-neutral Skill 在 mobile / desktop / cloud 三个 surface 上无缝工作，一个 MCP 协议中立 execution plane 在三个 surface 上无缝调用。

### 6.2 业界三维度全开的现状

R661 overview 提出「三维度全开是下一阶段演进方向」，R664 给出更精确的现状判断：

| 落地阶段 | horizontal | vertical | cross-device | 代表项目 |
|---------|-----------|----------|--------------|---------|
| **单维度**（R662 之前）| ✅ | ❌ | ❌ | Claude Code, Aider, Codex CLI |
| **双维度**（R663-664）| ✅ | ✅ | ❌ | Apple Xcode + Claude Agent SDK |
| **双维度** | ✅ | ❌ | ✅ | Cursor iOS（horizontal 部分：15 家 providers 尚未覆盖，但 cloud + local + mobile 已多 surface）|
| **双维度** | ✅ | ❌ | ✅ | OpenAI Codex cross-device（Codex + Remote SSH）|
| **三维度全开**（next）| ✅ | ✅ | ✅ | **SeemSeam/CCB v8.0.15**（部分三维度：cross-device ✅ + horizontal ✅ + vertical 部分）|

CCB 已经初步实现「**horizontal + cross-device + 部分 vertical**」的三维度组合，但 vertical 解耦的协议层（MCP）尚未在 CCB 中完全工程化。

**结论**：cross-device 协同的成熟度**领先**于 horizontal / vertical 解耦的协议层标准化——三个 primitive（append-only telemetry + cache-first + source tag）已经在 1st-party 实现中固化（Cursor + OpenAI + CCB 三家已收敛），但 horizontal 解耦的 vendor-neutral Skill 规范和 vertical 解耦的 MCP 协议层仍在演进中。

---

## 七、cross-device 协同的工程决策框架

### 7.1 6 类场景决策矩阵

不同 cross-device 场景对 harness 的要求差异极大，下表给出 6 类典型场景的工程决策：

| 场景 | 网络假设 | 状态一致性 | 推荐 primitives | 参考实现 |
|------|---------|-----------|-----------------|---------|
| **L1: Local-only single device** | LAN | 强一致（单一进程）| 无需 cross-device primitives | Claude Code CLI |
| **L2: Local multi-device same LAN** | LAN | 最终一致 | append-only log + source tag | 暂未广泛落地 |
| **L3: Local + cloud same vendor** | WAN | 最终一致 | append-only log + cache-first + source tag | Cursor iOS Remote Control |
| **L4: Local + cloud multi-vendor** | WAN | 最终一致 | 上述三者 + pairing profile + secure relay | OpenAI Codex cross-device |
| **L5: Local + cloud multi-vendor + multi-agent** | WAN | 最终一致 | 上述四者 + multi-agent orchestration | **SeemSeam/CCB v8.0.15** |
| **L6: 完全离线 cross-device** | 无网络 | 离线优先 | append-only log + cache-first + 离线合并 | 部分 IDE（VS Code Live Share）|

### 7.2 4 步实施步骤

要实现 L3+ 级别的 cross-device 协同 harness，建议以下 4 步：

**Step 1：抽象 agent loop + tool execution 解耦**

关键反模式：把 agent loop 和 tool execution 紧耦合在同一个进程里。正确做法：让 agent loop 可以独立部署在 cloud（决策），tool execution 必须留在 local（动手）。这是 vertical 解耦的延伸。

**Step 2：引入 append-only event log**

把所有状态变更（plan、tool call、permission、message）记录为只追加事件流。事件 schema 必须包含：
- `event_id`：唯一标识
- `session_id`：所属 session
- `source`：触发 surface（desktop / iosApp / slack / cli）
- `timestamp`：单调递增时间戳
- `payload`：结构化 payload

**Step 3：实现 cache-first 客户端**

客户端先读本地缓存（SQLite / CoreData / Hive / Isar）展示 UI，后台异步 sync event log。这保证：
- 网络断线时 UI 仍然可用
- 启动时秒开（不需要等网络）
- 减少 backend 负载

**Step 4：source 标签 + pairing profile scope**

session 必须打 `source` 标签（区分来源 surface），mobile 端必须用 pairing profile scope（限制授权）。这是 cross-device 协同的**安全护城河**——没有 source 标签，多 surface session 合并时会丢审计；没有 pairing profile scope，mobile 端会变成不受控的远程执行入口。

### 7.3 5 个常见反模式

**反模式 1：远程桌面当 cross-device**。RDP / VNC / SSH 端口转发不是 cross-device 协同，是屏幕镜像。屏幕镜像不解决「用户是移动的，agent 不需要跟着移动」的根本问题。

**反模式 2：CRDT 当 event sourcing**。CRDT 是「最终一致的状态合并」，不是「可重放的会话历史」。cross-device 协同需要后者（rewind + audit + 跨 surface 同步），不是前者。

**反模式 3：WebSocket 长连接当 append-only log**。WebSocket 是传输层，不是存储层。append-only log 必须是持久化的（event store），断线重连后可以从 log 重放，WebSocket 断了就什么都没了。

**反模式 4：单一 source（desktop only）**。只支持 `source: desktop` 标签的 session，等于不支持 cross-device。真正的 cross-device 必须支持至少 3 种 source（desktop / mobile / cloud），并允许同一 session 在多个 source 之间迁移。

**反模式 5：mobile 端无限授权**。mobile 端一旦获得「全权代表 desktop」的授权，就失去了 security 护城河。正确做法：pairing profile scope + 默认只读 + 写操作需明确授权 + 凭证本地化（文件 / SSH key 不离开 desktop）。

---

## 八、cross-device 协同对未来的判断

### 8.1 短期（6 个月内）

- **append-only telemetry + cache-first + source tag** 三个 primitives 成为 cross-device harness 的事实标准（已经在 Cursor / OpenAI / CCB 三家收敛）
- **Tailscale Serve** 类安全 relay 层成为跨设备 / 跨网络部署的事实标准
- **Flutter / React Native** 类跨平台 UI 框架成为 mobile agent harness 的首选（CCB 已用 Flutter）

### 8.2 中期（6-18 个月）

- **MCP 协议层扩展到 cross-device 场景**：现在 MCP 主要解决 vertical 解耦，未来可能扩展到「MCP over relay」——让 mobile 上的 MCP 客户端通过 secure relay 调用 desktop 上的 MCP server
- **Session State Protocol 标准化**：append-only event log + source tag 的 schema 可能形成社区规范（类似 OpenTelemetry 的 trace schema）
- **pairing profile scope** 成为 mobile agent harness 的安全标准

### 8.3 长期（18 个月+）

- **三维度全开的 harness runtime**：horizontal + vertical + cross-device 同时满足，类似 Kubernetes 之于分布式系统
- **harness-as-a-service**：用户购买「会话状态 + execution plane + Skill 库」三件套，云厂商提供 cross-device 协同 runtime
- **harness 联邦**：不同厂商的 harness 通过标准协议互联，类似 Kubernetes Federation
- **可能的下一波合并**：anthropics/claude-code + Claude Mobile + claude-agent-sdk-python 三件套若进一步融合，可能让 Anthropic 自家实现 cross-device + horizontal + vertical 三维度全开

---

## 九、给 R665 的开放问题

R664 完成 cross-device 协同 deep dive 后，harness 协议化三维度体系的 4 阶段已全部完成：

- ✅ R661：三维度体系 overview meta article
- ✅ R662：horizontal 解耦 deep dive
- ✅ R663：vertical 解耦 deep dive
- ✅ R664：cross-device 协同 deep dive

下一轮（R665）的开放问题：

1. **三维度全开是否会成为 awesome-harness-engineering v2.0 的新主线**？R661 overview 预测的 v2.0 演进（按维度组织 12 Primitives）是否会被三维度全开的实证推翻？
2. **cross-device 协同的协议层（MCP over relay）何时标准化**？是 Anthropic 主导还是社区自发？
3. **SeemSeam/CCB 是否会成为 cross-device + multi-agent 复合场景的事实标准**？还是会被 1st-party 实现（Cursor iOS multi-agent 或 OpenAI Codex multi-agent）取代？
4. **5 个反模式中最容易踩的是哪个**？从社区 issue 反馈看，「远程桌面当 cross-device」和「mobile 端无限授权」是两个最常见的工程错误。

---

## 十、参考来源

### 10.1 1st-party / 准 1st-party 来源

1. [Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile) — Cursor iOS cross-device 协同协议层
2. [Cursor for iOS blog](https://cursor.com/blog/ios-mobile-app) — Cursor iOS 产品层
3. [OpenAI: Codex 跨设备协作](https://openai.com/index/agents-of-change-mobile-collaboration/) — OpenAI Codex cross-device + Remote SSH
4. [Anthropic: Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview) — control plane SDK 化
5. [Apple Newsroom: Xcode 26.3 unlocks agentic coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/) — execution plane Apple 官方 1st-party
6. [Anthropic: How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) — Trust boundary 体系

### 10.2 社区 / 三方实证

7. [SeemSeam/claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge) — 3,190 ⭐ CCB v8.0.15 multi-agent + cross-device 复合实证
8. [SafeRL-Lab/cheetahclaws](https://github.com/SafeRL-Lab/cheetahclaws) — 747 ⭐ Python agent harness with cloud session sync
9. [Tailscale Serve](https://tailscale.com/kb/1223/serve/) — secure relay 层事实标准
10. [Apple Developer: Live Activities](https://developer.apple.com/documentation/activitykit) — iOS Live Activities 跨设备通知

### 10.3 本仓库关联阅读

- [R661 awesome-harness-engineering 三维度体系 overview](awesome-harness-engineering-three-dimensions-protocolization-2026.md) — 三维度体系综述
- [R662 harness horizontal 解耦 deep dive](harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) — horizontal 解耦姊妹篇
- [R663 harness vertical 解耦 deep dive](harness-vertical-decoupling-control-plane-execution-plane-protocol-2026.md) — vertical 解耦姊妹篇
- [Cursor iOS 移动-云混合 Harness 架构](cursor-ios-mobile-cloud-hybrid-agent-harness-2026.md) — cross-device 高层产品篇
- [Cursor iOS 远程控制协议深度拆解](cursor-ios-architecture-remote-control-handoff-deep-dive-2026.md) — cross-device 协议深度篇
- [OpenAI Codex 跨设备协作深度](openai-codex-cross-device-collaboration-mobile-remote-ssh-2026.md) — cross-device OpenAI 实现
- [OpenAI Codex Anywhere 移动-分布式架构](openai-codex-anywhere-mobile-distributed-agent-access-architecture-2026.md) — cross-device 分布式架构

---

## 十一、TL;DR

**cross-device 协同的范式是「会话状态协议」而非「远程桌面」**。三个 1st-party / 准 1st-party 实现（Cursor iOS + OpenAI Codex + CCB v8.0.15）都收敛到**四个 primitives**：append-only telemetry + cache-first 架构 + source 标签 session 模型 + rewind-safe replay。SeemSeam/CCB 3,190 ⭐ 是 cross-device + horizontal 解耦 + multi-agent orchestration 三维度复合场景的最佳实证标杆。R664 完成 cross-device 协同 deep dive 后，harness 协议化三维度体系的 4 阶段全部完成。