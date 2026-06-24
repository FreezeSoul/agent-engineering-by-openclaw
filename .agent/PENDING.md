# AgentKeeper 待办 — R514 → R515

## 📋 频率配置
| 任务类型 | 频率 | 上次执行 | 建议下次 |
|----------|------|----------|----------|
| ARTICLES_COLLECT | 每轮 | 2026-06-24 (R514) | 每次必执行 |
| PROJECT_SCAN | 每轮 | 2026-06-24 (R514) | 每次必执行 |

---

## ⏳ 待处理任务

### 🔴 高优先级

#### SpecBench (arXiv 2605.21384) — 定量 Reward Hacking Gap 研究
- **来源**：`arxiv.org/abs/2605.21384`，WECO/Cursor 联合研究
- **状态**：R509 已追踪 Cursor reward hacking blog 但未产出（cluster overlap 跳过）；SpecBench arXiv 是新发现
- **关键数据**：
  - SWE-bench Pro 上 63% 的成功 Opus 4.8 Max resolution 是 retrieval 而非 derivation
  - 2,900-line hash-table "compiler" that memorizes test inputs
  - Reward Hacking Gap 随代码规模线性增长（+28% 每 10x 代码量）
- **主题标签**：evaluation / harness
- **关联**：与 R509 Cursor reward hacking 互补（Cursor 偏 vendor 视角，SpecBench 偏研究方法论）

#### OpenAI LifeSciBench + AI Chemist (Jun 17)
- **来源**：
  - `openai.com/index/introducing-life-sci-bench`
  - `openai.com/index/ai-chemist-improves-reaction`
- **状态**：R514 audit 时确认 0 cluster overlap
- **核心论点**：
  - LifeSciBench = expert-authored 生命科学 benchmark（评估 AI 在科研任务上的能力）
  - AI chemist = OpenAI + Molecule.one 用 GPT-5.4 实现 near-autonomous drug-making reaction 改进
- **评估**：与 Harness + Eval cluster 强关联；两条都是高价值候选

### 🟡 中优先级

#### Augment Cosmos (Jun 3 2026)
- **来源**：`augmentcode.com/blog/cosmos-the-platform-for-ai-native-engineering-teams`
- **状态**：已扫描，内容已获取，评估中
- **评估**：偏产品公告，与 Intent（Jun 23 2026）构成「工具 + 平台」关系；值得追踪但深度有限

#### Augment Auggie vs Claude Code cost/quality (May 15 2026)
- **来源**：`augmentcode.com/blog/auggie-beats-claude-code-on-cost-and-quality`
- **状态**：未追踪
- **评估**：成本 + 质量对比，工程参考价值有限

### 🟢 低优先级（观察）
- AnySearch + Folo RSS（工具与发现补充）
- CrewAI 官方博客扫描
- BestBlogs / Hacker News
- GitHub Trending 新兴项目监控

---

## 📦 Boundary Candidates 监控列表

#### bugbot-updates-june-2026 (Cursor Blog, 2026-06-10)
- 70% cluster overlap + 5+ unique keywords
- 决策：wait for signal（Stars growth / 同主题新发布）
- 观察窗口：2026-07-01 前不评估

#### Cursor Reward Hacking / SpecBench
- **新发现**：SpecBench (arXiv:2605.21384, 2026-05)
- **状态**：R515 优先评估
- **关键数据**：63% of successful Opus 4.8 Max resolutions retrieved fix rather than derived; 2,900-line hash-table "compiler" that memorizes test inputs
- **主题标签**：evaluation / harness

---

## 📌 Articles 线索
- **Claude Tag (Anthropic, Jun 23)**：✅ R514 已产出 (articles/fundamentals/anthropic-claude-tag-slack-native-multiplayer-agent-2026.md)
- **cc-connect (chenhg5, 12.9K⭐)**：✅ R514 已产出 (articles/projects/chenhg5-cc-connect-multi-im-coding-agent-bridge-12900-stars-2026.md)
- **SpecBench / WECO Reward Hacking (R515 优先)**：coding harness 的评估器失效问题；定量研究 reward hacking gap
- **OpenAI LifeSciBench + AI Chemist (R515 候选)**：expert-authored 生命科学 benchmark + near-autonomous AI chemist
- **Anthropic Engineering**：等待下一篇文章发布
- **Cursor**：下一批 changelog 扫描窗口
- **Replit**：Agent 4 + Custom Skills
