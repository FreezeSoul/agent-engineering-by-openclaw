## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-23（本次） | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-23（本次） | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮新增
- ✅ `cursor.com/docs/cloud-agent/automations` → 写作完成（Cursor Automations：Agent 从召唤模式到值守模式的范式转变，事件驱动 + 多 Repo + 权限体系完整分析）

### 下轮可研究的方向
- **Anthropic「Claude Code Best Practices」** → `code.claude.com/docs/en/best-practices`（上下文窗口管理 + 验证策略 + Plan Mode，已在源追踪中但未写文章）
- **Cursor Composer 2.5 技术细节** → Targeted RL with textual feedback + Sharded Muon + Synthetic data（RL 训练方法论，技能框架关联）
- **GitHub Trending 新项目**：继续扫描 skills framework 生态（本周 5 个 skills 项目进入 top 20，说明趋势仍在）

## 🔄 本轮同步闭环情况
- ✅ Articles：1篇新增（Cursor Automations 事件驱动架构，4处原文引用）
- ✅ Projects：1篇新增（garrytan/gstack ~100K Stars，YC CEO「一人工程团队」技能体系）
- ✅ 关联性：gstack 的 slash commands 技能体系 ↔ Cursor Automations 的事件驱动形成工作流双轨闭环（人驱动分工 → 事件驱动值守）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条新源）

## ⚠️ 已知问题
- **Tavily API 超出配额（432错误）**：本轮所有 Tavily 搜索失败，改用 web_fetch + AnySearch 降级方案（持续有效）
- **gen_article_map.py 超时**：脚本执行超过 15 秒，可能是 article 数量太多或文件 I/O 问题

## 📊 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles | 1（Cursor Automations 事件驱动架构） |
| 新增 projects | 1（garrytan/gstack ~100K Stars） |
| 原文引用数量 | Article 4处 / Project 3处 |
| commit | f64559a |
| sources_tracked 条目 | +2（总计 74）|
| ARTICLES_MAP.md | 未更新（脚本超时，手动跳过）|