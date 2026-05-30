# Anthropic CursorBench vs Cursor Composer 2：AI 编程智能体评估体系的分叉演进

> ⚠️ **阅读说明**：这篇文章的核心不是对比"谁家模型更强"，而是回答一个更深层的工程问题：当两家顶级实验室都用"贴近真实环境"作为评估核心原则，为什么走向了完全不同的工程路径？

---

## 一、问题的起点：为什么公开基准测试失效了

2026 年，所有做 AI 编程智能体的团队都面临同一个困境：**公开基准测试无法反映真实开发体验**。

SWE-bench 的任务过于明确、代码库过小、解决方案单一。Terminal-Bench 覆盖了终端场景，但 prompt 仍然过于规范。真实开发中，任务描述是模糊的（"把这个模块重构一下"），解决方案需要跨数百文件改动，人类的模糊指令中埋藏着上下文才能理解的意图。

Cursor 的工程师在 Composer 2 技术报告中说了一句很直接的话：

> "A core challenge in building coding models is that public benchmarks often don't reflect the work developers actually do. Tasks are over-specified, solutions are narrow, and the codebases are small."
>
> （构建编程模型的核心挑战在于，公开基准测试往往无法反映开发者实际的工作。任务过于明确，解决方案过于狭窄，代码库规模过小。）

Anthropic 在 2026 年 1 月发布的《Demystifying evals for AI agents》中也表达了相同的观察：

> "We’ve learned how to design more rigorous and useful evals for agents... The strategies that work across deployments combine techniques to match the complexity of the systems they measure."
>
> （我们学会了如何为智能体设计更严格、更有用的评估……跨部署有效的策略是组合多种技术，以匹配被测系统的复杂性。）

**两家公司的共识**：评估必须重建真实环境。

但从共识出发，两条完全不同的工程路径展开了。

---

## 二、分叉点：外部评估 vs. 内部训练

### Anthropic：从外部逼近真实环境

Anthropic 的策略是**从外部逼近**——在真实代码库上构造评估任务，然后用自动化方式跑智能体，对比输出质量。

Claude Code 的评估体系经历了三个阶段：

1. **快速迭代期**：依赖 Anthropic 员工和外部用户的直接反馈，快速调整智能体行为
2. **窄域评估期**：针对特定维度（简洁性、文件编辑质量）构建专项评估
3. **复杂行为评估期**：针对"过度工程化"等更复杂的行为模式构建评估

这个路径的特点是：**评估和训练是分离的**。Anthropic 先有 Claude Code（通过海量真实用户反馈迭代），然后从中提炼出可以结构化测量的维度，最后将这些维度固化为可持续运行的自动化评估。

在《Demystifying evals for AI agents》中，Anthropic 总结了他们的 grader 类型选择策略：

> "Code-based, model-based, and human graders. Each grader evaluates some portion of either the transcript or the outcome. An essential component of effective evaluation design is to choose the right graders for the job."
>
> （基于代码的、基于模型的、和人工评分员。每种评分员评估转录本或结果的某一部分。有效评估设计的核心组件是为任务选择正确的评分员。）

关键点是** grader 的选择因任务类型而异**：代码正确性可以用精确匹配（exact match），事实性可以用 LLM 判断，支持证据可以用检索验证。不同维度需要不同的测量手段，这不是单一基准能覆盖的。

### Cursor：从内部模拟真实环境

Cursor 的策略是**从内部模拟**——不是等智能体出来后再评估，而是在训练阶段就让模型完全运行在真实的产品 harness（Anyrun）里。

Composer 2 的 RL 训练直接发生在 Cursor 的生产环境中：

> "Composer 2 RL training occurs in realistic Cursor sessions with the same tools and harness the deployed model uses, applied to a problem distribution that reflects the full range of what developers ask Composer to do."
>
> （Composer 2 的 RL 训练发生在逼真的 Cursor 会话中，使用与部署模型相同的工具和 harness，应用的问题分布反映了开发者对 Composer 的全部需求范围。）

