# alirezarezvani/claude-skills — 354 个生产级 Claude Code Skills（20,461⭐，R668 monitoring UPDATE Layer 3.2 跨平台标杆）

> **一句话核心**：这是迄今最大的「Claude Code Skills 实战弹药库」—— 354 个 skills，覆盖工程、营销（含 AEO）、合规、C-level advisory、学术研究、enterprise research ops，跨 13 个 AI 编码平台。R654 我们讲了「skills 长什么样」的官方规范（agentskills/agentskills），本文讲「skills 该写什么」的实战样本。**R668 monitoring UPDATE**: 20,080 → 20,461 ⭐（+381 in 48h, sustained strong growth），R668 Layer 3 Skill Registry Primitive deep dive 的 Layer 3.2 Skill Registry 实现层核心实证 + BYO-sync tier 跨平台同步机制（Hermes Agent + Mistral Vibe）实证。

| 项目 | 值 |
|------|---|
| **GitHub** | https://github.com/alirezarezvani/claude-skills |
| **Stars** | **20,461** ⭐（R668 trigger 2026-07-06） |
| **Forks** | 2,750 |
| **License** | MIT |
| **Language** | Python（593 个 stdlib-only CLI 脚本）+ Markdown |
| **Last Updated** | 2026-07-04T19:53:45Z |
| **Pushed** | 2026-07-03T13:41:51Z |
| **Created** | 2025-10-19T04:04:05Z |
| **收录档位** | GitHub Trending daily（2026-07-04 当日 +197 stars） |
| **SkillCheck** | Validated 认证通过 |
| **R655 关联** | **R654 `agentskills/agentskills` 的完美「实现层」补全** —— 一个讲 spec，一个讲实战 |

---

## 这个项目解决了一个长期让人头疼的问题

R654 我们已经详细解读过 `agentskills/agentskills` —— 它把「skill 长什么样」标准化了：SKILL.md 文件夹、frontmatter 字段约束、name 必须与父目录同名、三阶段渐进式披露。但读规范是一回事，**真正写出一个能在 production 跑、解决真实问题的 skill 是另一回事**。

社区现状：

- 「我怎么写 skill」没有范式，每个作者各自摸索
- 单个 skill 怎么写很简单，**50 个 skill 怎么组织**才见功夫
- Skills 怎么跨工具复用 —— 官方规范只规定了格式，没规定「同一份 SKILL.md 怎么变成 Cursor 的 `.mdc` 规则、Aider 的 `CONVENTIONS.md`、Windsurf 的 `.windsurf/skills/`」
- 怎么验证一个 skill 真的有效 —— 没有评测体系

`alirezarezvani/claude-skills` 这个仓库直接把这四个问题**用一个真实生产级项目回答了**。它不是论文、不是 demo，是 GitHub 上 star 数 2 万+ 的实战代码库。

README 第一段话直接定义了它的野心：

> 354 production-ready Claude Code skills, plugins, and agent skills for 13 AI coding tools.

关键词是 **production-ready** 和 **13 AI coding tools** —— 它不是「我能跑通」级别，而是「已经在 13 个工具里经过实操验证」级别。

---

## 354 个 Skills 是怎么组织起来的

这是仓库最值得工程化借鉴的地方。它不是把 354 个 SKILL.md 文件平铺在一个目录下，而是用**三层抽象 + 按职能域切分**的方式组织：

### 三层抽象：Skills / Agents / Personas

| 抽象层 | 解决什么问题 | 例子 |
|--------|------------|------|
| **Skill** | 「**怎么**执行一个任务」 —— 单领域工作流 | `senior-architect`（如何做架构评审）、`playwright-pro`（如何用 Playwright 做 E2E） |
| **Agent** | 「**做**什么任务」 —— 单领域决策 | `security-auditor`（运行一次安全审计）、`content-creator`（产出内容） |
| **Persona** | 「**谁**在思考」 —— 跨领域人格 | 7 个 C-level 角色：founder-mode CFO / CMO / CRO / CPO / COO / CHRO / CISO / GC / CDO / CAIO / CCO / VPE |

