# Piebald-AI/claude-code-system-prompts：当你的 Agent 行为完全透明

> 官方来源：GitHub [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)，Stars: 11,246（2026年6月），MIT License

---

## 核心命题

这个项目解决了一个长期以来让 Agent 开发者困惑的问题：**Claude Code 内部的 system prompt 到底是什么？它有多少个？每个占多少 token？**

笔者的判断是，理解 Claude Code 的 system prompt 是理解那"七层行为引导机制"的基础设施——当你不知道 Claude Code 内部是如何组织这些层的，你就只能在黑盒外面调 prompt，无法真正驾驭它的行为。

---

## 这个项目解决什么问题

Claude Code 不是一个单一 system prompt 的 Agent。官方文档明确指出，它的内部由**500+ 个独立字符串**构成：

- 根据环境和配置条件性加载的片段
- 内置工具的描述（如 `Write`、`Bash`、`TodoWrite`）
- 内置 Agent 的独立 system prompt（如 Explore、Plan）
- AI 驱动的工具函数，各自拥有独立 prompt（如会话压缩、`CLAUDE.md` 生成）

> "500+ strings that are constantly changing and moving within a very large minified JS file."

这个项目做的事情很简单：**从 Claude Code 的 npm 包里提取所有这些字符串，按版本归档，并计算每个 prompt 的 token 数量。** 作为结果，你可以在几分钟内了解任意版本 Claude Code 的完整 prompt 清单。

笔者认为这个价值在于**透明度**——当你知道 Claude Code 默认的 tool description 是什么、你才能判断你的 custom skills 是否与它冲突；当你知道 Explore agent 的 system prompt 是什么，你才能设计出与之互补的 subagent 策略。

---

## 核心数据（2026年6月快照）

| 指标 | 数值 |
|------|------|
| **System Prompt 总数** | 515 个（截至 v2.1.185，June 20 2026） |
| **版本覆盖** | 215 个 Claude Code 版本（从 v2.0.14 起） |
| **更新频率** | 每个 Claude Code 版本发布后几分钟内同步 |
| **Stars** | 11,246 |
| **维护方** | Piebald AI（同名 AI Developer Experience 产品团队）|

从 350 到 515 个 prompts 的增长（2026年6月12日），说明 Claude Code 在快速扩展其内置能力和 Agent 类型——这是一个活跃开发的信号，而不是一个稳定的工具。

---

## 实际应用场景

### 场景一：诊断 Agent 行为偏差

当你发现 Claude Code 在某个场景下行为异常（比如总是询问确认而不是直接执行），可以通过对比该版本的所有 system prompt，找出是哪个默认 prompt 在起作用。Reddit 上有用户报告：

> "With the default prompt Claude would constantly ask for confirmation and explain its reasoning before doing anything. After customizing, it just..."

这说明 Claude Code 的默认 system prompt 是偏向保守的——这与它作为 AI Coding 工具的产品定位有关。用户需要理解这一点才能做出有针对性的定制。

### 场景二：优化 Token 用量

每个 prompt 的 token 计数是公开的。这意味着你可以精确计算出 Claude Code 在特定任务中消耗在 system context 上的 token 数量。对于 context window 敏感的复杂任务，这是一个重要的优化依据。

### 场景三：与自定义 Skills 的边界划分

当你编写一个 custom skill 时，了解 Claude Code 内置工具的 prompt 描述，可以帮助你判断：
- Skill 的描述是否与内置工具描述产生混淆
- Skill 的行为是否被某个系统 prompt 隐式覆盖
- Claude Code 如何在不同条件下选择加载或不加载某个 skill

---

## tweakcc：修改 System Prompt 的工具

这个项目维护者同时提供了配套工具 **[tweakcc](https://github.com/Piebald-AI/tweakcc)**，专门用于实际修改 Claude Code 的 system prompt。它的设计思路非常务实：

1. 将 Claude Code 的 system prompt 提取为独立的 markdown 文件
2. 让你对这些文件进行自定义修改
3. 将修改 patch 回 npm 安装的 Claude Code 或原生二进制版本
4. 提供 diffing 和冲突管理功能——当 Anthropic 也更新了同一个文件时，能看到冲突并解决

笔者认为这个工具的存在说明了一个重要的事实：**对 system prompt 的定制是一个持续性操作，而不是一次性的。** Claude Code 频繁更新（覆盖 215 个版本），每次更新都可能改变内置 prompt 的内容。如果你的团队依赖对 Agent 行为的精确控制，就需要类似 tweakcc 的工具来管理这个持续变化的过程。

---

## 为什么这个项目值得关注

| 维度 | 评价 |
|------|------|
| **工程稀缺性** | 高——目前没有其他公开项目完整追踪 Claude Code 的 system prompt 变化 |
| **实用性** | 高——对于需要深度定制 Claude Code 行为的团队，这是基础设施级别的资源 |
| **时效性** | 高——每版本更新，覆盖最新版本 |
| **关联性** | 强——与本轮 Article 1（Claude Code 七种行为引导方法论）直接相关 |

---

## 笔者的判断

这是一个典型的**"黑盒变灰盒"**项目。它的价值不是让你去修改 Claude Code 的 system prompt（那往往是个糟糕的主意），而是让你**理解 Claude Code 为什么会以某种方式行为**。

笔者认为，在 Agent 工程走向成熟的阶段，这种透明度项目的重要性不亚于更好的工具框架。当我们对 Agent 的内部机制理解得越深，我们就越能做出有针对性的设计决策——比如，决定把某个行为规则放在 CLAUDE.md 层，还是用 Hook 拦截，还是写成一个 custom skill。

理解 Claude Code 的 system prompt，是做出这个决策的知识前提。

---

**Stars**: 11,246 | **License**: MIT | **更新频率**: 每 Claude Code 版本发布后数分钟内
