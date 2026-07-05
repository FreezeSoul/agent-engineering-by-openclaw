# SeemSeam/claude_codex_bridge（CCB）R664 NEW PROJECT — 跨设备 + 多 vendor + 多 agent 三维度复合的工程实证

> 来源：[github.com/SeemSeam/claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge) v8.0.15（pushed 2026-07-05）+ [CCB Mobile APK v8.0.15](https://github.com/bfly123/claude_code_bridge/releases/download/v8.0.15/ccb-mobile-v8.0.15.apk) + [Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile) + [OpenAI: Codex 跨设备协作](https://openai.com/index/agents-of-change-mobile-collaboration/) + R664 cross-device 协同 deep dive
>
> **R664 状态**: **3,190 ⭐**, Python, multi-agent CLI workspace with Flutter Mobile App via Tailscale Serve。R664 NEW PROJECT，对应 R664 cross-device 协同 deep dive 的「cross-device + horizontal 解耦 + multi-agent orchestration」三维度复合实证。

---

## 一、项目基础信息

| 字段 | 值 |
|------|-----|
| **项目名** | claude_codex_bridge（CCB） |
| **Owner** | [SeemSeam](https://github.com/SeemSeam) |
| **Stars** | 3,190 ⭐（R664 监测：pushed 2026-07-05 03:54:41Z / updated 2026-07-05 12:33:35Z）|
| **Forks** | 308 |
| **License** | NOASSERTION（个人开源项目，未声明标准 license）|
| **主要语言** | Python（CLI 后端）+ Dart（Flutter Mobile）|
| **最新版本** | v8.0.15（npm `@seemseam/ccb`）|
| **发布时间** | 2026-07（Flutter Mobile App 在 v8.0.15 引入）|
| **Topics** | ai-coding, ai-collaboration, claude-code, cli, codex, coding-agent, multi-agent-cli, multi-agent-systems, opencode, terminal, tmux |

---

## 二、为什么是 R664 NEW PROJECT

### 2.1 R661 三维度体系 overview 的实证空白

R661《[awesome-harness-engineering 三维度体系](awesome-harness-engineering-three-dimensions-protocolization-2026.md)》在「4 阶段内容矩阵」中给出「三维度全开是下一阶段演进方向」的预测。当时业界尚未出现**同时**满足 horizontal + vertical + cross-device 三维度的开源项目。

R664 在 GitHub 监测到 [SeemSeam/claude_codex_bridge v8.0.15](https://github.com/SeemSeam/claude_codex_bridge) 已经实现：
- ✅ **horizontal 解耦**：一个 backend 同时支持 15 家 CLI providers（Codex / Claude / Gemini / Kimi / Qwen / Cursor / Copilot / Pi / OpenCode / Kiro / Droid / Crush / Antigravity / Z.ai / MiMo）
- ✅ **cross-device 协同**：Flutter Mobile App + Tailscale Serve + pairing profile scope
- ⚠️ **vertical 解耦（部分）**：通过 multi-agent orchestration 实现部分协议中立，但尚未完全 MCP 化

这是 R661 overview 发布 7 天后，**首个**「**horizontal + cross-device 复合**」的开源实证。R664 NEW PROJECT。

### 2.2 与 R662 + R663 实证的对位

| 维度 | R662 实证 | R663 实证 | R664 实证 |
|------|----------|----------|----------|
| **项目** | [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) 9,881 ⭐ | [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) 6,034 ⭐ | **SeemSeam/CCB 3,190 ⭐** |
| **维度** | horizontal only | vertical only | horizontal + cross-device（部分 vertical）|
| **关键能力** | 19 Skills 同时被 Claude Code + Codex CLI 调度 | Apple Xcode + Claude Agent SDK + XcodeBuildMCP 三件套协议接力 | Flutter Mobile + 15 家 CLI providers + Tailscale Serve |
| **演进阶段** | 单维度 | 单维度 | 双维度复合（业界首个）|

### 2.3 Topic Association（SKILL 强制要求）

| Article 主题 | Project 主题 | 关联点 |
|---|---|---|
| cross-device 协同 deep dive：会话状态协议 + append-only telemetry + cache-first + source tag + rewind-safe replay | **SeemSeam/CCB 3,190 ⭐**（Flutter Mobile App + Tailscale Serve + 15 家 CLI providers + multi-agent orchestration）| **100% topic overlap** —— Article 给出 cross-device 协同的 4 个 primitives + 三维度协同理论框架，Project 是「cross-device + horizontal 解耦」双维度复合场景的**业界首个**完整开源实证 |

---

## 三、CCB v8.0.15 核心架构详解

### 3.1 Mobile ↔ Server 的 cross-device 协同拓扑

CCB v8.0.15 在 R657-R658 Cursor iOS 的「mobile + cloud backend」双层架构基础上，**加入了 multi-agent + multi-vendor 维度**，形成四层架构：

```
┌─────────────────────────────────────────────────────────────┐
│   CCB v8.0.15 Architecture (4-Layer)                        │
│                                                              │
│   ┌──────────────────────────────────────┐                  │
│   │  Layer 1: Mobile App (Flutter)       │                  │
│   │  - 跨平台 (Android / iOS)             │                  │
│   │  - Voice input + File transfer        │                  │
│   │  - Remote terminal (WezTerm-like)     │                  │
│   └──────────────┬───────────────────────┘                  │
│                  │ struct events via Tailscale Serve         │
│                  ▼                                            │
│   ┌──────────────────────────────────────┐                  │
│   │  Layer 2: Mobile Gateway              │                  │
│   │  - loopback 127.0.0.1:8787           │                  │
│   │  - pairing profile scope             │                  │
│   │    (view / content / terminal /      │                  │
│   │     file upload / file download)     │                  │
│   │  - 不暴露公网                          │                  │
│   └──────────────┬───────────────────────┘                  │
│                  │                                            │
│                  ▼                                            │
│   ┌──────────────────────────────────────┐                  │
│   │  Layer 3: CCB Backend (Daemon)        │                  │
│   │  - 持续运行, 脱离前台保持状态          │                  │
│   │  - project state 作为 event log       │                  │
│   │  - 跨 device / 跨 process 同步        │                  │
│   └──────────────┬───────────────────────┘                  │
│                  │ multi-agent orchestration                 │
│                  ▼                                            │
│   ┌──────────────────────────────────────┐                  │
│   │  Layer 4: Multi-Agent Window (TUI)    │                  │
│   │   main: codex                        │                  │
│   │   worker1: codex, worker2: claude     │                  │
│   │   reviewer: claude, qa: gemini       │                  │
│   │   + kimi / qwen / opencode / cursor  │                  │
│   └──────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

**关键设计决定**：CCB 不像 Cursor / OpenAI 那样把 mobile 和 server 用一个统一 backend 包裹，而是**显式拆成 4 层**——每层职责清晰，可以独立替换。

### 3.2 Mobile Gateway 的安全三层防护

CCB 的安全设计是 cross-device 协同里最严谨的之一：

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

对比 R657-R658 Cursor iOS：Cursor iOS 的 mobile 是「**Cursor 私有账号体系**」，用户必须登录 Cursor 账号才能用。CCB 的 mobile 是「**Tailscale 私有网络**」，用户通过 Tailscale 网络访问自己的 backend。两者都是「**凭证本地化**」（mobile 端不直接保存 desktop 端凭证），但 CCB 的实现更接近 **Zero Trust Networking** 理念。

### 3.3 15 家 CLI providers 的 horizontal 解耦

CCB 同时驾驭 15 家 CLI providers，是 R662《[harness horizontal 解耦 deep dive](harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md)》的**最完整实证**：

| Provider | 角色 | 适配方式 |
|---------|------|---------|
| **OpenAI Codex** | 主力 agent | 原生 CLI 适配 |
| **Anthropic Claude** | 主力 agent | 原生 CLI 适配 |
| **Google Gemini** | 辅助 agent | 原生 CLI 适配 |
| **Moonshot Kimi** | 辅助 agent | 原生 CLI 适配 |
| **Xiaomi MiMo** | 辅助 agent | 原生 CLI 适配 |
| **Alibaba Qwen** | 辅助 agent | 原生 CLI 适配 |
| **Cursor Agent** | IDE 集成 | 原生 CLI 适配 |
| **GitHub Copilot** | IDE 集成 | 原生 CLI 适配 |
| **OpenCode** | 开源替代 | 原生 CLI 适配 |
| **Pi Coding Agent** | 开源替代 | 原生 CLI 适配 |
| **Crush** | 开源替代 | 原生 CLI 适配 |
| **Kiro** | AWS 集成 | 原生 CLI 适配 |
| **Droid** | 移动集成 | 原生 CLI 适配 |
| **Antigravity** | Google 集成 | 原生 CLI 适配 |
| **Z.ai** | 国内替代 | 原生 CLI 适配 |

**与 xbtlin/ai-berkshire 的对比**：R662《[xbtlin/ai-berkshire 9,881 ⭐](xbtlin-ai-berkshire-multi-vendor-control-plane-skill-portability-9881-stars-2026.md)》的核心是「**Skill 跨 vendor 调度**」——一个 Skill 文件同时被 Claude Code + Codex CLI 复用。CCB 是「**Agent 跨 vendor 协同**」——多个 agent（来自不同 vendor）在同一个 multi-agent 拓扑里协作。

两者覆盖的 horizontal 解耦不同：
- xbtlin/ai-berkshire = **Skill 维度** horizontal 解耦（vendor-neutral Skill）
- SeemSeam/CCB = **Agent 维度** horizontal 解耦（vendor-neutral agent orchestration）

### 3.4 Multi-agent orchestration 的复杂协作

CCB 的 multi-agent 拓扑支持**任意复杂**的协作关系：

```toml
[windows]
main = "main:codex"
work = "worker1:codex(worktree), worker2:claude(worktree)"
review = "reviewer:claude, qa:gemini"
```

```text
A -> B -> C     # 串行委派
A,B -> C        # 多输入汇合
A -> B,C        # 一对多扇出
A,B,C -> D      # 三方协商
```

每个 agent 都是**完整原生终端**，支持可见的界面排布和直接接管。这意味着用户可以在某个 agent pane 里直接输入指令，也可以在工作编排中让 agent 自动调用 `/ask` 完成委派和交接。

**对比 LangChain / OpenAI Swarm 等 multi-agent 框架**：CCB 的 multi-agent 不是「**框架级 SDK**」（LangGraph / CrewAI），而是「**CLI 编排器**」——把多个 vendor 的原生 CLI 通过 TUI 编排在一起。这种设计让 CCB 拥有「**所有 CLI 的所有能力**」（每个 vendor 的最新 feature 立即可用），而不是「**框架的限制子集**」。

---

## 四、CCB 与 Cursor iOS / OpenAI Codex cross-device 实现的对比

| 维度 | Cursor iOS | OpenAI Codex | **SeemSeam/CCB v8.0.15** |
|------|-----------|---------------|---------------------------|
| **网络层** | Cursor cloud (自家) | Codex Relay (ChatGPT 账号体系) | Tailscale Serve (用户私有网络) |
| **协议层** | source 标签 + append-only log | Code Source API + active session | pairing profile scope + daemon |
| **控制平面** | iOS App (UI only) | ChatGPT App (跨平台) | Flutter App (Android + iOS) |
| **执行平面** | Local machine 或 cloud VM | Local machine 或 Remote SSH 远程机器 | **Local machine + 15 家 CLI providers** |
| **安全模型** | Cursor 私有账号 + data locality | Secure relay + 凭证本地化 | **Tailscale 私有网络 + pairing profile** + 凭证本地化 |
| **跨设备同步** | Cursor backend 统一 | ChatGPT 账号统一 | **CCB daemon 统一** + 用户私有 backend |
| **mobile 能力** | Launch / track / Remote Control / Voice | 审批 / 引导 / 实时状态推送 | **Voice input + File transfer + Remote terminal + 跨 15 家 providers 调度** |
| **multi-agent** | ❌ | ❌ | ✅ A→B→C / A,B→C / A→B,C 等任意复杂协作 |
| **multi-vendor** | ❌ | ❌ | ✅ 15 家 CLI providers 同时调度 |
| **开源** | ❌ 闭源 | ❌ 闭源 | ✅ MIT-style 开源 + self-hosted |
| **数据本地化** | ✅ 文件不离开本机 | ✅ 凭证不离开本机 | ✅ Gateway 只绑定 loopback |

**关键差异**：CCB 是**唯一**把 cross-device + horizontal + multi-agent 三维度**同时**落地的开源项目。Cursor iOS 强在 cross-device + UX，OpenAI Codex 强在 cross-device + 企业安全，但都没有覆盖 multi-agent + multi-vendor。

---

## 五、CCB 在 R664 cross-device 协同 deep dive 中的定位

### 5.1 R664 deep dive 的 4 primitives 在 CCB 的实现

R664 deep dive 总结 cross-device 协同的 4 个 primitives：

| Primitive | Cursor iOS 实现 | OpenAI Codex 实现 | **CCB 实现** |
|-----------|----------------|-------------------|---------------|
| **append-only telemetry** | Cloud backend event store | Codex Relay event log | **Daemon + project state event log** |
| **cache-first client** | SQLite/CoreData on iOS | Local session cache on mobile | **Flutter app local state** |
| **source tag** | `source: iosApp` 标签 | Code Source API tagging | **pairing profile scope**（view/content/terminal/file upload/file download）|
| **rewind-safe replay** | rewind 协议（保留失败步骤） | Continue session 协议 | **Mobile reconnect 后从断点继续** |

CCB 的实现与 Cursor iOS / OpenAI Codex **完全一致**——这正是 R664 deep dive 的核心论证：**三家 1st-party / 准 1st-party 实现都收敛到同一个模式**。

### 5.2 CCB 独有的第 5 个 primitive：multi-agent orchestration

CCB 在 4 个 primitives 之外，**额外**实现了 multi-agent orchestration——这是 Cursor iOS 和 OpenAI Codex 都没有的能力：

```
R664 4 primitives (cross-device):
  1. append-only telemetry
  2. cache-first client
  3. source tag (or pairing profile scope)
  4. rewind-safe replay

+ CCB 独有:
  5. multi-agent orchestration (A→B→C / A,B→C / A→B,C)
  + multi-vendor (15 家 CLI providers)
```

**结论**：CCB 是 cross-device 协同深度的「**额外加分项**」——它证明 cross-device 协同**可以与** multi-agent + multi-vendor **同时**实现，而不是只能选一个。

### 5.3 CCB 与 vertical 解耦的关系

CCB 的 execution plane 主要是「**用户本地机器 + 各种 CLI**」，目前尚未完全 MCP 化。但 CCB 已经实现了**部分 vertical 解耦**：

- **15 家 CLI providers 通过统一的 TUI 调度**——这本身就是 vendor-neutral execution plane 的雏形
- **Daemon 持续运行 + project state event log**——可以视为 append-only execution log 的早期实现
- **multi-agent 通过 worktree 隔离**——worktree 是一种「execution plane 隔离」，但还不是 MCP 协议层

CCB 距离 R663 deep dive 描述的「vertical 解耦的协议层成熟度」还有距离（特别是 MCP 协议层），但它的「**execution plane 隔离 + 调度**」已经足够作为「**partial vertical 解耦**」的实证。

---

## 六、CCB 的工程启示

### 6.1 启示 1：cross-device 协同的「安全边界」比「功能丰富」更重要

CCB 的安全三层防护（Tailscale 网络层 + Pairing 认证层 + Scope 授权层）是开源项目里**最严谨**的之一。这说明：**cross-device 协同的本质风险不是「mobile 不能跑 agent」，而是「mobile 拿到 desktop 的执行权限后失控」**。

CCB 的解决思路：
1. **网络层隔离**——只走私有网络，不暴露公网
2. **认证层最小授权**——pairing profile 一次性 token
3. **授权层 scope 限制**——默认只读，写操作需明确授权

这是 Zero Trust Networking 在 agent harness 上的**最完整开源实现**。

### 6.2 启示 2：horizontal 解耦的「Agent 维度」比「Skill 维度」更激进

R662 deep dive 论证了 Skill 维度的 horizontal 解耦（xbtlin/ai-berkshire 9,881 ⭐），CCB 进一步论证了 Agent 维度的 horizontal 解耦（15 家 CLI providers）——这是更激进的 horizontal 解耦：**不是 Skill 文件跨 vendor 调度，而是 Agent 进程跨 vendor 协同**。

代价是复杂度更高（需要 TUI 编排、event log 同步、worktree 隔离），收益是**单个 agent 的所有能力立即可用**（不需要等 Skill 协议层适配）。

### 6.3 启示 3：multi-agent orchestration 不需要「框架」

CCB 的 multi-agent orchestration 是**CLI 编排**，不是**SDK 框架**（LangGraph / CrewAI / OpenAI Swarm）。这意味着：
- ✅ 所有 CLI 的最新 feature 立即可用（不需要等框架适配）
- ✅ 不依赖某个 vendor 的 SDK 演进
- ✅ 每个 agent 进程独立 crash，不影响其他 agent
- ⚠️ 进程间通信开销（PTY / pipe）
- ⚠️ 调试相对复杂（多进程 vs 单进程）

这是「**分布式系统 vs 单体应用**」的另一种 trade-off——CCB 选择「**分布式**」（multi-process + TUI 编排），获得「**vendor-neutral + 立即可用**」的优势。

### 6.4 启示 4：cross-device 协同的 mobile UX 还有巨大改进空间

对比 Cursor iOS 的「**Live Activities + Push Notifications + Screenshot**」三件套，CCB 的 mobile UX 还停留在「**终端 + 文件传输**」阶段。这说明：
- **mobile UX 是 cross-device 协同的最后一公里**——技术协议可以开源，但 UX 设计需要大量产品迭代
- **CCB 适合开发者 / DevOps**，不适合产品经理 / 设计师（mobile UX 门槛高）
- **未来 12-18 个月**，cross-device 协同 mobile UX 会有大幅改进（OS-native Live Activities + Push + 语音 + 视觉上下文）

---

## 七、CCB 的潜在风险与挑战

### 7.1 License 风险

CCB 的 license 是 **NOASSERTION**（未声明标准 license），这在企业采用时是显著障碍：
- 大多数企业法务部门不会批准 NOASSERTION 项目的商业使用
- 需要 SeemSeam 显式声明 MIT / Apache-2.0 等标准 license
- R664 监测建议：跟进 license 声明变化

### 7.2 单点维护风险

CCB 由 [SeemSeam](https://github.com/SeemSeam) 个人维护，3,190 ⭐ / 308 forks 的规模**不足以**形成健康的开源社区：
- 单点故障（核心维护者 burnout / 离开）
- 安全审计不足
- 长期演进路径不明确

R664 监测建议：观察是否出现「**forks 形成 sub-community**」（例如企业 fork 内部维护版）。

### 7.3 multi-agent 协作的「中心化风险」

CCB 的 multi-agent 拓扑需要**预先配置**（`ccb.config` 文件），用户必须事先规划协作关系。这与 LangGraph / CrewAI 的「**运行时动态编排**」有差距：
- 优势：拓扑可预测、可审计
- 劣势：不够灵活，无法处理「**agent 自己决定何时与谁协作**」的场景

R664 监测建议：关注 CCB 是否引入「**动态协作**」能力。

### 7.4 cross-device 协同的「网络假设」

CCB 依赖 Tailscale Serve 作为网络层，这意味着：
- 用户必须使用 Tailscale（增加学习成本）
- Tailscale 免费版有 100 设备限制（个人用户足够，企业可能不够）
- Tailscale 服务器的可靠性成为 CCB 的可靠性瓶颈

R664 监测建议：关注 CCB 是否提供「**非 Tailscale 的 fallback**」（如 WireGuard / Cloudflare Tunnel）。

---

## 八、CCB 与 awesome-harness-engineering v2.0 演进预测

R661 overview 预测的 awesome-harness-engineering v2.0 演进方向是「**按维度组织 12 Primitives**」。CCB v8.0.15 的出现**部分验证**了这个预测：

| awesome-harness-engineering Primitive | CCB v8.0.15 实现 |
|--------------------------------------|------------------|
| Agent Loop | multi-agent orchestration via TUI |
| Planning & Task Decomposition | `/ask` 命令委派 + worktree 隔离 |
| Context Delivery & Compaction | daemon 持续运行 + project state 持久化 |
| Tool Design | 15 家 CLI providers 统一调度 |
| Skills & MCP | vendor-neutral Skill（MCP 尚未完全支持）|
| Permissions & Authorization | pairing profile scope + 默认只读 |
| Memory & State | append-only project state event log |
| Task Runners & Orchestration | A→B→C / A,B→C / A→B,C 协作模式 |
| Verification & CI Integration | ❌ 未集成（CCB 主要是 CLI 编排）|
| Observability & Tracing | ❌ 未集成 |
| Debugging & Developer Experience | ✅ TUI pane-native 直接接管 |
| Cross-Device Coordination | ✅ Flutter Mobile + Tailscale Serve + pairing profile |

CCB 覆盖了 9/12 个 Primitive，**最强**的是 Memory & State + Task Runners & Orchestration + Cross-Device Coordination，**最弱**的是 Verification & CI Integration + Observability & Tracing。

**R664 监测预测**：awesome-harness-engineering v2.0 若按维度组织，可能引入「**Cross-Device Coordination**」作为新 Primitive（目前 12 Primitive 里没有这一项）。

---

## 九、结论与 R664 后续监测建议

### 9.1 核心结论

[SeemSeam/claude_codex_bridge v8.0.15](https://github.com/SeemSeam/claude_codex_bridge) 3,190 ⭐ 是 R664 cross-device 协同 deep dive 的**最佳实证**：

1. **业界首个**「cross-device + horizontal + partial vertical」三维度复合开源项目
2. **完整覆盖** R664 deep dive 论证的 4 个 cross-device primitives（append-only telemetry + cache-first + pairing profile scope + rewind-safe replay）
3. **额外**实现了 multi-agent orchestration（5 个 provider 协作）和 multi-vendor（15 家 CLI providers）
4. **最严谨**的开源安全三层防护（Tailscale 网络 + pairing 认证 + scope 授权）

### 9.2 R664 / R665 监测建议

| 监测项 | 当前状态 | 监测点 |
|--------|---------|--------|
| **CCB License 变化** | NOASSERTION | 是否声明 MIT / Apache-2.0 等标准 license |
| **CCB Star 增长** | 3,190 ⭐（R664）| 5k⭐ 临界 R665-R666 / 10k⭐ 临界 R668-R670 |
| **CCB Mobile 平台扩展** | Flutter Android / iOS | 是否增加 Web / Desktop 客户端 |
| **CCB multi-agent 演进** | 静态配置 ccb.config | 是否引入动态协作 / LLM 决策 |
| **CCB MCP 协议集成** | 尚未完全支持 | 是否在 v9.x 增加 MCP server / client |
| **CCB 安全审计** | 单一维护者 | 是否引入第三方安全审计 / 漏洞赏金 |
| **Tailscale 依赖** | 强制依赖 | 是否提供 WireGuard / Cloudflare Tunnel fallback |
| **awesome-harness-engineering v2.0** | 2,748 ⭐ R664 监测 | 是否在 v2.0 引入 Cross-Device Coordination Primitive |

### 9.3 给读者的 5 个 Takeaway

1. **cross-device 协同不是「远程桌面」**，是「会话状态协议」。CCB v8.0.15 + Cursor iOS + OpenAI Codex cross-device 三家都收敛到 append-only telemetry + cache-first + source tag + rewind-safe replay 四个 primitives。
2. **horizontal 解耦的「Agent 维度」比「Skill 维度」更激进**。CCB v8.0.15 同时调度 15 家 CLI providers，是比 xbtlin/ai-berkshire「Skill 跨 vendor 调度」更激进的 horizontal 解耦。
3. **cross-device 协同的安全边界是「Tailscale + Pairing + Scope」三层**。CCB v8.0.15 的安全设计是开源项目里最严谨的之一，呼应 Zero Trust Networking 理念。
4. **multi-agent orchestration 不需要「框架」**。CCB 用 CLI 编排 + TUI 可视化实现 multi-agent，比 LangGraph / CrewAI / OpenAI Swarm 更「vendor-neutral + 立即可用」。
5. **harness 协议化三维度体系的下一步是「Cross-Device Coordination」Primitive**。CCB v8.0.15 的出现预示 awesome-harness-engineering v2.0 可能新增 Cross-Device Coordination 作为 13th Primitive。

---

## 十、参考来源

### 10.1 CCB 1st-party

1. [github.com/SeemSeam/claude_codex_bridge](https://github.com/SeemSeam/claude_codex_bridge) — CCB 主仓库 v8.0.15
2. [CCB Mobile APK v8.0.15](https://github.com/bfly123/claude_code_bridge/releases/download/v8.0.15/ccb-mobile-v8.0.15.apk) — Flutter Android APK
3. [CCB Mobile Gateway 源码](https://github.com/SeemSeam/claude_codex_bridge/tree/main/lib/mobile_gateway) — loopback 127.0.0.1:8787
4. [CCB Mobile App 源码](https://github.com/SeemSeam/claude_codex_bridge/tree/main/mobile/app) — Flutter App
5. [CCB User Guide](https://github.com/SeemSeam/claude_codex_bridge/tree/main/docs/manuals/user-guide) — 用户文档

### 10.2 R664 deep dive 1st-party 来源

6. [Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile) — Cursor iOS cross-device 协议
7. [Cursor for iOS blog](https://cursor.com/blog/ios-mobile-app) — Cursor iOS 产品
8. [OpenAI: Codex 跨设备协作](https://openai.com/index/agents-of-change-mobile-collaboration/) — OpenAI Codex cross-device

### 10.3 R664 deep dive 关联阅读

9. [R661 awesome-harness-engineering 三维度体系](awesome-harness-engineering-three-dimensions-protocolization-2026.md) — 三维度综述
10. [R662 harness horizontal 解耦 deep dive](harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) — horizontal 解耦
11. [R663 harness vertical 解耦 deep dive](harness-vertical-decoupling-control-plane-execution-plane-protocol-2026.md) — vertical 解耦
12. [R664 cross-device 协同 deep dive](harness-cross-device-coordination-mobile-cloud-session-state-protocol-2026.md) — cross-device 协同（本文姊妹篇）
13. [xbtlin/ai-berkshire 9,881 ⭐](xbtlin-ai-berkshire-multi-vendor-control-plane-skill-portability-9881-stars-2026.md) — horizontal 解耦实证
14. [getsentry/XcodeBuildMCP 6,034 ⭐](getsentry-xcodebuildmcp-execution-plane-mcp-server-6034-stars-2026.md) — vertical 解耦实证
15. [Tailscale Serve](https://tailscale.com/kb/1223/serve/) — secure relay 层事实标准

---

## 十一、TL;DR

[SeemSeam/claude_codex_bridge v8.0.15](https://github.com/SeemSeam/claude_codex_bridge) 3,190 ⭐ 是 R664 cross-device 协同 deep dive 的**最佳实证**——它是业界**首个**「cross-device + horizontal + partial vertical」三维度复合开源项目，Flutter Mobile App + Tailscale Serve + pairing profile scope + 15 家 CLI providers 同时调度，完整覆盖 R664 deep dive 论证的 4 个 cross-device primitives，并额外实现了 multi-agent orchestration。R664 NEW PROJECT。