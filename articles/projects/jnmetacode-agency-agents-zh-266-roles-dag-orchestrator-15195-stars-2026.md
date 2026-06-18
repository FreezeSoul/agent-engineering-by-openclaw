---
title: jnMetaCode/agency-agents-zh 266 专家角色库 2026
stars: 15195
license: MIT
date: 2026-03-06
source: https://github.com/jnMetaCode/agency-agents-zh
topics: [agency-orchestrator, multi-agent, hermes-agent, claude-code, no-code, ai-roles]
cluster: orchestration
pair_article: articles/orchestration/anthropic-multi-agent-decision-framework-when-not-2026.md
---

# jnMetaCode/agency-agents-zh — 266 个多 Agent 专家角色 + DAG 编排器

> 仓库：https://github.com/jnMetaCode/agency-agents-zh
> Stars: 15,195 (2026-06-18)
> License: MIT
> Topics: `agency-orchestrator` / `multi-agent` / `hermes-agent` / `claude-code` / `no-code` / `workbuddy` / `ai-roles`

## 核心定位

**"agency-agents" 的中文社区版** — 266 个即插即用的 AI 专家角色，覆盖工程、设计、营销、产品、游戏、安全、GIS、金融等 20 个部门。与 R439 Anthropic 多 Agent 决策框架（`when-not`）形成**强 4-way SPM 配对**：

| 维度 | Article (R439) | Project (R439) |
|------|----------------|----------------|
| **焦点** | 决策框架："何时**不要**用多 Agent" | 实施资源：266 个**已经可用的**多 Agent 角色 |
| **角色** | 哲学 / 启发式层 | 工程实现 / 开箱即用 |
| **关键产出** | 3 scenarios + 1 anti-pattern | 266 个角色 prompt + DAG 编排器 + 桌面客户端 |
| **使用场景** | "我应不应该用多 Agent？" | "我已经决定用多 Agent，怎么快速搭？" |

## 关键设计

### 266 个角色（不是模板，是完整人设）

每个角色包含：
- **独立人设**（身份、背景、专长领域）
- **专业流程**（按行业方法论设计 — 例如安全工程师按 OWASP Top 10 审查）
- **可交付成果**（角色激活后产出的具体 deliverable）

**20 个部门覆盖**：工程、设计、营销、产品、游戏、安全、GIS、金融、教育、医疗、法律、运营、内容、客服、销售、采购、行政、跨境电商、政务 ToG、工业。

### 配套编排器 — Agency Orchestrator

```bash
npm install -g agency-orchestrator
ao compose "帮我写一篇关于 AI Agent 的深度分析文章" --run
```

**特性**：
- 零代码编排（自然语言触发 DAG）
- DAG 并行（多角色协同）
- 断点续跑
- 10 种大模型（7 种免 key）
- 现成模板开箱即用
- 桌面客户端（macOS / Windows / Linux）+ 在线 Web

### 一键安装到 18 种 AI 编程工具

支持 Claude Code / Cursor / Copilot / Codex / Hermes Agent 等 18 种主流工具，每种工具一条命令安装。

## 与 R439 Article 的 4-way SPM 闭环

**Layer 1 — Cluster 共享**：✅ orchestration（多 Agent 编排）

**Layer 2 — 关键词字面级共享**：
- Article: "multi-agent" / "orchestrator-subagent" / "verification subagent" / "context pollution" / "parallel" / "specialization" / "decision framework"
- Project: "multi-agent" / "agency-orchestrator" / "DAG 并行" / "266 个专家" / "20 个部门" / "system-prompt" / "prompt-engineering"
- **共享关键词 ≥ 5 个** ✅

**Layer 3 — GitHub topics target-ecosystem 命中**：
- **`hermes-agent` 直接命中** ✅（R367 #27 决定性 tiebreaker — `topics` 含本仓库目标生态）
- `claude-code` / `claude` / `copilot-agent` / `cursor-rules` 间接命中 ✅
- `multi-agent` / `agency-orchestrator` 主题命中 ✅

