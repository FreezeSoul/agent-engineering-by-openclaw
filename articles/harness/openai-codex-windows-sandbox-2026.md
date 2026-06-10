#拆解 Codex Windows Sandbox：没有 OS 原语支持时，如何用 ACL + 专用用户构建隔离引擎

> 本文解读 OpenAI Codex 工程团队如何在 Windows 上从零实现生产级沙箱，涵盖 Synthetic SID + Write-Restricted Token 的文件隔离、环境变量网络阻断的局限，以及 Elevated Sandbox 的多用户架构设计。

---

## 核心命题

**Codex 的沙箱设计揭示了一个根本矛盾：开发者工具天生需要操作真实环境（文件系统、Git、终端命令），而 OS 的安全机制是为「已知用途的封闭程序」设计的，不是为「开放性 Agent 工作流」设计的。**

Windows缺乏 macOS Seatbelt 或 Linux seccomp/bubblewrap 这样的开箱即用沙箱原语，OpenAI 的工程团队在两年内经历了从「无沙箱」到「Unelevated Sandbox」再到「Elevated Sandbox」两次架构演进，最终用 Synthetic SID + Write-Restricted Token +专用 Windows 用户构建了一套在真实开发者机器上可用的隔离引擎。

---

##背景：Windows 用户的两难困境

在2025 年 9 月 Codex Windows 实现沙箱之前，Windows 用户面对的是两个糟糕的选项：

1. **每次都审批**：即使读取文件也需要人工确认，Codex 的价值几乎清零
2. **完全放行（Full Access）**：让 Codex 以当前用户身份运行所有命令，毫无约束

> "A major benefit of using Codex is that you don't have to do all the tedious work yourself." — Codex 工程团队

这个两难揭示了 Harness 设计的核心问题：**当安全边界缺失时，用户被迫在「无用」和「无险」之间二选一**。

---

## 为什么 Windows 原生方案全部不合适

OpenAI 评估了三种 Windows 原生的隔离机制：

| 方案 | 核心机制 | 为何不适合 Codex |
|------|---------|----------------|
| **AppContainer** | 能力模型（capability-based），OS 级强隔离 | 要求预先声明精确的资源需求，Codex 的工作负载是开放的（Shell、Git、Python、package manager），AppContainer 的「已知用途」假设与 Agent 的开放性根本冲突 |
| **Windows Sandbox** | 轻量级 disposable VM，完整 OS 隔离 | 需要作用在用户真实 checkout 和工具链上，不能用 VM；且 Windows Home SKU 不支持 |
| **MIC（Mandatory Integrity Control）** | 将进程标为 Low/Medium/High Integrity Level | 将 workspace 标记为 Low Integrity 后，所有 Low Integrity 进程都可以写入，不分是否是 Codex；改变了整台机器的信任模型，语义影响面太大 |

笔者认为，这里最深刻的教训是：**MIC 的失败不是技术问题，而是语义问题**——它设计的信任模型是「进程级别的权限继承」，而 Agent 的需求是「会话级别的边界控制」。这两个模型根本就不是一回事。

---

## Unelevated Sandbox：基于 ACL 的文件隔离

###核心机制：Synthetic SID + Write-Restricted Token

Unelevated Sandbox 不需要管理员权限，用两个 Windows 概念构建了文件写入边界：

**Synthetic SID**（安全标识符）：
Windows 允许创建「合成 SID」——不对应真实用户的 SID，但可以加入 ACL。例如 `sandbox-write` SID专门分配给 Codex 的沙箱写入区域。

**Write-Restricted Token**：
Windows 进程的 Token 定义了身份和权限。Write-Restricted Token 在正常的 Owner 检查之外，要求「受限 SID 列表中至少有一个 SID 被授予写入权限」才能写入。

这意味着：

```
写入成功 = (Owner本身有权限) AND (受限 SID 中至少有一个包含写入权限)
```

