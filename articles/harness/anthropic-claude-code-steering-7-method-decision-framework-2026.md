---
title: "Anthropic Claude Code 七种自定义方法决策框架 2026"
date: 2026-06-19
type: article
cluster: harness
subcluster: steering
source: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
tags: [claude-code, steering, decision-framework, harness, agent-customization, claude-md, rules, skills, subagents, hooks, output-styles]
pair_project: articles/projects/ciembor-agent-rules-books-claude-code-rules-skills-1897-stars-2026.md
---

# Anthropic Claude Code 七种自定义方法决策框架 2026

> 2026 年 6 月，Anthropic 在 Claude 博客上发表了一篇少见的「**自定义方法论**」文章：**明确回答了社区最关心的一个核心问题——"我有 N 条 Claude 指令应该放在哪？"** 本文解读这篇"七种方法 + 三维决策矩阵"背后的工程哲学：当 Claude Code 团队宣布支持 7 种不同的指令注入方式时，**选错方法 = 浪费 token / 错过 compaction / 上下文爆炸**——这才是 Harness 工程的真正门槛。

## 核心命题

Anthropic 把 Claude Code 的自定义方式正式归为 **七种方法**：

1. **CLAUDE.md**（root + subdirectory）
2. **Rules**（`~/.claude/rules/`）
3. **Skills**（`~/.claude/skills/`）
4. **Subagents**
5. **Hooks**
6. **Output styles**
7. **Appending the system prompt**（CLI flag）

每种方法在 **三个维度** 上有截然不同的取舍：
- **When it loads**（什么时候进入上下文）
- **Compaction behavior**（compaction 之后是否被保留/重注入）
- **Context cost**（每次消耗多少 token）

> "Each method controls: When an instruction loads into context; Whether it persists through long sessions (compaction behavior); and How much authority it carries."
> — [Anthropic: Steering Claude Code: Skills, hooks, rules, subagents, and more](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)

**笔者认为**：这篇文章把 Claude Code 的"配置工程"从"我随便写个 CLAUDE.md 试试"提升到"**我有 N 条指令，应该用 4 个维度决定它们各自归位**"的工程级别。这是 Anthropic 第一次把"决策矩阵"写进官方文档——它隐含的工程哲学是：**Steering（指令注入）是 Harness 工程的核心问题，不是一个简单的"配置文件"问题**。

---

## 一、官方决策矩阵：四列 × 七行

| 方法 | 何时加载 | Compaction 行为 | 上下文成本 | 何时使用 |
|------|---------|----------------|-----------|---------|
| **CLAUDE.md (root)** | Session 启动；会话全程驻留 | 记忆化（memoized）；compaction 后缓存被清并重新读取 | **高**（每行都消耗 token，无论是否相关）| 构建命令、目录结构、monorepo 结构、编码约定、团队规范 |
| **CLAUDE.md (subdirectory)** | 按需加载（当 Claude 读取该子目录下的文件时）| 直到该子目录再次被触碰前丢失 | **低**（仅当相关子目录被工作时消耗）| 特定子目录的约定 |
| **Rules** | Session 启动（用户级 rules）或仅当匹配文件被触碰时（path-scoped）| Compaction 时重新注入 | **中等**（除非 path-scoped，否则 always-on）| 特定约束或约定（如"所有 API handler 必须用 Zod 校验输入"）|
| **Skills** | Session 启动时仅加载 name + description；调用时加载完整 body | 被调用的 skill 在共享预算内重新注入；最老的先丢弃 | **低**（仅在调用时加载完整 body）| 程序化工作流（部署 / 发布检查清单）|
| **Subagents** | Session 启动时仅加载 name + description + tool list；通过 Agent 工具调用时加载 body | 只有最终消息（摘要 + 元数据）返回主会话 | **低**（在主上下文中零成本直到被调用；运行在独立的隔离上下文中）| 并行执行工作，或应在隔离中运行只返回摘要的子任务（深度搜索、日志分析、依赖审计）|
| **Hooks** | 触发生命周期事件时 | 完全绕过 compaction | **低**（配置存在于主上下文之外；某些输出可能返回，如阻塞错误）| 确定性自动化（运行 linter、完成时发 Slack、阻塞命令、PreCompact 时备份聊天历史）|
| **Output styles** | Session 启动；注入到系统提示中 | 从不 compact | **高**（占用上下文窗口，但覆盖默认系统提示）| 重大角色变更（从代码助手变成通用助手）|
| **Appending the system prompt** | Session 启动；作为 CLI flag 传入 | 从不 compact；仅对当前调用生效 | **中等**（在 session 中首次请求后被缓存）| 语气、响应长度、格式化偏好 |

