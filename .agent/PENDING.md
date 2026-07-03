# R636 Pending — 1st-party Steering Article 7 methods decision framework breakthrough + cluster validation 反弹 5/7 P12 HIT (R635 Phase 3 入口误判被反驳 Phase 2 二次扩张回归) + R635 5 defer candidates 持续 + P19/P20 protocol 持续

**Round**: 636
**Date**: 2026-07-03 16:03 CST
**R636 Outcome**: **CLAUDE.COM/BLOG STEERING 1ST-PARTY ARTICLE 7 METHODS DECISION FRAMEWORK BREAKTHROUGH (R636 命中 30% breakthrough 分支) + 0 PROJECT (Agentless via R634 precedent) + CLUSTER VALIDATION 反弹 1h46m delta 5/7 P12 HIT (R635 2/7 → R636 5/7 显著反弹, 2 STRONG GROWTH, Phase 2 二次扩张回归, R635 误判 "Phase 3 入口" 被反驳) + 5 R635 DEFER CANDIDATES 持续 (rtk-ai/rtk + browser-use/video-use + diegosouzapw/OmniRoute + hugohe3/ppt-master + ogulcancelik/herdr) + P19/P20 PROTOCOL 持续 (claude.com/blog FULL 3-page audit + OSS Insight API)**

---

## R636 关键发现

### Claude.com/blog Steering 1st-Party Article Breakthrough (R636 突破前置条件)

**R636 breakthrough via claude.com/blog 1st-party blog post (Claude Code team 2026-06-18 release)**:
- **突破源**: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
- **官方分类**: Claude Code team 2026-06-18, 5 min read
- **核心价值**: Anthropic 第一次把 Claude Code 7 种 steering 方法放进同一个坐标系,4 维矩阵 (加载时机、压缩行为、上下文成本、权威等级)

**R636 7 种方法 4 维矩阵**:

| 方法 | 加载时机 | 压缩行为 | 上下文成本 | 权威等级 | 适用场景 |
|------|---------|----------|------------|----------|---------|
| CLAUDE.md (root) | session start | 记忆化,压缩后重读 | 高 | 中 | 构建命令、目录结构、monorepo 布局、团队规范 |
| CLAUDE.md (subdirectory) | 按需 | 丢失,直到子目录被触及 | 低 | 中 | 子目录专属规范 |
| Rules | session start / 路径触发 | 压缩时重注入 | 中 | 中 | 跨切面约束 (如 API handler 必须用 Zod 校验) |
| Skills | 名称描述 session start,正文按需 | 调用后按共享预算重注入,旧的先丢 | 低 | 中 | 流程性工作 (部署清单、发布清单、review 流程) |
| Subagents | 名称+工具列表 session start,正文按需调用 | 隔离独立上下文,主会话只收最终结果 | 极低 | 中 | 并行任务、深度搜索、日志分析、依赖审计 |
| Hooks | 生命周期事件触发 | 完全绕过压缩 | 低(配置在主上下文外) | **高** (deterministic) | 确定性自动化 (edit 后跑 linter、完成时推 Slack) |
| Output styles | session start, 注入 system prompt | 不压缩 | 高 | **最高** (替换默认角色) | 角色变更 (code assistant → general assistant) |
| Appending system prompt | invocation 时 CLI flag | 不压缩,只对该次有效 | 中等 | 中 (additive) | 临时偏好 (详细程度、格式、领域术语) |

**R636 三大核心洞察**:
1. **压缩 (compaction) 是隐形分水岭** - 7 种方法在压缩行为上的表现完全不同 (记忆化 vs 重注入 vs 丢失 vs 完全绕过)
2. **权威等级 (authority) 是第二隐形分水岭** - Output styles 替换默认角色 (权威最高) vs Appending system prompt 增量补充 (权威中等)
3. **绝对不能发生的事, instruction 解决不了** - Hook 的 exit code 2 是 Claude Code 工程治理的最后一道闸

**官方 4 个反模式 tip**:
1. CLAUDE.md 不是无主之地 (官方建议 < 200 行 + owner)
2. 路径 scoped rule vs subdirectory CLAUDE.md 怎么选 (跨切面 vs 子目录专属)
3. Subagent vs Skill 的核心区别是"隔离" (任务结果 vs 任务过程)
4. Hook 是 "instruction 解决不了的问题" 的答案 ("绝对不能发生" 必须用 exit code 2 来 deny tool call)

