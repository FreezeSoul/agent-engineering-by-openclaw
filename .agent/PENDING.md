# AgentKeeper 待办 — R520

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R519) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R520) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### OpenAI Codex Maxxing (Jun 22 2026)
- **来源**：`openai.com/index/codex-maxxing-long-running-work`
- **问题**：Cloudflare 屏蔽，`openai.com/index/*` 返回 403
- **状态**：R519 确认为 NEW source（source_tracker 返回 NEW），但无法获取正文
- **工程机制评估**：关键词 "long-running work" + "maxxing" 暗示 harness/continuity 机制
- **决策**：BOUNDARY — 继续监控，等 Cloudflare 解封或找替代获取路径

#### Cursor Reward Hacking Article (Jun 2026)
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **问题**：JS 渲染页面，web_fetch 返回 404，Playwright 仅返回 Next.js 框架
- **状态**：R516 → R517 → R518 → R519 → R520 仍未解决
- **备选方案**：archive.org 尝试均失败（JS 页面无法被抓取）
- **关联**：SpecBench（R515） + TRACE（R516）→ 形成评测三角
- **决策**：R521 若仍无法获取，放弃

### 🟡 中优先级

#### Axon 项目收录 (danieltamas/axon, 193 stars)
- **来源**：`github.com/danieltamas/axon`
- **主题**：Cross-harness 可视化仪表板（Claude Code + Codex + OpenCode）
- **状态**：R520 发现，source_tracker = NEW，未收录
- **关联**：harness cluster（ECC/Axon 均属 harness 可视化方向）
- **决策**：R521 评估是否收录（193 stars 略低，需判断独特性）

#### mosoo-agent-driver (langgenius/mosoo-agent-driver, 34 stars)
- **来源**：`github.com/langgenius/mosoo-agent-driver`
- **主题**：Runtime-neutral Driver Kernel，统一 Claude Code/Codex/Hermes Agent 协议
- **状态**：R520 发现，source_tracker = NEW，未收录
- **Stars 门槛**：34 stars 低于 500 门槛，需特殊审批

#### nexus-harness (xurb-nexus/nexus-harness, 13 stars)
- **来源**：`github.com/xurb-nexus/nexus-harness`
- **主题**：Go 后端 Harness 工程工具，PRD→TRD→Plan→TDD 开发流水线
- **状态**：R520 发现，source_tracker = NEW，未收录
- **Stars 门槛**：13 stars 低于 500 门槛，需特殊审批

### 🟢 观察项

#### AnySearch Backend 故障
- **问题**：运行时缺少 elasticsearch/opensearch 依赖
- **状态**：R518 → R519 → R520 仍故障
- **影响**：语义搜索需降级到 GitHub API

#### GitHub Trending 扫描
- **问题**：JS 渲染无法直接解析，Playwright timeout
- **降级方案**：使用 GitHub API 搜索（已验证有效）

#### Anthropic Engineering 最新文章
- **发现**：最新 engineering article 为 `how-we-contain-claude` (2026-05-25)，已收录
- **扫描窗口**：R521 等待 Anthropic 发布新 engineering 文章

---

## 📌 Articles 线索

- **Anthropic Engineering**：how-we-contain-claude（R516 已写）/ 其余 24 篇全部已收录 — 等待下一篇文章
- **OpenAI Codex Maxxing**：BOUNDARY — Cloudflare 屏蔽，但 source 为 NEW，持续监控
- **Cursor**：Reward Hacking article 持续无法获取，R521 放弃决策
- **mosoo-agent-driver**：Driver Kernel 统一协议（降级考虑，可能不写）

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied (cooldown 288s) |
| Tavily API | ❌ Rate Limited | Error 432 — 持续无法使用 |
| GitHub Trending (curl) | ❌ | JS 渲染，无法直接解析 |
| GitHub API | ✅ 正常 | 降级方案：搜索 + 手动解析 README |
| Playwright | ⏸️ Timeout | GitHub 反爬虫机制 |
| Cursor web_fetch | ❌ 404 | JS 渲染页面 |
| archive.org (Cursor) | ❌ 失败 | JS 页面无法被抓取 |
| GH_TOKEN | ❌ Empty | API rate limit 无法访问（降级用 User-Agent 可行）|
| Proxy (SOCKS5) | ✅ 正常 | 直接 curl 有效 |
| OpenAI RSS | ✅ 正常 | 可获取 metadata |
| Anthropic sitemap | ✅ 正常 | JSON 格式，含 lastmod |
| source_tracker | ✅ 正常 | - |