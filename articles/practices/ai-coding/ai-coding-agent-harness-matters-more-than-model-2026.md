# AI Coding Agent 评测的正确问题：Harness 比模型更重要

## 核心命题

2026年的AI Coding Agent市场，三个界面形态瓜分天下：驱动Shell的终端Agent、嵌入编辑器的IDE原生工具、以及与代码平台深度绑定的平台Agent。头部玩家是Claude Code、OpenAI Codex、Cursor、GitHub Copilot和Google Antigravity，外加一群靠价格战抢市场的中国玩家。

但真正决定哪个工具能交付可工作代码的因素，**很少是模型本身**。真正重要的是**Harness**——围绕模型的那套脚手架：喂给它什么文件、运行什么命令、如何检查它的输出。

这个结论是反直觉的，但证据很扎实：在Terminal-Bench 2.1（2026年6月）上，GPT-5.5在Codex CLI里跑出83.4%，而同样的模型换到另一个Harness里只有76.4%。模型没变，脚手架变了，结果差了7个百分点。所以"哪个模型最强"是个错误的问题，"哪个Agent能交付任务"才是正确的问题。

---

## 一、2026 AI Coding Agent 全景图：三种形态

| 工具 | 厂商 | 界面 | 入门价格 | 适用场景 |
|------|------|------|---------|---------|
| Claude Code | Anthropic | 终端Agent | $20/月（Claude Pro）| 多文件重构、大规模代码库调试 |
| Codex | OpenAI | 终端 + IDE | $20/月（ChatGPT Plus）| 确定性多步任务、测试循环 |
| Antigravity 2.0 | Google | 桌面App + CLI | 绑定Google AI套餐 | 并行子Agent编排 |
| Gemini CLI | Google | 终端Agent | 免费层 + 付费 | Google技术栈内轻量终端任务 |
| Cursor | Anysphere | AI原生IDE | $20/月 | 内联编辑、文件感知补全 |
| Windsurf | Cognition | AI原生IDE | $20/月 | 编辑器内的in-house模型工作流 |
| Kiro | Amazon | AI原生IDE | 付费（AWS）| AWS上的Spec驱动开发 |
| GitHub Copilot | GitHub | 平台集成 | $10/月 | 最大用户基数，完整GitHub工作流 |
| GLM/Kimi/Qwen | 智谱/月之暗面/阿里 | 自带Harness | $18-$50/月 | 成本敏感场景，常内嵌于Claude Code或Cline |

三种界面形态里，**终端Agent的Harness设计空间最大**，因为它完全控制文件系统和命令执行；IDE原生工具的优势是上下文感知天然更强；平台集成工具的护城河是与代码托管流程的深度耦合。

---

## 二、Benchmark数据的盲区：为什么公开分数不等于真实能力

### Terminal-Bench 2.1 的数字

2026年6月的Terminal-Bench 2.1榜单（考核Agent在真实命令行环境中的任务完成能力）：

| Agent | 模型 | 得分 |
|-------|------|------|
| Codex CLI | GPT-5.5 | 83.4% |
| Claude Code | Opus 4.8 | 78.9% |
| Antigravity | Gemini 3.5 Flash | 76.2% |

但这些是**Agent+模型打包后的分数**，Harness的影响没有被隔离。

### 更干净的证据：统一Scaffold下的模型能力

Scale的SWE-bench Pro公开榜单，在**同一个SWE-Agent脚手架**下运行所有模型，结果完全不同：

- 最高分：GPT-5.4 @ xHigh设置，约59%
- 分数差距极小，头部模型咬得很紧

对比厂商自己报的SWE-bench Verified数字，动辄90%+——**这些数字是在各自调优过的Harness上跑出来的，不是统一舞台**。

从统一脚手架的59%到厂商自报的93%，这34个百分点的差距，就是Harness在干活。

### 为什么Harness能造成这么大差异

一个Coding Agent的Harness负责：

1. **上下文管理**：喂给模型的代码切片策略、Context Window利用方式
2. **命令执行**：允许Agent运行什么Shell命令，Fail-fast还是容错执行
3. **结果验证**：是否有多轮自我修正、错误后是否自动重试
4. **状态持久化**：长任务中断后能否从上一个检查点恢复

这四个维度在不同实现里差异巨大，直接决定了一个模型能发挥几成功力。

---

## 三、各家Harness设计哲学横评

### Claude Code：Planner-Evaluator内置合一

