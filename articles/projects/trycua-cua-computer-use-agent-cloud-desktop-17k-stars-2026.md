# trycua/cua：把云端桌面变成 Agent 的「标准操作界面」

> 当你的 Agent 需要控制一台真实桌面时，你还用 EC2 实例管理它吗？

---

## 核心命题

**CUA** 解决了一个正在爆发的问题：AI Agent 开始需要控制真实桌面（不只是终端），但现有的云端基础设施（EC2、VM）是为人设计的，不是为 Agent 设计的。

CUA 的解法是：**给每个 Agent 一个专属的云端桌面，里面有它需要的一切工具，而且 Agent 可以完全控制**。

这句话听起来简单，但它重新定义了「Harness 环境」的边界。

---

## 为什么这值得关注

### 1. Computer Use Agent 正在爆发

Cursor 的官方博客（2026年4月）专门描述了 Computer Use 在他们云端 Agent 中的角色：

> Cloud agents also need different kinds of prompts in the harness than local agents do. We encourage them to be more autonomous, because the cost of blocking is much higher. Locally, you know when an agent has stopped and is waiting for permission, but in the cloud, it could sit there for hours before you go back and check on it. Cloud agent harness has a dedicated subagent type for computer use, with its own model routing, custom prompting, and screen recording. The VNC and Chrome belong to the environment, which is shared between the parent agent and the subagent.

Cursor 在这里透露了一个关键信息：**他们的 Cloud Agent Harness 有一个专门的 Computer Use 子 Agent 类型，有自己的模型路由、定制提示和屏幕录制**。

但 Cursor 没有解决的是：这个 Computer Use Agent 在哪个环境里跑？Cursor 的答案是「共享 VNC 和 Chrome」，但这不够。

CUA 解决的是：给每个 Computer Use Agent 一个完整的、可配置的云端桌面 OS。

### 2. Harness 与基础设施的边界正在模糊

我在上一篇文章里（Anthropic vs OpenAI：两种 Harness 迭代哲学的本质差异）描述了顶级 Agent 团队正在把 Harness 从「模型配件」升级为「基础设施层」。

CUA 是这个趋势的具体化：**Harness 设计已经不只是在 prompt 和 tool 配置层面，而是到了 OS 层面**。

当你需要你的 Agent 控制一台 macOS 虚拟机去测试你的 iOS 应用时，你需要的不只是 EC2 instance，你需要的是一个专为 Agent 控制设计的桌面环境——有屏幕、有输入、有持久化状态、有快照机制。

CUA 就是这个。

---

## 核心能力

### Sandboxes：云端多系统桌面

CUA 支持 Linux、Windows、macOS、Android 的云端沙箱。每个沙箱有：
- 真实显示（VNC 可视化）
- 浏览器（Chrome）
- root/bash 访问
- 启动时间 < 1 秒

```bash
# 启动一个 Ubuntu 桌面
cua sb launch ubuntu

# 打开一个实时 GUI 会话
cua sb vnc curious-fox-123

# 控制鼠标、键盘、bash
cua sb shell curious-fox-123
```

这个命令行接口设计很有意思：**它把「云端桌面」当作一个可以命令行操作的对象**，而不是一个需要手动管理的远程机器。

### Snapshots：环境快照与分叉

你可以配置环境、安装依赖，然后快照保存。之后可以瞬间分叉出多个并行实例。

```bash
# 配置你的环境
# 安装依赖...
# 快照保存
cua sb snapshot my-dev-env

# 分叉出并行测试
cua sb fork my-dev-env --count 10
```

### Cua-Bench：真实桌面评测

提供跨 macOS、Linux、Windows、Android 的预建任务评测。对比不同模型在真实桌面环境中的表现。

```python
# 使用 Cua Python SDK 运行评测
from cua import Agent, Task

agent = Agent(model="claude-sonnet-4-20250514")
task = Task(description="Send a message in #general on Slack")

result = agent.run(task, sandbox="linux-chrome")
print(result.success, result.reward)
```

### 训练数据管道

录 Agent 会话，精选最佳运行，直接喂入训练流程。

```bash
# 录制会话
cua rec start --sandbox ubuntu-dev

# 录制完成后，标注并导出
cua rec export --filter "success==true" --format "rl-trainset"
```

---

## 技术架构

CUA 的架构分为三层：

| 层级 | 组件 | 说明 |
|------|------|------|
| **Sandbox** | Linux/Windows/macOS/Android VMs | Agent 的运行环境 |
| **Agent Runtime** | Claude/Gemini/Qwen/UI-TARS | 可以组合本地 grounding 模型 + 云端 planner |
| **Eval & Training** | Cua-Bench / RL Dataloader | 评测和训练数据生成 |

**Lume** 是他们面向 macOS 原生的方案：Apple Silicon 上的本地沙箱，接近原生速度，headless 模式，MIT 许可。

---

## 与 Claude Code / Cursor 的关系

CUA 的官网直接写了：

> Built for Claude Code, Codex, OpenClaw, and computer-use agents.

这不是一句营销话。

在 Claude Code 的语境下，当你需要你的 Agent 在一个完整的 macOS 桌面环境里运行时（测试你的 macOS 应用、操作真实 UI），CUA 提供了开箱即用的云端 macOS 沙箱。

在 Cursor Cloud Agent 的语境下，CUA 解决的是「计算机使用子 Agent」的基础设施问题——每个 Computer Use Agent 需要一个独立的、可配置的云端桌面，而不是共享一个 VNC session。

---

## 适用场景

| 场景 | CUA 能做什么 |
|------|------------|
| **iOS/macOS 应用测试** | Agent 控制真实的 macOS 沙箱，安装 Xcode，运行测试 |
| **多平台 UI 测试** | Linux + Windows + macOS 并行跑同一套测试 |
| **Computer Use 评测** | 在真实桌面环境里评测 Agent 的 computer use 能力 |
| **RL 训练数据收集** | 录制大量 Agent 与桌面交互的 session，精选后训练 |
| **复杂 Web 自动化** | Agent 控制真实浏览器，操作真实 Web 应用 |

---

## 快速上手

```bash
# 安装 CLI
npm install -g @trycua/cli

# 启动一个 Linux 桌面
cua sb launch ubuntu

# 在 Claude Code 里连接
claude mcp add cua -- npx @trycua/cua-mcp

# 开始控制
cua sb vnc <your-sandbox-id>
```

---

## 引用来源

1. CUA 官网: https://cua.ai/
2. GitHub Repository: https://github.com/trycua/cua
3. Cursor Research: *What we've learned building cloud agents* — Computer Use subagent type (https://cursor.com/blog/cloud-agent-lessons)

---

*本文为 Round 89 产出 | Project 关联 Article：Anthropic vs OpenAI：两种 Harness 迭代哲学的本质差异（系统级 Harness 设计 ↔ cua 的云端桌面基础设施 → 理论层 + 基础设施层互补闭环）*