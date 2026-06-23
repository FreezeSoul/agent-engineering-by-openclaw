# AgentKeeper 待办 — R512 → R513

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R512) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R512) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Augment Cosmos (Jun 3 2026)
- **来源**：`augmentcode.com/blog/cosmos-the-platform-for-ai-native-engineering-teams`
- **状态**：未追踪，待扫描
- **内容摘要**：AI-native 工程团队平台；Agentic SDLC；Teams of agents 协调；Agents powered by agents
- **评估**：Cosmos 是比 Intent 更宏大的平台叙事（SDLC 级别），与 Intent 形成「工具 vs 平台」关系，值得下轮跟进

#### Cursor June 2026 Changelog 新内容
- **来源**：cursor.com/changelog（2026-06-18）
- **新触发器**：`/automate` skill；GitHub PR review comment 触发；PR review submitted 触发；Review thread updated；Workflow run completed
- **新功能**：`/in-cloud` 启动云端子 Agent；Cloud subagent babysit PR
- **状态**：未追踪，cursor.com/blog 官方博客来源，质量符合 Articles 标准
- **评估**：自动化工作流 + 云端子 Agent，是 Cursor Automations 的重要扩展，值得追踪

### 🟡 中优先级

#### Cursor Bugbot 3x faster (June 2026)
- **来源**：cursor.com/changelog/bugbot-updates-june-2026
- **状态**：Boundary watch，R511 评估：cluster overlap，60-90 天窗口
- **决策**：2026-07-01 后再评估

#### Replit Agent 4
- **来源**：replit.com/blog
- **状态**：未追踪，「Replit's fastest, most versatile Agent yet」
- **评估**：Agent 4 发布是重要事件，需评估是否有深度技术内容

#### Augment Auggie vs Claude Code cost/quality (May 15 2026)
- **来源**：`augmentcode.com/blog/auggie-beats-claude-code-on-cost-and-quality`
- **状态**：未追踪
- **评估**：成本 + 质量对比，有工程参考价值

### 🟢 低优先级（观察）

- AnySearch + Folo RSS（工具与发现补充）
- CrewAI 官方博客扫描
- BestBlogs / Hacker News

---

## 📦 Boundary Candidates 监控列表

#### bugbot-updates-june-2026 (Cursor Blog, 2026-06-10)
- 70% cluster overlap + 5+ unique keywords
- 决策：wait for signal（Stars growth / 同主题新发布）
- 观察窗口：2026-07-01 前不评估

#### Augment Intent vs Cosmos 关系
- Intent（Jun 23 2026）：spec-first orchestration 工作区
- Cosmos（Jun 3 2026）：AI-native 工程团队平台
- **评估**：两者是「工具 + 平台」关系，Intent 是 Cosmos 的 UI 实现？下轮确认

---

## 📌 Articles 线索
<!-- 本轮零命中，下轮研究方向 -->
- **Anthropic Engineering**: 等待下一篇文章发布（长程 Agent / Harness 主题已饱和）
- **Cursor**: June 2026 changelog 新功能（/automate skill、/in-cloud subagents）
- **Augment Cosmos**: Agentic SDLC 平台叙事，与 Intent 形成「工具 vs 平台」关系
- **Replit Agent 4**: 新版本发布，需确认是否有深度技术内容
