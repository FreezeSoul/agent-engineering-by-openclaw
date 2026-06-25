# Advisor Strategy：Anthropic 官方定义的 Agent 分级协作范式

> 核心判断：Advisor Strategy 的本质是在 API 层面实现「按需智能」——让小模型驱动、大模型思考，比全流程跑大模型更聪明，比纯 prompt 调优更省成本。

---

## 背景：每个 Agent 开发者都在面对的永恒困境

做 AI 编程或 Agent 开发，迟早会遇到一个经典困境：**任务复杂度差异极大，但模型只有一个**。

- 简单任务（改个变量名、查个文档）：用 Sonnet 4 跑完，成本低，速度快
- 复杂任务（重构整个模块、设计 API 方案）：必须上 Opus 4，否则上下文窗口不够、推理深度不够

传统的解法有两个：

1. **全量跑大模型**：质量保证，但成本爆炸——简单任务也在按 Opus 的价格计费
2. **全量跑小模型**：成本可控，但复杂任务频频失败，debug 成本比省下的钱还多

Anthropic 的答案，是一个设计上的「小逆转」：

> **不要让大模型驱动任务，让小模型驱动，大模型只在关键时刻出手。**

这就是 **Advisor Strategy**。

---

## 核心架构：Executor + Advisor，单次请求内的协作

Advisor Strategy 的架构非常清晰，用一张图就能说明白：

```
┌─────────────────────────────────────────────────────┐
│            Sonnet 4（Executor，驱动者）              │
│                                                     │
│   工具调用 → 结果判断 → 遇到复杂决策 →  ┌──────────┐│
│                                        │  咨询    ││
│   ←──────────────────────────── 计划返回 │  Opus 4  ││
│                                        │（Advisor）││
│                                        └──────────┘│
│                       继续执行 ← 计划/修正/停止信号 │
└─────────────────────────────────────────────────────┘
```

**关键点**：

- **Executor**（这里用的是 Sonnet 4）负责端到端执行：调用工具、读取结果、向用户交付产出
- **Advisor**（这里用的是 Opus 4）**不调用工具，不直接输出用户可见内容**，只返回计划、修正或停止信号
- **协作发生在一 / 次 / 请 / 求 / 内**，不需要额外部署、没有跨模型状态管理

这是对传统 sub-agent 编排模式的「逆转」：

| | 传统 sub-agent 模式 | Advisor Strategy |
|---|---|---|
| 驱动者 | 大模型（Orchestrator） | 小模型（Executor） |
| 任务分解 | 大模型提前分解 | 小模型运行时按需升级 |
| 边界 | 明确的任务分工 | 模糊的智能升级边界 |
| 复杂度 | 需要自己管理 | API 原生支持 |

传统模式是大模型在「指挥」，把任务分解后交给小模型执行。Advisor Strategy 反过来——小模型主导，碰到过不去的坎才请教大模型。这不是编排，这是**按需智能**。

---

## 数字说话：效果有多显著？

Anthropic 给了三组 benchmark 数据，非常有说服力：

### SWE-bench Multilingual（软件工程任务）

> Sonnet 4.6 + Opus 4 Advisor vs. Sonnet 4.6 单独

- **+2.7 个百分点**的精度提升
- **成本下降 11.9%**per agentic task

质量提升的同时，成本还下降了——这个组合拳非常漂亮。

### BrowseComp（信息检索任务）

| 配置 | Score |
|------|-------|
| Haiku 4.5 单独 | 19.7% |
| Haiku 4.5 + Opus 4 Advisor | **41.2%** |
| Sonnet 4.6 单独 | 基准 |
| Sonnet 4.6 + Opus 4 Advisor | 基准 + 提升 |

**Haiku + Advisor 的分数是 Haiku 单独的 2 倍以上**。这说明在小模型上，Advisor 的效果更加显著——因为小模型的推理上限更低，遇到瓶颈的概率更高，Advisor 能补上的空间更大。

### 成本对比

| 配置 | 相对成本（vs Sonnet Solo）|
|------|--------------------------|
| Sonnet 4.6 + Opus 4 Advisor | -11.9%（省钱！）|
| Haiku 4.5 + Opus 4 Advisor | -85%（大模型价格的 15%）|

Haiku + Advisor 的成本只有 Sonnet Solo 的 15%，但精度接近 Sonnet Solo 的水平。这个数字非常震撼。

---

## 技术实现：API 怎么写

Advisor 不是一个独立服务，是 **Messages API 里的一个 tool**：

