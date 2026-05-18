# humanlayer/12-factor-agents：让 LLM 应用从"感觉不错"到"能上生产"

**这个项目解决了一个长期让人头疼的问题**：大多数标榜"AI Agent"的产品，实际上只是"在正确位置撒了点 LLM 魔法粉"的确定性软件。真正的问题是——**什么原则才能让 LLM 应用达到能交给生产用户的质量**？

---

## 为什么这个项目值得关注

作者 Dex 是资深的 Agent 构建者，访谈过大量 YC 创始人后发现一个反直觉的现象：

> *"Most of the products out there billing themselves as 'AI Agents' are not all that agentic. A lot of them are mostly deterministic code, with LLM steps sprinkled in at just the right points to make the experience truly magical."*

12-factor-agents 试图回答的核心问题是：**如何构建真正达到生产质量的 LLM 软件**？借鉴 12 Factor App 的思路，它提出了 12 条核心原则。

---

## 核心洞察：从 Agent Loop 重新理解软件

项目的核心洞察是把传统 Agent Loop 显式化：

```python
initial_event = {"message": "..."}
context = [initial_event]
while True:
  next_step = await llm.determine_next_step(context)
  context.append(next_step)

  if (next_step.intent === "done"):
    return next_step.final_answer

  result = await execute_step(next_step)
  context.append(result)
```

然后指出这个模式的问题——**它太简单了**。真实场景中需要考虑：状态管理、上下文窗口管理、错误恢复、人机协作、控制流等等。

---

## 12 条原则速览

| Factor | 核心思想 |
|--------|---------|
| Factor 1 | NL to Tool Calls — 自然语言转结构化工具调用 |
| Factor 2 | Own your prompts — 把提示词当作代码而非配置 |
| Factor 3 | Own your context window — 主动管理上下文而非被动填充 |
| Factor 4 | Tools are structured outputs — 工具调用本质是结构化输出 |
| Factor 5 | Unify execution and business state — 执行状态与业务状态统一 |
| Factor 6 | Launch/Pause/Resume — 支持可中断的 API 而非长时运行 |
| Factor 7 | Contact humans with tools — 人机协作通过工具调用而非直接等待 |
| Factor 8 | Own your control flow — 控制流由软件控制而非委托给 LLM |
| Factor 9 | Compact errors into context — 错误信息需要压缩后注入上下文 |
| Factor 10 | Small, focused agents — 多个小 Agent 比一个大 Agent 更可控 |
| Factor 11 | Trigger from anywhere — 从任意位置触发，适应用户所在之处 |
| Factor 12 | Stateless reducer — Agent 是无状态的 reducer，而非有记忆的实体 |

---

## 笔者的判断：框架之外的设计原则

很多 Agent 开发者（包括我自己）容易犯的错误是：**过度依赖框架，把质量寄托在"框架会越来越强"上**。

12-factor-agents 提供了另一种思路——**即使不用任何框架，你也可以通过遵循这些设计原则来构建可靠的 Agent 软件**。反过来说，即使用了最好的框架，如果这些原则没遵守，Agent 也很难达到生产质量。

特别值得关注的是 **Factor 8（Own your control flow）** 和 **Factor 9（Compact errors into context）**——这两个因子直接回应了实际生产中最常见的崩溃场景：LLM 在错误处理中迷失方向、上下文窗口被错误信息撑爆。

---

## 数据与可用性

- **Stars**：20,283 ⭐（Trending 认可）
- **许可证**：Apache 2.0（代码）+ CC BY-SA 4.0（内容）
- **平台**：提供 `npx/uvx create-12-factor-agent` 快速上手脚手架
- **社区**：Discord 活跃，有 YouTube deep dive 视频

---

## 引用

> *"The fastest way I've seen for builders to get good AI software in the hands of customers is to take small, modular concepts from agent building, and incorporate them into their existing product"* — humanlayer/12-factor-agents

> *"Agents, at least the good ones, don't follow the 'here's your prompt, here's a bag of tools, loop until you hit the goal' pattern. Rather, they are comprised of mostly just software."* — humanlayer/12-factor-agents

---

**Related Links**：
- [GitHub Repo](https://github.com/humanlayer/12-factor-agents)
- [Discord Community](https://humanlayer.dev/discord)
- [YouTube Deep Dive](https://www.youtube.com/watch?v=8kMaTybvDUw)