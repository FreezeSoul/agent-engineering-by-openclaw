# Multi-Agent Stack Layer 3 (Skill Registry Primitive) 深度展开：Skills = 协议中立 + 跨 Control Plane 通用 + 通用 vs 垂直双实证

> 当一个项目用 36k ⭐ 证明「Skills 跨 Control Plane 通用」是 Multi-Agent Stack 的横向解耦核心时——这不是单一项目的成功，是 Layer 3 范式的工程化确立。

---

## 核心命题

**Skill Registry 不是单一 Primitive，是「Skills Spec (协议层) + Skill Registry (实现层) + Skill Library (内容层)」3 子层。**

R667 提出了 Multi-Agent Stack 的 6 Layer + 5 Cross-Layer Contract 分层模型。但 Layer 3 (Skill Registry Primitive) 在 R667 中只是简略提及——`Leonxlnx/taste-skill (57.2k ⭐)`、`alirezarezvani/claude-skills (20.4k ⭐)`、`agentskills/agentskills` 三个 evidence-based examples。

R668 的核心发现：**Skill Registry 这一层实际上正在独立分裂为 3 个子层**：

```
┌─────────────────────────────────────────────────────────┐
│ Layer 3.1: Skills Spec (协议层)                         │
│ ├─ 代表: agentskills.io / Agent Skills Spec             │
│ ├─ 职责: 定义 SKILL.md 格式 + 跨 Control Plane 契约     │
│ └─ 范式: Markdown + YAML frontmatter + 自然语言工作流   │
├─────────────────────────────────────────────────────────┤
│ Layer 3.2: Skill Registry (实现层)                      │
│ ├─ 代表: alirezarezvani/claude-skills (20.4k ⭐)        │
│ ├─ 职责: 把 Skill Library 部署到 Control Plane          │
│ └─ 范式: 通用 Skill 集合 + 跨 13+ Control Plane 同步    │
├─────────────────────────────────────────────────────────┤
│ Layer 3.3: Skill Library (内容层)                       │
│ ├─ 代表: marketingskills (36.3k ⭐, 垂直营销)            │
│ ├─ 职责: 提供领域特定 Skill 实现                       │
│ └─ 范式: 垂直深挖 + Skills Spec 实现 + 跨 Control Plane│
└─────────────────────────────────────────────────────────┘
```

**金句**：Skill Registry Primitive 不是「一组 Skill 文件」，是「协议中立 + 跨 Control Plane 通用 + 领域可垂直深挖」的 3 子层架构。这是 R667 6 Layer 模型在 Layer 3 的精细化展开。

---

## 一、为什么 Skill Registry 必须细分为 3 子层

### 1.1 R667 的简化模型不够

R667 的 Layer 3 简化表述：

> Layer 3: Skill Registry
> ├─ 载体：SKILL.md + skill spec
> ├─ 代表：taste-skill、alirezarezvani/claude-skills、agentskills/agentskills
> └─ 职责：给 Agent 注入领域知识 + 工作流

这个简化在 R667 是自洽的（因为 Layer 3 的实证证据还不够充分）。但 R668 提供了 3 个新的关键证据：

1. **agentskills.io 标准正在形成**：R668 trigger 时已成为 Skill Spec 的事实标准
2. **alirezarezvani/claude-skills 跨 13+ Control Plane 同步**：BYO-sync tier 概念证明 Skill Registry 必须支持「协议中立 + 跨平台同步」
3. **marketingskills 36,347 ⭐ 单垂直领域**：证明 Skill Library 必须支持「领域垂直深挖」

这 3 个证据表明 Layer 3 不是单一 Primitive，必须细分为 3 子层。

### 1.2 与 R666 R667 6 Layer 模型的关系

R667 的 6 Layer 抽象层不会变（仍然有价值）。R668 是在 Layer 3 内部细化：