**Layer 4 — 维度互补非重叠**：
- Article = **何时不要用多 Agent**（决策层 / 哲学层 / 警告层）
- Project = **如何快速搭建多 Agent**（实施层 / 资源层 / 工具层）
- **维度互补** ✅ — 不是重复覆盖同一角度

**综合评级**：⭐⭐⭐⭐⭐ 4-way SPM 全中

## 与 R357 non-coder Agent builder cluster 的关联

R357 是"非工程师 Agent 构建"cluster 0→1 启动，project = `OthmanAdi/planning-with-files`（SKILL.md 跨 Agent 标准）。

**jnMetaCode/agency-agents-zh 与 R357 互补**：
- R357 = **协议层**（SKILL.md 是 metadata 协议，60+ Agent 兼容）
- R439 project = **角色库层**（266 个角色 prompt + 编排器）

两者都是"非工程师能用 Agent"路径：
- R357 路径：写 plan → SKILL.md 协议 → 任何 Agent 加载
- R439 project 路径：用现成角色 + 编排器 → 直接产出

**50 个中国市场原创智能体**：小红书 / 抖音 / 微信 / B 站 / 飞书 / 钉钉 等平台运营 + 跨境电商 / 政务 ToG / 医疗合规 / Qt 工业上位机 / 机械设计 / 畜禽养殖档案核对 — **这是真正"非工程师能用 Agent"的实战库**。

## License 验证

```
license: MIT (verified 2026-06-18 via GitHub API)
spdx_id: MIT
```

清洁度 OK，可作为实施参考 / fork / 二次开发。

## 适用场景

1. **新团队想快速搭建多 Agent 协作系统** → 直接用 266 角色库 + 编排器，几分钟产出完整方案
2. **AI 编程工具角色定制** → 18 种工具一键安装，避免每个工具写 prompt
3. **中国市场本地化 Agent 库** → 50 个原创角色（小红书/抖音/微信等）覆盖中文场景
4. **作为 R439 decision framework 的实施参考** → 决定用多 Agent 后，从这里选角色

## 不适用场景

1. **R439 文章明确反对的场景**：
   - 单 Agent 能达成等效结果 → 不需要
   - 任务 < 1000 tokens / 不存在并行机会 / 不需要专门化 → 不需要
   - 协调成本 > 收益 → 不需要
2. **需要严格 verification 子 Agent 的高质量场景** → 编排器内置 verification 不强，建议加自定义 verification 子 Agent

## 推荐路径

```
[读 R439 Article: 何时不用多 Agent]
       │
       ▼
[判断: 真的需要多 Agent 吗?]
       │
   ┌───┴───┐
  No      Yes
   │       │
   ▼       ▼
[改进   [用 jnMetaCode/agency-agents-zh]
单 Agent + 编排器 ao compose
 prompt]     │
             ▼
       [根据部门选 266 角色]
             │
             ▼
       [R337 Scheduled 调度自动化]
       [R407 verification subagent 加固]
```

## 相关引用

- **R439 Article（配对）**：`articles/orchestration/anthropic-multi-agent-decision-framework-when-not-2026.md`
- **R407 subagent 决策框架**：`articles/orchestration/claude-code-subagents-decision-framework-2026.md`
- **R357 非工程师 Agent 构建**：`articles/enterprise/anthropic-gtm-claude-code-non-coder-agent-builder-2026.md`
- **R337 Scheduled Deployments**：`articles/orchestration/claude-managed-agents-scheduling-vault-scheduled-execution-credential-injection-2026.md`
- **R375 nanoclaw**：另一 OpenClaw 兼容的多 Agent harness 路径

## 关键 takeaway

**R439 是"何时**不要**用多 Agent"的决策框架；jnMetaCode/agency-agents-zh 是"已经决定用多 Agent 后，怎么快速搭建"的实施资源**。

两个共同回答"多 Agent 怎么用"问题：
- **先读 R439** → 避免 over-engineering
- **真要用时** → 用 jnMetaCode/agency-agents-zh 加速落地
- **生产环境** → 加 R407 verification subagent + R337 scheduled orchestration

15K stars + MIT + `hermes-agent` topic 直接命中目标生态 = 4-way SPM ⭐⭐⭐⭐⭐。