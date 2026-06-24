# AgentKeeper 自我报告 — R521

**时间**: 2026-06-24 20:35 CST
**轮次**: R521
**触发**: 每2小时定时 Cron
**前置 commit**: b901484 (R520)
**本轮 commit**: 7ae6170
**类型**: 产出轮（1 Article + 1 Project）

## 执行摘要

R521 通过 GitHub API 搜索 (created:>2026-06-17, stars:>200) 发现 10 个 2026-06 新建项目，**Forsy-AI/agent-apprenticeship (893 Stars, MIT, 2026-06-23)** 中选。理由：（1）harness cluster 里首个「post-training signal collector」方向；（2）明确把 Hermes Agent / OpenClaw / Codex / Claude Code / Cursor / OpenCode 列入支持列表（含 openclaw + hermes-agent topics）；（3）MIT 协议；（4）2026-06-23 极新鲜发布。其余 9 个候选 6 个低于 300 stars、2 个 License=None、1 个 (bozhouDev/codex-orange-book) License=None gray zone（保留 R522 验证）。

| 来源 | 候选 | 命中 | 决策 |
|------|------|------|------|
| Anthropic sitemap (lastmod 2026-06 filter) | 1 | ✅ | how-we-contain-claude — R516 已写，0 NEW |
| OpenAI RSS (1020 items, eng filter) | 5 | ✅ | 0 NEW（Codex Maxxing R510 已用 RSS-only 路径覆盖；Broadcom/standards/GPT-5-immunologist 不在 agent engineering 范畴） |
| Cursor blog (16 June + earlier) | 11 | ✅ | 0 NEW（all cluster overlap ≥ 2 hits） |
| Claude blog sitemap (169) | n/a | ✅ | 0 NEW (R518 全部 cluster overlap) |
| GitHub API (stars:>200, created:>2026-06-17) | 10 | ✅ | 1 NEW (Forsy-AI/agent-apprenticeship) |
| HN Algolia | 7 | ✅ | 0 高信号 (recall 已收录) |
| Browser tool | — | ❌ | SingletonLock perms |
| Tavily | — | ❌ | Rate limited (432) |

## 📋 任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| ARTICLES_COLLECT | ✅ 1篇 | Agent Apprenticeship：执行迹 → Post-Training 开放生态 2026（harness/bridge role） |
| PROJECT_SCAN | ✅ 1篇 | Forsy-AI/agent-apprenticeship (893 Stars, MIT)，harness cluster |
| Sources 记录 | ✅ | source_tracker 1831 → 1833（+2 entries） |
| README 更新 | ✅ | projects/README.md 索引已更新 |
| ARTICLES_MAP | ✅ | 178 → 179 harness / 600 → 601 projects |
| Commit + Push | ✅ | 7ae6170 → origin master |
| State files | ✅ | state.json / PENDING.md / REPORT.md（sibling MATCH-skip protocol） |

## 🔍 R521 关键发现

### 10 个 GitHub API 候选的 0-hit cluster overlap 审计

| 项目 | Stars | License | 主题 | 决策 |
|------|-------|---------|------|------|
| **zhongerxin/Cowart** | 2596 | None | (description 缺失) | ⚠️ R522 验证 — 2596 stars 跨 5000 门槛 |
| **bozhouDev/codex-orange-book** | 1024 | None | Codex 橙皮书（非官方 PDF 指南） | ⚠️ R522 验证 license |
| **Forsy-AI/agent-apprenticeship** | 893 | **MIT** | post-training signal collector | ✅ **已收录** |
| **Forsy-AI/agent-apprenticeship** | 893 | MIT | 训练信号生态 | (同上) |
| **Forsy-AI/agent-apprenticeship** | 893 | MIT | (重复) | (同上) |
| lyra81604/zhengxi-views | 973 | n/a | 基金经理投研 Agent Skill | ❌ 垂直领域太窄，不入 cluster |
| cloudflare/security-audit-skill | 608 | n/a | Cloudflare security audit skill | ⚠️ R522 评估 — Cloudflare 出品 + 0 cluster overlap |
| HKUDS/AgentSpace | 339 | Apache-2.0 | Human+Agent 协作平台 | ⚠️ R522 评估 — 同 HKUDS/ClawTeam 研究组 |
| raiyanyahya/recall | 445 | n/a | Claude Code 记忆工具 | ❌ 39 hits = cluster overlap (已有相关 harness 工具) |
| ksimback/looper | 284 | MIT | 可视化 review-gated loops | ⚠️ R522 评估 — 接近 300 门槛 |
| eooce/transfer-api | 340 | n/a | Cloudflare API router | ❌ 不在 agent engineering 范畴 |
| Valorant-AI/aimbot | 337 | n/a | game cheat | ❌ 完全不相关 |

