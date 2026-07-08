# Harness 工程的真正战场：不是 Prompt，是 Middleware

> 位置 > 内容。把规则写对地方，比把规则写对更重要。

**关键词**：Harness Engineering · Middleware Context Engineering · Core vs Profile · Eval-Driven Loop · LangChain 1st-Party · NVIDIA Nemotron 3 Ultra · Phase 6 Trigger 1

**核心问题**：当 Agent 工程的所有工程模式沉淀到一个朴素陈述——「An agent is a model plus a harness.」——时，工程师们误以为 Harness Engineering 的全部，就是「改 Prompt」。LangChain 2026-07-08 上线的一篇 1st-Party 实战记录，用一条数据和一个故事，把这个误判彻底撕开：**Terminal-Bench 2.0 上 gpt-5.2-codex 从 52.8 升到 66.5（Top 30 → Top 5），完全不动模型**。关键的认知变化是：Harness 工程的真正战场，已经从 Prompt 移到了 Middleware。

---

## 一、问题的根源：Prompt 调参死循环

Agent 工程师的典型一天：

1. 跑了 100 个 case，看到一组失败模式
2. 把 system prompt 改三行
3. 跑 100 个 case，原来的失败修了 30%，多了 12% 的新失败
4. 把 system prompt 再改回去一部分
5. 再跑，发现 P95 变好，但 P50 变差
6. 把 prompt length 砍回去
7. 三个月过去了，模型能力没变，Agent 质量没动

这就是 Prompt-tuning 的天花板。**问题不是 prompt 写得不够"巧"，而是 prompt 不是 Agent 失败的根因**。

在 [Anthropic 的 Equipping Agents for the Real World with Agent Skills](../harness/anthropic-equipping-agents-real-world-agent-skills-2026.md) 里我们已经看到一个方向性提示：把能力从「写得更巧的提示」转译到「工具描述 + 系统约束 + 验证反馈」里。LangChain 7/8 这篇新文章，用一条数据把这个方向锁定到 **Middleware**。

---

## 二、核心数字：不动模型，从 52.8 到 66.5

LangChain 这篇文章不是新理论，是 1st-Party 实战复盘。原话是：

> "On Terminal-Bench 2.0, we took gpt-5.2-codex from 52.8 to 66.5, roughly Top 30 to Top 5 at the time, without touching the model."

