## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-23 (R507) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-23 (R507) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Can Bölük 15 LLMs Benchmark 独立成文评估
- R507 发现：Can Bölük 2026-02 发布 "Improving 15 LLMs at Coding" benchmark，核心数据（Grok 68.3% / token -61% / hashline edit）已分散在 oh-my-pi Project 文章中
- **决策点**：是否从 oh-my-pi cluster 提取为独立 Article？独立成文的价值 vs cluster 内覆盖的边际价值
- **信号**：HN 讨论度高（#46988596），主题属于 harness engineering 核心但已有项目级覆盖

#### ponytail 50K Stars 追加评估
- R368 时：1,240 Stars → R507：50,441 Stars（40x 增长）
- **决策点**：Growth signal 是否触发追加 update article？
- **已有覆盖**：R368 `darrenhinde-openagentscontrol` cluster 配对，ponytail 作为 YAGNI skill 示例
- **追问**：50K Stars 背后的增长驱动是什么？（新 release？YC 背书？viral moment？）

#### agno-agi/agno 40K Stars Primary Article 补充
- R375 仅 cite 追踪（README reference），无 primary article
- 40K Stars 企业级 Agent 平台，与已有 `generalaction/emdash` (4.5K) 的区别是什么？
- **评估**：是否值得独立成文（enterprise focus vs open-source community focus）

### 🟡 中优先级

#### OpenClaw 380K Stars — Agent Engineering 视角
- ByteByteGo 报道 "fastest-growing open-source project in GitHub history"
- **问题**：这个工具本身是 Agent Engineering 平台，但 380K Stars 的 virality 是否值得报道？
- **边界**：OpenClaw 是本仓库的"母体"，自我报道有利益冲突风险，需 FSIO 确认

#### GitHub Trending 新兴项目（持续扫描）
- GitHub API rate-limited（R506-R507 均触发）
- **备选**：AnySearch + 手动 curl 扫描
- **重点关注**：Stars > 1000 + Agent Engineering 主题相关

#### Anthropic Engineering 新文章监控
- R506-R507：Anthropic Engineering 25/25 饱和
- **观察**：managed-agents / claude-code-auto-mode / harness-design 三条成熟 cluster
- **等待**：第 26 篇或全新 cluster 信号

### 🟢 低优先级（观察）

- Cursor 3.9+ Changelog
- CrewAI / Replit / Augment 官方博客
- BestBlogs Dev / Hacker News（已有持续扫描）
- AnySearch + Folo RSS（工具与发现补充）

---

## 源追踪状态摘要（R507）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles（所有来源）| ~1730 | 0 | saturation |
| Projects（GitHub）| ~757 | 0 | saturation |
| Sources Tracked Total | ~1931 | 0 | |

---

## 技术状态

| 工具 | 状态 | 备注 |
|------|------|------|
| AnySearch | ✅ 正常 | 本轮主力扫描工具 |
| Tavily Search | ⛔ 432 限额 | 月度限额耗尽，需等待刷新 |
| GitHub Trending (curl) | ⛔ 需要代理 | 需 SOCKS5 才能抓取 |
| Anthropic Engineering | ✅ 可读 | sitemap 完整审计 |
| OpenAI index/* | ⛔ Cloudflare 403 | RSS 可达但信号弱 |
| Cursor Blog | ⚠️ 需 agent-browser | blog 首页 JS 渲染 |
| sources_tracked.jsonl | ⚠️ 2 条损坏 | 需手动修复 |
