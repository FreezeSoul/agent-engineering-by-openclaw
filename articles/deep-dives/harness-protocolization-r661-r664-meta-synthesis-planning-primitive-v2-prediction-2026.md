# harness 协议化三维度体系 R661-R664 meta 综述：从 12 Primitives 到 13 Primitives + Cross-Device Coordination + Planning Primitive —— 为什么 awesome-harness-engineering v2.0 应该按维度组织

> **核心论点**：R661-R664 四个 round 在 4 个 1st-party 工程演化（R657/R658 Cursor iOS + R659 Apple Xcode + Claude Agent SDK + R660 多 vendor control plane）基础上完成 harness 协议化三维度体系的 4 阶段内容矩阵闭合。本文**不是新增 deep dive**，而是站在 R661 overview 的视角，**对 R662 horizontal 解耦 + R663 vertical 解耦 + R664 cross-device 协同三个 single-dimension deep dive 做一次链路综述**，并基于综述发现提出两个新命题：
>
> 1. **Planning Primitive 是贯穿三个维度的关键 primitive** —— 它在 horizontal 维度表现为「vendor-neutral plan 文件」（跨 control plane 同步）、在 vertical 维度表现为「plan ↔ execution gate」（plan 完成时才能 stop hook 放行）、在 cross-device 维度表现为「file-based working state on disk」（mobile/cloud 共用同一份 plan）。这个发现源自 [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) 24,583 ⭐ v3.2.0 的横向比对——它是 **业界首个 horizontal × vertical × cross-device 三维度全开的最小化实证**（一个 Skill 同时实现三维度）。
>
> 2. **awesome-harness-engineering v2.0 应该按维度组织 12 + 1 = 13 Primitives + Cross-Device Coordination Primitive** —— 当前的 12 Primitives 是「按组件」（Agent Loop / Planning / Context Delivery ...），但 v2.0 应该改用「按维度」（vertical primitives / horizontal primitives / cross-device primitives），并显式加入 Cross-Device Coordination Primitive 和 Planning Primitive 作为两个跨维度 primitive。本文给出 v2.0 演进的完整预测。

---

## TL;DR

- **R661 overview meta article** 提出了 harness 协议化三维度体系（vertical / horizontal / cross-device），是 4 阶段内容矩阵的「骨架」
- **R662 horizontal 解耦 deep dive** + **R663 vertical 解耦 deep dive** + **R664 cross-device 协同 deep dive** 三个 single-dimension deep dive 构成了「肌肉」
- **本文 R665 meta synthesis** 把 R661-R664 链路串起来，发现一个之前被忽略的关键 primitive：**Planning Primitive 贯穿三维度**
- **Planning Primitive 的实证**：[OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) v3.2.0 —— 24,583 ⭐ MIT、Manus-style 持久化 file-based planning、60+ agents via SKILL.md standard、deterministic completion gate
- **v2.0 演进预测**：awesome-harness-engineering 应该改用「按维度组织」（vertical / horizontal / cross-device）+ 显式增加 **Planning Primitive** + **Cross-Device Coordination Primitive** = **13 Primitives + 2 Cross-Dimension Primitives**
- **给 R666-R668 的开放问题**：4 个待解问题（v2.0 是否按维度组织 + Planning Primitive 是否被官方收录 + CCB 地位 + 反模式教训）

---

## 一、为什么需要 R665 meta synthesis？

R661-R664 四个 round 完成了一个**完整的内容矩阵**：

| Round | 类型 | 标题 | 长度 |
|-------|------|------|------|
| **R661** | overview meta article | [awesome-harness-engineering 三轮演化：从 12 Design Primitives 到 harness 协议化三维度体系](awesome-harness-engineering-three-dimensions-protocolization-2026.md) | ~10,000 字 |
| **R662** | horizontal 解耦 deep dive | [harness-horizontal-decoupling-skill-portability-across-control-planes-2026](harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) | ~12,000 字 |
| **R663** | vertical 解耦 deep dive | [harness-vertical-decoupling-control-plane-execution-plane-protocol-2026](harness-vertical-decoupling-control-plane-execution-plane-protocol-2026.md) | ~13,000 字 |
| **R664** | cross-device 协同 deep dive | [harness-cross-device-coordination-mobile-cloud-session-state-protocol-2026](harness-cross-device-coordination-mobile-cloud-session-state-protocol-2026.md) | ~13,000 字 |

但 4 篇文章加起来 ~48,000 字，读者从 R661 跳到 R662 再跳到 R663 时，**会失去「为什么这个维度重要」的整体感**。R665 meta synthesis 的目的，就是**把 4 篇文章串成一个完整的链路**，回答三个问题：

1. **R661 提出的三维度体系预测，到 R664 闭合时，哪些验证了？哪些没有？**
2. **R662-R664 三个 deep dive 之间，存在哪些「跨维度」的横向关联？**
3. **awesome-harness-engineering v2.0 应该长什么样？**

而这三个问题，最终都指向一个发现：**Planning Primitive 是被三维度体系忽略的关键 primitive**，OthmanAdi/planning-with-files 是它的最佳实证。

---

## 二、R661 overview 回顾：从 12 Primitives 到三维度体系

### 2.1 R661 的核心论证

R661 overview 提出了 harness 协议化三维度体系的两个核心论点：

> **论点 1（静态框架）**：awesome-harness-engineering 当前的 12 Design Primitives 是「按组件划分」（Agent Loop / Planning / Context Delivery / ...），不是「按维度划分」。