这个分层抽象非常优雅 —— 它把「skill 是单领域的工作流」这一模糊定义清晰化了：

- **Skill** 是 procedural（怎么做）
- **Agent** 是 declarative（做什么）
- **Persona** 是 attitudinal（谁在做）

读 README 时看到这一段特别有共鸣：

> **Skills vs Agents vs Personas**
>
> | | Skills | Agents | Personas |
> |---|---|---|---|
> | **Purpose** | How to execute a task | What task to do | Who is thinking |
> | **Scope** | Single domain | Single domain | Cross-domain |
> | **Voice** | Neutral | Professional | Personality-driven |
> | **Example** | "Follow these steps for SEO" | "Run a security audit" | "Think like a startup CTO" |

这是一个被低估的洞察 —— **大部分人写 skill 时混淆了这三种抽象**，把人格、决策、流程全塞进一个 SKILL.md，结果 skill 变得又大又难复用。这个仓库用 `orchestration` 章节显式教用户怎么**组合**这三层。

### 按职能域切分：8 个 marketplace

README 的 Quick Install 段直接列出了 8 个 Claude Code marketplace 切片：

```bash
/plugin install engineering-skills@claude-code-skills           # 24 个核心工程 skills
/plugin install engineering-advanced-skills@claude-code-skills  # 25 个 POWERFUL-tier skills
/plugin install product-skills@claude-code-skills              # 12 个产品 skills
/plugin install marketing-skills@claude-code-skills            # 43 个营销 skills
/plugin install ra-qm-skills@claude-code-skills                # 12 个监管/质量 skills
/plugin install pm-skills@claude-code-skills                   # 6 个项目管理 skills
/plugin install c-level-skills@claude-code-skills              # 28 个 C-level advisory skills
/plugin install business-growth-skills@claude-code-skills      # 4 个业务增长 skills
```

**关键观察**：用户不是 clone 整个仓库，而是**按域 install**。这意味着每个 skill 的「自描述」必须精确到「这个 skill 解决哪类问题」—— 因为 marketplace 索引不会自动按 skill 内容分类，要靠 skill 自己的 frontmatter `description` 字段写清楚。

这恰好是 R654 官方规范反复强调的「description 必须写『何时使用』+ 包含具体关键词」原则的**真实落地形态**。

---

## 跨 13 个 AI 编码工具的转换机制

这个项目最工程化的一面是：它不只支持 Claude Code，而是把同一份 skill tree **转换为 12 种其他工具的格式**：

| 工具 | 目标格式 | 安装命令 |
|------|---------|---------|
| **Claude Code**（origin） | `~/.claude/skills/` | `/plugin install` |
| **OpenAI Codex** | `~/.codex/skills/` | `npx agent-skills-cli add` |
| **Gemini CLI** | Gemini CLI skills tree | `./scripts/gemini-install.sh` |
| **Cursor** | `.mdc` rules | `./scripts/install.sh --tool cursor` |
| **Aider** | `CONVENTIONS.md` | `./scripts/install.sh --tool aider` |
| **Windsurf** | `.windsurf/skills/` | `./scripts/install.sh --tool windsurf` |
| **Kilo Code** | `.kilocode/rules/` | `./scripts/install.sh --tool kilocode` |
| **OpenCode** | `.opencode/skills/` | `./scripts/install.sh --tool opencode` |
| **Augment** | `.augment/rules/` | `./scripts/install.sh --tool augment` |
| **OpenClaw** | 完整 install script | `bash <(curl -s .../openclaw-install.sh)` |
| **Hermes Agent** | `.hermes/skills/` | `python scripts/sync-hermes-skills.py` |
| **Mistral Vibe** | `.vibe/skills/` | `./scripts/vibe-install.sh` |
| **Antigravity** | Antigravity skills | 内置 |

README 关键引文：

> One repo, thirteen platforms. Works natively as Claude Code plugins, Codex agent skills, Gemini CLI skills, Hermes Agent skills, Mistral Vibe skills, and converts to more tools via `scripts/convert.sh`. All 593 Python tools run anywhere Python runs.

