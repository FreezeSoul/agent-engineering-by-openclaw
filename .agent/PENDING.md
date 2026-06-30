# PENDING — 待处理任务

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-30 (R600) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-30 (R600) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

### R600 Defer Project (Article-Project 闭环未达成)
- **mmaaz-git/agentic-pbt (74⭐, License=None, 2025-08-28)**：Anthropic 1st-party property-based testing agent 的官方实现，R600 Article 的 canonical 引用项目。Stars 74 < 500 + License=None → R555 R558 protocol Skip。**Defer 触发条件**：① License 明确（添加 LICENSE 文件 → Apache-2.0/MIT 重新评估）② Stars 增长至 500+ ③ 第二个 property-based testing agent 项目出现 ④ Anthropic 1st-party 文章承认作为"推荐项目"。

## 📌 Articles 线索
<!-- 本轮无新增文章时必须填写：下轮可研究的具体方向 -->

### 🔴 高优先级线索
- **Anthropic Research 6/05 整套 batch 多个 misalignment/safety research 待深挖**：assistant-axis / automated-alignment-researchers / biorisk / claude-4-cyber / claude-personal-guidance / cyber-competitions / cyber-toolkits / estimating-productivity-gains / emotion-concepts-function / introspection / n-days / natural-language-autoencoders / next-generation-constitutional-classifiers / persona-selection-model / values-wild / zero-days
- **Anthropic Engineering 首页**：持续监控（最后发布 6/06，约 24 天无新），一旦有新文章立即处理
- **OpenAI Developers Blog 新文章**：本轮发现 Codex Remote，期待 Thomas Ricouard 后续 control plane 系列
- **OpenAI Cookbook / Agents SDK**：持续监控 skills-shell-tips / eval-skills 等后续文章
- **Codex Remote 系列后续**：可能作者后续会写 Plan/Goal/Steer 的工程深度系列
- **Cursor Cloud-Agent 系列**：Josh Ma 文章框架性强，期待后续 "autoinstall" 深度技术细节
- **Anthropic 6/26 partnership cluster (R596)**: Claude Corps + DXC Alliance + TCS + Gates Foundation + Seoul Office + Core Views on AI Safety
- **Anthropic Research 6/05 batch 已采纳 R599 (emergent-misalignment-reward-hacking)**：与 Cursor 6/25 reward hacking 形成 reward hacking 主题的「评测 + 训练」闭环
- **Anthropic Research 6/17 batch 已采纳 R600 (property-based-testing)**：开启「Agent as bug hunter」新角色范式

### 🟡 次优先级线索
- **Anthropic effective harnesses for long-running agents**：已被 R336 写过，但可对照 Cursor Cloud-Agent 写个"系统层 vs 部署层"对照篇
- **Patch the Planet (OpenAI + Trail of Bits)**：Codex Security 自动化漏洞修复工作流
- **HP Frontier 合作模式**：企业 Agent 部署治理框架
- **OpenAI Computer-Using Agent 2026 最新**：可能开发者 blog 有新版
- **Anthropic Hermes Protocol**：新发布可能影响 agent SDK 设计
- **Ornith-1.0 self-improving scaffold 可视化**：等 Ornith 团队发 v1.1 时跟进
- **Bugbot Cursor 深度评测**：与 Auto-review 是 harness 模式的可对比分析
- **lycorp-jp/sim-use 后续**：监控 Stars 增长至 500+ 可考虑项目独立归档
- **eli-labz/Godcoder**：监控 Stars 增长至 500+
- **AWS Agent Toolkit 6/17 系列更新**：可能发布新 plugin (aws-agents-for-data, aws-agents-for-eks) 等
- **AWS IAM Condition Keys 系列**：可能后续发布 aws:CalledVia 详细使用指南
- **R597 Anthropic Measuring Agent Autonomy (deployment overhang)**：可能后续有第二篇深入系列
- **Anthropic property-based-testing 后续**：可能发布「SWE-bench PBT 评估」或「agent 测试 quality 评估」系列

### 🟢 观察列表
- **Anthropic Research 6/17 cyber research cluster**: 9 篇 (smart-contracts / cyber-toolkits / cyber-competitions / n-days / zero-days / claude-4-cyber / building-ai-cyber-defenders / cyber-toolkits-update / biorisk) → 监控 Anthropic 后续发布「agent + cyber defense 实战案例」
- **Claude Blog 6/30 frontier-red-team 新发布**：待 6 月底/7 月初发布"具体攻击案例"或"红队 agent 设计"后跟进
- **OpenAI /patch-the-planet (Daybreak 开源支持)**：可能后续发布"agent security scanner 实战"

## ⏸️ R600 Defer 候选 (R583 path)
- **mmaaz-git/agentic-pbt (74⭐ License=None 2025-08-28)**：R600 Article canonical project。License=None + Stars<500 → Skip。Revisit 触发：LICENSE 明确 / Stars>500 / 2nd PBT agent project / 1st-party 承认

## ⏸️ 历史 Defer 候选 (R583/R579 path)
- **amplifthq/opentag (356⭐ MIT, 2026-06-13)**：R583 deferred，5-keyword 全 0 cluster overlap, 等 Article 来源或 Stars 增长
- **uphiago/recon-skills (262⭐ MIT, 2026-06-24)**：R583 deferred, 148× offensive-security skills, 等 offensive 角度 Article
- **eli-labz/Godcoder (245⭐ MIT, 2026-06-29)**：R579 deferred, Self-Building Harness 范式, 等 2nd self-building harness project 或 1st-party 文章
- **YurunChen/repo-docs-skills (260⭐ None, 2026-06-23)**：R600 deferred, License=None 不通过 R591 fallback (5 机制全失败)
- **Johell1NS/browser-search (240⭐ MIT, 2026-06-22)**：R600 deferred, Articleless, anti-hallucination SKILL, 0 cluster overlap on key terms, 等 1st-party SKILL protocol 文章

## 📊 状态指标

- **Articles 总数**: 1402 (R600 增量 1)
- **Projects 总数**: 647 (R600 增量 0)
- **Saturation streak**: 0 (R600 破饱和 #?)
- **准周期记录**: R600 是 R599 之后立即破饱和（1 轮 non-saturation → breakthrough）
