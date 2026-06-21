# Anthropic 自托管沙箱与 MCP Tunnels：企业 Agent 安全基础设施的关键拼图

> 官方来源：Anthropic [Managed Agents Self-Hosted Sandboxes 文档](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes) + [MCP Tunnels 概览](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/overview)（2026年5月19日 Code with Claude London 发布）
>
> 分析来源：["Anthropic Self-Hosted Sandbox: 7 Production Patterns 2026"](https://www.digitalapplied.com/blog/anthropic-self-hosted-sandbox-7-production-patterns-2026)（Digital Applied，2026年5月25日）

---

## 核心命题

Anthropic 在 Code with Claude London（2026年5月19日）发布了两个企业级功能：**Self-Hosted Sandboxes（自托管沙箱）**和 **MCP Tunnels**。这两个功能共同回答了企业采用 Agent 时最关键的合规问题——"代码在哪里执行？数据在哪里流动？"

笔者认为，这两个功能的核心价值不是"让 Agent 跑在企业自己的基础设施上"，而是**将 Agent 的执行平面（execution plane）和编排平面（orchestration plane）解耦**——前者进入企业边界，后者留在 Anthropic。这是在不牺牲 Agent 能力的前提下满足企业安全合规要求的最优路径。

---

## 一、背景：企业采用 Agent 的安全困境

当企业想用 Claude Agent 处理包含敏感数据的任务时，安全团队会问三个问题：

1. **代码执行位置**：Agent 的代码在哪里运行？
2. **凭证管理**：Agent 能访问哪些 API key 和凭据？
3. **审计追溯**：Agent 的所有操作是否有完整日志？

在云托管模式下，这三个问题的答案都不在企业控制范围内。Orchestration 和 Execution 都在 Anthropic 的基础设施上，企业只能通过 API 调用和日志有限的可见性来管控风险。

Self-Hosted Sandboxes 的发布就是为了解决这个问题——但需要注意的是，它的解法是**有选择地将执行层移入企业边界**，而不是将整个 Agent 搬进企业网络。这是一个经过深思熟虑的架构决策。

---

## 二、架构解剖：双平面设计

理解 Self-Hosted Sandboxes 的关键，是掌握它的双平面架构：

### 2.1 Orchestration Plane（编排平面）— 留在 Anthropic

- Agent 的行为决策（使用哪个 Tool、如何规划步骤）
- Session 路由和状态管理
- Claude 模型本身

**这部分不进入企业边界。** 这意味着企业不需要在防火墙内运行任何 LLM 推理基础设施，同时仍然利用 Anthropic 的 Agent 能力。

### 2.2 Execution Plane（执行平面）— 进入企业基础设施

- 代码执行（Tool Call 的实际运行环境）
- 文件系统操作
- 网络出口流量

企业可以选择在容器、VM 或 Serverless 环境中运行这个执行层。

Anthropic 官方文档中的定义非常精确：

> "Self-hosted sandboxes move tool execution into infrastructure you control, so the agent's code, filesystem, and network egress never leave your environment."

笔者认为这个表述的关键在于**"tool execution"**——不是整个 Agent，而是 Agent 调用工具时的那部分操作。这是一种精确的能力解耦，而不是笼统的"本地部署"。

### 2.3 Environment Worker：企业侧的Agent执行代理

企业侧运行的核心组件是 **Environment Worker**。它是 Anthropic 提供的轻量级代理，运行在企业基础设施内，负责：

1. 从 Anthropic 的 Session Queue 中认领任务
2. 为每个 Session 生成隔离的执行上下文（容器/VM/Serverless）
3. 下载 Agent 的 Skills 到 `/workspace/skills/<name>/`
4. 本地执行 Tool Calls
5. 将结果返回到 Managed Agents 队列

Worker 接收 5 个环境变量用于身份认证：`ANTHROPIC_SESSION_ID`、`ANTHROPIC_ENVIRONMENT_KEY`、`ANTHROPIC_WORK_ID`、`ANTHROPIC_ENVIRONMENT_ID`、`ANTHROPIC_BASE_URL`。这些 token 是每个隔离 Session 的身份凭证，Anthropic 明确要求**不要在 Session 间共享这些凭证**。

Worker 支持两种调度模式：
- **Always-on Worker**：持续轮询 Session 队列，适用于高吞吐、低延迟需求的场景
- **Webhook-triggered Worker**：通过 `session.status_run_started` 事件触发唤醒，适用于成本敏感或突发性工作负载

Worker 的健康检查机制是 30 秒窗口——如果一个 Worker 超过 30 秒没有轮询，它会被标记为不健康。

---

## 三、MCP Tunnels：私有网络的零信任接入

MCP Tunnels 是与 Self-Hosted Sandboxes 配套发布的功能，用于解决一个非常具体的问题：**如何在不打开入站防火墙端口、不暴露服务到公网、不将 Anthropic IP 加入白名单的情况下，让 Agent 访问企业私有网络内的 MCP 服务器？**

答案是** outbound-only + Cloudflare 隧道 + 三层加密**。

### 架构原理

MCP Tunnels 通过 `cloudflared` 在企业基础设施和 Cloudflare Edge 之间建立持久隧道。连接方向始终是从企业侧向 Cloudflare Edge 发起（outbound-only），这意味着：

- 企业**不需要**在防火墙开放任何入站端口
- 企业**不需要**将任何服务暴露到公网
- Anthropic 的基础设施**不需要**加入企业的 IP 白名单

Anthropic 官方描述：

> "Outbound-only connection, so you don't need to open inbound firewall ports, expose services to the public internet, or allowlist Anthropic's IP ranges."

### 三层加密

MCP Tunnels 实现了三层加密架构：
1. **外层 mTLS**：Cloudflare 与企业侧之间的双向认证
2. **内层 TLS**：Claude 到 MCP 服务器的传输加密
3. **OAuth per MCP Server**：每个 MCP 服务器独立的 OAuth 认证

这个设计将 MCP 服务器的认证责任从企业网络的防火墙规则转移到了应用层协议本身，是一种更精细的安全边界设计。

**关键限制**：MCP Tunnels 依赖 Cloudflare 基础设施（需要 TCP/UDP port 7844 到 Cloudflare edge range `198.41.192.0/19`），且目前是 **Research Preview** 阶段，Anthropic 明确表示没有可用性承诺。

---

## 四、七种生产部署模式

Digital Applied 的深度分析文章提取了七种基于 Anthropic 官方文档的生产模式，按成熟度分级：

### Pattern 1：容器隔离 + 镜像固定（Container Isolation）

每个 Agent Session 运行在独立容器中，镜像通过 SHA digest 固定（而非 `:latest` mutable tag）。Anthropic 官方提供了基于 Docker + gVisor/Firecracker 的加固配方。

**关键警告**：镜像固定是企业的责任，Managed Agents 平台不强制要求 digest pinning。生产环境必须通过 SHA digest 引用镜像，否则供应链攻击可以无声地改变 Agent 运行时。

### Pattern 2：只读根文件系统 + 网络隔离

容器的 root 文件系统设为只读，网络 egress 完全禁止或严格限定。这是 Agent 运行的最保守安全配置。

### Pattern 3：Webhook-triggered Worker（成本优化模式）

不维持 Always-on Worker，而是通过 Webhook 按需唤醒。这样只在实际有任务时才付费，但会增加 Session 启动延迟（冷启动开销）。

### Pattern 4：多云/多区域弹性部署

通过在多个云服务商的容器环境中运行 Worker，实现故障域隔离。Anthropic 目前支持 Cloudflare、Daytona、Modal 和 Vercel 四家合作伙伴。

### Pattern 5：Vercel Sandbox 凭证代理

Vercel Sandbox 提供了独特的**凭证代理（Credential Brokering）**机制——Agent 使用的环境密钥从不进入 VM，而是通过 Vercel 的代理层转发。这将密钥的暴露面从 VM 级别降到了 Vercel 托管层。

### Pattern 6：gVisor/Firecracker 深度隔离

对于需要比 Docker namespace 隔离更强的场景，Anthropic 文档支持 gVisor（用户空间 syscall 拦截，CPU 密集型任务零开销，但 I/O 密集型任务有 2-200x 开销）和 Firecracker（微虚拟机，接近物理机性能但启动时间更长）。

### Pattern 7：混合编排模式

某些高敏感 Tool 在 Self-Hosted Sandbox 执行，非敏感 Tool 回退到云端 Anthroic 托管执行。这需要精细的 Tool 路由逻辑。

---

## 五、当前限制与已知差距

笔者认为，Anthropic 在发布这两个功能时的诚实态度值得肯定——他们在官方文档中明确披露了两个关键限制，而这些限制在很多发布报道中被忽略了：

### 限制一：AWS 上不可用

Self-Hosted Sandboxes **目前不支持 AWS 上的 Claude Platform**。对于已经深度使用 AWS 的企业来说，这个功能暂时无法使用。这是一个现实的企业采纳障碍。

### 限制二：不支持 Memory

在云托管模式下，Claude Managed Agents 支持跨 Session 的 Memory 功能（Agent 可以记住上一次会话中学到的内容）。但在 Self-Hosted Sandbox 模式下，这个功能**尚不支持**。

这意味着如果你的 Agent 工作流依赖长期记忆能力，切换到 Self-Hosted Sandbox 会导致功能降级。对于需要长周期任务的场景，这是一个重大权衡因素。

### 限制三：MCP Tunnels 是 Research Preview

没有 SLA 可用性承诺。在生产环境中依赖这个功能需要额外的风险评估。

---

## 六、工程判断

笔者认为，Self-Hosted Sandboxes 和 MCP Tunnels 的组合，代表了企业 Agent 基础设施的一个**有原则的设计选择**：不是在安全性和能力之间二选一，而是通过精确的平面解耦，让企业可以只把最敏感的部分留在自己的基础设施内。

这个架构判断的工程价值在于：**它将企业安全的复杂度从"如何部署一个完整的本地 Agent"降到了"如何配置一个工作负载引用的容器运行时"。** 企业安全团队不需要理解 Agent 的内部机制，只需要维护一个符合安全基线的执行环境。

但这个方案也有它的适用边界：
- **强数据主权要求**（数据完全不能出企业边界）：目前方案不满足，Orchestration 平面仍在 Anthropic
- **需要跨 Session 记忆的长任务**：当前不支持 Memory，需要等待官方支持
- **已深度集成 AWS 的企业**：当前不支持 AWS 部署

对于这些边界情况下的企业，或者对安全要求极高的金融、医疗行业，这个方案目前还不能完全替代自托管的 Agent 部署方案。

---

## 七、SaaS + 企业侧执行：新的范式

笔者认为，Self-Hosted Sandboxes 最重要的意义不是它本身的功能，而是它代表的一种架构方向：**SaaS 化的 Agent 智能 + 本地化的执行控制。**

这与传统的"要么全云、要么全本地"二选一思路不同。它允许企业在一个粒度级别（Execution Plane）做出安全决策，同时在另一个粒度级别（Orchestration Plane）利用 SaaS 的敏捷性。

这种分离式架构，与 Kubernetes 将 orchestration 和 workload 分离的设计思路一脉相承。它预示着企业 Agent 基础设施的未来方向：**不是重新发明轮子，而是通过清晰的平面边界，让不同专业团队负责不同层次的安全和运维。**

Anthropic 能否在未来版本中把 Memory 支持也带入 Self-Hosted 模式，以及是否会在 AWS 上推出支持，将是决定这个方案能否覆盖更广泛企业场景的关键。
