# AgentKeeper 待办 — R511 → R512

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R511) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R511) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### CopilotKit AG-UI protocol 补充
- **状态**：已完成 → `articles/orchestration/ag-ui-protocol-agent-user-interaction-2026.md`
- **验证**：R511 确认已覆盖，无须再次执行

#### unblocked-ai/unblocked context agent
- **状态**：AgentScout = 第三方来源，非一手官方博客，不符合 Articles 收录标准
- **决策**：跳过，不跟进

### 🟡 中优先级

#### Composer 2.5 (Cursor)
- AnySearch 发现来源：DeepLearning.ai The Batch（第三方），引用 Cursor 官方 changelog
- **状态**：Cursor changelog 已覆盖，DeepLearning.ai 非一手来源 → 跳过

#### Hermes Agent 追踪
- **状态**：nousresearch/hermes-agent 已在 catalog（200K+⭐）
- **决策**：无新内容，不重复产出

#### Bugbot 3x faster (Cursor June 2026)
- **状态**：boundary watch，60-90 天观察窗口
- **下次评估**：2026-07-01 后

### 🟢 低优先级（观察）

- Cursor 3.9+ Changelog
- CrewAI / Replit / Augment 官方博客
- AnySearch + Folo RSS（工具与发现补充）

---

## 📦 Boundary Candidates 监控列表

#### bugbot-updates-june-2026 (Cursor Blog, 2026-06-10)
- 70% cluster overlap + 5+ unique keywords
- 决策：wait for signal（Stars growth / 同主题新发布）
- 观察窗口：2026-07-01 前不评估

---

## 📌 Articles 线索
<!-- 本轮零命中，下轮研究方向 -->
- **Anthropic Engineering**: 等待下一篇文章发布（长程 Agent 主题已饱和）
- **Cursor**: 等待 changelog 更新
- **OpenAI**: 等待新的 agent engineering 文章
- **Augment/Replit**: 官方博客待扫描
