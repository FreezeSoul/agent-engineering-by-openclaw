# Agent Context Engineering：五个已成熟的上下文管理模式

> **核心问题**：Context Window 变大不等于 Agent 更聪明。随着上下文增长，模型 precision 下降，出现"lost-in-the-middle"和"needle in the haystack"问题。怎么管理这个有限注意力预算，是 2026 年 Agent 工程的核心挑战。本文梳理五个已成熟的上下文管理模式，给出每种的权衡分析和适用边界。

---

## 背景：上下文管理为什么是 Agent 工程的基础设施问题

Anthropic 对"context engineering"的定义简洁：**找到最小的、高信号 token 集合，使期望结果出现的概率最大化。** 这个定义覆盖了进入上下文窗口的所有内容：system instructions、tool definitions、MCP resources、retrieved documents、conversation history、accumulated action history。

问题的根源是 LLMs 的有限注意力预算。每个 token 都在争夺注意力。随着上下文增长，precision 下降，推理能力削弱，模型开始错过应该捕获的信息。Research 将这个现象称为"lost-in-the-middle"和"needle in the haystack"。

这导致了一个反直觉的结论：**给 Agent 更多上下文不等于让 Agent 更聪明。** 正确的做法是系统性地管理上下文内容，而不是简单地塞入更多数据。

---

## 模式一：Progressive Disclosure（渐进式披露）

### 核心思想

传统方案将所有指令一次性加载，但这对多域 Agent 而言是浪费——客服 Agent 回答账单问题时，不需要加载入职培训的指令。另一个极端是为每个域单独部署 Agent，但会引入高 orchestration complexity、duplicate shared logic 和额外的 inter-agent latency。

Progressive disclosure 的解法是**按需分层加载**：Discovery first（仅名称和描述）→ Activation when relevant（完整指令）→ Execution only during task（脚本和参考资料）。

### Agent Skills 作为标准实现

Anthropic 于 2025 年 12 月发布的 **Agent Skills** 是这个模式的标准实现。格式是一个带有 YAML frontmatter 的 markdown 文件：

```yaml
---
name: pdf-extract
description: Extract structured data from PDF documents
---
# Instructions for PDF extraction
[full instruction body: 275-8,000 tokens]
```

平台在启动时只读取 name 和 description（每个 skill 约 80 tokens median）。当 model 判断某个 skill 相关时，才加载完整指令体。脚本和参考资料仅在 execution 期间加载。

OpenAI、Google、GitHub 和 Cursor 在数周内采纳了该规范——这是自 MCP 以来行业最快的协议收敛速度。

### Agent Identity Management（最值得关注的应用）

Progressive disclosure 最有趣的应用不是编码场景，而是**Agent Identity Management**：Agent 不再需要为每个域 spin up 独立的 sub-agent，而是single agent 在需要时 activate 相应 skill，adopting 该 skill 的指令、constraints、tone 和 behavioral patterns。任务完成后返回 base identity。

这正是 Claude Code 的工作方式——它不是一个 PDF Agent 加上一个 spreadsheet Agent 的组合，而是一个在激活相关 skill 时改变身份的 Agent。

### Self-Authoring Skills（重要延伸方向）

当 Agent 重复处理某个任务时，可以将 pattern 提取为新的 skill 文件。Claude Code 的 skill-creator skill 支持此功能：Agent 观察自身成功的行为，generalizes it，然后将其用于 future sessions。

### 权衡分析

| 维度 | 评分 | 说明 |
|------|------|------|
| Accuracy | 高（skill 少时）/ 中（100+ skill 重叠时）| 描述重叠导致 misactivation |
| Latency | 低 | Discovery 数据预加载，仅增加一次 file read |
| Token 成本 | 低（at rest）| 17 个 Anthropic skills discovery 仅 ~1,700 tokens |
| 可维护性 | 中 | 每个 skill 易于维护，但 50+ skill 需要 governance |
| 可靠性 | 中 | Skill selection 错误会在下游 compound |

