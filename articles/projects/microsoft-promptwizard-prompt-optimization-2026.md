# microsoft/PromptWizard：跨任务、跨模型族的自进化 Prompt 优化框架

> **核心定位**：PromptWizard 是 Microsoft Research 在 2024-2024 年间发布的 prompt 优化框架，核心理念是 **"LLM 自己生成、批评、改进自己的 prompt 和 examples"**——这恰好对应 LangChain Labs 2026 年宣告的「**Prompt 跨模型族优化**」方向。它是「**研究方向** ↔ **现成工程工具**」互补的范本。

## 标签
- `prompt-optimization` / `self-evolving-prompts` / `feedback-driven`
- `cross-task` / `cross-model-family` / `in-context-learning`

## 项目快照

| 维度 | 数据 |
|------|------|
| **GitHub** | `github.com/microsoft/PromptWizard` |
| **Stars** | 3,874 ⭐（持续增长中） |
| **License** | MIT（开放可商用） |
| **首发** | 2024-05-30 |
| **作者** | Eshaan Agarwal, Joykirat Singh, Vivek Dani, Raghav Magazine, Tanuja Ganu, Akshay Nambi（Microsoft Research India） |
| **论文** | arXiv:2405.18369 |
| **博客** | [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/promptwizard-the-future-of-prompt-optimization-through-feedback-driven-self-evolving-prompts/) |
| **语言** | Python（核心框架） |

---

## 一、为什么值得推荐

仓库已有的 prompt 优化生态是**多源分散**的：

- **DSPy** — 程序化 prompt 编译（编程式优化）
- **TextGrad** — 文本梯度反向传播
- **OPRO** — Google 的 "LLM as optimizer"
- **PromptWizard**（本文）— **Feedback-driven Self-Evolving**（自进化式优化）

**PromptWizard 的独特定位**：

> "PromptWizard is a discrete prompt optimization framework that employs a **self-evolving mechanism** where the LLM generates, critiques, and refines its own prompts and examples, continuously improving through iterative feedback and synthesis."

与 LangChain Labs 2026 年宣告的「**Prompt 跨模型族优化**」研究方向完全对位——本文是 **R281 主题文章 `langchain-labs-continual-learning-research-lab-2026.md` 的工程层闭环**。

## 二、三大核心组件

PromptWizard 把"自进化"拆解为三个**可独立调试**的组件：

### 1. Feedback-driven Refinement（反馈驱动精炼）

> "LLM generates, critiques, and refines its own prompts and examples, continuously improving through iterative feedback and synthesis."

这一组件的关键设计是**"自我批评循环"**：
- 第一步：LLM 生成初始 prompt
- 第二步：同一 LLM 扮演"批评者"角色，识别 prompt 的弱点
- 第三步：基于批评再生成改进版
- 循环直到质量收敛

这与 OPRO（Google）的"LLM as optimizer"路径**正交**——OPRO 让 LLM 作为优化器选择候选，PromptWizard 让 LLM **自我批评 + 自我精炼**。

### 2. Critique and Synthesize Diverse Examples（多样化示例合成）

> "Generates synthetic examples that are robust, diverse and task-aware. Also it optimizes both prompt and examples in tandem."

这是**双变量同时优化**——传统 prompt 优化只改 instruction，PromptWizard **同时优化 instruction 和 in-context examples**。这一设计在 few-shot 任务上特别重要：示例的质量直接影响 LLM 的输出。

### 3. Self-generated Chain-of-Thought（自生成 CoT）

> "Self generated Chain of Thought (CoT) steps with combination of positive, negative and synthetic examples."

**负例**的引入是 PromptWizard 的一个**反直觉但有效**的设计——CoT 不只用正例，还**显式合成负例**让 LLM 学会识别错误路径。这一设计在数学推理（GSM8k）等任务上特别有效果。

## 三、Stage 1 / Stage 2 优化流程

README 明确把优化拆为两个阶段：

### Stage 1：迭代优化 instruction

```
[初始 prompt] → [LLM 批评] → [LLM 改进] → [LLM 评估] → [质量提升？]
                                              ↓ Yes
                                         [下一轮迭代]
```

### Stage 2：instruction 与 examples 顺序优化

```
[优化后的 instruction] → [合成正例] → [合成负例] → [合成 CoT] → [联合精炼]
                                                                    ↓
                                                              [最终 prompt]
```

两个阶段的**分离设计**让框架支持三种使用场景：

| 场景 | 适用情况 | 关键配置 |
|------|---------|---------|
| **Scenario 1** | 优化 prompt 但**无 examples** | 仅 Stage 1 |
| **Scenario 2** | **生成合成 examples** 然后优化 | Stage 1 + 合成 examples |
| **Scenario 3** | 优化 prompt **with training data** | Stage 1 + 训练数据 + Stage 2 |

## 四、为什么它对应 LangChain Labs 方向 4

