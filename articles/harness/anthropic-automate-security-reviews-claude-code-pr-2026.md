---
title: "Claude Code 安全审查自动化：内层命令 + 外层 Action"
cluster: harness
slug: anthropic-automate-security-reviews-claude-code-pr-2026
date: 2026-06-16
source: https://claude.com/blog/automate-security-reviews-with-claude-code
pair_project: anthropics-claude-code-security-review-5269-stars-2026
tags: [security, claude-code, github-action, dev-workflow, pr-review, automated-review]
---

# Claude Code 安全审查自动化：`/security-review` 命令与 GitHub Action 的双层部署

> 📅 2026-06-16 | 🔗 [原文](https://claude.com/blog/automate-security-reviews-with-claude-code) | 🏷️ harness / security / dev-workflow

---

## 核心论点

Anthropic 把"AI 写代码"推到生产级之后，下一个必然问题是**"AI 写出来的代码谁审"**。他们给出的工程答案是**双层自动化部署**：

- **开发内循环**：`/security-review` slash command —— 在 `git commit` 之前本地触发，针对 staged diff 跑安全模式扫描
- **团队外循环**：GitHub Action —— 在 PR 打开时自动分析每一个 PR，作为团队基线审查关卡

两层叠加的工程哲学是：**"把安全审查塞进开发者每天已经在用的工作流里，而不是再开一个新工具"**。

> 「This creates a consistent security review process across your entire team, ensuring no code reaches production without a baseline security review.」

## 为什么是"自动化"而不是"提示审批"？

Anthropic 已经验证的路径是：依赖"逐条权限弹窗"的开发者终将进入**审批疲劳（approval fatigue）**。一旦开发者习惯性地点"Allow"，整个权限系统的安全保证就崩塌了。

`/security-review` 与 GitHub Action 走的是相反的路径——**把安全分析也变成 LLM 自动行为，不需要开发者主动决策**。Claude 在扫描 diff 时，会按 security-focused prompt 检查常见的漏洞模式（OWASP Top 10、CWE Top 25 等）。

## `/security-review` 命令：开发内循环

### 工作机制

```bash
# 在 Claude Code REPL 中运行
/security-review
```

Claude 会：

1. **搜索代码库**：定位可能被当前 diff 影响的文件
2. **运行专用安全 prompt**：覆盖常见的漏洞模式（注入、SSRF、反序列化、路径穿越、敏感信息泄露等）
3. **输出详细解释**：对每个发现的问题给出根因和修复建议
4. **可执行修复**：开发者可以直接让 Claude 实现修复

### 关键工程价值

| 价值 | 解释 |
|------|------|
| **不离开开发循环** | 开发者写完代码 → 跑命令 → 看结果 → 改。整个流程在 IDE 内完成。 |
| **早期捕获** | 在 commit 之前发现漏洞，修复成本远低于 PR review 阶段。 |
| **可重复** | 每次跑命令都按相同 prompt 扫描，团队基线一致。 |

## GitHub Action：团队外循环

### 工作机制

```yaml
# .github/workflows/security-review.yml
name: Claude Code Security Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  security-review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-security-review@main
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Action 在 PR 打开/更新时**自动触发**，无需人工干预：

1. 读取 PR diff
2. 调用 Claude API 做安全分析
3. 在 PR 评论中输出 findings
4. 与现有 CI/CD 流水线无缝集成

### 关键工程价值

- **团队一致性**：所有 PR 都经过同一基线审查，无人绕过
- **可定制**：可以根据团队安全策略调整 prompt
- **零配置启动**：Anthropic 官方维护，默认 prompt 已覆盖 80% 常见漏洞

## 真实案例：Anthropic 自己的代码

Anthropic 在 blog 中披露了 GitHub Action 在 Anthropic 内部代码上发现的两个真实漏洞：

### 案例 1：DNS rebinding → RCE

> 一个内部工具的新功能依赖启动一个**只接受本地连接**的 HTTP server。GitHub Action 自动识别出：通过 **DNS rebinding 攻击**，这个 server 实际上可以被远程利用，执行任意代码。

漏洞在 PR 合并之前被捕获。如果没拦截，这个漏洞会进入 Anthropic 内部生产系统。

### 案例 2：SSRF on 内部凭证代理

> 一个工程师构建了一个代理系统来安全管理内部凭证。Action 自动标记出这个代理存在 **SSRF 攻击**风险，团队立即修复。

这两个案例的共同模式：**都是开发者"以为安全"的代码**——本地监听、代理隔离——但通过具体攻击向量（DNS rebinding、SSRF）暴露了真实风险。**仅靠人工 code review 很难捕获这些细节，因为攻击向量的细节需要专门的安全知识**。

## `/security-review` 与 GitHub Action 的协同

| 维度 | `/security-review` 命令 | GitHub Action |
|------|--------------------------|----------------|
| **触发时机** | commit 之前（开发者主动） | PR 打开/更新（自动） |
| **执行环境** | 本地 Claude Code | GitHub-hosted runner |
| **捕获窗口** | 个体开发内循环 | 团队协作外循环 |
| **覆盖范围** | 当前 diff + 相关上下文 | 当前 PR diff |
| **修复路径** | 开发者直接让 Claude 修复 | PR 评论 + 后续 commit |

**双层叠加 = 防御纵深**：内循环捕获开发者主动审查的部分，外循环兜底（防止开发者跳过手动审查 + 提供团队一致基线）。

## 与现有 security cluster 文章的维度差异

本仓库 `articles/harness/` 已有 159+ 篇安全相关文章。它们的覆盖维度：

| 既有维度 | 代表文章 |
|---------|---------|
| **沙箱隔离** | `anthropic-claude-code-sandboxing-containment-2026.md` |
| **OS 层隔离** | `anthropic-claude-code-sandboxing-os-level-isolation-2026.md` |
| **三层层防御** | `anthropic-containment-three-layer-defense-2026.md` |
| **Managed Agents Vault** | `anthropic-managed-agents-security-boundary-credential-vault-2026.md` |
| **Auto-mode 双层权限** | `anthropic-claude-code-auto-mode-dual-layer-permission-harness-2026.md` |
| **静态安全扫描器** | `agent-audit-static-security-scanner-llm-agents.md` |

**本文填补的结构性空白**：

> **"AI 在写代码时直接做安全审查"** —— 不同于沙箱隔离（运行时防护）、Vault（凭证隔离）、Auto-mode（权限架构），这是**代码生成侧的纵深防御**。让 AI 在产出代码的同时主动审查代码，形成"AI 生成 + AI 审查"的闭环。

## 对其他 LLM Coding 工具的可迁移性

`/security-review` 的核心模式是 **"slash command + 专用 security prompt"**。这个模式可以推广到：

- **Cursor**：自定义 `.cursorrules` 中的 security review 模式
- **Codex CLI**：custom slash command + security-focused prompt
- **Continue.dev**：自定义 slash command
- **Aider**：通过 `/security` 类似命令触发

**关键洞察**：security review 不必是 Anthropic 专属能力。**模式是普适的，prompt 是关键**。一个团队只要把"OWASP Top 10 + CWE Top 25 + 内部安全规范"写进 system prompt，任何 LLM coding 工具都能获得这个能力。

## 局限与未解决问题

1. **LLM 误报**：可能把正常代码标记为漏洞，需要开发者判断
2. **LLM 漏报**：复杂漏洞链可能不被识别，不能替代专业安全审计
3. **上下文长度限制**：超大型 PR 可能需要分块扫描
4. **Prompt 注入风险**：恶意代码可能试图通过 commit message / diff 内容操纵 Claude

## 实战推荐

对于 2026 年的 LLM Coding 团队，**双层部署应该是默认配置**：

1. **在 CLAUDE.md 中强制 `/security-review`**：每次重要 commit 前运行
2. **在所有 repo 启用 GitHub Action**：作为 CI 的一部分
3. **配合传统安全工具**：不替代 SAST/DAST，而是补充
4. **定期 review Claude 的 findings**：建立团队对 LLM 安全审查能力的校准

## 一句话总结

> **Claude Code 安全审查不是"让 AI 替换安全审计师"，而是"让 AI 在每一次 commit 时都做一次 30 秒的安全自检"**。把安全审查嵌入开发者的日常工作流，比再加一个独立的"安全工具"更有效。
