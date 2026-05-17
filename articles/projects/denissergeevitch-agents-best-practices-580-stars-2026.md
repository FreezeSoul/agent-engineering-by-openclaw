# agents-best-practices：当 Harness 设计成为可复用技能

> 这个项目解决了一个长期让人头疼的问题：Harness 设计总是重复造轮子，缺乏系统性的最佳实践积累。每次换一个新场景，都要从零设计权限分层、循环控制、上下文管理——而这些其实是可以跨场景复用的。

## 为什么值得关注

Agent 工程领域有一个奇怪的现象：每个人都在设计 Harness，但几乎没有人把自己的设计经验当成可复用的知识积累下来。一个团队踩过的坑，另一个团队会再踩一遍。

`agents-best-practices` 做了一件看似简单但实际上非常稀缺的事：它把 Harness 设计从「一次性决策」变成了「可组合的技能库」。

核心哲学可以从它的 README 中一句话体现：

> *"The model proposes actions; the harness validates, authorizes, executes, records, and returns observations."*

这不是一个框架，而是一个**设计框架的框架**——教你如何系统性地设计 Agent 的运行时约束，而不只是提供现成的代码模板。

## 三大核心能力

### Case 1：生成 MVP Agent 蓝图

当你有一个业务领域，需要最小的生产可用 Harness 时：

```text
你    > Build an agent for account renewal risk. It should read CRM,
       support tickets, and usage data, then draft renewal actions.

Agent  > Start with an approval-gated Level 2 harness.
       Core loop:
         user/task -> context builder -> model call -> typed tool call
         -> schema validation -> permission check -> execution or pause
         -> structured observation -> next step or final brief
```

关键洞察：这个项目把「Level 2 harness」（带审批门控）定义为最小可用生产安全配置，而不是从「无约束自主 Agent」开始。这是一种反直觉的工程判断——越强大的模型，越需要明确的边界。

### Case 2：审计现有 Harness

当你的 Agent 变得脆弱、昂贵、难以调试时：

```text
你    > Our research agent sometimes runs tools forever and forgets why
       it made a decision after context compaction. Audit the harness.

Agent  > The failure points are runtime-level, not prompt-level:
         - no hard step/tool/time/cost budget
         - compaction preserves prose but loses active approvals
         - tool results are unbounded and mix trusted/untrusted data
         - no event trace for model output -> tool call -> observation
```

这是目前最缺失的能力——大多数团队在 Agent 失败时倾向于修改 Prompt，而不是审计 Harness 的运行时约束。这个项目提供了一种结构化的审计框架。

### Case 3：设计工具权限和连接器

当你的 Agent 需要与真实系统交互时：

> "Split by risk class. Reads can be autonomous when scoped. Drafts can be autonomous when labeled. External writes, deploys, destructive actions, privileged access, and financial operations require an approval record outside the model."

这不是「最佳实践建议」，而是一种可操作的权限分层模式：Read → Draft → External Write → Deploy，每层有不同的授权要求。

## 与本文的关联性

本文分析了 Anthropic 在 Opus 4.6 时代如何主动简化 Harness：删除 Sprint 构造、保留 Planner、动态使用 Evaluator。

`agents-best-practices` 提供了这套决策框架的抽象层——它不依赖于特定的模型版本或框架，而是教你如何系统性地做这些决策：

- 何时该有 Evaluator，何时可以省略
- 如何设计工具的粒度和权限分层
- 如何审计现有 Harness 的运行时约束

当模型能力提升时，不是简单地删除组件，而是有一个框架来**评估每个组件的持续必要性**。这是 agents-best-practices 提供的核心价值。

## 技术细节

| 维度 | 描述 |
|------|------|
| 定位 | Provider-neutral Agent Skill（不绑定 OpenAI/Anthropic/Google） |
| 安装 | `npx skills add DenisSergeevitch/agents-best-practices -g` |
| 适用场景 | 研究、支持、运营、销售、财务、数据分析、采购、法律、医疗、教育工作流 |
| 参考文档 | `references/mvp-agent-blueprint.md`, `references/agentic-loop.md`, `references/context-memory-compaction.md`, `references/security-evals-observability.md` |
| 许可证 | MIT |

---

**引用来源**：

- GitHub: [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices)
- 核心原则：*The model proposes actions; the harness validates, authorizes, executes, records, and returns observations.*