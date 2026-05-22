# Vercel coding-agent-template：让所有主流 Coding Agent 在 Vercel Sandbox 上并行执行的多 Agent 编码平台

## TRIP 要素

**Target**：需要统一管理多个 Coding Agent（Claude Code、Codex CLI、Copilot CLI、Cursor CLI、Gemini CLI、opencode）、在隔离云端沙箱中自动执行代码任务的平台团队，以及需要为 AI Coding 提供企业级部署方案的 DevOps 工程师。

**Result**：一个 Next.js 应用，在 Vercel Sandbox 上同时支持 6 种主流 Coding Agent，通过 Vercel AI Gateway 实现模型路由，通过 AI-Generated Branch Names 自动管理 Git 工作流。开发者提交任务后 5 分钟内看到代码变更提交。

**Insight**：Vercel 的核心赌注是 **Sandbox as Infrastructure**——将代码执行环境从「本地机器」或「固定 CI Runner」变成按需创建的云端隔离单元。coding-agent-template 将这个能力开放给所有主流 Coding Agent，使多 Agent 并行编码任务的企业级编排成为可能。

**Proof**：GitHub 1.7k Stars，Vercel AI SDK 5 驱动，支持 6 种 Agent，Multipass 架构覆盖 5 小时超时粒度。

---

## P-SET 结构

### P - Positioning

**一句话定义**：一个基于 Vercel Sandbox 的多 Coding Agent 统一编排平台——让 Claude Code、Codex、Copilot、Cursor、Gemini 和 opencode 在同一个界面下并行执行代码任务。

**场景锚定**：当你需要让多个 Coding Agent 同时处理一个大型代码库的不同模块，或者你需要为企业内部署统一的 AI Coding 控制平面时，coding-agent-template 提供的是一个「多 Agent 即服务平台」而非「单一 Agent 包装器」。

**差异化标签**：多 Agent 统一编排 + Vercel Sandbox 隔离执行 + AI Gateway 模型路由

### S - Sensation

部署完成后，访问 Dashboard，你可以：
- 在下拉菜单中任选 6 种 Coding Agent 之一
- 提交一个代码改造任务
- 系统自动创建 Vercel Sandbox（最长等 2 分钟）
- Agent 在隔离环境中执行任务，文件变更自动提交到 AI-Generated Branch
- 全程可在 VSCode Server 实时查看 Agent 操作

关键在于**每个任务独占一个全新的沙箱实例**。Agent 的所有操作——依赖安装、代码生成、测试执行——都在隔离环境中完成，不会影响主机或其他任务的状态。

### E - Emotion

**「终于有人把 AI Coding 的基础设施做掉了」**——这是笔者看到 architecture diagram 时的感受。大多数团队在 AI Coding 上的工程投入不是训练模型，而是搭建「让模型能安全执行代码的环境」。coding-agent-template 把这个基础设施层直接产品化了。

对于平台团队而言，这意味着不再需要为每个新 Coding Agent 单独写适配器。对于安全团队，这意味着所有 Agent 执行都在 Vercel Sandbox 的网络限制下运行，不会出现「Agent 访问了不该访问的内部服务」的问题。

---

## 为什么值得关注

### 1. 多 Agent 统一接口的价值

当前 AI Coding 领域的一个现实是：**没有银弹 Agent**。Claude Code 在长上下文理解上表现优异，Codex 在 GitHub 生态集成上深度更深，Cursor 在产品交互上更流畅。每种 Agent 都有自己的最佳场景。

coding-agent-template 的价值不在于它自己做一个 Agent，而在于它**为所有 Agent 提供了统一的基础设施层**：
- 统一的认证（GitHub/Vercel OAuth）
- 统一的执行环境（Vercel Sandbox）
- 统一的输出格式（Git Branch + PR）
- 统一的超时控制（5 分钟到 5 小时可选）

这意味着平台团队可以专注在「何时用哪个 Agent」而非「如何让 Agent 正确执行」。

### 2. Sandbox as Infrastructure 的工程意义

Vercel Sandbox 不同于传统容器的地方在于它的**按需创建+自动回收**机制：
- 任务提交 → Sandbox 创建 → Agent 执行 → Git 提交 → Sandbox 保持存活（N 小时）→ 超时自动销毁
- 开发者可以在超时窗口内发送 follow-up 消息，Agent 继续在前一个会话中工作
- 所有文件系统状态在 Sandbox 存活期内保持

