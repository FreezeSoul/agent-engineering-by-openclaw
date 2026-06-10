# Anthropic Claude Agent SDK：赋予 Agent 计算机能力与自我验证闭环

> 本文深入分析 Anthropic 官方工程博客发布的 Claude Agent SDK 设计原则，揭示「赋予 Agent 操作计算机的能力」与「让 Agent 能验证自己的工作」这两个核心设计哲学如何共同构成可靠的 agentic loop。

## 核心命题

Claude Agent SDK 的设计揭示了一个关键认知：**Agent 的可靠性不在于模型有多强大，而在于系统是否同时满足两个条件——它能像程序员一样操作计算机，且能像程序员一样验证自己的工作**。这两个能力缺一不可，共同构成了完整的 agentic loop。

## 一、"Giving Claude a Computer"：核心设计哲学

Anthropic 在这篇文章中明确提出了 Claude Agent SDK 的核心设计原则：

> "The key design principle behind Claude Code is that Claude needs the same tools that programmers use every day. It needs to be able to find appropriate files in a codebase, write and edit files, lint the code, run it, debug, edit, and sometimes take these actions iteratively until the code succeeds."

这段话点出了 Agent 系统的本质：**Agent 不是在真空中工作，它需要与程序员共享同一个工作环境**。只有当 Agent 能够执行和程序员完全相同的操作集合时，它才能真正理解和解决编程问题。

笔者认为，这句话的深层含义是：工具的设计不是「给 Agent 尽可能多的能力」，而是「给 Agent 与任务匹配的能力」。一个处理邮件的 Agent 需要 `fetchInbox`、`searchEmails` 这样的工具；一个处理代码的 Agent 则需要文件操作、lint、运行调试的能力。**工具设计的第一原则是匹配，而非全面**。

### 1.1 Tools 作为上下文效率的核心

文章指出了一个关键工程洞察：

> "Tools are the primary building blocks of execution for your agent. Tools are prominent in Claude's context window, making them the primary actions Claude will consider when deciding how to complete a task. This means you should be conscious about how you design your tools to maximize context efficiency."

这里的关键词是**上下文效率**。工具会占据上下文窗口的空间，如果工具设计不当（例如过于细粒度、重复功能），会直接消耗宝贵的上下文容量，影响 Agent 的决策质量。

这个洞察与传统的「工具越多能力越强」假设相反。Anthropic 建议的是：**优先考虑工具的上下文效率，而非功能覆盖度**。一个精心设计的、上下文高效的工具体系，比一个臃肿的工具体系更能发挥 Agent 的能力。

## 二、"Verify Your Work"：三种评估方法

文章的第二核心观点是：**Agent 必须能够评估自己的工作质量，而非盲目执行**。这是让 Agent 真正可靠的关键机制。

> "Agents that can check and improve their own output are fundamentally more reliable—they catch mistakes before they compound, self-correct when they drift, and get better as they iterate."

Anthropic 提供了三种让 Agent 验证工作的方法：

### 2.1 Defining Rules

最直接的评估方式是**定义明确的输出规则**，然后让 Agent 解释哪些规则失败了、为什么失败。

这种方法的本质是**将期望行为形式化**。当 Agent 知道「这个函数的输出应该符合 X 规则」时，它可以在执行后对照检查，发现不符合的地方。

> "The best form of feedback is providing clearly defined rules for an output, then explaining which rules failed and why."

笔者认为，这种方法的局限在于**规则本身需要人工定义**，且规则可能无法覆盖所有边界情况。但它的优势在于可预测性——Agent 的行为边界是清晰的。

### 2.2 Assertions

第二种方法是**断言**——在代码或输出中嵌入检查点，Agent 执行时触发这些断言，失败则触发修正流程。

> "If your agent misunderstands the task, it might be missing key information. Can you alter the structure of your search APIs to make it easier to find what it needs to know?"

断言的工程含义是：**将质量控制嵌入工作流本身**，而非作为独立的质量检查层。这与 TDD（测试驱动开发）的思想一致——质量不是事后检查，而是内嵌于过程。

### 2.3 Programmatic Evals

