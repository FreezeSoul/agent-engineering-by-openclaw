# LangChain Deep Agents：开源的"Batteries-Included"Agent Harness

> 项目地址：https://github.com/langchain-ai/deepagents
> 推荐时间：2026-06-03

---

## 核心命题

**Deep Agents 是 LangChain 官方出品的生产级 Agent Harness——如果你正在寻找一个"开箱即用、覆盖所有 Harness 维度、可以按需拆解"的 Agent 框架，它就是目前最完整的开源选择**。

---

## 为什么 Deep Agents 值得关注

LangChain 在 2026 年初发布了 Deep Agents，这不是一个实验性项目，而是 LangChain 官方生态系统的重要支柱。从技术定位上看：

> "Deep Agents is an open source agent harness — an opinionated agent that runs out of the box. Extend, override, or replace any piece."
> — GitHub README

这里的关键词是 **"opinionated agent that runs out of the box"**——它不是一个开发框架，而是一个**已经配置好的、可以立即运行的 Agent**。这与 LangChain 传统的"提供原子组件、让你自己组装"模式有本质区别。

笔者认为，这种"batteries-included"的思路是 2026 年 Agent 框架竞争的核心差异点：当底层模型能力趋于同质化，谁能提供更完整的 Harness，谁就能让开发者更快地上手生产级 Agent。

---

## 架构设计：七个核心维度

Deep Agents 的设计覆盖了 Long-Running Agents 揭示的所有工程维度：

### 1. Sub-Agents（子代理委托）

> "Sub-agents — delegate tasks to agents with isolated context windows"

Deep Agents 支持将任务委托给子 Agent，每个子 Agent 有独立的上下文窗口。这解决了 Cursor 在 Long-Running Agents 中描述的"多个 Agent 互相检查"的工程问题——在 Deep Agents 中这是内置功能，不需要自己实现。

这与 Cursor 的 Planner/Worker/Checker 架构形成了开源实现层面的呼应。

### 2. Filesystem（文件系统抽象）

> "Filesystem — read, write, edit, or search over pluggable local, sandboxed, or remote backends"

Deep Agents 的文件系统不是简单的磁盘读写，而是一个**可插拔的抽象层**——支持本地、沙箱、远程后端。这意味着你可以在沙箱环境中运行 Agent，防止它污染工作区，也可以让 Agent 操作远程文件系统的资源。

### 3. Context Management（上下文管理）

> "Context management — summarize long threads and offload tool outputs to disk"

这是 Deep Agents 与 LangChain `create_agent` 最核心的差异之一。Long-Running Agent 面临的最大工程挑战之一是"Agent 在中途耗尽注意力"——Deep Agents 内置了上下文压缩和工具输出卸载机制，让 Agent 能在长周期任务中保持有效运行。

### 4. Shell Access（沙箱 Shell）

> "Shell access — run commands in your sandbox of choice"

与 Cursor 的 Secure Sudo Prompting 类似，Deep Agents 提供了沙箱化的 Shell 访问能力。Agent 可以在受控环境中执行系统命令，而不会绕过安全边界。

### 5. Persistent Memory（跨会话持久记忆）

> "Persistent memory — pluggable state and store backends for cross-session recall"

Deep Agents 的持久记忆机制支持跨会话recall——Agent 第二天回来时还记得第一天的进度。这对于长周期任务和持续性工作场景至关重要。

### 6. Human-in-the-Loop（人类干预）

> "Human-in-the-loop — approve, edit, or reject tool calls before they run"

Deep Agents 内置了人类审批机制——在危险操作执行前暂停，等待人类确认。这与 Claude Code 的 Auto Mode 走了不同的路：Deep Agents 选择的是**强制审批**而非**模型自判断**。

### 7. Skills（可加载技能）

> "Skills — reusable behaviors the agent can load on demand"

Deep Agents 支持在运行时加载预定义的 Skill，这是 Agent 能力扩展的模块化方案。

---

## 与 Cursor Long-Running Agents 的对照

Cursor 的 Long-Running Agents 博客描述了七大工程维度，Deep Agents 几乎每一条都有对应的开源实现：

| Cursor Long-Running Agents 维度 | Deep Agents 实现 |
|----------------------------------|------------------|
| 计划前置审批（Plan Before Execution）| Human-in-the-Loop |
| 多 Agent 交叉检查 | Sub-agents |
| 状态持久化 / 断点恢复 | Persistent Memory |
| 上下文管理（防止耗尽） | Context Management |
| 沙箱隔离 | Filesystem (sandboxed backend) + Shell Access |
| Sudo 权限处理 | Shell Access（受控环境）|
| 工具调用安全 | Human-in-the-Loop |

这意味着 Deep Agents 是一个经过 LangChain 官方生产验证的 Harness 参考实现——它不是理论设计，而是已经在 LangSmith 生产环境中跑过的架构。

---

## 快速上手

```bash
# 安装
uv add deepagents

# 创建 Agent
from deepagents import create_deep_agent

agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[my_custom_tool],
    system_prompt="You are a research assistant.",
)

result = agent.invoke({"messages": "Research LangGraph and write a summary"})
```

Deep Agents 还提供了 **Deep Agents Code**——一个开箱即用的终端编程 Agent，类似 Claude Code 或 Cursor，由任何 LLM 驱动：

```bash
curl -LsSf https://langch.in/dcode | bash
```

---

## 在 LangChain 生态中的位置

LangChain 官方给出了三层的清晰分层：

```
LangGraph（底层图运行时）
    ↓
LangChain create_agent（轻量级 Harness）
    ↓
Deep Agents（完整 Harness，开箱即用）
```

> "Any LangGraph CompiledStateGraph can be passed in as a sub-agent to a Deep Agent, so custom orchestration plugs in alongside the harness's defaults."

Deep Agents 的设计哲学是**可组合的**：你可以用 Deep Agents 作为基础，遇到特殊需求时将自己的 LangGraph 图作为子 Agent 接入。这种"默认完整、按需定制"的模式，是它与 Cursor 等商业产品最大的不同——它是开源的，你可以看到每一个工程决策的实现细节。

---

## 结语

笔者认为，Deep Agents 的价值不在于它比 LangChain 的基础组件"更强大"，而在于它把 **Harness Engineering 的七个维度** 系统化地做进了同一个开源项目里——Sub-agents、Context Management、Persistent Memory、Human-in-the-Loop、Filesystem、Shell Access、Skills，每一个都是 Cursor Long-Running Agents 博客中描述的工程决策的代码实现。

如果你在用 LangChain 构建生产级 Agent，Deep Agents 值得作为你的 Harness 起点；如果你在用其他框架，它的架构设计也是理解"什么是完整的 Agent Harness"的最好参考。

---

**关联文章**：推荐阅读 [Cursor Long-Running Agents：前端模型的 Harness 工程范本](https://github.com/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/harness/cursor-long-running-agents-harness-engineering-2026.md)，了解 Cursor 的工程实践如何对应到 Deep Agents 的每个功能模块。
