# OpenAI Codex Windows 沙箱架构：ACL 与 Token 机制深度解析

## 核心问题

Codex 在 Windows 上面临一个 macOS/Linux 不存在的困境：Windows 没有原生 sandbox 工具（macOS 有 Seatbelt，Linux 有 seccomp/bubblewrap），而开发者又需要既安全又可用的 AI Coding 环境。OpenAI 的工程团队花了大量精力解决这个问题，最终走出了一条「ACL + Write-Restricted Token + 专用 Windows 用户」的技术路线。

理解这个方案的价值不只是"知道 Codex 怎么实现沙箱"，而是**从根上理解为什么 Windows 的安全模型对 Agent 来说是个特殊挑战，以及为什么用 ACL 做进程级隔离是个bad smell**。

---

## 背景：为什么 Windows 沙箱是个难题

Codex 的沙箱需要解决两个核心约束：

1. **文件系统写限制**：Agent 只能在 workspace 目录内写文件，不能碰 `.git`、`.codex`、`.agents` 等敏感路径
2. **网络访问限制**：Agent 不能随意访问外网，防止数据泄露

在 macOS/Linux 上，这通过内核级 syscall 过滤（Seatbelt/seccomp）实现，约束直接在进程级别生效，Agent 无法绕过。

但 Windows 没有等效工具。OpenAI 评估了三种原生方案：

| 方案 | 优点 | 致命缺陷 |
|------|------|---------|
| **AppContainer** | 真正的 OS 级隔离边界 | 过于严格，只能用于「知道自己需要什么权限」的固定场景，而 Agent 工作流是开放式的 |
| **Windows Sandbox** | 强隔离，VM 级别 | 需要在独立 VM 内运行，无法访问用户真实的 checkout/工具链，且 Home SKU 不支持 |
| **MIC (Mandatory Integrity Control)** | 内核级完整性级别机制 | 标记 workspace 为 low-integrity 后，所有 low-integrity 进程都能写——这把用户真实 checkout 变成了公共 sink，风险无法控制 |

三个方案都不满足需求，OpenAI 决定自建。

---

## 第一代方案：Unelevated Sandbox

### 核心机制：Synthetic SID + Write-Restricted Token

在没有 admin 权限的情况下，OpenAI 用两个 Windows 机制组合实现文件系统约束：

**Synthetic SID（合成安全标识符）**

Windows 的 SID（Security Identifier）是权限系统的根基。每个用户、用户组、登录会话都有唯一 SID。关键能力是：**可以创建不对应真实用户的 Synthetic SID，并将其放入 ACL**。

Codex 创建一个 `sandbox-write` Synthetic SID，给它精确的写权限：

```
sandbox-write SID 被授予以下路径的写/执行/删除权限：
- 当前工作目录
- config.toml 中配置的所有 writable_roots

sandbox-write SID 被显式拒绝以下路径的写权限：
- /.git
- /.codex
- /.agents
```

**Write-Restricted Token（写限制令牌）**

Windows 的进程令牌定义了进程身份。Write-Restricted Token 是一种特殊令牌，它在检查写操作时执行**双重验证**：

```
写操作成功需要同时满足：
1. 正常身份检查：令牌 owner 有权限
2. Restricted SID 检查：令牌的 restricted SID list 中至少有一个 SID 被授予访问权限
```

Codex 用这个机制让进程同时持有多个 SID（Everyone、Logon Session SID、sandbox-write SID），然后通过 ACL 精确控制每个 SID 在各路径的权限。

**结果**：sandbox-write SID 对 workspace 有写权限，对敏感路径无写权限，且这个约束是 Windows ACL 强制执行的——不在进程内部，不在环境变量里。

### 网络限制：失效的 Plan A

文件系统约束用 ACL 解决了，但网络限制才是真正的难题。

理想方案是 Windows Firewall，但：

- 创建针对特定进程树的防火墙规则需要 admin 权限
- 防火墙规则不能按 "restricted token 中的 synthetic SID" 匹配——Windows 防火墙根本不认识这个身份维度

OpenAI 的妥协方案是**环境变量投毒**：

```
HTTPS_PROXY=http://127.0.0.1:9      # 让代理感知工具走不通的本地端口
ALL_PROXY=http://127.0.0.1:9
GIT_HTTPS_PROXY=http://127.0.0.1:9
NO_PROXY=localhost,127.0.0.1,::1
GIT_SSH_COMMAND=cmd /c exit 1       # SSH 直接失败
```

在 PATH 前置 stub 脚本覆盖 `ssh`、`scp` 等。

**这是一个 advisory 机制，不是强制机制**。OpenAI 在文章中承认：

> "plenty of good-intentioned code/binaries would also circumvent it simply if they didn't honor the environment proxy variables, or if they implemented their own socket-based network code"

对于企业级安全，这个方案是不够的。

### Unelevated 方案的三个问题

