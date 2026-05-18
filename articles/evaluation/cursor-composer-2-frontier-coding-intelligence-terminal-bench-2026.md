# Cursor Composer 2：前端级编程智能与 Terminal-Bench 2.0 评测体系的意义

2026年3月19日，Cursor 发布 Composer 2，宣称达到「前端级编程智能」。这不是营销话术，而是一个值得深究的工程声明。本文从技术细节出发，解释为什么这个声明值得认真对待，以及它背后的评测体系意味着什么。

## 核心数据：不是增量改进，是代际跨越

Composer 2 在三个主流基准上对比 Composer 1 有显著提升：

| 模型 | CursorBench | Terminal-Bench 2.0 | SWE-bench Multilingual |
|------|-------------|-------------------|----------------------|
| Composer 2 | 61.3 | 61.7 | 73.7 |
| Composer 1.5 | 44.2 | 47.9 | 65.9 |
| Composer 1 | 38.0 | 40.0 | 56.9 |

这不是常规迭代曲线。从 Composer 1 到 Composer 2，Terminal-Bench 2.0 提升超过 20 个百分点——通常这种幅度的提升需要换模型架构才能实现。Cursor 团队在技术报告中指出，提升来自「首次继续预训练 + 长程强化学习」的组合：先用更强的基座模型，再在长程任务上做 RL。

真正值得注意的不是绝对数字，而是这些数字背后的含义：**Terminal-Bench 2.0 是专门为 Agent 评测设计的基准**，不是刷题式的算法题。它测试的是 Agent 在真实 terminal 环境中的操作能力——这对实际编码工作流程才是有意义的度量。

## Terminal-Bench 2.0：为什么这个基准值得关注

Terminal-Bench 由 Laude Institute 维护，是当前少数几个专门针对 Agent terminal 操作能力的评测基准之一。它的设计目标是：

> "An agent evaluation benchmark for terminal use"

Composer 2 的技术报告注释中特别提到：

> "Anthropic model scores use the Claude Code harness and OpenAI model scores use the Simple Codex harness."

这句话透露了一个关键信息：模型评测结果高度依赖所使用的 Harness。同一个 Claude Opus 模型，用 Claude Code harness 和用其他 harness 跑出来的分数可以差很远。这意味着**评测的可重复性不仅取决于任务设计，还取决于标准 harness 的实现**。

这也是为什么 Harbor Framework 的出现变得重要——它是 Terminal-Bench 2.0 的官方 harness：

```bash
export ANTHROPIC_API_KEY=<YOUR-KEY>
harbor run --dataset terminal-bench@2.0 \
  --agent claude-code \
  --model anthropic/claude-opus-4-1 \
  --n-concurrent 4
```

Harbor 支持并发运行、云端部署（Dstone 和 Modal），以及多种 Agent 的标准化评测。它的设计理念是让研究者和工程师能够用同一套工具评估不同 Agent 的表现，而不是各自为政地造轮子。

## 为什么「前端级」这个说法值得认真对待

Cursor 敢用「frontier-level」这个词，一个重要原因是 Terminal-Bench 2.0 的结果具有可比性。Composer 2 的 61.7 分在这个基准上是公开可查的，且使用的是官方 Harbor harness 评测——排除了手工调优 Harness 刷分的可能。

但更值得注意的也许是另一个数字：Composer 2 的价格是 **$0.50/M 输入 + $2.50/M 输出**，比 Claude Opus 4.0 和 GPT-4.5 都便宜很多。如果在 Terminal-Bench 2.0 上达到相近甚至更好的表现，那「前端级智能 + 低成本」这个组合会改变 Agent 评测的性价比计算方式。

## 笔者认为：这个进展真正重要的地方

Cursor 的这篇 Blog 表面上是一个模型发布公告，但它透露了一个更重要的趋势：

**Agent 评测正在从「各自为政」走向「标准 Harness + 公开基准」的阶段**。Harbor Framework 作为 Terminal-Bench 2.0 的官方 harness，开始被多个模型评测所采用。这意味着：

1. **模型对比变得更可信**：用同一个 harness、同一套任务评测的不同模型，分数才真正可比
2. **Harness 工程质量成为竞争力**：谁能把 Agent harness 做稳定、做规范，谁的模型分数就更可信
3. **Agent 评测的「基础设施层」正在成型**：Harbor 不仅仅是一个评测工具，它的架构支持并行评测、RL 环境生成、云端部署——这实际上是一个 Agent 研发的基础设施平台

这与 Anthropic 在 Eval 上的投入方向一致：好的评测不只是打分，是研发流程的一部分。

## 参考来源

- [Cursor Blog: Introducing Composer 2](https://cursor.com/blog/composer-2)（2026年3月19日）
- [Terminal-Bench 2.0 官方 Leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.0)
- [Harbor Framework GitHub](https://github.com/harbor-framework/harbor)
- [Harbor 官方文档](https://harborframework.com/docs)