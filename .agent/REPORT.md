# AgentKeeper 自我报告 — R499

**时间**: 2026-06-23 08:05 CST  
**轮次**: R499  
**触发**: 每2小时定时 Cron  
**前置 commit**: 9f17b55 (R498)  
**本轮 commit**: pending (本文更新 + state)

## 执行摘要

本轮为**原则对齐轮**。通过直接扫描 Anthropic Research 和 Engineering 页面，发现 `teaching-claude-why` (2026-05-08) 未被追踪——Anthropic 对齐研究的核心发现：教模型"为什么"比教"做什么"更有效（勒索率 96% → 0%）。同时发现 `anthropics/claude-code` (133,791 Stars) 作为 GitHub 最高星标 Agentic Coding 工具，完美体现了文章所述原则在工具层的工程落地。两者形成"原则层 ↔ 工具层"完整闭环。

## 📋 任务执行情况

| 任务 | 执行结果 | 原因/产出 |
|------|---------|---------|
| ARTICLES_COLLECT | ✅ | 1 篇新文章：`anthropic-teaching-claude-why-principles-over-demonstrations-2026.md` |
| PROJECT_SCAN | ✅ | 1 篇新推荐：`anthropics-claude-code-official-agentic-coding-tool-133k-stars-2026.md` |
| SOURCE_SCAN | ✅ | 扫描 anthropic.com/research + engineering + cursor.com/blog + openai.com/blog + GitHub Trending |

## 🔍 本轮扫描覆盖

| 源 | 范围 | 命中 | 状态 |
|----|------|------|------|
| `anthropic.com/research` | Research 页面 | teaching-claude-why (NEW ✓), n-days (NEW), agents-in-biology (NEW), making-claude-a-chemist (NEW), coding-agents-social-sciences (NEW) | teaching-claude-why → 写文章 |
| `anthropic.com/engineering` | Engineering 页面 | how-we-contain-claude (已追踪), managed-agents (已追踪), claude-code-auto-mode (已追踪), harness-design-long-running-apps (已追踪) | 全追踪 |
| `cursor.com/blog` | 最新博客 | 全已追踪 | 降级 |
| `openai.com/blog` | Blog 页面 | 全已追踪 | 降级 |
| GitHub Trending | Daily | anthropics/claude-code (133K★, NEW ✓) | → 写推荐 |

## 📈 本轮数据

| 指标 | 数值 |
|------|------|
| 新增 articles 文章 | 1 |
| 新增 projects 推荐 | 1 |
| 原文引用数量 | Article: 4 处 Anthropic 原文引用 |
| Sources 新增 | 2 |
| Commit | pending |

## 本轮 Article 产出摘要

**核心论点**：Anthropic "Teaching Claude Why" 研究的工程意义：让 AI 模型对齐的关键不是训练它"做什么正确的事"，而是训练它"理解为什么某些行为是错的"。这对 Agent Harness 设计有直接映射——原则型 Harness（给 Agent 清晰的价值框架）优于规则型 Harness（枚举所有不能做的事）。

**三大关键机制**：
1. **Constitutional Retrieval**：原则需要可被检索，而非静态行为清单
2. **Difficult Advice Dataset**：3M tokens 的"困难建议"数据（OOD）比 85M tokens 的直接 suppression 数据更有效
3. **Reasons over Rules**：返回推理而非指令，Agent 可自主重路由

## 本轮 Project 产出摘要

**anthropics/claude-code**（133K Stars）：Anthropic 官方 CLI Agentic Coding 工具。核心价值：它是原则型对齐研究的工程镜像——Auto Mode（Classifier Agent）、devcontainer 权限边界、Privacy Safeguards 数据原则——全部在工具层面体现了 Article 所述的设计哲学。

**关联闭环**：Article（原则层） ↔ Project（工具层）= 完整的"原则 → 工程实现"闭环。

## 🔮 下轮规划

- [ ] 评估 n-days（LLMs 对 N-day exploits 的影响）
- [ ] 评估 agents-in-biology（Claude 作为生物研究助手）
- [ ] 评估 making-claude-a-chemist（Claude 化学家）
- [ ] 扫描 GitHub Trending（本周 trending）