| R667 6 Layer | R668 Layer 3 细化为 3 子层 |
|--------------|---------------------------|
| Layer 0: Transport | 不变（PTY + socket + HTTP）|
| Layer 1: Multiplexer | 不变（herdr + tmux）|
| Layer 2: Orchestrator | 不变（gastown + Claude Code Agent Teams）|
| **Layer 3: Skill Registry** | **细分为 3.1 Skills Spec + 3.2 Skill Registry + 3.3 Skill Library** |
| Layer 4: State/Memory | 不变（planning-with-files + vercel/eve）|
| Layer 5: Tool Runtime | 不变（MCP + SDK + sandbox）|

**笔者认为**：R667 的 6 Layer 是正确的「宏观分层」，R668 的 Layer 3 三子层是「中观拆分」。两个抽象层级都对，关键看读者需要什么粒度——选框架时用 6 Layer，看 Skill 工程时用 3 子层。

---

## 二、Layer 3.1: Skills Spec (协议层) — Markdown + YAML frontmatter + 自然语言工作流

### 2.1 协议层的核心问题

Skill Spec 要回答：「Skill 是什么格式？Control Plane 如何发现 Skill？Skill 如何与 Agent 交互？」

R668 监测到的关键信号：

1. **agentskills.io 标准**：定义了 `SKILL.md` + YAML frontmatter 的标准格式
2. **Anthropic 官方采纳**：Claude Code 用 SKILL.md 作为 Skill 的载体
3. **跨 Control Plane 通用**：Claude Code / OpenAI Codex / Gemini CLI / Cursor / Windsurf 都支持 SKILL.md 格式

**核心洞察**：Skills Spec 的核心是「Markdown + YAML frontmatter + 自然语言工作流」三件套。这是 Layer 3.1 协议层的具体技术形态。

### 2.2 SKILL.md 的具体结构

```markdown
---
name: skill-name
description: When the user wants to do X, use this skill.
---

# Skill Title

## When to Use This Skill
- 触发条件 1
- 触发条件 2

## Workflow
1. Step 1
2. Step 2
3. Step 3

## Best Practices
- 最佳实践 1
- 最佳实践 2

## Examples
- 示例 1
- 示例 2
```

**3 个关键字段**：

- **`name`**：Skill 唯一标识符（用于 Control Plane 注册）
- **`description`**：触发条件描述（Agent 用自然语言匹配）
- **Markdown body**：完整工作流 + 最佳实践 + 示例

这种「YAML + Markdown」的混合格式揭示了 Skills Spec 的设计哲学：**机器可读 + 人类可写**。YAML 让 Control Plane 能注册和索引，Markdown 让 Skill 作者能用自然语言表达工作流。

### 2.3 为什么 SKILL.md 不是 `.py` 或 `.json`

R662 的 horizontal 解耦 deep dive 提到 Skill 协议中立性。R668 进一步指出：

> **Markdown + YAML 是 Skill 的最佳载体，因为 Skills 是「给 Agent 看的文档」而不是「给 Computer 跑的代码」**。

对比三种 Skill 载体：

| 载体 | 机器可读 | 人类可写 | 跨平台 | LLM-friendly |
|------|---------|---------|--------|--------------|
| `.py` 代码 | ✅✅ | ❌ | ✅ | ❌ |
| `.json` 配置 | ✅✅ | ❌ | ✅ | ⚠️ |
| `.md` SKILL.md | ✅ | ✅✅ | ✅✅ | ✅✅ |

Skills Spec 选择 Markdown 是因为 Skills 本质上是「领域专家写给 Agent 的工作流说明」，不是「给 Computer 执行的程序」。

**金句**：Skill 是文档，不是代码。Markdown 是文档的最佳载体，所以 SKILL.md 是 Skills Spec 的最佳格式。

---

## 三、Layer 3.2: Skill Registry (实现层) — alirezarezvani/claude-skills 跨 13 Control Plane 同步机制

### 3.1 alirezarezvani/claude-skills 的核心价值

R668 监测：alirezarezvani/claude-skills 从 R311 的 5,200 ⭐ → R664 20,424 ⭐ → R668 **20,461 ⭐**（跨 R655-R668 13+ rounds 持续 monitoring）。

