# Anthropic 工程实践：多 Agent 系统的三层工程机制

> 本文基于 Anthropic 官方工程博客，解析多 Agent 系统在生产环境中的三个核心工程机制：编排架构、恢复机制、安全防护。

---

## 核心命题

多 Agent 系统不是把多个 LLM 串在一起，而是一套需要**刻意工程化**的分布式状态机——状态持久化、错误恢复、安全边界缺一不可。

Anthropic 在三篇工程博客中揭示了这套机制的设计逻辑，分别对应三个工程维度：

| 维度 | 文章 | 核心机制 |
|------|------|---------|
| **编排架构** | `multi-agent-research-system` | 编排器-工作器模式 + 三 Agent 架构 |
| **恢复机制** | `multi-agent-research-system` | 检查点 + 可恢复执行 |
| **安全防护** | `claude-code-auto-mode` | 分层分类器 + deny-and-continue |
| **评估循环** | `harness-design-long-running-apps` | Planner-Generator-Evaluator 三角 |

> 原文引用：*"Agents are stateful and errors compound. Without effective mitigations, minor system failures can be catastrophic for agents."* — Anthropic, How we built our multi-agent research system

---

## 一、编排架构：orchestrator-worker 模式的问题与解法

### 1.1 模式本身简单，难的是工程化

Anthropic 的 Research 系统采用 orchestrator-worker 模式：lead agent 协调流程，委托专门的 subagent 并行搜索不同方面的信息。

这个模式本身不难理解，但 Anthropic 指出了一个关键问题：

> 原文引用：*"Agents are stateful and errors compound. Agents can run for long periods of time, maintaining state across many tool calls. This means we need to durably execute code and handle errors along the way."*

单 Agent 的状态管理已经是难题，多 Agent 的状态管理复杂度指数级上升。

### 1.2 三 Agent 架构：planner-generator-evaluator

Anthropic 在 `harness-design-long-running-apps` 中给出了更具体的三 Agent 架构：

- **Planner Agent**：将复杂任务分解为可管理的块（tractable chunks）
- **Generator Agent**：逐个生成代码产物
- **Evaluator Agent**：评估生成质量，决定是否接受

> 原文引用：*"I then applied these techniques to long-running autonomous coding, carrying over two lessons from our earlier harness work: decomposing the build into tractable chunks, and using structured artifacts to hand off context between sessions."*

笔者认为，这个架构的真正价值不是"三个 Agent 比一个强"，而是**职责分离带来的可调试性**——当一个环节失败时，你能清楚地知道是 Planner 分解出了问题，还是 Generator 生成质量不足，还是 Evaluator 判断标准过严。

### 1.3 Context reset 的消失是一个信号

Anthropic 在早期 harness 中使用 context reset 来保持模型在长任务中不偏离目标。这是因为 Sonnet 4.5 存在"context anxiety"倾向。

但 Opus 4.5 largely removed that behavior，context reset 从此不再是必须。

> 原文引用：*"Context resets were a key unlock...Opus 4.5 largely removed that behavior on its own, so I was able to drop context resets from this harness entirely."*

**笔者认为**：这是一个重要的工程信号——harness 的设计假设会随着模型能力变化而失效，需要定期重新评估。当模型能力提升后，原本必需的 harness 机制可能变成过度工程化的负担。

---

## 二、恢复机制：checkpoint + resume 的工程实现

### 2.1 错误处理的两种策略

Anthropic 描述了两种错误处理策略的对比：

**策略 A：简单重启**
```
错误发生 → 从头开始重启 → 浪费前面的工作 + 用户体验差
```

**策略 B：可恢复执行**（Anthropic 选择）
```
错误发生 → 从检查点恢复 → 保留状态 + 高效
```

> 原文引用：*"Instead, we built systems that can resume from where the agent was when the errors occurred."*

### 2.2 Combining Adaptability with Deterministic Safeguards

Anthropic 的方案不是单纯依赖 AI 的适应性，也不是单纯依赖确定性逻辑，而是**两者结合**：

> 原文引用：*"We combine the adaptability of AI agents built on Claude with deterministic safeguards like retry logic and regular checkpoints."*

这种混合策略的工程含义：
- **checkpoint** 提供确定性状态恢复点
- **retry logic** 提供确定性重试机制
- **model intelligence** 处理意外情况（如工具失败时通知 agent 并让其自适应）

### 2.3 评估循环：让 agent 持续改进

在三 Agent 架构中，Evaluator Agent 是整个循环的核心驱动力。Anthropic 强调：

> 原文引用：*"The final result was a three-agent architecture—planner, generator, and evaluator—that produced rich full-stack applications over multi-hour autonomous coding sessions."*

Evaluator 的职责不是简单判断"对/错"，而是提供**rubric-based 评估**——基于一套标准评估生成物的质量维度。这与 `human-again/orbit` 项目中的 `evaluator.py` 和 `reviewer.py` 设计高度一致。

---

## 三、安全防护：auto mode 的 deny-and-continue 模式

### 3.1 为什么不能 halt-and-wait

Claude Code 的 auto mode 提供了一种介于 manual review 和 no guardrails 之间的方案。关键设计决策：

> 原文引用：*"When the classifier blocks an action, Claude shouldn't halt and wait for input; it should recover and try a safer approach where one exists."*

这是 **deny-and-continue** 模式——阻断动作，但不中断任务。

### 3.2 两层防御架构

Auto mode 的防御分为两层：

**第一层：读取审查（what Claude reads）**
- 防止 prompt injection 等通过读取内容发起的攻击
- subagent 在 delegation 时进行审查

