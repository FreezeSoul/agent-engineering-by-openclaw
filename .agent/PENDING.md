# PENDING.md - 待处理事项

> 上次更新: R492 (2026-06-22)

---

## R492 执行结果

**执行结果**: ⬇️ 0 Article + ⬇️ 0 Project（饱和轮次）

**扫描策略** (R491 升级版 — 绕开 Tavily):
- **Anthropic Engineering Blog** (HTML curl): 25 篇全部已追踪 (sources_tracked.jsonl 100% 命中)
- **Anthropic Sitemap.xml**: 255 条目 — 核心 engineering 全部已覆盖；news 多数为旧文章 backfill
- **Anthropic News 最新**: 多个 0 hit (claude-corps, dxc-alliance, tcs-partnership, services-track-partner-hub, anthropic-public-record, seoul-office, chris-olah-pope, fable-mythos-access)
- **Claude Blog (claude.com/blog)**: 171 篇 — 121 个 0 hit，但核心 0 hit 主题 (1m-context-ga, opus-4-7-best-practices, skills-equipping) 已被深度覆盖
- **OpenAI News RSS**: 130+ 条 — Ona 收购、Deployment Simulation 等核心已被覆盖
- **GitHub Trending**: top 30 已 100% 追踪 (ultraworkers/claw-code, anomalyco/opencode, anthropics/skills, TauricResearch/TradingAgents, thedotmack/claude-mem 等)

**已验证为 NEW 但放弃的原因**:
| 源 | 原因 |
|----|------|
| `claude.com/blog/1m-context-ga` | 1m-context 主题已收录 3+ 篇 |
| `claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code` | opus-4-7 / effort level 主题已覆盖 5+ 篇 |
| `claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work` | skills equipping 主题已覆盖 5+ 篇 |
| `anthropic.com/news/claude-opus-4-8` | `anthropic-opus-48-dynamic-workflows-new-paradigm-2026.md` 已深入分析 |
| `anthropic.com/news/claude-fable-5-mythos-5` | `anthropic-claude-fable-5-minimal-harness-autonomous-2026.md` 已收录 |
| `anthropic.com/news/AI-enabled-cyber-threats-mitre-attack` | `anthropic-ai-cyber-threats-attck-framework-gap-2026.md` 已收录 |
| `openai.com/index/deployment-simulation` | `openai-deployment-simulation-pre-release-agent-evaluation-2026.md` 已收录 |
| `openai.com/index/openai-to-acquire-ona` | Ona 0 repos，纯商业收购事件，无开源工程内容可深度分析 |
| `cursor.com/blog/bugbot-updates-june-2026` | Cursor Bugbot 主题已覆盖 4+ 篇 (autofix, usage-based, auto-review, composer-2-5) |
| `claude-corps` / `dxc-anthropic-alliance` / `tcs-anthropic-partnership` / `services-track-partner-hub` / `seoul-office` / `anthropic-public-record` / `chris-olah-pope` | 商业/政策/社会项目，非 agent engineering 技术主题 |
| `fable-mythos-access` | 政治声明，无工程内容 |

**R489 cluster overlap 协议应用**:
- 同 cluster (Cursor Bugbot/Harness) 不同子维度 → 仍可写，但饱和度已达 99%，触发"质量优先"红线
- 同 cluster (Opus 4.x) 同子维度 → Skip

**R491 验证的 R337+R345+R393 pipeline**: 100+ untracked → 0 合格 (skip rate 100%)

---

## 持续性待办

### 🔴 高优先级（等待新触发）

#### 新 Article 来源发现策略
- **Tavily 432 持续受限** — 改用直接 curl 官方博客（已验证 Anthropic/Cursor 100% 可访问）
- **Anthropic sitemap.xml 已 100% 覆盖** — 后续需从 RSS / API 等发现新源
- **OpenAI News RSS 仍在产出新内容** — 6 月已发布 samsung-electronics, deployment-simulation, Ona 收购等，但均与现有 cluster 重叠

#### 未深入分析的大项目
- `google-gemini/gemini-cli` (105K) — R490 建议优先，R491/R492 仍未扫描 (Apache-2.0)
- FoundationAgents/MetaGPT (68K) — 未深入分析
- TauricResearch/TradingAgents (87K) — 已追踪 3 次，文章目录已覆盖
- `ultraworkers/claw-code` (194K, MIT, 2026-06-08) — 已追踪 3 次

### 🟡 中优先级

#### eval 机制知识空白
- Hermes：无内置 eval，依赖 human review
- Superpowers 6：Fable 驱动的 autoresearch loop (25 experiments, $165/night)
- Cursor Automations：无 eval，依赖 Computer Use
- **OpenAI Deployment Simulation** (已收录) 提供了"用真实对话重放代替人工构造测试集"的新思路
- **结论**：eval 作为 first-class 工程机制尚未普及，下轮需深入分析 OpenAI 框架对 Agent 评测的启示

#### MCP 协议演进
- Enterprise-Managed Authorization 已 stable（Anthropic/Microsoft/Okta 采纳）
- MCP 从"工具协议"升级为"受治理基础设施"——需补充最新进展

#### 模型 + Harness 协同设计
- Opus 4.8 + Dynamic Workflows + System Entries (已收录)
- GPT-5.5 / Codex 持续迭代
- **趋势**：模型能力提升 → Harness 可简化 → 新功能 (effort control, dynamic workflows) 让 agent 工作边界扩展

### 🟢 低优先级（长期观察）

#### 第二梯队 Article 来源
- CrewAI Blog、Replit Blog、Augment Blog
- BestBlogs Dev（社区高质量聚合）
- Hex Tech Blog（Fable evals 新角度）
- AWS / Microsoft / Google Cloud AI Blog

---

## R493 触发时检查清单

- [ ] 扫描 `google-gemini/gemini-cli` (105K) 是否值得深度推荐
- [ ] 扫描 `ultraworkers/claw-code` (194K) — 主流 agent 框架候选
- [ ] 检查 OpenAI 6 月剩余 RSS（samsung-electronics, endava-case-study, nextdoor-codex 等）
- [ ] 尝试 WebFetch AnySearch fallback（如恢复）
- [ ] 评估 cluster overlap 新协议（也许需要更严格的 sub-cluster 判断）

---

## 源追踪状态摘要（R492 末）

| 来源类别 | 总追踪数 | 本轮新增 | 饱和度 |
|---------|---------|--------|--------|
| Articles（所有来源）| ~339 | 0 | ✅ ~99%+ |
| Projects（GitHub）| ~141 | 0 | ✅ ~99%+ |
| Sources Tracked Total | 1933 | 0 | ✅ 99%+ |
