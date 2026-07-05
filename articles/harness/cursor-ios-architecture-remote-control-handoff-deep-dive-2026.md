# Cursor iOS 远程控制协议深度拆解：从产品功能到跨设备 Agent Harness

> 来源：[Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile) + [Cursor for iOS blog](https://cursor.com/blog/ios-mobile-app)（Cursor 1st-party，2026-06/07）
>
> 本文是 [Cursor for iOS：移动-云混合 Agent Harness 架构](cursor-ios-mobile-cloud-hybrid-agent-harness-2026.md) 的工程深度篇。
> 前一篇从产品视角回答了「这是不是一个新拓扑」，本文从协议视角回答「**这套拓扑具体怎么实现、边界在哪、为什么这样设计**」。

---

## 一、核心命题

R657 文章留了 5 个开放问题。本文只回答其中 3 个——也是文档里第一次明确写出来的：

1. **Remote Control 协议的精确语义**：agent loop 与 tool execution 如何在两台机器上分别运行？
2. **跨设备 session 是怎么 sync 的**：手机和电脑看到的是不是同一份状态？用哪个标识区分？
3. **Permission 模型在跨设备场景下的统一**：手机上的指令能在电脑上执行吗？信任边界在哪？

读完本文你会得到一个明确的判断：**Cursor iOS 不是给本地 agent 加一个遥控器，而是把 agent harness 拆成了「控制平面（cloud loop）+ 执行平面（local tools）」两层架构，并通过 source 标签和 Privacy Mode 做隔离**。

---

## 二、Remote Control 协议的精确语义

### 2.1 表面看：把 agent 从电脑搬到手机上

如果你只看 blog 描述，Remote Control 听起来像「远程控制你的电脑上的 agent」：

> "Remote Control lets you take an agent you're running on your computer and keep directing it from your phone."

但当你打开 docs，会看到完全不一样的语义：

> "**The agent loop moves to the cloud while its tools keep running on your machine**, so it reads your files, runs your tests, and uses your local setup the same way it did on your desktop."

这就是关键的工程区别——**Remote Control 不是一个屏幕共享协议，也不是 SSH 隧道**。它的实际语义是：

| 组件 | 运行时位置 | 数据流 |
|------|-----------|--------|
| **Agent loop**（推理、规划、决策） | Cursor cloud | 从本地拉模型需要的 context |
| **Tool calls**（terminal、file edit、test、git） | 用户本地机器 | 在本地执行，结果回到 cloud loop |

也就是说，你的电脑不再跑 Claude 的推理循环了——它退化成「**纯执行器**」。真正的「思考」在 Cursor 的 cloud 里完成，但所有「动手」（改文件、跑测试、读 git）都在你的本地机器发生。

### 2.2 为什么必须这样设计

文档给了一个非常清晰的理由：

> "**Your repository, secrets, credentials, and build caches stay on your machine. Only tool results and the context the model needs cross to Cursor.**"

这个设计是**数据本地化（data locality）**的极致版本：

- 你电脑上的代码、密钥、credentials、build cache **完全不出本机**
- 只有「模型下一步推理需要的 context」和「工具执行结果」才会跨网络传输
- Cursor cloud 永远拿不到你的原始文件，只能拿到 LLM 上下文窗口里需要的片段

这跟 Anthropic 一直强调的「harness 的每个组件都基于『模型做不到』的假设」是一脉相承的——Remote Control 这个 harness primitive 的存在前提是：**模型还做不到在本地推理**（因为本地算力不够 / 没合适的 GPU），但模型也不需要直接访问你的整个文件系统。

### 2.3 Remote Control 跟 My Machines 不是一个东西

文档反复强调这两个的区别，但很容易混淆：

- **My Machines**：用户主动把自己的机器注册成一个 cloud agent 的 worker，agent loop 完全在 cloud 跑，tools 跑在用户机器
- **Remote Control**：用户本来在本地 desktop session 工作，主动用 `/remote-control` 命令把 session **搬**到 cloud loop（用户机器变成纯执行器）

关键差异：

| 维度 | My Machines | Remote Control |
|------|------------|---------------|
| 启动位置 | 直接在 mobile/web 选 worker | 先在 desktop 启动，再 `/remote-control` |
| 退出方式 | 任务结束 worker 释放 | 用户主动停 Remote Control |
| 适用场景 | 长时间任务（PR review、CI 修复） | 用户中途离开桌面（通勤、外出） |
| Agent loop 位置 | 一直 cloud | 从 local 迁到 cloud |

这两条路径最终都把 tools 留在用户机器上，但 Remote Control 多了一个**「从 local 到 cloud 的迁移」步骤**，这也是 source 标签的由来。

---

## 三、跨设备 Session Sync：source: iosApp 标签

### 3.1 一个被低估的工程细节

文档里有一句看起来不起眼的话：

> "Agents started on mobile are tagged with `source: iosApp` so you can tell where they came from."

这是整个跨设备架构里**最容易被忽视、但最重要的设计**。

为什么需要 source 标签？因为同一个用户的同一个 repo，可能存在多个并发 session：
- 桌面上一个 agent 在重构代码
- 手机上同一个 agent 继续 steer
- Slack 里又触发了一个 cloud agent

这三者最终会聚合到同一个 inbox，但它们的来源不同：
- 桌面 agent：source = `desktop`
- 手机 agent：source = `iosApp`
- Slack agent：source = `slack`

source 标签让你在 inbox 里**一眼区分这个 session 是从哪个 surface 触发的**。

### 3.2 source 标签隐含的工程约束

source 标签的存在，间接证明 Cursor 内部用了类似事件溯源（event sourcing）的 session 模型：

```
Session = {
  session_id: <uuid>,
  source: 'desktop' | 'iosApp' | 'slack' | 'cli' | 'web',
  worker: { type: 'cloud-vm' | 'self-hosted' | 'my-machine' },
  state: ConversationState,
  timeline: [Event{ source, payload, ts }]
}
```

如果 Cursor 用的是简单的"当前最新状态"模型（CRDT 之类），根本不需要 source 标签——因为状态最终一致即可。**只有当 session 历史、回放、审计成为一等公民时，source 才有意义**。

这也是为什么 cursor 自动做了一件事：把所有跨 surface 的 session 同步到同一个 backend：

> "The app runs on iPhone... on the same backend as cursor.com/agents and the desktop Agents Window, so the agents you start on mobile show up everywhere you work."

换句话说：**mobile 不是另一个客户端，它是同一个 backend 的另一个 surface**。

### 3.3 跨设备迁移的隐式协议

docs 里有一个细节经常被忽视：

> "From a local IDE session, push your work to a cloud agent first with Move to Cloud, or keep it on your computer and direct it from your phone with Remote Control."

这意味着 Cursor 实际上提供**两条**迁移路径：
1. **Move to Cloud**（local → cloud VM）：完整的迁移，session 状态搬到新 VM，tools 也搬过去
2. **Remote Control**（local → cloud loop + local tools）：状态搬到 cloud，但 tools 不搬

这两条路径的差异本质是：**你在迁移的是「session」还是「execution」**。Move to Cloud 迁的是 execution（VM 是 execution 容器），Remote Control 迁的是 session（cloud loop 是 control 容器，execution 仍在本地）。

这是非常工程化的设计——它意味着 Cursor 内部必须有一个**「execution 与 session 解耦」的抽象层**，否则不可能同时支持两种迁移方式。

---

## 四、Cache-first 架构：移动端为什么能秒开

### 4.1 表面看：用户体验优化

docs 里有一句话：

> "The app is cache-first. It reads from local data so the inbox and conversations open fast, then syncs once your connection returns."

听起来像普通的客户端缓存优化。但当你把这条和前面的 source 标签、跨设备 sync 放在一起，会发现它实际上是**离线优先（offline-first）架构的标准模式**：

```
┌─────────────────────────────────────────────────┐
│           Cursor iOS Client                     │
│  ┌──────────────────────────────────────────┐  │
│  │ Local Cache (SQLite/CoreData)            │  │
│  │  - sessions[]                            │  │
│  │  - messages[]                            │  │
│  │  - source: iosApp | desktop | slack      │  │
│  └──────────────────────────────────────────┘  │
│           │ sync when online                    │
│           ▼                                     │
│  ┌──────────────────────────────────────────┐  │
│  │ Conflict Resolution Layer                │  │
│  │  - LWW (last-write-wins) per session?    │  │
│  │  - Operational Transform?                │  │
│  │  - Append-only with rewind?             │  │
│  └──────────────────────────────────────────┘  │
│           │                                     │
│           ▼                                     │
│  Cursor Cloud Agent Backend                     │
└─────────────────────────────────────────────────┘
```

但 docs 还透露了一个关键细节：

> "On the conversation side, we separated the storage and streaming layer from the core agent workflow. We built an efficient append-only storage mechanism that streams conversation updates out to web and desktop clients."

这是 cloud 端的架构：**append-only storage + streaming layer + conversation state 解耦**。

为什么必须 append-only？因为 agent loop 里 streaming 输出可能中途失败、retry、partial output——如果 storage 是 mutable 的，retry 会把之前 partial 的内容覆盖掉。**append-only + rewind**让 retry 可以：

1. 检测到 partial output
2. 从上一个 checkpoint 重做
3. client 检测到 duplicate 后，rewind stream 显示新的数据

这套设计跟 R657 文章里讲 Live Activities 的设计是同一个思路：**「append-only + rewind」是分布式状态管理的最稳健模式**。

### 4.2 跨设备 cache invalidation

cache-first 架构的真正难点是**缓存失效**。Cursor 的解法是「缓存本地数据 + 联网同步」，但 sync 的频率和粒度决定了用户体验。

文档没说具体策略，但可以推断：
- inbox 列表：高频 sync（push notification 触发）
- session 内容：低频 sync（用户主动打开时）
- agent loop 状态：实时 sync（Live Activities 直接推送）

这个分层 sync 跟 R657 文章里讲的「8 个 Live Activities 同时追踪」的设计是匹配的——**Live Activities 承担实时状态，cache 承担历史状态，二者用不同协议**。

---

## 五、Permission 模型：跨设备场景下的边界

### 5.1 默认信任模型

docs 在 Remote Control 章节里有一句话非常重要：

> "Only you can control your agents. Cursor ties each session to your account and your machine, and rejects requests for agents you don't own."

这是一个**双因素绑定**：account + machine。换句话说，光有账号密码是不够的，还得在那台物理机器上启用过 Remote Control。

这跟 Anthropic Containment 体系是同一思路：**Trust boundary = user authorization × device enrollment**。Cursor 这边的实现是「账号 × 机器注册」。

### 5.2 Privacy Mode：隐式的兜底

docs 还有一段：

> "Cursor for iOS relies on Cloud Agents, which need cloud data storage to run. If you're on Privacy Mode (Legacy), switch to Privacy Mode before using the app."

也就是说：**用户必须 opt-in 到「Privacy Mode」（即允许 cloud data storage），才能用 iOS app**。Legacy Privacy Mode 是默认的本地化模式，但 cloud agent 需要 cloud storage，所以 iOS 强制要求用户切换。

这里有个关键的设计决策：**iOS 不是一个可选 surface，而是 cloud agent harness 的必备入口**。换句话说，Cursor 已经在产品层面把 Privacy Mode 默认往 cloud 倾斜——你想用 mobile control，就必须允许 cloud 存储你的代码上下文。

这是 Anthropic Containment 体系的「**progressive disclosure + progressive consent**」思路：用户不需要一开始就理解所有权限，但每一步都要明确 opt-in。

### 5.3 Team 场景的额外限制

docs 里还有一个团队场景的细节：

> "On Teams and Enterprise plans, an admin must enable Remote Control from Cursor Dashboard → Cloud Agents → Self-Hosted before members can use it."

也就是说：
- 个人 Pro 用户：自己决定
- 团队用户：管理员统一开关
- Enterprise 用户：必须 admin enable

这是 B2B 安全模型的典型做法：**个人能力 ≠ 团队能力**。一个团队成员能不能用 Remote Control，取决于 admin policy，不取决于他自己的账号权限。

### 5.4 跨设备的 Permission 继承

那手机上的指令会不会绕过电脑上的 permission 检查？docs 没明说，但从两个细节可以推断：

1. "Remote Control isn't available when your privacy settings disable cloud data storage" — Privacy Mode 是顶层开关
2. "agent loop lives in Cursor's cloud" — 所有 permission 决策都在 cloud 端做

也就是说：**permission 决策不在电脑本地做，而在 cloud agent loop 里做**。这就避免了「手机绕过电脑 permission 检查」的可能性——因为根本没有「电脑本地 permission 检查」这层。

这是非常优雅的设计：把 permission 从「本地端决策」变成「cloud 端集中决策」，自然就解决了跨设备的一致性问题。

---

## 六、回到 R657 文章的 5 个开放问题

R657 文章最后留了 5 个问题，现在可以明确回答其中 3 个：

| 问题 | 答案 |
|------|------|
| **Privacy** | account + machine 双因素绑定，Privacy Mode 必须 opt-in，permission 决策统一在 cloud 端 |
| **Multi-user** | Team/Enterprise 用户由 admin 控制 Remote Control，个人用户自己决定 |
| **Reverse handoff state 完整性** | cloud 端用 append-only storage + rewind 处理 retry，session 状态在 cloud 而非 local |

剩下 2 个（latency 公开数据、offline mode）docs 还没明确：

- **Latency**：docs 说 "Live Activities" 和 push notification 是状态通道，但没说 mobile → local tool call 的端到端延迟
- **Offline mode**：cache-first 解决了 inbox 读取，但 agent loop 启动、tool execution 完全依赖网络，没有真正的 offline agent 能力

这两个问题可能就是 Cursor 后续 iOS 迭代的方向。

---

## 七、5 个工程启示

### 启示 1：Agent harness 的「控制平面 / 执行平面」解耦是 2026 主流

R657 文章讲了 Cursor iOS 引入了「控制 vs 执行解耦」的拓扑。本文进一步证明这是 2026 年 harness 工程的**主流范式**：

- Remote Control = 显式的 control/execution 解耦
- Move to Cloud = execution 容器迁移（loop 跟着 execution）
- Apple Xcode + Claude Agent SDK = control 容器固定在 IDE（execution 在 IDE 内）

三者殊途同归：**2026 年的 harness 必须在 control plane 和 execution plane 之间划清楚边界**。

### 启示 2：source 标签是 session-level telemetry 的最小可行实现

很多团队想实现「跨 surface session 同步」但不知道从哪下手。Cursor 的 `source: iosApp` 标签是最小可行实现：

- 不需要改 session 核心模型
- 只需要在 session 创建时打一个 enum
- 在 inbox UI 上按 source 过滤即可

但这只是 MVP。完整的 telemetry 还应该包括：**device class、network condition、latency、failure mode**——Cursor 后续大概率会扩展这个 metadata。

### 启示 3：cache-first 不是用户体验优化，是分布式状态正确性的兜底

很多人把 cache-first 当成「让 app 打开更快」。但 Cursor 的设计证明它的真正价值是：**让 retry / partial output / network failure 这些分布式状态问题都变得可恢复**。

如果你正在设计一个 multi-surface agent 产品，cache-first 不应该是「等 app 做好了再加」，而应该是从一开始就在 data layer 里设计好。

### 启示 4：跨设备 Permission 决策应该在「权威端」做，不应该在「执行端」做

Cursor 把 permission 决策放在 cloud loop（control plane），不在 local execution。这样：
- 手机指令不能绕过电脑 permission
- permission 策略更新一次，全 surface 生效
- audit log 在一个地方

这是 enterprise-grade harness 的核心模式。**Permission 不应该跟着 execution 走，应该跟着 control 走**。

### 启示 5：Privacy Mode 的渐进同意是 B2B 落地的关键

Cursor 把 Privacy Mode 设计成「必须 opt-in 才能用 iOS」——这是 progressive consent。

B2B 产品落地 agent harness 时，最难的不是技术，是「用户敢不敢相信你」。Cursor 的解法是：**不强迫、不默认、不隐藏，每一步都明示同意**。

这跟 Apple 自己的「App Tracking Transparency」是同一个模式：**把控制权明确交给用户，代价是用户体验多一步，但换来的是 trust**。

---

## 八、参考材料

### 8.1 1st-party 来源（必读）

- [Cursor Cloud Agent — Mobile docs](https://cursor.com/docs/cloud-agent/mobile)（本文核心来源，2026-07）
- [Cursor for iOS blog](https://cursor.com/blog/ios-mobile-app)（R657 文章源，2026-06-29）
- [What we've learned building cloud agents](https://cursor.com/blog/cloud-agent-lessons)（Cursor cloud agent 一年经验总结，2026-06-02）
- [Cursor Cloud Agent capabilities](https://cursor.com/docs/cloud-agent/capabilities)（cloud agent 能力文档）
- [Cursor Cloud Agent setup](https://cursor.com/docs/cloud-agent/setup)（cloud agent 环境配置文档）

### 8.2 本仓库关联阅读

- [Cursor for iOS：移动-云混合 Agent Harness 架构](cursor-ios-mobile-cloud-hybrid-agent-harness-2026.md) — 本文的高层产品篇
- [Anthropic How we contain Claude across products](anthropic-how-we-contain-claude-across-products-2026.md) — Trust boundary 体系
- [Anthropic Scaling Managed Agents](anthropic-scaling-managed-agents-meta-harness-interface-design-2026.md) — Managed Agents 的接口稳定性设计
- [Cursor Self-hosted Cloud Agents](cursor-self-hosted-cloud-agents-harness-enterprise-2026.md) — enterprise IT for agents
- [Cursor Cloud Agent harness as product](cursor-cloud-agent-harness-as-product-99-reliability-2026.md) — 99% reliability 之路

### 8.3 设计模式映射

| Cursor iOS 设计 | 通用 harness 模式 |
|----------------|------------------|
| Remote Control 协议 | control plane / execution plane 分离 |
| source: iosApp 标签 | session-level source tagging |
| cache-first + append-only | offline-first + retry safety |
| Permission 决策在 cloud | centralized authorization |
| Privacy Mode opt-in | progressive consent |

---

**TL;DR**：Cursor iOS 不是一个 mobile app，是 Cursor 把 agent harness 拆成「cloud control loop + local execution」的工程化产物。Remote Control 协议、source 标签、cache-first 架构、Privacy Mode 四个机制构成一个完整的跨设备 agent harness 范式。下一代 AI coding 产品——不管是 IDE 扩展、CLI 还是 web app——都会沿用这套拓扑。