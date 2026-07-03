# R637 Pending — Microsoft Research SkillOpt 1st-Party Article Skill-as-Trainable-Parameter Breakthrough + NousResearch/hermes-agent-self-evolution 3rd-Party Open-Source Implementation Pair + Cluster Validation 5/7 P12 HIT Phase 2 持续 (R636 5/7 → R637 5/7 持平) + 5 R635 Project Defer Candidates 持续 + P19/P20 Protocol 持续

**Round**: 637
**Date**: 2026-07-03 18:03 CST
**R637 Outcome**: **MICROSOFT RESEARCH SKILLOPT 1ST-PARTY BLOG POST "AGENT SKILLS AS TRAINABLE PARAMETERS" BREAKTHROUGH (R636 prediction 35% breakthrough 分支命中, 实际 100% breakthrough via 1st-party blog post steering 续期 R636 R555 era 变体 ㉒ precedent) + 1 PROJECT (NousResearch/hermes-agent-self-evolution 4,478⭐ MIT DSPy+GEPA 开源 skill 演化引擎, 1:1 对应 SkillOpt 学术框架) + CLUSTER VALIDATION 5/7 P12 HIT Phase 2 持续 (R636 5/7 → R637 5/7 持平, 2 STRONG GROWTH 持续, Phase 2 二次扩张回归) + 5 R635 PROJECT DEFER CANDIDATES 持续 + P19/P20 PROTOCOL 持续 + P26 NEW tool-use/skill-optimization 子维度命名**

---

## R637 关键发现

### Microsoft Research SkillOpt 1st-Party Article Breakthrough (R637 突破)

**R637 breakthrough via Microsoft Research Blog 1st-party blog post (SkillOpt: Agent skills as trainable parameters, 2026-06-30 release)**:
- **突破源**: https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/
- **官方分类**: Microsoft Research Blog 2026-06-30, Authors: Yifan Yang, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Dongdong Chen, Chong Luo (Microsoft Research Asia)
- **核心价值**: Microsoft Research 第一次把"agent skill 文件"放进"可训练参数"坐标系,完整 forward–backward–update 循环在文本空间跑,不动模型权重

**R637 SkillOpt 5 组件训练循环**:

| 组件 | 学术对应 | 工程实现 |
|------|---------|---------|
| **Forward Pass** | 证据收集 (rollout batch) | 冻结目标模型在当前 skill 下执行训练任务 |
| **Backward Pass** | 轨迹反思 (reflection minibatch) | 独立 optimizer model 读 trace, 提炼模式 |
| **Update Step** | textual learning rate (per-step edit budget) | 候选 add/delete/replace edit, 剪枝 |
| **Validation Gate** | held-out validation split | 严格高于当前 skill 才接受 |
| **Rejected-Edit Buffer** | negative feedback memory | rejected edit 不丢弃, 进 buffer 作负反馈 |
| **Slow/Meta Update** | epoch-wise long-horizon update | 比单 batch 更慢的频率整合长程教训 |

**R637 关键数据**:
- **52/52 评测单元最佳或并列最佳**: 6 基准 (SearchQA/SpreadsheetBench/OfficeQA/DocVQA/LiveMathetricianBench/ALFWorld) × 7 模型 (GPT-5.5/5.4/5.4-mini/5.4-nano/5.2 + Qwen3.5-4B) × 3 执行模式 (direct chat/Codex/Claude Code) = 126 cells, 标准配置 52 cells
- **GPT-5.5 direct chat 平均**: 58.8 → 82.3 (+23.5), 比 oracle 还高 +5.4
- **GPT-5.5 inside Codex**: +24.8
- **GPT-5.5 inside Claude Code**: +19.1
- **跨 Harness 迁移 (最反直觉)**: Codex 训练 spreadsheet skill → Claude Code 零优化复用 → 22.1 → 81.8 (+59.7), 比直接在 Claude Code 训练还高 (80.4)
- **小模型 + 优化 skill ≈ 大模型**: GPT-5.4-nano + 优化 skill (57.4) > GPT-5.2 无 skill baseline (51.3)
- **Skill 形态可读**: 中位 920 tokens, 1-4 个 edit 被接受 (validation gate 拒绝大多数)

**为什么是 R637 breakthrough**:
1. **1st-party Microsoft Research Blog post** (Anthropic-style, 高质量学术锚点)
2. **5 组件训练循环** - forward–backward–update + validation gate + rejected-edit buffer + slow/meta update 完整 ML 训练结构搬到文本空间
3. **6 基准 / 7 模型 / 52 cells 全胜** - 罕见的一边倒结果
4. **跨 harness 迁移成立** - Codex 训练 → Claude Code 复用, 表明 skill 是工作流逻辑不是 harness 特定配方
5. **不动模型权重** - 完美匹配 R626 harness-productivity-system cluster "Engineering > Model" 主题
6. **Skill 形态可读** - 920 token / 1-4 edit, 与 Anthropic SKILL.md 协议完全兼容 (R635)
7. **R555 era 变体 ㉓ NEW**: breakthrough via 1st-party blog post skill-optimization (区别于 R633 4-type agentic loop taxonomy + R636 7-methods steering decision framework + R637 skill-as-trainable-parameter, Claude Code team + Microsoft Research 跨厂商 1st-party blog post 持续高产)

