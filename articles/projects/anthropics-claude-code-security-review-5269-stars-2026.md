---
project: anthropics/claude-code-security-review
stars: 5269
license: MIT
language: Python
created: 2025-08-04
updated: 2026-06-16
pair_article: articles/harness/anthropic-automate-security-reviews-claude-code-pr-2026.md
tags: [github-action, security, claude-code, pr-review, automated-review, anthropic-official]
---

# anthropics/claude-code-security-review (5,269⭐ MIT)

**GitHub**: https://github.com/anthropics/claude-code-security-review  
**Stars**: 5,269 (截至 2026-06-16)  
**License**: MIT  
**Language**: Python  
**Created**: 2025-08-04 | **Last updated**: 2026-06-16  
**Owner**: `anthropics` (官方)

## 项目定位

> "An AI-powered security review GitHub Action using Claude to analyze code changes for security vulnerabilities."

Anthropic 官方开源的 GitHub Action，**正是 [Anthropic 安全审查 blog](/blog/automate-security-reviews-with-claude-code) 中描述的双层部署"外层"**。这个项目让任何 GitHub 仓库都能在 PR 打开/更新时自动调用 Claude 做安全扫描。

## 与配对 Article 的关系

本项目是 [Claude Code 安全审查自动化：内层命令 + 外层 Action](../harness/anthropic-automate-security-reviews-claude-code-pr-2026.md) 中描述的"GitHub Action"的**官方参考实现**。

| 维度 | Article（理论） | Project（实现） |
|------|-----------------|-----------------|
| **角色** | 一手源描述"为什么 + 怎么部署" | 真实可用的 GitHub Action |
| **抽象层** | 双层部署哲学 + 案例 | 具体 YAML 配置 + Python 实现 |
| **来源** | blog 描述团队经验 | 同一团队开源的工具 |

## 4-way SPM 字面级对位

| Layer | Article 命题 | Project 特征 | 命中 |
|-------|-------------|--------------|------|
| **1. cluster** | harness/security | GitHub Action 安全审查 | ✅ |
| **2. SPM 关键词** | `security review`, `automate`, `GitHub Action`, `vulnerability`, `pull request`, `AI-powered` | `AI-powered security review GitHub Action`, `analyze code changes`, `security vulnerabilities`, `pull request` | ✅ 6 关键词全中 |
| **3. topics/owner** | anthropic.com (官方源) | `anthropics/` owner (官方) | ✅ |
| **4. 维度互补** | 设计哲学 + 案例 (Anthropic 内部 DNS rebinding + SSRF 案例) | 工程实现 (5,269⭐ 实际可用代码) | ✅ 抽象↔实现互补 |

**4-way SPM 满中** = ⭐⭐⭐⭐⭐

## 工程价值

### 1. 零配置启动

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

无需额外基础设施。GitHub Actions 本身就托管了 runner。

### 2. 自动 PR 评论

Action 触发后会在 PR 评论中输出 findings，包括：

- 漏洞位置（文件 + 行号）
- 漏洞类型（OWASP/CWE 分类）
- 严重程度评估
- 修复建议

### 3. 团队基线一致性

不同于 `/security-review` 命令（依赖开发者主动运行），Action 自动对**所有 PR** 执行扫描。这消除了"开发者忘记跑安全审查"的盲点。

### 4. MIT License

可自由 fork、修改、自托管。对于有特殊安全合规要求的组织（如金融、医疗），可以在内部 runner 上自托管，对 prompt 做定制。

## 实战案例

### Anthropic 内部

根据 blog 披露，这个 Action 已经在 Anthropic 内部捕获了至少两个严重漏洞：

1. **DNS rebinding → RCE** 在"只接受本地连接"的 HTTP server 中
2. **SSRF 攻击** 在内部凭证代理系统中

两个漏洞都在 PR 合并前被捕获。

### 开源社区

GitHub 上已经有大量 fork 和衍生项目，例如：

- `anthropics/claude-code-security-review` 5,269⭐ 本体
- 各组织 fork 后加上自定义 prompt（针对自己的安全规范）

## 与传统 SAST 工具的对比

| 维度 | 传统 SAST (Semgrep/CodeQL) | Claude Security Review |
|------|----------------------------|-------------------------|
| **检测原理** | 规则匹配 + AST 分析 | LLM 推理 |
| **误报率** | 高（规则易误报） | 中（LLM 会"理解"上下文） |
| **漏报率** | 中（不识别新攻击模式） | 低（LLM 可推理未知模式） |
| **修复建议** | 通用模板 | 上下文定制 |
| **配置成本** | 高（写规则） | 低（prompt 调优） |
| **运行成本** | CPU 时间 | API 费用 |
| **适用阶段** | CI 流水线 | PR 阶段 |

**互补关系**：传统 SAST 作为基线 + Claude Security Review 作为深度审查 = 防御纵深。

## 局限

1. **API 成本**：每次 PR 触发调用 Claude API，频率高时成本可观
2. **网络依赖**：必须能访问 Anthropic API，离线环境不可用
3. **数据隐私**：PR diff 会发送到 Anthropic API（不符合某些合规要求）
4. **LLM 不确定性**：相同 PR 可能产生不同 findings

## 对开发团队的建议

```yaml
# 推荐配置：双层部署
name: Security Review Pipeline
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  # 外层：自动触发
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-security-review@main
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
  
  # 内层：传统 SAST 基线
  sast-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: returntocorp/semgrep-action@v1
```

**双层叠加 = 自动化 + 基线 + AI 深度审查**。

## Star 数变化轨迹（验证项目活跃度）

| 时间 | Stars | 备注 |
|------|-------|------|
| 2025-08-04 | 0 | 项目创建 |
| 2026-06-16 | 5,269 | 本轮 cron 抓取 |

**平均增速**：约 13 stars/day —— 对于安全类工具是健康增速。

## 一句话总结

> **Anthropic 自己用来审查 Claude Code 代码的工具，现在每个 GitHub 团队都能用**。
