# NousResearch/hermes-agent：唯一内置学习循环的自学习 Agent

> 不是 coding copilot，不是 chatbot wrapper。是一个运行在服务器上的自主 Agent，能记住自己学到的东西，随着运行时间变长而变得更强。173K Stars，15 P0 + 65 P1 bug 修复，321 位贡献者——这不是一个实验项目，而是一个工程级别的自学习系统。

## 核心命题

**大多数 Agent 系统是「无状态的」——每次运行都是一次新开始，不记得上次怎么解决的。hermes-agent 破除了这个限制，它内置学习循环，能从经验中生成 skills，并在下次自动复用。**

这个设计从根本上改变了 Agent 的使用模式：从「每次都需要人工介入的 copilot」，变成「能独立完成工作并积累经验的 autonomous colleague」。

## 二、关键工程特性

### 2.1 自学习循环（Built-in Learning Loop）

hermes-agent 是目前唯一声称拥有「内置学习循环」的 Agent 系统。它的学习机制不是微调模型，而是：

- **Skill 生成**：从经验中自动生成 SKILL.md，而不是每次都依赖预定义的 skill
- **持久化记忆**：session_search 无需 LLM，4,500× 更快且免费（从 ~$0.30/call 降到 0 cost）
- **上下文积累**：每个 session 的工作成果被转化为下一个 session 的起点

这个机制的意义在于：**它让 Agent 的能力增长脱离了人工维护的瓶颈**。当一个新用户遇到一个场景时，Agent 会生成 skill；当下一次同样的场景出现时，skill 被自动复用。团队中一个人的经验可以无损地扩展到所有人。

### 2.2 Skill Bundles：组合式工作流

Skill bundles 是 hermes-agent v0.15 引入的新特性——用一个 slash 命令加载一组 skills：

```
/writing-day
→ activates: humanizer + ideation + obsidian + youtube-content
```

对比传统模式：用户需要记住 4 个不同的 skill 名称，逐一激活。

Bundle 的价值在于 **工作流层面的抽象**。当你知道「今天我要写内容」，你不需要思考「我需要哪几个工具」，你只需要说「我要写内容」，系统知道该激活哪组工具组合。这与 OpenAI eval-skills 文章中「让失败驱动 coverage」的思路不同——bundles 是「让成功经验驱动 workflow」的机制。

### 2.3 Promptware 防御（Brainworm-Class Attacks）

v0.15 带来了 Promptware 防御能力，专门对抗「Brainworm 级别的攻击」。这类攻击通过在 agent 的上下文中植入恶意指令，使其执行非预期的行为。

防御的核心是 **execution guidance**——在模型层的 probabilistic defense 之外，加入确定性的边界控制。这与 Anthropic「Design for containment at the environment layer first」的原则形成呼应：环境层的确定性边界是 probabilistic model layer 的最后防线。

### 2.4 多 Agent 编排（Kanban + Swarm）

v0.15 的一个重大工程突破是 **Kanban 成长为完整的多 Agent 平台**，在 104 个 PR 中实现：

- **Orchestrator-driven auto-decomposition**：triage 任务时自动分解为子树
- **Swarm topology**：一行命令 `hermes kanban swarm` 创建完整 Swarm v1 图（root + parallel workers + gated verifier + gated synthesizer + shared blackboard）
- **Per-task model overrides**：便宜模型处理 boilerplate，贵模型处理 hard sub-tasks
- **Worktree-per-task**：每个子任务有独立的 git worktree 和分支

这种「专业分工 + 动态调度」的多 Agent 架构与 TradingAgents 的辩论机制（fundamental/sentiment/technical analyst → trader → risk）处于同一层级，但 hermes-agent 更侧重「如何在长程任务中保持上下文不丢失」。

### 2.5 Bitwarden Secrets Manager：简化凭证管理

v0.15 引入 Bitwarden Secrets Manager，用一个 bootstrap token 替代 N 个 per-provider API keys。

这个改进的价值：**降低了多模型/多 provider 环境的配置复杂度**。当你需要同时调用 OpenAI、Anthropic、xAI 和 Grok 时，N 个 API keys 的管理本身就是一种认知负担。Bitwarden 集中管理把这个负担降到一个 token。

## 三、与 Article 的关联

本文与「系统性测试 Agent Skills：OpenAI 的 Eval 工程方法论」形成以下互补：

| 维度 | OpenAI eval-skills | hermes-agent |
|------|-------------------|--------------|
| **Skill 测试** | 如何验证 skill 行为是否符合预期 | 如何从经验中生成新 skill |
| **质量保障** | 确定性检查 + rubric grading | Promptware defense + 安全边界 |
| **能力积累** | 通过 eval 循环驱动改进 | 通过自学习循环自动积累 |
| **触发机制** | name/description 决定触发可靠性 | skill bundles 提供工作流级触发 |

两者共同指向一个更大的图景：**Agent Skills 的工程化**不只是「如何写 skill 指令」，还包括「如何测试 skill」和「如何让 skill 自己进化」。

## 四、快速上手

```bash
# 一键安装
pip install hermes-agent

# 启动（自动检测可用模型）
hermes chat

# 创建第一个 skill bundle
# 编辑 ~/.hermes/skill-bundles/writing-day.yaml
# 写入：
#   skills:
#     - humanizer
#     - ideation
#     - obsidian
#     - youtube-content

# 用 bundle 激活
/hermes load writing-day
```

完整的多 backend 支持（local / Docker / SSH / Singularity / Modal）和 23 个消息平台集成（Telegram、Discord、Slack、WhatsApp、Signal、Email 等）。

---

**引用来源**：
- GitHub README: "The self-improving AI agent built by Nous Research" (https://github.com/nousresearch/hermes-agent)
- Release v0.15.0 "The Velocity Release" (2026-05-28): 1,302 commits, 747 merged PRs, 560+ issues closed
- hermes-agent官网: https://hermes-agent.nousresearch.com/

**Stars**: 173,000+ | **License**: MIT | **Language**: Python | **贡献者**: 321 (含 co-authors)