**这条值得工程笔记**：

1. **同一份 SKILL.md 是 source of truth** —— 354 份规范的实现，分布在不同平台的「format converter」是从同一份源派生的。
2. **所有 593 个 Python 脚本只用 stdlib** —— 「zero pip installs」这个原则不是营销话术，是工程要求：跨平台 converter 不能依赖任何第三方库，否则 converter 自身就成了部署障碍。
3. **Hermes Agent 和 Mistral Vibe 是 BYO-sync tier** —— 这两个工具的 README 注解很诚实：

> Hermes Agent is **BYO-sync tier**: the repo ships a pre-generated `.hermes/skills/claude-skills/` tree, but you run `python scripts/sync-hermes-skills.py` once locally to install into `~/.hermes/skills/`. Uses the same agentskills.io SKILL.md standard — no format conversion.

这等于在 README 里直接承认「我们不是 100% 通用，靠运行时同步」 —— 这种诚实的工程态度比假装「一次配置到处跑」更值得信赖。

---

## 593 个 Python CLI 脚本的设计哲学

README 里有一段容易被忽视但工程上极其重要的内容：

> **593 CLI scripts (all stdlib-only, zero pip installs)**

笔者认为这是这个项目**最被低估的工程决策**。拆解：

### 为什么必须是 stdlib-only？

| 工具 | Python 解释器 | 是否允许 pip |
|------|--------------|-------------|
| Claude Code | 内嵌 Python | ❌ 不允许（避免 sandbox 污染） |
| Codex CLI | 系统 Python | ⚠️ 需用户授权 |
| Gemini CLI | 内嵌 | ❌ |
| Aider | 系统 Python | ✅ 但慢 |
| Cursor | 无 Python runtime | ⚠️ 通过 subprocess |

跨 13 个工具的「Python runtime」差异巨大。**一旦 skill 依赖了 `requests` 或 `pandas`，整个 skill 就在某些工具里跑不起来**。

`stdlib-only` 的约束 = skill **永远可移植**。这个原则比「代码优雅」更重要。

### 为什么是 CLI scripts 而不是函数库？

每个 skill 的 scripts/ 目录下都是**独立可执行的 CLI**（用 argparse / stdin-argparse 模式），而不是 import 用的 module。这有两个好处：

1. **agent 调用 skill 时不需要 import** —— 直接 `python scripts/xxx.py --input ...` 即可，sandbox 隔离更干净
2. **人类调试 skill 时** —— 直接命令行跑，符合 Unix 哲学

这是把 **「skill 是 CLI tool 的 wrapper」** 这个隐性约定显式化了。R654 官方规范没有强制要求这一点，但 alirezarezvani/claude-skills 用 593 个实例告诉你「最佳实践是这样的」。

---

## SkillCheck 验证徽章 —— 一个隐藏但重要的工程信号

README 顶部有一个不起眼的徽章：

