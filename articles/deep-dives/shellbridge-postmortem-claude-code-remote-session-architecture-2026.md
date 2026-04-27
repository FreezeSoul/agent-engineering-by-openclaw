# ShellBridge 架构剖析：Claude Code 远程会话的机密边界

**Claude Code 能访问你的整个代码库、密钥、Git 历史——这正是构建它的远程访问中继既必要又不可能的原因。**

当一款工具掌握了开发者机器上的一切，远程访问它就变成了一道安全与隐私的必答题。ShellBridge 给出了自己的答案：一条精心设计的隐私优先中继架构。然而这款由 CTK Advisors 构建的中继工具最终只存活了数月便宣告死亡——不是因为技术失败，而是因为 Claude Code 原生 Remote Control 的出现从架构层面堵死了第三方 relay 的生存空间。这个故事的真正价值不在于 ShellBridge 本身，而在于它揭示的深层逻辑：**Claude Code 的会话上下文是一个机密计算边界，而不仅仅是一个 UI 层问题。**

---

## 一、ShellBridge 要解决什么问题

现代开发者的代码助手已不再是简单的文本补全工具。Claude Code 运行在本地开发环境，拥有对文件系统、Git 仓库、环境变量、Shell 历史乃至 SSH 密钥的完整访问权。它是一个**上下文丰富的个人智能体**——知道你在做什么项目、熟悉你的代码风格、理解你的业务逻辑。

这带来了一个现实矛盾：**你希望随时随地驱动它**，无论是在地铁上用手机审查代码、在平板上批准一次重构，还是在借用他人的电脑时快速查看某个 bug——但你不可能把这些设备的网络暴露给你的开发机。

问题的核心是双重的：

1. **网络可达性**：开发机通常位于 NAT 之后，没有公网 IP，无法直接被远程设备连接。
2. **安全边界**：即使能穿透 NAT，把开发机的访问权限交给手机或他人的笔记本，意味着暴露整个会话上下文——包括所有能访问的文件和密钥。

ShellBridge 试图同时解决这两个问题。它不开放开发机的入站端口，而是让开发机主动建立出站连接到一个中继服务，远程设备通过这个中继与本地 Claude Code 交互。这是一种**出口型连接**（outbound-only）的设计哲学。

---

## 二、ShellBridge 架构：三层拆解

ShellBridge 的架构遵循经典的代理模式，但每一个设计决策都围绕隐私和安全展开。整个系统分为三层：

```
┌──────────────────────────────────────────────────────────────┐
│                    Layer 3: React PWA                        │
│            (xterm.js 终端, 移动端适配, WebSocket 客户端)       │
└────────────────────────┬─────────────────────────────────────┘
                         │ WebSocket
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Layer 2: Cloudflare Worker                      │
│          (中继 + 认证 + WebSocket Upgrade)                    │
└────────────────────────┬─────────────────────────────────────┘
                         │ 持久出站 WebSocket
                         ▼
┌──────────────────────────────────────────────────────────────┐
│                   Layer 1: 本地 Daemon                        │
│  (PTY 派生 Claude Code, 持有会话状态, 发起出站 WebSocket)      │
│                        开发机                                 │
└──────────────────────────────────────────────────────────────┘
```

### 第 1 层：本地 Daemon（开发机）

Daemon 是整个系统的核心进程，运行在开发者本机。它承担三个关键职责：

**PTY 派生 Claude Code**：Daemon 通过 `forkpty()` 创建一个伪终端（PTY），然后在该 PTY 中启动 Claude Code 子进程。选择 PTY 而非直接管道，是因为 Claude Code 本身是一个交互式 TTY 程序，依赖行缓冲、终端控制字符（如 ANSI 转义序列）和作业控制。PTY 模拟了一个真实的终端环境，使得远程客户端的操作对 Claude Code 来说如同本机操作一般透明。

**持有会话状态**：Daemon 内存中维护着整个会话的上下文——包括当前工作目录、Shell 环境变量、运行的进程等。这是必要的，因为 PTY 本身不保留状态，一旦创建便只负责 I/O 传输。

