# cobusgreyling/loop-engineering：让 Agent 系统代替你「催促」Agent

**Stars**: 143⭐ | **License**: MIT | **Topics**: `loop-engineering`, `claude-code`, `mcp`, `coding-agents`, `anthropic`

**GitHub**: https://github.com/cobusgreyling/loop-engineering

---

## 核心命题

Loop Engineering 的核心洞察是：**把「你催促 Agent 干活」这件事本身，变成一个可设计的系统**。不是写更好的 Prompt，而是设计 Prompt 的 Prompt——一套控制平面，让 Agent 在长任务中自主迭代、验证、交接。

> "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops."
> — **Boris Cherny**, Head of Claude Code at Anthropic

---

## 为什么值得关注

### 1. Claude Code 官方背书的元框架

Boris Cherny（Claude Code 产品负责人）在 loop-engineering essay 中明确引用了这个概念：「我的工作就是写 loops，不再直接 prompt Claude」。这意味着 Loop Engineering 不是社区自嗨，而是 Anthropic 内部认同的 Agent 演进方向。

### 2. 五块积木 + Memory = 可复用的控制平面

README 给出的 Loop 六要素：

| Primitive | 在 Loop 中的职责 |
|-----------|------------------|
| **Automations / Scheduling** | 定时发现 + 分拣 |
| **Worktrees** | 安全并行执行空间 |
| **Skills** | 持久化的项目知识 |
| **Plugins & Connectors** | 接入真实工具（MCP）|
| **Sub-agents** | Maker / Checker 分离 |
| **Memory / State** | 对话外持久化的脊柱 |

笔者认为，这六要素的组合本质上是把 **Harness 的评估器循环**（evaluator loop）拆解成了可独立替换的组件——每个组件都可以按需替换或升级，而不是绑定在某一个框架里。

### 3. 开箱即用的 CLI 工具链

项目自带三个可直接用的 npm 包：

```bash
# Loop 就绪度评分（活动检测）
npx @cobusgreyling/loop-audit . --suggest

# 脚手架生成（pattern + budget/run-log）
npx @cobusgreyling/loop-init . --pattern daily-triage --tool claude-code

# Token 消耗估算
npx @cobusgreyling/loop-cost
```

这三个工具覆盖了 Loop Engineering 最落地的三个问题：**我的 loop 设计得对不对？** → loop-audit；**怎么快速起一个新 loop？** → loop-init；**这次跑了多少 token？** → loop-cost。

### 4. 支持主流 Coding Agent

README 给出了 Grok / Claude Code / Codex / Cursor 的 **Primitives Matrix**（跨工具对照表），以及各工具的 starters 目录。团队里有人用 Claude Code，有人用 Cursor，可以各自跑自己的 loop，在 Memory 层共享状态。

---

## 架构解剖：Loop 的 Mermaid

```
Schedule / Automation → Triage Skill → Read/Write STATE/Memory 
→ Isolated Worktree → Implementer Sub-agent → Verifier Sub-agent 
→ MCP / Git / Tickets → {Human Gate?} → Commit/PR/Action
```

笔者认为这个流程图最有价值的地方在于 **Human Gate 的设计**：不是把 human-in-the-loop 当作「暂停按钮」，而是当作一个带上下文的 escalation 通道——ambiguous 或 risky 的决策才上报，安全决策直接通行。这比「每步都等人确认」高效得多。

---

## 与 R337 Checkpoint/Resume 协议的关联

Loop Engineering 和 R337 文章讨论的 Checkpoint/Resume 协议在工程上形成互补：

| Checkpoint/Resume 协议 | Loop Engineering |
|-----------------------|------------------|
| Context 的持久化与恢复 | State/Memory 层的 durability |
| Protocol 层规范（handover 格式）| 六要素组合的控制平面 |
| 长任务中断恢复 | Loop 的自动 resumption |

inferoa（R377）解决的是 **推理层的 token efficiency**，loop-engineering 解决的是 **控制层的迭代设计**——两者共同构成了 Harness 工程的两端。

---

## 快速上手

```bash
# clone 并查看 pattern picker
git clone https://github.com/cobusgreyling/loop-engineering.git
cd loop-engineering

# 看自己适合哪个 pattern
cat docs/pattern-picker.md

# 用 loop-init 初始化一个 daily-triage loop
npx @cobusgreyling/loop-init . --pattern daily-triage --tool claude-code
```

---

## 笔者判断

Loop Engineering 是一个**元框架**：它不替代 LangChain 或 CrewAI，它在这些框架之上提供了一套「如何组织 Agent 迭代」的设计原则。

**适合的场景**：
- 长任务（数小时/数天）需要自主迭代的 Agent
- 多 Agent 协作需要统一的 checkpoint/gate 规范
- 团队共用 Agent 系统，需要控制边界而非信任 Prompt

**不适合的场景**：
- 短任务（单轮或几轮）不需要循环控制
- 只需要单个 Agent 执行固定命令

**一句话总结**：与其花时间写更巧妙的 Prompt，不如用 loop-engineering 设计一套让 Agent 自己迭代的系统——Boris Cherny 已经在这么做。