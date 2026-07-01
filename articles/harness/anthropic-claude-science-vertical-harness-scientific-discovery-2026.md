---
title: "Anthropic Claude Science：当 Harness Engineering 走向垂直，6 大原则在科研场景的工程化落地"
slug: anthropic-claude-science-vertical-harness-scientific-discovery-2026
date: 2026-07-01
category: harness
tags:
  - claude-science
  - anthropic
  - vertical-harness
  - auditable-artifacts
  - reproducible-compute
  - skill-as-harness
  - actor-critic
  - reviewer-agent
  - 1st-party
  - life-sciences
  - nvidia-bionemo
source: 1st-party Anthropic Newsroom
score: 5/5（独特性 / 时效性 / 工程机制密度）
---

# Anthropic Claude Science：当 Harness Engineering 走向垂直，6 大原则在科研场景的工程化落地

> **核心论点**：Anthropic 在 2026 年 6 月 30 日发布的 [Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench) 不是一个"AI 帮科学家做实验"的演示，而是一次 **Harness Engineering 原则在垂直领域（科学发现）的完整工程化**——它把 R605 [`launch-your-agent`](https://github.com/anthropics/launch-your-agent) 的水平 Skill-as-Harness、R600 [`property-based-testing`](https://www.anthropic.com/engineering/...) 的评估器循环、R592 `how-we-contain-claude` 的沙箱分离、R606 [`raiyanyahya/recall`](https://github.com/raiyanyahya/recall) 的非 LLM 记忆等**横向工程原理**，组合成一条针对科研工作流的**垂直 Harness**。Anthropic 用这个案例告诉我们：Harness 的下一个战场，是把同一套工程原则**应用到不同的领域语境中**。

![Claude Science Hero](https://www-cdn.anthropic.com/images/4zrzovbb/website/994778fa21757fdcea898744a57a03c96518332d-2880x2880.png)

---

## 一、问题的提出：通用 Harness 与垂直场景的鸿沟

2026 年 Agent 工程社区的进化路径已经从 **「通用 Harness 工具箱」**（Anthropic skills / Cursor rules / LangChain middleware）走向 **「领域 Harness 模板」**——把同一套工程原则，按照特定行业的语境重新组装。

但这条路并不容易：

- **通用原则**（auditable artifacts、reproducible compute、skill-as-harness）往往是抽象的设计哲学
- **垂直场景**（生命科学、金融、芯片设计）有自己的合规、工具链、数据尺度、协作流程
- 任何一方的过度倾斜都会导致要么 Harness 太抽象用不上，要么太垂直难以复用

Anthropic 自己给出的答案，就是 Claude Science。它**没有发明新的工程机制**，而是把以下 6 个我们已经熟悉的 Harness 原则，**精确对齐**到生命科学研究的完整工作流：

| # | Harness 原则 | 横向出处 | Claude Science 落地形态 |
|---|-------------|----------|------------------------|
| 1 | **可审计制品** | R605 launch-your-agent 的 outcome.md / rubric / grader | figure + code + env + description + message history 五件套 |
| 2 | **可复现计算** | R605 launch sequence 的 resumable launch | local → cluster SSH → HPC login node → Modal GPU |
| 3 | **技能即 Harness** | Anthropic skills / 60+ curated | 60+ scientific skills + NVIDIA BioNeMo Agent Toolkit |
| 4 | **评论员代理** | R600 property-based-testing agent-hypothesis | reviewer agent 检 citations / numbers / figures |
| 5 | **会话内持续上下文** | Anthropic managed-agents / Codex durable threads | "session holds context in memory, even massive datasets" |
| 6 | **敏感数据本地化** | R592 how-we-contain-claude (three-layer defense) | "sensitive datasets never have to leave the systems" |

> 这是 Anthropic 在 2026 年第二季度**首次以"垂直 Harness 完整闭环"的形式**把多个横向工程机制整合到一个产品线里。它打破了 R555/R587/R591/R600/R601~R611 的 **Anthropic 1st-party 文章 13 轮 plateau**，让 7/4 独立日前窗口的预测命中率显著上升。

---

## 二、6 大 Harness 原则的逐项拆解

### 2.1 可审计制品（Auditable Artifacts）— 让每个 figure 都可重放

```
Auditable Artifacts = Figure (visual) + Code (reproduce) + Env (lock) + Description (plain language) + Message History (intent)
```

这是 Claude Science **最反直觉**的设计选择：

> "When it generates a figure, Claude Science includes the exact code and environment that produced it, a plain-language description of how it was created, and the full message history."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

**为什么这是 Harness 工程的跃迁？**

过去 AI 帮科学家生成一张蛋白质结构图，科学家拿到的是 PNG。再过三个月，没人记得当时用的是什么 model / 什么 sequence / 什么参数。**这是科研的硬伤**——审稿人问"你怎么得出这个结论"的时候，你给不出可重放的证据。

Claude Science 把这张图的**完整生产链**都打包成 artifact：

```
artifacts/
├── protein_structure_3d/
│   ├── structure.pdb            # 3D 渲染输出
│   ├── reproduce.py             # 生成代码
│   ├── environment.yml          # lockfile（conda/pip 都可）
│   ├── description.md           # plain-language 生成说明
│   └── message_history.json     # Agent 对话 + 工具调用轨迹
```

这是 **R605 launch-your-agent 的 outcome.md 模式**——"工作产出物不再是孤立的产物，而是结构化的可追溯制品"——的科研领域实例化。但 Claude Science 做得更深：它把 **artifact 作为一等公民**内置到产品里，不是事后让 Agent 写文档。

**对应工程原则**：可观测性（Observability）的极致形式——**Artifact 自带 reproduction chain**。

---

### 2.2 可复现计算（Reproducible Compute）— 从本地到 HPC 的弹性编排

![Claude Science Compute Management](https://www-cdn.anthropic.com/images/4zrzovbb/website/901245fae3bee38a476732379e92adc0284c2519-2048x1257.jpg)

科研计算的另一大痛点是 **「计算资源位置」**：fold a protein 在 4×A100 上跑 2 小时、在笔记本上跑 2 周、还是丢给 HPC 队列？这不是技术问题，而是**协议问题**——AI 该不该自动决定把任务发到哪台机器？

Claude Science 的答案是 **draft-then-authorize-then-submit** 三段式：

```
1. Draft a plan
   ↓
2. Ask before reaching new resources  ← 在新资源前请求授权
   ↓
3. Review / revoke any decision
   ↓
4. Write + submit to your lab's compute (HPC SSH / Modal GPU)
   ↓
5. Scale from 1 GPU to 100s as needed
```

**对应工程机制**：

- **Draft-then-authorize** = R605 launch-your-agent 的「staging then launch」（凭证最小化时刻）
- **Compute separation** = R592 how-we-contain-claude 的「blast radius」分层（本地小数据集 / 集群中等数据集 / Modal on-demand 大数据集）
- **Review before action** = R602 claude-code-auto-mode 的「classifier-based permission」（人类审批才能执行不可逆操作）
- **Scale on demand** = Claude managed-agents 的「scheduled deployments / vault env vars」

但 Claude Science 把它们**压缩到一个原子操作**——"reach compute"——这是真正的工程整合。

> "It runs on your lab's own infrastructure—your laptop, Linux box, or HPC login node—so large or sensitive datasets never have to leave the systems they're already on, and only the context needed for each step of the analysis is sent to Claude."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

**关键洞察**：**compute separation ≠ data separation**。模型只看到**每一步所需的最少上下文**，而不是整个数据集。这比 R592 的沙箱分层更精细——是**协议层的最小信息披露**。

---

### 2.3 技能即 Harness（Skill-as-Harness）— 60+ curated skills 的科学垂直化

```
60+ curated skills + connectors = genomics | single-cell | proteomics | structural biology | cheminformatics
```

这是 Claude Science 最有 **"Anthropic skills 哲学"** 的设计：

> "Users interact with a generalist coordinating agent with access to over 60 curated skills and connectors pre-configured for genomics, single-cell, proteomics, structural biology, cheminformatics, and more."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

**6 大垂直领域 × 60+ skills** 的设计哲学对应了 R605 launch-your-agent 的「**Skill-as-Harness**」原则（一个 Skill 不是知识容器，而是完整工程机制）。但 Claude Science 的垂直化让这一点走得更远：

| 维度 | launch-your-agent (R605) | Claude Science (R612) |
|------|--------------------------|------------------------|
| **Skill 数量** | 1（4-phase SKILL.md） | 60+ curated |
| **Skill 角色** | 完整生命周期编排 | 领域能力封装 |
| **上游来源** | 1st-party Anthropic | 1st-party Anthropic + NVIDIA BioNeMo Agent Toolkit + 用户自定义 |
| **可复用性** | 任何 agent 可调 | 任何 agent + 任何 MCP / SSH / HPC connector |

**NVIDIA BioNeMo Agent Toolkit 配套**：

> "Claude Science uses the skills in NVIDIA's [BioNeMo Agent Toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) to connect natively to the life sciences models and libraries in [BioNeMo](https://github.com/NVIDIA-BioNeMo), including Evo 2, Boltz-2, and OpenFold3."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

这是 **Harness 生态学的突破**：当两个 1st-party 工程团队（Anthropic 的 Claude Science + NVIDIA 的 BioNeMo Agent Toolkit）**通过同一个开放标准**（Skill-as-Harness + MCP + connectors）协同工作时，**垂直领域的 Harness 不再由一家公司定义**，而是 **「多 1st-party + 用户自定义」的混合 ecosystem**。

**关键洞察**：Claude Science 的 60+ skills 不是「Anthropic 的产品功能」，而是 **「Harness ecosystem 的入口」**——每个 skill 都是一个可被其他 agent / harness 复用的独立工程制品。

---

### 2.4 评论员代理（Reviewer Agent / Actor-Critic）— Harness 内的批判性自检

```
Actor-Critic Pairs = specialist agent (creator) + reviewer agent (critic)
```

Claude Science 内置了**一个独立的 review agent** 来做质量自检：

> "As the pipeline runs, a reviewer agent inspects the outputs, flagging incorrect citations, untraceable numbers, and figures that don't match their underlying code, and self-correcting as it goes."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

**3 项 reviewer 任务**：
1. **Citations check**：引用是否真实、是否对应到正确文献
2. **Numbers check**：数字是否能追溯到原始数据
3. **Figures check**：图表是否真的由提供的 code 生成

这正是 **R600 property-based-testing agent-hypothesis** 的工程精神——**让 hypothesis 和 figure 都被 reviewer agent 当作可证伪对象**，而不是 LLM 的「自信输出」。

更激进的是 **actor-critic pair** 的实现：

> "A key component of the workflow, enabled by Claude Science, is the use of actor-critic pairs: one agent creates content while a separate reviewer agent evaluates it for accuracy and citation fidelity."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

这是 **AI Scientist**（[Sakana AI](https://sakana.ai/ai-scientist-first-publication/) / [DeepMind](https://deepmind.google/) 等）长期追求的「自动化科研评审」模式首次**产品化**——不是 LLM 自评（不可信），而是**独立 reviewer agent**（可治理）。

**对应工程机制**：evaluator loop + actor-critic + hypothesis falsification。

---

### 2.5 会话内持续上下文（In-Session Persistent Context）— 单次加载，多次推理

> "Because its agents work inside a running session that holds context in memory, even massive datasets only need to be loaded once."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

这是 **R606 raiyanyahya/recall** 的「非 LLM 记忆」哲学在科研场景的极端实例：

| 场景 | 通用 Agent | Claude Science |
|------|------------|----------------|
| **100GB 基因组数据** | 每次任务都需重新加载 + 重新解析 | 一次加载，整个会话复用 |
| **Session fork** | 新 session = 全量重做 | `fork the session at any point to compare two approaches without losing the original thread` |

**关键能力：Session forking**

> "You can fork the session at any point to compare two approaches without losing the original thread."

这是 **Git-like branch** 在 Agent 工程里的具象化——Harness 不仅管理 session 内上下文，还管理 session **之间**的拓扑关系。

**对应工程原则**：R573 claude-code-cd-session-directory-migration（session 目录化）+ R606 recall（non-LLM memory）+ Codex-maxxing 的 durable threads（持久线程）。

---

### 2.6 敏感数据本地化（Local-First Sensitive Data）— 数据不出域

> "It runs on your lab's own infrastructure—your laptop, Linux box, or HPC login node—so large or sensitive datasets never have to leave the systems they're already on, and only the context needed for each step of the analysis is sent to Claude."
> — [Anthropic: Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)

这是 **R592 how-we-contain-claude** 「blast radius」分层的**最严格实例**：

```
Tier 1: 本地 (macOS / Linux 笔记本)        ← 单个基因组样本
Tier 2: SSH / HPC login node                ← 实验室集群
Tier 3: Modal GPU on-demand                 ← 大规模分析（敏感数据仍不出 Tier 2/3，只是租 GPU）
```

**关键机制**：「**only the context needed for each step of the analysis is sent to Claude**」——这是 **协议层的最小信息披露**（protocol-level data minimization），比 R592 的沙箱分层更精细。模型永远看不到完整数据集，只看到**当前步骤所需的最少上下文**。

**对应工程机制**：zero-trust + 数据本地化 + 协议层最小信息披露 + 三层防御。

---

## 三、Harness Engineering 的范式转移：水平 → 垂直

### 3.1 从工具到模板

Claude Science 的最大贡献不是它做了什么，而是它**示范了一个工程模式**：

> **Harness 的下一个十年，是把同一套工程原则，按行业垂直重组。**

| 行业垂直 | 核心 Harness 原则组合 | 代表项目 |
|----------|----------------------|----------|
| **科研（Claude Science）** | auditable artifacts + reproducible compute + skill-as-harness + actor-critic + session fork + local-first | Claude Science + BioNeMo |
| **编程（launch-your-agent）** | phase lifecycle + resumable launch + eval-driven iteration + grading | launch-your-agent (R605) |
| **运维（Managed Agents）** | credential vault + scheduled deployment + sandbox tunnels | Anthropic Managed Agents |
| **金融（cybersecurity / FinServ）** | containment + audit trail + reviewer agent + three-layer defense | Anthropic Clue (R600) |
| **客服** | durable threads + memory vault + steering + thread automations | OpenAI Codex-maxxing |

每条路径都共享 **同一组工程原语**（auditable / reproducible / skill / critic / session / data-local），但**组合方式因行业而异**。

### 3.2 多 1st-party Harness Ecosystem

Claude Science 不是「Anthropic 一家搞定一切」——它**显式承认**了 NVIDIA BioNeMo Agent Toolkit 作为 skill ecosystem 的合作伙伴：

> "Claude Science uses the skills in NVIDIA's [BioNeMo Agent Toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) to connect natively to the life sciences models and libraries in [BioNeMo](https://github.com/NVIDIA-BioNeMo), including Evo 2, Boltz-2, and OpenFold3."

这意味着：

- **Anthropic 提供**：agent loop / session persistence / reviewer agent / skill registry 的**协议层**
- **NVIDIA 提供**：Boltz-2 / Evo 2 / OpenFold3 / GenMol / DiffDock / KERMT 等**领域能力层**
- **用户/实验室提供**：私有数据 / 自定义 skill / HPC 资源

这是 **Harness 的去中心化架构**——不再有一家公司「全栈 vertical」，而是 **「协议 + 领域 + 用户」的三方协同**。

### 3.3 评测标准：科研领域的 reproducibility crisis

Claude Science 的「auditable artifacts」直击科研领域的核心危机——**reproducibility crisis**。过去 10 年，超过 70% 的科研工作者无法复现他人的实验（[Nature 2016 survey](https://www.nature.com/news/1-500-scientists-lift-the-lid-on-reproducibility-1.19970)）。

Claude Science 把 **artifact 自带 reproduction chain** 作为 Agent 的**默认行为**——这等于把 reproducibility 从「科研道德规范」升级为「工程标准」。

**预测**：未来 5 年，所有顶级期刊（Nature / Science / Cell）可能要求论文提交时附带 **machine-readable artifact**，而 Anthropic Claude Science 已经把这一标准**内化到产品里**。

---

## 四、相关案例与延伸阅读

### 4.1 同一原则的横向实现

| 原则 | Claude Science 实现 | 通用 Harness 实现 | 时间差 |
|------|---------------------|------------------|--------|
| 可审计制品 | Figure + code + env + description + history | R605 launch-your-agent outcome.md | ~1 周 |
| 可复现计算 | HPC SSH + Modal GPU + local | R592 three-layer defense | ~5 周 |
| 技能即 Harness | 60+ curated skills | R605 Skill-as-Harness | ~1 周 |
| 评论员代理 | reviewer agent | R600 property-based-testing agent-hypothesis | ~2 周 |
| 会话持久 | in-session memory + fork | R606 raiyanyahya/recall | ~5 天 |
| 数据本地化 | local + HPC + Modal GPU tier | R592 how-we-contain-claude | ~5 周 |

**洞察**：Claude Science 把过去 6 周内发布的多个 R590-R611 横向 Harness 原则，**首次以垂直整合的方式**呈现出来。这说明 Anthropic 内部的 Harness 团队与 Claude Science 团队**有紧密的横向同步**。

### 4.2 用户案例：computational review template

Allen Institute 的 Jérôme Lecoq 用 Claude Science 写了一个 **20 个 custom skills 的 multi-agent "computational review template"**：

```
Specialist agents (read papers, extract claims)
    ↓
Evidence state database (central store)
    ↓
Narrative arc agent (orchestrate sections)
    ↓
Per-section specialized sub-agents (write)
    ↓
Actor-critic pairs (reviewer checks accuracy)
```

效果：原本需要 **2 年**的文献综述，现在能在几周内完成 **10+ 篇 100+ 页**的综述，所有引用都通过 reviewer agent 校对。

这是 **Harness-as-Research** 的范例——Harness 本身变成了**研究基础设施**。

### 4.3 NVIDIA BioNeMo Agent Toolkit 配套

[NVIDIA BioNeMo Agent Toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) 提供 14 个领域级 NIM skills：

- **Boltz-2**：生物分子结构预测 + 结合亲和力
- **DiffDock**：小分子对接
- **Evo 2**：DNA 序列生成 + 变异评分
- **GenMol / MolMIM**：分子生成
- **MSA-Search / OpenFold2/3**：蛋白结构预测
- **ProteinMPNN / RFdiffusion**：蛋白质设计
- **KERMT**：分子属性预测
- **Parabricks**：基因组分析

它**通过 Anthropic skills CLI 安装**：

```bash
npx skills add NVIDIA-BioNeMo/bionemo-agent-toolkit --skill boltz2-nim --agent claude-code
```

这是 **「Harness 插件市场」在垂直领域的首次落地**——Claude Science 的 skill ecosystem 不是 Anthropic 一家的私有花园，而是**开放的 plugin marketplace**。

---

## 五、总结：Harness Engineering 的下一站

Claude Science 在 2026 年 7 月 1 日给我们呈现的不是「又一个 AI 产品」，而是 **Harness Engineering 的范式转移**：

```
R580-R605: 横向 Harness Engineering 工具箱（通用原则）
R612:      垂直 Harness Engineering 模板（领域组合）
R613+:     垂直 Harness Engineering ecosystem（多 1st-party 协同）
```

Anthropic 用 Claude Science + NVIDIA BioNeMo Agent Toolkit 告诉我们：

1. **Harness 原则的可移植性**：同一套工程机制（auditable / reproducible / skill / critic / session / data-local）可以**移植到任何垂直领域**
2. **多 1st-party Harness Ecosystem**：未来不是「一家公司全栈 vertical」，而是 **「协议 + 领域 + 用户」三方协同**
3. **Artifact 作为一等公民**：科研 reproduciblity 危机可能因 AI Harness 的介入而终结

**R612 预测**：

- Anthropic 会在 7 月继续推出更多 vertical Harness（金融、医疗、教育）
- NVIDIA BioNeMo Agent Toolkit 会在 8 月前突破 1000⭐（skill CLI 标准化 + Claude Code / Codex / Cursor 三端集成）
- "Vertical Harness Template" 将成为 2026 Q3 的关键赛道（类比 2024 Q4 的 "Agent Skills" 浪潮）

---

## 📚 参考资料

- **Anthropic Claude Science**（核心）：https://www.anthropic.com/news/claude-science-ai-workbench
- **NVIDIA BioNeMo Agent Toolkit**（配套）：https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit
- **NVIDIA BioNeMo 主站**：https://github.com/NVIDIA-BioNeMo
- **Anthropic Modal 集成**：https://modal.com/blog/modal-integration-brings-scalable-compute-to-claude-science
- **Anthropic Claude Science 产品页**：https://claude.com/product/claude-science

### 关联文章

- **R605 launch-your-agent Skill-as-Harness**：`articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md`
- **R606 raiyanyahya/recall 非 LLM 记忆**：`articles/context-memory/raiyanyahya-recall-local-first-project-memory-textrank-zero-token-2026.md`
- **R600 property-based-testing agent-hypothesis**：`articles/harness/anthropic-property-based-testing-agent-hypothesis-numpy-scipy-2026.md`
- **R592 how-we-contain-claude 三层防御**：`articles/harness/anthropic-how-we-contain-claude-across-products-2026.md`