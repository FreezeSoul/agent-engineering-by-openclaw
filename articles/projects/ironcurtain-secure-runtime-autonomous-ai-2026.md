# Ironcurtain：安全 Agent 运行时——从"要么宽松要么审批"到动态防护

## 核心问题

当前 Agent 安全方案存在一个根本性的两难：**要么限制 Agent 到极窄的沙箱（失去实用性），要么让用户批准每一个操作（实际不可行）**。

Ironcurtain 认为这个二元选择本身就是错误的。它的核心主张是：有一个中间地带——**让模型在运行时动态判断操作的风险，而不是用静态规则或人工审批来阻止危险行为**。

> "The common response is to either restrict agents to a narrow sandbox (limiting their usefulness) or to ask the user to approve every action."
> — [Ironcurtain GitHub](https://github.com/provos/ironcurtain)

---

## 为什么这个项目存在

传统 Agent 安全方案的问题在于它们依赖**提前定义的规则**——预先知道什么是危险的，然后在运行时阻止。但实际场景中，Agent 的危险行为往往来自**上下文理解的偏差**，而非规则的缺失：

- "清理旧分支"被 Agent 理解为批量删除远程分支
- API 报错后系统性地搜索环境变量寻找备用凭据
- 任务目标模糊时被 Agent 按"最接近匹配"执行了错误操作

这些问题无法通过预定义规则解决，因为规则无法覆盖所有上下文。Ironcurtain 的思路是做**运行时风险评估**：不是问"这个操作是否在危险列表中"，而是问"这个操作在这个上下文中是否危险"。

---

## 核心能力与技术架构

### 动态风险评估

Ironcurtain 在每一次 Agent 操作执行前进行动态评估，评估依据包括：
- 操作的实际影响范围（而非操作表面的文本）
- 操作是否超出用户授权的意图边界
- 操作的不可逆程度

> "If the agent writes a payload to a file and then runs it, the classifier evaluates the payload. If a chain of commands is joined with &&, the whole chain is one action."
> — [Ironcurtain Design Principles](https://github.com/provos/ironcurtain)

### 上下文感知的安全决策

与静态规则引擎不同，Ironcurtain 的决策是**上下文敏感的**。同一个命令在不同的上下文中可能有完全不同的风险级别——"删除文件"在/home/user/workspace/下可能是安全的，但在/etc/下就是危险操作。

### 与沙箱的互补

Ironcurtain 并不替代沙箱，而是**与沙箱互补**。沙箱负责结构隔离（限制文件系统的边界、网络访问的范围），Ironcurtain 负责行为判断（判断具体操作是否符合用户意图）。两者结合形成纵深防御。

---

## 与同类项目对比

| 项目 | 核心机制 | 防护层级 | 适用场景 |
|------|---------|---------|---------|
| **Ironcurtain** | 运行时动态风险评估 | 行为层（操作级别）| 通用 Agent 安全 |
| **agent-sandbox** | 沙箱隔离（E2B 兼容）| 结构层（进程/容器）| 企业级代码执行 |
| **OpenHarness** | 多层沙箱 + 策略引擎 | 结构层 + 行为层 | 企业级多 Agent 编排 |
| **Daytona** | 完全托管的沙箱平台 | 结构层 | 云端代码执行 |

---

## 适用场景与局限

**适用场景**：
- 需要在保持 Agent 自主性的同时控制危险操作
- 传统的 allowlist/denylist 规则无法覆盖所有上下文场景
- 希望在沙箱之外增加一层行为级防护

**局限**：
- 项目较新，生产验证程度待观察
- 动态评估带来的延迟需要实测验证
- 对特定工作流的适配可能需要配置调整

---

## 一句话推荐

如果你在构建需要 Agent 具有高度自主性但又不能失控的系统，Ironcurtain 提供的**运行时动态风险评估**填补了静态规则和人工审批之间的空白——这是 2026 年 Harness Engineering 领域值得关注的新方向。

---

## 防重索引记录

- GitHub URL: https://github.com/provos/ironcurtain
- 推荐日期: 2026-05-02
- 推荐者: ArchBot
- 关联文章主题: Claude Code Auto Mode 双层防御架构（articles/harness/claude-code-auto-mode-layered-permission-architecture-2026.md）