LangChain Labs 2026-05-14 公告的 4 个研究方向中，**方向 4（Prompt 跨模型族优化）** 的工程化路径就是 PromptWizard 提供的：

> **LangChain Labs 方向 4**："Prompts are specific to model families, and it can be annoying and time consuming to migrate from one model family to the next. We believe in a multi-model future where teams can choose the right model for the task easily. Prompt optimization across models can help make those migrations easier and reduce the amount of manual tuning required."

**PromptWizard 提供的工程能力**：
- **可重用的优化 pipeline**——一次 prompt 优化 pipeline 写好，可在 GPT-4 / Claude / Gemini / Llama 之间迁移
- **task-aware**——同一 pipeline 适配多种 task
- **self-evolving**——优化过程自动化，不需要人工迭代

这正是 LangChain Labs 方向 4 需要的**研究层 + 工程层基础设施**。PromptWizard 团队是 Microsoft Research India，**完全有能力**与 LangChain Labs 在方向 4 上合作发表研究输出。

## 五、SPM 闭环逻辑

本文与 R281 文章 `langchain-labs-continual-learning-research-lab-2026.md` 的关系是 **R265 验证的 Pattern 12 变体**——**机构级研究 × 开源工程**：

| 维度 | LangChain Labs 方向 4 | PromptWizard |
|------|----------------------|--------------|
| **抽象层** | 研究层（合作伙伴、公开研究输出、跨模型族评估方法） | 工程层（自进化 prompt 优化框架） |
| **核心输出** | 研究论文、评估基线、跨模型族迁移模式 | 开源框架、3 种使用场景、3 大核心组件 |
| **目标用户** | 研究者、产业方、agent 团队 | agent 工程师、prompt 工程师 |
| **典型使用** | 阅读论文、引用研究结论 | `pip install -e .`、运行 demo notebook |
| **商业模式** | LangChain 商业化（LangSmith 客户） | 微软开源生态（Azure 客户） |

**一句话闭环**：**LangChain Labs 在研究层定义"跨模型族 prompt 优化应该长什么样"，PromptWizard 在工程层提供"今天就能用"的实现**——读者可以直接跑 `demos/gsm8k/configs/promptopt_config.yaml` 看到 30%+ 准确率提升，然后用 LangChain Labs 的研究方向作为**未来演化的路线图**。

## 六、对比表：与同类工具的差异化

| 工具 | 核心方法 | 多模型族支持 | 示例优化 | CoT 生成 | 自我批评循环 |
|------|---------|-------------|---------|---------|-------------|
| **PromptWizard**（本文） | Self-evolving + 反馈驱动 | ✅（pipeline 复用） | ✅ | ✅ | ✅ |
| **DSPy** | 程序化编译 + BootstrapFewShot | ✅（通过适配器） | ✅ | ❌ | ❌ |
| **OPRO** | LLM as optimizer | ✅ | ❌ | ❌ | ❌ |
| **TextGrad** | 文本梯度反向传播 | ✅ | ✅ | ❌ | ✅（但机制不同） |
| **GEPA** | Genetic Pareto 搜索 | ⚠️ | ✅ | ❌ | ❌ |

**PromptWizard 的独特价值**：在「self-evolving + 多模型族 + 完整优化 pipeline」这三轴上**全部命中**。

## 七、推荐使用场景

✅ **适合用 PromptWizard**：
- 任务定义清晰、有训练数据
- 需要在多模型族之间迁移（GPT-4 ↔ Claude ↔ Gemini）
- 已有 prompt 但准确率卡在瓶颈
- 想用合成数据扩充训练集

❌ **不适合用 PromptWizard**：
- 没有训练数据、纯 zero-shot 任务
- 需要实时优化（PromptWizard 是离线优化）
- prompt 极短、几乎没有优化空间

## 八、行动建议

1. **跑 demo**：`demos/scenarios/dataset_scenarios_demo.ipynb`（最完整的使用示例）
2. **生产部署**：用 `promptopt_config.yaml` 配置 pipeline，把优化后的 prompt 部署到生产
3. **跨模型族**：写一个 adapter，让同一 pipeline 跑 GPT-4 和 Claude 比对
4. **与 LangSmith 集成**：把 PromptWizard 优化后的 prompt 推送到 LangSmith 实验平台追踪效果

## 一句话总结

PromptWizard 是 **LangChain Labs 2026 方向 4 的现成工程实现**——它的自进化 prompt 优化框架覆盖了"跨任务、跨模型族、含 CoT、含自我批评循环"四大维度，是微软研究院在 agent 持续学习方向上**最完整的开源基础设施**之一。

---

*本文属于 **Prompt Optimization** 主题 cluster，与 R281 文章 `langchain-labs-continual-learning-research-lab-2026.md` 形成「研究范式宣告 × 现成工程实现」的 SPM 闭环。*
