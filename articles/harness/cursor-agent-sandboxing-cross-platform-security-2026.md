# Cursor Agent 沙箱跨平台安全工程：如何让权限控制不打断 Agent 工作流

> 本文深度分析 Cursor Engineering Blog 原文：*Implementing a secure sandbox for local agents*（Feb 18, 2026）

---

## 核心命题

**沙箱安全对 Coding Agent 的挑战，根本上是一个 Harness 设计问题，而不是权限清单问题。** 真正困难的不在于操作系统层的沙箱原语（Landlock / seccomp / Seatbelt），而在于如何让 Agent 模型理解并主动预期自己的权限边界——以及如何在违反边界时给出有用的恢复提示而非静默失败。

---

## 一、问题的本质：Approval Fatigue 才是安全漏洞

Cursor 的工程师们观察到了一个反直觉的现象：

> 随着审批请求堆积，用户停止仔细检查它们。当工程师并行运行多个 Agent 时，情况更糟——他们需要在审批提示之间上下文切换。结果是 **approval fatigue**，而这恰恰破坏了设置审批的初衷。

换句话说：人工审批机制在高压力下会退化为形式主义，从而产生新的安全漏洞。

Cursor 的解决方案核心是：**把"审批"变成"沙箱"，让 Agent 在受控环境内自由行动，只在需要突破边界时才请求人工介入。**

关键数据：
- **沙箱化 Agent 比非沙箱化 Agent 停止率低 40%**
- 这直接节省了用户数小时的手动审查和审批时间

这个数字背后是一个清晰的工程判断：与其优化"如何在审批数量多的时候保持警惕"，不如直接减少审批数量。

---

## 二、跨平台沙箱实现：三个平台的四种思路

Cursor 在 macOS、Linux、Windows 上分别实现了沙箱，每个平台都走了不同的技术路线。

### macOS：Seatbelt 的历史包袱

macOS 的沙箱技术基于 `sandbox-exec`，具体来说是 **Seatbelt**——一个 2007 年引入、2016 年被废弃但至今仍被 Chrome 等关键应用使用的机制。

Seatbelt 的核心是一个**沙箱 profile**，通过一种特殊的策略语言定义权限，细粒度地限制系统调用以及对特定文件和目录的读写操作。

```text
(profile
  (allow file*)
  (deny network*)
)
```

Cursor 的沙箱 profile **在运行时动态生成**，输入包括：
- 工作区级别的配置
- 管理员级别的配置
- 用户的 `.cursorignore` 文件

**动态生成**是关键——静态配置无法覆盖不同用户、不同项目、不同安全需求的组合。

### Linux：Landlock + seccomp 的组合拳

Cursor 放弃了在 Linux 上使用沙箱 profile 的方案，改用 **Landlock + seccomp 直接组合**：

- **seccomp**：阻塞不安全的系统调用
- **Landlock**：强制文件系统限制，让被忽略的文件对沙箱内进程完全不可访问

具体实现上，Cursor 将用户工作区映射到一个 **overlay 文件系统**，用 Landlock 保护的副本覆盖 `.cursorignore` 中的文件——这些副本既不能被读取也不能被修改。

> **有趣的工程细节**：在 Linux 上寻找并重新挂载这些文件是整个沙箱实现中最慢的部分。Cursor 选择了积极地重新挂载，而不是像 macOS 那样延迟过滤文件系统操作——原因是 Linux 在 seccomp-bpf 上下文中无法轻松获取文件路径，这迫使他们采取更激进的前置策略。

### Windows：独立设计

Cursor 没有在正文中详细展开 Windows 的实现细节，只提到了"不同的沙箱原语"，暗示 Windows 使用了不同于 macOS/Linux 的底层机制。这是跨平台工程中常见的现实——无法用统一的抽象覆盖所有平台，Cursor 的策略是**暴露统一的沙箱 API，底层实现每个平台独立完成**。

---

## 三、让 Agent 理解沙箱约束：这是最难的部分

Cursor 在博文中有这样一句话：

> A sandbox is only effective if agents can anticipate which commands will succeed inside the sandbox and recognize when escalation is required.

