# affaan-m/ECC：190K Stars 的 Agent Harness 性能优化系统

> **核心论点**：ECC 不是配置包，而是一个完整的 Agent Harness 性能优化系统——Skills、Instincts、Memory 优化、安全扫描、持续学习、研究优先开发，五位一体。Anthropic Hackathon 获奖作品，跨 7 个主流 Agent 框架。
>
> **关键判断**：当 Agent 框架大战从「功能比拼」转向「深度优化」时，ECC 代表的是第三种路线——不在框架层内卷，而在框架之上构建优化层。

---

## T - Target：谁该关注

- **深度 Agent 用户**：已经在用 Claude Code/Cursor/OpenCode 但感觉效率还有提升空间
- **Agent 框架研究者**：想理解「好用的 Agent 系统」到底需要哪些组件
- **多框架用户**：同时使用 Claude Code + Cursor + Codex，需要统一优化方案

---

## R - Result：能带来什么

| 能力维度 | 传统方式 | ECC 方式 |
|---------|---------|---------|
| 上下文管理 | 每次手动清理 | Hook 自动持久化 |
| 技能复用 | 每次重写 | Instinct 持续学习 |
| Token 消耗 | 不控制 | 模型选择 + 压缩 |
| 安全审查 | 无 | AgentShield 1282 规则 |
| 多 Agent | 各跑各的 | PM2 协调工作流 |

---

## P - Positioning（定位破题）

### 它是什么

ECC（Everything Claude Code / Cross-harness Code）是 **Anthropic Hackathon 获奖作品**，定位为「harness-native operator system」——不是另一个 Agent 框架，而是在现有框架之上构建的性能优化层。

**支持框架**：Claude Code、Codex、Cursor、OpenCode、Gemini、Zed、GitHub Copilot

**核心规模**：
- 182K+ Stars，28K+ Forks
- 170+ 贡献者，12 种语言生态
- 60 个 Agents，232 个 Skills，75 个 Legacy Command Shims

### 它不是什么

- **不是新框架**：不替换 Claude Code/Cursor，是它们的优化层
- **不是配置包**：不是一堆 dotfiles，是有状态、带治理的系统
- **不只是 Claude Code 专用**：v2.0 明确标注跨 harness 架构

---

## S - Sensation（体验式介绍）

想象你装了 Claude Code 后，有个系统自动告诉你：

- 「这个任务适合用哪个模型」（成本感知路由）
- 「这类问题你之前解决过，这里是模式库」（Instinct 持续学习）
- 「提交前自动跑安全扫描」（AgentShield 集成）
- 「多 Agent 任务用 PM2 协调」（并行工作流）

这正是 ECC 在做的事情——不是教你用 Cursor，而是让 Cursor 用起来更高效。

---

## A - Architecture（核心架构）

### 五大核心模块

```
ECC System
├── Skills（技能）      — 可复用的领域能力单元
├── Instincts（本能）  — 从会话中自动提取的学习模式
├── Memory（记忆）      — 跨会话上下文持久化
├── Security（安全）    — AgentShield 1282 规则安全扫描
└── Research（研究）   — Research-first 开发方法论
```

### AgentShield 安全体系

AgentShield 是 ECC 的安全组件，提供：
- 1282 条安全规则
- `/security-scan` 命令，直接从 Claude Code 调用
- CVEs 监控和沙箱隔离

### 跨框架架构（v2.0 核心）

v2.0 引入了 Rust 控制平面（`ecc2/`），暴露命令：
- `dashboard` — GUI 面板
- `start / stop / resume` — 会话管理
- `sessions / status` — 状态查询
- `daemon` — 守护进程

---

## T - Technical（技术细节）

### 核心版本演进

| 版本 | 时间 | 核心能力 |
|------|------|---------|
| v1.2.0 | Feb 2026 | Python/Django + Java Spring Boot 支持 |
| v1.3.0 | Feb 2026 | OpenCode 全量集成 |
| v1.6.0 | Feb 2026 | Codex CLI + AgentShield + GitHub Marketplace |
| v1.8.0 | Mar 2026 | Harness-first 性能系统定位 |
| v1.9.0 | Mar 2026 | 选择性安装架构 + SQLite 状态存储 |
| v2.0.0-rc.1 | Apr 2026 | Rust 控制平面 + GUI Dashboard |

### 关键数字

- **997+** 内部测试全部通过
- **1282** AgentShield 安全规则
- **12** 语言生态（TypeScript/Python/Go/Java/Perl/PHP/Kotlin/C++/Rust 等）
- **75** Legacy Command Shims

### 安装方式

```bash
# 交互式安装向导
npx ecc install

# 选择性安装（按语言/功能）
npx ecc install --select

# 安全扫描
npx ecc security-scan

# 状态报告
npx ecc status --markdown --write status.md
```

---

## V - Vision（未来价值）

### 为什么它是重要的信号

Agent 框架大战正在进入第二阶段：

- **第一阶段**（2024-2025）：框架数量爆发，Cursor vs Claude Code vs Copilot 功能对比
- **第二阶段**（2026+）：框架深度优化，Token 节省、上下文复用、安全审查成为核心竞争力

ECC 代表的是第二阶段的优化路线——不在框架层内卷，而在框架之上构建优化层。这个定位使它能跨越框架本身存在。

### Rust 控制平面（ecc2）的意义

v2.0 的 Rust 控制平面不只是技术选型，它意味着：
- ECC 从「配置集合」升级为「独立系统」
- 可以脱离 Claude Code 独立运行（daemon 模式）
- 跨框架协调成为可能

---

## 与文章主题的关联

**Anthropic Desktop Extensions .mcpb**（本轮 Article）定义了 MCP 技能的分发标准；
**ECC** 则定义了 Harness 层 Skills 的实现标准。

两者形成互补：
- `.mcpb` 解决「技能如何分发」
- **ECC Skills** 解决「技能如何实现」

---

## 📚 原文引用

> "Not just configs. A complete system: skills, instincts, memory optimization, continuous learning, security scanning, and research-first development."
>
> — ECC README

> "Anthropic Hackathon Winner"
>
> — ECC README

> "Works across **Claude Code**, **Codex**, **Cursor**, **OpenCode**, **Gemini**, **Zed**, **GitHub Copilot**"
>
> — ECC README

> "ECC Pro is the hosted GitHub App for private repos. OSS stays free. This repo is MIT-licensed forever."
>
> — ECC README

---

## 防重索引

- `https://github.com/affaan-m/ECC` — 190415 Stars，Harness 性能优化
- 关键词：ECC / harness optimization / AgentShield / skills / instincts
- 不混淆：obra/superpowers（204K Stars，Skills Framework，专注开发方法论）