## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-20 | 2026-05-20 |
| PROJECT_SCAN | 每轮 | 2026-05-20 | 2026-05-20 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 本轮新增文章方向（已写入仓库）
1. **Cursor Agent Harness 持续改进工程** — 上下文从 Guardrails 到动态拉取、离线+在线双层评估体系、模型适配到版本级别、Mid-Chat 切换机制

### 下轮可研究的方向
- Anthropic Scaling Managed Agents（Apr 8）：Decoupling brain from hands 的工程实践
- Anthropic Harness Design for Long-Running Apps（Mar 24）：生产级 Agent 的持久化 harness 设计
- OpenAI Responses API WebSocket mode：实时 agent 通信的底层架构

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Cursor harness 改进（单 Agent 内部治理）↔ Hermes Control Room（多 Agent 治理结构），共同构成 Harness Engineering 的内外两个层次
- ✅ 原文引用：Article 3处，Project 2处
- ✅ 源追踪已更新：sources_tracked.jsonl

## ⚠️ 已知问题
- Tavily API 今日配额已超（432 错误），降级使用 GitHub API 直接查询
- AnySearch 匿名模式可用但首次搜索延迟较高
- Cursor/Anthropic 工程博客发现多个未覆盖的新内容（scaling managed agents、harness design for long-running），下轮可深度扫描