# yaodub/cast — Multi-User Claude Agent Harness

> Your agent team, on your machine. Open-source harness for multi-user Claude agents.

- **Stars**: 36 ⭐
- **License**: MIT
- **Created**: 2026-06-02
- **Pushed**: 2026-06-11
- **Topics**: `agent-orchestration` `multi-agent` `anthropic` `claude` `mcp` `self-hosted`

## 一句话描述

Cast 将 Claude Code 封装为多用户、多渠道的 agent 团队服务——用户通过 Slack、Telegram 或 Web 与同一 agent 对话，agent 以文件夹形式存在于本地文件系统。

---

## 核心架构

### Agent = 文件夹

Cast 的核心理念：**Agent 不是代码，是文件夹**。

```
~/.cast/agents/<name>/
```

每个 agent 就是一个目录，包含其配置、扩展和状态。所有 agents 默认存储在 `~/.cast/agents/` 下，可通过 `CAST_AGENTS_DIR` 环境变量重定向。

### 扩展系统

Agents 通过扩展（extensions）获取工具能力：

| 扩展 | 功能 |
|------|------|
| `ext-email` | 邮件读写 |
| `ext-calendar` | 日历事件管理 |
| `ext-web-fetch` | 网页抓取 |
| `ext-whatsapp` | WhatsApp 集成 |

这些扩展以独立的 npm 包形式存在（`packages/ext-*`），体现了 **Monorepo + 插件化扩展** 的架构设计。

### 多渠道用户接入

Cast 支持三种用户接入渠道：

- **Slack** — 团队协作
- **Telegram** — 即时通讯
- **Web** — 浏览器内对话

每个用户拥有独立的私有对话上下文，但共享同一个 agent 实例——这是"多用户同一 agent"的关键特征。

---

## 生命周期：从 Design 到 Pair

### Step 1: Design（设计）

用户描述需求：

> "an agent that reads my morning email and flags what's worth a reply"

Design agent 根据自然语言描述自动脚手架出 agent 文件结构。

### Step 2: Scaffold（脚手架）

自动生成的文件成为 agent 的"源代码"——不是传统意义的代码，而是配置驱动的 agent 定义。

### Step 3: Configure（配置）

- **Model 配置**：选择模型
- **Secrets 配置**：API keys 等敏感信息
- **Wires 配置**：agent 的连接关系

### Step 4: Pair（配对）

受邀用户通过渠道接入，获得与该 agent 的私人对话会话。同一 agent，多个独立会话。

---

## 工程特性

### 容器化隔离

Cast 要求容器运行时：
- **macOS**: Apple Container
- **Linux/WSL2**: Docker

Agent 容器镜像首次构建约 2 分钟，之后启动是即时的。隔离确保多用户场景下的安全边界。

### 身份与路由

Cast 在架构上明确分离了：
- **Identity** — agent 的身份定义
- **Routing** — 用户请求到 agent 的路由
- **Access Control** —  agent 间、用户间的权限控制

### Anthropic 凭证支持

支持两种认证方式：
- **Anthropic API Key** — 直接调用 API
- **Claude.ai Token** — 使用 Claude.ai 账号认证

---

## 与同类对比

| 维度 | Cast | OpenClaw | LangChain Agents |
|------|------|----------|-----------------|
| 核心抽象 | Agent = 文件夹 | Skill/Agent | LCEL Chain |
| 多用户 | ✅ 原生 | ✅ 多渠道 | ❌ 需自行实现 |
| 部署形态 | 本地服务 | 远程 + 本地 | 嵌入式 |
| 扩展机制 | 独立 npm 包 | Skill 机制 | Tool 机制 |
| 渠道接入 | Slack/TG/Web | 飞书/TG 等 | API |

---

## 质量评估

- ⭐⭐⭐ — 概念清晰（"Agent = 文件夹"），多用户场景明确，但 stars 过低（36），需观察社区活跃度
- **适用场景**：小型团队需要共享同一个 Claude agent 能力的场景
- **工程成熟度**：Developer Alpha，rough edges 预期内

---

## 来源

- GitHub: https://github.com/yaodub/cast
- Docs: https://getcast.dev
