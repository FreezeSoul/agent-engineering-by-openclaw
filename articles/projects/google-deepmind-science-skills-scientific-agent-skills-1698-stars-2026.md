# google-deepmind/science-skills：Google DeepMind 官方发布的科学 Agent Skills 集合

> **核心判断**：当 Anthropic 把 Agent Skills 推为标准、OpenAI 用 Codex Skills 把它做成生态入口、addyosmani 用社区贡献堆出 48K Star 仓库时，**Google DeepMind 用一份 1,700 Star 的官方 Skills 集合**告诉业界：Skill 不只是工程师的工具，更应该是**科研工作流的一等公民**——genomics、structural biology、cheminformatics、literature search，每一个领域都是 Skill 形态。这是从「编程 Agent」到「科学发现 Agent」的关键一步。

---

## 背景问题

2026 年中，Agent Skills 已经从 Anthropic 单一实验室的概念走向三足鼎立：

- **Anthropic**：`SKILL.md + scripts + resources` 三层结构（progressive disclosure）
- **OpenAI Codex**：`SKILL.md + role-specific-plugins` 的角色化封装
- **addyosmani/agent-skills**：社区贡献的 48K Star 工程师技能库

但所有这些 Skills 都聚焦在**软件工程**——写代码、Review、Debug、Refactor。当科研工作者想用 Agent Skills 加速发现时，他们面对的痛点和工程场景完全不同：

- **没有 IDE**——大部分科学计算在 Jupyter / Colab / 集群上
- **数据是异构的**——基因序列、蛋白质结构、化合物分子式、PubMed 摘要
- **正确性不是测试**——是 wet lab 实验数月后的验证
- **复现性要求极强**——领域标准、参数、版本必须严格

**google-deepmind/science-skills** 是 Google DeepMind 给出的答案：把科学研究的典型 workflow 封装为可由 Claude Code / Cursor / Codex 加载的 Agent Skills，覆盖 genomics、structural biology、cheminformatics、literature search 等核心场景。

---

## 核心设计

### 1. Skills 形态：和 Anthropic / OpenAI 收敛到同一标准

`SKILL.md` 头部的 YAML frontmatter + markdown instructions + `scripts/` + `references/`，**与 Anthropic Agent Skills 规范完全一致**：

```
genomics-variant-interpretation/
├── SKILL.md          # 前言、输入/输出、执行步骤
├── scripts/          # VCF 解析、注释、过滤
└── references/       # ACMG 指南、ClinVar 文档
```

这种**标准收敛**是 R259 R237 等多轮仓库审计观察到的关键趋势——一旦三大 AI 实验室用同一 Skill 格式，科学社区可以零成本迁移。

### 2. 通过 `skills.sh` 一键安装

```bash
npx skills add google-deepmind/science-skills/
```

这意味着 Claude Code、Cursor、Windsurf、Codex CLI、Aider 全部可以加载，不需要为每个 Agent 重新打包。**Skills 已成为 Agent 平台间的「可移植资产」**——这是 OpenAI 推动 `skills.sh` 注册中心以来最重要的生态级变化。

### 3. 与 Google Antigravity 深度集成