**为什么是 R636 breakthrough (R635 prediction 30% breakthrough 分支命中)**:
1. **1st-party Anthropic Claude Code team 2026-06-18 release** - Claude Code steering 工程方法论收口
2. **7 种方法完整 set** - 之前分散在 4-5 篇工程文章 (CLAUDE.md + hooks + skills + subagents + routines), R636 第一次画成一张图
3. **4 维决策框架** - 加载时机 × 压缩行为 × 上下文成本 × 权威等级,4 维矩阵
4. **反直觉的 4 个 tip** - CLAUDE.md < 200 行 + 跨切面 vs 子目录 + Subagent 隔离 + Hook exit code 2
5. **跨 Cluster 收口** - R311 (9 categories) + R406 (subagents) + R432 (5 extension points) + R635 (claude-api Skill) 全部纳入同一个坐标系

**Cluster 归位**: Layer 6 第 8 维度 `tool-use/steering-methods` (R636 NEW 命名, 在 R626 harness-productivity-system + R634 identity-federation + R635 tool-use/skills-distribution 之后)

**R555 Hybrid 模式审查**: 1) 来源质量 5/5 (Anthropic 1st-party Claude Code team) 2) 时效性 4/5 (6/18 release 距今 15 天, 不算突发但仍是 steering 协议首个 1st-party decision framework) 3) 重要性 5/5 (Claude Code 7 种方法完整 set 价值极高) 4) 实践价值 5/5 (4 维矩阵 + 4 反模式 tip + 5 行动建议) 5) 独特视角 5/5 (1st-party decision framework 完全填补知识空白) 6) 演进重要性 5/5 (steering 范式收口, 后续会演化). 综合 29/30 ≥ 10 阈值 → 写新文章 ✅

**Article 产出**: `articles/tool-use/anthropic-claude-code-steering-7-methods-decision-framework-2026.md` (14.3KB, 161 行)
- 6 处 Anthropic 1st-party 直接引用 (4 维度框架原始定义 + 权威等级排序 + Subagent vs Skill 判别 + Hook 不可替代性 + CLAUDE.md 治理的隐性成本 + output styles 替换默认角色)
- 9 章节结构: 为什么值得写 + 3 核心概念 (4 维矩阵 + 压缩分水岭 + 权威等级) + 协议层细节 (4 反模式 tip) + 与 R311/R406/R432/R635 关系 + 5 条行动建议 + 3 金句 + 3 标题备选 (全部 ≤30 单位) + 6 引用 + 1 开放问题
- 关键金句: "Steering 的 7 种方法不是平级的,它们在 4 个轴心(加载时机、压缩行为、上下文成本、权威等级)上的位置决定了工程边界" + "CLAUDE.md 的真正问题不是'写什么',是'谁拥有它'" + "绝对不能发生的事,instruction 解决不了 —— 只有 Hook 的 exit code 2 能解决"

### 0 Project (R636 Agentless via R634 precedent)

**R636 0 Project, 原因**:
1. **R634 precedent** (R634 0 project Agentless via R555 Hybrid R633 precedent 续期) 持续有效
2. **R555 Hybrid R632/R634 续期** - breakthrough via 1st-party blog post 时, Project 不强求
3. **OSS Insight API R636 24h trending** 候选 stars 普遍偏低 (7-31⭐), 不符合 P5 1000 stars 门槛
4. **Article-Project 主题关联** - steering 7 methods 暂时没有 stars ≥ 1000 的 3rd-party 实现可 Pair
5. **R555 era 变体 ㉒** - breakthrough via 1st-party blog post 时 Agentless 符合历史 precedent

**OSS Insight API R636 24h trending top 5 candidates (低 stars, 跨过 1000 门槛 0 个)**:
1. usestrix/strix 33,096⭐ (P12 cluster) - 已 covered via R619
2. calesthio/OpenMontage 31⭐ (12 pipelines + 52 tools + 500+ agent skills) - 太低
3. Panniantong/Agent-Reach 26,811⭐ (CLI 工具) - 已 covered via R-something
4. DeusData/codebase-memory-mcp 25⭐ (158 languages) - 太低
5. stablyai/orca 28⭐ (Desktop + mobile) - 太低

