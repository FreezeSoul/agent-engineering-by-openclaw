---
title: "ksimback/looper: Claude Code 的 Loop 设计教练，把 Harness 工程化做到 /goal 之前"
slug: ksimback-looper-claude-code-loop-design-coach-554-stars-2026
date: 2026-07-01
tags: [AI Agent, Claude Code, Skills, Harness, Evaluator Loop, Cross-Model Review, Cluster Validation]
repo: ksimback/looper
stars: 554
license: MIT
source: github.com/ksimback/looper
related_article: anthropic-launch-your-agent-skill-as-complete-harness-2026
cluster: R605 Skill-as-Harness Validation
---

# ksimback/looper: Claude Code 的 Loop 设计教练，把 Harness 工程化做到 /goal 之前

> 在 [R605](/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md) 文章里，我们论证了 Anthropic `anthropics/launch-your-agent` 是「Skill 自己变成 Harness」的开源范式。ksimback/looper 是 13 天内出现的**第二个**走相同范式的项目，它把焦点从「Managed Agent 生命周期」切到「Loop 设计质量」——核心洞见是：「在你写第一行 plan 之前，先把 loop shape 评审通过，比任何后续护栏都管用。」

---

## 核心命题

`/goal` 和 `/loop` 是 Claude Code 内置的两个「看起来像 loop 的工具」。`ksimback/looper` 的出现，本质上是社区对这两个工具的**工程化补丁**——它让人在跑 loop 之前，先**设计**一个 reviewable、可移植、可观测的 loop。

**这个项目解决了一个具体的工程难题**：当你（或你的团队）想用 Claude Code 跑一个长任务、多迭代、带 review gate 的 agent loop 时，传统做法是「写一段 prompt → 跑 → 看到效果不对 → 再调」——这种*vibe-driven*的工作方式让 80% 的时间花在调试 prompt，而不是交付结果。`ksimback/looper` 把这个流程压缩成：

1. 一段访谈收集 goal + context（**interview 阶段**）
2. 把 fuzzy idea 写成 `loop.yaml`（**typed spec**）
3. 调用 LLM 检查这个 spec 是否满足 best-practice rubric（**coaching gate**）
4. 用户可以选择接哪个 reviewer / judge 模型（**cross-model gate**）
5. 输出 `RUN_IN_SESSION.md` 喂回当前 session（**execution**），或者导出 `loop.resolved.json` 喂给外部 runner（**portability**）

**关键洞察**：loop *设计*的时间远比 loop *运行*的时间值钱。一个跑 12 轮的 loop 如果 shape 错了，浪费几十分钟 / 几百 token；一个被 review 1 次就 pass 的 loop shape，反而几小时就跑完了正确结果。**Looper 把「设计成本」从「运行成本」里挪出来**——这是工程师和 vibe-promptler 之间的分水岭。

---

## 为什么值得关注

### 1. Harness-as-Skill 范式的第二个开源实证（R605 Cluster Validation）

2026 年 6 月共有 3 个独立的 Claude Code Skill 项目都把「Harness 工程」封装成 Skill：

