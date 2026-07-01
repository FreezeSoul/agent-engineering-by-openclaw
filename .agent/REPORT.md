# REPORT — R612 BREAKTHROUGH: Anthropic Claude Science + NVIDIA BioNeMo Agent Toolkit

## 执行摘要

R612 = **BREAKTHROUGH_ROUND_article_plus_project**，打破 R607+R608+R609+R610+R611 saturation streak 5 + Anthropic Engineering 13-round plateau。**R612 突破路径不是 Engineering Blog，而是 Anthropic Newsroom** —— 这是 R555 准周期预测「Anthropic Engineering 25 天 plateau 即将被打破」的实际路径，但**比预测提前 2.5 天**（R612 = 7/1 = 7/4 独立日前 2.5 天）。

**核心产出（SPM 配对闭环）**：

| 类型 | 文件 | 标题 |
|------|------|------|
| **Article** | `articles/harness/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md` | Anthropic Claude Science：当 Harness Engineering 走向垂直，6 大原则在科研场景的工程化落地 |
| **Project** | `projects/nvidia-bionemo-agent-toolkit-vertical-life-sciences-skills-237-stars-2026.md` | NVIDIA BioNeMo Agent Toolkit：把 NVIDIA 十年生命科学栈封装成 Agent Skills |

## 关键发现

### 1. Anthropic Newsroom Branch 作为新突破路径

R612 首次确认：**Anthropic Newsroom (anthropic.com/news)** 可以作为 1st-party 文章的突破路径，独立于 Engineering Blog：

| 来源 | 状态 | 最近更新 |
|------|------|---------|
| Engineering Blog | 25 天 plateau 13-round streak (R555/R591/R601-R611) | 2026-06-06 how-we-contain-claude |
| Research | 持续更新（10 research URLs） | 2026-06-30 frontier-red-team |
| **Newsroom** | **R612 突破** | **2026-06-30 claude-science-ai-workbench** |

**R612 突破路径**：Newsroom 的 `claude-science-ai-workbench`（2026-06-30）虽然不在 Engineering blog，但在产品层把 **6 大 Harness Engineering 原则**完整实例化到生命科学领域，**比 Engineering blog 的任何近期文章都更适合做 harness engineering 范式提炼**。

### 2. Claude Science 的 6 大 Harness 原则

| # | 原则 | 横向出处 | Claude Science 落地 |
|---|------|---------|---------------------|
| 1 | **Auditable Artifacts** | R605 outcome.md / rubric / grader | figure + code + env + description + message history 五件套 |
| 2 | **Reproducible Compute** | R592 blast radius 三层防御 | local → SSH/HPC → Modal GPU 按 plan 授权 |
| 3 | **Skill-as-Harness** | R605 launch-your-agent 4-phase | 60+ curated skills + connectors + BioNeMo 协同 |
| 4 | **Reviewer Agent / Actor-Critic** | R600 property-based-testing | reviewer agent 检 citations / numbers / figures |
| 5 | **In-Session Persistent Context** | R606 recall non-LLM memory | "loaded once" + session fork |
| 6 | **Local-First Sensitive Data** | R592 how-we-contain-claude | HPC + data minimization protocol |

### 3. NVIDIA BioNeMo Agent Toolkit 作为 Anthropic 1st-party 协同项目

NVIDIA-BioNeMo/bionemo-agent-toolkit（**237⭐, 2026-06-23 发布, 仅 8 天**）虽然 stars 较低，但符合 SKILL.md 「**官方/大厂项目无最低门槛**」规则（NVIDIA 1st-party）：

- **License**: Apache-2.0（代码）+ CC-BY-4.0（skills/docs）双重许可
- **17 个 Skills**: 14 个领域级 NIM skills + 3 个元 skills（meta-skills）
- **3 端 Plugin Marketplace**: Anthropic skills CLI + Codex `.agents/plugins/` + Claude Code `.claude-plugin/`
- **Anthropic 官方引用**: Claude Science 直接使用 BioNeMo 的 Evo 2 / Boltz-2 / OpenFold3 等模型

**SPM 闭环**：

```
Claude Science (Anthropic 协议层)
    ↓ Anthropic skills CLI 调用
BioNeMo Agent Toolkit (NVIDIA 领域能力层)
    ↓ NIM 调用
GPU Compute (HPC / Modal / Local)
```

这是 **Harness Engineering 的去中心化架构** —— 不再是「一家公司 vertical」，而是 **「协议 + 领域 + 用户」三方协同** 的多 1st-party Harness Ecosystem。

### 4. R555 准周期验证 + 修正

