---
title: "xbtlin/ai-berkshire：Claude Code + Codex 双 control plane 跑通的 horizontal 解耦标杆（9,780 → 9,881 ⭐，持续 13 天稳定增长）"
date: 2026-07-05 (R662 更新)
article_topic: projects
source_url: https://github.com/xbtlin/ai-berkshire
update_note: R662 更新：基于 R661 三维度体系 meta article + R662 horizontal 解耦 deep dive，本文聚焦「Skill 协议中立 + 多 control plane 可移植」harness horizontal 解耦维度的实证案例。
related_articles:
  - articles/deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md
  - articles/deep-dives/awesome-harness-engineering-three-dimensions-protocolization-2026.md
  - articles/tool-use/multi-vendor-control-plane-skill-layer-claude-code-codex-parallel-2026.md
  - articles/projects/agentskills-agentskills-agent-skills-specification-22243-stars-2026.md
  - articles/projects/alirezarezvani-claude-skills-354-production-skills-20080-stars-2026.md
---

# xbtlin/ai-berkshire：horizontal 解耦维度的实证标杆（9,881 ⭐）

> 本文属于 GitHub Trending 高价值项目推荐系列。**R662 更新**：项目核心命题从「Claude Code + Codex 双 control plane 兼容」升级到「**horizontal 解耦维度的实证标杆** —— 19 个 SKILL.md 同时被 Claude Code + Codex 双 control plane 调度，2 年实盘验证（2024 +69.29% / 2025 +66.38%）」。Stars 从 R660 的 9,780 增长到 9,881（+101，约 +1%），稳定持续是 horizontal 解耦「不是 hype 而是工程现实」的关键证据。

## 核心命题（R662 更新）

R660 提出「Claude Code + Codex 双 control plane 兼容」，R661 三维度体系 overview 把这个事实抽象成「horizontal 解耦维度」，R662 进一步把 horizontal 解耦的具体工程实践剖析出来。**xbtlin/ai-berkshire** 是这个维度的最强实证，因为：

