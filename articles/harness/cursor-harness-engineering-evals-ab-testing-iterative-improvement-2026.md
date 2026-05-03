# Cursor 如何持续迭代 Agent Harness：一个工程方法论

> 来源：[Continually improving our agent harness](https://www.cursor.com/blog/continually-improving-agent-harness)，Cursor Engineering Blog，2026-04-30  
> 标签：`harness` `cursor` `evaluation` `context-engineering` `production`

---

## GAP 前置分析

**G（Goal）**：回答一个被长期低估的问题——Harness Engineering 不是写 prompt，而是构建一套可测量、可迭代、可迁移的工程系统。

**A（Audience）**：正在构建或使用 AI Coding Agent 的工程师和技术负责人，想理解如何让 agent 在生产环境真正可靠，而不是只在 demo 里看起来不错。

**P（Problem）**：业界对 harness 的理解普遍停留在"系统提示词技巧"层面，忽略了它作为独立工程学科的系统性——测量体系、迭代流程、模型适配、降解追踪。这导致大多数团队无法系统性地改进 agent 行为。

---

## PEC 骨架

### P（Position）——300字内确立核心主张

Cursor 的这篇文章揭示了一个被大多数团队忽视的事实：**Harness Engineering 是一门工程学科，不是 prompt 技巧的集合**。

Cursor 将构建 harness 的方式类比为构建任何 ambitious software product：先有 vision，再形成 hypothesis，执行实验，用定量的 evals 和真实使用数据迭代。这套方法论的核心不是某个具体的 prompt 技巧，而是一套**测量 → 假设 → 实验 → 迭代**的闭环系统。

文章揭示的核心张力在于：harness 和 model 共同决定 agent 质量，但"质量"本身难以定义。Cursor 的解法是构建多层测量体系——离线 CursorBench 基准测试提供快速标准读数，在线 A/B 实验追踪真实使用中的 Keep Rate（agent 生成的代码在用户代码库中留存的比例）和用户满意度语义评分。这两套体系互相补充：基准测试速度快但不完美，在线实验反映真实价值但成本高。

更值得注意的是，Cursor 展示了模型适配的深度不仅止于"选择哪个模型"，而是深入到**每个模型训练时使用的工具格式**（OpenAI patch-based vs Anthropic string replacement），以及针对特定模型 behavior quirk 的 prompt 调优（例如某个模型的"context anxiety"问题）。

---

### E（Evidence）——证据链与逻辑桥接

**1. Context Window 演进路线图**

Cursor 展示了一个清晰的演进路径：

| 阶段 | 特征 | 代表做法 |
|------|------|---------|
| 2024年初 | 大量 guardrails + 静态上下文 | 强制暴露 lint 错误、限制单轮 tool call 数量、预加载语义匹配代码段 |
| 现在 | 动态上下文 + guardrails 下撤 | 仅保留 OS/git status/current files，agent 自主拉取所需上下文 |

逻辑桥接：模型能力增强 → 人类设计的 guardrails 从必要变多余 → 动态获取取代静态注入。这是能力驱动的适应性架构，不是功能堆砌。

**2. 双轨测量体系**

```
离线: CursorBench (公开基准)
  → 优点: 快速、标准化、可跨时间对比
  → 局限: 近似真实使用，不等于真实使用

在线: A/B 实验 (真实用户)
  → Keep Rate: 追踪 agent 提案代码在 N 天后的留存率
  → 语义满意度: LLM 读取用户对 agent 首轮输出的反应
  → 指标: latency / token efficiency / tool call count / cache hit rate
```

逻辑桥接：质量无法用单一指标定义，需要多个正交维度；在实验成本和信号质量之间取得平衡。

**3. Tool Call 错误分类体系**

Cursor 建立了严格的错误分类：

| 分类 | 含义 | 处理方式 |
|------|------|---------|
| Unknown Error | harness bug | 任何工具超过阈值立即告警 |
| Expected Errors | 模型偶尔错误 | 按原因细分为 InvalidArguments/UnexpectedEnvironment/ProviderError |
| UserAborted / Timeout | 用户主动中断/超时 | 单独分类，不计入质量评估 |

关键洞察：Tool call 错误不会停留在当下，会在 context 中累积造成"context rot"——历史错误会污染后续决策质量。这解释了为什么工具错误率是系统性指标而非局部指标。

**4. 模型适配的深度**

- **工具格式适配**：OpenAI 模型训练使用 patch-based 编辑格式，Anthropic 模型使用 string replacement。给模型它不熟悉的工具格式会导致额外的 reasoning token 消耗和更多错误。Cursor 在 harness 层面为每个模型配置它训练时使用的格式。

- **行为适配**：Claude 模型更 intuitive，容忍 imprecise 指令；OpenAI 模型更 literal，要求精确指令-following。Harness 对不同供应商甚至不同版本提供定制 prompt。

- **Context Anxiety 问题**：Cursor 观察到某个模型在 context window 接近满载时开始拒绝工作（"任务看起来太大"），通过 prompt 调整减轻了这一行为。这说明模型 quirks 可以通过 harness 层缓解，而不是必须等模型修复。

**5. 自动化修复流水线**

Cursor 运行 weekly Automation（Cloud Agent）， equipped with skill that teaches the model 如何搜索日志、surface 问题、create/update tickets in Linear。他们声称在一轮 focused sprint 中将 unexpected tool call errors 降低了**一个数量级（order of magnitude）**。

关键机制：Cloud Agents 可以并行 kick off fixes for many issues at once，trigger directly from Linear。这是"software factory for agent harness"概念的具体实现——**用 agent 构建 agent harness**。

---

### C（Conclusion）——结论与 Implication

**核心结论**：Harness engineering 是独立于模型选择的工程学科，需要独立的测量基础设施、迭代流程和专业积累。

**具体行动项**：

1. **建立双轨测量体系**：不要只依赖基准测试，在真实使用中追踪 Keep Rate 和语义满意度。
2. **构建错误分类体系**：将工具调用错误分为 expected/unexpected，针对 expected errors 建立 per-tool/per-model baseline，用异常检测识别回归。
3. **深度适配而非通用配置**：每个模型有不同的工具格式偏好和行为特征，harness 需要模型特定配置。
4. **用 agent 维护 agent**：考虑用 Cloud Agent 实现 harness 自身的持续改进和 bug 修复。

**行业含义**：未来 multi-agent 系统（planner/edit/debug 分离）的编排能力将居住在 harness 层，而非单一 agent 内部。这意味着 harness engineering 的重要性只会增加。

---

## 自检清单

| 检查项 | 状态 |
|--------|------|
| GAP×3 完成 | ✅ G（工程学科定位）、A（工程师受众）、P（系统性 vs 技巧性矛盾） |
| PEC×4 完成 | ✅ P（300字主张）、E（5条证据链+逻辑桥接）、C（行动项+行业含义） |
| 逻辑桥接每条都有 | ✅ 每条 evidence 都回答了"为什么能证明论点" |
| 来源一手引用 | ✅ Cursor Engineering Blog 原文，2026-04-30 |
| 与 Projects 主题关联 | ✅ 两者都围绕 harness engineering 主题，Articles 分析 Cursor 方法论，Projects 推荐 AutoHarness 实现框架 |
| 中文输出 | ✅ |
| 无过时信息 | ✅ 基于一手来源的最新内容 |