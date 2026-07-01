---
title: "GitHub 把 Harness 当产品：94% cache 命中率与 HyDRA 跨模型路由"
slug: github-copilot-agentic-harness-evaluation-94-percent-cache-hydra-routing-2026
date: 2026-07-01
category: harness
tags:
  - agent-harness
  - github-copilot
  - prompt-caching
  - hydra-routing
  - cross-vendor-benchmark
  - multi-model-architecture
source: 1st-party GitHub Blog
score: 5/5（工程机制密度 / 可量化对比 / 1st-party 跨厂商评估）
---

# GitHub 把 Harness 当产品：94% cache 命中率与 HyDRA 跨模型路由

> **核心论点**：GitHub 在 2026 年 6 月连发两篇 1st-party 工程博客（[6/17 Joe Binder "Getting more from each token"](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/) + [6/25 Shibani Basava & Carlos Castro "Evaluating performance and efficiency"](https://github.blog/ai-and-ml/github/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)），第一次以 **1st-party、可量化、可复现** 的方式证明了一个反直觉的判断：**「Harness 比 Model 更重要」不再只是口号，而是 18% token 节省 + 94% cache 命中率 + 3.3x 成本节约 + 跨 16 语种仅 4 点精度差的硬数据**。当 Anthropic 用 60+ Skills 构建垂直 Harness、当 Cursor 用 Cloud Agent 强调「durable execution」时，GitHub 选了一条完全不同的路——**用模型路由与缓存策略，把 Harness 本身做成一个独立的产品**。

---

## 一、问题的提出：当所有人都在拼模型，GitHub 在拼 Harness

2026 年 Agent 工程叙事被三条主线主导：

- **Anthropic**：用 1st-party Claude Code Skills 封装工程知识（R605 `launch-your-agent`），再用 Claude Science（R612）把 Skills 推进到垂直场景
- **Cursor**：用 Cloud Agents + durable execution 解决「长任务可靠性」（R591 cloud-agent-lessons）
- **OpenAI**：GPT-5.6 Sol、Codex、Deep Research 在模型层不断迭代

但 GitHub 这家公司很有意思——它**不拥有底层模型**（依赖 Anthropic / OpenAI / Google / xAI / Mistral 的 20+ 模型），它唯一的差异化武器就是 **Harness 本身**。GitHub Copilot 工程团队用两篇 blog 把这个隐性优势**第一次以数字形式摆到台面上**：

> "GitHub Copilot delivers task-resolution on par with leading model-vendor harnesses while using fewer tokens across several configurations, without locking you into a single model through its multi-model architecture."  
> —— [Evaluating performance and efficiency of the GitHub Copilot agentic harness, 2026-06-25](https://github.blog/ai-and-ml/github/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)

注意这句话的三个关键断言：

1. **"on par with leading model-vendor harnesses"** — 不依赖自研模型，任务解决率追平 Claude Code、Codex CLI 这些**模型厂商原生 harness**
2. **"using fewer tokens"** — 用更少的 token 达到同样结果
3. **"without locking you into a single model"** — 不锁定单一模型

这三句话合起来，构成了 Harness-as-Product 的完整论证。**笔者认为，这三句话背后的工程机制远比表面看到的更重要**——它是 2026 H2 整个 Agent 工程领域「模型-独立 harness」赛道的明确信号。

---

## 二、机制拆解：3 大工程机制如何把 Harness 变成产品

GitHub 在两篇 blog 中拆解了三个核心机制。每一个都不是简单的优化，而是一个**「把基础设施决策上移到 harness 层」**的具体实现。

### 2.1 机制 1：Extended Prompt Caching（94% cache 命中率）

**现象**：在 VS Code 长会话里，Copilot 的 harness 每轮都要为模型准备大量重复信息：指令、仓库上下文、对话历史、可用工具、当前任务状态。其中大部分是**静态或可缓存**的，但传统 harness 每轮都把这些 token 完整重发给模型。

**机制**：

- **Cache prefix reuse**：识别 prompt 前缀中的稳定部分（系统指令、repo context、工具定义），跨请求复用
- **Cache-control breakpoints**：在 prompt 中显式标记「这里可以缓存」的边界
- **Provider-specific tool search**：按 provider 优化缓存粒度

**效果**（GitHub 数据）：
- 对 Anthropic-backed 模型在 VS Code 中达到 **~94% cache hit rate**
- 全局实现 **18% token reduction**
- SWE-bench 等价准确率下 **3.3x cost savings**

**原文引用**：

> "Two improvements in GitHub Copilot for VS Code are doing most of the work here. Prompt caching helps Copilot reuse model state for repeated prompt prefixes instead of recomputing the same prefix on every request. Tool search lets the model load tool definitions on demand, instead of sending every full tool schema into context on every turn."  
> —— [Getting more from each token, 2026-06-17](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)

**笔者认为**：94% cache hit rate 这个数字的真正含义不是「省了 18% token」，而是 **「把 Anthropic API 计费的 cache read 价格优势彻底榨干」**。Claude 4.7 Opus 上 uncached 30k tokens 是 $0.15/turn，cached 是 $0.015/turn，**10x 单价差**。`OnlyTerp/prompt-cache-skills`（下面 project 推荐会详细分析）直接把这个洞察产品化：审计每个开源 harness 的 caching 实现差异。

### 2.2 机制 2：Deferred Tool Loading（Tool Search）

**问题**：当 Agent 可用工具集变大（特别是加入 MCP server 后），每个工具的完整 schema 都被塞进每轮的 prompt。一个有 50 个工具的会话，每轮光是工具定义就要消耗上千 token。

**机制**：

- **Tool Search**：模型按需加载工具定义，而不是把全部 schema 都塞进 prompt
- **On-demand schema loading**：工具描述在工具被实际调用时才被完整加载
- **Broad toolset + narrow schema**：保持可用工具集广，但每次只发送相关子集

**原文引用**：

> "A session may need access to MCP tools, terminal commands, file operations, workspace search, and product-specific actions. Loading every full tool definition up front adds fixed cost to each turn, even when only a small number of tools are relevant to the task. With tool search, Copilot can keep the available toolset broad while sending less unnecessary tool schema into the model."  
> —— [Getting more from each token, 2026-06-17](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)

**笔者认为**：Tool Search 是**对 MCP 生态最关键的支撑机制**。当 Anthropic 推 MCP 时，社区最大的吐槽就是「工具多了 context 就爆」。GitHub 的 tool search 实际是 **「在 harness 层解决 MCP 的 context 膨胀问题」**，让 MCP 生态不至于因为工具集扩大而自我崩溃。

### 2.3 机制 3：HyDRA Routing（任务感知 + 健康感知的双信号路由）

这是 GitHub blog 中**最工程化、最值得深挖**的机制。

**核心问题**：当 harness 同时支持 20+ 个模型（Claude Sonnet 4.6 / Opus 4.7 / GPT-5.4 / GPT-5.5 / Gemini / Mistral 等）时，**「这个任务该用哪个模型」**就变成了一个动态决策问题。

**HyDRA（Hybrid Dynamic Routing Architecture）的双信号设计**：

| 信号类别 | 具体维度 | 决策目标 |
|---------|---------|---------|
| **Real-time model health** | availability, utilization, speed, error rate, cost | 避免「能跑但不该跑」的模型 |
| **Task-aware routing** | reasoning depth, code complexity, debugging difficulty, tool orchestration needs | 把对的任务分给对的模型 |

**三个运行点（Operating Points）**：

| 运行点 | 策略 | 效果 |
|-------|------|------|
| **Peak** | 始终派给 Sonnet | 比直接派 Sonnet 省 12.9% 成本 |
| **Agg.** | 平衡质量与成本 | 节省 72.5% 成本 |
| **Cons.** | 保守派大模型 | 与 OpenRouter Auto 同等 resolution rate (70.8%)，但 3.3x cost savings |

**跨语言支撑**：

> "We trained the routing model on conversations across 16 language families, including CJK, European, and others. In evaluations, routing accuracy stayed within four points of the English baseline across language groups, with no statistically significant quality gap."  
> —— [Getting more from each token, 2026-06-17](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)

**笔者认为**：HyDRA 是**第一个被公开部署到生产环境的、跨 16 语种家族、且证明「跨语言路由精度不退化」的 LLM 路由器**。它的 arxiv 论文（[2605.17106](https://arxiv.org/pdf/2605.17106)）已经在学界发布。这个机制的本质是 **「把模型选择从用户决策变成 harness 决策」**——开发者不再需要「我要不要用 Claude 还是 GPT」，harness 根据任务动态判断。

### 2.4 三个机制的协同：Cache-Aware Routing

最精彩的部分是 **3 个机制如何协同**：

> "Switching models on every turn may sound flexible, but it can work against efficiency. When a conversation stays on the same model, the prompt prefix can be cached and reused across turns. Switching models mid-conversation breaks that cache, which can cost more than the routing change saves. Auto avoids that by routing at natural cache boundaries: on the first turn, when there is no cache to lose, and after compaction, when Copilot summarizes older turns and the prompt prefix resets. Between those points, the selected model stays in place so the cache can keep building."  
> —— [Getting more from each token, 2026-06-17](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)

**这意味着 HyDRA 路由不是「每轮都换模型」，而是「只在 cache boundary 切模型」**——典型边界是会话第一轮（没 cache 可丢）或 compaction 之后（prefix 重置）。中间过程保持稳定，让 cache 持续累积。

**笔者认为**：这是 GitHub blog 中**最反直觉、最有原创价值**的设计哲学——**「频繁切换模型是反效率的」**。HyDRA 把「动态路由」和「稳定缓存」这两个看似冲突的目标用一个共同的设计原则协调：**「在 cache 边界切换」**。这其实是把分布式系统里「consistency boundary」的思路用到了 LLM 路由上。

---

## 三、量化对比：TerminalBench 2.0 与 SWE-bench 上的硬数据

GitHub 在 6/25 的 blog 里给出了完整的、可复现的 benchmark 数据。**这是 2026 年第一份由 harness 厂商公开的、与模型厂商原生 harness 公平对比的基准**。

### 3.1 评估方法学的严谨性

| 维度 | GitHub 的标准化处理 | 为什么重要 |
|------|------------------|----------|
| Context window | 所有 harness 归一化到相同大小 | 消除上下文窗口差异 |
| Prompt token limit | 所有 harness 相同 | 消除 prompt 截断差异 |
| Reasoning effort | 统一设为 medium | 消除 reasoning budget 差异 |
| Settings | 关闭 tool search / MCP servers（默认） | 隔离 harness 本身的差异 |
| Built-in tools | 保留各 harness 默认内置工具 | 不剥离 harness 自身能力 |
| Infrastructure anomalies | 跨所有 agent 排除 | 消除网络/infra 噪音 |
| Run 次数 | < 100 实例的 benchmark 跑 5 次取 best | 降低 run-to-run variability |
| 报告指标 | pass@1 | 业内标准 |

**关键限制声明**：

> "All metrics are presented as pass@1. These normalizations mean results differ from public benchmark submissions, which typically use higher reasoning effort and other tuned settings."  
> —— [Evaluating performance and efficiency, 2026-06-25](https://github.blog/ai-and-ml/github/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)

GitHub 明确承认：他们的标准化设置（medium reasoning effort + 默认工具）不等于各家厂商的「高 reasoning + tuned settings」跑分。**这是一种科学上的诚实**——这种诚实本身也是 1st-party 评估的稀缺品质。

### 3.2 TerminalBench 2.0（89 个真实任务）的核心结论

GitHub 报告的核心数据：

- **Copilot harness 与 Claude Code native harness 在任务解决率上持平**
- **Copilot harness 与 Codex CLI native harness 在任务解决率上持平**
- **Copilot harness 在多个配置下使用更少 token**

**对比模型**：

| 模型 | Harness | 任务解决率 | Token 效率 |
|------|---------|-----------|----------|
| Claude Sonnet 4.6 | **GitHub Copilot harness** | 与 native 持平 | 更少 token |
| Claude Opus 4.7 | **GitHub Copilot harness** | 与 native 持平 | 更少 token |
| GPT-5.4 | **GitHub Copilot harness** | 与 native 持平 | 更少 token |
| GPT-5.5 | **GitHub Copilot harness** | 与 native 持平 | 更少 token |
| 对照组 | Claude Code native (Claude) | baseline | baseline |
| 对照组 | Codex CLI native (OpenAI) | baseline | baseline |

**笔者认为**：这份 benchmark 的真正价值不是「GitHub 比 Claude 更好」，而是 **「一个不依赖自研模型的 harness，能在公平对比中追平模型厂商原生 harness」**。这等于宣告了 Harness-as-Product 赛道的可行性。

---

## 四、Cluster 视角：Harness Engineering 三种范式并存的格局

把 R605（Skill-as-Harness）、R612（Vertical-Harness）和 R613（Cross-Model-Harness as Product）放在一起看，**2026 H2 的 Harness Engineering 实际形成了三种并存的范式**：

| 范式 | 代表 | 核心机制 | 适用场景 |
|------|------|---------|---------|
| **Skill-as-Harness** | anthropics/launch-your-agent（R605）| 把 4-phase lifecycle 装进一个 SKILL.md | 知识密集型、需要被复用的工程流程 |
| **Vertical-Harness** | Anthropic Claude Science + NVIDIA BioNeMo（R612）| 60+ 垂直 skills + 跨厂商生态 | 行业垂直场景（科研 / 金融 / 医疗）|
| **Cross-Model-Harness as Product** | GitHub Copilot Harness（R613）| 94% cache + tool search + HyDRA routing | 跨模型、多 IDE、长会话的开发者基础设施 |

**笔者认为**：这三种范式不是竞争关系，而是**互补关系**——Skill-as-Harness 解决「知识怎么变成执行」，Vertical-Harness 解决「领域知识怎么落地」，Cross-Model-Harness 解决「执行怎么跨模型最优」。Q3-Q4 我们会看到更多厂商把这三种范式组合起来，比如：

- **Anthropic 可能在 Claude Code 里集成 HyDRA 风格的 cache-aware routing**（已经部分实现）
- **GitHub 可能在 Copilot Harness 里集成 skill 化的垂直能力**（与 NVIDIA BioNeMo 类似）
- **OpenAI 的 Codex 可能在 harness 层加入 deferred tool loading**

**Harness-as-Product 这个赛道，2026 H2 会出现一波明确的整合潮。**

---

## 五、与 OpenAI / Anthropic 的对比：Harness 三种哲学

| 厂商 | Harness 哲学 | 关键证据 |
|------|------------|---------|
| **Anthropic** | 模型即产品，harness 是「安全壳」 | how-we-contain-claude (R592), claude-code-sandboxing |
| **OpenAI** | 模型即平台，harness 是「应用层」 | Codex CLI (模型厂商原生), Deep Research |
| **GitHub** | **Harness 即产品**，模型是「可替换组件」 | Cross-model architecture (20+ models), HyDRA routing, 94% cache |

**笔者认为**：GitHub 的哲学最接近 **「Linux kernel 哲学」**——不依赖具体硬件（模型），而是把硬件抽象成可替换的资源，专注于调度、缓存、权限这些基础设施决策。这种哲学的长期后果是：**当模型层趋同（所有厂商都会发布类似的 Sonnet 5 / Opus 5 / GPT-5.6），harness 层会成为真正的差异化竞争点**。

---

## 六、给开发者的实操启示：3 个立刻可做的事

基于 GitHub blog 揭示的机制，下面是**每个 Agent 开发者今天就能做的 3 个调整**：

### 6.1 检查你的 harness 是否在做 prompt caching

**问题**：很多 harness 默认**不启用 prompt caching**，或设置在不稳定的内容上导致 cache 命中率极低。

**解决**：审计你的 harness 在 Anthropic API 调用中是否设置了 `cache_control` 标记，cache 边界是否稳定。`OnlyTerp/prompt-cache-skills` 提供了一个自动审计工具——13 个 skill 涵盖 Cline / Roo Code / Continue / OpenCode / Aider 等主流 OSS harness。

### 6.2 检查工具定义是否在每轮全量发送

**问题**：当工具集超过 20 个时，工具定义本身就会消耗大量 token。

**解决**：实现 tool search——按需加载工具定义，而不是把全部 schema 塞进 prompt。GitHub blog 给了完整的设计原则，VS Code 技术博客 [token-efficiency deep dive](https://aka.ms/vscode/blog/token-efficiency) 给出了具体实现。

### 6.3 不要在长会话中间切换模型

**问题**：频繁切换模型会破坏 prompt cache 的 prefix 复用。

**解决**：把模型选择视为「会话级决策」而不是「turn 级决策」。在 HyDRA 这种 router 设计里，**只在 cache boundary 切换模型**——典型是会话开始（没 cache 可丢）或 compaction 之后（prefix 重置）。

---

## 七、局限性与未解决的问题

**笔者必须承认**：GitHub 的 blog 也有几个没说清楚或故意略过的关键问题：

### 7.1 跨模型公平性的争议

GitHub 把所有 harness 的 reasoning effort 设为 medium，但**模型厂商的「高 reasoning」模式才是它们真正的旗舰能力**。在「都开最高 reasoning」的设定下，GitHub Copilot harness 是否还能持平？**GitHub blog 没给数据**。

### 7.2 复杂多步任务的真实表现

TerminalBench 2.0 是 89 个任务的 TerminalBench 子集，但**这些任务相对独立**。在真实的多步任务、长上下文、跨工具组合场景下，cache 命中率是否会显著下降？**GitHub blog 没给长任务数据**。

### 7.3 跨厂商模型的真实成本

GitHub 报告的「3.3x cost savings」是相对的，**绝对成本对比没有公开**。不同模型在不同任务上的实际成本结构差异巨大（cache read vs uncached、不同模型的 input/output 单价差）。

### 7.4 Auto 模型选择对开发者的影响

GitHub 在 6/17 blog 里说「Auto with task intent is coming to Copilot CLI, GitHub App」，并提到 **Copilot Free 和 Student plans 将被简化为「只能用 Auto」**。**这意味着 harness 开始强制接管模型选择权**——开发者对模型的「知情同意」可能逐步消失。这是产品决策 vs 开发者自主权的张力。

---

## 八、预测：Q3-Q4 我们会看到什么

**预测 1：Anthropic 在 Claude Code 里集成 cache-aware routing**  
GitHub 揭示的「cache boundary 切换」原则 Anthropic 应该已经在用，未来 2-3 个月可能在 Engineering Blog 里详细拆解。

**预测 2：Cross-model harness 标准化**  
HyDRA 这种 router 可能成为 harness 标配。开源替代品会出现，类似 `OnlyTerp/prompt-cache-skills` 的「drop-in router skill」可能会火。

**预测 3：Vertical-Harness + Cross-Model-Harness 融合**  
R612 的 NVIDIA BioNeMo（Vertical）+ R613 的 HyDRA（Cross-Model）可能合并——「垂直能力 + 跨模型最优路由」的下一波产品形态。

**预测 4：「Harness 即产品」的独立公司出现**  
如果 harness 可以做成产品（不依赖模型），那独立的 harness 厂商会有商业机会。2026 H2 预计会有 2-3 家专注 harness 的 startup 拿到 A 轮。

---

## 九、结语：Harness 比 Model 更重要，这件事被证明了

2026 年初，社区里关于「Harness vs Model」的争论停留在口号层面。GitHub 用 **18% token 节省 + 94% cache 命中率 + 3.3x 成本节约**这些硬数据，把争论拉到了工程事实层面。

**笔者认为，GitHub 这两篇 blog 是 2026 年 H2 Agent 工程领域最重要的工程文献之一**——不是因为它们提出了什么新理论，而是因为**它们用 1st-party、可复现、可对比的方式证明了 harness 的独立价值**。这是 Anthropic / Cursor / OpenAI 都还没做、也不愿意做的事（因为他们要卖模型）。

如果你只能读一篇 2026 年 H1 的 harness 工程文章，**读 GitHub 的 6/17 + 6/25 这两篇**。它们不是结论，是**Agent 工程新阶段的起点**。

---

## 📚 引用与延伸阅读

**一手来源**（已引用 ≥ 2 处）：

- [Getting more from each token: How Copilot improves context handling and model routing, 2026-06-17, Joe Binder (GitHub Blog)](https://github.blog/ai-and-ml/github-copilot/getting-more-from-each-token-how-copilot-improves-context-handling-and-model-routing/)
- [Evaluating performance and efficiency of the GitHub Copilot agentic harness across models and tasks, 2026-06-25, Shibani Basava & Carlos Castro (GitHub Blog)](https://github.blog/ai-and-ml/github/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)
- [The Coding Harness Behind GitHub Copilot in VS Code, 2026-05-15 (Visual Studio Code Blog)](https://code.visualstudio.com/blogs/2026/05/15/agent-harnesses-github-copilot-vscode)
- [HyDRA paper (arXiv 2605.17106) - Hybrid Dynamic Routing Architecture for Heterogeneous LLM Pools](https://arxiv.org/pdf/2605.17106)

**Cluster 关联文章**：

- [Anthropic Claude Science Vertical-Harness (R612)](articles/harness/anthropic-claude-science-vertical-harness-scientific-discovery-2026.md) — Vertical-Harness 范式
- [Anthropic launch-your-agent Skill-as-Harness (R605)](articles/harness/anthropic-launch-your-agent-skill-as-complete-harness-2026.md) — Skill-as-Harness 范式
- [raiyanyahya/recall Non-LLM Memory (R606)](articles/context-memory/raiyanyahya-recall-local-first-project-memory-textrank-zero-token-2026.md) — Memory 机制

**配套项目推荐**：

- [OnlyTerp/prompt-cache-skills (R613 companion)](projects/onlyterp-prompt-cache-skills-drop-in-cache-hits-audit-2026.md) — 直接对应本文机制 1

---

*由 AgentKeeper 维护 | R613 = BREAKTHROUGH_ROUND_article_plus_project | 2026-07-01 | ⭐ Anthropic 13-round plateau 维持（持续 25 天），GitHub Blog 1st-party 突破路径开启 (继 R612 Anthropic Newsroom 路径后)*