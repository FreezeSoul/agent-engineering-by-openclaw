# runkids/skillshare 跨 AI 工具 Skill 团队 2026

> 当 60+ AI CLI 工具各自维护一份 skills/ 目录时，**团队级单一事实源是部署速度的瓶颈**

---

## 核心命题

**runkids/skillshare** 是一个 Go 编写的 CLI 工具，**解决 AI Coding 工具在团队规模化部署中的"配置碎片化"问题**。它把 skills、agents、rules、commands 等 AI 资源集中到一个"Source Directory"（`~/.config/skillshare/`），然后通过 `skillshare sync` 一次命令同步到 Claude Code、Cursor、Codex、OpenClaw、OpenCode 等 60+ 目标工具。

这个项目的工程意义在于它把 Anthropic 团队规模化文章中提到的「**CLAUDE.md 团队级共享**」和「**Super Users 组建立知识库**」这些**理念**——落地成了**可执行的具体工具**。在没有 skillshare 之前，团队要部署 60+ 工具的共享 skills 通常需要维护 60+ 份重复文件；有了 skillshare，**一份 SKILL.md 就能同步到所有目标**。

> "One source of truth for AI CLI skills, agents, rules, commands & more. Sync everywhere with one command — from personal to organization-wide."
> — [runkids/skillshare README](https://github.com/runkids/skillshare) (v0.20.0, MIT, 2,234⭐)

---

## 为什么这是 Agentic Coding 团队规模化的关键工具

### 解决了 Anthropic 文章中的具体痛点

Anthropic 在 [How to scale agentic coding](https://claude.com/blog/scaling-agentic-coding) 一文中给团队部署 Agentic Coding 的核心建议是：

1. **20-50 人 Super Users 试点**
2. **创建自定义 slash command、CLAUDE.md、可复用认证脚本**
3. **共享项目级 CLAUDE.md（团队规范）**
4. **跨工具使用**（Claude Code + Cursor + Codex 等混合部署）

**第 2-4 条都涉及"同一份资产要在多个工具目录中重复维护"**——这正是 skillshare 解决的核心问题。

### 团队级单一事实源（SSOT）

skillshare 的目录结构：

```
~/.config/skillshare/
├── skills/      ← SKILL.md 文件
├── agents/      ← agent 定义
├── extras/      ← rules, commands 等
```

**`skillshare sync` 一次命令**把这些资源转换并分发到所有目标的本地 skills/ 目录。对于团队部署，**`skillshare` 进一步支持**：

- **项目级 skills**（`.skillshare/` 目录，跟随仓库）
- **组织级 skills**（通过 tracked repos 共享给全公司）
- **`SKILL.md` targets 字段**（声明这个 skill 同步到哪些目标）

**这意味着**：一个团队 100 个工程师 60+ 工具的部署场景，**维护成本从 100 × 60+ 份 SKILL.md 降到 100 份**。

### 跨工具同步 vs 平台锁定

skillshare 的另一个关键决策是**不绑定单一 AI 平台**。当 Anthropic 推 Claude Code、OpenAI 推 Codex、Cursor 推自己的 format 时，**团队面临"工具碎片化"**——不同工程师用不同工具，每个人维护自己的 skills 目录，**团队知识无法沉淀**。

skillshare 的设计哲学是"**Skills 是 AI 时代的文档格式**"——SKILL.md 是 source of truth，工具是分发渠道。这与 OpenAI、Hermes Agent 等推动的"开放 Agent 标准"方向一致。

---

## 关键技术能力

### 1. 多源支持

```
- GitHub
- GitLab
- Bitbucket
- Azure DevOps
- 任何 self-hosted Git
```

团队可以内部 host skills 仓库，用 skillshare 同步给全公司——这与 Anthropic 文章中"内部 Git 仓库作为知识沉淀"的建议完美契合。

### 2. 安全的 skill 审计

> "Built-in security — audit skills for prompt injection and data exfiltration before use"

**这是 R394 MCP 集成 / R390 AI Organizations Alignment Risks 系列文章一直强调的安全能力**。在企业部署中，**第三方 skill 可能携带 prompt injection 攻击**——skillshare 内置的 audit 机制是防御层。

### 3. 精细的过滤控制

- **`.skillignore`**：类比 `.gitignore`，控制哪些 skill 不分发到哪些目标
- **`SKILL.md` targets 字段**：声明这个 skill 同步到哪些目标
- **per-target include/exclude**：每个工具有自己的白名单/黑名单

**这解决了"Claude Code 用一份 skills，Cursor 用另一份"的工程现实**。

### 4. Extras 扩展机制

v0.20.0 的 **extension transforms** 允许在 sync 时**自动转换格式**——例如 Markdown 格式的 rules 转换为 Gemini TOML commands，Codex TOML agents 等。**一份源格式，多个目标格式**。

### 5. Git root 作用域

v0.20.0 的另一关键特性：**`commit`/`push`/`pull` 支持 skills/agents/extras 单独仓库**——团队可以选择"只把 skills 放进 Git 仓库"、"只把 agents 放进 Git 仓库"或"全部一起"。

---

## 适合使用的场景

| 场景 | 适合度 | 原因 |
|------|--------|------|
| **多 AI 工具团队（Claude Code + Cursor + Codex 混合）** | ⭐⭐⭐⭐⭐ | 单一事实源，一次同步所有目标 |
| **企业内部 AI Coding 推广** | ⭐⭐⭐⭐⭐ | 支持项目级 + 组织级 skills 仓库 |
| **AI Agent 安全敏感团队** | ⭐⭐⭐⭐⭐ | 内置 prompt injection 审计 |
| **多操作系统团队（macOS + Linux + Windows）** | ⭐⭐⭐⭐⭐ | 跨平台 single binary |
| **纯个人使用** | ⭐⭐⭐ | 工具探索期单用户也能用，但价值不如团队级 |

---

## 与仓库中其他项目的关系

| 项目 | 集群 | 关系 |
|------|------|------|
| `farion1231/cc-switch` (R393) | harness | 解决"管理多个 AI CLI 工具"的入口问题 |
| `thedotmack/claude-mem` (R383) | context-memory | 解决"Agent 跨 session 记忆"问题 |
| `VoltAgent/awesome-agent-skills` (R394) | skills | 解决"skills 内容来源"问题 |
| **`runkids/skillshare` (R397)** | **skills + 团队** | **解决"skills 在团队和多工具间分发"问题** |

**四者构成完整的 Agentic Coding 部署栈**：内容来源（awesome-agent-skills）→ 跨工具分发（skillshare）→ 多工具入口（cc-switch）→ 状态持久化（claude-mem）。

---

## Pair 闭环：与 R397 Anthropic 团队规模化文章的 SPM 对位

| Article 命题 | skillshare 实现 |
|-------------|----------------|
| "Begin with a pilot group of 20-50 developers" | `.skillshare/` 项目级 skills 仓库支持小团队起步 |
| "Creating custom slash commands for common tasks" | skillshare `extras/commands/` 统一管理命令 |
| "Building CLAUDE.md files that capture coding standards" | skillshare `extras/rules/` 统一管理规则 |
| "Setting up a dedicated channel for troubleshooting" | skillshare `tracked repos` 作为组织级知识沉淀 |
| "Practical pilot activities include ... repository root" | `.skillshare/` 正是项目根的统一入口 |
| "Treat like documentation: Update CLAUDE.md files when architectural decisions change" | v0.20.0 `git_root scope` 让 skills/agents/extras 可以独立版本化 |

**SPM 字面级命中** ≥ 6 个核心关键词（**pilot / shared / sync / team / project / skills**），**4-way SPM 评分**：

- Layer 1（cluster 共享）✅ — skills + harness cluster
- Layer 2（SPM 关键词字面级）✅ — 6+ 关键词同时命中
- Layer 3（topics target-ecosystem）✅ — `topics: ['openclaw', 'claude-code', 'skills', 'team-management']` 包含 1 个直接命中（openclaw）+ 3 个间接命中
- Layer 4（维度互补）✅ — Article 是"组织流程设计"（闭源 Anthropic 视角），Project 是"工具实现"（开源 Go 工具视角），互为补充

**总评**：⭐⭐⭐⭐⭐ SPM 字面级满中（开放层级 + 生态命中 + 维度互补）

---

## 引用来源

> "One source of truth for AI CLI skills, agents, rules, commands & more. Sync everywhere with one command — from personal to organization-wide. Codex, Claude Code, OpenClaw, OpenCode & 60+ more."
> — [runkids/skillshare README](https://github.com/runkids/skillshare)

> "skillshare fixes this: One source, every agent — sync to Claude, Cursor, Codex & 60+ more with `skillshare sync`. Agent management — sync custom agents alongside skills to agent-capable targets. More than skills — manage rules, commands, prompts & any file-based resource with extras. Team-ready — project skills in `.skillshare/`, org-wide skills via tracked repos. Built-in security — audit skills for prompt injection and data exfiltration before use."
> — [runkids/skillshare README](https://github.com/runkids/skillshare)

---

## 资源

- **GitHub**: https://github.com/runkids/skillshare
- **网站**: https://skillshare.runkids.cc
- **文档**: https://skillshare.runkids.cc/docs
- **License**: MIT
- **Stars**: 2,234⭐ (验证于 2026-06-16 via GitHub API)
- **最新版本**: v0.20.0 (2026-06-15)
