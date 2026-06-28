## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-29 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-29 | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->
- **Anthropic "how-we-contain-claude" (已追踪待采集)**：containment 三层防御体系（environment/model/external content），blast radius cap 框架，claude.ai + Claude Code + Cowork 三产品 containment architecture — 三层解耦值得深度文章
- **Anthropic "managed-agents" (已追踪待采集)**：brain/hands/session 接口解耦，harness as cattle，credential bundling/vault 模式，recover from harness failure — 多 Agent 生产级架构参考
- **Anthropic "building-agents-with-the-claude-agent-sdk" (已追踪待采集)**：working state + checkpoint + resume 工程机制详述，Claude Agent SDK walkthrough
- **OpenAI "skills-shell-tips" (已追踪待采集)**：Compaction（上下文压缩）+ Skills（技能系统）+ Shell 长期任务三件套，Agent SKill System 对齐
- **Cursor reward hacking 续篇**：SWE-bench 官方是否回应；其他团队（Harvard/GAIA）是否有类似发现
- **Claude Code W27**：预期 6/29-7/3，关注新 engineering mechanism 特性
- **Ponytail (62k⭐ → 68k+?)**：懒人老手模式 skill，AI Coding 场景代码量/成本优化，6/12 后持续增长

## ⏸️ 等待窗口
- **Anthropic Engineering 新发布**：截至 R576 仍是 2026-06-26 (partnership cluster)，11+ 周无新 engineering 文章（每次都检查首页 + sitemap）
- **Cursor 4.0 / Compile 2026**：持续监控
- **garrytan/gbrain Stars 24k → 50k+ 阈值**：synthesis layer / self-wiring graph / dream cycle 新工程机制角度
- **bolt-foundry/gambit (241→500+)**：等待阈值突破
- **SakanaAI/CoffeeBench (14→500+)**：multi-agent economic benchmark，Apache-2.0 + 真实工程机制
- **dredozubov/hazmat Stars 增长**：122 → 500+ 阈值（macOS containment + TLA+ verified）
- **HKUDS/AgentSpace (339→512⭐)**：已收录，Stars +51% growth，等待 1000+ 阈值再扩写

## ✅ R576 (Saturation round)
- **本轮：0 Article + 0 Project（100% skip rate）**
- **7 源 Tri-Scan 审计表**：
  | Source | Total | New (untracked) | Engineering Mechanism | Writable |
  |--------|-------|-----------------|----------------------|----------|
  | Anthropic sitemap | 256 | 0 (6/27-6/29 无新发布) | 0 | 0 |
  | Claude Blog | 172 | 124 | 0 (massive cluster overlap 60-1537 hits) | 0 |
  | OpenAI RSS top 20 | 20 | 15 | 5 → all Wrong Subject / 1st-party / cluster overlap | 0 |
  | Cursor Blog | 19 | 2 | 2 → both already cluster overlap (R506/R559) | 0 |
  | Sakana blog | - | 0 (SPA JS rendered, no scrape) | 0 | 0 |
  | GitHub Search | 10 | 4 | 0 (already tracked / Wrong Subject Domain) | 0 |
  | HN Algolia | - | 0 (R573 确认时间窗口偏旧) | 0 | - |
  | **总计** | **~510** | **145** | **7 candidates** | **0** |
- **0-hit 候选分类（7 类分类协议）**：
  - **Wrong Subject Domain (models)**：`previewing-gpt-5-6-sol` (R552 已 Skip)、`openai-broadcom-jalapeno-inference-chip` (硬件/芯片)
  - **Wrong Subject Domain (consumer)**：`chatgpt-enterprise-spend-controls` (1st-party product)、`helping-build-shared-standards-for-advanced-ai` (policy)、`introducing-openai-partner-network` (business)、`omio/preply/bbva/samsung` (customer stories)
  - **Cluster Overlap (1st-party)**：Anthropic 6/26 全部 partnership/cluster overlap、R576 Cursor Blog `notion` (R559/R560 covered)、`bugbot-updates-june-2026` (R506 covered)
  - **Cluster Overlap (general)**：所有 Claude Blog untracked engineering candidates (171-1537 hits overlap)
  - **Already Tracked**：`HKUDS/AgentSpace` (已收录 339⭐ → 512⭐ growth)、`QwenLM/Qwen-AgentWorld` (R545)、`OpenFugu` (R548)、`benchflow-ai/awesome-evals` (已收录)、`hermes-browser-extension` (cluster overlap)
  - **Wrong Subject Domain (other)**：`amplifthq/opentag` (Slack/GitHub mention routing)、`eli-labz/Godcoder` (NOASSERTION + 245⭐ < 阈值)
- **R555 准周期验证**：R573 saturation → R576 saturation = 3 轮连续 saturation ✅（与 R570-R572 → R573 同模式：3 轮 fuel 不足 → 触发 saturation）。完整周期 1-3 轮浮动规律不变，R577+ 继续完整 Tri-Scan。
- **协议贡献**：
  - **Sakana blog SPA JS-rendered pitfall**：R573 协议假设 8-label 可遍历，但实际 label pages 返回 same 85321 bytes（无 `/blog/<slug>/` hrefs）。R577+ 起草者可考虑用 Google Site Search 或直接搜 "sakana.ai/blog/2026" 替代。
  - **Anthropic 6/27-6/29 无新发布确认**：Anthropic sitemap lastmod 验证，6/26 后无新 URL，验证 R573 观察的 partnership cluster 6/26 一次性发布。

## ✅ R575 (上轮，已 commit)
- **本轮：1 Article + 1 Project（强关联）**
- **Article**：cursor-reward-hacking-coding-benchmarks-harness-2026.md（evaluation/）— Cursor 官方研究 Reward Hacking 评测危机：63% 成功解法靠检索；SWE-bench 分数掺水 10-21 分；History Isolation + Egress Proxying 严格 Harness
- **Project**：swe-agent-mini-swe-agent-5464-stars-2026.md（projects/）— SWE-bench 原创团队的 100 行极简实现；>74% SWE-bench Verified；与 Reward Hacking 文章形成闭环