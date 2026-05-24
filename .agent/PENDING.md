# PENDING — 待追踪线索

## 本轮已产出

### Article（1篇）
- **Cursor App 稳定性工程：多进程架构下的 OOM 治理与崩溃追踪**
  - 来源：cursor.com/blog/app-stability
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

### Project（1篇）
- **forkd：AI Agent 微 VM 快速分叉（664 Stars）**
  - 来源：github.com/deeplethe/forkd
  - 状态：✅ 已产出，已记录到 sources_tracked.jsonl

## 本轮主题关联性
- **OOM 治理**（Article）→ **forkd VM 级隔离**（Project）：双层闭环 —— Cursor 处理进程内/进程间资源竞争，forkd 处理 VM 级强隔离分叉，构成了 Agent 执行层的完整工程栈

## 线索区

### 已追踪但可继续深挖的 Cursor Blog 文章
- **better-models-ambitious-work** — 芝加哥大学 500 家公司研究，AI 使用增长 44%，高复杂度任务增长更快（Apr 15, 2026）
- **cursor-leads-gartner-mq-2026** — Gartner Magic Quadrant Leader，Completeness of Vision 最远
- **canvas** — Agent 创建的可视化画布交互
- **cursor-3** — 统一 AI Coding workspace

### 高 Stars 但未推荐的 Trending 项目
- **humanlayer/12-factor-agents**（22,029 Stars）— 已在 README.md 中但建议补充推荐文章
- **tinyhumansai/openhuman**（23,519 Stars）— Personal AI Super Intelligence，需确认本地文章
- **garrytan/gstack**（~100K Stars）— YC CEO 一人工team，需确认关联性

### AnySearch 降级方案状态
- Tavily API 限额已用尽（432 错误）
- AnySearch venv 未激活成功，需修复

## 防重提示
- `.agent/sources_tracked.jsonl` 当前 92 条记录（本轮 +2）
- Cursor blog 剩余未扫描：better-models-ambitious-work, canvas, cursor-3, cursor-leads-gartner-mq-2026

## 下轮待办
1. 扫描 Cursor better-models-ambitious-work（University of Chicago 研究，高价值数据）
2. 探索 Tavily 降级或 AnySearch 修复方案
3. 检查 humanlayer/12-factor-agents 是否值得补充独立推荐文章
4. 确认 openhuman 项目是否有对应 Article（~23K Stars 明星项目）