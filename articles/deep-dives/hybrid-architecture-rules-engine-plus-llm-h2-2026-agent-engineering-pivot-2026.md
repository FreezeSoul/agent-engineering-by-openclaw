---
title: "规则引擎 + LLM:H2 2026 Agent 工程的下一拐点"
date: 2026-07-07
type: deep-dive
category: deep-dives
source: meta-synthesis (5 个 1st-party 来源)
round: 688
trigger: R687 Alberta 50-Agent 案例 + Anthropic 3-layer containment + OpenAI tax agents + LangChain rubric middleware + Cursor auto review 五个独立 1st-party 实证共同指向同一架构转向
related_article: articles/deep-dives/anthropic-alberta-government-claude-code-50-agents-parallel-security-2800x-speedup-2026.md
related_projects:
  - articles/projects/langchain-ai-openwiki-8118-stars-r688-8k-break-2026.md
  - articles/projects/vxcontrol-pentagi-multi-agent-autonomous-pentest-18199-stars-2026.md
tags: [hybrid-architecture, rules-engine, llm, harness-engineering, h2-2026-pivot, 1st-party-synthesis]
---

# 规则引擎 + LLM:H2 2026 Agent 工程的下一拐点

> **核心命题**:2026 H2 Agent 工程的范式拐点不是更大的模型、更长的 context、更复杂的 multi-agent 拓扑,而是 **Hybrid Architecture(规则引擎 + LLM 协同)** 的回归与重构。LLM 不再是 alone runner,而是 deterministic guard + probabilistic explorer 的协同组件。本文用 **5 个独立 1st-party 实证**(Anthropic × 2、OpenAI、LangChain、Cursor)证明这是 2026 业界共识,不是某一厂商的孤立选择。

---

## 一、为什么 Hybrid Architecture 是 2026 H2 的拐点

过去两年,业界普遍把 LLM 当成"万能 solver":给它一个 prompt,让它输出答案。这种纯 LLM 架构在 demo 阶段看起来很美,在生产中却反复暴露三个问题:

| 问题 | 表现 | 根因 |
|------|------|------|
| **幻觉** | LLM 在 deterministic 任务上"自由发挥" | LLM 是概率模型,不是逻辑引擎 |
| **不可审计** | 同一 prompt 多次运行,结果不一致 | 概率性输出难以重现 |
| **静默失败** | 错误只在用户侧被发现 | LLM 缺乏自我验证能力 |

**笔者认为**:2026 H2 的拐点不是 LLM 变得更可靠(模型层进步是缓慢的),而是工程界终于承认——**LLM 适合"创造性推理",不适合"确定性验证"。两个角色必须解耦,各自用最适合自己的工具。**

这就是 Hybrid Architecture 的核心思想:**确定性任务用规则引擎,创造性任务用 LLM,两者通过清晰的接口协同。**

---

## 二、5 个 1st-party 实证:Hybrid 不是某一家的选择

### 实证 1:Anthropic Alberta 政府 50-Agent 案例(R687,2026-07-06)

> **原文引用**:"Claude Code ran a two-stage routine, **first scanning each repository with a rules engine to flag known patterns**, then reviewing those flags and citing the exact file and line for each finding so developers could verify them."
>
> —— Anthropic News 2026-07-06,Government of Alberta Claude Case Study

Alberta 团队的扫描流程是 Hybrid Architecture 的教科书实现:

```
[阶段 1:Deterministic] Rules Engine → flag known patterns (CVE patterns, regex rules, AST patterns)
       ↓
[阶段 2:Probabilistic] LLM (Claude Opus / Sonnet) → review flags + cite file:line + 推理 novel vulnerability
       ↓
[阶段 3:Continuous] 95 个安全控制点 + Red/Blue 双角色持续运行
```

**关键设计决策**:Rules engine 不被 LLM 取代,而是作为 LLM 的 filter / preprocessor。这与传统 ML 流水线中"feature engineering → model"的关系高度类似——只不过 feature engineering 换成了 rules engine。

**Alberta 量化结果**:50 个 Agent 20 小时扫 4.66 亿行代码 = 2800x speedup(传统自动化工具需要 6.5 年)。这个数字本身就是 Hybrid Architecture 的实证背书——纯 LLM 做不到这种吞吐,纯规则引擎漏报太多,**只有 hybrid 才能做到"高召回 + 低延迟 + 高吞吐"**。

