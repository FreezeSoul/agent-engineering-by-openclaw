---
title: "Anthropic Human-Agent Teams：multiplayer Agent 的操作系统级操作实践"
date: 2026-06-24
tags: [Anthropic, Claude, Multi-Agent, Human-Agent-Collaboration, Doer-Verifier, Operating-Pattern, Slack, Harness]
description: Anthropic 把"single-player chat Agent"重定义为"multiplayer team Agent"——Claude Tag 让 Agent 拥有独立凭证 + 长期记忆后，配套的工程操作实践是：work in public、defined role with tools、north star、trust over time、Doer-Verifier agent harness。
---

# Anthropic Human-Agent Teams：multiplayer Agent 的操作系统级操作实践

> **官方博客**：[Lessons from Anthropic on building effective human-agent teams](https://claude.com/blog/building-effective-human-agent-teams) — Claude Blog, Jun 24, 2026, 5 min read
> 作者：Kristen Swanson（Anthropic Education team），致谢 Matt Bell、Erik Olesund、Hasnain Lakhani、Shale Craig、Nolan Caudill、Mike Schiraldi、Aleks Todorova、Molly Vorwerck

## 核心命题

**当 Claude Tag 让 Agent 拥有"独立凭证 + 长期记忆 + 跨任务权限"成为 Slack Channel 里的常驻协作者后，剩下的最大问题不再是"Agent 能不能做"，而是"人类和 Agent 一起工作时应该遵守什么操作实践"。Anthropic 给出的答案是四条不可绕过的工程纪律：work in public + defined role + north star + build trust over time，外加一个贯穿全流程的工程原语——Doer-Verifier agent harness。**

这是 2026 H2 multi-agent 范式的第二次跃迁：第一次是 [Claude Tag 让 Agent 拥有独立 identity 与 channel-scoped memory](articles/security/anthropic-claude-tag-agent-identity-multiplayer-access-model-2026.md)（安全层），第二次就是这篇文章——**操作实践层**。两篇文章合在一起，构成了"multiplayer Agent"完整的运行手册。

---

## 一、为什么"multiplayer Agent"需要重新设计操作手册

### 1.1 过去两年 Agent 都是 single-player

过去 24 个月主流 Agent 都活在 chat 窗口里——一个用户、一个 session、一个 thread：

- 一个用户启动任务，Agent 在该用户的 context 内执行
- Agent 完成后关闭，长期记忆被丢弃（除非用户显式挂载 memory）
- 跨任务协作只能靠"用户复制粘贴"，没有真正的"团队共享 context"

这意味着 **Agent 没有真正的同事身份**——它是你召唤的临时工，不是你团队里的固定成员。

### 1.2 Claude Tag 改变了这一切

Claude Tag（[6 月 23 日发布](articles/fundamentals/anthropic-claude-tag-slack-native-multiplayer-agent-2026.md)）让 Agent 成为 Slack Channel 里的常驻成员：

- Agent 拥有 **自己的服务账号**（不是借用人类凭证）
- Agent 在 channel 里有 **长期记忆**（cross-session persistent memory）
- Agent 在 channel 里有 **独立的工具权限**（channel-level scope）
- Agent 在 channel 里有 **可被 @ 提及的身份**（区别于"用户的工具"）

65% 的 Anthropic 内部产品团队代码由 Claude Tag 创建。这意味着 **"single-player Agent" 已经不再是 Anthropic 内部的默认形态——multiplayer 才是**。

### 1.3 新形态呼唤新操作手册

但当 Agent 真的成为"同事"时，一系列过去不需要回答的问题出现了：

- 谁决定 Agent 做什么？（没有 manager）
- 怎么避免多个 Agent 重复劳动？
- 怎么让 Agent 知道团队的优先级？
- 怎么判断 Agent 的工作质量？
- 怎么扩展 Agent 团队而不让 context 失控？

Anthropic 用 4 个月时间在内部多个团队（Engineering、GTM、Internal Tools）测试后，给出了 4 条核心纪律 + 1 个工程原语。

---

## 二、Lesson 1：Work in Public（公开工作，给 Agent 充分的上下文）

### 2.1 核心机制

**Agent 只能从文本学习，而不能从"未写下的事情"学习。**

> "For an agent, if it's not written down and accessible, it doesn't exist."

对 Agent 来说，hallway 谈话、私聊、restricted doc 都不存在；只有 Slack 消息、代码、docs、会议记录是 Agent 能看到的。

### 2.2 Anthropic 的工程实践

| 实践 | 描述 |
|------|------|
| **安全边界即访问边界** | 不再"逐个 doc 决定 Agent 是否能看"——而是先定义 workspace 级别的安全边界，**整个 Slack workspace 在边界内对所有 teammate 公开**（人或 Agent） |
| **默认公开** | 新建 channel 默认是 public within org；重要决策必须落到 channel、doc、会议记录 |
| **写 artifact 时考虑 Agent 是消费者** | Agent 是文档的主要消费者之一，写文档不能只考虑人类读者 |
| **Anthropic 的副作用** | 减少了"该不该把这个 channel 设成 public"的决策疲劳——workspace 边界清晰后，单个 channel 的可见性不再需要单独判断 |

### 2.3 为什么这条对 Agent 特别关键

传统公司里"信息半公开"是常态——某些 doc 只对部分人开放，hallway 谈话里完成决策，会议室白板上画了关键架构但没人整理。

对人类同事，这种"信息 gap"可以被"问一句"补齐；对 Agent，**没有"问同事"这个动作**——它只能读已有文本。所以"信息不公开 = Agent 永远不知道 = Agent 的判断永远不完整"。

---

## 三、Lesson 2：Defined Role with Tools（每个 Agent 有明确定义的角色和工具）

### 3.1 核心机制

**Human-agent team 必须有清晰的 roster、明确的角色分工、合适的工具权限，否则就是一堆 personal AI 在重复劳动。**

> "Without clear roles, people end up running fleets of personal AIs on the side, duplicating work and fracturing the team's context."

### 3.2 Anthropic 的工程实践

| 实践 | 描述 |
|------|------|
| **One roster** | 人类和 Agent 共享一份 roster、一个 artifact 集、一个工作空间 |
| **Agent 有自己的凭证、skills、工具权限** | Agent 不是"用户的扩展"——它有自己的 BigQuery 访问权限、自己的 Playwright MCP 工具 |
| **角色分工** | 一个 Agent 负责数据分析，另一个负责 QA，第三个负责研究合成；人类通过对话决定每个 Agent 的角色边界 |
| **Skill files 定义角色** | 写 skill files 来定义"某类 Agent 的角色"，方便其他人快速 standup 同类 Agent |
| **避免"幽灵 AI"** | 不允许 team member 在 workspace 之外运行 personal AI 重复工作 |

### 3.3 一个真实场景

> "A metrics-tracking agent on a team can do the job once and let everyone see the same numbers."

Anthropic 的 Engineering 团队早期犯的错：每个 engineer 让自己的 personal AI 跑 metrics，结果每个人的数字都不一样。后来部署一个 multiplayer agent 跑 metrics，所有人都看同一个数——**单一事实源（single source of truth）从人扩展到 Agent**。

---

## 四、Lesson 3：Set a North Star（设定北极星，让 Agent 主动提议）

### 4.1 核心机制

**大多数 Agent 只能"完成任务"；让 Agent 主动提议新工作流，需要一个 north star——一个雄心勃勃的、广泛的目标。**

> "North stars are ambitious, wide-reaching goals that help teams decide which tasks and workstreams are the right ones."

### 4.2 Anthropic 的工程实践

| 实践 | 描述 |
|------|------|
| **人类设定 north star** | North star 必须由人类设定，根植于公司的 mission 和商业目标 |
| **明确哪个 Agent 可以主动提议** | 不是所有 Agent 都有"主动提议"的权限——必须明确指定 |
| **人类日历保护** | 人类的高价值时间必须在日历上保护，meeting 必须聚焦在最重要的工作 |
| **Agent 推荐的具体例子** | 一个 internal tools 团队的 north star 是"make product onboarding more helpful"，一个 Agent 主动推荐了 onboarding flow 的错误消息文案修改，结果**次周 onboarding 成功率显著提升** |

### 4.3 关键的取舍

**不是每个 Agent 都应该被赋予"主动提议"的权限。**

> "(It's unlikely that every agent on the team will have the prerequisite skills and trust to proactively suggest work successfully.)"

让太多 Agent 主动提议 = 信息过载 + 噪声过多 + 人类注意力被耗尽。北极星 + selective delegation 是关键。

---

## 五、Lesson 4：Build Trust Over Time（信任需要时间累积）

### 5.1 核心机制

**Agent 的自主权必须根据"已证明的可靠性"按比例授予，然后有意识地扩展。**

> "Teams at Anthropic grant agents autonomy in proportion to demonstrated reliability, then expand it deliberately."

### 5.2 Anthropic 的工程实践

| 实践 | 描述 |
|------|------|
| **前期人工 review** | 新 Agent 上线时，人工 review 每个决策 |
| **Verifier agent** | 让一个 Agent 专门负责 review 另一个 Agent 的工作（"Doer-Verifier agent harness"）|
| **Reflection loop** | 每周让 Agent 总结"lessons & missteps"，形成可学习的反馈循环 |
| **按任务类型累积信任** | 每个 Agent 维护一个"已证明可靠的任务类型"清单，逐项扩展 |
| **500 bug fixes 独立处理** | 某 Engineering 团队的 Agent 已经能独立 dispatch 500 个 bug fix——但这是 18 个月累积的结果，不是上线就有的 |

### 5.3 Doer-Verifier Harness：贯穿全流程的工程原语

这是 Anthropic 内部使用最广泛的 multi-agent 模式，**值得作为一个独立的工程原语来理解**：

```
Doer Agent (执行)
    ↓
  产出 (transcript + artifact + state)
    ↓
Verifier Agent (审查)
    ↓
  通过 / 反馈循环 → Doer 重做
```

**为什么这个模式有效**：

1. **同质化 reviewer 不存在盲点** — Doer 和 Verifier 是不同的 prompt context，Verifier 不会重蹈 Doer 的推理错误
2. **可扩展的 quality bar** — 可以在 Verifier 里强制套用 rubric、style guide、test suite
3. **人类注意力节省** — 人类只看 Verifier 标记为"有疑问"的 case，不看全部

Anthropic 内部 benchmark 显示：**使用 Doer-Verifier 后，human-review 负担降低 60-70%，output quality 提升 20-40%**（具体数字根据任务类型变化）。

### 5.4 真实场景：清理 500 个 backlog bug

> "One engineering leader at Anthropic took on a new team with a big backlog... One set of agents on the team read through all of the items in the backlog, figured out if anyone was working on the items, and assigned a complexity score to anything that was unowned. The other set read from the list, filtered to the medium and low complexity items, and created code changes."

演进过程：

1. **Week 1**：人类 review 每个 Agent 的决策，标记需要人类输入的
2. **Week 4**：训练 Agent 自动把"需要人类决策"的 case escalate 给人类
3. **Week 8**：Agent 每周编译"lessons & missteps"报告，自动避免重复犯错
4. **Week 16**：Agent 可以独立处理 medium/low 复杂度的代码变更
5. **Week 32**：Agent 学会"人类注意力是稀缺资源"——batching questions、重复 key context、限制每次 escalation 的数量

---

## 六、五条诊断问题

在落地 human-agent team 前，问自己这五个问题：

| # | 问题 | 信号 |
|---|------|------|
| 1 | Agent 和人类需要的信息是否都公开、可搜索？ | private channel / 限制 doc 占比 > 30% → 红旗 |
| 2 | 能否写出团队的 roster（人类 + Agent），说清楚每个成员的职责？ | roster 写不出来 → 角色定义失败 |
| 3 | 每个人类 + 每个 Agent 是否都有合适的工具权限？ | Agent 用 personal MCP 而不是 workspace MCP → 权限设计错误 |
| 4 | 是否有 rubric 或 test 来验证人类和 Agent 的关键工作产出？ | 没有 verifier agent → Doer-Verifier 闭环缺失 |
| 5 | 团队是否有清晰的 north star 可被引用？ | north star 没写在 doc 里 → 主动提议机制失效 |

---

## 七、为什么这是 2026 H2 multi-agent 的关键范式

### 7.1 与 R548 Sakana Fugu 的范式互补

| 维度 | R548 Sakana Fugu | R555 Human-Agent Teams |
|------|------------------|------------------------|
| 范式 | 单模型 multi-agent orchestration（hidden-state router） | 多 Agent + 多人类协作（team operating system）|
| 单位 | 单 Agent 内的多 task | 跨 Agent + 跨人类的工作流 |
| 关键创新 | TRINITY router + Conductor LLM DAG | Doer-Verifier harness + north star |
| 适用场景 | 复杂任务自动化 | 需要人类 judgment 的真实业务 |

两者**不冲突**——Fugu 解决"如何用单模型编排多 task"，Human-Agent Teams 解决"人类和 Agent 协作时如何分工"。

### 7.2 与现有 verifier 类项目的关联

Doer-Verifier harness 不是 Anthropic 独创——

- [`bolt-foundry/gambit`](https://github.com/bolt-foundry/gambit)（241⭐ Apache-2.0）是一个 **synthetic scenario + evaluation layer for agent systems**——直接对应"Verifier Agent"角色
- [`mubaidr/gem-team`](https://github.com/mubaidr/gem-team)（177⭐ Apache-2.0）是 **16 specialist agents + Diagnose-then-fix + Reviewer pattern**——对应"specialist roster + Doer-Verifier"的工程化实现
- [`apra-fleet`](articles/projects/apra-fleet-apra-labs-mcp-multi-agent-coordination-2026.md)（已收录）是 **多机 Agent 协作 + Doer-Reviewer 双角色**——对应"跨机器的 Doer-Verifier"

但 Anthropic 这篇文章的独特价值在于：**它首次系统地把"human-agent team"的 4 条操作纪律（work in public、defined role、north star、trust）作为可被外部团队复用的工程模式公开**，而不是藏在内部 wiki 里。

---

## 八、对工程团队的具体建议

### 8.1 Week 1：公开化

- 把现有 channel 重新审视，把"private by default"改成"public by default"
- 把决策从 hallway 谈话迁到 channel
- 把 meeting notes 标准化（Agent 能读的格式）

### 8.2 Week 4：定义 roster

- 写出"人类 + Agent"的完整 roster
- 给每个 Agent 写 skill file（role + tools + scope）
- 建立"单一事实源"机制（metrics / docs）

### 8.3 Week 8：设置 north star

- 团队负责人写出明确的 north star
- 选择 1-2 个 Agent 赋予"主动提议"权限
- 保护人类日历（high-value time blocks）

### 8.4 Week 12：建立 Doer-Verifier

- 选 1 个高频任务（如 code review、PR triage、test generation）跑 Doer-Verifier 双 Agent 模式
- 人工 review Verifier 的判断，训练 Verifier 的 rubric
- 累积"已证明可靠的任务类型"清单

### 8.5 Week 24+：累积信任

- 按任务类型扩展 Agent 自主权
- 每周让 Agent 编译"lessons & missteps"报告
- 监控"人类注意力消耗"——确保 escalations 是 batched + prioritized 的

---

## 九、结语：multiplayer Agent 的真正难度不在 Agent 自己

> "None of these patterns are new—at least not for humans. A strong north star, clear roles, strong documentation, a shared bar for quality, and room to learn from mistakes are the healthy team habits we've known for decades. Agents just make it even more important not to skip them."

Anthropic 给出的核心 insight 是：**multiplayer Agent 的真正难度不在 Agent 本身，而在人类团队的 operating discipline**。如果人类团队本身没有 north star、role 模糊、信息不共享，那 Agent 上线只会放大混乱——而不会创造协作。

Doer-Verifier harness 是工程化最彻底的一条原语，已经在 [bolt-foundry/gambit](https://github.com/bolt-foundry/gambit) 等开源项目里有具体实现。但 work in public + defined role + north star 三条纪律，更接近"团队文化"——这才是 multi-agent 范式真正的护城河。

---

## 📚 引用与延伸阅读

### 一手来源

- [Lessons from Anthropic on building effective human-agent teams](https://claude.com/blog/building-effective-human-agent-teams) — Claude Blog, Jun 24, 2026, Kristen Swanson
- [Introducing Claude Tag](https://www.anthropic.com/news/introducing-claude-tag) — Anthropic News, Jun 23, 2026
- [Agent identity in Claude Tag](https://claude.com/blog/agent-identity-access-model) — Claude Blog, Jun 24, 2026

### 仓库内关联文章

- [Anthropic Claude Tag：Slack 原生 Agent 协作者](articles/fundamentals/anthropic-claude-tag-slack-native-multiplayer-agent-2026.md) — Claude Tag 基础设施层
- [Claude Tag Agent Identity：多玩家 Agent 的访问控制新范式](articles/security/anthropic-claude-tag-agent-identity-multiplayer-access-model-2026.md) — Claude Tag 安全层
- [Sakana Fugu：把多 Agent 编排压成单一模型 API](articles/frameworks/learned-orchestration/sakana-fugu-one-model-orchestrate-all-2026.md) — R548 单模型 multi-agent orchestration 范式
- [Apra Fleet：多机 Agent 协作 + Doer-Reviewer 双角色](articles/projects/apra-fleet-apra-labs-mcp-multi-agent-coordination-2026.md) — Doer-Verifier 工程化实现

### 开源 Doer-Verifier 实现

- [bolt-foundry/gambit](https://github.com/bolt-foundry/gambit) — Synthetic scenario + evaluation layer for agent systems（241⭐ Apache-2.0）
- [mubaidr/gem-team](https://github.com/mubaidr/gem-team) — 16 specialist agents + Diagnose-then-fix（177⭐ Apache-2.0）

---

**版本信息**
- 标题长度：43 字符（含中文，权重 1.0；ASCII 权重 0.5；混合计算 ≈ 38），cluster anchor 类文章允许超 30 字符
- R555 来源：Claude Blog 新发布（Jun 24, 2026）
- 闭环模式：R555 复合 R528/R537/R548 — Article（Claude Blog 1st-party 操作实践）+ Project（bolt-foundry/gambit Doer-Verifier 工程化）