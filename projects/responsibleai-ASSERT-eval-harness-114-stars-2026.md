# responsibleai/ASSERT — NL Spec → Executable Eval Pipeline

## Metadata

| Field | Value |
|-------|-------|
| **Repo** | github.com/responsibleai/ASSERT |
| **Stars** | 114 |
| **License** | MIT |
| **Language** | Python 3.11 / 3.12 / 3.13 |
| **Org** | Microsoft Research — Responsible AI |
| **Date** | 2026-06-02 |
| **Round** | 329 |
| **Type** | project |
| **Theme** | evaluation-pipeline |

## 一句话评价

将自然语言行为规范直接转换为可执行评估管线的开源框架，填补「规范意图」到「评估执行」之间的工程鸿沟。

---

## 核心能力

### 问题背景

大多数 AI 系统在设计之初都有明确的规范：产品需求、政策文档、系统提示词、发布检查清单。但这些文字描述很难直接转化为可运行的评估套件——通用评分器、预定义基准或人工测试用例都会与原始意图产生漂移。

### ASSERT 解决路径

```
自然语言规范
    ↓
行为分类体系（Taxonomy）
    ↓
分层测试用例生成
    ↓
被测系统执行（全链路 trace）
    ↓
LLM Judge 评分（policy-aligned）
    ↓
标签 +理由 + 失败模式 → 可检视可迭代
```

### 四阶段详解

**Stage 1 — 规范系统化**
将宽泛的行为规范转化为显式的概念规范，再转换为细粒度、可编辑的行为分类体系（taxonomy），附带建议的允许/禁止行为。

**Stage 2 — 测试用例生成**
在开发者声明的维度上生成分层测试用例，覆盖单轮和多轮场景。

**Stage 3 — 执行与 Trace**
在被测系统上运行测试用例，记录完整 trace（包含工具调用和中间决策）。

**Stage 4 — LLM 评分**
使用 LLM Judge 对每条 trace 按行为分类体系和对应策略立场进行评分，产出标签、理由和失败模式，供开发者检视和迭代。

### 关键设计原则

- **Local-first**：不强制外发数据，默认不收集遥测
- **Framework-agnostic**：可对接任何目标（托管模型、可调用封装器、OTel-traced agents）
- **Trace-aware**：评估基于完整执行 trace，不只是单次输出
- **Policy-aligned**：评分与policy立场直接挂钩，失败可追溯到具体规范条款

### 快速启用

```python
from assert_ai import auto_trace
auto_trace.enable()
```

CLI 参考文档和示例均已提供。

---

## 工程意义

### 与同类方案的维度差异

| 维度 | 传统 Benchmark | LangSmith / Phoenix | ASSERT |
|------|--------------|---------------------|--------|
| **起点** | 预定义指标 | 已有 trace 回溯 | NL规范驱动 |
| **覆盖** | 单轮任务 | 多轮 trace | 单轮 + 多轮 |
| **评分依据** | 固定指标 | 人工定义 | Policy立场 |
| **可追溯性** | 无 | 部分 | 失败 →规范条款 |

### 在 Agent 工程中的定位

ASSERT处于 **evaluation 层**，是 Agent 生命周期的「验证」环节。它的核心价值在于：
- 不再需要手工编写评估用例 → 从 NL spec 自动生成
- 不再只有模糊的通过/失败 → 失败模式可直接映射到 policy 条款
- 支持 OTel trace集成 → 可对接现有可观测性基础设施

### 与 R328 的关联

R328 Article（Claude Zero Trust 三阶层）提供「架构设计层」的安全规范，R328 Project（AgentReady）提供「基准验证层」的 OWASP Top 10 测试。ASSERT 则处于「规范层」——将安全/行为规范直接转化为可执行评估，三者形成 **规范 → 架构 → 验证** 的完整闭环。

---

## 数据

- Stars: 114（2026-06-11）
- Language: Python
- License: MIT
- Python: 3.11 / 3.12 / 3.13
- 发布日期: 2026-06-02（Build 2026）

---

## 原文引用

1. "Most AI systems start with a specification: product requirements, policies, system prompts, or launch criteria describing what the system should and should not do. The more difficult step is turning that intention into an eval suite that's specific enough to run, inspect, and update as the system changes." — Microsoft Command Line Blog
2. "From the natural language specification, the ASSERT pipeline derives behavior categories, generates single-turn and multi-turn test cases, inferences them against your target, and uses an LLM judge to score each conversation against your policies." — GitHub README

---

## 来源

- GitHub: https://github.com/responsibleai/ASSERT
- Blog: https://commandline.microsoft.com/assert-written-intent-executable-evals
- Foundry: https://devblogs.microsoft.com/foundry/build-2026-open-trust-stack-ai-agents