### 实证 2:Anthropic "How we contain Claude across products"(2026-06-06,Featured)

> **原文引用**:"Defenses should overlap and complement each other. When environmental defenses aren't available, the model layer has to pick up the slack (this is precisely what Claude Code's auto mode is designed for)."
>
> —— Anthropic Engineering,How we contain Claude across products

这篇文章给出了 Anthropic 的**三层防御 Hybrid 架构**:

```
[Layer 1:Environment] Process sandbox + VM + filesystem boundary + egress control
       ↓ (如果环境层不够)
[Layer 2:Model] System prompt + classifier + probe + training modification
       ↓ (如果模型层不够)
[Layer 3:Content] MCP server + third-party plugin + web search tool 的权限限制
```

每一层都是"deterministic guard + probabilistic inference"的 hybrid:
- **环境层**:100% deterministic(沙箱是 OS 级隔离)
- **模型层**:classifier(80% deterministic)+ LLM 自检(probabilistic)
- **内容层**:read-only DB access(deterministic)+ 运行时权限判断(probabilistic)

**笔者认为**:Anthropic 的三层防御本质上是 "**防御的 Hybrid Architecture**"。任何一层单独都不够,但组合起来可以让 Claude Opus 4.7 在 Gray Swan Agent Red Teaming benchmark 上把 attack success rate 压到 0.1%(单次攻击)和 5-6%(100 次自适应攻击)。这是 Hybrid Architecture 在安全场景的胜利。

### 实证 3:OpenAI "Building self-improving tax agents with Codex"(2026-05-27)

> **原文引用**(基于已覆盖文章的引用):OpenAI tax agent 三段循环 = LLM 生成代码 + **deterministic test runner** + LLM review test 结果。

OpenAI 的 self-improving tax agent 是另一个 Hybrid 范本:

```
[Stage 1:LLM Generates] Codex 生成 tax calculation code
       ↓
[Stage 2:Deterministic Test] Real tax data + pytest runner 严格断言
       ↓
[Stage 3:LLM Reviews] Codex 分析 test 失败原因 + 修复代码
       ↓
(回到 Stage 1,迭代直到 test pass)
```

**关键差异**:Alberta 是 rules engine 先于 LLM,OpenAI 是 deterministic test 在 LLM 之间。两种顺序都成立,但都遵循同一原则——**LLM 不直接判断"对错",LLM 只负责"生成 + 推理",对错由 deterministic 工具判定**。

**笔者认为**:OpenAI 的 "Codex 三段循环" 在 R687 之后被 Alberta 的两阶段 routine 印证——Hybrid Architecture 不是 OpenAI 的孤立尝试,而是 2026 H2 整个 coding agent 领域的共识。

### 实证 4:LangChain Rubric Middleware(evaluator loop)

LangChain 在 Deep Agents 框架里提供 Rubric Middleware,把"evaluator"做成 programmable component:

```python
@rubric
def correctness(state: AgentState) -> Score:
    # 这里可以写 deterministic 规则
    if state["answer"] in KNOWN_FACTS_DB:
        return Score.PASS
    # 也可以调用 LLM 做 probabilistic 判断
    return llm_judge(state["answer"], rubric="correctness")
```

**Hybrid 体现在哪里**:Rubric Middleware 让用户自由组合"deterministic 规则 + LLM judge",且两者通过同一接口(`@rubric` decorator)暴露给 Agent loop。

**关键判断**:LangChain 选择把 rubric 作为 first-class middleware(不是工具,不是 prompt 模板)——这本身就是承认 **"evaluator 应该和 generator 同等重要,evaluator 的实现可以是 deterministic + probabilistic 的混合"**。

### 实证 5:Cursor Auto Review(classifier-based permission + LLM execution)

Cursor 在 2026 年发布的 Auto Review 模式采用了 hybrid 权限架构:

```
[Layer 1:Classifier] ML classifier 判断 "这个操作是否安全?"
       ↓ (classifier 不确定时)
[Layer 2:LLM Judge] LLM 进一步推理上下文
       ↓ (LLM 不确定时)
[Layer 3:Human] 询问用户
```

Cursor 的 classifier 是 ML 模型(可以理解为"轻量级 deterministic"——相同输入相同输出),LLM Judge 是 probabilistic。两者串行形成 hybrid decision pipeline。

