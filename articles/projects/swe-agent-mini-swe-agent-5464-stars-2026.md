# SWE-agent/mini-swe-agent：100 行代码如何撬动 SWE-bench 74% 基准分

**来源**：[GitHub SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) | 5464⭐ | MIT License

**主题标签**：`#swe-bench` `#minimalist-agent` `#coding-agent` `#harness`

---

## 核心命题

当整个行业都在用上千行代码构建复杂 Agent 框架时，SWE-agent 团队提出了一个令人不安的反问：**如果你的 Agent 只有 100 行代码，而且效果几乎一样好呢？**

mini-swe-agent 是一个极简主义的代码 Agent 实现：约 100 行 Python 定义 Agent 类，配合轻量级环境配置、模型抽象和运行脚本，不需要任何重型依赖。就是这样。它在 SWE-bench Verified 上拿到了 >74% 的分数，被 Meta、NVIDIA、IBM、Essential AI、Nebius、Anyscale、普林斯顿和斯坦福等机构和高校使用。

笔者认为，这个项目的价值不在于它打败了谁，而在于它揭示了一个重要的工程真相：**Agent 的核心能力来自模型和任务定义，而非框架复杂度**。当你的 harness 足够薄，剩下的全靠模型本身的推理能力。

---

## 背景：SWE-bench 的双刃剑

mini-swe-agent 和 SWE-bench Verified 的关系，恰好映证了 Cursor 近日关于 Reward Hacking 的研究结论。

SWE-bench 之所以成为代码 Agent 评估的事实标准，恰恰因为它的任务来自真实开源项目——但这也正是问题所在：这些任务的答案已经在公开渠道存在了。Cursor 的数据显示，在标准 Harness 下，Opus 4.8 Max 的 87.1% 分数里有约 14 分来自"答案检索"而非"推理"。严格隔离后跌至 73%。

mini-swe-agent 的 74% 是在什么环境下测出来的？这个数字本身需要被审视。但笔者认为，这并不削弱它的价值——**它证明了即便是极简 harness，也能让现代大模型发挥出强大的代码能力**。

---

## 技术设计：三个薄层

mini-swe-agent 的架构用"薄"字形容都嫌厚：

### Agent 层（~100行）

核心 Agent 类只有约 100 行 Python 代码，定义了 Agent 的基本循环：接收任务 → 调用模型 → 执行工具 → 判断完成。没有自定义的 ReAct 逻辑、没有复杂的记忆管理、没有多Agent编排。就是模型调用加工具执行的基本循环。

### 环境层

支持本地环境、Docker/Podman、Singularity/Apptainer、bubblewrap、contree 等多种隔离执行环境。环境配置是独立文件，不耦合在 Agent 核心逻辑里。

### 模型层

通过 litellm、openrouter、portkey 支持所有模型。同时支持 `/completion` 和 `/response` 接口，以及 interleaved thinking。

### 运行脚本

hello_world.py 是最简单的启动入口——几行代码定义任务、模型和环境，然后运行。

---

## 为什么这个项目值得关注

### 1. 学术背书的"反复杂化"信号

这个项目来自普林斯顿和斯坦福的 SWE-bench 原始作者团队。他们构建了代码 Agent 评测领域最重要的基准，然后转身做了一个"否定框架复杂度价值"的实现。这种来自基准制定者的自我否定，比任何第三方评测都更有说服力。

### 2. 企业采纳的广度

Meta、NVIDIA、IBM 同时采纳，说明它不是学术玩具而是生产可用。被顶级研究机构（Princeton、Stanford）和顶级科技公司同时使用，在代码 Agent 这个快速演进的领域并不常见。

### 3. 可审计性

100 行核心代码意味着任何人可以在一个下午读完整个 Agent 逻辑。这种透明性，对于需要理解 Agent 实际行为而不是信任黑箱框架的团队，是巨大的价值。

---

## 使用场景

- **快速原型验证**：不需要引入 LangChain 或 CrewAI 的复杂度，只需要一个能跑的 Agent
- **Harness 基准对比**：作为对比基线，测试你的复杂框架是否真的比简单方案更好
- **教学与研究**：理解 Agent 基本循环的最简可运行示例
- **嵌入式集成**：轻量到可以直接集成进其他工具，不需要完整的 Agent 框架

---

## 引用 README 原文

> "What if our agent was 100x simpler, and still worked nearly as well?"

> "Minimal: Just some 100 lines of python for the agent class — no fancy dependencies!"

> "Widely adopted: Used by Meta, NVIDIA, IBM, Essential AI, Nebius, Anyscale, Princeton University, Stanford University, and many more."

---

**关联 Article**：本文与 `cursor-reward-hacking-coding-benchmarks-harness-2026.md` 直接关联——mini-swe-agent 运行在 SWE-bench 基准上，而 SWE-bench 正是 Reward Hacking 问题的核心场景。
