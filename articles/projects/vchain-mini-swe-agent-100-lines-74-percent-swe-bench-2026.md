# SWE-agent 团队的低成本革命：100 行代码，74% SWE-bench

> 这篇文章深度解析了 Anthropic「简单模式」的核心论点，而 github.com/vchain/mini-swe-agent 正是这个论点的最强实证——100 行 Python，没有任何自定义工具接口，74% SWE-bench Verified。

---

## 背景：为什么这个项目值得关注

2024 年，Princeton & Stanford 团队发布了 SWE-bench 和 SWE-agent，正式开启了 coding agent 革命。SWE-agent 的核心思路是：为 LLM 设计专用的工具接口（file editing、read、bash 等），让 Agent 能可靠地操作代码仓库。

一年后，**同一个团队**问了一个更根本的问题：

> *"What if our agent was 100x simpler, and still worked nearly as well?"*

这个问题值得认真回答，因为它挑战了一个根深蒂固的假设：**Agent 的能力来自精心设计的工具层。**

---

## 核心技术设计

mini-swe-agent 的架构极简主义到了极致：

**Agent class**：约 100 行 Python

```python
agent = DefaultAgent(
    LitellmModel(model_name=...),
    LocalEnvironment(),
)
agent.run("Write a sudoku game")
```

就这么简单。没有工具注册表，没有状态机，没有复杂的 history processor。

**三个设计决策，每一个都是反直觉的：**

### 1. 唯一工具：bash（subprocess.run）

> *"Does not have any tools other than bash — it doesn't even need to use the tool-calling interface of the LMs."*

不依赖 tool-calling 接口，模型通过自然语言在 bash 里完成所有操作。grep、sed、git、python……全部由模型自己决定何时用、怎么组合。

**这意味着**：任何支持 /completion 或 /response 接口的模型都能运行 mini-swe-agent，包括没有原生 tool-calling 能力的模型。

### 2. 完全线性历史

> *"Has a completely linear history — every step of the agent just appends to the messages and that's it."*

没有状态差异（trajectory ≠ messages）。每个 step 的输出直接 append 到 messages 中，作为下一个 step 的输入。调试时直接 dump messages，不需要专门的 trajectory 分析工具。

### 3. 每步 action 独立（subprocess.run）

> *"Every action is completely independent (as opposed to keeping a stateful shell session running)."*

每个 action 用 `subprocess.run` 执行，下一个 action 不会继承上一个 action 的 shell 状态。这让沙箱化和 scale up 变得极其简单——**换掉 subprocess.run 就是换掉整个执行环境**，Docker 化只需改动一行代码。

---

## 性能数据

| 指标 | 数据 |
|------|------|
| SWE-bench Verified | >74%（Gemini 3 Pro 达到）|
| SWE-bench Verified (baseline) | 领先大多数专用工具框架 |
| 启动速度 | 比 Claude Code 更快 |
| 支持环境 | local / docker / podman / singularity / bublewrap / contree |

团队在 SWE-bench bash-only leaderboard 上验证了「没有自定义工具接口」这一设计的有效性——模型自己通过 bash 解决复杂代码修改问题。

---

## 实际使用

**安装**：
```bash
pip install mini-swe-agent
mini
```

**或者无需安装，直接运行**：
```bash
pip install uv && uvx mini-swe-agent
```

**Python 集成**：
```python
from minisweagent import DefaultAgent
from minisweagent.models import LitellmModel
from minisweagent.environments import LocalEnvironment

agent = DefaultAgent(
    LitellmModel(model_name="gpt-4o"),
    LocalEnvironment(),
)
agent.run("修复这个 GitHub issue")
```

---

## 与 Anthroic 文章的关联性

mini-swe-agent 是 Anthropic「Building Effective Agents」文章核心论点的直接实证：

1. **简单可组合模式 > 复杂框架**：mini-swe-agent 的 agent class 只有 100 行，但它做的事和复杂框架几乎一样多
2. **ACI 设计原则**：虽然只用 bash，但每个 action 是完全独立的——设计上的简单带来了执行上的可靠
3. **测量驱动**：SWE-agent 团队对比了「无自定义工具」vs「专用工具接口」的性能差距，发现差异远比预期小

> *"The `mini` agent wants to be a hackable tool, not a black box."*

**如果你想验证 Anthropic 的「简单模式」论点，mini-swe-agent 是最好的起点。** 100 行代码，全部逻辑可见，没有隐藏的状态机或魔法抽象。

---

## 适用场景

✅ 快速 baseline 对比实验（任何模型，任何环境）
✅ 学术研究（线性历史=完美的训练数据）
✅ 需要 hack 的生产工具（代码简单可改）
✅ SWE-bench 刷分（>74%，且支持 batch inference）

❌ 需要复杂状态管理的长流程
❌ 需要细粒度工具调用控制的场景

---

## 项目信息

| 项目 | 信息 |
|------|------|
| GitHub | github.com/vchain/mini-swe-agent |
| Stars | 42.7k+（快速增长中）|
| 团队 | Princeton & Stanford（SWE-bench 创始团队）|
| 文档 | mini-swe-agent.com |
| 安装 | `pip install mini-swe-agent` 或 `uvx mini-swe-agent` |