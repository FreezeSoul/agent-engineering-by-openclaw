# Harbor Framework Terminal-Bench：真实终端环境下的 Agent 评测标准

> Harbor Framework 的 Terminal-Bench 是当前最具实操价值的 coding agent 评测工具之一。它不测试「能不能回答问题」，而测试「能不能在真实终端里搞定真实任务」。

---

## 核心命题

coding agent 的评测有一个根本问题：**我们测的是什么？** 

大多数 benchmark（HumanEval、MATH 等）测的是「能不能给出正确答案」——这是静态评测。但真实的 coding agent 工作在动态环境里：它要编辑文件、运行测试、安装依赖、调试错误。这些行为没法用静态题目测。

Terminal-Bench 的核心贡献是：**把 benchmark 从「答题」变成「干活」**。

> 「Terminal-Bench evaluates whether agents can perform the kind of high-skill work that professionals are paid to do, including configuring legacy systems, reimplementing research papers, and solving general software engineering problems.」—— Terminal-Bench Paper

---

## 为什么这重要

### 评测的边界问题

Anthropic 近期一篇关于 infrastructure noise 的文章（`anthropic-infrastructure-noise-benchmark-validity-2026.md`）揭示了一个关键发现：

> 「基础设施配置本身就能让 agentic coding benchmark 产生几个百分点的波动——有时甚至超过 leaderboard 榜首之间的差距。」

这个发现说明：benchmark 的结果不只是模型能力的体现，也是评测环境配置的函数。Terminal-Bench 通过其 Harbor harness 设计，明确承认并处理了这个根本问题。

### 真实任务的评测复杂度

从 Terminal-Bench 论文中可以看到它定义的评测任务类型：
- 配置遗留系统
- 重新实现研究论文
- 解决通用软件工程问题
- 编译代码、训练模型、配置服务器

每一类任务都需要 Agent 在真实的 terminal shell 里与环境交互，完成多步骤的探索和操作。

---

## 技术架构

### 两层设计：Dataset + Harness

Terminal-Bench 由两部分组成：

1. **Dataset**：89 个手工验证的真实任务，每个任务包含：
   - Containerized environment（初始化好的容器环境）
   - Instruction（描述要完成的任务）
   - Tests（验证完成与否的测试套件）
   - Reference solution（手工写的参考答案）

2. **Harbor Harness**：连接 LLM 与 terminal sandbox 的执行框架，支持：
   - Claude Code
   - Codex CLI
   - OpenHands
   - Mini-SWE-Agent
   - Terminus 2（他们自己开发的 neutral 测试床）

> 「Tasks are specified using the Harbor task format and are run using the Harbor harness」—— Terminal-Bench Paper

### Harbor 框架

Harbor 是他们发布的用于大规模构建和运行 agent 评测的框架。Terminal-Bench 任务以 Harbor task format 实现，通过 `harbor run -d terminal-bench@2.0` 即可运行。

这意味着 Harbor 不仅仅服务于 Terminal-Bench 这一个 benchmark——它是一个通用的 agent eval 基础设施，可以通过相同的接口运行其他任务集。

---

## 评测数据揭示的模型差异

从 Terminal-Bench 2.0 的评测结果表格中可以看到关键数据：

| 模型 | Agent | 解决率 | Input Tokens | Output Tokens |
|------|-------|--------|-------------|--------------|
| GPT-5.2 | Codex CLI | 62.9% | 137.5M | 2.3M |
| Claude Opus 4.5 | Terminus 2 | 57.8% | 3.9M | 1.3M |
| Claude Opus 4.5 | Claude Code | 52.1% | 256.9M | 0.8M |

几个值得注意的观察：

1. **Agent 选择影响巨大**：同一个模型（Claude Opus 4.5）配 Terminus 2 是 57.8%，配 Claude Code 是 52.1%——差了将近 6 个点
2. **Claude Code 的 token 消耗异常高**：256.9M input tokens 是 Terminus 2 的 65 倍，说明它在环境探索上消耗了大量 context
3. **Top 模型在 65% 以下**：连最好的组合（GPT-5.2 + Codex CLI）也只有 62.9%，说明这个 benchmark 的难度是真实的前沿水准

---

## 与本仓库的关联

### Agent Harness 工程

Terminal-Bench 是 Agent Harness 工程的典型案例：
- Containerized environment 是 harness 的基础设施层
- Task specification format 是 harness 的任务定义层
- Harbor harness 连接 LLM 与 sandbox，是 harness 的执行层

本仓库在 `articles/harness/` 下已有 Anthropic 的 harness 设计文章，以及 Stanford Meta-Harness 的自动化优化研究。Terminal-Bench 提供了另一个视角：**如何设计 benchmark harness 本身**。

### coding agent 评测生态

本仓库的 `practices/ai-coding/` 目录下有 Cursor Composer 2.5 的训练方法论文章。Terminal-Bench 正是这类更聪明 coding agent 的评测验证层——你训练出来的能力需要通过这类 benchmark 验证是否真实。

> 「The benchmark gives you a reproducible task suite and execution harness designed for practical, real-world evaluation.」—— Harbor Framework README

---

## 引用

- [Terminal-Bench Paper (arXiv 2601.11868)](https://arxiv.org/html/2601.11868v1)
- [Harbor Framework GitHub](https://github.com/harbor-framework/terminal-bench)
- [Terminal-Bench Leaderboard (tbench.ai)](https://www.tbench.ai)