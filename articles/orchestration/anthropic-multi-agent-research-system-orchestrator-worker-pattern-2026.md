# Multi-Agent Research System：Token 经济学与编排模式的工程实践

当一个 AI 任务无法在单一 Agent 的上下文中完成时，工程师面临的核心问题是：**如何将工作有效地分配给多个 Agent，同时保持协调性和结果质量？**

Anthropic 在 2025 年 6 月发布的 **Multi-Agent Research System** 工程实践提供了一个经过生产验证的答案。该系统采用了 **orchestrator-worker** 多 Agent 架构模式，在内部研究评估任务上实现了比单 Agent Opus 4 **提升 90.2%** 的性能表现。更关键的是，Anthropic 通过 BrowseComp 评估数据集分析发现：**Token 使用量单独解释了 80% 的性能方差**——这意味着多 Agent 架构的核心价值，在于突破单 Agent 的 token 上限以解决更复杂的问题。

笔者认为，这一发现对 Agent 系统设计具有重要的指导意义：多 Agent 架构的主要作用不是让 Agent 更聪明，而是让系统能够**花费足够的 token 来解决问题**。

---

## 为什么研究任务天然需要多 Agent 架构

传统的信息检索系统（如 RAG）采用静态检索模式：给定输入查询，从向量数据库中提取最相似的文本块，然后基于这些块生成回答。这种模式的根本局限在于：它假设正确答案已经存在于某个静态语料库中。

但研究工作的本质是**开放性的**——步骤无法提前预测，路径依赖于中间发现。Anthropic 如此描述：

> "Research work involves open-ended problems where it's very difficult to predict the required steps in advance. You can't hardcode a fixed path for exploring complex topics, as the process is inherently dynamic and path-dependent."

研究任务要求 Agent 具有灵活性，能够在发现新线索时转向或探索切向连接。这是一种**迭代式信息压缩**过程：Agent 在 vast corpus 中探索，将最有价值的 tokens 凝结为最终答案。

多 Agent 架构的优势在于：每个 subagent 拥有**独立的上下文窗口**，并行探索问题的不同方面，然后再将结果汇总给 lead agent。这种并行化不仅加速了过程，更重要的是通过**关注点分离**（separation of concerns）减少了路径依赖——每个 subagent 有自己的工具集、prompt 和探索轨迹，互不干扰。

---

## 架构解析：LeadResearcher → Subagents → CitationAgent

Anthropic 的 Research 系统采用三层架构：

**LeadResearcher（编排层）**：作为主控 Agent，LeadResearcher 接收用户查询后进行分析和策略规划，然后将任务分解为多个并行的 subtask，创建 Subagent 来执行。在执行过程中，LeadResearcher 通过**扩展思考模式**（Extended Thinking）来规划方法：评估哪些工具适合任务、判断查询复杂度、确定 subagent 数量，以及为每个 subagent 定义角色。由于研究过程可能产生超过 200,000 token 的上下文，LeadResearcher 会将计划持久化到 Memory 中，以防止被截断时丢失关键上下文。

**Subagents（并行工作层）**：每个 Subagent 是独立的 research worker，拥有特定的研究任务和明确的边界。Subagent 使用**交错式思考**（Interleaved Thinking）：在每次工具调用后评估结果质量、识别信息缺口，然后调整下一步查询策略。Anthropic 在实践中发现，在 subagent 层面也启用思考模式，显著提升了其适应性和任务完成效率。

**CitationAgent（后处理层）**：在 LeadResearcher 完成综合研究后，所有发现被传递给 CitationAgent。该 Agent 负责处理研究报告，识别需要引用的具体位置，确保所有声明都正确归因于来源。这一层的存在说明了多 Agent 架构的另一个优势：**不同阶段的任务可以使用不同的 prompt 模板和能力配置**，而非用同一个 Agent 完成所有事情。

从工作流来看，系统遵循以下迭代循环：用户提交查询 → LeadResearcher 制定计划并持久化 → 创建 Subagent 并行执行 → Subagent 通过搜索工具收集信息 → 评估结果并决定是否需要进一步研究 → 汇总结果到 LeadResearcher → 如果需要更多研究，创建额外的 Subagent 或调整策略 → 达到充分信息量后退出研究循环 → 传递给 CitationAgent 生成带引用的最终报告。

---