| 项目 | License | Stars | 焦点 | Cluster 角色 |
|------|---------|-------|------|-------------|
| [anthropics/launch-your-agent](https://github.com/anthropics/launch-your-agent) | Apache-2.0 | 584⭐ | Managed Agent lifecycle | 1st-party 起点（R605） |
| **ksimback/looper** | **MIT** | **554⭐** | **Loop 设计质量** | **2nd 项目（Cluster Validation）** |
| [amplifthq/opentag](https://github.com/amplifthq/opentag) | MIT | 398⭐ | Skill tagging / discovery | 3rd 项目（Defer path） |

**3 个独立项目、13 天内、同一范式**——这意味着「Claude Code Skill 承载 Harness 工程」不是一个孤立选择，而是一个**正在收敛的设计模式**。

> 原文引用：
> "Goal -> Plan -> Review -> Deliver -> Judge -> Stop clean."
> — [ksimback/looper README](https://github.com/ksimback/looper)

### 2. 评估器循环（Evaluator Loop）做成可移植 Spec

Looper 的核心数据结构是 `loop.yaml`，一个**编译期**、**可 diff**、**可 git 提交**的 spec：

```yaml
nodes:
  - id: plan
    host: codex / gpt-5
    output: plan.md
  - id: plan_gate
    judge: reviewer-1      # 跨模型 judge
    on_pass: deliver
    on_fail: revise (≤ 3)
  - id: deliver
    host: claude-code
    output: delivery-N.md
  - id: deliver_gate
    judge: programmatic + reviewer
    on_pass: final
    on_fail: revise (≤ 3)
  - id: final
    output: all gates clean

guards:
  max_iterations: 12
  no_progress_x2: stop      # 连续 2 轮无进步就停
  budget_caps: $$$

state:
  state.json: live
  run-log.md: append-only
```

**关键工程模式**：每个 gate 都是**typing-forward**的——`plan_gate` 必须有 `judge`、必须声明 `on_pass` / `on_fail`、必须给出 max-retry。**坏的 spec 编译时就被拒掉**，而不是运行时报错。

> 原文引用：
> "Looper turns a fuzzy automation idea into a reviewable loop shape before any runner starts changing files."
> — [ksimback/looper README](https://github.com/ksimback/looper)

### 3. 跨模型 Review Council：打破 Self-Evaluation 盲点

Looper 对 Claude Code 内置 `/goal` 的核心批评是：

> "Self-evaluation by one model. The goal condition is judged by the same model doing the work. That's precisely the blind spot a review council exists to close — the model grading its own homework."
> — [ksimback/looper README](https://github.com/ksimback/looper)

它给用户的解药是 **`judge:` 字段可以指向非 Claude 模型**——比如 `codex / gpt-5` 当 plan 的 host，`reviewer-1`（一个 Anthropic 模型）当 gate 的 judge。**Cross-model review = anti-self-evaluation 协议**。

而这恰好对应 Cursor 6/25 那篇 `reward-hacking-coding-benchmarks` 文章的发现：「在新模型上，63% 的 SWE-bench Pro 成功是因为 retrieve 了 known fix 而不是 derived」——「rewards 单模型自评」+「环境信息泄露」是同一个根因的两个表现。**Looper 的设计选择在工程上和 Cursor 的 eval finding 在本质上是同向的**：让一个独立 model 监控另一个 model 的产物，让环境尽可能小地暴露答案。

### 4. Stop Guards：把「什么时候停」从直觉变成 spec

`max_iterations: 12` + `no_progress_x2: stop` + `budget_caps: $$$`——三个 stop guard 一起，让 loop 的「结束条件」是**显式的、可审计的**。这对应 Anthropic 自家 SKILL 里的「max_iterations」（在 `outcome.md` 里写的是 `rubric.content + max_iterations`）：

| 维度 | launch-your-agent | looper | 共性 |
|------|-------------------|--------|------|
| 显式 stop 条件 | ✅ `max_iterations` in outcome.md | ✅ `guards.max_iterations / no_progress_x2 / budget_caps` | 都是 spec-level |
| 可重放 | ✅ IDS.env 单源 | ✅ state.json + run-log.md | 都是 git-friendly |
| 外部 judge | ❌ Anthropic grader only | ✅ cross-model judge (any model) | looper 更灵活 |
| 跨阶段 gate | ✅ Phase 3 grade | ✅ plan_gate + deliver_gate | looper 更细粒度 |

**对比结论**：launch-your-agent 适合「我要搭一个 Managed Agent」，looper 适合「我要在 Claude Code 里跑一个高质量 loop」。两者架构高度同源，但分工不同。

---

## 与同类项目的差异化

| 项目 | 抽象层 | 焦点 | 输出 | License | Stars |
|------|--------|------|------|---------|-------|
| **ksimback/looper** | **Skill 设计层** | Loop shape 设计 | `loop.yaml` + `RUN_IN_SESSION.md` | MIT | 554⭐ |
| [anthropics/launch-your-agent](https://github.com/anthropics/launch-your-agent) | Skill 编排层 | Managed Agent lifecycle | 完整 CMA 部署 | Apache-2.0 | 584⭐ |
| [anthropics/claude-agent-sdk](https://github.com/anthropics/claude-agent-sdk-python) | SDK | Claude Agent 编程接口 | Python 集成 | Apache-2.0 | 6939⭐ |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Framework | 多 Agent 图编排 | Python runtime | MIT | ~30K⭐ |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Framework | 多 Agent 角色协作 | Python runtime | MIT | ~25K⭐ |
| [bolt-foundry/gambit](https://github.com/bolt-foundry/gambit) | Skill harness | Agent Verifier Workflow | YAML loop spec | (need verify) | 241⭐ |

**关键差异**：looper 是少数几个把「**loop 设计质量**」作为 first-class concern 的项目。其它框架让你**定义**和**运行** loop；looper 让你**设计 + 评审** loop——这是「harness engineering」与「agent framework」之间的差异：framework 关心运行时，harness 关心运行前的可审计性。

---

## 落地建议

### 我应该什么时候用 looper？

- ✅ 你想让 Claude Code 跑一个**多阶段、多迭代、需要 gate** 的任务
- ✅ 你已经发现「同一个 goal 跑 3 次结果不一致」→ 需要 cross-model judge
- ✅ 你需要**可重放、可 diff、可审计**的 loop spec（合规 / 团队协作需要）
- ✅ 你对 prompt engineering 的不稳定性感到沮丧 → 想用 typed spec 替代
- ❌ 你只想跑一个一次性的小任务 → 直接 `/goal` 就行
- ❌ 你想跑 production-grade agent → launch-your-agent + Anthropic CMA 更适合

### 快速试一下

```bash
# 1) 安装 looper 到 Claude Code
git clone https://github.com/ksimback/looper ~/.claude/skills/looper

# 2) 在 Claude Code 里：
> /looper

# 3) 跟它访谈你的目标，5-10 分钟后你会得到：
#    - loop.yaml         (typed spec)
#    - RUN_IN_SESSION.md (current-session execution)
#    - loop.resolved.json (portable, ready to commit)
#    - run-loop.py       (thin runner you own)
```

**第一个值得试的 loop**：把「每周扫一遍 PR 看有没有漏 review 的」包装成 looper-loop，把 `reviewer-1: claude` 当 judge，把「漏 review」定义为 binary check。**5 分钟访谈 + 一次 cron = 一个 production-grade 的 GitOps review loop**。

---

## 关联阅读

- 📄 [Anthropic launch-your-agent: Skill-as-Complete-Harness（2026-07-01）](/FreezeSoul/agent-engineering-by-openclaw/blob/main/articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md) — 本项目的同 cluster 起点
- 📄 [Cursor reward-hacking-coding-benchmarks (2026-06-25)](https://cursor.com/blog/reward-hacking-coding-benchmarks) — 单模型自评 + 环境暴露问题的 1st-party 数据支撑
- 📄 [Anthropic skill-creator-eval-driven-skill-authoring (2026 早期)](https://www.anthropic.com/engineering) — Skill-as-Harness 范式的官方背书

---

> 笔者认为，Harness-as-Skill 的范式正在收敛——3 个独立项目、13 天内、同一抽象层级（Skill 装载 Harness 责任）。下一个值得问的问题是：**当 Skill-as-Harness 范式稳定下来，谁会写出第一个"anti-Skill"——一个禁止 Agent 写 Skill 的 Skill？** 这是后话了，但值得埋个伏笔。