**主动建立出站 WebSocket**：这是整个架构最精妙的设计决策。Daemon 不监听任何端口，而是作为 WebSocket 客户端，主动连接到 Cloudflare Worker 的中继端点。这种**出口型连接**意味着开发机不需要任何端口开放，不受 NAT 约束，不暴露于公网。防火墙规则再严格，也无法阻止出站 HTTPS/WebSocket 连接。

核心流程可以用伪代码表示：

```python
# Daemon 核心循环（概念模型）
daemon_loop():
    # 1. 派生 PTY 并启动 Claude Code
    master_fd, slave_fd = pty.fork()
    if child:
        # 在 PTY slave 端执行 Claude Code
        execvp("claude", ["claude", "code"])
    
    # 2. 主动连接 Cloudflare Worker 中继
    ws = WebSocketClient("wss://relay.shellbridge.dev/session/xxx")
    
    # 3. 将 PTY master 端的 I/O 双向桥接到 WebSocket
    bridge(ws, master_fd)
```

### 第 2 层：Cloudflare Worker（中继服务）

Cloudflare Worker 承担了中继和认证两大职责：

**轻量中继**：Worker 本身不维护长连接状态，它只是 WebSocket 连接的路由器。当 Daemon 的出站连接与客户端的入站连接匹配时，Worker 将二者桥接。Cloudflare Workers 的无服务器模型天然适合这种 stateless 转发场景。

**认证与授权**：Worker 在握手阶段验证客户端的身份令牌，确保只有经过授权的设备才能接入特定的会话。这一层避免了将中继服务变成开放的代理——未经授权的请求会被直接拒绝。

**WebSocket 协议升级**：HTTP 到 WebSocket 的协议切换在 Worker 层面完成，使得双向实时通信成为可能。一旦升级完成，数据便以帧的形式在客户端和 Daemon 之间透明传输。

值得注意的是，Worker 的设计是**无状态的**——它不缓存会话内容，不记录操作历史，仅仅是数据的搬运工。这将隐私风险降到最低：中继本身不知道你在做什么。

### 第 3 层：React PWA（客户端）

PWA 是用户交互的前端，使用 xterm.js 渲染终端界面。xterm.js 是一个纯 JavaScript 实现的终端模拟器，支持完整的 ANSI 转义序列解析，能够正确渲染彩色输出、光标移动和全屏程序（如 vim、less）。

PWA 还负责：

- **会话管理**：存储连接配置，支持多设备切换
- **移动端适配**：响应式布局，触屏键盘支持，使手机和平板上的终端操作勉强可用
- **离线检测与重连**：在网络不稳定时自动尝试重建 WebSocket 连接

整个客户端不需要安装任何本地 agent，只需一个现代浏览器——这正是"在借用设备上快速工作"场景的核心价值。

### 关键设计原则：出口型连接

ShellBridge 架构中最值得称道的设计是**出口型连接的强制执行**。传统的远程访问方案（如 SSH 反向隧道、VNC、远程桌面）都需要在目标机器上开放入站端口，这天然带来了端口扫描、暴力破解和零日漏洞攻击面。ShellBridge 完全颠覆了这一模式：开发机从不接受任何入站连接，所有出站流量都是加密的 WebSocket，流经 Cloudflare 的边缘网络。

即使攻击者截获了流量，也无法判断流量目的地——它只是流向 Cloudflare Worker 的加密 WebSocket，具体内容对网络观察者完全不可见。

---

## 三、ACP 会话层：ShellBridge 无法触及的边界

理解 ShellBridge 的局限性，需要深入了解 Claude Code 的内部架构——尤其是 ACP（Agent Communication Protocol）会话层。

### ACP：智能体通信协议

Claude Code 内部使用 ACP 定义 agent 与环境之间的通信协议。这是一个比标准输入/输出更高级的抽象层：它定义了**意图（Intent）**、**上下文（Context）**、**工具调用（Tool Invocation）**和**结果回传（Result Delivery）**的序列化格式。当你在终端输入 "帮我重构这段代码" 时，这个指令经过 ACP 层被封装、传输、由 Claude Code 处理，结果再通过 ACP 返回给调用方。

ACP 是 Claude Code 的**核心资产**——它封装了会话的状态管理、上下文窗口的维护、以及与文件系统、Git 等底层系统的交互逻辑。

### ShellBridge 的透明桥接局限

