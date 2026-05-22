# garrytan/gstack：YC CEO 开源的「一人工程团队」技能体系

> 源：https://github.com/garrytan/gstack | Stars: ~100K | MIT License

---

## 核心命题

gstack 的本质不是「一个 AI 工具」，而是 **YC CEO Garry Tan 用 20 年工程经验训练的虚拟工程团队**——23 个 specialized agents，通过 slash commands 协作，模拟了一个完整工程组织的职责分工。

笔者认为，这个项目的意义远超其技术实现——它代表了一种「AI Agent 架构」的新思路：**与其构建一个通用的 Agent，不如构建一组各司其职的 specialized agents，让它们在同一个 runtime 中协作**。

---

## GitHub 项目页

![GitHub](screenshots/garrytan-gstack-20260523.png)

---

## 一、项目背景：YC CEO 的个人生产力系统

Garry Tan 是 Y Combinator 的 CEO，曾是 Palantir 最早一批工程师，联合创办了 Posterous（被 Twitter 收购），还构建了 YC 内部社交网络 Bookface。

> "I've been building products for twenty years, and right now I'm shipping more products than I ever have. In the last 60 days: 3 production services, 40+ shipped features, part-time, while running YC full-time."

他用「logical code change」而非「raw LOC」来衡量生产力：

- 2026 年的运行效率是 2013 年的 **~810 倍**（11,417 vs 14 logical lines/day）
- 2026 年前四个月的产出已经超过整个 2013 年

> "The point isn't who typed it, it's what shipped."

这个数据本身就是对他整个生产力系统的最佳证明。

---

## 二、设计哲学：一个 Agent，还是一个团队？

传统上，我们倾向于给 Agent 一个「通用的、超能的」定位——一个能做所有事情的 AI 助手。但 Garry Tan 的设计思路完全不同：**他不是在做加法，而是在做分工**。

### 2.1 23 个 Specialized Agents

| Agent | 角色 | 核心能力 |
|-------|------|----------|
| `/office-hours` | YC Office Hours | 六个强制问题重新审视产品，在写代码前挑战假设 |
| `/plan-ceo-review` | CEO | 重新思考产品方向，生成替代方案 |
| `/plan-eng-review` | 工程负责人 | 锁定架构决策，预研技术风险 |
| `/design-review` | 设计评审 | 识别 AI 生成的设计「平庸感」 |
| `/review` | 代码评审 | 发现生产级 bug |
| `/qa` | QA Lead | 开真实浏览器测试，自动生成回归测试 |
| `/ship` | Release Engineer | sync main → run tests → audit coverage → push → open PR |
| `/security` | 安全官 | 运行 OWASP + STRIDE 审计 |
| `/browse` | 研究员 | 真实 Chromium 浏览器 + 反爬虫 stealth |

> "It turns Claude Code into a virtual engineering team — a CEO who rethinks the product, an eng manager who locks architecture, a designer who catches AI slop, a reviewer who finds production bugs, a QA lead who opens a real browser, a security officer who runs OWASP + STRIDE audits, and a release engineer who ships the PR."

### 2.2 为什么分工比通用更有效

笔者认为，Garry Tan 的洞察是对的：**通用 Agent 的问题是「什么都想做，但什么都做不精」**。

当一个 Agent 被赋予「CEO」的角色时，它的prompt会自动带上「挑战假设、重新思考方向」的思维模式。这不是加一个系统 prompt 那么简单——而是通过角色分工，让每个 Agent 形成了自己的「专业直觉」。

---

## 三、多 Agent 协作模式：slash commands 作为协议

gstack 的交互协议不是对话，而是 **slash commands**——每个命令对应一个 specialized agent：

```
/office-hours    → 战略层：重新审视产品方向
/plan-ceo-review → 产品层：评估功能优先级
/plan-eng-review → 技术层：架构风险评估
/design-review   → 设计层：发现平庸设计
/review          → 代码层：生产 bug 检测
/qa              → 测试层：真实浏览器 + 回归测试
/ship            → 交付层：git → tests → push → PR
```

这种设计的精妙之处在于：**它是显式的角色调用，而非隐式的 prompt 注入**。