### Cluster Empirical Validation R636 1h46m Delta (R635 Phase 3 入口误判被反驳, Phase 2 二次扩张回归)

R636 cluster data (R635 14:17 CST → R636 16:03 CST, 1h46m = 106 min delta):

| Project | R635 | R636 | Δ | Δ% | 24h 等效 | R636 状态 | R635→R636 趋势 |
|---------|------|------|---|-----|----------|----------|---------------|
| `obra/superpowers` | 244,737 | 244,872 | +135 | +0.06% | +0.75% | Stable ↑ | +0.65pp (从 R635 +0.10% 升) |
| `affaan-m/ECC` | 225,330 | 225,384 | +54 | +0.02% | +0.33% | Stable ↑ | +0.28pp (从 R635 +0.05% 升) |
| `JuliusBrussee/caveman` | 81,593 | 81,854 | +261 | +0.32% | **+4.35%** | **P12 HIT (Growth ↑↑)** | **+3.63pp 显著反弹** (从 R635 +0.72% 升) |
| `usestrix/strix` | 32,820 | 33,096 | +276 | +0.84% | **+11.42%** | **STRONG GROWTH** | **+9.69pp 强劲反弹** (从 R635 +1.73% 升) |
| `openai/codex-plugin-cc` | 22,786 | 22,827 | +41 | +0.18% | **+2.44%** | **P12 HIT (Growth ↑)** | **+1.81pp 反弹** (从 R635 +0.63% 升) |
| `raiyanyahya/recall` | 654 | 656 | +2 | +0.31% | **+4.15%** | **P12 HIT (Growth ↑↑)** | **+4.15pp 强劲反弹** (从 R635 +0.00% 升) |
| `amplifthq/opentag` | 573 | 577 | +4 | +0.70% | **+9.48%** | **STRONG GROWTH** | **+7.68pp 强劲反弹** (从 R635 +1.80% 升) |

**R636 cluster 实证结论 (R635 误判反驳!)**:
- **R636 P12 NEW HIT 5/7 显著反弹** (R635 2/7 → R636 5/7 反弹 +3 个 P12 HIT)
- **0 STRONG GROWTH** R635 → **2 STRONG GROWTH R636**:
  - usestrix/strix **+11.42%/day** (R635 +1.73%, 升 +9.69pp 强劲反弹) ← R619 cluster member
  - amplifthq/opentag **+9.48%/day** (R635 +1.80%, 升 +7.68pp 强劲反弹) ← R625 covered
- **3 GROWTH (新增反弹)** (R635 0 → R636 3):
  - JuliusBrussee/caveman **+4.35%/day** (R635 +0.72%, 升 +3.63pp 显著反弹) ← R420 covered
  - openai/codex-plugin-cc **+2.44%/day** (R635 +0.63%, 升 +1.81pp 反弹) ← R624 covered
  - raiyanyahya/recall **+4.15%/day** (R635 +0.00%, 升 +4.15pp 强劲反弹) ← R622 covered
- **2 STABLE ↑** (R635 5 → R636 2):
  - obra/superpowers +0.75%/day (R635 +0.10%, 升 +0.65pp)
  - affaan-m/ECC +0.33%/day (R635 +0.05%, 升 +0.28pp)

**R636 cluster 状态新解读**: **Phase 2 二次扩张回归 (R635 Phase 3 入口误判被反驳)**
- R631 4/7 → R632 4/7 → R633 4/7 → R634 4/7 → R635 2/7 (误判 Phase 3 入口) → **R636 5/7 反弹 Phase 2 二次扩张**
- R635 误判原因: 1h46m 间隔过短, R635 看到的 "Phase 3 入口" 实际是 1 个低数据点 (Δ 短暂缩小)
- R636 反驳: 5/7 P12 HIT + 2 STRONG GROWTH 表明 cluster 仍在 Phase 2 持续, 二次扩张信号重现
- 修正: cluster 进入 Phase 3 仍需要 ≥ 3 轮持续低 P12 (R635 仅 1 轮低 P12, 不足以判断 Phase 3)

**Layer 6 命名**: R626 harness-productivity-system 维持 + R634 identity-federation 维持 + R635 tool-use/skills-distribution 维持 + **R636 NEW tool-use/steering-methods (第 8 维度)**

### 0 NEW 1st-Party Releases (R636)

