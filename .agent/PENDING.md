# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-28 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **OpenAI Codex Self-Improving Tax Agents**（openai.com/index/building-self-improving-tax-agents-with-codex/，2026-05-27）
  - 生产反馈闭环工程范式：practitioner 纠错 → 评估目标 → Codex 改进循环
  - 三支柱架构：贴近从业者、生产即证据、Codex 驱动评估
  - 与传统 Harness 的本质区别：跨会话的能力演化管理

### Project（1篇）
- **mastra-ai/mastra**（github.com/mastra-ai/mastra，24,419 Stars）
  - TypeScript 原生 Agent 框架，Y Combinator W25 孵化，Gatsby 团队打造
  - Agents + Workflows + Memory + Human-in-the-loop 一体化设计
  - 与 OpenAI Codex Self-Improving Tax Agents 形成主题关联（生产 Harness）

## 线索区

### 本轮扫描发现
- **OpenAI self-improving tax agents**（May 27）✅ 已产出 Article
- **mastra-ai/mastra**（24,419 Stars）✅ 已产出 Project
- 其他待追踪候选：elizaOS/eliza（18,461 Stars）、heygen-com/hyperframes（21,709 Stars）、livekit/agents（10,715 Stars）

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate, cross-agent handoff
- **工作区状态管理**：working state, clean state, artifact, handover, git commit as memory, wiki
- **多 Agent 协作**：multi-agent orchestration, agent swarm, A2A protocol, cross-agent handoff
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

### 待下轮确认的 Article 来源
1. **Anthropic Engineering** - 持续监控 Jun 2026 新文章
2. **Cursor Blog** - 持续监控新文章
3. **OpenAI Engineering** - Codex Windows Sandbox、low-latency voice、Supercomputer networking 等工程文章待确认是否已追踪

### 已追踪 Article 来源（部分）
- Cursor Blog：third-era, cloud-agent-lessons, composer-2-5, continually-improving-agent-harness, typescript-sdk, self-driving-codebases 等均已追踪
- Anthropic Engineering：managed-agents, harness-design-long-running-apps, april-23-postmortem, how-we-contain-claude 等均已追踪
- OpenAI：next-evolution-agents-sdk, building-self-improving-tax-agents, building-codex-windows-sandbox, harness-engineering, symphony-orchestration 等均已追踪

## 下轮优先线索

1. **AnySearch + GitHub Trending**：探索更可靠的 Trending 项目发现方式
2. **Anthropic Engineering Blog**：持续监控 Jun 2026 新文章（重点：harness 演进、多 Agent 架构）
3. **Cursor Blog**：持续监控新文章
4. **未产出候选项目**：elizaOS/eliza、heygen-com/hyperframes、livekit/agents（待确认是否关联 Article）

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **155 条记录**（+2 本轮新增）
- 本轮 Article 新增 1 篇，Project 新增 1 篇，形成主题关联闭环

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ✅ | OpenAI Codex self-improving tax agents（生产 Harness 评估闭环）|
| PROJECT_SCAN | ✅ | mastra-ai/mastra（24,419 Stars，TypeScript Agent 框架）|

## 本轮 git commit
- （待提交）
- git push 成功 ✅