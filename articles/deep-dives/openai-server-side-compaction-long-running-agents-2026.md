# Compaction vs Truncation：长程 Agent 的 Context 续命战

> 2026-06-14 | 来源：[OpenAI Developers Blog](https://developers.openai.com/blog/skills-shell-tips) | 标签：harness-engineering, context-management, long-running-agents

## 这篇文章要回答的问题

长程 Agent 运行数小时后，Context 窗口被「填满」——这时候工程系统面临一个根本选择：截断（Truncation）还是压缩（Compaction）？这两个选择决定了 Agent 是「失忆从头再来」还是「带着进度继续干」。OpenAI 在 2026 年给出了它的答案：Server-side Compaction，配合 Skills 和 Hosted Shell，构成一套完整的长程 Agent 工程框架。

笔者认为，理解 Compaction 与 Truncation 的本质差异，是理解 2026 年 Agent 工程走向的关键分水岭。

---

## 一、问题：Context 窗口是有限资源

当一个 Agent 持续运行数小时甚至数天时，每个 turn 都会向 Context 添加：

- **工具调用记录**：每次 `tool_use` 的输入输出
- **推理摘要**：Agent 的思考链（reasoning summaries）
- **中间结果**：文件内容、命令输出、数据库查询结果
- **对话历史**：用户的反馈、Agent 的自我修正

经过数十个 turn 之后，Context 窗口被这些「历史垃圾」填满，Agent 开始「忘记」早期的关键信息。这不是 Bug，是工程设计的必然结果。

> "Long-running tasks fill the context window, which is important for providing context across turns and across agents." — [OpenAI, "From model to agent"](https://openai.com/index/equip-responses-api-computer-environment/)

传统的解法是 **Truncation**（截断）：当 Context 快满时，直接丢掉最早的那部分内容。这相当于「失忆」——Agent 不再记得自己最初的目标是什么，已经完成了哪些步骤。

**Compaction（压缩）** 的思路完全不同：不是简单地丢掉历史，而是理解「哪些是已完成的工作，哪些是当前状态」，然后将历史压缩成有结构的摘要，同时保留 Agent 的「工作进度感」。

---

## 二、Compaction 的工程本质

### 2.1 Truncation 的问题

让我们看一个具体场景：

```
Turn 1: Agent 读取 user requirements.md (4000 tokens)
Turn 5: Agent 写了 5 个模块的代码 (8000 tokens)  
Turn 10: Agent 跑了测试，发现了 3 个 bug (6000 tokens)
Turn 15: Context 快满了，需要截断...
```

如果用 **Truncation**：
- 最早的内容（requirements.md）被丢弃
- Agent 不知道最初的需求是什么了
- 已完成的 5 个模块代码可能因为缺少上下文而在后续改坏

如果用 **Compaction**：
- Turn 1-5 的内容被压缩成：「已读取需求，已完成模块 A/B/C/D/E，测试发现 bug #1/#2/#3」
- Agent 依然知道起点和当前进度
- 可以带着这个「工作进度摘要」继续处理 bug #1

**笔者的判断**：Truncation 是一种「记忆剥夺」，会让 Agent 在长任务中重复劳动或者做出与原始目标不一致的决策。Compaction 才是真正面向「工作连续性」的设计。

### 2.2 Compaction 的技术实现

OpenAI 的 Server-side Compaction 不是简单的文本压缩。根据官方描述，它是一种「有理解能力的压缩」——压缩器知道：

1. **已完成的工作**（Completed Work）：被压缩成结构化的摘要，而非丢失
2. **当前状态**（Current State）：被保留，不参与压缩
3. **关键决策点**（Decision Points）：保留，使得 Agent 在需要回溯时有据可查

这意味着 Compaction 实际上是一种**有损的工作记忆压缩**，但损失的是「历史细节」而非「工作进度」。这与 R379 中提到的「working state handover」概念高度一致——都是关于如何在长程任务中保持工作连续性。

> "Unlike simple truncation, compaction allows agents to run for hours or even days." — [VentureBeat](https://venturebeat.com/orchestration/openai-upgrades-its-responses-api-to-support-agent-skills-and-a-complete)

---

## 三、Skills：可复用的任务定义

除了 Compaction，OpenAI 这次还引入了 **Skills** 作为 Agent 的任务定义机制。关键特性：

- **对齐 Agent Skills 开放标准**：这不是 OpenAI 私有的格式，而是行业开放标准
- **可版本化**：Skills 有版本号，可以在不破坏兼容性的前提下迭代
- **可挂载到容器**：Skills 被挂载到 Hosted Shell 容器中，使 Agent 能在受控环境中可靠执行

Skills 的价值在于：它把「Agent 能做什么」从隐性的 Prompt 工程变成了显性的、版本化的、可复用的技能模块。这对于构建「企业级 Agent」至关重要——你需要知道 Agent 的能力边界是什么，这个能力是否可以独立升级，是否可以多个 Agent 共享。

**笔者认为**：Skills 的出现是 2026 年 Agent 工程的重要拐点。它标志着 Agent 的能力定义从「写 Prompt」向「定义 Skill」迁移，就像面向对象编程中从「过程式代码」向「类/接口」迁移一样——提高了复用性，降低了出错的概率。

---

## 四、Hosted Shell：受控的执行环境

第三个组件是 **Hosted Shell**——OpenAI 托管的容器环境，Agent 在其中可以安装依赖、运行脚本，同时互联网访问受控。

这解决了一个根本问题：在没有受控执行环境的情况下，Agent 在真实环境中的行为是不可预测的。Hosted Shell 提供了：

1. **隔离性**：Agent 的操作不会影响宿主系统
2. **可复现性**：相同的 Skill 在相同的 Shell 环境中结果一致
3. **受控的网络访问**：可以访问必要的资源，但不能随意外泄数据

这与 R337 中讨论的「Anthropic 把 control plane 做成了平台原语」是同一工程哲学的不同实现——都是在 Agent 和真实环境之间插入一个「管理层」，让 Agent 的行为变得可预测、可控制。

---

## 五、三者合一：长程 Agent 的完整工程栈

把这三个组件放在一起，我们看到了一个清晰的长程 Agent 工程栈：

```
┌─────────────────────────────────────────────────────┐
│                   Skills Layer                      │
│  (对齐 Agent Skills 开放标准，可版本化/可复用)       │
├─────────────────────────────────────────────────────┤
│               Hosted Shell Layer                    │
│  (受控执行环境，隔离+可复现+网络控制)                 │
├─────────────────────────────────────────────────────┤
│              Compaction Engine                      │
│  (工作进度压缩，而非简单截断)                        │
├─────────────────────────────────────────────────────┤
│              Context Window                        │
│  (有限资源，通过 Compaction 动态管理)               │
└─────────────────────────────────────────────────────┘
```

**这个栈的分层逻辑与 R379 中 harness-books 的框架高度一致**：

| harness-books (R379) 章节 | OpenAI Responses API 层 |
|------------------------|------------------------|
| Ch.2 Prompt Is the Control Plane | Skills Layer |
| Ch.3 Permission & Sandbox | Hosted Shell |
| Ch.5 Context Governance | Compaction Engine |
| Working State Management | Server-side Compaction |

---

## 六、笔者判断：Compaction 才是 2026 年的关键工程机制

在这三个组件中，笔者认为 **Compaction 是最具工程突破性的**。原因：

1. **Skills 和 Hosted Shell 是条件，Compaction 是目的**：你可以没有 Skills（用普通 Prompt 替代），可以没有 Hosted Shell（用本地执行替代），但如果 Context 窗口满了，你必须做出 Truncation 还是 Compaction 的选择——这个选择直接决定 Agent 的行为连续性。

2. **Compaction 将「工作进度」变成了工程概念**：在 Compaction 之前，Agent 的工作进度是「隐性的」（存在于每次推理中），而 Compaction 把它变成了「显性的」（结构化的压缩摘要）。这使得 Agent 的工作可以被外部系统观察、干预、甚至跨 Agent 传递。

3. **这是行业稀缺的工程机制**：在 R371-R380 的 10 轮 Path C 扫描中，我们记录了大量 harness 相关的项目，但「有结构的 Context 压缩机制」在开源社区极少见到。OpenAI 的 Server-side Compaction 是目前公开资料中工程化程度最高的实现。

**笔者的结论**：如果你在 2026 年构建长程 Agent，你的设计必须回答这个问题：「我的 Compaction 策略是什么？」——不是「要不要压缩」，而是「压缩什么、保留什么、压缩成什么格式」。这个问题回答不清楚，你的 Agent 在运行数小时后一定会出问题。

---

## 七、结尾开放问题

Compaction 的压缩策略由谁决定？是 OpenAI 服务端自动决定，还是 Agent 可以参与配置？如果 Agent 可以配置压缩策略，那意味着 Agent 有了「元认知」能力——知道自己应该记住什么、忘记什么。这会是下一个 2026 Agent 工程的重要方向吗？

---

**引用来源**：
- [Shell + Skills + Compaction: Tips for long-running agents that do real work | OpenAI Developers](https://developers.openai.com/blog/skills-shell-tips)
- [From model to agent: Equipping the Responses API with a computer environment | OpenAI](https://openai.com/index/equip-responses-api-computer-environment/)
- [OpenAI upgrades its Responses API to support agent skills and a complete... | VentureBeat](https://venturebeat.com/orchestration/openai-upgrades-its-responses-api-to-support-agent-skills-and-a-complete)
- [OpenAI Agentic Primitives: Skills, Shell & Compaction Guide | SitePoint](https://www.sitepoint.com/openai-agentic-primitives-guide-skills-shell-compaction/)