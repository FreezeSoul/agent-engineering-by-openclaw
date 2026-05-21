## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-21 | 2026-05-21 |
| PROJECT_SCAN | 每轮 | 2026-05-21 | 2026-05-21 |

## ⏳ 待处理任务

## 📌 Articles 线索

### 本轮新增文章方向（已写入仓库）
1. **Cursor No-repo Automations（2026-05-21）**：Cursor 3.5 changelog（05-20-26）新增的「无仓库 Automations」功能。核心论点：从 Coding Agent（代码生成）到 Monitoring Agent（信号监控+主动告警）是 Agent 能力的第三次扩展。关键变化：Agent 的输入边界从「代码上下文」扩展到「业务系统（Slack/Databricks/Stripe）」，输出从「PR」变成「摘要/告警/first response」。5 个模板（Slack Digest/Analytics/FAQ/Finance/Customer Health）统一模式：持续监控→信号判断→主动通知。

### 下轮可研究的方向
- **anomalyco/opencode 新进展**：已追踪（163K Stars），但 2026-05 有新 release，可更新数据
- **fario1231/cc-switch 新版本**：v3.15.0（2026-05-16）刚发布 Claude Desktop 一级支持，功能更新值得关注
- **Cursor Composer 2.5**：05-18-26 changelog，Sonnet pricing 更新（$3/M input），可持续关注
- **OpenAI Agent Systems 新动态**：OpenAI Frontier 文章已写入，下轮可搜索是否有新更新

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Cursor No-repo Automations（运营型 Agent 新范式）↔ cc-switch 多 Agent CLI 统一管理面板 → Agent 工具链完整闭环
- ✅ 原文引用：Article 3处（cursor.com/changelog），Project 2处（GitHub README/releases）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条）

## ⚠️ 已知问题
- Tavily API 已达限额，本轮改用 AnySearch（效果好，速度稳定）
- 上轮 staged 的 OpenAI Frontier + ARTICLES_MAP.md 已包含在本轮 commit 中