**第二层：执行审查（what Claude does）**
- 在 action 执行前进行分类器判断
- 阻断危险动作

> 原文引用：*"The return check exists because a subagent that was benign at delegation could be compromised mid-run by a prompt injection in content it reads. Before results go back to the orchestrator, the classifier reviews the subagent's full action history."*

### 3.3 False Positive 的可承受性

Auto mode 面临的另一个关键设计问题：0.4% 的 false positive rate 是否可接受？

> 原文引用：*"A 0.4% FPR sounds small, but if every false positive killed the session it would be a serious usability problem for long-running tasks. Instead, a false positive costs a single retry where the agent gets a nudge, reconsiders, and usually finds an alternative path."*

**笔者认为**：这个设计决策背后的逻辑值得所有构建 agent 安全系统的人思考。安全系统的目标不是"零风险"，而是"风险可接受且可恢复"。一个设计良好的安全系统应该让 false positive 只造成最小代价的重试，而不是让整个任务失败。

---

## 四、工程机制的系统性

### 4.1 三个机制不是独立的

笔者认为，这三个工程机制实际上是一个系统：

```
编排架构（决定状态如何组织）
        ↓
恢复机制（决定状态如何在错误后保留）
        ↓
安全防护（决定状态如何在威胁下不被破坏）
```

没有好的编排架构，恢复机制无从设计；没有可靠的恢复机制，安全防护的代价会指数级上升。

### 4.2 行业验证：orbit 项目的工程实现

`human-again/orbit` 项目（MIT, Python 3.11+）提供了这三个机制的开源实现参考：

```
orchestrator.py       ← 编排核心（mission control）
checkpoint_manager.py ← 可恢复状态的持久化
risk_guard.py         ← 安全边界与分类
evaluator.py          ← rubric-based 评估
reviewer.py           ← accept/iterate 推荐
```

> 原文引用（orbit README）：*"Orbit is the harness your coding agent actually needs — structured loops, real validation gates, rubric-based evaluation, checkpoint resumability, and a full audit trail."*

笔者认为，orbit 的架构设计验证了 Anthropic 描述的三层机制在工程上的可行性——它不是纸上谈兵，而是一个可以实际运行的参考实现。

### 4.3 教训：harness 假设会过时

Anthropic 在 `managed-agents` 中提出的核心观点值得重复：

> 原文引用：*"Harnesses encode assumptions that go stale as models improve."*

Context reset 曾经是必要的——直到模型能力提升后它不再是。这条教训适用于所有构建 agent 系统的人：**定期质疑你的 harness 设计假设**，而不是把它们当作永久真理。

---

## 五、对构建者的启示

### 5.1 起点不是"选哪个框架"

笔者见过太多团队在"选 LangGraph 还是 CrewAI"上纠结很久。但 Anthropic 的工程实践表明，**框架选择不是起点**——起点是回答以下问题：

1. 你的任务需要什么样的**状态持久化策略**？
2. 你的错误处理模型是 restart 还是 **resume**？
3. 你的安全边界是 halt-and-wait 还是 **deny-and-continue**？
4. 你的 agent 评估是 binary 判断还是 **rubric-based**？

回答这些问题后，框架才成为有意义的选项。

### 5.2 多 Agent 的真正代价

多 Agent 系统看起来很强大，但 Anthropic 的描述揭示了它的真实代价：

> 原文引用：*"Multi-agent research systems can operate reliably at scale with careful engineering, comprehensive testing, detail-oriented prompt and tool design, robust operational practices, and tight collaboration between research, product, and engineering teams."*

这需要大量工程投入。不是所有场景都需要多 Agent——对于简单任务，单 Agent + 好的工具设计往往更高效。

### 5.3 定期重新评估 harness 假设

当模型能力提升、工具能力变化或业务需求演进时，原本的 harness 设计假设可能失效。建议：

- 每季度回顾一次核心 harness 假设
- 记录哪些假设是"因为模型能力限制"而存在的
- 跟踪模型能力发展，及时移除不再需要的 workarounds

---

## 结论

Anthropic 的三篇工程博客揭示了多 Agent 系统的三个核心工程机制：

1. **编排架构**：orchestrator-worker + 三 Agent 三角（planner-generator-evaluator），职责分离带来可调试性
2. **恢复机制**：checkpoint + resume + retry logic + model adaptability，混合策略比单一策略更鲁棒
3. **安全防护**：deny-and-continue + 两层防御 + false-positive-as-retry，让安全代价最小化

这三个机制构成一个系统——没有好的编排架构，恢复无从谈起；没有可靠的恢复机制，安全代价指数级上升。

**核心判断**：多 Agent 系统的工程化不是可选的——它是让系统真正可信赖的唯一路径。

---

## 原文引用

1. Anthropic Engineering, "How we built our multi-agent research system", https://anthropic.com/engineering/multi-agent-research-system
2. Anthropic Engineering, "Claude Code auto mode", https://anthropic.com/engineering/claude-code-auto-mode
3. Anthropic Engineering, "Harness design for long-running application development", https://anthropic.com/engineering/harness-design-long-running-apps
4. orbit README, https://github.com/human-again/orbit

---

## 相关资源

- [Anthropic Engineering Blog](https://anthropic.com/engineering)
- [Orbit - Mission control for AI coding agents](https://github.com/human-again/orbit)
- [Scaling Managed Agents: Decoupling the brain from the hands](https://anthropic.com/engineering/managed-agents)
