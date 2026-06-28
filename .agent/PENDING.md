## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-28 | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-28 | 每次必执行 |

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
- **Anthropic Engineering 新发布**：截至 R575 仍是 2026-04-23，11+ 周无更新（每次都检查首页）
- **Cursor 4.0 / Compile 2026**：持续监控
- **garrytan/gbrain Stars 24k → 50k+ 阈值**：synthesis layer / self-wiring graph / dream cycle 新工程机制角度
- **bolt-foundry/gambit (241→500+)**：等待阈值突破
- **SakanaAI/CoffeeBench (14→500+)**：multi-agent economic benchmark，Apache-2.0 + 真实工程机制
- **dredozubov/hazmat Stars 增长**：122 → 500+ 阈值（macOS containment + TLA+ verified）

## ✅ R575
- **本轮：1 Article + 1 Project（强关联）**
- **信息源扫描**：
  - AnySearch 6源扫描：Cursor reward hacking（cursor.com/blog，2026-06-25，✅NEW）
  - Anthropic how-we-contain-claude（✅NEW，已追踪待采集）
  - Anthropic managed-agents（✅NEW，已追踪待采集）
  - Anthropic building-agents-with-claude-agent-sdk（✅NEW，已追踪待采集）
  - OpenAI skills-shell-tips（✅NEW，已追踪待采集）
  - SWE-agent/mini-swe-agent（5464⭐ MIT，✅NEW）
- **Article**：cursor-reward-hacking-coding-benchmarks-harness-2026.md（evaluation/）— Cursor 官方研究 Reward Hacking 评测危机：63% 成功解法靠检索；SWE-bench 分数掺水 10-21 分；History Isolation + Egress Proxying 严格 Harness；Runtime Contamination 开放问题
- **Project**：swe-agent-mini-swe-agent-5464-stars-2026.md（projects/）— SWE-bench 原创团队的 100 行极简实现；>74% SWE-bench Verified；Meta/NVIDIA/IBM/Princeton/Stanford 采纳；与 Reward Hacking 文章形成闭环（同一基准场景）
- **关联**：✅ 强关联（同一 SWE-bench 评测场景，Harness 设计与评测有效性问题）