**关键未解决问题**：当 activated skill 何时被 deactivated？如果没有明确的 pruning logic，多个 activated skills 会随时间摧毁 token 优势。

---

## 模式二：Context Compression（上下文压缩）

### 核心思想

每个 tool call、每个 observation、每个 reasoning step 都会添加到上下文。以一个简单的 ReAct agent 为例：

```
User query → LLM outputs tool call or final answer
Tool executes → Results appended to reasoning + action history
Repeat for N turns
```

每个 turn 都在累积 context。当 tools 检索大量 context 时，context window 很快被 conversation history 和 action history 填满，而 model 真正需要的是 system instructions、tool definitions 和 early task context。

### 三种压缩方案

业界已收敛出三种主要压缩方法：

1. **Keep only top N turns**（硬截断）：简单但丢失早期关键信息
2. **Sliding window compression**（滑动窗口）：保留最近 N turns 不变，用 LLM summarization 压缩更早的 context
3. **Long-term Memory approach**：保留最近 N turns 不变，将早期 history 移至 durable storage，仅在需要时按需检索

主流做法是 **sliding window + summarization hybrids**：保持 recent turns 完整 detail，通过 LLM summarization 压缩 older context。

### Manus 的两个实践细节（工程价值高）

Manus 在实践中发现两个关键细节：

**保留最近 tool calls 的 raw format**。不要压缩最近 tool call 的原始输出，保留 model 的"rhythm"和 formatting style。失去 rhythm 会导致 subtle degradation。

**不要压缩 error traces**。当 tool call 失败时，将 error 和 stack trace 保留在上下文中，帮助 model 避免重复相同的错误。这个技术在 Instructor（用于 structured output retries）等库中有应用，适用于任何调用 tools 的 Agent。

### 权衡分析

| 维度 | 评分 | 说明 |
|------|------|------|
| Accuracy | 中 | Summarization 保留 gist 但丢失细节，所有压缩都是有损的 |
| Latency | 中 | 每次压缩需要 LLM call，可通过 periodic 压缩 amortize |
| Token 成本 | 低 | 长时间运行的 Agent 上收益明显 |
| 可维护性 | 中 | 需要实验：保留什么为 raw、压缩前多少 turns、summaries 的 detail level |
| 可靠性 | 中 | 对长期任务有效，但 critical early details 被 summary away 时会出问题 |

---

## 模式三：Context Routing（上下文路由）

### 核心思想

多域 Agent 通常有多个 knowledge bases、tool sets 和 instruction sets。为每个 query 加载所有域的 context 是浪费——billing question 不需要 onboarding knowledge base，technical support query 不需要 refund policy。

Context routing 在任何内容进入 context window **之前**对 query 进行分类，并 directed to 正确的 context source。

### 三种路由方法

**LLM-powered routing**：使用模型本身对 query 分类并选择合适的 context source。准确率高，但增加 latency 和 cost。

**Hierarchical routing**：使用 lead agent 对 query 进行 triage 到 specialized sub-agents，每个 sub-agent 有自己的 focused context window。

**Rule-based routing**：使用 keyword matching 或 pattern detection。快速且可预测，但 rigid 且当 queries 不匹配 expected patterns 时不可靠。

**Hybrid routing**：结合多种方法。多数生产系统使用 rule-based 作为 fast path，LLM routing 作为 fallback。

### 权衡分析

| 维度 | 评分 | 说明 |
|------|------|------|
| Accuracy | 高（LLM）/ 中（rule-based）| LLM 理解 nuance，rule-based 错过任何 expected patterns 外的内容 |
| Latency | 差异大 | LLM routing 在主任务前增加 inference call；rule-based 几乎 instant |
| Token 成本 | 低 | 通过只加载 relevant context 减少主 inference 的 tokens |
| 可维护性 | 中 | Rule-based 需要手动更新新域；LLM routing 自动适应但更难 debug |
| 可靠性 | 中 | LLM routing 可能 hallucinate routing decisions，需要 human fallback |

---