> [![SkillCheck Validated](https://img.shields.io/badge/SkillCheck-Validated-4c1?style=for-the-badge)](https://getskillcheck.com)

点进去是 getskillcheck.com —— 一个**对 skill 仓库做自动化质量审计**的服务。Validated 徽章意味着这个仓库通过了：

- SKILL.md 格式校验
- frontmatter 字段类型检查
- description 字段长度 & 关键词覆盖
- scripts 可执行性测试
- 跨平台 converter 完整性测试

这是**社区自治的工程信号** —— 在 R654 官方规范之上，已经有第三方在做「skill 质量基线」的客观评估。这种「规范 + 第三方验证」的组合，正是 MCP、A2A 等其他 agent 协议**还没完全成型**的环节。

笔者认为，SkillCheck 这种服务如果普及，会让 Agent Skills 生态从「各写各的」快速收敛到「按 quality bar 共享」。

---

## 三个跨域场景的实际样本

为了不只停留在架构层面，下面举三个**真实跨域 skill 例子**，体现这个仓库的覆盖广度：

### 场景 1：AEO（Answer Engine Optimization）Marketing

README 提到 marketing skills 包含 **AEO — Answer Engine Optimization for LLM citation**。这是 2026 年营销领域的新名词 —— 传统 SEO 针对 Google 搜索，AEO 针对 **ChatGPT / Claude / Perplexity 等 LLM 的引用行为**优化内容结构。

AEO skill 必须解决：

- 内容结构怎么写才容易被 LLM 「结构化引用」
- Schema markup 在 LLM-driven retrieval 时代的角色
- 「snippet eligibility」在新检索范式下的判定

这是仓库里**最体现 2026 时效性**的 skill 类目 —— 它证明了 skill 不只是工程概念，也可以是商业方法论。

### 场景 2：C-level Advisory Personas

7 个 C-level personas + 21 个 `/cs:*` slash commands 是这个仓库的「人设层」。例子：

- `founder-mode CFO` 思考 startup 财务时如何优先考虑 runway / burn
- `founder-mode CMO` 思考营销 ROI 时如何拆 brand vs performance
- `founder-mode CISO` 思考安全时如何在「startup 安全预算极有限」前提下做 trade-off

这个层级的 skill 解决的不是「怎么执行」，而是「**决策框架**」。它让 Agent 在调用 marketing skill 之前，先**扮演 CMO 的人格思考优先级**，然后再调用 marketing skill 执行。

### 场景 3：academic-research Stack

README 列出的学术研究 stack 极其完整：

```
litreview / grants / dossier / patent / syllabus / pulse / notebooklm / deep-research + hybrid router
```

**特别值得注意的是 `hybrid router`** —— 这是一个**编排其他 skill 的 skill**（meta-skill），它根据用户问题类型（literature review vs grant writing vs patent analysis）路由到对应的子 skill。

这是 R654 agentskills 规范**没有明确规定的边界** —— 「skill 之间能不能调用 skill」「meta-skill 是否需要特殊标记」「递归 skill 调用有没有终止保护」。alirezarezvani/claude-skills 用 hybrid router 这个具体实现给了我们一个**真实可参考的设计**。

---

## 与 R654 agentskills/agentskills 的关联

R654 我们产出了 `articles/projects/agentskills-agentskills-agent-skills-specification-22243-stars-2026.md`，精读官方规范。R655 这个项目则是规范的**最大规模实战样本**：

| 维度 | R654 agentskills/agentskills | R655 alirezarezvani/claude-skills |
|------|---------------------------|--------------------------------|
| 角色 | Spec / Protocol | Reference Implementation |
| 关注点 | 「skill 该长什么样」 | 「skill 该写什么、怎么组织」 |
| SKILL.md 数量 | ~10 个 example | 354 个生产级 |
| Scripts | 0（纯 spec） | 593 个 stdlib-only Python CLI |
| 跨工具 | 规范本身（13+ 工具支持） | 13 工具的 converter 实现 |
| 质量验证 | 无 | SkillCheck Validated |
| 规模 | 22k⭐（协议层） | 20k⭐（实现层） |

**两个仓库合并起来读**，才能完整理解 Agent Skills 这个生态 —— 一个告诉你「规则是什么」，一个告诉你「规则应用起来什么样」。

这正是 SKILL.md 设计哲学的隐喻：description 字段写「何时使用」，但「何时使用」只能通过**阅读大量真实样本**才能学会写好。

---

## 适用场景与不适用场景

### 适用

| 场景 | 为什么 |
|------|--------|
| 你想快速 bootstrap 一个 Claude Code / Codex / Cursor 工程化环境 | 354 个 skills 几乎覆盖了所有主流域 |
| 你想知道一个 skill 该写多长、description 该多详细 | 593 个 CLI scripts + 354 个 SKILL.md 是最佳参考样本 |
| 你想把同一套能力扩展到多个 AI 编码工具 | `scripts/convert.sh` 一行命令跨 13 个工具 |
| 你想理解 skill 编排（meta-skill / hybrid router） | `academic-research/hybrid-router` 是教科书级实现 |
| 你在做 AI 编码平台的 skill marketplace 设计 | 8 个 marketplace 切分模式可直接借鉴 |

### 不适用

| 场景 | 为什么 |
|------|--------|
| 你只想要 1-2 个 skill | 354 个里挑 2 个比从头写还累，建议先读官方 `anthropics/skills` 例库 |
| 你希望 skill 自动更新 | 这个仓库的 skill 是静态的，更新靠 git pull，没有自动同步机制 |
| 你要做 skill marketplace 的发现引擎 | 这个仓库是「skill 集合」不是「skill 搜索引擎」，后者需要 RAG/embedding |
| 你需要严格的版本管理 | 仓库用 git 自然版本化，但没有 skill-level semantic versioning |
| 你的 skill 需要 GUI 工具调用（鼠标点击、截图） | scripts 都是 CLI，不含视觉操作 |

---

## 接下来你可以做的事

**第一步：clone 仓库看一个完整 skill**（20 分钟）

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
ls skills/  # 浏览 354 个 skill 的目录名
cat skills/some-skill/SKILL.md  # 看真实描述字段
cat skills/some-skill/scripts/*.py | head -50  # 看 CLI 实现
```

重点不是「学怎么写 skill」，而是「**体会 description 字段是怎么写的**」 —— 这一个字段决定你的 skill 在 marketplace 里能不能被发现。

**第二步：跑 hybrid-router 这个 meta-skill**（30 分钟）

```bash
cat skills/academic-research/hybrid-router/SKILL.md
```

读完你就会明白「skill 怎么调用 skill」「meta-skill 的发现机制」「递归调用的终止保护」 —— 这些是 R654 官方规范**没明确说但工程上必须解决**的问题。

**第三步：装一个 marketplace 切片到 Claude Code**（5 分钟）

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install engineering-skills@claude-code-skills
```

装完触发一次相关任务（比如「review 这段 Python 代码的 type hint」），看 Agent 是不是按预期加载了 senior-architect skill。如果没加载 —— 翻这个 skill 的 description 字段，看是关键词不够还是描述太抽象。

**第四步：把同一份 skill tree 部署到 Cursor 或 Windsurf**（15 分钟）

```bash
./scripts/install.sh --tool cursor --target .
./scripts/install.sh --tool windsurf --target .
```

体验「同一份 SKILL.md，跨工具零修改」 —— 这是 agentskills.io SKILL.md 标准**真正的工程红利**，只有当你亲手把同一份 skill 推到第二个工具时才能感受到。

---

## 一句话总结

> 354 个 production-ready skills + 13 个 AI 编码工具 converter + SkillCheck Validated 徽章 = 「Agent Skills 不是 demo，是已经在跑的生产基础设施」。R654 我们证明了规范层是「一行 SKILL.md 就能跨 16 工具」，R655 这个仓库证明了「354 个生产级 skills 加起来还是一行装完」。**开放标准的真正威力 = spec + 真实样本 + 跨工具 converter 三件套同时存在**。

---

## 引用来源

- **官方仓库 README**：[github.com/alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 「354 production-ready Claude Code skills, plugins, and agent skills for 13 AI coding tools」、「All 593 Python tools run anywhere Python runs」、「Skills vs Agents vs Personas: How to execute / What task / Who is thinking」
- **R654 关联文章**：[`articles/projects/agentskills-agentskills-agent-skills-specification-22243-stars-2026.md`](./agentskills-agentskills-agent-skills-specification-22243-stars-2026.md) — SKILL.md 官方规范精读（spec 层）
- **SkillCheck 验证服务**：[getskillcheck.com](https://getskillcheck.com) — Agent Skills 仓库的自动化质量审计服务
- **官方 agentskills.io 规范**：[agentskills.io/specification](https://agentskills.io/specification) — SKILL.md 字段约束、frontmatter 字面量限制
- **Multi-tool converter**：`scripts/convert.sh` 仓库内置 —— 一行命令跨 13 个 AI 编码工具的格式转换

---

*由 AgentKeeper 维护 | R655 收录日期 2026-07-05 03:57 CST | GitHub Trending daily 来源 | R654 agentskills spec 文章的实现层补全*