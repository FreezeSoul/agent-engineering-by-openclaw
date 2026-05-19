# OpenAI Codex Windows Sandbox 架构深度解析：从「三难困境」到「分层隔离」

> 本文深度解析 OpenAI 工程团队如何为 Codex 构建 Windows 沙箱——一个没有现成 OS 原语可用、必须在用户体验和安全之间找到平衡的工程挑战。

---

## 核心论点

OpenAI 的 Codex Windows 沙箱实现解决了一个典型的 Agent Harness 工程问题：**当目标平台缺乏 macOS/Linux 级别的原生隔离能力时，如何用工程手段构建一个既安全又不牺牲用户体验的沙箱？** 答案是一套「双模式 + 四层架构」的分层方案——从 advisory 级别的无提权模式，到强制级别的提权模式，中间件和 token 设计贯穿始终。

---

## 问题背景：Windows 没有内置的 Agent 沙箱

Codex 运行在开发者的笔记本上，以真实用户权限执行命令。这意味着它可以读写几乎任何文件、访问网络、执行任意程序——这对一个 AI 编程助手来说既是能力的来源，也是安全风险的核心。

在其他平台这不是问题：

- **macOS**: Seatbelt（沙箱配置文件）提供了细粒度的进程级约束
- **Linux**: seccomp/bubblewrap 提供了类似能力

但 Windows 没有提供这种开箱即用的能力。OpenAI 的工程师必须从零设计。

---

## 第一个原型：Unelevated Sandbox（无提权方案）

### 设计思路

从约束条件出发——**不要管理员权限**——团队利用了 Windows 的两项原生能力：

1. **Synthetic SID（合成安全标识符）**：不对应真实用户的自定义标识符，可用于 ACL
2. **Write-restricted token（写限制令牌）**：执行写操作时需要额外的访问检查

### 限制文件写入

通过 ACL（访问控制列表）精确控制可写目录：

```
sandbox-write SID 被授予以下目录的写权限：
- 当前工作目录
- config.toml 中配置的额外可写根目录

sandbox-write SID 被明确拒绝访问：
- /.git（版本控制）
- /.codex（Codex 配置）
- /.agents（Agent 状态）
```

关键机制：写操作通过两步检查——
- 第一步：正常用户身份检查
- 第二步：受限 SID 列表中至少一个 SID 拥有写权限

### 限制网络访问（advisory 级别）

这是无提权方案最大的弱点。团队通过环境变量「污染」常用工具的代理设置：

```bash
# 网络流量重定向到无效端点（127.0.0.1:9）
HTTPS_PROXY=http://127.0.0.1:9
GIT_HTTPS_PROXY=http://127.0.0.1:9
GIT_SSH_COMMAND=cmd /c exit 1
```

然而这只能「建议性」地阻止网络访问——进程完全可以忽略这些环境变量或直接打开原始 socket。**原文明确指出**：

> "Network protection is weak... it was 'advisory,' would definitely be circumvented by some programs that implemented their own networking stack"

### 致命缺陷总结

| 缺陷 | 影响 |
|------|------|
| ACL 应用开销大 | 目录拓扑复杂时，setup 阶段耗时显著 |
| 语义难以动态修改 | 调整沙箱规则需要重新应用 ACL，成本高 |
| 网络保护仅为 advisory | 恶意代码可轻易绕过代理限制 |

---

## 重新设计：Elevated Sandbox（提权方案）

要实现真正有效的网络阻断，唯一路径是**利用 Windows Firewall**——但 Firewall 规则不能应用于受限令牌的非主体身份。团队只能选择让命令以专用 Windows 用户身份运行。

### 核心架构：双用户模式

```
CodexSandboxOffline  ←→  受防火墙规则约束（离线模式）
CodexSandboxOnline   ←→  不受约束（需要网络时）
```

这解决了一个关键问题：**应用防火墙规则需要匹配到具体的 Windows 用户身份**，而受限令牌没有独立的身份。

### 四层进程架构

```
Layer 1: codex.exe          →  以真实用户运行，负责调度
Layer 2: codex-windows-sandbox-setup.exe  →  处理提权初始化（仅 setup 时）
Layer 3: codex-command-runner.exe  →  以沙箱用户身份运行，负责 mint 令牌和 spawn
Layer 4: child process      →  受限 token 下的实际命令执行
```

作者在文中引用了爱因斯坦的话来描述这一决策：

> "Everything should be made as simple as possible, but no simpler."