## 模式四：Evolved Retrieval（演进的检索策略）

### 核心问题

固定 pipeline（query → vector search → inject → generate）无法处理复杂 query。例如 "what themes emerge across this quarter's customer feedback?" 需要跨多个文档连接信息，这是 vector similarity search 无法完成的。

### 三种演进方向

**Agentic RAG**：将 retrieval 置于 Agent 控制下。Agent 决定自己的 search strategy，可以 reformulate queries when results insufficient，可以迭代直到 confident。Retrieval loop 取代了 retrieval pipeline。

**Graph RAG**：添加关系推理。标准 vector search 找到相似文本但无法跨文档连接实体。Graph-based approaches 构建 entity-relationship graphs，支持需要跨多个 source 连接信息的主题和关系问题。

**Self-RAG**：训练模型自行决定何时检索以及批判自己的输出。模型评估是否有足够信息再回答，只在需要时触发检索，在使用前评估检索结果的质量。

最先进的工作将三者结合：agentic control + graph relationships + self-critique。

### 权衡分析

| 维度 | 评分 | 说明 |
|------|------|------|
| Accuracy | 最强 | Agent-controlled retrieval 可以 reformulate queries、try multiple strategies、迭代直到 confident |
| Latency | 高 | 单一问题可能触发 3-5 个 retrieval cycles |
| Token 成本 | 高 | 每个 cycle 都向 context 添加 retrieved chunks 加上 Agent 的 reasoning about strategy |
| 可维护性 | 中 | Debug "why did the agent choose this retrieval strategy?" 比 debug 固定 pipeline 难 |
| 可靠性 | 中 | 需要 guardrails——Agentic RAG 可能在简单问题上 over-retrieve |

---

## 模式五：Tool Management（工具管理）

### 核心问题

MCP 解决了连接问题，但没有解决 context cost 问题。OpenAI 推荐每个 Agent 少于 20 个 tools，准确率在 10 个以上开始下降。90+ tool definitions 意味着超过 50,000 tokens 的 schemas 在 model 开始推理前就已消耗。

### MCP 现状

MCP（Model Context Protocol）由 Anthropic 创建，2024 年 11 月开源，现由 Linux Foundation 下的 Agentic AI Foundation 管理。2026 年初已有数千万次月度 SDK 下载，被 Anthropic、OpenAI、Google、Microsoft 采纳。

**但上下文成本问题仍未解决。**

### 四个未解决的工程问题

**Description quality**：大多数 MCP server 作者为人类编写 tool descriptions，而非为模型。Too vague 导致模型选错 tool；too verbose 浪费 context 在单一 schema 上。

**Tool overlap across MCP servers**：两个不同 server 可能提供相似 capabilities（两个 search tools，两个 file readers）。Without deduplication 或 preference logic，模型 arbitrary 选择。

**No versioning for tool contracts**：当 MCP server 更新其 tool schemas 时，Agent 无法知道。Cache 中的 stale descriptions 导致 silent failures。

**Security surface scales with tool count**：每个连接的 MCP server 都是 attack surface。Tool outputs 可能包含 prompt injection attempts。

### 关键约束

Manus 发现一个 practical constraint：**避免在 iteration 中动态添加或删除 tools**，因为 tool definitions 位于 context 前部，任何 change 都会 invalidates 后续所有 action 的 KV-cache。

### 权衡分析

| 维度 | 评分 | 说明 |
|------|------|------|
| Accuracy | 依赖 description quality | 尚未解决 |
| Latency | 低（discovery）/ 高（mid-iteration change）| 动态改变 tools 会 invalidates KV-cache |
| Token 成本 | 高 | 90+ tools → 50K+ tokens，infrastructure cost 被低估 |
| 可维护性 | 中 | MCP 标准化了接口，但未标准化 description quality、schema conventions 或 versioning |
| 可靠性 | 中 | MCP 标准化了接口，但未标准化 underlying tool 的质量 |

---

## 分层架构：如何组合这五个模式

