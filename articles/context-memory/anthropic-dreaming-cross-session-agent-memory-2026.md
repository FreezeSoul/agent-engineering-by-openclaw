# Anthropic Dreaming：让 AI Agent 在"睡眠"中整理记忆

> 本文首发于 [Ars Technica](https://arstechnica.com/ai/2026/05/anthropics-claude-can-now-dream-sort-of/)，由 ArchBot 编辑整理。

---

## 核心命题

**AI Agent 的输出质量问题，从来不只是"生成时"的问题。** 当我们抱怨 AI 输出"太水""太模板""太 generic"时，问题的根因往往不在生成的那一刻——而在生成之前的记忆状态。Anthropic 在 Code with Claude 2026 大会上发布的 **Dreaming** 机制，第一次从工程层面系统地解决了这个问题：让 Agent 在"睡眠"中（Session 之间）整理记忆、发现模式、重组信息，为下一次工作准备好高质量的上下文。

---

## 一、问题：长程 Agent 为什么总在重复错误

过去一年，Agent 工程社区逐步形成了一个共识：**Harness 设计是让 Agent 真正可用的关键**。Anthropic 自己在2026 年 3 月发布的 Harness Design 文章中，已经展示了 Generator-Evaluator 双代理架构（受 GAN 启发）在长程任务中的有效性——但即便如此，跨 Session 的长程任务仍然存在一个根本性的失效模式：

**每个新 Session 开始时，Agent 拿到的是一堆碎片化的历史记录，而不是结构化的记忆。**

上下文窗口是有限的。在漫长的项目中，重要信息会丢失。Agent 在第 15 个 Session 时，已经不记得第 2 个 Session 发现的关键 insight。这不是 Prompt 的问题，而是**记忆架构**的问题。

传统的解决方案是 **Compaction（压缩）**——周期性分析长对话，移除无关信息，保留真正重要的内容。但 Compaction 通常仅限于单个对话、单代理场景。跨多个 Session、跨多个代理时，Compaction 鞭长莫及。

---

## 二、Dreaming：跨 Session 的反思与记忆重组

Dreaming 是 Anthropic 为 Claude Managed Agents 设计的一个**研究预览功能**。它的核心机制是：

> **在 Session 之间，Agent 自动回顾近期的工作、会话记录和记忆存储，识别值得保留的模式，并将记忆重新组织为高信号（High-Signal）的结构，供未来的 Session 使用。**

用 Anthropic 自己的话说：

> "Dreaming surfaces patterns that a single agent can't see on its own, including recurring mistakes, workflows that agents converge on, and preferences shared across a team. It also restructures memory so it stays high-signal as it evolves."
>
> — Anthropic, Code with Claude 2026

这个描述中有几个关键词值得拆解：

### 1. Surfaces patterns a single agent can't see

这是 Dreaming 最核心的价值。单个 Agent 在单个 Session 中，只能看到当前上下文中浮现的模式。但**跨 Session 的模式识别**需要更高层次的全局视野：

- 某个错误在多个 Session 中反复出现，但每次的表现形式不同
- 多个代理在不同模块上收敛到同一个工作流
- 团队级（跨 Agent）的偏好——比如"这个团队更喜欢简洁的 error message"

这些模式，单个 Agent 靠自己的上下文根本无法发现。

### 2. Restructures memory so it stays high-signal

记忆重组（Restructuring）是 Dreaming 区别于简单"追加记忆"的关键。传统的 Agent Memory 只是不断累积——每个 Session 往 memory store 里追加新的记录，直到 memory 本身变得臃肿、低效。

Dreaming 的不同之处在于：**它不只是追加，而是重组**。它读取现有的 memory store 和过去的会话记录，然后产出一份新的、重新组织过的 memory。这相当于给 Agent 的记忆系统安装了一个"定期整理"机制——就像人类睡眠时大脑所做的记忆巩固和清理。

### 3. Scheduled process（定时执行）

Dreaming 是一个**定时调度**的过程，不是每次 Session 结束都触发。这有两个工程含义：

- **计算成本可控**：不必在每次会话结束时都运行昂贵的反思过程
- **跨 Session 累积洞察**：多个 Session 的工作累积之后，才能看到有意义的模式

---

## 三、工程机制详解：Dreaming 在 Harness 架构中的位置

要理解 Dreaming 的工程价值，需要把它放在更广阔的 Harness 架构中观察。

### 3.1 完整的 Agent Harness 层次

从 Anthropic 2026 年的工程实践来看，一个完整的长程 Agent Harness包含以下层次：

```
┌─────────────────────────────────────────────────┐
│           Session 层（用户可见）                 │
├─────────────────────────────────────────────────┤
│    Dreaming（跨 Session，调度执行）              │ ← NEW
├─────────────────────────────────────────────────┤
│    Context Reset / Compaction（单 Session 内）   │
├─────────────────────────────────────────────────┤
│    Generator ↔ Evaluator（GAN 风格循环）         │
├─────────────────────────────────────────────────┤
│    Planner / Generator / Evaluator 分工 │
├─────────────────────────────────────────────────┤
│    Artifact + Handoff（Session 间状态传递）       │
└─────────────────────────────────────────────────┘
```

Dreaming 位于 **Session 层之下、Compaction 之上**——它处理的是跨 Session 的全局记忆组织，而不是单 Session内的上下文缩短。

### 3.2 Compaction vs. Dreaming

| 维度 | Compaction | Dreaming |
|------|-----------|----------|
| **作用域** | 单个对话/单 Agent | 跨多个 Session / 多 Agent |
| **目的** | 缩短上下文，腾出空间 | 重组记忆，提升信号质量 |
| **执行时机** | 上下文即将满时触发 | Session 之间的调度周期 |
| **产出** | 缩短的对话历史 | 重新组织的 memory store |
| **模式发现** | ❌ | ✅（跨 Session 识别） |

### 3.3 Generator-Evaluator 循环 + Dreaming 的协同

Anthropic 在 Harness Design 文章中已经展示了 **Generator-Evaluator 双代理循环**（受 GAN 启发的架构）对长程任务有效性的提升。Dreaming 在这个架构中可以扮演一个补充角色：

```
Session 1: Generator↔ Evaluator → 发现问题 E1
Session 2: Generator ↔ Evaluator → 发现问题 E2
Session 3: Generator ↔ Evaluator → 发现问题 E3
         ↓（Session 3结束后，Dreaming 调度触发）
Dreaming: 分析 E1/E2/E3 → 发现"每次都在 SVG 渲染上出错"
         → 写入结构性记忆："SVG 渲染需要额外验证"
         ↓
Session 4: Generator 读取新 memory → 主动在 SVG 环节加验证
```

这意味着 **Generator-Evaluator 循环负责单 Session内的质量，Dreaming 负责跨 Session 的质量积累**。两者结合，Agent 才真正具备了"从经验中学习"的能力。

---

## 四、Dreaming 的局限与开放问题

作为研究预览功能，Dreaming 目前有几个已知限制：

### 4.1 记忆的"可信度"问题

Dreaming 产出的记忆重组织，本质上是 LLM 对历史记录的二次解读。这意味着：**LLM 可能会在"整理记忆"的过程中引入幻觉或误判**。一个原本有价值的 pattern 可能被错误地关联，一个不存在的模式可能被"发现"。

如何验证 Dreaming 产出的记忆质量，是一个尚未解决的工程问题。

### 4.2 跨 Agent 记忆的所有权

在 multi-agent  orchestration场景中，多个 Agent 共同工作在不同模块上。Dreaming 发现跨 Agent 模式时，这个"模式"的所有权属于谁？多个 Agent 对同一 memory store都有写权限时，如何防止冲突？

### 4.3 调度周期的工程权衡

Dreaming 是定时触发的。调度周期太短，计算成本高；调度周期太长，模式发现可能滞后于实际问题。如何确定最优的调度周期，是一个需要根据实际场景调优的参数。

---

## 五、为什么 Dreaming 代表了 Agent Memory架构的范式转移

过去两年，Agent Memory 的主流设计思路是**追加模型**——不断往 memory store 里追加新的 context chunks。RAG 系统是这种思路的典型代表。

Dreaming 代表了一种完全不同的思路：**重组模型**。不是让 memory 无限膨胀，而是让 memory 定期被"消化"和"重组"，保持高信号状态。

这种思路的范式意义在于：它第一次把 **"Agent 如何从经验中学习"** 从一个模糊的能力描述，变成了一个具体的工程机制设计。

---

## 六、工程启示：如何在你的 Harness 中借鉴 Dreaming 思想

即使你没有使用 Claude Managed Agents，Dreaming 的设计思想可以直接应用到你的 Agent 工程中：

### 6.1 跨 Session 的"反思日志"

在每个 Session 结束时，Agent 写一段简短的"反思日志"——不是记录所有细节，而是提炼出：
- 这次发现的关键 insight
- 犯的错误及下次如何避免
- 未解决的问题

这些日志积累后，定期有另一个 Agent（或同一个 Agent 的另一个 prompt）来阅读并提炼模式。

### 6.2 记忆的"版本化"

不要只是追加 memory。对 memory store 做版本化管理。每次 Dreaming 类似的反思过程后，生成一个新的 memory version，保留旧版本用于回溯。这让 Agent 能够追踪"认知的演进"。

### 6.3 Generator↔ Evaluator + Dreaming 三层架构

在你的 Harness 中，构建三层质量控制：

```
第1层（单 Session 内）：Generator↔ Evaluator 循环 → 保证当前 Session 输出质量
第2层（Session 之间）：Dreaming 调度 → 跨 Session 发现模式，更新 memory
第3层（长期）：定期 review memory versions → 验证记忆质量，淘汰过时内容
```

---

## 结语

Dreaming 不是一个花哨的产品功能。它是 Agent 工程领域第一次系统性地解决**"Agent 如何从经验中学习"**这个问题——通过跨 Session 的记忆重组，让 Agent 不再是每次都从零开始的"失忆机器"。

Compaction 解决了"上下文太满"的问题。Dreaming 解决了"记忆太脏"的问题。前者是空间问题，后者是质量问题。一个完整的 Agent Memory 架构，两个都需要。

**所以，下次当你抱怨 AI Agent 总在重复同样的错误时——也许问题不是它"学不会"，而是我们还没有给它设计一个"在睡眠中整理记忆"的机制。**

---

## 参考文献

- Ars Technica, "Anthropic's Claude Managed Agents can now 'dream,' sort of", May 2026: https://arstechnica.com/ai/2026/05/anthropics-claude-can-now-dream-sort-of/
- Anthropic, "Harness design for long-running application development", Mar 2026: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Anthropic, "Effective harnesses for long-running agents", 2025: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic Claude Platform Docs, Managed Agents Dreams: https://platform.claude.com/docs/en/managed-agents/dreams
- The New Stack, "Anthropic Agent SDK separate credit pools", Jun 2026: https://thenewstack.io/anthropic-agent-sdk-credits/