这是根本性的差异：**Anthropic 在评估真实产品**，**Cursor 在用真实产品训练模型**。

Composer 2 的训练基础设施 Anyrun 并不是一个专门为评估搭建的模拟环境——它就是支撑 Composer 在生产环境中运行的核心平台。换句话说，Cursor 用生产级 harness 作为 RL 训练的仿真器，训练和推理共享同一套环境实现。

> "Training Composer 2 required substantial infrastructure development with custom low-precision kernels for efficient MoE training on Blackwell GPUs, a fully asynchronous RL pipeline spanning multiple regions, and Anyrun, our internal compute platform for running hundreds of thousands of sandboxed coding environments."
>
> （训练 Composer 2 需要大量的基础设施开发：高效的 MoE 低精度内核、跨越多个区域的完全异步 RL 管道，以及 Anyrun——我们运行数十万个沙盒编码环境的内部计算平台。）

---

## 三、工程路径对比

| 维度 | Anthropic（外部逼近） | Cursor（内部模拟） |
|------|---------------------|-------------------|
| **核心思路** | 先有产品，再提炼评估 | 先有 harness，再从中训练 |
| **训练环境** | Claude Code 作为 harness，评估在其外部运行 | Anyrun（生产 harness）直接作为 RL 训练环境 |
| **评测基准** | Claude Code 用户反馈 → 结构化 eval → 自动化 CI | CursorBench（来自真实会话）→ 持续 RL 训练 |
| **反馈闭环** | 用户反馈慢，但评估可持续、可比较 | 模型在生产环境中学习，反馈极快但存在风险 |
| **可解释性** | 高——eval 维度清晰，可独立运行 | 低——模型学到的行为嵌入了 harness 的细节 |
| **基础设施** | 相对轻量，重点在 eval 框架设计 | 重度投入——Anyrun 需要支撑数十万并发沙盒环境 |

两条路径各有取舍。Anthropic 的外部评估更容易构建可重复的基准（因为评估和训练是分离的），但评估的保真度受限于"模拟环境能否真实还原生产体验"。Cursor 的内部训练保真度极高（因为模型直接在生产 harness 中学习），但训练和推理耦合过深，模型行为难以跨 harness 迁移。

---

## 四、两种路径的隐含假设

### Anthropic 的隐含假设

> "Harnesses encode assumptions about what Claude can't do on its own. However, those assumptions need to be frequently questioned because they can go stale as models improve."
>
> （Harness 编码了关于 Claude 无法自主完成什么的假设。但这些假设需要经常被质疑，因为它们会随着模型的改进而变得过时。）

Anthropic 的假设是：**模型能力是变的，harness 是相对稳定的**。因此，评估体系应该围绕"在不同 harness 配置下模型的表现"来设计，而不是让模型去适应特定的 harness。Managed Agents 的核心设计（session/harness/sandbox 解耦）也是基于这个假设——接口不变，实现可以随时替换。

### Cursor 的隐含假设

> "We find that reducing pretraining loss improves downstream RL performance, with better base knowledge reliably translating into a better agent."
>
> （我们发现降低预训练损失可以提高下游 RL 性能，更好的基础知识可靠地转化为更好的智能体。）

Cursor 的假设是：**模型能力和 harness 环境是共同进化的**。Composer 2 针对 Anyrun 优化，Anyrun 也为 Composer 2 的训练做了专门调整。两者不是独立的——这是高度优化的端到端系统，而非模块化设计。

---

## 五、Benchmark 设计的工程哲学

两种路径代表了 AI 系统中两种截然不同的工程哲学：

