# 桌面 AI Agent 三大架构：OpenClaw vs Manus AI vs Perplexity Computer Use

> **本质**：三种不同的"让 AI 操作电脑"思路，背后是三种完全不同的工程哲学、安全模型和成本结构。本文不是功能对比，而是架构层拆解。

---

## 一、为什么这个对比重要

2026年，"让 AI 操作电脑"这件事已经分化出了三条截然不同的技术路线。这不是功能多少的差异，而是**根本性的架构选择**——这些选择直接决定了系统的安全边界、成本结构、适用场景和技术天花板。

理解这三种架构，是理解当前 Agent 技术演进方向的最佳窗口。

---

## 二、三种架构的核心定义

### OpenClaw：本地优先的开放 Agent 框架

**定位**：开源 Agent 框架，给 AI 对本地机器的完整控制权。

**架构本质**：OpenClaw 在本地机器上启动一个 WebSocket 网关（`ws://127.0.0.1:18789`），通过 Bridge 插件连接各种消息平台（WhatsApp、Telegram、Discord、Slack 等），同时将本地文件、终端、浏览器等资源作为 Skills 暴露给 AI 模型。

GitHub 60 天内从 9,000 星飙升至 157,000 星，成为 2026 年最受关注的开源项目之一。

**核心技术路径**：
```
用户消息 → Platform Bridge → Gateway（WebSocket）
  → Node（AI模型对话）→ Skills/Memory Layer → 本地资源
```

**代表能力**：直接文件系统访问、终端命令执行、浏览器自动化、跨消息平台接入、Skill 插件生态（100+ 官方/社区 Skills）、Supermemory 持久化记忆、Hooks 事件驱动自动化。

---

### Manus AI（Meta 收购）：云端沙箱 + 本地桌面延伸

**定位**：通用 AI Agent 服务，通过云端隔离环境完成任务执行。

**架构本质**：Manus 最初运行于云端隔离沙箱（网络、Python 执行环境、文档编辑），通过 Telegram 或网页控制。**2026年3月16日发布桌面应用「My Computer」**，通过 `osascript`（macOS）和 CLI 命令在用户机器上执行操作——这是**云端智能 + 本地执行混合架构**的首次大规模产品化。

Meta 收购的背景让 Manus 从独立创业公司变成了巨头的战略布局。

**核心技术路径**（My Computer 模式）：
```
用户任务 → Manus云端（规划+智能）→ osascript/CLI（本地执行）
  → 结果回传云端 → 最终交付物
```

**代表能力**：云端通用任务执行（Telegram 控制）、My Computer 本地文件操控（osascript）、多步自主任务（数十分钟跨度）、Gmail/Google Calendar 云端集成。

---

### Perplexity Computer Use：浏览器自动化的极致简化

**定位**：以浏览器自动化为核心的 AI 助手，专注信息获取和网页操作。

**架构本质**：Perplexity Computer Use 将整个浏览器作为 Agent 的操作界面，通过浏览器自动化（点击、填表、导航）完成任务。最轻量的桌面 Agent 方案——不需要本地安装、不需要 API key、不需要配置。

**核心技术路径**：
```
用户指令 → AI模型（Perplexity后端）→ 浏览器自动化API
  → 网页操作 → 结果呈现
```

**代表能力**：网页信息获取、在线表单填写、浏览器内多步骤操作、云端模型推理。

---

## 三、架构哲学的深层对比

### 控制权归属：谁做主

| 维度 | OpenClaw | Manus AI | Perplexity |
|------|----------|----------|------------|
| **AI 运行位置** | 本地（用户机器）| 云端（Manus服务器）| 云端（Perplexity服务器）|
| **数据流向** | 不离开用户机器 | 经过 Manus 云端 | 经过 Perplexity 云端 |
| **配置复杂度** | 高（需技术配置）| 低（开箱即用）| 最低（无需安装）|
| **定制空间** | 无限（开源代码）| 受限（无源码）| 受限（无源码）|
| **运维责任** | 用户承担 | Manus 承担 | Perplexity 承担 |

**核心哲学分歧**：

OpenClaw 的哲学是"**最大权力交给用户**"——类似 Linux 的思路。强大、灵活，但要求用户有能力对系统负责。

Manus 的哲学是"**用户只管干活，基础设施我们包**"——类似 Apple 的思路。零配置，但付出了对云端的信任代价。

Perplexity 的哲学是"**最简单的事，最简单的方案**"——专注浏览器场景，不做全系统控制。

---

## 四、安全模型：三种完全不同的风险结构

这是三种架构最核心的差异点，也是企业选型时最容易被忽视的维度。

### OpenClaw：本地全权访问 = 本地全部风险

OpenClaw 给 AI 的权限是**机器级**的——文件读写、终端命令、应用启动。**CVE-2026-25253**（OpenClaw 一键 RCE）揭示了这个问题的本质：当 AI 有完整系统访问权限时，一个 prompt injection 就可能导致完整的机器接管。