**官方明确指出**："The table below provides a quick summary of key differences across each method while the post provides additional detail and decision framework for determining where each of your Claude instructions belongs."

**笔者认为**：这表格本身就是一个 **决策矩阵**——它把"我有 N 条指令"这个问题转化成了"每条指令在哪个格子"。如果你不能用这个矩阵把现有指令分类，**你的 Harness 就还不是工程化的**。

---

## 二、Rules：path-scoped 是核心创新

Anthropic 在文章中重点讨论了 **Rules** 这一较新的方法。Rules 是位于 `.claude/rules/` 下的 markdown 文件，给 Claude 提供特定约束或约定。

**核心问题**：Unscoped rules 在行为上类似于 CLAUDE.md——它们在 Session 启动时加载，compaction 时重新注入。这意味着即使当前任务与该 rule 无关，它也会消耗 token。

**解法：path-scoped rules** —— 通过在 frontmatter 中添加 `paths` 字段，让 rule 仅在 Claude 读取匹配该路径的文件时才加载。

```yaml
---
paths:
  - "src/api/**"
  - "**/*.handler.ts"
---
All API handlers must validate input with Zod before processing.
```

**关键效果**：当 Claude 在 docs-only session 中工作时，这条 rule 不会出现在上下文中；只有当 Claude 读取 `src/api/` 目录或 `*.handler.ts` 文件时，它才会被加载。

> "A file-specific constraint, like 'migrations are append-only,' fits best as a rule placed in your paths: frontmatter. Reach for a path-scoped rule over a nested CLAUDE.md file when the instruction regards a cross-cutting concern or file that appears in multiple (but not all) corners of the codebase."

**笔者认为**：path-scoped rules 是这次发布的 **核心工程创新**——它把"上下文管理"从"我手动管理"提升到"**Harness 帮你按需加载**"。在没有 path-scoped rules 之前，要实现"仅在 API handler 工作中加载 Zod 校验规则"通常需要嵌套 CLAUDE.md（即在 `src/api/CLAUDE.md` 里写），但这种方式的问题是：当 Claude 跨多个子目录工作时，多份 CLAUDE.md 都会被加载。**path-scoped rules 解决了这个粒度问题**——一条 rule 可以同时覆盖 `src/api/**` + `**/*.handler.ts` 而不限定于单一目录。

---

## 三、Skills：渐进式披露（Progressive Disclosure）的工业化

文章对 Skills 的描述呼应了 Anthropic 早些时候发布的 Agent Skills 文档：

> "Skills live in `.claude/skills/` as folders of instructions, scripts, and resources that Claude loads dynamically. Each skill has a SKILL.md file with a name, description, and body. Only the name and description load at session start; the full body loads when Claude invokes the skill, either through a slash command (`/code-review`) or by auto-matching the task."

**关键约束**：
- **Session 启动时**仅加载 `name` + `description`（约几十 token）
- **被调用时**才加载完整 body
- **共享 token 预算**：所有被调用的 skills 共享一个总预算，**最老的先被丢弃**（LRU 策略）

**对比 Rules**：Rules 是"约束/约定"——总是描述"什么不能做"；Skills 是"程序化工作流"——描述"按什么步骤做某件事"。

> "Use rules for constraints and conventions, use skills for procedural workflows."

**笔者认为**：这个区分非常关键。一个常见的反模式是把"代码规范"写成 skill（"请按 PEP 8 风格写代码"）——这种约束应该在 Rules 或 CLAUDE.md 中；而"如何做 release"这种"按步骤执行"的工作流才适合作为 skill。

---

## 四、Hooks：确定性自动化的独占路径

Hooks 的位置独特——它 **完全绕过 compaction**。

**核心特性**：
- **不进入主上下文**：hooks 配置存在于主上下文之外
- **触发生命周期事件**：PreToolUse、PostToolUse、PreCompact、SessionStart 等
- **可阻断**：某些 hook 可以返回 blocking error 阻止操作继续
- **运行确定性逻辑**：linter、Slack 通知、备份、命令阻断

> "Hooks fire on lifecycle events... Bypass compaction entirely... Configuration lives outside main context; some output may return (e.g., blocking errors)."

