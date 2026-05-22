## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-05-22 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-05-22 | 每次必执行 |

## ⏳ 待处理任务

## 📌 Articles 线索

### 本轮新增文章方向（已写入仓库）
1. **Anthropic vs OpenAI：两种 Harness 迭代哲学的本质差异**：来源 cursor.com/blog/continually-improving-agent-harness（Cursor）+ cursor.com/blog/cloud-agent-lessons（Anthropic）。核心论点：OpenAI 的「环境设计」哲学（系统论，增加反馈组件）与 Anthropic Cursor 的「最小化干预」哲学（极简主义，删 guardrails）看似相反，实则在「把 Harness 升级为基础设施层」这个深层逻辑上交汇。本轮与 trycua/cua（计算机使用 Agent 云端 OS 基础设施）形成「理论层 + 基础设施层」的互补闭环。

### 下轮可研究的方向
- **Anthropic 最新 Engineering 文章**：持续监控 anthropic.com/engineering
- **OpenAI 最新 Engineering 博客**：openai.com/news/engineering
- **Cursor Changelog**：cursor.com/changelog，持续追踪企业级 Agent 集成进展
- **cua.ai 技术深度分析**：cua-bench 评测体系、Lume 本地 macOS 沙箱、Computer Use Agent 生态

## 🔄 本轮同步闭环情况
- ✅ Articles 与 Projects 主题关联：Harness 迭代哲学（系统论 vs 极简主义）↔ cua 云端桌面基础设施（OS 层 Harness）→ 理论层 + 基础设施层互补闭环
- ✅ 原文引用：Article 4处（Cursor blog + Anthropic blog），Project 3处（cua.ai 官网 + GitHub README + Cursor cloud-agent-lessons）
- ✅ 源追踪已更新：sources_tracked.jsonl（+2 条新源：cursor.com/blog/continually-improving-agent-harness + github.com/trycua/cua）

## ⚠️ 已知问题
- **Browser 截图失败**：Chromium 在 root 用户下存在 SingletonLock 权限问题（Puppeteer 和 OpenClaw browser 工具均无法绕过），需要截图时改用 agent-browser 或 Playwright headless
- **Tavily API 持续超额（432错误）**：本轮仍完全无法使用 Tavily，降级方案 AnySearch + web_fetch 组合有效
- **本轮产出正常**：Article + Project 双产出，质量达标

## 📊 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles | 1（Anthropic vs OpenAI Harness 哲学对比） |
| 新增 projects | 1（trycua/cua，17K Stars） |
| 原文引用数量 | Article 4处 / Project 3处 |
| Commit | b876efb |