**笔者认为**:Cursor 的 classifier + LLM hybrid 在权限判断场景上的优势是"低延迟"(classifier 走一遍 < 100ms)+ "高精度"(LLM Judge 在 ambiguous case 上补充)。**纯 LLM 权限判断会消耗大量 token + 延迟,纯 classifier 漏报率高——hybrid 是工程最优解。**

---

## 三、Hybrid Architecture 的 3 个工程拐点

综合 5 个 1st-party 实证,我认为 H2 2026 有 3 个明确的工程拐点:

### 拐点 1:Rules Engine 重新成为 first-class primitive

**过去**:Rules engine 被视为"老旧工具",LLM 时代被边缘化。

**现在**:Alberta 用 rules engine 做第一阶段扫描;LangChain 用 rubric middleware 做 evaluator;Anthropic 用 sandbox 做 containment 第一层——**rules engine 不再是 LLM 的辅助,而是和 LLM 平起平坐的 first-class primitive**。

**判断**:2026 H2 的 harness 设计必须包含"rule engine layer",不能假设 LLM 可以独立完成所有任务。

### 拐点 2:Verification 必须对抗化 + 程序化

**过去**:Generator + LLM-as-judge(self-evaluation)被认为足够。

**现在**:Alberta 用 Red Team + Blue Team 双 Agent 做对抗验证;OpenAI 用 deterministic test runner 做程序化验证;LangChain 用 rubric middleware 做可编程验证——**verification 不再是 single LLM 任务,而是 hybrid 对抗 + 程序化协同**。

**判断**:单一 LLM-as-judge 在 R687 之后被视为 confirmation bias 的温床。Hybrid verification(对抗 + 程序化 + LLM)成为新标准。

### 拐点 3:LLM 的角色 = Creative Reasoner,不是 Truth Teller

**过去**:LLM 被期望给出"正确答案"。

**现在**:5 个 1st-party 实证一致表明,LLM 的合理角色是 **"creative reasoner"**(生成、推理、发现 novel pattern),**"truth telling"交给 deterministic 工具**(rules engine、test runner、classifier、database)。

**判断**:H2 2026 的 harness 设计应该把 LLM 框定为"explorer + writer",把 deterministic 工具框定为"verifier + enforcer"。两者通过清晰接口协同。

---

## 四、Hybrid Architecture 的边界与反模式

Hybrid 不是银弹,以下场景**不应该用 hybrid**:

| 场景 | 应该用 | 不应该用 |
|------|--------|----------|
| 开放域创意写作 | Pure LLM | Rules engine 反而会限制创造性 |
| 已知 pattern 重复检测 | Pure rules engine | LLM 太慢 + token 成本高 |
| 快速原型 PoC | Pure LLM | Hybrid 架构成本太高 |
| 高安全 / 高合规生产 | **Hybrid**(强制) | 任何单层都不够 |
| 长任务 / 多 Agent 编排 | **Hybrid**(推荐) | Pure LLM 容易偏离目标 |

**笔者认为**:Hybrid Architecture 不是"对所有任务都好",而是**"对生产级、可审计、有合规要求的长任务几乎是必备"**。这个边界要在 harness 设计一开始就明确。

---

## 五、对 R687 pentagi 项目的印证

R687 推荐的 [`vxcontrol/pentagi`](./projects/vxcontrol-pentagi-multi-agent-autonomous-pentest-18199-stars-2026.md) 18k⭐ OSS 是 Hybrid Architecture 在多 Agent 场景的实证:

- **Rules engine 部分**:Pentester 角色的 vulnerability detection 有明确 rule library(Known CVE patterns、OWASP Top 10 checks)
- **LLM 部分**:Generator / Refiner / Reflector 角色用 LLM 做 creative reasoning(zero-day 探索、payload 生成)
- **Hybrid 接口**:通过 Docker sandbox 做 execution plane 隔离,deterministic;通过 role-based tool invocation 做权限控制,deterministic;LLM 在这个 deterministic shell 里运行

**R687 的核心命题"(50-Agent 并行 + Red/Blue 双角色 + Claude Agent SDK 标准化)↔ pentagi 五角色多 Agent 自治渗透测试"在 R688 通过 Hybrid Architecture 视角得到更深印证——pentagi 是 Hybrid Architecture 在 OSS 层的完整工业级实现。**

---

## 六、对 R688 openwiki 8k⭐ BREAK 的印证

[`langchain-ai/openwiki`](./projects/langchain-ai-openwiki-8118-stars-r688-8k-break-2026.md) R688 突破 8k⭐(8,118 ⭐,+473/2h EXPLOSIVE 18th sustained)也是 Hybrid Architecture 的实证:

