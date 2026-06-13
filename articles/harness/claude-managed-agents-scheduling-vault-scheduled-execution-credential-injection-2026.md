# Claude Managed Agents 新特性：定时执行与凭据保险库

> **本文来源**：Claude Blog - "[New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults](https://claude.com/blog/whats-new-in-claude-managed-agents)"（2026年6月9日）
>
> **核心论点**：定时执行和凭据保险库是 Managed Agent Harness 进化的两个关键维度——前者解决了"谁来触发长期任务"的问题，后者解决了"如何安全注入敏感凭据"的问题。两者共同构成了生产级 Agent 的时间与安全基础设施。

---

## 一、定时执行：让 Agent 获得"时间感知"

传统 Agent 交互模型是**请求-响应**式的：用户发起，Agent 执行，结果返回。但生产环境中的许多任务需要**时间维度**：

- 每日数据同步
- 定时健康检查
- 周期性报告生成
- 定时告警响应

Claude Managed Agents 现在支持按 schedule 触发执行。这意味着 Agent 不再只能被动等待用户请求，而是可以主动在预定时间点启动任务。

笔者认为，这看似是一个"调度功能"，实际上是 Agent 从"工具"向"服务"转变的关键一步。当 Agent 能够按时间计划执行任务，它就不再只是人类的即时助手，而是可以承担**周期性职责**的数字员工。

---

## 二、凭据保险库：安全注入的工程范式

凭据管理是 Agent 工程中的持久难题。Agent 需要访问各种外部服务：

- MCP 服务器的 OAuth 令牌
- API 的 Bearer Token
- 数据库连接字符串
- 第三方服务的认证凭据

传统做法是将凭据硬编码在提示词或配置文件中，这带来两个问题：

1. **安全风险**：凭据暴露在代码仓库中
2. **复用困难**：不同 Agent 无法共享凭据基础设施

Claude Managed Agents 的 Vault 机制提供了解决方案。根据官方文档，Vault 支持两种凭据类型：

| 凭据类型 | 说明 | 注入方式 |
|---------|------|---------|
| `mcp_oauth` / `static_bearer` | MCP 服务器认证凭据 | 运行时自动注入到对应 MCP Server URL |
| `environment_variable` | 环境变量形式的密钥 | 按名称注入，供 Agent 运行时访问 |

关键设计：**按名称键入，按 URL/用途匹配**。Agent 连接 MCP Server 时，令牌自动注入，无需在提示词中暴露。这种"上下文解耦"设计让凭据管理从 Agent 逻辑中分离出来，单独维护。

---

## 三、定时 + 凭据 = 生产级 Agent 的基础组件

将定时执行和凭据保险库组合在一起，我们得到一个生产级 Agent 的基础运行模型：

```
[定时触发器] → [Agent 上下文加载] → [Vault 凭据注入] → [任务执行] → [结果输出]
```

这个模型解决了三个生产级问题：

1. **谁来触发**：Schedule 解决了被动等待问题
2. **如何认证**：Vault 解决了凭据安全问题
3. **如何传递**：上下文加载解决了状态恢复问题

---

## 四、与传统 Harness 组件的对比

| 组件 | 解决的问题 | Claude Managed Agents 实现 |
|------|----------|--------------------------|
| 定时触发 | 被动→主动 | Schedule 配置 |
| 凭据注入 | 安全访问外部服务 | Vault 机制 |
| 上下文传递 | 跨会话状态恢复 | 上下文加载 |
| Sandbox | 隔离执行 | 自托管 Sandbox |

---

## 五、笔者的判断

**定时执行和 Vault 是一对互补的基础设施**：定时解决"何时干"，Vault 解决"如何安全地干"。两者单独看都不复杂，但组合在一起，就构成了生产级 Agent 的最小运行集。

对于构建长期运行任务的开发者而言，笔者建议优先关注这两个能力的集成：

1. 如果你的 Agent 需要定期执行任务，Schedule 是必须集成的
2. 如果你的 Agent 需要访问外部服务，Vault 是必须集成的

这两个能力让 Agent 从"被召唤的工具"进化为"有职责的员工"——这是 Harness Engineering 在 2026 年的重要演进方向。

---

**引用来源**：

1. Claude Blog - "[New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults](https://claude.com/blog/whats-new-in-claude-managed-agents)"（2026-06-09）
2. Claude Platform Docs - "[Authenticate with vaults](https://platform.claude.com/docs/en/managed-agents/vaults)"