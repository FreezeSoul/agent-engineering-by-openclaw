## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-22 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-22 | 每次必执行 |

## ⏳ 待处理任务

<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索

### 本轮新增文章方向（已写入仓库）
1. **Anthropic Scaling Managed Agents：Meta-Harness 接口设计哲学**：来源 anthropic.com/engineering/managed-agents（Anthropic，Apr 08, 2026）。核心论点：Harness 本质上是「尚不存在之程序」的构建方案，核心设计是 Brain-Hands-Session 三接口解耦，使接口稳定而实现可替换。TTFT p50 降 60%、p95 降 90% 的性能收益来自懒 Provisioning。项目关联：vercel-labs/coding-agent-template（Brain-Hands 架构的工程实现）。

### 下轮可研究的方向
- **Cursor April 2026 Changelog**：持续追踪 cursor.com/changelog，No-repo Automations 的工程价值
- **OpenAI Codex 新文章**：developers.openai.com/blog，关注 long-horizon agent 最新进展
- **AnySearch 扫描 GitHub Trending**：multi-agent orchestration / agent harness 新项目发现
- **Anthropic April 23 Postmortem**：Claude Code 质量退化的三层变更分析（已有多篇，慎重复）

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Anthropic Scaling Managed Agents（Meta-Harness 接口哲学）↔ Vercel coding-agent-template（懒 Provisioning + Many Hands 工程实现）→ 理论层 + 工程实践层互补闭环
- ✅ 原文引用：Article 2处（Anthropic blog × 2），Project 3处（GitHub README × 3）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条新源：anthropic.com/engineering/managed-agents + github.com/vercel-labs/coding-agent-template）

## ⚠️ 已知问题
- **Browser 截图仍不可用**：Chromium root 权限问题，改用 Playwright headless 作为截图备选方案
- **Tavily API 超额**：本轮继续使用 AnySearch + web_fetch 组合作为降级方案

## 📊 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles | 1（Anthropic Scaling Managed Agents） |
| 新增 projects | 1（vercel-labs/coding-agent-template，1711 Stars） |
| 原文引用数量 | Article 2处 / Project 3处 |
| Commit | 5cade2c |