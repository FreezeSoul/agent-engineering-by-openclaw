# NVIDIA BioNeMo Agent Toolkit：把 NVIDIA 十年生命科学栈封装成 Agent Skills

> **GitHub**: [NVIDIA-BioNeMo/bionemo-agent-toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit)  
> **Stars**: 237+ ⭐（持续快速增长中，发布仅 8 天）  
> **License**: Apache-2.0（代码）+ CC-BY-4.0（skills 与文档）双重许可  
> **官方定位**: Turn any agent into a life science expert with NVIDIA BioNeMo skills  
> **关联 Article**: R612 Anthropic Claude Science (`articles/harness/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md`)  
> **SPM 配对**: Claude Science 60+ skills + BioNeMo Agent Toolkit 14 NIM skills = **Harness Ecosystem 的首个多 1st-party 协同实例**

---

## 1. 概述

NVIDIA BioNeMo Agent Toolkit 把 NVIDIA 过去十年积累的生命科学 GPU 加速库、工具、开放模型（Evo 2 / Boltz-2 / OpenFold3 / DiffDock / GenMol / ProteinMPNN / RFdiffusion / KERMT 等），**统一打包为 Agent 可调用的 Skills**。

**核心定位**：不是又一个 NVIDIA 内部工具，而是 **「NVIDIA 生命科学栈 × Open Agent Skill 生态」的桥梁**。

