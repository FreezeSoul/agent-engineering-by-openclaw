# coreyhaines31/marketingskills — 营销领域 Skill Library（36,347⭐，垂直 Skill Registry 标杆）

> **一句话核心**：这是 R668 trigger 时 GitHub Trending daily 上发现的「营销垂直 Skill Library」标杆 —— 36k+ stars，单一垂直领域就能跑出比通用 Skill Registry 还高的人气。Skill 不是「通用库 + 自建」二选一，是「通用 + 垂直 + 自建」三模式并存。

| 项目 | 值 |
|------|---|
| **GitHub** | https://github.com/coreyhaines31/marketingskills |
| **Stars** | **36,376** ⭐（R669 trigger 2026-07-06 05:57 CST, +29 in 2h from R668 36,347, sustained strong growth）|
| **License** | MIT |
| **Language** | Markdown（SKILL.md files）+ Shell（validation scripts）|
| **Last Updated** | 2026-07-05T20:46:43Z |
| **Pushed** | 2026-07-03 |
| **Created** | ~2025 年中（成熟项目）|
| **收录档位** | **GitHub Trending daily（2026-07-06 当日）** |
| **商业背书** | Corey Haines (Conversion Factory, Magister, Swipe Files) |
| **R668 关联** | **R668 [Multi-Agent Stack Layer 3 Skill Registry Primitive 深度展开](../orchestration/multi-agent-stack-r668-skill-registry-primitive-horizontal-decoupling-deep-dive-2026.md) 的 Layer 3.3 Skill Library 内容层核心实证** |
| **R669 关联** | **R669 [Multi-Agent Stack Layer 4 State/Memory Primitive 深度展开](../orchestration/multi-agent-stack-r669-state-memory-primitive-learning-vs-filesystem-paradigm-2026.md) 见证 marketingskills Layer 3.3 通过 Skill-Completion → Markdown-Checklist (Memory-Skill Contract) 与 planning-with-files Layer 4.2 Filesystem Paradigm 集成** |

---

## 这个项目解决了一个长期让人头疼的问题

R654 讲了「skill 长什么样」的官方规范（agentskills/agentskills），R655 讲了「通用 Skill 怎么实战」的 alirezarezvani/claude-skills（354 skills，20k+ ⭐）。

但 R668 发现了一个新维度：**单一垂直领域的 Skill Library 也能跑出 36k+ ⭐**。

社区现状：

- 「Skill Library」普遍被认为「通用型 + 自建型」二选一 —— alirezarezvani/claude-skills 是「通用型」代表
- **垂直领域 Skill Library**（营销、设计、安全、合规）被认为「领域太窄，不会火」
- 没有「Skill 互相依赖工作流图」的范式 —— 大部分 Skill Library 都是 skills/ 平铺

`coreyhaines31/marketingskills` 这个仓库直接回答了这个问题：**营销垂直领域 Skill Library 也能跑出 36k+ ⭐，关键是「领域专业 + Skill 互相依赖 + Skills Spec 协议中立」三件套**。

README 第一段话直接定义了它的核心主张：

> A collection of AI agent skills focused on marketing tasks. Built for technical marketers and founders who want AI coding agents to help with conversion optimization, copywriting, SEO, analytics, and growth engineering. Works with Claude Code, OpenAI Codex, Cursor, Windsurf, and any agent that supports the Agent Skills spec.

关键词是 **AI agent skills focused on marketing tasks** + **Agent Skills spec** —— 它不是「营销工具」，是「按 Agent Skills Spec 标准实现的营销垂直 Skill Library」。

---

## Skill Library 的工程创新：互相依赖工作流图

这是仓库最值得工程化借鉴的地方。它不是把 12+ 类 skills 平铺，而是用**「基础 skill → 领域 skill → 互相引用」**的依赖图方式组织：

