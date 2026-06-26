---
name: QwenLM/Qwen-AgentWorld
description: 原生语言世界模型 — 用长链思维推理模拟 Agent 在 MCP、Search、Terminal 等 7 个统一域的环境，是 Qwen 团队 2026-06-22 发布的 Agent 研究基础设施。
owner: QwenLM
repo: Qwen-AgentWorld
stars: 533
license: Apache-2.0
created: 2026-06-22
added: 2026-06-26
tags: [language-world-model, agent-eval, moe, qwen, agent-research, benchmark]
related_article: ../articles/research/openai-agents-transforming-work-research-2026.md
---

# QwenLM/Qwen-AgentWorld — Agent 语言世界模型

> **仓库**：[github.com/QwenLM/Qwen-AgentWorld](https://github.com/QwenLM/Qwen-AgentWorld)
> **Stars**：533 ⭐ (截至 2026-06-26)
> **License**：Apache-2.0
> **首次发布**：2026-06-22
> **关联主题**：Agent 研究 / 语言世界模型 / Agent 评测
>
> **关联 Article**：[OpenAI 研究：AI Agent 重塑工作方式](../articles/research/openai-agents-transforming-work-research-2026.md)

---

## 项目定位

**Qwen-AgentWorld** 是阿里 Qwen 团队 2026-06-22 发布的 Agent 研究基础设施项目，包含两个核心组件：

1. **Qwen-AgentWorld-35B-A3B**：原生语言世界模型（MoE，35B 总参 / 3B 激活，256K 上下文）
2. **AgentWorldBench**：覆盖 7 个统一域（MCP / Search / Terminal / GUI / Code / Tool / Web）的 Agent 评测 benchmark

项目的核心洞察是：**Agent 环境本身可以被语言模型模拟**。传统 Agent 研究依赖真实环境（真实 API、真实工具），而 Qwen-AgentWorld 提出**用 LLM 模拟 Agent 运行环境**——这让大规模 Agent 评测成为可能，且成本可控。

---

## 技术架构亮点

### 1. 原生语言世界模型 (Language World Model)

AgentWorld 的核心创新是**语言世界模型**概念——一个能通过长链思维（long chain-of-thought）推理来**模拟 Agent 环境状态转移**的语言模型：

```
传统 Agent 评测：  Agent → 真实环境 API → 真实反馈
Qwen-AgentWorld：  Agent → LLM 模拟环境 → 模拟反馈
```

这类似 AlphaGo 用 MCTS 模拟围棋局面——但 Qwen-AgentWorld 把这个思路推广到 **Agent 环境的通用模拟**。

### 2. MoE 架构：35B 总参 / 3B 激活

模型采用 MoE 架构：

- **总参数**：35B（专家网络总和）
- **激活参数**：3B（每次推理实际激活）
- **上下文长度**：256K

这种「高容量 + 低推理成本」的 MoE 设计特别适合**大规模 Agent 评测场景**——评测需要频繁调用环境模拟模型，每次调用的成本必须可控。

### 3. 7 域统一评测 (AgentWorldBench)

AgentWorldBench 覆盖 7 个 Agent 核心域：

| 域 | 评测目标 | 典型任务 |
|----|---------|---------|
| **MCP** | Model Context Protocol 工具调用 | 多工具组合调用 |
| **Search** | 信息检索 | 多轮搜索 + 整合 |
| **Terminal** | 命令行操作 | 复杂 shell 任务 |
| **GUI** | 图形界面交互 | 桌面应用操作 |
| **Code** | 代码生成与执行 | 长程编程任务 |
| **Tool** | 通用工具使用 | API 链式调用 |
| **Web** | 网页交互 | 表单填写、数据提取 |

**关键设计**：7 个域共享同一套评测框架（基于语言世界模型的环境模拟），这意味着评测结果**跨域可比**——可以量化「同一个 Agent 在不同域的能力分布」。

---

## 与 OpenAI Agent 研究的互补关系

R545 同时收录了 OpenAI 的 [How agents are transforming work](../articles/research/openai-agents-transforming-work-research-2026.md) 研究论文。这两篇产出构成 2026 H2 Agent 研究的**工具层 + 现象层**完整闭环：

| 维度 | OpenAI 研究 | Qwen-AgentWorld |
|------|------------|----------------|
| **视角** | 真实用户行为 | 模拟环境 benchmark |
| **数据源** | 大规模部署 | 7 域合成环境 |
| **评测对象** | 人类 + Agent 协作 | Agent 单体能力 |
| **输出** | 经济学发现 | 模型权重 + 评测榜单 |
| **回答的问题** | Agent 在真实工作中表现如何？ | 如何系统化评测 Agent 能力？ |
| **时间** | 2026-06-25 | 2026-06-22 |

**闭环逻辑**：
- OpenAI 提供**现象证据**（Agent 改变工作）
- Qwen-AgentWorld 提供**评测工具**（如何度量 Agent 能力）
- 两者互补：没有评测工具的现象是轶事，没有现象的评测是 benchmark 分数

R545 这对产出共同回答了「Agent 工程社区最需要什么」：**真实影响数据 + 可复现评测工具**。

---

## 实际应用场景

### 场景 1：Agent 训练数据合成

传统 Agent 训练数据来自人工标注或真实部署，成本高且规模受限。Qwen-AgentWorld 提供：

```python
# 用 Qwen-AgentWorld 模拟环境生成训练数据
from qwen_agent_world import WorldModel

world = WorldModel(model="Qwen/Qwen-AgentWorld-35B-A3B")
trajectory = world.simulate(
    task="查找订单 #12345 的状态",
    agent_actions=["调用 API", "解析响应", "格式化输出"],
    max_steps=20
)
# 用 trajectory 训练下游 Agent
```

### 场景 2：Agent 评测

```python
from qwen_agent_world import AgentWorldBench

bench = AgentWorldBench(
    domains=["mcp", "search", "terminal", "code", "tool"],
    n_tasks_per_domain=100
)
results = bench.evaluate(agent=my_agent)
print(results.summary())  # 跨域能力分布
```

### 场景 3：Agent 调试与失败分析

```python
# 重放失败的 Agent 任务
failure_replay = world.replay(
    trajectory=failed_trajectory,
    perturbation="swap_tool_call_order"
)
# 分析扰动后的环境响应，理解失败原因
```

---

## 与 R521 agent-apprenticeship 的协同

R521 收录的 [Forsy-AI/agent-apprenticeship](../projects/forsy-ai-agent-apprenticeship-post-training-signal-collector-893-stars-2026.md)（893⭐）专注于**真实部署中的 post-training signal 收集**——把生产环境的 Agent 行为数据收集起来作为持续改进的基础。

Qwen-AgentWorld 与 Forsy-AI 形成**互补关系**：

| 维度 | Qwen-AgentWorld | Forsy-AI/agent-apprenticeship |
|------|----------------|------------------------------|
| **数据来源** | 合成模拟环境 | 真实部署环境 |
| **评测时间** | 开发阶段 | 生产阶段 |
| **评测成本** | 低（可控模拟） | 高（真实用户） |
| **评测规模** | 高（可批量模拟） | 中（依赖部署量） |
| **评测真实性** | 中（受模型能力限制） | 高（真实场景） |

**协同工作流**：
1. **开发阶段**：用 Qwen-AgentWorld 快速迭代 Agent 实现，定位明显问题
2. **部署阶段**：用 Forsy-AI 收集真实信号，发现模拟环境无法捕捉的边界 case
3. **持续改进**：用真实信号 fine-tune Agent，然后回到开发阶段重新评测

R545 + R521 这对项目构成了 Agent 评测的**完整生命周期工具链**。

---

## 项目亮点总结

1. **首创「语言世界模型」概念**：用 LLM 模拟 Agent 环境，类似 AlphaGo MCTS 但推广到通用 Agent
2. **MoE 架构实用化**：35B/3B 设计平衡容量与推理成本，特别适合评测场景
3. **7 域统一评测框架**：跨域可比，覆盖 MCP/Search/Terminal/GUI/Code/Tool/Web 全场景
4. **Apache-2.0 License**：完全开源，包括模型权重和评测 benchmark
5. **完整 release 链**：HuggingFace + ModelScope 双发布，国内用户可访问
6. **2026 H2 Agent 研究基础设施标杆**：与 OpenAI 真实用户研究形成现象-工具互补

---

## 局限性与开放问题

Qwen-AgentWorld 作为新兴项目，仍有以下局限：

1. **模拟真实性边界**：语言世界模型能模拟的环境类型受 LLM 能力限制，物理世界 / 复杂 GUI 可能失真
2. **3B 激活参数的容量上限**：对于复杂 7 域评测，3B 激活可能不够
3. **AgentWorldBench 任务覆盖度**：每个域 100 个任务对真实 Agent 评测仍偏少
4. **与真实部署的差距**：合成环境评测结果与生产表现的相关性仍需更多验证

这些问题也是 R541 / R528 收录的真实案例研究（OpenAI GPT-5 免疫学 / Wasmer Codex）所关心的——**模拟评测 vs 真实部署**的差距如何弥合，是 2026 H2 Agent 评测领域的核心开放问题。

---

## 总结

Qwen-AgentWorld（533⭐）是 R545 收录的第二个**Agent 研究基础设施级**项目（第一个是 R521 Forsy-AI）。它代表了 Agent 评测从「静态 benchmark」向「动态环境模拟」的方法论转变，与 OpenAI 的真实用户研究形成完美互补。

对于 Agent 工程师，这意味着：
- **不要只用 HumanEval / SWE-bench** 这类静态 benchmark
- **关注 AgentWorldBench 等动态环境评测**——它们更接近真实使用
- **结合真实部署信号**（Forsy-AI 路线）和模拟环境评测（Qwen-AgentWorld 路线），构建完整的评测体系

R545 + R521 + R541 + R528 这四篇产出共同构成 2026 H2 Agent 工程的**评测方法论完整图景**。

---

**参考资料**：
- Qwen-AgentWorld GitHub: [github.com/QwenLM/Qwen-AgentWorld](https://github.com/QwenLM/Qwen-AgentWorld)
- Technical Report: [arxiv.org/abs/2606.24597](http://arxiv.org/abs/2606.24597)
- Qwen Blog: [qwen.ai/blog?id=qwen-agentworld](https://qwen.ai/blog?id=qwen-agentworld)
- HuggingFace: [huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B](https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B)
- 关联 Article：[OpenAI 研究：AI Agent 重塑工作方式](../articles/research/openai-agents-transforming-work-research-2026.md)
- 关联项目：[Forsy-AI/agent-apprenticeship](../projects/forsy-ai-agent-apprenticeship-post-training-signal-collector-893-stars-2026.md) (893⭐)
- 关联案例：[OpenAI GPT-5 + 免疫学家 Derya 案例](../articles/case-studies/openai-gpt5-immunology-mystery-derya-unutmaz-2026.md)