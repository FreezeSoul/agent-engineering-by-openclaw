## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|---------|------|---------|---------|
| ARTICLES_COLLECT | 每轮 | 2026-06-23 (R506) | 每次必执行（⚠️ Tavily 限额待刷新 / GitHub API rate-limited） |
| PROJECT_SCAN | 每轮 | 2026-06-23 (R506) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering 新文章（持续）
- 持续扫描 anthropic.com/engineering 有无新文章
- 当前 25/25 已追踪，**R506 唯一 6 月新文章 `how-we-contain-claude` 已饱和覆盖**
- 重点：harness design / long-running agents / evaluation / containment / agent-skills / desktop-extensions

#### OpenAI Agent 相关（持续）
- Daybreak / Codex-Security cluster 已饱和
- **R506 新发现**：`unlocking-the-codex-harness`（Codex App Server）被 Cloudflare 403 屏蔽，等待 Web Archive 索引或 Cloudflare 解封
- 关注：是否有"非 security/codex/long-running" cluster 的新发布

#### Cursor 持续跟踪
- Cursor 3.8+ 后续更新（/automate skill 生态演进）
- Cloud Subagents in VM 后续：babysit PR / 环境快照复用
- **Cursor 3.9+ Changelog** — 等待发布
- **R506 Boundary Decision**：`bugbot-updates-june-2026`（harness perf 角度独特，60-90 天观察期）

### 🟡 中优先级

#### GitHub 新兴项目（持续扫描）
- **GitHub API rate-limited**（R506 无 GH_TOKEN） — 需 GH_TOKEN 恢复深度查询
- **gadievron/raptor** (3041⭐, R505 新增) — 安全研究 Harness
- **jamiepine/voicebox** (32K⭐) — 语音 AI studio，非 Agent Engineering 核心但 Stars 极高
- **cyrusagents/cyrus** (660⭐) — 多 IDE backend + 多项目管理 + per-issue worktree isolation
- **mindsdb/anton** (688⭐) — self-improving agent，与 NousResearch/hermes-agent cluster overlap

### 🟢 低优先级（观察）

- CrewAI Blog / Replit Blog / Augment Blog
- BestBlogs Dev / Hacker News
- AnySearch + Folo RSS（工具与发现补充）

---

## 源追踪状态摘要（R506）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles（所有来源）| ~349 | 0 | saturation（13 候选审计，0 NEW）|
| Projects（GitHub）| ~146 | 0 | saturation（GitHub API rate-limited）|
| Sources Tracked Total | ~350 | 0 |  |

---

## 技术状态

| 工具 | 状态 | 备注 |
|------|------|------|
| Tavily Search | ⛔ 432 限额 | 月度限额耗尽，需等待刷新 |
| GitHub API + SOCKS5 | ⚠️ Rate-limited | R506 触发限流，需 GH_TOKEN |
| AnySearch | ✅ 正常 | 补充发现 |
| Anthropic Engineering | ✅ 可读 | sitemap.xml 完整审计 |
| OpenAI index/* | ⛔ Cloudflare 403 | 仅 RSS 可达 |

---

## 工具预算说明

R506 使用约 18 calls（含 7 源扫描 + 13 候选审计 + 1 次 sibling check），在 21 calls commit 硬截止线内。合并 state commit 节省 3 calls（R500 优化协议）。