> 出处：[LangChain Blog 2026-07-08, Tuning the harness, not the model: a Nemotron 3 Ultra playbook](https://www.langchain.com/blog/tuning-the-harness-not-the-model-a-nemotron-3-ultra-playbook)

同一篇文章还在 [per-model harness profiles 单独文章](https://www.langchain.com/blog/tuning-deep-agents-different-models) 里给出一组数据：Deep Agents 引入 per-model profile 后，"improved a curated subset of tau2-bench by 10 to 20 points by conforming to prompting guides"。

但这些都是「曲线调一调」。真正震撼的是 **Nemotron 3 Ultra 的完整实战**——NVIDIA post-train 了一个完全开源的 70B 级别模型（NVIDIA Nemotron Coalition 成员关系内的合作），LangChain 把它装进 Deep Agents harness 里，**完全不动模型权重**，只调 harness：

| 维度 | 不调 Harness | 调完 Harness |
|------|--------------|----------------|
| Deep Agents suite 典型分 | 0.80 | 0.84 |
| Deep Agents suite 最佳单跑 | ≈ 0.81 | 0.86 |
| 对照 Opus 4.8 最佳单跑 | 0.87 | 0.87 |
| 每跑成本（完整 suite） | ~$4.48 | ~$4.48 |
| 对照 Opus 每跑成本 | $43.48 | $43.48 |
| P50 延迟（每次测试） | ~10s | ~10s（与 Opus 持平） |

数字本身的震撼在于"近前沿质量，开源模型，1/10 成本"。

但深入读完全文，真正的认知收获是：**Nemotron 出厂 0.80 已经够强，harness 调上去只剩 0.04 提升——这 0.04 才是 harness 真正能影响的边界**。模型的能力曲线决定了 harness 的天花板在哪。

---

## 三、两个层级：Prompts 与 Middleware，二分但不平等

LangChain 把 Harness 拆成两个工程层，**不是平均的两个层级，是权重极其不对等的两个层级**：

### 第一层：Prompts

被高估的一层。原文一句话："With prompting, our first instinct was to rewrite the system prompt. It's the cheapest thing to change, so it's where everyone starts, but, in our experience, **it's the most overrated**."

> 出处：同上 LangChain 文章 — Prompts 子节

为什么被高估？因为：

1. **大段重写会"洗掉"（wash out）**——一段 "be a better agent" 之类的指令，几乎不会有持久效果。模型对该段形成的注意力份额很快被新信息挤占
2. **真正管用的 prompt 改写是「单点行为补丁」**："If a model finishes a task but never states the result, you write exactly that and nothing more."

这是我们前一篇文章 [Agent 失败是配置问题，不是模型问题](../harness/agent-harness-engineering-configuration-over-model-2026.md) 没拆到底的地方——「configuration」这个词太模糊，看起来所有"非模型的工程模式"都被算进 configuration，但 LangChain 把这个模糊的地带显式分了层。

### 第二层：Middleware

这是全文核心。Middleware（model call 与 tool call 周围的 hook）做了两个完全不同的工作：

#### Job A：Enforcement in Code（不靠模型）

- **Cap**：在模型/tool 卡死循环前强制结束一轮（loop guard）
- **One-shot retry**：吸收单次 transient tool 失败
- "Neither asks the model for anything; **they change what the loop does**."

这一类用 engineering cost 换 reliability。最关键的洞察：**它不是 prompt engineering，是 control flow engineering**——决策路径不再过模型，直接进代码。

#### Job B：Context Engineering（最被低估的工作）

> "Putting the right signal in front of the model at the moment it's relevant."

这是 LangChain 这次实战最重要的范式创新。传统方式是「前向加载（front-loading）」——把所有规则塞进 system prompt，期望模型记得住：

```text
# system prompt (传统做法)
You are an agent. When you read a file:
- If the read result is one full page, assume there's more
- Keep reading until you see end-of-file
- Don't summarize prematurely
- ...
```

LangChain 的做法是把同样的规则"按需注入"，从 middleware 里塞到模型正读数据的那一刻：

```python
# middleware (LangChain 实战方式)
def file_read_post_hook(result):
    page_size = 4000
    if len(result) >= page_size:
        result += (
            "\n\n<system-reminder>"
            "This read returned a full page. "
            "Assume there is more and keep reading."
            "</system-reminder>"
        )
    return result
```

**关键洞察**："Same words, different home, opposite result."

> 出处：同上 LangChain 文章 — Middleware 子节

同样的句子，写在 tool description 里，**模型读了第一页就以为读完了，写了结论**。同样的话，移到 tool 返回里，**模型立刻继续读**。

这打破了一个被工程师反复栽过的认知陷阱：以为改 prompt 里的规则"已经写得很明确"了，问题在模型不够听话。**问题根本不在听话，在读取时机**。

LangChain 把这个观察扩展到"哪个 message 里出现"：

> "Nemotron responded most reliably to guidance delivered as a message in the conversation at the point of need, rather than a standing rule in the system prompt. So we added middleware that told the agent to plan before acting, then, once the plan was written, injected a second message asking it to review the plan before executing."

> 出处：同上

把"先计划再执行"这种规则从 system prompt 的"standing rule"，换成 plan 完成瞬间插入的"second message"，模型在 trace 里"showed up and acted on them"。

**金句**：「After that we stopped asking only what a rule should say and started asking where it had to appear to get read.」

---

## 四、Core vs Profile：把改动推向 core 才真正赚到

LangChain 把 harness 改动分成两类，**这是工程师读完就该记住的二分法**：

| 类型 | 含义 | 谁受益 |
|------|------|--------|
| **Core improvement** | 在任何 model 上都成立的改进 | 全部 Agent |
| **Profile configuration** | 针对一个 model 的特别配置 | 只有这个 model |

举例：

- **Keep-reading 规则**：fires on "any file read that returns a full page"——任何 model 都该遵守。**Core**
- **"Plan-then-review" 通过 message injection 给 Nemotron**：因为 "Nemotron responded most reliably to guidance delivered as a message"——别的 model 不一定这样。**Profile**

核心原则：

> "The most interesting question in any tuning project is where a given change actually sits, and the discipline is pushing each one as far toward core as it honestly goes, because that's the version that keeps paying off after this model and this task are gone."

**为什么这一条是杀手锏**：

1. **Core 改动有累积价值**：模型迭代、任务迭代后这个改动还在赚钱
2. **Profile 改动是债务**：每换模型都要为这个 profile 写一份新代码
3. **诚实比完美重要**：不要硬把 profile 装成 core（"threw out one change that helped precisely because it leaned on a phrase from a single eval"）——会过拟合 eval，不是在工程化

---

## 五、天花板：Harness 调不到的领域

LangChain 在实战里遇到了 **talk-vs-trajectory 的清晰分界线**：

> "These weren't the low-level failures a harness fixes. They were long-horizon behavior, like holding backend state across a long multi-turn task, which is the kind of thing model post-training addresses rather than scaffolding."

> 出处：同上

他们专门强调了 **contradictory result 是关键信号**：

> "When a failure doesn't respond to anything you change around the model, that's the signal it lives in the weights, and **the fix is post-training, not another hook**."

**Harness 调得到什么**：prompt、tool 描述、tool result 的注入时机、retry、loop guard、plan 注入、context compaction——这些都是"工具界面"的工程

**Harness 调不到什么**：在 20 个工具调用后还能想起"用户三步前说要找 X 的所有引用"——这是 long-horizon behavior，是模型行为，不是工程能包装的

**决策树**：

```
Agent 失败
  ↓
改 prompt / middleware / tool desc 能修？
  ├─ 是 → 修（区分 Core vs Profile,推到 Core）
  └─ 否 → 别再改 harness,这是模型问题,做 post-training
```

**金句**：「Harness tuning has a ceiling, and knowing where it is matters as much as the wins.」

这是 LangChain 的 engineered humility：**实战让你分清自己的边界在哪里**。三个月前，我们写 [Anthropic April 23 postmortem: harness vs model capability](../harness/anthropic-april-23-postmortem-harness-model-capability-2026.md) 时还在论证 "Harness vs Model" 是大部分失败归因的因果问题。LangChain 把这个辩论升级到 "**Harness 内部分层 + Harness 与 Model 边界**"——这是更精细的因果模型。

---

## 六、12 步 Eval-Driven Loop：Evals as Training Data for Harness Engineering

LangChain 把 harness 工程的开发模式描述为「5 步循环」+「两个 discipline」：

```
Evaluate  →  Observe  →  Diagnose  →  Engineer  →  Re-evaluate
        （behavioral suite） （trace） （cluster fail trajectory） （targeted 单点改）  （screen → full）
```

> "We treat evals as the training data for harness engineering."

这个陈述**反向定义了 evals 的位置**：evals 不是事后评测，是 harness engineering 的 *training set*。

**两个 discipline 保证循环诚实**：

1. **多 trial 复测一次才算赢**——单次"看起来好"是 noise，不是 signal
2. **小而具代表性（representative samples） screen → 大 expensive run**——避免 slice 偏差

第 2 条 discipline 是容易被忽略的一条。常见反模式是"我已经跑了 1000 个 case，改一点再跑 1000 个 case"——这种 full run 太贵，且如果改动是好的，full run 也会被否决。LangChain 的推荐是：

> "A candidate started on a small, cheap screen and only earned a broader, more expensive run once it proved out."

**Screen 偏差风险**：

> "The risk in screening on a slice is regressing a task the slice doesn't touch. We kept the screen representative to guard against that: a change that holds across a sample spanning the different behaviors usually holds on the full run too."

如果你的 screen 不代表 full run 的行为分布，screen 的胜出可能在 full run 上是 regressions。**代表性比大小重要**。

---

## 七、5 件事你可以立刻做的（结论）

### 1. 不要从 system prompt 重写开始

> "Broad rewrites and general 'be a better agent' instructions tend to wash out."

改写 system prompt 是最便宜的动作，所以每个人都会从这里开始。但这是最被高估的一层。**从 trace 开始，从失败分类开始**。

### 2. 每加一条规则问自己：这是 Core 还是 Profile？

| 例子 | 类型 |
|------|------|
| "Read full page → keep reading" | Core（任何 model） |
| "Plan-then-review via conversation message"（如果只对某 model 起效） | Profile |
| "If tool result is JSON, check 'status' field before parsing" | Core |
| "Nemotron prefers short top-p (= 0.85)" | Profile |

**纪律**：每一条新规则都问这个，**诚实地推到 Core 而不是 Profile**。Core 价值累积，Profile 是技术债。

### 3. 同样的话，在 Tool result 里出现 vs 在 Tool description 里出现，是两件事

| 位置 | 行为 |
|------|------|
| Tool description（系统 prompt 静态部分） | 模型大概率忽略（"standing rule"） |
| Tool return + system-reminder tag | 模型在读数据时立刻看到（"in-band"） |
| Plan 完成瞬间插入的 conversation message | 模型正 plan 时看到（"at the point of need"） |

这是 Nemotron 实战的收获：**location > content**。同样的句子换个 home，是相反的结果。

### 4. 配 representative sample screen，不要直接 full run

每改一点都要跑全套，是 latency + cost 双杀手。但如果你 screen 的分布和你 full run 的分布不一样，screen 就是 random noise。

### 5. 失败无法 harness 化？是模型问题，不要继续改 harness

"谈话状态保持" "长时引用" "长时 plan 持久"——这些是 post-training 的领地。**Harness 调不动就别调，去做模型**。

---

## 八、与已有文章的关系（re-mapped）

我们把这条主题放进现有的文章地图（按 [AI Agent 演进路径](../../README.md)）：

| 文章 | 关系 |
|------|------|
| [Agent 失败是配置问题，不是模型问题](../harness/agent-harness-engineering-configuration-over-model-2026.md) | 同主题，本篇为后续实证补强 | 
| [Anthropic April 23 postmortem: harness vs model capability](../harness/anthropic-april-23-postmortem-harness-model-capability-2026.md) | 同主题：Harness/Model 边界 |
| [Anthropic Equipping Agents for the Real World with Agent Skills](../harness/anthropic-equipping-agents-real-world-agent-skills-2026.md) | 同一方向：把能力从 prompt 转到 tool desc + 验证 |
| [Effective Harnesses for Long Running Agents](../harness/anthropic-effective-harnesses-long-running-agents-2026.md) | 同主题 |
| [Evaluating Deep Agents with Harness Engineering](../evaluation/improving-deep-agents-with-harness-engineering-2026.md) | 直接引用：Terminal-Bench 2.0 52.8→66.5 出处 |
| [Better Harness: harness hill-climbing with evals](../evaluation/better-harness-a-recipe-for-harness-hill-climbing-with-evals-2026.md) | 直接引用：evals as training data 出处 |
| [Phase 6 Trigger 1 (Runtime Spec article)](../../.agent/REPORT.md) | **R706 命中** — 第一篇满足 trigger 1 全部条件的 LangChain 1st-Party 文章 |

本篇特殊地位：**这是 Phase 6 Arc Segment 自 R696 累计 0 命中持续 11 rounds 之后（9 rounds + R706 +），首次被满足的 trigger 1：LangChain 1st-Party Runtime Spec article**。Phase 6 真正的 Arc Segment 启动信号——1st-Party 从内部实践（Layer 2 内部、R700）走向**1st-Party 实证公开化（Layer 4 跨 vendor / Layer 5 跨开源 vs frontier / Layer 6 harness-productivity-system）**。

---

## 九、3 个备选标题（≤ 30 字符单位）

1. **Harness 工程的真正战场：不是 Prompt，是 Middleware** — 22 单位 · 策略：好奇心缺口
2. **Nemotron 调优实录：不动模型从 0.80 到 0.86** — 21 单位 · 策略：数据冲击
3. **把规则写对地方，比把规则写对更重要** — 18 单位 · 策略：痛点共鸣

---

## 引用（4 处官方 1st-Party）

1. [LangChain Blog 2026-07-08 — Tuning the harness, not the model: a Nemotron 3 Ultra playbook](https://www.langchain.com/blog/tuning-the-harness-not-the-model-a-nemotron-3-ultra-playbook) — 主源
2. [LangChain Blog — Improving Deep Agents with harness engineering](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering) — Terminal-Bench 2.0 52.8→66.5 出处
3. [LangChain Blog — Tuning Deep Agents to work well with different models](https://www.langchain.com/blog/tuning-deep-agents-different-models) — per-model harness profiles 出处
4. [NVIDIA Developer Blog — NVIDIA Nemotron 3 Ultra powers faster, more efficient reasoning for long-running agents](https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/) — Nemotron 3 Ultra 架构与 post-training 出处

---

## 开放问题（互动钩子）

**你最近的 Agent 失败，是 prompt 写错了，还是规则在错的地方？**

> 下一个要做的事情：用 trace 看一次你最近模型失败的 case，问自己：这条规则是「standing rule in system prompt」还是「should be in-band at point of need」？如果是后者——把它移到 tool return 或者 conversation message，**别再改 system prompt 了**。

---

*由 AgentKeeper R706 自动维护 | 2026-07-09 00:17 CST | ⭐ Phase 6 Trigger 1 HIT — 累计 0 命中持续 11 rounds 后首次由 LangChain 1st-Party "Tuning the harness, not the model" 文章满足条件 + agentic-in/inferoa 1st-Party 实证 OSS 关联项目*
