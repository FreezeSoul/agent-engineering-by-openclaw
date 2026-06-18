---
title: "Anthropic 大代码库 Claude Code 五大扩展点 2026"
date: 2026-05-14
slug: how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
source: https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
cluster: practices
cluster_role: cluster_anchor
pair_article: null
pair_project: articles/projects/jeremylongshore-claude-code-plugins-plus-skills-marketplace-2026.md
tags: [claude-code, harness, large-codebase, monorepo, enterprise-rollout, agent-manager, dri, applied-ai]
authors: Alon Krifcher, Charmaine Lee, Chris Concannon, Harsh Patel, Henrique Savelli, Jason Schwartz, Jonah Dueck, Kirby Kohlmorgen (Anthropic Applied AI team)
---

# Anthropic 大代码库 Claude Code 五大扩展点 2026

> 一手源：Anthropic Applied AI 团队 2026-05-14 发布
> 原文：https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start
> 配套 Project：`jeremylongshore/claude-code-plugins-plus-skills`（2,390⭐ MIT，5 扩展点的开源 marketplace 工程化身）

## 核心命题

在大型代码库（百万行 monorepo、跨十年 legacy、几十个微服务、多语言 C/C++/Java/PHP）部署 Claude Code 时，**模型本身不是决定性因素，决定性因素是围绕模型的 Harness 五层扩展点**。Anthropic Applied AI 团队在多次客户部署中观察到，harness 质量 > 模型质量，且五层扩展点的构建顺序敏感。

**第一性原则**：Claude Code 像人类工程师一样在本地文件系统中工作（ls、grep、读文件、跨文件跟踪引用）—— 不需要中央 codebase index，不上传代码到服务器。RAG-based AI 编码工具试图 embed 整个 codebase，但在大型活跃代码库中，embed pipeline 永远追不上工程师的 commit 速度 → 检索到的是几周前甚至几天前重命名过的函数。Agentic search 避免了索引陈旧，但代价是"足够好的起点 context"是必要条件——这正是 harness 5 层扩展点的设计目标。

## 五层扩展点（按构建顺序敏感度）

### 1. CLAUDE.md 文件（最先建）

每个会话自动加载的 context 文件。**根目录 CLAUDE.md 写全局图景，子目录 CLAUDE.md 写本地约定**。它们无条件加载到每个 session，所以**保持聚焦是性能前提**——写太多会拖累所有任务。

> "Because they load in every session regardless of the task, keeping them focused on what applies broadly will prevent them from becoming a drag on performance." — Anthropic Applied AI

### 2. Hooks（让 setup 自我改进）

多数团队把 hooks 视为"防止 Claude 做错事的脚本"，但更有价值的用途是**持续改进**：stop hook 在 session 结束时反思发生了什么、提议 CLAUDE.md 更新（趁 context 鲜活）；start hook 动态加载团队特定 context（让每位开发者按模块自动获得正确 setup）。linting/formatting 类自动检查用 hooks 比依赖 Claude 记忆指令更确定性。

### 3. Skills（按需加载专家知识，不污染每个 session）

大型代码库有几十种任务类型，不是所有专家知识都要在每个 session 出现。**Skills 通过 progressive disclosure 实现按需加载**：security review skill 只在 Claude 评估代码漏洞时加载；document processing skill 只在代码变更触发文档更新时加载。Skills 可按 path 范围绑定——支付服务团队的 deployment skill 只在那个目录自动加载，不会在 monorepo 其他地方误触发。

### 4. Plugins（把工作有效的 setup 打包分发）

大型代码库的难题是"好 setup 困在小团队内部"。**Plugin 把 skills + hooks + MCP 配置打包成可安装的包**——新工程师 day one 安装 plugin 就获得与老工程师相同的 context 和能力。**Plugin 更新通过 managed marketplace 跨组织分发**。一家大型零售组织在 Claude Code 广泛推广前，把内部 analytics 平台的 skill 打包为 plugin，先在业务分析师小范围试运行再放大。

### 5. MCP Servers（扩展到内部一切）

MCP servers 是 Claude 连接内部工具、数据源、API 的标准方式。最成熟的团队构建 MCP servers 把**结构化搜索暴露为 Claude 可直接调用的 tool**；其他团队连接内部文档、ticket 系统、analytics 平台。

### 附加：LSP + Subagents

- **LSP integrations**：给 Claude 同样的 IDE 导航能力（go to definition, find all references）—— 跨语言 codebase 中这是最高价值投资之一。一家企业软件公司在 Claude Code 推广前先全组织部署 LSP，专门为 C 和 C++ 导航可靠性。
- **Subagents**：分离"探索"和"编辑"。Read-only subagent 映射子系统的文件、写入发现到文件，然后主 agent 带着全图编辑。

## 三大反复出现的部署模式

### 模式 1：先投资 codebase 对 Claude 的"可读性"

Claude 的能力受限于"找到正确 context"的能力。**每个 session 加载太多 context 降低性能，context 太少则让 Claude 盲目导航**。最有效的部署前期投资让 codebase 对 Claude 可读：
- 层级化 CLAUDE.md
- Skills 按 path 范围绑定（避免误触发）
- LSP 提供 symbol-level 精度

### 模式 2：定期 harness 调整（3-6 个月一次）

> "As models evolve, instructions written for your current model can work against a future one. CLAUDE.md files that guided Claude through patterns it used to struggle with may either become unnecessary or actively constraining when the next model ships."

为当前模型写好的 CLAUDE.md 规则，可能在下一代模型时变成不必要甚至反约束——例如告诉 Claude 把每个 refactor 拆成单文件变更的规则，曾经帮早期模型保持正轨，但会阻止新模型做它擅长的跨文件协调编辑。**为模型特定限制做补偿的 skills 和 hooks 在限制消失后变成 overhead**（一个 Perforce codebase 中拦截 file write 强制 p4 edit 的 hook，在 Claude Code 增加原生 Perforce 模式后就冗余了）。**配置 review 每 3-6 个月做一次**——或者当主要模型发布后感觉性能 plateau 时做。

