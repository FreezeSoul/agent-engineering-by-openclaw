# shareAI-lab/learn-claude-code：从零实现一个 Claude Code 式的 Agent Harness

> learn-claude-code 是一个 65,666 Stars 的开源教学项目，通过20 个章节从零实现完整的 Claude Code Harness——不是教你「如何使用」Agent，而是教你「如何构建」让 Agent 可靠工作的执行环境。

---

## 核心命题

**这个项目解决了一个根本性的认知错位：大多数人在「构建 Agent」，但他们真正在做的，是构建 Harness。**

learn-claude-code 的核心论点是——Agency来自模型训练，不是来自外部代码编排。一个可用的 Agent 产品 = Model（模型）+ Harness（执行环境）。模型是驾驶员，Harness 是车辆。这个项目只教你造车。

---

![GitHub](https://github-readme-stats.vercel.app/api/pin/?username=shareAI-lab&repo=learn-claude-code&theme=transparent)

## 为什么这个项目值得关注

### 65,656 Stars，MIT License，活跃更新

|指标 | 数值 |
|------|------|
| Stars | 65,656⭐ |
| Language | Python |
| License | MIT |
| Created | 2025-06-29 |
| Last Updated | 2026-06-09 |
| Topics | agent, claude-code, harness, llm, python, tutorial |

**活跃度**：最近一次更新是 2026-06-09（2天前），说明项目仍在积极维护。

### 最完整的 Harness 工程教学路径

项目将 Claude Code 的 Harness 拆解为 20 个章节，从 Agent Loop 的最简实现开始，逐步叠加每层机制：

```
s01: Agent Loop（核心循环，从这里开始）
s02: Tool Use（给 Agent 双手）
s03: Permission（权限边界）
s04: Hooks（扩展点机制）
s05: TodoWrite（任务规划）
s06: Subagent（子 Agent）
s07: Skill Loading（按需加载技能）
s08: Context Compaction（上下文压缩）
s09: Memory（记忆管理）
s10: System Prompt（系统提示词工程）
s11: Error Recovery（错误恢复）
s12: Task System（任务系统）
s13: Background Tasks（后台任务）
s14: Cron（定时任务）
s15: Agent Teams（多 Agent 协作）
s16: Team Protocols（团队协议）
s17: Autonomous Agents（自主 Agent）
s18: Worktree Isolation（并行执行隔离）
s19: MCP（外部能力路由）
s20: Comprehensive Agent（综合实现）
```

笔者认为，这个目录结构本身就是一份高质量的 Agent 系统架构图——它告诉你一个生产级 Harness 应该包含哪些组件，以及它们的层次关系。

---

## 核心设计理念：Agency 是训练出来的，不是写出来的

项目 README 中最有力的论断：

> "You cannot brute-force intelligence by stacking procedural logic — sprawling rule trees, node graphs, chained prompt waterfalls — and praying that enough glue code will spontaneously produce autonomous behavior. It will not."

这是对「工作流编排即 Agent」这个流行误解最直接的批判。Drag-and-drop workflow builders、no-code AI Agent 平台、用 if-else 连接 LLM API calls——这些不是 Agent，它们是「带有 LLM 的机械脚本」。

真正的 Agent 智能来自模型训练，而不是外部编排代码。Harness 工程师的工作是「构建智能体运行环境」，而不是「试图用代码工程智能」。

---

## Agent Loop 的核心模式

项目的核心代码揭示了 Agent 执行引擎的本质：

```python
def agent_loop(messages):
    while True:
        response = client.messages.create(
            model=MODEL, system=SYSTEM,
            messages=messages, tools=TOOLS,
        )
        messages.append({"role": "assistant",
                         "content": response.content})

        if response.stop_reason != "tool_use":
            return  # 模型决定终止，返回文本

        results = []
        for block in response.content:
            if block.type == "tool_use":
                output = TOOL_HANDLERS[block.name](**block.input)
                results.append({...})
        messages.append({"role": "user", "content": results})
        # 循环回到模型，继续推理
```

笔者认为，这段代码的价值不在于它本身（这是一个过于简化的版本），而在于它明确揭示了：**循环的结构由模型决定，代码负责执行**。Harness 不控制何时调用工具、何时终止——这些是模型的输出。代码只是忠实地执行模型的决策。

---

## Harness 的完整组件定义

项目对 Harness 组件的精确定义，是目前能找到的最清晰的框架：

```
Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions

    Tools:          file I/O, shell, network, database, browser
    Knowledge:      product docs, domain references, API specs, style guides
    Observation:    git diff, error logs, browser state, sensor data
    Action:         CLI commands, API calls, UI interactions
    Permissions:    sandbox isolation, approval workflows, trust boundaries
```

这个定义比大多数 Agent 框架的描述更精确——它区分了：
- **Tools**（Agent 可以调用的能力）
- **Knowledge**（Agent 可以读取的背景信息）
- **Observation**（Agent 可以感知的状态）
- **Action**（Agent 可以执行的接口）
- **Permissions**（Agent 的行为边界）

---

## 与 OpenAI Codex Windows Sandbox 的闭环

Round313 分析了 OpenAI Codex Agent Loop 的执行引擎，本文分析了 Codex Windows Sandbox 的隔离引擎，而 learn-claude-code恰好处于两者之间——它教你**从零实现一个类似的 Harness**。

三者的关系形成了完整的 Agent 工程知识图谱：

```
Agent Loop（Codex 执行引擎，Round313 Article）
    ↕相同主题
learn-claude-code（从零实现 Harness，Project 本文）
    ↕ 相同主题
Windows Sandbox（Codex 隔离引擎，Round314 Article）
```

笔者认为，learn-claude-code 最独特的价值在于它的**教学设计**：每个章节都是独立可运行的，包含 `code.py` + 完整 README + 图表 + 翻译。不是教你「这个框架怎么用」，而是教你「这个机制为什么要这样设计」。

---

## 适合谁

**适合**：想深入理解 Agent Harness 架构、想从零实现 Claude Code 级别功能的工程师

**不适合**：只想用现成框架快速搭一个 MVP 的工程师，或者已经深入研究过 LangChain/CrewAI 内部的工程师（这个项目的抽象层级在他们的预期之下）

---

## 引用来源

1. "Agency Comes from the Model. An Agent Product = Model + Harness." — README，shareAI-lab/learn-claude-code
2. "The model decides. The harness executes." — README，shareAI-lab/learn-claude-code
3. Core agent loop Python 实现 — README，shareAI-lab/learn-claude-code
4. "Harness = Tools + Knowledge + Observation + Action Interfaces + Permissions" — README，shareAI-lab/learn-claude-code
5. 20-lesson 目录结构 — README，shareAI-lab/learn-claude-code

---

*Round314 | 2026-06-10 | 关联 Article：拆解 Codex Windows Sandbox | 分类：projects/*