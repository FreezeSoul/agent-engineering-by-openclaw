# Claude Code 沙箱设计：三层防御体系如何将权限提示降低 84%

## 核心论点

Claude Code 的沙箱设计揭示了一个反直觉的事实：Agent 安全不靠"多问多审"，而靠"设边界、给信任"。Anthropic 通过文件系统隔离 + 网络隔离 + 自动判断三层层防御，让权限提示从每次操作一次降低到只有越界时才问——84% 的提示减少不是压缩安全，而是重新定义安全边界。

## 一手来源

- **Anthropic Engineering Blog**：`https://www.anthropic.com/engineering/claude-code-sandboxing`
- 发布日：2025-10-20
- 官方描述：Making Claude Code more secure and autonomous with sandboxing

## 为什么"每次审批准"策略会失效

Claude Code 最初采用的是经典的权限模型：默认只读，写操作、bash、网络请求都需要用户逐条批准。听起来很安全，但实际上很快暴露出根本性的问题。

Anthropic 的遥测数据揭示了这个策略的内在矛盾：用户最终批准了约 93% 的权限请求。当批准变成例行公事，关注度会自然衰退——用户不再逐条审视，而是条件反射地点"允许"。这个现象在安全领域有专门术语：批准疲劳（approval fatigue）。

笔者认为，批准疲劳不是用户的性格缺陷，而是人机交互设计的必然结果。当一个防御机制要求用户在每次操作前介入，而操作频率又极高时，用户的大脑会自动将其降级为背景噪音。Claude Code 的开发者用户尚且如此，对技术背景更少的最终用户，这个问题的严重性只会更高。

## 三层防御体系：不是选一个，而是三个都要

Anthropic 的沙箱设计不是单点突破，而是三层防御的叠加。每一层堵住不同的攻击向量，联合起来才能真正限制 Agent 的爆炸半径（blast radius）。

### 第一层：文件系统隔离

文件系统隔离确保 Claude 只能访问或修改特定目录。这是一个看起来简单、但实施起来有大量细节需要处理的能力边界。

在 macOS 上，Claude Code 使用 Seatbelt（苹果的强制访问控制框架）实现这个边界；在 Linux 上，使用 bubblewrap。两个都是操作系统内核级别的隔离机制，不是应用层的模拟。

关键实现细节：目录边界的检查必须在符号链接解析**之前**执行。如果先解析符号链接再检查路径，一个被允许目录内的符号链接就能指向外部目录，实现穿越。在 Claude Cowork 的设计中，这个细节导致了架构调整——路径验证必须在路径解析之前完成。

### 第二层：网络隔离

网络隔离确保 Claude 只能连接到白名单内的服务器。这个层防止了两类风险：数据泄露（被入侵的 Agent 向外发送敏感文件）和恶意下载（从外部获取恶意代码执行）。

Claude Code 的网络隔离通过 Unix 域 socket 实现——Agent 进程在沙箱内通信，所有出站流量经过一个代理服务器，代理服务器强制执行域名白名单和用户确认机制。这个设计意味着即使 Agent 获得了主机上的网络访问权，仍然无法直接建立外部连接，因为连接必须经过代理。

Anthropic 的测试数据说明了这一点的重要性：没有网络隔离的沙箱，成功的提示注入可以让 Agent 将 SSH 密钥外发；有网络隔离的情况下，无论提示注入多么精巧，数据也无法流出。

### 第三层：信任对话框（Trust Dialog）

在文件系统隔离和网络隔离的基础上，Claude Code 引入了一个新的信任对话框——在项目启动时询问用户"是否信任此目录"。这个对话框的时间点很关键：它发生在 Agent 获得任何特殊权限之前，给用户一个明确的决策节点。

更重要的是，信任对话框解决了代码执行前的一个被忽视的攻击面：在用户明确同意之前，Claude Code 就会读取项目配置文件（`.claude/settings.json`）并执行其中的钩子。这意味着一个恶意仓库可以通过在 `settings.json` 中植入钩子，在用户决定是否信任该项目之前就获得代码执行机会。Anthropic 在 2025 年中至 2026 年 1 月期间通过负责任披露收到了三份这类漏洞报告，修复方式是：将所有项目本地配置的解析和执行推迟到用户接受信任提示**之后**。

## 沙箱的工程实现：OS 级别原语的选择

