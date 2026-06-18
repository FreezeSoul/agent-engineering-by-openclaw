---
title: Anthropic 多 Agent 决策框架 单 vs 多 2026
cluster: orchestration
date: 2026-01-23
source: https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
author: Anthropic Applied AI
tags: [multi-agent, decision-framework, context-pollution, verification, when-to-use]
---

# Anthropic 多 Agent 决策框架 单 vs 多 2026

> 原文：Building multi-agent systems: When and how to use them — claude.com/blog (Jan 23, 2026)
> 作者：Cara Phillips (Anthropic), with Paul Chen, Andy Schumeister, Brad Abrams, Theo Chu

## 核心命题

**Anthropic 在 2026 年 1 月首次系统披露多 Agent 架构的"决策三场景"**——这是与既有 R407 (`claude-code-subagents-decision-framework-2026`) 不同的**哲学层判定框架**：

- R407 = 战术层："什么时候 spawn 一个 subagent"（命令级决策）
- **本文 = 架构层："什么时候把整个系统改成多 Agent"（系统级决策）**

Anthropic 内部观察到：很多团队花数月搭建多 Agent 架构，最后发现"在单 Agent 上做更好的 prompt 就能达到同样效果"。

## 三场景适用 + 一场景禁用

### ✅ Context protection（上下文污染防护）

**核心机制**：当子任务产出大量 tokens（>1000），但绝大部分对主线无关时，单 Agent 主对话的注意力被稀释。

```python
# Single agent — context pollution
conversation_history = [
    {"role": "user", "content": "My order #12345 isn't working"},
    # Tool result adds 2000+ tokens of order history
    {"role": "assistant", "content": "Now let me diagnose..."},
    # Context now polluted with irrelevant order details
]

# Multi-agent — context isolation
class OrderLookupAgent:
    def lookup_order(self, order_id: str) -> dict:
        # Separate agent with own context
        return extract_summary(...)

class SupportAgent:
    def handle_issue(self, user_message: str):
        order_summary = OrderLookupAgent().lookup_order(order_id)
        # Only 50-100 essential tokens reach main agent
```

**3 个判断条件**：
1. 子任务产出高 context 体积（>1000 tokens）但多数信息对主线无关
2. 子任务定义清晰、有明确提取标准
3. 是 lookup / retrieval 类操作（需要先过滤再使用）

### ✅ Parallelization（并行化）

**核心机制**：当任务需要覆盖大搜索空间时，多个 Agent 并行探索不同 facet 比单 Agent 串行更彻底。

**实战：Anthropic Research feature**

```python
import asyncio
from anthropic import AsyncAnthropic

async def research_topic(query: str) -> dict:
    facets = await lead_agent.decompose_query(query)
    tasks = [research_subagent(facet) for facet in facets]
    results = await asyncio.gather(*tasks)
    return await lead_agent.synthesize(results)
```

**关键洞察**：并行化的主收益是**搜索覆盖度**，**不是速度**——多 Agent 系统总计算量往往是单 Agent 的 3-10 倍，但因为并行分发，wall-clock time 可以更短。

### ✅ Specialization（专业化）

**核心机制**：当单一 Agent 难以在所有领域同时做好时，专门化 Agent 在各自窄领域表现更好。

**典型场景**：代码生成 Agent + 测试 Agent + 文档 Agent 协同（vs 一个全栈 Agent）

### ❌ Always-default 失败模式

**反模式**：很多团队"先默认多 Agent + 多个 subagent for planning / execution / review / iteration"，结果在 handoff 时丢失 context，协调 tokens 比执行 tokens 还多。

**Anthropic 数据**：多 Agent 实现通常消耗单 Agent 3-10x tokens for equivalent tasks。

## 关键决策启发式

### 1. Context-centric decomposition（按 context 分解，非按任务类型）

**错误做法**："前端 Agent + 后端 Agent + 数据库 Agent"（按任务类型分）

**正确做法**："高 context 体积但主线无关的子任务抽出独立 Agent"（按 context 隔离需求分）

### 2. Verification subagent pattern（验证子 Agent）

**机制**：主 Agent 完成后，spawn 一个独立 verification subagent 验证输出。

**适用场景**：
- Generated content meets specifications before delivery
- Factual verification（独立 Agent 验证引用/claim）

**Early Victory Problem（最关键失败模式）**：验证 Agent 跑 1-2 个测试就 declare success，**没有真正 thorough testing**。

