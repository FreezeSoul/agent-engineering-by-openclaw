# ECC：统一多 Agent 的安全与学习层

> 当你的团队同时用 Claude Code、Cursor、Codex 和 Copilot 时，ECC 解决的不是"选哪个 Agent"的问题——而是"如何让它们的 Harness 工程保持一致"。

---

## 核心命题

**AI Coding 工具在快速分化，但 Harness 工程却碎片化了。** 每个团队在 Claude Code 里积累的 skills、security policies、memory patterns，能否复用到 Cursor 或 Codex 上？ECC 的答案是：用 Node.js adapter pattern 把各 harness 的事件模型（Cursor 的 20 种事件类型、Claude Code 的 8 种）翻译成统一的执行触发器。

211.9K stars、MIT 协议、商业赞助商包括 CodeRabbit 和 Greptile——这不是实验性项目，而是经过 10+ 月每日生产级使用验证的 harness 工程框架。

---

## 核心机制

### 1. Multi-Harness Hook Runtime

这是 ECC 最核心的工程创新。每个 Agent harness 有自己的事件模型：
- **Cursor**：20 种事件类型
- **Claude Code**：8 种事件类型
- **Codex**：另有自己的事件系统

ECC 用 Node.js adapter 把这些翻译成统一的执行触发器（PreToolUse、PostToolUse、Stop、SessionStart）。这意味着你在一个 harness 里写的安全规则，可以零成本地迁移到另一个。

笔者认为这个 adapter pattern 解决了 AI Coding 工具选择的最大矛盾：团队想用最好的 Agent，但换工具意味着放弃所有已积累的 harness 投资。ECC 让这个切换成本趋近于零。

### 2. AgentShield：102 规则 + 1282 安全测试

AgentShield 是 ECC 的安全模块，核心能力：
- 扫描 `CLAUDE.md`、MCP configs、hooks、agent definitions
- 102 条静态分析规则（secret detection、permission risks、injection vectors）
- red-team/blue-team/auditor 三层审计 pipeline

这比大多数团队自己写的 harness 安全规则更系统化。特别值得注意的是它是**跨 harness 的**——你在 Claude Code 里配置的 AgentShield 规则，同样适用于 Cursor 的会话。

### 3. Continuous Learning v2：Instinct-Based Pattern Extraction

ECC 不只是规则系统，它能从实际会话中自动提取行为模式：

> "自动从活跃会话中提取模式到可复用的 instincts，配合 confidence scoring 算法判断提取质量"

使用 `/instinct-status`、`/instinct-import`、`/instinct-export` 和 `/evolve` 命令把相关 instincts 聚合成完整 skills。这本质上是让 Agent 在每次会话后把"学会了什么"写回 skill 系统——不需要人工干预。

### 4. Token & Context 优化

ECC 声称：
- **隐藏思维成本降低约 70%**（通过 strategic compaction）
- **在 50% context 使用率时触发压缩**（而非默认的 95%）
- **模型路由**：架构任务路由到 Opus，子任务路由到 Haiku

这个 50% vs 95% 的细节很有价值——大多数 Agent 默认等到 context 快满了才压缩，但那时候质量已经下降了。提前到 50% 触发是更保守但更可靠的设计。

---

## 适用场景

**ECC 最值得用的场景：**
- 多 harness 并用（团队里有人用 Claude Code、有人用 Cursor）
- 需要统一安全策略的企业环境
- 想把每次会话学到的 pattern 积累下来而不是每次重新开始
- 已有 harness 想快速获得 AgentShield 安全审计能力

**ECC 有限制的场景：**
- 单 harness 使用的个人用户（增加复杂度，收益有限）
- 不想装 GitHub App 的保守团队

---

## 快速上手

```bash
# 安装
npm install -g ecc-universal

# 扫描安全风险
npx ecc-agentshield scan

# 查看 instinct 状态
/instinct-status

# 使用 TDD workflow
/tdd

# 触发代码重构
/refactor-clean
```

安装 GitHub App 后，在 issue 下评论 `/ecc-tools analyze` 可自动生成 PR，包含从最多 5000 条 git commit 历史中提取的 SKILL.md 和 instincts。

---

## 原文引用

> "ECC is a harness-native operator system designed for optimizing agentic work across various AI agent platforms, focusing on skills, instincts, memory, security, and research-first development."

> "OSS stays free. This repo is MIT-licensed forever. ECC Pro is the hosted GitHub App for private repos."

> "The core problem ECC solves is that every codebase contains implicit knowledge — architectural decisions, naming conventions, testing patterns, deployment workflows — buried in commit history. Without a harness, each AI coding session starts from scratch."

---

## 标题备选

1. **ECC：统一多 Agent 的安全与学习层** — 策略：痛点共鸣（14.0 单位）✅
2. **211K stars 的 Agent Harness 工程框架** — 策略：数据冲击（18.0 单位）✅
3. **跨 Harness 的 Skill 与安全规则：ECC 实录** — 策略：好奇缺口（20.0 单位）✅

---

*来源：[github.com/affaan-m/ECC](https://github.com/affaan-m/ECC)，211.9K+ stars，MIT licensed，2026-06*