## Token 经济学：性能提升的真实来源

Anthropic 分享了一个极具洞察力的统计数据：在 BrowseComp 评估（测试 browsing agent 定位难以找到的信息的能力）中，**三个因素解释了 95% 的性能方差**：
- Token 使用量单独解释了 **80%** 的方差
- 工具调用次数是第二个解释因素
- 模型选择是第三个因素

这意味着多 Agent 系统有效的原因很简单：**它们帮助花费足够的 token 来解决问题**。

Anthropic 进一步指出，最新的 Claude 4 系列模型是 token 使用效率的重大改进：

> "The latest Claude models act as large efficiency multipliers on token use, as upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget on Claude Sonnet 3.7."

笔者认为，这一结论对工程决策有直接影响：与其为单 Agent 分配更多 token，不如通过多 Agent 架构在多个并行的上下文窗口中分配 token——后者能更有效地利用模型的能力。

然而，经济成本是必须正视的现实：Agent 交互通常消耗约 **4 倍于普通 chat 的 token**，多 Agent 系统则消耗约 **15 倍**。这意味着多 Agent 架构的适用场景必须满足：任务价值足够高、需要大量并行化、信息量超过单 Agent 上下文窗口限制，以及需要与多个复杂工具交互。Research 任务恰好满足这些条件——因此这是 Anthropic 选择多 Agent 架构的核心理由。

---

## Prompt 工程：7 条核心原则

Anthropic 在文章中总结了 7 条 prompt 工程原则，这些经验来自从原型到生产系统的完整迭代过程：

**1. 像你的 Agent 一样思考（Think like your agents）**

迭代 prompt 的前提是理解 prompt 的效果。Anthropic 使用 Console 构建了精确模拟真实系统行为的仿真环境，然后观察 Agent 逐步执行的过程。这种方法立即暴露了失败模式：Agent 在已有足够结果时继续搜索、使用过于冗长的搜索查询、或选择了错误的工具。

**2. 教授编排者如何委托（Teach the orchestrator how to delegate）**

Lead agent 需要将查询分解为 subtask 并向 subagent 描述。每个 subagent 需要：objective（目标）、output format（输出格式）、tools and sources guidance（工具和来源指导）、以及 clear task boundaries（明确的任务边界）。Anthropic 发现，简单短小的指令（如"research the semiconductor shortage"）往往过于模糊，导致 subagent 之间重复工作或误解任务。

**3. 根据查询复杂度缩放 effort（Scale effort to query complexity）**

Agent 难以自主判断不同任务所需的 effort。Anthropic 在 prompt 中嵌入了缩放规则：简单的事实查询需要 1 个 Agent 加 3-10 次工具调用；直接比较类任务需要 2-4 个 subagent 各 10-15 次调用；复杂研究可能需要 10+ 个 subagent 且有明确分工。没有这些显式规则，Agent 倾向于在简单查询上投入过多资源——这是早期版本的常见失败模式。

**4. 工具设计与选择至关重要（Tool design and selection are critical）**

Agent 与工具的接口（interface）的重要性不亚于 HCI。正确的工具是高效的——有时甚至是必需的。如果一个 Agent 在 Slack 中搜索上下文，而 Slack 没有被接入工具集，它从一开始就是徒劳的。通过 MCP server 接入外部工具时，问题会进一步放大，因为 Agent 会遇到描述质量参差不齐的未见过的工具。Anthropic 为 Agent 提供了明确的启发式规则：先检查所有可用工具、将工具使用与用户意图匹配、搜索广泛外部探索时使用 Web search、优先选择专业工具而非通用工具。

**5. 让 Agent 改进自己（Let agents improve themselves）**

Anthropic 发现 Claude 4 模型可以成为优秀的 prompt 工程师。当给定一个 prompt 和一个失败模式时，它们能够诊断 Agent 失败的原因并提出改进建议。Anthropic 甚至创建了一个工具测试 Agent：当给出一个有缺陷的 MCP 工具时，它尝试使用该工具，然后重写工具描述以避免失败。通过数十次测试，该 Agent 发现了关键细微差别和 bug——这使得使用新描述的未来 Agent 的任务完成时间**减少了 40%**。

**6. 先广度，后收窄（Start wide, then narrow down）**

