# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-28 | 每次必执行 |

## 本轮已产出

### 维护操作
- **Round 144 维护轮次**：新增 Article 1 篇 + Project 1 个
- sources_tracked.jsonl 健康度：162 条记录（84 article / 78 project）— 新增 TypeScript SDK article + wshobson/agents project
- 本轮发现 wshobson/agents（36,075 Stars）未追踪，产出 Project；Cursor TypeScript SDK 未追踪，产出 Article

## 线索区

### 源扫描状态（Round 144）
- **Anthropic Engineering Blog**：直接 curl 成功抓取（JS-free HTML），发现已追踪所有可见文章（how-we-contain 等 10 篇已全部追踪）
- **Cursor Blog**：curl 扫描 54 个 slug，确认全部已追踪（bootstrapping-composer 已追踪）
- **GitHub API 扫描**：发现多个未追踪高价值项目
  - wshobson/agents（36,075 Stars）：**新增**（本轮产出 Project）
  - hesreallyhim/awesome-claude-code（45,039 Stars）：未追踪（Stars 门槛达标但内容为 awesome-list 性质，降级不收录）
  - x1xhlol/system-prompts-and-models-of-ai-tools（138,409 Stars）：未追踪（内容性质偏向系统提示词收集，非 Agent 工程实践，降级不收录）
  - jarrodwatts/claude-hud（23,934 Stars）：未追踪（为 Claude Code Plugin 非框架类，降级不收录）
  - revfactory/harness（3,729 Stars）：未追踪（但 Claude Code Plugin 类，非核心框架）

### 未追踪项目（持续监控，不影响本轮）
以下项目 Stars 门槛达标但内容性质不匹配 Agent 工程框架方向：
- hesreallyhim/awesome-claude-code（45,039 Stars）：awesome-list 类，非工程框架
- x1xhlol/system-prompts-and-models-of-ai-tools（138,409 Stars）：系统提示词收集，非 Agent 工程实践
- jarrodwatts/claude-hud（23,934 Stars）：Claude Code 插件，非框架

### 工程机制关键词持续监控
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery, snapshot, rehydrate
- **工作区状态管理**：working state, clean state, artifact, handover, git commit as memory
- **多 Agent 协作**：multi-agent orchestration, agent swarm, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, credential isolation

## 下轮优先线索

1. **Anthropic Engineering Blog**：持续监控新文章（重点：harness 演进、多 Agent 架构）
2. **GitHub 新兴框架**：持续扫描 Stars > 1000 的新兴 Agent 框架项目
3. **OpenAI Engineering Blog**：监控 anysearch 发现的新内容
4. **GNAP 协议**：farol-team/gnap（61 Stars）值得关注，但 Stars 偏低，下轮再评估

## 防重提示

- `.agent/sources_tracked.jsonl` 当前 **162 条记录**（84 article / 78 project）
- 新增 Cursor TypeScript SDK article + wshobson/agents project

## 本轮执行摘要

| 任务 | 结果 | 说明 |
|------|------|------|
| GIT_SYNC | ✅ | git pull --rebase → Already up to date |
| SOURCE_SCAN | ✅ | Anthropic（HTML 抓取成功）、Cursor（54 slug 已追踪）、GitHub API（多个高 Stars 项目）|
| ARTICLES_COLLECT | ✅ | 发现 TypeScript SDK 未追踪，产出 Article |
| PROJECT_SCAN | ✅ | 发现 wshobson/agents 未追踪，产出 Project（36k Stars）|
| GIT_COMMIT | ✅ | 162859a — Cursor TypeScript SDK + wshobson/agents |
| GIT_PUSH | ✅ | fa31280..162859a |

## 本轮 git commit

- `162859a` — Round 144: Add Cursor TypeScript SDK article + wshobson/agents Project