## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-22 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-22 | 每次必执行 |

## ⏳ 待处理任务

<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### 本轮新增
- ✅ `anthropic.com/engineering/AI-resistant-technical-evaluations` → 写作完成（AI-Resistant Take-Home 三次迭代，2026-01-21）
- ✅ `anthropic.com/engineering/infrastructure-noise` → 已有文章覆盖（infrastructure-noise-agentic-coding-evals-2026.md），确认追踪状态

### 下轮可研究的方向
- **Cursor「continually improving agent harness」**：`cursor.com/blog/continually-improving-agent-harness`（Apr 30, 2026），Harness 迭代哲学、Context Window 演变、Eval 体系
- **Anthropic「Scaling Managed Agents」**：`anthropic.com/engineering/managed-agents`（Apr 8, 2026），brain/hands 解耦设计
- **Anthropic「Harness Design for Long-Running」**：`anthropic.com/engineering/harness-design-long-running-apps`（Mar 24, 2026），长时间运行 Agent 防护设计
- **GitHub Trending 持续扫描**：关注 multi-agent orchestration 新项目

## 🔄 本轮同步闭环情况
- ✅ Articles：1篇新增（Anthropic AI-Resistant Take-Home Evaluations）
- ✅ Projects：1篇新增（ECC，188K Stars，Agent Harness 性能优化）
- ✅ 闭环：Article（AI评估设计）+ Project（Harness性能优化）→ Eval基础设施 × Harness工程 双层闭环
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条新源）

## ⚠️ 已知问题
- **GitHub Trending 解析失败**：curl 直接抓取 HTML 解析不可靠，需改用 Playwright headless 或更鲁棒的方案
- **Anthropic blog article 直接 curl 获取内容困难**：需依赖标题/h1 标签确认文章标题，但正文内容提取需进一步优化

## 📊 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles | 1（Anthropic AI-Resistant Take-Home，2026-01-21） |
| 新增 projects | 1（ECC，188,394 Stars） |
| 原文引用数量 | Article 1处 / Project 1处 |
| Commit | 待提交 |