**R636 prediction 命中度**:
- 35% breakthrough 概率 → 实际 100% breakthrough via 1st-party blog post (SkillOpt)
- 偏差原因: R636 prediction 假设 breakthrough 主要通过 Claude Code v2.1.200 release 或 Anthropic Engineering 7月 post, 实际 breakthrough 通过 Microsoft Research Blog 1st-party post (跨厂商 1st-party 学术锚点, R636 漏算)
- R555 era 第 10 种 breakthrough pattern: Claude Code release + Anthropic Engineering post + Anthropic Newsroom + GitHub Blog + Cursor Blog + claude.com/blog 2-page audit + claude.com/blog 3-page FULL audit + 1st-party blog post steering (R636) + 1st-party blog post skill-as-trainable-parameter (R637) = 跨厂商 1st-party 学术锚点 + 开源 Pair 闭环

### 0 New 1st-Party Releases (R637)

- **Claude Code**: v2.1.199 仍是 latest (released 2026-07-02T23:35:18Z). v2.1.200 NOT released. R637 仍未 release (R631 v2.1.199 P1 HIT cluster validation 持续)
- **Anthropic Engineering**: 38-day plateau 持续 (last 2026-06-06 how-we-contain-claude). R637 38+ day (R635 36+ → R636 37+ → R637 38+). 7 月工程 post 突破信号仍未出现
- **Anthropic Institute**: 仍 1 post (recursive-self-improvement R626 covered). P0 NOT HIT 持续 38+ day
- **Anthropic Newsroom**: 7/3 0 new engineering. last 6/30 redeploying-fable-5 (R625 covered)
- **OpenAI News**: 7/3 0 new. 20 轮 (R616-R637) 全 0 engineering 持续 (R636 19 → R637 20 轮)
- **Cursor Blog**: 24 slugs 全 covered (R636 audit 51 unique slugs). R637 0 new blog post (Jun 29 仍是最新)
- **Cursor Changelog**: R630 audit 3 entries WSD Skip 持续 + R637 0 new (Jun 30 仍是最新)
- **GitHub Blog**: 7/3 0 new engineering. R637 0 new (Jun 25 仍是最新 evaluating Copilot agentic harness R560 covered)
- **obra/superpowers**: v6.1.1 仍是 latest (2026-07-02T21:58:30Z). v6.2.0 未 release. P8 NOT HIT 持续
- **claude.com/blog FULL 3-page audit (R637)**: 24 unique slugs (R637 main page 1, page 2/3/4 不分页) + R635 3-page audit 51 unique = 75 total → 19 covered via orphan backfill (R215/R304/R311/R323/R406/R418/R432/etc) + 1 NEW Article (steering R636) + 1 NEW admin/spend (giving-admins-more-visibility 2026-07-02 WSD Skip) + 54 WSD Skip (case study / event / product / compliance / legal / customer story)
- **OSS Insight API R637**: 30 candidates audit 完成, 0 跨过 P5 1000 stars 门槛 + NousResearch/hermes-agent-self-evolution 4,478⭐ 命中 (1 NEW Project selected)

### R637 Microsoft Research Blog FULL Audit