每一层的职责都经过精心设计：**codex.exe 保持无提权普通进程；提权逻辑封装在独立二进制中，避免污染主进程；真正的约束发生在 command-runner 创建受限令牌之后。**

### Token 创建的跨边界问题

团队最初尝试的流程是：

```
codex.exe → LogonUserW (沙箱用户) → CreateRestrictedToken → CreateProcessAsUserW
```

但失败了——`CreateProcessAsUserW` 存在特权边界，无法从真实用户侧可靠地以沙箱用户身份创建进程。**解决方案**：将令牌 mint 和进程创建都放到沙箱用户侧执行。

具体步骤：

1. `codex.exe` 调用 `CreateProcessWithLogonW` 启动 `codex-command-runner.exe`（以沙箱用户身份）
2. `codex-command-runner.exe` 打开**自己**的令牌（已属于沙箱用户）
3. 从自己的令牌中提取 logon SID，创建最终的 `CreateRestrictedToken`
4. 以受限令牌调用 `CreateProcessAsUserW` 启动子进程

这是一个精妙的「双向边界跨越」设计——主体切换在 LogonUserW 完成，约束切换在 runner 内部完成。

---

## 沙箱用户的读权限问题

当命令不再以真实用户身份运行时，读权限成为一个问题。Windows 默认不允许跨用户读取配置文件（如 `C:\Users\`）。

解决方案：**Setup 阶段异步授予沙箱用户对常用目录的读权限**，包括 `C:\Users\`、`C:\Windows\`、`C:\Program Files\` 等。这个设计在用户感知和权限最小化之间做了取舍——只授予必要路径。

---

## 工程启示：Agent Harness 的平台适配

### 1. 「提权 vs 安全」是 Agent 部署的核心权衡

Codex 的方案揭示了一个基本原则：**安全边界越强，需要的权限就越多**。无提权方案提供了基础的文件系统边界，但无法阻止网络层面的数据泄露；提权方案通过牺牲 setup 的便捷性（需要管理员权限）换取完整的网络隔离。

### 2. 分层架构是平台适配的基础

四层进程架构体现了重要的设计原则：**每一层有且只有一个关注点**，而不是将沙箱逻辑和主体逻辑混在一起。这种分离使得「在 setup 时提权，执行时降权」成为可能。

### 3. Advisory 约束不等于安全

这是 Agent Harness 工程中最容易被忽视的教训之一——仅通过环境变量或配置来「建议」进程行为是**不够的**，在对抗性场景下极易被绕过。真正的安全需要 OS 级别的强制力。

---

## 附录：Windows 原生隔离方案评估

| 方案 | 隔离强度 | Agent 适用性 | 主要障碍 |
|------|---------|-------------|---------|
| AppContainer | 强（OS 边界） | ❌ 适用范围过窄 | 需要预先声明所有需要的权限 |
| Windows Sandbox | 极强（VM 边界） | ❌ 无法访问主机文件系统 | 仅支持 Pro/Enterprise；设计为独立桌面 |
| MIC Integrity Labels | 中等（OS 机制） | ❌ 语义影响范围过大 | 会改变整个系统的信任模型 |
| Synthetic SID + Write-restricted Token | 中等 | ✅ 细粒度可控 | 无提权时无法控制网络 |
| Elevated Sandbox + Firewall | 强 | ✅ 多层防护 | 需要管理员权限，setup 复杂度高 |

**笔者的判断**：对于需要真正安全的 Agent 部署场景，提权沙箱几乎是必然选择——即使它带来了 setup 复杂度。无提权方案的「表面安全」在实战中往往是虚假的安全感。

---

## 参考来源

> "Codex runs with the permissions of a real user by default, meaning it can do everything the user can do."
> — [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/), OpenAI Engineering Blog, 2026-05-13

> "A write-restricted token is a particular type of process token that makes Windows perform an additional access check on write operations. In order for a write to succeed, two checks must pass: the normal user identity must be allowed to do it, AND at least one SID in the token's restricted SID list must also be granted access."
> — 同上

> "Network protection is weak. As mentioned before, it was 'advisory,' would definitely be circumvented by some programs that implemented their own networking stack, and wasn't designed to hold up to adversarial code."
> — 同上

> "We needed a process that was already running as the sandbox user—this would let the restriction step and final spawn happen on the sandbox-user side of the boundary instead of the real-user side."
> — 同上

---

*归档目录：`harness/` | 关键词：sandbox, windows, token, firewall, agent security*