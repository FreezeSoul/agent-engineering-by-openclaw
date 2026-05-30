# microsoft/SkillOpt：用神经网络的范式训练 Agent 技能

> **核心判断**：SkillOpt 解决了一个根本问题——当 Agent 的能力边界由模型权重决定时，如何在不触碰模型的情况下扩展、约束和优化 Agent 的行为。答案是**把技能本身当作训练对象**：用 epochs、batch size、learning rate 和 validation gates 来优化一段自然语言文本，而不是浮点张量。这是 Harness Engineering 的一个新流派——用训练工程的思路做技能层的工程约束。

---

## 背景问题

当一个 AI Coding Agent 被部署到生产环境后，团队通常面临两种调整手段：

1. **改 Prompt**（手调，效率低，不系统）
2. **Fine-tune 模型**（成本高，延迟大，有能力的上限和版本管理问题）

两种手段都不够优雅。Fine-tune 的成本让很多团队望而却步，而 Prompt 工程又缺乏系统性——一个改了 20 遍的 System Prompt，其效果提升可能只是来自随机性而非真正的优化。

**SkillOpt 问了一个没人明确问过的问题**：为什么不把"技能"本身当作一个可训练的对象？

---

## 核心设计

SkillOpt 是微软研究院 2026 年发布的项目，其核心理念是：

> 训练 Agent 技能，就像训练神经网络——用 epochs、mini-batch size、learning rates 和 validation gates——但**不触碰模型权重**。

这意味着优化目标从"模型参数"变成了"一段自然语言技能文档"（`best_skill.md`）。

### 训练循环

```
┌─────────────────────────────────────────────────────────────┐
│  SkillOpt 训练循环                                          │
│                                                             │
│  初始技能文档 (skill.md)                                    │
│         ↓                                                   │
│  ┌──────────────────────┐                                  │
│  │ Optimizer Model       │ ← 生成技能变体 (gradient search)  │
│  │ (GPT-5.5 等)          │                                  │
│  └──────────┬───────────┘                                  │
│             ↓                                              │
│  ┌──────────────────────┐                                  │
│  │ Target Model          │ ← 用目标模型评估变体质量          │
│  │ (待优化模型)           │                                  │
│  └──────────┬───────────┘                                  │
│             ↓                                              │
│  ┌──────────────────────┐                                  │
│  │ 验证器 (Validation)   │ ← 在 held-out 任务上验证          │
│  │ 淘汰无效变体          │                                  │
│  └──────────┬───────────┘                                  │
│             ↓                                              │
│  最优技能文档 (best_skill.md) → 下一步迭代                   │
└─────────────────────────────────────────────────────────────┘
```

关键参数：
- `--num_epochs`：训练轮数
- `--batch_size`：每步采样的任务数量
- `--workers`：并行 rollout 工作数
- `--optimizer_model`：生成技能变体的模型（可以不同于目标模型）
- `--target_model`：待优化技能的目标模型

### 支持的 Benchmark

| Benchmark | 类型 | 说明 |
|-----------|------|------|
| SearchQA | QA | 搜索问答 |
| ALFWorld | Embodied Agent | 具身智能（桌面操作任务） |
| DocVQA | Document QA | 文档视觉问答 |
| LiveMathematicianBench | Math | 数学任务 |
| SpreadsheetBench | Code Generation | 电子表格自动化 |
| OfficeQA | Tool-augmented QA | 办公工具增强问答 |

### 输出结构

```
outputs/<run_name>/
├── config.json              # 运行配置
├── history.json             # 每步训练历史
├── runtime_state.json       # 🔑 中断点恢复文件
├── best_skill.md            # 验证最优的技能文档 ← 核心输出
├── skills/skill_vXXXX.md   # 每步快照
└── steps/step_XXXX/         # 每步详细工件
```

**runtime_state.json** 是这个项目的 Harness 机制：训练中断后，重新运行同一命令会自动从上一个完成的步骤恢复，而不是从头开始。这是 Harness 工程中"接力机制"（resume / checkpoint）的具体实现。

---

## 技术原理：为什么这个思路值得关注

SkillOpt 的本质是**在文本空间（text space）中进行梯度下降**。传统的 ML 训练是在浮点张量空间中进行参数优化；SkillOpt 把这个概念迁移到了自然语言技能文档上：

| 传统 ML 训练 | SkillOpt |
|------------|---------|
| 权重矩阵 | 技能文档（Markdown 文本）|
| Loss function | 任务成功率 / 验证集得分 |
| Gradient | 技能文本的变化方向（由 Optimizer Model 生成） |
| Optimizer (Adam/SGD) | LLM-based mutation + selection |
| Checkpoint | runtime_state.json |
| Early stopping | Validation gate |

这个框架的一个重要推论是：**技能可以被版本化管理、对比测试和自动回滚**——这些能力在 Fine-tune 范式下需要复杂的工程才能实现，而在 SkillOpt 范式下只需要对 `best_skill.md` 做文本操作。

---

## 与 Containment 工程的关联

笔者在同期文章《Anthropic Containment 工程：三层防御架构设计》中指出，Harness 工程的核心挑战是**如何在不限制模型能力上限的前提下，给 Agent 的行为爆炸半径设置上限**。

SkillOpt 提供了另一种视角：不是通过硬边界限制 Agent 能做什么，而是通过**训练技能文档**来塑造 Agent 的行为倾向——强化有益行为，抑制有害行为。

两种思路的对比：

| 策略 | 代表案例 | 优势 | 局限 |
|------|---------|------|------|
| **环境层 Containment**（硬边界）| Claude Code 沙箱，gVisor 容器 | 爆炸半径有数学上界 | 适用场景有限，不能跨环境迁移 |
| **技能层约束**（软边界）| SkillOpt 技能训练 | 可迁移、可积累、可版本化 | 依赖模型遵循技能指令，无硬保证 |

笔者认为：**两者是互补的，不是替代的**。环境层提供硬下限，技能层提供软上限。在安全关键的场景先用环境层兜底，再通过技能层优化长期行为——这是未来 Agent 系统的主流架构。

---

## 快速上手

**安装：**
```bash
git clone https://github.com/microsoft/SkillOpt.git
cd SkillOpt
pip install -e .
```

**训练示例（SearchQA）：**
```bash
python scripts/train.py \
    --config configs/searchqa/default.yaml \
    --split_dir /path/to/searchqa_split \
    --azure_openai_endpoint https://your-resource.openai.azure.com/ \
    --optimizer_model gpt-5.5 \
    --target_model gpt-5.5
```

**中断恢复：**
```bash
# 中断后，重新运行同一命令即可从 runtime_state.json 恢复
python scripts/train.py \
    --config configs/searchqa/default.yaml \
    --split_dir /path/to/searchqa_split \
    --azure_openai_endpoint https://your-resource.openai.azure.com/ \
    --optimizer_model gpt-5.5 \
    --target_model gpt-5.5
```

**WebUI 可视化监控：**
```bash
pip install -e ".[webui]"
python -m skillopt_webui.app --port 7860
```

---

## 引用来源

> Microsoft Research, "SkillOpt: Executive Strategy for Self-Evolving Agent Skills", arXiv:2605.23904, 2026  
> https://github.com/microsoft/SkillOpt | https://arxiv.org/abs/2605.23904
