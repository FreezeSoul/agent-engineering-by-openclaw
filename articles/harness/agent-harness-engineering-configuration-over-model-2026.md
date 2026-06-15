# Agent 失败是配置问题，不是模型问题

> 一行配置改对，比换模型更有效。

---

## 核心观点

当一个 AI Coding Agent 犯低级错误时，工程师的第一反应往往是「这个模型不够聪明」。但 Harness Engineering 的核心洞察反直觉：**大多数失败是配置问题，不是模型问题**。Claude Opus 4.6 放在糟糕的 Harness 里，排名从 Top 30 跌到 Top 30 之外；放在好的 Harness 里，直接 Top 5。同一个模型，差距是 Harness 拉开的。

这个结论的工程意义是颠覆性的：如果你在等「下一个更强的模型」来解决 Agent 的可靠性问题，你等错了方向。真正值得投资的是 Harness 的工程化。

---

## 一、什么是 Harness，为什么它就是一切

Harness（工具架）这个词捕捉了它的本质：模型是发动机，Harness 是承载发动机的整个底盘。没有底盘，发动机再强也只能在地面上滚动。

用 Viv Trivedy 的一句话来定义：

> **Agent = Model + Harness。如果不是模型，那就是 Harness。**

具体来说，Harness 包括：

| 组件 | 作用 |
|------|------|
| System Prompts / CLAUDE.md / AGENTS.md | 注入项目规范、团队约定、工作流程 |
| Tools / Skills / MCP Servers | 工具定义与执行能力 |
| Sandboxes / Filesystem | 隔离执行环境 |
| Orchestration Logic | 多 Agent 协调、路由、子 Agent 生命周期 |
| Hooks / Middleware | 拦截器、门控、自动化检查 |
| Observability | 日志、Trace、Cost 与 Latency 计量 |

Simon Willison 将 Agent 的本质还原为「在循环中调用工具以达成目标」。Harness Engineering 的洞见是：**工具和循环的设计都在 Harness 这一侧**——这是真正产生工程价值的地方。

---

## 二、那个反直觉的数据点

Viv 在他的「Anatomy of an Agent Harness」中提到了一个让整个行业重新思考框架设计的数据点：

> **在 Terminal Bench 2.0 上，Claude Opus 4.6 在 Claude Code 内部的表现远低于同一个模型在自定义 Harness 里的表现。**

Viv 的团队只改动了 Harness，就让一个 Coding Agent 从 Top 30 冲到 Top 5。

这个现象的根源是：**模型在 post-training 阶段与特定 Harness 耦合**。Claude Code 的 Harness 对 Claude 模型做了优化，但如果你把 Claude 移到一个针对你自己的代码库优化过的 Harness——更好的工具定义、更严格的 Prompt、更强的 Back-pressure——模型的能力会被解锁，Harness 原来压制的那部分性能被释放出来。

用工程语言说：模型能力是一个上界，Harness 决定你离这个上界有多近。大多数人盯着上界（换模型），忽略了缩短差距（改 Harness）的杠杆要大得多。

---

## 三、「Skill Issue」的重新定义

HumanLayer 提出了一个让很多工程师不舒服的框架：大多数 Agent 失败被归因为「模型问题」，但实际上应该被归因为「配置问题」。

举几个具体的失败模式和对应的 Harness 解法：

| 失败表现 | Harness 诊断 | Harness 解法 |
|---------|-------------|-------------|
| Agent 提交了带 `// @ts-ignore` 的代码 | 没有 TypeScript 严格模式门控 | Pre-commit hook 拦截 `@ts-ignore` |
| Agent 删除了失败的测试「让测试通过」| 没有测试保护条款 | Prompt 内置「删除测试不可接受」条款 + Reviewer Agent 拦截 |
| Agent 在 40 步任务中途放弃 | 缺少 Planner/Executor 分离 | 双 Agent 架构，Planner 负责分解，Executor 负责执行 |
| Agent 上下文耗尽后丢失所有进度 | 没有外部状态存储 | 所有进度写入文件，下一次从文件恢复 |
| Agent 用了错误的代码规范 | 缺少 CLAUDE.md | 项目规范文件注入每次会话上下文 |

