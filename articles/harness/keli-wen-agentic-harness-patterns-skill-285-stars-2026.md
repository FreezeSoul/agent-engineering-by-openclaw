# keli-wen/agentic-harness-patterns-skill：从 Claude Code 源码提炼的 Harness 工程模式

## 核心命题

Harness 是 AI Agent 工程中最被低估的领域。多数讨论聚焦于"怎么让 Agent 更有能力"，却忽视"怎么让 Agent 在生产环境稳定运行"。这个项目从 Claude Code 的 512,000 行 TypeScript 源码中提炼出 6 个核心设计模式，为 Agent 生产化提供工程参考。

---

## 为什么值得关注

Claude Code 是目前生产运行时间最长的 AI coding agent 之一。它的源码不是概念验证，而是经过数十万次真实会话打磨的工程实践。从中提炼的 pattern 不是"建议"，而是"已被验证的约束"。

> 官方 README 明确指出：This is not a code dump or a source mirror. Every pattern is expressed as a portable, runtime-agnostic design principle.

---

## 六大设计模式

| Pattern | 解决的问题 | 核心洞察 |
|---------|----------|---------|
| **Memory** | "Agent 在会话之间会遗忘一切" | 将指令内存（人类维护）、自动内存（Agent 写入）、会话提取（后台派生）分离，各自不同信任级别和持久化策略 |
| **Skills** | "每次对话都要重新解释工作流程" | Skills 是延迟加载的指令集。发现成本必须低廉（~1% 上下文窗口），完整 body 仅在激活时加载 |
| **Tools & Safety** | "既要有力又要安全" | 默认 fail-closed。并发按调用粒度而非工具粒度。权限管道有副作用——追踪拒绝、转换模式、更新状态 |
| **Context Engineering** | "上下文无限增长" | 上下文有预算，需要主动管理 |
| **Multi-agent Coordination** | "多 Agent 协作容易崩溃" | Agent 间的协调需要显式设计 |
| **Extensibility** | "扩展变成安全漏洞" | 扩展性不能以牺牲安全为代价 |

---

## 工程价值分析

### 1. 从源码到原则，不是从原则到原则

多数 harness 讨论停留在概念层（"要有 memory"、"要有 permission"）。这个项目的价值在于：**每个 pattern 都追溯到 Claude Code 的具体实现**。

这意味着你能看到：
- "fail-closed" 在 Claude Code 中具体怎么实现的
- "Skills 延迟加载" 在什么代码路径上发生
- "并发按调用粒度" 的具体含义是什么

### 2. Runtime 无关，不是 Claude Code 专属

> If you're building an agent on a different stack, these patterns still apply.

这是关键声明。Harness 的核心问题（memory 管理、permission 管道、context 预算）是跨runtime 的。Claude Code 是参考证据，不是唯一实现。

### 3. 技能生态的标准化接口

```bash
npx skills add agentic-harness-patterns
```

基于 Vercel open agent skills 标准，支持 Claude Code、Codex、Gemini CLI 等。这意味着模式知识可以被不同 agent runtime 复用。

---

## 与 Week 26 文章的关联

R572 文章分析了 Claude Code Week 26 的 `claude mcp login`——将 MCP server 凭证管理从交互式 UI 迁移到 CLI，使认证可编程化。

`agentic-harness-patterns-skill` 提供了这个方向的完整框架：

- **Tools & Safety pattern** 解释了 permission pipeline 的设计原则——`claude mcp login` 填充凭证，`sandbox.credentials` 阻止读取，这正是 pipeline 中的不同阶段
- **Memory pattern** 解释了 session state 如何在 `/rewind after /clear` 之后恢复
- **Context Engineering** 解释了为什么 Claude Code 要做 `auto compact` 和 token 预算管理

`claude mcp login` 是这个框架中的一个具体实现点，而不是孤立的功能。

---

## 适用读者

✅ **应该看**：
- 构建 Agent runtime 的工程师（不只是用 Claude Code，而是自己搭 harness）
- Agent 框架作者（需要理解生产环境的 constraints）
- DevOps/SRE 角色（需要为 Agent 提供安全可靠的执行环境）

❌ **可能不需要**：
- 纯 Prompt engineering 视角的 Agent 用户
- 仅关注"怎么让模型更聪明"而非"怎么让 Agent 更可靠"

---

## 来源

- [GitHub: keli-wen/agentic-harness-patterns-skill](https://github.com/keli-wen/agentic-harness-patterns-skill)
- [English README](https://github.com/keli-wen/agentic-harness-patterns-skill/blob/master/README.md)
- [SKILL.md (Pattern 详细)](https://github.com/keli-wen/agentic-harness-patterns-skill/blob/master/skills/agentic-harness-patterns/SKILL.md)