### 具体实现

沙箱启动时：

1. 创建 `sandbox-write` 合成 SID，授予对 `cwd`（当前工作目录）和 `config.toml` 中 `writable_roots` 的写入权限
2. 明确拒绝 `sandbox-write` 对 `/.git`、`/.codex`、`/.agents` 等敏感目录的写入
3. Codex 启动子进程时使用 Write-Restricted Token，受限 SID 列表包含 `[Everyone, Logon SID, sandbox-write SID]`

这在 ACL 层面实现了精确的文件边界：只有明确定义的区域可写，其他区域对沙箱进程只读。

### 网络隔离：环境变量毒化

网络隔离在无管理员权限时更难做。OpenAI 选择了「环境变量毒化」策略：

```bash
HTTPS_PROXY=http://127.0.0.1:9     # 代理到不存在地址
ALL_PROXY=http://127.0.0.1:9
GIT_HTTPS_PROXY=http://127.0.0.1:9
GIT_SSH_COMMAND=cmd /c exit 1      # SSH 直接失败
```

在 PATH 前面插入 `denybin` 目录，拦截 `ssh`、`scp` 等真实二进制。

### Unelevated Sandbox 的局限性

笔者认为这是整篇文章最有价值的部分——OpenAI 团队坦诚地记录了「看起来能工作」的设计为何不够：

1. **ACL 操作昂贵**：workspace 目录拓扑复杂时，ACL 应用耗时显著
2. **ACL 语义难以改变**：macOS 上改 Seatbelt 配置只需重生成 `.sbpl` 文件；Windows 上改 ACL 是高成本操作
3. **网络保护是「 advisory」的**：环境变量可以被进程忽略，可以绕过 PATH，可以直接打开 socket

> "Network protection is weak... was advisory... too risky." — Codex 工程团队

---

## Elevated Sandbox：从 UAC 绕过到多用户架构

###核心问题：为什么需要管理员权限

要实现真正的网络隔离（Windows Firewall），需要将防火墙规则绑定到特定用户身份。但 Windows Firewall 不支持「匹配 restricted token 中的 synthetic SID」——这个维度根本不存在。

唯一的解法：**用独立的 Windows 用户身份运行沙箱进程**。

### Elevated Sandbox 的两个专用用户

Codex 在 Windows 上创建两个本地用户：

- `CodexSandboxOffline`：所有网络访问被防火墙阻断
- `CodexSandboxOnline`：保留网络访问能力（用于需要网络的场景）

这不是「管理员 vs 普通用户」的简单区分，而是「为沙箱专门创建的、精确配置过的用户身份」。

### 三层二进制架构

这是工程上最有趣的部分——为了在普通用户和沙箱用户之间建立安全通道，OpenAI 将职责拆分到了三个二进制文件：

```
codex.exe（以真实用户身份运行）
    │
    │ CreateProcessWithLogonW(CodexSandboxUser)
    ▼
codex-command-runner.exe（以沙箱用户身份运行）
    │  在沙箱用户上下文中获取 Token
    │  添加受限 SID（write-restricted）
    │  CreateProcessAsUserW(受限Token, 子进程)
    ▼
子进程（受限 Token + 沙箱用户身份）
```

**codex-windows-sandbox-setup.exe**：处理所有需要提升权限的初始化工作（创建用户、配置 DPAPI加密的凭证存储、设置防火墙规则）。这个二进制只在 setup 时跨越 UAC boundary，平时 codex.exe 保持普通权限运行。

### 读取权限的特殊处理

