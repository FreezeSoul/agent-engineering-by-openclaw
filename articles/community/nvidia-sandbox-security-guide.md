# NVIDIA AI Red Team: Practical Security Guidance for Sandboxing Agentic Workflows

> 来源：NVIDIA Developer Blog
> 评分：4.5/5（实践 5 / 独特 4 / 质量 5）
> 关联 FSIO 文章：智能体设计思考（四）：Agent 与 Sandbox 的集成架构

## 核心威胁：间接 Prompt Injection

AI 编码 Agent 通过命令行执行工具，拥有与用户相同的权限——这使得它们成为"计算机使用 Agent"，风险巨大。

**攻击向量**：
- 恶意仓库或 PR
- 含 prompt injection 的 git 历史
- .cursorrules、CLAUDE/AGENT.md 文件中的恶意 MCP 响应

**后果**：LLM 执行攻击者影响的行为

## 必须实施的安全控制

### 强制控制（Mandatory）

| 控制项 | 作用 |
|--------|------|
| **网络出口控制** | 阻止任意站点访问，防止数据泄露或建立远程 shell |
| **阻止工作区外的文件写入** | 防止持久化、沙箱逃逸、RCE |
| **阻止配置文件写入** | 防止 hooks、skills、MCP 配置被利用 |

### 建议控制（Recommended）

| 控制项 | 作用 |
|--------|------|
| 阻止工作区外的文件读取 | 限制主机枚举 |
| 整个 IDE 和衍生函数沙箱化 | 以独立用户身份运行 |
| 使用虚拟化隔离 | microVM、Kata Container、Full VM |
| 敏感操作需用户审批 | 禁止 allow-once/run-many |
| 密钥注入方案 | 防止环境变量中的密钥泄露 |
| 生命周期管理 | 防止代码/IP/密钥积累 |

## 为什么必须 OS 层控制

Agent 工具执行任意代码是设计如此。应用层控制会在工具调用和参数传递时拦截，但一旦控制权传给子进程，应用层就失去可视性和控制。

**OS 层控制（如 macOS Seatbelt）**工作在应用层之下，覆盖沙箱中的每个进程，无论如何启动，都能阻止它们访问危险系统能力。

## 关键洞察

> "No matter how these processes start, they're kept from reaching risky system capabilities, even through indirect paths."

## 另一个问题：习惯化风险

用户审批是最常见风险管理方式，但：
- 持续开发者摩擦
- 用户可能习惯性地批准潜在风险操作而不审查

**核心需求**：在人工输入和自动化之间找到平衡。

## 一句话总结

> NVIDIA AI Red Team 实录：三大强制控制（网络出口/工作区写限制/配置写阻止）+ OS 层沙箱——应用层不够用，必须到内核。

## 原文

https://developer.nvidia.com/blog/practical-security-guidance-for-sandboxing-agentic-workflows-and-managing-execution-risk/

## 标签

#community #sandbox #security #NVIDIA #prompt-injection #agent-security
