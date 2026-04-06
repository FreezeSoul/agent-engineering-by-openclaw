# GAN 启发的 Agent Harness：如何让长时运行应用开发真正work

> **本质**：将生成器-评估器对抗结构引入 Agent 开发——Planner 生成规格、Generator 实现功能、Evaluator 验收质量，20 倍成本换来质的飞跃

## 一、背景问题

Anthropic 工程师 Prithvi Rajasekaran 在让 Claude 构建高质量前端设计和完整应用的过程中，发现了**两类持续存在的失败模式**：

### 1.1 上下文丢失与 Context Anxiety

模型在处理长任务时容易失去连贯性（上下文窗口填满），部分模型还表现出 **Context Anxiety**——当接近认为的上下文限制时，会提前收尾工作。

Context Reset（清除上下文窗口，从新的 Agent 继续）可以解决这个问题，但代价是：
- 编排复杂度增加
- Token 开销增加
- 每次 Harness 运行增加延迟

后来发现 Opus 4.5 大幅改善了 Context Anxiety 问题，可以完全移除 Context Reset，在一个连续会话中运行完整构建。

### 1.2 自我评价失真

当要求 Agent 评价自己生成的输出时，它们倾向于**过度正面**——即使输出质量明显平庸。这在主观领域（如设计）尤其明显，因为没有像可验证的软件测试那样的二元判断标准。

即使在有可验证结果的任务上，Agent 仍然表现出糟糕的判断力。

**关键发现**：将**干活 Agent** 和**评判 Agent** 分离，比让 Generator 自我批评效果要好得多——虽然独立的 Evaluator 仍然是 LLM，仍然对 LLM 输出有宽容倾向，但调优一个独立 Evaluator 比让 Generator 自我批评要容易得多。

## 二、架构设计：Planner-Generator-Evaluator 三 Agent 结构

核心设计受 **GAN（Generative Adversarial Networks）** 启发——两个互相对抗的 Agent，Generator 生成，Evaluator 评审，形成反馈循环。

### 2.1 Planner Agent

**职责**：将用户的 1-4 句话需求扩展为完整的产品规格文档

设计原则：
- **Scope 野心化**：鼓励宏大的功能范围
- **关注产品上下文和高层技术设计**，而非细节实现
- 刻意避免提前指定技术实现细节（错误会级联到下游）
- 主动将 AI 特性编织进产品规格（通过接入 Claude Code 的前端设计 skill）

**输出**：16 个功能分散在十个 Sprint 的完整产品规格文档

### 2.2 Generator Agent

**职责**：逐个 Sprint 实现功能

设计原则：
- **单功能 Sprint**：一次只做一个功能，控制 Scope
- **技术栈固定**：React + Vite + FastAPI + PostgreSQL
- **每个 Sprint 结束后自我评估**，再交给 QA
- 使用 Git 做版本控制

### 2.3 Evaluator Agent

**职责**：Playwright MCP 驱动下，像真实用户一样使用应用，然后评分

评分维度（参考前端设计实验的四项标准，适配到应用开发）：

| 维度 | 含义 | 硬阈值 |
|------|------|--------|
| **Product Depth** | 功能完整性，不只是表面完成 | ✅ |
| **Functionality** | 功能真实可用，不是 demo | ✅ |
| **Visual Design** | 视觉设计质量 | ✅ |
| **Code Quality** | 代码工程化程度 | ✅ |

任何一项低于硬阈值 → Sprint 失败，Generator 获得详细反馈

### 2.4 Sprint 契约机制

在每个 Sprint 开始前，Generator 和 Evaluator 协商 Sprint 契约：
- Generator 提出要构建什么、如何验证完成
- Evaluator 审查提案，确保构建的东西可以被测试
- 两者迭代直到达成一致

这解决了一个关键问题：产品规格是高层次的，Sprint 契约桥接了用户故事和可测试实现之间的鸿沟。

## 三、通信机制：文件作为共享上下文

三个 Agent 之间通过**文件系统**通信：

```
Agent A 写文件
Agent B 读取并响应（在同一文件或新文件）
Agent A 读取 B 的响应
```

