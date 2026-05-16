# OpenAI Codex Windows 沙箱：一场没有标准答案的工程突围

> 本文分析 OpenAI 工程团队为 Codex for Windows 构建沙箱环境的技术决策过程，涵盖 Windows 隔离机制的局限性分析、自定义沙箱的原型设计，以及最终 elevated sandbox 架构的权衡取舍。

## 核心问题

Codex 作为编程辅助 agent，默认以用户权限运行——这意味着它能执行用户可以执行的一切操作。Windows 用户面临一个糟糕的二选一：

- **Approve-all 模式**：几乎每个命令都需要用户批准，效率极低
- **Full Access 模式**：Codex 可无限制运行，牺牲了安全性

问题的本质是：需要一个沙箱环境，让 Codex 的文件写入和网络访问被约束在安全边界内，同时不影响正常的开发工作流。

## Windows 隔离机制的局限

OpenAI 评估了三种 Windows 原生隔离方案：

| 方案 | 核心能力 | 被放弃的原因 |
|------|---------|------------|
| **AppContainer** | 能力沙箱（capability-based），提供真实 OS 边界 | 面向的是「预先知道需要哪些权限」的固定场景，而 Codex 的工作流是开放的——Shell、Git、Python、构建工具，事先无法枚举 |
| **Windows Sandbox** | 轻量级Disposable VM，强隔离 | Codex 需要直接操作用户实际的代码 checkout，而非在访客桌面重新配置环境；且 Windows Home SKU 根本不支持 |
| **MIC（Mandatory Integrity Control）** | 按信任级别（Low/Medium/High）控制对象访问 | 将 workspace 标记为 Low Integrity 意味着**所有**低权限进程都能写入——这改变了系统信任模型，风险无法控制 |

这三个方案的共同问题在于：它们是为「固定作用域应用」设计的，而 Codex 是「开放工作流 agent」，二者形态不匹配。

## 第一个原型：Unelevated Sandbox

既然没有现成工具，OpenAI 自己造。

核心设计基于两个 Windows 概念：

**SID（Security Identifier）**：Windows 中绑定权限的身份标识。OpenAI 创建了一个 synthetic SID（`sandbox-write`），专门用于沙箱，写入权限通过 ACL 精确授予该 SID，而非修改真实用户的权限。

**Write-restricted Token**：Windows 允许创建受限进程 token，写操作必须同时满足两个条件：
1. 正常身份检查通过（用户本就有权限）
2. Token 的 restricted SID 列表中至少有一个 SID 被授予了写入权限

这实现了：**只有携带特定 synthetic SID 的沙箱进程才能写入指定目录**。

文件系统写入限制得以精细化控制，但网络隔离成为弱点。OpenAI 通过环境变量「毒化」常见工具的代理设置：

```bash
HTTPS_PROXY=http://127.0.0.1:9    # 让 HTTPS 请求失败
GIT_HTTPS_PROXY=http://127.0.0.1:9
GIT_SSH_COMMAND=cmd /c exit 1    # SSH 直接失败
```

但这只是「 advisory 级别」——进程完全可以忽略这些环境变量。这是设计上的根本缺陷。

## Elevated Sandbox：引入专用 Windows 账户

真正解决网络隔离需要 Windows Firewall，但 Firewall 规则的匹配维度（用户/程序/端口/地址）无法精确到「某个 restricted token 启动的进程树」。

OpenAI 发现的约束：**Windows Firewall 无法匹配 non-principal identity（即 synthetic SID）**。

唯一的解法：让沙箱进程以**独立的 Windows 账户**运行，而不是当前用户的 token。Codex 创建了两个本地账户：

- `CodexSandboxOffline`：被防火墙规则 targeting，阻断外网访问
- `CodexSandboxOnline`：不受防火墙限制，允许必要的外网操作（如 package download）

这是一个权衡取舍：
- **放弃**了"No elevation"的约束
- **获得**了可依赖的 Windows Firewall 网络隔离

这是典型的工程决策：**没有完美的方案，只有在当前约束下最可接受的方案**。

## 关键教训

### 1. OS 原生隔离机制是为固定场景设计的，agent 的开放工作流是另一种问题形态

AppContainer 要求应用预先声明能力，MIC 要求改变对象的 trust level——这些都和「让 agent 按需使用任意开发工具」的动态性不兼容。

### 2. Advisory 级别的网络隔离是不可接受的

仅靠环境变量覆盖无法抵御真实攻击。OpenAI 最终选择 elevated 方案，说明了一个现实：**安全隔离不能打折**。

### 3. Platform constraints 会反向驱动架构决策

最初坚持 unelevated 是因为不想让用户配置 admin 权限。但当安全目标无法在不 elevation 的前提下实现时，constraints 驱动了架构演进——而不是目标为 constraints 让步。

## 原文引用

> "A sandbox is a constrained execution environment. When a developer uses Codex, their computer's operating system launches a command with reduced permissions, and those constraints propagate down the process tree."
>
> — [Building a safe, effective sandbox to enable Codex on Windows](https://openai.com/index/building-codex-windows-sandbox/), OpenAI Engineering Blog

---

**Tags**: #sandbox #windows #harness #security #agent-architecture