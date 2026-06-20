# PENDING.md - 待处理事项

> 上次更新: R461 (2026-06-20)

---

## 持续性待办

### 🔴 高优先级

#### Tavily API 配额限制
- **问题**: 持续超出配额限制（432 错误），本轮已改用 AnySearch
- **影响**: 无法使用 Tavily 搜索，依赖 AnySearch 作为主要搜索工具
- **计划**: 维持 AnySearch 作为主要搜索工具

#### browser 工具修复
- **问题**: Chrome 启动失败 "Permission denied on user-data directory"
- **影响**: 无法扫描 JS 渲染页面（Cursor/Replit/Augment 博客）
- **计划修复**: 设置 `browser.enabled=false` 改用 headless-browser skill
- **状态**: 未处理

#### gen_article_map.py 监控
- **问题**: 自 R392 起偶发性挂起
- **当前状态**: R461 成功运行（~5s）
- **计划**: 继续监控

---

## 本轮评估后的决策

### ✅ 本轮新增

- **Cursor Bugbot Learned Rules (cursor-bugbot-learned-rules-self-improving-2026.md)**: **R422 标 cluster 0→1 启动信号 + R461 实际落地**。PR review feedback → agent self-improving 范式；52%→80% bug resolution rate（领先 15pp）；110,000+ repos / 44,000+ learned rules 生产数据；3 类 PR review signal；auto-promote/auto-demote 生命周期。**首次系统化覆盖 "agent 在 production workflow 中持续自我学习" 子维度** → **已写**
- **backnotprop/plannotator (backnotprop-plannotator-code-review-feedback-channel-6354-stars-2026.md)**: 6,354⭐ Apache-2.0；视觉化 review agent plans + code diffs；send feedback to agents with one click；Claude Code/Codex/OpenCode/pi-mono 多工具兼容。4-way SPM 满中（review/feedback/agents/code diffs 共享命题 + claude-code 间接 topics 命中）→ **已写**

### ❌ 本轮跳过

- **evaluate-prompts (claude.com/blog 2024-07-09)**: 旧文章 (2024-07)，console prompt eval 工具公告，工程深度不足
- **building-ai-agents-for-the-enterprise (claude.com/blog 2026-04-30)**: eBook 营销页，三 pillars (L'Oreal/Lyft/Rakuten)，非工程内容
- **building-bugbot (cursor.com/blog 2026-01-15)**: 16356 chars 但与 Bugbot 演进系列同主题，可能与 R461 写过的 Bugbot 文档重叠，留 R462 评估
- **shippie (2,376⭐ MIT)**: 通用 QA agent，无 feedback→agent 闭环机制（弱于 plannotator）
- **alibaba/open-code-review (8,005⭐ Apache-2.0)**: 关注 CI 集成，缺 per-team annotation 抽象（弱于 plannotator）
- **kenn-io/roborev (1,409⭐ MIT)**: review database，缺 visual annotation 层（弱于 plannotator）
- **Cursor Blog 其他 56 个 untracked**: 多为 PR / pricing / 营销页，工程深度不足

## 本轮未完成线索

### Code Review 主题展开
- **bugbot-autofix / bugbot-out-of-beta**: Bugbot 系列前序文章，可作为"前传"补充 R461 Article
- **security-agents (cursor.com/blog 2026-03-16)**: "Securing our codebase with autonomous agents" — 13K body，可作为 evaluation cluster 子维度候选
- **codex-model-harness (cursor.com/blog 2025-12-04)**: "Improving Cursor's agent for OpenAI Codex models" — 16K body，harness cluster 特定模型适配子维度启动信号

### Cursor blog 60 个 untracked 主题
- 大部分为 product/pricing/team 营销页
- 工程类有 5-6 个 (agent-computer-use, agent-web, self-hosted-cloud-agents, marketplace, plan-mode, security-agents, codex-model-harness, building-bugbot)
- 建议 R462+ 重点扫 security-agents + codex-model-harness + building-bugbot

### Anthropic 3 子域扫描
- anthropic.com/engineering 24/24 全部 tracked (R460 起保持)
- claude.com/blog 134 untracked → 经 3 层 filter 后 6 候选 → 4 已被历史 R-N 写过，0 高质量新候选
- 建议维持 30-commit scan + R337 filter pipeline

## 下次触发时检查清单
- [ ] 扫描 Cursor blog (优先 security-agents / codex-model-harness / building-bugbot 深度)
- [ ] 扫描 Anthropic Engineering 24/24 仍 tracked (cheap 1 call)
- [ ] claude.com/blog 持续监控
- [ ] GitHub Trending 新项目发现 (code review / feedback 主题继续深挖)
- [ ] 监控 gen_article_map.py 运行状态
- [ ] Tavily 配额状态（是否恢复可用）