OpenAI 总结了这个原型的三个缺点：

1. **Setup 速度慢**：ACL 变更代价高昂（取决于目录拓扑），且会真正修改主机文件系统语义
2. **不可变的安全性**：相比 macOS 的 `.sbpl` 配置文件可以动态重载，Windows ACL 语义一旦设定就难以调整
3. **网络保护太弱**：环境变量投毒防不住自建网络栈的程序

---

## 第二代方案：Elevated Sandbox

### 核心变化：引入专用 Windows 用户

OpenAI 放弃了"零 admin"的约束，改为**在 setup 阶段需要 admin，但运行时不需要**。这解锁了两个关键能力：

**创建专用 Windows 用户**

```
CodexSandboxOffline — 目标防火墙规则的用户，网络访问被严格限制
CodexSandboxOnline  — 不受防火墙限制的用户（需要外网访问时）
```

注意这里的**离线/在线是预先划分的**，而不是运行时动态判断。这是正确的安全设计——runtime 决策容易出错。

**用 Windows Firewall 实现真正的网络隔离**

因为进程现在以专用用户身份运行，Windows Firewall 可以按用户维度匹配规则：所有以 `CodexSandboxOffline` 身份运行的进程都被禁止 outbound 连接，而 `CodexSandboxOnline` 不受限制。

### 架构对比

```
Unelevated Sandbox:
  进程身份 = 真实 Windows 用户
  文件系统隔离 = ACL + Write-Restricted Token（有效）
  网络隔离 = 环境变量投毒（脆弱）
  需要 admin = 否（但牺牲了网络安全性）

Elevated Sandbox:
  进程身份 = CodexSandboxOffline / CodexSandboxOnline
  文件系统隔离 = 继承自 Unelevated 的 ACL 机制（不变）
  网络隔离 = Windows Firewall 强制执行（真正有效）
  需要 admin = setup 时需要，runtime 不需要
```

---

## 关键工程判断

### 为什么不用 AppContainer？

AppContainer 是 Windows 原生最强的隔离机制，但 OpenAI 拒绝它的核心理由值得深思：

> "Codex is not one tightly scoped app. It drives open-ended developer workflows: shells, Git, Python, package managers, build tools, and whatever other binaries the agent decides it needs."

这揭示了一个 Agent 沙箱设计的根本矛盾：**强隔离要求已知且固定的权限集合，而 Agent 工作流天生是开放式的**。AppContainer 适合「从已知起点出发、执行已知任务」的固定 agent，但不适合「探索环境、执行任何开发工具」的开放式 agent。

### 为什么 MIC 最终被放弃？

MIC 的问题是**语义变更范围太大**。把 workspace 标记为 low-integrity 不只是「Codex 可以写这里」，而是「所有 low-integrity 进程都可以写这里」。在真实开发机上，这个变更把用户代码库变成了低信任级别的公共空间，引入了比它解决的问题更大的风险。

**教训**：用 OS 安全机制做 Agent 隔离时，必须确保安全机制的语义变更范围是精确且可控的，不能引入侧信道风险。

### Elevated 方案的真正价值

OpenAI 在文章中提到「在 setup 时需要 admin」是值得付出的代价。这个判断基于一个现实：**企业用户通常有 admin 权限，且愿意在 setup 时授予一次权限换取运行时零提示**。而 macOS/Linux 用户早就习惯了安装软件时的权限授予。

---

## 对 Harness 设计的启示

### 平台安全原语决定架构上限

Codex Windows 沙箱的复杂度很大程度上是因为 Windows 缺乏一等公民的进程隔离原语。如果你在设计 Agent Harness 并需要跨平台支持，必须承认：**每个平台的安全隔离能力不同，架构需要为最弱的那个平台做规划**。

### ACL 作为安全机制的双刃剑

ACL 确实能工作，但它修改的是主机文件系统语义——一旦应用到真实开发者的 checkout 上，这个变更对其他进程也生效。真正的容器级隔离（Docker、Kata Containers）隔离的是进程视角的文件系统，而不是在真实 FS 上雕刻 ACL。

### 网络隔离是最后一道防线

OpenAI 在文章中把网络隔离放在了非常重要的位置——宁可放弃"Unelevated"方案也要用 Firewall 做真正的网络隔离。这是正确的判断：**文件系统误操作有 Git 可以恢复，但数据通过网络外传是不可逆的**。

---

## 引用

> "Codex runs with the permissions of a real user by default, meaning it can do everything the user can do. This is powerful and potentially dangerous."

> "plenty of good-intentioned code/binaries would also circumvent it simply if they didn't honor the environment proxy variables, or if they implemented their own socket-based network code."

> "To gain better network suppression, we wanted to use Windows Firewall... Unfortunately, we couldn't effectively create a functional firewall rule that applied only to the commands spawned by the Codex harness."

来源：[Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/)，OpenAI Engineering，2026-05-13