| | **接口稳定路径**（Anthropic） | **端到端优化路径**（Cursor） |
|--|------------------------------|------------------------------|
| **系统设计** | 模块化，组件可替换 | 高度耦合，端到端联合优化 |
| **评估角色** | 外部基准，用于比较和回归检测 | 训练环境本身，用于能力获取 |
| **演进方式** | 模型改进 → 重新评估 → 更新 harness | 模型 + harness 共同迭代 |
| **适用场景** | 多模型评估、生产监控、A/B 测试 | 单一模型的极致性能优化 |

在接口稳定路径下，评估是独立的——任何模型都可以用同一套 harness 来评估。CursorBench 可以用来测量任何编程智能体，而不仅仅是 Composer。在端到端优化路径下，评估和训练是同一个系统——CursorBench 就是 Composer 2 的训练数据分布，不是用来对比其他模型的。

**这意味着两者生产的"benchmark"本质上是不同的东西**：
- Anthropic 的 eval 体系产出的是**可比较的基准**
- Cursor 的 CursorBench 产出的是**可学习的目标分布**

这不是哪个更好，而是适用于不同的工程目标。

---

## 六、值得关注的共同发现

尽管路径不同，两家公司的评估实践都指向了相同的工程结论：

**1. 评估饱和是个真实问题**

Anthropic 指出 SWE-bench Verified 的分数从 30% 升到 >80% 后，"only the most difficult tasks remain"（只剩下最困难的任务）。这使得基准分数的增量越来越难以反映真实能力提升。这不是某个基准的问题，而是所有固定任务集基准的数学宿命。

**2. 隔离性是评估可靠性的前提**

Anthropic 强调"Each trial should be 'isolated' by starting from a clean environment"（每次试验都应该通过从干净环境开始来隔离）。共享状态会导致"infrastructure flakiness rather than agent performance"（评估失败来自基础设施不稳定性，而非智能体性能）。Cursor 的 Anyrun 平台实际上也在解决这个问题——每个 RL rollout 运行在独立的沙盒中。

**3. 多维度 grader 组合优于单一评分**

两家都没有只用一种 grader。Anthropic 组合了代码匹配（exact match）、LLM 判断（开放合成）、人类校准（主观输出）。Cursor 在 CursorBench 中混合了客观评测和人类判断。这些都说明，单一指标无法捕捉智能体行为的全部维度。

---

## 七、对工程实践的启示

如果你正在构建 AI 编程智能体的评估体系，有两条路可以选：

**路径 A（接口稳定）**：采用 Anthropic 的思路
- 先用现有产品收集用户反馈，提炼关键行为维度
- 将每个维度翻译为独立的自动化评估
- 投资评估基础设施（隔离环境、可重复运行、多 grader 组合）
- 确保 harness 设计与模型解耦，接口稳定

**路径 B（端到端优化）**：采用 Cursor 的思路
- 直接用生产 harness 作为训练和评估的统一环境
- 用真实会话数据构建 CursorBench 类型的目标分布
- 投资底层基础设施（大规模沙盒编排、异步 RL 管道）
- 接受模型和 harness 的高度耦合，接受跨环境迁移的代价

**关键判断**：哪条路更适合取决于你的目标。如果你是模型提供商（Anthropic、OpenAI），你的基准需要能对比多个模型，路径 A 更合适。如果你是产品公司（Cursor），你的目标是让模型在特定产品中表现极致，路径 B 更合适。

这解释了为什么两家顶级实验室走向了不同的工程路径——不是因为其中一个"错了"，而是因为他们的工程目标从一开始就不是同一个。

---

**引用来源**：

1. Anthropic Engineering, "Demystifying evals for AI agents", 2026-01-09 — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
2. Cursor Blog, "A technical report on Composer 2", Sasha Rush, 2026-03-27 — https://cursor.com/blog/composer-2-technical-report
3. Anthropic, "Scaling Managed Agents: Decoupling the brain from the hands", 2026-04-08 — https://www.anthropic.com/engineering/managed-agents
4. arXiv, "Composer 2 Technical Report" (2603.24477), 2026-03 — https://arxiv.org/abs/2603.24477