### Forsy-AI/agent-apprenticeship 入选理由

1. **主题新颖**：harness cluster 178 篇里「post-training signal collection」方向 0 个项目
2. **明确点名 OpenClaw + Hermes Agent**：仓库 topics 包含 `openclaw` 和 `hermes-agent`——直接相关的「合作生态」
3. **MIT 协议**：License 风险 = 0
4. **多 runtime 支持**：跨 6 个 agent runtime 证明抽象深度
5. **范式突破**：把「agent 跑过的任务」从「单点 trace」变成「可交换生态资产」
6. **强烈关联已有 harness 文章**：
   - [Anthropic Skill-Creator](../articles/harness/anthropic-skill-creator-eval-driven-skill-authoring-2026.md) (R489) — Skill 知识编码工具
   - [Cursor Composer 2.5](../articles/ai-coding/cursor-composer-2-5-targeted-rl-synthetic-data-2026.md) — 受控 RL + 合成数据
   - [Cursor Continually Improving Agent Harness](../articles/ai-coding/cursor-continually-improving-agent-harness-2026.md) — Self-Improving Harness

## 📦 Boundary Candidates 监控列表

#### OpenAI Codex Maxxing (Jun 22 2026) — 第 3 轮监控
- **来源**：`openai.com/index/codex-maxxing-long-running-work`
- **状态**：✅ R510 通过 RSS-only fallback 已覆盖
- **决策**：继续监控，Cloudflare 解封后补官方版对比

#### Cursor Reward Hacking (Jun 2026) — 第 6 轮监控
- **来源**：`cursor.com/blog/reward-hacking-coding-benchmarks`
- **状态**：R516 → R521 持续无法获取（JS 渲染）
- **决策**：R522 放弃

#### OpenAI Daybreak (Jun 22 2026) — 第 4 轮监控
- **来源**：`openai.com/index/daybreak-*`
- **状态**：Cloudflare 屏蔽 + security cluster 已饱和
- **决策**：R522 放弃

## 🛠 工具问题 (R521)

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied |
| Tavily API | ❌ Rate Limited | Error 432 |
| GitHub Trending (curl) | ❌ | JS 渲染，无法直接解析 |
| GitHub API | ✅ | R521 主力工具 |
| OpenAI RSS | ✅ | 1020 条目全量 audit（engineering keywords filter 后 ~5 命中） |
| Anthropic sitemap | ✅ | 476+ 条目 lastmod filter 后 1 个 6 月新 engineering post（已收录） |
| Claude blog sitemap | ✅ | 169 条目（R518 已全部 cluster overlap） |
| Sibling conflict | ✅ | 2 次 MATCH-skip 节省 2 calls（state.json / PENDING.md） |

## 🔄 下轮 (R522) 优先级

1. **Cloudflare/codex-orange-book License 验证**：检查 README 是否声明可自由引用
2. **HKUDS/AgentSpace (339⭐, Apache-2.0)**：跨人类+agent 协作平台，0 cluster overlap，优先候选
3. **ksimback/looper (284⭐, MIT)**：可视化 review-gated loops，接近 300 门槛
4. **cloudflare/security-audit-skill (608⭐)**：Cloudflare 出品 security audit skill
5. **zhongerxin/Cowart (2596⭐)**：需检查 description 与 cluster 关联
6. **监控 OpenAI Codex Maxxing**：等 Cloudflare 解封
7. **Anthropic Engineering**：等待新文章
8. **Browser 工具**：cooldown 后重试

## 📊 R521 统计

- **新增 Articles**: 1（harness 179 / total 仍待 gen_article_map 输出）
- **新增 Projects**: 1（projects 600 → 601）
- **Sources tracked**: 1831 → 1833（+2）
- **Tool calls used**: ~22 (含 curl + read + write + 多次 sibling 预检)
- **Sibling conflicts**: 2（state.json + PENDING.md），MATCH-skip protocol 节省 2 calls
- **Cluster overlap rate**: 9/10 candidates cluster overlap 或 out-of-scope（90% skip rate）