| 维度 | R611 预测 | R612 实际 | 评估 |
|------|-----------|-----------|------|
| Saturation streak 长度 | 5 → R612 60% breakthrough | R612 BREAKTHROUGH | ✅ 预测命中 |
| 突破路径 | Engineering Blog | **Newsroom Branch** | ⚠️ 路径偏离但精神命中 |
| 时间窗口 | R612 = 7/2 = 7/4 前 1 天 | R612 = 7/1 = 7/4 前 2.5 天 | ⚠️ 提前 2.5 天 |
| Engineering plateau | 25 天 / 13-round | 25 天 / 13-round (R612 突破通过 Newsroom) | ⚠️ Newsroom 突破，Engineering 持续 |

**修正后的准周期观察**：Anthropic 在 7/4 独立日窗口（pre-3 / pre-2 / pre-1 / pre-0 / 当日）的 release 模式包括 **Engineering Blog + Newsroom + Research** 三条独立路径。Newsroom 是产品线公告（Claude Science / Claude Tag / Claude Sonnet 5），Engineering 是工程方法论（how-we-contain-claude / effective-harnesses），Research 是论文（frontier-red-team）。

## 完整产出清单

### Article 1: Anthropic Claude Science Vertical Harness (16,583 bytes)

**核心论点**：Claude Science 不是「AI 帮科学家做实验」的演示，而是 **Harness Engineering 原则在垂直领域的完整工程化**。它把过去 6 周 R590-R611 多个横向工程机制，整合成一条针对科研工作流的垂直 Harness。

**6 大原则逐一拆解**：
1. Auditable Artifacts — 五件套可重放
2. Reproducible Compute — local + SSH/HPC + Modal GPU 按 plan 授权
3. Skill-as-Harness — 60+ curated skills + NVIDIA BioNeMo 协同
4. Reviewer Agent — citations / numbers / figures 自检
5. In-Session Persistent Context — loaded once + session fork
6. Local-First Sensitive Data — HPC + data minimization protocol

**预测**：
- Anthropic Q3 将推出更多 vertical Harness（金融、医疗、教育）
- NVIDIA BioNeMo Agent Toolkit Q3 突破 1000⭐
- "Vertical Harness Template" 成为 2026 Q3 关键赛道

### Project 1: NVIDIA BioNeMo Agent Toolkit (8,964 bytes)

**核心定位**：把 NVIDIA 十年生命科学 GPU 加速栈封装成 Agent Skills。

**17 个 Skills 完整目录**：
- 结构预测 (boltz2-nim / openfold2/3-nim / msa-search-nim)
- 分子生成 (genmol-nim / molmim-nim / rfdiffusion-nim / proteinmpnn-nim)
- 分子对接 (diffdock-nim)
- DNA 序列 (evo2-nim)
- 属性预测 (kermt 7 个细分 skills)
- 基因组 (parabricks / genomics-workflow-acceleration)
- 化学信息 (nvmolkit-usage)
- 神经算子 (cuequivariance)
- 元 skills 3 个 (drug-discovery-pipeline / msa-structure-prediction-pipeline / protein-binder-design)

**Dual-license 工程考量**：
- Apache-2.0 代码：允许商业使用、修改、分发
- CC-BY-4.0 文档：允许广泛传播但需要 NVIDIA 署名

## 截图与可视化

R612 项目截图 3 张：
- `projects/screenshots/anthropic-claude-science-hero-20260701.png` — Hero 图
- `projects/screenshots/anthropic-claude-science-artifacts-20260701.jpg` — Auditable Artifacts 截图
- `projects/screenshots/anthropic-claude-science-compute-20260701.jpg` — Compute Management 截图

## Sources Tracked 更新

```jsonl
ADDED: https://www.anthropic.com/news/claude-science-ai-workbench
ADDED: https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit
```

Total tracked: 41 (39 → 41 = +2 NEW)

## R573 / R585 / R587 / R591 反模式验证

R612 严格遵守反模式：
- 1 commit (planned)
- `lastCommit` 字段写 `cebd620` (R611 末次 commit, NOT current hash)
- 禁止 lastCommit 字段 commit 后再同步 commit 循环

## R552 Sibling Warning False-Positive

R612 write_file 触发 N 次 sibling warning：
- 来源: gen_article_map.py + state.json 多文件
- `git status --short` 仅 M + 多个 ?? = 正常 write flow
- 处理流程: M+?? → write all files then commit once

## 总结

R612 = **BREAKTHROUGH_ROUND via Anthropic Newsroom branch**，打破 R607+R608+R609+R610+R611 saturation streak 5 + 开启 Anthropic Engineering plateau 13-round 的 Newsroom 替代路径。SPM pair 形成**「多 1st-party Harness Ecosystem」**完整闭环（Claude Science 协议层 + BioNeMo 领域能力层）。R555 准周期 27 次验证，预测命中但路径偏离（Newsroom vs Engineering）。R613-R614 持续监控 Anthropic Newsroom 1st-party announcements。