但硬币的另一面：**所有数据都在本地**，不存在数据泄露给第三方的问题。

```
OpenClaw 安全特点：
✅ 数据主权完整（无云端数据泄露风险）
✅ 用户完全控制 API key 和凭据
✅ 可观测性强（本地日志完全透明）
❌ AI 自主操作风险由用户承担
❌ 本地漏洞 = 系统漏洞
❌ 需要用户具备安全运维能力
```

### Manus AI：云端隔离 = 信任换便利

Manus 的安全模型是"沙箱隔离"——任务在 Manus 的云端沙箱中执行，结果返回用户。本地机器的资源（文件、应用）通过 osascript 访问，但核心推理和数据处理在云端。

```
Manus 安全特点：
✅ 有安全团队负责基础设施
✅ 沙箱提供任务级隔离
✅ 无本地 AI 漏洞暴露面
❌ 所有任务数据经过 Manus 云端
❌ 企业合规要求（GDPR、数据主权）需评估
❌ osascript 本地命令执行仍存在攻击面
❌ 云服务中断 = Agent 能力中断
```

### Perplexity Computer Use：浏览器沙箱 = 最小攻击面

Perplexity 的安全模型最为简单——浏览器沙箱本身就是隔离层。恶意操作最多影响浏览器会话，不涉及文件系统或系统级权限。

```
Perplexity 安全特点：
✅ 最小权限原则（浏览器沙箱）
✅ 无本地安装，无持久化访问
✅ 架构简单，安全审计成本低
❌ 能力受限（只做浏览器内操作）
❌ 无法访问本地文件/应用
❌ 任务复杂度上限低
```

### 安全选型矩阵

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| 处理敏感企业数据 | OpenClaw（本地模型）| 数据不出机器 |
| 非技术团队快速上手 | Manus AI | 零配置， Telegram 控制 |
| 仅需网页信息获取 | Perplexity | 最小权限，够用即可 |
| 高安全要求（金融/医疗）| OpenClaw + 严格 Harness | 本地 + 人机协同 |
| 移动优先场景 | Manus AI | iPhone 也能跑 Agent |

---

## 五、成本结构对比

### OpenClaw：前期贵，后期几乎为零

```
框架本身：免费（开源）
API 调用：按量付费（Claude/GPT-4o/本地模型）
运维成本：配置 + 维护（时间成本高）
规模化：边际成本趋近于零
```

某社区用户评估：重度使用每月 API 费用可控（取决于模型选择和任务量），但"学习曲线成本"不可忽视。

### Manus AI：前期零成本，后期按订阅

```
入门门槛：极低（Telegram 开聊即可）
免费额度：有限
Pro 订阅：按月/年付费
规模化：成本线性增长
隐性成本：数据隐私溢价
```

用户社区反馈："Manus feels like the most non config instantly usable agent but expensive as hell."

### Perplexity Computer Use：最低门槛方案

```
使用成本：包含在 Perplexity 订阅中
额外费用：无
规模化：受限于 Perplexity 服务条款
```

---

## 六、四层架构 vs 云端沙箱：工程细节

### OpenClaw 四层架构

```
Layer 1 · Gateway（WebSocket，ws://127.0.0.1:18789）
  └── 接收 Bridge 消息、会话管理、速率限制、Token 验证

Layer 2 · Nodes（AI模型实例）
  └── 与模型通信、上下文维护、Skill 调用协调
  └── 支持 Agent Teams（多 Node 协作）

Layer 3 · Channels（Bridges for 每种消息平台）
  └── WhatsApp/Telegram/Discord/Slack/Signal/iMessage
  └── 每 Bridge 独立进程，消息格式标准化

Layer 4 · Skills & Memory
  └── Skills：文件I/O、代码执行、GitHub操作、日历、邮件等
  └── Supermemory：持久化记忆（Markdown格式）
  └── Hooks：事件驱动自动化
```

### Manus 云端沙箱架构

```
用户任务 → 云端 Manus 引擎
  → Plan-Execute-Reflect 循环
  → [云端操作：Web浏览 / 数据处理 / 报告生成]
  → [本地操作：osascript / CLI → 文件/应用]
  → 结果交付

My Computer 增强：
  云端保留 Gmail/Calendar 集成
  本地增加 osascript 文件操作
  形成"文件本地 + 邮件云端"混合流
```

### Perplexity 浏览器架构

```
用户指令 → Perplexity 云端推理
  → 浏览器自动化 API
  → DOM 操作（点击/填表/导航）
  → 结果渲染
```

---

## 七、能力边界：谁擅长什么