以独立用户身份运行时，`CodexSandboxOffline` 用户的读取权限默认仅限于「Authenticated Users」可访问的位置。开发者常用的目录如 `C:\Users\<username>`、`C:\Windows\`、`C:\Program Files\` 等，默认对其他本地用户是关闭的。

解决方案：在沙箱 setup 阶段，异步地为沙箱用户添加对这些目录的读取 ACL。这是一个 Best-Effort 列表，安装过程异步执行，不阻塞用户操作。

### 跨 UAC 边界的架构决策

OpenAI 将沙箱 setup 封装为独立二进制有三个原因，不只是「避免污染 codex.exe」：

1. **跨 UAC 边界只在必要时发生**：setup 完成后退役，不需要 codex.exe 持续持有管理员权限
2. **生命周期解耦**：长时间运行的 setup 逻辑不影响 codex.exe 的稳定性
3. **平台差异隔离**：Windows 专用的 setup 逻辑不会增加其他平台的复杂度

笔者认为，第三点尤为重要——这也是 Harness 设计中常被忽视的原则：**将平台差异隔离到独立的边界模块，而不是让它渗透到核心逻辑中**。

---

## 工程启示录：Agent 沙箱设计的六个原则

从 OpenAI 的 Windows 沙箱实践中，可以提炼出六条工程原则：

### 1. OS 能力决定沙箱架构起点
不同 OS 的沙箱原语差异巨大。在 macOS/Linux 有原生支持的情况下，Windows 需要「从零发明轮子」。设计 Harness 时，必须先评估目标 OS 的安全原语，再决定沙箱的实现路径。

### 2. 文件边界用 ACL，网络边界用用户身份
Unelevated Sandbox 证明：基于 ACL 的文件边界可以在无管理员权限时工作。但网络边界必须依赖 OS 的用户/防火墙体系——这是环境变量无法可靠替代的。

### 3. Advisory 机制不是安全机制
环境变量、PATH 拦截、代理变量——这些「软」机制在对抗性环境下不可靠。任何声称提供网络隔离的实现，都必须回答「如果进程忽略环境变量，直接打开 socket，这个方案还成立吗？」

### 4. 多用户身份是权限分离的基础
Elevated Sandbox 的核心设计洞察：真正的权限分离需要独立的用户身份，而不只是受限的 Token。这比简单的 Token 限制更强，但也更复杂——需要在 setup阶段管理用户创建、凭证存储和 ACL 配置。

### 5. 平台差异应隔离在独立模块
Windows 沙箱 setup 的所有复杂度都封装在 `codex-windows-sandbox-setup.exe` 中，codex.exe 保持平台无关。这是 Harness 跨平台设计的典范——平台特定逻辑作为独立的边界模块，而不是污染核心。

### 6. 「无摩擦的安全」需要分层迭代
从「无沙箱」到「Unelevated」再到「Elevated」，OpenAI 经历了两次迭代。第一版优先无管理员权限，第二版解决网络隔离。每一次迭代都在「用户摩擦」和「安全强度」之间重新校准。这是一个持续的过程，不是非此即彼的选择。

---

## 与 Round313 的闭环：Agent Loop 的「执行」与「隔离」

Round313 分析了 Codex Agent Loop 的执行引擎（Prompt 构建、上下文管理、工具调用），本文则聚焦于 Codex 的**隔离引擎**——即 Harness 层如何为 Agent Loop 提供安全的执行环境。

两者共同揭示了 Codex架构的完整视图：

- **Agent Loop（Round313）**：模型的推理引擎——Prompt 如何构建、上下文如何管理、工具如何调用、循环何时终止
- **Harness Sandbox（本文）**：Agent 的安全引擎——文件边界如何划定、网络如何隔离、权限如何分层

缺少任何一个，Agent 系统都无法在真实环境中可靠运行。

---

## 引用来源

1. OpenAI Codex 工程团队，"Building a safe, effective sandbox to enable Codex on Windows"，OpenAI Index，2026
2. 同上，关于 Synthetic SID 和 Write-Restricted Token 的 Windows 机制描述
3. 同上，关于 Elevated Sandbox 的 `codex-command-runner.exe` 架构
4. 同上，关于网络隔离的局限性分析

---

*Round314 | 2026-06-10 |分类：harness/*