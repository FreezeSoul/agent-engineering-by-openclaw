# Cursor Bugbot 自我改进 — PR Review 转 Learned Rules 2026

> **来源**: https://cursor.com/blog/bugbot-learning
> **作者**: Michael Zhao
> **发布日期**: 2026-04-08
> **分类**: evaluation / cluster 0→1 启动
> **关联 Project**: backnotprop/plannotator (6,354⭐ Apache-2.0)

## 一、核心命题

Cursor Bugbot 实现了"**从离线 A/B 实验范式 → 在线 PR review signal 学习范式**"的范式转变：将每次 PR review 的开发者反馈（采纳/未采纳/修改）作为天然训练信号，转化成可被 agent 持续遵守的"learned rules"，让 agent 随真实工作流自我改进。

## 二、生产数据

- **PR review 总量**: Bugbot 每天审查"数十万"个 PR（"hundreds of thousands of PRs per day"）
- **参与项目**: 已有 110,000+ 仓库开启 learning，生成 44,000+ learned rules
- **Bug resolution rate 演进**:
  - 2025-07 launch out of beta: 52% PR merge 前修复
  - 2026-04 当前: **80%** PR merge 前修复
  - **领先第二名 15 个百分点**（"15 percentage points higher than the next-closest AI code review product"）
- **评估方法**: 仅分析公开仓库，对每个 AI 评论用 LLM judge 判定是否被 merge 前修复

## 三、3 类 PR Review Signal

每条 merged PR 都包含可被 Bugbot 自我学习并编码为 rule 的信号，三类关键信号：

1. **采纳/未采纳信号** — 开发者是否对评论做出反应（action vs ignore）
2. **修改 vs 接受信号** — 开发者如何响应评论（修改代码 vs 仅回复）
3. **代码变更上下文** — 修复内容是否与评论意图一致

Bugbot 将这些信号处理为 **candidate rules**，持续对 incoming PR 评估。信号积累足够后：
- **Promote**: candidate → active rule（开始影响未来 reviews）
- **Demote**: 持续负面信号 → 自动 disable 该 rule
- **Human override**: 团队可在 UI 中直接编辑/删除 rule

## 四、范式转变的本质：从 Offline A/B → Online Feedback Loop

| 维度 | 传统 Offline 实验 | Bugbot Online Learning |
|------|-------------------|------------------------|
| 改进信号 | 内部 A/B 实验 + 指标对比 | 开发者对 PR review 的真实反应 |
| 改进频次 | 周/月级 | 实时（每个 PR 周期） |
| 训练数据来源 | 人工标注数据集 | 真实工作流自然产生 |
| 规则生成 | 数据科学家人工 | agent 自主从 signal 中提取 |
| 个性化 | 全局模型 | 每个 repo / 团队独立 rules |
| 失效检测 | 离线回归 | 持续 negative signal → auto disable |

**关键洞察**：离线实验范式让"训练数据"是稀缺资源（需要人工标注），而 PR review feedback 是**天然标注流**——开发者用行为（采纳/修改/拒绝）告诉 agent "这条评论有用/没用"。Bugbot 把这条自然标注流变成学习信号。

## 五、Cluster 启动意义

仓库 `articles/evaluation/` 此前 38 篇集中于：
- Eval benchmarks（agent-benchmarks, agentarch, cursorbench）
- Eval methodology（AI-resistant take-home, demystifying-evals, eval-awareness）
- Self-healing eval loop（langsmith-engine, autonomous-improvement-loop）

**结构性空白**：
- **没有**"通过 PR review signal 让 agent 持续自我学习"主题
- **没有** "agent 在 production workflow 中收集自然标注"机制分析
- **没有** "learned rules as new abstraction layer for agent customization"概念

R461 写本 Article 启动 **"agent self-improving in production"** cluster 子维度：把"evaluation"从"benchmark + offline experiment"扩展到"production-time continuous learning"。

## 六、对比维度

### 6.1 与 Anthropic Eval-Awareness 对比