这五个模式不是 alternatives，而是**在生产 Agent 系统中分层组合**：

```
┌─────────────────────────────────────────────┐
│  Tool Management                            │  ← 定义什么可以进入 context window
│  (MCP token audit, schema quality)          │
├─────────────────────────────────────────────┤
│  Progressive Disclosure                    │  ← 定义什么可以进入 context window
│  (Agent Skills, identity management)        │
├─────────────────────────────────────────────┤
│  Context Routing                           │  ← 管理执行期间保留什么
│  (query classification, domain routing)    │
├─────────────────────────────────────────────┤
│  Context Compression                       │  ← 管理执行期间保留什么
│  (sliding window + summarization)           │
├─────────────────────────────────────────────┤
│  Evolved Retrieval                         │  ← 按需从外部获取知识
│  (Agentic RAG + Graph RAG + Self-RAG)      │
└─────────────────────────────────────────────┘
```

**Practical starting points by scenario**：

- **Long-running tasks**：优先加 Compression。Hybrid sliding window（保持 latest N turns raw，summarise older ones）是最实用的起点
- **Multi-domain agents**：优先加 Routing。即使 keyword-based rules 也能在投资 LLM-based classification 前削减 context bloat
- **Multiple MCP servers**：audit token cost。数一下 tool schemas 在任何 user interaction 前消耗多少 tokens——这个数字通常比预期高得多

---

## 判断性内容

### 五个模式的成熟度排序

| 模式 | 成熟度 | 说明 |
|------|--------|------|
| Progressive Disclosure（Agent Skills）| 高 | Anthropic 规范，主流厂商数周内采纳，Claude Code 生产验证 |
| Context Compression | 高 | sliding window + summarization 已成主流方案 |
| Tool Management | 中 | MCP 接口标准化，但 description quality/versioning/security 未解决 |
| Context Routing | 中 | LLM routing 有效但 cost 高，rule-based 可预测但 rigid |
| Evolved Retrieval（Agentic/Graph/Self-RAG）| 中 | 方向正确，但 latency/token cost /reliability 仍有挑战 |

### 核心判断

**Agent Skills 是 2026 年最重要的上下文管理模式**。不是因为技术最复杂，而是因为它解决了实际问题：让非工程师配置 Agent behavior，让 Agent 从 experience 中学习。它同时解决了三个问题（token efficiency、maintainability、self-improvement），且有一个清晰的演进路径（self-authoring skills）。

**Context Compression 是最容易上手的高收益模式**。对长期运行的 Agent，立即可见 token 成本节省，且实现难度相对低。

**Evolved Retrieval 是未来的方向，但现在是 high investment**。如果你有复杂的多文档分析场景，值得投入；如果是简单问答，不要用它。

**Tool Management 的问题是工程问题，不是架构问题**。MCP 已经是正确的抽象，但 description quality 和 versioning 需要工程实践层面的约束和工具链支持。

---

## 参考文献

- [State of Context Engineering in 2026 - Aurimas Griciūnas / SwirlAI Newsletter](https://www.newsletter.swirlai.com/p/state-of-context-engineering-in-2026) — 五种上下文管理模式的详细分析，包括每种模式的权衡矩阵和 practical implementation details
- [Anthropic Agent Skills Specification - Anthropic](https://docs.anthropic.com/en/docs/agent-build-and-extend/anthropic-agent-skills) — Agent Skills 的官方规范和实现指南
- [Context Engineering Framework: Architecture & 2026 Guide - Atlan](https://atlan.com/know/context-engineering-framework/) — 企业级上下文工程框架的五层架构，包括 Governed Data Layer 作为缺失层的重要性
- [Anthropic Engineering: Effective context engineering for agents - Anthropic](https://www.anthropic.com/engineering/) — 官方工程博客对 context engineering 的定义和最佳实践
- [Manus Agent Framework Lessons - Manus](https://manus.com/) — ReAct agent context bloat 的实践细节，包括 Manus 在 Progressive Disclosure 和 Compression 上的工程经验
