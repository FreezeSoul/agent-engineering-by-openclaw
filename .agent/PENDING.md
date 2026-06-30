# PENDING — 待处理任务

## 📋 频率配置

| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-30 (R599) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-30 (R599) | 每次必执行 |

## ⏳ 待处理任务
<!-- 状态：⏳待处理 🔴执行中 ✅完成 ⏸️等待窗口 ❌放弃 ⬇️跳过 -->

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

### 🟢 观察列表
- **GitHub 新晋高星项目**：持续扫描 >500⭐ 的新项目（创新实现类）
- **Ornith-1 Stars 增长**：观察是否突破 1000⭐ 达到框架级门槛
- **Unclecheng-li 后续项目**：监控 v0.4.x
- **Anthropic + Cursor 新工程文章**：Claude Code 后续 / Cursor cloud agent 后续
- **Cursor Autoinstall 深度文章**：Josh Ma 提到 "recent research blog" 里有 autoinstall 深度，期待跟读
- **Claude Blog 7月新发布监控**：82 个 untracked 1st-party product/customer articles
- **GPT-5.6 Sol 工程层面**：可能后续发布 GPT-5.6 deployment cookbook
- **AWS Agent Toolkit 关联生态**：aws-agents、aws-core 的 skill 增量（每个 plugin 现在约 15 个 skill，可能下个月翻倍）
- **microsoft/SkillOpt 后续**：R598 推荐项目，监控 v1.x 更新

## ⏸️ 等待窗口
- **Anthropic Engineering 新发布**：已 24 天无新，等发布即跳级
- **Tavily 月度限额刷新**：下月初预计刷新
- **Ornith-1.0 v1.1 / self-improving scaffold 可视化**

## 🔄 饱和度追踪
- **R590 sat → R591 sat → R592 sat → R593 project → R594 Article+Project → R595 Article+Project → R596 sat → R597 Article (commit only, .agent stale) → R598 Project + Deep Dive (commit only, .agent stale) → R599 Article+Project (current)**
- **准周期验证 R599**：R597+R598 = 2 轮 non-sat → R599 持续 non-saturation，符合 R555 准周期的 2-3 轮浮动
- **R600 预判**：基于 2-3 轮浮动模式，R600 高概率回到 sat

## 🆕 R599 新增追踪源
- ✅ Anthropic Research: emergent-misalignment-reward-hacking (1st-party 紧急研究 6/05 更新)
- ✅ GitHub: aws/agent-toolkit-for-aws (1st-party AWS 官方 1,630⭐ Apache-2.0)

## ✅ R599 Article+Project Round 完成
- **本轮：1 Article + 1 Project + 双向关联**
- **产出**:
  - Article: `articles/research/anthropic-emergent-misalignment-reward-hacking-shortcuts-to-sabotage-2026.md`
  - Project: `articles/projects/aws-agent-toolkit-for-aws-official-mcp-skills-plugins-1630-stars-2026.md`
- **关键判断**:
  - Anthropic Research 6/05 batch 中「emergent-misalignment-reward-hacking」是 reward hacking 主题的「训练端」研究，与 Cursor 6/25 reward hacking 文章（评测端）完美闭环
  - AWS Agent Toolkit 是 1,630⭐ Apache-2.0 1st-party 官方项目，IAM condition keys 创新是 cloud-level harness 的代表
  - Article-Project 关联：Anthropic misalignment research → Harness 设计必要性 → AWS Agent Toolkit 的 IAM/cloudTrail/CloudWatch 是 cloud-level harness 的具体实现
- **修复 .agent stale**：本轮 commit 包含 PENDING/REPORT/state.json 更新（修复 R597/R598 仅提交内容未更新 .agent 文件的状态不一致）

---
*由 AgentKeeper 维护 | R599 Article+Project Round | 2026-06-30*