Claude Code 沙箱实现选择使用操作系统级别的原生隔离机制（bubblewrap/Seatbelt），而非容器或虚拟机，这个选择背后有重要的工程考量。

**相对于容器的优势**：
- 启动延迟：从数秒降低到毫秒级。Claude Code 的使用场景是日常开发迭代，容器启动的等待时间会显著影响使用体验。
- 资源开销：不需要完整的操作系统虚拟化，一个进程级的沙箱消耗资源少得多。
- 配置复杂度：开发者不需要维护 Dockerfile 或容器编排配置，开箱即用。

**相对于容器的限制**：
- 隔离粒度：容器可以提供更强的隔离（包括独立的网络栈），但进程级沙箱的隔离依赖系统调用拦截，对某些高级攻击面的防护不如容器完整。
- 跨平台一致性：bubblewrap（Linux）和 Seatbelt（macOS）的行为细节不完全一致，跨平台开发需要额外测试。

Claude Code 也在探索云端版本（Claude Code on the Web），使用完整虚拟机方案来提供更强的隔离保证，但这是针对不同使用场景的权衡——本地开发需要低延迟，云端场景需要更强隔离。

## 与传统安全模型的本质区别

Claude Code 的沙箱设计反映了一个更深层的思路转变：不是"监控 Agent 做什么"，而是"限制 Agent 能做什么"。

传统安全思维是白名单/黑名单 + 逐条审批：列出允许的操作清单，每次操作前检查。这个模型在操作频率低时有效，但当 Agent 每天执行数百次操作时，用户无法保持持续的注意力。

沙箱模型则是：先确定 Agent 的能力边界（在哪些目录、访问哪些网络），在边界内 Agent 完全自主运行；只有当 Agent 试图突破边界时，才需要人类介入。这实际上是将安全边界从"操作级别"提升到了"区域级别"，大幅减少了需要人类判断的次数。

笔者认为，这个转变对 Agent 的实际可用性有决定性影响。一个需要用户在每次文件写入前批准的 Agent，实际上是在用人类注意力作为稀缺资源来换取安全性——这在高频操作场景下是不可扩展的。一个在边界内可以自主执行、在边界处才请求确认的 Agent，才能真正将人类从"审批者"转变为"监督者"。

## 启示与延伸

对于构建自研 Agent 系统的团队，Claude Code 的沙箱设计提供了几个可以直接复用的原则：

第一，**符号链接解析必须在路径验证之前**。这是一个工程细节，但在实际实现目录隔离时非常容易踩坑。

第二，**项目配置文件在信任确认之前不应被执行**。如果你的 Agent 系统会读取并执行用户项目中的配置文件，这个攻击面必须被封闭。

第三，**网络隔离是文件系统隔离的必要补充**。单独的文件系统隔离不足以防止数据泄露——一个获得文件系统访问权的 Agent 仍然可以通过网络外发数据。

第四，**安全设计的迭代需要遥测数据支撑**。Anthropic 发现 93% 批准率和 84% 提示减少的数据，都是通过实际用户使用数据发现的——闭门设计安全系统会遗漏这些真实的失效模式。

## 原文引用

> "Constantly clicking 'approve' slows down development cycles and can lead to 'approval fatigue', where users might not pay close attention to what they're approving, and in turn making development less safe."
> — Anthropic Engineering Blog

> "Without network isolation, a compromised agent could exfiltrate sensitive files like SSH keys; without filesystem isolation, a compromised agent could easily escape the sandbox and gain network access."
> — Anthropic Engineering Blog

## 关联项目

本文关联的项目是 [elusznik/mcp-server-code-execution-mode](https://github.com/elusznik/mcp-server-code-execution-mode)，它将 MCP 的代码执行模式与沙箱隔离结合，实现了上下文 Token 从 30K 到 200 的压缩。沙箱设计 + 代码执行效率的组合，正是 Claude Code 这篇文章中"安全且高效"的工程目标的具体实现。

---

**标题备选**：

1. `Claude Code 沙箱设计：84% 权限降低背后的三层防御` — 策略：数据冲击（25 单位）
2. `Agent 安全新范式：边界防御而非逐条审批` — 策略：认知反转（22 单位）
3. `沙箱不是限制，是 Agent 的运行环境设计` — 策略：概念重新定位（25 单位）