# SakanaAI/AI-Scientist：自动化科研闭环平台（14K Stars）

> Sakana AI 发布的 AI Scientist 是目前**最接近「全自动科学发现」的开源实现**——从 idea generation、实验设计、代码实现、到论文撰写，LLM 全程自主完成。本文分析其工程实现与 evaluator loop 设计，并标注 License 风险。

## 核心数据

| 维度 | 数值 |
|------|------|
| Stars | 14,082 |
| License | **The AI Scientist Source Code License v1.0**（自定义，基于 Responsible AI Source License v1.1） |
| 维护方 | Sakana AI（东京，2023 年成立，Daniel Foote 团队） |
| 首次发布 | 2024-08（v1 论文 arXiv 2408.06292） |
| 核心能力 | idea generation → experiment design → code implementation → paper writing → peer-review simulation |

## ⚠️ License 风险提示（必读）

这不是标准 OSI License，是 Sakana AI 自定义的「责任 AI 协议」。**关键限制**：

- **3.2e "The AI Scientist Clause"**：禁止**未声明 AI 生成**地发布科研论文
- **3.2a Surveillance 限制**：禁止基于受保护属性（种族、性别、宗教等）的推断
- **3.2b Deepfake 限制**：禁止生成未标注的逼真人物/事件内容
- **3.2c Healthcare 限制**：禁止无人工监督的医疗诊断
- **3.2d Criminal Justice 限制**：禁止犯罪预测

**对读者的影响**：
- ✅ **可读、可学习、可作为 reference 引用**（仓库本身是公开的）
- ⚠️ **不可直接 fork 用于自动化生产科研论文**（除非包含机器生成声明）
- ⚠️ **不可用于上述受限制的场景**

**R529 决策依据**：项目作为**「evaluator loop 在科学发现中的工程实践」**被推荐——这是评论性引用，**不构成 license 授权的二次分发**。读者若想 fork 使用，需自行阅读完整 LICENSE 条款。

## 工程实现：evaluator loop 的完整闭环

AI Scientist 的核心是**端到端的多阶段 evaluator loop**，与 Chi-kwan Chan × Codex 的人机协作形成「工业实现 vs 个人实践」的对照：

### 阶段 1：Idea Generation（生成器）
LLM 根据种子主题生成多个研究方向，输出"novelty score"和"feasibility score"。

### 阶段 2：Experiment Design + Code Implementation
LLM 自主编写实验脚本，支持 NanoGPT / 2D Diffusion / Grokking 三种模板（持续扩展）。

### 阶段 3：Result Analysis（验证器 1）
LLM 分析实验输出，识别异常与趋势。

### 阶段 4：Paper Writing
LLM 撰写完整 LaTeX 论文，含 abstract / introduction / methods / results / discussion / references。

### 阶段 5：Reviewer Simulation（验证器 2）
**关键创新**：另一个 LLM 扮演 reviewer，对生成的论文进行评分（soundness / presentation / contribution），决定是否"接受"。

```
[LLM Generator] → Idea → Code → Results → Paper
                                          ↓
                       [LLM Reviewer] ←─┘
                              ↓
                    accept / reject / revise
```

## 与 Chi-kwan Chan × Codex 的对照

| 维度 | Chi-kwan Chan × Codex (用户实践层) | SakanaAI/AI-Scientist (工业化) |
|------|-----------------------------------|-------------------------------|
| **生成器** | Codex（GPT 系列） | Claude / GPT-4（可切换） |
| **验证器** | 人类科学家（物理学家本人） | LLM Reviewer + 模拟 peer review |
| **反馈粒度** | 算法级别的物理一致性 | 论文级别的 novelty / soundness |
| **失败容忍** | 高（"大多数想法会失败"） | 高（多 idea 并行筛选） |
| **可重复性** | 取决于人 | 标准化实验模板 |
| **输出物** | 候选算法（待人工实现） | 完整论文 + LaTeX 源码 |

**核心洞察**：两者都遵循 evaluator loop 范式，但**人类专家 vs LLM Reviewer** 的替换让**工程成本从稀缺的人力变成可扩展的 token 消耗**——这是 AI Agent 工业化最值得借鉴的设计选择。

## 对 Agent 工程的启示

### 1. 标准化实验模板是规模化的前提
AI Scientist 的三种模板（NanoGPT / 2D Diffusion / Grokking）覆盖了 ML 研究最常见的实验范式。**给 Agent 标准化实验骨架**，才能让 LLM 在其中自由发挥。

### 2. 多 idea 并行筛选比单 idea 优化更高效
AI Scientist 一次生成 ~50 个 idea 并行筛选（per template / base model 组合）。这种"宽进严出"的策略比"精雕细琢一个 idea"更适合发现类任务。

### 3. Reviewer 模拟是把"开放任务"变成"评估任务"的关键
科研写作本质是开放任务，但通过 LLM Reviewer 评分变成了**有明确通过标准的评估任务**——这让 evaluator loop 真正能运行起来。

### 4. License 设计本身就是一种"护栏"
SakanaAI 选择自定义 license（明确禁止未声明生成），是给工业级 AI Agent 设置**责任边界**的早期探索。这种设计对**高风险 Agent 应用**（医疗 / 法律 / 科研）有借鉴意义。

## 适用场景

- ✅ **参考实现**：学习如何把 evaluator loop 应用到开放性任务
- ✅ **研究 Agent 教学**：展示从生成到评审的完整流水线
- ✅ **失败案例研究**：仓库 README 警告"会执行 LLM 写的代码"，是研究 Agent 失控风险的典型案例
- ❌ **生产环境部署**：License + 安全风险不适合
- ❌ **学术不端场景**：3.2e 条款明确禁止

## 参考来源

- GitHub: [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist)（14,082 ⭐, 2026-06-25）
- Paper: [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](https://arxiv.org/abs/2408.06292)
- Blog: [Sakana AI Blog - The AI Scientist](https://sakana.ai/ai-scientist/)
- License: [The AI Scientist Source Code License v1.0](https://github.com/SakanaAI/AI-Scientist/blob/main/LICENSE)

---

**关联 Article**：[Codex 模拟黑洞：科学发现中的生成-验证循环](../deep-dives/openai-codex-astrophysics-black-hole-algorithm-discovery-harness-loop-2026.md) — 用户实践层（单科学家 + Codex 协作）vs 工业化层（Sakana AI Scientist + LLM Reviewer）的对照