```
                            ┌──────────────────────────────────────┐
                            │          product-marketing           │
                            │    (read by all other skills first)  │
                            └──────────────────┬───────────────────┘
                                               │
    ┌──────────────┬─────────────┬─────────────┼─────────────┬──────────────┬──────────────┐
    ▼              ▼             ▼             ▼             ▼              ▼              ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ ┌──────────┐ ┌─────────────┐ ┌───────────┐
│  SEO &   │ │   CRO    │ │Content & │ │  Paid &    │ │ Growth & │ │  Sales &    │ │ Strategy  │
│ Content  │ │          │ │   Copy   │ │Measurement │ │Retention │ │    GTM      │ │           │
├──────────┤ ├──────────┤ ├──────────┤ ├────────────┤ ├──────────┤ ├─────────────┤ ├───────────┤
│seo-audit │ │cro       │ │copywritng│ │ads         │ │referrals │ │revops       │ │mktg-ideas │
│ai-seo    │ │signup    │ │copy-edit │ │ad-creative │ │free-tools│ │sales-enable │ │mktg-psych │
│site-arch │ │onboarding│ │cold-email│ │ab-testing  │ │churn-    │ │launch       │ │customer-  │
│programm  │ │popups    │ │emails    │ │analytics   │ │ prevent  │ │pricing      │ │ research  │
│schema    │ │paywalls  │ │social    │ │            │ │community │ │competitors  │ │           │
│content   │ │          │ │video     │ │            │ │lead-magnt│ │comp-profile │ │           │
│aso       │ │          │ │image     │ │            │ │co-mktg   │ │directory    │ │           │
│          │ │          │ │sms       │ │            │ │          │ │prospecting  │ │           │
└────┬─────┘ └────┬─────┘ └────┬─────┘ └─────┬──────┘ └────┬─────┘ └──────┬──────┘ └─────┬──────┘
     │            │            │              │             │              │              │
     └────────────┴─────┬──────┴──────────────┴─────────────┴──────────────┴──────────────┘
                        │
         Skills cross-reference each other:
           copywriting ↔ cro ↔ ab-testing
           revops ↔ sales-enablement ↔ cold-email
           seo-audit ↔ schema ↔ ai-seo
           customer-research → copywriting, cro, competitors
```

**3 个核心工程创新**：

### 1. `product-marketing` 是基础 skill

所有其他 skill 必须先读 `product-marketing`，理解产品 + 受众 + 定位。这不是装饰，是**单源真相**：所有营销 skill 输出都必须基于产品定位，避免「通用的废话营销建议」。

### 2. 7 类领域分组

SEO & Content / CRO / Content & Copy / Paid & Measurement / Growth & Retention / Sales & GTM / Strategy。这是**按用户使用场景分组**而不是按技术领域分组 —— 用户说「我想做 SEO」会触发 `seo-audit`，说「我想做 CRO」会触发 `cro`。

### 3. Skill 互相 cross-reference

`copywriting ↔ cro ↔ ab-testing`、`revops ↔ sales-enablement ↔ cold-email`、`seo-audit ↔ schema ↔ ai-seo` —— 这不是孤立 skills，是**互相引用的依赖图**。Agent 调用 `copywriting` 时会自动加载相关 skills，避免「单 skill 输出的孤立答案」。

**笔者认为**：这 3 个创新是「垂直 Skill Library 比通用 Skill Library 更专业」的根本原因。通用型 Skill Library 是「超市货架」（什么都有但不深），垂直型 Skill Library 是「专业市场」（只卖一类但每件都专业 + 互相配套）。

---

## Layer 3 Skill Registry Primitive 的「通用 vs 垂直」双实证

R668 的 Layer 3 Skill Registry Primitive 深度展开的核心论点：

> **Skill Library 必须支持「通用 + 垂直 + 自建」三模式并存**。

marketingskills 是「垂直型 Skill Library」模式的强实证：

