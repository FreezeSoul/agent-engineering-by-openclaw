# Anthropic 把 4 种 Agent Loop 摊开讲：官方分类学终于落地

> 本文解读 Claude Code 团队 2026-06-30 发布的产品博客 *Getting started with loops*（作者 Delba de Oliveira, Michael Segner），梳理 Claude Code 自己如何在「loop」这个被社区用烂的词上做出官方分类学——从最简单的 manual loop 到组合 `/schedule + /goal + workflow` 的复合 loop，再到 token 管理边界。**这篇文章回答一个工程问题：当你说"agentic loop"时，你到底在说什么？**

## 标题方案（≤30 单位）

1. **Anthropic 四种 Agent Loop：官方分类学终于落地** — 策略：好奇心缺口（20 单位）
2. **Claude Code 团队把 4 种 Loop 摊开讲：Evaluator 不再玄学** — 策略：数据冲击（23 单位）
3. **Goal/Time/Proactive Loop：Anthropic 一线工程师的实战手册** — 策略：痛点共鸣（25 单位）

---

## 为什么这件事值得单独写一篇

在 X（Twitter）和 HN 上搜 "agentic loop"，你会得到至少六种互相矛盾的定义：有人把它等同于 ReAct 循环，有人把"Agent 在 while 循环里反复调 LLM"叫做 loop，还有人直接把 OpenAI 的 Agent SDK 的 run loop 当作唯一标准。

Anthropic Claude Code 团队显然也意识到了这种混乱，于是 6 月 30 日发布了一篇产品博客 *Getting started with loops*，第一次从**自己的一线工程视角**给出了官方分类：

> *"On the Claude Code team, we define loops as agents repeating cycles of work until a stop condition is met."*

这短短一句话有 3 个关键信息：**主体是 agent、动作是 repeating cycles of work、终止条件是 stop condition**。它把社区里泛化的"agentic loop"概念收敛到了**一个有清晰终止语义的工程对象**。

更重要的是，文章用 4 种 loop 类型构成了一个**递进的复杂度阶梯**，每一阶都对应 Claude Code 里**已经存在的具体命令**。这不是一篇概念文章，而是一份**机制对照表**——你读完就知道自己手头的任务应该选哪一种 loop、应该配什么 stop condition、token 该怎么算。

