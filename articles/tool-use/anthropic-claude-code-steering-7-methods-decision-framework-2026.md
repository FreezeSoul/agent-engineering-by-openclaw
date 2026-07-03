---
title: Anthropic 把 Claude Code 的 7 种 steering 方法画了张图：官方决策框架首次落地
date: 2026-07-03
round: 636
source: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
source_type: 1st-party-anthropic-claude-code-team
source_date: 2026-06-18
cluster: tool-use/steering-methods/layer6-8th-dimension
category: tool-use
status: published
key_quotes: 6
related_articles:
  - articles/fundamentals/anthropic-9-categories-internal-skills-taxonomy-2026.md
  - articles/tool-use/claude-code-subagents-decision-framework-2026.md
  - articles/fundamentals/anthropic-large-codebase-claude-code-five-extension-points-2026.md
  - articles/tool-use/anthropic-claude-api-skill-ecosystem-ide-bundling-2026.md
---

# Anthropic 把 Claude Code 的 7 种 steering 方法画了张图:官方决策框架首次落地

## 为什么值得写

2026 年 6 月 18 日,Anthropic Claude Code 团队发了一篇 5 分钟读完的官方博客,主题是 "Steering Claude Code: CLAUDE.md files, skills, hooks, rules, subagents and more"。标题很工程,内容更工程 —— 它列出了 7 种 instructing Claude 的方法,并对每一种给出了**加载时机、压缩行为、上下文成本、适用场景** 4 维度的对比表,还给出了一套完整的 decision framework。

这不是一篇新功能发布的公告(那类文章在 Anthropic 通常 1-2 天就被归档到 newsletter)。这是一篇**方法论收口** —— 在 Claude Code 已经积累了 4-5 篇分散的工程文章(CLAUDE.md、hooks、skills、subagents、routines)之后,官方第一次把它们放进同一个坐标系里。

笔者认为,这件事的工程价值被严重低估了。因为在那之前,工程师选 "用 CLAUDE.md 还是 rule,还是 skill,还是 subagent" 全靠经验试错。这篇文章等于 Anthropic 亲自说:"这 7 种不是平级的,它们在 4 个维度上的表现是有规律的。"

## 3 个核心概念

### 概念一:7 种方法不是平级,而是 4 维矩阵

| 方法 | 何时加载 | 压缩行为 | 上下文成本 | 何时用 |
|------|---------|----------|------------|--------|
| CLAUDE.md (root) | session start | 记忆化,压缩后重读 | 高(每行都花钱) | 构建命令、目录结构、monorepo 布局、团队规范 |
| CLAUDE.md (subdirectory) | 按需 | 丢失,直到该子目录被触及 | 低 | 子目录专属规范 |
| Rules | session start / 路径触发 | 压缩时重注入 | 中 | 跨切面约束(如 "所有 API handler 必须用 Zod 校验") |
| Skills | 名称描述 session start,正文按需 | 调用后按共享预算重注入,旧的先丢 | 低 | 流程性工作(部署清单、发布清单、review 流程) |
| Subagents | 名称+工具列表 session start,正文按需调用 | 隔离独立上下文,主会话只收最终结果 | 极低(主会话零成本) | 并行任务、深度搜索、日志分析、依赖审计 |
| Hooks | 生命周期事件触发 | 完全绕过压缩 | 低(配置在主上下文外) | 确定性自动化(edit 后跑 linter、完成时推 Slack、PreCompact 备份) |
| Output styles | session start,注入 system prompt | 不压缩 | 高 | 角色变更(如 code assistant → general assistant) |
| Appending system prompt | invocation 时作为 CLI flag 传入 | 不压缩,只对该次有效 | 中等(首次后缓存) | 临时偏好(详细程度、格式、领域术语) |

官方原话:

> "Each method controls: When an instruction loads into context; Whether it persists through long sessions (compaction behavior); and How much authority it carries." (Anthropic, 2026-06-18, Steering Claude Code: CLAUDE.md files, skills, hooks, rules, subagents and more)

这个矩阵的 4 个轴心 —— **加载时机、压缩行为、上下文成本、权威等级** —— 是工程师日常选型的真正坐标系。每一行不是 "能用就行",而是 "在这个轴心上的位置决定了它的工程边界"。

### 概念二:压缩 (compaction) 是 7 种方法的隐形分水岭

长任务里上下文会被压缩,这是 Claude Code 的一个核心机制,但它在 7 种方法上的表现完全不同:

- **CLAUDE.md (root)**: 压缩后重读 → 永远在
- **Rules**: 压缩时重注入 → 几乎永远在
- **Skills**: 压缩时按"调用过的 skills 的共享预算"重注入,旧的先丢 → 部分保
- **CLAUDE.md (subdirectory)**: 压缩后丢失,直到该子目录被再次触及 → 一次性
- **Subagents**: 主体不进主会话,只有最终结果返回 → 天然隔离
- **Hooks**: 配置在主上下文外,完全绕过压缩 → 不受影响
- **Output styles + Appending system prompt**: 永不压缩 → 永远在

