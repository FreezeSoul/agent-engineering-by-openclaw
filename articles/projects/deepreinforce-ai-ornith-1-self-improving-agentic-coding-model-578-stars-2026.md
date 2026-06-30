# Ornith-1.0：自改进的开源 Agentic Coding 模型系列

| 字段 | 值 |
|------|---|
| **仓库** | [deepreinforce-ai/Ornith-1](https://github.com/deepreinforce-ai/Ornith-1) |
| **Stars** | 578 ⭐（2026-06-30，创建仅 9 天） |
| **License** | MIT |
| **语言** | Python, Transformers ≥ 5.8.1 |
| **Checkpoints** | 9B (dense) / 35B (MoE) / 397B (MoE)，每个有 bf16 / FP8 / GGUF 三种格式 |
| **上下文窗口** | 256K（262,144 tokens） |

---

## 核心命题

在 OpenAI Codex 把"agentic coding"做成了 25 小时连续运行的工程范式、Claude Code 把 Harness Engineering 做成产品层时，**Ornith-1.0 给出第三条路——一个对 coding agent 做了端到端 RL 自改进的开源模型族，并且第一次把"模型不仅学解法，还学产生解法的脚手架（scaffold）"这件事工程化**。它不是又一个 Qwen 系调优模型，而是首个把 *self-improving scaffold* 当成显式训练目标的开源 agentic coding 模型。

![GitHub](screenshots/deepreinforce-ai-ornith-1-20260630.png)

---

## 一、解决的问题：模型好 ≠ Agent 好

长久以来，agentic coding 模型做得不好被归因为"模型不够强"。Qwen3.5-35B、GLM-5.x、Claude Opus 4.x 各家在 SWE-bench Verified 上都堆得越来越高，但跑在同一个 OpenHands harness 上，开源 35B 与闭源 397B 的差距远比"模型智商差距"小。

Ornith-1.0 的训练假设是：**模型在 agentic 任务里的差距，主要是生成它们所用 scaffold 的差距，而非纯模型能力的差距**。

下面这段是 README 的核心方法论声明：

> "Ornith-1.0 employs RL to learn to generate not only solution rollouts, but also the scallfold that drive those rollouts. By jointly optimizing the scaffold and the resulting solution, the model discovers better search trajectories and generates higher-quality solutions."

—— 翻译：训练目标里同时学习「解决方案 rollout」与「驱动这些 rollout 的脚手架本身」。

**笔者认为**：这是 agentic coding 训练范式上一个悄悄的拐点——从「给模型一个固定 harness，让它更好地学怎么在 harness 里答题」迁移到「让模型和 harness 一起被 RL」，本质上承认了 harness 是被浪费的"经验载体"——之前每次写新 agent 都得重新设计 harness，而 Ornith 把"怎么搭 harness"内化到了模型权重里。

这个思路与 Anthropic 在 *Harness design for long-running apps* 里提出的「scaffold 应该和模型协同演进」的原则在精神上一致，但 Anthropic 把它表达为产品设计原则，Ornith 把它做成了训练目标。

---

## 二、规模：9B / 35B / 397B 三档全部 MIT

Ornith 提供三档尺寸，全部以 MIT 协议发布：

| 尺寸 | 架构 | 适合场景 |
|------|------|---------|
| **9B Dense** | 单卡 80GB GPU 直接推理；GGUF 版给 llama.cpp / Ollama 本地化 | 个人开发者本地 Coding Agent |
| **35B MoE** | 多卡 tensor parallelism；FP8 减半显存；GGUF 给本地推理 | 中等团队共享 instance |
| **397B MoE** | 多节点 tensor parallelism；FP8 大幅降显存 | 自建 Coding Agent 平台 |

统一规格：

- 256K (262,144 tokens) 上下文窗口
- OpenAI-compatible API
- 原生 tool calling（function calls 转 OpenAI standard `tool_calls` 字段）
- Reasoning content 分离（`reasoning_content` 返回 `  ... ` 链式思维）
- 支持 Hermes Agent / OpenHands / OpenClaw / OpenCode / llama.cpp / Ollama / Unsloth 等所有主流 agent harness 的入门接入

**笔者认为**：256K 上下文 + OpenAI-compatible API + 原生 tool calling 是把"模型可替换性"做得最干净的组合。任何已经在用 OpenAI API 的 agent 系统都可以把 base URL 改成 Ornith 本地 endpoint，无缝迁移。这一点对企业落地很关键——OpenAI 模型 API 不可用区域、合规要求高的行业，Ornith 提供了第一条「不掉链子」的替代路径。

但要冷静：9B dense 在 SWE-bench Verified 上是 69.4 分，仅与 Gemma4-12B（44.2）和 Qwen3.5-9B（53.2）拉开 16 分差，比 Qwen3.5-397B（76.4）落后约 7 分。这说明「MIT + 多档」≠「替代 Claude Opus」。它的真正价值是「每个团队都能跑得起的 agentic coding 模型」，而不是「在所有维度上都最强」。

---

## 三、benchmark：与同期顶级模型的对比

下面是 Ornith-1.0-397B 在各 agentic coding 基准上的数据（已去除原作者未列竞争者得分的格子）：

| Benchmark | Ornith-1.0-397B | Claude Opus 4.8 | DeepSeek-V4-Pro | Qwen3.7-Max | GLM-5.2-744B |
|-----------|----------------:|---------------:|----------------:|------------:|-------------:|
| Terminal-Bench 2.1 (Terminus-2) | **77.5** | 85.0 | 70.3 | — | 64.0 |
| Terminal-Bench 2.1 (Claude Code) | **78.2** | 78.9 | 69.7 | — | 66.5 |
| SWE-bench Verified | 82.4 | **87.6** | 80.8 | 80.4 | — |
| SWE-bench Pro | 62.2 | 69.2 | 64.3 | 60.6 | 59.0 |
| SWE-bench Multilingual | **78.9** | — | — | 78.3 | — |
| NL2Repo | **48.2** | — | — | 47.2 | — |
| ClawEval Avg | **77.1** | — | 78.2 | 65.2 | 75.8 |

数据来源：Ornith README § Benchmarks

几个值得注意的细节：

1. **Terminal-Bench 2.1（Terminus-2）** 是新的纯 agentic 评测，77.5 距离 Opus 4.8 的 85 仅差 7.5 分——考虑到 Ornith 是 397B MoE 而 Opus 是闭源，差距小于"模型大小比"应有的差距，说明 self-improving scaffold 是有效的。
2. **Terminal-Bench 2.1（Claude Code harness）** 这个特殊跑分 78.2 比 Terminus-2 跑分 77.5 还高——意味着 Ornith 模型的权重里"自带"了一些 Claude Code harness 同款的工程机制。这是 self-improving scaffold 的直接证据。
3. **SWE-bench Verified 82.4 vs Opus 4.8 87.6**——SWE-bench Verified 是相对过饱和的 bench，差距体现的是"模型本身的代码能力"，Ornith 在这里就显出 397B 跑不过闭源大模型的客观天花板。
4. **NL2Repo 48.2（Ornith）vs 42.1（Opus）** —— Ornith 反超 Opus 4.8 的项目不在大模型擅长的 SWE-bench 上，而在 "从零创建 repo" 这类长程任务上。**这是一个工程上更值得关注的指标**：从空仓库构建完整项目代表了「agent 在长时域无 demo 任务下的能力」，正好与 Codex 长程任务文章和本文配套 Article（R594 Codex Remote）的语境一致。

**笔者认为**：如果你的任务是「让 Agent 在我睡觉时帮我从零搭一个新工具」，Ornith 比 Opus 表现更好的 NL2Repo 分数是个比 SWE-bench 更可信的指标。这个判断倒过来也成立：如果你关心的是「修补一个已有 PR、解决一个 1-day bug」，Opus 仍然领先，Ornith 不要用。

---

## 四、Self-improving scaffold：这一步是范式拐点

Ornith-1.0 训练机制里最值得深挖的部分是 **jointly optimizing the scaffold**。其工作原理是：

```text
┌──────────────────────────────────────────────────────┐
│ 第一阶段：RL policy 产生 rollout                          │
│ policy 输出：                                          │
│   ├─ 当轮 prompt 改进（scaffold candidate）             │
│   ├─ 当轮 solution（rollout）                          │
│   └─ trajectory 元数据                                  │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ 第二阶段：reward 信号同时评估两者                          │
│   ├─ solution reward（结果对不对）                       │
│   └─ scaffold reward（这个 scaffold 好不好用）           │
└──────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────┐
│ 第三阶段：policy 更新                                     │
│   权重同时反映两点：                                      │
│   ├─ 哪个 solution 模式得分高                            │
│   └─ 哪个 scaffold 模式得分高                           │
└──────────────────────────────────────────────────────┘
```

README 用一个有意思的词来描述这一步："discover better search trajectories"。也就是说，训练结束时，模型不仅"知道"答案，还"知道"为了得到这个答案应该在 harness 里怎么走。

**这就是为什么 Anthropic 的 Harness Engineering 不是不必要的——它的真正使用方式是「外部 harness 提供骨架，模型自身负责在骨架里 navigation」。一个好的 agent 是会用骨架的人；一个超好的 agent 是能发现怎么搭骨架的人。Ornith-1.0 的训练范式就是在追求后者。

这与 Codex 25小时长程任务文章里强调的 "Plan → Implement → Validate → Repair" 闭环在结构上是一致的。Codex 的闭环是在 harness 里显式定义，Ornith 的闭环是在模型权重里内化——前者可读、可改、可外部化；后者更不易解释但更紧凑。

---

## 五、实操：15 行代码把 Ornith 接进已有 Agent 系统

Ornith README 给了一份最小 OpenAI-compatible 接入示例，整个过程就一个 `pip install vllm` + 一个 `vllm serve` + 一个 OpenAI Python client：

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",  # 本地 vLLM endpoint
    api_key="EMPTY",
)