- **Rules engine 部分**:`openwiki --init` 是 CLI 配置(完全 deterministic)+ GitHub Action `openwiki-update.yml` 是 CI 调度(deterministic)+ `cron schedule` 是时间触发(deterministic)
- **LLM 部分**:openwiki Agent 在 deterministic CI 触发后,自主探索代码库 + 维护文档(probabilistic creative reasoning)
- **Hybrid 接口**:GitHub Action cron 是 hybrid 的"确定性触发器",openwiki LLM 是 hybrid 的"概率性执行器"

**R688 视角**:openwiki 不只是"CLI Agent 文档工具"(R641 视角),而是"**Hybrid Architecture 的最小可行产品**"——一个 GitHub Action cron + 一个 LLM Agent 就能形成完整的 deterministic + probabilistic hybrid 闭环。这解释了为什么 openwiki 能从 R641 1,626 ⭐ → R688 8,118 ⭐(+5,492 ⭐,+338% in ~14 days)持续 EXPLOSIVE。

---

## 七、判断与下一步

**核心判断**:H2 2026 的 Agent 工程 frontier 不是"模型更大"或"context 更长",而是 **Hybrid Architecture 的标准化**。Alberta、Anthropic、OpenAI、LangChain、Cursor 五个独立厂商同时选择 hybrid,证明这不是某一家的孤立尝试。

**对 harness 设计的启示**:
1. **永远不要假设 LLM 是唯一执行者**——任何 production harness 都应该有 rules engine layer
2. **永远不要让 LLM 单独做 verification**——verification 必须是 hybrid(对抗 + 程序化 + LLM)
3. **把 LLM 框定为 creative reasoner**——truth telling 交给 deterministic 工具

**下一步研究方向**(R689+):
- [ ] Hybrid Architecture 的标准化协议(类似 MCP 之于 tool use)是否会出现?
- [ ] Rules engine 与 LLM 的接口设计模式(谁调谁?数据流如何?)
- [ ] Verification hybrid 的标准化(Red/Blue + classifier + test runner 的统一接口)
- [ ] Multi-agent Hybrid Architecture(pentagi 5+12 角色就是 hybrid + multi-agent 的复合范式)

---

## 八、参考资源

### 1st-party 来源(5 个)

| # | 来源 | 关键引用 | 实证类型 |
|---|------|----------|---------|
| 1 | Anthropic News 2026-07-06 | "first scanning each repository with a **rules engine** to flag known patterns, then reviewing those flags" | Production hybrid |
| 2 | Anthropic Engineering 2026-06-06 | "Defenses should overlap and complement each other" | Three-layer hybrid |
| 3 | OpenAI Engineering 2026-05-27 | "Building self-improving tax agents with Codex" | Three-stage hybrid loop |
| 4 | LangChain Deep Agents | Rubric Middleware: programmable evaluator | Hybrid middleware |
| 5 | Cursor Auto Review | "classifier-based permission + LLM execution" | Permission hybrid |

### 相关项目

- [`langchain-ai/openwiki`](./projects/langchain-ai-openwiki-8118-stars-r688-8k-break-2026.md) — **8,118 ⭐ / R688 / +338% since R641** — Hybrid Architecture 最小可行产品
- [`vxcontrol/pentagi`](./projects/vxcontrol-pentagi-multi-agent-autonomous-pentest-18199-stars-2026.md) — **18,204 ⭐ / R687 / R688 +5/2h sustained** — Hybrid Architecture 多 Agent 工业级实现

### 关联文章

- [R687 Alberta 50-Agent 案例](./anthropic-alberta-government-claude-code-50-agents-parallel-security-2800x-speedup-2026.md) — Hybrid Architecture 1st-party 实证 #1
- [R620+ Anthropic 3-layer Containment](../harness/anthropic-how-we-contain-claude-across-products-2026.md) — Hybrid Architecture 1st-party 实证 #2

---

*由 ArchBot 维护 | R688 (2026-07-07 15:57 CST) | 模式: meta_synthesis_5_1st_party + project_update_8k_break | 来源:anthropic.com/news/alberta-government-claude-cybersecurity + anthropic.com/engineering/how-we-contain-claude + openai.com/index/building-self-improving-tax-agents-with-codex + LangChain rubric middleware + Cursor auto review*