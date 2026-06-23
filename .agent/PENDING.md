## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-23 (R505) | 每次必执行（⚠️ Tavily 限额待刷新） |
| PROJECT_SCAN | 每轮 | 2026-06-23 (R505) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering 新文章（持续）
- 持续扫描 anthropic.com/engineering 有无新文章
- 当前全部已追踪
- 重点：harness design / long-running agents / evaluation / containment / agent-skills / desktop-extensions
- ⚠️ 需 agent-browser 辅助（JS 渲染问题）

#### OpenAI Agent 相关（持续）
- Daybreak / Codex-Security cluster 已饱和
- 关注：是否有"非 security/codex/long-running" cluster 的新发布

#### Cursor 持续跟踪
- Cursor 3.8+ 后续更新（/automate skill 生态演进）
- Cloud Subagents in VM 后续：babysit PR / 环境快照复用
- **Cursor 3.9+ Changelog** — 等待发布

### 🟡 中优先级

#### GitHub 新兴项目（持续扫描）
- **gadievron/raptor** (3041⭐, R505 新增) — 安全研究 Harness，已写
- **jamiepine/voicebox** (32K⭐) — 语音 AI studio，非 Agent Engineering 核心但 Stars 极高
- **cyrusagents/cyrus** (660⭐) — 多 IDE backend + 多项目管理 + per-issue worktree isolation
- **mindsdb/anton** (688⭐) — self-improving agent，与 NousResearch/hermes-agent cluster overlap

### 🟢 低优先级（观察）

- CrewAI Blog / Replit Blog / Augment Blog
- BestBlogs Dev / Hacker News
- AnySearch + Folo RSS（工具与发现补充）

---

## 源追踪状态摘要（R505）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles（所有来源）| ~349 | 0 | saturation |
| Projects（GitHub）| ~146 | 1 | gadievron/raptor |
| Sources Tracked Total | ~350 | 1 | |

---

## 技术状态

| 工具 | 状态 | 备注 |
|------|------|------|
| Tavily Search | ⛔ 432 限额 | 月度限额耗尽，需等待刷新 |
| GitHub API + SOCKS5 | ✅ 正常 | 主要发现工具 |
| AnySearch | ✅ 正常 | 补充发现 |
| Anthropic Engineering | ⚠️ JS 渲染 | 需 agent-browser |

---

## 工具预算说明

R505 使用约 12 calls，远低于 21 calls 硬截止线。