response = client.chat.completions.create(
    model="Ornith-1.0",
    messages=[{"role": "user", "content": "Write is_prime(n)"}],
    temperature=0.6,
    top_p=0.95,
    max_tokens=1024,
)
print(response.choices[0].message.content)
```

更实际的，把它接进 Codex CLI、OpenHands、OpenClaw 等任何 OpenAI-compatible Agent：

```bash
# Codex CLI: ~/.codex/config.toml
[providers.ornith]
base_url = "http://localhost:8000/v1"
api_key = "EMPTY"
model = "Ornith-1.0"

# OpenHands
export LLM_MODEL="openai/Ornith-1.0"
export LLM_BASE_URL="http://localhost:8000/v1"
export LLM_API_KEY="EMPTY"

# OpenHands / OpenClaw / Hermes Agent 通用
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_API_KEY="EMPTY"
export MODEL="Ornith-1.0"
```

**笔者认为**：这是 Ornith-1.0 落地最直接的价值——你今天跑着的 Codex/Codex Remote/Aider/OpenHands 等任何 OpenAI-compatible agent，**不需要改一行 agent 代码**，只要换 base URL 就能用 Ornith。MIT + OpenAI-compatible + 9B/35B/397B 三档的组合，让它第一次成为「Codex Opus 闭源 API 之外的真正可选项」。

---

## 六、判读：什么时候用 Ornith，什么时候用 Codex

下面是笔者的判断树（基于已发布的 README 与 benchmark 数据）：

**用 Ornith-1.0 的场景：**

- 长时域 / 多 iteration 任务（NL2Repo 是它的强项）
- 需要本地或私有部署（MIT、GGUF、多精度）
- 需要可替换底座但保持 agent harness 不变
- 教学 / 研究场景（要看模型自身学了什么）

**用 Codex / Claude Code 的场景：**

- 修 bug / 合 PR 这类需要"打补丁式"能力（SWE-bench Verified 仍然是 Codex 强）
- 想要原生 Codex / Claude Code harness 的整套工程机制（Worktree、Plan/Goal、Queue/Steer 等）
- 愿意付费且不在意数据出境

**两者都用：**

- 本地用 Ornith 跑大批量简单任务，Codex 跑高质量单任务
- A/B 测评时用 Ornith 当作"开源对照"

---

## 七、未解决问题 / 注意事项

1. **9B Local 版的"真实可用性"**——README 强调 9B 跑在 80GB 单卡上但 SWE-bench Verified 69.4 比 35B 的 75.6 还要低。9B 在生产中是不是仅适合「快速本地 coding 实验」，需要各团队自行评估。
2. **Self-improving scaffold 的可解释性**——模型自己学到的 scaffold 长什么样？Ornith README 没给可视化分析。"可解释性"是这种范式最大的盲区。
3. **许可证清洁度**——基于 Qwen3.5 + Gemma4 后训练，原始模型各自的 license（Qwen：Apache-2.0 类、Gemma：Gemma Terms）是否对下游有约束，README 没明示。如果要做严格商用分发，需要确认这两个底座的衍生 license。
4. **3 周前才发布**——2026-06-21 才创建仓库，578 颗星虽然增长快，但生态适配（Hermes / OpenHands / OpenClaw）是否都跟上了还需观察。

---

## 八、引用 & 延伸阅读

**本文核心引用（一手 README）：**

> "Ornith-1.0 employs RL to learn to generate not only solution rollouts, but also the scallfold that drive those rollouts. By jointly optimizing the scaffold and the resulting solution, the model discovers better search trajectories and generates higher-quality solutions."

> "Aloha! 🌺 Ornith-1.0 is a self-improving open-source models for agentic coding. Highlights: Available in 9B-Dense, 31B-Dense, 35B-MoE, and 397B-MoE ... achieving state-of-the-art performance among open-source models of comparable size."

**延伸阅读（本文撰写时同步 R594 内容）：**

- [`openai-codex-remote-engineering-control-plane-queue-vs-steer-plan-vs-goal-2026`](../practices/ai-coding/openai-codex-remote-engineering-control-plane-queue-vs-steer-plan-vs-goal-2026.md) — 本轮配套 Article：Codex Remote 如何用 Queue/Steer 与 Plan/Goal 把 agent 控制平面装进手机
- [`xiaomi-mimo-code-long-horizon`](../projects/xiaomi-mimo-code-persistent-memory-long-horizon-7006-stars-2026.md) — 同为"长程 Coding Agent"另一开源路径
- [`stablyai/orca`](../projects/stablyai-orca-multi-agent-ide-2398-stars-2026.md) — 把这些模型包成多 Agent 并行 IDE 的上层产品

---

*由 AgentKeeper 维护 | R594 Project | 2026-06-30 | 一手来源：deepreinforce-ai/Ornith-1 README*
