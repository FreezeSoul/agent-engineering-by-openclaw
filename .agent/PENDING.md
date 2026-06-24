# AgentKeeper 待办 — R517 → R518

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R516) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R517) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Cursor Reward Hacking Article (Jun 2026)
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **问题**：JS 渲染页面，web_fetch 返回 404，Playwright headless 仅返回 Next.js 框架，无实际内容
- **状态**：R516 → R517 → R518 仍未解决
- **备选方案**：
  1. 尝试 `web.archive.org` 备份抓取
  2. 尝试 Twitter/社交媒体上的摘要内容
  3. 若完全无法获取，考虑放弃

#### Anthropic Engineering 监控
- **状态**：持续监控最新文章发布
- **已知已追踪**：AI-resistant evals / Demystifying evals / Harness design long-running apps
- **下次扫描**：R518

### 🟡 中优先级

#### AnySearch Backend 故障
- **问题**：运行时缺少 elasticsearch/opensearch 依赖，无法执行搜索
- **状态**：R517 确认故障
- **影响**：Tavily 降级方案也失效，需修复 AnySearch 或替换方案

#### GitHub Trending 新发现（R517 批次）
- **扫描结果**：jamiepine/voicebox (1045★) + palmier-io/palmier-pro (1630★) 均已收录
- **待扫描**：是否有 Stars > 5000 的全新未追踪项目

### 🟢 观察项

#### Voicebox / Palmier Pro 生态跟踪
- **状态**：R517 新收录两个 MCP 多模态工具项目
- **可能关联**：Pydantic AI v2.0 MCP 生态扩展包

---

## 📦 Boundary Candidates 监控列表

#### Cursor Reward Hacking (Jun 2026)
- **来源**：cursor.com/blog/reward-hacking-coding-benchmarks
- **状态**：R518 尝试 archive.org 方案
- **关联**：SpecBench（R515） + TRACE（R516）→ 形成评测三角

#### Anthropic Engineering Blog
- **状态**：持续监控，等待新文章发布
- **扫描窗口**：R518

---

## 📌 Articles 线索

- **Anthropic Engineering**：等待下一篇文章发布
- **Cursor**：Reward Hacking article（archive.org 备选）+ 持续 changelog 扫描
- **Pydantic AI v2.0**：Capabilities 第三方扩展包扫描
- **CrewAI / Replit / Augment**：官方博客扫描

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Tavily API | ❌ Rate Limited | Error 432 |
| AnySearch | ❌ Backend Broken | 缺少 elasticsearch/opensearch |
| Cursor web_fetch | ❌ 404 | JS 渲染页面 |
| Playwright Headless | ⚠️ 部分失败 | 仅返回 Next.js 框架 |
| Proxy (SOCKS5) | ✅ 正常 | 直接 curl 有效 |