> "The maximum duration setting controls how long the Vercel sandbox will stay alive from the moment it's created. You can select timeouts ranging from 5 minutes to 5 hours."
> — [GitHub README: vercel-labs/coding-agent-template](https://github.com/vercel-labs/coding-agent-template)

这种「按需分配+自动回收」模式，将云端资源的成本从「包月制」变成「按任务计费」——对于需要批量运行 AI Coding 任务的团队，这是显著的Cost Efficiency提升。

### 3. AI Gateway 的模型路由能力

项目使用 Vercel AI SDK 5 + AI Gateway，这意味着：
- 可以在同一任务中路由到不同的模型（如 Opus 4.7 做架构设计，Sonnet 4.6 做代码生成）
- 可以 A/B 测试不同 Agent 在同一任务上的表现
- 可以集中管理所有 API Key，不分散在各个 Agent 配置中

---

## 架构解析

```
User submits task
    ↓
Database (Neon Postgres): store task metadata
    ↓
AI Branch Name Generation (AI SDK 5 + Gateway)
    ↓
Vercel Sandbox Creation (per task)
    ↓
Agent Selection (Claude Code / Codex / Copilot / Cursor / Gemini / opencode)
    ↓
Git Operations: create branch → commit → push
    ↓
Sandbox stays alive for MAX_SANDBOX_DURATION (follow-up messages allowed)
    ↓
Timeout → Sandbox destroyed
```

关键设计点：
- **每个任务独立 Sandbox**：隔离执行，互不干扰
- **数据库记录任务状态**：支持任务历史的持久化
- **OAuth 统一认证**：GitHub + Vercel，不需要为每个 Agent 单独配置凭证
- **MCP Server 支持**（仅限 Claude Code）：可连接 MCP 服务器扩展 Agent 能力

---

## 与 Article 的关联

本文 Project 与 Article「Anthropic Scaling Managed Agents：Meta-Harness 设计范式」形成主题关联：

| 维度 | Article 理论层 | Project 工程层 |
|------|--------------|--------------|
| **核心接口** | Brain-Hands 解耦：execute()→string | Vercel Sandbox：HTTP API 调用执行环境 |
| **Session 外部化** | Session Log 独立于 Brain/Hands | 任务状态存 Postgres，Sandbox 外持久化 |
| **懒 provisioning** | Brain 按需启动 Sandbox，TTFT 降 60-90% | 任务提交时才创建 Sandbox，不提前占用资源 |
| **Many Hands** | 每个 Hand 是独立工具，Brains 可传递 Hands | 6 种 Agent（= 6 种 Brain 变体）× 多 Sandbox（= Many Hands）|
| **安全边界** | Credential Vault + MCP Proxy 隔离凭证 | Vercel Sandbox 网络限制 + OAuth 集中管理凭证 |
| **Meta-Harness** | 接口稳定，实现可替换 | 统一的 Agent 抽象层，下层可替换为任何支持 CLI 的 Agent |

两者共同指向的核心结论：**AI Agent 的基础设施层正在从「定制化缠绕」向「标准化接口」演进**。Anthropic 给出了这个演进的设计哲学，Vercel 给出了开源实现参考。

---

## 使用建议

**适用场景**：
- 企业内部需要统一管理多个 Coding Agent 的使用策略
- 平台团队需要为 AI Coding 任务提供按需分配的云端执行环境
- 需要批量运行 AI Coding 任务（批量代码审查、批量迁移、批量测试生成）

**不适用场景**：
- 单个开发者本地使用（直接用各 Agent 的原生 CLI 更轻量）
- 对数据主权有严格监管要求（代码在 Vercel Sandbox 中执行，需要评估合规性）
- 需要与内部 CI/CD 系统深度集成的场景（需要额外适配）

**快速上手**：
```bash
git clone https://github.com/vercel-labs/coding-agent-template
npm install
# 配置环境变量
npx playwright install --with-deps chromium
npm run dev
```

核心环境变量：
- `DATABASE_URL`：Neon Postgres 连接字符串
- `VERCEL_TOKEN`：Vercel API Token（用于创建沙箱）
- `OPENAI_API_KEY`：AI Gateway 路由用

---

## 参考文献

- [vercel-labs/coding-agent-template](https://github.com/vercel-labs/coding-agent-template) — GitHub README
- [Vercel Sandbox Documentation](https://vercel.com/docs/sandbox) — Vercel Docs
- [Vercel AI SDK 5](https://sdk.vercel.ai/) — Vercel AI Gateway