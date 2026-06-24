# Cloudflare security-audit-skill：让 AI Agent 成为安全审计员

**GitHub**: [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | **Stars**: 632 | **License**: MIT | **更新**: 2026-06-20

---

## 核心命题

Cloudflare 用一个 632 星的单仓 skill，把「让 AI Agent 做安全审计」这件事从概念变成了可复用的工程流程——一个 skill，6 个阶段，多个并行 Agent，结果可直接集成到开发流程里。

这不是「给 Agent 加个安全检查」，而是**用多 Agent 协作架构重新设计了整个审计流程**。

---

## 为什么值得推荐

### 1. 六阶段审计管道：并行 Agent 的工程化样本

Cloudflare 的设计把安全审计拆成了一个结构化管道：

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: RECON — 并行研究 Agent                         │
│  映射应用架构、信任边界、输入表面 → architecture.md        │
├─────────────────────────────────────────────────────────┤
│  Phase 2: HUNT — 多角度攻击 Agent（并行）                 │
│  injection / access control / 业务逻辑 / 加密 / 链式攻击  │
│  每个 Agent 可再 spawn 子 Agent 深入                   │
├─────────────────────────────────────────────────────────┤
│  Phase 3: VALIDATE — 对抗性 Agent 审查                   │
│  独立 Agent 尝试反驳每个发现，杀死误报                 │
├─────────────────────────────────────────────────────────┤
│  Phase 4: REPORT — 产出双格式报告                        │
│  REPORT.md（人读）+ FINDINGS-DETAIL.md（MIL+ 详情）       │
├─────────────────────────────────────────────────────────┤
│  Phase 5: Structured Output — JSON Schema 验证           │
│  findings.json + validate-findings.cjs 零依赖校验        │
├─────────────────────────────────────────────────────────┤
│  Phase 6: Independent Verification — 独立 Agent 验证     │
│  用全新 Agent 验证每条事实性声明是否与源码对应           │
└─────────────────────────────────────────────────────────┘
```

**笔者认为**：Phase 3（Validate）的设计是最聪明的部分——让发现者之外的 Agent 来反驳，这直接解决了「Agent 自己发现的问题自己不会怀疑」这一认知偏差。这比任何静态规则都有效。

### 2. 多次运行叠加：对抗 AGENT 审计的「浅度」问题

README 里有一句关键描述：

> 「单次运行大约只能找到全部漏洞的一半」

这说明 Cloudflare 团队对 Agent 能力边界有清醒的认知。他们的解法不是提升单次能力，而是**让多次运行结果叠加**——每次运行探索不同代码路径，Agent 读取之前的 findings.json 跳过已知问题、专注空白区域。

**笔者认为**：这是对「Agent 审计容易漏报」问题的诚实回应。大多数安全工具追求「一次全搞定」，Cloudflare 选择接受限制并用工程手段弥补——这种工程诚实值得尊敬。

### 3. MIT License + Cloudflare 团队背景

MIT License 意味着任何人都可以直接使用、修改、商业化。Cloudflare 内部已经在用它做 fleet-wide 的漏洞发现，这个 skill 是他们内部系统的单仓起点。

### 4. 与 Giskard（5458⭐）的互补关系

| 项目 | 核心能力 | Stars | 方向 |
|------|---------|-------|------|
| Giskard | 开源 LLM/Agent 评估平台 | 5458 | Agent 能力评测 |
| security-audit-skill | 多阶段安全审计管道 | 632 | Agent 安全落地 |

Giskard 回答「Agent 能力有多强」，security-audit-skill 回答「Agent 会不会引入新漏洞」。两者形成 Agent 工程化的完整闭环。

---

## 技术原理

### 核心文件结构

```
SKILL.md              — 平台术语、核心原则、工作流概览
RECONNAISSANCE.md     — Phase 1 侦察提示词 + 综合指令
HUNTING.md            — Phase 2 编排 + 攻击方法论
ATTACK-CLASSES.md     — 攻击类别提示词（核心 + 野生 + 明显类）
VALIDATION-AND-REPORTING.md — Phase 3-6 验证 + 报告 + 验证
report-schema.json    — findings.json 的 JSON Schema
validate-findings.cjs — 零依赖 Node.js 校验器
```

### Phase 2 攻击维度

每个维度都是一个独立 Agent：
- **Core attacks**：injection, access control, business logic, cryptography, feature abuse
- **Chained attacks**：跨维度组合攻击
- **Wildcard**：开放探索，发现意料之外的问题

### 触发方式

```
security audit this codebase
find security vulnerabilities in ./src
do a security review, output to ~/audits/my-project
```

零配置激活，Agent 自动识别审计意图。

---

## 安装与使用

```bash
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit

# 或全局安装
npx skills add https://github.com/cloudflare/security-audit-skill \
  --skill security-audit --global

# 启动审计
# 在目标代码库中直接对话：
"security audit this codebase"
```

**要求**：
- 支持工具调用和并行子 Agent 的编码 Agent（如 Claude Code、Cursor）
- Node.js（仅用于 Phase 5 的 JSON Schema 校验）

---

## 设计原则（README 原文）

> 「Only report what you can exploit. Every finding needs a concrete attack scenario, not 'an attacker could theoretically...'」

> 「Adversarial validation. The agent that checks a finding is never the agent that found it.」

> 「Defense-in-depth gaps are not vulnerabilities. If Layer A prevents the attack, the absence of Layer B is a hardening note.」

---

## 竞品对比

| 方案 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| **security-audit-skill** | Agent skill | 多 Agent 并行、6 阶段结构化、MIT | 需要 Agent 支持子 Agent |
| 传统 SAST 工具 | 静态扫描 | 覆盖广、无误报 | 无法理解上下文、产生大量噪音 |
| 人工渗透测试 | 专家驱动 | 深度最高 | 成本高、速度慢 |

---

## 适用场景

✅ **适用**：
- 在 CI/CD 流程中集成 Agent 安全审计
- 对第三方依赖做快速安全评估
- 作为红队工具定期扫描代码库
- 学习如何用多 Agent 协作解决复杂任务

❌ **不适用**：
- 需要 100% 无误报的安全合规场景
- 纯黑盒渗透测试（需要运行时分析）
- 没有支持子 Agent 的编码 Agent 环境

---

## 笔者的判断

Cloudflare security-audit-skill 填补了「Agent 安全工程」的一个关键空白：不是给 Agent 加个检查列表，而是**用多 Agent 协作架构重新设计审计流程本身**。

它和 Giskard 共同构成了 Agent 工程化的双环：能力评测 ↔ 安全落地。对于正在用 AI Coding 工具（Claude Code、Cursor）的团队，这个 skill 直接解决了「AI 生成的代码安全性靠得住吗」这个问题。

如果你在用 Claude Code 或类似的编码 Agent，这是目前最工程化的安全审计起点。
