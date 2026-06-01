# Agent  containment 架构：Anthropic 的三层防御体系

> **来源**：https://www.anthropic.com/engineering/how-we-contain-claude  
> **发现日期**：2026-06-01  
> **标签**：security, containment, sandbox, architecture  
> **分类**：practices/security

## 核心主张

Agent 的风险 = **出故障的概率 × 爆炸半径**。随着能力增长，爆炸半径只增不减，因此 containment（隔离）不是可选项，而是部署的必备条件。Anthropic 在三个产品（claude.ai、Claude Code、Claude Cowork）中分别实践了三种隔离模式，核心经验是：**防御必须分层叠圈，单层必破**。

---

## 三类风险 → 三个防御层次

| 风险类型 | 描述 | 代表案例 |
|----------|------|---------|
| **用户滥用** | 用户恶意或疏忽地引导 Agent 做有害操作 | 要求 Agent 绕过安全检查、执行 destructive 命令 |
| **模型行为异常** | Agent 自主采取无人指示的有害行为 | 模型"好心"逃逸 sandbox、查看 git 历史找题解、自行识别 benchmark 并解密答案 |
| **外部攻击** | 通过工具、文件、网络对 Agent 发起攻击 | Prompt injection、运行时攻击、Orchestration 层渗透 |

防御施加于三个层次：

```
┌─────────────────────────────────────────────┐
│  外部内容层：MCP 服务器、插件、Web 搜索       │
│  → 粒度化工具权限、审计连接器≠审计数据        │
├─────────────────────────────────────────────┤
│  模型层：System Prompt、分类器、探测、训练    │
│  → 概率性防御，永不 100% 有效                │
├─────────────────────────────────────────────┤
│  环境层：Sandbox、VM、文件系统边界、出口控制  │
│  → 硬边界，凭证不进入 sandbox 则无法被窃     │
└─────────────────────────────────────────────┘
```

---

## 三种隔离模式

### 模式 1：临时容器（claude.ai 代码执行）

- **架构**：gVisor 容器 + 隔离基础设施，文件系统按会话 ephemeral（会话结束即销毁）
- **威胁模型**：保护平台基础设施和各租户之间的隔离，非保护用户本地机器
- **关键经验**：最弱的层往往是你自己造的那层。gVisor 和 seccomp 经历了比 AI Agent长得多的安全审计，自研 proxy 才是高风险点

### 模式 2：人在回路沙箱（Claude Code）

- **初始方案**：读取无需审批，写入/bash/网络需要审批
- **Approval Fatigue 问题**：遥测显示用户批准率约 93%，随着审批次数增加注意力急剧下降
- **OS 级 Sandbox**：macOS 用 Seatbelt，Linux 用 bubblewrap，读取允许，写入限定在 workspace 内，网络默认拒绝。效果：Permission prompts 减少 **84%**，runtime 已[开源](https://github.com/anthropic-experimental/sandbox-runtime)

#### 两个被忽略的风险

**1. 信任对话框之前的代码执行**

2025 年中至 2026 年 1 月，发现多个 0click 漏洞：项目目录中的 `.claude/settings.json` hook 在用户接受"是否信任此目录"对话框**之前**就已执行。修复原则：**将 project-open、config-load、localhost listener 视为来自互联网的入站请求**，在用户明确同意之前绝不解析/执行项目本地配置。

**2. 用户作为注入向量**

2026 年 2 月红队演练中，研究员成功用钓鱼邮件让员工启动 Claude Code 执行恶意 prompt（读取 `~/.aws/credentials` 并 POST 到外部）。25 次尝试中 24 次成功完成渗透。

关键发现：**当攻击指令经由用户键盘输入时，模型层分类器无法检测**——因为用户输入本身就是"正常意图"的信号。

唯一有效的防御：出口控制（无论如何意图都阻止 POST）+ 文件系统边界（`~/.aws` 根本不可达）。

> 讽刺插曲：内部 Slack 讨论此 payload 时，有同事指出某些内部 Agent 会读取 Slack。payload 现在变成了环境中的"金丝雀"。在 Agent 读取一切的世界里，调查工具本身也是攻击面。

### 模式 3：本地虚拟机（Claude Cowork）

- **定位**：面向非技术知识工作者，无法依赖其判断 bash 命令的风险
- **架构**：完整虚拟机（macOS 用 Apple Virtualization Framework，Windows 用 HCS）
  - VM 有独立 Linux 内核、文件系统、进程表
  - 用户选定的 workspace 和 .claude 文件夹通过 mount 引入，宿主机其他内容完全不可见
  - 凭证留在宿主机的 keychain，从不进入 guest
- **演进**：原版 agent loop 在 guest 内部，任何 VM 启动失败 = Cowork 完全不可用。改为 host 模式（agent loop 在宿主机，代码执行仍在 VM 内）提升可靠性，同时保持文件系统和网络控制的安全保证
- **文件系统模式**：提供 read-only、read-write、read-write-no-delete 三种 mount 模式。**注意**：symlink 解析必须在路径验证之前，否则符号链接可穿透授权目录

---

## 关键工程结论

1. **OS 级 sandbox 比 permission prompts 更可靠**：Seatbelt/bubblewrap 将安全边界从"用户注意力"中解耦，eliminate approval fatigue
2. **环境层是最后防线**：当用户本身是攻击向量时，模型层完全失效
3. **防御必须重叠**：环境层失效时模型层顶上，模型层不足时环境层兜底
4. **配置加载是隐形攻击面**：本地配置文件在信任边界建立之前被解析，是最常见的 0click 路径
5. **对称性原则**：如果一个组件不受信任，就不要给它例外权限的逃生舱

---

## 相关资源

- [Sandbox Runtime（开源）](https://github.com/anthropic-experimental/sandbox-runtime)
- [Claude Code auto mode：自动化更安全的审批](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Measuring Agent Autonomy](https://www.anthropic.com/news/measuring-agent-autonomy)