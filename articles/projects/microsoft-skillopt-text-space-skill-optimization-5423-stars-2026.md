# microsoft/SkillOpt：用文本空间优化训练 Agent 技能

> "Train agent skills like you train neural networks — with epochs, (mini-)batchsize, learning rates, and validation gates — but without touching model weights."

## 核心命题

SkillOpt 解决了一个长期困扰 Agent 开发的问题：**Skill 文档是手写的、不稳定的、无法保证持续提升的**。

笔者的判断：**这是 Agent Skill 工程的范式转变——从手工 crafting 到可训练的技能工件**。

![GitHub](screenshots/microsoft-skillopt-5423-stars-2026.png)

## 为什么这个项目值得关注

### 核心创新：Text-Space 优化

传统 Agent 开发中，Skill（提示、技能描述、工具使用规范）都是手工编写或一次性生成的。SkillOpt 的核心洞察是：**把 Skill 文档当作可训练的状态，用优化器模型对它进行梯度式的增删改**。

工作流程：

```
Rollout → Reflect → Aggregate → Select → Update → Evaluate
   ↑                                            │
   └──────────── validation gate ────────────────┘
```

**关键约束**：
- 优化器模型生成有界的 add/delete/replace 编辑
- 只有在 held-out validation score 严格提升时才接受编辑
- 部署时零推理时模型调用（skill 文档在运行时是静态的）

### 惊人的效果数据

在 **6 个 benchmark、7 个目标模型、3 个执行 harness**（direct chat、Codex CLI、Claude Code CLI）上：

- **GPT-5.5** 提升：+23.5 points（direct chat）、+24.8（Codex agentic loop）、+19.1（Claude Code）
- **52 个评估 cell 全部达到最佳或并列最佳**

更重要的是：**优化后的 skill 可以在不同模型规模间转移，在 Codex 和 Claude Code harness 间转移**，无需进一步优化。

### 工程实现亮点

**零推理时开销**：训练时的优化器模型不参与部署，best_skill.md（通常 300-2000 tokens）直接作用在目标模型上。

**多后端支持**：OpenAI / Azure / Claude / Qwen / MiniMax 开箱即用。

**6 个内置 benchmark**：覆盖 ALFWorld、WebShop 等标准评估环境。

**WebUI Dashboard**：Gradio 监控界面，实时观察训练曲线。

## 技术原理

SkillOpt 将神经网络的优化 discipline 应用于文本状态空间：

| 概念 | 神经网络 | SkillOpt |
|------|---------|----------|
| 可训练状态 | 权重矩阵 | Skill 文档 |
| 优化器 | SGD/Adam | LLM（optimizer model）|
| 梯度 | 权重更新 | 有界编辑（add/delete/replace）|
| Validation | Val loss | Held-out benchmark score |
| 学习率 | LR hyperparameter | Textual LR budget |
| 正则化 | Weight decay | Rejected-edit buffer |

## 笔者的判断

**SkillOpt 填补了一个重要的工程空白**：社区有大量关于"如何写好 prompt"和"如何用 LLM 生成 prompt"的研究，但缺少系统性的**技能工件优化**方法。

笔者认为，SkillOpt 的长期影响可能比肩超参数优化对深度学习的意义：**把人工调优的过程变成可自动化、可复现的系统性过程**。

适用场景：
- 需要在不同模型上部署相同技能的工作流
- 技能性能需要持续提升而非一次性优化
- 多模型/多 harness 的统一技能管理

不适用场景：
- 运行时动态调整的技能（SkillOpt 的 skill 是静态的）
- 资源受限环境（训练需要优化器模型调用）

---

**引用来源**：

- [SkillOpt GitHub README](https://github.com/microsoft/SkillOpt)
- [SkillOpt Paper: arXiv/2605.23904](https://arxiv.org/abs/2605.23904)
