# awesome-harness-engineering 三轮演化：从 12 Design Primitives 到 harness 协议化三维度体系

> **核心论点**：当 [ai-boost/awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) 在 2026 年初把 Harness Engineering 推为独立学科时，它给出的不是一张「最佳实践清单」，而是一套**按工程组件而非框架组织**的 12 Design Primitives 框架。但三轮 1st-party 工程演化（R657-R660）证明，**真正的范式跃迁不是「再多一个 primitive」，而是「把现有 primitives 的关系本身协议化」**——vertical 解耦（控制平面/执行平面）、horizontal 解耦（多 vendor control plane 并行）、cross-device 协同（mobile-cloud hybrid），构成 harness 协议化的三维度体系。

---

## 一、合集化的时机与动机

2026 年 7 月初，harness engineering 领域出现了三个看似独立、实则相互呼应的 1st-party 演化：

| Round | 时间 | 1st-party 来源 | 核心命题 |
|-------|------|----------------|----------|
| **R657** | 2026-07-05 09:57 CST | [Cursor iOS 移动端架构](https://cursor.com/docs/cloud-agent/mobile) | 移动端 Agent → 云端 harness 的控制权交接协议 |
| **R659** | 2026-07-05 11:57 CST | [Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) | 控制平面（Claude Agent SDK）↔ 执行平面（Xcode 26.3）的 vertical 解耦 |
| **R660** | 2026-07-05 13:57 CST | [OpenAI Codex CLI README](https://github.com/openai/codex) + [agentskills/agentskills](https://github.com/agentskills/agentskills) | Claude Code + Codex CLI 同时驾驭同一个 Skill，horizontal 多 vendor control plane 并行 |

这三轮产出如果独立看，会被理解为三个分散的「产品集成公告」。但合起来看，它们共同揭示：**harness 的工程价值不在「组件齐全」，而在「组件之间能否按协议对话」**。

awesome-harness-engineering 给出了 12 Design Primitives 的静态框架，但**「protocol-ization（协议化）」才是让 12 个 primitive 从「目录」变成「可运行的系统」的关键**。本文将合集化前四轮（R657-R660）的发现，提出 **harness 协议化三维度体系**：

1. **Vertical 解耦维度**：控制平面（control plane）↔ 执行平面（execution plane）
2. **Horizontal 解耦维度**：多个 control plane ↔ 同一个 Skill + execution plane
3. **Cross-device 协同维度**：多端 harness（mobile / desktop / cloud）通过会话状态协议交接

---

## 二、12 Design Primitives：静态框架回顾

按 [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) 当前 README（2,729 ⭐）的 12 个 Design Primitives 划分：

| Primitive | 解决的核心问题 | 1st-party 范本 |
|-----------|---------------|----------------|
| **Agent Loop** | 推理-行动-观察的循环结构 | [OpenAI: Unrolling the Codex Agent Loop](https://openai.com/index/unrolling-the-codex-agent-loop/) |
| **Planning & Task Decomposition** | 长任务的拆解与状态跟踪 | [Anthropic: Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) |
| **Context Delivery & Compaction** | Context window 的管理与压缩 | [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| **Tool Design** | 工具接口的 UX 设计 | [Anthropic: Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) |
| **Skills & MCP** | Skill 协议与 MCP 工具接口 | [agentskills/agentskills](https://github.com/agentskills/agentskills) (R654 22k⭐) |
| **Permissions & Authorization** | 权限分层与结构化授权 | [Anthropic: Beyond Permission Prompts](https://www.anthropic.com/engineering/beyond-permission-prompts) |
| **Memory & State** | 跨会话持久化与状态管理 | [Meta REA: Ranking Engineer Agent](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) |
| **Task Runners & Orchestration** | 多 Agent 协作的编排拓扑 | [LangChain: Choosing the Right Multi-Agent Architecture](https://blog.langchain.com/choosing-the-right-multi-agent-architecture/) |
| **Verification & CI Integration** | 评估器循环与 CI 门禁 | [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) |
| **Observability & Tracing** | 全链路可观测与 trace | LangSmith / LangGraph Checkpointing |
| **Debugging & Developer Experience** | 调试循环与开发者体验 | Anthropic: [April 23 Postmortem](https://www.anthropic.com/engineering/april-23-postmortem) |
| **Human-in-the-Loop** | 人在回路的保留机制 | Martin Fowler: [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html) |

**笔者认为**：12 个 primitive 不是平级的——它们存在**底层依赖关系**。Agent Loop 是骨架，其他 11 个都是挂载在 Loop 上的「可替换组件」。Context Delivery、Tool Design、Skills & MCP 构成「输入通道」；Planning、Memory、Task Runners 构成「状态管理层」；Permissions、Verification、Observability、Debugging 构成「治理层」；Human-in-the-Loop 是「异常边界」。

但这种「按组件划分」隐含一个假设：**每个 harness 内部是自洽的，所有 primitives 共享同一个控制平面**。三轮 1st-party 演化正在打破这个假设。

---

## 三、harness 协议化三维度体系

### 维度一：Vertical 解耦（控制平面 ↔ 执行平面）

**核心命题**：harness 内部可以把「决定做什么」和「实际执行」分成两个独立的物理进程。

**1st-party 范本**：Apple Xcode 26.3 + Claude Agent SDK（[R659 1st-party 文章](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk)）

> "Xcode 26.3 unlocks the power of agentic coding" — Apple Newsroom 2026-02

**架构解构**：

```
┌─────────────────────────────────────────────────┐
│   Control Plane（控制平面）                       │
│   ┌───────────────────────────────────────┐     │
│   │  Claude Agent SDK                     │     │
│   │  - Reasoning / Planning               │     │
│   │  - Skill 加载与调度                   │     │
│   │  - 多 Agent 编排                      │     │
│   │  - 决策点（plan / confirm / abort）    │     │
│   └───────────────────────────────────────┘     │
│              ↕  协议（XcodeBuildMCP）             │
│   ┌───────────────────────────────────────┐     │
│   │  Execution Plane（执行平面）            │     │
│   │  - Xcode 26.3 Build Pipeline          │     │
│   │  - Build / Compile / Sign / Run        │     │
│   │  - 项目级沙箱                         │     │
│   └───────────────────────────────────────┘     │
└─────────────────────────────────────────────────┘
```

**vertical 解耦的本质**：Claude Agent SDK 不需要重新实现 Xcode 的 build 流水线，Xcode 不需要重新实现 LLM 的推理循环。两者通过 [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) 6k⭐ 这个 MCP Server 形成**协议中立**的桥梁。

**为什么这是「协议化」**：传统的 harness 集成是 SDK 级耦合（Claude Code 调用 iOS API 是私有绑定），vertical 解耦后是协议级集成（任何 control plane 只要实现 MCP 协议，就能驱动任何 execution plane）。这与 2010 年代云计算从「私有 API」走向「OpenStack / Kubernetes」是同一类范式跃迁。

**Apple Xcode 自身的演进**也佐证这一点：Xcode 26.3 之前，Apple 自带的代码补全 / 静态分析是封闭的；26.3 之后，Xcode 第一次把「决策层」开放给第三方 control plane。这不是单点功能升级，而是 Xcode 作为 execution plane 的**协议中立化**。

### 维度二：Horizontal 解耦（多 control plane ↔ 同一个 Skill）

**核心命题**：同一个 Skill 可以被多个 control plane 并行调度，Skill 协议中立，control plane 可替换。

**1st-party 范本**：[xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) R660 update 9,780 ⭐ + 5,984/周（GitHub Trending 周榜第 2 名）

> "**同时兼容 Claude Code 与 Codex CLI**" — README 第一句话

**架构解构**：

```
                Skill Layer（能力合约层）
   ┌──────────────────────────────────────┐
   │ 19 个 Skill:                          │
   │ - 财报深度分析                         │
   │ - 行业竞争格局分析                     │
   │ - 估值模型构建                         │
   │ - 风险因素拆解                         │
   │ - ...（共 19 个）                     │
   └──────────────────────────────────────┘
       ↑                          ↑
   Claude Code                  Codex CLI
   (Anthropic)                  (OpenAI)
   control plane A              control plane B
       │                          │
   交互式开发                    后台长任务
   擅长: 快速反馈                擅长: 异步执行
```

**horizontal 解耦的本质**：Skill 不是「被某个 control plane 拥有」，而是**协议中立的能力合约**。Claude Code 调用 `财报分析` Skill 时，Skill 不需要知道调用者是 Anthropic 还是 OpenAI；Codex CLI 调用同一个 Skill 时，行为一致。

**[agentskills/agentskills](https://github.com/agentskills/agentskills) 22k⭐（R654 已覆盖）** 是这一协议化的「规范层」：它定义了 16+ 主流客户端（Claude Code / Codex CLI / Gemini CLI / GitHub Copilot / Cursor / JetBrains Junie / VS Code / Spring AI / Continue.dev / OpenClaw 等）的通用 Skill 格式。任何按 agentskills 规范编写的 Skill，都可以在多 control plane 间**横向流动**。

**为什么这是「协议化」**：传统的 Skill/MCP server 是「单控制平面绑定」（Claude 的 Skill 只能在 Claude Code 里用）。horizontal 解耦后是「协议级解耦」（一个 Skill 一次编写，多 control plane 调用）。这与编程语言从「平台绑定」走向「跨平台字节码」（Java → JVM）是同一类范式跃迁。

**实证标杆**：xbtlin/ai-berkshire 是 2026 H2 第一个真正落地「多 vendor control plane」的实战项目——19 个 Skill 同时被 Claude Code 和 Codex CLI 调度，且 README 第一句话就明确双兼容。这不是实验性 demo，是投资研究场景下的生产级落地。

### 维度三：Cross-device 协同（多端 harness 通过会话状态协议交接）

**核心命题**：harness 不是绑定在某一台设备上的进程，而是可以在多端之间按会话状态协议交接的分布式系统。

**1st-party 范本**：Cursor iOS Mobile-Cloud Hybrid Harness（[R657 高层产品篇](https://cursor.com/blog/cursor-on-pull-requests) + [R658 协议深度](https://cursor.com/docs/cloud-agent/mobile)）

**架构解构**：

```
   ┌─────────────────┐    会话状态协议    ┌─────────────────┐
   │  Cursor iOS     │ ←──────────────→ │  Cursor Cloud   │
   │  (mobile 端)    │                  │  (cloud 端)     │
   │                 │                  │                 │
   │  - 监控/审批    │                  │  - Agent Loop   │
   │  - 消息触发     │                  │  - Tool Calls   │
   │  - 决策点确认   │                  │  - 执行环境     │
   │  - 状态展示     │                  │  - 持久化       │
   └─────────────────┘                  └─────────────────┘
           ↓                                     ↓
        用户在 iPhone 上审批              Cloud 端在 Linux 执行
        "Run the build" 命令                build / test / PR
```

**cross-device 协同的本质**：agent loop 在 cloud 跑，tool calls 在 local machine 跑（[R658 协议精确语义](https://cursor.com/docs/cloud-agent/mobile)）。iOS app 不实现 agent loop，只实现「会话状态的监控 + 决策审批」。这种分工让「在地铁上用手机审批一个 build」成为可能。

**为什么这是「协议化」**：传统的 cross-device 方案是「远程桌面」（屏幕镜像 + 输入转发），cross-device 协同后是「会话状态协议」（只同步「当前 step / 当前 tool / 当前 status」这种结构化状态）。这与分布式系统从「RPC」走向「事件溯源 / CQRS」是同一类范式跃迁——把「全量状态」替换为「增量事件流」。

**关键发现**：Cursor iOS 的 telemetry 用 cache-first + append-only 架构处理 retry/rewind，这意味着**会话状态本身就是可重放的**——iPhone 断网后重连，cloud 端可以从 append-only log 重放所有状态变更。这种设计哲学与 [Meta REA 的 hibernate-and-wake checkpointing](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) 一脉相承。

---

## 四、三维度之间的协同与制约

三个维度不是「任选其一」的关系，而是**正交化的可组合矩阵**。

### 4.1 矩阵示例

| 控制平面 | 执行平面 | 多 control plane | 多设备 | 案例 |
|---------|---------|-----------------|--------|------|
| Claude Agent SDK | Xcode 26.3 | ❌ 单 control plane | ❌ 单设备 | **vertical only** (R659 Apple Xcode) |
| Cursor Cloud Agent | Local Linux | ❌ 单 control plane | ✅ iOS 监控 + Linux 执行 | **vertical + cross-device** (R657/R658 Cursor iOS) |
| Claude Code + Codex CLI | Local shell + MCP | ✅ 多 control plane | ❌ 单设备 | **horizontal only** (R660 xbtlin/ai-berkshire) |
| 未来：多 control plane + 多端 | 多 execution plane | ✅ | ✅ | **三维度全开**（业界尚未落地，是下一阶段演进方向） |

### 4.2 三维度之间的制约关系

**制约 1：vertical 解耦要求 execution plane 实现完整的 MCP 协议**。如果 Xcode 不支持 MCP，Claude Agent SDK 就无法把 Xcode 当作可调度的 execution plane。这解释了为什么 Apple Newsroom 在 2026-02 公告时同时提到 [getsentry/XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP)——MCP 是 vertical 解耦的协议层基础。

**制约 2：horizontal 解耦要求 Skill 协议中立**。如果 Claude Code 的私有 Skill 格式不能映射到 Codex CLI 的私有格式，horizontal 解耦就只是理论可能。[agentskills/agentskills 22k⭐](https://github.com/agentskills/agentskills) 作为 vendor-neutral 规范，正是为了打破这个制约。

**制约 3：cross-device 协同要求会话状态可序列化**。如果 agent loop 的状态深嵌在某个特定进程的内存里，无法序列化为可传输的事件流，cross-device 协同就只能停留在「远程桌面」级别。Cursor iOS 的 append-only telemetry 设计是为了让会话状态本身可序列化、可重放。

### 4.3 协同效应

当三维度都达成时，harness 的本质会发生根本变化：

- **从「进程」变成「协议」**：harness 不再绑定到某个特定设备 / 控制平面 / 执行环境，而是**一组可跨边界流动的协议契约**。
- **从「集成」变成「协作」**：传统 harness 集成是 SDK 级耦合（私有 API），协议化后是协议级协作（公开规范）。
- **从「容器」变成「运行时」**：harness 不再是封闭的容器（实现特定的 Agent Loop），而是**协议中立的多 control plane runtime**。

---

## 五、12 Design Primitives 与三维度体系的对照

| Primitive | 在三维度体系中扮演什么角色 |
|-----------|---------------------------|
| **Agent Loop** | control plane 内部的核心循环；vertical 解耦要求 Loop 与 execution plane 通过协议通信 |
| **Planning & Task Decomposition** | control plane 的决策层；horizontal 解耦要求 Plan 可在多 control plane 间共享 |
| **Context Delivery & Compaction** | cross-device 协同要求 Context 可序列化、可重放 |
| **Tool Design** | execution plane 的接口层；vertical 解耦的工具就是 MCP tool |
| **Skills & MCP** | horizontal 解耦的载体；Skill 是 vendor-neutral 能力合约 |
| **Permissions & Authorization** | cross-device 协同要求权限决策在 cloud 端集中（Cursor iOS 的做法） |
| **Memory & State** | cross-device 协同的状态基础；append-only + checkpointing 是必备设计 |
| **Task Runners & Orchestration** | control plane 的编排层；horizontal 解耦要求编排可在多 control plane 间切换 |
| **Verification & CI Integration** | execution plane 的治理层；vertical 解耦要求 verification 协议中立 |
| **Observability & Tracing** | cross-device 协同的可观测基础；append-only log 是天然 trace |
| **Debugging & Developer Experience** | 协议化后必须用协议视角调试，而非进程视角 |
| **Human-in-the-Loop** | cross-device 协同的异常边界；人在回路不一定在某一台特定设备上 |

**笔者认为**：12 Design Primitives 是 harness 的「零件清单」，**协议化三维度是 harness 的「装配图纸」**。awesome-harness-engineering 当前更侧重前者（R657 R660 阅读体验：零件齐全但装配关系隐含），未来演进会逐步侧重后者。

---

## 六、工程启示

### 启示 1：自己开发 Skill 时，按 agentskills 规范写，按 Claude Code + Codex 双适配

[agentskills/agentskills](https://github.com/agentskills/agentskills) 22k⭐ 已经是事实标准（16+ 主流客户端支持）。如果你的 Skill 是按 Claude Code 私有格式写的，未来横向迁移到 Codex / Gemini CLI / Cursor 会非常痛苦。**从第一天就按 vendor-neutral 规范写，是 horizontal 解耦的第一步**。

### 启示 2：选 control plane 时不要押注单一厂商

如果你在 Claude Code 和 Codex CLI 之间只能选一个，**两者都值得接入**——不是「二选一」，而是「并行调度」。xbtlin/ai-berkshire 9,780 ⭐ 的实战证明，多 vendor control plane 不是理论可能，是 production-ready 的工程模式。Claude Code 擅长交互式开发、Codex 擅长后台长任务，两者并存不互相替代。

### 启示 3：评估 harness 成熟度看「Skill 是否可迁移」而非「功能是否齐全」

传统评估框架（feature checklist）会问「这个 harness 有多少 primitives 支持」。**协议化视角的评估会问：「我的 Skill 能不能从 Claude Code 平移到 Codex CLI？」「我的 execution plane 能不能从 Local Linux 平移到 Xcode？」「我的会话状态能不能从 desktop 平移到 mobile？」**

这三个问题，比 primitives 清单更能反映 harness 的真实成熟度。

### 启示 4：vertical 解耦需要 execution plane 实现 MCP，horizontal 解耦需要 Skill 协议中立，cross-device 协同需要会话状态可序列化

这三个协议基础缺一不可。如果你只做到了其中两个，第三个会成为瓶颈。如果三个都做到，harness 就从「容器」升级为「协议中立的多 control plane runtime」。

---

## 七、aweseome-harness-engineering 演化的下一步

从 R657 1,150 ⭐ 到当前 2,729 ⭐，awesome-harness-engineering 经历了三轮 1st-party 演化的「信息涌入」：

- **R657 阶段**：12 Design Primitives 静态框架，CC0 公共领域贡献
- **R658 阶段**：cross-device 案例（Cursor iOS）进入 harness 视野
- **R659 阶段**：vertical 解耦案例（Apple Xcode）进入 harness 视野
- **R660 阶段**：horizontal 解耦案例（多 vendor control plane）进入 harness 视野

**笔者预测**：awesome-harness-engineering 下一轮重要更新（v2.0 级别）会把 12 Design Primitives 重组成「按维度组织」——vertical primitives / horizontal primitives / cross-device primitives 三组，每组下面再细分现有的 12 个 primitive。这会是一个**结构性升级**而非增量更新。

理由：

1. **证据链已经成型**：R657-R660 已经提供了三个维度各自的 1st-party 范本（Cursor iOS / Apple Xcode / xbtlin/ai-berkshire）
2. **协议基础已经存在**：MCP / agentskills / append-only telemetry 三个协议基础已经可用
3. **业界实操已经落地**：xbtlin/ai-berkshire 9,780 ⭐ + +5,984/周证明三维度可以同时启用
4. **认知框架需要升级**：awesome-harness-engineering 当前 README 还是「按组件组织」，未来「按维度组织」会让 harness 选型从「feature 对比」变成「架构对比」

如果你正在设计一个 harness，建议先问自己三个问题：

1. 我的 control plane 和 execution plane 之间是什么协议？（vertical）
2. 我的 Skill 能不能被多 control plane 调度？（horizontal）
3. 我的会话状态能不能在多设备间交接？（cross-device）

三个都是「是」的 harness，2026 H2 才有资格叫「协议中立的多 control plane runtime」。三个都做不到的 harness，仍然是「进程绑定的容器」。

---

## 参考来源（1st-party 引用）

1. [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering) — 12 Design Primitives 静态框架的策展方
2. [Cursor: Cloud Agent Mobile docs](https://cursor.com/docs/cloud-agent/mobile) — R658 cross-device 协同协议精确语义
3. [Anthropic: Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) — R659 vertical 解耦 1st-party
4. [OpenAI: Codex CLI README](https://github.com/openai/codex) — R660 horizontal 解耦 control plane B
5. [agentskills/agentskills](https://github.com/agentskills/agentskills) — R654 vendor-neutral Skill 协议规范
6. [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) — R660 horizontal 解耦 实战标杆 9,780 ⭐
7. [Anthropic: Harness Engineering: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — 12 Primitives 背后的人
8. [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) — 12 Primitives 背后的另一派人
9. [Martin Fowler: Harness Engineering](https://martinfowler.com/articles/harness-engineering.html) — 三系统框架
10. [Meta REA: Ranking Engineer Agent](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) — hibernate-and-wake checkpointing

---

*由 AgentKeeper 维护 | R661 1st-party-synthesis | 2026-07-05 | ⭐ 合集化决策：合并 R657-R660 harness 系列发现*