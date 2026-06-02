# vstorm-co/pydantic-deepagents：Python 版 Claude Code 深度 Agent 框架

**推荐理由**：`pydantic-deepagents` 在 Pydantic AI 上构建 Claude Code 风格的深度 Agent，支持工具调用、沙箱执行、多 Agent 团队、Skills、Checkpoints 和无限上下文。为 Python 开发者提供了一条从原型到生产级深度 Agent 的清晰路径。

**关联 Article**：LangSmith Sandboxes 架构模式

---

## 基本信息

| 指标 | 数值 |
|------|------|
| GitHub | `vstorm-co/pydantic-deepagents` |
| Stars | 832 |
| 语言 | Python |
| 主题 | agent-framework, ai-agents, anthropic, claude-code, cli, coding-agent, deep-research, docker-sandbox |

## 核心能力

`pydantic-deepagents` 提供完整的深度 Agent 技术栈：

- **Tool Calling**：标准化的工具调用接口，与 Claude Code 兼容
- **Sandboxed Execution**：Docker 沙箱隔离执行，确保安全
- **Multi-Agent Teams**：多 Agent 协作，支持分工和层级
- **Skills System**：Agent Skills 可复用技能模块
- **Checkpoints**：中间状态保存，支持恢复和回溯
- **Unlimited Context**：突破上下文长度限制，处理长任务

```
Deep Agent → Pydantic AI → Tool Calling + Sandboxed Exec + Multi-Agent + Skills + Checkpoints
```

## 技术栈

基于 Pydantic AI 框架构建，提供类型安全的 Agent 开发体验：

```python
from pydantic_ai import Agent
from pydantic_deepagents import sandbox, skills

agent = Agent(
    model='claude-sonnet-4',
    tools=[sandbox.docker(), skills.file_operations()],
    max_context_tokens=200_000
)
```

## 为什么值得推荐

1. **Claude Code 兼容**：复现 Claude Code 的核心能力（深度执行、工具调用、沙箱隔离）
2. **Python 原生**：为 Python 开发者提供构建深度 Agent 的首选框架
3. **沙箱安全**：Docker 隔离执行，可运行不可信代码
4. **生产就绪**：从 Checkpoints 到 Multi-Agent，提供企业级功能
5. **活跃主题**：coding-agent、deep-research、docker-sandbox 等热门方向

## 与 LangSmith Sandboxes 的互补性

LangSmith Sandboxes 解决的是「执行环境隔离」问题，`pydantic-deepagents` 解决的是「如何构建能在隔离环境中运行的深度 Agent」问题。两者组合：LangSmith Sandboxes（WHERE to run）+ pydantic-deepagents（HOW to build the agent）。

---

**引用来源**：
- GitHub: `https://github.com/vstorm-co/pydantic-deepagents`