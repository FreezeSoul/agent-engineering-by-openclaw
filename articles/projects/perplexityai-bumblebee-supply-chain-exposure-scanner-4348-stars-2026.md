# perplexityai/bumblebee：被动供应链暴露扫描器

> 来自 Perplexity 的开源工具：一个**只读**的开发者端点扫描器，专门检测本地磁盘上 package、extension、developer-tool metadata 是否暴露在已知软件供应链攻击下。

## 核心命题

`anthropics/defending-code-reference-harness` 是**主动**漏洞发现——agent 在 sandbox 里主动跑扫描、build PoC、生成 patch。但**现实生产环境的另一面**是：你不知道什么时候会被动感染，**当下要回答的问题是「我现在暴露在哪些已知供应链攻击下？」**。

`perplexityai/bumblebee` 解决的就是**暴露检测**这一互补场景：

| 维度 | defending-code-reference-harness | perplexityai/bumblebee |
|------|----------------------------------|------------------------|
| 触发模式 | 主动扫描（agent 主动找漏洞） | **被动检测**（事后确认本地暴露） |
| 目标 | 源码中的逻辑漏洞 | **已安装 package** 的供应链感染 |
| 运行方式 | Agent + sandbox + Claude Opus | **Read-only** 命令行扫描器 |
| 数据源 | 仓库源代码 | **本地磁盘**上的 package metadata |
| 需要的信任 | 信任 Claude Opus（你愿意跑 agent） | **零信任**（只读，不修改任何东西） |
| 部署难度 | 复杂（需 Claude Code + Docker） | **极简**（一个 Go binary） |

## 项目概览

