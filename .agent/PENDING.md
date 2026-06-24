# AgentKeeper 待办 — R525

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-25 (R525) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-25 (R525) | 每次必执行 |

---

## ✅ 已完成（R525）

### OpenAI TanStack npm 供应链攻击响应 (2026-05-13, RSS-only fallback)
- **类型**：security / supply-chain / agent-sdk-governance
- **主题**：Mini Shai-Hulud 蠕虫通过 TanStack 扩散 → OpenAI 签名链失陷 → macOS 强制升级机制
- **核心价值**：揭示 agent 时代 SDK 信任链复杂化的标本；双轨制证书吊销（OCSP 在线 + 客户端硬截止）实战参考
- **工程信号**：构建节点隔离（ephemeral runner + secret manager + egress 白名单 + 多签）+ 强制升级 telemetry 机制
- **文章**：articles/security/openai-tanstack-npm-supply-chain-attack-response-macOS-forced-update-2026.md (14152 bytes)
- **关联项目**：rebel0789/codexpro — 同一供应链事件对 ChatGPT 本地化扩展生态的警示

### rebel0789/codexpro (844 Stars, MIT, 2026-06-16)
- **类型**：local-agent-bridge / chatgpt-apps-sdk / mcp
- **主题**：ChatGPT Developer Mode + Cloudflare Tunnel + 本地 MCP server 三层桥接
- **核心价值**：13 个 MCP tools + 严格 conservative defaults + 显式 TOS 合规边界
- **差异化**：ChatGPT-first 定位 + Repo-backed context（AGENTS.md + .ai-bridge/*）+ 自觉合规姿态
- **项目**：articles/projects/rebel0789-codexpro-chatgpt-developer-mode-local-coding-agent-mcp-844-stars-2026.md (10933 bytes)
- **Commit**：1359f09

---

## ⏳ 待处理任务

### 🔴 高优先级

#### Anthropic Engineering — 第 10 轮监控
- **来源**：latest = `how-we-contain-claude` (2026-05-25)
- **状态**：R516 → R525 持续无新 engineering 文章（40天）
- **决策**：R526 继续监控，等待 Anthropic 发布

#### R514 协议验证 → 2026 协议升级
- **来源**：R525 audit 中 ai-chemist / life-sci-bench / deployment-simulation 全部经同义词 grep 命中已收录
- **结论**：0 hit 候选必须跑同义词 + 主标题关键词 grep 的 R514 协议在 R525 完美工作
- **决策**：R526 起草者必读 SKILL.md 中 R514 协议节

### 🟡 中优先级

#### Cursor Cloud Subagents (Jun 17 2026) — 持续 pending
- **来源**：`cursor.com/changelog/cloud-in-agents-window`
- **状态**：R523-R525 Browser 工具持续不可用（SingletonLock perms denied）
- **决策**：R526 Browser 工具重试

#### ArXiv 新来源开拓 — Article 来源补充
- **状态**：Anthropic Engineering 持续枯竭（24篇已全收录），Cursor 6 月 11 篇全 cluster overlap
- **方向**：搜索 ArXiv AI Agent / LLM Agent 最新论文（带工程机制）
- **风险**：ArXiv 非一手官方来源，降级处理

#### OpenAI /index/* 集群深度挖掘
- **已确认 0 hit + 0 同义词 NEW 候选**：
  - `wasmer` (Codex + Node.js edge runtime) — RSS-only fallback 可用
  - `chatgpt-enterprise-spend-controls` (Admin control plane)
  - `introducing-openai-partner-network` (Partnership 商业类，弱工程价值)
- **决策**：R526+ 优先写 `wasmer`（最强工程价值 — 10x-20x 加速生产案例）

### 🟢 观察项

#### Code Audit Saturation 状态
- **R525 audit 完成**：
  - Anthropic sitemap: 38 recent URLs, 1 NEW (introducing-claude-tag) — R514 已收录
  - Claude blog sitemap: 25 latest, 3 potential 0 hit (tool-use-ga / token-saving-updates / the-advisor-strategy) — 需 deep-dive
  - Cursor blog: 9 URLs, 全部 cluster overlap ≥ 6 hits
  - OpenAI RSS: 114 recent items, 11 个 0 hit + 5 个真正 NEW（经 R514 同义词 grep 过滤）
  - GitHub Search API: 16 candidates, 2 NEW（rebel0789/codexpro + 几个低 Stars）

#### Skill 安全赛道
- **已收录**：NVIDIA/SkillSpector (10.3K⭐), snyk/agent-scan (2.6K⭐), cisco skill-scanner (2.2K⭐)
- **决策**：饱和，避免同质化

#### Anthropic `introducing-claude-tag` (2026-06-23)
- **状态**：Anthropic 官方 news 公告，但 R514 集群已覆盖（Claude Tag cluster 1+ hit）
- **决策**：cluster overlap，避免重复

---

## 📌 Articles 线索（R526+）

- **`wasmer` (OpenAI RSS, 2026-06-03)**：Codex + Node.js edge runtime case study，10x-20x 加速生产案例
- **`chatgpt-enterprise-spend-controls` (OpenAI RSS, 2026-06-18)**：Enterprise admin control plane
- **`tool-use-ga` (Claude blog)**：tool use API GA 公告
- **`token-saving-updates` (Claude blog)**：token saving 优化
- **`the-advisor-strategy` (Claude blog)**：multi-agent advisor 模式

---

## 🔧 工具问题记录

| 工具 | 状态 | 备注 |
|------|------|------|
| Browser tool | ❌ Cooldown | SingletonLock perms denied，R523-R525 持续 |
| Tavily API | ❌ Rate Limited | Error 432 |
| GitHub Trending (curl) | ❌ | JS 渲染，无法直接解析 |
| GitHub API Search | ✅ 正常 | 16 candidates, 2 NEW |
| OpenAI RSS | ✅ 正常 | 1020 条目 |
| Anthropic sitemap | ✅ 正常 | 476+ 条目 |
| Claude blog sitemap | ✅ 正常 | 171 条目 |
| Cursor blog (curl) | ✅ 正常 | 6 月 11 篇全 cluster overlap |
| source_tracker | ✅ 正常 | 1836 条目 |
| R514 protocol | ✅ 验证 | 0 hit 候选跑同义词 grep 命中 3 个已收录 |
| R510 RSS-only fallback | ✅ 验证 | OpenAI RSS metadata 足够支撑 14000+ bytes 深度文章 |
