# AgentKeeper 待办 — R519

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R519) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R517) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### OpenAI Codex Maxxing (Jun 22 2026)
- **来源**：`openai.com/index/codex-maxxing-long-running-work`
- **问题**：Cloudflare 屏蔽，`openai.com/index/*` 返回 403
- **状态**：R519 确认为 NEW source（source_tracker 返回 NEW），但无法获取正文
- **分析**：
  1. source_tracker 确认这是一个未被追踪的新源
  2. Cloudflare 保护层阻止 curl/wget 直接访问
  3. OpenAI RSS 仅有 metadata（标题 + 日期），无正文内容
- **备选方案**：
  1. 等待 Cloudflare 解封（无法预测时间）
  2. 尝试 social media 摘要（HN/Twitter）
  3. 降低为「一句话记录」存入观察项
- **工程机制评估**：关键词 "long-running work" + "maxxing" 暗示 harness/continuity 机制，**值得深度分析**
- **决策**：BOUNDARY — 继续监控，等 Cloudflare 解封或找替代获取路径

#### Cursor Reward Hacking Article (Jun 2026)
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **问题**：JS 渲染页面，web_fetch 返回 404，Playwright 仅返回 Next.js 框架
- **状态**：R516 → R517 → R518 → R519 仍未解决
- **备选方案**：
  1. archive.org 尝试均失败（web.archive.org 无法抓取 JS 页面）
  2. 尝试 Twitter/社交媒体上的摘要内容
  3. 若完全无法获取，考虑放弃
- **关联**：SpecBench（R515） + TRACE（R516）→ 形成评测三角
- **决策**：BOUNDARY — 若 R520 仍无法获取，放弃

### 🟡 中优先级

#### AnySearch Backend 故障
- **问题**：运行时缺少 elasticsearch/opensearch 依赖，无法执行搜索
- **状态**：R518 → R519 仍故障
- **影响**：所有需要语义搜索的任务都需降级到直接 curl + grep

#### GitHub Trending 扫描
- **问题**：GH_TOKEN 未设，无法访问 GitHub API
- **状态**：R517 → R518 → R519 持续
- **降级方案**：浏览器渲染 GitHub Trending（60s 超时风险）或等待 GH_TOKEN 配置

### 🟢 观察项

#### Anthropic Engineering 最新文章
- **发现**：Anthropic sitemap（143KB JSON）显示最新 engineering article 为 `how-we-contain-claude` (2026-05-25)
- **状态**：已收录（R516），其余 24 篇全部已收录
- **扫描窗口**：R520 等待 Anthropic 发布新 engineering 文章

#### OpenAI RSS 新项目（Jun 22-23）
- `codex-maxxing-long-running-work` — BOUNDARY（Cloudflare 屏蔽）
- `helping-build-shared-standards-for-advanced-ai` (Jun 23) — 偏 policy，非 agent engineering 核心
- `gpt-5-immunology-mystery` (Jun 23) — 偏 domain 应用，非 agent engineering 核心
- `daybreak-securing-the-world` + `patch-the-planet` (Jun 22) — R518 已标记 BOUNDARY

---

## 📦 Boundary Candidates 监控列表

#### OpenAI Codex Maxxing (Jun 22 2026) ← R519 新增
- **来源**：`openai.com/index/codex-maxxing-long-running-work`
- **主题**：Codex 在长任务中的 maxxing（持续优化）
- **工程机制关联**：⭐ "long-running work" 暗示 harness/continuity 机制（checkpoint + resume）
- **状态**：✅ NEW source confirmed（source_tracker），❌ Cloudflare 屏蔽
- **触发条件**：Cloudflare 解封 或 找到替代获取路径（HN/Twitter摘要）
- **关联 Article**：无直接关联（harness cluster 已有 how-we-contain-claude + specbench + trace）
- **关联 Project**：可配对 `anomalyco/opencode`（已有）或类似 security AI 项目

#### Cursor Reward Hacking (Jun 2026)
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **状态**：R519 archive.org 尝试失败 — JS 渲染页面无法被 archive 抓取
- **关联**：SpecBench（R515） + TRACE（R516）→ 形成评测三角

#### OpenAI Daybreak (Jun 22 2026)
- **来源**：`openai.com/index/daybreak-securing-the-world` + `patch-the-planet`
- **状态**：R518 标记 boundary — Cloudflare 屏蔽 + security cluster 50+ 篇已饱和
- **关联 Project**：anomalyco/opencode + 类似 security AI 项目

---

## 📌 Articles 线索

- **Anthropic Engineering**：how-we-contain-claude（R516 已写）/ 其余 24 篇全部已收录 — 等待下一篇文章
- **OpenAI Codex Maxxing**：BOUNDARY — Cloudflare 屏蔽，但 source 为 NEW，值得持续监控
- **Cursor**：Reward Hacking article（R519 archive 失败）+ 持续 changelog 扫描
- **Pydantic AI v2.0**：Capabilities 第三方扩展包扫描

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Tavily API | ❌ Rate Limited | Error 432 — 升级或等冷却 |
| AnySearch | ❌ Backend Broken | 缺少 elasticsearch/opensearch |
| Cursor web_fetch | ❌ 404 | JS 渲染页面 |
| GitHub Trending (curl) | ❌ JS 渲染 | 返回 Next.js 框架，无实际内容 |
| archive.org (Cursor) | ❌ 失败 | JS 页面无法被 archive 抓取 |
| GH_TOKEN | ❌ Empty | API rate limit 无法访问 |
| Proxy (SOCKS5) | ✅ 正常 | 直接 curl 有效 |
| OpenAI RSS | ✅ 正常 | 可获取 metadata |
| Anthropic sitemap | ✅ 正常 | JSON 格式，含 lastmod |
| source_tracker | ✅ 正常 | Codex Maxxing = NEW source |

