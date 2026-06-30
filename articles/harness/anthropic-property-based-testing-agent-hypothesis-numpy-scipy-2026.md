---
title: "Anthropic Agent Property-Based Testing 56% NumPy SciPy Bugs"
date: 2026-06-30
cluster: harness
source: https://www.anthropic.com/research/property-based-testing
license: Anthropic 1st-party research
authors: Muhammad Maaz, Liam DeVoe, Zac Hatfield-Dodds, Nicholas Carlini
paper: https://arxiv.org/abs/2510.09907
code: https://github.com/mmaaz-git/agentic-pbt
tags: [property-based-testing, hypothesis, harness-engineering, agent-evaluation, anthropic-research]
---

# Anthropic Agent Property-Based Testing: 56% NumPy SciPy Bugs Found via Claude Code

> **核心结论**：Anthropic 2026-06-17 发布 agent-driven property-based testing research，把 property-based testing (PBT) 从「开发者手写 Hypothesis 策略」转化为「Claude Code agent 自动挖 bug」的工作流。Opus 4.1 在 100+ PyPI 包上跑出 984 个 bug 报告，**56% 验证为 valid bug，32% 达到 maintainer 报告阈值**。**最重要的工程贡献不是 bug 数字，而是 agent harness 的 4 步自反思循环 + rubric 排序 + 多 reviewer 验证三件套**——这是「agent 作为 bug hunter」这一新角色的首批可复用模板。

## 一、问题域：Example-based testing 的天花板

Example-based unit test 是软件工程的主流范式：

```python
# example-based test
def test_sort():
    assert my_sort([1,3,2]) == [1,2,3]
    assert my_sort([1,0,-5]) == [-5,0,1]
```

开发者写出具体的输入与预期输出。但问题在于：**如果开发者没想起某个 edge case，他也不会测它**。要穷举所有 edge case 是不现实的。

Property-based testing (PBT) 是 30+ 年的老技术（Hypothesis、QuickCheck、fast-check），但需要**开发者**手写 invariant + input strategy。Anthropic 的核心问题是：**能否让 agent 接管「写 PBT」这个脑力活？**

## 二、Agent Harness：4 步自反思工作流

`mmaaz-git/agentic-pbt` 把这个想法落成一个 Claude Code custom command（`.claude/commands/hypo.md`）：

```bash
# 安装：把 hypo.md 放到 ~/.claude/commands/ 或项目本地
# 运行：claude "/hypo numpy" 或 claude "/hypo statistics.median" --model opus
```

**Agent 工作流的 4 步循环**：

1. **理解目标** — 读代码、拉文档、探索与 codebase 其余部分的关系
2. **提出 properties** — 基于 type annotations、docstrings、function names、comments 推断「应该为真的不变量」
3. **写 Hypothesis tests** — 把 properties 编译成可执行测试
4. **运行 + 自反思** — 失败时区分「真 bug」vs「test 写错」；成功时区分「测试有信号」vs「测试 trivial」

第 4 步的 self-reflection 是工程关键：论文给了一个反例——agent 写的 test 第一次 pass，但反思时意识到自己把整个 test 包在 try-catch 里（吞掉了异常）。去掉 try-catch 后 test 失败，找到真 bug。**这种「检测自己写测试时埋的雷」的能力，是 Sonnet 4.5 / Opus 4.1 相比 Sonnet 4 的显著提升点。**

## 三、评估结果：984 bug 报告 → 56% valid → 32% reportable

论文评估分两阶段：

### Phase 1: Opus 4.1 横扫 100+ PyPI 包
- **984 个 bug 报告**生成
- 人工抽 50 个 review：**56% valid, 32% reportable**
- 训练 Opus 4.1 一个 15 分 rubric（基于抽样的 valid rate）做排序
- **Top-scored bug reports: 86% valid, 81% reportable** ← rubric 排序大幅提升 precision

### Phase 2: Sonnet 4.5 重点 10 包
- 多次重复运行 + Sonnet 4.5 评估 agent 做 correctness/severity 检查
- 3 个 expert human reviewer 评估 high-severity bug

**Maintainer 反馈**：论文精选 5 个有趣的 bug + 提议 patch 报到 GitHub，maintainer 已 accept 修复（numpy#29609 等 PR 已 merged）。

## 四、关键工程发现：harness 设计的 4 个反直觉点

