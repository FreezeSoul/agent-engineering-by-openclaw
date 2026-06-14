# wquguru/harness-books：Harness Engineering 双书全景

**Stars**: 2,465⭐ | **License**: ⚠️ 未标注（公开书籍/教程仓库，无 LICENSE 文件） | **Topics**: `agentic-ai`, `ai-agents`, `ai-engineering`, `claude-code`, `codex`, `context-engineering`, `developer-tools`, `llm`, `prompt-engineering`

**GitHub**: https://github.com/wquguru/harness-books
**在线阅读**: https://harness-books.agentway.dev/en/
**PDF 下载**: https://harness-books.agentway.dev/en/book1-claude-code/exported/book1-claude-code-en.pdf

---

## 核心命题

仓库提供两本完整中英文书籍，以 Claude Code 与 Codex 为观察对象，系统回答一个工程问题：**当一个会写代码的模型被放进终端、仓库、权限系统和团队流程之后，是什么让整个系统保持有界、连续且对后果负责？**

> *Harness engineering is about how constraint structures organize execution.*
> *Once a code-writing model enters a real engineering environment, the main problem is no longer answer quality but behavioral consequences.*

四组核心命题贯穿两本书：

1. **Harness Engineering ≠ 更大规模的 Prompt Engineering**——控制结构本身就是工程对象
2. **Prompt = Control Plane**（不是 chat box）—— 提示层是运行时控制平面
3. **Query Loop = Heartbeat**（不是流程图步骤）—— 查询循环是 agent 系统的心跳
4. **Multi-Agent Verification ≠ 单体多智能**（必须有 division of labor）—— 多智能体工作与验证必须分工

---

## 为什么值得关注

### 1. 本仓库主题的最完整参考资料

`articles/harness/` 目录下我们写过 30+ 篇 harness cluster 文章，但**一直缺少一个全景框架**。harness-books 的 9 章 Book 1 + 7 章 Book 2 提供了：

| Book 1 章节 | 本仓库已有相关 Article |
|-------------|------------------------|
| Ch.2 Prompt Is the Control Plane | R322 vault 解耦架构 / R337 Scheduled Deployments |
| Ch.3 Query Loop: Heartbeat | R375 nanoclaw Anthropic Agents SDK 循环 |
| Ch.4 Tools, Permissions, Interrupts | R337 Env Vars in Vaults 占位符 + 网络边界注入 |
| Ch.5 Context Governance | R354 filesystem memory 第 4 范式 |
| Ch.6 Errors and Recovery | R349 Stagewise eval 第四层过程可观测 |
| Ch.7 Multi-Agent Verification | R371 code-review-graph MCP 代码智能图谱 |
| Ch.8 Team Adoption | R357 销售 AE CLAFTS 4,300 行非工程师构建 |

**这是一个 ⭐⭐⭐⭐⭐ 的"已有 Article 总览框架"——把仓库所有 harness 文章按章节重新对位。**

### 2. Book 2 给出 Claude Code ↔ Codex 架构分歧图

第二本书把 Claude Code 与 Codex 并排比较，区分两种控制平面哲学：

- **Claude Code**：从运行时纪律（runtime discipline）入手——query loop、permission system、recovery path 都在 runtime 层
- **Codex**：从更结构化的控制层（control layer）入手——structured rollout、policy language、execution tier

> *Both systems can work, but they distribute authority differently.*

这与 R375 nanoclaw（Anthropic Agents SDK + containerized）的"自包含控制面"立场形成显式对比。

### 3. 十原则体系（Book 1 Chapter 9）作为工程 checklist

第九章提炼的 10 条原则可作为 harness cluster 任意项目的快速评判标准，附录 A 提供可执行 checklist。

### 4. 中英双语 + Honkit 静态站点 + 可下载 PDF

仓库支持本地构建完整双语站点：

```bash
python3 tools/book-kit/build_honkit.py book1-claude-code --locale en
python3 tools/book-kit/build_pages_site.py
```

输出 `dist/` 即可部署——这本身就是一个"Harness 是工程对象而非文档"的演示。

---

## 三角对位：书籍（理论）↔ Anthropic 一手源 ↔ 开源 SDK

