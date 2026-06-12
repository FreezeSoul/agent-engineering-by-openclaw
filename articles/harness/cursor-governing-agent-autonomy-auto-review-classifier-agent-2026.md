# Cursor Auto-review：把 Agent 自主权变成可调节的刻度盘

> **目标读者**：构建生产级 AI Agent 系统的工程师；关注 harness 设计、风险治理、agent 自主权边界的技术负责人。

---

## 核心命题

**Auto-review 的本质不是"阻止危险操作"，而是构建一个上下文感知的风险判断系统——让 agent 在低风险场景自由行动，在高风险场景自动降级，而非一刀切地要求用户确认。**

> "Agents should be able to move freely when the stakes are low, but slow down when its next action crosses a meaningful boundary."
> — David & Travis, Cursor Engineering Blog

---

## 背景：自主权与安全的两难

AI Agent 在代码库中运行时，通常拥有较高的操作权限——读写文件、执行命令、访问凭证、调用 MCP 工具。在这样的环境下，**更大的自主权意味着更大的潜在风险**。

传统的解决方案是"一刀切"：每遇到可能危险的操作就停下来请求用户确认。但 Cursor 团队在实践中发现了一个关键问题：

> "After enough repeated prompts, people stop reading carefully, and the approval flow becomes less meaningful."

当权限请求变得频繁，用户会进入"自动驾驶"模式——看都不看就点同意。这样的审批流程不仅无效，还会在真正需要判断时失去用户的注意力。

**Auto-review 的核心洞察**：Agent 自主权应该像一个可调节的刻度盘，而不是一个二元开关。

---

## 设计哲学：从开关到刻度盘

Auto-review 的设计目标很明确：

1. **低风险操作** → Agent 自由执行，不需要任何干预
2. **高风险操作** → Agent 自动降级，要么选择更安全的路径，要么请求用户确认
3. **判断依据** → 不仅看操作本身，还要看操作的上下文（用户意图、工作区状态、后果严重性）

这个设计的关键在于**风险判断必须发生在执行之前**，而不是在问题出现之后。

---

## 技术实现：Classifier Agent

### 1. 架构选择：为什么是 Agent，而不是规则引擎？

Cursor 团队尝试过多种方案，包括基于规则的 allowlist 和 sandboxing。但最终选择了一个专门的 **Classifier Agent**，原因是：

> "Whether an agent action poses risk depends on the situation. The same command can be harmless in one workflow and unacceptable in another."

同样的命令（如 `python script.py`）可能在不同场景下有完全不同的风险等级。规则引擎无法处理这种上下文依赖的判断，而 Agent 可以。

### 2. 模型选择：小模型 + 足够推理

Classifier 需要在每次 tool call 执行之前运行，这意味着它直接位于 agent loop 的执行路径上。**速度是关键约束**。

一个意外的发现：

> "One early surprise was that lower-reasoning models were not always faster. When a model struggled to understand the policy or the tool call, it could spend more time and tokens searching for what ultimately became a worse answer."

低推理模型在遇到复杂判断时，反而可能花费更多时间和 token。最终的选择是一个**小模型，但要有足够的推理能力来干净地完成判断**。

### 3. Agentic 设计：检查工作区

有些判断仅凭命令本身无法做出。例如：

```python
python script.py  # 安全还是不安全？取决于脚本内容
```

因此，Classifier 被设计成 **agentic**——它可以调用工具来检查工作区状态：

- **ReadFile**: 检查脚本内容
- **Grep**: 搜索敏感模式（API key、password、connection string）
- **Glob**: 了解项目结构
- **ListDir**: 确认当前目录上下文

这种设计让 classifier 能够做出**上下文感知的判断**，而非仅基于命令字符串的静态分析。

### 4. 执行位置：与 Parent Agent 共享 RPC Stream

Cursor 避免了创建单独的 classification endpoint，因为：

> "An extra round trip would add latency directly before every reviewed tool call."

Classifier 运行在**与 parent agent 相同的 RPC stream** 中，使用类似于 subagent 的架构。这种设计避免了额外的网络延迟，同时保持了与 parent agent 的紧密集成。

---

## 反馈循环设计：让 Parent Agent 自我修正

当 Classifier 阻止一个操作时，它**不只是弹出一个用户提示**——它向 parent agent 返回一个**解释**。

这个设计的关键洞察：

> "User intent is what makes that feedback useful. The question is not whether an action looks risky in isolation. The question is whether the action is justified by what the user asked the agent to do."