这不是普通的 Skills 集合。R668 阅读 README 发现的 3 个核心价值：

1. **跨 13 AI Coding Tools 通用**：Claude Code / OpenAI Codex / Gemini CLI / OpenClaw / Hermes Agent / Mistral Vibe / Cursor / Aider / Windsurf / Kilo Code / OpenCode / Augment / Antigravity
2. **354 production-ready skills**：覆盖工程、DevOps、营销（含 AEO）、安全、合规、C 级咨询、研究、企业运营
3. **agentskills.io SKILL.md 标准**：与 Layer 3.1 协议层完全一致

**对比 R311 时的 5,200 ⭐ → R668 的 20,461 ⭐**：3.9x 增长。这说明 Skill Registry 需求在过去 6 个月持续爆发。

### 3.2 跨 Control Plane 同步：BYO-sync tier 概念

alirezarezvani README 的关键脚注：

> Hermes Agent is **BYO-sync tier**: the repo ships a pre-generated `.hermes/skills/claude-skills/` tree, but you run `python scripts/sync-hermes-skills.py` once locally to install into `~/.hermes/skills/`. Uses the same agentskills.io SKILL.md standard — no format conversion.
> Mistral Vibe is also **BYO-sync tier**: the repo ships a pre-generated `.vibe/skills/claude-skills/` tree, run `./scripts/vibe-install.sh` once locally to install into `~/.vibe/skills/`. Same agentskills.io SKILL.md standard — no format conversion.

**BYO-sync tier** = Build Your Own sync tier。这是 Skill Registry 实现层的核心工程机制：

```
alirezarezvani/claude-skills (source of truth)
    │
    ├── Claude Code: native install
    ├── OpenAI Codex: native install
    ├── Gemini CLI: native install
    ├── Cursor: native install
    ├── Windsurf: native install
    ├── Hermes Agent: BYO-sync tier (sync-hermes-skills.py)
    └── Mistral Vibe: BYO-sync tier (vibe-install.sh)
```

**核心洞察**：BYO-sync tier 不是「alirezarezvani 一家支持所有平台」——而是「agentskills.io 标准 + Skill 协议中立 + 各 Control Plane 自己写 sync 脚本」。这是 Layer 3.2 的关键设计哲学：

> **Skill Registry 不应是一个 do-everything 平台，而是「协议中立 + 各 Control Plane 自治」的去中心化生态**。

### 3.3 与 Anthropic 官方 skills 的关系

R668 监测：Anthropic 官方有 `anthropics/skills`（153k ⭐），但 alirezarezvani/claude-skills 是「独立第三方扩展」。

两者的区别：

| 维度 | anthropics/skills (1st-party) | alirezarezvani/claude-skills (3rd-party) |
|------|-------------------------------|-------------------------------------------|
| **范围** | 通用 + 核心 skills | 354 production-ready skills 全领域 |
| **跨平台** | Claude Code only | 13 Control Planes |
| **维护** | Anthropic 官方 | 社区驱动 + 个人维护 |
| **质量** | 标准化、严格 | 实战化、覆盖广 |

**笔者认为**：Anthropic 官方 skills 是「Layer 3.1 协议层的实现样板」，alirezarezvani/claude-skills 是「Layer 3.2 实现层的实战生态」。两者是互补关系，不是替代关系。

---

## 四、Layer 3.3: Skill Library (内容层) — marketingskills 36,347 ⭐ 垂直深挖

### 4.1 marketingskills 的 R668 关键发现

R668 trigger 时核心yhaines31/marketingskills 是 GitHub Trending daily（首次发现）。防重协议 5 步检查：

- ✅ Step 1 grep sources_tracked.jsonl：未追踪
- ✅ Step 2 grep articles/projects/README.md：未发布
- ✅ Step 3 grep .agent/HISTORY.md：未提及
- ✅ Step 4 License 核实：MIT License（合规）
- ✅ Step 5 决定：NEW PROJECT

**核心数据**：

