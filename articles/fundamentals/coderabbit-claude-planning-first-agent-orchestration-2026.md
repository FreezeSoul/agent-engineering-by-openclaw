# Plan as Quality Gate：CodeRabbit 的 Planning-First Agent 编排架构

> 本文来源：[How CodeRabbit used Claude to build an agent orchestration system](https://claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system)（Claude Blog，2026-05-27）

##核心命题

CodeRabbit 的实践回答了一个根本性问题：**AI coding 的质量瓶颈不在代码生成层，而在规划层**。

他们构建的系统核心洞察是：**让 plan 本身成为质量门控，而非等到 code review 才发现问题**。这个思路直接将错误发现时机从「代码生成之后」提前到「代码生成之前」。

---

## 一、问题：代码评审来得太晚

传统 AI coding 工作流中，许多决策错误在 code review 阶段才暴露——此时代码已经写完，改动成本高昂。CodeRabbit 团队将这称为「规划层空洞化」：Agent 在没有充分上下文和对齐的情况下直接生成代码，导致输出与团队意图产生偏差。

CodeRabbit 创始人在访谈中指出：

> "What we've built, using the Claude ecosystem, is a team-wide planning system. The plan itself becomes a quality gate. If we can make sure the quality of that plan is really good upfront, the downstream effect is very pronounced. You end up with a lot better code at the end of it."

这揭示了一个关键工程判断：**规划层的质量改进，其杠杆效应沿着整个下游链条放大**。

---

## 二、解决方案：三层规划架构

CodeRabbit 的系统并非单一 Agent 生成代码，而是一个**分层规划体系**：

### 第一层：Strategic Plan（战略规划）

由 Opus驱动，负责理解问题本质、设定整体方向、进行高层战略判断。这一层需要最强的推理能力——理解业务上下文、识别约束条件、制定实现策略。

### 第二层：Implementation Plan（实现规划）

由 Sonnet 接收战略规划的输出，将其分解为结构化的步骤序列。这一层将模糊的战略意图转化为可执行的具体计划。

### 第三层：Code Generation（代码生成）

Claude Code pick up 细粒度的实现计划，生成具体代码。计划的粒度经过精心调校——太粗会导致 Agent 填入错误假设，太细会因代码库变化而过时。

关键工程挑战在于**找到合适的抽象层级**：CodeRabbit 团队花大量时间迭代 eval harness 才找到那个「刚刚好」的粒度。

---

## 三、Eval Harness：让规划质量可测量

这是整个系统最值得深入分析的部分。

CodeRabbit 原本有成熟的代码评审 eval 系统，但**规划质量评估是空白**。他们必须从零构建：

### 3.1 LLM Judges 作为评估器

团队开发了 LLM judges 库，专门对计划质量的特定维度打分：

- **完整性**：计划是否覆盖了所有必要的步骤
- **一致性**：计划与原始需求的对齐程度
- **可执行性**：计划步骤是否清晰可操作
- **上下文保持**：计划是否充分保留了代码库的当前状态

这些 judges 不是简单的规则匹配，而是让模型评估模型的「元评估」机制。

### 3.2 隔离实验设计

关键验证方法：**同一任务 with/without 规划步骤的对比**。

```
Task → Without Planning → Output A
Task → With Planning → Output B
```

通过对比 A 和 B，可以**孤立出规划步骤的独立价值**。这是 eval harness 设计中最聪明的地方——不是评估计划本身好不好，而是评估「加了这个计划之后，输出是否真的变好了」。

### 3.3 迭代收敛

CodeRabbit 团队承认：

> "We didn't realize what the right level of detail was going to be for that plan."

这说明 eval harness 的核心价值不仅是「评分」，而是**提供了迭代方向**——通过反复实验和数据反馈，最终收敛到最优的抽象粒度。

---

## 四、Multi-Model Routing：成本与质量的权衡

CodeRabbit 实现了**根据任务复杂度动态选择模型**的路由策略：

| 层级 | 模型 | 职责 | 选择逻辑 |
|------|------|------|----------|
| 战略规划 | Opus | 问题理解、高层方向、复杂推理 | 需要最强推理时 |
| 序列规划 | Sonnet | 将战略拆解为结构化步骤 | 需要平衡质量与成本 |
| 窄任务执行 | Haiku | 上下文蒸馏、定向工具调用 | 任务足够简单可用小模型 |

**Routing原则**："If Haiku does as well as Sonnet on a given task, we use Haiku. If the evaluation harness tells us the plan quality improves when we give Opus more room, we give it more room. **We don't guess.**"

这个原则体现了工程思维的核心：**用数据而非直觉决定模型路由**。Eval harness 不只是评估计划质量，还成为模型路由决策的依据。

---

## 五、工程机制分析

### 5.1 Plan as Artifact

计划不仅是内部执行的中间产物，还成为**团队共享的 artifact**：

- **决策记录**：capture what was decided and why
- **验证基准**：later validate that the output matched the original intent
- **新人 onboarding**：新工程师可以通过阅读计划快速理解项目上下文

这使得「规划」从 Agent 内部活动外化为团队协作资产。

### 5.2 错误前置而非后置

通过将错误发现时机从 code review 前移到 planning review，CodeRabbit 实现了：

- **改造成本降低**：计划修改 << 代码修改
- **团队对齐提前**：stakeholder 在代码生成前就能 review方向
- **上下文保留**：计划 artifact 保留了决策链，便于事后追溯

### 5.3 Eval-Driven Development

CodeRabbit 的开发模式可以总结为：

```
Hypothesis → Build eval → Run experiment → Measure → Iterate
```

这不是传统的 test-driven development，而是 **eval-driven planning optimization**——用评估数据而非主观判断来驱动规划系统的迭代。

---

## 六、对 AI Coding 工程的启示

CodeRabbit 的案例揭示了几个重要的工程判断：

### 判断 1：规划层是当前 AI coding 的最大瓶颈

社区普遍关注「如何让 Agent 生成更好的代码」，但 CodeRabbit 的实践表明**规划层质量才是杠杆点**。改进代码生成是线性优化，改进规划层是倍增放大。

### 判断 2：Eval harness 是规划系统的必要基础设施

没有可测量的评估标准，规划系统的迭代就只能靠主观判断。CodeRabbit 的 LLM judges 方法提供了一种**将主观质量客观化的工程路径**。

### 判断 3：Multi-model routing 的价值在规划层差异最大

代码生成层的小模型表现通常已经足够好，但**规划层对模型能力的需求差异最为显著**——这使得规划层成为 multi-model routing 最有价值的应用场景。

### 判断 4：Plan artifact 是团队协作的关键资产

将计划外化为团队可见、可review、可引用的 artifact，实现了 AI native 工作流下的**人类协作平权**——不只是 AI 在工作，而是人类和 AI 共同在同一个计划上下文里协作。

---

## 七、对比：Planning-First vs Code-First

| 维度 | Code-First（传统）| Planning-First（CodeRabbit）|
|------|------------------|---------------------------|
| 错误发现时机 | 代码生成后 | 代码生成前 |
| 改造成本 | 高（需返工）| 低（计划调整）|
| 团队对齐 | Code review阶段 | Planning review 阶段 |
| 上下文保留 | 代码注释 | Plan artifact |
| 可测量性 | 代码质量可测 | 规划质量需构建 eval harness |

---

## 八、结论

CodeRabbit 的案例证明了一个重要命题：**在 AI coding 领域，真正的创新不在于让 Agent更快地生成代码，而在于构建让人类和 AI 共同在规划层对齐的质量门控**。

Eval harness 的引入不仅解决了「如何评估计划质量」的技术问题，更解决了「如何迭代规划系统」的工程问题。这代表了 AI coding 工程化的下一个重要方向：**从 prompt engineering 到 eval engineering**。

---

**引用来源**：
- [How CodeRabbit used Claude to build an agent orchestration system](https://claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system)（Claude Blog，2026-05-27）
- CodeRabbit 团队最佳实践（见原文 Best practices from the CodeRabbit team）