这句话揭示了沙箱设计中最深刻的洞察：**沙箱的效力取决于 Agent 能否主动预期边界并识别需要升级的场景**，而不是被动地被系统拦截。

为了让模型"沙箱感知"，Cursor 做了两件事：

### 1. 更新 Shell 工具描述

```text
Shell tool now includes:
- Whether commands run with filesystem, git, or network access
- Based on user settings
- How the agent can request elevated permissions when needed
```

这是一个** Harness 层面的改动**：不在操作系统层强制限制，而是在模型层的工具描述中嵌入沙箱语义的说明。

### 2. Shell 结果渲染加入约束提示

Cursor 发现了一个常见的失败模式：**Agent 会反复重试同一个被沙箱拦截的终端命令，而不改变权限配置。**

解决方法是更新 Shell 工具结果的渲染方式：**明确显示导致失败的沙箱约束，并在某些情况下推荐 Agent 升级权限。**

这一改动上线后，Agent 从沙箱相关失败中恢复的优雅程度显著提升，离线评估性能也大幅改善。

---

## 四、工程判断：沙箱设计的核心权衡

Cursor 工程师在文中写道：

> Designing a usable sandbox is an exercise in navigating tradeoffs between security and usability, while working within the parameters set by each operating system.

这句话点出了沙箱设计的核心矛盾：

| 维度 | 一端（安全优先） | 另一端（可用性优先） |
|------|----------------|-------------------|
| **权限粒度** | 最小权限，精确白名单 | 宽松策略，减少阻断 |
| **失败处理** | 静默失败，要求手动审批 | 明确提示，引导权限升级 |
| **跨平台一致性** | 统一抽象，牺牲平台特色 | 平台原生实现，一致性降低 |
| **动态性** | 静态配置，预先声明 | 运行时生成，动态适应 |

Cursor 的选择是：中间表走 —— **统一 API + 平台差异化实现 + 动态 profile 生成**。

---

## 五、未来方向：Sandbox-Native Agents

博文结尾有一个值得特别关注的展望：

> Going forward, we're especially excited about **sandbox-native agents** trained on the constraints of their environment. These agents can be given the freedom to write scripts and programs directly, rather than being limited to tool-calling.

这是从"用沙箱限制 Agent"到"让 Agent 天生理解沙箱"的一次转变。Sandbox-native agents 不是被沙箱约束的工具调用者，而是**被沙箱环境训练出来的、能直接写脚本和程序的自主执行者**。

这与 Anthropic 提出的"Models are middleware"的思路一脉相承——当模型对执行环境有结构性理解时，它不再需要人类帮助它理解"能做什么 / 不能做什么"。

---

## 六、工程启示录

### 核心观点

**沙箱不是安全护栏，而是 Agent 工作流的一部分。** 当沙箱的约束能被 Agent 主动预期和表述时，它就不再是中断源，而是工作环境的一部分。

### 实践要点

1. **Approval fatigue 是真实的安全威胁**：当人工审批机制在高频率下失效时，它比没有审批更危险。沙箱化是绕过这个失效模式的设计选择。
2. **动态沙箱 profile 优于静态配置**：基于 `.cursorignore`、工作区设置、管理员配置的动态生成，可以覆盖静态配置无法处理的组合场景。
3. **模型感知是沙箱有效性的关键**：让 Agent 理解约束边界比仅仅拦截违规操作重要得多。Shell 工具描述的更新和结果渲染的约束提示都是 Harness 层面的投资。
4. **跨平台统一 API + 平台差异化实现是唯一可行路径**：不可能用单一抽象覆盖三个平台，必须接受实现层的分裂。

### 引用来源

> Coding agents are getting much better at running terminal commands to explore the environment and make changes. Users who auto-approve these commands unlock significantly more powerful agents, but at the cost of increased risk.
> — Cursor Engineering Blog, "Implementing a secure sandbox for local agents"

> A sandbox is only effective if agents can anticipate which commands will succeed inside the sandbox and recognize when escalation is required.
> — Cursor Engineering Blog, "Implementing a secure sandbox for local agents"

---

*本文归档于 `articles/harness/` — 代表 Harness Engineering（权限分层、防护机制、审计）方向的核心内容。*