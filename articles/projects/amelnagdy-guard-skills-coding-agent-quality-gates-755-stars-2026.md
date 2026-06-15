---
title: guard-skills：AI Coding Agent 的第二关质量门控
date: 2026-06-16
source: GitHub
project: amElnagdy/guard-skills
stars: 755
license: MIT
topics: [agent-skills, claude, claude-code, code-review, codex, skills-sh]
description: guard-skills 为 AI coding agent 提供五类质量门控（clean-code / test / docs / WordPress / WooCommerce），在 Agent 完成后运行第二关检查，捕捉系统性生成失败模式。
round: 398
cluster: ai-coding
cluster_role: complement
pair_article: articles/harness/anthropic-claude-code-auto-mode-dual-layer-permission-harness-2026.md
pair_reason: "Path C 互补配对：Auto Mode 是 Agent 权限判断的双层防御，guard-skills 是 Agent 产出质量的双层防御——一个管「能做什么」，一个管「做得对不对」，共同构成完整的 Agent Coding Harness 体系"
---

# guard-skills：AI Coding Agent 的第二关质量门控

> GitHub：[amElnagdy/guard-skills](https://github.com/amElnagdy/guard-skills) | 755⭐ | MIT License

## 核心命题

guard-skills 解决了一个被长期忽视的问题：**AI Agent 生成代码通过第一次检查后，缺乏第二关质量门控**。当你让 Agent 完成一个任务后，你会 review 它生成的代码——guard-skills 就是把这个 review 过程自动化，让 Agent 自己跑一遍质量门控再交付。

这不是给 Agent 增加限制，而是**在 Agent 完成后加一道质量门**：Agent 负责创作，Guard 负责审计，两者各司其职。

## 为什么值得推荐

### 第二关质量门控的理念

大多数 Agent 工具专注于「让 Agent 更好地工作」——更好的上下文、更好的工具、更强的推理。guard-skills 反其道而行：**在 Agent 工作完成后，提供一个独立的质量验证层**。

这个理念的核心洞察是：AI Agent 生成代码有一个系统性的失败模式分布——不是随机错误，而是有规律的、可以捕捉的类型错误。guard-skills 的五个 Guard 就是针对这些规律性失败设计的：

| Guard | 针对的操作 | 捕捉的系统性失败 |
|-------|-----------|----------------|
| `clean-code-guard` | 任何语言的生成代码 | LLM 特有的代码味道：错误吞掉、硬编码成功返回、幻觉 API、过早抽象、注释污染 |
| `test-guard` | 测试代码 | Mock 滥用、重复测试体、无效断言、测试捕获空操作 |
| `docs-guard` | README、API 文档、教程 | 文档与代码不一致、幻觉符号、无效示例 |
| `wp-guard` | WordPress 插件/主题/ REST | 安全漏洞（escaping/sanitization/nonce）、数据库查询错误 |
| `woo-guard` | WooCommerce 扩展 | HPOS 破坏、支付漏洞、订单逻辑错误 |

每个 Guard 都不是泛泛的质量检查，而是**针对特定领域已知失败模式的专业规则集**。

### 专门处理 LLM 特有的代码问题

这是 guard-skills 最独特的价值。传统代码审查工具（ESLint、PHPUnit 规则等）专注于人类程序员的错误模式。guard-skills 额外增加了一层专门针对 AI 生成代码的质量规则：

- **重复生长**：Agent 在每次迭代中向代码库添加重复逻辑
- **包幻觉**：Agent 引用不存在的 npm/PyPI 包
- **假装成功**：Agent 报告测试通过但实际测试什么都没捕获
- **错误吞掉**：`try/catch -> return ok` 模式，优雅地隐藏了失败

> "catch-all error swallowing, hardcoded 'success' returns, hallucinated APIs, premature abstraction, comment pollution, and copy-from-similar bugs"

这些是 AI 生成代码特有的失败模式，传统的静态分析工具无法捕捉，因为它们不是「语法错误」，而是「语义习惯错误」。

### 与主流 Agent 工具的兼容性

guard-skills 通过 [skills.sh](https://github.com/vercel-labs/skills) CLI 分发，与当前主流 Agent 工具集成：

```bash
# 安装全部 Guard
npx skills add amElnagdy/guard-skills

# 针对特定 Agent 安装
npx skills add amElnagdy/guard-skills --skill test-guard --agent claude-code
npx skills add amElnagdy/guard-skills --agent codex
npx skills add amElnagdy/guard-skills --agent cursor
```

支持的 Agent：Claude Code、Codex、Cursor、OpenCode，以及其他通过 Skills CLI 集成的 Agent。安装后，Agent 可以通过 `$clean-code-guard`、`$test-guard` 等指令调用对应的质量门控。

### 与 R397 Anthropic 文章的关联

R397 探讨了 Anthropic 关于 Agentic Coding 团队规模化的方法论（Super Users → Hackathon → 内部专家）。guard-skills 直接对应了这个方法论的**第三阶段（内部专家沉淀）**：当团队有多人使用 Agent 时，需要把「专家的质量判断」固化成可重复的质量门控，而不是每次靠人工 review。

## 使用方式

### 作为第二关运行（推荐）

让 Agent 完成工作后，用 Guard 做质量门控：

```text
Use $clean-code-guard on the diff you just produced.
Use $test-guard on the tests you just wrote.
Use $docs-guard on this README update before we ship it.
```

### 作为主动约束（较少使用）

当你想在写作时就约束 Agent 行为时：

```text
Use $wp-guard while implementing this REST endpoint, then self-check before delivery.
```

## Pair 配对分析

| 维度 | 评估 |
|------|------|
| 主题关联性 | ⭐⭐⭐⭐⭐（Claude Code Auto Mode 权限判断 ↔ guard-skills 质量门控）|
| 互补性 | ⭐⭐⭐⭐⭐（Auto Mode 管「能做什么」，Guard 管「做得对不对」）|
| License | ⭐⭐⭐⭐⭐（MIT，完全开源）|
| 工程机制稀缺性 | ⭐⭐⭐⭐（AI 生成代码特有的质量门控，领域稀缺）|

**Pair 强度**：⭐⭐⭐⭐⭐ 双层防御体系（权限 + 质量），共同构成 Agent Coding Harness 完整体系

## 与类似工具的对比

| 工具 | 定位 | guard-skills 的差异 |
|------|------|-------------------|
| ESLint / PHPUnit 规则 | 语法/风格检查 | guard-skills 额外处理 LLM 特有失败模式 |
| CodeRabbit / Cursor Review | AI 代码审查 | guard-skills 是轻量级 Guard 系统，可本地运行，不依赖外部服务 |
| Claude Code Auto Mode | 权限判断 | Auto Mode 管「执行前」，Guard 管「完成后」——两个方向互补 |

## 适用场景

- **团队使用多个 coding agent**：需要统一的质量标准
- **高风险代码生成**：金融、医疗、法律等需要对 AI 生成代码做额外审计的领域
- **WordPress / WooCommerce 开发**：专门的领域 Guard 覆盖常见安全漏洞
- **持续集成**：在 CI 中跑 Guard 作为自动化质量门控

## 如何快速上手

```bash
# 查看可用的 Guard
npx skills add amElnagdy/guard-skills --list

# 安装完整包
npx skills add amElnagdy/guard-skills

# 对 Claude Code 的产出跑质量门控
# 在 Claude Code 对话中：
Use $clean-code-guard on the diff.
Use $test-guard on the tests.
```

---

*amElnagdy/guard-skills | 755⭐ | MIT | [GitHub](https://github.com/amElnagdy/guard-skills) | Skills CLI 集成*