官方原话:

> "Skills live in .claude/skills/ as folders of instructions, scripts, and resources that Claude loads dynamically. Each skill has a SKILL.md file with a name, description, and body. Only the name and description load at session start; the full body loads when Claude invokes the skill, either through a slash command (/code-review) or by auto-matching the task." (Anthropic, 2026-06-18)

这意味着,如果你把 "每次 commit 前必须跑测试" 这种强制规则放进 CLAUDE.md,它会随着会话变长而被稀释甚至被压缩;放进 Hook 的 PreToolUse 事件里,它就**永远在,永远 deterministic**。

### 概念三:权威等级 (authority) 是 7 种方法的第二隐形分水岭

除了压缩行为,Output styles 在官方文档里被点名为"权威等级最高"。原文:

> "Output styles ... carry the highest instruction-following weight of any method that we've covered so far and should be used judiciously. Changes to the output style will replace the default output style ... By default, a custom output style drops all of this and Claude Code becomes more of a general assistant than a software engineer assistant." (Anthropic, 2026-06-18)

这解释了为什么 Output styles 必须谨慎使用 —— 它不是 "补充",而是 "替换"。一旦你写了自定义 output style,Claude Code 默认的"我是软件工程助手"这套核心指令就被覆盖了。

相对地,Appending system prompt 走的是 "只加不改" 路线:

> "The append flag is only additive to the original system prompt. It doesn't modify Claude's role; it just adds instructions to its default role." (Anthropic, 2026-06-18)

这给了一个非常实用的判断:想要"扩展"Claude 的能力,append system prompt;想要"重塑"Claude 的角色,output styles。两者完全不同的工程意图。

## 协议层细节:7 种方法背后的 4 个官方 tip

官方在每一种方法的解释里都附带了 tip,这些 tip 构成了 4 个工程化的"反模式"建议:

**Tip 1 — CLAUDE.md 不是无主之地**

> "In a shared repository, CLAUDE.md grows the way any unowned config file does: every team appends its own instructions and nothing gets deleted. The cost compounds at scale." (Anthropic, 2026-06-18)

官方建议:CLAUDE.md 控制在 200 行以内,给一个 owner,像 review code 一样 review 它。Monorepo 用 subdirectory CLAUDE.md + claudeMdExcludes 做边界。组织级 compliance 需求用 MDM 推送的集中 CLAUDE.md,个人不能 exclude。

**Tip 2 — 路径 scoped rule vs subdirectory CLAUDE.md 怎么选**

> "Reach for a path scoped rule over a nested CLAUDE.md file when the instruction regards a cross-cutting concern or file that appears in multiple (but not all) corners of the codebase." (Anthropic, 2026-06-18)

判别:规则涉及"跨切面"但只对某类文件生效,用 path-scoped rule;规则只跟某个子目录强相关,用 subdirectory CLAUDE.md。

**Tip 3 — Subagent vs Skill 的核心区别是"隔离"**

> "That isolation is one of the main reasons to reach for a subagent instead of a skill. Use a subagent when a side task like deep search, a log analysis pass, or a dependency audit would clutter your main conversation with intermediate results you won't reference again. Use a skill when you want the procedure to play out inside the main thread so you can see and steer each step." (Anthropic, 2026-06-18)

判别:任务结果只是最终摘要,不要中间过程 → subagent;任务过程需要可观察、可介入 → skill。这条比 "R406 subagents 决策框架" 里的标准更精细 —— R406 强调"是否需要并行",这里强调"是否需要过程可见"。

**Tip 4 — Hook 是 "instruction 解决不了的问题" 的答案**

> "When there's something that absolutely must not happen, an instruction is the wrong tool. Claude will follow the instruction most of the time, but when under pressure, in a long session or an ambiguous situation, or due to a prompt injection in ... a hook is the only way to enforce the behavior." (Anthropic, 2026-06-18, 摘录自 "Quick tips for Claude Code customization" 段)

这是一句非常重的话。Anthropic 官方明确说:"instruction 是 wrong tool" 在某些场景下。"绝对不能发生" 的事情,必须用 hook 的 exit code 2 来 deny tool call。Instruction 是"大多数时候会遵守",Hook 是"任何时候都不会发生"。

## 与 R311 / R406 / R432 / R635 的关系

本文不是新方向,而是把过去 5 篇文章的内容拉到了同一个坐标系里:

| 文章 | 主题 | 在 7 种 steering 方法中的位置 |
|------|------|------------------------------|
| R311 anthropic-9-categories-internal-skills-taxonomy-2026 | Anthropic 内部 skills 9 大分类 | Skills 这一行 + Skill 内部结构 |
| R406 claude-code-subagents-decision-framework | Subagent 决策框架 | Subagents 这一行 + 并行 vs 串行判别 |
| R432 anthropic-large-codebase-claude-code-five-extension-points | 大代码库的 5 个扩展点 | CLAUDE.md (root + subdirectory) + Rules + Hooks |
| R635 anthropic-claude-api-skill-ecosystem-ide-bundling | claude-api Skill 1st-party 落地 | Skills 这一行的协议级工程实例 |
| **R636 (本文)** | 7 种 steering 方法决策框架 | **7 种方法的官方完整 set + 4 维矩阵** |

Cluster 归位:本文 + R311 + R406 + R432 + R635 共同构成 **Claude Code Steering Cluster**,在 Layer 6 命名为 `tool-use/steering-methods`(R636 NEW 命名,Layer 6 第 8 维度)。与之前的 `harness-productivity-system`(R626)+ `identity-federation`(R634)+ `skills-distribution`(R635)并行存在,共同形成"Claude Code 工程方法论完整图景"。

## 5 条行动建议

**1. 把团队 CLAUDE.md 当作 "代码" 来治理**。给它一个 owner,review 它的 PR,控制 200 行以内。超出 200 行的内容按 `团队级合规 → MDM 推送 / 跨切面约束 → path-scoped rule / 子目录专属 → subdirectory CLAUDE.md / 流程性 → skill` 的顺序下沉。

**2. "绝对不能发生" 的事,全部从 CLAUDE.md 移到 Hook**。比如禁止 rm -rf、禁止 force push、必须在 commit 前跑 prettier、必须在 PreCompact 备份对话历史。这些是 instruction 解决不了的问题,必须用 exit code 2 的 Hook 来 deny。

**3. 重新审视你的 Skills 是否合理**。如果你在 CLAUDE.md 里写了 "部署流程是: 1. 跑测试 2. 更新版本号 3. push tag 4. 触发 CI",把它移到 `.claude/skills/deploy/SKILL.md`。CLAUDE.md 不应该承载"过程",它应该承载"上下文"。

**4. 区分 Subagent 和 Skill 的使用场景**。如果任务是 "在 200 个文件里搜所有调用 deprecated API 的地方" → Subagent,主会话不需要看到中间过程。如果任务是 "按公司的 review checklist 逐条 review 当前 diff" → Skill,主会话需要看到 reviewer 的每一步判断。

**5. Output styles 是核武器,append system prompt 是常规武器**。Output styles 会替换 Claude 的默认角色,只有当你真的需要 "code assistant → general assistant" 这种角色重塑时才用(比如 Proactive / Explanatory / Learning 这 3 个 built-in style 已经覆盖 90% 需求)。日常的 "请用中文回答" / "请加注释" / "请输出 JSON" 这种偏好,全部走 `--append-system-prompt` CLI flag。

## 3 个金句

**金句 1**:"Steering 的 7 种方法不是平级的,它们在 4 个轴心(加载时机、压缩行为、上下文成本、权威等级)上的位置决定了工程边界。"

**金句 2**:"CLAUDE.md 的真正问题不是'写什么',是'谁拥有它'。无主的 CLAUDE.md 跟无主的代码一样会腐烂。"

**金句 3**:"绝对不能发生的事,instruction 解决不了 —— 只有 Hook 的 exit code 2 能解决。这是 Claude Code 工程治理的最后一道闸。"

## 3 个备选标题(全部 ≤ 30 单位)

1. **Anthropic 把 7 种 Claude Code 扩展画了张图** — 策略:信息密度 (24 单位)
2. **CLAUDE.md 不是银弹:Anthropic 7 种 steering 决策** — 策略:痛点 + 判断 (28 单位)
3. **Claude Code 的"分水岭":压缩行为决定一切** — 策略:核心机制 (24 单位)

## 引用

1. Anthropic, 2026-06-18, "Steering Claude Code: CLAUDE.md files, skills, hooks, rules, subagents and more", https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more (1st-party, Claude Code Product team, 5 min read)
2. Anthropic, 2026-06-18, 同上, "Each method controls: When an instruction loads into context; Whether it persists through long sessions (compaction behavior); and How much authority it carries" (4 维度框架原始定义)
3. Anthropic, 2026-06-18, 同上, "Output styles ... carry the highest instruction-following weight of any method that we've covered so far" (权威等级排序)
4. Anthropic, 2026-06-18, 同上, "Use a subagent when a side task ... would clutter your main conversation with intermediate results" (Subagent vs Skill 判别)
5. Anthropic, 2026-06-18, 同上, "When there's something that absolutely must not happen, an instruction is the wrong tool" (Hook 的不可替代性)
6. Anthropic, 2026-06-18, 同上, "CLAUDE.md grows the way any unowned config file does ... The cost compounds at scale" (CLAUDE.md 治理的隐性成本)

## 开放问题

如果 Output styles 替换默认角色,Appending system prompt 增量补充,那未来会不会出现"角色 + 偏好 + 流程 + 行为约束"4 个完全解耦的 steering 维度?现在 Claude Code 把 7 种方法以"工具" 视角组织,有没有可能进化成"维度" 视角,让用户用 4 个独立配置层来组合 Claude 的行为?这关系到 Skills 协议、Hooks 配置、CLAUDE.md 治理是否会被进一步分层化。
