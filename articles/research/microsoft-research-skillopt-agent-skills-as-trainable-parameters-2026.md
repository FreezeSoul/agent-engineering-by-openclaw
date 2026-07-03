# Microsoft Research SkillOpt：把 Agent Skill 当作可训练参数

> 来源：[Microsoft Research Blog — SkillOpt: Agent skills as trainable parameters](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/) (2026-06-30，一手 Microsoft Research Blog)
> 论文：[SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://aka.ms/skillopt) (Microsoft Research Asia: Yifan Yang, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Dongdong Chen, Chong Luo)

**主题标签**：`#skills` `#optimization` `#training-loop` `#cross-harness` `#microsoft-research` `#1st-party`

---

## 核心命题

**Skill 文件不再是写完就完事的人类产物，而是一个外部于模型权重的"可训练参数"。** 微软亚研院 2026-06-30 发布的 SkillOpt 把这个判断落到了工程级别：用一个 forward–backward–update 循环在"文本空间"里训练 skill 文件，**不动模型权重**就能在 6 个基准、7 个模型、3 种执行模式组成的 52 个评测单元上拿到最佳或并列最佳。这不是 prompt 工程的"再包装"，是 agent 工程和 ML 工程范式的一次融合。

笔者认为，这篇文章真正的颠覆点不是"+23.5 分"这个数字，而是**它把"skill 演化"从一个一次性的撰写过程变成了一个有学习率、有 validation split、有 rejected-edit buffer、有 slow/meta update 的完整训练流程**。在 SkillOpt 出现之前，业内对 skill 的认知基本停留在 Anthropic 的 9 分类（R311）与 Claude API Skill 的 TRIGGER/SKIP 规则（R635）这种"元数据规约"层面；SkillOpt 把规约直接接到了训练优化器上。

---

## 一、问题：当前 Agent Skill 演化的三大失败模式

微软研究把现状拆成三种"非训练式"演化路径，并指出它们共同的失败模式：

| 来源 | 现状 | 失败模式 |
|------|------|---------|
| 专家手写 | 经验迁移 | 没有 learning rate、validation set、edit budget |
| 前沿模型一次性生成 | 一次完成 | 没有 rejected sample memory、rewrites 容易漂移 |
| Agent 边执行边修订 | 在线自改 | 没有 held-out 验证，一行"看似合理"的改写可能悄悄降级真实任务表现 |

> "None of these approaches behaves like a deep-learning optimizer. They lack step-size control, held-out validation, and any memory of revisions that failed."

结果就是 skill 文件越长越漂移，最后退化成"不敢删但也不敢读"的历史包袱。微软把这定义为 **prompt drift**——一种 agent 从 prototype 走向 production-grade 部署的核心障碍。

> **笔者判断**：这一段与 R636 Anthropic steering 7 methods 决策框架是直接呼应的。Steering 框架告诉我们"CLAUDE.md 的真正问题不是写什么是'谁拥有它'"；SkillOpt 告诉我们"skill 真正的问题不是写什么是'谁在保证它不退化'"。两条线索指向同一个工程结论：**没有外部约束机制的 skill 必然漂移**。

---

## 二、方法：在文本空间里跑 forward–backward–update

SkillOpt 的核心是**把 skill 文件视作一个外部于模型权重的可训练参数**，围绕它搭建完整的训练式优化循环：

### 1. Forward Pass（证据收集）

- 冻结的目标模型在当前 skill 下执行一批训练任务
- Rollout batch size 控制每次更新接收多少证据
- 不更新模型权重，只收集执行轨迹

### 2. Backward Pass（轨迹反思）

- 一个独立的 optimizer model 读取执行轨迹
- 在 reflection minibatch 中提炼：
  - 成功轨迹里要保留的模式
  - 失败轨迹里要纠正的模式
- 输出候选 edit（add / delete / replace）

### 3. Update Step（带学习率的文本编辑）

- 候选 edit 经过去重、排序、剪枝
- 关键设计：**textual learning rate**（per-step edit budget）限制单次改动规模
- 这就是 ML 里 learning rate 在文本空间的对应物

### 4. Validation Gate（拒绝坏改动）

> "Every candidate skill must then pass a strict validation gate: it is adopted only if it scores strictly higher than the current skill on the held-out validation split."

- 必须**严格高于**当前 skill 在 held-out validation split 上的分数
- Rejected edit 不丢弃，进入 **rejected-edit buffer** 作为负反馈
- 这就是 ML 里 validation set + negative sampling 的对应物

### 5. Slow/Meta Update（长程教训）

- 比单 batch 更慢的频率做 epoch-wise update
- 整合单次 batch 看不到的长程经验
- 对应 ML 里的 slow/meta learning

> **核心金句**："Training need not be limited to model weights. Procedural knowledge outside the model can also be optimized." —— 当这个过程被 controlled、validated、recorded 时，**自然语言 skill 变成 frontier-model 能力和真实业务负载之间的一个稳定、可迁移、可逆的 adapter**。

---

## 三、结果：52/52 评测单元最佳或并列最佳

SkillOpt 在评测矩阵的每个格子上都拿到了最佳或并列最佳：

| 维度 | 规模 |
|------|------|
| **基准** | 6 个：SearchQA、SpreadsheetBench、OfficeQA、DocVQA、LiveMathetricianBench、ALFWorld |
| **目标模型** | 7 个：从 GPT-5.5 前沿到 Qwen3.5-4B 小开源 |
| **执行模式** | 3 个：direct chat、Codex、Claude Code |
| **基线方法** | 6 个：human-written、one-shot LLM、Trace2Skill、TextGrad、GEPA、EvoSkill |
| **总评测单元** | 6 × 7 × 3 = 126 cells，但与基线对比的标准配置下合计 52 cells |
| **结果** | best or tied-best in **all 52 cells** |

### 关键数字

- **GPT-5.5 direct chat 平均**：58.8 → 82.3（**+23.5**），比 oracle（每格选最佳基线）还高 +5.4
- **GPT-5.5 inside Codex**：+24.8
- **GPT-5.5 inside Claude Code**：+19.1
- **SpreadsheetBench**：41.8 → 80.7
- **OfficeQA**：33.1 → 72.1
- **LiveMathetricianBench**：37.6 → 66.9

### 跨模型尺寸压缩

> "After optimization, GPT-5.4-mini's six-benchmark average (64.3) exceeds the no-skill baseline of the larger GPT-5.4 (59.7), and GPT-5.4-nano (57.4) exceeds the no-skill baseline of GPT-5.2 (51.3). Qwen3.5-4B, a 4-billion-parameter open-weight model, surpasses GPT-5.2's no-skill baseline as well."

**含义**：以前需要"换更大模型"才能拿到的能力，现在用一个优化过的 skill 文件就能逼近。

### 跨 Harness 迁移（最反直觉的发现）

> "A spreadsheet skill trained inside Codex, dropped into Claude Code with no further optimization, lifts the no-skill baseline from 22.1 to 81.8 (+59.7) — slightly above the 80.4 achieved by training directly inside Claude Code."

**含义**：在 Codex 训练出的 spreadsheet skill，不做任何调整直接放进 Claude Code，**比直接在 Claude Code 里训练的效果还高**。这说明 SkillOpt 学到的是**通用工作流逻辑**，不是 harness 特定配方。

---

## 四、Skill 的形态：920 token、1–4 edit、人类可读

| 维度 | 数据 | 含义 |
|------|------|------|
| **中位最终长度** | ~920 tokens | 不是黑箱参数 blob，也不是无限增长的 log |
| **被接受的 edit 数** | 1–4 个 | 验证门把绝大多数 edit 挡在外面 |
| **极端例子** | OfficeQA +39.0 | **只来自一个被接受的 edit** |
| **生成规则** | "像资深工程师的建议" | 自然语言可读 |

> **笔者判断**：这个形态非常重要。SkillOpt 没有把 skill 变成另一组 RL 权重或隐式向量，而是**保留了 skill 作为人类可读 Markdown 的可审计性**。这与 Anthropic 1st-party 的 SKILL.md TRIGGER/SKIP 规则（R635）、9 分类内部 Skills 体系（R311）完全兼容——SkillOpt 优化的产物是同一类对象，只是演化机制从"人手改"升级为"训练循环改"。

---

## 五、组件消融证明 controls 在做事

| 消融项 | 效果 |
|--------|------|
| 移除 rejected-edit buffer | 三个消融基准分数全部下降 |
| 移除 meta skill + slow update | SpreadsheetBench 从 77.5 跌到 55.0 |

这两个消融说明了 SkillOpt 的核心不是"再加一个 prompt 优化器"那么简单——**控制结构本身就是价值**。这与 R622 Anthropic Autonomous Delivery Harness 的"background agent 收尾"机制、R635 claude-api Skill 的 TRIGGER/SKIP 规则一脉相承：**没有 guardrails 的 harness 不是 harness**。

---

## 六、与仓库既有 Skills 主题文章的关系

| 既有文章 | 与 SkillOpt 的关系 |
|---------|------------------|
| R311 [Anthropic 9 分类内部 Skills taxonomy](./anthropic-9-categories-internal-skills-taxonomy-2026.md) | 9 分类是"skill 是什么"，SkillOpt 是"skill 怎么演化"——互补 |
| R635 [Anthropic claude-api Skill 1st-party](./anthropic-claude-api-skill-ecosystem-ide-bundling-2026.md) | claude-api Skill 定义了 TRIGGER/SKIP 规则元数据，SkillOpt 给了这些规则一个"训练式"的演化机制 |
| R636 [Anthropic steering 7 methods decision framework](./../tool-use/anthropic-claude-code-steering-7-methods-decision-framework-2026.md) | steering 框架说"谁拥有 CLAUDE.md"，SkillOpt 回答"skill 的演化责任在谁"——同一个治理问题 |
| R432 [Anthropic Claude Code 5 extension points](./../deep-dives/anthropic-large-codebase-claude-code-five-extension-points-2026.md) | 5 个扩展点里 Skills 是其一，SkillOpt 让 Skills 变成可训练对象 |
| 本文 SkillOpt | **第 3 维度：skill 演化机制**——既有 9 分类（what）+ claude-api Skill（when），本文加 when-not-only：how skill gets better |

**Cluster 归位**：Layer 6 第 7 维度 `tool-use/skills-distribution`（R635 命名）扩展到 `tool-use/skill-optimization` 子维度。SkillOpt 是该子维度的 1st-party 学术锚点；NousResearch/hermes-agent-self-evolution 是 3rd-party 开源实现。

---

## 七、5 条对工程团队的启示

1. **如果你有 verifier，就值得训 skill**：SkillOpt 适用范围是"anywhere automatic evaluation or a reliable verifier exists"。在生产里有 eval 信号的团队可以直接受益。
2. **小模型 + 优化 skill ≈ 大模型**：GPT-5.4-nano 优化 skill 后能超过 GPT-5.2 无 skill baseline。**token 成本视角下，训 skill 比换模型便宜**。
3. **跨 harness 迁移成立**：在一个 harness 训的 skill 放进另一个 harness 仍然有效。意味着 skill 资产**不再被某个特定 IDE/CLI 锁定**。
4. **可读性是护城河**：920 token / 1-4 edit 的形态让 skill 保持可审计、可 diff、可回滚。**别把 skill 训成黑箱**。
5. **控制结构是价值核心**：rejected-edit buffer、validation gate、slow/meta update 缺一不可。**没有 guardrails 的 skill optimizer 必然走向 prompt drift**。

---

## 八、3 个标题备选（全部 ≤ 30 单位）

1. **SkillOpt：Agent Skill 的训练式演化**（14 单位）— 策略：术语锚定
2. **不动模型权重 +52 评测单元全胜的工程奇迹**（26 单位）— 策略：数据冲击
3. **从 prompt 工程到 skill 工程：920 token 跨 harness 迁移**（28 单位）— 策略：痛点共鸣

---

## 九、3 个金句

1. "Skill 真正的问题不是写什么是'谁在保证它不退化'"——本文核心判断
2. "Training need not be limited to model weights. Procedural knowledge outside the model can also be optimized." — 微软原话
3. "在没有 verifier 的领域，skill optimizer 与 prompt drift 之间的距离就是 refused-edit buffer 与 validation gate" — 笔者推论

---

## 十、引用（6 处 1st-party + 2 处核心数字）

1. [Microsoft Research Blog 原文](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/) — 1st-party 官方发布
2. [SkillOpt Paper (aka.ms/skillopt)](https://aka.ms/skillopt) — 1st-party 论文
3. [SkillOpt GitHub](https://github.com/microsoft/SkillOpt) — 1st-party 开源实现
4. "All 52 cells best or tied-best" — 1st-party 评测数据
5. "GPT-5.5 direct chat 58.8 → 82.3 (+23.5)" — 1st-party 关键数据
6. "Cross-harness transfer: 22.1 → 81.8 (+59.7)" — 1st-party 反直觉发现

---

## 十一、开放问题

**SkillOpt 假设存在 reliable verifier。但在没有 verifier 的领域（开放式对话、创作、探索性研究），如何构造"近乎 verifier"的信号？** 微软论文里没有直接回答，但这正是下一阶段 skill optimizer 能否走出 benchmark 的关键门槛。

一种可能方向：借鉴 R622 Anthropic Background Agent 的"auto-PR + 人类 review"机制——**把 PR review 当 verifier**。这恰好是 R555 Hybrid "模型擅长的事 vs 人类擅长的事"分工的延伸，但 SkillOpt 论文里没提。
