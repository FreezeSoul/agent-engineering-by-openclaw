# TracecatHQ/tracecat：让 AI Agent 安全跑在生产环境的安全编排平台

**这篇文章要回答的问题是**：当企业想把 AI Agent 集成到安全运营流程中时，需要什么样的基础设施——以及为什么 Tracecat 把「安全沙箱 + MCP + Temporal 持久化工作流 + 人工审批」这些能力融合在一起的架构，是目前最完整的开源方案。

---

## 背景：安全运营中的 AI Agent 需要什么

在 OpenAI Daybreak 的案例中，Codex Security 的评估器循环展现了 AI Agent 在安全漏洞发现和修复中的巨大潜力。但把同样的能力搬到企业安全运营环境里，需要的不只是一个 Agent，而是一整套**安全基础设施**：

- **沙箱隔离**：Agent 执行的动作不能直接影响生产系统
- **持久化工作流**：安全事件响应通常是跨小时的复杂流程，不能因为网络中断而中断
- **MCP 集成**：企业安全工具链多样（SIEM、SOAR、漏洞扫描器），需要一个统一的协议来连接
- **人工审批节点**：关键操作（封锁账户、隔离主机）必须有人类确认才能执行
- **审计日志**：所有 Agent 操作必须可追溯，满足合规要求

这正是 Tracecat 试图解决的核心问题。

---

## 核心能力解析

### Prompt-to-Automation：把自然语言变成可执行工作流

Tracecat 提供了 MCP 服务器，支持通过 Claude Code、Codex、Copilot 等主流 Coding Agent 直接触发安全自动化工作流。官方 README 明确说：

> *"Tracecat MCP: turns prompts into automations through Claude Code, Codex, Copilot, etc."*

这意味着安全工程师可以用自然语言描述一个响应剧本，Tracecat 将其转化为可执行的 Workflow。与传统 SOAR（Security Orchestration, Automation and Response）平台不同，Tracecat 的 Workflow 是**持久化的**——基于 Temporal 构建，即使进程重启也能从断点恢复。

### 安全沙箱：让 Agent 动作在可控范围内执行

Tracecat 使用 **nsjail** 实现沙箱隔离。沙箱在安全 Agent 中的作用，和 Daybreak 中 Codex Security 的验证阶段类似：确保 Agent 的输出（补丁、操作指令）在被采纳前，经过了安全边界的验证。

> *"Sandboxed-by-default with nsjail and run on Temporal for security, reliability, and scale."*

这里有一个有趣的对比：Daybreak 的验证器（GPT-5.5-Cyber）是模型层面的验证，而 Tracecat 的沙箱是执行层面的隔离。两者解决的是不同层次的风险——模型可能生成看似正确但实际有问题的补丁，沙箱则确保即便 Agent 被攻击者诱导，执行的影响范围也是有限的。

### 100+ 预置集成：MCP 作为协议层

Tracecat 提供了 100+ 预置的 MCP 服务器，覆盖主流安全工具：

- HTTP/SMTP/gRPC/OAuth 协议连接各种企业安全工具
- 自定义 MCP 客户端可以连接任何 MCP 兼容的服务器
- 自定义注册表允许将 Python 脚本转化为 Agent 工具

这个集成层的意义在于：它把「安全 Agent」从单点工具变成了**平台**。企业不需要为每个安全场景单独训练 Agent，而是可以在统一平台上组合不同的工具和 Agent。

### 人工审批节点（Human-in-the-loop）

关键安全操作（隔离主机、封锁账户、变更防火墙规则）必须有人类确认才能执行。Tracecat 的审批机制支持：

- 统一收件箱审批
- Slack/邮件通知审批
- 细粒度 RBAC/ABAC/OAuth2.0 权限控制

这与 Daybreak 中 "human oversight" 的设计哲学一致：在自动化和安全之间，找到人类必须介入的那个精确节点。

---

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Tracecat 技术栈                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  前端：Next.js + TypeScript + React Query + Shadcn UI       │
│  后端：Python + FastAPI + SQLAlchemy + Pydantic + uv        │
│  工作流引擎：Temporal（持久化、容错）                         │
│  沙箱：nsjail（进程级隔离）                                  │
│  数据库：PostgreSQL                                         │
│  对象存储：S3 兼容                                          │
│  协议：MCP（Model Context Protocol）                         │
│  部署：Docker / AWS Fargate / Kubernetes Helm / 云托管        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Tracecat × Daybreak 主题关联                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Daybreak（OpenAI）：                                        │
│  • Codex Security = 执行 Agent                              │
│  • GPT-5.5-Cyber = 验证 Agent                              │
│  • 评估器循环在单次任务内完成                                 │
│                                                             │
│  Tracecat（企业版）：                                        │
│  • 任意 Coding Agent（Claude Code/Codex）= 执行 Agent       │
│  • nsjail 沙箱 = 执行边界验证                                │
│  • Temporal 工作流 = 跨会话持久化                           │
│  • 人工审批节点 = 人类在环                                    │
│  • 评估器循环在企业工作流中完成                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 与同类项目的对比

| 维度 | Tracecat | OpenAI Daybreak | 西门子/传统 SOAR |
|------|---------|-----------------|----------------|
| **定位** | 开源安全自动化平台 | 商业漏洞发现/修复服务 | 企业级安全编排 |
| **Agent 集成** | MCP 兼容多 Agent | 单一 OpenAI Agent | 通常无 Agent |
| **工作流持久化** | Temporal（跨会话恢复）| 单次评估循环 | 脚本/流程图 |
| **沙箱** | nsjail | 无（API 调用）| 无 |
| **人工审批** | 完整（RBAC + 通知）| 最小化 | 完整 |
| **部署方式** | 自托管/云托管 | SaaS | 本地 |
| **开源** | ✅（AGPL-3.0） | ❌ | ❌ |

---

## 适用场景

Tracecat 特别适合以下场景：

1. **安全运营中心（SOC）自动化**：把重复性的安全响应剧本自动化，减少分析师手动操作
2. **AI Agent 安全集成**：在企业环境中安全地引入 Coding Agent 处理安全任务
3. **合规审计**：所有 Agent 操作有完整审计日志，支持导出到 SIEM
4. **跨团队安全协作**：工作流跨越安全、开发、运维多个团队，需要持久化和审批节点

---

## 局限性

- **v0.x 版本**：产品仍在活跃开发中，升级前需要审查 changelog
- **没有内置漏洞发现能力**：与 Daybreak/Codex Security 的漏洞发现不同，Tracecat 更像是把已有的安全工具连接起来
- **AGPL-3.0 许可**：如果需要闭源集成，需要考虑许可兼容性问题

---

**核心结论**：Tracecat 填补了「让 AI Agent 安全地跑在企业安全运营流程中」这个空白。它不是另一个漏洞扫描器，而是**安全运营的 Agent 操作系统**——通过 MCP 集成任意 Agent、通过 Temporal 实现持久化工作流、通过 nsjail 隔离执行、通过人工审批节点保留人类决策权。这套组合与 OpenAI Daybreak 的设计哲学高度一致：在自动化和人工控制之间，找到精确的平衡点。
