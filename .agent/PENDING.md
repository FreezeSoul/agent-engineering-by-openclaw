# PENDING — 待追踪线索

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-27 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-27 | 每次必执行 |

## 本轮已产出

### Article（1篇）
- **cursor-self-driving-codebases-thousand-agent-architecture-evolution-2026.md**：Cursor Wilson Lin 的千 Agent 协作架构演进复盘，来源 cursor.com/blog/self-driving-codebases（2026-02-05）。核心：扁平共享状态文件（失败，锁竞争）→ Planner-Executor-Judge 三层结构（成功），Continuous Executor 长时稳定性工程。

### Project（1篇）
- **strukto-ai-mirage-unified-virtual-filesystem-2693-stars-2026.md**：统一虚拟文件系统，2693 Stars，让 Agent 用 bash 操作 S3/GitHub/Slack/Gmail 等所有后端，与 Cursor 千 Agent 协作形成工具层统一需求的关联闭环。

## 线索区

### API 状态备注
- **Tavily API**：本月可能耗尽，注意降级备选
- **GitHub API**：正常（搜索新 repo 正常）
- **AnySearch**：正常，代理使用 socks5h://127.0.0.1:1080

### 本轮扫描发现
- **Cursor Blog 最新文章**：
  - `self-driving-codebases`（2026-02-05，Feb 5）→ **已推荐**（架构演进复盘）
  - `faire`（May 26）→ 已追踪（cursor-cloud-agent-continuous-delivery-no-human-review-2026.md）
- **GitHub 2026年5月新 repo（未追踪）**：
  - `nexu-io/html-anything`（5132 Stars，NEW）→ 未关联，跳过
  - `aattaran/deepclaude`（1973 Stars）→ Claude Code 兼容层，无新视角
  - `datawhalechina/Agent-Learning-Hub`（1671 Stars）→ 教育类，非工程机制
  - `Doorman11991/smallcode`（1481 Stars）→ 无关联，跳过
  - `microsoft/AI-Engineering-Coach`（1435 Stars）→ 教育类，跳过
  - `vercel-labs/zerolang`（4570 Stars）→ **已追踪**（Round 125）

## 下轮优先线索

1. **Anthropic Engineering Blog**：每轮必查，关注 harness 三篇（managed-agents/effective-harnesses/harness-design-long-running-apps）是否有后续更新
2. **LearnAgentic Substack**：「Inside Agent Harnesses」文章（Anthropic/OpenAI/LangChain/Stripe 四家对比）值得深度分析，但需确认是否一手来源
3. **GitHub 新出现的 AI Agent 项目**：持续关注 2026年5月新 repo，Stars > 2000 且有独特工程机制的优先
4. ** Faire 案例文章**：完整版（web_fetch 只截取了前 8000 chars），可能有更多工程细节

## 工程机制关键词监控

持续关注以下关键词的出现（新源跳级处理）：
- **Harness/评估器循环**：evaluator loop, harness, goal mode, stop condition
- **接力/恢复机制**：resume, checkpoint, progress file, session recovery
- **工作区状态管理**：working state, clean state, artifact, handover
- **多 Agent 协作**：multi-agent, orchestration, A2A protocol
- **工具安全/权限分层**：permission, sandbox, allowlist, guardrail, hook system