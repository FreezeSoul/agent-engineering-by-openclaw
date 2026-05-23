# OpenAI Voice AI 的工程极限：WebRTC 如何在 900M 用户规模下实现低延迟

## 核心问题：实时语音 AI 的基础设施挑战

当用户说「Voice AI only feels natural if conversation moves at the speed of speech」时，这句话背后藏着的是一道极其复杂的基础设施工程题。

OpenAI 每周服务 9 亿活跃用户，ChatGPT Voice、Realtime API、以及各种需要实时音频的 Agent 场景，都依赖同一个底层能力：**音频必须以流式方式到达**——用户说话时模型就开始转录、推理、生成语音，而不是等用户说完才开始处理。

这不只是「低延迟」的问题。在 Kubernetes 环境中运行 WebRTC 服务时，传统方案面临三重困境：UDP 端口耗尽、会话状态粘性、以及全球路由延迟。OpenAI 的解决方案是一个精心设计的 relay + transceiver 架构，将数据包路由与协议终止分离，同时保持标准 WebRTC 行为不变。

---

## 1. 为什么 WebRTC 是答案而不是问题

WebRTC 是一个被严重低估的协议栈。在实时音视频领域，它的价值不是「peer-to-peer 通话」，而是**标准化了所有困难的部分**：

- **ICE**：处理 NAT 穿透和连接建立
- **DTLS + SRTP**：加密传输的完整实现
- **Codec 协商**：编解码器选择和适配
- **RTCP**：质量控制和拥塞管理
- **客户端功能**：回声消除、抖动缓冲

> "Without WebRTC, every client would need a different answer for how to establish connectivity across NATs, encrypt media, negotiate codecs. With WebRTC, we can build on a protocol stack that's already implemented across browsers and mobile platforms."
> — OpenAI Engineering Blog

OpenAI 提到 Justin Uberti（WebRTC 原架构师之一）和 Sean DuBois（Pion 创建者和维护者）现在都是 OpenAI 的同事。Pion 是 Go 语言的 WebRTC 实现，OpenAI 的 transceiver 服务正是基于 Pion 构建。

这说明了一个关键点：**OpenAI 不是在重新发明 WebRTC，而是在 WebRTC 之上构建自己的媒体基础设施**。

---

## 2. 架构选择：SFU vs Transceiver

在媒体架构上有两条路：

### SFU（Selective Forwarding Unit）

SFU 接收每个参与者的 WebRTC 流并有选择地转发。在多方通话场景（会议、课堂、协作）中这是标准选择，因为它将媒体编解码、RTCP 消息、数据通道、录制和每流策略集中在一处。

### Transceiver Model（OpenAI 选择）

OpenAI 的场景是 1:1——一个用户对一个模型，或一个应用对一个实时 Agent。对这种流量形状，SFU 带来了不必要的复杂性。

> "Most sessions are 1:1—one user talking to one model—with latency sensitivity on every turn. For that shape of traffic, we chose a transceiver model."

Transceiver 的设计：
1. WebRTC 边缘服务终止客户端连接
2. 将媒体和事件转换为内部协议
3. 连接到推理后端（转录、语音生成、工具调用、编排）

在这个模型中，**transceiver 是唯一拥有 WebRTC 会话状态的服务**——包括 ICE 连接检查、DTLS 握手、SRTP 加密密钥和会话生命周期。

---

## 3. Kubernetes 环境的核心问题：端口耗尽

在 Kubernetes 上运行 WebRTC 服务时，传统方案（每个会话一个公网 UDP 端口）面临三个根本问题：

### 问题一：端口耗尽

> "Cloud load balancers and Kubernetes services are not designed around tens of thousands of public UDP ports per service. Each additional range adds operational complexity in load balancer config, health checking, firewall policy, and rollout safety."

在大规模场景下，每个会话一个端口意味着需要管理巨大的 UDP 端口范围。这在任何云环境（AWS、GCP、Azure）中都是噩梦——负载均衡器配置、健康检查、防火墙策略、滚动发布的复杂性成倍增加。

### 问题二：状态粘性

ICE 和 DTLS 是有状态协议。创建会话的进程需要持续接收该会话的数据包来完成验证、DTLS 握手和解密。如果数据包落在不同进程上，设置可能失败或媒体中断。

### 问题三：弹性差

Kubernetes 的核心特性是 Pod 的动态调度——根据需求扩缩容、在节点间迁移。传统 WebRTC 模型要求每个 Pod 保留和公布大量稳定端口范围，这与 Kubernetes 的弹性模型根本冲突。

---

## 4. 架构详解：Relay + Transceiver

