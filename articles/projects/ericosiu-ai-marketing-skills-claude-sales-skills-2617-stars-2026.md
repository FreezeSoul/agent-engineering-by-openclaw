---
title: "ericosiu/ai-marketing-skills Claude 销售技能 2617 星 2026"
slug: ericosiu-ai-marketing-skills-claude-sales-skills-2617-stars-2026
date: 2026-06-21
github_url: https://github.com/ericosiu/ai-marketing-skills
stars: 2617
license: MIT
owner: ericosiu
source_date: 2026-06
verified_at: 2026-06-21
verification: github_api_spdx_id
pair_article: anthropic-claude-cowork-sales-leader-4000-accounts-gtm-2026
pair_strength: 5
tags: [claude-code, skills, marketing, sales-pipeline, revops, gtm]
---

# ericosiu/ai-marketing-skills：营销销售的 Claude Code Skills 全家桶

## 一句话推荐

15 个销售/营销 Skill category + 完整 SKILL.md + Python pipeline，每个 skill 都经过真实 pipeline 验证（"battle-tested on real pipelines generating millions in revenue"），是 Anthropic 销售 Leader Claude Cowork 实战的开源工程化身。

## 核心命题

`ericosiu/ai-marketing-skills` 由 Single Brain 团队（Single Grain）开源：把"营销 + 销售"的全流程工作编码成 Claude Code 可调用的 Skill，每个 Skill 不是 toy demo 而是**完整 workflow**（scripts + scoring algorithms + expert panels + automation pipelines）。

**与文章配对**：R472 (`anthropic-claude-cowork-sales-leader-4000-accounts-gtm-2026`) 讲 Anthropic 销售 Leader 用 Claude Cowork + Scheduled Skills 把数据拼装自动化。本项目是该实战的**开源工程化版本** —— 同样思路（SKILL.md + scheduled automation）但覆盖更广（15 个 category 而非 3 个 cadence）。

## 15 个 Skill Category 全景

### 直接对位 R472 文章的 category

| Category | 关键 Skill | R472 文章对位 |
|----------|------------|---------------|
| **Sales Pipeline** | RB2B Router / Deal Resurrector / Trigger Prospector / ICP Learner | 文章第 2 层（每周 forecast） + 第 3 层（propensity scoring） |
| **Sales Playbook** | Pre-Call Briefing / Tiered Packager / Call Analyzer / Pattern Library | 文章第 1 层（每日客户拜访准备） |
| **Revenue Intelligence** | Gong Insight Pipeline / Revenue Attribution / Client Report Generator | 文章第 2 层（每周 forecast report） |
| **Outbound Engine** | Cold Outbound Optimizer / Lead Pipeline / Competitive Monitor | 文章延伸：4,000 账户 prospect 列表重打分 |

### 补充 category

| Category | 关键 Skill | 价值 |
|----------|------------|------|
| **Growth Engine** | Experiment Engine / Pacing Alerts / Weekly Scorecard | 自动营销实验 |
| **Content Ops** | Expert Panel / Quality Gate / Editorial Brain / Quote Miner | 90+ 分内容自动化 |
| **SEO Ops** | Content Attack Briefs / GSC Optimizer / Trend Scout | 关键词攻击 |
| **Finance Ops** | CFO Briefing / Cost Estimate / Scenario Modeler | AI CFO 30 分钟找隐藏成本 |
| **Conversion Ops** | CRO Audit / Survey-to-Lead-Magnet Engine | 着陆页评分 |
| **Podcast Ops** | Podcast-to-Everything Pipeline / Content Calendar | 一集播客 → 20+ 内容 |
| **Team Ops** | Elon Algorithm / Meeting-to-Action Extractor | 严格绩效审计 |
| **Autoresearch** | Variant Generator / Expert Panel Scorer / Evolution Engine | Karpathy-inspired 50+ variants |
| **Deck Generator** | Image Generator / Google Slides Builder | AI 演示文稿生成 |
| **YT Competitive Analysis** | Outlier Detector / Title Pattern Extractor | YouTube outlier 视频分析 |
| **X Long-Form + Humanizer** | Post Writer / Humanizer Checklist / ASCII Diagram Builder | 24-pattern AI slop 检测 |

## 工程实现亮点

### 1. SKILL.md 跨 Agent 标准

每个 category 含 `SKILL.md` 文件，遵循与 Anthropic Skills / MCP 类似的协议标准。Drop 到 Claude Code 项目后 Agent 自动理解工具用法：

```bash
cp ai-marketing-skills/growth-engine/SKILL.md .claude/skills/growth-engine.md
```

然后告诉 Claude Code "Run an experiment testing carousel vs. static posts on LinkedIn" —— Agent 处理其余。

### 2. 真实统计非凭感觉

**Growth Engine** 用 bootstrap confidence intervals + Mann-Whitney U tests —— 真实统计，非 vibes。这与 R337 Trigger.dev 的"durability from real engineering, not toy demo"是同一原则。

**Deal Resurrector** 有三层智能：含 "follow the champion"（跟踪离职联系人到新公司）—— 真实销售场景验证的逻辑。

**ICP Learner** 根据实际 win/loss 数据自动重写 ideal customer profile —— targeting 持续优化。

**Expert Panel** 用递归 domain-specific expert personas 评分内容，直到质量达 90+。

### 3. 安装即用，非 toy