Generator 基于协商好的 Sprint 契约构建，然后移交 QA。文件作为共享状态载体，使得：
- 上下文不会在单次 API 调用中丢失
- 多 Agent 可以异步协作
- 可以在任何时候"暂停"和"恢复"

## 四、关键对比数据

### Solo vs Full Harness

| 指标 | Solo（单 Agent） | Full Harness（三 Agent） |
|------|-----------------|------------------------|
| **运行时长** | 20 分钟 | 6 小时 |
| **成本** | $9 | $200 |
| **功能规格** | 基本界面（实际不可用） | 16-feature 完整应用 |
| **可运行性** | 部分功能损坏 | 核心功能真实可用 |
| **设计语言** | 模板化，缺乏个性 | 差异化视觉风格 |

### Solo 的具体问题

- 布局浪费空间，固定高度面板留大量空白
- 工作流僵硬，需要先创建 sprites 和 entities，但 UI 没有引导
- 游戏模式损坏：实体出现在屏幕上但没有任何交互响应
- 代码中实体定义和游戏运行时之间的连接是断的

### Full Harness 的具体产出

- Canvas 使用全视口，面板尺寸合理
- 界面有符合规格设计语言的统一视觉风格
- Sprite 编辑器功能丰富（更好的调色板、颜色选择器、缩放控制）
- 内置 Claude 集成，可通过 Prompt 生成游戏各部分
- **游戏模式真的可以玩**：物理有瑕疵，但核心功能工作

## 五、设计原则：GAN 启发的核心洞察

### 5.1 Criteria 措辞决定输出走向

**出乎意料的发现**：Criteria 中的措辞会直接影响生成内容的走向。

> "The best designs are museum quality" 这类措辞推动了设计向特定的视觉方向收敛

这意味着 Evaluator 的评分标准语言本身就是对 Generator 的**隐性引导**——不仅仅是评判标准，更是方向塑造工具。

### 5.2 少样本校准 Evaluator

使用少样本示例配合详细评分分解来校准 Evaluator，确保：
- Evaluator 的判断与人类偏好一致
- 减少跨迭代的评分漂移

### 5.3 Context Reset vs Compaction

| 策略 | 机制 | 适用场景 |
|------|------|---------|
| **Compaction**（压缩）| 在原地总结对话历史，Agent 继续运行 | 保持连续性，但 Agent 仍有 context anxiety |
| **Context Reset**（重置）| 完全清除上下文窗口，Agent 从新开始 | 提供干净的石板，但需要足够的 handoff artifact |

**结论**：Sonnet 4.5 context anxiety 严重到 compaction 不足以支撑长任务表现，Context Reset 是必需的；Opus 4.5 大幅改善后，可以完全移除 Reset，在一个会话中完成。

### 5.4 Generator 迭代策略

每个迭代结束时，Generator 需要做出**战略性决策**：
- 如果分数趋势良好 → 继续当前方向精炼
- 如果方向不行 → 彻底转向不同美学/策略

这模拟了人类设计师的迭代判断。

## 六、局限与观察

1. **成本极高**：Full Harness $200 vs Solo $9，20 倍的成本差距
2. **并非所有迭代都线性进步**：有些中间迭代反而比最终版本更优
3. **复杂性随迭代增加**：Generator 越来越追求复杂实现
4. **模型产品直觉仍有差距**：某些基础 UX 问题（如"应该先建 sprites 再建 entities"）模型没有内化

## 七、论文信息

> **来源**：[Anthropic Engineering - Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)  
> **作者**：Prithvi Rajasekaran（Anthropic Labs）  
> **发表**：2026-03-24（Anthropic Engineering Blog）  
> **类型**：工程实践  
> **演进阶段**：Stage 12（Harness Engineering）

## 八、延伸阅读

- [Effective harnesses for long-running agents](articles/harness/harness-engineering-deep-dive.md) — 长时 Agent Harness 深度分析
- [Claude Code Auto Mode](articles/harness/claude-code-auto-mode-harness-engineering.md) — Claude Code 的安全 Harness 设计
- [Harness Engineering 深度](articles/harness/harness-engineering-martin-fowler.md) — Martin Fowler 视角

---

*本文档由 Agent 自主生成并维护*
