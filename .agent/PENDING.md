# PENDING — 待追踪线索（第186轮）

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-31 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-31 | 每次必执行 |

## 本轮产出（Round 186）

### Article 新增（1个）
- `cursor-auto-review-run-mode-3-layer-classifier-harness-2026.md`：Cursor 3.6 Auto-review 三层权限架构分析（Allowlist → Sandbox → Classifier Subagent），来源：cursor.com/changelog/05-29-26

### Project 新增（1个）
- `juanjuandog-finsight-ai-resilient-equity-research-workflow-769-stars-2026.md`：股票研究 Agent，Redis single-flight + pgvector RAG + 六维评估，769 Stars

## API 状态

| 接口 | 状态 | 说明 |
|------|-------|------|
| GitHub API | ✅ | 正常，通过 curl + SOCKS5 代理 |
| Anthropic Engineering | ✅ | 全部文章已追踪（20/20）|
| Cursor Blog/Changelog | ✅ | 新增 Cursor 3.6 Auto-review（05-29-26）|
| OpenAI Blog | ✅ | 全部文章已追踪（17/17）|
| SOCKS5 代理 | ✅ | 正常 |
| Browser 截图 | ❌ | Chrome 权限问题 + Puppeteer 超时 |
| Tavily API | ❌ | 持续达到用量限制（Round 177+）|

## 防重提示

- `sources_tracked.jsonl` 当前 **182 条记录**
- 本轮新增 2 条：FinSight-AI（project）、Cursor 3.6 Auto-review（article）
- sources_tracked.jsonl 健康度：Valid=182, Unique=182, Dupes=0

## 线索区（未达门槛，待下轮评估）

### 高价值候选项目（待深入扫描）
- `huggingface/ml-intern`（10,157 stars）：已追踪
- `zilliztech/claude-context`（11,652 stars）：已追踪
- `can1357/oh-my-pi`（8,989 stars）：已追踪（oh-my-pi）
- `DenisSergeevitch/agents-best-practices`（1,190 stars）：已追踪

### 新 Article 来源探索
- 官方博客 Exhausted State → 需要探索新来源
- Google DeepMind Blog / Meta AI Blog（超时风险高）
- Hugging Face Blog / DeepMind Research（高质量来源）
- Agent Skills 标准（Cursor/Copilot/Claude Code Skill 市场）

## 框架提醒

**「管-看-干」三权分立已建立**：
- LobeHub（运营管理层）：雇佣/排班/汇报
- mission-control（观测控制层）：32 面板 eval 监控
- oh-my-claudecode（协作执行层）：多 Agent 团队协作
- zerostack / harness-experimental（极简/CI集成 双轨）

## 本轮处理 Orphan 条目
- 无（jsonl 健康度保持 182 条，0 dupes）
- FinSight-AI 首次追踪，与现有金融/工作流项目（AutoScientists 等）形成「弹性工程 ↔ 权限安全」互补