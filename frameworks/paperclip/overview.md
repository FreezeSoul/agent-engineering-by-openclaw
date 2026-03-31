# Paperclip — Company OS for Zero-Human AI Teams

> Paperclip is the company layer that turns a pile of agents into a coordinated organization.

---

## 核心概念

Paperclip（[GitHub: paperclipai/paperclip](https://github.com/paperclipai/paperclip)，41.6k ⭐，MIT License）是一个开源的 Node.js + React 平台，专门用于**将多个 AI Agent 组织成一家「零人类公司」**运营。

Paperclip 解决的不是「如何构建单个 Agent」，而是「如何让多个 Agent 像公司一样协调工作」。它的核心定位是：**If OpenClaw is an employee, Paperclip is the company**。

### 核心理念：AI agents need a company, not just a prompt

当同时运行的 Agent 数量从 1 扩展到 20 时，传统的 Agent 管理方式全面崩溃：
- 20 个 Claude Code 标签页同时运行，你分不清谁在做什么
- 重启后所有上下文丢失
- 成本没有上限，API 账单一夜之间爆掉
- 定期任务（客服、社交媒体、数据报告）需要人工手动触发

Paperclip 将公司管理机制引入 Agent 编排：**Org Chart → Goal Alignment → Ticket System → Budget Control → Governance → Audit Trail**。

---

## 核心架构

### 三步启动一家 AI 公司

| 步骤 | 描述 | 示例 |
|------|------|------|
| **01** | Define the goal | _「将 AI 笔记应用做到 $1M ARR」_ |
| **02** | Hire the team | CEO、CTO、工程师、设计师、营销——任意 Agent，任意 Provider |
| **03** | Approve and run | 审批策略，设定预算，启动，从 Dashboard 监控 |

### 支持的 Agent Adapter

Paperclip 不绑定特定 Agent 实现，通过 **Adapter 模式** 接入任意 Agent：

| Adapter | 说明 |
|---------|------|
| OpenClaw | OpenClaw Gateway（本地/云端）|
| Claude Code | Anthropic 官方 CLI Agent |
| Codex | OpenAI Coding Agent |
| Cursor | Cursor AI IDE 内置 Agent |
| Bash | 本地命令行 Agent |
| HTTP | 任意支持 HTTP API 的 Agent |
| Hermes | Hermes CLI（新增）|
| Pi | Pi AI Agent（新增）|
| OpenCode | 开源 Coding Agent（新增）|

> _「If it can receive a heartbeat, it's hired.」_

### 核心功能模块

| 模块 | 功能 | 对应公司机制 |
|------|------|------------|
| **Org Chart** | Agent 层级结构、角色、汇报线 | 组织架构图 |
| **Goal Alignment** | 任务携带完整目标祖先链，Agent 始终知道「为什么做」 | 战略解码 |
| **Heartbeats** | Agent 按计划唤醒，检查工作，执行任务 | 工作日志 |
| **Cost Control** | 每个 Agent 设月度预算，超额自动停止 | 财务管理 |
| **Ticket System** | 每条对话可追踪，每项决策有解释，完整工具调用日志 | 工单系统 |
| **Governance** | 人类作为「董事会」，审批招聘、否决策略、暂停/终止任意 Agent | 公司治理 |
| **Multi-Company** | 单实例运行多家公司，数据完全隔离 | 控股集团 |
| **Company Skills Library** | 运行时向 Agent 注入新技能，无需重新训练 | 员工培训 |

---

## 工程特性

### 正确处理的编排细节

| 特性 | 说明 |
|------|------|
| **Atomic Execution** | 任务检出和预算执行是原子的，无双重执行，无超支 |
| **Persistent Agent State** | Agent 在不同 Heartbeat 之间恢复同一任务上下文，而非从头开始 |
| **Runtime Skill Injection** | Agent 在运行时学习 Paperclip 工作流和项目上下文，无需重新训练 |
| **Governance with Rollback** | 审批门强制执行，配置变更版本化，错误变更可安全回滚 |
| **Goal-Aware Execution** | 任务携带完整目标祖先，Agent 始终理解「为什么」，不只是任务标题 |
| **Portable Company Templates** | 导出/导入组织、Agent 和技能，带密钥清理和冲突处理 |
| **True Multi-Company Isolation** | 每个实体都是公司范围的，一个部署可运行多家独立公司和审计日志 |

---

## 快速开始

```bash
# 最简启动（一行命令 onboard）
npx paperclipai onboard --yes

# 或手动
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
# 启动后访问 http://localhost:3100
# 嵌入式 PostgreSQL 自动创建，无需手动配置
```

> **要求**：Node.js 20+，pnpm 9.15+

---

## 与其他编排范式的区别

Paperclip 刻意不是以下工具：

| 不是 | 原因 |
|------|------|
| **LangGraph / CrewAI / AutoGen** | 这些是工作流/多 Agent 框架，Paperclip 是公司管理层 |
| **Zapier / n8n** | 拖拽式流程构建器，Paperclip 用组织模型（Org Chart + Goals + Budgets + Governance）|
| **Prompt Manager** | Agent 带来自己的 Prompts，Paperclip 管理 Agent 所在组织的运行方式 |
| **Chatbot** | Agent 有工作，不是有聊天窗口 |
| **Single-Agent Tool** | 如果你只有 1 个 Agent，你不需要 Paperclip；如果有 20 个，你绝对需要 |
| **PR Review Tool** | Paperclip 编排工作，不是审查 Pull Request |

---

## 治理 UX：30 秒内做出决策

Paperclip 提出的一个关键 UX 问题是：

> _「How do you give a human enough context to make a governance decision about an agent's work in under 30 seconds?」_

这不是传统的「如何引导用户完成流程」的设计问题，而是：**如何让人类在 30 秒内获得足够的上下文来审批一个 Agent 的战略决策**。

Paperclip 的解法：
- **Goal Alignment Auditor Agent**：定期审查所有活跃任务，标记任何偏离父目标的子目标
- **Ticket + Audit Trail**：每项决策的完整上下文可追溯
- **Governance Gate**：Agent 无法自主做出重大决策，必须人类审批

---

## 定位：演进路径中的位置

Paperclip 处于 **Stage 7（Orchestration）→ Stage 9（Multi-Agent）** 的交叉地带：

- **Stage 7（Orchestration）**：提供了比 LangGraph/CrewAI 更高的抽象——不是编排任务流程，而是编排整个组织的运营
- **Stage 9（Multi-Agent）**：真正实现了 Agent Team 的组织化——Org Chart + 汇报线 + 预算 + 治理

**演进链**：LangGraph（Cyclic Graph） → CrewAI（Role-Based Team） → Paperclip（Company OS）

Paperclip 的出现代表了 Multi-Agent 领域的一个新阶段：**从「如何让多个 Agent 协作完成一个任务」，到「如何让多个 Agent 像公司一样自主运营」**。

---

## 学习资源

| 资源 | 链接 |
|------|------|
| GitHub | https://github.com/paperclipai/paperclip |
| 官方文档 | https://paperclip.ing/docs |
| Discord | https://discord.gg/m4HZY7xNG3 |
| 视频演示 | GitHub user-attachments |
| 社区：Zero-Human Company Book | https://github.com/AnthonyDavidAdams/zero-employee-company-book |

---

*最后更新：2026-03-31*