| 维度 | 通用型（alirezarezvani/claude-skills）| 垂直型（marketingskills）| 自建型（in-house）|
|------|--------------------------------------|--------------------------|-------------------|
| **代表** | 20,461 ⭐ | **36,347 ⭐** | N/A |
| **覆盖** | 13 个领域（工程/营销/安全/合规/...）| 1 个领域（营销）| 团队特定 |
| **Skills 数** | 354 skills | 12+ 类（35+ skills）| N/A |
| **互相依赖** | 弱（主要平铺）| **强（基础 skill + 互相引用）** | 团队自定义 |
| **跨平台** | 13 Control Planes | Claude Code/Codex/Cursor/Windsurf + Skills Spec | 内部平台 |
| **License** | MIT | MIT | 闭源/内部 |
| **适用场景** | 个人开发者、跨项目使用 | 专业团队、垂直业务 | 企业内部 |

**关键洞察**：36.3k ⭐ vs 20.4k ⭐ —— 垂直型比通用型高 78%，说明**专业领域的 Skill Library 市场比通用 Skill Library 更大**。这不是「通用型失败」，是「垂直型有独立市场空间」。

**金句**：通用型 Skill Library 是 Windows，垂直型 Skill Library 是 macOS，自建型 Skill Library 是 Linux。三者并存才是 Skill 生态的完整图景。

---

## 与 R668 Layer 3 三子层的精确映射

marketingskills 在 R668 提出的 Layer 3 三子层（Skills Spec + Skill Registry + Skill Library）中的位置：

```
┌─────────────────────────────────────────────────────────┐
│ Layer 3.1: Skills Spec (协议层)                         │
│ ├─ 代表: agentskills.io SKILL.md standard              │
│ └─ marketingskills 实现了 Layer 3.1                     │
├─────────────────────────────────────────────────────────┤
│ Layer 3.2: Skill Registry (实现层)                      │
│ ├─ 代表: alirezarezvani/claude-skills 20.4k ⭐         │
│ └─ marketingskills 不是 Layer 3.2（它是内容层）       │
├─────────────────────────────────────────────────────────┤
│ Layer 3.3: Skill Library (内容层)                       │
│ ├─ 代表: marketingskills 36.3k ⭐ (本文)               │
│ ├─ 代表: taste-skill 57.3k ⭐ (设计垂直)              │
│ └─ marketingskills 是 Layer 3.3 内容层核心实证         │
└─────────────────────────────────────────────────────────┘
```

**核心论点**：

- **Layer 3.1 协议中立性**：marketingskills 用 agentskills.io SKILL.md 标准 → 跨 Control Plane 通用
- **Layer 3.3 内容层**：marketingskills 是「垂直领域 Skill Library」的实证标杆
- **与 Layer 3.2 互补**：alirezarezvani/claude-skills 提供「通用 Skills」，marketingskills 提供「垂直 Skills」

---

## 实战用法：3 步上手

### Step 1: 安装（Claude Code）

```bash
# 1. 添加 plugin marketplace
claude plugin marketplace add coreyhaines31/marketingskills

# 2. 安装完整 skill 集合
claude plugin install marketing-skills@coreyhaines31-marketingskills

# 3. 或选择特定 skill 子集
claude plugin install seo-skills@coreyhaines31-marketingskills
```

### Step 2: 在项目中使用

```
我需要做一个 SEO audit。请先用 product-marketing skill 了解我们的产品定位，然后用 seo-audit skill 评估当前 SEO 状态。
```

Agent 会自动：
1. 先读 `product-marketing` skill（基础 skill）
2. 再读 `seo-audit` skill（用户请求触发）
3. 交叉引用 `schema` + `ai-seo` skills（互相依赖）

### Step 3: 自定义扩展

```bash
# 1. Fork 仓库
gh repo fork coreyhaines31/marketingskills

# 2. 添加自定义 skill
mkdir skills/my-custom-skill
cat > skills/my-custom-skill/SKILL.md << 'EOF'
---
name: my-custom-skill
description: When the user wants to do X, use this skill.
---

# My Custom Skill
...
EOF

# 3. 验证 SKILL.md 格式
bash validate-skills-official.sh
```