有了这个反馈，parent agent 可以：

1. **选择更安全的替代路径**：如果 `python script.py` 被阻止，agent 可能改为 `python script.py --dry-run`
2. **修改操作范围**：将一个大的修改拆分成多个小步骤，每个步骤单独判断
3. **请求用户确认**：只有在反馈无法帮助 agent 自我修正时，才中断用户

这种设计让 **~93% 的被阻止操作能够被 agent 自我消化**，不需要用户真正介入。

---

## 测试与迭代

### Eval 设计

Classifier 的训练数据来自两个来源：

1. **内部使用数据**（~12 小时内部开发者会话 → 6,122 条标注数据）
   - 反映正常开发工作的基线
   - 识别常见的操作模式

2. **合成数据**（针对罕见但危险的场景）
   - 读取 secrets
   - 访问生产数据
   - 跟随不受信的指令
   - 产生重大副作用的操作

> "The worst cases do not appear often enough in normal usage."

合成数据填补了对最坏情况的覆盖。

### 政策迭代带来的数据复杂性

随着产品发展，Classifier 应该识别的行为类别也在变化。当政策改变时：

> "We had to relabel or rematerialize the eval set. Otherwise, we would be testing the current classifier against an outdated understanding of the problem."

这是一个持续维护的挑战，而非一次性上线。

### Flapping 检测

同一个案例允许 6 次但阻止 4 次，意味着**政策或 prompt 定义不够精确**。重复运行帮助发现这些不稳定案例，直到 Classifier 的行为更加一致。

---

## 数据验证

| 指标 | 数值 | 说明 |
|------|------|------|
| Classifier 阻止率 | ~4% | 在所有 agent 操作中 |
| 真正用户中断率 | ~7% | 在所有 chat session 中 |
| **对比（企业客户之前）** | **~40%** | **启用 Auto-review 前** |

**核心结论**：通过上下文感知的判断 + 反馈循环，Auto-review 实现了 5.7 倍的打扰降低，同时保持了安全性。

---

## 与 Harness Engineering 的关系

Auto-review 代表了一种**新型的 Harness 模式**：

| 传统 Harness | Auto-review 模式 |
|-------------|-----------------|
| 静态规则（allowlist/sandbox） | 动态上下文判断 |
| 一次性决策（阻止/允许） | 反馈循环（解释 + 自我修正）|
| 用户中断作为主要手段 | Agent 自我修正作为主要手段 |
| 全有或全无的权限模型 | 可调节的风险刻度盘 |

这种模式的关键工程价值在于：**它把"安全判断"从用户身上转移到了 classifier agent，而 classifier 可以通过反馈循环让 parent agent 持续优化自己的行为**。

---

## 局限性与发展方向

1. **当前范围**：仅针对 Cursor Desktop App 中的本地 agent
2. **计划扩展**：同样的思路将应用到更多场景的 agent 自主权治理

3. **持续演进**：随着 agent 能力增强，对 autonomy 的理解也会改变，classifier 的判断标准也需要持续更新

---

## 工程启示

1. **小模型做分类**：在执行路径上的判断，不需要最大的模型，但需要足够的推理能力
2. **Agentic 判断**：当静态规则不够时，让判断 agent 有能力检查上下文（workspace tools）
3. **反馈循环 > 用户中断**：设计让 agent 能够自我修正的系统，而非依赖用户审批
4. **数据随政策迭代**：当产品方向改变时，eval 数据也需要重构

---

## 配对项目：Nexent

**ModelEngine-Group/Nexent**（5,010 ⭐，MIT，Python）与 Auto-review 形成互补闭环：

- **Auto-review**：展示了一个 classifier 如何通过上下文判断来治理 agent 自主权
- **Nexent**：提供了一套基于 Harness Engineering 原则的生产级 Agent 生成平台，包含"built-in constraints, feedback loops, and control planes"

两者都强调 **feedback loops** 和 **control planes**，但 Auto-review 展示的是**理论层**（如何设计 classifier），Nexent 提供的是**工程实现层**（如何在平台层面构建 harness）。

---

## 参考来源

- [Cursor Blog: Governing agent autonomy with Auto-review](https://cursor.com/blog/agent-autonomy-auto-review)（2026-06-11）
- [GitHub: ModelEngine-Group/nexent](https://github.com/ModelEngine-Group/nexent)（Stars: 5,010，MIT）