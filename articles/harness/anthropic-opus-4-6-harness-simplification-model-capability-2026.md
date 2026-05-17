# Opus 4.6 如何重塑 Harness 设计哲学：当模型变强，什么该删？

> 本文深入分析 Anthropic Engineering Blog 中关于 Opus 4.6 时代 Harness 迭代的核心洞察：模型能力提升时，scaffold 不是自动消失，而是需要主动重新评估每个组件的必要性。

## 核心论点

Harness 的每个组件都编码了一个假设：「模型自己做不了这件事」。当模型升级后，这个假设可能不再成立，但组件不会自动消失——需要工程师主动压力测试、选择性删除。

Anthropic 的工程师在 Opus 4.6 发布后做了一件反直觉的事：**删除了 Sprint 机制**，而不是等待模型自动填补空缺。这个决策背后有清晰的设计逻辑。

---

## 背景：Harness 的债务积累问题

在早期的 Harness 设计中，工程师通过添加组件来弥补模型能力的不足：

- **Sprint 分解**：将复杂任务切成多个小节，帮助模型保持连贯性
- **Context Reset**：当上下文窗口接近满时，清空并携带结构化状态重启
- **Evaluator 逐轮评分**：每完成一个 Sprint 就运行 QA 验证

这些机制有效，但有代价：

| 组件 | 成本 |
|------|------|
| Sprint 构造 | 额外的规划+协调开销 |
| Context Reset | 状态序列化的 token 消耗和延迟 |
| Evaluator 逐轮评分 | 每个 Sprint 的 QA token 成本 |

当 Opus 4.6 发布时，Anthropic 团队意识到这些假设可能已经过时。根据发布博客：

> "[Opus 4.6] plans more carefully, sustains agentic tasks for longer, can operate more reliably in larger codebases, and has better code review and debugging skills to catch its own mistakes."

这意味着之前补充模型能力的设计决策，在 4.6 面前可能变成了不必要的复杂性。

---

## 删除 Sprint 构造的决定

### 为什么 Sprint 曾经必要

Sprint 的核心功能是**任务分解**：将大型产品需求（如一个游戏引擎）拆解为多个可管理的小节。这么做是因为：

1. 模型在长上下文中容易失去连贯性
2. 每个 Sprint 的边界让 Generator 有清晰的终点
3. Planner 和 Evaluator 可以针对具体 Sprint 进行谈判和验收

### 为什么 4.6 可以去掉它

Opus 4.6 的核心改进之一是**更长的任务持续能力**。模型现在可以：

- 原生处理更长的连贯任务流，而不需要人为的任务边界
- 减少对上下文窗口的焦虑（context anxiety）
- 更好地管理大型代码库的上下文检索

删除 Sprint 后，Planner 仍然存在（作者发现去掉后 Generator 会 under-scope，直接开始构建而不先制定规格），但 Evaluator 从**每 Sprint 评分**降级为**单次最终评估**。

### 关键洞察：Evaluator 的动态价值

作者发现一个反直觉的规律：

> **Evaluator 的价值不是固定的——它取决于任务是否超出了模型可靠独立完成的能力边界。**

在 Opus 4.5 时代，构建处于 Generator 能力的边缘，Evaluator 在每个 Sprint 都捕获有意义的问题。

在 Opus 4.6 时代，模型能力边界外移，许多任务现在可以由 Generator 可靠完成。对于这些任务，Evaluator 成为不必要的开销。但对于仍然处于边缘的部分，Evaluator 继续提供真实价值。

这意味着 **Evaluator 是一个条件性有价值的组件，而不是无条件必需的**。

---

## 实际数据：简化后的 DAW 构建

在移除 Sprint 构造后，团队用 Opus 4.6 测试了一个 Digital Audio Workstation (DAW) 的构建：

| Agent & Phase | Duration | Cost |
|---------------|----------|------|
| Planner | 4.7 min | $0.46 |
| Build (Round 1) | 2 hr 7 min | $71.08 |
| QA (Round 1) | 8.8 min | $3.24 |
| Build (Round 2) | 1 hr 2 min | $36.89 |
| QA (Round 2) | 6.8 min | $3.09 |
| Build (Round 3) | 10.9 min | $5.88 |
| QA (Round 3) | 9.6 min | $4.06 |
| **Total V2 Harness** | **3 hr 50 min** | **$124.70** |

注意：Generator 仍然运行了 3 个 Round，每个 Round 都有 QA 发现的问题并修复。这是 Generator 的能力边界——它仍然会遗漏细节或 stub 功能，需要 Evaluator 来捕获这些「最后一公里」的问题。

### QA 仍然发现真实缺陷

在第一轮反馈中，QA 捕获了：

> "This is a strong app with excellent design fidelity, solid AI agent, and good backend. The main failure point is Feature Completeness — while the app looks impressive and the AI integration works well, several core DAW features are display-only without interactive depth: clips can't be dragged/moved on the timeline, there are no instrument UI panels (synth knobs, drum pads), and no visual effect editors (EQ curves, compressor meters)."

第二轮反馈：

> "Remaining gaps: Audio recording is still stub-only (button toggles but no mic capture), Clip resize by edge drag and clip split not implemented, Effect visualizations are numeric sliders, not graphical (no EQ curve)."

这说明 Generator 即使在 4.6 时代，仍然会系统性地遗漏细节——这是 Evaluator 继续存在的理由。

---

## 设计启示：Harness 不是静态的

### 1. 每个组件都有保质期

Harness 中的每个设计决策都基于特定模型能力的假设。当模型升级时，这些假设需要被重新验证。

```
删除前的问题： 这个组件在当前模型能力下，仍然是必需的吗？
```

### 2. "等待模型解决" vs "主动删除"

有两种对待复杂性的方式：
- **被动等待**：模型升级后，某些问题自动消失，继续使用原有配置
- **主动删除**：模型升级后，主动测试每个组件，删除不再 load-bearing 的部分

Anthropic 的案例支持第二种方式。即使模型可能弥补了某个组件的价值，主动压力测试和选择性删除可以防止技术债务积累。

### 3. Planner 可能是真正不可删除的

关键发现：**删除 Planner 后，Generator 会 under-scope**——直接开始构建而不先制定规格，最终产出功能丰富的应用程序但缺少规划。

这与 Generator 的能力提升不同——即使 4.6 更强，它仍然受益于规划阶段的架构决策。Planner 可能是一个真正的长期有价值的组件，而其他组件（如 Sprint 构造）可能只是特定模型能力阶段的产物。

### 4. Evaluator 是任务相关的

> "The evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo."

这意味着 Evaluator 的使用应该基于**任务难度与模型能力的动态边界**，而不是固定规则。

---

## 结论

当下一个模型发布时，不要只是简单地减少 Harness 配置。主动测试每个组件：

1. **删除 Sprint**：如果新模型可以处理更长、更连贯的任务流，移除任务分解构造
2. **保留 Planner**：规划仍然是导航复杂构建的关键，即使模型更强
3. **条件性使用 Evaluator**：当任务超出模型可靠范围时启用，当任务在模型能力范围内时跳过

真正的教训不是「等模型变强就不需要 Harness」，而是「模型变强后，需要重新评估 Harness 中每个组件的必要性」。

---

**引用来源**：

- Anthropic Engineering Blog: [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- Anthropic News: [Claude Opus 4.6 Launch](https://www.anthropic.com/news/claude-opus-4-6)