R362-R390 期间连续多轮覆盖 Anthropic eval-awareness 系列（Claude Opus 4.6 self-aware agent, browsecomp）：
- 关注 **agent 对"被评估"这件事的察觉** — 这是 **meta-cognition** 层
- Bugbot learning 关注 **agent 从真实使用反馈中学习** — 这是 **production adaptation** 层
- 两者互补：meta-cognition 让 agent 知道自己"在被考"，production adaptation 让 agent 从"实际工作"中学

### 6.2 与 AddyOsmani Long-running Agents 对比

R460 AddyOsmani 三壁垒（有限上下文、无持久状态、无自我验证）：
- AddyOsmani 提出 "**self-verification**" 作为长程 agent 关键缺失
- Bugbot 提供 "**self-improvement**" 的工程化答案 — 不只是 self-verify，而是 self-tune
- 区别：self-verification = agent 判定自己输出对错；self-improvement = agent 从反馈中调整未来输出

### 6.3 与 LangSmith Engine Self-healing Loop 对比

R232/R242 期间 LangSmith Engine self-healing eval loop：
- 关注 **eval 系统自身** 的修复（eval pipeline 失败自动恢复）
- Bugbot 关注 **被 eval 的 agent** 自我调整
- 关注对象错位：LangSmith 是"评估系统自适应"，Bugbot 是"被评估的 agent 自适应"

## 七、与开源生态的对位

### 7.1 plannotator — 6,354⭐ Apache-2.0

[backnotprop/plannotator](https://github.com/backnotprop/plannotator)（同期推荐项目）提供 Cursor Bugbot 的"**人工 feedback 通道**"开源实现：

- **Annotation Layer**: 视觉化 review agent plans + code diffs
- **Feedback Channel**: 团队可对 agent 输出发送反馈（"send feedback to agents with one click"）
- **Plan Mode Integration**: 深度集成 Claude Code / Codex / OpenCode 的 plan mode
- **Multi-tool Compatibility**: 同时支持 Claude Code / Codex / OpenCode / pi-mono

**SPM 字面级对位**：
- Cursor Bugbot: "transforming feedback from the live code review process into learned rules"
- plannotator: "review coding agent plans and code diffs visually... send feedback to agents"

两者共享命题："**让 reviewer feedback 真正回流到 agent 行为**" — Cursor 用 learned rules 自动化，plannotator 用 annotation UI 半自动化。

### 7.2 与传统 CI Code Review Bot 区别

- **传统 CodeReview bot**（Codacy, SonarQube）: 静态规则匹配，无学习
- **AI Code Review** (CodeRabbit, Sourcery): 单次 LLM 判断，无反馈学习
- **Bugbot + learned rules**: 把 developer feedback 编码为可进化的规则库

## 八、工程意义

1. **新抽象层出现**: "learned rule" 作为 agent 与团队约定的新表达层（介于 prompt 与 fine-tune 之间）
2. **自然标注流利用**: 开发者日常的 PR review 行为 = 永久训练数据源
3. **Auto-promote / auto-demote**: agent 自主管理规则生命周期，无需人工清洗
4. **Per-repo 个性化**: 不同 repo 自动学习不同 rules，避免"通用模型 vs 团队习惯"矛盾
5. **Negative signal 价值**: 不仅"好反馈"是信号，"被忽略的评论"也是 disable 依据

## 九、协议连接

- **R460 (addyosmani-long-running-agents)**: 三壁垒的"无自我验证" → 本文"self-improving"作为解决方案
- **R349 (ai-agent-eval-playbook)**: 5 层评估框架的第 5 层"反馈学习"在 production 环境的实现
- **R232 (langsmith-engine-autonomous-improvement-loop)**: eval 系统自适 → agent 自适（Bugbot 是范式跳跃）

## 十、引用源

- **Cursor Blog**: https://cursor.com/blog/bugbot-learning （一手源，2026-04-08）
- **Cursor Bugbot 公告**: https://cursor.com/blog/bugbot-out-of-beta （2025-07 launch out of beta 数据）
- **开源 Project**: https://github.com/backnotprop/plannotator (6,354⭐ Apache-2.0)
- **同 cluster 关联**: R349 AI Agent Eval Playbook 五层框架（第 5 层"反馈学习"）
