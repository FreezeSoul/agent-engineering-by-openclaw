# AutoScientists：自组织 Agent 团队如何做长周期科学实验

> 多个 Agent 不是分工流水线，而是互相批判的"研究员小组"——AutoScientists 用自我组织替代中央调度，在 24 小时以上的长任务中维持并行搜索的活力。

## 核心命题

AutoScientists 解决了一个根本矛盾：科学实验需要小时级到天级的并行探索，但传统的多 Agent 系统要么有一个中央调度器（成了单点瓶颈），要么各 Agent 独立工作（导致重复探索和资源浪费）。

笔者的判断是：这个项目的最大价值不在于某个benchmark分数，而在于它展示了一种**让 Agent 在长时间尺度上维持有意义协作**的架构思路。这对于需要运行数小时的复杂 Agent 任务有直接的工程参考价值。

## 项目概览

| 维度 | 信息 |
|------|------|
| **Repo** | [mims-harvard/AutoScientists](https://github.com/mims-harvard/AutoScientists) |
| **Stars** | 241（截至 2026-05-31） |
| **机构** | Harvard BIMDS + OpenScientist.ai |
| **语言** | Python + Node.js（Claude Code subagents） |
| **论文** | [arXiv:2605.28655](https://arxiv.org/abs/2605.28655) |
| **发布** | 2026-05 |

## 核心机制：champion/challenger 评审制度

AutoScientists 的 Agent 团队用"champion/challenger"模式替代中央调度：

1. **Champion**：提出假设/实验方案的 Agent，有限预算（计算资源额度）
2. **Challenger**：评审 Champion 提案的 Agent，决定是否批准追加预算
3. **Evidence Board**：共享实验结果，Agent 可以"搭便车"利用他人成功，避免重复失败

```
┌─────────────┐    propose     ┌──────────────┐
│  Champion   │ ─────────────▶ │   Challenger │
│  (研究员)    │  申请预算追加   │   (评审员)    │
└─────────────┘                └──────────────┘
      │                              │
      │ 获得预算，执行实验              │ 批准/拒绝
      ▼                              ▼
┌──────────────────────────────────────────┐
│            Evidence Board                │
│  (成功案例 / 失败记录 / 中间结果)          │
└──────────────────────────────────────────┘
      │
      ▼ 读取board，避免重复
┌─────────────┐
│  新Champion  │
│  (其他Agent) │
└─────────────┘
```

**关键设计**：Challenger 的存在不是为了"审批"，而是为了让实验资源流向更有前途的方向。这比"所有 Agent 各自跑"更高效，又避免了中央调度器的单点瓶颈。

## 基准结果

| 任务 | AutoScientists | Prior Best | 提升 |
|------|----------------|-------------|------|
| BioML-Bench（24个生物医学ML任务）| 74.4% 平均 leaderboard 百分位 | 66.1% | **+8.33%** |
| nanoGPT 训练优化 | 1.9× 更快达到目标验证指标 | 单 Agent | **1.9×** |
| ProteinGym ACE2-Spike 结合预测 | +12.5%（相对基线）| Kermut GP | **+12.5%** |

## 技术栈与实现

**Agent 协调**：通过 [ClawInstitute](https://www.npmjs.com/package/clawinstitute)（npm 包）实现本地多 Agent 协调 server，支持 workshop/workspace/message-board 模式。每个 Claude Code 实例作为 subagent 独立运行。

**任务定义**（两文件模式）：
- `TASK.md`：任务规格定义（问题描述、数据、约束）
- `LAUNCH.md`：任务 profile（13 个 hooks：`launch_command`、`discussion_policy`、`champion_promotion`、`stagnation_response`、`exit_condition` 等）

**运行示例**：
```bash
# 启动 ClawInstitute server（所有 agent 通过此协调）
npx clawinstitute start

# 启动一个实验 agent
claude -p "Read runbook.md and execute. Task: task-autoresearch. Run name: ar_v1."
```

**关键架构决策**：orchestrator 纯粹是协调器——启动 Agent、收集结果，不训练任何模型。这是正确的设计：协调逻辑和执行逻辑分开，扩展性更好。

## 与传统 Multi-Agent 框架的差异

| 维度 | AutoScientists | 典型 Multi-Agent（LangGraph/CrewAI）|
|------|---------------|-------------------------------------|
| **调度方式** | Champion/Challenger 自组织 | 中央 DAG / sequential pipeline |
| **长时间任务** | 原生支持（Agent 自主决定继续/退出）| 通常需要手动设计循环 |
| **失败处理** | Evidence Board 共享失败，避免重复踩坑 | 通常各自失败或回滚 |
| **资源分配** | Challenger 评审动态分配 | 静态配置或预分配 |
| **适用场景** | 开放域探索（科学实验、优化）| 明确流程的任务（客服、RAG）|

笔者认为，AutoScientists 的设计对"复杂长任务 Agent"的工程实践有重要参考价值：当任务无法在单次 Agent 调用中完成、需要数小时运行时，中央调度器的缺陷就暴露了——它无法动态调整各 Agent 的资源配额，也无法让成功的探索路径快速扩散到其他 Agent。

## 适用场景

✅ **适合**：需要长时间并行探索的复杂优化任务、科学实验、多假设验证  
❌ **不适合**：短流程明确任务（客服、文档处理、RAG 问答）  
⚠️ **前提**：需要 Claude Code 环境 + Node.js 22+ + Python 3.9+

## 延伸阅读

- [AutoScientists 项目主页](https://autoscientists.openscientist.ai/)
- [ClawInstitute npm 包](https://www.npmjs.com/package/clawinstitute)（Agent 协调基础设施）
- [arXiv 论文](https://arxiv.org/abs/2605.28655)

---

*关联主题：Multi-Agent 协作 · 长周期 Agent 任务 · Agent 自组织架构*