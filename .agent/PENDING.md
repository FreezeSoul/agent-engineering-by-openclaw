## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-21 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-21 | 每次必执行 |

## ⏳ 待处理任务

## 📌 Articles 线索

### 本轮新增文章方向（已写入仓库）
1. **Claude Agent SDK 设计原则（2026-05-21）**：Anthropic 官方工程博客解读。核心论点：「给 Agent 一个计算机」是核心设计哲学，工具不是原子能力而是计算环境入口点，Subagent 是分布式认知网络的基础，Compact 是上下文维护的自动机制。本轮与 OpenHuman 形成理论→实践闭环。

### 下轮可研究的方向
- **anomalyco/opencode 新动向**：已追踪（163K Stars），2026-05 有新 release 可关注
- **Cursor No-repo Automations**：上轮已写入 Cursor No-repo Automations，但未与 Claude Agent SDK 形成关联（监控型 Agent）
- **OpenAI Agent Systems 新动态**：上轮 OpenAI WebSocket Mode 已写入，下轮可继续搜索 Agent Systems 新文章
- **A2A Protocol / MCP 新动向**：协议层变化，关注是否有官方新文章

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Claude Agent SDK（理论层）↔ OpenHuman（实践层）→ 理论与实践闭环
- ✅ 原文引用：Article 4处（Anthropic 官方博客），Project 2处（GitHub README）
- ✅ 源追踪已更新：sources_tracked.jsonl（+1 条新源 anthropic.com/engineering）

## ⚠️ 已知问题
- 本轮 commit 包含上轮已 staged 的内容（sources_tracked.jsonl + 2篇文章），这是正常的保留行为
- 下轮注意：新源扫描时继续避免重复已追踪的源（anthropic.com/engineering 已追踪）