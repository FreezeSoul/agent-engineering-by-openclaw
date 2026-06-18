---
title: "jeremylongshore claude-code-plugins-skills marketplace 2026"
date: 2026-06-18
stars: 2390
license: MIT
source: https://github.com/jeremylongshore/claude-code-plugins-plus-skills
cluster: projects
tags: [claude-code, marketplace, plugins, skills, agents, mcp, open-source, harness-extension-points]
pair_article: articles/practices/anthropic-large-codebase-claude-code-five-extension-points-2026.md
---

# jeremylongshore/claude-code-plugins-plus-skills

> **5 扩展点的开源 marketplace 工程化身** — Anthropic 大型代码库部署指南的工程配套
> ⭐ 2,390 | MIT License | Topics: `claude-code` `anthropic` `mcp` `plugin-marketplace` `skills` `agent-skills` `developer-tools`
> 配套 Article: [Anthropic 大代码库 Claude Code 五大扩展点 2026](../practices/anthropic-large-codebase-claude-code-five-extension-points-2026.md)

## 项目一句话定位

**425 plugins + 2,810 skills + 200 agents for Claude Code**，配合开源 marketplace（tonsofskills.com）和 ccpi CLI package manager，是 Anthropic 2026-05-14 发布的《How Claude Code works in large codebases》中**5 扩展点框架（CLAUDE.md / hooks / skills / plugins / MCP）的最大规模开源工程化身**。

## 4-way SPM 配对强度

| 层 | 信号 | 强度 |
|----|------|------|
| **Layer 1 (cluster 共享)** | `practices` cluster — AI coding 大规模部署方法论 | ⭐⭐ |
| **Layer 2 (SPM 关键词字面级)** | 5 关键词共享：`Claude Code` / `skills` / `plugins` / `marketplace` / `MCP` / `agents` | ⭐⭐⭐⭐⭐ |
| **Layer 3 (target-ecosystem topics)** | 4 间接命中：`claude-code` `anthropic` `mcp` `plugin-marketplace` `skills` | ⭐⭐⭐⭐⭐ |
| **Layer 4 (维度互补)** | Article = "Applied AI 团队方法论层（5 扩展点框架 + agent manager + DRI）" ↔ Project = "开源 marketplace + ccpi CLI 工具层（425 plugins 实体库）" | 抽象↔实现强互补 |

**综合判定**：⭐⭐⭐⭐⭐ 4-way SPM 满中（R375/R383/R397/R401/R406/R410 第七次连续实战满中）。

## 项目核心数据

- **仓库规模**：425 plugins + 2,810 skills + 200 agents
- **License**：MIT（清洁，R364 #8 协议一次 API 调用确认 spdx_id）
- **创建时间**：2025-10-10（运行 ~8 个月）
- **Stars 增长**：2,390⭐（2026-06-18）—— 中等偏高 signals
- **Topics 标签**：`claude-code` `claude-code-plugins` `anthropic` `mcp` `plugin-marketplace` `plugin-system` `agent-skills` `developer-tools` `devops` `llm` `marketplace` `skills` `automation` `ai-agents` `ai` `saas`

## 与 Article 的闭环对位

**Article 5 扩展点 → Project 工程化体现**：

| Anthropic 5 扩展点（Article） | jeremylongshore 实体实现（Project）|
|-------------------------------|--------------------------------------|
| **1. CLAUDE.md**（context 文件） | 配套的 CLAUDE.md templates + 每个 plugin 自带 example CLAUDE.md |
| **2. Hooks**（自我改进脚本） | Plugin hooks 仓库统一管理，可通过 ccpi CLI 安装/更新 |
| **3. Skills**（progressive disclosure） | **2,810 skills** — 正是 Article 描述的"按需加载"工程化最大集合 |
| **4. Plugins**（可安装包） | **425 plugins** — 每个 plugin bundle skills + hooks + MCP configs |
| **5. MCP Servers**（连接内部一切） | 配套 marketplace 含多个 MCP server 模板（anthropic/figma/github/slack 等） |

**附加对位**（Article 提到的"managed marketplace"概念）：tonsofskills.com 就是 Article 倡导的"plugin 跨组织分发"机制的开源实现。

## 关键引用

> "An emerging role in several organizations is an agent manager: a hybrid PM/engineer function dedicated to managing the Claude Code ecosystem."
> — Anthropic Applied AI 团队

> "Bottoms-up adoption generates enthusiasm but can fragment without someone to centralize what works."
> — Anthropic Applied AI 团队

**jeremylongshore 项目的实际价值**：把"agent manager 角色的工作产出"沉淀为可版本化、可分发的 marketplace —— 让中小组织无需专职 agent manager 也能获得集中化的 skills/plugins 集。

## Pair 强度判定（4-way）

R375 #34 协议 + R401 #41 协议硬化算法（7 次连续实战满中）。本 Pair 通过：
1. **cluster 共享**（⭐⭐）：practices cluster — AI coding enterprise methodology
2. **SPM 字面级**（⭐⭐⭐⭐⭐）：5 个核心关键词共享
3. **target-ecosystem topics**（⭐⭐⭐⭐⭐）：claude-code + anthropic + mcp + plugin-marketplace 多个间接命中
4. **维度互补 ≠ 重叠**（确认）：Article = 抽象方法论（5 扩展点框架 + 组织工程化）↔ Project = 具体 marketplace 实体（425 plugins 实体库）= 抽象↔实现

## License 验证

- API 验证时间：2026-06-18
- 验证方式：`curl -s https://api.github.com/repos/jeremylongshore/claude-code-plugins-plus-skills | grep spdx_id`
- 结果：spdx_id = "MIT"
- 判定：清洁开源 License，可直接收录

## 反模式警告

**反模式**（R393 #33 验证）：把"plugin marketplace 仓库"误归类为"AI 应用层" → 错过"它是 5 扩展点框架的工程化身"这一定位。**正确路径**：本仓库的真正价值不是"有什么 plugins"（那是 marketplace 数据），而是"它是 Article 倡导的 plugin/hook/MCP 集中化分发模式的工程实现"。

## 战略意义

R401 期间 antigravity-awesome-skills（40,807⭐）揭示了"个人开发者 curated skills 集"的爆发式增长，R432 jeremylongshore-claude-code-plugins-plus-skills 揭示了"**集中化 marketplace + CLI package manager 工具链**"的工程化方向——两者互补：**前端 curated discovery + 后端 CLI 工具链分发**。R432 的 Article 框架（5 扩展点 + agent manager + DRI + 3-6 个月 review 周期）正是连接两者的**方法论桥梁**。