### 模式 3：组织层（不是技术配置）驱动采纳

技术配置 alone 不驱动采纳。**采纳最快的部署有专门的基础设施投资先于广泛访问**。小团队（甚至一个人）提前接好工具，让开发者首次接触 Claude 时就 fit 现有 workflow。一家公司几个工程师构建一套 plugins + MCPs 让 day one 可用；另一家公司整个团队专注管理 AI 编码工具，在 rollout 前把基础设施就位。**这两家公司的开发者首次体验都是 productive 而非 frustrating，采纳从此扩散**。

**今天做这些工作的团队通常在 Developer Experience 或 Developer Productivity 下**——这两个功能负责 onboarding 新工程师和构建开发者工具。**多个组织出现新角色：agent manager**——一个 PM/工程师混合岗位，专注管理 Claude Code 生态。

## 最小可行版本：单一 DRI

**没有专门团队的组织，最小可行版本是一个 DRI（Directly Responsible Individual）**：
- 拥有 Claude Code 配置所有权
- 有权决定 settings、permissions policy、plugin marketplace、CLAUDE.md 约定
- 负责让它们保持 current

**自下而上的采纳能产生热情但容易碎片化**——必须有个人或团队组装、传播正确的 Claude Code 约定（标准化的 CLAUDE.md 层级、curated 的 skills 和 plugins 集）。**没有这个工作，知识留在 tribal 状态，采纳会 plateau**。

## 治理与跨职能工作组

在大型组织（特别是受监管行业），治理问题早期就出现：
- 谁控制哪些 skills 和 plugins 可用
- 如何防止数千工程师独立重建相同的东西
- 如何确保 AI 生成代码与人类生成代码走同样 review 流程

**建议从有限初始访问 + 已批准 skills 集 + 必要 code review 流程开始**，随信心建立扩展。**最顺利的部署在早期建立跨职能工作组**——把工程、信息安全、治理代表聚在一起，共同定义需求、构建 rollout 路线图。

## 配套 Project 闭环：`jeremylongshore/claude-code-plugins-plus-skills` (2,390⭐ MIT)

[Project 文件](articles/projects/jeremylongshore-claude-code-plugins-plus-skills-marketplace-2026.md) 是 Anthropic 5 扩展点框架的开源 marketplace 工程化身：
- **425 plugins + 2,810 skills + 200 agents** for Claude Code
- Open-source marketplace at tonsofskills.com
- ccpi CLI package manager
- License: MIT
- Topics 直接命中目标生态：`claude-code`、`anthropic`、`mcp`、`plugin-marketplace`、`skills`、`agent-skills`、`developer-tools`

**Pair 4-way SPM 满中**：
- **Layer 1 (cluster 共享)**：enterprise/practices cluster 共享
- **Layer 2 (SPM 关键词字面级)**：5 关键词共享 `Claude Code` / `skills` / `plugins` / `marketplace` / `MCP`
- **Layer 3 (target-ecosystem topics)**：`claude-code` + `anthropic` + `mcp` + `plugin-marketplace` 4 个间接命中
- **Layer 4 (维度互补)**：Article = "Applied AI 团队方法论"（抽象层，5 扩展点框架）↔ Project = "开源 marketplace + CLI 工具"（具体实现层，425 plugins 实体库）= 抽象↔实现强互补

## 这个 Article 相对历史 R-N 的位置

`articles/practices/` 既有文章覆盖：
- Anthropic April 2026 postmortem 配置降级
- Anthropic data analytics agent context-not-generation
- Anthropic harness design long-running apps
- Cursor self-hosted cloud agents
- OpenAI harness engineering codex
- Azure developer CLI azd local agent
- MCP enterprise infrastructure
- Microsoft agent governance

**结构空白填补**："5 扩展点框架（CLAUDE.md/hooks/skills/plugins/MCP）+ agent manager 角色 + DRI 最小可行版本 + 3-6 个月 harness review 周期" = **0 命中 cluster 内 0→1 启动**。这一框架从"机制层"（5 个具体扩展点的工程化）跃升到"组织层"（agent manager / DRI / 跨职能工作组）——是 practices cluster 首次系统化披露"组织工程化"维度。

## 关键引用

- "The ecosystem built around the model—the harness—determines how Claude Code performs more than the model alone."
- "An emerging role in several organizations is an agent manager: a hybrid PM/engineer function dedicated to managing the Claude Code ecosystem."
- "Teams should expect to do a meaningful configuration review every three to six months."
- "Bottoms-up adoption generates enthusiasm but can fragment without someone to centralize what works."

## 致谢

**Anthropic Applied AI 团队**：Alon Krifcher, Charmaine Lee, Chris Concannon, Harsh Patel, Henrique Savelli, Jason Schwartz, Jonah Dueck, Kirby Kohlmorgen —— 分享他们在大规模部署 Claude Code 的一手经验。**Zoox 的 Amit Navindgi** 为本文提供反馈。这是 Anthropic Applied AI 与企业客户合作将模式转化为组织特定需求的第一手工程披露。

## 局限性

**适用边界**：本文假设**传统软件工程环境**（工程师是主要 codebase 贡献者、用 Git、代码遵循标准目录结构）。**非传统设置**（游戏引擎的大二进制资产、非传统版本控制的环境、非工程师贡献的 codebase）需要额外配置工作。**极端案例**（数十万文件夹、百万文件的 codebase；非 git 版本控制的 legacy 系统）将在本系列后续 installment 中单独讨论。
