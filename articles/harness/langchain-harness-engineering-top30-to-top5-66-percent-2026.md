# LangChain Harness Engineering：从 Top 30 到 Top 5 的 13.7 分跃升

> **笔者认为**：LangChain 这篇文章最重要的贡献不是那个 66.5% 的分数，而是它用可重复的实验证明了**同一个模型，换一个 harness，性能可以差出一整个leaderboard梯队**。这不是调参，这是系统级的工程跃迁。

---

## 核心命题

LangChain 的 coding agent `deepagents-cli` 在 Terminal Bench 2.0 上从 **52.8% 提升到 66.5%**（+13.7 分），排名从 Top 30 以外冲进 Top 5。整个过程**只改了 harness，模型一动不动**——用的是同一个 GPT-5.2-Codex。

这个数字背后的工程含义是：模型是通用品，harness 才是专用件。真正的 Agent 工程差距不在于选哪个模型，在于怎么设计 harness。

---

## Harness Engineering 的本质

LangChain 给出了一个定义：

> "The goal of a harness is to mold the inherently spiky intelligence of a model for tasks we care about. Harness Engineering is about systems, you're building tooling around the model to optimize goals like task performance, token efficiency, latency, etc."

Harness 是围绕模型的系统层工程，它的三个核心调节旋钮是：

| 旋钮 | 作用 | 示例 |
|------|------|------|
| **System Prompt** | 指导模型行为模式 | Planning/Build/Verify/Fix 四阶段框架 |
| **Tools** | 赋予模型执行能力 | 文件读写、bash 命令、测试运行 |
| **Middleware** | 模型与工具调用时的钩子 | PreCompletionChecklist、LoopDetection、LocalContext |

LangChain 的基准测试起步于"默认 prompt + 标准 tools+middleware"，得分 52.8%，刚好在 Top 30 门槛外面。这说明没有针对性优化的 harness，再强的模型也只能给出"还行"的下限。

---

## 实验方法：Trace Analyzer Skill

LangChain 的关键方法论是**让错误分析变成可重复的 Agent Skill**。

流程是：
1. 从 LangSmith 拉取实验 traces
2. 并行生成 error analysis agents → 主 agent 综合发现 + 建议
3. 聚合反馈 → 有针对性地修改 harness

> "This works similarly to boosting which focuses on mistakes from previous runs."

这个方法的价值在于**把人工经验固化成可执行的循环**。每次实验的失败案例都成为下次改进的输入，类似机器学习里的 gradient descent，只是搜索空间是 harness 配置而不是模型权重。

LangChain 承认人在第 3 步（验证和讨论修改建议）仍然有帮助，而且过度拟合特定任务会导致其他任务回退。但这个自动化的 trace 分析流程让实验周期从"几天"压缩到"几小时"。

---

## 真正起作用的工程机制

### 1. Build & Self-Verify 循环

LangChain 发现最常见的失败模式是：**agent 写完代码，重读一遍，确认看起来没问题，然后就停了**。没有测试，没有验证环节。

所以他们在 system prompt 里加了强制性的验证流程：

```
Planning & Discovery → Build → Verify → Fix
```

具体实现是一个 `PreCompletionChecklistMiddleware`：在 agent 退出前拦截，强制它跑一遍验证。LangChain 把它比作"Ralph Wiggum Loop"——一个 hook 强制 agent 在退出前继续执行验证，而不是直接 exit。

> "Testing is a key part of autonomous agentic coding. It helps test for overall correctness and simultaneously gives agents signal to hill-climb against."

这里的工程洞察是：**模型天然倾向于接受第一个看起来合理的解**。你需要主动打破这个倾向，强制它走一遍 build-verify 循环。

### 2. LocalContextMiddleware：替 agent 做好环境上下文

Terminal Bench 的任务带有目录结构、内置工具和严格超时。Agent 在陌生环境里容易犯错，因为不知道当前工作目录的结构、有什么工具可用。

LangChain 的解法是 `LocalContextMiddleware`：在 agent 启动时自动：
- 映射 cwd 和父子目录结构
- 运行 bash 命令找到 Python 安装等工具
- 把这些环境上下文注入 agent

> "Context discovery and search are error prone, so injecting context reduces this error surface and helps onboard the agent into its environment."