**Mitigation**：
1. **Concrete criteria**：明确说 "Run the full test suite and report all failures"，**不**说 "make sure it works"
2. **Comprehensive checks**：要求验证 Agent 测试多种场景和 edge cases
3. **Negative tests**：让验证 Agent 尝试应该失败的输入，确认它确实失败
4. **Explicit instructions**：`You MUST run the complete test suite before marking as passed` —— 没有这句话，verification Agent 会偷懒

### 3. Pre-flight checklist（升级前确认 3 件事）

升级到多 Agent 前必须确认：
1. **存在 genuine constraints**（context 限制、并行化机会、专门化需求）
2. **Decomposition follows context, not problem type**
3. **Clear verification points**（子 Agent 可以在不需完整 context 的情况下验证工作）

否则：**保持最简单能 work 的方案**。

## 与 R407 subagent 决策框架的关系

| 维度 | R407 (`claude-code-subagents-decision-framework-2026`) | 本文 (`when-not`) |
|------|--------------------------------------------------------|-------------------|
| **决策粒度** | 战术级（"何时 spawn 一个 subagent"）| 架构级（"何时把整个系统改成多 Agent"）|
| **决策场景** | 单个 subagent 调用 vs 串行工具调用 | 整个 multi-agent 架构 vs single-agent |
| **触发问题** | "这个任务是否需要隔离 context？" | "我们的系统是否真的需要多 Agent？" |
| **决策方向** | 鼓励多 spawn（解释 subagent 何时更好）| 警告 over-engineering（解释何时**不需要**多 Agent）|
| **覆盖 prompt** | 200+ 行 tools、code patterns | 决策启发式、3 场景 + 1 反模式 |
| **Anthropic 一手源** | claude.com/blog/subagents-in-claude-code | claude.com/blog/building-multi-agent-systems |

两者**互补**：R407 解释"subagent 工具怎么用"，本文解释"subagent 架构要不要建"。

## 与 Anthropic 既有多 Agent 文章的差异

Anthropic 在过去一年写过多个 multi-agent 相关一手源：

- `How we built our multi-agent research system` (2024)：Research 系统架构深度解析
- `anthropic-multi-agent-research-system-architecture-2026` (R389)：研究系统 orchestrator-worker 模式
- `anthropic-c-compiler-parallel-claudes-lock-based-coordination-2026`：C compiler 多 Agent 协调
- `anthropic-multi-agent-harness-engineering-lessons-from-2000-sessions-2026`：2000 session 经验

**本文的独特贡献**：
1. **首次明确"何时不用多 Agent"** —— 之前所有文章都假设多 Agent 已成立，本文直接挑战这个假设
2. **3 场景 + 1 反模式量化**：3 scenarios where multi-agent excels + 1 always-default anti-pattern
3. **3-10x token overhead 量化数据**：Anthropic 第一次给出明确的 token 开销范围
4. **Verification subagent 早期胜利问题**：识别 verification subagent 的具体失败模式 + mitigation 清单

## 实战决策流程

```
[新项目/重构触发]
       │
       ▼
[Context 体积评估]──→ 单任务 < 1000 tokens? ──Yes──→ 用单 Agent
       │                                            + 改进 prompt
       │ No
       ▼
[并行机会评估]──→ 需要覆盖大搜索空间? ──Yes──→ 多 Agent (parallel)
       │                                       + 接受 3-10x tokens
       │ No
       ▼
[专门化需求]──→ 单一 Agent 难以全栈? ──Yes──→ 多 Agent (specialized)
       │                                         + 严格 verification
       │ No
       ▼
[用单 Agent] + 监控 context 增长
       │
       ▼ (3-6 个月后)
[如果单 Agent context 持续超阈值 → 重评估升级]
```

## 相关引用

- **R407 战术层决策**：`articles/orchestration/claude-code-subagents-decision-framework-2026.md`
- **R389 研究系统架构**：`articles/orchestration/anthropic-multi-agent-research-system-orchestrator-worker-pattern-2026.md`
- **Anthropic Engineering**：`anthropic.com/engineering` 多篇 multi-agent 经验文
- **R337 Scheduled Deployments**：cron + Agent 协调的另一维度（基础设施层）

## 关键 takeaway

**"Multi-agent 不是默认，是需要 justified 的升级路径"**

Anthropic 在 2026 年初明确传递这一信号：multi-agent 的协调成本（3-10x tokens + handoff context loss + 验证失败）通常超过其收益，除非满足 3 个 specific scenarios（context pollution / parallelization / specialization）。

**对工程师的实际意义**：在搭建多 Agent 系统前，先用单 Agent + 改进 prompt 验证基线。如果单 Agent 能达到 equivalent results，**不要**升级到多 Agent。