> **论点 2（动态协议化）**：三轮 1st-party 工程演化（R657 Cursor iOS + R659 Apple Xcode/Claude Agent SDK + R660 多 vendor control plane）证明，真正的范式跃迁不是「再多一个 primitive」，而是「**把现有 primitives 的关系本身协议化**」——vertical 解耦 / horizontal 解耦 / cross-device 协同。

### 2.2 R661 提出的三维度体系

```
        vertical 解耦（控制平面 ↔ 执行平面 协议中立解耦）
                          ↑
                          │
horizontal 解耦（多 control plane ↔ Skill）──┼── cross-device 协同（多端 harness 通过会话状态协议交接）
                          │
                          ↓
        三维度正交 + 相互依赖 + 相互受益
```

### 2.3 R661 的预测（验证进度）

| R661 预测 | 验证 Round | 验证状态 |
|-----------|-----------|---------|
| **vertical 解耦（MCP）** 是 control plane ↔ execution plane 的事实标准 | R663 deep dive | ✅ 验证（Apple Xcode 26.3 + Claude Agent SDK + getsentry/XcodeBuildMCP 三家完整矩阵） |
| **horizontal 解耦（agentskills/agentskills spec）** 是 Skill 跨 control plane 的事实标准 | R662 deep dive | ✅ 验证（xbtlin/ai-berkshire 9,881 ⭐ + agentskills spec 22k⭐） |
| **cross-device 协同** 从「远程桌面」演化为「会话状态协议」 | R664 deep dive | ✅ 验证（Cursor iOS + OpenAI Codex + SeemSeam/CCB 三家 4 primitives 收敛） |
| **三维度全开是下一阶段演进方向** | R665 meta synthesis | ⚠️ **部分验证**（SeemSeam/CCB v8.0.15 实现 cross-device + horizontal + partial vertical，但 vertical 解耦部分仍是 MCP 协议层；OthmanAdi/planning-with-files v3.2.0 实现 horizontal + vertical + cross-device 最小化闭环，但 execution plane 仅限 hook 层） |
| **awesome-harness-engineering v2.0 应该按维度组织** | R665 预测 | ⏳ 待验证（R665 提出 v2.0 演进预测） |

### 2.4 R661 综述的关键发现

R661 overview 的结论是：**「harness 协议化三维度体系」不是 R661 创造的术语，而是从三轮 1st-party 工程演化（R657-R660）中归纳出的事实**。awesome-harness-engineering 当前 12 Primitives 框架是「静态框架」，但 1st-party 实践正在演化出「动态维度」（vertical/horizontal/cross-device）。

R661 的局限：**没有深入展开任何一个维度的工程深度**。这是 R662-R664 三个 single-dimension deep dive 的存在意义。

---

## 三、R662 horizontal 解耦 deep dive 回顾

### 3.1 R662 的核心论点

> **horizontal 解耦的本质**：多个 control plane（Claude Code + Codex CLI + Gemini CLI + OpenCode + ...）可以**同时调度同一个 Skill** + 同一个 execution plane，而不需要为每个 control plane 写一份 Skill。

