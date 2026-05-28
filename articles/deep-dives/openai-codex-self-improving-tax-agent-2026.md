# OpenAI Codex 驱动自改进 Agent：生产反馈闭环的工程范式

> **核心论点**：OpenAI 与 Thrive Holdings 合作的 Tax AI 项目证明了一个关键工程范式——当 Agent 系统能够将生产环境中的 practitioner 纠错自动转化为结构化评估（eval），再驱动 Codex 执行改进循环时，Agent 不再是被动执行工具，而是能够自主进化的生产系统。这个进化的驱动力不是模型参数更新，而是**生产证据 → 评估目标 → Codex 工程任务**这套自动化闭环。

## 背景：手动反馈循环的根本困境

现实生产系统暴露的问题往往超出实验室预期。传统模式下，团队在发布后才发现 Agent 的失败案例，然后花费数周检查边缘情况、调整 prompt、将生产反馈转化为产品改进。反馈循环依赖工程师手动推进，改进速度受限于人力投入。

Tax AI 项目针对希腊克里特岛 30+ 会计师事务所的复杂税务申报场景——单个中等复杂度申报仅数据录入就需 8 小时。在 2026 报税季中，Tax AI 处理了 7,000 份税表，覆盖 1040 和 1041 表格。更值得关注的是，**系统本身在三个月内可测量地优于最初部署版本**。

## 可测量的自我改进轨迹

OpenAI 的衡量标准是「无需后续修正即可正确完成的税务申报比例」：

- **75% 正确率**：上线时仅 25% 的申报达到此标准，六周内提升至 86%
- **90% / 100% 正确率**：提升速度更快
- **任务复杂度迁移**：从简单的 W-2、1099 逐步扩展到 K-1、Schedule 等复杂场景

笔者认为，**这个指标设计本身就是核心工程贡献**——它将 practitioner 的「后续修正成本」量化为 Agent 能力的代理指标，而不是用实验室 benchmark 衡量生产系统。

## 三支柱闭环架构

```
┌─────────────────────────────────────────────────────────┐
│                 Practitioner 反馈层                      │
│    practitioners.shape(the.product)                      │
│   practitioners upload source files + client notes      │
└──────────────────────┬──────────────────────────────────┘
                       │ correction evidence
                       ▼
┌─────────────────────────────────────────────────────────┐
│               Production Evidence 层                    │
│   full trace: source → extracted fields → provenance     │
│            → submission → expert correction             │
└──────────────────────┬──────────────────────────────────┘
                       │ structured findings
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Codex-Driven 改进循环                       │
│   findings → tailored evals → scoped engineering tasks  │
│   Codex investigates → proposes → validates → ships      │
└─────────────────────────────────────────────────────────┘
```

### 支柱一：贴近 practitioner

> "The people doing the work need to steer what the product learns. Their intuition and understanding reveal which errors matter."

税务从业者的纠错不是噪声，而是产品学习的信号。系统设计必须让 practitioner 的修正行为本身产生可操作的工程数据。

### 支柱二：生产即证据

产品不仅记录输入输出，还要记录从源文件、提取字段、来源追踪、下游提交到专家修正的完整路径。这是后续分析「哪个环节出了问题」的数据基础。

### 支柱三：Codex 驱动的评估循环

一旦生产问题被结构化呈现，它们转化为 findings → tailored evals → scoped engineering tasks，Codex 在每个环节中协助调查、提出变更、针对定向评估和回归评估验证，并将产品向前推进。

## 案例：租赁物业 Schedule E 提取

```python
# 简化示例：生产纠错如何转化为改进循环

# 1. Practitioner 纠错揭示失败
practitioner_correction = {
    "agent_predicted": "$12,400",
    "actual_value": "$9,800",
    "form": "Schedule E",
    "error_type": "extraction_miss"  # vs mapping_problem / missing_support / workflow_noise
}

# 2. 生产证据记录
production_trace = {
    "source_package": ["rental_notes.pdf", "bank_statement.xlsx"],
    "extracted_fields": {"rental_income": "$12,400", "expenses": "$2,100"},
    "field_provenance": "rental_notes.pdf → line 18 → manual extraction",
    "downstream_submission": "Schedule E → Part I → Line 3"
}

# 3. Structured finding
finding = {
    "error_type": "extraction_miss",
    "source_file_pattern": "rental_notes.pdf with handwritten annotations",
    "affected_field": "rental_income",
    "practitioner_significance": "high",  # 从业者认为这个错误很关键
    "eval_target": "schedule_e_rental_income_extraction"
}
```

## 关键工程洞察

### 1. 纠错的分类比纠错本身更重要

系统设计必须区分四类「修正后值与预测值不同」的情况：

- **真实提取失误**（extraction miss）
- **映射问题**（mapping problem）
- **产品本身不支持的场景**（missing product support）
- **预期的工作流噪声**（expected workflow noise）

只有区分清楚，才能将「需要产品改进」的信号从「预期行为」中分离出来。

### 2. 评估基础设施即产品核心

笔者认为，**Tax AI 项目最重要的工程贡献不是 Agent 本身，而是一套将生产行为转化为评估目标的流水线**。这套流水线让「产品改进」不再依赖工程师手动分析和优先级排序。

### 3. Agent 自我改进的边界

系统改进的是**产品能力**，而不是 Agent 的通用推理能力。Codex 在闭环中扮演的是「辅助工程师」角色——调查问题、提出修改建议、验证改动。真正判断「改什么」的是 practitioner 反馈和评估数据。

## 与传统 Harness 的区别

传统 Agent harness 关注的是**如何在单次执行中控制 Agent 行为**（权限、安全、停止条件）。而 Tax AI 展示的闭环是一种**跨执行会话的 harness**——它管理的不是单次任务，而是产品能力的演化轨迹。

笔者认为，这种「生产驱动、Codex 执行、评估验证」的三层架构，代表了一种新的 Agent 工程方向：**Agent 不只是工具，而是工具的改进者**。

---

**原文引用**

> "Real-world systems behave differently in production than they do in a lab, breaking in ways that are hard to anticipate before deployment."
>
> "Instead of relying on engineers to find and fix each failure, Tax AI uses Codex to turn production use into structured signals that fuel autonomous improvement."
>
> "The system showed even faster growth at the 90% and 100% correct field completion levels."
>
> — [Building self-improving tax agents with Codex](https://openai.com/index/building-self-improving-tax-agents-with-codex/), OpenAI Engineering, May 27, 2026

**关联项目**

- [mastra-ai/mastra](https://github.com/mastra-ai/mastra)（TypeScript Agent 框架，支持 human-in-the-loop workflow，24,419 Stars）

**标签**：#self-improving-agent #codex #production-harness #eval-loop #agent-engineering