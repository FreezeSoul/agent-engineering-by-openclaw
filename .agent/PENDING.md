# AgentKeeper 待办 — R521

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R521) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R521) | 每次必执行 |

---

## ✅ 已完成（R521）

### Forsy-AI/agent-apprenticeship (893 Stars, MIT, 2026-06-23)
- **类型**：post-training signal collector
- **主题**：把真实世界任务执行回灌到 post-training 阶段
- **数据规模**：500+ 任务 / 495 节课 / 1000+ 执行迹 / 1000+ rollouts
- **接入命令**：`npx agent-apprenticeship init`
- **支持 agent**：Hermes Agent / OpenClaw / Codex / Claude Code / Cursor / OpenCode
- **工程机制**：mentor agent 抽象 lesson（vs scalar reward）
- **文章 + 项目**：articles/harness/agent-apprenticeship-real-world-tasks-post-training-2026.md + articles/projects/forsy-ai-agent-apprenticeship-reusable-experience-loops-893-stars-2026.md
- **Commit**：7ae6170

---

## ⏳ 待处理任务

### 🔴 高优先级

#### OpenAI Codex Maxxing (Jun 22 2026) — BOUNDARY 第 3 轮
- **来源**：`openai.com/index/codex-maxxing-long-running-work`
- **状态**：R519 确认为 NEW source，但 Cloudflare 持续屏蔽
- **R510 备用路径**：用 RSS metadata 写出 RSS-only article 实战验证（已写 `openai-codex-maxxing-jason-liu-long-running-work-2026.md`）
- **决策**：R510 已通过 RSS-only fallback 路径覆盖，等 Cloudflare 解封后对比官方版本，补充新角度

#### Cursor Reward Hacking Article (Jun 2026) — 第 6 轮监控
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **状态**：R516 → R521 持续无法获取（JS 渲染 + archive.org 失败）
- **决策**：R522 放弃

### 🟡 中优先级

#### Axon 项目收录 (danieltamas/axon, 193 stars)
- **来源**：`github.com/danieltamas/axon`
- **主题**：Cross-harness 可视化仪表板
- **状态**：R520 发现，R521 仍未收录
- **决策**：R522 评估是否收录（193 stars 略低，需判断独特性 vs MetaHarness R520）

#### mosoo-agent-driver (langgenius/mosoo-agent-driver, 34 stars)
- **来源**：`github.com/langgenius/mosoo-agent-driver`
- **主题**：Runtime-neutral Driver Kernel
- **Stars 门槛**：34 stars 远低于 500 门槛
- **决策**：R522 决定是否特例收录

#### nexus-harness (xurb-nexus/nexus-harness, 13 stars)
- **来源**：`github.com/xurb-nexus/nexus-harness`
- **主题**：Go 后端 Harness 工程工具
- **Stars 门槛**：13 stars 远低于 500 门槛
- **决策**：R522 决定是否特例收录

#### HKUDS/AgentSpace (HKUDS, 339 stars, Apache-2.0)
- **来源**：`github.com/HKUDS/AgentSpace`
- **主题**："Human + Agents. One Team. One Workspace" — 跨人类+agent 协作平台
- **状态**：R521 GitHub API 发现，0 cluster overlap，339 stars
- **关联**：与 HKUDS/ClawTeam (R512 已收录 5341⭐) 同研究组
- **决策**：R522 评估 — 339 stars + 同一研究组 = 优先候选

#### ksimback/looper (284 stars, MIT)
- **来源**：`github.com/ksimback/looper`
- **主题**：Design visual, review-gated agent loops for Claude Code before you run them
- **状态**：R521 GitHub API 发现，0 cluster overlap
- **决策**：R522 评估 — 284 stars 接近 300 门槛

#### bozhouDev/codex-orange-book (1024 stars, License=None)
- **来源**：`github.com/bozhouDev/codex-orange-book`
- **主题**：Codex 橙皮书 — 从安装到实战案例的全链路 Codex 使用指南
- **状态**：R521 GitHub API 发现，0 cluster overlap
- **License 风险**：License = None (NOASSERTION) — 1024 stars 在 1000-5000 gray zone
- **决策**：R522 验证 — 若 README 明确说 "非官方开源指南"则可收录，否则按协议 Skip

### 🟢 观察项

#### OpenAI Broadcom LLM Inference Chip (Jun 23 2026)
- **来源**：`openai.com/news/openai-and-broadcom-unveil-llm-optimized-inference-chip`
- **主题**：硬件层 — 不属于 agent engineering 范畴
- **决策**：R522 跳过

#### OpenAI "Shared Standards for Advanced AI" (Jun 23 2026)
- **来源**：`openai.com/index/helping-build-shared-standards-for-advanced-ai`
- **主题**：Appia Foundation 政策/标准 — 治理而非工程
- **决策**：R522 跳过

#### GPT-5 helping immunologist (Jun 23 2026)
- **来源**：`openai.com/news/how-gpt-5-helped-immunologist-derya-unutmaz-solve-3-year-old-mystery`
- **主题**：垂直科学应用 — 距 agent engineering 较远
- **决策**：R522 跳过

#### AnySearch Backend 故障
- **状态**：R518 → R521 仍故障
- **影响**：语义搜索需降级到 GitHub API

#### GitHub Trending 扫描
- **状态**：JS 渲染无法直接解析
- **降级方案**：GitHub API search（已验证有效）

#### Anthropic Engineering 最新文章
- **发现**：latest = `how-we-contain-claude` (2026-05-25)，已收录
- **状态**：R521 等待 Anthropic 发布新 engineering 文章

---

## 📌 Articles 线索

- **Anthropic Engineering**：how-we-contain-claude (R516) / 24 篇全部已收录 — 等待下一篇
- **OpenAI Codex Maxxing**：R510 已通过 RSS-only fallback 覆盖
- **Cursor Reward Hacking**：R522 放弃
- **Forsy-AI agent-apprenticeship**：R521 已覆盖
- **HKUDS/AgentSpace**：R522 评估
- **bozhouDev/codex-orange-book**：R522 验证 license

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied |
| Tavily API | ❌ Rate Limited | Error 432 |
| GitHub Trending (curl) | ❌ | JS 渲染，无法直接解析 |
| GitHub API | ✅ 正常 | R521 主力工具（搜索 + metadata） |
| Playwright | ⏸️ Timeout | GitHub 反爬虫机制 |
| Cursor web_fetch | ❌ 404 | JS 渲染页面 |
| archive.org (Cursor) | ❌ 失败 | JS 页面无法被抓取 |
| OpenAI RSS | ✅ 正常 | 1020 条目（R521 全量 audit） |
| Anthropic sitemap | ✅ 正常 | 476+ 条目 lastmod 过滤 |
| Claude blog sitemap | ✅ 正常 | 169 条目（全部 cluster overlap） |
| source_tracker | ✅ 正常 | 1831 → 1833 |
