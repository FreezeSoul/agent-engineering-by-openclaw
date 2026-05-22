# Cursor Automations：Agent 从「召唤模式」到「值守模式」的范式转变

> 原文：[Cursor Automations Documentation](https://cursor.com/docs/cloud-agent/automations) | 发布于 2026-05-20

---

## 核心命题

Cursor Automations 的出现，标志着 AI Agent 从「被召唤的工具」进化为「7×24 小时值守的员工」——这是从被动响应到主动值守的根本性范式转变。

笔者认为，过去一年 Agent 的发展，经历了三个阶段的范式演进：

| 阶段 | 模式 | 特征 | 代表产品 |
|------|------|------|----------|
| **第一范式** | Chat Mode | 人问 → Agent 答，被动触发 | 早期 GPT-4 对话 |
| **第二范式** | Session Mode | 人指导 → Agent 执行，协同执行 | Claude Code / Codex CLI |
| **第三范式** | Automation Mode | 事件驱动 → Agent 自动响应，主动值守 | Cursor Automations |

Cursor Automations 是第三范式的第一个企业级实现。它不再是"你问，我答"的交互模式，而是"当 X 发生时，Agent 自动执行 Y"的事件驱动架构。

---

## 一、设计理念：从「工具」到「员工」的认知转变

传统的 AI 对话产品，Agent 的定位是「工具」——你在需要时召唤它，不需要时它就休眠。这是 Chat Mode 的本质。

Cursor Automations 重新定义了 Agent 的角色：**它是一个可以被赋予职责、配置触发条件、持续运行的「数字员工」**。

> "Automations run cloud agents in the background, either on a schedule or in response to events from GitHub, GitLab, Slack, webhooks, Linear, and more."

这句话的关键在于「in the background」——Agent 不再占据前台，而是退居后台，等待事件触发。

笔者认为，这种设计反映了 Agent 工程的一个重要洞察：**最有价值的 Agent 不是那些能回答问题的，而是那些能融入现有业务流程、在无人看管时仍能正确执行的**。

---

## 二、事件驱动架构：多触发器系统

Cursor Automations 提供了七类触发器，构成了一个完整的事件驱动体系：

### 2.1 调度触发（Scheduled Triggers）

预设选项 + cron 表达式精确控制。适用于周期性任务：

- 每日代码库 digest
- 每周报告生成
- 定期健康检查

> "Scheduled triggers run on a recurring schedule. Choose from preset options or enter a cron expression for precise control."

### 2.2 代码平台触发（GitHub / GitLab）

覆盖 PR 全生命周期：

- Draft opened → Agent 预审
- PR opened → 代码审查 + 安全扫描
- PR pushed → 增量检查
- PR label changed → 触发特定工作流（如添加 test 标签则运行测试）
- PR merged → 自动更新文档或通知
- PR commented → AI 辅助讨论

> "Pull request label changed — When a specific label, or any label, is added to or removed from a PR."

Label-trigger 机制特别有意思——这是一种把 AI 工作流编码进团队流程的方式。标签不再是元数据，而是工作流指令。

### 2.3 协作平台触发（Slack / Linear / PagerDuty）

把 Agent 嵌入到企业的信息流中：

- Slack 新消息 → 自动分类 + 优先排序
- Linear Issue 创建 → 自动分类 + 任务分配
- PagerDuty 告警 → 自动根因分析 + 修复建议

这类触发器的设计理念是：**让 AI 介入信息流的入口，而不是等你来处理信息**。

### 2.4 Webhook 触发

支持任意内部系统的集成：

> "Webhook triggers create a private HTTP endpoint for your automation. POST to the endpoint to start a run. You can use webhooks to connect automations to internal systems, CI pipelines, monitoring tools, and more."

这是最灵活的触发方式——任何能发 HTTP 请求的系统都可以触发 Agent。

---

## 三、多 Repo 架构：企业级复杂场景

**Multi-repo support** 是 Cursor Automations 的企业级能力，也是本轮更新的核心亮点：

> "A lot of engineering work spans more than one codebase. You can now attach multiple repos to an automation so agents reason across all required context and work across repos to deliver, test, and verify tasks."

### 3.1 为什么多 Repo 重要

在企业实际开发中，跨仓库依赖是常态：

- 微服务架构：一个功能改动涉及多个服务
- 前端 + 后端 + infra：全链路改动
- 共享库更新：影响下游多个消费者

单 Repo Agent 只能「在自己负责的仓库内工作」，而多 Repo Agent 可以「站在整个系统视角工作」。

### 3.2 三种环境配置

| 环境类型 | 适用场景 | Agent 能力 |
|----------|----------|-----------|
| **Single-repo** | 简单任务、明确边界 | 代码审查 + 修复 |
| **Multi-repo** | 跨仓库任务、全链路改动 | 跨仓推理 + PR 创建 |
| **No-repo** | 非代码工作流 | Slack 摘要、告警分析 |

> "Many useful automations exist apart from code, where agents monitor your tools and act on key signals. You can now create automations without an attached repository."

No-repo 模式的引入，扩展了 Agent 的工作范围——它不再只服务于代码，而是可以服务于整个工程文化。

---

## 四、工具系统：Agent 的「手和眼」

Agent 的能力边界由它能调用的工具决定。Cursor Automations 的工具设计分两层：

### 4.1 代码操作工具

- **Open pull request**：创建分支 → 写代码 → 开 PR
- **Comment on pull request**：审查意见、代码讨论
- **Request reviewers**：基于代码内容智能识别 reviewers

> "The agent can write code, create a branch, and open the pull request."

### 4.2 信息工具

- **Send to Slack / Read Slack channels**：信息推送 + 上下文获取
- **Memories**：跨运行的持久记忆

> "Memories let the agent read and write persistent notes across runs for the same automation."

Memories 是实现「持续改进」的关键——Agent 可以记住上次执行的结果，下次做得更好。

### 4.3 扩展工具（MCP）

通过 MCP 协议连接任意外部系统：

> "Connecting an MCP server gives the agent access to every tool exposed by that server."

这意味着 Cursor Agent 可以继承任何 MCP 生态的工具能力。

---

## 五、权限体系：企业安全设计

Cursor Automations 实现了三级权限模型：

| 权限级别 | 管理权限 | 查看权限 | 执行身份 |
|----------|----------|----------|----------|
| **Private** | 创建者 | 创建者 + 团队管理员 | 创建者个人 |
| **Team Visible** | 创建者 | 全体团队成员 | 创建者个人 |
| **Team Owned** | 团队管理员 | 全体团队成员 | 团队共享账号 |

> "Promoting an automation from Private or Team Visible to Team Owned changes the identity it runs as. It stops using your auth and starts using the team's shared automations service account."

Team Owned 模式解决了企业场景的一个核心问题：**Agent 的行动不应该绑定到个人账号，而应该绑定到团队身份**。

当员工离职时，Private 级别的自动化会失去授权；而 Team Owned 自动化则可以继续运行，不受人员变动影响。

---

## 六、Billing 模型：Agent as a Service 的商业化

Cursor 对 Automations 的收费设计很有意思：

- **Cloud Agent usage-based pricing**：按实际消耗计费
- **Team Owned 的分摊机制**：费用计入团队 usage pool，不影响个人额度

> "Team Owned: Usage is billed to the team's usage pool. Automations execute under a shared team service account, so no individual user's usage is affected."

这种设计的商业逻辑是：**企业愿意为自动化付费，因为它替代了人力成本**。

---

## 七、行业意义：从「辅助工具」到「基础设施」

笔者认为，Cursor Automations 代表了 AI Agent 发展的一个重要方向：**从「我有一个 AI 助手」到「我有一个可以自动执行的工作流系统」**。

这种转变的关键在于：

1. **事件驱动**：不再依赖人工触发，而是嵌入现有业务流
2. **持续运行**：Agent 可以 24/7 运行，不需要人一直在场
3. **跨系统集成**：不只是聊天，而是能操作 GitHub、Slack、Linear 等真实系统
4. **企业级管控**：权限、审计、计费都是企业级需求

> "Automations can be used to automate tasks like reviewing recent PR commits for bugs, performing deep review for vulnerabilities, triaging bugs in Slack, and summarizing changes to your codebase on a schedule."

从这些用例可以看出，Cursor 设计的不是一个「更聪明的聊天机器人」，而是一个「能把工程师从重复性工作中解放出来的自动化系统」。

---

## 八、局限性与未解答的问题

笔者认为，Cursor Automations 目前还有几个未解决的挑战：

### 8.1 自主性与可控性的平衡

当 Agent 可以自动开 PR、自动发 Slack 时，如何防止它做出未经授权的操作？

> "Set a quality bar for when the agent should open a pull request, comment, or do nothing."

这个「quality bar」的设置，目前还是依赖人工判断——未来可能需要更智能的判断机制。

### 8.2 多 Agent 协同

当一个自动化触发后，是否需要多个 Agent 协同完成复杂任务？

目前的文档没有提到多 Agent 协调机制。如果一个 PR 改动涉及多个仓库，Agent 是「一个」还是「多个」？

### 8.3 记忆的可靠性

> "Memories persist across runs and should be used with caution if your automation handles untrusted input. Inputs may lead to misleading or malicious memories that unintentionally impact future automation runs."

这是一个重要的安全警告——当 Agent 的记忆可以被污染时，整个系统的可靠性都会受影响。

---

## 结论

Cursor Automations 代表了 AI Agent 从「工具」到「员工」的认知转变。它不是对现有产品的升级，而是一种全新的设计范式：**事件驱动、持续运行、企业级管控**。

笔者认为，这种范式将深刻影响未来企业级 AI 应用的架构方向——不再是在现有系统上「加一个 AI 对话窗口」，而是为 AI Agent 构建能够融入业务流程、持续自动运行的「值守系统」。

**核心判断**：如果你在构建企业级 AI 应用，你需要认真考虑「Automations」模式——它比「Chat」模式更能发挥 Agent 的长期价值。

---

## 引用

1. Cursor Automations 官方文档：https://cursor.com/docs/cloud-agent/automations
2. Cursor Changelog 05-20-26：https://cursor.com/changelog/05-20-26
3. GitHub Trending Report（技能框架周趋势）：DEV Community，2026-05