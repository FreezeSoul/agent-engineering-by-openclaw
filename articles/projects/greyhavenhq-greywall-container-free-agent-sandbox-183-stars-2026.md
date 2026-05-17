# Greywall：容器无关的内核级 Agent 沙箱

> **核心结论**：Greywall 是第一个无需 Docker/容器即可实现内核级隔离的 Agent 沙箱方案，用 Landlock + Seccomp BPF + eBPF 在 Linux/macOS 上构建五层安全防护。配合 GreyProxy 透明代理，可以实现"工作目录外一切皆拒"的最小权限原则。对 Claude Code、Cursor、Codex 等主流 Agent 开箱即用。

---

## 这个项目解决什么问题

Claude Code、Cursor、Codex 等 AI 编码 Agent 在你的开发环境中拥有相当高的权限——读取文件、执行命令、访问网络。问题是：**它们默认可以访问 SSH keys、环境变量、home 目录等敏感区域**。

大多数现有解决方案依赖 Docker 容器来隔离，但这带来几个痛点：
- **资源开销大**：每个容器都要占用额外资源
- **配置复杂**：需要写 Dockerfile、维护镜像
- **与本地工作流冲突**：在容器中运行 Agent，打破了原有的编辑器/终端集成

Greywall 的核心价值主张：**容器无关的内核级隔离，无需 Docker 开销**，开箱即用地支持 Claude Code、Cursor、Codex、Aider、Goose、Gemini、OpenCode、Amp、Cline、Copilot 等主流 Agent。

---

## 技术原理：五层内核级防护

Greywall 在 Linux 上构建了五层安全架构：

| 层级 | 技术 | 作用 |
|------|------|------|
| **文件系统** | Bubblewrap (user namespaces) | 仅允许访问工作目录，其他路径默认拒绝 |
| **文件系统（高级）** | Landlock | 内核级强制文件系统策略，比 Bubblewrap 更细粒度 |
| **系统调用** | Seccomp BPF | 限制允许的系统调用，防止特权操作 |
| **监控** | eBPF | 实时追踪 Agent 行为，捕获异常 |
| **网络** | TUN-based capture | 透明流量抓取，配合 GreyProxy 实现网络隔离 |

### --learning 模式：自动生成最小权限配置

Greywall 有一个智能的 `--learning` 模式：

```bash
greywall --learning -- opencode
```

学习模式会追踪命令实际需要的文件系统访问和系统调用，然后**自动生成最小权限配置文件**。你不需要手动配置权限，Greywall 会通过观察告诉你"这个 Agent 实际需要访问哪些路径"。

### GreyProxy：网络隔离的透明代理

GreyProxy 是 Greywall 的配套组件，是一个"默认拒绝的透明代理"：

- 所有网络流量默认被阻止
- Agent 需要时可以通过 `--proxy socks5://localhost:1080` 显式放行特定流量
- 提供实时仪表板，可查看哪些连接被允许/拒绝

```bash
# 阻止所有网络
greywall -- claude

# 通过 SOCKS5 代理放行 npm install
greywall --proxy socks5://localhost:1080 -- npm install
```

---

## 关键特性

- **Deny-by-default 文件系统**：只有工作目录可访问，除非你显式允许更多
- **网络隔离**：所有流量被阻止或通过 GreyProxy 路由，带实时仪表板
- **危险命令阻止**：如 `rm -rf /` 和 `git push --force` 被默认拒绝
- **内置 Agent profiles**：一条命令为 Claude Code、Cursor、Codex 等设置沙箱
- **学习模式**：追踪并自动生成最小权限配置
- **无需容器**：内核级沙箱，不需要 Docker 开销

### 支持平台

- **macOS**：通过 syscall 过滤实现
- **Linux**：Bubblewrap + Landlock + Seccomp BPF + eBPF 五层防护
- **依赖**：Bubblewrap、socat（必需）；xdg-dbus-proxy、libsecret-tools（可选）

---

## 使用示例

```bash
# 用网络和文件系统默认拒绝的方式沙箱化一个命令
greywall -- curl https://example.com

# 用内置 profile 沙箱化 Claude Code
greywall -- claude

# 学习命令需要什么文件系统访问，然后自动生成最小权限配置
greywall --learning -- opencode

# 阻止危险命令
greywall -c "rm -rf /"  # → 被命令拒绝规则阻止
```

---

## 与主流替代品的对比

| 特性 | Greywall | microsandbox | Docker 隔离 |
|------|----------|--------------|-------------|
| 容器依赖 | ❌ 无 | ❌ 无 | ✅ 需要 |
| 内核级强制 | ✅ 五层 | ✅ microVM | ✅ cgroups/namespaces |
| 网络隔离 | ✅ GreyProxy | ✅ microVM | ✅ Docker network |
| 学习模式 | ✅ 自动生成配置 | ❌ | ❌ |
| 开箱即用 Agent | ✅ 10+ | ❌ | ❌ |
| 多平台 | ✅ Linux + macOS | ✅ Linux | ✅ Linux/macOS/Windows |

---

## 笔者观点

### 1. 无容器是正确的产品方向

容器在服务器端有优势，但在开发者本地环境中开销过大。Greywall 理解了这个场景差异，直接在内核层面做隔离，既避免了容器开销，又保持了与本地工作流的兼容性。

### 2. 学习模式是杀手级特性

大多数沙箱方案要求用户手动配置权限，这本质上需要用户理解 Agent 的行为模式。Greywall 的 `--learning` 模式反其道而行——**让 Agent 跑一次，观察它实际用了什么，然后生成配置**。这比任何白名单配置都准确。

### 3. 危险命令阻止的实用价值

`rm -rf /` 和 `git push --force` 是 Agent 高危操作的两大代表。Greywall 把这些命令默认阻止，比依赖 Agent 的"判断力"更可靠。这对 harness 设计是一个有价值的参考：危险操作的默认策略应该是拒绝，而非让 Agent 自己判断。

### 4. GreyProxy 的仪表板价值

实时允许/拒绝网络连接的仪表板，解决了"Agent 到底能访问什么"的可见性问题。在企业场景中，审计和合规要求通常需要这种级别的可见性。

---

## 关键引用

> "Greywall is a container-free, deny-by-default sandbox for AI agents on Linux and macOS. It restricts filesystem access, network connections, and system calls to only what you explicitly allow."
> — Greywall README

> "Use `--learning` to trace what a command needs and auto-generate a least-privilege config profile."
> — Greywall README

---

**项目信息**

| 项目 | 值 |
|------|------|
| GitHub | [GreyhavenHQ/greywall](https://github.com/GreyhavenHQ/greywall) |
| Stars | 183 |
| Language | Go |
| License | Apache 2.0 |
| 主页 | https://greywall.io |
| 主题关联 | 与"多 Agent 并行开发"文章形成闭环：Git Lock 协调 + 内核级沙箱隔离 |

---

**参考来源**：[Greywall GitHub README](https://github.com/GreyhavenHQ/greywall)（Stars: 183, Created: 2026-03-04）