```bash
git clone https://github.com/ericosiu/ai-marketing-skills.git
cd ai-marketing-skills
cd growth-engine  # or sales-pipeline, content-ops, etc.
pip install -r requirements.txt
cp .env.example .env  # edit with API keys
python experiment-engine.py create \
  --hypothesis "Thread posts get 2x engagement vs single posts" \
  --variable format \
  --variants '["thread", "single"]' \
  --metric impressions
```

## 与 R472 的 4-way SPM 配对强度

| Layer | 评估 | 强度 |
|-------|------|------|
| **Layer 1: cluster 共享** | Article 在 `enterprise/` (Sales/RevOps) ↔ Project 在 marketing/sales cluster | ⭐⭐ |
| **Layer 2: SPM 关键词** | "scheduled skill" / "sales pipeline" / "forecast" / "propensity scoring" / "SKILL.md" / "Anthropic" / "Cowork" 共享 | ⭐⭐⭐⭐⭐ |
| **Layer 3: GitHub topics / OpenClaw** | 无 topics，但 README "battle-tested on real pipelines generating millions in revenue" 强暗示 | ⭐⭐⭐ |
| **Layer 4: 维度互补** | Article = Anthropic 内部 closed 实战（4,000 accounts, 1 team）↔ Project = 开源 SDK（数百万 pipeline, generalizable） | ⭐⭐⭐⭐⭐ |

**综合强度**：⭐⭐⭐⭐⭐

## 与其他 Sales/RevOps 项目的对比

| 项目 | Stars | License | 与 R472 主题契合 | 备注 |
|------|-------|---------|------------------|------|
| **ericosiu/ai-marketing-skills** | 2,617 | MIT | ⭐⭐⭐⭐⭐（SKILL.md 协议 + scheduled + sales） | **选定** |
| filip-michalsky/SalesGPT | 2,654 | NOASSERTION | ⭐⭐ (context-aware sales outreach, 不涉及 Cowork/scheduled) | 不选（License 不洁 + 主题偏离）|
| zubair-trabzada/ai-sales-team-claude | 764 | NOASSERTION | ⭐⭐⭐ (Claude Code sales team 但规模小) | 不选（Stars < 1000 + License 不洁）|
| mayooear/ai-company-researcher | 206 | NOASSERTION | ⭐⭐⭐ (lead prospecting with langgraph) | 不选（Stars 低）|

`ericosiu/ai-marketing-skills` 在所有 Sales/RevOps 候选中**唯一同时满足**：
- MIT License 清洁
- Stars > 1000
- SKILL.md 协议与 Anthropic Skills 对齐
- scheduled + sales pipeline 主题与 R472 文章强对位

## 应用场景

### 场景 1：销售 Leader 个人工作流

```bash
# 周五 forecast 自动化（直接对位 R472 文章第 2 层）
pip install ai-marketing-skills/sales-pipeline
python sales-pipeline.py forecast-rollup \
  --salesforce-org $SF_ORG_ID \
  --bigquery-project $BQ_PROJECT \
  --format "anthropic-leadership"
```

### 场景 2：营销 Growth 实验自动化

```bash
# Growth Engine：自动跑 A/B 测试 + 统计显著性
python experiment-engine.py create \
  --hypothesis "Variant B has 20% higher CTR" \
  --metric ctr \
  --variants '["A", "B"]' \
  --auto-stop p-value=0.95
```

### 场景 3：ICP 持续学习

```bash
# ICP Learner：从 win/loss 数据自动重写 ideal customer profile
python icp-learner.py fit \
  --crm-data $CRM_CSV \
  --lookback-days 90 \
  --output ./new-icp.yaml
```

## License / 验证

- **License**：MIT (Copyright 2026 Single Grain)
- **验证路径**：GitHub API `repos/ericosiu/ai-marketing-skills/license` → `spdx_id: "MIT"` (一次 API 调用确认)
- **Stars 验证**：GitHub API `stargazers_count` = 2617 (2026-06-21)
- **License 文件备份验证**：`raw.githubusercontent.com/ericosiu/ai-marketing-skills/main/LICENSE` (主分支 LICENSE 文件确认 MIT)

---

## 关键 Takeaway

1. **SKILL.md 是 Anthropic Skills 协议的最佳生态实践** —— 不是每家公司重写协议，而是直接遵循 Anthropic Skills + Claude Code 的 SKILL.md 标准
2. **Scheduled + sales pipeline = R337 模式的销售版** —— Trigger.dev 在 DevOps 实现的 scheduler + vault + automation 在 Sales Ops 完全复用
3. **真实统计 + 真实业务验证** —— bootstrap confidence intervals + "millions in revenue" 是质量保证，不是 toy demo
4. **开箱即用 + 完整 pipeline** —— 不只 scripts，每个 skill 有 scoring algorithms + expert panels + automation pipelines

---

**引用源**（≥4 处）：
- GitHub 仓库主页 + 15 个 category 表格
- README Quick Start 安装命令
- "What Makes These Different" 段落（真实统计三层）
- "battle-tested on real pipelines generating millions in revenue" README 开头
- LICENSE 文件（MIT）

**Pair**：`articles/enterprise/anthropic-claude-cowork-sales-leader-4000-accounts-gtm-2026.md`

---

> 这个项目不是又一个"AI 工具合集"，而是 **Single Brain 团队把自家数百万营收的真实销售/营销 pipeline 编码成开源 SKILL.md** —— Anthropic 销售 Leader 的 Cowork 实战，是这个项目所代表的范式的 closed-source 实例化。