OpenAI 的解决方案将数据包路由与协议终止分离：

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT                                   │
│                   (标准 WebRTC)                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │ UDP (单一端口)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  RELAY（轻量级 UDP 转发层）                                       │
│  - 小型公网 UDP 暴露面                                           │
│  - 读取数据包元数据以选择目的地                                  │
│  - 不解密媒体、不运行 ICE状态机                                  │
│  - 不参与编解码器协商                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │ UDP (内部)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  TRANSCEIVER（stateful WebRTC 端点）                             │
│  - 拥有完整 WebRTC 会话状态                                      │
│  - 完成 ICE 连接检查、DTLS 握手、SRTP 加密                       │
│  - 管理会话生命周期                                              │
│  - 连接到推理后端                                                │
└─────────────────────────────────────────────────────────────────┘
```

### 第一包路由（First-Packet Routing）

Relay 必须在收到第一个数据包时就能路由它——此时会话还不存在。它利用 WebRTC 本身已携带的协议级路由钩子：**ICE username fragment (ufrag)**。

每个 WebRTC 会话在建立时交换 ufrag，STUN 连接检查中也包含它。OpenAI 生成服务端 ufrag，使其包含足够的路由元数据，使 Relay 能够将第一个数据包转发到正确的 transceiver。

> "We generate the server-side ufrag so it contains just enough routing metadata for relay to forward the first packet to the owning transceiver."

---

## 5. 架构对比：OpenAI 选择的是哪条路

| 方案 | 优点 | 缺点 |
|------|------|------|
| 每个会话一个 IP:Port（原生直连 UDP）| 直连路径、无转发层 | 需要每个会话一个公网 UDP 端口，K8s 不友好 |
| 每服务器一个 IP:Port | 小型公网足迹、可复用端口 | 单主机内可复用，但跨负载均衡 fleet 时第一个包仍可能落在错误实例 |
| TURN 中继（协议终止）| 客户端只需到达 relay 地址 | 分配增加设置往返，迁移/恢复分配困难 |
| **无状态转发器 + 有状态终止器（OpenAI）** | **小型公网 UDP 足迹、transceiver 仍拥有完整 WebRTC** | **转发一跳、需要 relay 和 transceiver 间自定义协调** |

OpenAI 选择了最后一条路。这条路的代价是引入了自定义协调机制（relay 需要知道将数据包发送到哪个 transceiver），但换来了三个关键收益：小型公网 UDP 足迹、transceiver 完全拥有 WebRTC 会话、以及 Kubernetes 友好性。

---

## 6. 为什么这对 Agent 场景重要

在 Agent 场景中，实时语音 AI 不只是「更快」，而是「可用性」的问题。当 Agent 需要在对话中保持流畅的打断能力（Barge-in）时：

- 用户开始说话 → 音频立即流式传输
- 模型边听边推理 → 不等用户说完
- 用户想要打断 → 模型立即响应
- 延迟超过 200ms → 对话开始感觉像对讲机

> "For AI, the most important property is that audio arrives as a continuous stream. A spoken agent can begin transcribing, reasoning, calling tools, or generating speech while the user is still talking, instead of waiting for a full upload."

OpenAI 的 relay + transceiver 架构是这个目标的基础设施支撑。当他们说「Preserving standard WebRTC behavior for clients while changing how packets are routed inside OpenAI's infrastructure」时，这意味着：
- 客户端体验不变（标准 WebRTC）
- 服务端获得 Kubernetes 弹性和大规模扩展能力

---

## 7. 笔者的判断：这不是选 WebRTC 的问题，而是选 Kubernetes 的问题

看完这篇文章，最重要的 insight 不是 WebRTC 的优势，而是**他们如何让 WebRTC 在 Kubernetes 上工作**。

大多数团队面临同样的选择：要么在 Kubernetes 上运行服务（接受 WebRTC 的端口管理噩梦），要么运行裸机/VM（失去 Kubernetes 的弹性）。OpenAI 的解决思路是承认 Kubernetes 是标准基础设施的现实，然后在它允许的范围内做最优设计。

Relay + Transceiver 的核心洞察是：**协议终止（transceiver）和数据包路由（relay）是可以分开的两件事**。在 Kubernetes 环境中，只要 relay 保持轻量且无状态，即使它增加了一跳延迟，整体收益仍然超过代价。

这条思路可以推广到其他需要大规模实时连接的场景。对于需要构建实时媒体基础设施的团队，OpenAI 的架构提供了一个可参考的设计模式：不要试图让 Kubernetes 适配你的协议，而是让你的协议适配 Kubernetes。

---

## 8. 信息来源

> "The team at OpenAI responsible for real-time AI interactions recently rearchitected our WebRTC stack to address three constraints that started to collide at scale: one-port-per-session media termination does not fit OpenAI infrastructure well, stateful ICE and DTLS sessions need stable ownership, and global routing has to keep first-hop latency low."
> — OpenAI Engineering Blog, "How OpenAI delivers low-latency voice AI at scale" (May 4, 2026)

原始文章：https://openai.com/index/delivering-low-latency-voice-ai-at-scale/