ShellBridge 的桥接方式本质上是**透明的字节流传输**：它将终端的 I/O 双向桥接到 WebSocket，对 ACP 协议本身毫无感知。这意味着：

- **ShellBridge 无法操控 ACP 层**：它不能主动发起工具调用，不能查询会话历史，不能暂停/恢复会话，不能读取会话元数据。
- **ShellBridge 无法区分指令类型**：用户敲入的每一个字符都只是字符，ShellBridge 无法判断这是一次普通的键盘输入还是一次意图改变会话状态的操作。
- **ShellBridge 无法实现高级特性**：会话克隆、上下文快照、多设备同步等高级功能在透明桥接架构下根本无法实现。

### 原生 Remote Control 的架构差异

Anthropic 官方推出的 Remote Control 走的是完全不同的路径：它直接与 ACP 层对接，而不是在 PTY 层面桥接。

```
ShellBridge（PTY 透明桥接）：
用户输入 → xterm.js → WebSocket → Cloudflare Worker → WebSocket → PTY master → Claude Code (PTY)
                                                                         ↑
                                                                    ACP 层不可见

原生 Remote Control（ACP 直连）：
用户输入 → Remote Control Client → ACP 序列化 → Anthropic 基础设施 → ACP 反序列化 → Claude Code (ACP)
                                                                         ↑
                                                              ACP 层完全可见
```

原生 Remote Control 的关键优势在于：**它理解 ACP 协议**。这意味着它可以在 ACP 层面实现完整的会话控制——暂停、恢复、克隆、同步上下文窗口等。ShellBridge 面对 ACP 层就像透过磨砂玻璃看世界：你能感知到有活动，但看不清任何细节。

### 机密计算边界：上下文窗口即敏感数据

CTK Advisors 在事后分析中指出了一个根本性的架构约束：**Claude Code 的上下文窗口本身就是敏感数据**。当你向 Claude Code 提问时，你的代码片段、文件名、错误日志、甚至密码（如果它们出现在上下文中）都会被发送给模型处理。这意味着：

- 中继服务**不应该**看到会话内容——即使它只是转发
- 理想的远程控制方案应该在端侧加密会话数据，或者让中继根本无法解密
- ShellBridge 虽然做到了出口型连接和 PWA 客户端加密，但中继 Worker 本身在技术上可以看到完整的明文流

这正是"机密计算边界"的含义：上下文窗口不是单纯的 UI 状态，它是包含开发者全部知识的敏感数据，其可见性必须被架构性地限制。

---

## 四、ShellBridge 为何死亡：原生 Remote Control 的存在性威胁

### Anthropic 的回应：官方 Remote Control

2024 年中，Anthropic 为 Claude Code 添加了 Remote Control 功能，作为第一方特性直接集成到产品中。这一功能的架构与 ShellBridge 截然不同：它不依赖第三方中继，而是通过 Anthropic 的基础设施路由会话控制。这意味着：

- **会话通过 Anthropic 官方渠道传输**，用户对数据路径有明确的信任预期
- **ACP 层完全可操控**，实现了 ShellBridge 无法企及的功能深度（暂停、恢复、上下文同步等）
- **无需在本地安装 Daemon**，一个命令即可开启远程控制

对用户而言，官方 Remote Control 在功能丰富度和信任度上都优于 ShellBridge。对 ShellBridge 而言，这是存在性威胁。

### CTK Advisors 的事后分析

