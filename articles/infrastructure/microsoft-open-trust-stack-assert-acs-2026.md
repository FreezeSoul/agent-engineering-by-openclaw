# Microsoft Open Trust Stack — 构建 Agent 信任的评估-控制闭环

## Metadata

| Field | Value |
|-------|-------|
| **URL** | devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents |
| **Author** | Sarah Bird (CPO, Responsible AI, Microsoft) |
| **Date** | 2026-06-02（Build 2026） |
| **Round** | 329 |
| **Type** | article |
| **Theme** | evaluation-runtime-control-loop |
| **Category** | Infrastructure |

## 一句话评价

Microsoft 在 Build 2026 发布 Open Trust Stack，用 ASSERT（评估）+ ACS（运行时控制标准）构成「政策→评估→执行→验证」的完整闭环，让 Agent 信任从口号变成工程实践。

---

## 核心内容

### 问题：为什么需要 Open Trust Stack

当前 Agent 评估和控制的困境：
- **评估层**：通用基准与实际 policy 脱节；Agent drift（偏离规范）在生产环境才暴露
- **控制层**：每家厂商各自实现 guardrails，互不兼容；控制逻辑与评估结果无法联动
- **根本问题**：评估（policy 检查）和控制（runtime干预）是两个割裂的系统

### Open Trust Stack 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Open Trust Stack                          │
│ ┌──────────────┐    ┌───────────────────┐                │
│  │   ASSERT │───▶│   ACS (Runtime)    │                │
│  │  (Evaluation) │    │  (Control Spec)   │                │
│  └──────────────┘    └───────────────────┘                │
│         │                      ▲ │
│         │ │                            │
│         ▼                      │                            │
│  ┌──────────────┐    ┌───────────────────┐                │
│  │   Re-run    │◀───│   Policy Update │                │
│  │  ASSERT │    │   from Results    │                │
│  └──────────────┘└───────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

**闭环流程**：
1. **Run ASSERT** — 识别 Agent 在哪些 policy 要求上失败
2. **Apply ACS controls** — 在正确的检查点放置正确的控制
3. **Re-run ASSERT** — 确认改进效果
4. **Iterate** — 评估结果反馈到 policy 更新

### ASSERT详解

> Adaptive Spec-driven Scoring for Evaluation and Regression Testing

**核心价值**：将自然语言行为规范直接转换为可执行评估。

**4阶段管线**：
1. **Spec → Taxonomy**：NL spec → 显式概念规范 → 细粒度行为分类体系（允许/禁止行为）
2. **Test Generation**：基于 taxonomy 生成分层测试用例（单轮+多轮）
3. **Execution**：在被测系统上运行，记录完整 trace（含工具调用）
4. **Scoring**：LLM Judge 按 policy立场评分，产出标签+理由+失败模式

**关键特点**：
- Framework-agnostic（可对接任何 target）
- Local-first（默认不外发数据）
- Trace-aware（基于完整执行 trace 而非单次输出）
- 失败可追溯到具体 policy 条款

### ACS 详解

> Agent Control Specification — 运行时安全控制的开放标准

**核心定位**：stateless、deterministic、fail-closed 的运行时 policy 决策引擎。

**5个检查点（Intervention Points）**：

| 检查点 | 时机 |
|--------|------|
| `input` | Agent 收到输入时 |
| `llm_call` | LLM 调用前 |
| `state` | 状态更新时 |
| `tool_execution` | 工具执行时 |
| `output` | 最终输出前 |

**设计原则**：
- **Portable**：控制逻辑随 Agent 移动，不绑定特定基础设施或厂商
- **Stateless + Deterministic**：每个检查点只做「给定 snapshot + policy manifest → verdict」的纯函数
- **Fail-closed**：默认拒绝，安全性优先

**ACS 是 AGT 5.0 的 policy 层**：
- 已集成到 `microsoft/agent-governance-toolkit`（AGT）
- SDK 支持：Python、Node.js、.NET、Rust
- PyPI 包名：`agent-control-specification`

###评估 → 控制 → 验证的闭环意义

```
Policy → ASSERT（识别失败点）→ ACS（放置控制）→ 重新评估 → Policy 更新
```

这个闭环让 Agent 信任不再是静态配置，而是**可量化、可验证、可持续迭代**的工程过程。

### 与其他方案的关系

**OpenInference 作为共享 telemetry 层**：
- ASSERT 的每个评估结果
- ACS 的每个控制决策
- Phoenix / Arize AX 的每条生产 trace

都使用**相同的语言**（OpenInference 标准），形成统一的观测性层。

---

## 工程意义

### 在 Agent 工程栈中的位置

| 层级 | 代表方案 | 关注点 |
|------|---------|--------|
| **规范层** | ASSERT | Policy → 可执行评估 |
| **架构层** | Claude Zero Trust 三阶层 | 分层安全架构设计 |
| **验证层** | AgentReady (OWASP) | 基准测试 |
| **控制层** | ACS | 运行时安全控制 |
| **观测层** | OpenInference | 统一 trace 标准 |

### 三层闭环的完整性

- **R328 Article** (Claude Zero Trust) — 架构设计层（三阶层成熟度模型）
- **R328 Project** (AgentReady) — 基准验证层（OWASP Top 10）
- **R329 Article** (Open Trust Stack) —评估-控制闭环（ASSERT + ACS）

三者形成：**架构设计 → 基准验证 → 评估-控制闭环** 的完整安全工程链条。

---

## 原文引用

1. "ASSERT and ACS are designed to work together: Run ASSERT to identify where your agent is failing policy requirements. Use ACS to place the right controls at the right checkpoints to address those failures. Re-run ASSERT to confirm improvement." — Sarah Bird, Microsoft Foundry Blog
2. "ACS is a portable standard for runtime controls. ACS is an open spec for placing deterministic safety controls at five checkpoints in the agent loop: input, LLM call, state, tool execution, and output." — Arize AI Blog
3. "This is a closed loop from evaluation to enforcement, and ACS gives developers a portable control layer that travels with the agent, not locked to any infrastructure or dependent on any single vendor." — Microsoft Foundry Blog

---

## 来源

- Microsoft Foundry Blog: https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents
- ASSERT GitHub: https://github.com/responsibleai/ASSERT
- ACS Spec: https://microsoft.github.io/agent-governance-toolkit/packages/agent-control-specification
- TechCrunch: https://techcrunch.com/2026/06/02/microsoft-offers-devs-a-better-way-to-control-ai-agent-behavior
- Command Line Blog: https://commandline.microsoft.com/assert-written-intent-executable-evals