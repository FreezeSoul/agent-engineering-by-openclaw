# Claw-Eval：让 Agent 评估真正可信的开源 Harness

> 来源：[claw-eval/claw-eval](https://github.com/claw-eval/claw-eval)，GitHub，684⭐，PKU + HKU 联合开发

## 核心命题

Agent 评估最大的问题不是"有没有 benchmark"，而是**"评估结果能不能信"**。大多数现有评测要么靠人工主观打分，要么只跑一次就出结果，要么缺少 sandbox 隔离——用 GitHub Copilot harness benchmark 文章的话说，这些都会导致"false negative"：Agent 实际上做对了，但测试说它失败了。

Claw-Eval 是一套从北大和港大走出来的开源评估 harness，核心解决一个问题：**如何用可复现的方式，真实地评估 LLM 作为 Agent 的能力**。它不是又一个"SWE-bench 复刻"，而是一套从任务设计到评分逻辑再到 sandbox 隔离的完整工程框架。

## 为什么这个项目值得关注

笔者认为，Claw-Eval 的价值不在于"有多少个任务"（300 个确实不少），而在于它对评估方法论本身做了深度思考。这与 GitHub Copilot 团队在 harness benchmark 中揭示的"方差问题"形成了直接的工程呼应——Claw-Eval 就是为了解决这个问题而生的。

**引用自 README**：
> "We are committed to end-to-end reproducibility. Our codebase is currently being audited to ensure all benchmark results on the leaderboard can be verified by the community."

笔者认为，"end-to-end reproducibility"和"社区可验证"是评估框架最重要的两个工程属性，但大多数评测框架在这两点上都做得很薄弱。Claw-Eval 能明确承诺这两点，说明团队对评估的科学性有清醒认知。

## 任务体系：300 个任务，9 个类别，3 个 Split

Claw-Eval 将任务分为三个 split，覆盖不同的 Agent 能力维度：

| Split | 任务数 | 描述 |
|-------|--------|------|
| **general** | 161 | 核心 Agent 任务，覆盖通信、金融、运维、 productivity 等领域 |
| **multimodal** | 101 | 感知与创作：网页生成、视频 QA、文档提取等 |
| **multi_turn** | 38 | 对话式任务，带有模拟用户 persona 进行澄清和建议 |

值得注意的是，multi_turn 这个 split 在现有评测中非常稀缺。大多数 benchmark 只评估单轮任务，但真实世界的 Agent 工作流往往是多轮的——用户给一个模糊目标，Agent 提问，用户提供反馈，Agent 继续执行。这个场景被严重低估了。

## Pass^3 评分机制：解决方差问题的工程方案

这是 Claw-Eval 最有技术含量的设计。传统的评测方法是"N=1"：跑一次，成功就是成功，失败就是失败。但 Agent 行为具有随机性，单次运行的结果波动很大——GitHub Copilot benchmark 文章中展示的 TerminalBench 方差分析图就清楚说明了这一点。

Claw-Eval 的解决方案是 **Pass^3**：

> "To eliminate 'lucky runs,' a model must now consistently pass a task across three independent trials (N=3) to earn a success credit."

只有当模型在 3 次独立运行中**全部通过**时，任务才被标记为成功。这个设计直接呼应了 GitHub 文章中方差分析的洞察：平均分一样没用，可重复的成功才是可靠的。

此外，对于 API 波动导致的执行错误，团队会手动重新触发评估，确保恰好生成 3 条有效轨迹。这个细节在工程上非常重要——大多数开源评测遇到 API 错误就直接放弃了。

## 三维评分：Completion + Safety + Robustness

大多数评测只看"任务有没有完成"，但 Claw-Eval 采用了更细粒度的三维评分：

- **Completion**：Agent 是否完成了任务？
- **Safety**：Agent 是否避免了有害或未授权的行为？
- **Robustness**：跨多次试验是否表现一致？

这个三维框架笔者认为非常有价值。特别是 Safety 维度——大多数 Agent 评测完全忽略了这个维度，但生产环境中一个不安全的 Agent 造成的损失可以远超效率提升带来的收益。

## 技术架构亮点

**构建在社区工作之上**：
Claw-Eval 借鉴了 OpenClaw、PinchBench、OfficeQA、OneMillion-Bench、Finance Agent 和 Terminal-Bench 2.0 的任务设计。这个继承关系让它站在了前人的肩膀上，而不是重新发明轮子。

**完整的 Sandbox 隔离**：
从 README 看，提供了 `test_sandbox.sh` 脚本处理环境隔离。对于评估 Agent 来说，sandbox 是安全性和可复现性的基础保障——没有隔离的评估，其结果是不可信的。

**基于 Hugging Face 的数据集分发**：
视频等大文件 fixture 存放在 Hugging Face datasets 上，而不是 GitHub repo（受文件大小限制）。这个工程选择很务实，也方便社区使用。

## 竞品对比

| 维度 | SWE-bench | Terminal-Bench | Claw-Eval |
|------|-----------|----------------|-----------|
| 任务类型 | 代码修复 | 终端操作 | 综合（general + multimodal + multi_turn）|
| 评分方式 | 单一结果 | 单一结果 | Pass^3（3轮全过）|
| 安全评估 | ❌ | ❌ | ✅ |
| 多轮对话 | ❌ | ❌ | ✅ |
| 社区验证 | 部分 | 部分 | 承诺 full reproducibility |

笔者认为，Claw-Eval 的最大差异化在于**multi_turn 和 Safety 这两个维度**，以及 **Pass^3 的评分机制**。这两点都是现有主流评测严重缺失的。

## 局限性

1. **Stars 只有 684**：相比 SWE-bench 等知名基准，社区认可度还在早期
2. **PKU/HKU 学术团队背景**：工程化程度和长期维护能力待验证
3. **Grader 依赖专有模型**：README 提到使用 gemini-3-flash 和 claude-opus-4.6 作为 grader，这引入了第三方依赖和成本

## 适用场景

- 评估 Agent 模型选型（特别是需要多轮对话能力的场景）
- 对 Agent Safety 有要求的生产环境
- 需要可复现评估结果的研究团队
- 与 GitHub Copilot harness benchmark 文章形成"理论 ↔ 工程实现"的闭环学习

## 如何使用

```bash
pip install uv
uv venv --python 3.11
source .venv/bin/activate

export OPENROUTER_API_KEY=sk-or-...
export SERP_DEV_KEY=...
bash scripts/test_sandbox.sh

claw-eval batch --config model_configs/claude_opus_46.yaml --sandbox --trials 3 --parallel 16
```

## 结语

Claw-Eval 解决了一个根本问题：Agent 评估不能只报平均分，要关注可重复性和安全性。配合 GitHub Copilot harness benchmark 文章一起阅读，能形成从"为什么 harness 设计重要"到"如何工程化实现可信评估"的完整认知闭环。

笔者认为，这个项目值得在 Agent 工程实践者的工具箱中占有一席之地——不是因为它完美，而是因为它认真对待了评估这件事本身。

---

**引用来源**：
- "To eliminate 'lucky runs,' a model must now consistently pass a task across three independent trials (N=3) to earn a success credit." — claw-eval README
- "We are committed to end-to-end reproducibility. Our codebase is currently being audited to ensure all benchmark results on the leaderboard can be verified by the community." — claw-eval README
- Task split: general (161) / multimodal (101) / multi_turn (38) — claw-eval README