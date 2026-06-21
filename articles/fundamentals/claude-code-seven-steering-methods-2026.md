# Claude Code 七种行为引导方法论：系统化调控 Agent 的技术栈

> 官方来源：["Steering Claude Code: skills, hooks, subagents and more"](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) | Claude Blog，2026年6月18日发布
>
> 补充来源：[Skills 官方文档](https://code.claude.com/docs/en/skills) | [Memory 官方文档](https://code.claude.com/docs/en/memory.md) | [Commands 参考](https://code.claude.com/docs/en/commands)

---

## 核心命题

Claude Code 官方博客近期披露了七种行为引导机制的完整技术栈——这不是一套平行的选项，而是一套分层设计的控制系统，每层解决不同层次的调控粒度问题。

笔者认为，理解这七层机制的关键在于一个核心判断：**Claude Code 的设计哲学是将"持久规则"（CLAUDE.md、Rules）和"按需能力"（Skills、Subagents）分离，前者决定 Agent 默认行为，后者决定它在具体任务中的发挥上限。** 这与 LangChain 的 tool-first 路线截然不同——Claude 选择的是 prompt-first、skill-on-top 的架构。

---

## 一、为什么需要七种引导机制

当 Agent 进入开发环境，面临的第一个工程问题不是"它能做什么"，而是"它应该以什么方式做事"。

这个区别至关重要。一个能写代码的 Agent 和一个按团队规范写代码的 Agent，是两个完全不同的工程产品。Prompt 可以控制行为，但 prompt 是瞬态的——每次新会话都要重新注入。Rules 可以持久化，但粒度太粗。要在长周期、多人协作、高复杂度项目中保持 Agent 行为一致性，必须有一套分层控制系统。

Claude Code 的答案是七层机制，分布于两个维度：

| 维度 | 机制 |
|------|------|
| **持久化上下文** | CLAUDE.md 文件（项目/用户/组织三级）|
| **即时调控** | Rules（规则）、Skills（技能）、Subagents（子 Agent）、Hooks（钩子）、Output Styles（输出风格）、System Prompt 追加 |

---

## 二、七层机制逐层解析

### 2.1 CLAUDE.md 文件：持久化规则的核心

CLAUDE.md 是整个系统的基座。它在每次新会话开始时加载，**以 Memoized 方式缓存**——即每个会话只读取一次，之后常驻上下文。

官方文档明确给出了四种存放位置和对应的作用域：

| 作用域 | 位置 | 用途 |
|--------|------|------|
| **Managed Policy** | `/etc/claude-code/CLAUDE.md`（Linux）等 | IT/DevOps 管理的全组织规则 |
| **User** | `~/.claude/CLAUDE.md` | 个人偏好，跨所有项目 |
| **Project** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享的项目规范 |
| **Local** | `./CLAUDE.local.md` | 个人项目本地偏好（加入 .gitignore）|

加载顺序从宽泛到具体：Managed Policy → User → Project → Local。这意味着你的个人偏好可以被项目规范覆盖，项目规范可以被组织级政策覆盖——这正是一个正常的技术组织应有的权限层级。

关于何时使用 CLAUDE.md，官方给了一个精准的判断标准：

> "Treat CLAUDE.md as the place you write down what you'd otherwise re-explain. Add to it when: Claude makes the same mistake a second time; A code review catches something Claude should have known about this codebase."

笔者认为这个设计非常务实——CLAUDE.md 不是用来写"所有代码都要遵循的规范"，而是用来存**那些 Agent 会重复犯错的事实**。每次 Agent 犯了一个本可避免的错误，就把对应规则写进 CLAUDE.md。这是技术债务管理思路在 Agent 行为调控上的应用。

此外，Claude Code 还提供了**自动记忆（Auto Memory）**机制——Agent 会自动记录它从你的修正中学到的东西，与 CLAUDE.md 的区别如下：

| | CLAUDE.md | Auto Memory |
|--|-----------|-------------|
| **编写者** | 人类 | Agent 自身 |
| **内容类型** | 指令和规则 | 从修正中学习的模式和偏好 |
| **加载范围** | 每个会话前 200 行或 25KB | 每个会话前 200 行或 25KB |
| **作用域** | 项目/用户/组织 | 按仓库，跨 worktree 共享 |

### 2.2 Skills：按需加载的可扩展能力包

Skills 是 Claude Code 官方定义的第三类扩展机制（区别于 Commands 和 Plugins）。创建技能只需一个 `SKILL.md` 文件，Claude 自动将它纳入工具箱。

Skills 的核心设计原则是**延迟加载**（Lazy Loading）：不同于 CLAUDE.md 的会话开始即加载，Skill 的内容只在被使用时才读入上下文。这意味着可以在 Claude Code 中存放大量参考材料而几乎不消耗上下文窗口——只有在实际调用时才付出成本。

Skills 遵循 [Agent Skills 开放标准](https://agentskills.io)，这意味着 Skills 文件可以在多个 AI 工具间迁移。Claude Code 在此标准基础上增加了三项扩展：调用控制（决定谁可以触发技能）、子 Agent 执行（允许技能在子 Agent 中运行）、动态上下文注入（`!` 前缀执行命令并内联结果）。

官方文档中的动态上下文注入示例非常说明问题：

```yaml
---
description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
---

## Current changes

!`git diff HEAD`

## Instructions

Summarize the changes above in two or three bullet points...
```

这里的 `!`git diff HEAD`` 会在 Skill 执行时运行 git 命令，将其输出直接内联到提示词中。这解决了 Agent 在没有实际代码状态的情况下给出猜测性建议的常见问题。

Claude Code 还内置了**Bundled Skills**（`/run`、`/verify`、`/run-skill-generator`），这三个技能协同工作：run-skill-generator 记录项目的启动配方并提交为 per-project skill，之后 `/run` 和 `/verify` 就可以在清洁环境中复现启动过程，而不再依赖推断。这个设计解决了 AI Coding 工具最常见的一个痛点：Agent 无法可靠地启动复杂项目。

### 2.3 Subagents：独立上下文的委托机制

Subagents 允许在独立上下文窗口中运行专门的 Agent 任务。官方给出了典型使用场景：

- 将大型改动分解为独立单元，通过 `/batch` 在各自的 worktree 中运行
- 使用 `/code-review ultra` 在云端运行多 Agent 代码审查
- 通过 `/background` 将整个会话分离为后台 Agent

Subagents 也可以拥有自己的 auto memory，这意味着子 Agent 可以在多次调用间保持学习连续性。

### 2.4 Hooks：生命周期拦截点

Hooks 允许在特定生命周期事件发生时注入自定义逻辑。官方文档特别强调了一个关键用例：**"要阻止某个行为，不管 Claude 如何决定，使用 PreToolUse hook"**。这说明 Hooks 是 Claude Code 行为控制的最强制层——可以在 Tool 执行前进行拦截，而不是依赖 prompt 中的软性建议。

### 2.5 Rules：CLAUDE.md 的细粒度版本

Rules 允许将指令限定在特定文件类型或子目录范围内。存放在 `.claude/rules/` 目录下，每个规则文件对应特定路径模式。当 Agent 进入对应目录或操作对应类型文件时，相关规则自动激活。这解决了"项目规范"与"通用偏好"混在一处导致的上下文膨胀问题。

### 2.6 Output Styles：输出格式控制

Output Styles 允许定义 Agent 输出的格式规范，比如强制使用特定注释风格、文档模板等。这是行为引导中最细粒度的一层。

### 2.7 System Prompt 追加：兜底的硬编码控制

在所有机制都失效或不足的场景，可以通过直接追加 system prompt 来强制指定行为。这是最后一层，代价是每次会话都要重新注入，且会占用上下文空间。

---

## 三、七层机制的工程意义

笔者认为，Claude Code 这七层机制的设计反映了一个重要的工程判断：**Agent 行为调控必须分层，因为不同类型的行为规则有不同的变更频率和作用范围。**

项目架构是稳定的，所以放进 CLAUDE.md。编码规范可能因文件类型而异，所以需要 Rules。特定技能（如何运行这个项目、如何进行 code review）是可复用的，所以封装成 Skills。安全相关的强制约束必须拦截，所以需要 Hooks。

这种分层设计的工程价值在于：**每层机制都可以独立演进和版本化，而不会互相干扰。** 在一个多人协作的 Agent 项目中，IT/DevOps 可以管理 Managed Policy，Team Lead 管理 Project CLAUDE.md，Individual Developer 管理自己的 Skills 和 Local 配置——每层都有明确的 Owner 和变更流程。

相比之下，大多数 Agent 框架选择将所有行为规则塞进 system prompt 或一个全局配置里。当项目规模扩大，这种设计的维护成本会急剧上升。

---

## 四、与主流 Agent 框架的对比

| 维度 | Claude Code | LangChain Agents | CrewAI |
|------|-------------|-----------------|--------|
| 持久化行为规则 | CLAUDE.md + Rules + Managed Policy | Prompt 模板 | System Prompt |
| 可扩展技能 | Skills（标准格式，按需加载）| Tools（代码级集成）| Tools |
| 子任务委托 | Subagents（独立上下文）| Sub-agents / LangGraph | Agents |
| 生命周期拦截 | Hooks |Callbacks | — |
| 上下文分离策略 | 多文件 + 路径限定 | 单一 prompt | 单一 prompt |

笔者认为这个对比揭示了一个核心差异：Claude Code 把**行为调控**（steering）放在了架构核心位置，而大多数框架把**工具执行**（tool use）放在核心。这两种路线的取舍取决于使用场景——对于需要多人在同一项目中长期协作的场景，Claude Code 的分层 steering 机制更有优势；对于需要灵活编排多种工具的场景，LangChain 的 tool-first 设计更合适。

---

## 五、实践建议

基于以上分析，笔者给出以下判断：

**应该用 CLAUDE.md 的场景**：团队编码规范、项目架构决策、构建/测试命令、任何 Agent 第二次犯的同一个错误。

**应该用 Skills 的场景**：多步骤的标准操作流程（如部署、检查、code review）、需要动态注入当前状态的复杂任务、跨项目复用的专业技能。

**应该用 Hooks 的场景**：安全相关的强制约束（如禁止向上游服务发送敏感数据）、API key 保护、代码质量强制检查。

**应该用 Rules 的场景**：按文件类型区分的编码规范（如前端用 ESLint 配置，后端用特定 import 顺序）。

**不应该做的**：把所有规则都塞进 CLAUDE.md。这会导致上下文膨胀，使 Agent 难以在大量规则中找出当前任务相关的部分。Rules 和 Skills 正是为解决这一问题设计的。

---

## 结语

Claude Code 的七层行为引导机制，本质上是一套**系统化的 Agent 调控技术栈**。它的设计者显然花了很多精力思考"如何在多人协作的复杂项目中，让 Agent 的行为既可预测又可演进"这个问题。

笔者认为这代表了 AI Coding 工具的一个成熟方向：**从"调 prompt"的原始阶段，进化到"构建行为操作系统"的工程化阶段。** 当你在团队中使用 Claude Code，遇到 Agent 行为不一致的问题，首先应该问的不是"如何改 prompt"，而是"这个问题应该由哪一层机制来处理"。

这个问题的答案，往往比改 prompt 更持久。