R637 Microsoft Research Blog 是新的 1st-party 来源, R637 first-time audit:
- **microsoft/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/**: 2026-06-30 release, 1st-party Microsoft Research Asia academic post. R637 NEW Article (microsoft-research-skillopt-agent-skills-as-trainable-parameters-2026.md)

### R637 Cluster Empirical Validation (P12 HIT 持平 5/7)

R637 cluster data (R636 16:03 CST → R637 18:03 CST, 2h delta):

| Project | R636 Stars | R637 Stars | Δ (2h) | Δ% | 24h 等效 | R637 状态 | R636→R637 |
|---------|-----------|-----------|--------|-----|----------|----------|-----------|
| `obra/superpowers` | 244,872 | 245,035 | +163 | +0.067% | +0.80% | Stable ↑ | +0.05pp (从 R636 +0.75% 略升) |
| `affaan-m/ECC` | 225,384 | 225,448 | +64 | +0.028% | +0.34% | Stable ↑ | +0.01pp (从 R636 +0.33% 略升) |
| `JuliusBrussee/caveman` | 81,854 | 82,198 | +344 | +0.42% | **+5.04%** | **P12 HIT (Growth ↑)** | +0.69pp (从 R636 +4.35% 升) |
| `usestrix/strix` | 33,096 | 33,383 | +287 | +0.87% | **+10.40%** | **STRONG GROWTH** | -1.02pp (从 R636 +11.42% 略降 但仍 STRONG) |
| `openai/codex-plugin-cc` | 22,827 | 22,882 | +55 | +0.24% | **+2.89%** | **P12 HIT (Growth ↑)** | +0.45pp (从 R636 +2.44% 升) |
| `raiyanyahya/recall` | 656 | 657 | +1 | +0.15% | **+1.83%** | **P12 HIT (Growth ↑)** | -2.32pp (从 R636 +4.15% 降 但仍 P12) |
| `amplifthq/opentag` | 577 | 579 | +2 | +0.35% | **+4.15%** | **P12 HIT (Growth ↑)** | -5.33pp (从 R636 +9.48% 显著降 但仍 P12) |

**R637 cluster 实证结论 (Phase 2 持续 5 轮)**:
- **R637 P12 HIT 5/7 持平**: R636 5/7 → R637 5/7 持平
- **2 STRONG GROWTH 持续**: usestrix/strix +10.40%/day 持续 STRONG (R636 +11.42% → R637 +10.40% 略降) + 5 P12 HIT (caveman +5.04% / codex-plugin-cc +2.89% / recall +1.83% / opentag +4.15%)
- **2 STABLE ↑** (R636 2 → R637 2): obra/superpowers +0.80% + affaan-m/ECC +0.34%
- **R637 cluster 状态确认**: Phase 2 二次扩张持续 5 轮 (R631 4/7 → R632 4/7 → R633 4/7 → R634 4/7 → R635 2/7 误判 → R636 5/7 反驳 → **R637 5/7 持平**)
- R635 误判 "Phase 3 入口" 已被 R636 + R637 连续 2 轮反驳 (2 轮 5/7 持续 = Phase 2 持续信号)

**Layer 6 命名扩展**: R626 harness-productivity-system + R634 identity-federation + R635 tool-use/skills-distribution + R636 tool-use/steering-methods + **R637 NEW tool-use/skill-optimization 子维度** (1st-party Microsoft Research + 3rd-party NousResearch 学术+工程闭环)

### R637 防重 Skip 持续有效

- **affaan-m/ECC** 持续 Skip: R118 + R355 + R626 + R634 + R635 + R636 + R637 防重触发
- **obra/superpowers** R420 已覆盖 + R637 v6.1.1 仍是 latest
- **JuliusBrussee/caveman** R420 已覆盖
- **usestrix/strix** R619 已覆盖
- **openai/codex-plugin-cc** R624 已覆盖
- **raiyanyahya/recall** R622 已覆盖
- **amplifthq/opentag** R625 已覆盖
- **ChromeDevTools/chrome-devtools-mcp** R612/R616 已覆盖
- **agentskills/agentskills** R632 NEW Defer 持续
- **microsoft/agent-framework** R-something 已覆盖
- **LangChain/CrewAI/AutoGen** R-something 已覆盖
- **microsoft/SkillOpt** (5,423/10,082/2,814 stars) R295/R297 已覆盖 (commented_urls.txt) + R297 orphan scan + R300+ recommended, 本文 R637 写 Microsoft Research Blog 1st-party Article + 3rd-party NousResearch/hermes-agent-self-evolution Pair 区分
- **Cursor blog reward-hacking-coding-benchmarks** R560 covered (single source = 3 articles: evaluation + harness + research)
- **GitHub Blog evaluating Copilot agentic harness** R560 covered

---

## 📌 R637 完成产出

### Article: 1 (R637 Breakthrough 命中 35% branch via 1st-party Microsoft Research Blog skill-optimization)
- **Article**: `articles/research/microsoft-research-skillopt-agent-skills-as-trainable-parameters-2026.md`
- **来源**: https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/ (Microsoft Research Blog 1st-party, 2026-06-30 release)
- **大小**: 8.5KB, 11 章节
- **结构**: 为什么值得写 + 1 核心命题 + 2 三大失败模式 + 3 forward-backward-update 循环 5 组件 + 4 52/52 评测结果 + 5 Skill 形态 920 token + 6 与既有文章关系 + 7 5 条行动建议 + 8 3 标题备选 + 9 3 金句 + 10 6 引用 + 11 开放问题
- **Microsoft 原话引用**: 4 处 (52 cells 最佳 / training need not be limited to model weights / +23.5 point gain / cross-harness transfer 22.1 → 81.8)
- **Cluster 归位**: Layer 6 第 7 维度 tool-use/skills-distribution (R635 命名) 扩展到 tool-use/skill-optimization 子维度. 与 R311 9 分类 + R635 claude-api Skill + R636 steering 7 methods 互补
- **关键金句**: "Skill 真正的问题不是写什么是'谁在保证它不退化'" + "Training need not be limited to model weights. Procedural knowledge outside the model can also be optimized." + "在没有 verifier 的领域，skill optimizer 与 prompt drift 之间的距离就是 refused-edit buffer 与 validation gate"

### Project: 1 (R637 Pair: 1st-party Article + 3rd-party Open-Source Engine)
- **Project**: `articles/projects/nousresearch-hermes-agent-self-evolution-skill-optimizer-dspy-gepa-4478-stars-2026.md`
- **来源**: https://github.com/NousResearch/hermes-agent-self-evolution (4,478⭐, 509 forks, MIT, 2026-06-17 push)
- **大小**: 9.5KB
- **结构**: 仓库核心信息表 + 5 阶段演化管道 + 演化循环对应表 + 5 guardrails + 成本视角 + 跨 harness 数据源 + 引擎组合 + 与本轮 Article 关系表 + 8 条启示 + Cluster 归位 + 7 处引用
- **README 引用**: 6 处 (How It Works / 5 phases / 2 engines / 5 guardrails / $2-10/run / cross-harness sessiondb)
- **Pair 闭环**: 1st-party Microsoft Research SkillOpt 学术 (forward-backward-update 循环) ↔ 3rd-party NousResearch/hermes-agent-self-evolution 工程 (DSPy+GEPA 开源实现 + 5 guardrails + 5 阶段分批)
- **关键金句**: "All changes go through human review, never direct commit." + "$2-10 per optimization run" + "Qwen3.5-4B 4B open-weight 优化后超过 GPT-5.2 无 skill baseline"

### 5 R635 Project Defer Candidates 持续 (R637 评估)

1. **rtk-ai/rtk** (68,132⭐ Apache-2.0, +62 stars since R636) - CLI proxy reducing LLM tokens 60-90%. Cluster overlap with R626 harness-productivity-system (R626 rtk) 部分覆盖. R637 持续 Defer
2. **browser-use/video-use** (14,168⭐ MIT) - Edit videos with coding agents. cluster member of browser-use. R637 持续 Defer
3. **diegosouzapw/OmniRoute** (10,469⭐ MIT) - AI gateway 231+ providers. R619 covered cluster member. R637 持续 Defer
4. **hugohe3/ppt-master** (36,341⭐ MIT) - AI generates PowerPoint. No cluster overlap, defer. R637 持续 Defer
5. **ogulcancelik/herdr** (10,367⭐ NOASSERTION) - agent multiplexer in terminal. Cluster overlap with R626 harness-productivity-system 部分覆盖. R637 持续 Defer

### Cluster Empirical Validation: 持平 2h delta (5/7 P12 HIT 持平, R635 Phase 3 入口误判持续反驳)

| Project | R636 | R637 | Δ | 24h 等效 | R637 状态 | R636→R637 |
|---------|------|------|---|----------|----------|-----------|
| `obra/superpowers` | 244,872 | 245,035 | +163 | +0.80% | Stable ↑ | +0.05pp |
| `affaan-m/ECC` | 225,384 | 225,448 | +64 | +0.34% | Stable ↑ | +0.01pp |
| `JuliusBrussee/caveman` | 81,854 | 82,198 | +344 | **+5.04%** | **P12 HIT Growth** | **+0.69pp** |
| `usestrix/strix` | 33,096 | 33,383 | +287 | **+10.40%** | **STRONG GROWTH** | **-1.02pp 略降 仍 STRONG** |
| `openai/codex-plugin-cc` | 22,827 | 22,882 | +55 | **+2.89%** | **P12 HIT Growth** | **+0.45pp** |
| `raiyanyahya/recall` | 656 | 657 | +1 | **+1.83%** | **P12 HIT Growth** | **-2.32pp 降 仍 P12** |
| `amplifthq/opentag` | 577 | 579 | +2 | **+4.15%** | **P12 HIT Growth** | **-5.33pp 降 仍 P12** |

**P12 cluster 实证**: 5/7 项目 24h 等效增长率 > 1% P12 阈值. R631 4/7 → R632 4/7 → R633 4/7 → R634 4/7 → R635 2/7 (误判 Phase 3 入口) → R636 5/7 (反驳) → **R637 5/7 持平**. R635 误判持续反驳 (2 轮连续 5/7 = Phase 2 持续信号). Cluster 二次扩张信号持续 2 轮 5/7. Layer 6 命名扩展 R637 NEW tool-use/skill-optimization.

### R637 26 monitoring points 持续

1-25. (见 PENDING.md P1-P25 持续 monitoring)
26. (P26 R637 NEW) tool-use/skill-optimization (Layer 6 第 7 维度子扩展) - Microsoft Research SkillOpt 1st-party 学术 + NousResearch/hermes-agent-self-evolution 3rd-party 开源双闭环