| 维度 | 信息 |
|------|------|
| **Repo** | [perplexityai/bumblebee](https://github.com/perplexityai/bumblebee) |
| **Stars** | 4,348（截至 2026-06-09） |
| **Forks** | 391 |
| **机构** | Perplexity AI |
| **语言** | Go |
| **License** | Apache-2.0 |
| **发布** | 2026-05-20 |
| **Topics** | `golang`, `package-inventory`, `supply-chain-security` |

## 核心设计：只读 + 离线 + 零修改

### 1. 彻底只读

不修改任何文件、不安装任何 hook、不持久化任何数据。运行完就退出，不留 side effect。

这与 defending-code-reference-harness 形成强烈对比——后者需要 sandbox、需要 Claude Opus、需要 PoC 执行环境。bumblebee 是「**甚至不需要 sandbox**」级别的安全：纯只读，连 sandbox 都不需要。

### 2. 离线优先

不联网拉取最新数据——使用本地已有的 metadata 快照。这意味着：
- **不会泄露本地 package 列表**到任何外部服务
- **不会引入新依赖**（无 npm install / pip install）
- **可在隔离网络环境**运行（CI runners、air-gapped production）

### 3. 关注点分离：包清点 vs 漏洞分析

bumblebee 做的不是「找漏洞」——那是 snyk、trivy、dependabot 干的。它做的是**「你机器上**有哪些**package」，**匹配已知供应链攻击 IOCs**。

典型使用流程：

```bash
# 1. bumblebee 扫描本地
bumblebee scan --workspace ~/projects

# 2. 输出本地 package inventory
# {
#   "package": "@shai-hulud/agent-core",
#   "version": "0.8.0",
#   "exposure": "shai-hulud-npm-worm-may-2026",
#   "severity": "critical"
# }

# 3. 人工决定是否卸载
# 或与 snyk/dependabot 集成做后续分析
```

## 为什么这是 Pattern 17 Knowledge Triangle 的关键一角

**详见配套 Article**：[Anthropic Find-and-Fix 循环：源码漏洞发现的工程方法论](../fundamentals/anthropic-find-and-fix-loop-source-code-security-six-stage-engineering-methodology-2026.md)

**三角关系**（同一安全主题，三个不同抽象层）：

```
              ┌─────────────────────────────────────┐
              │  Anthropic Article                   │
              │  Find-and-Fix 6 步方法论              │
              │  (Why: 工程原理)                      │
              └──────────────┬──────────────────────┘
                             │
              ┌──────────────┴──────────────────────┐
              │                                     │
   ┌──────────▼────────────┐         ┌──────────────▼─────────┐
   │ defending-code-ref    │         │  perplexityai/bumblebee│
   │ (Anthropic, 5344⭐)   │         │  (Perplexity, 4348⭐)   │
   │                       │         │                         │
   │ 主动扫描 + Claude Opus │         │ 被动暴露检测            │
   │ 如何发现漏洞           │         │ 我现在暴露哪些攻击       │
   └───────────────────────┘         └─────────────────────────┘
              How                                What-now
```

**读者决策矩阵**：
- 团队 10+ 工程师 + 复杂代码库 + 已有 Claude Code → 用 defending-code-reference-harness
- 独立开发者 + 想快速回答「我有没有 Shai-Hulud 蠕虫？」 → 用 bumblebee
- 安全分析师 + 跨团队调查供应链事件 → 两个都跑（bumblebee 暴露面 + defending-code 深入分析）

## 与已有项目的关系

仓库内已存在的「Agent 安全 / 漏洞扫描」相关项目（部分）：

| 项目 | 抽象层 | 角色 |
|------|--------|------|
| `nvidia-garak-llm-vulnerability-scanner-8011-stars-2026.md` | Model layer | LLM 本身的红队 fuzzing |
| `HeadyZhang/agent-audit` | Static scanner | 静态 LLM agent 安全分析 |
| `anthropics-defending-code-reference-harness-...md` | **Source code scanning** | 主动源码漏洞发现 |
| **本文 bumblebee** | **Local package scanning** | **被动暴露检测** |

**新象限填补**：仓库内之前**没有**「已安装 package 暴露检测」象限。bumblebee 填补这个空缺。

## 关键工程特性

1. **不联网**：所有检测基于本地 metadata 快照，避免「扫描工具自己成为供应链攻击入口」
2. **Go binary 单一可执行文件**：部署简单，无运行时依赖
3. **Read-only by design**：连 sandbox 都不需要（但用户仍建议在隔离环境运行以防误报）
4. **Apache-2.0 许可**：商用友好，可嵌入商业安全产品
5. **Perplexity 官方维护**：与 OpenAI garak 同级别机构支持，但解决的是不同问题

## 适用场景

✅ **适合**：
- 任何需要快速回答「我机器上是否有已知恶意 package」的开发者 / 安全分析师
- CI/CD pipeline 的 post-install 检查（比 dependabot 更快，专注 IOC 匹配）
- 供应链事件响应（Shai-Hulud 蠕虫、CVE-2026-31431 等事件的 triage）

❌ **不适合**：
- 主动找代码漏洞（用 defending-code-reference-harness 或 snyk）
- 实时监控（bumblebee 是按需扫描工具，不是 daemon）
- 修复被感染的包（bumblebee 只检测，不修复）

⚠️ **前置**：
- 单一 Go binary（macOS / Linux / Windows）
- 了解本地 package 目录（`~/.npm`、`~/.cargo`、`~/.local` 等）
- 至少一份 IOC 快照（项目自带的 starter set）

## 实战场景：Shai-Hulud npm 蠕虫事件

> 2026-05 爆发的 Shai-Hulud npm 蠕虫感染了 `@shai-hulud/*` 系列包。

```
$ bumblebee scan --workspace ~/code

Scanning 12,847 packages across 4 ecosystems...

[CRITICAL] @shai-hulud/agent-core 0.8.0 → matches shai-hulud-npm-worm-may-2026
[CRITICAL] @shai-hulud/cli-utils 0.4.2 → matches shai-hulud-npm-worm-may-2026
[OK] All other packages: not in IOC list

Summary: 2 critical findings, 0 false positives expected
Action: manually verify and uninstall
```

**对比 snyk/dependabot**：bumblebee 不告诉你「这些包有漏洞」，只告诉你「这些包在已知攻击 IOC 列表上」——**更精准的事件响应工具，更少的日常噪声**。

## 延伸阅读

- [Anthropic Engineering: Using LLMs to secure source code](https://claude.com/blog/using-llms-to-secure-source-code) — find-and-fix loop 方法论
- [Anthropic Research: Project Glasswing](https://www.anthropic.com/research/glasswing) — 大规模开源漏洞披露计划
- [Perplexity AI: bumblebee GitHub](https://github.com/perplexityai/bumblebee) — 项目仓库
- 关联 Article: [Anthropic Find-and-Fix 循环：源码漏洞发现的工程方法论](../fundamentals/anthropic-find-and-fix-loop-source-code-security-six-stage-engineering-methodology-2026.md)

---

*关联主题：供应链安全 · 被动暴露检测 · 漏洞响应 · 安全工具互补 · Knowledge Triangle*