它通过 [Anthropic skills CLI](https://github.com/vercel-labs/skills) 一键安装到 Claude Code / Codex / Cursor Agent 等任意 Agent，让任何 Coding Agent **立即具备生命科学领域能力**：

```bash
# 交互式安装
npx skills add NVIDIA-BioNeMo/bionemo-agent-toolkit

# 单个 skill + 不询问
npx skills add NVIDIA-BioNeMo/bionemo-agent-toolkit --skill boltz2-nim --yes

# 定向到特定 agent
npx skills add NVIDIA-BioNeMo/bionemo-agent-toolkit --skill boltz2-nim --agent claude-code
```

或者通过自托管 plugin marketplace：

```bash
# Codex
.agents/plugins/marketplace.json

# Claude Code
.claude-plugin/marketplace.json
```

---

## 2. Skill Catalog：14 个领域级 NIM Skills

| 类别 | Skills | 能力描述 |
|------|--------|---------|
| **结构预测** | `boltz2-nim`, `openfold2-nim`, `openfold3-nim`, `msa-search-nim` | Boltz-2 生物分子结构预测 + 结合亲和力；OpenFold2/3 蛋白结构预测；MSA-Search ColabFold 多序列比对 |
| **分子生成** | `genmol-nim`, `molmim-nim`, `rfdiffusion-nim`, `proteinmpnn-nim` | GenMol / MolMIM 分子生成与优化；RFdiffusion / ProteinMPNN 蛋白质设计 |
| **分子对接** | `diffdock-nim` | DiffDock 小分子对接 + 结合姿态预测 |
| **DNA 序列** | `evo2-nim` | Evo 2 DNA 序列生成 + 变异评分 |
| **属性预测** | `kermt-setup/infer/embed/finetune/...` | KERMT 分子属性预测（ADMET），基于 GROVER 多任务扩展 |
| **基因组** | `parabricks`, `genomics-workflow-acceleration` | Parabricks 加速基因组分析 |
| **化学信息** | `nvmolkit-usage` | nvMolKit GPU 加速化学信息学 |
| **神经算子** | `cuequivariance` | cuEquivariance 等变神经网络原语 |

每个 skill 都是**标准 Anthropic skills 目录结构**：

```
skill-name/
├── SKILL.md              # YAML frontmatter + instructions
├── references/           # 可选文档
├── scripts/              # 可选脚本
└── data/                 # 可选数据
```

---

## 3. 元 Skill（Meta Skills）：复杂工作流的编排

除了单 NIM skills，BioNeMo 还提供 **3 个元 skills**（meta-skills）来编排复杂科研工作流：

### 3.1 蛋白结合剂设计（Protein Binder Design）

```
complexa-binder-design: 蛋白结合剂 de novo 设计
    ├─ complexa-setup        ← 环境初始化
    ├─ complexa-target       ← 目标定义
    ├─ complexa-design       ← 蛋白设计
    ├─ complexa-sweep        ← 参数扫描
    ├─ complexa-evaluate-pdbs ← PDB 评估
    └─ complexa-slurm        ← SLURM 集群调度
```

### 3.2 分子生成虚拟筛选（Generative Virtual Screening）

```
drug-discovery-pipeline: GenMol → DiffDock → Boltz-2
```

### 3.3 MSA-启用的蛋白结构预测

```
msa-structure-prediction-pipeline: MSA-Search → OpenFold3
```

**关键洞察**：元 skills 把单 NIM skill **组合成 multi-step scientific workflows**——这是 **Skill-as-Harness**（R605）在垂直领域的实例化。

---

## 4. 设计哲学：为什么 BioNeMo Agent Toolkit 重要

### 4.1 多 1st-party Harness Ecosystem 的第一个实例

传统 AI Agent 产品是「**一家公司做完全栈**」：

- OpenAI Codex = 模型 + Codex app + Codex skill ecosystem
- Anthropic Claude = 模型 + Claude Code + Claude skills
- Google Gemini = 模型 + Gemini CLI + Gemini agent

BioNeMo Agent Toolkit 走出了**完全不同**的路：**NVIDIA 不做完整垂直 Harness，而是把 NVIDIA 的 GPU 加速能力**封装成开放 skills，让 Anthropic Claude Science / Cursor / Codex 等**任意外部 Agent**可以调用。

```
┌──────────────────────────────────────────────────────┐
│                    Harness Ecosystem                  │
├──────────────────────────────────────────────────────┤
│  Agent Loops (Claude Science / Codex / Cursor)       │
│       ↓ calls                                        │
│  Skill Registry (Anthropic skills CLI)               │
│       ↓ loads                                        │
│  ┌──────────────────────────────────────────┐        │
│  │ NVIDIA BioNeMo Agent Toolkit            │        │
│  │ ├─ NIM Skills (14)                       │        │
│  │ ├─ Meta-Skills (3)                       │        │
│  │ └─ Plugin Marketplaces (.agents/...)     │        │
│  └──────────────────────────────────────────┘        │
│       ↓ invokes                                      │
│  GPU Compute (HPC / Modal / Local)                   │
└──────────────────────────────────────────────────────┘
```

这是 **Harness Engineering 的去中心化架构**——不再是「一家公司 vertical」，而是 **「协议 + 领域 + 用户」三方协同**。

### 4.2 与 Claude Science 的协同（SPM 配对）

R612 Anthropic Claude Science 的核心声明：

> "Claude Science uses the skills in NVIDIA's [BioNeMo Agent Toolkit](https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit) to connect natively to the life sciences models and libraries in [BioNeMo](https://github.com/NVIDIA-BioNeMo), including Evo 2, Boltz-2, and OpenFold3."

这是一个 **「互补型 1st-party 协同」**：

- **Anthropic 提供**：agent loop / session persistence / reviewer agent / skill registry 协议层
- **NVIDIA 提供**：14 个 NIM skills + 3 个 meta skills 的领域能力层

任何一家单独都不够：NVIDIA 有 GPU + 模型但没有完整 Agent Loop；Anthropic 有完整 Agent Loop 但没有 GPU + 领域模型。**协同之后，两者都成为 Harness Ecosystem 的关键节点**。

### 4.3 dual-license 的工程考量

| 类别 | 许可 | 工程意义 |
|------|------|---------|
| **代码**（scripts / tests / build tooling） | Apache-2.0 | 允许商业使用、修改、分发 |
| **Skills 与文档**（SKILL.md / workflows / READMEs） | CC-BY-4.0 | 允许复制、分发、修改，但需要归属 |

这是 NVIDIA **精心设计的 licensing**：

- **Apache-2.0 代码**：让任何公司可以在自己的产品里 fork / 嵌入
- **CC-BY-4.0 文档**：让知识可以广泛传播，但 NVIDIA 始终作为原作者被署名

**洞察**：dual-license 反映了 NVIDIA **「让 skill ecosystem 最大化扩散」**的战略意图——不是卖软件，而是 **「成为生命科学 Agent 领域的默认基础设施」**。

---

## 5. 工程机制密度分析

### 5.1 跨平台 Harness 集成

BioNeMo Agent Toolkit 通过 **3 个独立路径** 接入不同 agent：

| 路径 | 目标 Agent | 安装方式 |
|------|-----------|---------|
| **Anthropic skills CLI** | Claude Code / Codex / Cursor / OpenCode | `npx skills add ...` |
| **Codex Plugin Marketplace** | OpenAI Codex | `.agents/plugins/marketplace.json` |
| **Claude Code Plugin Marketplace** | Claude Code | `.claude-plugin/marketplace.json` |

这是 **「Write once, deploy anywhere」**——一个 skill 目录可以**同时**在 3 个独立 agent 生态中运行。

### 5.2 内置 MCP / Connector 协议

每个 meta-skill 内部都包含 **MCP 兼容的 connector 实现**——可以直接接 Claude Science 的 connector 系统，无需额外胶水代码。

### 5.3 本地优先的数据流

参考 Anthropic Claude Science 的 **「data minimization」** 原则：

- **数据集**（如 PDB、CIF 文件）保存在本地 / HPC，不上传到 Claude / OpenAI
- **模型权重** 通过 NIM 本地部署
- **只有当前步骤所需的最少上下文** 发送到 Agent

---

## 6. 在 Claude Science 中的使用案例

Allen Institute 的 Jérôme Lecoq 用 Claude Science + BioNeMo Agent Toolkit 写了一个 **20 个 custom skills 的 multi-agent "computational review template"**：

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

效果：原本需要 **2 年**的文献综述，现在能在几周内完成 **10+ 篇 100+ 页**的综述。

---

## 7. 工程机制统计

| 维度 | 数量 | 评级 |
|------|------|------|
| **领域级 NIM Skills** | 14 | ⭐⭐⭐⭐ |
| **元 Skills** | 3 | ⭐⭐⭐⭐⭐ |
| **KERMT 细分 Skills** | 7 | ⭐⭐⭐⭐ |
| **支持 Agent** | Claude Code + Codex + Cursor + OpenCode | ⭐⭐⭐⭐⭐ |
| **Plugin Marketplace 路径** | 2（Codex + Claude Code） | ⭐⭐⭐⭐⭐ |
| **License 灵活性** | Apache-2.0 + CC-BY-4.0 | ⭐⭐⭐⭐⭐ |
| **1st-party 背书** | NVIDIA（GPU 领域最强） | ⭐⭐⭐⭐⭐ |
| **Anthropic 官方协同** | Claude Science 引用 | ⭐⭐⭐⭐⭐ |
| **社区活跃度** | 8 天 237⭐，增长曲线极陡 | ⭐⭐⭐⭐ |

**总评**：尽管 stars 暂时只有 237，但**作为 NVIDIA 1st-party + Anthropic 官方协同的工程产物**，其工程价值与潜在影响力远超 stars 数字。

---

## 8. 局限与未来

### 8.1 当前局限

- **stars 较低（237）**：发布仅 8 天，尚未充分扩散
- **License NOASSERTION**：GitHub 自动识别失败，需要用户细读 LICENSE 文件
- **领域特定**：仅限生命科学，非通用 Agent skill

### 8.2 未来预测

- **Q3 2026**：预计 stars 突破 1000（skill CLI 标准化 + Claude Code / Codex / Cursor 三端集成）
- **Q4 2026**：预计 NVIDIA 推出 BioNeMo Agent Toolkit v2，扩展到材料科学、化学工程
- **2027**：BioNeMo Agent Toolkit 可能成为 **「AI for Science」** 领域的默认 infrastructure layer

---

## 9. SPM 配对总结

**Article (R612)**: Anthropic Claude Science — 6 大 Harness 原则在生命科学场景的工程化落地
**Project (R612)**: NVIDIA BioNeMo Agent Toolkit — 14 NIM skills + 3 meta-skills 的垂直领域能力层

**两者形成完整 Harness Ecosystem 闭环**：

- Article 示范了**如何**用 Harness 原则做垂直科学
- Project 提供了**具体可调用**的 17 个领域 skills

**没有 Claude Science，BioNeMo Agent Toolkit 只是孤立 GPU skills；**
**没有 BioNeMo Agent Toolkit，Claude Science 缺少 14 个最关键的生命科学 NIM 能力。**

---

## 📚 参考资料

- **GitHub**: https://github.com/NVIDIA-BioNeMo/bionemo-agent-toolkit
- **NVIDIA BioNeMo 主站**: https://github.com/NVIDIA-BioNeMo
- **Anthropic Claude Science 配套引用**: https://www.anthropic.com/news/claude-science-ai-workbench
- **Anthropic Skills CLI**: https://github.com/vercel-labs/skills
- **NVIDIA BioNeMo Agent Toolkit 发布**: https://nvidianews.nvidia.com/news/nvidia-launches-bionemo-agent-toolkit-giving-ai-agents-the-tools-to-accelerate-scientific-discovery