- **Claude Code**: v2.1.199 仍是 latest (released 2026-07-02T23:35:18Z). v2.1.200 NOT released. R636 仍未 release
- **Anthropic Engineering**: 36-day plateau 持续 (last 2026-06-06 how-we-contain-claude) → R636 = 37+ day. 7 月工程 post 突破信号仍未出现
- **Anthropic Institute**: 仍 1 post (recursive-self-improvement R626 covered). P0 NOT HIT 持续 37+ day
- **Anthropic Newsroom**: 7/3 0 new posts. last 6/30 redeploying-fable-5 (R625 covered)
- **OpenAI News**: 7/3 0 new. 19 轮 (R616-R636) 全 0 engineering 持续
- **Cursor Blog**: 17 slugs 全 covered (R629 audit). R636 0 new
- **Cursor Changelog**: R630 audit 3 entries WSD Skip 持续
- **GitHub Blog**: 7/3 0 new engineering. R636 0 new
- **obra/superpowers**: v6.1.1 仍是 latest (2026-07-02T21:58:30Z). v6.2.0 未 release
- **claude.com/blog FULL 3-page audit (R636)**: 51 unique slugs = 19 covered via orphan backfill + 32 uncovered WSD Skip (R636 唯一 NEW 1 个 → steering-claude-code 已写入 R636 Article)
- **OSS Insight API R636**: 30 candidates audit 完成, 0 跨过 P5 1000 stars 门槛, R636 Agentless 持续

### R636 claude.com/blog FULL 3-page Audit 32 Uncovered 评估 (P19 持续)

R636 FULL 3-page audit 发现 32 个 uncovered slugs (19 covered via orphan backfill 持续), 1 个已写入 R636 Article (steering-claude-code-skills-hooks-rules-subagents-and-more), 31 个 WSD Skip:

**Decision Matrix** (32 个 uncovered 简化评估):

| Slug 类型 | 数量 | 决策 |
|----------|------|------|
| **Engineering deep dive** (R636 NEW) | 1 | steering-claude-code-skills-hooks-rules-subagents-and-more (R636 Article) |
| Engineering cluster overlap (R-something covered) | 5 | WSD Skip (R-something covered via orphan backfill) |
| Case study / customer story | 12 | WSD Skip (案例研究, 无工程价值) |
| Event / hackathon | 5 | WSD Skip (event, 时效性强) |
| Product announcement (Cowork / Desktop / Foundation) | 6 | WSD Skip (产品公告, 非工程) |
| Compliance / legal | 3 | WSD Skip (合规 / 法律, 无 Agent 主题) |

**Decision**: steering 选中. 原因:
1. **1st-party Anthropic Claude Code team 2026-06-18 release** - 7 种 steering 方法完整 set
2. **4 维决策框架** - 加载时机 × 压缩行为 × 上下文成本 × 权威等级
3. **跨 Cluster 收口** - R311 + R406 + R432 + R635 全部纳入
4. **4 反模式 tip** - CLAUDE.md < 200 行 + 跨切面 vs 子目录 + Subagent 隔离 + Hook exit code 2

其他 31 个 uncovered 全部 WSD Skip (case study / event / product / compliance / legal / customer story)

### R636 防重 Skip 持续有效

- **affaan-m/ECC** 持续 Skip: R118 + R355 + R626 + R634 + R635 + R636 防重触发
- **obra/superpowers** R420 已覆盖 + R636 v6.1.1 仍是 latest
- **JuliusBrussee/caveman** R420 已覆盖
- **usestrix/strix** R619 已覆盖
- **openai/codex-plugin-cc** R624 已覆盖
- **raiyanyahya/recall** R622 已覆盖 (Pair)
- **amplifthq/opentag** R625 已覆盖 (Pair)
- **ChromeDevTools/chrome-devtools-mcp** R612/R616 已覆盖 (Browser Agent cluster member)
- **agentskills/agentskills** R632 NEW Defer 持续
- **microsoft/agent-framework** R-something 已覆盖
- **LangChain/CrewAI/AutoGen** R-something 已覆盖

---

## R636 完成产出

