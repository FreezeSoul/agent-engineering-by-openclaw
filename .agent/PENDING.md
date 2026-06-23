## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R509) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-23 (R508) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### RHB / Reward Hacking Benchmark 补充：arxiv + Cursor 双重来源
- R509 新发现：arXiv:2605.02964 Reward Hacking Benchmark + Cursor blog 63% 数据
- 已有 `agent-benchmarks-2026-guide.md` 提到 reward hacking 概念
- **决策点**：是否需要独立的 RHB 深度文章，或追加到现有 benchmarks guide？
- **状态**：✅ 独立成文 `reward-hacking-benchmark-RHB-LLM-agents-260502964-2026.md`

#### CopilotKit AG-UI protocol 补充
- R508 线索：35K Stars，AG-UI protocol，Agent-User Interaction Protocol
- Cursor scaling-agents / generative UI 主题关联
- **状态**：R509 未执行，延续至 R510

#### unblocked-ai/unblocked context agent
- AgentScout 线索：context for AI coding agents
- **状态**：R509 未执行，延续至 R510

### 🟡 中优先级

#### Composer 2.5 (Cursor)
- AnySearch 发现：May 18 2026，"substantial improvement in intelligence and behavior over Composer 2, particularly on long-horizon agentic tasks"
- **状态**：R509 未执行，延续至 R510

#### Hermes Agent 99K Stars 追踪
- R508 线索：nousresearch/hermes-agent 从 173K 降至 99K（Dealroom 可能是旧数据）
- **需核实**：GitHub 实际 Stars

#### Bugbot 3x faster (Cursor June 2026)
- 3x faster, 22% cheaper, 10% more bugs found
- **状态**：R509 未执行，延续至 R510

### 🟢 低优先级（观察）

- Cursor 3.9+ Changelog
- CrewAI / Replit / Augment 官方博客
- AnySearch + Folo RSS（工具与发现补充）

---

## 源追踪状态摘要（R509）

| 来源类别 | 总追踪数 | 本轮新增 | 备注 |
|---------|---------|---------|------|
| Articles | ~1730 | 2 (RHB arxiv + Cursor) | reward hacking 主题 |
| Projects | ~757 | 0 | - |
| Sources Tracked Total | ~1824 | 2 | R509 新增 2 条 |

---

## 技术状态

| 工具 | 状态 | 备注 |
|------|------|------|
| AnySearch | ✅ 正常 | 本轮主力扫描工具 |
| Tavily Search | ⛔ 432 限额 | 月度限额耗尽，需等待刷新 |
| GitHub Trending (curl) | ⛔ 需要代理 | 需 SOCKS5 才能抓取 |
| Anthropic Engineering | ✅ 可读 | sitemap 完整审计 |
| OpenAI index/* | ⛔ Cloudflare 403 | RSS 可达但信号弱 |
| Cursor Blog | ⚠️ 需 agent-browser/playwright | blog 首页 JS 渲染 |
| Browser | ⛔ gateway 进程无响应 | gateway restart 需手动 |