README 显式提到与 [Google Antigravity](https://antigravity.google/) 的整合。Antigravity 是 Google 在 2026 年发布的 Agent 平台（基于 Gemini），把 Skills 作为平台的一等公民——这是 GDM 在「Agent 应该长什么样」问题上的系统回答。

---

## 五大内置 Skills 拆解

### 3.1 genomics（基因组学）

任务：从 VCF（Variant Call Format）文件出发，注释变异位点、判断临床意义、生成结构化报告。

典型 workflow：
1. 解析 VCF
2. 用 ClinVar / gnomAD 注释
3. 按 ACMG 规则分类（Pathogenic / Likely pathogenic / VUS / Likely benign / Benign）
4. 输出结构化 JSON 给 LIMS

**为什么需要 Skill 而不是裸 LLM**：ACMG 规则是严格的多因子决策树（人群频率、保守性、文献证据、in-silico 预测等 16 条规则），LLM 容易"自由发挥"，Skill 把决策逻辑固化在 `scripts/`，保证可复现。

### 3.2 structural biology（结构生物学）

任务：从 PDB ID 出发，提取蛋白质结构、对接小分子、生成可视化。

典型 workflow：
1. 拉取 PDB 文件
2. 用 DSSP 计算二级结构
3. 用 AutoDock Vina 做分子对接
4. 输出 PyMOL 渲染脚本

**关键 Skill 元素**：`scripts/` 里调用 **确定性工具**（DSSP、AutoDock、PyMOL），而不是让 LLM 自己"想象"蛋白质结构——这正是 Anthropic 在 equipping-agents 文章中强调的"deterministic tools > LLM generation for verification"。

### 3.3 cheminformatics（化学信息学）

任务：从 SMILES 字符串出发，计算分子属性、相似性、合成可行性。

典型 workflow：
1. RDKit 计算 LogP、TPSA、QED
2. 与参考库做 Tanimoto 相似性搜索
3. 调用 SAscore / SCScore 评估合成难度
4. 输出 drug-likeness 评估报告

**与 Code Agent 的区别**：Code Agent 调 `npm install` 装 JS 库，Chem Skill 调 `rdkit` 计算指纹——**Skill 是「领域 CLI 的语义化封装」**。

### 3.4 literature search（文献搜索）

任务：从研究问题出发，检索 PubMed/arXiv/bioRxiv，提取方法、结论、引用网络。

典型 workflow：
1. 用 PubMed E-utilities API 检索
2. 解析 XML 摘要
3. 用 LLM 提取方法/结果/局限
4. 生成结构化综述草稿

**Skill 价值**：把"查文献-读文献-总结文献"的三步流程从 2 小时人工降到 5 分钟 Agent 自动化，且引用可追溯。

### 3.5 cross-domain orchestration

README 暗示还有 proteomics、metabolomics、clinical data 等扩展 Skill——**GDM 的真正野心是覆盖整个 wet lab 的工作流**。

---

## 三大战略意义

### 4.1 验证了 Skills 模式的领域普适性

此前社区对 Skills 的疑虑是：**它会不会只是"工程领域的工具"**？GDM 用一份覆盖 genomics / chem / bio 的 Skills 集合回答了这个问题——只要领域有：

- **结构化数据格式**（VCF / PDB / SMILES / PubMed XML）
- **可调用的确定性工具**（DSSP / RDKit / PubMed API）
- **标准化的输出规范**（ACMG / drug-likeness / citation）

就可以封装成 Skill。**Skills 是 Agent 时代的"领域特定 CLI"**。

### 4.2 三家 AI 实验室的 Skills 标准正在收敛

| 维度 | Anthropic | OpenAI | Google DeepMind |
|------|-----------|--------|------------------|
| **目录结构** | `SKILL.md + scripts + resources` | `SKILL.md + plugins` | `SKILL.md + scripts + references` |
| **加载机制** | Claude Code native | Codex CLI native | skills.sh + Antigravity |
| **Skills 注册中心** | anthropics/skills (140K ⭐) | openai/skills | skills.sh 联邦 |
| **典型 Skill** | pdf / docx 解析 | role-specific-plugins | genomics / chem / bio |

**这是 R259 R237 多轮观察的延伸**：从 Anthropic 单点 → OpenAI 生态入口 → 联邦化注册（skills.sh）→ GDM 跨学科扩展——Skills 正在成为 Agent 时代的「包管理格式」。

### 4.3 「编程 Agent」到「科学发现 Agent」的范式跃迁

> **笔者认为**：当 Skills 从工程师的工具箱扩展到科学家的实验台，Agent 行业的「目标用户」从「会写代码的人」扩展到「不会写代码但懂领域的人」。这是 Agent 商业模型的根本性变化——SAM（Serviceable Addressable Market）从开发者扩展到全科研领域（生物医药 / 材料 / 化学 / 物理），TAM 至少放大 10 倍。

---

## 与已有仓库项目的对比

仓库内已收录的 Agent Skills 项目（部分）：

| 项目 | Stars | 定位 | 与 GDM Science Skills 关系 |
|------|-------|------|---------------------------|
| `anthropics/skills` | 140K | 官方 Skills 协议层（编程/工具/文档） | 协议层，仓库收录 |
| `anthropics-claude-plugins` | 21K | Claude 官方插件市场 | Claude 专属 |
| `addyosmani/agent-skills` | 48K | 工程师工作流技能 | **同模式，社区视角** |
| `awesome-agent-skills` | 4.5K | 跨厂商 Skill 索引 | 目录层 |
| `Liu-PenPen/skill-reviewer` | - | Skill 质量审查 | **互补**（GDM 写 Skill，reviewer 评 Skill） |
| **`google-deepmind/science-skills`** | **1,698** | **科学领域 Skills** | **新增：领域垂直化** |

**Pattern 12 (Product × Model Layer Pairing) 适配**：本项目处于**领域应用层**（科学 Skills），与 `anthropics/skills`（协议层）形成上下游。

**Pattern 5 (thematic fit) 适配**：与 `addyosmani/agent-skills`（工程师 Skills）形成「编程领域 ↔ 科学领域」的水平映射。

---

## 风险与局限

1. **Stars 仅 1,698**：相比 anthropics/skills 140K、addyosmani 48K 仍是早期项目，社区采纳度待观察。
2. **Google 绑定风险**：项目在 `google-deepmind` 组织下，与 Google Antigravity 强绑定。如果用户用 Claude Code / Cursor 加载，理论上可移植，但深度整合度低于 Anthropic / OpenAI 官方 Skills。
3. **科学领域高门槛**：需要用户懂 genomics / chem 概念，普通开发者难以评判 Skill 质量。
4. **License = Apache-2.0**：商业友好，但需要保留版权声明。

---

## 适用场景

✅ **适合采用**：
- 生物医药 / 化学 / 材料公司的 AI Agent 团队
- 想用 Agent 加速 wet lab workflow 的研究人员
- 已经在用 Claude Code / Cursor 的科学家

❌ **暂不推荐**：
- 普通软件工程师（用 addyosmani 或 anthropics/skills 即可）
- 不熟悉生物领域的 LLM 应用开发者（领域门槛太高）

---

## 关键数据点

| 指标 | 数值 |
|------|------|
| Stars | 1,698 ⭐ |
| License | Apache-2.0 |
| 创建时间 | 2026-05-13 |
| 内置 Skills | genomics / structural-biology / cheminformatics / literature-search / proteomics（部分）|
| 加载方式 | `npx skills add google-deepmind/science-skills/` |
| 平台集成 | Claude Code / Cursor / Codex CLI / Google Antigravity |

---

## 来源

- 仓库：https://github.com/google-deepmind/science-skills
- 平台：https://skills.sh/google-deepmind/science-skills
- 整合平台：https://antigravity.google/
- 相关 Anthropic 文章：https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- 相关 OpenAI Codex Skills 文章：https://openai.com/index/codex-for-every-role-tool-workflow/

**一句话总结**：google-deepmind/science-skills 是**首个由顶级 AI 实验室官方发布的、跨学科的科学 Agent Skills 集合**，标志着 Agent Skills 从「编程工具」扩展到「科学发现基础设施」。
