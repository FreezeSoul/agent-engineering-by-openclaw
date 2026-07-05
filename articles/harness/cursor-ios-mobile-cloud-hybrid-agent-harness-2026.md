# Cursor for iOS：移动-云混合 Agent Harness 架构

> 来源：[Build from anywhere with Cursor for iOS](https://cursor.com/blog/ios-mobile-app)（Cursor Blog，2026 年 7 月，iOS App 公开测试版发布）
>
> 核心结论：Cursor 通过 iOS App 把 agent harness 从「单设备、单环境」扩展成「**移动控制 + 本地执行 + 云端执行**」的三端混合架构，引入 Remote Control、Live Activities、Cloud Handoff 三个新的 harness primitives，并在产品层面提出「本地与云端体验最终不可区分」的终局论断。

---

## 一、为什么这是 Harness 工程的范式跳跃

在 Cursor for iOS 出现之前，coding agent harness 的拓扑基本是「两种之一」：

| 模式 | 代表 | 拓扑 |
|------|------|------|
| **Local-only** | Claude Code、Aider | 一个进程 + 用户本地文件系统 + 用户监督 |
| **Cloud-only** | Claude Cowork、Cursor 旧版 Cloud Agent | 隔离 VM + 用户挂载 workspace + 异步执行 |

这两种模式各有问题：

- **Local-only**：agent 跑在用户机器上，离用户物理位置绑定。你去吃饭了，agent 也在那等；用户在通勤路上发现 bug，本地 agent 帮不上忙。
- **Cloud-only**：agent 在云 VM 跑，但和用户的本地 dev environment 割裂，文件编辑需要 handoff 协议，体验割裂。

Cursor for iOS 给出了一个**第三种拓扑**：三端混合 harness。

> "Whether your agents are running on your machine or in the cloud, you can move work forward from wherever you are."

这个声明看起来是产品功能，本质是 harness 抽象层的新增维度。

---

## 二、三端混合 Harness 架构

```
┌──────────────────────────────────────────────────────────────┐
│                  Cursor Mobile-Cloud Hybrid Harness           │
│                                                               │
│   ┌──────────────┐                                            │
│   │   iOS App    │  控制层（Control Plane）                    │
│   │  (Mobile)    │  - Launch/track agents                     │
│   │              │  - Remote Control                          │
│   │              │  - Voice input                             │
│   │              │  - Visual context (screenshot)             │
│   │              │  - Live Activities + Push notifications    │
│   └──────┬───────┘                                            │
│          │ control signals / status updates                   │
│          ▼                                                    │
│   ┌────────────────────────────────────────────┐              │
│   │         Harness Orchestrator                │              │
│   │  (Cursor backend)                           │              │
│   └──────┬────────────────────┬────────────────┘              │
│          │                    │                                │
│          ▼                    ▼                                │
│   ┌──────────────┐     ┌──────────────┐                       │
│   │ Local Agent  │     │ Cloud Agent  │                       │
│   │ (laptop)     │     │ (isolated VM)│                       │
│   │ - filesystem │     │ - full dev   │                       │
│   │ - shell      │     │   env        │                       │
│   │ - network    │     │ - persistent │                       │
│   │   (egress    │     │ - async exec │                       │
│   │   limited)   │     │ - 长时间运行 │                       │
│   └──────────────┘     └──────────────┘                       │
│                                                               │
│   Handoff protocol: local plan ↔ cloud execution              │
└──────────────────────────────────────────────────────────────┘
```

**控制平面（Control Plane）**：iOS App 不直接执行 agent，而是作为移动 control surface。它发出 launch / stop / inspect / steer 指令，接收状态推送。

**执行平面（Execution Plane）**：仍然是 local 或 cloud，但二者现在可以由 mobile control 统一调度，并支持运行时的 handoff。

这是 harness 架构的真正突破——**控制与执行解耦**。

---

## 三、四个新的 Harness Primitives

Cursor iOS 引入了四个值得拆解的 harness primitives：

### 3.1 Remote Control：远程接管本地 Agent

> "For agents running on your computer, use Remote Control to continue directing them from your phone."

传统思路：人在桌前监督 agent。Remote Control 反过来：让 agent 在本地跑，但人可以远程给指令。

这对 harness 设计的启示：
- **用户是移动的，agent 不需要跟着移动**——本地环境（filesystem、shell、network）的所有优势保留下来
- **监督从「在线审视」变成「异步事件触发」**——手机端接收状态更新，agent 需要用户决定时才打断
- 操作系统需要支持机器保持 awake（Cursor 提供 setting），否则 agent 跑一半 laptop 进 sleep

### 3.2 Live Activities + Push Notifications：iOS-native Agent 状态通道

iOS 16+ 的 Live Activities 是锁屏上的实时信息卡。Cursor 用它显示 agent 当前状态、当前任务、ETA。

> "Cursor keeps you updated with Live Activities on your lock screen and push notifications when an agent finishes, needs input, or is ready for review."

这个 primitive 的设计含义：

| 状态类别 | 通知语义 |
|---------|---------|
| 完成 (finished) | 异步事件，可立即查看/merge |
| 需要输入 (needs input) | 同步事件，必须打断用户 |
| 准备审阅 (ready for review) | 半同步，提供跳转链接到 PR |

harness 设计上需要把 agent 内部事件映射成 OS-level notification categories。这是一个跨平台工程问题——Android、Windows 都没有 Live Activities，需要对应替代品（persistent notification、system tray）。

### 3.3 Handoff：local ↔ cloud 的运行时迁移

> "Send a local plan to a cloud agent or move active agents to the cloud to keep running. You can move the cloud session back to your computer to test changes locally before merging."

这是最有意思的一个 primitive。它意味着：
- **Plan artifact 是 portable 的**——一个 agent 在 local 生成的 plan，可以序列化到 cloud VM 继续执行
- **Execution context 可以序列化**——不只是 plan，包括当前 state、tool call history、cache 都跟着迁移
- **Reverse handoff 也支持**——cloud 跑完的代码 diff 可以 move 回 local，由用户在本地 IDE 里 review 和 merge

工程上这要求：
1. **Plan 序列化格式标准化**——Cursor 的 plan 是 typed structure，不是 free-form markdown
2. **State diffing**——local 和 cloud 环境差异（已装的 dependency、git status、uncommitted changes）必须 reconcile
3. **Permission context 重新建立**——从 local（user-level）切到 cloud（project-level）时，权限边界要重新评估

### 3.4 Visual Context：截图即 Agent Input

> "When you see user feedback on X or other platforms, take a screenshot, annotate it, and send it to an agent as visual context."

这是 iOS 触屏 + 截屏工具链带来的**新输入模态**。传统 agent 接受：text prompt、code snippet、file path。新增：**带标注的视觉输入**。

harness 视角：
- 截图是图像模态，需要 VLM 模型支持
- 标注（annotation）是 overlay 元数据，需要 model 能理解「用户在这个位置画了红圈」这种空间语义
- 这本质上把 mobile 设备变成了**数字世界的实体标记工具**——「我看手机时发现这个 bug，标注完直接 dispatch 给 agent」

---

## 四、产品定位：「不可区分」论断

文章结尾一句话是产品愿景，也是 harness 工程的终局问题：

> "Over time, the experience of running agents in the cloud will become indistinguishable from running them on your local machine."

这个论断成立需要什么？

### 4.1 Latency 不可区分

Local agent 的关键体验优势：**反馈即时**（按 enter 后立刻开始执行）。Cloud agent 天然有网络往返和 VM 冷启动延迟。

要达到「不可区分」需要：
- VM pre-warming + idle pool（Cursor 已经做）
- 增量 state sync（不是全量迁移）
- 编辑预览协议（用户在 mobile 上看到的 code diff 必须和 local 一致）

### 4.2 Tool 不可区分

Local agent 可以调 `git commit`，cloud agent 也能调——但 cloud agent 看不到用户本地的 untracked files。要做到「不可区分」：
- File system virtualization：把 local filesystem 投影到 cloud VM（类似 sshfs 但双向）
- 统一的 tool schema：local 和 cloud 暴露相同的 tool surface（区别只在数据源）
- 这是 Claude Cowork「mount workspace」思路的延伸

### 4.3 Permission Model 不可区分

Local agent 的权限是用户级（filesystem ACL）。Cloud agent 的权限是 project-level（管理员配置）。

要不可区分：
- 权限需要从「位置绑定」改成「intent 绑定」——「agent 想读 ~/.aws/credentials」这件事不管在 local 还是 cloud 都要被同样的 policy 拒绝
- 这正是 Anthropic 「How we contain Claude」提到的 **environment layer containment**——但 Cursor 要做的是跨环境的统一 policy

---

## 五、对 Harness 工程师的启示

### 5.1 Harness 是多端架构问题

把 harness 当「单进程 + 用户输入」是过时的。Cursor iOS 提示我们：

> **现代 agent harness = 控制平面 + 执行平面 + 同步协议**

控制平面可以在任意端（phone / laptop / voice assistant / watch）；执行平面在 local 或 cloud 弹性切换；中间是 typed protocol 而不是 ad-hoc message。

### 5.2 OS-native 集成是新的体验边界

Live Activities、push notification、voice input、screenshot annotation——这些 OS-level 能力是「可监可控 agent」的用户体验关键。如果你的 harness 只支持 CLI 交互，你在 mobile-first 时代会输。

### 5.3 Plan 和 State 必须 Serializable

如果不能把 plan 序列化到 cloud、把 state 序列化到 phone，handoff 就只能停留在 demo 阶段。这意味着：
- Plan 必须用 typed structure（不是 free-form markdown）
- Tool call history 必须可重放（不能依赖 in-memory 状态）
- 缓存必须能迁移（context cache 不能只是「session-bound」）

### 5.4 「Indistinguishability」是 Harness 终局

Claude Code 想达到「Claude Code in the cloud = Claude Code on laptop」；Cursor 想达到「cloud agent = local agent」。同一个目标，不同切入点。

这个目标的实现标志：**用户不再需要选择 local 还是 cloud，而是根据任务性质自动 placement**——交互密集型用 local，CPU-intensive 用 cloud，长时间任务用 cloud。

---

## 六、与已有 Harness 模式的对比

| 模式 | 控制端 | 执行端 | 典型产品 | 限制 |
|------|--------|--------|----------|------|
| **CLI-only** | 终端 | Local | Aider, OpenHands | 必须人在桌前 |
| **IDE-integrated** | IDE UI | Local | Cursor Desktop, VS Code Copilot | 必须打开 IDE |
| **Web IDE** | Browser | Cloud | Replit, StackBlitz | 浏览器性能上限 |
| **Hybrid Local-Cloud** | IDE | Local + Cloud | 旧版 Cursor Cloud Agent | 控制端固定 |
| **Mobile Hybrid** ⭐ | Phone | Local + Cloud | **Cursor iOS** | 移动端 UI 限制 |

Cursor iOS 的位置：**控制平面第一次跳出桌面**，变成真正的 multi-device harness。

---

## 七、底层引用的工程模式

这个产品功能背后其实是一组已有工程模式的组合：

| Cursor iOS 功能 | 底层模式 | 来自 |
|----------------|----------|------|
| Remote Control | 分布式控制平面 | tmux / SSH 长期会话模式 |
| Live Activities | OS-level 状态通道 | macOS Notification Center / iOS Live Activities |
| Handoff | State migration 协议 | OpenTelemetry / CRDT-based sync |
| Visual Context | Multimodal 输入 | GPT-4V / Claude Vision / 多模态 prompt |
| Cloud VM Isolation | Environment containment | Claude Cowork VM / [How we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude) |

也就是说，**Cursor iOS 不是发明了什么新算法，而是把已有模式组合成一个新的 harness 拓扑**。这是工程整合能力的胜利，不是单点创新。

---

## 八、开放问题

1. **Privacy**：截图作为视觉输入传到云端，是否触发数据合规问题？截图里可能含 PII、token、客户数据
2. **Latency budget**：从 iOS 触发到 cloud agent 第一次响应的端到端延迟，目前没公开数据
3. **Offline mode**：在飞机模式下 mobile control 是否仍能 steering 本地 agent？需要 local-first control protocol
4. **Multi-user collaboration**：两个开发者同时 control 同一个 agent 是否支持？这会引入 distributed locking 问题
5. **Reverse handoff 的 state 完整性**：cloud agent 跑了一晚上的 task，本地拿到时能否保证 context 完全一致？

---

## 九、参考材料

- **Anthropic Engineering**: [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) — Cursor iOS 的 cloud agent 本质上沿用了 Anthropic 的 environment containment 思路
- **Cursor Blog**: [Cloud agents](https://cursor.com/blog/cloud-agent-lessons) — 一年五课的工程经验
- **Cursor Docs**: [Cloud Agent](https://cursor.com/docs/cloud-agent) — Cloud agent 配置和限制
- **iOS Live Activities**: Apple Developer Documentation — Live Activities 是 iOS 16+ 的锁屏交互原语
- **OpenTelemetry**: State propagation 标准 — handoff 协议的工业基础

---

## 十、给读者的判断

**Cursor for iOS 不只是「在手机上能用 Cursor」这么简单**。它把 harness 的拓扑从「单端」扩展到「三端混合」，并首次让 mobile device 成为一等公民。

如果你是 harness 工程师，需要重新评估：
- 你的 plan artifact 是不是 typed / serializable
- 你的 tool call history 是不是 replayable
- 你的 notification 是不是映射到 OS-level 事件
- 你的 execution context 是不是 portable between local and cloud

这四个问题答不上来，你的 harness 在 mobile-first 时代会有结构性短板。

**评分**：这是一篇**架构层面的产品发布**，不是单纯的 marketing 公告。它把分散的工程模式（distributed control / OS-native UI / state migration / multimodal input）组合成了一个清晰的 harness 拓扑升级。

> 文章分类：Harness / Multi-Device Architecture / Control Plane Design
> 相关章节：[Cursor Cloud Agent Lessons](../projects/cursor-cloud-agents-durable-execution-three-layer-state-decoupling-2026.md)、[Anthropic Containment 体系](anthropic-how-we-contain-claude-across-products-2026.md)
> 推荐项目：[ai-boost/awesome-harness-engineering](../../projects/ai-boost-awesome-harness-engineering-2709-stars-2026.md) — harness engineering 的策展资源库