此外还加了**时间预算警告**：在 agent 快超时时提醒它切到验证阶段。模型不天然知道怎么估算时间，这个 heuristic 帮助 agent 在时间约束下做出正确决策。

### 3. LoopDetectionMiddleware：打断 Doom Loop

Agent 一旦决定某个方案，容易在同一个错误方向上重复尝试——LangChain 观察到有些 traces 出现了 10+ 次同一文件的编辑。

`LoopDetectionMiddleware` 通过 tool call hooks 追踪每个文件的编辑次数，在达到 N 次时主动注入"consider reconsidering your approach"的上下文。

> "This is a design heuristic that engineers around today's perceived model issues. As models improve, these guardrails will likely be unnecessary, but today helps agents execute correctly and autonomously."

这个工程选择承认了一个现实：**今天的模型还不够完美，harness 设计者的工作是围绕当前的缺陷做设计，同时为未来的模型做准备**。

### 4. Reasoning Sandwich：xhigh-high-xhigh

GPT-5.2-Codex 有 4 档推理模式：low、medium、high、xhigh。

LangChain 测试了不同的推理预算分配策略，发现：

| 策略 | 分数 | 问题 |
|------|------|------|
| 全程 xhigh | 53.9% | 超时太多 |
| high | 63.6% | 基线 |
| **xhigh-high-xhigh（头尾高、中间低）** | **66.5%** | 最优 |

> "A good plan helps get to a working solution more quickly... Later stage verification also benefits from more reasoning to catch mistakes and get a solution submitted."

推理预算的分配本身就是一个 harness 旋钮，不是模型参数。

---

## 定量结果与工程含义

| 指标 | 数值 |
|------|------|
| Terminal Bench 2.0 基准分 | 52.8% → 66.5%（+13.7） |
| 排名变化 | Top 30 以外 → Top 5 |
| 模型 | GPT-5.2-Codex（一动不动）|
| 改动范围 | System Prompt + Middleware + Context Injection |
| 主要工程机制 | Self-Verification + Tracing + Context Engineering + Loop Detection |

LangChain 还开源了他们的 traces 数据集和 deepagents 代码库（Python + JavaScript），允许社区复现和进一步研究。

---

## 关键 Pattern：Harness 的可迁移性

LangChain 的文章验证了一个重要假设：**harness 工程经验可以在模型间迁移，但需要适配**。

他们用 Claude Opus 4.6 测试了同一套 harness，得分 59.6%，比 Codex 差。这是因为他们没有针对 Claude 做同样的 improvement loop。

> "Many principles generalize like good context preparation and a focus on verification, but running a few rounds of harness iterations for your task helps maximize agent performance across tasks."

这意味着：
- **原则可以泛化**：好的上下文准备、验证优先
- **但每换一个模型都需要重新跑优化循环**：因为不同模型的 weaknesses 不同

---

## 开放研究问题

LangChain 列出了几个有价值的探索方向：

1. **多模型 Harness**：Codex + Gemini + Claude 协同，不同模型负责不同阶段（planning 用大模型，execution 用小模型）
2. **Memory Primitives**：让 agent 在持续任务中自主学习和改进
3. **RLM（Reasoning Model Learning）**：用强化学习方法更高效地挖掘 traces
4. **Harness 变化的跨模型测量**：什么样的 harness 改动在不同模型间有一致性效果

---

## 工程启示

**Harness Engineering 是让 Agent 从"能跑"到"跑好"的核心杠杆。**

LangChain 的 13.7 分跃升证明：
- **同样的模型，harness 不同，效果可以差一整个 leaderboard**
- **Self-verification 不是可选项，是让 agent 真正自主的核心机制**
- **Trace 分析是把工程经验固化成可重复循环的关键手段**
- **Loop detection / time budgeting 等 guardrails 是工程设计，不是模型缺陷**

笔者认为，这篇文章最重要的 insight 不是任何一个具体技术，而是**承认模型不完美，然后围绕这个现实做系统设计**。Harness 工程师的工作不是等待更好的模型，而是让今天的模型在当前约束下发挥最大价值。

---

**来源**：
- LangChain Blog: "Improving Deep Agents with harness engineering" (2026)
- Terminal Bench 2.0 Leaderboard
- LangChain Deep Agents GitHub (langchain-ai/deepagents)
- LangSmith Traces Dataset