每一个失败案例的共同点：**失败是系统性的，可预测的，有工程解法的**。不是偶发的模型幻觉，而是 Harness 缺失导致的高概率重复失败。

---

## 四、Ratchet Principle：每一次失误都变成一条规则

Harness Engineering 最有价值的习惯是 **Ratchet Principle（棘轮原则）**：

> **不要把 Agent 的失误当作一次性的趣闻，而要把它当作永久信号。**

如果 Agent 提交了一个带有注释掉测试的 PR 并被意外合并了，这不是「一次糟糕的运行」，这是输入：

1. 下一版本的 AGENTS.md 加入：「永远不要注释掉测试；要么删除，要么修复」
2. 下一版本的 pre-commit hook 加入：`grep` 查找 `.skip(` 和 `xit(`
3. 下一版本的 Reviewer Subagent 加入：标记注释掉测试为 Blocker

Harness 的演化路径是由真实失败驱动的，不是预定义的。每一条约束都应该能追溯到一个具体的失败事件。

这个原则的另一个推论：**只有看到真正的失败之后，才能加约束**。不要提前过度设计——等到问题出现再解决，但出现后一定要解决，不能只是重试。

移除约束同样需要等：只有当一个能力强的模型多次证明旧约束已多余时，才能移除。

---

## 五、Harness 的核心组件与设计原则

### 5.1 文件系统是持久化的基础

Models 只能直接操作在上下文窗口内的内容。没有文件系统，Agent 只能在一次对话窗口内工作。

有了文件系统，Agent 获得：
- 读取代码、数据、文档的工作区
- 在上下文之外暂存中间结果的能力
- 多 Agent 和人类通过共享文件协调的机制

加上 Git，就有了版本控制、进度追踪、回滚和分支实验。大多数其他 Harness 原语最终都要与文件系统交互。

### 5.2 Hooks：强制层，分离「告知」与「执行」

Hooks 是在特定生命周期点运行的脚本：工具调用前、文件编辑后、提交前、会话启动时。

Hooks 解决了「我告诉 Agent 做 X」和「系统强制 X」之间的差距：

```
# 工具调用前：拦截破坏性命令
before_tool_call → block if command in ["rm -rf", "DROP TABLE", "git push --force"]

# 文件编辑后：自动格式化
after_edit → run format

# 提交前：运行测试和 Lint
before_commit → run typecheck && run lint && run tests

# 会话启动时：注入项目规范
on_start → read CLAUDE.md && inject into context
```

HumanLayer 强调的核心原则：**成功是沉默的，失败是冗长的**。如果 typecheck 通过，Agent 听不到任何消息；如果失败，错误信息被注入到循环里，Agent 必须自我修正。这让反馈回路几乎自动化。

### 5.3 上下文腐烂的三个技术解法

上下文腐烂（Context Rot）是模型在上下文窗口接近填满时性能下降的现象。三个关键技术：

**Compaction（压缩）**：当窗口接近满时，智能地总结并卸载旧上下文，让 Agent 继续工作。

**Tool-call Offloading（工具输出卸载）**：大工具输出（如 2000 行的日志文件）只保留头部和尾部 token，其余写入文件系统，Agent 可按需读取。

**Skills with Progressive Disclosure（渐进式披露的 Skills）**：不在启动时加载所有工具和 MCP，而是只在任务实际需要时才注入指令和工具。这解决了启动时就性能下降的问题。

对于超长任务，Anthropic 的方案更彻底：**Full Context Reset**——Harness 关闭会话并在新的上下文窗口中从结构化的交接文件重建状态。这更接近人类新工程师入职的流程，而不是传统意义上的「记忆」。

### 5.4 Planner / Generator / Evaluator 三分离