**典型用例**：
- `PreToolUse` hook: 阻断 `git push --force` 到 main 分支
- `PostToolUse` hook: 每次写文件后自动运行 prettier
- `PreCompact` hook: 在 compaction 之前备份聊天历史

**笔者认为**：Hooks 是七种方法中 **唯一可以"确定性"控制行为的**——其他六种都是"软指令"（Claude 可能遵循也可能不遵循），只有 Hooks 是"硬约束"。**这就是为什么安全相关的策略（如"禁止 force push"）应该用 Hooks 而不是 CLAUDE.md**——后者可能被 Claude 误读或忽略。

---

## 五、Output styles 与 system prompt appending 的边界

文章还讨论了两个更窄的方法：

**Output styles**：在 Session 启动时注入到系统提示中，**覆盖默认系统提示**。典型用例是"从代码助手变成通用助手"——比如切换成"幽默导师"或"代码评审员"风格。
- 缺点：占用上下文窗口，且从不 compact。
- 适用：仅当你需要 **重大角色变更** 时使用。

**Appending the system prompt**：通过 CLI flag 传入，**仅对当前调用生效**。典型用例是"语气、响应长度、格式化偏好"。
- 优点：在 session 中首次请求后被缓存——**不会重复消耗 token**。
- 适用：临时性偏好，而不是项目级配置。

**笔者认为**：这两个方法的共同点是"**它们影响 Claude 的输出风格而不是行为约束**"。把它们放在"七种方法"列表里其实有点勉强——它们的本质是"渲染层配置"而不是"指令注入"。这可能是 Anthropic 为了完整性才列出的。

---

## 六、决策算法：选错方法的代价

根据官方矩阵，选错方法的具体代价：

| 选错 | 代价 | 案例 |
|------|------|------|
| 把"全局约定"放进 Skills | 浪费 token（完整 body 被加载即使不相关）| "Always use TypeScript strict mode" 应在 CLAUDE.md，不应在 skill |
| 把"路径相关约束"放进 CLAUDE.md (root) | 全局污染（即使在不相关目录也消耗 token）| "All API handlers must validate input with Zod" 应在 path-scoped rule，不应在 root CLAUDE.md |
| 把"安全策略"放进 CLAUDE.md | 软约束可能被忽略 | "Never force push to main" 应在 PreToolUse hook，不应在 CLAUDE.md |
| 把"程序化工作流"放进 Rules | 失去 procedural loading 优势 | "How to do release" 应在 skill，不应在 rule |
| 把"并行任务"放进 CLAUDE.md | 主上下文爆炸 | "For deep search use subagent" 应配置 subagent，不应在 CLAUDE.md 写提示 |

**官方推荐流程**（隐含在文章结构中）：
1. **先列指令清单**：你希望 Claude 知道的所有约束/约定/工作流
2. **画决策矩阵**：每条指令在四列（When/Compaction/Cost/When to use）上的位置
3. **挑方法**：根据矩阵决定每条指令归位
4. **验证 token 预算**：用 `/context` 或类似工具看实际 token 消耗
5. **迭代**：跑几次 session，看是否有重复或不必要的指令加载

---

## 七、与既有 Harness 工程的关联

**R432 large-codebase 五扩展点**（5 extension points for large codebases）：
- 那篇文章讨论的是"在大型代码库中 Claude Code 的 5 个扩展点"
- 与本文的 7 种方法不同维度——R432 是"扩展 Claude Code 的接口"，本文是"向 Claude Code 注入指令的方法"

**R434 best-practices-configuration**（4 layers of Claude Code best practices）：
- 那是按"配置层级"分类（环境配置 / 并行会话管理 / ...）
- 与本文的 7 种方法不同分类——R434 是"配置的位置"，本文是"指令注入的方法"

**R435 extending-claude-capabilities-skills-mcp**（Skills + MCP 协同）：
- 那篇讨论 Skills 与 MCP 的分工
- 本文把 Skills 作为七种方法之一详细讨论**何时使用 Skills**

**笔者认为**：这三篇文章构成了 Anthropic Claude Code 工程的**官方三件套**：
- **R432** = "能力扩展"维度（怎么接入外部系统）
- **R434** = "配置层级"维度（配置在哪一层）
- **R443（本篇）** = "指令注入"维度（怎么注入 Claude 的行为）

---

## 八、工程教训：常见反模式

根据文章提供的决策矩阵，识别几个常见反模式：

