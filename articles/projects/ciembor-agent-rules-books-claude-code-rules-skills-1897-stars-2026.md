---
title: "ciembor/agent-rules-books 经典书籍编码规则库 2026"
date: 2026-06-19
type: project
stars: 1897
license: MIT
source: https://github.com/ciembor/agent-rules-books
cluster: harness
subcluster: rules-and-skills
pair_article: articles/harness/anthropic-claude-code-steering-7-method-decision-framework-2026.md
tags: [claude-code, codex, cursor, agent-rules, claude-md, skills, ddd, clean-architecture]
---

# ciembor/agent-rules-books：1,897⭐ 的「经典书籍编码规则库」AGENTS.md / Rules / Skills 三合一

> 项目地址：<https://github.com/ciembor/agent-rules-books>  
> Stars：1,897  
> 协议：MIT  
> 验证日期：2026-06-19（GitHub API）  
> Topics：`agent-rules`, `agent-skills`, `agents-md`, `ai-agent`, `ai-skills`, `claude-code`, `claude-code-skills`, `codex`, `codex-skills`, `cursor-rules`, `cursor-skills`, `code-quality`, `domain-driven-design`, `programming-books`, `refactoring`

## 核心命题

**ciembor/agent-rules-books** 是 Anthropic "七种自定义方法决策框架"（CLAUDE.md / Rules / Skills / Subagents / Hooks / Output styles / System prompt appending）中 **Rules + Skills 两种方法的工业化实现库**。它把 Clean Code、Refactoring、Domain-Driven Design、Clean Architecture、Designing Data-Intensive Applications（DDIA）等经典编程书籍的工程原则，**逐条翻译成 AGENTS.md 规则和 Claude Code Skills**，让 5 个主流 Coding Harness（Claude Code、Codex、Cursor、OpenCode、Gemini CLI）能够直接消费同一套规则。

这个项目的工程意义在于它把 Anthropic 决策框架中"**用 Rules 装约束、用 Skills 装程序化工作流**"的分工——**落地成可生产消费的规则库**。在 R443 决策框架中，Anthropic 指出 path-scoped rules 是"按需加载约束"的核心创新，而 ciembor/agent-rules-books 正是首批将这一机制系统化的开源实现。