Agent 倾向于默认使用过于具体和冗长的查询，导致返回结果稀少。Anthropic 的策略是：先让 Agent 使用简短、宽泛的查询进行探索，评估返回内容后再逐步聚焦特定主题。

**7. 引导思维过程（Guide the thinking process）**

Extended Thinking 模式可以作为可控的草稿纸。Lead agent 使用思考来规划方法，subagent 则在工具调用后使用交错式思考来评估质量、识别缺口并完善下一步查询。Anthropic 的测试表明，Extended Thinking 显著改善了指令遵循、推理和效率。

此外，Anthropic 还强调了**并行工具调用**的重要性：将 lead agent 启动 subagent 的方式从串行改为并行（每次 3-5 个），以及 subagent 内部从串行搜索改为并行搜索（每次 3+ 个工具），使复杂查询的研究时间**减少了高达 90%**。

---

## 评估方法：如何在不确定性中验证系统质量

多 Agent 系统的评估面临独特挑战：即使从相同的起点出发，Agent 也可能采取完全不同的有效路径——这意味着传统的"给定输入 X，系统应该遵循路径 Y 产生输出 Z"的评估模型不再适用。

Anthropic 的解决方案是：

**小样本快速启动**：在 Agent 开发的早期阶段，由于大量低垂的果实存在，单个 prompt 调整可能将成功率从 30% 提升到 80%。这种规模的改进可以通过仅几个测试用例就被识别出来。Anthropic 从约 20 个代表真实使用模式的查询开始，快速验证改动影响。

**LLM-as-Judge 规模化评估**：研究输出是自由形式的文本，很少有单一正确答案，这使得编程式评估变得困难。Anthropic 使用 LLM judge 根据评估标准对每个输出进行评分：事实准确性（声明是否与来源匹配？）、引用准确性（引用来源是否与声明匹配？）、完整性（是否涵盖了请求的所有方面？）、来源质量（是否优先使用一手来源而非低质量二手来源？）、工具效率（是否合理次数地使用了正确的工具？）。Anthropic 发现，单个 LLM call 输出 0.0-1.0 的分数和通过/失败等级的评估方法，与人类判断的一致性最高。

**人工评估捕捉自动化遗漏**：人类测试者能发现 eval 遗漏的边缘情况：异常查询上的幻觉回答、系统失败、或微妙的来源选择偏见。Anthropic 发现，早期 Agent 一致性地选择 SEO 优化的内容农场，而非权威但排名较低的来源（如学术 PDF 或个人博客）。在 prompt 中添加来源质量启发式规则解决了这个问题。

---

## 工程挑战：状态管理与错误级联

多 Agent 系统引入了单体系统不存在的工程挑战。Agent 是**有状态的**——它们可以长时间运行，在多次工具调用中维护状态。这意味着minor系统失败可能对 Agent 造成灾难性影响。

Anthropic 提到，传统的软件 bug 可能破坏一个功能，而 Agent 系统中的 minor 改动会级联成大的行为变化——这使得编写必须长时间运行并维护状态的复杂 Agent 代码变得异常困难。

笔者认为，这正是为什么多 Agent 系统的可靠性高度依赖于**观察性**（observability）和**快速迭代循环**。没有对 Agent 行为的细粒度可见性，工程师几乎不可能在问题扩散前识别和修复它们。

---

## 对工程师的落地启示

Anthropic 提出的一个开放性问题值得关注：未来是**通用 Agent** 还是在特定上下文中表现出色的**专用 Agent**？这个问题的答案将直接影响 Agent 系统的架构决策。

但从当前的工程实践角度，笔者认为最关键的收获是：多 Agent 架构不是万能药——它最适合的场景是高任务价值、大量并行化需求、单一上下文窗口无法容纳信息量、以及需要与多个复杂工具交互的任务。对于依赖共享上下文或 Agent 间存在大量依赖关系的任务，多 Agent 架构的协调开销可能超过其收益。

对于计划构建多 Agent 系统的工程师，Anthropic 的经验提供了一个清晰的优先级：**好的 prompt 设计和工具设计，比 Agent 数量更能决定系统质量**。从 few-shot prompt 优化开始，建立可靠的评估体系，才是大规模多 Agent 系统成功的真正基础。

---

**来源**：Anthropic Engineering Blog, *"How we built our multi-agent research system"*, Published Jun 13, 2025. https://www.anthropic.com/engineering/multi-agent-research-system