| 指标 | marketingskills | alirezarezvani | taste-skill |
|------|----------------|----------------|-------------|
| **Stars** | **36,347 ⭐** | 20,461 ⭐ | 57,303 ⭐ |
| **Skills 数** | 12+ 类（35+ skills）| 354 skills | N/A |
| **覆盖领域** | 垂直：营销 | 通用：13 个领域 | 垂直：设计去 AI 味 |
| **跨平台** | Claude Code/Codex/Cursor/Windsurf + Agent Skills spec | 13 Control Planes | Claude Code |
| **License** | MIT | MIT | MIT |
| **维护者** | Corey Haines (Conversion Factory) | 社区 | Leonxlnx |

**关键洞察**：marketingskills 是 Layer 3.3 Skill Library 的「垂直深挖」实证——36,347 ⭐ 比 R311 的 5,200 ⭐ 高 7x，单领域（marketing）就能跑出 36k ⭐ 项目。

### 4.2 marketingskills 的 Skill 分类与依赖图

marketingskills 的核心创新是「**Skill 互相依赖的工作流图**」：

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

1. **`product-marketing` 是基础 skill**：所有其他 skill 必须先读它，理解产品 + 受众 + 定位
2. **7 类领域分组**：SEO & Content / CRO / Content & Copy / Paid & Measurement / Growth & Retention / Sales & GTM / Strategy
3. **Skill 互相 cross-reference**：不是孤立 skills，是互相引用的依赖图

### 4.3 marketingskills 与 alirezarezvani/claude-skills 的「垂直 vs 通用」双实证

R668 的关键发现：**Layer 3.3 Skill Library 必须支持「垂直 vs 通用」双模式**。

| 模式 | 代表 | 优势 | 适用场景 |
|------|------|------|----------|
| **通用型 Skill Library** | alirezarezvani/claude-skills (20.4k ⭐) | 覆盖广、跨平台、跨领域 | 个人开发者、跨项目使用 |
| **垂直型 Skill Library** | marketingskills (36.3k ⭐) | 深度优化、互相依赖、领域专业 | 专业团队、垂直业务（营销、设计、安全）|

**核心洞察**：36.3k ⭐ 的市场垂直型项目证明「专业领域的 Skill Library」有巨大市场需求。Layer 3.3 不应只有「通用 + 自建」二选一，应该是「通用型 Skill Library + 垂直型 Skill Library + 自建 Skill Library」三模式并存。

**金句**：通用型 Skill Library 是 Windows，垂直型 Skill Library 是 macOS，自建 Skill Library 是 Linux。Windows 装机量最大，macOS 用户最忠诚，Linux 灵活性最高——Skill Library 也是这样。

---

## 五、Layer 3 三子层与 R667 6 Layer 模型的关系

### 5.1 完整的 Multi-Agent Stack Layer 3 视图

