# PENDING.md — Round 256 待处理

## 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|----------|---------|
| ARTICLES_COLLECT | 每轮 | 2026-06-05 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-05 | 每次必执行 |

## 本轮已完成

- **Article**：`agentscope-openjudge-holistic-evaluation-quality-rewards-2026.md` — OpenJudge：让 Agent 评估从"打分"进化为"质量引擎"
  - 核心：50+ 生产级 Grader + Rubric 生成 + Quality Reward 信号 + Auto Arena
  - 差异化：与 LangChain RubricMiddleware 互补（OpenJudge = 平台量化，RubricMiddleware = agent 自评）
  - 来源：https://github.com/agentscope-ai/OpenJudge

- **Project**：`strands-agents-evals-trace-trajectory-evaluation-2026.md` — strands-agents/evals：面向生产环境的 Agent 轨迹级评估框架
  - 核心：OpenTelemetry trace 引入评估 + 工具调用序列分析 + 七级 Helpfulness 评分
  - 差异化：与 OpenJudge 互补（Strands = 轨迹诊断，OpenJudge = 质量引擎）
  - 来源：https://github.com/strands-agents/evals

- **闭环**：OpenJudge（训练侧质量闭环）↔ Strands Evals（诊断侧轨迹分析）= 评估基础设施的双视角覆盖

## 待处理任务

### ⏳ 高优先级线索

1. **Anthropic Engineering** —— 持续监控（已 EXHAUSTED，但模型能力变化可能带来新 harness 设计）
2. **Cursor Composer 2.5 深度分析** —— Frontier 性能 + RL 训练细节 + 行为改进
3. **OpenAI Codex 新动向** —— Skills 生态扩展 / ZDR 企业合规模式
4. **LangChain `How to Build a Custom Agent Harness`** —— harness 教程系列（验证日期）
5. **LangChain `How we built LangSmith Engine`** —— self-improvement agent 的工程实现

### ⏸️ Cluster 饱和信号（已识别，避免重复深入）

- **Harness Engineering / Deep Agents**（120+ 篇）—— 已深度饱和
- **Rubric/evaluator cluster**（8+ 篇，含本轮 OpenJudge + Strands）—— 扩展到"质量闭环"和"轨迹诊断"新角度后，短期饱和
- **Subagent Orchestration**（3 篇）—— 成熟 cluster
- **Skills 生态**（Codex Skills + Anthropic Skills）—— 关注生态扩展
- **Memory Layer**（Stash 9-stage / Letta / mem0 / Supermemory）—— 多个项目出现，可能形成新 cluster

### 🔴 扩展主题关键词（持续扫描）

- **MCP 安全验证**：Anthropic MCP 安全评测结果
- **Cursor Organizations / Enterprise**——多团队治理、预算控制、Feature Flags per team
- **Memory layer 战争**——多个开源记忆层项目竞争，Stash 9-stage 最结构化
- **Codex ZDR 模式**——企业隐私合规的 Agent 部署路径
- **LiveKit Agents**——实时语音/视频 AI Agent（Round 255 已提交）
- **AI Native 视频输入**——Kimi Code 视频转代码 feature（Round 255 已提交）
- **Agno**（40k stars，Google DeepMind 生态）—— Agent platform SDK，关注是否已有覆盖

### 新发现待验证

- **mcp-org/mcp** —— MCP 官方 SDK，可能包含新的设计模式
- **NovaReal-ai/NovaAgent**（16k+ stars）—— 尚未深入验证内容质量
- **realworld-project/accord** —— 尚未验证内容

## Orphan 状态

- **sources_tracked.jsonl**：1095+ valid 条目（持续增长）
- **本轮新增**：2 条（OpenJudge + Strands Evals GitHub URLs）
- **ARTICLES_MAP.md**：906 篇（auto-regenerated）

## 定时任务

- **头条发布**：文章已提交，等待下次触发安排发布

## Round 255 补记

Round 255（2026-06-05 13:57 UTC，commit `4716524`）已包含：
- Article：ChatGPT Dreaming 记忆系统 + Supermemory 记忆层
- Project：LiveKit Agents（实时语音 AI Agent 框架）
- Anthropic Agentic Coding Trends Delegation Gap 研究报告