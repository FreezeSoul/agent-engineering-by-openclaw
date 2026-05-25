# Seeing Like an Agent：Anthropic 的工具设计方法论

> 原文：[Seeing like an agent: how we design tools in Claude Code](https://claude.com/blog/seeing-like-an-agent)（2026年4月10日，Anthropic，Thariq Shihipar）

## 核心论点

**工具设计不是填功能表，而是一场持续的用户研究——只不过用户是模型。**

Anthropic 工程师 Thariq Shihipar 在这篇博客中揭示了 Claude Code 工具设计的底层方法论：设计工具时，不是问"这个工具该有什么功能"，而是问"这个工具是否适配模型当下的能力边界"。随着模型变强，昨天正确的工具可能正在成为今天的约束。

---

## 一、核心原则：工具服务于能力，而非弥补缺陷

设计工具时，团队用了一个类比：如果让你解一道复杂的数学题，你会想要什么工具？

- 纸笔：最基础，但受限于手动计算
- 计算器：更好，但需要知道高级选项怎么用
- 计算机：最强大，但需要会写代码并执行

这个框架的核心洞察是：**你希望工具与使用者自身的能力模型对齐，而不是替它补足能力**。

> "You want to give it tools that are shaped to its own abilities. But how do you know what those abilities are? You pay attention, read its outputs, experiment. You learn to see like an agent."
>
> 你想让工具适配模型自身的能力。但你怎么知道这些能力边界在哪里？你需要关注模型的输出、阅读它的行为、不断实验。**学会像 Agent 一样看问题。**

这引出了工具设计方法论的第一性原则：**工具设计的依据是模型的真实行为数据，而不是功能清单**。

---

## 二、三个迭代案例：从失败中逼近正确答案

### 案例1：AskUserQuestion — 工具需要被模型愿意调用

**问题**：如何降低用户与 Claude 之间的沟通摩擦，让 Claude 的提问更高效？

**尝试1：修改 ExitPlanTool 参数**
在退出计划工具中加入 questions 数组参数，让 Claude 在返回计划时附带问题。这个方案实现成本最低，但让模型困惑——它同时被要求给出一个计划和问题列表，两者之间产生了冲突。当用户答案与计划矛盾时，模型该如何处理？方案放弃。

**尝试2：改变输出格式**
让 Claude 输出带格式的问题列表（Markdown bullet + 括号选项），由前端解析成 UI。但 Claude 做不到可靠地遵循这个格式——它会附加额外句子、遗漏选项、或直接放弃结构。方案放弃。

**尝试3：专用 AskUserQuestion 工具**
最终解法是一个专用的结构化工具，Claude 可以在任何时机调用，尤其在 plan mode 时会被特别提示触发。工具调起一个模态框展示问题，等待用户回答后才继续执行。

**关键洞察**：即使是最优设计，如果模型不理解怎么调用它，工具也不会起作用。最终方案成功的根本原因是 Claude "愿意"调用这个工具——它感知到了这个工具的调用收益。

> "Most importantly, Claude seemed to like calling this tool and we found its outputs worked well. After all, even the best designed tool doesn't work if Claude doesn't understand how to call it."

---

### 案例2：Tasks vs Todos — 工具会随模型进化从助力变成阻力

**问题**：TodoWrite 工具曾经有效，但随着模型能力提升，它开始产生副作用。

早期 Claude Code 为模型提供了 TodoWrite 工具，用于维护任务清单并向用户展示进度。即使如此，Claude 仍然经常遗忘待办事项，于是团队在每 5 轮对话时插入系统提醒。

**问题在于**：随着模型能力变强，这些提醒开始起反作用——Claude 开始认为它"必须严格遵守清单"，而不是根据实际情况修改它。当 Opus 4.5 开始更好地使用 subagent 时，新的问题出现了：多个 subagent 如何在一个共享的 Todo 列表上协调？

**解法**：用 Task 工具替代 TodoWrite 工具。Tasks 的设计目标不是"保持模型在轨道上"，而是"帮助 agents 之间互相通信"。Tasks 可以包含依赖关系、在 subagents 之间共享更新，模型可以 altering and deleting them。

**核心判断**：当模型能力跨越某个门槛时，曾经帮助它的工具反而开始限制它。工具设计者需要**周期性地推翻自己之前的假设**，这是 Harness Engineering 的核心能力。

> "As model capabilities increase, the tools that your models once needed might now be constraining them."

---

### 案例3：搜索接口 — 渐进式披露（Progressive Disclosure）代替增加工具

**问题**：Claude Code 早期用 RAG 构建上下文——向量数据库预索引代码库，Harness 在每次响应前检索相关片段并交给模型。

RAG 方案的问题：
1. 需要 indexing 和 setup，在各种环境下脆弱
2. **最重要的**：模型是被"给予"上下文，而不是自己"找到"上下文

团队问自己：如果 Claude 能搜索网页，为什么不能搜索本地代码库？

**解法**：给 Claude 一个 Grep 工具，让它自己构建上下文。随着模型变强，它在给定正确工具后，越来越擅长自己构建上下文。

**Progressive Disclosure 原则**：当引入 Agent Skills 后，团队将这个思路 formalize——允许 agents 通过探索逐步发现相关上下文。Skills 文件可以引用其他文件，模型可以递归地读取它们。Skills 的一种常见用途就是为 Claude 添加更多搜索能力——给它使用某个 API 或查询数据库的指令。

> "Over the course of a year, Claude went from not really being able to build its own context to being able to do nested search across several layers of files to find the exact context it needed."

---

## 三、Progressive Disclosure 的极致案例：Claude Code Guide 子 Agent

Claude Code 目前有约 20 个工具。团队持续评估是否需要这么多工具——**新增工具的门槛很高，因为每增加一个工具，模型就需要多一个"需要考虑"的选项**。

当团队发现 Claude 对 Claude Code 本身的功能（如"如何添加 MCP"、"slash 命令是什么"）了解不足时，有两个选择：

1. 把所有文档塞进 system prompt → 造成上下文腐化，干扰模型的主要任务（写代码）
2. 渐进式披露：给 Claude 一个链接，让它按需加载和搜索文档

第二个方案尝试后出现了新问题：Claude 会把一大段文档都拉进上下文，只为找一句话能回答的答案。

**最终解法：Claude Code Guide 子 Agent**

这不是一个新工具，而是一个专用子 Agent。当用户询问关于 Claude Code 本身的问题时，主 Agent 调用这个 subagent。subagent 在自己的上下文中做文档搜索、按照详细指令提取信息，只把最终答案返回给主 Agent。主 Agent 的上下文保持干净。

> "The subagent does the doc-searching in its own context, follows detailed instructions on how to search and what to extract, and hands back only the answer. The main agent's context stays clean."

---

## 四、方法论总结：工具设计的五个判断原则

| 判断维度 | 错误做法 | 正确做法 |
|---------|---------|---------|
| **工具边界** | 用工具弥补模型能力不足 | 工具应适配模型已有能力 |
| **调用率** | 功能完整但模型不调用 | 模型主动愿意调用 |
| **进化性** | 设计一次，长期不更新 | 周期性重新评估：工具是否从助力变阻力 |
| **数量控制** | 功能越多越好 | 新增工具门槛高，优先用 Progressive Disclosure |
| **上下文管理** | 把信息塞进 system prompt | 建立专门子 Agent 处理专门信息的获取 |

---

## 五、实践启示

**1. 建立"模型视角"的观察机制**

工具设计不是架构师坐在办公室里想出来的。你需要：
- 定期阅读模型输出，理解它实际如何使用工具
- 分析工具调用日志，找出"设计意图 vs 实际行为"的偏差
- 设计 A/B 测试，验证新工具是否真的被采用

**2. 工具清单需要版本化管理**

Claude Code 的 ~20 个工具不是一次性设计出来的，而是经过多次迭代。每引入一个工具，都要假设它将来可能需要被修改或移除。TodoWrite → Task 的演进不是失败，是正常的产品迭代过程。

**3. Progressive Disclosure 是扩展功能的首选策略**

在考虑新增工具前，先问：
- 能否通过 subagent 或专用技能处理这个需求？
- 能否通过给模型提供搜索能力让它自己找到答案？
- 塞进 system prompt 的信息是否会干扰模型的主要任务？

> "The bar to add a new tool is high, because this gives the model one more option to think about."

**4. Claude Code Guide 是一个范式转移**

把专门信息的获取封装成 subagent，而不是工具或 system prompt，是一个重要的架构选择。它示范了：主 Agent 的上下文应该只保留当前任务相关的信息，支撑信息应该通过专门渠道按需获取。

---

## 原文引用

> "One of the hardest parts about building an agent harness is constructing its tools. Claude acts completely through tool calling, but there are a number of ways tools can be constructed in the Claude API with primitives like bash, skills and code execution."

> "Designing the tools for your models is as much an art as it is a science. It depends heavily on the model you're using, the goal of the agent and the environment it's operating in. Our best advice? Experiment often, read your outputs, try new things. And most importantly, try to see like an agent."

---

*文章分类：`fundamentals/`（Agent 设计模式 · 工具工程方法论）*
*关联 Project：`epiral/bb-browser`（MCP Browser Use — 将真实浏览器登录态作为 Agent 的工具接口）*