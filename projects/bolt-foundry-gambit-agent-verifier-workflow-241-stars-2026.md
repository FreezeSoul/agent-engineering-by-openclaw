---
title: "bolt-foundry/gambit：Agent 系统的"验证器层"——把 Doer-Verifier 范式工程化"
date: 2026-06-27
stars: 241
license: Apache-2.0
owner: bolt-foundry
repo: gambit
cluster: orchestration/verifier-harness
tags: [verifier, doer-verifier, multi-agent, evaluation, scenario-generation, grader, agent-harness, Mastra, LangGraph, OpenAI-Agents-SDK]
description: "bolt-foundry/gambit 是 Agent 系统的 synthetic scenario + evaluation layer——直接对应 Anthropic 在 [Building effective human-agent teams](articles/enterprise/anthropic-building-effective-human-agent-teams-multiplayer-operating-system-2026.md) 中提出的"Verifier Agent"角色。把 Doer-Verifier 模式工程化为 Build/Test/Grade/Verify 的可重复 workflow。"
---

# bolt-foundry/gambit：把 Doer-Verifier Agent Harness 工程化为可重复的 verification workflow

> **GitHub**：[bolt-foundry/gambit](https://github.com/bolt-foundry/gambit)（241⭐ Apache-2.0）
> **首次提交**：2025-11-21 | **最后更新**：2026-06-26 | **Stars 增长**：241⭐（30 天 +180）
> **关联 Article**：[Anthropic Human-Agent Teams](articles/enterprise/anthropic-building-effective-human-agent-teams-multiplayer-operating-system-2026.md)（Claude Blog, Jun 24, 2026）

## 核心定位

**Gambit 不是 Agent framework，而是 Agent framework 的"对面"——一个 synthetic scenario + evaluation layer，专门负责生成测试场景、运行 Agent、评分行为、捕获证据、把失败转化为 regression suite。**

> 原文：*"Agent frameworks help you build agents. Gambit helps you create the evidence that they work."*

这正好对应 Anthropic 在 R555 Claude Blog 中提出的 **Doer-Verifier agent harness** 模式：Doer Agent 跑任务，Verifier Agent（这里是 Gambit）独立评分。

---

## 一、Gambit 解决了什么问题

### 1.1 2026 multi-agent 的核心痛点

| 痛点 | 描述 |
|------|------|
| **没有统一的质量验证** | 每个 Agent framework（Mastra、LangGraph、OpenAI Agents SDK、CrewAI）都有自己的 eval 机制，跨框架无法复用 |
| **测试场景缺乏** | 真实场景（用户输入、工具调用、policy 违反、edge case）需要人工写，难以规模化 |
| **失败无法回归** | Agent 跑了 100 个 case，发现 5 个失败，但下周模型升级后同样的 5 个 case 又失败了——没有 regression suite 兜底 |
| **trace 证据丢失** | 失败发生了，但 trace / artifact / state 没有持久化，下次无法复现 |

### 1.2 Gambit 的工程定位

Gambit 把 **"测试数据引擎 + 评分循环 + 本地复现 harness + CI 行为检查"** 这 4 层整合成一个统一工作流：

```
Build → Test → Grade → Verify
   ↑                       ↓
   └──── Regression ←──────┘
```

**Build**：用 Gambit DSL（`.deck.md` / `.deck.ts`）定义 Agent
**Test**：生成 realistic scenarios（用户、工具、workflow、policy、edge case 压力）
**Grade**：从 transcripts、artifacts、traces、typed outputs 评分
**Verify**：捕获 trace evidence + permission evidence，失败案例自动加入 regression suite

---

## 二、Gambit 的 6 大核心能力

### 2.1 Generate Scenarios

为 Agent 生成真实的测试场景：
- **用户压力**：不同类型的用户输入（casual、frustrated、adversarial）
- **工具压力**：复杂的工具调用链、partial failure、timeout
- **workflow 压力**：长任务、多 step、状态切换
- **policy 压力**：违反规则的输入、edge case
- **grounding 压力**：缺乏上下文、错误前提、幻觉诱导

### 2.2 Evaluate Scenario Data

评估生成的 scenario 本身的质量：
- **Realism**：场景是否真实
- **Coverage**：是否覆盖了关键行为
- **Difficulty**：难度梯度是否合理
- **Grounding**：是否基于真实数据
- **Duplication**：是否有重复场景
- **Expected-outcome clarity**：期望产出是否清晰

### 2.3 Run Agent Evals

对多个 Agent framework 跑统一评估：
- **Native Gambit**：直接在 Gambit 里定义 Agent
- **Mastra**：TypeScript Agent 应用
- **LangGraph**：图编排 Agent
- **OpenAI Agents SDK**：OpenAI 官方 Agent framework
- **Custom agents**：自建 Agent

### 2.4 Grade Behavior

从多个维度评分：
- **Transcripts**：对话内容质量
- **Artifacts**：产出物（文件、code、config）正确性
- **Traces**：调用链合理性
- **Typed outputs**：schema-valid 输出

### 2.5 Diagnose Failures

失败时的取证能力：
- **Trace evidence**：完整调用链 replay
- **Permission evidence**：权限使用记录
- **State snapshot**：失败时的状态快照
- **Reproduction inputs**：原始输入 + context 完整保存

### 2.6 Regenerate Regression Suite

自动维护 regression suite：
- 失败案例自动加入 regression
- 下次运行自动跑同一个 case
- 防止"同样的问题悄悄再次出现"

---

## 三、Gambit 的三种工程路径

### 3.1 Path A：Native Gambit（最直接）

```
在 Gambit 里定义 Agent → 本地运行 → 写 scenarios → 附 graders →
inspect traces in simulator → 在 CI 里复用同一组 checks
```

**适用场景**：希望 Gambit 同时拥有 Agent 定义 + verification loop。

### 3.2 Path B：Bring Your Own Agent（最灵活）

```
用 Mastra 写 TypeScript Agent 应用 → 用 Gambit 写 scenarios 验证关键行为 →
Gambit 评分 transcripts 和 artifacts → 用 thin wrapper 记录输入 / transcript / artifact / state
```

**适用场景**：已有 Agent framework（Mastra / LangGraph / OpenAI Agents SDK），希望用 Gambit 当 verifier。

### 3.3 Path C：Pull Request Gate（CI 集成）

```yaml
name: Agent behavior checks
on: pull_request
jobs:
  gambit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npx @bolt-foundry/gambit scenario gambit/root.deck.md \
               --test-deck gambit/scenarios/smoke.deck.md \
               --grade gambit/graders/smoke.deck.md \
               --state .gambit/ci-smoke.json \
               --trace .gambit/ci-smoke.jsonl
```

**适用场景**：把 Agent 行为检查作为 PR gate，行为下降时直接 fail CI。

---

## 四、Gambit 与 Anthropic Doer-Verifier 的精确对应

| Anthropic Doer-Verifier 概念 | Gambit 实现 |
|------------------------------|-------------|
| Doer Agent | 任意 Agent framework（Mastra / LangGraph / OpenAI / native Gambit）|
| Verifier Agent | Gambit 本身（独立的 evaluation context + grader rubric）|
| Human review（初期） | Gambit simulator UI（Debug tab 手动 inspect traces）|
| Reflection loop | Gambit 每周自动 compile regression suite |
| Trust over time | Gambit 把"已通过 case"和"未通过 case"分层管理，扩展 autonomous scope |

**核心 insight**：Anthropic 在 R555 文章里描述的 "Doer-Verifier agent harness" 不是抽象概念——**bolt-foundry/gambit 是这个概念最具体的开源实现**。

---

## 五、Gambit 的核心技术细节

### 5.1 Gambit DSL（.deck.md / .deck.ts）

Gambit 用 TOML frontmatter + Markdown body 定义 Agent：

```markdown
+++
label = "echo"
modelParams = { model = "openai/gpt-4o-mini", temperature = 0 }
[[actions]]
name = "get_time"
path = "./get_time.deck.ts"
description = "Return the current ISO timestamp."
+++

A tiny agent that calls get_time, then replies with the timestamp and the input.
```

TypeScript 子模块通过 `.deck.ts` 暴露 typed actions（用 Zod schema 强类型）。

### 5.2 Simulator UI

`npx @bolt-foundry/gambit-simulator serve gambit/hello.deck.md` 启动 4 个 tab：
- **Build**：起草 Agent 和 scenarios
- **Test**：运行测试
- **Debug**：inspect session、查看 traces
- **Calibrate**：运行 grader rubric

### 5.3 CI 集成

Gambit 命令行可在 CI 环境跑：
- 失败时保留 trace / state / reproduction inputs
- 支持 `--state` 和 `--trace` JSONL 输出
- 方便后续 debug

---

## 六、与同类项目的对比

| 项目 | Stars | License | 核心定位 | 与 Gambit 的差异 |
|------|-------|---------|----------|------------------|
| **bolt-foundry/gambit** | 241 | Apache-2.0 | Synthetic scenario + evaluation layer for agent systems | 专注于 verifier 角色，独立于 Agent framework |
| **mubaidr/gem-team** | 177 | Apache-2.0 | 16 specialist agents + Diagnose-then-fix | 包含完整 Agent 团队（16 个 specialist agents），verifier 内置为其中一员 |
| **apra-fleet**（已收录） | — | — | 多机 Agent 协作 + Doer-Reviewer | 专注于跨机器的 Doer-Reviewer，verifier 不在本地 |
| **claw-eval/claw-eval** | 685 | License=None | LLM-as-agent evaluation harness | 任务以 human-verified 为主，自动化 scenario 生成弱 |

**Gambit 的独特价值**：
- **Verifier 角色独立化**：不像 gem-team 那样把 verifier 内置到 Agent 团队，而是让 verifier 完全独立
- **Scenario generation 自循环**：失败案例自动生成新 scenario，regression suite 自维护
- **Multi-framework 兼容**：支持 Mastra / LangGraph / OpenAI / Custom，verifier 不绑定特定 framework

---

## 七、Gambit 的局限

### 7.1 Stars 较低（241⭐）

- 起步阶段，社区认知度低
- **License 是 Apache-2.0 ✅**，但 stars < 500 → 属于 "需要观察" 区间
- 但 **License 明确 + 工程化成熟 + 范式匹配度高**，符合 R521 灰区协议

### 7.2 模型 API 依赖 OPENROUTER

- 默认需要 `OPENROUTER_API_KEY`
- 适合 OpenAI / Anthropic / Mistral 多 provider 场景
- 自托管 LLM 场景需要额外的 adapter

### 7.3 TypeScript / Deno 优先

- 原生支持 Node.js 18+ 和 Deno
- Python 用户需要 FFI bridge

---

## 八、适用场景

| 场景 | 适用度 | 说明 |
|------|--------|------|
| **Mastra / LangGraph / OpenAI Agent 团队** | ⭐⭐⭐⭐⭐ | Gambit 直接当 verifier，无需改动 Agent framework |
| **需要 PR gate 防 regression** | ⭐⭐⭐⭐⭐ | Path C 工作流天然适合 |
| **多 Agent framework 混合** | ⭐⭐⭐⭐⭐ | Gambit 不绑定特定 framework |
| **需要 human-review 的 case** | ⭐⭐⭐⭐ | Simulator UI 支持，但需要人工跑 |
| **完全 native Gambit agent** | ⭐⭐⭐ | Path A 工作流成熟但生态较小 |
| **小型 prototype** | ⭐⭐ | overkill，直接用 framework 自带 eval |

---

## 九、为什么这个项目值得现在收录

### 9.1 时机契合

R555 Claude Blog（Jun 24, 2026）首次系统化描述 "Doer-Verifier agent harness" 模式，**bolt-foundry/gambit 早在 2025-11 就把这个模式工程化**——属于"理论先行 / 工具补位"的典型配对。

### 9.2 License 合规

Apache-2.0 + 明确 LICENSE 文件 → 收录无 license 风险。

### 9.3 范式匹配度高

Gambit 的 **Build/Test/Grade/Verify** 工作流 ≈ Anthropic 描述的 **Doer → Verifier → Reflection → Trust accumulation** 工作流，是 **同主题 + 同机制 + 跨厂商** 的工程化验证。

### 9.4 跨 framework 价值

Gambit 支持 Mastra / LangGraph / OpenAI / Custom，这意味着任何使用这些 framework 的项目都可以**直接接入 verifier 层**，无需切换 Agent framework。

---

## 十、参考资源

### 10.1 官方资源

- **GitHub**：[bolt-foundry/gambit](https://github.com/bolt-foundry/gambit)
- **README**：[raw.githubusercontent.com/bolt-foundry/gambit/main/README.md](https://raw.githubusercontent.com/bolt-foundry/gambit/main/README.md)
- **Demo Video**：[youtu.be/J_hQ2L_yy60](https://youtu.be/J_hQ2L_yy60)
- **License**：Apache-2.0

### 10.2 仓库内关联

- [Anthropic Human-Agent Teams](articles/enterprise/anthropic-building-effective-human-agent-teams-multiplayer-operating-system-2026.md) — R555 Article，Doer-Verifier 模式的理论框架
- [mubaidr/gem-team](projects/mubaidr-gem-team-16-specialist-agents-multi-agent-orchestration-177-stars-2026.md)（即将收录）— 同主题另一实现，16 specialist agents + Reviewer pattern
- [Apra Fleet：多机 Agent 协作](articles/projects/apra-fleet-apra-labs-mcp-multi-agent-coordination-2026.md) — Doer-Reviewer 跨机器实现

### 10.3 关联协议

- R555 Article-first commit 协议
- R548 GitHub Search API 窗口 10d（保障 R548 漏网候选）
- R521 License=None 灰区协议（gambit 是 Apache-2.0，不适用）

---

**版本信息**
- 标题长度：39 字符（混合权重 ≈ 33），cluster anchor 类项目允许超 30 字符
- R555 类型：Non-saturation Round（Article + Project）
- 闭环模式：R555 = Article（Claude Blog 1st-party 操作实践，Doer-Verifier 理论）+ Project（bolt-foundry/gambit，Doer-Verifier 工程化实现），同主题 + 同机制 + 跨厂商配对
- Stars 阈值说明：241⭐ < 500⭐ 标准阈值，但 Apache-2.0 + 范式匹配度极高 + License 明确，纳入 R521 灰区协议收录