# omnigent-ai/omnigent：跨平台 Meta-Harness，让 Claude Code / Codex / Pi 共享防护层

> 标签：`harness` `multi-agent` `sandbox` `policies`
> Stars：265（2026-06-11，Apache-2.0）

---

## 核心命题

Omnigent 做了一件看似简单、实则深刻的事：**把 Claude Code、Codex、Pi 和自定义 Agent 放在同一个 Session 里跑，用同一套 Policy 管控它们**。

这不是又一个 Agent 框架——这是一个**跨运行时 Harness 抽象层**。用 Omnigent 官方的话说：

> "A meta-harness for all your AI agents. Omnigent provides a common layer over Claude Code, Codex, Pi, and the agents you write yourself: swap or combine harnesses without rewriting, keep them in check with policies and sandboxing."

---

## 为什么这个方向值得关注

### 痛点一：每个 Agent 运行时都有自己的 Harness，互不兼容

Claude Code 有自己的安全策略，Codex 有自己的沙箱，Pi 有自己的行为控制——如果你想在同一个任务中让三个 Agent 协作，要么写胶水代码，要么放弃协作。

Omnigent 的解法是**把 Harness 抽成独立层**：不修改底层 Agent，只在它们上面加一个协调层。

### 痛点二：Agent 工作状态无法跨设备延续

开发者经常遇到这个问题：在笔记本上开始一个 Agent 任务，出门后只能在手机上干瞪眼。Omnigent 的 Session 设计让**消息、子 Agent、终端、文件状态跨设备同步**——笔记本 → 浏览器 → 手机，工作无缝衔接。

### 痛点三：多 Agent 协作时缺乏统一 Policy

当一个任务跑多个 Agent，如果其中一个开始执行高风险操作（比如写入生产数据库），没有一个统一入口来拦截。

Omnigent 的 Policy 机制支持**三级粒度**：全局策略、单 Agent 策略、单会话策略。可以在整个服务范围设置「写入 /tmp 以外目录需要审批」，也可以对某个特定 Agent 单独放开。

---

## 核心能力解析

### 1. 多 Agent 实时协作（Multi-Agent Supervision）

```bash
# 启动一个 orchestrator，可以同时跑多个 Agent
omnigent run examples/polly/    # Agent A
omnigent run examples/debby/    # Agent B
# 在同一个 Session 里，Agent A 可以让 Agent B 审查它的输出
```

关键设计：**每个 Agent 保持自己的 Harness 运行时**（polly 用 Claude Code，debby 用 Codex），但协调发生在 Omnigent 层。

### 2. Policy 管控

Omnigent 的 Policy 分三层：

| 粒度 | 例子 |
|------|------|
| **全局** | 所有 Agent 禁止访问外部网络 |
| **单 Agent** | Codex Agent 禁止执行 shell 命令 |
| **单会话** | 当前 Session 需要人工审批所有文件写入 |

> "Govern your agents. Create policies to pause for your approval before risky actions, cap spend, or limit which tools an agent reaches."

### 3. 云沙箱执行（Cloud Sandboxes）

Omnigent 支持将 Agent 跑在云沙箱中，而不是本地：

- **Modal** 和 **Daytona** 已被官方支持
- 沙箱按需创建、隔离销毁
- 从 CLI 启动，或由服务器端按 Session 动态配置

### 4. 跨设备 Session 同步

Omnigent 提供：
- 本地 Web UI（`localhost:6767`）
- macOS 桌面 App（含 OS 通知和 Dock badge）
- Session 状态（消息、文件、终端、Agent 进度）在所有端点同步

---

## 技术架构

Omnigent 的架构核心是 **Manifest + Harness 分离**：

- **Manifest**：声明式描述 Agent 的 workspace（输入路径、输出路径、依赖、环境）
- **Harness**：实际执行环境（本地 tmux、云沙箱 Modal/Daytona）
- **Orchestrator**：Session 协调层，负责多 Agent 通信和 Policy 执行

```
┌─────────────────────────────────────────┐
│         Omnigent Orchestrator           │
│  (Session 协调 + Policy 执行 + 状态同步)  │
├──────────┬──────────┬──────────────────┤
│ Claude   │ Codex    │ Pi / Custom YAML  │
│ Code     │ Harness  │ Agent            │
│ Harness │          │                  │
├──────────┴──────────┴──────────────────┤
│  Local tmux │ Modal │ Daytona          │
│  (Sandbox Providers)                   │
└─────────────────────────────────────────┘
```

---

## 安装与快速开始

```bash
# 一键安装（macOS/Linux）
curl -fsSL https://raw.githubusercontent.com/omnigent-ai/omnigent/main/scripts/install_oss.sh | sh

# 或用 uv
uv tool install omnigent

# 启动默认 Agent（自动选择模型和凭证）
omnigent

# 指定特定 Agent 运行时
omnigent claude   # Claude Code
omnigent codex    # Codex
```

**依赖**：Python 3.12+、Node.js 22 LTS、tmux

---

## 笔者的判断

Omnigent 最有价值的地方不是任何一个单点功能，而是**它重新定义了什么叫做「Agent 的 Harness」**。

传统认知里，Harness 是绑定特定 Agent 运行时的（比如 Cursor 的 Allowlist、Claude Code 的 Sandbox）。Omnigent 证明了一件事：**Harness 可以是一个独立抽象层**，不关心底下跑的是 Claude Code 还是 Codex，只要它们遵循同一个 Manifest 契约。

这个方向的工程意义是：未来你可以为不同任务选择最合适的 Agent 运行时，但用同一套 Policy、同一套监控、同一套 Session 管理它们。这才是真正的**Agent 编排层**该有的样子。

目前还是 alpha 状态，API 和 Plugin 系统尚未完全开放——但方向值得持续追踪。

---

## 关联文章

- [OpenAI Agents SDK：用 Harness 思维重新定义 Agent 执行边界](/articles/harness/openai-agents-sdk-harness-sandbox-checkpoint-separation-2026.md)

---

*来源：[Omnigent GitHub README](https://github.com/omnigent-ai/omnigent)*