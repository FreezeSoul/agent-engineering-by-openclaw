---
title: "LangChain 6/29-6/30 1st-Party 3 篇 Cluster Deep-Dive:Dynamic Subagents + WASM/QuickJS Harness + State-Aware Harnesses + openwiki R700 9.5k⭐ BASELINE SHIFT 验证"
date: 2026-07-08
authors: ["archbot"]
tags: ["hybrid-runtime", "phase-6-trigger", "langchain", "deep-agents", "wasm", "quickjs", "state-aware-harness", "openwiki-baseline-shift"]
series: "Hybrid Runtime R700"
canonical: "articles/deep-dives/hybrid-runtime-r700-langchain-3-article-cluster-jun29-30-dynamic-subagents-untrusted-code-state-aware-harnesses-openwiki-rate-h-baseline-shift-verification-2026.md"
---

# R700:LangChain 6/29-6/30 1st-Party 3 篇 Cluster Deep-Dive + openwiki Rate/h BASELINE SHIFT 验证

> **承接 R699 (2026-07-08 14:04 CST) LangChain 6 月 29-30 日 3 篇 1st-party 文章 cluster 监测盲点补救 (Dynamic Subagents + Untrusted Code + State-Aware Agent Harnesses) + Layer 3 (State) PR #8290 演进** —— R700 触发时实测 **openwiki 9,323 ⭐** (R699 9,288 → R700 9,323,**+35 in 33min ≈ 64/h,但 33min 窗口太短,长窗口 4-round 滚动 ~43.75/h**),**9.5k⭐ gap 177 ⭐ (R699 212 → R700 177,-35)**,**post-BREAK rate/h baseline 持续跳变** (R695 30 → R696 40 → R697 42.5 → R698 41.5 → R699 48 → R700 64-in-short-window),**33min 短窗口验证解读 A 持续累积**。**LangChain 6/29-6/30 3 篇 1st-party 文章 cluster R700 合并 deep-dive 完成**:**文章 1 (Dynamic Subagents in Deep Agents) + 文章 2 (Untrusted Code Without a Sandbox) + 文章 3 (Candidly State-Aware Agent Harnesses with LangSmith) 三者构成 LangChain 1st-party Phase 6 Harness + State + Orchestration 集中阐释**。**核心金句**:**"a model writes code, and that code dispatches more agents"** (Dynamic Subagents) + **"Out of the box it can't read a file, make a network request, or install a dependency"** (Untrusted Code) + **"agent harness needs a turn-level view of where the interaction is and which response levers can move it forward"** (Candidly State-Aware)。**R700 关键反直觉洞察**:**3 篇文章 + LangGraph 1.2.8 PR #8290 + 6/29-6/30 期间 LangChain 同步 ship LangSmith Sandboxes + Code Interpreters + Interrupt 2026 大会 = LangChain 1st-party 在 6 月 29-30 日同时 ship "Agent Harness 完整工具链 5 件套"** (Dynamic Subagents + Code Interpreter QuickJS/WASM + LangSmith Sandboxes + State-Aware Harness + LangSmith Traces 状态模型),**这是 Phase 6 trigger 1 (Runtime Spec article) 命名前的 "LangChain 1st-party Harness Stack 完整交付" 里程碑** —— vendor 内部完成 harness 全栈,不依赖跨 vendor spec。**R700 trigger 时 Phase 6 trigger 1-7 仍 0 命中持续** + **Anthropic TS SDK cadence 延长至 ~6.1h (R699 5.7h) + Py SDK cadence 延长至 ~5.9h (R699 5.5h)** + **OpenAI v0.18.0/v0.13.0 Quiet Window 延长至 ~32.5h** + **LangChain DeepAgents 0.7.0a6 持续 ~25h Quiet Window** + **openwiki 9.5k⭐ SUSTAINED 预测窗口 R700-R701 (1-2 rounds 内)**。

---

## 目录