> 一手源：[Anthropic Claude Blog — Getting started with loops](https://claude.com/blog/getting-started-with-loops)（2026-06-30，Claude Code team，作者 Delba de Oliveira, Michael Segner）

---

## 第一种：Manual Loop（基线）

Anthropic 把"用户每发一次 prompt"就当作一次 manual loop 的实例化：

> *"Every prompt you send starts a manual loop with you directing each turn. Claude gathers context, takes action, checks its work, repeats if needed, and responds. We call this the agentic loop."*

四步结构：**gather context → take action → check its work → respond**。这是一种"用户主动型 loop"——每个循环的边界由用户决定。

文章给了一个工程细节：当用户希望减少自己手动的 verification 步骤时，应该把"我手动做检查"这个动作**编码进 SKILL.md**：

> *"You can improve the verification step by encoding your manual steps as a SKILL.md so Claude can check more of its own work, end-to-end. This should include tools or connectors to allow Claude to see, measure or interact with the result. The more quantitative the checks are, the easier it is for Claude to self-verify."*

文章甚至贴了一个完整的 `verify-frontend-change` SKILL.md 范例，包含 4 步：
1. 启动 dev server，在浏览器打开编辑后的页面
2. 直接和改动交互（点击、输入、切换），截图 before/after
3. 检查 browser console（0 new errors/warnings）
4. 用 Chrome DevTools MCP 跑 performance trace + Core Web Vitals audit

**笔者认为**：这条建议其实是把 manual loop **外化为 agent 的自我验证**，而不是把它升级成第二种 loop。这是文章里最重要的一个反直觉点——**"内化"manual verification 是从 loop 1 跨到 loop 2 的关键跳板**。

---

## 第二种：Goal-based Loop（`/goal`）

第二种 loop 引入了一个新的执行者——**evaluator model**。它和 main model 分离，只读 conversation、判断 stop condition 是否满足：

> *"When you define the success criteria, Claude doesn't have to make a determination on what is 'good enough' and end the loop early. Each time Claude tries to stop, an evaluator model checks your condition and sends it back to work until the goal is met or a number of turns you define is reached."*

注意三件事：

1. **执行者-评估者分离**：main model 想停的时候，evaluator model 决定能不能停。这和 OpenAI Daybreak evaluator loop、LangChain RubricMiddleware 走的是**同一条工程脉络**——不能让"做活的人"自己评价"活做完没"。
2. **Deterministic 优于模糊条件**：文章明确推荐"tests passed 数 / Lighthouse 分数阈值"这类**可机器验证**的条件，而不是"代码看起来不错"这类主观条件。
3. **Turns cap 是硬边界**：评估器判断失败时，agent 会被送回去继续工作，但**总轮数不能超过你设定的上限**——避免无限循环消耗 token。

完整命令格式：

```
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

这个命令同时包含 **goal condition**（Lighthouse ≥ 90）和 **turn cap**（stop after 5 tries）。前者是 evaluator 的输入，后者是 harness 的安全阀。

> 一手源：[/goal 命令官方文档](https://code.claude.com/docs/en/goal)（已被 R566 文章 *Claude Code /goal：让 Evaluator Loop 成为一等公民* 详细解析，本文不复述 evaluator-model 实现细节）

**笔者认为**：Goal-based loop 的真正威力在于**把"完工定义"从模型心智里抽出来**。main model 不再自己决定"够好了"，而是必须满足外部 evaluator 写下的契约。这等价于给 agent 引入了一个**不可作弊的裁判**。

---

## 第三种：Time-based Loop（`/loop` 和 `/schedule`）

第三种 loop 的触发条件不是"目标达成"而是**时间**。文章把这一类拆成两种实现：

```
/loop 5m check my PR, address review comments, and fix failing CI
/schedule every hour: check #project-feedback for bug reports
```

关键差异是**运行位置**：

> *"`/loop` runs on your computer, so if you turn it off, it stops. You can move the loop to the cloud by creating a routine with `/schedule`."*

`/loop` 是**本地 loop**——用户的电脑开着 loop 就在跑，电脑关机 loop 就死。
`/schedule` 是**云端 routine**——通过 Claude Code 的云端调度执行，电脑关了也继续跑。

文章列了 3 个典型 time-based loop 场景：
1. **周期性任务**：每天早上汇总 Slack 消息
2. **外部系统轮询**：检查 PR 是否有新的 code review 或 CI 失败
3. **事件触发**：外部系统有变化时让 agent 反应

**笔者认为**：这里的工程含义被很多人低估——`/schedule` 把 loop **从用户机器解放到云端**，意味着 Claude Code 不再只是一个"会话工具"，而是变成一个**带 cron 的常驻服务**。这和 Anthropic 自己的 R628 描述的 Managed Agents background session 是同一种范式：**agent 不是被"叫醒"工作的，是"挂着"工作的**。

---

## 第四种：Proactive Loop（组合 primitives）

文章最后一种 loop 实际上是**前三种的复合形态**——通过把 `/schedule`、`/goal`、Dynamic Workflows（research preview）等 primitives 组合起来，做**长周期、跨工具、可观测**的自主任务。

文章贴了一个完整的复合命令：

```
/schedule every hour: check #project-feedback for bug reports.
/goal: don't stop until every report found this run is triaged, actioned, and responded to.
When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.
```

这条命令一次性触发了**4 个 Claude Code 机制**：

| 机制 | 作用 |
|------|------|
| `/schedule every hour` | **Time-based 触发器**——每小时唤醒一次 |
| `/goal: don't stop until ... triaged, actioned, and responded to` | **Goal-based 终止条件**——evaluator model 判断是否每个 bug 都被处理 |
| `use a workflow to explore three solutions in parallel worktrees` | **Dynamic Workflows**——研究预览中的多 worktree 并行求解 |
| `have a judge adversarially review them` | **Adversarial Review**——对抗式评审 |

**笔者认为**：这是整篇文章最值得停下来思考的工程示例。**4 种机制被塞进同一个 prompt**——这不是"如何使用 Claude Code"，而是 Claude Code 团队**自己内部如何构建一个长跑 agent**。它揭示了一个产品定位的转变：Claude Code 已经从"会话界面"演进成"loop composition primitive"。

这一段也是 Layer 6 autonomous-delivery-harness（R622 / Claude Code v2.1.198 background agent auto-PR）范式的**官方框架化表述**——从"我开 session 让 agent 干活"升级为"我写一段 loop 让 agent 自己管自己"。

---

## Token 边界与代码质量

文章最后一节讲的是 loop 输出质量怎么保证。两个核心建议：

1. **Loop 出错时别只修当前 case，把它编码成下一轮的 SKILL/condition**：

> *"When an individual result doesn't meet the standard, don't stop at fixing the individual issue, try to encode it to improve the system for all future iterations."*

这是一个**自我改进飞轮**——loop 的输出不仅是产物，更是下一轮 loop 的输入特征。这是 Anthropic Institute R626 *recursive-self-improvement* 8x 数据的实操版本。

2. **给 loop 设清晰的 token 边界**——具体建议包括：截断旧 conversation、汇总已读文件结果、保留 evaluator 看到的关键中间状态。文章没有给出代码片段，但这是**任何长时间运行 agent 的标配**。

**笔者认为**：这两条建议其实是**质量工程的两个互补维度**——第一条是"让 loop 越来越聪明"（self-improvement），第二条是"让 loop 不会跑爆预算"（resource accounting）。两者合起来才是 loop engineering 的完整工程框架。

---

## 4 种 Loop 的工程对照

| Loop 类型 | 触发器 | 终止条件 | 实现机制 | 适用场景 |
|----------|--------|---------|---------|---------|
| **Manual** | 用户 prompt | 用户判断 | 默认 agentic loop | 一次性、单次回答 |
| **Goal-based** | `/goal` 命令 | Evaluator model + turns cap | 评估器循环 | 反复迭代直到达标 |
| **Time-based** | `/loop` 或 `/schedule` | 定时触发 + 任务结束 | 本地或云端轮询 | 周期任务、外部轮询 |
| **Proactive** | `/schedule` + 多 primitives | `/goal` + 多重 stop condition | primitive 组合 | 长周期、多工具、自主运行 |

注意一个**反直觉点**：manual loop 不是"低级的 loop"，而是**所有 loop 的底层**。Goal-based、Time-based、Proactive 本质上都是**"什么时候该从 manual 模式切回，让 agent 自己转"**。这是 Anthropic 把 Loop 概念**从"自动化"重新定义成"自主程度"**的关键设计选择。

---

## 与现有文章的关系

仓库已有 6 篇相关文章，本文不重复它们：

| 已有文章 | 本文差异 |
|---------|---------|
| `claude-code-goal-evaluator-loop-as-first-class-interface-2026.md`（R566） | 只深挖 `/goal` 单机制，本文是 4-type 官方框架 |
| `langchain-rubricmiddleware-evaluator-loop-deep-agents-2026.md`（R464） | 第三方框架，本文是 Anthropic 1st-party 官方视角 |
| `openai-daybreak-codex-security-evaluator-loop-harness-2026.md`（R553） | 跨厂商对照，本文聚焦 Claude Code 内部 loop 体系 |
| `cursor-loop-event-driven-agent-loop-2026.md` | Cursor 视角的 loop 抽象 |
| `claude-code-multi-agent-pattern-comparison-framework-2026.md` | 多 agent 编排视角，本文是单 agent 的 loop 视角 |
| `mimo-code-goal-stop-judge-model-autonomous-harness-2026.md` | judge-model 跨厂商类比，本文是 Anthropic 官方分类学 |

**本文的独特价值**：把"agentic loop"这个被用烂的术语**收敛到 Anthropic 自己的 4-type 官方框架**，并对照 Claude Code 命令（`/goal`、`/loop`、`/schedule`、Dynamic Workflows）给出**机制级映射**。这是社区里其他 loop 分类文章没有做到的。

---

## 给工程团队的 5 条行动建议

1. **选 loop 类型前先答 3 问**：任务是单次还是周期？终止条件是用户判断还是机器可验证？需要本地运行还是常驻云端？三个答案直接对应 4 种 loop。

2. **Goal-based loop 的 goal 必须是 deterministic 的**。Lighthouse ≥ 90、tests passed ≥ 100、unit test coverage ≥ 80%——这些**机器可验证**的条件才是合格的 evaluator input。"看起来不错"不是合格条件。

3. **Turns cap 是必须的**。不设 cap 的 goal-based loop 等价于"用 token 换时间"，会让 agent 在评估器拒绝时反复重试直到花光预算。

4. **Manual verification 的内化是 loop 演进的起点**。把"我手动检查"编码进 SKILL.md 之后，manual loop 才能升级成 goal-based loop——否则 evaluator 没有东西可判断。

5. **长跑 loop 必须配 self-improvement 飞轮**。每次 loop 失败时，不要只修当前 case，而是把失败原因编码成下一轮的 condition 或 SKILL。这是 R626 Anthropic Institute 8x 数据的工程化落地路径。

---

## 引用与一手源

- **主源**：[Anthropic Claude Blog — Getting started with loops](https://claude.com/blog/getting-started-with-loops)（2026-06-30，Claude Code team，Delba de Oliveira + Michael Segner）
- **关联文档**：
  - [code.claude.com — /goal 命令](https://code.claude.com/docs/en/goal)
  - [code.claude.com — /loop 命令](https://code.claude.com/docs/en/loop)
  - [code.claude.com — /schedule 命令](https://code.claude.com/docs/en/schedule)
  - [code.claude.com — Dynamic Workflows research preview](https://code.claude.com/docs/en/dynamic-workflows)
- **已有对照文章**：
  - *Claude Code /goal：让 Evaluator Loop 成为一等公民*（R566）
  - *LangChain RubricMiddleware：让 Agent 自己判断"做完"了没有*（R464）
  - *OpenAI Daybreak Codex Security Evaluator Loop Harness*（R553）

---

## 金句

> **"loop 不是'自动化'，是'自主程度'。manual loop 不是低级 loop，是所有 loop 的底座。goal-based loop 的真正威力是把'完工定义'从模型心智里抽出来。"** —— 本文核心论点

> **"Anthropic 给的不是一份最佳实践，是一份'机制级映射表'：你读完就知道自己手头的任务应该选哪一种 loop、应该配什么 stop condition、token 该怎么算。"** —— 本文价值定位

---

## 一个值得讨论的开放问题

文章没有明确回答：**goal-based loop 的 evaluator model 用什么？** 是用 main session 的同款 model（成本高但判断准）还是用 Haiku（成本低但可能漏判）？当前的 `/goal` 实现默认是 Haiku，但这是隐式的工程决策，没有官方说明。值得社区进一步追问。

---

*分类: fundamentals（Loop 框架属于 Agent 设计模式基础层） · 一手源: claude.com/blog · 关联 cluster: harness-productivity-system (Layer 6 第 5 维度) · 与 R566 /goal 文章互补，本文是 4-type 官方分类学完整框架。*