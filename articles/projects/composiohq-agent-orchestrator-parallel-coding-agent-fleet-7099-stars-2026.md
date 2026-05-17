# ComposioHQ/agent-orchestrator：并行 Agent 编排的企业级解法

## 核心主张

当一个代码库需要同时处理 10 个 Issue，每个 Issue 都需要独立的 Agent 分支、独立的环境、独立的 PR——这已经不是一个「Agent」的问题，而是一个**分布式编排**的问题。agent-orchestrator 正是为这个场景设计的：它将多个 AI 编码 Agent 同时部署到同一个代码库的不同分支上，通过 git worktree 做环境隔离，通过自动化 reactions 处理 CI 失败和 Review 评论，让人类只在需要判断时介入。

笔者认为：这个项目的价值不在于「让一个 Agent 变得更强」，而在于**重新定义了人类在多 Agent 环境中的角色**——从「启动者」变成「裁判」。

---

## 解决了什么问题

**单 Agent 场景**：运行一个 AI 编码 Agent 在终端里工作，这已经比较成熟了。

**多 Issue 并行场景**：当你想让多个 Issue 同时被处理时，问题就出现了：
- 每个 Agent 需要自己的 git branch 和 worktree
- CI 失败需要路由回对应的 Agent
- Review 评论需要路由回对应的 Agent
- 你需要跟踪 10 个 PR 的状态，而不是 1 个

没有编排工具，这些都需要人工协调。agent-orchestrator 把这些全部自动化了。

---

## 核心架构

### 七个插件槽位，全部可替换

| 槽位 | 默认 | 可选 |
|------|------|------|
| Runtime | tmux (macOS/Linux) / process (Windows) | docker |
| Agent | claude-code | codex, aider, cursor, opencode, kimicode |
| Workspace | worktree | clone |
| Tracker | github | linear, gitlab |
| SCM | github | gitlab |
| Notifier | desktop | slack, discord, composio, webhook, openclaw |
| Terminal | iterm2 | web |

核心只有一个：**生命周期管理**。所有其他能力都是插件。7 个槽位意味着如果你想用 GitLab + GitLab Issues + Slack 通知，只需要换掉 tracker 和 notifier，runtime、agent、workspace 全都不变。

笔者认为：这种「核心固定 + 周边可插拔」的设计，是面向多团队协作场景的事实标准。

### Reactions 系统

```yaml
reactions:
  ci-failed:
    auto: true
    action: send-to-agent
    retries: 2
  changes-requested:
    auto: true
    action: send-to-agent
    escalateAfter: 30m
  approved-and-green:
    auto: false
    action: notify
```

CI 失败 → Agent 自动收到日志并尝试修复。Reviewer 要求修改 → Agent 自动处理。你只在「PR 合并」这个动作上需要人工判断。

### Agent-agnostic 设计

同一套配置可以切换 Claude Code / Codex / Aider：

```yaml
defaults:
  agent: claude-code  # 换成 codex 就换底层引擎
```

这意味着你可以用 Claude Code 处理日常任务，用 Codex 处理需要 Windows 兼容性的任务——但用同一套编排逻辑。

---

## 与同类项目的差异

**与 ruflo 的对比**：ruflo 做的是 Claude 原生的多 Agent 编排，强调的是「如何让多个 Agent 互相通信」。agent-orchestrator 做的是「如何让多个 Agent 在同一个代码库上并行工作不打架」，强调的是隔离和协调。

**与 swarms 的对比**：swarms 是通用多 Agent 框架，包含内存、MCP、调度、委托等能力。agent-orchestrator 专注于「代码库并行工作」这个垂直场景，不做通用编排。

**与 open-swe 的对比**：open-swe 是异步编码 Agent 框架，目标是自动化 GitHub Issue 处理。agent-orchestrator 在概念上类似，但更强调「人类判断保留」——它不追求完全自动化，而是在关键节点保留人类介入的能力。

---

## 使用场景

**适合团队的场景**：
- 团队有多个 Issue 需要同时处理，人工分配和跟踪成本高
- 希望 AI Agent 能够自动响应 CI 失败，而不需要人类转发日志
- 需要同时评估多个 Agent 在同一个代码库上的表现

**不适合的场景**：
- 单 Issue 或低并发场景（用单个 Agent 更简单）
- 需要复杂的多 Agent 协作逻辑（需要通用编排框架）
- 对 Windows CI 环境有深度需求（Codex 支持更好，但 agent-orchestrator 的 agent-agnostic 意味着你可以换引擎）

---

## 快速上手

```bash
npm install -g @aoagents/ao

# 在任意代码库启动
cd ~/your-project && ao start

# 或者指定远程仓库
ao start https://github.com/your-org/your-repo
```

仪表板在 `http://localhost:3000`，自动生成 `agent-orchestrator.yaml` 配置文件。

---

## 关联主题

- **GAN 三代理架构**（Anthropic）：Planner-Generator-Evaluator 的分离逻辑与 agent-orchestrator 的「Agent 工作 + 人类裁判」模式高度一致——Evaluator 判定失败后，Generator 重新执行。
- **Parameter Golf 社区运营**（OpenAI）：@notapplica 的 Agent 运营「实时更新」公告牌，本质上也是一种编排——但编排的是信息流，而非代码。agent-orchestrator 编排的是代码开发流。

---

*来源：[ComposioHQ/agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator) | 7,099 Stars | MIT License | 2026-02-13 Created*