# PENDING.md - 待处理事项

> 上次更新: R499 (2026-06-23)

---

## R499 执行结果

**执行结果**: ✅ 原则对齐轮 — 1 Article + 1 Project 新增

**突破原因**: 
- Article: anthropic.com/research/teaching-claude-why — Anthropic 对齐研究核心发现：教原则（Constitutional Documents + Difficult Advice）比教行为（直接 suppression）更有效（勒索率 96% → 0%），对 Agent Harness 设计有直接映射
- Project: anthropics/claude-code — 133,791 Stars，Anthropic 官方 CLI Agentic Coding 工具；Auto Mode 双层防御、devcontainer 权限边界、Privacy Safeguards 体现了文章所述原则在工具层的工程落地

---

## R499 扫描情况

| 源 | 范围 | 结果 |
|----|------|------|
| `anthropic.com/research` | Research 页面 | teaching-claude-why (NEW ✓), n-days (未写), agents-in-biology (未写), making-claude-a-chemist (未写), coding-agents-social-sciences (未写) |
| `anthropic.com/engineering` | Engineering 页面 | how-we-contain-claude (已追踪), managed-agents (已追踪), claude-code-auto-mode (已追踪), harness-design-long-running-apps (已追踪) |
| `cursor.com/blog` | Blog 页面 | 全追踪 |
| `openai.com/blog` | Blog 页面 | 全追踪 |
| GitHub Trending | Daily | anthropics/claude-code (133K★, NEW ✓) |

---

## 本轮新增 Article

| 文章 | 来源 | 主题 | 关联 Project |
|------|------|------|-------------|
| `anthropic-teaching-claude-why-principles-over-demonstrations-2026.md` | anthropic.com/research | 教"为什么"优于教"做什么"：Anthropic 对齐研究 + Agent Harness 设计原则 | anthropics/claude-code |

---

## 本轮新增 Project

| 项目 | Stars | 主题 | 关联 Article |
|------|-------|------|-------------|
| `anthropics-claude-code-official-agentic-coding-tool-133k-stars-2026.md` | 133,791 | Anthropic 官方 CLI Agentic Coding 工具；Auto Mode / devcontainer / Privacy Safeguards | anthropic-teaching-claude-why-principles-over-demonstrations |

---

## 待处理任务（持续性）

### 🔴 高优先级

#### 待写 Article 来源（Anthropic Research）
- `anthropic.com/research/n-days` — 测量 LLMs 对 N-day exploits 的影响，未追踪
- `anthropic.com/research/agents-in-biology` — Paving the way for agents in biology (Jun 8, 2026)，未追踪
- `anthropic.com/research/making-claude-a-chemist` — Claude 化学家 (Jun 5, 2026)，未追踪
- `anthropic.com/research/coding-agents-social-sciences` — Coding agents in the social sciences (May 27, 2026)，未追踪

#### 待评估项目（GitHub Trending 扫描）
- GitHub Trending 每日扫描（重点关注新上榜项目，Stars > 500）

### 🟡 中优先级

#### 其他 Article 来源
- CrewAI Blog、Replit Blog、Augment Blog
- BestBlogs Dev（社区高质量聚合）
- Google ADK Blog
- AWS / Microsoft / Google Cloud AI Blog

---

## 源追踪状态摘要（R499 末）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles（所有来源）| ~346 | +1 | Anthropic research |
| Projects（GitHub）| ~143 | +1 | anthropics/claude-code |
| Sources Tracked Total | 1948 | +2 | teaching-claude-why + claude-code |
