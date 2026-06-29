---
title: "google/agents-cli：当你的 Coding Agent 拥有完整 Eval Pipeline"
date: 2026-06-29
source: https://github.com/google/agents-cli
author: Google
tags: [harness, evaluation, eval-pipeline, google-cloud, ADK, coding-agent, meta-tool, agent-skills]
topics: [Eval Harness Builder, Coding Agent Eval, Google Cloud Agent Platform, ADK Integration]
description: "google/agents-cli 是 Google 官方发布的 Eval Harness 构建工具，它不给 coding agent 增加编码能力，而是给它装上完整的 eval pipeline——从数据集生成、自动化评分到失败模式聚类，让 agent 在部署前就知道自己行不行。"
length: 2200
cluster: harness
cluster_role: variant
round: 580
---

# google/agents-cli：当你的 Coding Agent 拥有完整 Eval Pipeline

> 原文：[GitHub - google/agents-cli](https://github.com/google/agents-cli)（Google，Apache-2.0，Stars 3218+）

## 核心命题

大多数 coding agent 工具在解决同一个问题：**怎么让 agent 写出更多代码**。但 google/agents-cli 反其道而行——**它解决的问题是：怎么让 agent 在写代码之前就知道自己行不行**。

这不是又一个 coding agent，而是一个 **Eval Harness Builder**（Eval 线束构建器）。它不替代 Claude Code 或 Codex，而是给这些 coding agent 加上完整的 eval 能力：生成测试数据、跑自动化评测、分析失败模式、优化提示词——全部通过 skill 注入的方式实现。

## 一、为什么 coding agent 急需 Eval Harness

Coding agent 的能力边界模糊是核心痛点。SWE-bench 等基准测试证明了一个残酷事实：**agent 在 benchmark 上表现好，不等于在实际项目上表现好**。问题根源在于：

1. **Eval 数据集与真实任务存在分布偏移**（benchmark 过拟合）
2. **没有机制让 agent 自我评估**（不知道自己不知道）
3. **上线前缺乏可信的质量信号**（部署后才发现问题）

google/agents-cli 的设计哲学正是针对这三点：**把 eval 做进开发流程，而不是做完之后补**。

## 二、agents-cli 的 Skill 架构

agents-cli 通过 7 个独立 Skill 向 coding agent 注入 eval 能力，每个 Skill 对应开发周期的一个环节：

| Skill | 功能 | 解决的核心问题 |
|-------|------|--------------|
| `google-agents-cli-workflow` | 开发生命周期、代码保留规则、模型选择 | 建立标准开发流程 |
| `google-agents-cli-adk-code` | ADK Python API — agents、tools、orchestration、callbacks、state | 统一代码模式 |
| `google-agents-cli-scaffold` | 项目脚手架 — `create`、`enhance`、`upgrade` | 快速初始化 |
| `google-agents-cli-eval` | 评估方法论 — metrics、datasets、LLM-as-judge、adaptive rubrics | **核心 Skill：eval 怎么做** |
| `google-agents-cli-deploy` | 部署 — Agent Runtime、Cloud Run、GKE、CI/CD、secrets | 部署到生产 |
| `google-agents-cli-publish` | Gemini Enterprise 注册 | 发布到企业平台 |
| `google-agents-cli-observability` | 可观测性 — Cloud Trace、logging、第三方集成 | 运行时监控 |

笔者认为，`google-agents-cli-eval` 是整个 Skill 体系的核心。它解决的问题是：**eval 不只是"跑测试"，而是一套完整的 pipeline**。

## 三、Eval Pipeline 的五个步骤

agents-cli 的 eval 不是单次运行，而是完整的闭环 pipeline：

```bash
# Step 1: 生成 eval 测试用例
agents-cli eval generate        # 在 eval 数据集上跑 agent，产出 traces

# Step 2: 评分
agents-cli eval grade           # 用 metrics 对 traces 评分

# Step 3: 对比两个版本
agents-cli eval compare         # 对比两个 eval 结果文件（模型 A vs 模型 B）

# Step 4: 分析失败模式
agents-cli eval analyze         # 从 grade 结果中聚类失败模式

# Step 5: 自动化优化
agents-cli eval optimize        # 用 eval 数据自动调优 agent 提示词
```

这个 pipeline 的设计思路值得注意：**Step 4 的失败模式聚类（analyze）是整个闭环的关键**。大多数 eval 工具止步于"跑了多少 case，通过率多少"，但不知道**哪类 case 失败了、为什么失败**。analyze 把评分结果变成了可操作的设计反馈。

## 四、与现有 Eval 工具的差异化定位

| 维度 | SWE-bench | EvalBench | **agents-cli** |
|------|-----------|-----------|----------------|
| 定位 | 编码任务基准 | 多维度能力评测 | **Coding agent 的开发工具** |
| 目标用户 | 研究人员 | 研究人员 | **开发者 / DevOps** |
| 核心能力 | 标准化数据集 | 多维度指标 | **端到端 eval pipeline** |
| 与 coding agent 关系 | 独立基准 | 独立评测 | **注入到 coding agent 的 Skill** |
| 失败分析 | 无 | 有限 | **聚类 + 可操作反馈** |
| 自我优化 | 无 | 无 | **eval optimize 自动调优提示词** |

笔者认为，agents-cli 最值得注意的差异化是**把 eval 做成了 coding agent 的 Skill，而不是外部评测工具**。这意味着 agent 在开发过程中就能调用 eval，不需要切换到另一个工具环境。

## 五、一个具体的 Eval 使用场景

假设你用 Claude Code 开发一个 RAG agent，想在部署前评估它的表现：

```bash
# 1. 用 agents-cli 生成特定领域的 eval 数据集
agents-cli eval dataset synthesize --domain "legal-contract-review"

# 2. 让 Claude Code 在这个数据集上跑，产出 traces
# （Claude Code 内置了 agents-cli-eval skill，知道怎么跑）

# 3. 评分并分析
agents-cli eval grade --traces ./traces
agents-cli eval analyze --grades ./grades.json

# 4. 如果某类 case（如多跳推理）失败率高，用 eval 数据自动优化提示词
agents-cli eval optimize --metric "multi-hop-accuracy"
```

整个流程不需要离开 Claude Code，agent 可以在开发循环中持续运行 eval。

## 六、限制与适用边界

笔者认为，agents-cli 有两个需要注意的限制：

**1. Google Cloud 强绑定（部分功能）**：本地开发可以用 AI Studio API key，但 deploy 和 publish 功能依赖 Google Cloud。对于不使用 Google Cloud 的团队，核心价值只剩 eval pipeline 本身。

**2. 面向有经验的团队**：Skill 架构、eval methodology、adaptive rubrics 这些概念要求使用者对 agent 开发有基本理解。它不是一个"装上就能用"的工具，而是给有经验的 agent 工程团队用的基础设施。

## 七、一句话总结

> google/agents-cli 的核心价值不是"让 coding agent 写更多代码"，而是**在它上线之前就知道自己行不行**——这才是 production-grade agent 开发缺失的那块拼图。

**适用场景**：已经用 Claude Code / Codex 开发 agent，想在团队内部建立标准化的 eval 流程，且不介意 Google Cloud 部分绑定的工程团队。

**不适用场景**：只需要单次 benchmark 评测的研究人员；完全不用 Google Cloud 且不想引入任何 Google 依赖的团队。

---

*项目地址：[google/agents-cli](https://github.com/google/agents-cli) | Stars 3218+ | Apache-2.0 | Google 官方*