**反模式 1：把所有内容写进 CLAUDE.md (root)**
- 症状：Harness 一启动就消耗几千 token，跨目录工作时大量 token 被浪费
- 解法：把"路径相关"的约束移到 path-scoped rules，把"程序化"的工作流移到 skills

**反模式 2：把"全局安全策略"写成 CLAUDE.md 文字**
- 症状：Claude 可能误读或忽略该策略
- 解法：用 Hooks（PreToolUse）实现硬约束

**反模式 3：创建大量"一次性 skills"**
- 症状：Skills 库膨胀，token 预算爆满
- 解法：把"约束"放 Rules，"程序化"才放 Skills，每个 skill 必须有明确触发场景

**反模式 4：用 Output styles 实现角色变更，但忘记它从不 compact**
- 症状：长 session 中后期角色变更占用大量上下文
- 解法：仅在需要"重大角色变更"时使用，且应评估上下文开销

**反模式 5：用 subagent 实现"并行"但没有隔离**
- 症状：subagent 的中间结果污染主上下文
- 解法：subagent 必须返回"摘要 + 元数据"而不是完整上下文

---

## 九、为何 2026 年才出现这种"决策框架"？

**回顾**：2025 年 8 月，Anthropic 把 Agent Skills 发布为跨平台开放标准时，社区主流误解是"skills = 配置文件"。但 Anthropic 在 2026 年 6 月的这篇文章里明确把 Skills 定位为 **7 种方法中的一种**，且只有满足"程序化工作流"特征时才用 Skills。

**笔者认为**：这种**从"配置文件范式"到"决策框架范式"**的转变背后是 **Anthropic 的工业化教训**——当 Claude Code 用户从个人开发者扩展到团队（数千人）、再扩展到企业（数万人）时，"我随便写个 CLAUDE.md 试试"模式不可持续。**官方决策框架是 Anthropic 自己踩坑后的总结**：他们发现"团队层面 CLAUDE.md 一致性"无法靠文档规范保证，必须靠"工程化的方法选择"。

---

## 十、可执行建议

**第一步：清单化你的指令**
- 列出 Claude Code 当前加载的所有指令（CLAUDE.md、rules、skills、settings 等）
- 评估每条指令的"何时使用"特征

**第二步：用决策矩阵归位**
- 路径相关 → path-scoped rule
- 全局约定 → CLAUDE.md
- 程序化工作流 → skill
- 安全/硬约束 → hook
- 临时偏好 → system prompt appending

**第三步：监控 token 预算**
- 使用 `/context` 命令查看实际 token 消耗
- 识别"从未触发"的指令 → 移到 path-scoped 或 subagent

**第四步：迭代**
- 跑一个完整的项目 session
- 看 compaction 前后指令是否正确保留/重新加载
- 调整

**第五步：团队化**
- 把决策矩阵写进团队 onboarding
- Code Review 中加一条："你新加的指令经过决策矩阵了吗？"

---

## 总结

Anthropic 这篇文章表面上是"7 种方法的对比表"，**实际上是 Harness 工程从"配置即一切"范式到"决策即一切"范式的拐点**。

- **决策矩阵**（4 列 × 7 行）本身是文档级别的产物
- **path-scoped rules** 是核心工程创新
- **七种方法的边界划定**标志着 Harness 工程的工业化阶段

对于团队采用 Claude Code：**学习并严格执行这个决策矩阵**，比学习更多"高级用法"更重要——因为选错方法的代价是 token 浪费、compaction 失败、上下文爆炸。而这些代价在个人使用时可能看不出来，但在团队规模化时会**指数级放大**。

---

## 参考

- [Anthropic: Steering Claude Code: Skills, hooks, rules, subagents, and more](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)
- [Anthropic Engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- R432 large-codebase 五扩展点：[articles/practices/anthropic-large-codebase-claude-code-five-extension-points-2026.md](../practices/anthropic-large-codebase-claude-code-five-extension-points-2026.md)
- R434 best-practices-configuration：[articles/harness/anthropic-claude-code-best-practices-configuration-scaling-2026.md](anthropic-claude-code-best-practices-configuration-scaling-2026.md)
- R435 extending-claude-capabilities-skills-mcp：[articles/tool-use/anthropic-extending-claude-capabilities-skills-mcp-coordination-2026.md](../tool-use/anthropic-extending-claude-capabilities-skills-mcp-coordination-2026.md)
- R406 subagents-in-claude-code：[articles/orchestration/claude-code-subagents-decision-framework-2026.md](../orchestration/claude-code-subagents-decision-framework-2026.md)