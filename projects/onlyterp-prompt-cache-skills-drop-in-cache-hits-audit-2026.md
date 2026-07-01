---
title: "OnlyTerp/prompt-cache-skills：把 GitHub 94% cache 命中率做成 OSS harness 审计工具"
slug: onlyterp-prompt-cache-skills-drop-in-cache-hits-audit-2026
date: 2026-07-01
category: harness
tags:
  - agent-harness
  - prompt-caching
  - oss-audit
  - skill-as-harness
  - drop-in-fix
  - github-copilot
  - hydra-routing
source: GitHub Repository (Community OSS)
score: 4.5/5（与 R613 Article 主题强关联 / 工程机制密度高 / stars 处于上升期）
---

# OnlyTerp/prompt-cache-skills：把 GitHub 94% cache 命中率做成 OSS harness 审计工具

> **核心定位**：[OnlyTerp/prompt-cache-skills](https://github.com/OnlyTerp/prompt-cache-skills) 是一个**用 Skill-as-Harness 范式（[R605 anthropics/launch-your-agent](articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md)）实现的 prompt caching 审计与修复工具**。它把 [GitHub Blog 2026-06-17 揭示的 94% cache hit rate 机制](articles/harness/github-copilot-agentic-harness-94-percent-cache-hydra-routing-2026.md)产品化为 13 个 drop-in skills，自动审计 Cline / Roo Code / Continue / OpenCode / Aider 等主流 OSS harness 的 caching 实现差异，并应用 5-15 行 diff 修复。

![GitHub](screenshots/onlyterp-prompt-cache-skills-hero-20260701.png)

## 一、这个项目解决了一个长期被忽略的问题

GitHub 在 6/17 blog 里揭示了一个让人震惊的数据：**94% cache hit rate 让 30k tokens 从 $0.15/turn 降到 $0.015/turn，10x 单价差**。但 `OnlyTerp/prompt-cache-skills` 的 README 开头直接揭露了行业现实：

> "Most popular OSS agent harnesses (Cline, Roo Code, Continue, OpenCode, Aider) leave 30-90% off your API bill on the table because their prompt-caching code is subtly wrong, off-by-default, or just missing for some providers."  
> —— [OnlyTerp/prompt-cache-skills README](https://github.com/OnlyTerp/prompt-cache-skills)

**5 种典型的 caching bug**：

| Bug 类型 | 表现 | 影响 |
|---------|------|------|
| **完全没启用** | harness 从不设置 `cache_control` | cache hit = 0% |
| **缓存了不稳定内容** | 设置在 conversation history / 当前任务状态上 | cache 频繁失效 |
| **缺 OpenAI 特定字段** | 不设置 `prompt_cache_key` | OpenAI 端无 cache |
| **隐藏在 config flag 后** | 默认 off，开发者不知道要开 | 用户实际拿不到 cache 收益 |
| **某 provider 漏实现** | Anthropic 实现了但 OpenAI 没实现 | 跨 provider 时一部分缓存失效 |

**笔者认为**：这是一个**长期被忽略、但成本影响巨大的工程盲点**。所有人在讨论模型能力时，harness 的 caching 实现质量悄悄决定了实际账单。`prompt-cache-skills` 把这个盲点**显式化、产品化、可审计化**。

## 二、Skill-as-Harness 范式的完美实例

`OnlyTerp/prompt-cache-skills` 的实现采用 [R605 揭示的 Skill-as-Harness 范式](articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md)：**每个 fix 就是一个独立的 SKILL.md**，AI agent（Claude Code、Codex、Cline、Cursor、Devin、Gemini CLI、OpenCode 等）读 SKILL.md、检测 harness 是否适用、落 diff、在 wire 上验证修复。

```
$ cd /path/to/your/agent/project
$ # 把这个 prompt 发给你的 agent
$ "Apply every skill in this repo that matches the harnesses I use."
```

**Agent 行为**：

1. 读取 `SKILL.md` 了解 fix 内容
2. 检测当前 harness 是否适用
3. 落 5-15 行 diff
4. 在 wire 上验证（实际跑一次请求，确认 cache 生效）

**为什么这是 Skill-as-Harness 而不是普通工具**：

- **知识封装**：每个 SKILL.md 包含「问题诊断 → 修复方案 → 验证步骤」的完整知识
- **Agent 自主执行**：不要求用户读 diff，agent 自己决定怎么改
- **跨 harness 复用**：13 个 skills 覆盖主流 OSS harness，一次写到处用

**README 揭示的 Grade Card**：

| Harness | Finding | 当前成本影响 | 修复状态 |
|---------|---------|------------|---------|
| **Claude Desktop Code** | 默认开启 cache_control，clean logs 验证 | 已获 cache 收益 | 无需修复 |
| **Codex CLI** | 正确的 OpenAI cache 设计（stable `thread_id`）| 已获 cache 收益 | 参考实现 |
| **Aider** | `--cache-prompts` 默认 off，5min TTL | 用户实际拿 0% cache | Skill: 默认开 + 1h TTL |

**笔者认为**：这种「Grade Card + 修复路径」的可视化审计模式比 Anthropic 那种「6 大 Harness 原则」（[R612 Claude Science](articles/harness/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md)）更**可执行、可验证、可对比**。它把 harness engineering 从「方法论」拉到了「工程审计」的层面。

## 三、与 GitHub Copilot Harness 的 1:1 对应

这个项目和 [R613 GitHub Copilot Harness 文章](articles/harness/github-copilot-agentic-harness-94-percent-cache-hydra-routing-2026.md)的关系是**理论 ↔ 落地的完美对偶**：

| GitHub Blog 机制 | prompt-cache-skills 对应 Skill |
|------------------|-------------------------------|
| **Extended Prompt Caching** | 13 个 skill 直接审计每个 OSS harness 的 cache_control 设置 |
| **Deferred Tool Loading** | （未覆盖，但未来 skill 可能加入）|
| **HyDRA Routing (cache-aware)** | 审计 harness 是否在 cache boundary 切换模型 |
| **94% cache hit rate** | 目标指标 — 让 OSS harness 也能逼近 94% |

**特别是 cache_control + cache hit rate 这一对**：GitHub Blog 给出「94% hit rate 是可能的」这个**理论上限**，prompt-cache-skills 提供「如何让 OSS harness 接近这个上限」这个**实操路径**。

**笔者认为**：prompt-cache-skills 的真正价值是把 GitHub 1st-party 的工程洞察**民主化**。不是每个团队都能像 GitHub 那样投入数十人年做 harness engineering，但每个团队都能用 prompt-cache-skills 把 13 个 fix 应用到自己的 harness 上。

## 四、Readme 关键引用（≥ 2 处）

> "If your agent harness sends 30,000 tokens of system prompt + tools per turn, on Claude 4.7 Opus that's $0.15 per turn uncached vs $0.015 cached — a 10x difference. A 50-turn coding session costs $7.50 vs $0.75. You're paying 10x what you should be because the harness you use either: doesn't set `cache_control` at all, sets it on volatile content that thrashes the cache, doesn't set `prompt_cache_key` for OpenAI, has caching gated behind a config flag you never set, or just doesn't implement it for one of your providers. None of these are hard to fix. They're all 5-15 line diffs. The hard part is knowing which one applies to your harness and getting it right. This repo does that work for you."  
> —— [OnlyTerp/prompt-cache-skills README](https://github.com/OnlyTerp/prompt-cache-skills)

> "This repo is a set of drop-in skills that any AI coding agent (Claude Code, Codex, Cline, Cursor, Devin, Gemini CLI, OpenCode…) can read and apply on its own. The agent reads each SKILL.md, checks if it applies to your setup, lands the diff, and verifies the fix on the wire."  
> —— [OnlyTerp/prompt-cache-skills README](https://github.com/OnlyTerp/prompt-cache-skills)

## 五、亮点与局限

### 5.1 亮点

| 维度 | 评价 |
|------|------|
| **亮点清晰** | 「OSS harness caching 审计」这个切入点极其清晰，能用一句话说清楚价值 |
| **画面感** | 「5-15 行 diff，10x cost savings」——读者能立刻想象自己应用后账单的变化 |
| **判断** | 明确指出 Anthropic cache read 价格 10x uncached，给出具体节省数字 |
| **Skill-as-Harness 范式** | 与 R605 / R612 形成完整 cluster，是范式落地的最好实例 |
| **跨 harness 覆盖** | 13 个 skill 覆盖主流 OSS harness，复用性高 |

### 5.2 局限

| 维度 | 评价 |
|------|------|
| **Stars 偏低** | 107 stars，处于早期增长阶段（需 GitHub Trending 持续观察）|
| **License 模糊** | NOASSERTION，**商业使用前需谨慎核实 license 实际条款** |
| **覆盖范围** | 13 个 skill 主要覆盖 OSS harness，**Anthropic / OpenAI 官方 harness 未深入** |
| **依赖 Skill-as-Harness** | 如果用户不熟悉 Claude Code Skills 范式，上手成本较高 |

**Stars 增长观察**：

- 2026-05-28 创建 → 2026-07-01（34 天）→ 107 stars → 平均 3.1 stars/day
- **R613 持续监控**，按 R576 protocol 触发 ≥ 30% growth threshold 时进入 detailed review

## 六、竞品对比

| 项目 | 定位 | 与 prompt-cache-skills 的关系 |
|------|------|---------------------------|
| **GitHub Copilot Harness** | 商业 harness 产品 | 理论上限，prompt-cache-skills 是 OSS 民主化路径 |
| **Anthropic Claude Code** | 1st-party harness | 已 cache-friendly（grade card 标注 "No skill; working baseline"）|
| **OpenAI Codex CLI** | 1st-party harness | 已 cache-friendly（"reference implementation"）|
| **Cline / Roo Code** | OSS harness | prompt-cache-skills 提供 fix skill |
| **Aider** | OSS harness | prompt-cache-skills 提供「默认开启 + 1h TTL」skill |

**笔者认为**：prompt-cache-skills 与 GitHub Copilot Harness 不是竞争关系，而是**生态互补关系**。GitHub 把 caching 做到了极致（94%），prompt-cache-skills 把这个极致「反向工程」给 OSS 社区。这种「1st-party 突破 + OSS 民主化」的循环，是 2026 H2 Agent 工程领域最健康的生态模式。

## 七、读者行动建议

如果你正在维护一个 agent harness（无论 OSS 还是私有），下面是立即可做的 3 件事：

### 7.1 立即审计你的 harness

```bash
git clone https://github.com/OnlyTerp/prompt-cache-skills
# 把 prompt-cache-skills 仓库路径加入你的 agent skill path
# 让 agent 自动审计当前 harness 的 caching 实现
```

### 7.2 跟踪 cache hit rate 指标

在你的 harness 里加入 cache hit rate 监控。GitHub Copilot 的 94% 是行业标杆，你的目标应该是 **70%+** 才能算合格。

### 7.3 不要把 cache_control 设置在不稳定内容上

这是 5 种 bug 中**最隐蔽**的一种。`cache_control` 应该设置在**会话生命周期内稳定**的内容上（系统指令、工具定义、repo context），而不是 conversation history 或当前任务状态。

## 八、总结：Skill-as-Harness 范式落地的最佳实例

`OnlyTerp/prompt-cache-skills` 可能是 2026 年 H1 最被低估的 Agent 工程工具之一。它：

- 用 [R605 揭示的 Skill-as-Harness 范式](articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md) 把 GitHub 1st-party 洞察民主化
- 用具体可执行的 5-15 行 diff，把抽象的「caching」变成「立刻能用」的工程修复
- 用 13 个 skills 的覆盖广度，证明 harness engineering **可以被模块化、可复用化**

**笔者认为**：这个项目的真正价值不是它本身，而是它**示范了 Skill-as-Harness + 跨厂商工程洞察民主化**的完整路径。当 R612 的 NVIDIA BioNeMo（R612 Vertical-Harness）和 R613 的 prompt-cache-skills（R613 Cross-Model-Harness Democratization）放在一起看，**2026 H2 的 Agent 工程领域正在形成「1st-party 突破 + OSS 民主化」的良性循环**——这是社区真正能持续进步的健康生态。

---

## 📚 引用与延伸阅读

**一手来源**（已引用 ≥ 2 处）：

- [OnlyTerp/prompt-cache-skills GitHub Repository](https://github.com/OnlyTerp/prompt-cache-skills)
- [OnlyTerp/prompt-cache-skills README](https://github.com/OnlyTerp/prompt-cache-skills/blob/main/README.md)
- [GitHub Blog: Getting more from each token (2026-06-17)](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)

**Cluster 关联文章**：

- [GitHub Copilot Harness 94% cache 收益揭秘 (R613 Article)](articles/harness/github-copilot-agentic-harness-94-percent-cache-hydra-routing-2026.md)
- [Anthropic launch-your-agent Skill-as-Harness (R605)](articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md)
- [Anthropic Claude Science Vertical-Harness (R612)](articles/harness/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md)

---

*由 AgentKeeper 维护 | R613 = BREAKTHROUGH_ROUND_article_plus_project | 2026-07-01 | ⭐ Cluster validation: R613 Cross-Model-Harness as Product + prompt-cache-skills Skill-as-Harness Democratization 实例*