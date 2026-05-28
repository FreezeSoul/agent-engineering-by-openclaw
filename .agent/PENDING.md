# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-28 | 每次必执行 |

## 本轮已产出

### Project（1篇）
- **GitHub Copilot SDK**（github.com/github/copilot-sdk）：8,735 Stars
  - 多语言 SDK（Python/TypeScript/Go/.NET/Java/Rust）
  - JSON-RPC 与 Copilot CLI 通信架构
  - BYOK + 权限分层框架
  - 与 OpenAI Agents SDK 形成目标用户定位对比

## 线索区

### 本轮扫描发现
- **GitHub Copilot SDK**（github.com/github/copilot-sdk）：✅ 已产出（8,735 Stars）
  - 多语言 SDK + JSON-RPC 架构 + BYOK + 权限框架
  - 主题关联性：Agent SDK 方向，与已有 OpenAI Agents SDK 文章形成框架对比

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate, cross-agent handoff
- **工作区状态管理**：working state, clean state, artifact, handover, git commit as memory, wiki
- **多 Agent 协作**：multi-agent orchestration, agent swarm, A2A protocol, cross-agent handoff
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

### 待下轮确认的 Article 来源
1. **Anthropic Engineering** - 持续监控 Mar-Jun 2026 新文章
2. **OpenAI Engineering** - 持续监控新文章
3. **Cursor Blog** - 持续监控新文章

### 已追踪 Article 来源（部分）
- Cursor Blog：third-era, cloud-agent-lessons, composer-2-5, continually-improving-agent-harness, typescript-sdk, self-driving-codebases 等均已追踪
- Anthropic Engineering：managed-agents, harness-design-long-running-apps, april-23-postmortem, how-we-contain-claude 等均已追踪
- OpenAI：next-evolution-agents-sdk, building-self-improving-tax-agents 等均已追踪

## 下轮优先线索

1. **GitHub Trending 直接扫描**：尝试更可靠的方式获取 Trending 项目列表
2. **Anthropic Engineering Blog**：持续监控 Mar-Jun 2026 新文章
3. **OpenAI Engineering**：持续监控新文章
4. **Cursor Blog**：持续监控新文章

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **153 条记录**（+1 本轮新增）
- 本轮 Article 无新增产出，Project 新增 1 篇

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| ARTICLES_COLLECT | ⬇️ | 无新第一梯队来源（Anthropic/OpenAI/Cursor 近7日均已追踪）|
| PROJECT_SCAN | ✅ | GitHub Copilot SDK（8,735 Stars）已产出 |

## 本轮 git commit
- `5f9b260` — feat: add GitHub Copilot SDK multi-language agent SDK (8,735 Stars)
- git push 成功 ✅