```python
response = client.messages.create(
    model="claude-sonnet-4-6",  # Executor：实际执行任务的模型
    tools=[
        {
            "type": "advisor_20260301",  # Advisor 工具类型
            "name": "advisor",
            "model": "claude-opus-4-6",   # Advisor：只在关键时刻介入
            "max_uses": 3,                 # 每次请求最多咨询 3 次（成本控制）
        },
        # 你的其他工具：web_search, bash, file editing...
    ],
    messages=[...]
)
```

**技术细节**：

- Executor 遇到需要判断的时刻，**内部调用 Advisor**，不需要你写任何调用逻辑
- 整个过程在一个 `/v1/messages` 请求内完成，**没有额外的网络往返**
- Advisor 返回的内容（通常 400-700 tokens），由 Executor 继续执行或作为最终输出

这个实现有一个微妙之处：虽然文档说「Executor decides when to invoke it」，但实际判断逻辑是 **API 内部决定的**，不是由 prompt 控制的。这意味着：不是 Sonnet「调用」了 Opus，而是 Sonnet 在遇到特定模式时，API 自动路由到了 Opus。用户体验上，是 Sonnet 突然变得「更聪明了」。

---

## 战略意义：Harness 范式的分层演进

Advisor Strategy 的出现，需要放在 Anthropic 近期一系列动作的背景下来看：

| 时间 | 发布 | 角色 |
|------|------|------|
| 2026-03 | Skill-Creator | Agent 的**技能创作**生态 |
| 2026-03 | Advisor Tool | Agent 的**运行时协作**生态 |
| 2026-06 | Knowledge Work Plugins | **企业级垂直 Agent** 落地参考 |

**Skill 系统**处理的是「Agent 的能力边界定义和持续改进」——一次性创作，长期复用。

**Advisor 工具**处理的是「推理过程中的智能升级」——按需调用，单次生效。

这两个是**互补的**：Skill 定义了 Agent 擅长什么，Advisor 在运行时弥补了 Executor 模型能力上限的不足。

如果用 Harness 的视角来看，Advisor Strategy 是一个**更细粒度的 meta-harness**：

- 传统 Harness：定义 Agent 什么时候该停止（Stop Condition）
- Advisor Strategy：定义 Agent 在什么时候该升级智能（Upgrade Condition）

这是一个有意思的范式演进——从「防止 Agent 跑偏」到「主动提升 Agent 能力上限」。

---

## 实践建议

### 适合场景

- **任务复杂度差异大**：一个任务里混合了简单和复杂的子任务
- **成本敏感**：不想为简单任务支付 Opus 的价格
- **推理深度要求高**：复杂决策需要 Opus 级别的推理，但大多数时候 Sonnet 足够

### 不适合场景

- **简单任务全集**：如果任务本身很简单，Executor 自己就能搞定，Advisor 的作用不大
- **低延迟要求**：虽然 API 内部调用没有额外往返，但 Executor 等待 Advisor 响应会增加一些内部延迟
- **需要频繁工具调用**：Advisor 不调用工具，如果任务需要大量工具交互，Executor 模型的选择更重要

### 如何评估

```bash
# 推荐对比测试
1. Sonnet solo（基准）
2. Sonnet + Opus Advisor（推荐配置）
3. Opus solo（上限参考）

运行你的 eval suite，对比质量 + 成本，选择最优配置
```

---

## 开放问题

笔者认为，Advisor Strategy 有几个值得思考的问题：

**1. 多轮 Advisor 调用如何影响 Agent 的可预测性？**

Executor 每次调用 Advisor 的时机是 API 内部决定的，这意味着同一个输入，每次运行可能 Advisor 被触发的次数不同。这对需要确定性输出的场景是一个隐患。

**2. Advisor Strategy 如何与 Multi-Agent 编排系统共存？**

CrewAI、LangGraph 等框架有明确的 Orchestrator → Sub-Agent 关系。Advisor Strategy 在概念上与 Multi-Agent 有重叠，但实现粒度更细。两者如何协作，目前没有最佳实践。

**3. 角色专用 Agent 的时代即将到来？**

Anthropic 的 Knowledge Work Plugins（11 个企业级 Agent 技能包）和 Advisor Strategy 结合，可能预示着一个趋势：未来的 Agent 不是通用的，而是在特定角色上配置了专属技能和升级路径。

---

**引用来源**：

> "Pair Opus as an advisor with Sonnet or Haiku as an executor, and get Opus-level intelligence in your agents at a fraction of the cost."
> — Anthropic, [The advisor strategy: Give agents an intelligence boost](https://claude.com/blog/the-advisor-strategy)

> "In our evaluations, Sonnet with Opus as an advisor showed a 2.7 percentage point increase on SWE-bench Multilingual 1 over Sonnet alone, while reducing cost per agentic task by 11.9%."
> — Anthropic, [The advisor strategy](https://claude.com/blog/the-advisor-strategy)