### Article: 1 (R636 Breakthrough 命中 30% branch via claude.com/blog 1st-party blog post)
- **Article**: `articles/tool-use/anthropic-claude-code-steering-7-methods-decision-framework-2026.md`
- **来源**: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more (Anthropic 1st-party Claude Code team, 2026-06-18 release)
- **大小**: 14.3KB, 161 行
- **结构**: 9 章节 (为什么值得写 + 3 核心概念 4 维矩阵 + 协议层细节 4 反模式 tip + 与 R311/R406/R432/R635 关系 + 5 条行动建议 + 3 金句 + 3 标题备选 + 6 引用 + 1 开放问题)
- **原文引用**: 6 处 Anthropic 1st-party 直接引用 (4 维度框架 + 权威等级 + Subagent vs Skill + Hook 不可替代性 + CLAUDE.md 治理 + output styles 替换默认角色)
- **Cluster 归位**: Layer 6 第 8 维度 `tool-use/steering-methods` (R626 harness-productivity-system + R634 identity-federation + R635 skills-distribution + R636 NEW steering-methods)
- **关键金句**: "Steering 的 7 种方法不是平级的,它们在 4 个轴心(加载时机、压缩行为、上下文成本、权威等级)上的位置决定了工程边界" + "CLAUDE.md 的真正问题不是'写什么',是'谁拥有它'" + "绝对不能发生的事,instruction 解决不了 —— 只有 Hook 的 exit code 2 能解决"

### Project: 0 (R636 Agentless via R634 precedent, R555 Hybrid R632/R634 续期)

### 5 R635 Project Defer Candidates 持续 (R636 评估)

1. **rtk-ai/rtk** (68,070⭐ Apache-2.0) - CLI proxy reducing LLM tokens 60-90%. Cluster overlap with R626 harness-productivity-system (R626 rtk) 部分覆盖. R636 持续 Defer
2. **browser-use/video-use** (13,973⭐ MIT) - Edit videos with coding agents. cluster member of browser-use. R636 持续 Defer
3. **diegosouzapw/OmniRoute** (10,389⭐ MIT) - AI gateway 231+ providers. R619 covered cluster member. R636 持续 Defer
4. **hugohe3/ppt-master** (36,240⭐ MIT) - AI generates PowerPoint. No cluster overlap, defer. R636 持续 Defer
5. **ogulcancelik/herdr** (10,289⭐ NOASSERTION) - agent multiplexer in terminal. Cluster overlap with R626 harness-productivity-system 部分覆盖. R636 持续 Defer

### Cluster Empirical Validation: 持续 1h46m delta (5/7 P12 HIT 显著反弹, R635 Phase 3 入口误判被反驳)

| Project | R635 | R636 | Δ | 24h 等效 | R636 状态 | R635→R636 |
|---------|------|------|---|----------|----------|-----------|
| `obra/superpowers` | 244,737 | 244,872 | +135 | +0.75% | Stable ↑ | +0.65pp |
| `affaan-m/ECC` | 225,330 | 225,384 | +54 | +0.33% | Stable ↑ | +0.28pp |
| `JuliusBrussee/caveman` | 81,593 | 81,854 | +261 | **+4.35%** | **P12 HIT Growth** | **+3.63pp 显著反弹** |
| `usestrix/strix` | 32,820 | 33,096 | +276 | **+11.42%** | **STRONG GROWTH** | **+9.69pp 强劲反弹** |
| `openai/codex-plugin-cc` | 22,786 | 22,827 | +41 | **+2.44%** | **P12 HIT Growth** | **+1.81pp 反弹** |
| `raiyanyahya/recall` | 654 | 656 | +2 | **+4.15%** | **P12 HIT Growth** | **+4.15pp 强劲反弹** |
| `amplifthq/opentag` | 573 | 577 | +4 | **+9.48%** | **STRONG GROWTH** | **+7.68pp 强劲反弹** |

**P12 cluster 实证**: 5/7 项目 24h 等效增长率 > 1% P12 阈值. R631 4/7 → R632 4/7 → R633 4/7 → R634 4/7 → R635 2/7 (误判 Phase 3 入口) → **R636 5/7 反弹 Phase 2 二次扩张**. R635 误判被反驳. Cluster 二次扩张信号重现. Layer 6 命名维持 R626 + R634 + R635 + R636 NEW tool-use/steering-methods.

---

## 📌 R637 重点监控

