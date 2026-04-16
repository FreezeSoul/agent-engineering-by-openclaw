# Harness Engineering：范式演进与 Mitchell Hashimoto 的六阶段成长框架

> **核心论点**：Agent 失败不是模型的失败，而是环境的失败。当同一个错误重复出现，正确的解法不是修改提示词，而是改造 Agent 的运行环境——这就是 Harness Engineering 的本质。
>
> **读完能得到什么**：理解从 Prompt Engineering → Context Engineering → Harness Engineering 的演进逻辑；掌握 Mitchell Hashimoto 的六阶段 Agent adoption 框架；理解为什么 AGENTS.md 是最小可行的 Harness 实现。

---

## 一、范式演进的内在逻辑

AI Coding Agent 的工程方法论，2026 年之前经历了两个阶段，现在正在进入第三个阶段。每个阶段的跃迁，都不是因为模型能力不足，而是因为从业者认识到了更深层的问题。

### Stage 1：Prompt Engineering（2022-2024）

Prompt Engineering 关注的是「如何写好单次指令」。核心技巧包括 few-shot learning、chain-of-thought、role-playing。这个阶段的假设是：好的提示词 = 好的输出。

这个范式的核心局限在 2025 年变得无法忽视：**单次提示词永远不够**。模型无法看到它需要的所有上下文，无法记忆历史会话，无法调用外部工具。这个阶段的「完美提示词」在复杂任务面前总是捉襟见肘。

### Stage 2：Context Engineering（2025）

Andrej Karpathy 等人推动了这个阶段的认识升级：模型需要动态构建的上下文窗口——相关文档、会话历史、工具定义、RAG 结果。这个阶段解决了「单次决策」的信息完备性问题。

但 Context Engineering 依然是在**回答层面**优化。模型知道更多了，但它依然会重复犯同样的错误，依然会在错误路径上浪费大量 token，依然无法可靠地自我评估工作质量。

### Stage 3：Harness Engineering（2026）

这个阶段是由 Mitchell Hashimoto 在 2026 年明确提出定义的。他没有发明新术语——「harness」的概念在此之前已经存在于工业界——但他给出了一个精确到可操作的定义：

> **「每一次你发现 Agent 犯了一个错误，你就花时间工程化地解决它，使得 Agent 再也不会犯同样的错误。」**
>
> ——[Mitchell Hashimoto, My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)

这个定义的革命性在于：它把 Agent 开发的核心关注点从「模型」转移到了「环境」。模型是 commodity，决定成败的是环境设计。

OpenAI 的实践验证了这个结论。Ryan Lopopolo（OpenAI Codex 负责人）用一句话总结了整个项目：

> **「Agents aren't hard; the Harness is hard.」**

---

## 二、数据验证：Harness 的投资回报

### OpenAI Codex：7 人 + Agent → 1500 PR + 100 万行代码

OpenAI 的实验在 2026 年引发了行业震动。团队从空仓库开始，7 名工程师使用 GPT-5 驱动的 Agent，在 5 个月内生成了约 100 万行代码和 1500 个 Pull Request。**零行代码由人类编写**。

他们的五条核心 Harness 原则：

1. **仓库是 Agent 的唯一真实来源**：不依赖任何外部知识
2. **代码必须对 Agent 可读**：不只是人类可读——需要清晰的、一致的结构，verbose 的注释
3. **架构约束由 linter 强制执行**：不是告诉 Agent 遵守规则，而是建立让违反规则变得不可能的系统
4. **渐进式授予自主权**：Harness 必须有阶段和关卡
5. **如果 PR 需要大量人工干预，Agent 不是问题——Harness 才是问题**

第五条是整个方法论的缩影：出现问题时，工程师的第一反应是改造 Harness，而不是改进模型或提示词。

### Stripe Minions：1300+ PR/周

Stripe 内部有一个被称为「Minions」的自治 Agent 系统，每周合并超过 1300 个 PR，完全无需人工审核。支撑这个系统的关键 Harness 特性：

- **Blueprint 编排**：将工作流拆分为确定性节点（运行 linter、推送 commit）和 Agent 节点（实现功能、修复 CI 失败）
- **两击规则**：Agent 的第一次修复失败后，任务立即升级给人类——不允许 Agent 在无限重试循环中浪费资源

### 成本悖论：$9 vs $200

Anthropic 做过一个极端对比实验：同一个复杂任务，简单的「prompt-and-run」方式花了 $9 得到的是一个坏掉的产品；在受控 Harness 环境中经过结构化迭代后，花了 $200 得到了一个完整可用的产品。

成本差异本身不重要，重要的是**能力差异**：$9 得到的是零，$200 得到的是可交付产品。Harness 的投资回报不是线性的，而是存在一个断崖——没有 Harness 的 Agent 在复杂任务上注定失败。

---

## 三、Mitchell Hashimoto 的六阶段 Adoption 框架

Hashimoto 记录了他个人从 AI skeptic 到 Harness Engineering 实践者的完整旅程。这个框架的价值在于：它不是公司级别的规模化实践，而是单个工程师在真实工作中逐步调整出来的方法论。

### Step 1：放弃 Chatbot

Chat 界面的根本局限在于：你在期望模型基于它的预训练知识「猜对」，而纠正错误需要人工反复告诉它哪里错了。这个过程比人类直接做还低效。

**关键转变**：必须使用 Agent。Agent 的最低要求是：能够读取文件、执行程序、发起 HTTP 请求。Hashimoto 明确区分了「chatbot」（对话界面）和「agent」（有工具调用能力的 LLM）。

