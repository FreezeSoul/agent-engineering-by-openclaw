# ADHD: 并行发散思维框架——让 Agent 在收敛前先「想宽」

> **一句话评价**：这不是又一个 Prompt 技巧，而是对「自回归推理中过早收敛」这一结构性问题的架构级修复——通过隔离分支 + 生成器-评审器分离，让 Agent 在深度之前先真正「想宽」。

**项目信息**

| 属性 | 值 |
|------|-----|
| **GitHub** | [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd) |
| **Stars** | 471（2026-05-25 创建，23 Forks）|
| **语言** | TypeScript |
| **NPM** | [adhd-agent](https://www.npmjs.com/package/adhd-agent) |
| **论文** | [adhdstack.github.io](https://adhdstack.github.io/) |

---

## 一、核心命题：为什么 Agent 会「想偏」？

大多数 Agent 在第一次生成答案后就锚定在那个方向上——即使提示它「再想想」，它也会在已经形成的上下文上做微调，而不是真正从零重新思考。

官方称之为**过早收敛（Premature Convergence）**，并认为这是「自回归推理的架构问题，而不是 Prompt 问题」：

> **"Linear Chain-of-Thought anchors on whatever it says first. Tree-of-Thought widens the search but still walks a single shared context, so the anchoring persists across branches."**  
> — ADHD README

传统 CoT 在单一上下文中逐步推理，ToT 虽然探索多个分支但共享上下文导致锚定效应仍然存在。ADHD 的解决思路是：**在发散阶段强制完全隔离，让分支之间没有任何信息交流。**

---

## 二、工作机制：两阶段循环 + 硬隔离墙

ADHD 的工作流分为两个阶段，两者之间有严格的机械隔离（非 Prompt 承诺，而是通过系统配置强制）：

### Phase 1：Diverge（发散）

1. **选择 N 个认知框架（Cognitive Frames）**
2. **并行启动 N 个隔离的 Agent 调用**——每个调用只看到：问题 + 该框架的视角 Prompt + 禁止评估的系统 Prompt
3. 分支之间**互相不可见**，因此不存在锚定效应

### Phase 2：Focus（聚焦）

1. **独立的评审器调用**（Critic）逐项评分：新颖性（Novelty）/ 可行性（Viability）/ 匹配度（Fit）
2. 标记陷阱（Trap）并说明原因
3. 按底层角度聚类
4. **深挖 Top-K 的幸存者**，生成带风险和第一步的草图

关键设计：**生成器-评审器分离是机械性的**——两个独立的 LLM 调用，有相反的系统 Prompt，而不是在一个 Prompt 里同时要求「边想边评」。这避免了评审结果被生成阶段「污染」。

---

## 三、实验数据：5/6 战胜单射基线

根据 ADHD 提供的评测数据：

| 指标 | ADHD vs 单射基线 |
|------|-----------------|
| **胜率** | 5/6 |
| **新颖性提升** | +5.17 |
| **陷阱检测提升** | +7.67 |

> **"A method that makes coding agents think wide before deep — and the evaluation showing it. Wins 5/6 against single-shot baseline with +5.17 novelty, +7.67 trap detection."**  
> — ADHD Landing Page

评测方法论有公开文档支撑（11 个来源，8 轮验证），并在 GitHub 上以 Issue #16-18 形式追踪。

---

## 四、工程实践：30 秒安装，支持所有主流 Agent

安装只需要一行命令，自动检测当前使用的 Agent（Claude Code、Cursor、Antigravity、Codex、Cline、Gemini CLI、Windsurf 等 50+）：

```bash
npx skills add UditAkhourii/adhd
```

之后在需要发散性思考的场景下调用：

```
/adhd "give me a few ways to solve X"
```

适用场景（官方推荐）：
- **设计决策**：不满足于第一个方案
- **模糊 Debugging**：问题根源不够清晰
- **Naming / API Surface Design**：避免过早锚定在一个命名方向
- **战略规划**：需要真正多角度思考

> **"Reach for it on design decisions, fuzzy debugging, naming, API surface design, strategy, and any prompt of the shape 'give me a few ways to…'."**

---

## 五、采用情况：已有开源项目官方集成

| 集成项目 | 做了什么 |
|---------|---------|
| [repowire](https://github.com/prassanna-ravishankar/repowire) | 将 ADHD port 到 mesh-orchestrator 原语上：frames → frame-shifted temp peers，generator/critic split → separate peers vs. orchestrator。已在默认 orchestrator 模板中发货（[PR #313](https://github.com/prassanna-ravishankar/repowire/pull/313)，已 merge）|

> **"The first OSS project to officially ship ADHD"** — ADHD README

---

## 六、外部评价

- 🔌 **Repowire 官方集成**：已 merge 到默认模板
- 📰 **[The New Stack](https://thenewstack.io/claude-code-adhd/)** 专题报道
- 🔬 **独立研究验证**：han 项目发布了 11 来源、8 轮验证的[evidence-based research review](https://github.com/testdouble/han/blob/adhd-swarm-research/docs/research/adhd-application-to-han.md)
- 💬 **OpenClaw 社区反馈**：有 tester 评价 *"I read it, installed it on two different agents… I actually love it. This is great. I thought this was gonna be another useless post. But no, it wasn't."*

---

## 七、与现有知识体系的关联

ADHD 的核心机制——Generator/Critic 分离 + 隔离分支——与仓库中已有的多个主题形成深层共鸣：

| 关联主题 | 对应文章 | 关联说明 |
|---------|---------|---------|
| **Chain-of-Thought 演进** | fundamentals/ 相关文章 | ADHD 是 CoT → ToT 演进路径上的又一次范式跳跃：隔离分支是 ToT 的「架构修正版」|
| **Harness 工程（评估器循环）** | harness/ 目录下文章 | ADHD 的评审器本质上是一个独立的评估器：评分 → 标记陷阱 → 聚类 → 深挖，这是一个典型的「 evaluator loop」模式 |
| **多 Agent 协作** | orchestration/ 目录下文章 | ADHD 的 N 个分支可以理解为 N 个并行 Agent，只不过它们被强制隔离、没有互相通信——这是一种极端的「隔离协作」模式 |
| **Prompt Engineering** | practices/prompting/ | ADHD 在 README 中明确表示「这不是一个 Prompt 技巧，而是架构级修复」——这对 Prompt 工程社区是一个重要的认知挑战 |

---

## 八、笔者判断：为什么这值得推荐？

**优点**：
1. **问题定义锐利**：准确识别了「自回归推理中过早收敛」这个根本问题，而不是又一篇「如何使用 CoT」的水文
2. **机制设计有新意**：Generator/Critic 的机械分离 + 分支间硬隔离墙，这个设计在现有开源方案中不多见
3. **工程可用性高**：30 秒安装、自动检测 50+ Agent、无需修改工作流
4. **有真实采用**：Repowire 官方集成，不是自 High
5. **评测方法开放**：论文 + 公开评测 + GitHub Issue 追踪，可验证

**局限**：
- 当前 Stars 仅 471（2026-05-25 创建），属于早期项目，尚未经过大规模社区验证
- 主要在 Claude Code 生态上测试，其他 Agent 上的效果有待验证
- 对简单确定性问题（答案明确、无需探索的场景）可能过度工程

**适用判断**：如果你在构建需要「先想宽再想深」的 Agent 任务（比如架构设计、API 设计、复杂 Bug 根因分析），ADHD 值得一试。对于简单任务，保持现状即可。

---

*推荐理由：这不是又一个 Prompt 模板，而是对 LLM 推理过程中「过早收敛」这一结构性问题的一次有实验数据支撑的架构级回应。Generator/Critic 机械分离的设计尤其值得在 Harness 工程上下文中关注。*