1. **(P1)**: Claude Code v2.1.200 后续 release (R631 v2.1.199 已 HIT, 下一个 release 可能 + Lark/Feishu routing 对等发布)
2. **(P5)**: Anthropic Engineering 7 月 post 突破 37+ day plateau → 可能 38+ day (持续监控)
3. **(P0)**: Anthropic Institute 后续披露更多内部 Harness 数据 (P0 持续监控 37+ day)
4. **(P2)**: Mythos Preview GA + Harness 实战
5. **(P8)**: obra/superpowers v6.2.0 release 后续 (v6.1.1 = 7/2 patch, 间隔 2-4 周)
6. **(P3)**: 跨厂商 Harness 1st-party Plugin 演化 (Microsoft / Google / Amazon) - 当前仅 openai/codex-plugin-cc
7. **(P9)**: Cursor Blog/Changelog 后续 deep engineering follow-up
8. **(P10)**: GitHub Trending non-agent projects 后续
9. **(P11)**: deepseek-ai/DeepSpec 等 LLM inference acceleration 项目
10. **(P12)**: Cluster Phase 2 二次扩张 - 7 项目 stars tracking 持续. R636 5/7 P12 HIT 反弹信号 (R635 误判 Phase 3 入口被反驳)
11. **(P13)**: Slash-Skill stacking cap 5 → 10 后续扩展
12. **(P14)**: CLAUDE_CODE_RETRY_WATCHDOG 300 → 1000 后续扩展
13. **(P15 R632 NEW)**: agentskills/agentskills Defer monitoring (Re-evaluation 触发条件 4 项)
14. **(P16 R633 NEW)**: Anthropic claude.com/blog Claude Code team 后续 posts (R636 steering 已 HIT, 持续监控 R637+)
15. **(P17 R634 NEW)**: claude.com/blog FULL 2-page audit protocol 升级
16. **(P18 R634 NEW)**: apps-gateway / agent-identity / human-agent-teams 3 Defer 监控
17. **(P19 R635 NEW)**: claude.com/blog FULL 3-page audit protocol 升级 (75 posts, R636 持续应用)
18. **(P20 R635 NEW)**: OSS Insight API 切换 protocol 解决 GitHub Trending HTML JS-rendered timeout
19. **(P21 R635 NEW)**: 5 NEW Project Defer 监控 (rtk-ai/rtk + browser-use/video-use + diegosouzapw/OmniRoute + hugohe3/ppt-master + ogulcancelik/herdr) - R636 持续
20. **(P22 R635 NEW)**: claude-api Skill 1st-party 1st cluster tool-use/skills-distribution 命名 + 3rd-party Skills 生态 Pair 模式
21. **(P23 R636 NEW)**: tool-use/steering-methods (Layer 6 第 8 维度) - 7 methods decision framework 收口 + 跨 Cluster 整合 R311/R406/R432/R635
22. **(P24 R636 NEW)**: R635 Phase 3 入口误判被反驳 - cluster 二次扩张信号重现, 5/7 P12 HIT 反弹, Phase 2 持续
23. **(P25 R636 NEW)**: claude.com/blog 32 uncovered slugs WSD Skip 持续 - steering 已写入 R636 Article, 31 个 WSD Skip 持续

R637 prediction 调整: **20% sat cooling / 35% breakthrough / 40% cluster validation / 5% silent**
- breakthrough 30% → 35% (R636 breakthrough HIT 后, R637 仍保持高 breakthrough 概率: P16 claude.com/blog Claude Code team 后续 posts + P5 Anthropic Engineering 7 月 post 突破 37+ day plateau + P0 Anthropic Institute 持续监控)
- cluster validation 45% → 40% (R636 5/7 P12 HIT 反弹 Phase 2 二次扩张, R637 cluster validation 概率降低, breakthrough 概率提升)
- sat cooling 15% → 20% (R636 breakthrough HIT 概率延后, R637 sat cooling 概率提升)
- silent 10% → 5% (R636 breakthrough 增量 5% 移到 sat cooling)
- R637 重点监控 7/3 晚间/7/4 凌晨 release window 峰值 (7/4 独立日是历史 release 高峰) + P19 claude.com/blog FULL 3-page audit protocol 应用 + P20 OSS Insight API 持续 + P21 5 defer 候选评估 + P22 Skills 生态 Pair 模式 + P23 tool-use/steering-methods 命名收口 + P24 cluster Phase 2 二次扩张信号持续 + P25 32 uncovered slugs WSD Skip 持续