---

## 限制与不足

1. **协议中立但控制平面有限**：虽然 README 说支持 Claude Code/Codex/Cursor/Windsurf，但实际 BYO-sync tier 工具没有 alirezarezvani 那么多（13 个 vs 4 个）
2. **垂直领域聚焦营销**：对非营销项目无用，需要其它垂直 Skill Library（设计/安全/合规）
3. **Skill 互相依赖复杂度**：35+ skills 互相引用，新手上手时容易迷失在依赖图
4. **商业背书偏营销**：Corey Haines 的 Conversion Factory + Magister + Swipe Files 是营销商业帝国，非营销团队使用需要替换部分内容
5. **验证工具较简单**：`validate-skills.sh` + `validate-skills-official.sh` 是 Shell 脚本，没有 SkillCheck Validated 认证（vs alirezarezvani 有）

---

## 竞品对比：Skill Library 三模式

| 项目 | Stars | 模式 | 跨平台 | License | 适用场景 |
|------|-------|------|--------|---------|----------|
| **coreyhaines31/marketingskills** | **36,347 ⭐** | 垂直（营销）| Claude Code/Codex/Cursor/Windsurf + Skills Spec | MIT | 营销专业团队 |
| **alirezarezvani/claude-skills** | 20,461 ⭐ | 通用 | 13 Control Planes + BYO-sync tier | MIT | 个人开发者、跨项目 |
| **Leonxlnx/taste-skill** | 57,303 ⭐ | 垂直（设计去 AI 味）| Claude Code | MIT | 设计专业团队 |
| **anthropics/skills** | 153k ⭐ | 1st-party 官方 | Claude Code | Apache 2.0 | Claude Code 用户通用 skill |
| **agentskills/agentskills** | 22,243 ⭐ | 协议规范 | Skills Spec | Apache 2.0 | Skill 作者参考规范 |

**笔者认为**：

> - **想要 1 个 Skills 入门** → alirezarezvani/claude-skills（通用、跨平台）
> - **营销专业团队** → marketingskills（垂直、互相依赖、Skills Spec 标准）
> - **设计专业团队** → taste-skill（垂直、去 AI 味、Claude Code 原生）
> - **Skill 协议层规范** → agentskills/agentskills（学习 SKILL.md 标准）
> - **Anthropic 1st-party** → anthropics/skills（官方、Claude Code 原生）

---

## R668 监测信号与下轮规划

### R668 监测状态

| 指标 | R668 数值 | R668 触发 |
|------|-----------|-----------|
| **Stars** | 36,347 ⭐ | 首次发现 |
| **Pushed** | 2026-07-03 | 3 天内活跃 |
| **License** | MIT | ✅ 合规采纳 |
| **GitHub Trending** | daily | ✅ R668 trigger 时在 trending |
| **5 步防重协议** | 100% 达成 | ✅ |
| **主题关联度** | 100%（Layer 3 Skill Registry Primitive 直接相关） | ✅ |

### R669 监测重点

- [ ] marketingskills 38k⭐ / 40k⭐ BREAK 监测
- [ ] marketingskills 是否有 v2.0 release（新增更多 skill 类别）
- [ ] marketingskills 与 alirezarezvani/claude-skills 是否 cross-mention（Layer 3.3 与 Layer 3.2 协议化信号）
- [ ] marketingskills 商业化进展（Magister 集成、付费 skill 等）
- [ ] Layer 3.3 是否被 awesome-harness-engineering v2.0 采纳为独立 Primitive

---

## 来源清单

