# LangChain Deep Agents：子 Agent 隔离与 SKILL.md 渐进式披露的工程架构

> 本文解读 LangChain Deep Agents 的两大原生原语：**Subagents**（上下文隔离）和 **Skills**（SKILL.md 渐进式能力披露），以及它们如何共同解决 context bloat 与 context rot 这两个生产级 Agent 的核心工程问题。

## 核心命题

当一个 Agent 在长程任务中调用数十次工具、读取大量文件之后，它的 context window 会趋近于饱和，模型开始进入「低效区间」——这是 context rot 现象。LangChain Deep Agents 提出的解法是：**让子 Agent 在独立上下文中工作，让 Skills 按需加载到 context**。这两个原语共同构成了生产级多 Agent 系统的两大支柱。

---

## 一、Context Rot：被低估的生产级 Agent 问题

### 1.1 问题的本质

Chroma 的研究（[Context Rot Research](https://research.trychroma.com/context-rot)）指出：当模型的 context window 趋近于满载时，其完成任务的能力会显著下降。HumanLayer 将这个区间称为 **"dumb zone"**——模型仍然在生成 token，但质量已经显著下降。

这在单 Agent 架构中尤为突出。当一个 Agent 需要：
- 执行 20 次 web search 收集信息
- 读取 15 个文件理解代码库
- 多次调用 tools 获取中间结果

这些中间结果会填满 context window，但它们大多数只在中间过程有意义，最终只需要一个答案。

### 1.2 业界当前的误区

大多数 Agent 框架（包括早期的 LangChain）的做法是：将所有中间结果累积到主 context 中，让主 Agent 自己消化。这在短任务中没问题，但在生产级长程任务中会导致：

| 症状 | 影响 |
|------|------|
| Context 趋近满载 | 模型推理质量下降（进入 dumb zone）|
| 工具调用信息冗余 | 主 Agent 需要理解「是如何得出这个结论的」而非「结论是什么」|
| 上下文污染 | 中间步骤的思考过程干扰最终决策 |

> 笔者认为，这个问题在 2026 年之前被严重低估——大多数 benchmark 只测试短程任务，无法反映 context rot 对生产级 Agent 的真实影响。

---

## 二、Subagents：隔离上下文的工程设计

### 2.1 核心设计

Deep Agents 的 Subagent 机制允许将工作委托给**隔离的 Agent 实例**，每个 Subagent 有自己的 context window。主 Agent 只接收最终结果，而非 20 次工具调用的中间过程。

```python
from deepagents import create_deep_agent

research_subagent = {
    "name": "research-agent",
    "description": "Used to research more in depth questions",
    "system_prompt": "You are a great researcher",
    "tools": [internet_search],
    "model": "openai:gpt-4o",  # 可选：覆盖主 agent 模型
}

agent = create_deep_agent(
    model="claude-sonnet-4-5-20250929",
    subagents=[research_subagent]
)
```

### 2.2 Subagent 的使用场景

| 场景 | 为什么需要 Subagent |
|------|---------------------|
| **Context Preservation** | 多步骤任务会污染主 context，Subagent 隔离工作过程 |
| **Specialization** | 不同团队可以开发不同垂直领域的 Subagent |
| **Multi-Model** | Subagent 可以使用不同的模型（如用小模型处理简单任务降低延迟）|
| **Parallelization** | Subagent 可以并发运行，主 Agent 等待所有结果 |

### 2.3 通用 Subagent：镜像主 Agent 能力

Deep Agents 内置了一个**通用 Subagent**，它镜像主 Agent 的 system prompt、tools 和 model。这个设计非常聪明——主 Agent 不需要为每个任务定义专门的 Subagent，只需要指定任务名称即可：

```python
# 主 Agent 不需要为每次搜索定义专门的 Subagent
task(name="general-purpose", task="Research quantum computing trends")
# Subagent 执行所有搜索，返回摘要给主 Agent
```

### 2.4 最佳实践

**描述要清晰**——主 Agent 通过 description 决定调用哪个 Subagent：

```python
# ✅ 好的描述
"Analyzes financial data and generates investment insights with confidence scores"

# ❌ 差的描述
"Does finance stuff"
```

**Tool set 要精简**——只给 Subagent 它需要的工具：

```python
# ✅ 好的：聚焦的工具集
email_agent = {
    "name": "email-sender",
    "tools": [send_email, validate_email],
}

# ❌ 差的：工具过多
email_agent = {
    "name": "email-sender",
    "tools": [send_email, web_search, database_query, file_upload],
}
```

---

## 三、Skills：SKILL.md 渐进式能力披露

### 3.1 问题的另一面：工具过载

即使解决了 context bloat，还有另一个问题：当 Agent 有几十个工具时，选择哪个工具本身就是一种认知负担。传统的 RAG 方式是将工具描述全部塞入 context，但这会：

1. 占用大量 context 空间
2. 让模型在大量相似工具描述中做出次优选择
3. 无法表达工具之间的依赖关系和适用场景

### 3.2 Skills 的解法：按需加载

Skills 采用了**渐进式披露**（Progressive Disclosure）模式：

- **Skill 描述**（名称 + 一句话说明）：预加载到 context window
- **Skill 主体**（完整 SKILL.md 指令）：仅在 Agent 决定使用该 skill 时才加载

```
┌─────────────────────────────────────────────────┐
│ Context Window (预加载)                          │
│ ─────────────────────────────────────────────── │
│ Skill Name      │ Skill Description             │
│ deploy          │ Deploy to production          │
│ review-pr       │ Review pull requests          │
│ analyze-code    │ Analyze codebase structure    │
└─────────────────────────────────────────────────┘
                    ↓ Agent 决定需要 deploy
┌─────────────────────────────────────────────────┐
│ Context Window (按需加载)                        │
│ ─────────────────────────────────────────────── │
│ [之前的内容...]                                  │
│                                                 │
│ SKILL.md (deploy) 内容被加载：                  │
│ 1. Run tests: `npm test`                       │
│ 2. Build: `npm run build`                       │
│ 3. Deploy: `npm run deploy:prod`               │
│ 4. Verify health endpoint                       │
└─────────────────────────────────────────────────┘
```

### 3.3 SKILL.md 规范

Skills 使用 [agentskills.io](https://agentskills.io/?ref=blog.langchain.com) 规范，结构如下：

```markdown
---
name: deploy
description: Deploy to production
version: 1.0.0
tags: [deployment, production]
---
# Deploy to Production

When the user asks to deploy, follow these steps:
1. Run tests: `npm test`
2. Build the application: `npm run build`
3. Deploy to production: `npm run deploy:prod`
4. Verify deployment: Check the health endpoint
Always confirm with the user before deploying to production.
```

### 3.4 与 Subagents 的关系

Skills 和 Subagents 解决的是不同维度的问题：

| 原语 | 解决的问题 | 机制 |
|------|-----------|------|
| **Subagents** | Context 饱和（dumb zone）| 隔离 context，主 Agent 只接收结果 |
| **Skills** | 工具过载（选择负担）| 按需加载，仅在需要时加载完整指令 |

两者可以组合使用：Subagent 可以有自己的 Skills，主 Agent 通过 Skills 调用 Subagent。

---

## 四、Backends：Skills 的存储与分发

### 4.1 三种 Backend

Deep Agents 支持三种 Skill Backend：

| Backend | 适用场景 | 特点 |
|---------|---------|------|
| **FilesystemBackend** | 本地开发 / CI | 从文件系统加载 SKILL.md |
| **StateBackend** | 临时性 skill | Ephemeral，不持久化 |
| **StoreBackend** | 生产环境 | 基于 LangGraph Store，跨会话持久化 |

### 4.2 动态 Skill 注入

```python
from deepagents.middleware.filesystem import FileData

agent = create_deep_agent(
    model="anthropic:claude-sonnet-4-20250514",
    skills=["/skills/"],
)

skill_content = """..."""

result = agent.invoke({
    "messages": [HumanMessage(content="Research the latest Python releases")],
    "files": {
        "/skills/web-research/SKILL.md": FileData(content=skill_content)
    }
})
```

---

## 五、与业界其他方案的对比

### 5.1 SKILL.md vs MCP（Model Context Protocol）

| 维度 | SKILL.md (agentskills.io) | MCP |
|------|---------------------------|-----|
| **设计目标** | 渐进式能力披露（按需加载）| 标准化工具发现与调用 |
| **上下文占用** | 仅加载使用的 skill | 全部工具定义预加载 |
| **适用场景** | 长程任务 + 多工具 | 通用工具集成 |
| **成熟度** | 规范阶段 | 社区广泛采用 |

> 笔者认为，两者并非竞争关系。SKILL.md 解决的是「Agent 如何在大量工具中做出正确选择」，MCP 解决的是「工具如何被标准化发现与调用」。一个完整的生产级 Agent 系统可能同时使用两者。

### 5.2 Subagent vs CrewAI 的 Task Assignment

| 维度 | Deep Agents Subagent | CrewAI Task |
|------|---------------------|-------------|
| **Context 隔离** | ✅ 原生隔离 | ❌ 共享 context |
| **结果粒度** | 仅最终结果 | 可配置（过程/结果）|
| **模型差异** | 支持不同模型 | 统一模型 |
| **适用场景** | 上下文敏感任务 | 流程编排任务 |

---

## 六、工程启示

### 6.1 Context 管理是生产级 Agent 的核心工程问题

LangChain Deep Agents 的设计揭示了一个重要认知：**生产级 Agent 的核心瓶颈不是模型能力，而是 context 管理能力**。当业界还在讨论「哪个模型更好」的时候，真正做生产的团队已经开始关注：

1. 如何避免 context rot
2. 如何在有限 context 中塞入更多信息
3. 如何让 context 的使用效率最大化

### 6.2 渐进式披露是解决工具过载的有效路径

SKILL.md 的渐进式披露模式值得借鉴。与其把所有工具定义一次性塞入 context，不如让 Agent 自己决定「我需要什么工具」然后再加载详细指令。这比 RAG 方式更精确，比直接注入更节省空间。

### 6.3 Subagent + Skill 的组合是 LangChain 的差异化优势

相比其他 Agent 框架，Deep Agents 的**原生双原语设计**（Subagent + Skill）提供了一个连贯的 context 管理方案。其他框架通常只解决其中一个维度，或者通过第三方集成勉强实现类似效果。

---

## 七、结论

LangChain Deep Agents 的 Subagent 和 Skills 机制，本质上是在解决**生产级 Agent 的两大核心工程问题**：

1. **Context rot**：Subagent 通过隔离上下文，防止主 Agent 进入 dumb zone
2. **工具过载**：Skills 通过渐进式披露，让 Agent 按需加载而非全量预加载

这两个原语共同构成了一个完整的 context 工程体系——不是靠更大的 context window，而是靠更聪明 context 使用策略。

> 笔者认为，这个方向代表了一个重要趋势：**2026 年之后，Agent 工程的焦点会从「模型能力」转向「context 管理能力」**。谁能在有限 context 中实现更高效的信息利用，谁就能在生产级 Agent 系统中占据优势。

---

**引用来源**：
- [Building Multi-Agent Applications with Deep Agents - LangChain Blog](https://blog.langchain.dev/building-multi-agent-applications-with-deep-agents)
- [Context Rot Research - Chroma](https://research.trychroma.com/context-rot)
- [HumanLayer "dumb zone" concept](https://www.hlyr.dev/blog/context-efficient-backpressure)
- [agentskills.io 规范](https://agentskills.io/?ref=blog.langchain.com)