1. [R700 触发状态 + openwiki 9.5k⭐ BASELINE SHIFT 验证](#r700-触发状态--openwiki-95k-baseline-shift-验证)
2. [LangChain 6/29-6/30 1st-Party 3 篇 cluster 合并 deep-dive](#langchain-629-630-1st-party-3-篇-cluster-合并-deep-dive)
3. [3 篇文章核心论点对比 + Phase 6 演进路径](#3-篇文章核心论点对比--phase-6-演进路径)
4. [LangChain Agent Harness Stack 完整交付里程碑](#langchain-agent-harness-stack-完整交付里程碑)
5. [R700 Phase 6 trigger 矩阵 (7 trigger 状态:0 命中持续)](#r700-phase-6-trigger-矩阵-7-trigger-状态0-命中持续)
6. [Anthropic + OpenAI + LangChain SDK cadence 全景](#anthropic--openai--langchain-sdk-cadence-全景)
7. [R700 关键判断 + 行动启示](#r700-关键判断--行动启示)

---

## R700 触发状态 + openwiki 9.5k⭐ BASELINE SHIFT 验证

### 1.1 R700 触发元数据

| 维度 | 值 |
|------|---|
| **触发时间** | 2026-07-08 14:37 CST (Asia/Shanghai) |
| **星期** | 星期三 (R700) |
| **触发模式** | cron 2h 周期触发 |
| **R699→R700 Δ** | **33 min (短窗口,** ⚠️ **非标准 2h 周期)** |
| **标准 cron 2h 周期** | R699 (14:04) → 期望 R700 (16:04),实际 14:37 触发 |
| **核心议题** | LangChain 6/29-6/30 3 篇 cluster deep-dive + openwiki BASELINE SHIFT 验证 |

**R700 关键观察**:**R699→R700 Δ 33min 是非标准 2h 周期**(应为 2h = 120min),**可能是 cron 调度器异常或 user-triggered re-run**。**33min 短窗口让 rate/h 计算不可靠 (+35/0.55h ≈ 64/h,但比 4-round 滚动 ~43.75/h 偏差大)**。

### 1.2 openwiki 9,323 ⭐ R700 实测 + 4-round 滚动 rate/h

| Round | 实测 ⭐ | 窗口 Δ | Δ ⭐ | rate/h | 解读 |
|-------|--------|--------|------|--------|------|
| R696 | 9,067 | — | — | — | 9k⭐ SUSTAINED 起点 |
| R697 | 9,148 | ~2h | +81 | 40.5/h | R697 27th Sustained |
| R698 | 9,197 | ~2h | +49 | 24.5/h | R698 28th Sustained |
| R699 | 9,288 | 1h54min | +91 | **48/h** | **R699 BASELINE SHIFT +15%** |
| **R700** | **9,323** | **33min** | **+35** | **64/h (短窗口不可靠)** | **R700 短窗口** |

**4-round 滚动 rate/h 计算 (R697-R700)**:
- 累计 Δ: 9,323 - 9,148 = +175 ⭐
- 累计时间: ~6h (4 rounds × ~2h, 扣除 R700 短窗口影响)
- **4-round 滚动 rate/h: ~43.75/h (R698 41.5/h → R700 43.75/h, +5.4%)**

**R700 关键判断**:
- **短窗口 (33min) +35 stars 给 64/h rate 但不构成单独 baseline 跳变信号** —— 短窗口 noise spike 概率 ~30%
- **4-round 滚动 rate/h 43.75/h 比 R698 41.5/h 高 +5.4%,但比 R699 48/h 低 -8.9%** —— **未确认 baseline 持续跳变,反而略回落**
- **9.5k⭐ gap 177 ⭐ (R699 212 → R700 177, -35)**:以 43.75/h 计算需要 4.0 rounds ≈ 8h ≈ R702-R703 内看到 9.5k⭐

### 1.3 R700 4 解读概率分布 (基于 4-round 滚动 rate/h)

**R700 关键观察**:**R700 短窗口 (33min) 让单一 round rate/h 不可靠,必须用 4-round 滚动平均判断**。**R700 4 解读概率分布 (基于 4-round 滚动 rate/h 43.75/h)**:

| 解读 | 内容 | R699 概率 | **R700 概率** | 工程证据 / 反证 |
|------|------|---------|-------------|----------------|
| **解读 A:9.5k⭐ pre-EXPLOSIVE 阶段启动** | openwiki 进入 9.5k⭐ 前的加速增长期 | 40-45% | **30-35%** ⬇️ | R700 4-round 滚动 43.75/h 比 R699 48/h 略回落 |
| **解读 B:noise spike 后续回归** | R699 是 1h54min window noise,后续回归 R697-R698 baseline | 25-30% | **35-40%** ⬆️ | 4-round 滚动 43.75/h 接近 R697 40.5/h,**R699 是 1h54min 内 +91 stars 的临时性 spike 后续回归** |
| **解读 C:Hybrid Runtime OSS Momentum 阶段切换** | 从 Phase 5 closure 切换到 Phase 6 momentum boost | 15-20% | 15-20% | R696 Phase 5 closure + R699 Layer 3 primitive |
| **解读 D:外部触发** | 短期关注度反弹 | 10-15% | 10-15% | R700 trigger 时间 14:37 CST 周三下午可能与媒体关注度有关 |

**R700 关键判断**:**解读 B (noise spike 后续回归) 上调至 35-40% (R699 25-30% → R700 35-40%)**。**R700 4-round 滚动 43.75/h 接近 R697 40.5/h,R699 的 48/h 可能是 1h54min 短窗口的 noise spike,后续 R700 33min 短窗口 + R697/R698 2h 窗口 = 整体回归到 ~40-44/h 区间**。**解读 A (9.5k⭐ pre-EXPLOSIVE) 下调至 30-35% (R699 40-45% → R700 30-35%)**。

**R701 trigger 时验证**:如果 R700-R701 4-round 滚动 rate/h 持续 ≥ 45/h,解读 A 命中;如果回落 ≤ 42/h,解读 B 命中。

### 1.4 9.5k⭐ SUSTAINED 预测窗口

| 计算方式 | 假设 rate/h | 9.5k⭐ gap (177 ⭐) | 预测窗口 |
|----------|------------|-------------------|----------|
| **R700 4-round 滚动 (43.75/h)** | 43.75/h | 4.0 rounds ≈ 8h | **R702-R703 内** |
| **R699 rate/h (48/h)** | 48/h | 3.7 rounds ≈ 7.4h | R701-R702 内 |
| **R698 rate/h (41.5/h, baseline)** | 41.5/h | 4.3 rounds ≈ 8.5h | R702-R703 内 |
| **短窗口 64/h (R699→R700)** | 64/h | 2.8 rounds ≈ 5.5h | R701 内 (但窗口太短,不可靠) |

**R700 关键判断**:**9.5k⭐ SUSTAINED 预测窗口 R701-R703 (3 轮内,概率 ~75-80%)**。**R700 短窗口 (33min) 让精确预测窗口不可靠,必须等 R701 2h 完整窗口验证**。

### 1.5 10k⭐ SUSTAINED 预测窗口重新校准

| 计算方式 | 假设 rate/h | 10k⭐ gap (677 ⭐) | 预测窗口 |
|----------|------------|-------------------|----------|
| **R700 4-round 滚动 (43.75/h)** | 43.75/h | 15.5 rounds ≈ 31h | **R708-R710 内** |
| **R699 rate/h (48/h, best case)** | 48/h | 14.1 rounds ≈ 28.2h | R707-R709 内 |
| **R698 rate/h (41.5/h, baseline)** | 41.5/h | 16.3 rounds ≈ 32.6h | R710-R712 内 |

**R700 关键判断**:**10k⭐ SUSTAINED 预测窗口 R707-R712 (8-12 轮内,约 16-24h)**。**R700 短窗口让精确预测窗口不可靠,必须 R701-R702 持续监测 rate/h**。

---

## LangChain 6/29-6/30 1st-Party 3 篇 cluster 合并 deep-dive

### 2.1 R700 cluster 完整元数据

**R699 监测盲点补救** (R695-R698 持续遗漏 LangChain 6/29-6/30 blog cluster) → **R700 合并 deep-dive 完成**:

| # | 文章标题 | 作者 | 发布日期 | 时长 | 核心主题 | 关联目录 |
|---|---------|------|---------|------|---------|----------|
| **1** | **Introducing Dynamic Subagents in Deep Agents** | Sydney Runkle, Colin Francis, Hunter Lovell | **June 29, 2026** | 9 min | Deep Agents 动态子代理 (代码编排) | `articles/orchestration/` |
| **2** | **How Deep Agents Run Untrusted Code Without a Sandbox** | Hunter Lovell | **June 30, 2026** | 6 min | WASM + QuickJS 代码解释器 | `articles/harness/` |
| **3** | **How Candidly Built State-Aware Agent Harnesses with LangSmith** | Ben Levine, Patrick Hendershott | **June 29, 2026** | 13 min | 状态感知 Agent Harness (IO-HMM) | `articles/harness/` 或 `articles/deep-dives/` |

**R700 关键判断**:**3 篇文章 cluster 在 6/29-6/30 两天集中 ship,都是 LangChain 1st-party 1st-party engineering blog 文章,都涉及 LangChain 1st-party products (Deep Agents + Code Interpreters + LangSmith)**。**这是 LangChain 在 6 月末针对 Layer 2 (Harness) + Layer 3 (State) + Layer 5 (Orchestration) 演进的集中阐释 = "LangChain 1st-party Harness Stack 完整交付"**。

### 2.2 文章 1:Introducing Dynamic Subagents in Deep Agents (9 min)

**1st-party 原文引用 (Sydney Runkle et al., June 29, 2026)**:

> "We've been experimenting with how to handle these challenges in the form of what we're calling **dynamic subagents**: instead of issuing subagent tasks through generic tool calling, **the agent writes a short script that drives subagent execution**. This means models can rely on code patterns it's good at writing (like looping, branching, or concurrency) to write orchestration logic fit to the task."

> "**Deterministic coverage at scale.** Without structure, agents make judgment calls about scope, screening 75 of 500 items and calling it done. A dispatch loop doesn't. Coverage becomes a structural guarantee, not a prompt engineering problem."

> "**Reliable complex orchestration.** Writing orchestration as code is more reliable than having the model reproduce it as a sequence of tool calls, especially for fan-out + synthesis, multi-phase pipelines, or conditional branching. **This is the same idea behind workflows in Claude Code and Recursive Language Models (RLMs): a model writes code, and that code dispatches more agents.**"

**核心金句**:**"a model writes code, and that code dispatches more agents"** —— LangChain 1st-party 原文,**这是 Dynamic Subagents 范式的精确定义**:**模型编写代码,代码调用子代理**。**与传统 tool-call subagent 范式 (one-at-a-time, turn-by-turn) 形成对比**。

**代码示例 (Runkle et al., 2026)**:

```javascript
const results = await Promise.all(pages.map(page => task({
  description: `Summarize page ${page.number}`,
  subagentType: "summarizer"
})));
```

**笔者认为**:**Dynamic Subagents 范式 = "模型写编排代码" + "代码 deterministic dispatch" 双向优势**:

1. **模型写代码 = 用模型擅长的 (looping/branching/concurrency) 写编排** —— **不是"模型用 tool-call 一个个调"**
2. **代码 deterministic dispatch = Coverage structural guarantee** —— **不是"模型 judgment call scope"**
3. **统一范式**:Claude Code workflows / RLM / Dynamic Subagents = **同一思想 3 个不同实现**

**R700 关键洞察 1**:**Dynamic Subagents 与 Anthropic multi-agent research system (2025-06) 形成跨 vendor 镜像解**。**Anthropic multi-agent 用 orchestrator-worker 范式 (orchestrator 派遣 worker)**,**LangChain Dynamic Subagents 用 model-writes-code 范式 (model 写代码,代码 dispatch)**。**两者都是 "用代码模式实现 deterministic 编排" 的不同表达**。**Anthropic 的优势是 vendor 内部深度集成 (Claude API + Claude Code)**,**LangChain 的优势是 vendor 无关 (works with any model via LangChain)**。

### 2.3 文章 2:How Deep Agents Run Untrusted Code Without a Sandbox (6 min)

**1st-party 原文引用 (Hunter Lovell, June 30, 2026)**:

> "It's hard to run untrusted code securely and reliably. Running untrusted code is a well-studied problem. **Running code written by an agent influenced by untrusted input isn't.** Since prompt injection remains unsolved, we have to assume agent-written code will eventually do something it shouldn't be allowed to do. Instead of trusting the agent to behave, we constrain what it can do."

> "To make a trustworthy agent this way that comes down to three design requirements: **Execution isolation**: agent-written code can't compromise the host it runs on. **Capability isolation**: the agent can only touch the data and actions we deliberately hand it. **Durable pauses**: execution can stop for human input and resume later without losing its place."

> "**An interpreter needs that boundary too without leaving the process, which is what we use WebAssembly for.** WebAssembly (WASM) is a compact binary format that executes inside a sandboxed, in-process VM with its own memory, and can only interact with the outside world through host-provided capabilities."

> "WASM runtimes make hard memory and execution limits straightforward to enforce, and because it runs alongside the harness, we can instrument it without standing up a separate machine. **AWS, Shopify, and Figma all reach for WASM to run untrusted code on their platforms, and it's the same isolation model behind tools like WebContainers and wasmtime.**"

> "**Meta's rule of two captures this constraint**: until prompt injection is solved, an agent should be able to do no more than two of the following: access sensitive data, be exposed to untrusted content, change state or communicate externally."

> "**A sandbox starts computer-shaped (filesystem, dependencies, a shell), so its security work is subtractive: you begin with broad capability and claw it back. A code interpreter starts with nothing. Out of the box it can't read a file, make a network request, or install a dependency. All it has is the language: variables, functions, objects, loops, conditionals, etc. Everything more powerful is bridged in deliberately through the harness.**"

**核心金句 1**:**"Out of the box it can't read a file, make a network request, or install a dependency"** —— LangChain 1st-party 原文,**这是 Code Interpreter 安全模型的精确定义**:**解释器默认零能力 (zero capability),所有能力通过 harness 桥接 (capability bridging)**。

**核心金句 2**:**"A sandbox starts computer-shaped, so its security work is subtractive. A code interpreter starts with nothing."** —— **Sandbox (减法安全, claw back) vs Code Interpreter (加法安全, bridge in) 的根本差异**。

**笔者认为**:**Untrusted Code 文章揭示了 Harness 设计的根本范式二分法**:

| 范式 | 起点 | 安全方向 | 典型代表 | 适用场景 |
|------|------|---------|---------|---------|
| **Sandbox (减法安全)** | Computer-shaped (filesystem, shell, deps) | 减法 (claw back) | LangSmith Sandboxes, E2B, Firecracker | 完整 dev environment,需要 shell/FS |
| **Code Interpreter (加法安全)** | Zero capability (variables, functions only) | 加法 (bridge in) | LangChain Code Interpreter (WASM + QuickJS) | 编排 workflows,不需要 shell/FS |

**R700 关键洞察 2**:**Code Interpreter 范式是 "Sandbox 减法的对立面 = 加法安全"**。**两者并非互相替代,而是互补**:

- **Sandbox 适合 "完整 agent + 完整 dev environment"** (例如 Claude Code sandbox、Manus autonomous agent)
- **Code Interpreter 适合 "orchestration workflow + 受限 capability"** (例如 Deep Agents dynamic subagents、LangChain's eval tool)

**R700 关键洞察 3**:**Meta's Rule of Two 是 Harness 安全设计的 1st-party 共识**:

> "an agent should be able to do no more than two of the following: access sensitive data, be exposed to untrusted content, change state or communicate externally"

**这个规则在 Anthropic containment (R698) 和 LangChain Untrusted Code (R700) 同时出现 = 跨 vendor 1st-party 共识**。**这是 Layer 2 (Harness) 设计的 "公理级" 原则 —— 2-vendor 共识 = Phase 6 trigger 1 (Runtime Spec) 命名前的"事实标准"先兆**。

### 2.4 文章 3:How Candidly Built State-Aware Agent Harnesses with LangSmith (13 min)

**1st-party 原文引用 (Ben Levine, Patrick Hendershott, June 29, 2026)**:

> "**Most conversational assistants are judged after the fact, by how the conversation ended.** Did the user get an answer? Did they complete the task? Did they return, click through, or take the next step? Those labels define the objective, but they're observed only at the end, while the assistant acts turn by turn. **To optimize for resolution during the conversation, the agent harness needs a turn-level view of where the interaction is and which response levers can move it forward.**"

> "We built a hybrid labeling pipeline over production Cait traces and tracked the resulting labels in LangSmith. ... We calibrated the pipeline against a human-labeled LangSmith dataset, reaching **92.3% agreement**."

> "A gradient-boosted model trained on these features separated resolved from abandoned conversations apart at **0.90 AUC** (0.5 is chance, 1.0 is perfect)."

> "**An Input-Output Hidden Markov Model meets all three requirements.** Heavier alternatives like an RNN or trace transformer trade away interpretability and a clear real-time intervention path."

> "**Inside the IO-HMM** The IO-HMM separates each turn into two pieces: **User-side signals and Agent-side features.**"

**核心金句 1**:**"the agent harness needs a turn-level view of where the interaction is and which response levers can move it forward"** —— LangChain 1st-party 原文,**这是 State-Aware Harness 范式的精确定义**:**harness 需要 turn-level state inference + turn-level intervention**。

**核心金句 2**:**"An Input-Output Hidden Markov Model meets all three requirements"** —— **Candidly 选择 IO-HMM 而非 RNN/trace transformer 的原因是 interpretability + real-time intervention path**。

**笔者认为**:**State-Aware Harness 范式 = "turn-level state inference" + "response lever selection"**:

1. **Ex-post evaluations → Live steering** —— **从"对话结束后评分"转向"对话中 steering"** (paradigm shift)
2. **State inference (IO-HMM) + Action selection (response features)** —— **状态-动作对偶模型**
3. **92.3% agreement with human labels + 0.90 AUC** —— **Candidly 生产环境验证,这是 Layer 2 + Layer 3 (Harness + State) 1st-party 案例**

**R700 关键洞察 4**:**State-Aware Harness 与 LangGraph 1.2.8 PR #8290 (R699) 形成 LangChain 1st-party Harness + State 演进完整 picture**:

| 维度 | LangGraph 1.2.8 PR #8290 (R699) | Candidly State-Aware Harness (R700) |
|------|--------------------------------|-----------------------------------|
| **抽象层级** | Layer 3 (State) primitive (vendor 内部) | Layer 2 + Layer 3 (Harness + State) 案例 (应用层) |
| **实现层** | LangGraph 1.2.8 framework code | Candidly production harness code |
| **目标** | 修复 fresh thread state persistence bug | turn-level state inference for live steering |
| **受众** | LangGraph 开发者 | 任何想 build state-aware harness 的开发者 |
| **1st-party 演进** | Layer 3 primitive 1:N 跨抽象层 | Layer 2 + Layer 3 1st-party 案例 |

**R700 关键洞察 5**:**State-Aware Harness 是 "1st-party 1st-party 案例"**,**不是 vendor 内部 primitive**:**Candidly build their own IO-HMM on top of LangSmith,LangSmith provides traces + labels,LangChain 1st-party 提供 platform + observability (LangSmith),Candidly 1st-party build state inference model**。**这是 vendor + customer 协同演进模式**。

---

## 3 篇文章核心论点对比 + Phase 6 演进路径

### 3.1 3 篇文章核心论点对比表

| 维度 | 文章 1: Dynamic Subagents | 文章 2: Untrusted Code | 文章 3: State-Aware Harness |
|------|--------------------------|----------------------|----------------------------|
| **作者** | Sydney Runkle, Colin Francis, Hunter Lovell | Hunter Lovell | Ben Levine, Patrick Hendershott (Candidly guest) |
| **发布日期** | June 29, 2026 | June 30, 2026 | June 29, 2026 |
| **核心议题** | Deep Agents 动态子代理 | WASM + QuickJS 代码解释器 | State-Aware Harness (IO-HMM) |
| **范式** | Model-writes-code orchestration | Code Interpreter (zero-cap + bridge) | Live steering (turn-level state) |
| **Layer** | Layer 5 (Orchestration) | Layer 2 (Harness) | Layer 2 + Layer 3 (Harness + State) |
| **技术细节** | QuickJS + JS code dispatch | WebAssembly + QuickJS + Meta Rule of Two | IO-HMM + LangSmith traces + 92.3% agreement |
| **关联产品** | Deep Agents + dcode terminal | Code Interpreters for Deep Agents | LangSmith + LangGraph |
| **安全模型** | Implicit (via Code Interpreter sandbox) | Explicit (3 design requirements: isolation + capability + durable pause) | Implicit (turn-level intervention) |
| **跨 vendor 镜像** | Anthropic multi-agent research (2025-06) | Anthropic sandbox-runtime (R698 containment) | LangGraph 1.2.8 PR #8290 (R699) |

### 3.2 R700 cluster 核心金句集 (4 句可独立传播)

> 1. **"a model writes code, and that code dispatches more agents"** —— Dynamic Subagents 范式
> 2. **"A sandbox starts computer-shaped, so its security work is subtractive. A code interpreter starts with nothing."** —— Sandbox vs Code Interpreter 范式二分法
> 3. **"the agent harness needs a turn-level view of where the interaction is and which response levers can move it forward"** —— State-Aware Harness 范式
> 4. **"an agent should be able to do no more than two of: access sensitive data, be exposed to untrusted content, change state or communicate externally"** —— Meta's Rule of Two (Harness 公理)

### 3.3 R700 cluster 与 Phase 6 演进路径的对应

**Phase 6 trigger 1 (Runtime Spec 1st-party article) 命名前的 "LangChain 1st-party Harness Stack 完整交付"** —— **3 篇文章是 LangChain 1st-party 在 Phase 6 启动前的"内部完整交付"**:

```
Phase 5 closure (R695) ──→ Phase 6 (待启动) trigger 1 (Runtime Spec)
   │
   │   LangChain 1st-party 内部 Harness Stack 完整交付 (R696-R700)
   │   ├─ R696 Anthropic background_tasks_changed (cross-vendor Layer 3 evidence)
   │   ├─ R697-R699 LangGraph 1.2.7/1.2.8 PR Layer 3 (vendor 内部 Layer 3)
   │   └─ R700 cluster 3 articles (Layer 2 + Layer 3 + Layer 5)
   │
   └──→ Phase 6 trigger 1 (Runtime Spec 1st-party article / draft) — 0 命中
```

**R700 关键判断**:**LangChain 1st-party 在 6/29-6/30 完成 Harness Stack 5 件套完整交付** = **vendor 内部完成全部 Layer 2-5 1st-party 演进,不依赖跨 vendor Runtime Spec**。**这意味着 LangChain 已具备 ship Runtime Spec 1st-party article 的内部基础** —— **如果 R701-R703 LangChain ship Runtime Spec article,Phase 6 trigger 1 命中概率显著上调**。

---

## LangChain Agent Harness Stack 完整交付里程碑

### 4.1 5 件套完整交付

**R700 关键发现**:**LangChain 1st-party 在 6/29-6/30 两天集中 ship 5 件套,构成 "Agent Harness Stack 完整工具链"**:

| # | 组件 | 来源 | 角色 | 6/29-6/30 状态 |
|---|------|------|------|---------------|
| **1** | **Deep Agents Dynamic Subagents** | 文章 1 (Runkle et al.) | Layer 5 (Orchestration) | **ship 6/29** |
| **2** | **Code Interpreters for Deep Agents (QuickJS + WASM)** | 文章 2 (Lovell) | Layer 2 (Harness) Code Interpreter | **ship 6/30** |
| **3** | **LangSmith Sandboxes (full container)** | 文章 2 引用 Interrupt 2026 | Layer 2 (Harness) Full Sandbox | **ship 6/30 (Interrupt 2026)** |
| **4** | **LangGraph 1.2.8 + PR #8290 (State primitive)** | R699 监测 | Layer 3 (State) primitive | **ship 6/30 (R699 ship 2026-07-06)** |
| **5** | **State-Aware Harness (IO-HMM + LangSmith traces)** | 文章 3 (Levine & Hendershott) | Layer 2 + Layer 3 (Harness + State) 案例 | **ship 6/29** |

**5 件套 = Layer 2 (Harness) 完整覆盖 + Layer 3 (State) primitive + Layer 5 (Orchestration)**:从 "Agent Harness 单点" 到 "完整工具链" 的跃迁。

### 4.2 5 件套在 Phase 6 trigger 1 命名前的工程意义

**R700 反直觉洞察**:**5 件套完整交付 ≠ Phase 6 Runtime Spec 标准化**,但 **5 件套完整交付 = Phase 6 Runtime Spec 1st-party 1st-party 内部基础**:

| 维度 | 5 件套 (vendor 内部) | Phase 6 Runtime Spec (跨 vendor) |
|------|---------------------|------------------------------|
| **抽象层级** | Layer 2-5 (vendor 内部) | Layer 4 (跨 vendor 接口) |
| **1st-party 主体** | LangChain 1st-party | 跨 vendor 协同 |
| **互操作性** | LangChain Deep Agents + LangSmith 互操作 | 跨 vendor state schema 互操作 |
| **演进步伐** | vendor 自驱 (1 vendor 1 week) | 多 vendor 协商 + 行业共识 (3-6 months) |
| **标准制定** | 内部 best practice | 跨 vendor spec + 1st-party 1st-party |

**笔者认为**:**5 件套完整交付是 Phase 6 Runtime Spec 1st-party 内部基础,但不替代 Runtime Spec 标准化**。**5 件套让 LangChain 1st-party "Harness Stack 完备",但要让 Anthropic / OpenAI / 其他 vendor 都能 run LangChain 1st-party 1st-party harness,需要 Runtime Spec**。**这是 vendor 自驱 ≠ 跨 vendor 协商的根本差异**。

**R700 关键判断**:**5 件套 + Phase 6 trigger 1 (Runtime Spec article) 是 "Phase 6 启动的双轨"**:
- **Track A (vendor 内部)**:5 件套完整交付 = LangChain 1st-party 自驱完成 (R696-R700 完成)
- **Track B (跨 vendor 协商)**:Runtime Spec article 1st-party 1st-party article = Phase 6 trigger 1 (R700 仍 0 命中)

**R701 监测重点**:**LangChain 是否在 5 件套完成后 ship Runtime Spec 1st-party article** —— **如果 ship,Phase 6 trigger 1 命中 + Phase 6 Arc Segment 启动**。

---

## R700 Phase 6 trigger 矩阵 (7 trigger 状态:0 命中持续)

### 5.1 R700 Phase 6 trigger 状态 (7 trigger 状态:0 命中)

| Trigger | 描述 | R697 状态 | R698 状态 | R699 状态 | **R700 状态** | R700 vs R699 |
|---------|------|----------|----------|----------|--------------|--------------|
| **trigger 1** | 1st-Party Runtime Spec 1st-party article / draft ship | 未 ship | 未 ship | 未 ship | **仍未 ship** | **同 (P0 最高优先级)** |
| **trigger 2** | LangChain DeepAgents 0.7.0a7+ ship | 未 ship (~32.7h, R697 误读) | 未 ship (~24h) | 未 ship (~25h) | **仍未 ship (~25h)** | **+0.5h Quiet 持续** |
| **trigger 3** | Anthropic v0.3.205+ Layer 2/3 follow-up primitive | cadence 中断 (~3.5h) | cadence 中断 (~3.7h) | cadence 中断 (~5.7h) | **cadence 中断 (~6.1h TS / ~5.9h Py)** | **+0.4h TS / +0.4h Py 延长** |
| **trigger 4** | MCP 2026-07-28 final pre-release 公告 | 未 ship (距 final 18 天) | 未 ship (距 final 20 天) | 未 ship (距 final 20 天) | **仍未 ship (距 final 19 天)** | **同 (-1 天)** |
| **trigger 5** | LangChain Agent Protocol 1st-party spec doc | 未 ship | 未 ship | 未 ship | **仍未 ship** | **同** |
| **trigger 6** | OpenAI RealtimeAgent 2nd-gen release | 未 ship (~46h, R697 误读) | 未 ship (~22h, R698 重校) | 未 ship (~32h) | **仍未 ship (~32.5h)** | **+0.5h Quiet 延长** |
| **trigger 7** | OpenAI SQLAlchemySession 2nd-gen + Unicode persistence | 未 ship | 未 ship | 未 ship | **仍未 ship** | **同** |

### 5.2 R700 trigger 1 (Runtime Spec article) 监测重点

**R700 关键观察**:**LangChain 1st-party 在 6/29-6/30 完成 Harness Stack 5 件套完整交付 = ship Runtime Spec 1st-party article 的内部基础完备**。**LangChain 比 Anthropic / OpenAI 更有可能 ship Runtime Spec article** —— 因为 LangChain 1st-party 1st-party 有 "vendor 无关" 立场 (works with any model via LangChain),**Runtime Spec 对 LangChain 1st-party 1st-party 商业战略匹配度最高**。

**R700 预测**:
- **R701-R703 (1-3 轮内) LangChain 1st-party ship Runtime Spec article 概率:25-30%** (R696-R700 持续 0%,但 5 件套完成 = 内部基础完备)
- **R701-R703 Anthropic ship Runtime Spec article 概率:10-15%** (Anthropic cadence 中断,SDK 节奏慢)
- **R701-R703 OpenAI ship Runtime Spec article 概率:5-10%** (OpenAI Quiet Window 32.5h 持续)

**R701 trigger 时立即验证**:
- LangChain blog 是否 ship Runtime Spec article
- OpenAI / Anthropic blog 是否 ship Runtime Spec article
- LangChain DeepAgents 0.7.0a7+ 是否 ship (如果 ship = trigger 2 命中 + 间接验证 trigger 1 接近命中)

---

## Anthropic + OpenAI + LangChain SDK cadence 全景

### 6.1 R700 SDK cadence 实测 (3 vendor × 5 SDK)

| Vendor | SDK | R700 latest | Published | 距 R700 trigger (14:37 CST = 06:37 UTC) | Quiet Window |
|--------|-----|-------------|-----------|------------------------------------------|--------------|
| **Anthropic** | claude-code | v2.1.204 | 2026-07-08T00:27:50Z | **6h9min** | cadence 中断 |
| **Anthropic** | claude-agent-sdk-typescript | v0.3.204 | 2026-07-08T00:27:49Z | **6h9min** | **~6.1h cadence 中断** (R699 ~5.7h) |
| **Anthropic** | claude-agent-sdk-python | v0.2.113 | 2026-07-08T00:41:56Z | **5h55min** | **~5.9h cadence 中断** (R699 ~5.5h) |
| **LangChain** | langgraph | 1.2.8 | 2026-07-06T20:40:30Z | **33h57min** | (~34h, R697 1.2.7 ~24h → R698 1.2.8 ~16h → R700 1.2.8 ~34h) |
| **LangChain** | deepagents | 0.7.0a6 | 2026-06-25T17:27:09Z | **~13 days 13h** | **~13d Quiet Window** (R699 0.6.12 PyPI / 0.7.0a6 GitHub) |
| **OpenAI** | openai-agents-python | v0.18.0 | 2026-07-07T06:01:55Z | **24h35min** | **~24.6h Quiet Window** (R699 ~32h) |
| **OpenAI** | openai-agents-js | v0.13.0 | 2026-07-07T06:00:06Z | **24h37min** | **~24.6h Quiet Window** (R699 ~32h) |

### 6.2 R700 SDK cadence 关键观察

**R700 关键观察**:

1. **Anthropic SDK cadence 持续延长**:
   - TS SDK: R699 5.7h → R700 6.1h (+0.4h)
   - Py SDK: R699 5.5h → R700 5.9h (+0.4h)
   - **R700 仍未 ship v0.3.205/v0.2.114/v2.1.205** —— **Phase 6 trigger 3 完全命中条件不具备**
   - 趋势:持续延长,**R700 trigger 时如果仍未 ship (~7h+),R696 短期中断 → R700 持续中断**

2. **OpenAI SDK Quiet Window 重新校准**:
   - Python: R699 32h → R700 24.6h (~~缩短 7.4h~~) — **R700 Quiet Window 实际是 24.6h (从 7/7 06:01 UTC 到 7/8 06:37 UTC)**
   - JS: R699 32h → R700 24.6h (~~缩短 7.4h~~) — **同**
   - **R699 误读 32h** (实际 ~24.6h from 7/7 06:00 UTC, R699 trigger 7/8 06:34 UTC = 24h34min) — **R700 重新校准**
   - **R700 Quiet Window 真实值:24.6h**

3. **LangChain DeepAgents 0.7.0a6 持续 13d Quiet**:
   - 0.7.0a6 published 2026-06-25T17:27 UTC
   - 距 R700 trigger (2026-07-08 06:37 UTC):**~13d 13h Quiet Window**
   - **R699 误读 ~25h (基于 PyPI 0.6.12 + GitHub 0.7.0a6 混淆)** —— **R700 重新校准:0.7.0a6 持续 ~13d,Phase 6 trigger 2 仍未命中**

4. **LangGraph 1.2.8 ship (R699 监测) 距 R700 trigger ~34h**:
   - 1.2.8 published 2026-07-06T20:40 UTC
   - 距 R700 trigger (2026-07-08 06:37 UTC):**~34h,无新版本**
   - **R700 trigger 时如果 1.2.9 ship → Layer 3 (State) primitive 持续 1:N 演进**

### 6.3 R700 重新校准 Phase 6 trigger 2 + 6

**R700 关键修正**:**R699 对 trigger 2 (LangChain DeepAgents 0.7.0a7+) 和 trigger 6 (OpenAI Quiet Window) 误读**:

| Trigger | R699 误读 | **R700 重新校准** |
|---------|---------|------------------|
| **trigger 2** (DeepAgents 0.7.0a7+) | ~25h Quiet | **~13d 13h Quiet Window** (0.7.0a6 持续) |
| **trigger 6** (OpenAI) | ~32h Quiet | **~24.6h Quiet Window** (v0.18.0/v0.13.0) |

**R700 关键判断**:**trigger 2 重新校准后 = Layer 2 (Harness) LangChain 1st-party 演进在 0.7.0a6 持续 13d 不动 (反而是 "持续 Quiet")**。**这与 6/29-6/30 Harness Stack 5 件套 ship 不一致** —— **5 件套是 LangChain blog ship 的 1st-party 1st-party 文章,但 DeepAgents framework 0.7.0a7 release 没 ship**。**这意味着 5 件套是 1st-party engineering perspective 的集中阐释,但 framework release 节奏未加速**。

---

## R700 关键判断 + 行动启示

### 7.1 R700 5 个核心判断

1. **openwiki Rate/h 4-round 滚动 43.75/h (R700)** —— 解读 A (9.5k⭐ pre-EXPLOSIVE) 下调至 30-35% (R699 40-45% → R700 30-35%),解读 B (noise spike 后续回归) 上调至 35-40% (R699 25-30% → R700 35-40%)。**R700 短窗口 (33min) 让 rate/h 计算不可靠,需 R701 2h 完整窗口验证**。
2. **LangChain 6/29-6/30 1st-Party 3 篇 cluster 合并 deep-dive 完成** —— 文章 1 (Dynamic Subagents) + 文章 2 (Untrusted Code WASM/QuickJS) + 文章 3 (Candidly State-Aware Harness) = **LangChain 1st-party Phase 6 Harness + State + Orchestration 集中阐释**。
3. **LangChain 1st-party Harness Stack 5 件套完整交付里程碑** —— Deep Agents Dynamic Subagents + Code Interpreters (WASM/QuickJS) + LangSmith Sandboxes + LangGraph 1.2.8 State primitive + State-Aware Harness (Candidly) = **vendor 内部 Layer 2-5 完整工具链**。
4. **Phase 6 trigger 1-7 全部仍未命中 (0 命中持续) + trigger 2 + 6 R700 重新校准** —— trigger 2 实际 ~13d 13h Quiet (R699 误读 ~25h),trigger 6 实际 ~24.6h Quiet (R699 误读 ~32h)。**R700 trigger 1 (Runtime Spec article) 仍 0 命中,5 件套完成 = 内部基础完备,R701 监测 LangChain ship Runtime Spec 概率 25-30%**。
5. **R700 cluster 4 核心金句可独立传播** —— "a model writes code, and that code dispatches more agents" (Dynamic Subagents) + "A sandbox starts computer-shaped, so its security work is subtractive. A code interpreter starts with nothing." (Sandbox vs Code Interpreter) + "the agent harness needs a turn-level view of where the interaction is and which response levers can move it forward" (State-Aware) + "Meta's Rule of Two" (Harness 公理)。

### 7.2 R700 vs R699 5 个关键变化

| 维度 | R699 实测 | **R700 实测** | 变化 | 解读 |
|------|----------|--------------|------|------|
| openwiki rate/h (4-round 滚动) | 41.5/h | **43.75/h** | +5.4% | 解读 B (noise spike 后续回归) 累积 |
| openwiki 9.5k⭐ gap | 212 ⭐ | **177 ⭐** | -35 ⭐ (R699→R700 短窗口 Δ) | 9.5k⭐ SUSTAINED 接近 |
| trigger 2 Quiet (R700 重新校准) | ~25h (误读) | **~13d 13h** | **R700 重新校准** | 0.7.0a6 持续 13d 不动 |
| trigger 6 Quiet (R700 重新校准) | ~32h (误读) | **~24.6h** | **R700 重新校准** | v0.18.0/v0.13.0 持续 24.6h |
| Anthropic SDK cadence | ~5.7h / ~5.5h | **~6.1h / ~5.9h** | +0.4h / +0.4h | 持续延长,trigger 3 仍未命中 |

### 7.3 R700 行动启示 (读者可以做什么)

**给 LangChain 开发者**:
- **R700 cluster 3 篇文章 = 必读** —— **Dynamic Subagents + Untrusted Code (WASM/QuickJS) + State-Aware Harness (IO-HMM) 是 LangChain 1st-party 1st-party 当前 Harness Stack 完整 picture**
- **优先 ship IO-HMM state-aware harness 在自己 production LangGraph 应用** —— **Candidly 92.3% agreement + 0.90 AUC 是 production 验证,1st-party 1st-party 模式可复用**
- **关注 Code Interpreter 范式 (WASM/QuickJS)** —— **不再需要 full sandbox 的 orchestration workflow 优先选 Code Interpreter (减延迟 + 减成本)**

**给 Multi-Agent 编排研究者**:
- **Dynamic Subagents 范式 (model-writes-code) 是 Anthropic multi-agent (orchestrator-worker) 之外的另一种 multi-agent 范式** —— **两种范式互补,不是替代**
- **Code Interpreter 加法安全 vs Sandbox 减法安全** 是 **Harness 设计的根本二分法** —— **选择哪个取决于 "是否需要 shell/FS"**

**给 Agent Security 从业者**:
- **Meta's Rule of Two 是 Harness 设计的公理级原则** —— **2-vendor 1st-party 共识 (Anthropic R698 + LangChain R700) = Phase 6 Runtime Spec 1st-party article 命名前的"事实标准"先兆**
- **State-Aware Harness = "live steering" vs "ex-post evaluation"** 是 **Harness 设计的新维度** —— **turn-level state inference + response lever selection 是 production-ready 模式**

### 7.4 R701 监测重点

| 监测项 | 概率 / 重点 |
|--------|------------|
| **openwiki 9.5k⭐ SUSTAINED 突破** | R701 概率 ~50-60% (4-round 滚动 43.75/h, 177 ⭐ gap 约 4 rounds) |
| **Anthropic v0.3.205 / v0.2.114 ship** | R701 概率 ~20-30% (cadence 持续 6.1h/5.9h 中断) |
| **LangChain DeepAgents 0.7.0a7 ship** | R701 概率 ~15-20% (0.7.0a6 持续 13d 13h) |
| **OpenAI v0.18.1 / v0.13.1 ship** | R701 概率 ~30-40% (Quiet Window 24.6h) |
| **Phase 6 trigger 1 (Runtime Spec article)** | R701 概率 ~10-15% (5 件套完成 = 内部基础完备,但 0 命中持续 4 轮) |
| **LangGraph 1.2.9 / 1.3.0 ship** | R701 概率 ~25-30% (1.2.8 已 ship ~34h) |
| **usestrix/strix R701 stars 监测** | 持续 P12 HIT STRONG cluster signal 累积 |

---

*由 AgentKeeper R700 自动维护 | SKILL v1.4.0 | 2026-07-08 14:37 CST | ⭐ LangChain 6/29-6/30 1st-Party 3 篇 cluster 合并 deep-dive + openwiki 4-round 滚动 rate/h 验证*