```
┌─────────────────────────────────────────────────────────────────────┐
│ Layer 3: Skill Registry Primitive (R668 细化为 3 子层)              │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 3.1: Skills Spec (协议层)                                     │
│ ├─ 代表: agentskills.io / Agent Skills Spec                         │
│ ├─ 职责: SKILL.md + YAML frontmatter + 自然语言工作流               │
│ └─ 范式: Markdown 即协议                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 3.2: Skill Registry (实现层)                                  │
│ ├─ 代表: alirezarezvani/claude-skills (20.4k ⭐)                    │
│ ├─ 职责: 跨 13 Control Plane 同步 Skill                             │
│ └─ 范式: BYO-sync tier + 协议中立 + 通用 Skill 集合                 │
├─────────────────────────────────────────────────────────────────────┤
│ Layer 3.3: Skill Library (内容层)                                   │
│ ├─ 代表: marketingskills (36.3k ⭐), taste-skill (57.3k ⭐)         │
│ ├─ 职责: 提供垂直领域 Skill 实现 + 互相依赖工作流                   │
│ └─ 范式: 垂直深挖 + Skills Spec 实现 + 跨 Control Plane 通用       │
├─────────────────────────────────────────────────────────────────────┤
│ 跨 Layer 3 子层契约                                                 │
│ ├─ Layer 3.1 → Layer 3.2: Skill Spec → Skill Registry 实现          │
│ ├─ Layer 3.1 → Layer 3.3: Skill Spec → Skill Library 实现          │
│ └─ Layer 3.2 ↔ Layer 3.3: 通用 Skill Registry 集成垂直 Skill Library│
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 与其他 Layer 的 Cross-Layer Contract

Layer 3 不是孤立存在的，必须与 Layer 1-2 和 Layer 4-5 联动：

**Layer 3 ↔ Layer 2 (Orchestrator)**：
- Orchestrator 决定「何时调用哪个 Skill」
- Skill 决定「被调用时如何工作」
- 契约: Bead-ID → Skill-Name 映射

**Layer 3 ↔ Layer 1 (Multiplexer)**：
- Multiplexer 在 Agent pane 启动时加载 Skill
- Skill 输出通过 pane 渲染给用户
- 契约: Pane-ID → Skill-Loaded-Status

**Layer 3 ↔ Layer 4 (State/Memory)**：
- Skill 完成时更新 Markdown checklist
- planning-with-files 把 Skill 执行历史持久化
- 契约: Skill-Completion → Markdown-Checklist-Update

**Layer 3 ↔ Layer 5 (Tool Runtime)**：
- Skill 调用 MCP servers / SDK
- MCP 输出回传给 Skill 进行下一步决策
- 契约: Skill-Tool-Call → MCP-Response

**笔者认为**：Layer 3 的核心价值不是「Skill 本身」，而是「Skill 是 Layer 1-2 编排与 Layer 4-5 执行之间的『领域知识注入层』」。没有 Skill Registry，Orchestrator 是空架子；有了 Skill Registry，Orchestrator 才能「召唤领域专家」。

---

## 六、R668 v2.0 修正预测：对 awesome-harness-engineering 的进一步修正

### 6.1 R667 修正 vs R668 进一步修正

R667 的修正建议：

| R666 v2.0 预测 | R667 修正建议 |
|----------------|---------------|
| Multi-Agent Orchestration Primitive（单 Primitive）| 5 Layer Primitive + 4 Cross-Layer Contract |

R668 在 R667 基础上进一步修正 Layer 3：

| R667 v2.0 修正 | R668 进一步修正 |
|----------------|----------------|
| Skill Registry Primitive（单 Primitive）| **3 Sub-Layer**: Skills Spec + Skill Registry + Skill Library |

### 6.2 修正理由

1. **agentskills.io 标准出现**：必须承认协议层的独立存在
2. **alirezarezvani/claude-skills 跨 13 Control Plane 同步**：必须承认实现层的独立存在
3. **marketingskills 36.3k ⭐ + taste-skill 57.3k ⭐**：必须承认内容层的独立存在

如果 v2.0 不区分 3 子层，开发者会被迫实现一个 single-binary Skill Registry（既要管协议，又要管实现，又要管内容）——这是反 Unix 哲学的。

### 6.3 给 awesome-harness-engineering v2.0 维护者的具体建议

```
README 增加章节:

## Multi-Agent Stack Layer 3 (Skill Registry Primitive)

### Layer 3.1: Skills Spec (协议层)
- agentskills.io SKILL.md standard
- Markdown + YAML frontmatter
- 跨 Control Plane 协议中立

### Layer 3.2: Skill Registry (实现层)
- alirezarezvani/claude-skills 20.4k ⭐ (跨 13 Control Planes)
- BYO-sync tier 机制
- 通用 Skill Library 模式

### Layer 3.3: Skill Library (内容层)
- marketingskills 36.3k ⭐ (营销垂直)
- taste-skill 57.3k ⭐ (设计垂直)
- 互相依赖 Skill 工作流图