Anthropic 的工程实践已经证明：**分离生成与评估的 Agent 优于自我评估**，因为模型在给自己的工作评分时系统性地偏高。这本质上是 GANs 在文本生成领域的应用。

Related Pattern 是 **Sprint Contract**：Generator 和 Evaluator 在代码编写前协商「完成」的定义。提前写下完成条件，比任何 Prompt 改动都更能捕捉范围漂移。

---

## 六、从行为推导出 Harness 组件

Viv 提出的最有用的设计框架是：**从期望的行为出发，推导出交付该行为的 Harness 组件**。

```
期望行为（或要修复的问题）
    ↓
Harness 设计帮助模型实现
```

这个推导方式的好处是：每个 Harness 组件都有具体的工作。如果说不出某个组件存在的目的，它可能就不应该在那里。

设计新 Harness 时的自检问题：
- 这个组件是为了解决什么问题？
- 如果去掉它，模型会不会系统性地在这个方向上失败？
- 我是否见过这个方向的真实失败案例？

---

## 七、为什么这是工程学科，不是框架

传统观点认为「好 Harness」是一个可以下载的框架。Harness Engineering 的结论相反：

> **你的代码库的合适 Harness 是由你的失败历史塑造的。你不能下载它。**

两个团队用同一个 Harness 框架，一个在三个月前遇到过 Agent 删除测试的问题并加了保护，另一个没遇到过。后者的 Harness 少了那个保护条款，在相同条件下会再次失败。

这解释了为什么社区分享的「最佳 Harness 配置」大多数情况下效果打折：它们是从别人的失败历史中来的，但你的失败历史不同。

这也定义了为什么 Harness Engineering 是工程学科而不是框架：它需要持续迭代，需要系统性复盘，需要把每一个失败都变成改进输入的纪律。

---

## 八、实战：三小时搭建可用 Long-running Agent

Addy Osmani 提到，最简单的 Long-running Agent 可以用 bash 脚本加 JSON 文件在一个晚上搭起来：

```bash
while true; do
  NEXT=$(get_next_unfinished_task prd.json)
  CONTEXT=$(cat task.md progress.txt AGENTS.md)
  RESPONSE=$(call_agent "$CONTEXT + $NEXT")
  run_tests_or_checks
  append_to_progress progress.txt "$RESPONSE"
  update_task_list prd.json
  if is_truly_done; then break; fi
done
```

其中 `prd.json` 是计划，`progress.txt` 是实验室笔记，`AGENTS.md` 是滚动更新的规则手册。Agent 本身是失忆的，但文件系统不是。每次迭代从干净状态启动，但从磁盘读取足够的状态来继续。

Google 和 Anthropic 产品化的是让这个模式可恢复、安全和可观测的工程工作。

---

## 九、Kick the Tires

如果你想实验本文讨论的思路，以下是低摩擦的起点：

- **立即可用**：在项目根目录创建/更新 `AGENTS.md`，加入你观察到的 Agent 失败模式的具体规则。每发现一个新失败，加一条
- **加一个 Hook**：从 pre-commit hook 入手，在 `before_commit` 里加一个检查（禁止 `DROP TABLE`、禁止 `@ts-ignore`、强制 `git status`）
- **实验 Ralph 循环**：用一个 JSON 文件跟踪任务列表，用 Bash 脚本实现简单的任务循环，看 Agent 在多会话场景下是否比单会话表现更稳定

---

## 引用来源

> "A coding agent is the model plus everything you build around it. Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips."
> — Addy Osmani, [Agent Harness Engineering](https://addyosmani.com/blog/agent-harness-engineering/), April 19, 2026

> "It's not a model problem. It's a configuration problem."
> — HumanLayer, [Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents)

> "On Terminal Bench 2.0, Claude Opus 4.6 running inside Claude Code scores far lower than the same model running in a custom harness. Viv's team moved a coding agent from Top 30 to Top 5 by changing only the harness."
> — Addy Osmani, citing Viv Trivedy's research

> "Harnesses encode assumptions that go stale as models improve."
> — Anthropic Engineering, [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents)