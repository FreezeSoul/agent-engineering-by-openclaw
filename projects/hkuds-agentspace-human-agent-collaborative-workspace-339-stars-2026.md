# HKUDS/AgentSpace：Human + Agents. One Team. One Workspace

> **项目定位**：Agent 原生协作工作空间 — 把人类与 Agent 的协作从「单点对话」变成「团队协作」
> 
> **收录依据**：AgentRouter 作为 Provider Harness 标准化层，实现跨运行时（Claude Code / Codex / OpenCode / OpenClaw / Hermes）的统一执行调度；与 HKUDS/ClawTeam (5341⭐) 同研究组，Apache-2.0 协议

| 项目 | 值 |
|------|-----|
| **GitHub** | https://github.com/HKUDS/AgentSpace |
| **Stars** | 339 (2026-06-22 创建) |
| **License** | Apache-2.0 |
| **语言** | TypeScript |
| **主页** | https://hire-an-agent.online/ |
| **组织** | HKUDS（香港大学） |

---

## 核心定位

AgentSpace 是一个 **Agent 原生协作工作空间**，解决当前 Agent 框架的核心问题：

> 大多数 Agent 产品面向个人使用设计 — 单人、单终端、单会话。一旦团队尝试将 Agent 纳入日常运营，一切就开始崩溃。

### 当前问题

| 痛点 | AgentSpace 的解法 |
|------|-----------------|
| Agent 处于私有状态 — 存在于个人终端或账户，对团队不可见 | **数字员工看板** — 私有 Agent 在整个组织内可见、可借用、可复用 |
| 上下文分散 — 消息、文档、审批、截图和运行时文件散落各处 | **共享工作空间** — 人与 Agent 共用同一操作上下文 |
| 执行碎片化 — 每个 Provider 有自己的 CLI 行为、会话模型和诊断 | **AgentRouter** — 统一标准化所有 Harness 的事件、会话、输出和诊断 |
| 治理缺失 — 凭证、文档、运行时访问、工具调用和出站操作几乎无法统一审视 | **权限控制平面** — 集中管理授权、审批、委托和审计跟踪 |

---

## AgentRouter：Provider Harness 标准化层

AgentRouter 是 AgentSpace 的**核心抽象**，它不替换工作空间，也不拥有业务队列，而是：

1. 启动不同的 Agent CLI
2. 标准化事件、结果、会话和诊断

### 支持的运行时

| Provider | 执行路径 | 诊断能力 |
|----------|---------|---------|
| **Claude Code** | AgentRouter | stream-json events, session fallback, tool approval bridge |
| **Codex CLI** | AgentRouter | JSON events, session fallback, runtime tool capability diagnostics |
| **OpenCode** | AgentRouter | JSON events, session propagation, timeout/nonzero/empty diagnostics |
| **OpenClaw** | AgentRouter | health/preflight, auth/profile/model/tool/protocol diagnostics, missing session fallback |
| **Hermes Agent** | AgentRouter | text output, executable compatibility checks, timeout and empty-response diagnostics |
| Gemini CLI | legacy provider-runtime | one-shot CLI |
| NanoBot | legacy provider-runtime | one-shot CLI |

> AgentRouter 选择正确的运行时执行每个任务，**Skills、Knowledge、Permissions 和完整员工上下文在切换执行路径时保持不变**。

### AgentRouter 的架构意义

AgentRouter 代表了一个重要的架构演进方向：**Provider Harness 标准化层**。

```
Workspace Layer (Skills, Permissions, Knowledge, Audit)
         ↓
    AgentRouter ← 核心抽象层
         ↓
    ┌────┼────┬────────┐
    ↓    ↓    ↓        ↓
Claude  Codex OpenCode OpenClaw
Codex   (各运行时 CLI)
```

这与传统的「一个框架对应一个 Agent」模式不同，AgentRouter 把「多运行时」从框架层的概念变成了基础设施层的现实。

---

## 核心功能

### 1. 数字员工看板（Digital Employee Board）
将私有 Agent 变成组织内可见、可借用、可复用的数字员工。

### 2. AgentRouter 调度
同一 Agent 跨多个运行时运行，身份、上下文和技能在整个过程中保持完整。

### 3. 多 Agent 协作
多个 Agent 协调高风险运营决策，通过人类审批门推进。

### 4. 权限与审批
权限、授权、凭证、文档和出站操作 — 全部可见、可审计、在人类控制之下。

### 5. 共享工作空间
人类和 Agent 共用同一操作上下文，而不是人类手动在聊天、文档、表格和任务之间传递上下文。

---

## 部署方式

| 模式 | 适用场景 | 启动方式 |
|------|---------|---------|
| ☁️ **平台模式（托管）** | 团队想立即开始 — 无需基础设施、数据库或守护进程主机 | 访问 hire-an-agent.online |
| 🖥️ **自托管模式** | 团队需要完全控制数据、基础设施、Provider CLI、运行时机器和内部部署策略 | Clone 仓库并按照设置指南操作 |

---

## 与 ClawTeam 的关系

| 项目 | Stars | 主题 | 协议 |
|------|-------|------|------|
| **HKUDS/ClawTeam** | 5341 | 多 Agent 并行调度 CLI | Apache-2.0 |
| **HKUDS/AgentSpace** | 339 | Human+Agent 协作工作空间 + AgentRouter | Apache-2.0 |

两个项目同属 HKUDS 研究组，ClawTeam 解决「多 Agent 并行执行」问题，AgentSpace 解决「人与 Agent 的团队协作」问题。AgentRouter 作为共同基础设施连接两者。

---

## 工程亮点

1. **AgentRouter 的统一执行契约**：所有运行时共享同一 JSON 事件标准化和会话传播机制
2. **执行路径变更时技能不变**：Skills、Knowledge、Permissions 在切换 Harness 时保持完整
3. **数字员工身份抽象**：Agent 不再是工具，而是有角色、负责人和责任的第一等团队成员
4. **完整的治理审计链**：从权限授予到审批委托，每个操作都有审计跟踪

---

## 延伸阅读

- [HKUDS/ClawTeam：多 Agent 并行调度 CLI，5341 Stars](../projects/hkuds-clawteam-agent-swarm-intelligence-cli-5341-stars-2026.md)
- [OpenHarness：HKUDS 开源的 Agent Harness，深度集成 Claude Code / OpenClaw](../projects/openharness-hKUDS-agent-harness-open-source-2026.md)
- [Anthropic Claude Code Auto Mode：Harness Engineering 的权限设计范式转变](../harness/claude-code-auto-mode-harness-engineering.md)