> "AGENTS.md rules / skills for AI coding agents: Codex, Cursor & Claude Code. Inspired by Clean Code, Refactoring, DDD, Clean Architecture and DDIA programming books."
> — [ciembor/agent-rules-books README](https://github.com/ciembor/agent-rules-books) (v1.x, MIT, 1,897⭐)

## 为什么这是 Anthropic 决策框架的工业化锚点

### 1. 跨 Harness 规则共享：解决"碎片化 CLAUDE.md"

在没有 ciembor/agent-rules-books 之前，团队部署 Claude Code 时通常需要：
- 在每个仓库写一份 CLAUDE.md（项目级约束）
- 在 `~/.claude/rules/` 写用户级 rules（个人偏好）
- 在 `~/.claude/skills/` 写程序化工作流

**问题**：当团队同时使用 Claude Code + Codex + Cursor + OpenCode 时，每种工具都有自己的规则格式（CLAUDE.md / AGENTS.md / .cursorrules / .codex/），导致同一份规则要写 4 份。

**ciembor/agent-rules-books 的解法**：用 AGENTS.md 作为**单一事实源**，通过工具链或手工复制生成各 Harness 的原生格式。这与 runkids/skillshare 的"skills 同步"理念一致，但 ciembor/agent-rules-books 更聚焦于 **rules + skills 的工业化内容**。

### 2. 经典书籍的工程化翻译：把"原则"变成"可执行规则"

项目的核心价值在于把经典书籍的工程原则**逐条翻译成 AI 可消费的规则**：

| 来源书籍 | 翻译成的 AI 规则 |
|---------|----------------|
| Clean Code（Robert C. Martin） | 函数命名约定、单一职责、注释规范 |
| Refactoring（Martin Fowler） | 重构触发信号、函数提取模式 |
| Domain-Driven Design（Eric Evans） | 限界上下文、聚合根、值对象命名 |
| Clean Architecture（Robert C. Martin） | 依赖倒置、接口隔离 |
| DDIA（Martin Kleppmann） | 一致性模型、数据分区、事务隔离 |

**对比 R435 的 Skills + MCP 协同文章**：R435 给出的是"如何用 Skills 表达专业工作流"的协议层；ciembor/agent-rules-books 是"具体哪些规则值得做成 Skills"的内容层。

### 3. Topics 命中目标生态：claude-code + codex + cursor 全覆盖

```
['agent-rules', 'agent-skills', 'agents-md', 'ai-agent', 'ai-skills',
 'claude-code', 'claude-code-skills', 'codex', 'codex-skills',
 'cursor-rules', 'cursor-skills', 'code-quality', 'domain-driven-design',
 'programming-books', 'refactoring']
```

按 R375 #36 协议分级：
- **直接命中**（⭐⭐⭐⭐⭐）：无（无 openclaw/hermes/qclaw）
- **间接命中**（⭐⭐⭐）：`claude-code`、`claude-code-skills`、`codex`、`codex-skills`、`cursor-rules`、`cursor-skills` —— 6 个 Anthropic 生态标签
- **宽泛命中**：`agent-rules`、`agent-skills`、`ai-agent`、`ai-skills`

**综合判断**：⭐⭐⭐⭐——目标生态间接命中 6 次，是"跨 Harness 规则库"赛道的核心项目。

## 与 R443 决策框架的 4-way SPM 对位

按 R375 #34 协议 4 层叠加判定：

| Layer | 检查项 | 结果 |
|-------|-------|------|
| **Layer 1 cluster 共享** | harness cluster | ✅ 命中 |
| **Layer 2 SPM 关键词字面级** | "AGENTS.md rules" / "claude-code" / "agent-rules" / "skills" / "code-quality" | ✅ 5 关键词共享 |
| **Layer 3 topics 间接命中** | `claude-code` + `claude-code-skills` + `cursor-rules` | ✅ 6 个间接命中 |
| **Layer 4 维度互补** | Article=决策框架（理论）+ Project=规则库（实现）| ✅ 抽象 ↔ 实现 |

**4-way SPM 满中** = ⭐⭐⭐⭐⭐ 强度（R375 #34 协议）。

## 与 Anthropic 决策框架的具体对应

按 R443 决策矩阵的 4 列（When/Compaction/Cost/When to use），ciembor/agent-rules-books 中的内容对应：

| 项目内容 | 决策矩阵位置 | 工程含义 |
|---------|------------|---------|
| **AGENTS.md 通用规则** | Rules（unscoped）| 用户级 always-on 约束——如"函数命名用 camelCase" |
| **路径相关约束** | Rules（path-scoped）| 如 `frontend/**` 的 React 规则 vs `backend/**` 的 Java 规则 |
| **Skills 工作流** | Skills（按需加载）| 如"如何做 TDD"、"如何做 code review" 的程序化步骤 |
| **编程书籍原则** | CLAUDE.md（root）| "整个项目遵循 DDD" 这类全局约束 |

**核心工程创新**：该项目不是"一份规则文件"，而是 **4 类规则 + 5 个 Harness 的笛卡尔积**——一个组织可以把"DDD 全局约束 + Java 路径特定约束 + TDD 流程"打包部署到 5 个 Harness，而每个 Harness 拿到的是**原生格式**。

## 安装与使用

**基础用法**：
1. Clone 或 fork 仓库
2. 选择你使用的 Harness（Claude Code / Codex / Cursor / OpenCode / Gemini CLI）
3. 复制对应的规则目录到你的项目或 `~/.claude/`、`~/.codex/` 等
4. 重启 Harness，新规则自动生效

**进阶用法**：
- 团队级部署：通过 `git subtree` 或 sub-module 把规则仓库嵌入主项目
- 自定义规则：在 `agents-md/` 下新建 markdown 文件，遵循 AGENTS.md frontmatter 规范
- 路径特定：使用 `paths:` frontmatter 字段限定规则触发路径

## 与类似项目的对比

| 项目 | Stars | 协议 | 特点 |
|------|------|------|------|
| **ciembor/agent-rules-books** | 1,897 | MIT | 经典书籍规则库 + 跨 5 Harness |
| runkids/skillshare | 2,234 | MIT | CLI 工具做 skills/rules 同步 |
| jeremylongshore/claude-code-plugins-plus-skills | 2,390 | MIT | Claude Code 插件市场 |
| hesreallyhim/awesome-claude-code | 46,792 | NOASSERTION | awesome-list 策展 |
| VoltAgent/awesome-claude-code-subagents | 22,056 | MIT | 154+ subagents |

**差异化定位**：ciembor/agent-rules-books 是 **rules 内容层**（具体规则），runkids/skillshare 是 **rules 同步工具层**（如何分发），两者互补而非竞争。

## 工程教训：经典书籍的"AI 化"范式

**反模式**：把经典书籍的"原则摘要"作为 CLAUDE.md 一句话——Claude 读到时不知道具体怎么应用。

**正模式**：把原则拆成**可执行的步骤**——
- Clean Code 的"函数应该短小" → "函数超过 30 行时提取子函数，命名以动词开头"
- DDD 的"聚合根" → "聚合根命名以 Aggregate 结尾，跨聚合操作通过领域服务"
- DDIA 的"最终一致性" → "异步任务用 event log + 幂等 consumer 处理"

**ciembor/agent-rules-books 的工程意义**：它示范了"**经典书籍的 AI 化不是摘要化而是步骤化**"——只有可步骤化的原则才能被 AI 在每个具体场景中正确应用。

## 适用场景

✅ **适合**：
- 团队统一 Claude Code / Codex / Cursor 等多 Harness 的编码规范
- 把经典工程原则（DDD、Clean Architecture）落到 AI 消费层
- 跨项目共享"约束 + 工作流"资产

⚠️ **不适合**：
- 单人项目（直接写 CLAUDE.md 即可）
- 临时性偏好（用 system prompt appending 更快）
- 安全硬约束（用 Hooks 更可靠）

## 总结

ciembor/agent-rules-books 在 R443 Anthropic 决策框架的工业化路径上扮演 **"内容层锚点"** 角色——它是首批将"决策矩阵"中 Rules + Skills 两种方法**用经典书籍原则系统填充**的开源实现。

- **跨 Harness 兼容性**：5 个 Harness 原生格式，避免规则碎片化
- **经典书籍工业化**：把 Clean Code / DDD / DDIA 等原则翻译成可执行规则
- **Topics 生态信号**：6 个间接命中 Claude Code / Codex / Cursor 生态

对于在多个 Harness 上规模化部署 Claude Code 的团队：**直接 fork ciembor/agent-rules-books 作为规则基线**，再叠加团队特定约束，是当前最工程化的路径。

## 参考

- [ciembor/agent-rules-books GitHub](https://github.com/ciembor/agent-rules-books)
- [ciembor/agent-rules-books 主页](https://ciembor.github.io/agent-rules-books/)
- [R443 决策框架 Article](anthropic-claude-code-steering-7-method-decision-framework-2026.md)
- [R435 Skills + MCP 协同](../tool-use/anthropic-extending-claude-capabilities-skills-mcp-coordination-2026.md)
- [R432 large-codebase 五扩展点](../practices/anthropic-large-codebase-claude-code-five-extension-points-2026.md)
- [Anthropic: Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)