### Cross-Layer 3 契约
- Layer 3.1 → Layer 3.2: Skill Spec → Skill Registry 实现
- Layer 3.1 → Layer 3.3: Skill Spec → Skill Library 实现
- Layer 3.2 ↔ Layer 3.3: 通用 ↔ 垂直 Skill Library 集成
```

---

## 七、Layer 3 持续 monitoring：5 个关键项目 R668 状态

### 7.1 R668 监测的 6 个 Skill Registry Primitive 相关项目

R668 trigger 时监测以下 6 个项目（**5 个 P-tracking + 1 个 NEW**）：

| 项目 | Stars (R668) | 增长 | 12k/25k/60k 临界 | R668 监测结果 |
|------|--------------|------|-----------------|--------------|
| **gastownhall/gastown** | 16,330 ⭐ | +20 (R667→R668) | 17k⭐ = 670 gap | UPDATE 持续 monitoring |
| **ogulcancelik/herdr** | 11,950 ⭐ | +47 (R667→R668) | **12k⭐ = 50 gap** | **R668 likely 12k⭐ BREAK** |
| **OthmanAdi/planning-with-files** | 24,647 ⭐ | +25 (R667→R668) | 25k⭐ = 353 gap | UPDATE 持续 monitoring |
| **ai-boost/awesome-harness-engineering** | 2,762 ⭐ | +5 (R667→R668) | v2.0 NOT released | UPDATE 监测 v2.0 |
| **alirezarezvani/claude-skills** | 20,461 ⭐ | +37 (R664→R668) | 20k⭐ 已过 | UPDATE R668 monitoring |
| **coreyhaines31/marketingskills** | **36,347 ⭐** | **首次发现** | 35k⭐ 已过 | **R668 NEW PROJECT** |

### 7.2 R668 关键信号

1. **herdr 12k⭐ BREAK 临界**：R667 时 97 gap → R668 时 **50 gap**，R668 likely BREAK（持续增长 +47/2h）
2. **planning-with-files 25k⭐ BREAK 临界**：R667 时 378 gap → R668 时 **353 gap**，R668-R670 likely BREAK（持续增长 +25/2h）
3. **gastown 17k⭐ BREAK 临界**：R667 时 690 gap → R668 时 **670 gap**，R668-R672 likely BREAK
4. **taste-skill 60k⭐ BREAK 临界**：R667 时 2,778 gap → R668 时 **2,697 gap**，R672-R680 likely BREAK
5. **awesome-harness-engineering v2.0 NOT released**：R667 时 2,757 ⭐ → R668 时 2,762 ⭐，持续监测
6. **marketingskills 36.3k ⭐ NEW**：首次发现，**R668 NEW PROJECT**

### 7.3 R668 选题决策的关联性

R668 选题「Layer 3 Skill Registry Primitive deep dive」与监测信号的关联：

- **alirezarezvani/claude-skills 20.4k ⭐**：Layer 3.2 Skill Registry 实现层实证
- **marketingskills 36.3k ⭐ NEW**：Layer 3.3 Skill Library 内容层实证
- **taste-skill 57.3k ⭐**：Layer 3.3 Skill Library 内容层垂直（设计去 AI 味）实证
- **gastownhall/gastown 16.3k ⭐**：Layer 2 Orchestrator，与 Layer 3 通过 Bead-ID → Skill-Name 契约联动
- **herdr 11.95k ⭐**：Layer 1 Multiplexer，与 Layer 3 通过 Pane-ID → Skill-Loaded-Status 契约联动
- **planning-with-files 24.6k ⭐**：Layer 4 State/Memory，与 Layer 3 通过 Skill-Completion → Markdown-Checklist 契约联动
- **awesome-harness-engineering 2.76k ⭐**：v2.0 应采纳 R668 Layer 3 三子层修正建议

**主题关联度 100%**：所有监测项目与 R668 文章主题直接相关。

---

## 八、给读者的行动启示

### 8.1 如果你正在设计 Skill Registry

**R668 Layer 3 三子层设计原则**：

1. **协议中立**（Layer 3.1）：用 SKILL.md + agentskills.io 标准，不要发明私有格式
2. **跨 Control Plane 同步**（Layer 3.2）：支持 BYO-sync tier，让各 Control Plane 自己写 sync 脚本
3. **垂直 vs 通用双模式**（Layer 3.3）：不要假设只有一个 Skill Library，要支持通用 + 垂直 + 自建三模式并存

### 8.2 如果你正在选 Skill Registry 框架

**判断清单**：

1. 它实现 Layer 3 哪个子层？（3.1 Spec / 3.2 Registry / 3.3 Library）
2. 它的 Layer 3.1-3.3 是否都支持？（任何一子层缺失会成为瓶颈）
3. 它是否支持 SKILL.md agentskills.io 标准？（不要选私有格式）
4. 它的跨 Control Plane 同步机制是什么？（native / BYO-sync tier）
5. 它的 License 是什么？（marketingskills = MIT，alirezarezvani = MIT，anthropics/skills = Apache 2.0）

### 8.3 如果你正在为 Agent 写 Skill

**R668 Skill 写作原则**：

1. **YAML frontmatter 必填**：`name` + `description` 必须清晰
2. **Markdown body 用自然语言**：不要写 `.py` 代码片段，让 Agent 自己生成
3. **触发条件写在 description**：用「When the user wants to do X, use this skill」句式
4. **工作流写步骤**：1/2/3 步骤让 Agent 能逐步执行
5. **互相 cross-reference**：在 Related Skills 章节引用其他 Skills

### 8.4 如果你正在维护 awesome-harness-engineering v2.0

**R668 v2.0 修正建议**：

- 在 README 增加 **"Multi-Agent Stack Layer 3 三子层"** 章节
- 在 v2.0 Primitives 列表中将 Skill Registry Primitive 拆分为 3 个子 Primitive
- 引用 alirezarezvani/claude-skills + marketingskills + taste-skill + agentskills.io 作为 3 子层的 evidence-based examples
- 在 v2.0 Cross-Dimension 章节中新增 **Layer 3 Cross-Sub-Layer Contract**

---

## 九、结论

R668 的核心发现：

> **Skill Registry 不是单一 Primitive，是「Skills Spec + Skill Registry + Skill Library」3 子层**。

R667 的 6 Layer 模型在 Layer 3 上不够精细化。R668 通过 marketingskills 36.3k ⭐ + alirezarezvani/claude-skills 20.4k ⭐ + agentskills.io 标准形成的证据链，证明 Layer 3 必须细分为 3 子层。

**Layer 3 三子层的核心洞察**：

1. **Skills Spec (协议层)** = Markdown + YAML frontmatter + agentskills.io 标准（机器可读 + 人类可写）
2. **Skill Registry (实现层)** = 跨 13+ Control Plane 同步 + BYO-sync tier + 协议中立（alirezarezvani/claude-skills）
3. **Skill Library (内容层)** = 垂直深挖 + 互相依赖工作流图 + 跨 Control Plane 通用（marketingskills 36.3k ⭐ + taste-skill 57.3k ⭐）

**给 awesome-harness-engineering v2.0 的进一步修正建议**：

> Skill Registry Primitive → 拆分为 3 个 Sub-Primitive：Skills Spec + Skill Registry + Skill Library

**R669 监测重点**：

- herdr 12k⭐ BREAK（50⭐ gap R668 likely BREAK）
- planning-with-files 25k⭐ BREAK（353⭐ gap R668-R670 likely BREAK）
- gastown 17k⭐ BREAK（670⭐ gap R668-R672 likely BREAK）
- awesome-harness-engineering v2.0 release + R668 Layer 3 三子层修正建议采纳
- Layer 3.1 Skills Spec 是否被 1st-party 采纳（agentskills.io 标准化）

---

## 来源清单

1. [agentskills.io Agent Skills Spec](https://agentskills.io/) — Layer 3.1 Skills Spec 协议层标准
2. [coreyhaines31/marketingskills GitHub README](https://github.com/coreyhaines31/marketingskills) — **36,347 ⭐ MIT** Layer 3.3 Skill Library 垂直（营销）实证
3. [coreyhaines31/marketingskills AGENTS.md](https://github.com/coreyhaines31/marketingskills/blob/main/AGENTS.md) — Skill 工作流图详细说明
4. [alirezarezvani/claude-skills GitHub README](https://github.com/alirezarezvani/claude-skills) — 20,461 ⭐ MIT Layer 3.2 Skill Registry 跨 13 Control Plane 实证
5. [alirezarezvani/claude-skills Hermes BYO-sync tier 脚注](https://github.com/alirezarezvani/claude-skills#readme) — BYO-sync tier 跨平台同步机制
6. [alirezarezvani/claude-skills Mistral Vibe BYO-sync tier 脚注](https://github.com/alirezarezvani/claude-skills#readme) — BYO-sync tier 跨平台同步机制
7. [Leonxlnx/taste-skill GitHub README](https://github.com/Leonxlnx/taste-skill) — 57,303 ⭐ MIT Layer 3.3 Skill Library 垂直（设计去 AI 味）实证
8. [gastownhall/gastown GitHub README v1.2.1](https://github.com/gastownhall/gastown) — 16,330 ⭐ MIT Layer 2 Orchestrator + 与 Layer 3 契约
9. [ogulcancelik/herdr GitHub README](https://github.com/ogulcancelik/herdr) — 11,950 ⭐ AGPL-3.0 Layer 1 Multiplexer + 与 Layer 3 契约
10. [OthmanAdi/planning-with-files GitHub](https://github.com/OthmanAdi/planning-with-files) — 24,647 ⭐ MIT Layer 4 State/Memory + 与 Layer 3 契约
11. [ai-boost/awesome-harness-engineering GitHub](https://github.com/ai-boost/awesome-harness-engineering) — 2,762 ⭐ v2.0 NOT released R668 监测目标
12. [R667 multi-agent-stack-r667 deep dive](../orchestration/multi-agent-stack-r667-harness-protocolization-empirical-layering-2026.md) — 6 Layer + 5 Cross-Layer Contract 分层模型起源
13. [R666 gastown multi-agent orchestration deep dive](../orchestration/gastown-multi-agent-orchestration-deep-dive-r666-harness-protocolization-extension-2026.md) — Multi-Agent Orchestration Primitive 起源
14. [R662 harness horizontal 解耦 deep dive](../deep-dives/harness-horizontal-decoupling-skill-portability-across-control-planes-2026.md) — Skill 协议中立性起源
15. [R665 meta synthesis + Planning Primitive](../deep-dives/harness-protocolization-r661-r664-meta-synthesis-planning-primitive-v2-prediction-2026.md) — Planning Primitive 起源
16. [R661 overview meta article](../deep-dives/awesome-harness-engineering-three-dimensions-protocolization-2026.md) — harness 协议化三维度体系起源
17. [anthropics/skills GitHub](https://github.com/anthropics/skills) — 153k ⭐ Anthropic 官方 Skill Layer 3.1 协议层样板
18. [agentskills.io](https://agentskills.io/) — Skills Spec 标准来源
19. [YAML frontmatter standard](https://yaml.org/spec/1.2/spec.html) — Skills Spec YAML 格式标准

---

**R668 实证结论**：Layer 3 Skill Registry Primitive 必须细分为 3 子层（Skills Spec + Skill Registry + Skill Library）。R667 的 6 Layer + 5 Cross-Layer Contract 模型在 Layer 3 上不够精细，R668 通过 marketingskills 36.3k ⭐ + alirezarezvani/claude-skills 20.4k ⭐ + agentskills.io 标准形成完整证据链。

**R668 修正建议**：awesome-harness-engineering v2.0 应将 Skill Registry Primitive 拆分为 3 个 Sub-Primitive：Skills Spec + Skill Registry + Skill Library。

**R669 监测重点**：herdr 12k⭐ BREAK + planning-with-files 25k⭐ BREAK + gastown 17k⭐ BREAK + awesome-harness-engineering v2.0 release + Layer 3.1 Skills Spec 1st-party 采纳监测。