# Microsandbox：每个 Agent 都值得拥有自己的计算机

> 本文推荐 superradcompany/microsandbox：一个用 Rust 编写的轻量级 microVM 沙箱框架，100ms 内启动，支持 Rust/Python/TypeScript/Go 多语言 SDK，为 AI Agent 提供硬件级隔离。

## 解决什么问题

当你在生产环境中运行 AI coding agent 时，最大的安全焦虑来自哪里？

不是模型幻觉，不是 prompt 注入，而是 **agent 拿着你的用户权限在真实系统上执行命令**。Git commit、npm install、curl 外传数据——这些操作如果不受限制，后果不堪设想。

Microsandbox 的核心价值主张：**让每个 agent 都运行在独立的轻量级虚拟机中，物理隔离，无可穿透。**

> "every agent deserves its own computer"

## 为什么选 microVM 而不是容器

Docker 容器共享宿主机内核， namespace 逃逸和容器逃逸漏洞历史悠久。microVM 提供了：

- **硬件级虚拟化**：每个沙箱是独立的虚拟机，没有共享内核风险
- **比容器更快的启动**：平均 <100ms（使用 libkrun 实现）
- **比 VM 轻量得多**：保留了容器的速度和资源效率

关键区别在于 threat model：如果你的 agent 可能被恶意 prompt 注入诱导执行危险操作，容器的隔离等级不够。MicroVM 是认真的沙箱，而不是「社区级隔离」。

## 核心能力一览

| 特性 | 说明 |
|------|------|
| **启动速度** | 平均 <100ms |
| **隔离级别** | Hardware-level microVM（libkrun） |
| **SDK 多语言** | Rust / Python / TypeScript / Go |
| **镜像兼容** | OCI 标准镜像（Docker Hub、GHCR、私有 registry）|
| **Secret 保护** | 密钥永不进入 VM，无法被提取 |
| **长会话支持** | 支持 detached 模式，适合 long-running agent 会话 |
| **Agent 集成** | 原生 Agent Skills + MCP Server |

## 代码体验

```rust
use microsandbox::Sandbox;

let sandbox = Sandbox::builder("my-sandbox")
    .image("python")
    .cpus(1)
    .memory(512)
    .create()
    .await?;

let output = sandbox
    .exec("python", ["-c", "print('Hello from a microVM!')"])
    .await?;

println!("{}", output.stdout()?);
sandbox.stop_and_wait().await?;
```

5 行代码，一个完全隔离的 Python 执行环境。对 agent harness 开发者来说，这意味着：

- 可以给每个 task 分配独立沙箱
- 可以限制网络访问（通过 VM 的网络栈）
- 可以挂载特定目录为只读
- 沙箱崩溃不影响主进程

## Agent-Ready 设计

Microsandbox 专门面向 AI agent 场景提供了两个集成点：

**Agent Skills**：一键安装到 Claude Code、Cursor、Codex、Gemini CLI、GitHub Copilot 等主流 coding agent。安装后 agent 自动获得 `msb` 命令能力，可以自己创建和管理沙箱。

```sh
npx skills add superradcompany/skills
```

**MCP Server**：通过 MCP 协议暴露沙箱操作能力，连接任何 MCP-compatible agent：

```sh
claude mcp add --transport stdio microsandbox -- npx -y microsandbox-mcp
```

这是笔者见过的最干净的 agent-native 沙箱集成方案——不是让人类配置沙箱规则，而是让 agent 学会自己用沙箱。

## 和 OpenAI Codex Windows 沙箱的对比

有趣的是，OpenAI 在 Codex Windows 实现中遇到了和 Microsandbox 完全不同的工程挑战：

| 维度 | OpenAI Codex | Microsandbox |
|------|-------------|--------------|
| 平台 | Windows | Linux/macOS (Apple Silicon) |
| 隔离实现 | Write-restricted token + synthetic SID | microVM (libkrun) |
| 网络隔离 | Windows Firewall（elevated 模式）| VM 网络栈 |
| 初始约束 | 不想要求 admin 权限 | 本身需要 KVM/HVF |
| 最终方案 | 引入专用 Windows 账户 | 本地 microVM |

OpenAI 的困境本质是：Windows 没有提供足够灵活的进程级隔离原语，所以被迫引入账户体系。而 Microsandbox 在 Linux/macOS 上可以直接使用 KVM/HVF，绕过了这个问题。

这也说明了为什么 Windows 上做 agent 沙箱比 Linux/macOS 复杂得多。

## 适用场景

**适合用 Microsandbox 的场景**：
- 在服务器端运行 untrusted agent code（代码评审、自动化测试）
- Agent 执行敏感操作（数据库迁移、文件删除）前先在沙箱验证
- 多 agent 并行执行，每个 agent 独立隔离
- 运行用户提交的代码片段

**不适合的场景**：
- Windows 环境（当前不支持）
- 需要 GPU 加速的工作负载
- 对启动延迟极其敏感（<10ms）的场景

## 竞品参考

| 项目 | 方向 | Stars |
|------|------|-------|
| [superradcompany/microsandbox](https://github.com/superradcompany/microsandbox) | microVM 沙箱，Agent-Ready | 6106 |
| [kubernetes-sigs/agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) | K8s 容器隔离方案 | - |
| [romanklis/openclaw-contained](https://github.com/romanklis/openclaw-contained) | gVisor 沙箱，TaskForge 使用 | 28 |

## 原文引用

> "Microsandbox spins up lightweight VMs in milliseconds from our SDKs. Runs locally on your machine. No server to set up. No lingering daemon. It is all embedded and rootless!"
>
> — [Microsandbox README](https://github.com/superradcompany/microsandbox)

> "Hardware-Level Isolation: Hardware-level isolation with microVM technology."
>
> — [Microsandbox README](https://github.com/superradcompany/microsandbox)

---

**Stars**: 6,106 | **Language**: Rust | **License**: Apache 2.0 | **Backed by Y Combinator**

**Related Article**: [OpenAI Codex Windows 沙箱架构](/articles/harness/openai-codex-windows-sandbox-architecture-2026.md)

**Tags**: #sandbox #microvm #rust #agent-harness #security #multi-language-sdk