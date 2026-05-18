# Harbor Framework：当 Agent 评测有了官方 Harness

[Harbor](https://github.com/harbor-framework/harbor) 解决了一个长期以来让 Agent 研究者头疼的问题：同一套评测任务，用不同的 Harness 跑出来的结果完全不可比。Harbor 是 Terminal-Bench 2.0 的官方 Harness，也是当前少数几个试图建立「标准 Agent 评测基础设施」的开源项目之一。

## 这个项目解决了一个什么问题

如果你在评测一个新 Agent，你通常会写一个自己的 Harness 来控制它：启动进程、发送指令、捕获输出、判断成功失败。但问题是——**你的 Harness 和别人的 Harness 不一样**，所以你跑的 SWE-bench 分数和别人的分数没有可比性。甚至同一个模型，用 Claude Code harness 和用自己写的 harness 跑 Terminal-Bench，分数可以差 10-20 分。

Harbor 试图解决这个问题：

> "Harbor is a framework for running agent evaluations and creating and using RL environments."

它提供标准化的接口，支持主流 Agent（Claude Code、OpenHands、Codex CLI 等），研究者可以直接用官方 harness 跑评测，不用再自己造轮子。

## 核心能力

**标准 Harness + 并行评测**：

```bash
export ANTHROPIC_API_KEY=<YOUR-KEY>
harbor run --dataset terminal-bench@2.0 \
  --agent claude-code \
  --model anthropic/claude-opus-4-1 \
  --n-concurrent 100 \
  --env daytona
```

一条命令就能并发跑 100 个实例，自动部署到 Daytona 或 Modal 云端。

**多基准支持**：Harbor 不只支持 Terminal-Bench，还支持 SWE-Bench、Aider Polyglot 等主流评测：

```bash
harbor datasets list
harbor run -d "<dataset@version>" -m "<model>" -a "<agent>"
```

**RL 环境生成**：除了评测，Harbor 还支持生成 RL 训练用的 rollout 环境——这意味着你可以在它上面做 Agent 的强化学习训练。

## 关键数字

| 指标 | 数值 |
|------|------|
| GitHub Stars | 1,985 |
| Forks | 1,029 |
| 维护方 | Laude Institute（Terminal-Bench 2.0 维护方）|
| 支持的 Agent | Claude Code、OpenHands、Codex CLI 等 |
| 云端支持 | Daytona、Modal |

## 为什么值得关注

Cursor Composer 2 的技术报告中特别提到，Anthropic 模型在 Terminal-Bench 2.0 上用的是 Claude Code harness，OpenAI 模型用的是 Simple Codex harness。这句话背后是一个残酷的现实：**Harness 的质量直接决定评测结果的可信度**。

Harbor 的出现意味着 Agent 评测正在走向标准化。如果你的 Agent 支持 Harbor 接口，你就能在同一个基础上和所有其他 Agent 比较。这对研究者和有评测需求的企业来说都是有价值的。

## 适用场景

- **模型研发团队**：需要标准化的端到端评测，而不是自己造 Harness
- **Agent 开发者**：想知道自己的实现和其他 Agent 比处于什么水平
- **学术研究者**：需要可重复的评测结果用于论文

## 引用

> "Harbor is the official harness for Terminal-Bench 2.0." — [Harbor GitHub](https://github.com/harbor-framework/harbor)

> "You can use Harbor to evaluate arbitrary agents like Claude Code, OpenHands, Codex CLI, and more, and build and share your own benchmarks and environments." — [Harbor Framework Docs](https://harborframework.com/docs)

## 相关链接

- GitHub: https://github.com/harbor-framework/harbor
- 官方文档: https://harborframework.com/docs
- Terminal-Bench Leaderboard: https://www.tbench.ai/leaderboard/terminal-bench/2.0
- Cookbook: https://github.com/harbor-framework/harbor-cookbook