1. **多步推理需要 to-do list** — PBT 是长程任务（读代码 → 提 properties → 写 tests → 反思），agent 必须显式维护 todo 跟踪进度。论文的 agent 用 Claude Code 内置 to-do 机制。
2. **self-reflection 显著降 false positive** — 论文把「写完 test 不反思」和「写完 test 反思」对比，反思版 false positive 率显著下降。
3. **Opus 4.1 ≠ Sonnet 4.5 在反思能力上** — 论文明确写：「We also observed a notable improvement in self-reflection with Opus 4.1 and Sonnet 4.5, compared to Sonnet 4」——**更强的模型才有更可靠的反思**，这给 agent harness 设计一个 hard constraint。
4. **rubric 排序 > 原始概率** — 984 个 bug 报告里 56% valid 是「随机抽」的数字；用 rubric 排序后 top 86% valid。这是「**用模型给模型输出打分**」的经典方法论。

## 五、与现有 harness cluster 的关系

| 维度 | R336 effective harnesses | R418 planner-generator-evaluator | **R600 property-based-testing** |
|------|--------------------------|---------------------------------|---------------------------------|
| 角色 | 通用 long-running agent | 三 agent 协作 | **agent 作为 bug hunter** |
| 核心机制 | init/planning/retrieval | planner 生成 → generator 实现 → evaluator 评估 | **理解 → 提 properties → 写 tests → 反思** |
| 反馈循环 | human-in-loop | evaluator → planner | **self-reflection (模型自己 review)** |
| 适用阶段 | agent 设计期 | agent 协作 | **production 代码 quality 验证** |
| 评估指标 | 任务完成度 | 子任务质量 | **bug valid rate (56% / 86% top)** |

**R600 与 R418 的关键区别**：R418 是「agent 评估 agent」（evaluator 是独立 agent），R600 是「agent 评估自己」（reflection 是同一 agent 多次调用）。这两种 self-check 范式在生产 harness 设计中需要**明确选择**：评估多样性高的场景用 R418，反思一致性高的场景用 R600。

## 六、可复用模板：5 步复制路径

任何团队想复现 R600 的能力：

1. **选 PBT 框架** — Python 用 Hypothesis，JS 用 fast-check，Rust 用 proptest
2. **定义 target scope** — 单文件 / 单 module / 单函数，明确边界
3. **写 agent command** — `.claude/commands/hypo.md` 模板可直接 fork `mmaaz-git/agentic-pbt`
4. **加 reflection loop** — agent 写完 test 必须「检查自己是否吞掉异常 / 写 trivial property」
5. **rubric 排序** — 人工标 50 个样本，训练模型做 top-K 排序，把 precision 从 56% 提到 86%

**重要前提**：第 4 步需要 Opus 4.1+ 或 Sonnet 4.5+ 模型，Sonnet 4 反思能力不足。

## 七、对 Agent Engineering 社区的启示

R600 揭示了一个新角色定位：**「Agent as bug hunter」**。这与「agent as coder」(Copilot/Cursor/Codex)、「agent as reviewer」(R546 Coderabbit) 并列，是 2026 H2 emerging 角色之一。

**对 harness 设计的具体影响**：
- **长程任务必须配 self-reflection loop**，不能用单次 LLM 调用
- **多 reviewer 验证是 production-grade agent 的标配**（3 expert human + rubric 双轨）
- **agent 输出排序比 agent 输出生成更可工程化**（rubric 排序把 precision 提升 30+ 百分点）

## 八、引用

- **Anthropic Blog (1st-party)**: https://www.anthropic.com/research/property-based-testing
- **NeurIPS 2025 DL4C Workshop Paper**: https://arxiv.org/abs/2510.09907
- **GitHub Repo**: https://github.com/mmaaz-git/agentic-pbt (74⭐, License=None — research artifact)
- **Bug Reports Site**: https://mmaaz-git.github.io/agentic-pbt-site/
- **Hypothesis Plugin Article**: https://hypothesis.works/articles/claude-code-plugin/

## 结论

R600 = **「Agent as bug hunter」角色正式化**。Anthropic 给出第一个可复现模板：Claude Code custom command + 4 步自反思 + rubric 排序 + 多 reviewer 验证。在 100+ PyPI 包上 56% valid / 32% reportable，maintainer 已接受多个 fix。**核心工程贡献不是 bug 数字，是「agent harness 4 步循环 + 3 阶段评估」这个可复用的 production-grade 模板**。对 Agent Engineering 社区的意义：长程 agent 任务必须显式 self-reflection，多 reviewer 验证是 production 标配，agent 输出排序（rubric 评分）比生成（原始概率）更可工程化。
