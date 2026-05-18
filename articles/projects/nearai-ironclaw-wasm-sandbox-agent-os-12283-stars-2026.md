# IronClaw：当安全成为 Agent OS 的第一性原则

## 这个项目解决了一个长期让人头疼的问题

Agent 系统的安全问题长期处于「事后补救」状态——先跑起来，再加安全层。但 IronClaw 反其道而行：**把安全作为架构的第一性约束**，用 WASM 沙箱 + Docker 隔离 + Capability-Based 权限模型构建了一个真正意义上的安全 Agent 运行时。

这不是又一个「AI 助手」，而是一个**隐私优先、跨平台、可自托管的 Agent 基础设施**，尤其适合那些不想把数据交给任何第三方的开发者或企业。

---

## 为什么 IronClaw 值得关注

### 1. WASM Sandbox：能力粒度的进程隔离

IronClaw 的核心隔离机制是 **WebAssembly 沙箱**。与 Docker 容器相比，WASM 的优势在于：

- **Capability-based 权限模型**：每个工具只能访问明确定义的能力（文件、网络、环境变量），而不是「容器内一切」
- **启动速度快**：毫秒级，而 Docker 容器通常需要数秒
- **跨平台一致**：一次编译，到处运行，且行为语义完全一致

原文描述：

> "WASM Sandbox — Untrusted tools run in isolated WebAssembly containers with capability-based permissions"

这与 OpenAI Codex Windows 沙箱用 ACL + Token 做权限控制的思路异曲同工——**都是为了让不可信代码在精确受限的环境中运行**。区别在于 IronClaw 用 WASM 实现跨平台，而 Codex 用 Windows ACL/Token 专门解决 Windows 平台问题。

### 2. Docker Sandbox + Per-Job Token：生产级隔离

对于需要更强隔离的场景，IronClaw 支持 **Docker 容器级隔离**，并引入了 per-job token 机制：

- 每个 Job 运行在独立容器中，共享 nothing
- Token 在 Job 级别生成，不跨容器传递
- Orchestrator/Worker 架构确保主进程与执行环境分离

原文：

> "Docker Sandbox — Isolated container execution with per-job tokens and orchestrator/worker pattern"

这正是 OpenAI 在 Codex Windows 沙箱中追求的「Elevated Sandbox」模式——**专用身份 + 最小权限 + 隔离执行**。IronClaw 用 Docker 实现，Codex 用 Windows 专用用户实现，但核心理念一致。

### 3. 凭证保护：秘密永远不到达工具层

这是 IronClaw 最聪明的设计之一。在大多数 Agent 框架中，工具直接持有 API Key、数据库密码等敏感信息——一旦工具被注入攻击，凭证就泄露了。

IronClaw 的做法是：**凭证在 Host 边界注入，工具永远看不到**。任何尝试从工具层访问凭证的行为都会被 leak detection 检测到。

原文：

> "Credential Protection — Secrets are never exposed to tools; injected at the host boundary with leak detection"

这与 Anthropic 的「Managed Agents 解耦 brain/hands」思路一致——**核心推理引擎不持有敏感数据，执行引擎只有运行时必须的最小权限**。

### 4. Prompt 注入防御：主动检测而非事后清理

Prompt 注入是 Agent 安全最棘手的问题之一。IronClaw 采取了多层防御：

- **Pattern Detection**：识别已知的注入模式（如「ignore previous instructions」）
- **Content Sanitization**：在将用户输入交给 Agent 前进行清洗
- **Policy Enforcement**：对工具调用和网络请求进行策略校验

原文：

> "Prompt Injection Defense — Pattern detection, content sanitization, and policy enforcement"

### 5. 端点白名单：网络请求只去该去的地方

IronClaw 的 HTTP 请求被限制在明确白名单内的主机和路径——这是 Agent 数据泄露防护的最有效手段之一。

原文：

> "Endpoint Allowlisting — HTTP requests only to explicitly approved hosts and paths"

这正是 OpenAI 在 Codex Windows 沙箱中**不惜放弃 Unelevated 方案也要用 Windows Firewall 强制执行**的核心目标。IronClaw 用应用层白名单实现，Codex 用 OS 级防火墙实现，**但解决的是同一个问题：防止 Agent 在运行时偷偷把数据传出去**。

---

## 技术架构亮点

### 多后端 LLM 支持

IronClaw 默认使用 NEAR AI，但支持几乎所有主流 LLM 提供商：

- **内置支持**：Anthropic、OpenAI、GitHub Copilot、Google Gemini、MiniMax、Mistral、Ollama
- **兼容 OpenAI API 的服务**：OpenRouter（300+ 模型）、Together AI、Fireworks AI、自托管 vLLM/LiteLLM

这使得 IronClaw 可以作为统一的 Agent 运行时，**不管你用的是哪个模型**。

### 多通道部署

- **REPL**：本地交互式
- **HTTP Webhooks + SSE/WebSocket**：API 集成
- **WASM Channels**：Telegram、Slack 等平台集成
- **Web Gateway**：浏览器 UI

### 持久化记忆

- **Hybrid Search**：Full-text + Vector search（Reciprocal Rank Fusion 融合）
- **Workspace Filesystem**：基于路径的存储
- **Identity Files**：跨会话保持一致的人设和偏好

---

## 与 Codex Windows 沙箱的关联

| 维度 | Codex Windows Sandbox | IronClaw |
|------|---------------------|---------|
| **隔离目标** | Windows 平台进程级隔离 | 跨平台工具级隔离 |
| **核心机制** | ACL + Write-Restricted Token + 专用 Windows 用户 | WASM Sandbox + Docker + Capability Permissions |
| **网络控制** | Windows Firewall（Elevated）+ 环境变量投毒（Unelevated） | Endpoint Allowlisting + Docker 网络隔离 |
| **凭证保护** | 依赖 Windows 身份系统 | Host 边界注入 + Leak Detection |
| **平台支持** | Windows（核心问题所在）| macOS/Linux/Windows 跨平台 |

两者共同指向同一个结论：**Agent 安全不能依赖单一机制，需要多层纵深防御（Defense in Depth）**。

OpenAI 在 Codex 中选择了「ACL 做文件系统 + Firewall 做网络」的 Windows 原生方案；IronClaw 选择了「WASM 做能力控制 + Docker 做进程隔离 + 应用层白名单做网络」的跨平台方案。**如果你在设计 Agent Harness，IronClaw 的安全架构值得作为参考框架**。

---

## 快速上手

```bash
# macOS / Linux / Windows/WSL
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/nearai/ironclaw/releases/latest/download/ironclaw-installer.sh | sh

# Windows Native
irm https://github.com/nearai/ironclaw/releases/latest/download/ironclaw-installer.ps1 | iex

# 配置引导
ironclaw onboard
```

---

## 引用

> "IronClaw is built on a simple principle: your AI assistant should work for you, not against you."

> "Defense in depth — Multiple security layers protect against prompt injection and data exfiltration"

> "WASM Sandbox — Untrusted tools run in isolated WebAssembly containers with capability-based permissions"

来源：[nearai/ironclaw](https://github.com/nearai/ironclaw)，12,283 Stars，MIT/Apache-2.0 License