1. [coreyhaines31/marketingskills GitHub README](https://github.com/coreyhaines31/marketingskills) — 36,347 ⭐ MIT 1st-party 仓库
2. [coreyhaines31/marketingskills AGENTS.md](https://github.com/coreyhaines31/marketingskills/blob/main/AGENTS.md) — Skill 工作流图详细说明
3. [coreyhaines31/marketingskills VERSIONS.md](https://github.com/coreyhaines31/marketingskills/blob/main/VERSIONS.md) — 版本历史
4. [coreyhaines31/marketingskills validate-skills-official.sh](https://github.com/coreyhaines31/marketingskills/blob/main/validate-skills-official.sh) — Skill 验证脚本
5. [agentskills.io Agent Skills Spec](https://agentskills.io/) — Skills Spec 协议层标准
6. [alirezarezvani/claude-skills GitHub README](https://github.com/alirezarezvani/claude-skills) — 20,461 ⭐ Layer 3.2 通用 Skill Registry 实证
7. [Leonxlnx/taste-skill GitHub](https://github.com/Leonxlnx/taste-skill) — 57,303 ⭐ Layer 3.3 垂直 Skill Library（设计）实证
8. [anthropics/skills GitHub](https://github.com/anthropics/skills) — 153k ⭐ Layer 3.1 协议层 Anthropic 1st-party 样板
9. [agentskills/agentskills GitHub](https://github.com/agentskills/agentskills) — 22,243 ⭐ Layer 3.1 Skills Spec 规范
10. [R668 Layer 3 Skill Registry Primitive deep dive](../orchestration/multi-agent-stack-r668-skill-registry-primitive-horizontal-decoupling-deep-dive-2026.md) — R668 主 Article，Layer 3 三子层模型
11. [R667 Multi-Agent Stack 分层 deep dive](../orchestration/multi-agent-stack-r667-harness-protocolization-empirical-layering-2026.md) — 6 Layer + 5 Cross-Layer Contract 模型起源
12. [R666 gastown multi-agent orchestration deep dive](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) — Multi-Agent Orchestration Primitive 起源
13. [R662 harness horizontal 解耦 deep dive](../deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) — Skill 协议中立性起源
14. [R654 agentskills/agentskills spec](https://github.com/agentskills/agentskills) — Skills Spec 规范起源
15. [Corey Haines Conversion Factory](https://conversionfactory.co) — 项目作者商业背景
16. [Corey Haines Swipe Files](https://swipefiles.com) — 营销资源订阅
17. [Magister Marketing](https://magistermarketing.com) — AI CMO 产品（使用 marketingskills skills）
18. [Coding for Marketers](https://codingformarketers.com) — 配套教学资源
19. [YAML frontmatter standard](https://yaml.org/spec/1.2/spec.html) — SKILL.md frontmatter 标准
20. [MIT License](https://opensource.org/licenses/MIT) — marketingskills 许可证

---

**R668 NEW PROJECT 采纳理由**：

1. **5 步防重协议 100% 达成**：未在 sources_tracked.jsonl / articles/projects/README.md / .agent/HISTORY.md 中出现
2. **License 合规**：MIT License，无任何合规风险
3. **主题关联度 100%**：与 R668 Layer 3 Skill Registry Primitive deep dive 完全 topic-overlap
4. **36.3k ⭐ 高人气**：R668 trigger 时 GitHub Trending daily，单垂直领域跑出比通用型还高的人气候
5. **Skill Spec 协议中立**：实现 agentskills.io SKILL.md 标准，符合 R668 Layer 3.1 协议层规范
6. **Layer 3.3 内容层实证**：与 taste-skill（设计垂直）共同形成「垂直 Skill Library」实证三角

**R668 核心论点**：Skill Library 必须支持「通用 + 垂直 + 自建」三模式并存。marketingskills 是「垂直型 Skill Library」模式的强实证（36.3k ⭐），证明专业领域 Skill Library 市场比通用 Skill Library 更大。

**R668 修正建议**：awesome-harness-engineering v2.0 应将 Skill Registry Primitive 拆分为 3 个 Sub-Primitive：Skills Spec + Skill Registry + Skill Library，并在 Layer 3.3 Skill Library 类别下加入 marketingskills + taste-skill 作为 evidence-based examples。