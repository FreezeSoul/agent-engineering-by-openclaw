# Anthropic 内部分享：Claude Code Skills 工程实践的 8 条硬经验

> 原文：https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills  
> 作者：Anthropic Engineering Team  
> 标签：#fundamentals #skills #engineering-patterns  

---

## 核心命题

Anthropic 在内部运行了数百个 Claude Code Skills，这些经验揭示了一个反直觉的结论：**最容易做的 Skills 反而最没用**。真正有价值的 Skills 不是塞给 Agent 更多知识，而是修正 Agent 的默认行为模式。

---

## 背景

Claude Code Skills 是 Claude Code 的扩展机制，将领域专业知识封装成文件格式，让通用 Agent 变成特定领域的专家。Anthropic 自己在内部部署了数百个 Skills，这些经验形成了他们独特的工程认知。

**笔者认为**：大多数 Skills 教程强调「给 Agent 知识」，但 Anthropic 的经验指向了一个更精准的定位——**Skills 是用来修正 Agent 默认行为的，不是用来补充知识的**。这个认知转变决定了 Skills 的设计方向。

---

## 经验 1：不要陈述显而易见的事

> "Claude already knows how to code and can read your codebase. A skill that restates what Claude would do by default adds context without adding value."

这是 Anthropic 最反直觉的一条经验。开发者本能地想用 Skills 给 Agent 填充知识，但 Claude Code 本身已经具备编程能力——一个只提供「标准知识」的 Skill 只是在浪费上下文窗口。

**真正值得做的 Skills**：提供 Claude 默认行为中**缺失或薄弱**的领域知识。

**案例**：前端设计 Skill 不是告诉 Claude「如何写 CSS」，而是修正它默认的设计品味——避免 Inter 字体、紫渐变等经典俗套。这个 Skill 来自 Anthropic 工程师与客户的迭代，核心价值是「推着 Claude 走出舒适区」。

**笔者认为**：这个原则的直接推论是——如果你写 Skill 时大部分内容是「告诉 Agent 正常工作流程」，那你应该直接删掉这些内容，把空间留给真正独特的东西。

---

## 经验 2：加上一个「踩坑记录」章节

Anthropic 建议每个 Skill 都包含一个 `## Gotchas` 或 `## Pitfalls` 章节，记录这个领域中最容易出错的地方。

**为什么这很重要**：Agent 在执行长任务时，容易在边界条件处滑入错误路径。明确的踩坑记录让 Agent 能够在决策点主动规避问题，而不是遇到错误再回头。

**笔者的工程判断**：这个设计呼应了 LangChain 的 `RubricMiddleware` 思路——让 Agent 自己知道「做够了没有」。Gotchas 章节本质上是一种**负样本工程**，告诉 Agent「这里不要这样做」。

---

## 经验 3：小型团队直接提交到代码库，大型团队需要内部插件市场

Anthropic 观察到了明显的规模效应：

| 团队规模 | 策略 | 原因 |
|---------|------|------|
| 小型团队（少量仓库）| 将 Skills 提交到各仓库 | 简单直接，Skills 与代码紧耦合 |
| 大型团队（多仓库/多团队）| 内部插件市场 | 分布式管理，团队自主选择，包含安装引导流程 |

**内部插件市场的关键设计**：Anthropic 没有建立「中央委员会」来审批 Skills。他们采用**有机发现**机制——任何人创建了有用的 Skill，就上传到一个沙箱文件夹，分享链接到 Slack 或其他论坛让大家试用。

**笔者认为**：这个设计体现了 Anthropic 一贯的「去中心化」工程文化。集中审批的问题是：审批者不是一线工程师，无法判断 Skill 的实际价值。让使用者投票比让委员会审批更有效。

---

## 经验 4：Skills 的上下文成本需要被管理

> "Every skill that is checked in also adds a little bit to the context of the model."

这条经验点出了一个被普遍忽视的问题：每个 Skill 都会占用 Context Window 空间。当一个团队有几十个 Skills 时，累积的上下文成本可能影响 Agent 的推理质量。

**工程权衡**：Skills 不是越多越好。需要建立一种机制来评估「这个 Skill 带来的价值 vs. 它占用的上下文成本」。

**笔者的实践建议**：定期 review 团队内的 Skills，删除那些「偶尔有用但大部分时间浪费上下文」的低价值 Skill。

---

## 经验 5：Skills 已成为 Claude Code 最常用的扩展点

Anthropic 在文章中明确指出：

> "Skills have become one of the most used extension points in Claude Code."

这不是一个随意的评价。这意味着 Skills 机制的设计是成功的——它足够灵活（容易做、容易分发），同时又足够结构化（SKILL.md 格式统一，支持跨工具）。

**从工程角度的理解**：成功的扩展机制需要平衡两个维度——**准入门槛**（不能太难做）和**产出质量**（不能太水）。Skills 做到了前者，但质量控制交给了社区和市场机制，而非中央审查。

---

## 经验 6：Skills 的「有机发现」模式优于「中央审批」

Anthropic 内部的 Skills 分发机制：
1. 工程师创建 Skill → 上传到 GitHub 沙箱文件夹 → 在 Slack 分享链接
2. 其他工程师试用 → 觉得有用就保留，觉得没用就忽略
3. 真正有用的 Skills 会自然传播，不需要推广

**笔者认为**：这种模式的核心洞察是——**「有用」是一个社会现象，不是一个技术判断**。中央审批机构无法预测哪些 Skills 会在实践中被真正使用，而有机发现让市场来筛选。

这与开源软件的「fork and pull request」模式是同一逻辑——好的东西自然会被人发现和传播。

---

## 经验 7：Skill 的核心价值是「推着 Agent 走出默认路径」

综合所有经验，Anthropic 的 Skills 哲学可以提炼为一句话：

> **好的 Skill 不是告诉 Agent 更多它已经知道的事，而是修正它的默认行为模式。**

这个洞察的工程含义：
- 不要在 Skill 里写「如何遍历数组」——Claude 本来就会
- 要在 Skill 里写「这个领域有哪些常见的错误模式需要避免」
- 要在 Skill 里写「这个领域有哪些非显而易见的好资源/工具」

---

## 经验 8：Skills 的分发需要「低摩擦」

从有机发现到广泛使用，Anthropic 发现最大的阻力是**安装摩擦**。为此他们设计了：
- `/plugin marketplace add` 命令一行安装市场
- `/plugin install <name>@claude-code-skills` 安装具体 Skill
- 跨工具格式自动转换（同一份 SKILL.md 适配 13+ 种 AI 编码工具）

**工程教训**：再好的工具，如果安装过程超过 30 秒，就会失去大量潜在用户。Skills 的分发设计是它成功的关键基础设施之一。

---

## 笔者的工程总结

Anthropic 的 Skills 经验揭示了一个更大的主题——**Agent 的可扩展性设计**。好的扩展机制不是「堆功能」，而是：

1. **修正默认行为** > 补充额外知识
2. **有机发现** > 中央审批
3. **低摩擦分发** > 强流程安装
4. **负样本工程**（Gotchas）> 正样本堆砌

这些原则不仅适用于 Skills，对整个 Agent 工程领域都有参考价值。

---

## 相关资源

- 原文：https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
- Anthropic Agent Skills 官方文档：https://claude.com/blog/skills
- SKILL.md 开放标准：https://agentskills.io