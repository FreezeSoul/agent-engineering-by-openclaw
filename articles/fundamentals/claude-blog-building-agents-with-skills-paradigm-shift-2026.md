# 从专用 Agent 到 Skills：Anthropic 的范式转移

> 原文：[Building agents with Skills: Equipping agents for specialized work](https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work)（2026-01-22，claude.com/blog）
>
> 核心命题：**停止构建专用 Agent，开始构建 Skills。Agent 的专业化不是改模型，而是给它正确的技能包。**

---

## 一、范式转移：专用 Agent 的时代正在结束

长期以来，给 Agent 赋予专业能力的思路是**构建专用 Agent**——用特定数据微调、在特定领域 prompt 工程、或者直接训练一个领域专用模型。这个思路直观，但有一个致命问题：**每个新领域都需要从零开始**。

2026 年 1 月 22 日，Anthropic 在 Claude Blog 发布了一篇标志性的范式转变声明：

> "Building agents with Skills is about packaging domain expertise for AI agents — turning capable generalists into knowledgeable specialists through organized files and workflows."
>
> — [Building agents with Skills: Equipping agents for specialized work](https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work)，2026-01-22

这句话的核心是**解耦**：不是改变 Agent 的"脑子"（模型），而是给它一个可拔插的专业技能包。模型还是那个通用模型，但因为加载了不同的 Skills，它能在不同领域达到专家级的表现。

笔者认为，这个转变的意义不亚于当年从"单机程序"到"可组合微服务"的架构演进——**专业化不是重写核心，而是正确地组装组件**。

---

## 二、Skills 是什么：不只是 Prompts 的集合

理解 Skills 的第一个误区是把它等同于"一组 Prompts"。实际上，Anthropic 定义的 Skill 是一个标准化的目录结构：

```
skill-name/
├── SKILL.md          # 核心规范文件
├── instructions/    # 任务指令集
├── scripts/         # 可执行脚本
└── resources/       # 参考资源
```

SKILL.md 是这个技能包的核心——它不只是 instructions 的集合，而是一套**能让 Agent 动态发现、加载并执行特定任务的组织化规范**。

> "A skill is a directory containing a SKILL.md file that contains organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks."
>
> — Anthropic Engineering Blog，Oct 2025

Skills 的可发现性（discoverable）和动态加载（dynamically load）是它与传统 system prompt 的本质区别。传统 prompt 是硬编码的、静态的；Skills 是可发现的、可组合的。

---

## 三、为什么 Skills 比专用 Agent 更优

| 维度 | 专用 Agent | Skills 模式 |
|------|-----------|-------------|
| **开发成本** | 每个领域需独立开发 | 一个 Skills 库，多个 Agent 复用 |
| **专业化速度** | 需要数据 + 微调 + 评测 | 加载对应 Skill 即可 |
| **模型更新** | 领域知识可能需要重新训练 | Skills 独立于模型，可复用 |
| **可组合性** | 差，领域 Agent 难以组合 | 强，多个 Skills 可叠加 |
| **可审计性** | 领域逻辑埋在模型权重里 | Skills 文本化，完全可审计 |

笔者认为，最关键的是**专业化速度**和**模型更新解耦**。在 2026 年的模型迭代速度下，任何基于特定模型训练的专用 Agent 都面临"模型一更新，能力就退化"的问题。而 Skills 模式中，模型升级只需要验证 Skills 的兼容性，不需要重新训练。

---

## 四、Skills 的标准化：agentskills.io 的意义

Anthropic 推动的 Skills 标准不仅仅是给自己用——它正在通过 **agentskills.io** 形成行业开放标准。目前支持 Skills 的平台已经包括：

- Claude Code（原生支持）
- GitHub Copilot
- OpenAI Codex CLI
- Cursor
- Gemini CLI
- 以及所有 agentskills.io 兼容平台

这个标准化的意义在于：**Skills 不再是某一家的独占资产，而是可以跨平台复用的行业公共品**。一个安全团队的 Skills 库可以同时给 Claude Code 安全分析 Agent 和 Cursor 开发 Agent 使用，不需要重复建设。

---

## 五、工程落地：从"技能清单"到"动态编排"

Skills 模式的工程落地有一个关键设计原则：**Skills 应该是细粒度的、可组合的**。不要做一个"全能安全 Agent"，而是做一组细粒度 Skills：

- `sigma-rule-writing`：编写检测规则
- `volatility3-memory-analysis`：内存镜像分析
- `cloud-breach-scoping`：云安全事件范围界定
- `threat-intel-enrichment`：威胁情报充实

每个 Skill 专注一个原子能力，通过 Agent 的编排层（orchestration）将多个 Skills 组合成完整的分析流程。这是真正的**Unix 哲学在 Agent 时代的复现**：做一件事，做好它，通过管道组合。

---

## 六、Skills 的局限与适用边界

笔者认为，Skills 模式并非银弹，有明确的适用边界：

**Skills 擅长的**：
- 有明确流程的专业任务（取证分析、代码审查、威胁情报）
- 需要跨平台复用的领域知识
- 需要频繁更新的知识（监管合规、漏洞库）

**Skills 不擅长的**：
- 需要深层世界知识的任务（常识推理、复杂数学证明）
- 实时感知类任务（需要模型原生能力）
- 高度个性化、难以规范化的创意任务

Skills 是 Agent 专业化的**工程杠杆**，不是替代模型智能的捷径。

---

## 七、实战建议：如何构建你的第一个 Skill

1. **从原子能力开始**：不要一开始就做一个"安全分析 Skill"，从 `analyze-suspicious-file` 这样单一任务的 Skill 入手
2. **遵循 agentskills.io 规范**：标准的 SKILL.md 结构是跨平台复用的前提
3. **每个 Skill 有明确的 stop condition**：好的 Skill 知道自己什么时候完成，什么时候应该报错
4. **用真实任务测试**：Skills 的价值在实战中体现，在模拟环境中设计、在真实任务中验证
5. **建立 Skills 索引**：当 Skills 超过 10 个时，需要一个索引机制让 Agent 知道该加载哪个

---

## 结语

Anthropic 在 2026 年初给出的答案很清晰：**Agent 的专业化不是改变模型，而是给它正确的 Skills**。这个范式转移的核心洞察是——通用模型 + 正确技能包 = 专家级 Agent，而不是专家级模型 + 通用提示词 = 还行的 Agent。

前者是可工程化的、可复用的、可组合的。后者是把问题推给模型，期望模型自己解决。

> "Turning capable generalists into knowledgeable specialists through organized files and workflows."
>
> — Anthropic，2026-01-22

**所以你应该**：停止追求"一个更聪明的 Agent"，开始构建"一个可组合的 Skills 体系"。这是 2026 年 Agent 工程化的正确方向。