当你输入 `/qa` 时，你不是在「给 Claude 一个 QA 的 system prompt」——你是在「召唤一个 QA 专家来接管当前会话」。

---

## 四、/office-hours：产品决策的「苏格拉底法」

最值得关注的技能是 `/office-hours`。这是 Garry Tan 从 YC 数千次 Office Hours 中提炼出的决策框架：

> "Start here. Six forcing questions that reframe your product before you write code. Pushes back on your framing, challenges premises, generates implementation alternatives."

「在写代码之前，重新审视产品」——这正是许多 AI Coding 项目忽视的东西。AI 能帮你写代码，但不能帮你判断「该不该写这段代码」。

笔者认为，`/office-hours` 的设计反映了一个重要的工程原则：**代码产出之前，需要有充分的问题定义**。大多数 AI Coding 的问题不是「代码写得不够快」，而是「方向就错了」。

---

## 五、跨 Agent 记忆与上下文

gstack 实现了 **team-aware retrospective**：

> "Team-aware retro global across all your projects and AI tools (Claude Code, browse..."

这意味着 `/retro` 能访问你在所有项目中的决策历史和执行记录——不是简单的对话历史，而是结构化的「团队记忆」。

---

## 六、与 Cursor Automations 的互补闭环

笔者认为，**gstack + Cursor Automations = Agent 工作流的两个维度**：

| 维度 | gstack | Cursor Automations |
|------|--------|---------------------|
| **触发方式** | 人工主动调用 slash commands | 事件驱动（GitHub/Slack/Webhook） |
| **Agent 定位** | 虚拟工程团队（多角色分工） | 值守员工（7×24 自动响应） |
| **协作模式** | 人驱动 Agent（人选择调用哪个 specialist） | Agent 自主响应事件 |
| **时间维度** | 同步（人随时介入） | 异步（无人看管时也能执行） |

**两者互补**：当你坐在电脑前时，gstack 的 slash commands 让你拥有整个工程团队的能力；当你离开时，Cursor Automations 让 Agent 继续监控和处理事件。

---

## 七、技术实现：不是框架，是配置

> "Twenty-three specialists and eight power tools, all slash commands, all Markdown, all free, MIT license."

gstack 的技术实现非常简洁——不是一个新的框架，而是对现有 Agent（Claude Code、Codex、Gemini CLI 等）的 **skill 配置**。

安装只需要三步：
```bash
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup
```

然后在 CLAUDE.md 中配置 gstack section。

> "gstack works on 10 AI coding agents, not just Claude. Setup auto-detects which agents you have installed."

这种设计哲学的优势：**不需要学习新的 API，不需要迁移现有工作流，只需要把 gstack 的 skills 配置注入到你已有的 Agent 中**。

---

## 八、局限性

1. **主要面向 Claude Code**：虽然说支持 10 种 agent，但核心设计是针对 Claude Code 的 slash commands 体系
2. **个人最佳实践**：这是 Garry Tan 个人的工程方法论，不一定适合所有团队
3. **没有自动化触发**：gstack 依赖人工调用，不具备 Cursor Automations 的事件驱动能力

---

## 结论

gstack 是目前最高质量的「AI Coding Agent 技能体系」开源项目之一。Y Combinator CEO 的背书 + 100K Stars 的社区认可 + 23 个 specialized agents 的完整设计，使它成为 AI Coding 领域不可忽视的项目。

笔者认为，gstack 的核心价值在于：**它证明了「分工优于通用」的 Agent 设计哲学是正确的**。当你有一个能扮演 CEO、Eng Manager、QA Lead 的 Agent 系统时，产出的质量远高于一个「通用的 AI 助手」。

对于想构建自己的 Agent 技能体系的工程师，gstack 是一个值得深入研究的案例——它展示的不是「怎么做 AI」，而是「怎么让 AI 像一个团队一样工作」。

---

## 引用

1. garrytan/gstack README: https://github.com/garrytan/gstack
2. Reddit 讨论: https://www.reddit.com/r/ClaudeAI/comments/1s7jdof/garry_tan_opensourced_gstack_his_personal_skill/