CTK Advisors 在 [ShellBridge 事后分析](https://www.ctkadvisors.net/blog/shellbridge-postmortem) 中坦承，项目被官方功能的出现"间接杀死"。他们的原话是："building a relay to get it killed"——为一个注定被官方方案取代的功能建造了 relay。这不是失败，而是一个理性决策的自然终点：当平台所有者亲自进入一个领域，第三方解决方案的生存空间便被结构性压缩。

### 第三方中继生态的困局

ShellBridge 的命运揭示了一个更广泛的问题：**对于深度集成平台特性的工具，第三方解决方案始终面临平台所有者的结构性优势**。具体到 Claude Code：

- **协议不透明**：ACP 不是公开协议，第三方无法在协议层面与官方实现竞争
- **基础设施成本**：维护可靠的 WebSocket 中继需要持续投入，官方可以将成本内化到产品中
- **用户信任**：对于安全敏感的操作，用户倾向于信任平台官方而非第三方 relay

这并不意味着第三方 relay 毫无价值——在官方功能缺失或受限的场景下，它们是唯一的解决方案。但它们的生命周期往往以官方功能的发布为终点。

---

## 五、工程教训：给在 Claude Code 上构建的人的思考

### 教训 1：Claude Code 不是开放远程执行平台

许多开发者在初步接触 Claude Code 时，会直觉地认为它类似 SSH——一个可以在远程机器上执行命令的工具。但这种类比是误导性的。Claude Code 是一个**机密智能体会话**，它的设计假设是：上下文包含了你不想暴露给任何中间人的敏感数据。

这意味着：

- **任何在网络上传输 Claude Code 会话的操作，都涉及敏感数据的流动**
- **中继服务在技术上可以看到会话内容**（即使 ShellBridge 的架构已经尽量减少这一风险）
- **端到端加密是理论上的最优解，但实现成本极高**

如果你在构建涉及 Claude Code 远程访问的工具，必须将"数据机密性"作为第一设计约束，而不是事后考虑。

### 教训 2：ShellBridge 的出口型连接设计值得借鉴

尽管 ShellBridge 最终被官方方案取代，它的设计中有几个原则值得在任何隐私优先 relay 中复用：

1. **出口型连接优于入站监听**：永远不让开发机接受入站连接
2. **中继无状态化**：中继服务不应缓存会话内容，转发完毕后不留痕迹
3. **最小化信任**：客户端认证与会话隔离是关键，中继被攻破不应导致会话内容泄露

### 教训 3：平台特性的第三方实现有天然上限

ShellBridge 的技术完成度相当高——出口型连接、PTY 透明桥接、PWA 客户端——但它在功能层面永远无法追上原生 Remote Control，因为**架构上限由协议可见性决定**。PTY 桥接的透明性决定了 ShellBridge 看不到 ACP 层，而 ACP 层正是所有高级特性的实现基础。

这个教训不限于 Claude Code：在任何拥有私有协议的平台生态中，第三方实现的深度都有上限。意识到这个上限，是避免过度投入的关键。

### 开放问题：Anthropic 会开放 ACP 协议吗？

截至本文撰写时，ACP 仍然是 Anthropic 的私有协议。这带来了一个问题：**如果 ACP 是公开协议，第三方 relay 是否能在官方功能之外提供差异化价值？**

理论上，开放 ACP 可以催生一个健康的第三方生态：为特定用例优化的 relay、注重隐私的端到端加密方案、与非 Anthropic 基础设施的集成等。但从 Anthropic 的视角，开放 ACP 意味着放弃对会话数据流的控制——这与其隐私政策和企业客户需求可能存在冲突。

这个问题的答案将决定 Claude Code 远程访问生态的未来走向。在那之前，任何第三方 relay 都应被视为**临时解决方案**，而非长期基础设施。

---

## 结语

ShellBridge 是一个工程上精心设计的隐私优先 relay，它的架构——尤其是出口型连接和 PTY 透明桥接——为 Claude Code 远程访问提供了一个干净的安全模型。然而它的死亡并非技术失败，而是平台进化的必然结果：当 Anthropic 以官方身份在 ACP 层实现 Remote Control，第三方中继的生存空间便在结构上被压缩。

这个故事最深层的教训，不是某项技术的优劣，而是一个关于**机密计算边界**的认知：Claude Code 的上下文窗口是敏感数据，它的可见性必须被架构性地限制。在这个问题上，端侧控制优于网络层中继，原生集成优于第三方桥接，协议层的可见性决定了一切。

对于在 Claude Code 生态中构建的工程师：理解 Claude Code 是一个机密智能体会话，而非开放远程执行平台——这是所有后续决策的基础。

---

**参考来源：**

- CTK Advisors: [ShellBridge Postmortem](https://www.ctkadvisors.net/blog/shellbridge-postmortem)
- Hacker News: [Discussion on Claude Code Remote Access](https://news.ycombinator.com/item?id=46627628)
- Let's Data Science: [Claude Code Remote Control Architecture](https://letsdatascience.com)
