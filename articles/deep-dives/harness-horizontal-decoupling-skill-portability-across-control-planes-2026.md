# harness 协议化三维度体系 — horizontal 解耦 deep dive：Skill 协议中立与多 control plane 可移植

> **关联文章**: [awesome-harness-engineering-three-dimensions-protocolization-2026](./awesome-harness-engineering-three-dimensions-protocolization-2026.md)（R661，三维度体系 overview）
>
> **本文定位**：三维度体系 overview 之后的第一篇 single-dimension deep dive，聚焦 **horizontal 解耦** —— 即「一个 Skill 同时被多个 control plane 调度」背后的协议中立性、可移植性、迁移工程实践。
>
> **核心论点**：harness horizontal 解耦已经从「大多数 Skill 锁死在 control plane A」演化到「Skill 协议中立、control plane 可替换、execution plane 可替换」三件套 —— [agentskills/agentskills](https://github.com/agentskills/agentskills) 22k⭐ 把 SKILL.md 这个最小公约数固化成了 vendor-neutral 协议，[xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) 9,881 ⭐ 19 个 Skill 已经在 Claude Code + Codex 双 control plane 跑通，而 [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) 20,281 ⭐ 直接承诺兼容 13 个 control plane。这不是「多写一个适配器」的故事，而是「以 SKILL.md 为接口契约的跨 control plane 编译期/运行期兼容」的故事。

---

## 一、为什么 horizontal 解耦单独成文

R661 提纲挈领地把 harness 协议化拆成了 vertical / horizontal / cross-device 三个维度，但每个维度都值得一篇 deep dive。本文聚焦 horizontal 解耦，原因有三：

1. **可移植性是当下最热门的问题**：Anthropic → OpenAI → Cursor → Gemini CLI → 自建 control plane，每多一个 control plane 都面临「Skills 怎么办」的复盘。
2. **SKILL.md 已经成为事实标准**：agentskills/agentskills 22k⭐ 仓库托管的不是「某个 control plane 的 Skill」而是「跨 control plane 的 Skill 规范」。这意味着 Skill 层的协议中立性已经发生。
3. **实战案例已经成熟**：xbtlin/ai-berkshire 9,881 ⭐ 这一周就涨了 5,876 ⭐（+147%），19 个 Skill 在 Claude Code + Codex 双 control plane 实盘跑通两年（2024 实盘 +69.29%，2025 实盘 +66.38%）。这不是「PoC」而是「能挣钱的 PoC」。

## 二、horizontal 解耦的最小公约数：SKILL.md 到底是什么

[agentskills/agentskills](https://github.com/agentskills/agentskills) README 直接给出 SKILL.md 的最小结构：

```
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

SKILL.md 的 frontmatter 至少包含 `name` + `description`，正文是给 agent 看的 markdown instructions。Agent 通过「渐进式披露（progressive disclosure）」在三个阶段加载：

| 阶段 | 触发 | 加载内容 | Context 成本 |
|------|------|---------|-------------|
| Discovery | Agent 启动 | `name` + `description`（每个 Skill） | 几十 tokens/Skill |
| Activation | 任务匹配 `description` 关键词 | 完整 `SKILL.md` 正文 | 数百 tokens/Skill |
| Execution | Skill 内指令触发 | `scripts/` / `references/` / `assets/` | 按需 |

要点：**SKILL.md 不是某个 control plane 的私有发明**，而是 Anthropic 在 2025 年 4 月 [equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) 一文中公开出来的开放规范，后被 Cross-vendor 标准化组织托管到 agentskills/agentskills（22,438 ⭐ Apache-2.0 + CC-BY-4.0）。

**为什么这个最小结构足够让 horizontal 解耦成立**：

- control plane 不需要关心 Skill 的内部 workflow，只要发现 `name` + `description` 就能纳入候选；
- Skill 不需要关心 control plane 的内部状态，只要 `SKILL.md` 的语义清晰就能被多种 control plane 复用；
- 这是「接口契约中立」而非「实现中立」—— Skill 可以用 Python 脚本、bash、HTML 模板、Rust 二进制，但只要组织成 SKILL.md + 资源目录的形式，control plane 就能调度。

## 三、horizontal 解耦的协议层：agentskills.io/specification 强制了什么

[agentskills.io/specification](https://agentskills.io/specification) 是与 GitHub README 配套的规范网站，其核心结构（前两节）：

### 3.1 Frontmatter Schema（YAML 在 `---` 之间）

```yaml
---
name: skill-name              # required, kebab-case, ≤64 chars
description: >                # required, ≤1024 chars
  What this skill does and when the agent should use it.
license: Apache-2.0           # optional but recommended
allowed-tools: Bash Read       # optional, restricts execution plane tool list
---
```

### 3.2 Body（markdown 指令正文）

- 第一人称或第二人称告诉 agent 「你怎么做什么」
- 可以调用 `scripts/`、`references/`、`assets/`
- 可以分段、列表、表格、代码块
- **不能依赖 control plane 特定功能**（如 Claude Code 的 `~/.claude.json` 字段、Codex CLI 的 `[features]` 配置块）

这条「不能依赖 control plane 特定功能」是 horizontal 解耦成立的根本约束：SKILL.md 是跨 vendor 接口契约，不是某一家 control plane 的配置文件。

### 3.3 Progressive Disclosure 三阶段的具体实现

| 阶段 | Discovery | Activation | Execution |
|------|-----------|------------|-----------|
| Claude Code | 把每个 Skill 的 `name` + `description` 注册到 ~/.claude/skills/ 的 metadata 索引 | 任务匹配时 `Read` SKILL.md 全文 | 按需调用 scripts/ bash + reference `Read` |
| Codex CLI | 把每个 Skill 的 `name` + `description` 注册到 ~/.codex/skills/ 的 metadata 索引 | 任务匹配时 `cat` SKILL.md 全文 | 按需 bash + read_file |
| Gemini CLI | 同理 | 同理 | 同理 |

三个 control plane 在 SKILL.md 这一层是 100% 等价的实现。差异只发生在「Skill 内的脚本如何调用」和「Skill 内如何引用 context」这两层。

## 四、horizontal 解耦的实战案例：xbtlin/ai-berkshire 双 control plane 跑通两年

[xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) 9,881 ⭐（R660 时 4,005 ⭐ → R662 9,881 ⭐ +147% in 7 天）是 horizontal 解耦最有说服力的实证。仓库 README 第一句话：

> AI Berkshire 是一套**同时兼容 Claude Code 与 Codex** 的投资研究 Skill 合集……一个人 + Claude Code / Codex = 一个投研团队。

### 4.1 三层架构（Skill 层 + Agent 层 + 工具层）

仓库 README 的「设计理念」部分把架构拆成三层：

| 层 | 职责 | 解耦维度 |
|----|------|---------|
| **Skill 层** | 把「你要做什么」抽象成 19 个明确入口 —— 深度研究 / 财报分析 / 行业筛选 / 持仓管理 / 思维工具 | horizontal 解耦的核心（19 个 Skill 同属 Claude Code + Codex） |
| **Agent 层** | 每个 Skill 内部都是 4 个 Agent 并行 —— 它们各自独立搜索、独立判断、互相挑战，最后由 Team Lead 综合 | control plane 内多 agent orchestration |
| **工具层** | 精确计算 / 实时检索 / 报告抽检 —— 保证每份报告的数据严谨性可验证 | execution plane 工具调用 |

### 4.2 19 个 Skill 全部双 control plane 可移植

xbtlin/ai-berkshire 把这 19 个 Skill 分了 5 类，每一类都有明确的 Claude Code + Codex 双 control plane 对应路径：

| 类别 | Skill 数量 | 代表 Skill | 关键能力 |
|------|---------|-----------|---------|
| 深度研究类 | 5 | `/investment-research`（四大师综合）/ `/investment-team`（多 Agent 并行） | 投资研究 Skill 抽象 |
| 财报分析类 | 2 | `/earnings-review`（一手资料）/ `/earnings-team`（多 Agent + 发布文章） | 财报精读 |
| 行业筛选类 | 6 | `/industry-research`（产业链）/ `/industry-funnel`（漏斗）/ `/quality-screen`（7 条硬指标） | 行业筛选 |
| 持仓管理类 | 4 | `/portfolio-review`（组合管理）/ `/thesis-tracker`（论文追踪） | 持仓纪律 |
| 思维工具类 | 2 | `/dyp-ask`（段永平问答）/ `/financial-data`（数据交叉验证） | 思维方法 |

每个 Skill 都有 markdown 文档（`skills/<skill-name>.md`），可以被 Claude Code 通过 `Read` 工具加载，也可以被 Codex CLI 通过 `cat` 加载。**关键是**：Skill 内部不依赖任何 Claude Code 特有的 feature（如 `~/.claude.json` 字段、CLAUDE.md 自动加载逻辑），所以可以在两个 control plane 间无修改迁移。

### 4.3 实盘业绩作为「horizontal 解耦真的 work」的铁证

2024 年实盘收益 +69.29%，2025 年实盘收益 +66.38%，连续两年大幅跑赢标普 500（2024 跑赢 46 pp / 2025 跑赢 50 pp）和恒生指数（2024 跑赢 52 pp / 2025 跑赢 39 pp）。**这不是「能跑」的 PoC，而是「能挣钱」的 PoC** —— 也就是说，双 control plane 横移的真实负担已经被两年的实盘验证消化了。

### 4.4 升维启示：Skill 是「知识资产」而非「prompt 工程」

xbtlin/ai-berkshire 用 19 个 Skill 把「巴菲特 + 芒格 + 段永平 + 李录」四位价值投资大师的方法论转译成了 portable 的 SKILL.md。这启示我们：**Skill 是「知识资产」而非「prompt 模板」**——一旦 portable，就可以脱离 control plane 单独投资、单独迭代、单独维护。这正是 horizontal 解耦的真正商业价值。

## 五、horizontal 解耦的最大实证样本：alirezarezvani/claude-skills 20,281 ⭐ 兼容 13 个 control plane

如果说 xbtlin/ai-berkshire 是「19 个 Skill 跨 2 个 control plane」的纵深案例，那 [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) 20,281 ⭐（R655 时 20,080 ⭐ → R662 20,281 ⭐）就是「354 个 Skill 跨 13 个 control plane」的广度案例。README 列出的兼容 control plane：

| Control Plane | 来源 |
|--------------|------|
| Claude Code | Anthropic |
| Codex CLI | OpenAI |
| Gemini CLI | Google |
| OpenClaw | FreezeSoul |
| Hermes | Nous Research |
| Mistral Vibe | Mistral AI |
| Cursor | Anysphere |
| Aider | Paul Gauthier |
| Windsurf | Codeium |
| Kilo Code | Kilo-Org |
| OpenCode | opencode-ai |
| Augment | augmentcode |
| Antigravity | Google DeepMind |

**13 个 control plane 同时兼容**意味着：

1. SKILL.md 已经被当成「跨 vendor Skill 协议」的事实标准
2. alirezarezvani 的工作是「Skill 内容生产」而非「Skill 适配」—— 他不需要为每个 control plane 写 354 个 Skill × 13 个适配器 = 4602 个产物，只需要写 354 个 portable Skill，每个 control plane 自动加载
3. **这是 horizontal 解耦的工业级验证** —— 如果 portable 性不能成立，354 个 Skill × 13 个 control plane 的维护成本会让这个仓库不可能存在

## 六、horizontal 解耦的工程决策框架：何时押注 vendor-neutral，何时押注 vendor-specific

horizontal 解耦给了我们「Skill 协议中立、control plane 可替换」的能力，但工程现实是：**不是每个 Skill 都应该被写成 portable**。给一个决策矩阵：

| Skill 类型 | 例子 | 建议 | 理由 |
|----------|------|------|------|
| 数据操作 / 工具调用型 | 财务数据交叉验证 / HTTP 抓取 / Shell 编排 | **vendor-neutral** | SKILL.md 的语义足够清晰，跨 control plane 都能跑 |
| 思维方法 / 知识资产型 | 价值投资 / 工程评审 / 代码评审 | **vendor-neutral** | 思维方法是知识资产，portable 让知识资产可累积、可迁移 |
| 复杂上下文工程 | 大型代码项目理解 / 多 Agent 协作编排 | **vendor-specific** | 依赖 control plane 特有的 context 管理（如 Claude Code 的 CLAUDE.md、Codex CLI 的 AGENTS.md） |
| 平台特定集成 | VSCode 插件 / JetBrains 集成 / Xcode 调用 | **vendor-specific** | 集成点本身绑定了 control plane A 的 binary |

### 6.1 决策框架的第四条：用 control plane features 的下限做判断

简单规则 ——「如果一个 Skill 在最薄 control plane（如 Codex CLI）也能跑，就在最薄的 control plane 写，然后逐层向上兼容」：

1. **Step 1**: 用 Codex CLI 写 Skill（最薄 control plane，feature set 最小，强制你写 portable 代码）
2. **Step 2**: 验证在 Claude Code 上能跑（验证 progressive disclosure 三阶段无 bug）
3. **Step 3**: 验证在 Gemini CLI / Cursor / Aider 上也能跑（验证 cross-vendor 兼容）
4. **Step 4**: 只有当某个 vendor 有决定性 productivity 优势（如 Claude Code 的 CLAUDE.md 自动加载）时，才写一个 vendor-specific 适配 Skill，而把 portable 版本留作 canonical

### 6.2 反模式：vendor lock-in Skill

如果你的 Skill 入口处包含以下任何一句：

```
- # only for Claude Code 4.5+
- # uses Claude Code-specific .claude.json field
- # depends on `~/.claude/skills/<name>/settings.local.json`
```

那么这个 Skill 已经 vendor lock-in 了。在 13 个 control plane 兼容的工业级验证（alirezarezvani/claude-skills 354 Skills 跨 13 vendor）面前，vendor lock-in 是 horizontal 解耦的反模式。

## 七、horizontal 解耦的协议之外：vertical 与 cross-device 协同

横向解耦并不是孤立的。R661 的三维度体系告诉我们，horizontal 解耦通常需要配合 vertical 解耦与 cross-device 协同：

- **vertical 解耦需要 execution plane 实现 MCP 协议**：horizontal 解耦让 Skill 可移植，但 Skill 内的 `scripts/` 调用工具需要走 MCP 协议中立层 —— 这是 vertical 解耦的职责
- **cross-device 协同需要会话状态可序列化**：多个 device 上使用同一个 Skill 时，Skill 的状态需要可序列化（如 append-only telemetry）—— 这是 cross-device 协同的职责
- **三者协同**：SKILL.md 自身 portable（horizontal）+ Skill 内部工具调用走 MCP（vertical）+ Skill 执行状态可序列化（cross-device），三件套合一才能让 harness 真正跨 vendor / 跨 device / 跨 execution plane 跑通

## 八、可执行的验证问题（给 R663 留引子）

horizontal 解耦是否真的 work？给三个验证问题：

1. **如果你今天写的一个 SKILL.md，在 30 天后还能在 Claude Code / Codex CLI / Gemini CLI 同时被调度吗？** 如果不能，问题在 SKILL.md 的 frontmatter 还是正文？
2. **如果某一天 Claude Code 的某个 feature 被 deprecate（如 subagent 改名为 task），你有多少个 Skill 需要重写？** 0 个说明你的 Skill 是 portable 的，> 0 个说明你偷懒用了 vendor-specific shortcut
3. **如果只能用一个 control plane，你会选哪个？** 这个问题如果你的答案是「那只能放弃这个 Skill」，说明你写了 vendor lock-in Skill；如果答案是「那就是把 Codex CLI 拉起来跑 portable 版本」，说明 horizontal 解耦真的 work

## 九、结论

horizontal 解耦是 harness 协议化三维度体系中**最贴近工程师日常的维度**——它不要求企业搭建复杂的 execution plane MCP 桥（vertical 解耦），也不要求多端会话状态交接（cross-device 协同），只要求一件事：**把 Skill 当接口契约写，而不是当 vendor 配置文件写**。

agentskills/agentskills 22k⭐ 的 SKILL.md 最小约定 + xbtlin/ai-berkshire 9,881 ⭐ 的 19 Skill 实盘验证 + alirezarezvani/claude-skills 20,281 ⭐ 的 354 Skill 跨 13 vendor 工业验证，三个证据叠加足以让 horizontal 解耦不再是一个「方向性」讨论，而是一个「你今天就能 write Skill 跨 multiple control plane 跑起来」的工程现实。

下一篇 R663 deep dive 将聚焦 **cross-device 协同** —— 把 Cursor iOS Mobile-Cloud Hybrid Harness 的 append-only telemetry + cache-first 架构做一次完整剖析。这会比 horizontal 解耦涉及更多移动端工程细节，但工程价值同样巨大。

## 参考资料（10 个 1st-party 来源 + 2 个三方仓库）

### harness 协议层（horizontal 解耦的协议基础）

1. [agentskills/agentskills](https://github.com/agentskills/agentskills) — vendor-neutral Skill 规范（22,438 ⭐ Apache-2.0 + CC-BY-4.0）
2. [agentskills.io/specification](https://agentskills.io/specification) — SKILL.md frontmatter schema + progressive disclosure 三阶段
3. [Anthropic: equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — Skills 开放规范的 1st-party 出处
4. [Anthropic: Claude Code Skills](https://docs.claude.com/en/docs/claude-code/skills) — vendor A 官方 Skills 实现

### Harness 三维度体系（context 提供）

5. [awesome-harness-engineering-three-dimensions-protocolization-2026](./awesome-harness-engineering-three-dimensions-protocolization-2026.md) — R661 meta article
6. [Cursor: Cloud Agent Mobile docs](https://cursor.com/docs/cloud-agent/mobile) — cross-device 协同协议精确语义（用于三维度协同章节）
7. [Anthropic: Apple Xcode + Claude Agent SDK](https://www.anthropic.com/news/apple-xcode-claude-agent-sdk) — vertical 解耦范本（用于三维度协同章节）

### 多 control plane 实现

8. [OpenAI: Codex CLI README](https://github.com/openai/codex) — vendor B control plane 实现
9. [Google: Gemini CLI](https://github.com/google-gemini/gemini-cli) — vendor C control plane 实现
10. [Anthropic: Codex CLI Skills Migration Guide](https://docs.claude.com/en/docs/claude-code/skills#migrating-skills-from-other-clients) — vendor A 的「如何把 Skills 从 vendor B 迁过来」官方指南

### 实战案例 / 三方仓库

11. [xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) — 19 Skills 跨 Claude Code + Codex 双 control plane 实盘跑通 2 年（9,881 ⭐）
12. [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) — 354 Skills 跨 13 control plane 工业级验证（20,281 ⭐）

### 关联项目

13. [mattpocock/skills](https://github.com/mattpocock/skills) — 156,976 ⭐ Skills engineering 大型库（SKILL.md 实例参考）
14. [anthropics/skills](https://github.com/anthropics/skills) — 158,308 ⭐ Anthropic 官方 Skills examples 仓库