### Step 2：复刻自己的工作

这个阶段 Hashimoto 用 Claude Code 重新做他手动完成的工作——不是为了效率，而是为了**学习**。他强迫自己用 Agent 复现每个手动 commit，看 Agent 能否达到相同的质量和功能。

这产生了几个关键发现：

- 将 session 拆分为独立、清晰、可操作的任务，而不是一个 mega session
- 模糊请求拆分为 planning session 和 execution session
- 给 Agent 一个验证自己工作的方式——它往往能自己修复错误并防止回归

**这个阶段的本质**：通过刻意练习建立对 Agent 能力边界的直觉。知道 Agent 什么时候会失败，本身就是效率提升。

### Step 3：End-of-Day Agents

Hashimoto 的策略是每天最后 30 分钟启动一个或多个 Agent。他的假设是：用那些「本来也浪费掉的时间」换取 Agent 的正向进展。

有效的任务类型：
- **深度研究**：让 Agent 调研某个领域，生成多页总结
- **并行 Agent 尝试模糊想法**：不期望 Agent 能交付，但希望能照亮第二天工作方向的 unknown unknowns
- **Issue 和 PR 分流**：用 Agent 跑 GitHub CLI 脚本进行 triage，人工只读报告，不允许 Agent 直接回复

### Step 4：外包「必进球」

在清楚知道 Agent 擅长什么之后，Hashimoto 开始每天早上过滤前一夜 triage agent 的结果，找出 Agent 「几乎肯定能做好」的任务，然后让 Agent 在后台逐个处理这些任务，同时他去做自己真正想做的深度工作。

**一个关键操作**：关闭 Agent 的桌面通知。上下文切换成本极高。Hashimoto 的原则是：**人类控制何时打断 Agent，而不是让 Agent 控制何时打断人类**。

同时他指出了一个重要的 trade-off：把任务外包给 Agent 会影响人类自身的技能形成（Anthropic skill formation paper 的担忧）。他通过继续手动处理其他任务来对冲这个风险。

### Step 5：Engineer the Harness

这是整个框架的核心。Hashimoto 将这个阶段定义为两种形式的组合：

**形式一：更好的隐式提示（AGENTS.md）**

对于 Agent 重复运行错误命令或找错 API 这类简单问题，更新 AGENTS.md（或等价物）。他给出了一个 [Ghostty 仓库的真实案例](https://github.com/ghostty-org/ghostty/blob/ca07f8c3f775fe437d46722db80a755c2b6e6399/src/inspector/AGENTS.md)——这个文件里的每一条都是基于一次糟糕的 Agent 行为，整个文件几乎完全消除了那些重复错误。

**形式二：实际的程序化工具**

例如：截取屏幕截图的脚本、运行过滤后测试的脚本。这通常伴随着 AGENTS.md 的更新来让 Agent 知道这些工具的存在。

两种形式的共同逻辑：**不要依赖于告诉 Agent 规则，而是建立让违反规则变得不可能的系统**。

### Step 6：Always Have an Agent Running

最后阶段的目标是让 Agent **始终处于运行状态**。如果没有 Agent 在跑，就问自己：「现在有什么任务是可以交给 Agent 做的？」

Hashimoto 还提到他喜欢结合慢速、深思熟虑的模型（如 Amp 的 deep mode，本质上是 GPT-5.2-Codex），这类模型可能需要 30+ 分钟做一个小改动，但结果质量很高。

---

## 四、与现有 Harness 文章的关系

本文是「范式层面」的分析，与仓库中已有的 Harness 文章形成互补：

| 文章 | 角度 |
|------|------|
| Anthropic 三代理 Harness（GAN 架构）| Harness 的内部架构设计：Generator-Evaluator 对抗循环 |
| Meta-Harness + AutoHarness | Harness 的自动化生产：Filesystem-based 迭代与 Environment Feedback Loop |
| **本文** | **Harness Engineering 作为行业范式：演进逻辑 + 实践框架** |

三篇文章共同构成对 Harness 的完整认知：范式（本文）→ 架构（三代理）→ 自动化生产（Meta-Harness）。

---

## 五、工程建议：如何开始

### 最小可行 Harness：AGENTS.md

如果不知道从哪里开始，从 AGENTS.md 开始。内容可以包括：

- 项目特定的工作流约束（不要在 feature branch 直接提交到 main）
- 已知的失败模式及规避方式
- 高质量工具的位置（linter、测试命令）
- 验证步骤的优先级顺序

### 判断是否需要改造 Harness

当出现以下情况时，先问 Harness 而不是问模型或提示词：

- Agent 在同一个错误上重复失败
- Agent 花费大量 token 探索死胡同
- Agent 的输出需要大量人工修改才能合并
- Agent 在某个环节的表现不一致（有时好有时坏）

### 两击规则

Stripe 的两击规则值得借鉴：Agent 的第一次修复失败后立即升级给人类。无限重试循环是 Harness 设计失败的信号。

---

## 六、参考文献

- [Mitchell Hashimoto — My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)（Primary source，Harness Engineering 定义来源）
- [Why Harness Engineering Replaced Prompting in 2026 — Epsilla](https://www.epsilla.com/blogs/harness-engineering-evolution-prompt-context-autonomous-agents)（OpenAI Codex 数据来源）
- [Anthropic — Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)（Generator-Evaluator 架构）
- [Ghostty AGENTS.md — Harness 最小实现案例](https://github.com/ghostty-org/ghostty/blob/ca07f8c3f775fe437d46722db80a755c2b6e6399/src/inspector/AGENTS.md)