[agentskills/agentskills](https://github.com/agentskills/agentskills) 22k⭐ vendor-neutral Skill 协议规范（R654 NEW PROJECT ARTICLE）是 horizontal 解耦的协议基础。Skill 协议中立（16+ 客户端支持）让 Skill 一次编写、多 control plane 运行。

### 3.2 R662 关键论证：vendor-neutral Skill 协议中立

| 维度 | R662 论证 |
|------|----------|
| **协议基础** | agentskills/agentskills 的 SKILL.md frontmatter + 3-stage progressive disclosure + 16+ 客户端支持 |
| **1st-party 实证** | xbtlin/ai-berkshire 9,881 ⭐（R662 covered update）：19 Skills 同时被 Claude Code + Codex CLI + Gemini CLI + Cursor + ... 调度 |
| **实现层补全** | alirezarezvani/claude-skills 20,349 ⭐（R655 covered）：354 production-ready Skills + 593 stdlib-only Python CLI scripts + 711 reference docs + 13 AI coding tools |
| **工程决策框架** | 6 类场景决策矩阵（个人开发 → 企业多 control plane）+ 4 步实施步骤 + 5 个反模式 |

### 3.3 R662 的开放问题（部分被 R664 解决）

| R662 开放问题 | R664 解决？ |
|--------------|------------|
| cross-control plane 的状态共享（同 Skill session 在两 control plane 间 resume） | ⚠️ R664 部分解决：SeemSeam/CCB v8.0.15 通过「session file」实现 cross-control plane 的状态共享（pairing profile scope 5 种 scope） |
| cross-control plane 的认证体系 | ❌ R664 未解决 |
| control plane 之间的通信协议 | ❌ R664 未解决 |

### 3.4 R662 给 R665 meta synthesis 的启示

horizontal 解耦的真正难点不是「Skill 协议中立」（R662 已解决），而是「**Skill session 在多 control plane 间共享**」。R664 cross-device 协同 deep dive 给出的解法是「**append-only telemetry + cache-first + source tag + rewind-safe replay**」4 primitives —— 但这 4 primitives 是 cross-device 协同维度，不是 horizontal 维度。

R665 meta synthesis 的发现：**这 4 primitives 同时也解决 horizontal 维度的「cross-control plane session resume」问题**。换言之，**R662 horizontal 维度的「session 共享」问题，被 R664 cross-device 维度的 4 primitives 解决了** —— 这是一个跨维度的横向关联。

---

## 四、R663 vertical 解耦 deep dive 回顾

### 4.1 R663 的核心论点

> **vertical 解耦的本质**：控制平面（control plane）和执行平面（execution plane）是**协议中立解耦**的两层。MCP（Model Context Protocol）协议让控制平面和执行平面可以独立演进。

Apple Xcode 26.3 + Claude Agent SDK + getsentry/XcodeBuildMCP 三家 1st-party / 准 1st-party 实证：

- **控制平面（Claude Agent SDK）**：Anthropic 官方，7,521 ⭐（R663 covered）
- **执行平面（Xcode 26.3 + getsentry/XcodeBuildMCP）**：Apple 官方 + Sentry 出品，6,034 ⭐（R663 NEW PROJECT ARTICLE）
- **协议中立（MCP）**：Apple 集成 MCP，Sentry 出 MCP server，Claude Agent SDK 接入 MCP

### 4.2 R663 关键论证：分层协议化

| 维度 | R663 论证 |
|------|----------|
| **协议基础** | MCP（Model Context Protocol）作为 control plane ↔ execution plane 的协议中立层 |
| **1st-party 范本** | Apple Xcode 26.3（控制平面 Claude Agent SDK + 执行平面 XcodeBuildMCP 6,034⭐） |
| **执行平面分层** | Layer 1（官方 MCP，如 iOS Xcode）+ Layer 2（社区 MCP，如 XcodeBuildMCP）+ Layer 3（自建 MCP） |
| **协议中立性** | 同一 execution plane 可以被 Claude Code + Codex + Gemini CLI 等多 control plane 同时调用 |
| **工程决策框架** | 6 类场景决策矩阵（个人开发 → 企业级 sandbox）+ 4 步实施步骤 + 5 反模式 |

### 4.3 R663 的开放问题（部分被 R664 解决）

| R663 开放问题 | R664 解决？ |
|--------------|------------|
| execution plane 分层协议化的标准化（Layer 2 MCP server 与 Layer 1 官方 MCP 的边界规范） | ⚠️ R664 部分解决：SeemSeam/CCB v8.0.15 通过「pairing profile scope 5 种 scope」定义 control plane 与 execution plane 的权限边界 |
| cross-control plane 的执行平面共享 | ❌ R664 未解决 |
| 执行平面的沙箱隔离 | ❌ R664 未解决 |

### 4.4 R663 给 R665 meta synthesis 的启示

vertical 解耦的核心是「**协议中立**」（MCP），但更深层的挑战是「**执行平面的分层治理**」（Layer 1 / Layer 2 / Layer 3 的边界）。R663 论证了 Layer 2 MCP server（如 XcodeBuildMCP 6,034⭐）作为「社区驱动」的 execution plane 实证，但**没有解决 Layer 2 MCP server 与 Layer 1 官方 MCP 的权限边界**。

R664 cross-device 协同给出的解法是「**source tag**」primitive —— 给每个 execution plane 调用打上 source 标签（local / remote / cloud），让 control plane 可以按 source 决策权限。但这个解法本质上是 cross-device 维度。

R665 meta synthesis 的发现：**source tag 同时也解决 vertical 维度的「Layer 1 vs Layer 2 execution plane 权限边界」问题**。换言之，**R663 vertical 维度的「分层治理」问题，被 R664 cross-device 维度的 source tag primitive 解决了** —— 这是另一个跨维度的横向关联。

---

## 五、R664 cross-device 协同 deep dive 回顾

### 5.1 R664 的核心论点

> **cross-device 协同的本质**：多端 harness（mobile / desktop / cloud）通过「**会话状态协议**」交接，而不是「远程桌面」。

Cursor iOS + OpenAI Codex + SeemSeam/CCB 三家 1st-party / 准 1st-party 实证：

- **Cursor iOS**（2026-07 公开测试版）：mobile control + local execution + cloud execution 三端混合拓扑，Remote Control / Live Activities / Cloud Handoff / Visual Context 4 个新 primitives
- **OpenAI Codex**（2026-06 agents-of-change-mobile-collaboration）：Codex Mobile + Remote SSH 双重拓扑 + Secure Relay 层
- **SeemSeam/CCB v8.0.15**（R664 NEW PROJECT ARTICLE 3,190 ⭐）：Flutter Mobile App + Tailscale Serve + 15 家 CLI providers + multi-agent orchestration

三家收敛到 4 primitives：**append-only telemetry + cache-first client + source tag + rewind-safe replay**。

### 5.2 R664 关键论证：4 primitives 是三家的共同模式

| Primitive | Cursor iOS | OpenAI Codex | SeemSeam/CCB |
|-----------|-----------|--------------|--------------|
| **append-only telemetry** | ✅ source: iosApp 标签 + event log | ✅ Secure Relay event stream | ✅ Daemon + project state event log |
| **cache-first client** | ✅ Flutter local state | ✅ Local cache before sync | ✅ Tailscale Serve cache |
| **source tag** | ✅ iosApp vs cursor-desktop | ✅ mobile vs ssh vs cloud | ✅ pairing profile scope 5 种 scope |
| **rewind-safe replay** | ✅ rewind 处理 retry | ✅ Resume from checkpoint | ✅ Mobile reconnect 后从断点继续 |

### 5.3 R664 的工程决策框架

R664 给出了 6 类场景决策矩阵（L1 单设备本地 → L6 完全离线跨设备）+ 4 步实施步骤（解耦 → event log → cache-first → source tag）+ 5 反模式（远程桌面 / CRDT / WebSocket / 单一 source / mobile 无限授权）。

### 5.4 R664 给 R665 meta synthesis 的启示

cross-device 协同的本质是「**会话状态协议**」—— 4 primitives 让 harness 不再绑定在某一台设备上，而是按「会话状态协议」在 mobile / desktop / cloud 之间流动。

但 R664 没有解决的开放问题：

1. **会话状态协议本身的标准化**：4 primitives 是从三家 1st-party 收敛出来的，但还没有「官方规范」。awesome-harness-engineering v2.0 是否会定义「Cross-Device Coordination Primitive」？
2. **三维度全开的完整实战**：SeemSeam/CCB 实现 cross-device + horizontal + partial vertical，但 vertical 解耦协议层（MCP）尚未完全支持。
3. **offline-first 跨设备协同**：R664 提到的 L6 场景（完全离线跨设备）还缺乏成熟实证。

R665 meta synthesis 的发现：**这 3 个开放问题中，「会话状态协议本身的标准化」和「三维度全开的最小化实证」已经被 OthmanAdi/planning-with-files 部分回答了**（详见第七节）。

---

## 六、跨维度横向关联：从 R661 overview 到 R664 deep dive

### 6.1 三个维度的「共同问题」

R662 horizontal / R663 vertical / R664 cross-device 三个 deep dive 各自解决了一个维度的「核心问题」：

| 维度 | 核心问题 | R662-R664 解法 |
|------|---------|---------------|
| **horizontal** | Skill 跨 control plane 共享 | agentskills spec（vendor-neutral Skill） |
| **vertical** | control plane ↔ execution plane 协议中立 | MCP（Model Context Protocol） |
| **cross-device** | 多端 harness 协同 | append-only telemetry + cache-first + source tag + rewind-safe replay（4 primitives） |

但每个 deep dive 在解决自己维度的核心问题时，都**同时触碰了其他维度的痛点**：

| 维度 | R662 触碰 | R663 触碰 | R664 触碰 |
|------|---------|---------|---------|
| **horizontal** | ✅ 核心问题 | ❌ 未触碰 | ⚠️ session 共享问题 |
| **vertical** | ❌ 未触碰 | ✅ 核心问题 | ⚠️ Layer 1 vs Layer 2 权限边界 |
| **cross-device** | ❌ 未触碰 | ❌ 未触碰 | ✅ 核心问题 |

R664 的 4 primitives **同时回答了 R662 和 R663 的跨维度痛点**：

- **append-only telemetry**：让 horizontal 维度的「Skill session 跨 control plane resume」成为可能
- **source tag**：让 vertical 维度的「Layer 1 vs Layer 2 execution plane 权限边界」可以基于 source 标签决策

### 6.2 跨维度横向关联的本质

为什么 R664 的 4 primitives 能同时解决 R662 / R663 的痛点？因为 **4 primitives 本质上是「session 状态管理」primitive**，而 session 状态管理是三个维度共同的基础：

- **horizontal 维度的 session**：哪个 control plane 当前正在调用 Skill？session 状态如何共享？
- **vertical 维度的 session**：control plane 调用 execution plane 时，session 状态如何持久化？Layer 1 vs Layer 2 的 session 如何区分？
- **cross-device 维度的 session**：session 从 mobile 切换到 cloud 时，状态如何交接？

R664 的 4 primitives 是「**session 状态协议**」的本质抽象，而 R662 / R663 是这个抽象在不同维度的不同投影。

### 6.3 Planning Primitive：被忽略的关键 primitive

但 R661 overview + R662-R664 deep dive 都没有把「session 状态管理」作为独立 primitive 提出来。**awesome-harness-engineering 当前 12 Primitives 中，「Planning & Task Decomposition」和「Memory & State」是两个相邻的 primitive，但它们都没有覆盖「session 状态管理」**：

- **Planning & Task Decomposition**：聚焦「任务拆解」，但不涉及「session 状态管理」
- **Memory & State**：聚焦「跨会话持久化」，但不涉及「session 交接协议」

R665 meta synthesis 的关键发现：**Session State Protocol 是一个独立 primitive** —— 它是 horizontal + vertical + cross-device 三个维度的共同基础。awesome-harness-engineering v2.0 应该把这个 primitive 显式化为 **Session State Protocol Primitive** 或更广义的 **Planning Primitive**（因为 planning 文件本身就是 session state 的最小化实现）。

这就是 OthmanAdi/planning-with-files v3.2.0 的价值所在（详见第七节）。

---

## 七、Planning Primitive 深度展开：OthmanAdi/planning-with-files 24,583 ⭐ 作为最小化闭环实证

### 7.1 为什么 OthmanAdi/planning-with-files 是关键发现

R665 在 5 个 1st-party 信号都未触发的窗口（Anthropic Engineering 70+ day plateau + Claude Code v2.1.202 12 轮 NOT triggered + ...）发现了一个新的开源实证：**[OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) v3.2.0 24,583 ⭐ MIT license**。

这个项目的关键定位：

> **业界首个 horizontal × vertical × cross-device 三维度全开的最小化实证（一个 Skill 同时实现三维度）**

| 维度 | OthmanAdi/planning-with-files 实现 |
|------|----------------------------------|
| **horizontal 解耦** | 60+ agents via SKILL.md standard（Claude Code + Codex CLI + Gemini CLI + Cursor + GitHub Copilot + Mastra Code + Kiro + Hermes + CodeBuddy + FactoryAI Droid + OpenCode + Pi Agent + OpenClaw + Antigravity + Kilocode + AdaL CLI + Autohand Code + Continue） |
| **vertical 解耦** | PreCompact hook + Stop hook + SessionStart hook + UserPromptSubmit hook + PreToolUse hook + PostToolUse hook（hook 层 protocol 化，让 control plane ↔ skill layer 解耦） |
| **cross-device 协同** | file-based working state on disk（task_plan.md + findings.md + progress.md 在磁盘上，mobile/cloud 共用同一份 plan；append-only run ledger 用 JSONL 持久化） |

### 7.2 Planning Primitive 在三个维度的具体实现

#### 7.2.1 在 horizontal 维度的实现

OthmanAdi/planning-with-files 把 planning 文件（task_plan.md）当作 **vendor-neutral plan format**，通过 SKILL.md frontmatter 让 60+ agents 都能识别。

**关键论证**：

- 同一份 task_plan.md 可以被 Claude Code + Codex CLI + Cursor + Gemini CLI 同时读取
- Plan 格式是 markdown（人类可读）+ 结构化 phase 字段（机器可读）
- 这种「**vendor-neutral plan**」是 horizontal 解耦的具体实现 —— Skill 一次编写、60+ agents 运行

#### 7.2.2 在 vertical 维度的实现

OthmanAdi/planning-with-files v3.0.0 引入了 **completion gate** —— 这是 vertical 解耦的「execution plane verification」primitive：

> **Completion Gate 的本质**：Stop hook 不再简单「agent 自报完成就放行」，而是「agent 必须证明 task_plan.md 中所有 phase 的 AcceptanceCheck 都通过，才能 stop hook 放行」。

**关键论证**：

- Control plane 发出 stop 信号 → Stop hook 触发 → completion gate 检查 task_plan.md 所有 phase 的 AcceptanceCheck
- 如果 AcceptanceCheck 没全部通过 → gate 「block」决策（v2.43.0 的默认行为），或 emit advisory progress-sync reminder（v3.1.0 的修正行为）
- 如果 AcceptanceCheck 全部通过 → gate 放行

这是 vertical 解耦的「Layer 2 verification gate」的具体实现：control plane（agent）和 execution plane（task_plan.md）的 protocol boundary 由 completion gate 显式化。

#### 7.2.3 在 cross-device 维度的实现

OthmanAdi/planning-with-files 把 task_plan.md / findings.md / progress.md 持久化到磁盘，这是 cross-device 协同的「**file-based working state on disk**」primitive：

> **File-based Working State 的本质**：会话状态（task progress）不是存在 agent 的 context window，而是存在磁盘上的 markdown 文件。Mobile / desktop / cloud 共用同一份 plan 文件。

**关键论证**：

- Context window 满了 → agent /clear → session-catchup.py 读磁盘上的 task_plan.md → 自动恢复上下文
- Mobile 切换到 cloud → cloud agent 读磁盘上的 task_plan.md → 接续 mobile 的工作进度
- Crash recovery → agent 重启 → 读磁盘上的 plan → 从断点继续

这是 cross-device 协同的「**会话状态协议**」的最小化实现 —— 不需要 append-only telemetry，也不需要 cache-first client，**只用磁盘上的 plan 文件就实现了会话状态交接**。

### 7.3 v3.0.0 autonomous + gated modes 的工程意义

OthmanAdi/planning-with-files v3.0.0（2026 早期发布）引入了两个关键模式：

**Autonomous mode**：
- 强模型下，去掉 per-tool-call plan re-injection（避免重复提示）
- 仅保留 turn-start injection（让模型随时知道 plan 状态）
- 减少 token 开销，提升性能

**Gated mode**：
- 在 autonomous 基础上加入 completion gate
- Stop hook 触发时检查 5 个条件（gated mode + in_progress phase + stop_hook_active false + block count < cap + ledger progressed since last block）
- 5 个条件全部满足才 block，否则 emit advisory reminder

**这两个模式的工程意义**：

1. **autonomous mode 解决了「plan 重复注入的 token 开销」** —— 这是 R661 提到的「context window vs plan state」trade-off 的实际解法
2. **gated mode 解决了「agent 自报完成不可信」** —— 这是 R663 vertical 解耦 deep dive 中提到的「execution plane verification」的最小化实现
3. **v3.2.0 session-catchup.py Windows fix** —— 解决了「Windows path sanitization + UTF-8 encoding」的实战问题，是 R664 cross-device 协同 deep dive 中提到的「实战可移植性」的最小化实证

### 7.4 与 awesome-harness-engineering 的对照

awesome-harness-engineering 当前 12 Primitives 中，**Planning & Task Decomposition** 是最接近 Planning Primitive 的：

> **awesome-harness-engineering 当前 Planning & Task Decomposition 描述**：长任务的拆解与状态跟踪

但这是「**静态描述**」—— 只关注「怎么拆任务」，不关注「plan 怎么跨 control plane / execution plane / device 共享」。

OthmanAdi/planning-with-files v3.2.0 提供的是「**动态协议**」—— plan 不只是「拆任务」，而是「跨 control plane 共享 + 跨 execution plane 验证 + 跨 device 持久化」的三合一协议。

R665 meta synthesis 的关键建议：**awesome-harness-engineering v2.0 应该把 Planning & Task Decomposition 升级为 Planning Primitive** —— 显式加入「vendor-neutral plan format」+「completion gate」+「file-based working state」三个属性。

### 7.5 OthmanAdi/planning-with-files 与 SeemSeam/CCB v8.0.15 的对比

R664 deep dive 把 SeemSeam/CCB v8.0.15 3,190 ⭐ 作为 cross-device + horizontal + partial vertical 三维度复合实证。OthmanAdi/planning-with-files 24,583 ⭐ 与 SeemSeam/CCB 的对比：

| 维度 | SeemSeam/CCB v8.0.15 | OthmanAdi/planning-with-files v3.2.0 |
|------|----------------------|--------------------------------------|
| **horizontal 范围** | 15 家 CLI providers | 60+ agents via SKILL.md standard |
| **vertical 解耦** | partial（pairing profile scope 5 种 scope） | ✅（hook + completion gate） |
| **cross-device 协同** | ✅ Flutter Mobile + Tailscale Serve | ✅（file-based working state on disk） |
| **协议基础** | 自研 CCB daemon | agentskills spec + SKILL.md |
| **应用场景** | 多设备协同 + multi-agent orchestration | 长任务跨 session 持久化 + multi-agent 共享 |
| **License** | NOASSERTION | MIT |

**结论**：

- **SeemSeam/CCB** 是 **cross-device 维度的额外加分项**（mobile + multi-agent + multi-vendor），但 License 风险（NOASSERTION）
- **OthmanAdi/planning-with-files** 是 **planning primitive 维度的最小化闭环**（60+ agents + hook + file-based state），但 Star 规模较小，跨设备场景不如 CCB 完整

两个项目是**互补的**：

- CCB 适合「**多设备协同 + multi-agent orchestration**」场景
- planning-with-files 适合「**长任务跨 session 持久化 + multi-agent 共享**」场景

---

## 八、awesome-harness-engineering v2.0 演进预测

### 8.1 当前框架（v1.x，2,749 ⭐ 2026-07-05）的局限

awesome-harness-engineering 当前 12 Primitives 框架有两个局限：

**局限 1：按组件组织，不按维度组织**

当前的 12 Primitives 是「按组件」（Agent Loop / Planning / Context Delivery / Tool Design / Skills & MCP / Permissions & Authorization / Memory & State / Task Runners & Orchestration / Verification & CI Integration / Observability & Tracing / Debugging & Developer Experience / Human-in-the-Loop），不是「按维度」（vertical / horizontal / cross-device）。

**问题**：当读者想找「跨 control plane 共享 Skill」的工具时，他要在 12 Primitives 中跨多个章节寻找（Skills & MCP + Task Runners & Orchestration + Memory & State ...），而不是直接跳到「horizontal 维度」章节。

**局限 2：缺少跨维度 primitive**

当前 12 Primitives 没有显式的「Cross-Device Coordination Primitive」，也没有显式的「Planning Primitive」（当前的 Planning & Task Decomposition 范围太窄）。

### 8.2 v2.0 演进预测：按维度组织 + 13 Primitives + 2 Cross-Dimension Primitives

R665 预测 v2.0 应该按以下结构组织：

```
awesome-harness-engineering v2.0
├── 📐 Foundations（保留）
├── 🧩 Vertical 解耦维度（控制平面 ↔ 执行平面）
│   ├── Vertical Agent Loop（控制平面的推理-行动-观察循环）
│   ├── Vertical Skill Spec（vendor-neutral Skill 协议，如 agentskills spec）
│   ├── Vertical MCP Protocol（control plane ↔ execution plane 的协议中立）
│   ├── Vertical Permissions & Authorization（基于 source tag 的权限分层）
│   ├── Vertical Verification Gate（completion gate / CI 门禁）
│   └── Vertical Execution Plane（Layer 1 官方 MCP + Layer 2 社区 MCP + Layer 3 自建 MCP）
├── 🔗 Horizontal 解耦维度（多 control plane ↔ 同一个 Skill + execution plane）
│   ├── Horizontal Skill Spec（同上，但强调跨 control plane）
│   ├── Horizontal Agent Loop（多 control plane 并行的 agent loop）
│   ├── Horizontal Memory & State（multi-control-plane 的状态共享）
│   ├── Horizontal Task Runners & Orchestration（多 control plane 协同）
│   └── Horizontal Authentication（双 control plane 的认证体系）
├── 📱 Cross-Device 协同维度（多端 harness 通过会话状态协议交接）
│   ├── Cross-Device Agent Loop（harness 在 mobile/desktop/cloud 间流动）
│   ├── Cross-Device Skill Spec（Skill 在多端共用）
│   ├── Cross-Device MCP Protocol（execution plane 跨端调用）
│   ├── Cross-Device Coordination Primitive（append-only telemetry + cache-first + source tag + rewind-safe replay 4 primitives）
│   └── Cross-Device Privacy & Consent（progressive consent + permission 集中）
├── 🔄 跨维度 Primitive（横切关注点）
│   ├── Planning Primitive（vendor-neutral plan + completion gate + file-based working state）
│   ├── Context Delivery & Compaction（跨维度共享）
│   ├── Observability & Tracing（跨维度共享）
│   └── Human-in-the-Loop（跨维度共享）
├── 🔍 Reference Implementations（保留）
├── 🛠️ Tools（保留）
└── 📚 Resources（保留）
```

### 8.3 v2.0 演进的关键变化

| v1.x | v2.0 | 变化原因 |
|------|------|---------|
| 12 Primitives 按组件组织 | 13 Primitives 按维度组织 | 三维度体系（R661）已经被 1st-party 实践验证 |
| 无 Cross-Device Coordination Primitive | 新增 Cross-Device Coordination Primitive | Cursor iOS + OpenAI Codex + SeemSeam/CCB 三家已收敛 4 primitives |
| Planning & Task Decomposition（范围窄） | 升级为 Planning Primitive（跨维度） | OthmanAdi/planning-with-files v3.2.0 + Anthropic: Harness Design for Long-Running Apps 双重验证 |
| 无 Session State Protocol Primitive | 显式化为跨维度 Primitive | R662 horizontal + R663 vertical + R664 cross-device 三个 deep dive 都触及 session 状态管理 |
| Skills & MCP 单独 | 拆分为 Vertical Skill Spec + Horizontal Skill Spec + Cross-Device Skill Spec | 不同维度下 Skill 的职责不同 |

### 8.4 v2.0 演进的实证基础

v2.0 演进不是 R665 的凭空预测，而是基于以下 1st-party / 准 1st-party 实证：

| v2.0 Primitive | 实证 |
|---------------|------|
| Vertical 解耦维度 | Apple Xcode 26.3 + Claude Agent SDK + getsentry/XcodeBuildMCP（R663 deep dive） |
| Horizontal 解耦维度 | agentskills spec 22k⭐ + xbtlin/ai-berkshire 9,881⭐ + alirezarezvani/claude-skills 20,349⭐（R662 deep dive） |
| Cross-Device 协同维度 | Cursor iOS + OpenAI Codex + SeemSeam/CCB v8.0.15 3,190⭐（R664 deep dive） |
| Planning Primitive | OthmanAdi/planning-with-files 24,583⭐ v3.2.0 + Anthropic: Harness Design for Long-Running Apps（本次 R665） |
| Cross-Device Coordination Primitive | Cursor iOS Remote Control 4 primitives + OpenAI Codex Secure Relay + SeemSeam/CCB Tailscale Serve（R664 deep dive） |

### 8.5 v2.0 演进对 awesome-harness-engineering 维护者的建议

如果 awesome-harness-engineering 维护者（ai-boost）采纳 R665 的预测，需要做 3 件事：

1. **新增 Cross-Device Coordination Primitive 章节**：收录 Cursor iOS Remote Control + OpenAI Codex Secure Relay + SeemSeam/CCB Tailscale Serve + OthmanAdi/planning-with-files file-based working state
2. **升级 Planning & Task Decomposition 为跨维度 Planning Primitive**：明确 vendor-neutral plan + completion gate + file-based working state 三属性
3. **重组 12 Primitives 为 3 个维度 + 4 个跨维度 primitive**：按维度组织而非按组件组织

但 R665 也承认：**v2.0 演进只是预测，不是确定**。awesome-harness-engineering 维护者可能选择其他演进路径（比如保持 12 Primitives 静态框架，但新增 Cross-Device Coordination Primitive 作为第 13 个）。

---

## 九、对 R666-R668 后续演进的判断

### 9.1 R666 监测重点

R665 进入「监测 + meta synthesis」阶段后，R666 应该继续监测 5 个关键信号：

1. **Anthropic Engineering 7 月 post breakthrough**：从 last engineering post 2026-06-06 起已 31+ 天，70+ day plateau 临界
2. **Claude Code v2.1.202 release**：累计 12 轮 R654-R665 NOT triggered，predicted next window 重启 7/6 19:00-01:00 CST
3. **awesome-harness-engineering v2.0 演进**：监测 awesome-harness-engineering 是否采纳 R665 的 v2.0 预测
4. **cluster signal 反弹**：监测 R655+ cluster signal 是否反弹到 4/7 strict-or-strong
5. **新 1st-party 范本**：监测 Anthropic / OpenAI / Cursor / Microsoft / Apple 是否有新文章

### 9.2 R666-R668 选题策略

**优先级 1**：如果 5 个关键信号中任一触发，执行对应主题的 deep dive

**优先级 2**：如果 5 个信号都 NOT triggered，进入 R666 选题决策：

- **选项 A**：multi-agent orchestration deep dive（基于 gastownhall/gastown 16,270 ⭐ + 0xnyk/council-of-high-intelligence 2,759 ⭐）—— 多 Agent 协作的编排拓扑与协议
- **选项 B**：Awesome Claude Code 综述（基于 hesreallyhim/awesome-claude-code 48,150 ⭐）—— Claude Code 生态的现状综述
- **选项 C**：Apple XcodeBuildMCP + Claude Agent SDK vertical 解耦延展 —— 在 R663 基础上深入
- **选项 D**：持续 meta synthesis 链（综述 R662-R664 + R665 之后，进一步综述跨维度 primitive 集合）

**优先级 3**：R667-R668 持续监测 + 周期 deep dive

### 9.3 R665 给开发者的 6 条实践建议

基于 R661-R664 + R665 meta synthesis，给正在搭建 harness 的开发者 6 条实践建议：

1. **不要假设你的 harness 是「自洽」的**：horizontal + vertical + cross-device 三个维度迟早会触及，提前按协议设计而不是「all-in-one」
2. **优先使用 vendor-neutral Skill spec**：agentskills spec 22k⭐ 已经被 60+ agents 支持，不要为每个 control plane 写一份 Skill
3. **执行平面优先 MCP**：MCP 是 control plane ↔ execution plane 的协议中立层，避免私有协议
4. **会话状态持久化到磁盘**：不要把 session state 放在 context window，参考 OthmanAdi/planning-with-files 的 file-based working state
5. **completion gate 比自报完成更可靠**：agent 自报完成不可信，参考 OthmanAdi/planning-with-files v3.0.0 gated mode
6. **cross-device 协同从一开始就按 4 primitives 设计**：append-only telemetry + cache-first + source tag + rewind-safe replay，不要等「需要跨设备」时再重构

---

## 十、参考来源（1st-party / 准 1st-party 引用）

### 10.1 R661 overview meta article 引用的 1st-party 来源（10 个）

- [Cursor iOS Mobile-Cloud Hybrid Harness (2026-07)](https://cursor.com/blog/ios-mobile-app)
- [Cursor Cloud Agent Mobile docs](https://cursor.com/docs/cloud-agent/mobile)
- [Apple Newsroom: Xcode 26.3 unlocks the power of agentic coding (2026-02)](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/)
- [Anthropic: Apple Xcode + Claude Agent SDK (2026-06)](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)
- [Claude Agent SDK Python (control plane SDK)](https://github.com/anthropics/claude-agent-sdk-python)
- [Anthropic: How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
- [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [agentskills/agentskills spec (vendor-neutral Skill)](https://github.com/agentskills/agentskills)
- [Model Context Protocol (MCP) official site](https://modelcontextprotocol.io)

### 10.2 R662 horizontal 解耦 deep dive 引用的 1st-party 来源（11 个）

- [agentskills/agentskills spec (vendor-neutral Skill)](https://github.com/agentskills/agentskills)
- [Claude Code official docs](https://code.claude.com/docs/en/overview)
- [Codex CLI official docs](https://developers.openai.com/codex)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [OpenCode](https://github.com/anomalyco/opencode)
- [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire)
- [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- [Skills vs Agents vs Personas 三层抽象 (Anthropic)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Steering 7 methods](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)
- [Anthropic: Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)

### 10.3 R663 vertical 解耦 deep dive 引用的 1st-party 来源（11 个）

- [Apple Newsroom: Xcode 26.3 unlocks the power of agentic coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/)
- [Anthropic: Apple Xcode + Claude Agent SDK (2026-06)](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)
- [Claude Agent SDK Python](https://github.com/anthropics/claude-agent-sdk-python)
- [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [OpenAI: Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Anthropic: Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Anthropic: Beyond Permission Prompts](https://www.anthropic.com/engineering/beyond-permission-prompts)
- [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)

### 10.4 R664 cross-device 协同 deep dive 引用的 1st-party 来源（11 个）

- [Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile)
- [Cursor for iOS blog (2026-07)](https://cursor.com/blog/ios-mobile-app)
- [OpenAI: Codex 跨设备协作 (agents-of-change-mobile-collaboration)](https://openai.com/index/agents-of-change-mobile-collaboration/)
- [SeemSeam/claude_codex_bridge v8.0.15](https://github.com/SeemSeam/claude_codex_bridge)
- [Tailscale Serve](https://tailscale.com/kb/1223/serve/)
- [Apple Developer: Live Activities](https://developer.apple.com/documentation/activitykit)
- [Anthropic: How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude)
- [Anthropic: Claude Agent SDK](https://docs.claude.com/en/api/agent-sdk/overview)
- [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)

### 10.5 R665 meta synthesis 新增的 1st-party / 准 1st-party 来源（5 个）

- [OthmanAdi/planning-with-files v3.2.0 (24,583 ⭐)](https://github.com/OthmanAdi/planning-with-files)
- [Anthropic: Harness Design for Long-Running Apps (2026-03)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [Anthropic: Effective Harnesses for Long-Running Agents (2025-11)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Meta: REA: Ranking Engineer Agent (2026-03)](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/)
- [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/)

### 10.6 awesome-harness-engineering 框架演化

- [ai-boost/awesome-harness-engineering v1.x (2,749 ⭐ 2026-07-05)](https://github.com/ai-boost/awesome-harness-engineering)
- [ai-boost/awesome-harness-engineering 演进预测（R665 v2.0）](#八awesome-harness-engineering-v20-演进预测)

---

## 十一、本仓库关联阅读

- [R661 overview meta article](./awesome-harness-engineering-three-dimensions-protocolization-2026.md) —— harness 协议化三维度体系的起源
- [R662 horizontal 解耦 deep dive](./harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) —— Skill 跨 control plane 的协议中立
- [R663 vertical 解耦 deep dive](./harness-vertical-decoupling-control-plane-execution-plane-protocol-2026.md) —— control plane ↔ execution plane 的协议中立
- [R664 cross-device 协同 deep dive](./harness-cross-device-coordination-mobile-cloud-session-state-protocol-2026.md) —— 多端 harness 通过会话状态协议交接
- [R665 PROJECT: OthmanAdi/planning-with-files 24,583 ⭐ NEW PROJECT](../projects/othmanadi-planning-with-files-manus-style-persistent-planning-24583-stars-2026.md) —— 三维度全开最小化闭环实证

---

## 十二、给 R666 的开放问题

1. **awesome-harness-engineering v2.0 是否采纳 R665 的 v2.0 演进预测**？监测 ai-boost/awesome-harness-engineering 是否有新结构发布
2. **Planning Primitive 是否被官方收录**？监测 Anthropic / OpenAI 是否在 7 月发布新的 planning primitive 1st-party 范本
3. **CCB v8.0.15 与 OthmanAdi/planning-with-files 的关系**？监测 SeemSeam/CCB 是否引入 planning-with-files 作为底层 plan 实现
4. **awesome-harness-engineering 反模式教训**？R665 提到 5 个反模式，awesome-harness-engineering 是否会收录反模式章节？

---

**R665 meta synthesis 完成**：完成 R661 overview + R662-R664 三个 deep dive 的链路综述，提出 Planning Primitive 是被忽略的关键 primitive，给出 awesome-harness-engineering v2.0 演进预测。下一轮（R666）继续监测 5 个关键信号，等待 1st-party 触发或进入 R666 选题决策。