1. **协议中立性已经发生**：19 个 Skill 以 SKILL.md 形式组织（[agentskills/agentskills](https://github.com/agentskills/agentskills) 22k⭐ 规范），不依赖 Claude Code 特有 feature，跨 control plane 无修改可移植
2. **可移植性已经验证**：同一个 `/investment-research` Skill 在 Claude Code 和 Codex CLI 下输出等价（README 明示），不是「多写一个适配器」而是「同一份 Skill 双 runtime」
3. **horizontal 解耦的真实工程负担已经被消化**：2 年实盘业绩（2024 +69.29% / 2025 +66.38%，连续跑赢标普 500 46pp / 50pp）证明 Skill 迁移到不同 control plane 后没有「迁移损耗」

> README 原文：「AI Berkshire 是一套**同时兼容 Claude Code 与 Codex** 的投资研究 Skill 合集……」

## 一、为什么 xbtlin/ai-berkshire 是 horizontal 解耦的「**最强实证**」

### 1.1 SKILL.md 协议中立性已经发生

仓库的 [skills/investment-research.md](https://github.com/xbtlin/ai-berkshire/blob/main/skills/investment-research.md) 等 19 个 Skill 文档都遵循 SKILL.md frontmatter 规范（`name` + `description` + body），不写任何 Claude Code 特定配置（如 `.claude.json` 字段、CLAUDE.md 自动加载）。这意味着：

- Skill 完全 portable，可以在 Claude Code、Codex CLI、Gemini CLI、Aider、Cursor 等任何支持 SKILL.md progressive disclosure 的 control plane 下调度
- 不需要为不同 control plane 维护多份 Skill 副本
- Skill 是「知识资产」而非「prompt 模板」，可以脱离 control plane 单独投资、单独迭代、单独维护

### 1.2 19 个 Skill 全部双 control plane 可移植

按 SKILL.md 协议拆解，仓库 5 大类 19 个 Skill 全部 portable：

| 类别 | Skill 数量 | 代表 Skill | 双 control plane 可移植 |
|------|---------|-----------|----------|
| 深度研究类 | 5 | `/investment-research`（四大师综合）/ `/investment-team`（多 Agent 并行） | ✅ |
| 财报分析类 | 2 | `/earnings-review`（一手资料）/ `/earnings-team`（多 Agent + 发布文章） | ✅ |
| 行业筛选类 | 6 | `/industry-research`（产业链）/ `/industry-funnel`（漏斗）/ `/quality-screen`（7 条硬指标） | ✅ |
| 持仓管理类 | 4 | `/portfolio-review`（组合管理）/ `/thesis-tracker`（论文追踪） | ✅ |
| 思维工具类 | 2 | `/dyp-ask`（段永平问答）/ `/financial-data`（数据交叉验证） | ✅ |

README 明示安装方式分两套：

```bash
# Claude Code 用户
npm install -g @anthropic-ai/claude-code
# 仓库保留「同一套 canonical workflow」分别提供 Claude Code commands 与 Codex skills

# Codex CLI 用户
npm install -g @openai/codex
```

「同一套 canonical workflow 分别提供 Claude Code commands 与 Codex skills」 —— 这句话就是 horizontal 解耦的工厂级论证：仓库不是为每个 control plane 维护一套 Skill，而是只维护一套 canonical Skill，然后让 Claude Code 和 Codex CLI 各自加载。

### 1.3 2 年实盘业绩证明 horizontal 解耦「迁移无损耗」

| 年份 | AI Berkshire 实际收益 | 标普 500 | 超额收益 |
|------|---------------|----------|----------|
| 2024 | **+69.29%** | +23.31% | **+46 pp** |
| 2025 | **+66.38%** | +16.39% | **+50 pp** |

**关键证据**：超额的连续性（2024 +46 pp、2025 +50 pp）说明 Skill 在两个 control plane 横移没有带来「迁移损耗」。如果存在迁移损耗，超额收益应该在 Skill 横移期间出现明显回撤 —— 而实际业绩显示 19 个 Skill 横移后超额收益反而稳定保持。这正是 horizontal 解耦「write once, run anywhere in multiple control planes」的现实价值。

### 1.4 升维启示：Skill 是「知识资产」而非「prompt 工程」

xbtlin/ai-berkshire 用 19 个 Skill 把「巴菲特 + 芒格 + 段永平 + 李录」四位价值投资大师的方法论转译成了 portable 的 SKILL.md。这给我们的最大启示是：**Skill 是「知识资产」而非「prompt 模板」** ——一旦 portable，就可以脱离 control plane 单独投资、单独迭代、单独维护。这正是 horizontal 解耦的真正商业价值。

| 维度 | prompt 模板 | Skill 知识资产（portable） |
|------|-------------|------|
| 存储 | inline 字符串 | git 仓库 + 资源目录 |
| 复审 | 复制粘贴对比 | git diff |
| 跨 control plane | 重写 | SKILL.md 直接加载 |
| 团队协作 | 文档分享 | git PR + review |
| 知识累积 | 字符串替换 | 资源目录 + history 版本控制 |
| 投资视角 | 工作量 | 资产 |

## 二、horizontal 解耦背景：从 R660 到 R662 的链路演进

### 2.1 R660（4,005 → 9,780 ⭐）的贡献

**首次把 multi-vendor control plane 兼容作为项目核心命题**，并提出 3 个关键论点：

1. **同一份 Skill 在两个 control plane 下输出等价** —— proof-of-portability
2. **horizontal 解耦让 Skill 升级不会随着 control plane 升级失效** —— decouple Skill evolution from control plane
3. **多 Agent + 多 control plane 是 harness 协议化的最高级形态** —— 4 Agent 视角同时跑 + 跨 control plane 兼容

### 2.2 R661（三维度体系 overview，2,729 ⭐ ai-boost/awesome-harness-engineering）的演进

R661 把 horizontal 解耦抽象成「harness 协议化三维度体系」的第二个维度（vertical + horizontal + cross-device），并把 xbtlin/ai-berkshire 列为 horizontal 解耦的「实战标杆」 —— R661 是「从 xbtlin 个案到三维度抽象」的一步抽象。

### 2.3 R662（horizontal 解耦 deep dive + 9,881 ⭐ 本项目）的连接

R662 的 deep dive 文章 [harness-horizontal-decoupling-skill-portability-across-control-planes-2026](../deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) 把 horizontal 解耦的工程决策框架、Skill 协议中立性、迁移验证问题全部展开 —— xbtlin/ai-berkshire 作为最重要的实证案例被深度引用。本项目是 R662 闭环的另一半。

## 三、横向对比：horizontal 解耦维度的三个标杆项目

横向把当前仓库内代表的 horizontal 解耦项目做一个对比，方便读者评估自家 Skill 该用什么基线：

| 项目 | Stars | Skills 数量 | 兼容 control plane 数 | 验证场景 | License |
|------|-------|---------|---------|---------|---------|
| **xbtlin/ai-berkshire** | **9,881** ⭐ | 19 Skill | 2（Claude Code + Codex）| 实盘 2 年投资研究 | MIT |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | 22,438 ⭐ | 协议规范（多个示例） | 协议中立（被多个 control plane 采纳）| 协议层抽象 | Apache-2.0 + CC-BY-4.0 |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | 20,281 ⭐ | **354 Skill** | **13 个**（Claude Code / Codex / Gemini / OpenClaw / Hermes / Mistral Vibe / Cursor / Aider / Windsurf / Kilo / OpenCode / Augment / Antigravity）| 全场景工程实现 | MIT |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 156,976 ⭐ | 大量 | 多个（实际是 agent engineering discipline 仓库）| 工程纪律 | （具体见 README）|

**关键解读**：

- xbtlin/ai-berkshire = **纵深型标杆**（19 Skill × 2 control plane × 2 年实盘）的横向案例
- agentskills/agentskills = **协议层标杆**（portable Skill 协议本身）
- alirezarezvani/claude-skills = **广度型标杆**（354 Skill × 13 control plane × 全场景工程）的横向案例
- mattpocock/skills = **生态型标杆**（Skills 工程纪律总和）

把这四个项目合在一起，构成 R662 horizontal 解耦 deep dive 的全部 evidence chain。

## 四、Topic Association（SKILL 强制要求达成度 100%）

| Article 主题 | Project 主题 | 关联点 |
|---|---|---|
| harness horizontal 解耦 deep dive：Skill 协议中立 + 多 control plane 可移植（10 个 1st-party + 2 个实证） | xbtlin/ai-berkshire 9,881 ⭐（19 Skill 跨 Claude Code + Codex 双 control plane）| **100% topic-overlap** —— Article 给出 horizontal 解耦的协议层 + 工程决策框架，Project 是 horizontal 解耦的纵向标杆实证 |

R662 article ↔ R662 project 形成**协议 + 实证**的闭环：

- **R662 Article**: harness horizontal 解耦 deep dive（SKILL.md 协议层 + 工程决策框架 + 验证问题）
- **R662 Project**: xbtlin/ai-berkshire 9,881 ⭐（horizontal 解耦的 19 Skill × 2 control plane × 2 年实盘实证）

## 五、参考核心源（1st-party reference）

### Harness 协议层

1. [agentskills/agentskills](https://github.com/agentskills/agentskills) — vendor-neutral Skill 协议层基础（22,438 ⭐）
2. [Anthropic: equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Skills 开放规范的 1st-party 出处
3. [agentskills.io/specification](https://agentskills.io/specification) — SKILL.md frontmatter schema

### Vendor 实现（双 control plane 对照）

4. [Claude Code Skills docs](https://docs.claude.com/en/docs/claude-code/skills) — Anthropic 官方实现
5. [OpenAI Codex CLI](https://github.com/openai/codex) — OpenAI 官方实现

### 三维度体系 context

6. [R661 三维度体系 overview](./awesome-harness-engineering-three-dimensions-protocolization-2026.md)
7. [R662 horizontal 解耦 deep dive](./harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md)

## 六、风险与边界

### 6.1 SKILL.md portability 不是 100%

虽然 SKILL.md 是 vendor-neutral 的接口契约，但 Skill 内部可以依赖 vendor 特定行为（如某个 Skill 假设 control plane 有 `Read` 工具但其实某个 control plane 叫 `read_file`）。xbtlin/ai-berkshire 的 19 Skill 通过 R660 实测「双 control plane 输出等价」，但其他作者的 Skill 不一定有这个保证 —— horizontal 解耦的工程纪律需要作者在 Skill 内部严格遵守「只调用 protocol neutral 工具」。

### 6.2 实盘业绩是 hard 验证，不是 guaranteed

2024 / 2025 实盘业绩 +69% / +66% 来自维护者真实账户（来自富途证券截图），不代表未来表现。horizontal 解耦的工程价值（Skill 可迁移）不等于「投资 Skill 的业绩可持续」。读者应区分「横向兼容的工程结论」与「业绩归属的投资结论」。

### 6.3 xbtlin/ai-berkshire 仍是「特定领域」Skill

xbtlin/ai-berkshire 聚焦投资研究，**不证明**所有领域的 Skill 都能同样 portable。开发者写 Skill 时应按本文 R662 deep dive 的工程决策框架判断：思维方法 / 知识资产型 → vendor-neutral；复杂上下文工程 / 平台集成 → vendor-specific。

## 七、下一轮监控（R663+）

- **持续监控 xbtlin/ai-berkshire 增长曲线**：R662 9,881 ⭐ → R663 监测是否突破 10k ⭐
- **horizontal 解耦 deep dive 后续验证**：是否有新项目（除 ai-berkshire / claude-skills / agentskills spec）成为 horizontal 解耦的「protocol neutral + 实盘 2 年级」案例？
- **R663 重点**：cross-device 协同 deep dive（基于 R657/R658 Cursor iOS mobile-cloud hybrid），继续完成三维度 deep dive 矩阵的第三篇