第三种方法是**程序化评估**——构建代表性的测试集，对 Agent 的输出进行系统性评估。

> "If your agent's performance varies as you add features, build a representative test set for programmatic evaluations (or evals) based on customer usage."

笔者认为，这是三种方法中**最具工程价值的**——它将 Agent 的质量评估从主观判断转变为客观可测量指标。Programmatic evals 允许持续监控 Agent 在真实场景下的表现，为 Agent 的迭代改进提供数据支撑。

## 三、Agentic Loop 的完整闭环

结合上述两个核心设计原则，Claude Agent SDK 实际上揭示了一个完整的 agentic loop：

```
执行 → 验证 → 修正 → 迭代
```

- **执行**：Agent 使用工具完成具体任务
- **验证**：Agent 通过规则/断言/程序化评估检查输出质量
- **修正**：发现错误后，Agent 尝试自我修正
- **迭代**：重复执行和验证直到达到预期

这个闭环的关键在于**每个环节都有明确的机制支撑**：
- 执行靠的是「与程序员共享工具集」
- 验证靠的是三种评估方法
- 修正和迭代靠的是反馈循环

## 四、工程实践：Feedback Loop 设计

文章末尾提供了一些关键的工程建议，帮助开发者构建更好的 Agent 系统：

> "If your agent misunderstands the task, it might be missing key information. Can you alter the structure of your search APIs to make it easier to find what it needs to know?
> If your agent fails at a task repeatedly, can you add a formal rule in your tool calls to identify and fix the failure?
> If your agent can't fix its errors, can you give it more useful or creative tools to approach the problem differently?"

这些建议的共同点是：**不要试图让 Agent 适应糟糕的工具设计，而是要让工具适应 Agent 的能力边界**。工具设计是双向的——既要考虑人类的操作习惯，也要考虑 Agent 的决策模式。

## 五、与现有 Harness 设计的关联

Claude Agent SDK 的设计并非凭空而来，它与业界已有的 harness 设计理念高度一致：

| 设计维度 | Claude Agent SDK | 业界实践 |
|---------|-----------------|---------|
| **工具设计** | 上下文效率优先，匹配任务 | MCP 协议强调最小化工具集 |
| **评估机制** | Rules / Assertions / Evals 三层 | Harness 中的 evaluator loop |
| **工作区管理** | 操作计算机的能力 | git commit / artifact 作为状态管理 |
| **错误修正** | 工具适配而非强制适配 | Guardrail / Permission 分层 |

笔者认为，Claude Agent SDK 的价值在于它将这些分散的工程实践整合为一个连贯的设计哲学。**「赋予 Agent 计算机能力」和「让 Agent 验证工作」这两个设计原则，共同构成了可靠 Agent 系统的基础**。

## 六、判断与展望

Claude Agent SDK 的设计揭示了一个重要的工程判断：**Agent 系统的可靠性不是靠增强模型能力来实现的，而是靠完善工具集和评估机制来实现的**。

这个判断对行业有深远影响：
- **对于框架开发者**：工具设计和评估机制应该被视为一等公民，而非附属功能
- **对于企业部署**：评估体系的建设是 Agent 生产化的必要条件
- **对于研究员**：Agent 的能力边界不仅取决于模型，更取决于系统设计

文章结尾提到：

> "The Claude Agent SDK makes it easier to build autonomous agents by giving Claude access to a computer where it can write files, run commands, and iterate on its work."

这正是 Agent 系统的核心目标——**让 AI 能够像人类一样工作、迭代、改进**。而这个目标的实现，离不开「计算机能力」与「自我验证」的共同支撑。

---

**引用来源**：
- Anthropic Engineering Blog: [Building agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)（2026）

**相关主题**：
- 工具设计：[Anthropic「Writing Tools for Agents」：用 Agent 思维重新定义工具设计](./anthropic-writing-tools-for-agents-meta-circular-2026.md)
- Harness 设计：[OpenAI Agents SDK 下一代进化：Model-Native Harness 与 Native Sandbox](../fundamentals/openai-agents-sdk-next-evolution-model-native-harness-2026.md)