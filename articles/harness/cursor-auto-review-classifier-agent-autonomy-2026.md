# Cursor Auto-review：把安全变成刻度盘，而非开关

> 原文：[Governing agent autonomy with Auto-review](https://cursor.com/blog/agent-autonomy-auto-review) (Cursor Engineering Blog, Jun 11, 2026)

---

## 核心问题：Agent 自主性越高，安全风险越大

Cursor 团队遇到了一个所有 AI Coding 工具都会面对的张力：**Agent 越自主，生产力越高；但自主性越高，误操作的风险也越大。**

这个张力的极端解法是"每次操作前都问用户"。但Cursor团队发现，一旦用户被反复询问，他们就会停止仔细阅读——approval flow 变成了一个毫无意义的过场。

> "Asking for permission too often creates its own safety problem. After enough repeated prompts, people stop reading carefully." — Cursor Engineering

这个矛盾的本质是：**我们把"安全"和"自主"当成二元对立的开关，而不是一个连续的光谱。**

---

## Auto-review 的核心思路

Auto-review 的答案是**一个上下文敏感的分类器 Agent**，在每次工具调用执行前判断风险等级：

- **低风险** → 直接放行，Agent 继续自主工作
- **高风险** → 拦截，返回解释，让 Agent 自行调整路径

关键设计原则：**Block 不等于用户中断**。分类器拦截后返回的是反馈（feedback），Agent 可以根据反馈选择更安全的路径，而不必惊动用户。

这个思路把安全机制从"批准开关"变成了**"梯度决策 + 反馈循环"**。

---

## 分类器设计：三处关键工程决策

### 决策一：小模型反而更快

直觉上我们会认为，用最强的模型做安全判断最靠谱。但 Cursor 团队发现这是个误区：

> "Lower-reasoning models were not always faster. When a Model struggled to understand the policy or the tool call, it could spend more time and tokens searching for what ultimately became a worse answer."

当模型推理能力不足时，它会花更多 token 去"猜"一个本该直接拒绝/放行的答案。Cursor 最终选择的是一个**推理能力足够但体型更小的模型**，核心诉求是"快且准"——因为这个分类器直接坐落在 Agent 执行路径上，每一次工具调用都要经过它。

### 决策二：分类器本身是 Agentic 的

有些工具调用的风险无法从命令本身判断。比如 `python script.py` 是安全还是危险，取决于脚本内容是什么。

所以这个分类器**可以调用工具**来检查上下文：
> "The classifier can inspect the workspace with tools like ReadFile, Grep, Glob, and ListDir before deciding."

这是一个很反直觉的设计——安全分类器不是静态规则，而是一个有工具调用能力的小 Agent。这让它能做 context-aware 的判断，而不只是做命令级别的 pattern matching。

### 决策三：避免额外的网络往返

如果分类器是独立的微服务，每次判断都要多一次网络往返，直接加在每次工具调用前面。Cursor 选择让分类器**运行在父 Agent 同一个 RPC stream 里**：

> "We avoided a separate classification endpoint, because an extra round trip would add latency directly before every reviewed tool call."

架构上类似 Subagent 的实现方式，但共享 stream，避免了额外的网络延迟。这是典型的工程取舍：为了性能，放弃了架构上的清晰分离。

---

## 反馈循环设计：Block 不是终点，是调整的起点

如果分类器只是返回"阻止"，那它就变成了另一个 approval prompt——和"每次都问用户"没有本质区别。

Auto-review 的关键设计是：**当分类器阻止一个动作，它返回的是解释（explanation），而不是一个用户 prompt。**

父 Agent 收到解释后，可以选择：
- **窄化操作**：比如原本要删除整个目录，改为只删除某个文件
- **换工具**：原本要用 shell，改为用更安全的 API 包装
- **跳过步骤**：直接放弃这个操作

这让大多数 block 变成了 Agent 的**自我修正机会**，而不是用户中断。

### 真实数据

Cursor 给了两个数字来说明效果：

| 指标 | 数值 |
|------|------|
| 被分类器审查的动作比例 | ~4% |
| 导致用户中断的聊天比例 | ~7% |
| 某企业客户之前（无 Auto-review）的 block 率 | ~40% |

关键在于：**7% 是全局聊天中断率，而不是工具调用 block 率**。大多数 block 被 Agent 自行吸收并调整了。

---

## Eval 方法：如何在安全性和流畅性之间找到平衡点

分类器最难调的点不是"能catch住危险操作"，而是**不能误伤正常开发工作**。

Cursor 的 eval 分两部分：

### 内部数据构建

> "We started with roughly 12 hours of internal developer sessions, then cut that down and deduplicated common actions into 6,122 labeled rows."

6,122 行标签数据代表了"正常开发工作的 baseline"。分类器必须能放行这些操作。

### 综合数据（Synthetic Data）

正常数据覆盖不了极端情况：
> "We generated cases where the agent might read secrets, touch production data, follow untrusted instructions, or take actions with large side effects."

这些低频高损的场景必须被单独覆盖。

### Policy 迭代带来的复杂度

Cursor 特别提到一件事：当 policy 本身发生变化时，之前的 eval 数据可能就过时了——你需要重新标注或重新生成。

> "When we changed the categories of behavior the classifier should recognize, we had to relabel or rematerialize the eval set."

这对所有基于 ML 的安全系统都是个普遍问题：**安全策略的迭代速度必须和模型评估数据的更新速度匹配**。

### 稳定性测试（Flapping Detection）

> "If the same case allowed six times and blocked four times, that usually meant the policy or prompt was underspecified."

重复运行同一case多次，检查行为是否稳定。这是一个容易被忽视但很重要的测试维度——分类器在边界情况下的不稳定性比一致性偏差更危险。

---

## 工程意义：从二元开关到梯度决策

Auto-review 的核心贡献不是"一个做得很准的分类器"，而是**重新定义了 Agent 安全的思维模型**：

| 旧范式 | Auto-review 范式 |
|--------|----------------|
| 全局开关（开/关） | 刻度盘（梯度） |
| 每次操作前批准 | 上下文敏感的分类器 |
| Block = 用户中断 | Block = 父 Agent 的反馈信号 |
| 静态规则 | Agentic 的上下文判断 |
| 单点延迟（每次都问） | 极低比例审查（~4%） |

这种思路和 Anthropic 的 **Classifier-based Permission Control**（Claude Code auto mode）以及 **Harness Design for Long-Running Apps** 中的 GAN-inspired 三角色架构有类似的工程直觉：**把安全判断从人的审批变成系统的梯度决策**。

笔者认为，这条路比"让用户每次都批准"更可持续——因为它解决的不是单次操作的风险，而是**整个 Agent 运行的信任模型问题**。

---

## 引用

> "We want agents to have real autonomy, while making the decision to slow them down depend on context rather than a single global permission setting." — Cursor Engineering

> "The classifier rarely interrupts the user directly, and in most blocked cases the parent agent can use the feedback to continue in a safer, narrower way." — Cursor Engineering