| 任务类型 | OpenClaw | Manus AI | Perplexity |
|---------|----------|----------|------------|
| 本地文件批量处理 | ✅ 极强 | ✅ 强（osascript）| ❌ 不支持 |
| 浏览器自动化 | ✅ 强 | ✅ 云端模拟 | ✅ 强 |
| API / 数据库操作 | ✅ 强 | ⚠️ 受限 | ❌ 不支持 |
| 多步骤自主任务（小时级）| ✅ 强 | ✅ 强 | ❌ 受限 |
| 实时终端操作 | ✅ 极强 | ⚠️ 有限 | ❌ 不支持 |
| 移动端控制 | ⚠️ 需配置 | ✅ Telegram | ❌ 不支持 |
| 代码编写/调试 | ✅ 极强 | ✅ 强 | ⚠️ 受限 |
| 非技术用户友好度 | ❌ 低 | ✅ 高 | ✅ 极高 |
| 数据隐私保证 | ✅ 最高 | ⚠️ 需评估 | ⚠️ 需评估 |

---

## 八、选型决策框架

### 问自己三个问题

**问题 1：数据主权要求多高？**

- 金融/医疗/法律数据 → **OpenClaw**（数据不出机器）
- 一般业务数据 → **Manus AI**（评估合规要求后）
- 公开信息操作 → **Perplexity**（无需考虑）

**问题 2：用户的技术能力如何？**

- 能配置本地环境、管理 API key → **OpenClaw**
- 非技术背景，需要快速上手 → **Manus AI**
- 只需简单网页操作 → **Perplexity**

**问题 3：任务的复杂度上限？

- 需要深度系统集成、长期自主执行 → **OpenClaw**
- 需要通用任务能力，但不想管运维 → **Manus AI**
- 单一网页任务，不需要复杂流程 → **Perplexity**

### 实践中的选择

| 用户画像 | 推荐 | 理由 |
|---------|------|------|
| 独立开发者，技术流 | OpenClaw | 最大控制力，长期成本低 |
| 创业公司，快速验证 | Manus AI | 零配置，快速出活 |
| 企业安全团队 | OpenClaw + DefenseClaw | 本地控制 + Agent 安全审计 |
| 非技术业务人员 | Manus AI | Telegram 控制，随时随地 |
| 研究/爬虫场景 | Perplexity | 最小摩擦，够用就好 |

---

## 九、融合趋势与未来

### 架构正在融合

**Manus My Computer** 的出现本身就是证明：纯云端路线不够，需要本地执行能力。这意味着：

- **OpenClaw** 未来可能增加更简单的非技术用户入口
- **Manus** 不会放弃本地能力（osascript 只是开始）
- **Perplexity** 可能在浏览器之外扩展本地能力

### Agent Protocol 的角色

三条路线最终都需要解决同一个问题：**Agent 如何可靠地操作各种工具和资源**。

这正是 MCP（Model Context Protocol）成为 97M+ 安装的事实标准的原因——无论底层架构是本地框架还是云端服务，MCP 提供了统一的工具调用接口。

未来，选择 OpenClaw、Manus 还是 Perplexity，可能更多是**部署架构**的决策，而非**能力边界**的决策——因为通过 MCP，它们可以互操作。

---

## 十、总结

| 维度 | OpenClaw | Manus AI | Perplexity |
|------|----------|----------|------------|
| **架构哲学** | 本地优先，最大控制 | 云端智能 + 本地执行 | 浏览器自动化，轻量 |
| **数据主权** | 最高（数据不出机器）| 需评估（经过云端）| 需评估（经过云端）|
| **技术门槛** | 高 | 低 | 最低 |
| **安全模型** | 机器级权限+用户负责 | 沙箱隔离+厂商负责 | 浏览器沙箱，最小攻击面 |
| **成本结构** | 前期高/后期低 | 前期低/订阅制 | 包含在订阅中 |
| **适用场景** | 技术用户/高隐私需求 | 非技术/快速上手 | 简单网页任务 |

**没有"最好"的架构，只有"最适合"的选择。**

理解这三种架构的设计哲学和工程边界，比争论功能多少更有价值。

---

## 参考文献

1. [OpenClaw vs Manus AI: The Complete 2026 Comparison - FlyPix AI](https://flypix.ai/openclaw-vs-manus-ai/)
2. [Manus vs Claude Code vs OpenClaw: 2026 AI Agent Framework Deep Comparison - Meta Intelligence](https://www.meta-intelligence.tech/en/insight-openclaw-vs-manus)
3. [Introducing My Computer: When Manus Meets Your Desktop - Manus](https://manus.im/blog/manus-my-computer-desktop)
4. [March 2026 AI Roundup: The Month That Changed AI Forever - DigitalApplied](https://www.digitalapplied.com/blog/march-2026-ai-roundup-month-that-changed-everything)
5. [CVE-2026-25253 - OpenClaw Security Advisory](https://www.reddit.com/r/node/comments/1r7ipzc/agent_wall_opensource_security_firewall_for/)

---

*本文属于 Stage 11（Deep Agent）演进阶段，探讨 Deep Agent 的具体落地形态差异。*
