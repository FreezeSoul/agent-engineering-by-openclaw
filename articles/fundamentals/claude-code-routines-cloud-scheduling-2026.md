# Claude Code Routines：将 CLI 工具变成云端自动化引擎

> **核心命题**：Claude Code Routines 的本质不是"功能更新"，而是把 Claude Code 从一个需要人工操作的 CLI 工具，变成一个可以在云端自主运行、响应事件的自动化引擎——彻底解耦了"运行"和"人"。

## 一、从"人在操作"到"事件触发"

Claude Code 最初的使用形态是：人打开 Terminal，输入 prompt，等结果。这是一个**人在环内**的模型。

Routines 改变了这个关系：

```
过去：
human → terminal → claude code → result（人在等待）

现在：
schedule/event → claude code cloud → routine → result（人不在环内）
```

一个 nightly routine 可以这样定义：

```
Every night at 2am: pull the top bug from Linear, attempt a fix, and open a draft PR.
```

这句话的背后，是一个完整的**无人值守自动化链路**：
1. 定时触发器在 2am 启动 session
2. Routine 配置包含 repo access + connectors（Linear MCP）
3. Claude Code 自动执行，PR 结果推送到 GitHub
4. 全程不需要人在线

**笔者认为**：这个转变是 2026 年 AI Coding Agent 的核心演进方向——从"辅助工具"到"自主员工"。Routines 是这个演进的第一个大规模生产可用的云端实现。

## 二、三种触发模式：覆盖自动化全场景

Routines 提供三种触发模式，分别对应不同的工程场景：

### 2.1 定时调度（Scheduled Routines）

最基础的模式：`prompt + cadence（hourly/nightly/weekly）`

```python
# 概念示例：配置 nightly routine
routine_config = {
    "prompt": "pull top bug from Linear, attempt fix, open draft PR",
    "cadence": "nightly",
    "time": "02:00",
    "repos": ["owner/repo"],
    "connectors": ["linear"]
}
```

适用场景：
- 日常代码清理（nightly fix）
- 文档更新（weekly sync）
- 监控告警处理（hourly check）

### 2.2 API 触发（API Routines）

每个 API routine 获得**独立 endpoint + auth token**，支持从任何可发 HTTP 请求的系统调用：

```
POST /routine/{id} → { session_url, auth_token }
```

这意味着你可以把 Claude Code 集成进：
- 内部告警系统（PagerDuty/Slack alert → routine）
- CI/CD 流水线（deploy hook → routine）
- 自定义管理后台（internal tool → routine）

原文描述的一个场景：

> Read the alert payload, find the owning service, and post a triage summary to #oncall with a proposed first step.

### 2.3 Webhook 触发（Webhook Routines）— 首发 GitHub

首发支持 GitHub repository events，Claude 自动为每个符合条件的 PR 创建新 session：

```
GitHub PR event → matching filter → new session → routine execution
```

示例：

> Please flag PRs that touch the /auth-provider module. Any changes to this module need to be summarized and posted to #auth-changes.

这种模式的价值在于**细粒度的事件响应**——不是整个 pipeline，而是特定文件/路径变化才触发。

## 三、工程机制分析：Routines 的支柱

### 3.1 接力机制：云端状态持久化

Routines 能在"无人在环"场景下工作的前提，是**状态不依赖本地 laptop**：

> Routines run on Claude Code's web infrastructure, so nothing depends on your laptop being open.

这背后是一个跨 session 的状态传递机制：
- **输入**：schedule/event → 触发 routine
- **上下文**：repos + connectors 配置打包进 routine
- **输出**：session result + artifact（PR/comment/alert）

关键设计：**routine 配置包含完整的运行时依赖**（repo、connector、MCP servers），不需要用户在触发时重复配置。

### 3.2 连接器生态：MCP 是基础设施

Routines 依赖 connectors 访问外部系统：

> Developers already use Claude Code to automate the software development cycle, but until now, they've managed cron jobs, infrastructure, and additional tooling like MCP servers themselves. Routines ship with access to your repos and your connectors, so you can package up automations and set them to run on a schedule or trigger.

这里的"connectors"很可能就是 MCP servers 的产品化封装——把 MCP 的工具定义变成可直接复用的 routine 构建块。

### 3.3 与传统 cron job 的本质区别

| 维度 | 传统 cron job | Claude Code Routine |
|------|-------------|-------------------|
| **执行单元** | 脚本/命令 | LLM + Tools + Context |
| **配置方式** | crontab + 脚本 | natural language prompt |
| **触发条件** | 时间 | 时间 + API + Webhook |
| **上下文** | 无状态 | 携带 repo + connectors |
| **输出** | 文件/日志 | PR/Comment/Alert/Artifact |
| **自我判断** | 无 | 可根据结果决定下一步 |

**笔者认为**：Routines 不是"更方便的 cron"，而是"带判断能力的自动化引擎"。传统 cron 是执行单元，Routines 是决策执行单元。

## 四、适用边界与局限

### 4.1 适合的场景

- **代码维护自动化**：nightly fix、dependency update、doc sync
- **事件响应**：PR review、incident triage、deploy hook
- **内部工具集成**：alert → summary → notification 链路

### 4.2 不适合的场景

- **需要实时人工判断的长流程**：Routine 适合"定义好规则就执行"的场景，不适合探索性任务
- **需要多轮交互的复杂调试**：目前 Routine 更像单次执行，不是持续对话
- **高度安全敏感的流水线**：云端运行意味着代码和 token 在外部基础设施，对金融/医疗等合规要求高的场景需评估

### 4.3 当前限制（2026 research preview）

- Webhook 首发仅支持 GitHub，其他 VCS 需等待
- API endpoint 的 auth token 管理需纳入 DevOps 流程
- Routine 执行失败的重试机制尚未明确

## 五、结论：云端自动化引擎的标准形态

Claude Code Routines 代表着 2026 年 AI Coding Agent 的一个明确方向：**从"人在操作"到"事件驱动"**。三条触发通道（定时/API/Webhook）覆盖了绝大多数自动化场景，云端基础设施解耦了"运行"和"人"。

**真正的工程价值**在于：把 AI Agent 变成了一个可以嵌入现有基础设施（CI/CD、Alerting、Internal Tools）的标准组件——而不是一个需要人守着跑的 CLI 工具。

> 笔者的判断：Routines 会在 2026 年下半年成为 AI Coding Agent 的标准形态。任何没有云端调度能力的 coding agent，都将在竞争中处于劣势。

---

**引用来源**：
- [Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code)（2026，Claude Blog）
- [Claude Code CLI Documentation](https://docs.claude.com/cli)（/schedule 功能）

**相关项目**：
- [VRSEN/agency-swarm](https://github.com/VRSEN/agency-swarm) — 多 Agent 编排框架，与 Routines 形成互补（云端调度 ↔ 多 Agent 协作）