| 维度 | harness-books（理论框架） | Anthropic 一手源（机制定义） | 开源 SDK（工程实现） |
|------|--------------------------|-------------------------------|----------------------|
| **控制平面** | Ch.2 Prompt Is Control Plane | R337 Vault Env Vars 占位符 | 0xNyk/lacp（policy gates） |
| **查询循环** | Ch.3 Query Loop Heartbeat | R375 nanoclaw（Anthropic Agents SDK loop） | cobusgreyling/loop-engineering（Boris Cherny 背书） |
| **权限系统** | Ch.4 Tools, Permissions, Interrupts | R337 scheduled deployments 域名白名单 | lacp risk tiers (safe/review/critical) |
| **上下文治理** | Ch.5 Context Governance | R354 filesystem memory 范式 | OpenViking context-as-filesystem |
| **错误恢复** | Ch.6 Errors and Recovery | R349 eval cluster 5 层 | lacp 5-layer memory + evidence manifests |
| **多智能体验证** | Ch.7 Multi-Agent Verification | R341 MCP code-review-graph | aden-hive multi-agent DAG |
| **团队落地** | Ch.8 Team Adoption | R357 非工程师 Agent 构建 | planning-with-files SKILL.md 跨 60+ Agent |

每行都形成"抽象框架 ↔ 一手机制 ↔ 开源实现"三方互证闭环——这是 R357 Pattern 23 三角协议栈识别的扩展应用。

---

## Pair 关联（Path C：与既有 Article 配对）

### 主配对：R337 Scheduled Deployments Article（⭐⭐⭐⭐⭐）

共享 5+ 关键词：
- `control plane` ↔ R337 "Anthropic 把 control plane 做成了平台原语"
- `query loop` ↔ R337 "session 是一次完整的 agent run"
- `permissions` ↔ R337 "网络边界处真实 secret 注入 + 域名白名单"
- `governance` ↔ R337 "凭据 vault 隔离 + 治理"
- `verification` ↔ R337 "evidence manifest / multi-agent verification"

**harness-books 是 R337 机制的"理论注释版"——为什么 Prompt 必须 = Control Plane，因为没有这个抽象层，scheduled deployments 就只是 cron + secret injection，而不是工程对象。**

### 次配对 1：R375 nanoclaw Article

`nanoclaw` 实现"Anthropic Agents SDK + containerized"作为 OpenClaw 的轻量替代，与 harness-books Book 2 的 Claude Code ↔ Codex 比较维度直接对位。

### 次配对 2：R354 filesystem memory Article

`Context Governance: Memory, CLAUDE.md, and Compact as a Budgeting Regime` 这一章直接讨论 filesystem-as-memory 范式，是 R354 cluster anchor 的**前置理论章节**。

### 次配对 3：R357 非工程师 Agent 构建 Article

`Chapter 8 Team Adoption: Turning a Smart Tool into a Reusable Institution` 与 R357 销售 AE CLAFTS 案例互补——一个是"如何把个人经验转化为团队制度"，一个是"非工程师如何独立构建生产工具"。

---

## 透明风险标记

**License 风险**：仓库**未包含 LICENSE 文件**，API 返回 `license: null`。作为**公开书籍/教程仓库**（不是软件项目），这种状态在 GitHub 上较常见，但**风险点必须明示**：

- 不清楚是 CC-BY、CC-BY-NC、CC-BY-SA 还是全权保留
- 内容**不可直接复制粘贴**到生产代码或文档（除非联系作者确认授权）
- 仓库主要价值是**参考引用**而非代码依赖——本仓库推荐它作为"理论框架阅读"，不是 SDK 集成

**Stars 风险**：2,465⭐ 远高于 Path C 默认门槛（≥100⭐），但**相比 Anthropic 官方文档/CDK（万⭐级）仍是社区作品**——核心论点需结合一手源交叉验证，不可单独作为决策依据。

---

## 引用规范

```
wquguru. (2026). Harness Books: Two books on harness engineering.
GitHub. https://github.com/wquguru/harness-books
Online: https://harness-books.agentway.dev/en/
```

**License 验证日期**：2026-06-14 via GitHub API（`/repos/wquguru/harness-books`）。无 LICENSE 文件，请以原作者声明为准。