Claude Code的Harness最显著的特征是**主Agent本身就是Planner和Evaluator**，不依赖外部验证节点。Dynamic Workflows（2026年5月随Opus 4.8推出）进一步把这一设计扩展到多Agent场景：主Agent在Plan阶段拆分任务，在Execute阶段启动数百个并行子Agent，在Verify阶段对所有输出做质量门控后才交付用户。

这种设计的代价是**对模型本身的长程推理能力要求极高**——只有Opus 4.8级别的大模型才能稳定支撑这个循环。但好处是上下文共享是原生的，不需要额外配置状态快照。

### Codex CLI：确定性优先，Scaffold可观测

OpenAI的Harness设计哲学强调**可预测性和可调试性**。Codex CLI的Agent执行路径更线性，错误后倾向于快速失败而非无限重试，这让它的Terminal-Bench得分好看（因为Benchmark任务有明确终点），但在模糊的长程任务上可能比Claude Code更早放弃。

GPT-5.6 Sol（2026年6月27日）在官方演示中跑出Terminal-Bench 2.1最高分88.76%（max模式）和91.91%（ultra模式），但这些数字来自**政府限制预览**，约20个合作伙伴才能访问，公开榜单尚未更新。考虑到历史规律，这些数字应视为**厂商自报**，需等独立跑分验证。

### Antigravity：并行子Agent作为一等公民

Google的Antigravity从一开始就把并行子Agent编排做进了核心设计，而不是像Claude Code那样作为"研究预览"功能。这意味着它的Harness对多Agent状态聚合、冲突检测、结果汇交有更成熟的支持——代价是学习曲线更陡，配置项更多。

### Cursor：IDE上下文作为Harness优势

Cursor的Harness护城河不是模型，而是**编辑器内建的上下文感知能力**。它知道你在哪个函数里、哪个文件被打开、哪段代码被高亮，这使得它的上下文喂送策略比纯终端Agent更精准。代价是它被困在编辑器里，不适合纯命令行的长程重构任务。

---

## 四、笔者的判断：选型决策树

**错误的问题**：「用GPT-5.5还是Opus 4.8？」

**正确的问题**：「我的任务特征最适合哪种Harness设计？」

| 任务特征 | 推荐工具 | 原因 |
|---------|---------|------|
| 跨数十个文件的大规模代码迁移 | Claude Code（Dynamic Workflows）| 子Agent并行 + Verify机制 |
| 确定性测试生成和循环改进 | Codex | 线性执行路径，Fail-fast可预测 |
| 模糊的探索性调试 | Claude Code或Cursor | 上下文感知强，支持长程推理 |
| AWS技术栈内的Spec驱动开发 | Kiro | 平台集成深度 |
| 预算敏感的小任务 | GLM/Kimi/Qwen | 成本低，常嵌入Claude Code使用 |
| 需要GitHub平台深度集成 | GitHub Copilot | 工作流耦合最紧密 |

**一个关键规律**：如果你发现某个模型在你的任务上表现不如预期，先问Harness配置对不对，再考虑换模型。同一模型换一套Harness，分数可以差10个百分点以上。

---

## 五、Benchmark之外：Harness的隐性成本

公开的Benchmark只覆盖了"能跑通"这个维度，真实场景里还有几个Benchmark测不出来的隐性成本：

1. **配置复杂度**：Claude Code的Harness开箱即用，但Deep Tuning需要理解它的Planner逻辑；Antigravity的Harness功能最全，但上手配置项可能是最多的
2. **错误可调试性**：线性Harness（Codex）的错误更容易追踪；Planner+Evaluator合一的Harness（Claude Code）出错时需要理解整个评估循环的逻辑
3. **长任务稳定性**：Harness的状态管理能力直接决定了一个Agent能否完成跨越数小时的长程任务，而非在中途迷路

这三个隐性成本，才是真正拉开工具差距的地方。

---

## 结语

2026年的AI Coding Agent竞争，本质上已经不是模型的军备竞赛。GPT-5.5和Opus 4.8在基础能力上已经非常接近，真正决定交付质量的是**Harness的工程成熟度**：上下文管理、命令控制、结果验证、状态恢复。

选型时忘掉「哪个模型最强」这个问题。问自己：我的任务需要什么样的Harness？然后找到那个Harness设计最匹配任务的工具。

---

**引用来源**

- Capital & Compute: "The 2026 AI Coding Agent Landscape: Leaders, Costs, Harness" (https://capitalandcompute.net/blog/the-2026-ai-coding-agent-landscape/)
- Terminal-Bench 2.1 公开榜单 (https://arxiv.org/html/2601.11868v1)
- Scale SWE-bench Pro 公开leaderboard